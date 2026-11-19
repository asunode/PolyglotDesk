"""Parça parça çeviri: sıra ve önbellek.

Metin `parcala` ile bölünür; parçalar sırayla çevrilir, her parça akış hâlinde
ekrana gelir. Çevrilen parçalar önbellekte tutulur: metinde bir yer düzeltilince
yalnız değişen parça yeniden çevrilir. Çeviri sürerken metin düzeltilirse yarıdaki
parça, kendisi değişmediyse kesilmez. Kaynakta olmayan boş satırlar kodla kaldırılır.

Kalın yazı: kod denetimi bir parçada kalın yazının kaybolduğunu ya da olumsuzlukta yanlış yerde olduğunu
bulursa önce kod yerleştirmeyi dener (`bicim.kalin_kodla`); olmazsa kısa bir ek istekle modele yalnız hangi
parçanın kalın olacağı sorulur, `**` işaretlerini kod koyar (`bicim.kalin_uygula`). Sorun yoksa ek istek yapılmaz.

Tutarlılık: Ollama önbelleği başka türden bir istekle (Detaylı, denetim, kalın) değiştiyse hızlı çeviriden önce kısa
bir sınır isteği gönderilir (`Ollama.onbellek_sinirda`); böylece aynı metin her koşulda aynı çeviriyi verir
(doc/olcum/tutarlilik-inceleme.md).

Parçalar arası tutarlılığı, tüm metinden çıkarılan ortak terim listesi ve aynı
sistem istemi sağlar. Önceki parçayı bağlam olarak vermek denendi: Ollama bu
kısmı önbellekten kullanmadığı için her parçaya ~9 sn ekliyordu (Adım 3 ölçümü).
"""

import json
import time

from PySide6.QtCore import QObject, Signal

from . import bicim
from .bicim import bos_satirlari_duzelt
from .istem import KALIN_SEMASI, SURUM, kalin_istemi, kalin_mesaji, sinir_istemi, sistem_istemi
from .ollama import Ollama
from .parcala import Parca, parcala
from .sozluk import Sozluk
from .temizle import temizle


class Cevirici(QObject):
    guncellendi = Signal(str)       # şu ana kadarki çeviri (tam metin)
    ilerleme = Signal(int, int)     # sıradaki parça (1'den), çevrilecek parça sayısı
    bitti = Signal()
    hata = Signal(str)

    def __init__(self, ollama: Ollama, sozluk: Sozluk, parent=None):
        super().__init__(parent)
        self.ollama = ollama
        self.sozluk = sozluk
        self._onbellek: dict[tuple, str] = {}
        self._akis = None
        self._parcalar: list[Parca] = []
        self._ceviriler: list[str | None] = []
        self._sira = 0
        self._ham = ""
        self._anahtarlar: list[tuple | None] = []
        self._akis_anahtar: tuple | None = None   # süren isteğin parçası (önbellek anahtarı)
        self._akis_parca = ""
        self._kalin_taslak: str | None = None     # kalın yazı isteği sürerken parçanın çevirisi
        self._kalin_ham = ""
        # Son çevirinin özeti (durum satırı ve ölçüm için)
        self.istek_sayisi = 0
        self.kalin_istegi = 0
        self.kalin_kaydi: list[str] = []           # kalın yazı düzeltmelerinin kaydı (ölçüm için)
        self.sinir_istegi = 0
        self.onbellekten = 0
        self.ilk_parca_suresi: float | None = None
        self.baslangic = 0.0

    @property
    def calisiyor(self) -> bool:
        return self._akis is not None

    @property
    def parca_sayisi(self) -> int:
        return sum(p.cevrilsin for p in self._parcalar)

    def baslat(self, metin: str, kaynak: str, hedef: str) -> None:
        self.sozluk.guncelle()
        self._kaynak, self._hedef = kaynak, hedef
        self._parcalar = parcala(metin)
        self._anahtarlar = [self._anahtar(p) if p.cevrilsin else None for p in self._parcalar]
        # Yarıdaki parça yeni metinde de varsa kesilmez: bitince önbelleğe girer, sırası gelince kullanılır.
        if self._akis is not None and self._akis_anahtar not in self._anahtarlar:
            self.durdur()
        if self._akis is None:
            self._ham = ""
        self._ceviriler = [None] * len(self._parcalar)
        # Terimler tüm metin için: sistem istemi parçalar arasında aynı kalır.
        terimler = self.sozluk.eslesenler(metin, kaynak, hedef)
        self._sistem = sistem_istemi(kaynak, hedef, terimler)
        self._kalin_sistem = kalin_istemi(kaynak, hedef, terimler)
        self._sira = 0
        self.istek_sayisi = 0
        self.kalin_istegi = 0
        self.kalin_kaydi = []
        self.sinir_istegi = 0
        self.onbellekten = 0
        self.ilk_parca_suresi = None
        self.baslangic = time.monotonic()
        self._ilerle()

    def durdur(self) -> bool:
        if self._akis is None:
            return False
        self._akis.durdur()
        self._akis = None
        self._kalin_taslak = None
        return True

    def metin(self) -> str:
        """Ekrandaki çeviri: tamamlanan parçalar + akıştaki parça."""
        cikti = []
        for i, parca in enumerate(self._parcalar):
            if i < self._sira:
                cikti.append(self._ceviriler[i] + parca.ayrac)
            elif i == self._sira and self._kalin_taslak is not None and self._akis_anahtar == self._anahtarlar[i]:
                cikti.append(self._kalin_taslak)  # çeviri bitti, kalın yazı isteği sürüyor
                break
            elif i == self._sira and self._ham and self._akis_anahtar == self._anahtarlar[i]:
                # Akıştaki ya da durdurulan/yarıda kalan parça
                cikti.append(temizle(self._ham, parca.icerik, son=self._akis is None))
                break
            else:
                break
        return "".join(cikti)

    def _anahtar(self, parca: Parca) -> tuple:
        terimler = tuple(self.sozluk.eslesenler(parca.icerik, self._kaynak, self._hedef))
        return (SURUM, self.ollama.ayarlar["model"], self._kaynak, self._hedef, parca.icerik, terimler)

    def _ilerle(self) -> None:
        while self._sira < len(self._parcalar):
            parca = self._parcalar[self._sira]
            if not parca.cevrilsin:
                self._ceviriler[self._sira] = parca.icerik
                self._sira += 1
                continue
            onbellekte = self._onbellek.get(self._anahtarlar[self._sira])
            if onbellekte is None:
                if self._akis is None:
                    self._istek_gonder(parca, self._anahtarlar[self._sira])
                else:
                    # Önceki metinden kalan istek sürüyor; bitince devam edilir.
                    self._ilerleme_bildir()
                    self.guncellendi.emit(self.metin())
                return
            self._ceviriler[self._sira] = onbellekte
            self.onbellekten += 1
            self._sira += 1
            self._ilk_parca()
        self.guncellendi.emit(self.metin())
        self.bitti.emit()

    def _ilerleme_bildir(self) -> None:
        sira = sum(p.cevrilsin for p in self._parcalar[:self._sira + 1])
        self.ilerleme.emit(sira, self.parca_sayisi)

    def _istek_gonder(self, parca: Parca, anahtar: tuple) -> None:
        self._ham = ""
        self._akis_anahtar, self._akis_parca = anahtar, parca.icerik
        self.istek_sayisi += 1
        if self.ollama.onbellek_sinirda:
            self._ceviri_istegi()
        else:
            self.sinir_istegi += 1
            self._akis = akis = self.ollama.sinir(sinir_istemi())
            akis.bitti.connect(lambda: self._sinir_bitti(akis))
            akis.hata.connect(lambda m: self._parca_hatasi(akis, m))
        self._ilerleme_bildir()
        self.guncellendi.emit(self.metin())

    def _sinir_bitti(self, akis) -> None:
        if akis is not self._akis:
            return
        self._akis = None
        self._ceviri_istegi()

    def _ceviri_istegi(self) -> None:
        mesajlar = [{"role": "system", "content": self._sistem}, {"role": "user", "content": self._akis_parca}]
        self._akis = akis = self.ollama.cevir(mesajlar, hizli=True)
        akis.parca.connect(lambda p: self._parca_geldi(akis, p))
        akis.bitti.connect(lambda: self._parca_bitti(akis))
        akis.hata.connect(lambda m: self._parca_hatasi(akis, m))

    def _ilk_parca(self) -> None:
        if self.ilk_parca_suresi is None:
            self.ilk_parca_suresi = time.monotonic() - self.baslangic

    def _parca_geldi(self, akis, parca: str) -> None:
        if akis is not self._akis:
            return
        self._ham += parca
        metin = self.metin()
        if metin.strip():
            self._ilk_parca()
        self.guncellendi.emit(metin)

    def _parca_bitti(self, akis) -> None:
        if akis is not self._akis:
            return
        self._akis = None
        ceviri = bos_satirlari_duzelt(self._akis_parca, temizle(self._ham, self._akis_parca, son=True))
        if bicim.kalin_sorunlari(self._akis_parca, ceviri, self._kaynak, self._hedef):
            kodla = bicim.kalin_kodla(self._akis_parca, ceviri, self._kaynak, self._hedef)
            if kodla:
                self.kalin_kaydi.append(f"kod (olumsuzluk sırası): {kodla}")
                ceviri = kodla
            else:
                self._kalin_iste(ceviri)
                return
        self._parca_tamam(ceviri)

    def _parca_tamam(self, ceviri: str) -> None:
        self._onbellek[self._akis_anahtar] = ceviri
        self._ham = ""
        self._kalin_taslak = None
        self._ilerle()

    def _kalin_iste(self, ceviri: str) -> None:
        """Kısa ek istek: model yalnız çeviriden hangi parçaların kalın olacağını söyler."""
        self._kalin_taslak = ceviri
        self._kalin_ham = ""
        self.kalin_istegi += 1
        mesaj = kalin_mesaji(self._kaynak, self._hedef, self._akis_parca, bicim.kalinsiz(ceviri),
                             bicim.kalin_parcalari(self._akis_parca))
        mesajlar = [{"role": "system", "content": self._kalin_sistem}, {"role": "user", "content": mesaj}]
        self._akis = akis = self.ollama.cevir(mesajlar, KALIN_SEMASI)
        akis.parca.connect(lambda p: self._kalin_parca(akis, p))
        akis.bitti.connect(lambda: self._kalin_bitti(akis))
        akis.hata.connect(lambda m: self._kalin_bitti(akis))  # kalın yazı isteği başarısızsa çeviri olduğu gibi kalır

    def _kalin_parca(self, akis, parca: str) -> None:
        if akis is self._akis:
            self._kalin_ham += parca

    def _kalin_bitti(self, akis) -> None:
        if akis is not self._akis:
            return
        self._akis = None
        ceviri = self._kalin_taslak
        try:
            parcalar = json.loads(self._kalin_ham).get("bold")
        except (ValueError, AttributeError):
            parcalar = None
        yeni, neden = bicim.kalin_uygula(ceviri, parcalar, self._akis_parca, self._kaynak, self._hedef)
        self.kalin_kaydi.append(f"model parçaları {parcalar!r} " + ("uygulandı" if yeni else f"uygulanmadı: {neden}"))
        self._parca_tamam(yeni or ceviri)

    def _parca_hatasi(self, akis, mesaj: str) -> None:
        if akis is not self._akis:
            return
        self._akis = None
        self.guncellendi.emit(self.metin())
        self.hata.emit(mesaj)
