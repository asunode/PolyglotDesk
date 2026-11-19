"""Ana pencere ve ayarlar penceresi."""

import time
from pathlib import Path

from html import escape

from PySide6.QtCore import QSize, Qt, QTimer, QUrl, Signal
from PySide6.QtGui import QDesktopServices, QGuiApplication, QIcon, QKeySequence, QShortcut, QTextCursor
from PySide6.QtWidgets import (
    QButtonGroup, QCheckBox, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QFrame, QHBoxLayout,
    QLabel, QPlainTextEdit, QPushButton, QSizePolicy, QTextBrowser, QToolButton, QVBoxLayout, QWidget,
)

from . import ayarlar as ayar_dosyasi
from .cevirici import Cevirici
from .detayli import ASAMALAR, DetayliCevirici
from .istem import DILLER, sinir_istemi
from .ollama import Ollama
from .sozluk import Sozluk

SIMGELER = Path(__file__).parent / "simgeler"
# Yazmayı bırakınca çeviriye başlamadan önce beklenen süre.
OTOMATIK_MS = 1000

STIL = f"""
#kok {{ background: #f4f4f4; }}
#kart {{ background: #ffffff; border: 1px solid #e3e3e3; border-radius: 14px; }}
QComboBox#dil {{
    border: none; background: transparent; font-weight: 600; font-size: 15px;
    color: #202124; padding: 6px 4px 6px 10px;
}}
QComboBox#dil:hover {{ background: #f1f3f4; border-radius: 8px; }}
QComboBox#dil::drop-down {{ border: none; width: 22px; }}
QComboBox#dil::down-arrow {{ image: url({(SIMGELER / "asagi.svg").as_posix()}); width: 16px; height: 16px; }}
QComboBox#dil QAbstractItemView {{
    background: #ffffff; border: 1px solid #e3e3e3; selection-background-color: #e8f0fe;
    selection-color: #202124; font-size: 15px; padding: 4px; outline: none;
}}
QToolButton#simge {{ border: none; border-radius: 18px; padding: 6px; }}
QToolButton#simge:hover {{ background: #f1f3f4; }}
QPlainTextEdit {{
    border: none; background: transparent; font-size: 18px; color: #202124;
    selection-background-color: #c6dafc; selection-color: #202124;
}}
QPushButton {{
    border: 1px solid #dadce0; border-radius: 16px; padding: 6px 14px; background: #ffffff;
    font-size: 14px; font-weight: 600; color: #202124;
}}
QPushButton:hover {{ background: #f1f3f4; }}
QPushButton:disabled {{ color: #b0b0b0; border-color: #ececec; }}
QPushButton#birincil {{ background: #1a73e8; border-color: #1a73e8; color: #ffffff; }}
QPushButton#birincil:hover {{ background: #1765cc; }}
QPushButton#birincil:disabled {{ background: #a8c7fa; border-color: #a8c7fa; color: #ffffff; }}
QLabel#durum {{ font-size: 13px; color: #5f6368; }}
QPushButton#gorunum {{ border-radius: 12px; padding: 3px 12px; font-size: 13px; font-weight: 600; color: #5f6368; }}
QPushButton#gorunum:checked {{ background: #e8f0fe; border-color: #c6dafc; color: #1967d2; }}
QToolButton#acilir {{ border: none; font-size: 13px; font-weight: 600; color: #5f6368; padding: 2px 0; }}
QTextBrowser#bilgiler {{ border: 1px solid #e3e3e3; border-radius: 8px; background: #fafafa; font-size: 13px; }}
"""

RENK_BILGI = "#5f6368"
RENK_HATA = "#c5221f"


class KaynakKutusu(QPlainTextEdit):
    """Yapıştırmayı (Ctrl+V, sağ tık menüsü, sürükle-bırak) ayrıca bildiren metin kutusu."""

    yapistirildi = Signal()

    def insertFromMimeData(self, kaynak) -> None:
        self.yapistirildi.emit()
        super().insertFromMimeData(kaynak)


def _dil_secici() -> QComboBox:
    kutu = QComboBox()
    kutu.setObjectName("dil")
    kutu.setCursor(Qt.CursorShape.PointingHandCursor)
    for kod, ad in DILLER.items():
        kutu.addItem(ad, kod)
    return kutu


def _simge_dugmesi(dosya: str, ipucu: str) -> QToolButton:
    dugme = QToolButton()
    dugme.setObjectName("simge")
    dugme.setIcon(QIcon(str(SIMGELER / dosya)))
    dugme.setIconSize(QSize(22, 22))
    dugme.setToolTip(ipucu)
    dugme.setCursor(Qt.CursorShape.PointingHandCursor)
    return dugme


class AnaPencere(QWidget):
    def __init__(self):
        super().__init__()
        self.ayarlar = ayar_dosyasi.yukle()
        self.ollama = Ollama(self.ayarlar, self)
        self.sozluk = Sozluk()
        self.sozluk.hazirla()
        self.cevirici = Cevirici(self.ollama, self.sozluk, self)
        self.cevirici.guncellendi.connect(self._hizli_geldi)
        self.cevirici.ilerleme.connect(self._ilerleme)
        self.cevirici.bitti.connect(self._ceviri_bitti)
        self.cevirici.hata.connect(self._ceviri_hatasi)
        self.detayli = DetayliCevirici(self.ollama, self.sozluk, self)
        self.detayli.guncellendi.connect(self._detayli_geldi)
        self.detayli.asama.connect(self._detayli_asama)
        self.detayli.bilgiler.connect(self._bilgileri_goster)
        self.detayli.bitti.connect(self._detayli_bitti)
        self.detayli.hata.connect(self._detayli_hatasi)
        self._hizli_metin = ""
        self._detayli_metin = ""
        self._gorunum = "hizli"       # sağ panelde gösterilen sonuç
        self._yapistirma = False
        self._son_ceviri = None    # (metin, kaynak dil, hedef dil, model) — tekrar çevirmemek için
        self._yukleme = None
        self._yon = (self.ayarlar["kaynak_dil"], "en" if self.ayarlar["kaynak_dil"] == "tr" else "tr")

        self.setObjectName("kok")
        self.setWindowTitle("PolyglotDesk")
        self.resize(1180, 600)
        self.setMinimumSize(720, 420)
        self.setStyleSheet(STIL)
        self._arayuzu_kur()

        self.zamanlayici = QTimer(self)
        self.zamanlayici.setSingleShot(True)
        self.zamanlayici.setInterval(OTOMATIK_MS)
        self.zamanlayici.timeout.connect(self.cevir)
        self.kaynak.textChanged.connect(self._kaynak_degisti)
        self.kaynak.yapistirildi.connect(self._yapistirildi)
        QShortcut(QKeySequence("Ctrl+Return"), self, activated=self.detayli_cevir)
        QShortcut(QKeySequence("Ctrl+Enter"), self, activated=self.detayli_cevir)
        QShortcut(QKeySequence("Escape"), self, activated=self.durdur)

        self._dilleri_goster()
        self._dugmeleri_guncelle()
        QTimer.singleShot(0, self._acilis_denetimi)

    # ---------------------------------------------------------------- arayüz
    def _arayuzu_kur(self) -> None:
        kok = QVBoxLayout(self)
        kok.setContentsMargins(6, 6, 6, 6)
        kok.setSpacing(8)

        ust = QFrame(objectName="kart")
        ust.setFixedHeight(60)
        ust_duzen = QHBoxLayout(ust)
        ust_duzen.setContentsMargins(12, 0, 12, 0)
        self.sol_dil = _dil_secici()
        self.sag_dil = _dil_secici()
        self.takas_dugmesi = _simge_dugmesi("degistir.svg", "Yönü değiştir")
        self.ayar_dugmesi = _simge_dugmesi("ayarlar.svg", "Ayarlar")
        denge = QWidget()
        denge.setFixedSize(self.ayar_dugmesi.sizeHint())
        ust_duzen.addWidget(denge)
        ust_duzen.addStretch(1)
        ust_duzen.addWidget(self.sol_dil)
        ust_duzen.addSpacing(12)
        ust_duzen.addWidget(self.takas_dugmesi)
        ust_duzen.addSpacing(12)
        ust_duzen.addWidget(self.sag_dil)
        ust_duzen.addStretch(1)
        ust_duzen.addWidget(self.ayar_dugmesi)
        kok.addWidget(ust)

        paneller = QHBoxLayout()
        paneller.setSpacing(8)
        kok.addLayout(paneller, 1)

        sol = QFrame(objectName="kart")
        sol_duzen = QVBoxLayout(sol)
        sol_duzen.setContentsMargins(18, 16, 18, 14)
        self.kaynak = KaynakKutusu()
        self.kaynak.setPlaceholderText("Çevirmek için yazın ya da yapıştırın.")
        sol_duzen.addWidget(self.kaynak, 1)
        sol_alt = QHBoxLayout()
        self.ipucu = QLabel("Ctrl+Enter: Detaylı Çevir · Esc: durdur", objectName="durum")
        self.detayli_dugmesi = QPushButton("Detaylı Çevir", objectName="birincil")
        self.detayli_dugmesi.setToolTip("Bilgi paketiyle çevirir ve çeviriyi ikinci bir geçişte denetler (daha uzun sürer).")
        sol_alt.addWidget(self.ipucu)
        sol_alt.addStretch(1)
        sol_alt.addWidget(self.detayli_dugmesi)
        sol_duzen.addLayout(sol_alt)
        paneller.addWidget(sol, 1)

        sag = QFrame(objectName="kart")
        sag_duzen = QVBoxLayout(sag)
        sag_duzen.setContentsMargins(18, 16, 18, 14)
        self.gorunum_satiri = QWidget()
        gorunum_duzen = QHBoxLayout(self.gorunum_satiri)
        gorunum_duzen.setContentsMargins(0, 0, 0, 6)
        self.hizli_gorunum = QPushButton("Hızlı", objectName="gorunum", checkable=True, checked=True)
        self.detayli_gorunum = QPushButton("Detaylı", objectName="gorunum", checkable=True)
        grup = QButtonGroup(self)
        grup.setExclusive(True)
        for d in (self.hizli_gorunum, self.detayli_gorunum):
            grup.addButton(d)
            d.setCursor(Qt.CursorShape.PointingHandCursor)
            gorunum_duzen.addWidget(d)
        gorunum_duzen.addStretch(1)
        self.gorunum_satiri.hide()
        sag_duzen.addWidget(self.gorunum_satiri)
        self.hedef = QPlainTextEdit()
        self.hedef.setReadOnly(True)
        self.hedef.setPlaceholderText("Çeviri burada görünecek.")
        sag_duzen.addWidget(self.hedef, 1)
        self.bilgi_dugmesi = QToolButton(objectName="acilir", checkable=True)
        self.bilgi_dugmesi.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.bilgi_dugmesi.setArrowType(Qt.ArrowType.RightArrow)
        self.bilgi_dugmesi.setCursor(Qt.CursorShape.PointingHandCursor)
        self.bilgi_kutusu = QTextBrowser(objectName="bilgiler")
        self.bilgi_kutusu.setMaximumHeight(220)
        self.bilgi_dugmesi.hide()
        self.bilgi_kutusu.hide()
        sag_duzen.addWidget(self.bilgi_dugmesi)
        sag_duzen.addWidget(self.bilgi_kutusu)
        sag_alt = QHBoxLayout()
        self.durum = QLabel(objectName="durum")
        self.durum.setWordWrap(True)
        self.durum.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.durdur_dugmesi = QPushButton(QIcon(str(SIMGELER / "durdur.svg")), "Durdur")
        self.kopyala_dugmesi = QPushButton(QIcon(str(SIMGELER / "kopyala.svg")), "Kopyala")
        sag_alt.addWidget(self.durum, 1)
        sag_alt.addWidget(self.durdur_dugmesi)
        sag_alt.addWidget(self.kopyala_dugmesi)
        sag_duzen.addLayout(sag_alt)
        paneller.addWidget(sag, 1)

        for dugme in (self.detayli_dugmesi, self.durdur_dugmesi, self.kopyala_dugmesi):
            dugme.setCursor(Qt.CursorShape.PointingHandCursor)

        self.sol_dil.currentIndexChanged.connect(lambda: self._dil_secildi(self.sol_dil, 0))
        self.sag_dil.currentIndexChanged.connect(lambda: self._dil_secildi(self.sag_dil, 1))
        self.takas_dugmesi.clicked.connect(self.takas)
        self.ayar_dugmesi.clicked.connect(self.ayarlari_ac)
        self.detayli_dugmesi.clicked.connect(self.detayli_cevir)
        self.hizli_gorunum.clicked.connect(lambda: self._gorunum_sec("hizli"))
        self.detayli_gorunum.clicked.connect(lambda: self._gorunum_sec("detayli"))
        self.bilgi_dugmesi.toggled.connect(self._bilgi_ac_kapa)
        self.durdur_dugmesi.clicked.connect(self.durdur)
        self.kopyala_dugmesi.clicked.connect(self.kopyala)

    def _dilleri_goster(self) -> None:
        for kutu, kod in ((self.sol_dil, self._yon[0]), (self.sag_dil, self._yon[1])):
            kutu.blockSignals(True)
            kutu.setCurrentIndex(kutu.findData(kod))
            kutu.blockSignals(False)

    def _durum_yaz(self, metin: str, hata: bool = False) -> None:
        self.durum.setStyleSheet(f"color: {RENK_HATA if hata else RENK_BILGI};")
        self.durum.setText(metin)

    def _dugmeleri_guncelle(self) -> None:
        self.durdur_dugmesi.setEnabled(self.cevirici.calisiyor or self.detayli.calisiyor)
        self.kopyala_dugmesi.setEnabled(bool(self.hedef.toPlainText().strip()))
        self.detayli_dugmesi.setEnabled(bool(self.kaynak.toPlainText().strip()) and not self.detayli.calisiyor)

    # ---------------------------------------------------------------- açılış
    def _acilis_denetimi(self) -> None:
        istek = self.ollama.modeller()
        istek.tamam.connect(self._modeller_geldi)
        istek.hata.connect(lambda mesaj: self._durum_yaz(mesaj, hata=True))

    def _modeller_geldi(self, adlar: list) -> None:
        model = self.ayarlar["model"]
        if model not in adlar:
            self._durum_yaz(f"“{model}” modeli Ollama'da kurulu değil. Ayarlar'dan kurulu bir model seçin.", hata=True)
            return
        self._onden_yukle()

    def _onden_yukle(self) -> None:
        if self._yukleme is not None:
            self._yukleme.iptal()
        self._yukleme = istek = self.ollama.onden_yukle(sinir_istemi())
        if not self.cevirici.calisiyor:
            self._durum_yaz(f"{self.ayarlar['model']} yükleniyor…")

        def bitti(hata=None):
            if self._yukleme is not istek:
                return
            self._yukleme = None
            if not self.cevirici.calisiyor and (hata or not self._son_ceviri):
                self._durum_yaz(hata or f"{self.ayarlar['model']} hazır.", hata=bool(hata))

        istek.tamam.connect(lambda _: bitti())
        istek.hata.connect(bitti)

    # ---------------------------------------------------------------- hızlı çeviri
    def _yapistirildi(self) -> None:
        self._yapistirma = True

    def _kaynak_degisti(self) -> None:
        # Kaynak değişince Detaylı sonuç geçersizdir; hızlı çeviri yeniden başlar.
        self._detayliyi_sifirla()
        self._dugmeleri_guncelle()
        yapistirma, self._yapistirma = self._yapistirma, False
        if self.kaynak.toPlainText().strip():
            # Yapıştırınca beklemeden, elle yazarken yazma bitince başlar.
            self.zamanlayici.start(0 if yapistirma else OTOMATIK_MS)
        else:
            self.zamanlayici.stop()
            self.cevirici.durdur()
            self._hizli_metin = ""
            self.hedef.clear()
            self._son_ceviri = None
            self._durum_yaz("")
            self._dugmeleri_guncelle()

    def cevir(self, zorla: bool = False) -> None:
        self.zamanlayici.stop()
        metin = self.kaynak.toPlainText()
        if not metin.strip():
            return
        istek = (metin, *self._yon, self.ayarlar["model"])
        if not zorla and istek == self._son_ceviri:
            return
        self._son_ceviri = istek
        self._durum_yaz("Çevriliyor…")
        # Önbellekteki parçalar hemen gelir; yalnız değişen parçalar modele gider.
        self.cevirici.baslat(metin, *self._yon)
        self._dugmeleri_guncelle()

    def _hedefi_goster(self, yeni: str) -> None:
        eski = self.hedef.toPlainText()
        if yeni == eski:
            return
        if eski and yeni.startswith(eski):
            imlec = self.hedef.textCursor()
            imlec.movePosition(QTextCursor.MoveOperation.End)
            imlec.insertText(yeni[len(eski):])
        else:
            self.hedef.setPlainText(yeni)
        self.hedef.moveCursor(QTextCursor.MoveOperation.End)
        self.hedef.ensureCursorVisible()
        self._dugmeleri_guncelle()

    def _hizli_geldi(self, metin: str) -> None:
        self._hizli_metin = metin
        if self._gorunum == "hizli":
            self._hedefi_goster(metin)

    def _ilerleme(self, sira: int, toplam: int) -> None:
        if not self.detayli.calisiyor:
            self._durum_yaz("Çevriliyor…" if toplam == 1 else f"Çevriliyor… (parça {sira}/{toplam})")
        self._dugmeleri_guncelle()

    def _ceviri_bitti(self) -> None:
        c = self.cevirici
        sure = time.monotonic() - c.baslangic
        ek = ""
        if c.parca_sayisi > 1:
            ek = f" · {c.parca_sayisi} parça"
        if c.onbellekten:
            ek += f" ({c.onbellekten} önbellekten)"
        if c.kalin_istegi:
            ek += " · kalın yazı yeri soruldu"
        if not self.detayli.calisiyor and self._gorunum == "hizli":
            self._durum_yaz(f"Hızlı · {self.ayarlar['model']} · {sure:.1f} sn{ek}")
        self._dugmeleri_guncelle()

    def _ceviri_hatasi(self, mesaj: str) -> None:
        self._son_ceviri = None
        self._durum_yaz(mesaj, hata=True)
        self._dugmeleri_guncelle()

    def durdur(self) -> None:
        self.zamanlayici.stop()
        if self.detayli.durdur():
            self._detayli_metin = self.detayli.metin()
            if self._gorunum == "detayli":
                self._hedefi_goster(self._detayli_metin)
            self._durum_yaz("Detaylı Çevir durduruldu. Yeniden başlatmak için Detaylı Çevir'e basın.")
        elif self.cevirici.durdur():
            self._hizli_geldi(self.cevirici.metin())
            self._son_ceviri = None
            self._durum_yaz("Durduruldu. Çevrilen parçalar saklandı; metni değiştirince kalan kısım çevrilir.")
        self._dugmeleri_guncelle()

    # ---------------------------------------------------------------- Detaylı Çevir
    def detayli_cevir(self) -> None:
        metin = self.kaynak.toPlainText()
        if not metin.strip() or self.detayli.calisiyor:
            return
        self.zamanlayici.stop()
        # Ollama istekleri sırayla işler; süren hızlı çeviri durdurulur (gelen kısmı korunur).
        if self.cevirici.durdur():
            self._hizli_geldi(self.cevirici.metin())
            self._son_ceviri = None
        self._detayli_metin = ""
        self.gorunum_satiri.show()
        self._gorunum_sec("detayli")
        self.detayli.baslat(metin, *self._yon)
        self._dugmeleri_guncelle()

    def _detayliyi_sifirla(self) -> None:
        self.detayli.durdur()
        self._detayli_metin = ""
        self.gorunum_satiri.hide()
        self.bilgi_dugmesi.hide()
        self.bilgi_dugmesi.setChecked(False)
        self.bilgi_kutusu.clear()
        if self._gorunum != "hizli":
            self._gorunum_sec("hizli")

    def _gorunum_sec(self, gorunum: str) -> None:
        self._gorunum = gorunum
        self.hizli_gorunum.setChecked(gorunum == "hizli")
        self.detayli_gorunum.setChecked(gorunum == "detayli")
        self._hedefi_goster(self._hizli_metin if gorunum == "hizli" else self._detayli_metin)

    def _detayli_geldi(self, metin: str) -> None:
        self._detayli_metin = metin
        if self._gorunum == "detayli":
            self._hedefi_goster(metin)

    def _detayli_asama(self, kod: str, sira: int, toplam: int) -> None:
        ek = f" (parça {sira}/{toplam})" if toplam > 1 else ""
        self._durum_yaz(f"Detaylı Çevir: {ASAMALAR[kod]}…{ek}")
        self._dugmeleri_guncelle()

    def _detayli_bitti(self) -> None:
        d = self.detayli
        sure = time.monotonic() - d.baslangic
        toplam = {a: sum(s.sure.get(a, 0) for s in d.sonuclar if s) for a in ASAMALAR}
        mesaj = (f"Detaylı · {sure:.1f} sn (arama {toplam['arama']:.1f}, çeviri {toplam['ceviri']:.1f}, "
                 f"denetim {toplam['denetim']:.1f} sn)")
        kalan = [p for s in d.sonuclar if s for p in s.sorunlar_sonra]
        if kalan:
            mesaj += " · Uyarı: biçim farkı kaldı (Kullanılan bilgiler'e bakın)."
        self._durum_yaz(mesaj)
        self._bilgileri_goster(d.tum_kayitlar())
        self._dugmeleri_guncelle()

    def _detayli_hatasi(self, mesaj: str) -> None:
        self._durum_yaz(mesaj, hata=True)
        if not self._detayli_metin.strip():
            self.gorunum_satiri.hide()
            self._gorunum_sec("hizli")
        self._dugmeleri_guncelle()

    def _bilgileri_goster(self, kayitlar: list) -> None:
        if not kayitlar:
            self.bilgi_dugmesi.hide()
            self.bilgi_kutusu.hide()
            return
        gruplar = [("kalip", "Kalıplar ve deyimler"), ("anlam", "Çok anlamlı kelimeler"),
                   ("ornek", "Örnek cümleler"), ("sozluk", "Kullanıcı sözlüğü")]
        html = []
        for tur, baslik in gruplar:
            secilen = [k for k in kayitlar if k.tur == tur]
            if not secilen:
                continue
            html.append(f"<p style='margin:6px 0 2px 0'><b>{baslik}</b></p><ul style='margin:0'>")
            for k in secilen:
                html.append(f"<li>{escape(k.istem)} <span style='color:#5f6368'>— {escape(k.kaynak)}"
                            + (f", {escape(k.lisans)}" if k.lisans != "—" else "") + "</span></li>")
            html.append("</ul>")
        kararlar = [s for s in self.detayli.sonuclar if s and s.karar is not None]
        if kararlar:
            html.append("<p style='margin:6px 0 2px 0'><b>Denetim kararı</b></p><ul style='margin:0'>")
            for s in kararlar:
                if isinstance(s.karar, str):
                    html.append(f"<li>{escape(s.karar)} — taslak korundu</li>")
                elif not s.uygulanan and not s.geri_alinan and not s.uygulanmayan:
                    html.append("<li>hata yok — taslak olduğu gibi kaldı</li>")
                for h in s.uygulanan:
                    html.append(f"<li>düzeltildi ({escape(h.get('type', ''))}): “{escape(h.get('draft_text', ''))}” → "
                                f"“{escape(h.get('corrected_text', ''))}”</li>")
                for h in s.geri_alinan + s.uygulanmayan:
                    html.append(f"<li>uygulanmadı: “{escape(h.get('draft_text', ''))}” → “{escape(h.get('corrected_text', ''))}” "
                                f"<span style='color:#5f6368'>({escape(h.get('neden', ''))})</span></li>")
            html.append("</ul>")
        kalan = [p for s in self.detayli.sonuclar if s for p in s.sorunlar_sonra]
        if kalan:
            html.append("<p style='margin:6px 0 2px 0'><b>Denetimden sonra kalan biçim farkları</b></p><ul style='margin:0'>")
            html += [f"<li>{escape(p)}</li>" for p in kalan]
            html.append("</ul>")
        self.bilgi_kutusu.setHtml("".join(html))
        self.bilgi_dugmesi.setText(f"Kullanılan bilgiler ({len(kayitlar)})")
        self.bilgi_dugmesi.show()
        self.bilgi_kutusu.setVisible(self.bilgi_dugmesi.isChecked())

    def _bilgi_ac_kapa(self, acik: bool) -> None:
        self.bilgi_dugmesi.setArrowType(Qt.ArrowType.DownArrow if acik else Qt.ArrowType.RightArrow)
        self.bilgi_kutusu.setVisible(acik)

    # ---------------------------------------------------------------- yön
    def _dil_secildi(self, kutu: QComboBox, taraf: int) -> None:
        # İki dil var: bir taraftaki seçim değiştiyse yön tersine dönmüştür.
        if kutu.currentData() != self._yon[taraf]:
            self.takas()

    def takas(self) -> None:
        self.zamanlayici.stop()
        if self.cevirici.durdur():
            self._hizli_geldi(self.cevirici.metin())
        self.detayli.durdur()
        self._yon = (self._yon[1], self._yon[0])
        self._dilleri_goster()

        eski_kaynak = self.kaynak.toPlainText()
        eski_hedef = self.hedef.toPlainText()   # ekrandaki (hızlı ya da detaylı) çeviri
        self.kaynak.blockSignals(True)
        self.kaynak.setPlainText(eski_hedef)
        self.kaynak.blockSignals(False)
        self._detayliyi_sifirla()
        self._hizli_metin = eski_kaynak
        self.hedef.setPlainText(eski_kaynak)
        # Metinler zaten birbirinin çevirisi; yeniden çevirmeye gerek yok.
        self._son_ceviri = (eski_hedef, *self._yon, self.ayarlar["model"]) if eski_hedef.strip() else None
        self._durum_yaz("")
        self._dugmeleri_guncelle()

    # ---------------------------------------------------------------- diğer
    def kopyala(self) -> None:
        metin = self.hedef.toPlainText().strip()
        if not metin:
            return
        QGuiApplication.clipboard().setText(metin)
        self.kopyala_dugmesi.setText("Kopyalandı")
        QTimer.singleShot(1500, lambda: self.kopyala_dugmesi.setText("Kopyala"))

    def ayarlari_ac(self) -> None:
        pencere = AyarlarPenceresi(self.ollama, self.ayarlar, self.sozluk.hazirla(), self)
        kabul = pencere.exec() == QDialog.DialogCode.Accepted
        yeni = pencere.secilenler()
        pencere.deleteLater()
        if not kabul:
            return
        if yeni == {k: self.ayarlar[k] for k in yeni}:
            return
        self.ayarlar.update(yeni)
        ayar_dosyasi.kaydet(self.ayarlar)
        self._onden_yukle()
        if self.kaynak.toPlainText().strip():
            self.cevir(zorla=True)

    def closeEvent(self, olay) -> None:
        self.cevirici.durdur()
        self.detayli.durdur()
        if self.ayarlar["kaynak_dil"] != self._yon[0]:
            self.ayarlar["kaynak_dil"] = self._yon[0]
            ayar_dosyasi.kaydet(self.ayarlar)
        super().closeEvent(olay)


class AyarlarPenceresi(QDialog):
    def __init__(self, ollama: Ollama, ayarlar: dict, sozluk_yolu: Path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ayarlar — PolyglotDesk")
        self.setMinimumWidth(460)
        self.setStyleSheet("QLabel#aciklama { color: #5f6368; font-size: 12px; }")
        self._model = ayarlar["model"]

        duzen = QVBoxLayout(self)
        form = QFormLayout()
        self.model_kutusu = QComboBox()
        self.model_kutusu.addItem(f"{self._model} (liste yükleniyor…)", self._model)
        form.addRow("Model:", self.model_kutusu)
        self.model_durumu = QLabel(objectName="aciklama")
        self.model_durumu.setWordWrap(True)
        form.addRow("", self.model_durumu)
        self.cpu_kutusu = QCheckBox("Yalnız işlemciyi (CPU) kullan")
        self.cpu_kutusu.setChecked(ayarlar["yalniz_cpu"])
        form.addRow("", self.cpu_kutusu)
        aciklama = QLabel(
            "Bu bilgisayarda ekran kartı (R9 380, 4 GB) modeli hızlandırmıyor; "
            "yalnız işlemciyle ilk kelime daha erken geliyor.",
            objectName="aciklama",
        )
        aciklama.setWordWrap(True)
        form.addRow("", aciklama)

        sozluk_satiri = QHBoxLayout()
        yol = QLabel(str(sozluk_yolu).replace(str(Path.home()), "~"))
        yol.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        ac = QPushButton("Sözlüğü aç")
        ac.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(str(sozluk_yolu))))
        sozluk_satiri.addWidget(yol, 1)
        sozluk_satiri.addWidget(ac)
        form.addRow("Terim sözlüğü:", sozluk_satiri)
        sozluk_aciklama = QLabel(
            "Düz metin dosyası; biçimi dosyanın başında anlatılır. Kaydettiğiniz anda "
            "sonraki çeviride geçerli olur, yeniden başlatmak gerekmez.",
            objectName="aciklama",
        )
        sozluk_aciklama.setWordWrap(True)
        form.addRow("", sozluk_aciklama)
        duzen.addLayout(form)

        hakkinda = QLabel(
            "<b>PolyglotDesk</b> — yerel, internetsiz Türkçe ↔ İngilizce çevirmen (MIT lisansı).<br><br>"
            "<b>Detaylı Çevir veri kaynakları</b><br>"
            "Bilgi paketi yerel PostgreSQL'de (<i>cevirmen</i> veritabanı, yalnız okuma) durur; çeviri sırasında internete çıkılmaz.<br>"
            "• <a href='https://en.wiktionary.org'>Wiktionary</a> (İngilizce Vikisözlük; "
            "<a href='https://kaikki.org/dictionary/rawdata.html'>kaikki.org</a> / wiktextract çıkarımı): "
            "kalıplar, deyimler, çok anlamlı kelimeler, çekimli biçimler. Lisans: "
            "<a href='https://creativecommons.org/licenses/by-sa/4.0/'>CC BY-SA 4.0</a> (ayrıca GFDL).<br>"
            "• <a href='https://tatoeba.org'>Tatoeba</a>: Türkçe–İngilizce örnek cümle çiftleri. Lisans: "
            "<a href='https://creativecommons.org/licenses/by/2.0/fr/'>CC BY 2.0 FR</a>.<br>"
            "Her kaydın kaynağı ve lisansı veritabanında tutulur ve \"Kullanılan bilgiler\" bölümünde gösterilir.",
            objectName="aciklama",
        )
        hakkinda.setWordWrap(True)
        hakkinda.setOpenExternalLinks(True)
        hakkinda.setTextFormat(Qt.TextFormat.RichText)
        duzen.addSpacing(8)
        duzen.addWidget(hakkinda)

        dugmeler = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        dugmeler.button(QDialogButtonBox.StandardButton.Save).setText("Kaydet")
        dugmeler.button(QDialogButtonBox.StandardButton.Cancel).setText("Vazgeç")
        dugmeler.accepted.connect(self.accept)
        dugmeler.rejected.connect(self.reject)
        duzen.addWidget(dugmeler)

        istek = ollama.modeller()
        istek.tamam.connect(self._modeller_geldi)
        istek.hata.connect(self._liste_hatasi)

    def _modeller_geldi(self, adlar: list) -> None:
        self.model_kutusu.clear()
        for ad in adlar:
            self.model_kutusu.addItem(ad, ad)
        if self._model not in adlar:
            self.model_kutusu.insertItem(0, f"{self._model} (kurulu değil)", self._model)
            self.model_durumu.setText("Seçili model Ollama'da bulunamadı; listeden kurulu bir model seçin.")
        self.model_kutusu.setCurrentIndex(self.model_kutusu.findData(self._model))

    def _liste_hatasi(self, mesaj: str) -> None:
        self.model_kutusu.setItemText(0, self._model)
        self.model_durumu.setText(mesaj)

    def secilenler(self) -> dict:
        return {"model": self.model_kutusu.currentData(), "yalniz_cpu": self.cpu_kutusu.isChecked()}
