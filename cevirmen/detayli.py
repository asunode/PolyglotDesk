"""Detaylı Çevir: bilgi paketiyle çeviri + denetim geçişi.

Her parça için üç aşama:
1. Bilgi aranıyor: PostgreSQL bilgi paketinde arama (ayrı iş parçacığında; arayüz donmaz).
2. Çevriliyor: ortak istem + terimler + bulunan kayıtlarla çeviri (akış hâlinde ekrana gelir).
3. Denetleniyor: kod denetimi (boş satır, kalın/italik ve yeri, satır yapısı) + model kaynakla taslağı
   karşılaştırıp JSON ile karar verir ("hata yok" ya da hata listesi). Kararı kod uygular
   (`denetim.py`): hata yoksa taslak olduğu gibi kalır; güvenli olmayan düzeltmeler geri alınır.
   Kalın yazı: olumsuzlukta önce kod yerleştirir (`bicim.kalin_kodla`); yine sorun varsa modelin "bold"
   listesindeki taslaktan birebir parçalara `**` işaretlerini kod koyar (`bicim.kalin_uygula`).
"""

import threading
import time
from dataclasses import dataclass, field

from PySide6.QtCore import QObject, Signal

from . import bicim, bilgi, denetim
from .bicim import bos_satirlari_duzelt, denetle
from .istem import DENETIM_SEMASI, denetim_istemi, denetim_mesaji, detayli_istem
from .ollama import Ollama
from .parcala import parcala
from .sozluk import Sozluk
from .temizle import temizle

ASAMALAR = {"arama": "bilgi aranıyor", "ceviri": "çevriliyor", "denetim": "denetleniyor"}


@dataclass
class ParcaSonucu:
    kaynak: str
    taslak: str = ""
    son: str = ""
    sorunlar_once: list[str] = field(default_factory=list)   # denetimden önce kodla bulunan
    sorunlar_sonra: list[str] = field(default_factory=list)  # denetimden sonra kalan
    karar: dict | str | None = None                           # denetimin JSON kararı
    uygulanan: list[dict] = field(default_factory=list)
    geri_alinan: list[dict] = field(default_factory=list)     # güvenlik kontrolünün geri aldıkları
    uygulanmayan: list[dict] = field(default_factory=list)    # taslakta bulunamayan vb.
    kalin: list[str] = field(default_factory=list)            # kalın yazı düzeltmesinin kaydı
    kayitlar: list = field(default_factory=list)
    sure: dict = field(default_factory=dict)                 # aşama → saniye


class DetayliCevirici(QObject):
    asama = Signal(str, int, int)        # aşama kodu, parça sırası (1'den), parça sayısı
    guncellendi = Signal(str)
    bilgiler = Signal(list)              # şimdiye kadar modele giden tüm kayıtlar
    bitti = Signal()
    hata = Signal(str)
    _arama_bitti = Signal(int, object)   # iş parçacığından ana iş parçacığına

    def __init__(self, ollama: Ollama, sozluk: Sozluk, parent=None):
        super().__init__(parent)
        self.ollama = ollama
        self.sozluk = sozluk
        self._akis = None
        self._kusak = 0                  # her başlat/durdur'da artar; eski sonuçlar yok sayılır
        self._arama_bitti.connect(self._aranan_geldi)
        self.sonuclar: list[ParcaSonucu | None] = []
        self.ilk_parca_suresi: float | None = None
        self.baslangic = 0.0
        self._calisiyor = False

    @property
    def calisiyor(self) -> bool:
        return self._calisiyor

    @property
    def parca_sayisi(self) -> int:
        return sum(p.cevrilsin for p in self._parcalar)

    def baslat(self, metin: str, kaynak: str, hedef: str) -> None:
        self.durdur()
        self.sozluk.guncelle()
        self._kaynak, self._hedef = kaynak, hedef
        self._parcalar = parcala(metin)
        self.sonuclar = [None] * len(self._parcalar)
        self._terimler = self.sozluk.eslesenler(metin, kaynak, hedef)
        self._teknik = self.sozluk.teknik_mi(metin, kaynak)
        self._sozluk_kayitlari = [
            bilgi.Kayit("sozluk", "kullanıcı sözlüğü", "—", str(t),
                        f"{t.kaynak}: keep in English" if t.hedef is None else f"{t.kaynak} → {t.hedef}")
            for t in self._terimler]
        self._sira = 0
        self._ham = ""
        self._gosterilen = ""            # akıştaki taslak (ekranda)
        self.ilk_parca_suresi = None
        self.baslangic = time.monotonic()
        self._calisiyor = True
        self.bilgiler.emit(list(self._sozluk_kayitlari))
        self._sonraki()

    def durdur(self) -> bool:
        calisiyordu = self._calisiyor
        self._kusak += 1
        self._calisiyor = False
        if self._akis is not None:
            self._akis.durdur()
            self._akis = None
        return calisiyordu

    def tum_kayitlar(self) -> list:
        kayitlar = list(self._sozluk_kayitlari)
        for s in self.sonuclar:
            if s:
                kayitlar += s.kayitlar
        return kayitlar

    def metin(self) -> str:
        cikti = []
        for i, parca in enumerate(self._parcalar):
            s = self.sonuclar[i]
            if i < self._sira:
                cikti.append((s.son if s else parca.icerik) + parca.ayrac)
            elif i == self._sira and self._gosterilen:
                cikti.append(self._gosterilen)
                break
            else:
                break
        return "".join(cikti)

    # ------------------------------------------------------------ akış
    def _sonraki(self) -> None:
        while self._sira < len(self._parcalar) and not self._parcalar[self._sira].cevrilsin:
            self._sira += 1
        if self._sira >= len(self._parcalar):
            self._calisiyor = False
            self.guncellendi.emit(self.metin())
            self.bitti.emit()
            return
        parca = self._parcalar[self._sira]
        self.sonuclar[self._sira] = ParcaSonucu(parca.icerik)
        self._gosterilen = ""
        self._asama("arama")
        kusak, sira = self._kusak, self._sira
        self._t0 = time.monotonic()

        def calis():
            try:
                sonuc = bilgi.ara(parca.icerik, self._kaynak, self._hedef, teknik=self._teknik)
            except bilgi.BilgiHatasi as e:
                sonuc = e
            except Exception as e:  # beklenmeyen: arayüze anlaşılır mesaj
                sonuc = bilgi.BilgiHatasi(f"Bilgi araması başarısız: {e}")
            self._arama_bitti.emit(kusak, (sira, sonuc))

        threading.Thread(target=calis, daemon=True).start()

    def _asama(self, kod: str) -> None:
        sira = sum(p.cevrilsin for p in self._parcalar[:self._sira + 1])
        self.asama.emit(kod, sira, self.parca_sayisi)

    def _aranan_geldi(self, kusak: int, veri) -> None:
        sira, sonuc = veri
        if kusak != self._kusak or sira != self._sira:
            return
        s = self.sonuclar[sira]
        s.sure["arama"] = time.monotonic() - self._t0
        if isinstance(sonuc, bilgi.BilgiHatasi):
            self._calisiyor = False
            self.hata.emit(str(sonuc))
            return
        s.kayitlar = sonuc
        self.bilgiler.emit(self.tum_kayitlar())
        self._blok = bilgi.istem_blogu(sonuc)
        mesajlar = [{"role": "system", "content": detayli_istem(self._kaynak, self._hedef, self._terimler, self._blok)},
                    {"role": "user", "content": s.kaynak}]
        self._asama("ceviri")
        self._istek(mesajlar, self._ceviri_bitti, goster=True)

    def _istek(self, mesajlar, bitince, goster: bool, bicim: dict | None = None) -> None:
        self._ham = ""
        self._t0 = time.monotonic()
        self._akis = akis = self.ollama.cevir(mesajlar, bicim)
        akis.parca.connect(lambda p: self._parca_geldi(akis, p, goster))
        akis.bitti.connect(lambda: self._istek_bitti(akis, bitince))
        akis.hata.connect(lambda m: self._istek_hatasi(akis, m))

    def _parca_geldi(self, akis, parca: str, goster: bool) -> None:
        if akis is not self._akis:
            return
        self._ham += parca
        if goster:
            self._gosterilen = temizle(self._ham, self._parcalar[self._sira].icerik, son=False)
            if self._gosterilen.strip() and self.ilk_parca_suresi is None:
                self.ilk_parca_suresi = time.monotonic() - self.baslangic
            self.guncellendi.emit(self.metin())

    def _istek_bitti(self, akis, bitince) -> None:
        if akis is not self._akis:
            return
        self._akis = None
        bitince(self._ham)

    def _istek_hatasi(self, akis, mesaj: str) -> None:
        if akis is not self._akis:
            return
        self._akis = None
        self._calisiyor = False
        self.hata.emit(mesaj)

    def _ceviri_bitti(self, ham: str) -> None:
        s = self.sonuclar[self._sira]
        s.sure["ceviri"] = time.monotonic() - self._t0
        s.taslak = bos_satirlari_duzelt(s.kaynak, temizle(ham, s.kaynak, son=True))
        self._denetlenen = s.taslak
        if bicim.kalin_sorunlari(s.kaynak, s.taslak, self._kaynak, self._hedef):
            kodla = bicim.kalin_kodla(s.kaynak, s.taslak, self._kaynak, self._hedef)
            if kodla:
                self._denetlenen = kodla
                s.kalin.append(f"kod (olumsuzluk sırası), denetimden önce: {kodla}")
        self._gosterilen = self._denetlenen
        self.guncellendi.emit(self.metin())
        s.sorunlar_once = denetle(s.kaynak, self._denetlenen, self._kaynak, self._hedef)
        mesajlar = [{"role": "system", "content": denetim_istemi(self._kaynak, self._hedef, self._terimler, self._blok)},
                    {"role": "user", "content": denetim_mesaji(self._kaynak, self._hedef, s.kaynak, self._denetlenen,
                                                               s.sorunlar_once)}]
        self._asama("denetim")
        self._istek(mesajlar, self._denetim_bitti, goster=False, bicim=DENETIM_SEMASI)

    def _denetim_bitti(self, ham: str) -> None:
        s = self.sonuclar[self._sira]
        izinli = {w for t in self._terimler for y in (t.kaynak, t.hedef or "")
                  for w in denetim._kelimeler(y, "tr") + denetim._kelimeler(y, "en")}
        b = None
        try:
            b = bilgi.baglan()
            kaynak_kelimeleri = bilgi._kelimeler(s.kaynak, self._kaynak)
            islev = {r[0] for r in b.execute("SELECT kelime FROM bilgi.siklik WHERE dil = %s AND sira <= %s",
                                             (self._hedef, bilgi.SIK_KELIME_SIRASI))}
            karsilik = lambda w: bilgi.karsilik_var_mi(b, self._kaynak, kaynak_kelimeleri, w)  # noqa: E731
        except Exception:
            karsilik, islev = None, set()   # veritabanı yoksa karşılık denetimi atlanır
        try:
            u = denetim.uygula(self._denetlenen, s.kaynak, ham, self._kaynak, self._hedef, izinli, karsilik, islev)
        finally:
            if b is not None:
                b.close()
        s.sure["denetim"] = time.monotonic() - self._t0
        s.karar, s.uygulanan, s.geri_alinan, s.uygulanmayan = u.karar, u.uygulanan, u.geri_alinan, u.uygulanmayan
        metin = u.metin
        if bicim.kalin_sorunlari(s.kaynak, metin, self._kaynak, self._hedef):
            parcalar = u.karar.get("bold") if isinstance(u.karar, dict) else None
            yeni, neden = bicim.kalin_uygula(metin, parcalar, s.kaynak, self._kaynak, self._hedef)
            if yeni is None:
                s.kalin.append(f"model parçaları {parcalar!r} uygulanmadı: {neden}")
                yeni = bicim.kalin_kodla(s.kaynak, metin, self._kaynak, self._hedef)
                if yeni:
                    s.kalin.append(f"kod (olumsuzluk sırası), denetimden sonra: {yeni}")
            else:
                s.kalin.append(f"model parçaları {parcalar!r} uygulandı")
            metin = yeni or metin
        s.son = bos_satirlari_duzelt(s.kaynak, metin)
        s.sorunlar_sonra = denetle(s.kaynak, s.son, self._kaynak, self._hedef)
        self._gosterilen = ""
        self._sira += 1
        self.guncellendi.emit(self.metin())
        self._sonraki()
