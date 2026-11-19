"""Ollama HTTP API istemcisi: akışlı çeviri, model listesi, önden yükleme.

QtNetwork ile çalışır; ayrı iş parçacığı gerekmez, durdurmak isteği iptal etmektir.
"""

import json

from PySide6.QtCore import QObject, QUrl, Signal
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

# Kaynak + çeviri için yeterli; değişirse Ollama modeli yeniden yükler.
BAGLAM = 8192
# Aynı metin aynı ayarlarla hep aynı çeviriyi versin.
TOHUM = 42
# Bu süre boyunca hiç veri gelmezse istek zaman aşımına düşer (model yükleme dahil).
BEKLEME_MS = 300_000

_HATA = QNetworkReply.NetworkError


def hata_metni(ollama_hatasi: str, model: str) -> str:
    """Ollama'nın döndürdüğü hata metnini kullanıcıya gösterilecek Türkçe mesaja çevirir."""
    kucuk = ollama_hatasi.lower()
    if "not found" in kucuk and "model" in kucuk:
        return f"“{model}” modeli Ollama'da bulunamadı. Ayarlar'dan kurulu bir model seçin."
    if "memory" in kucuk:
        return f"“{model}” için yeterli bellek yok. Ayarlar'dan daha küçük bir model seçin. (Ollama: {ollama_hatasi})"
    return f"Ollama hata verdi: {ollama_hatasi}"


def _yanit_hatasi(yanit: QNetworkReply, govde: bytes, model: str, adres: str) -> str | None:
    durum = yanit.attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute)
    if durum and durum >= 400:
        try:
            metin = json.loads(govde).get("error") or f"HTTP {durum}"
        except (ValueError, AttributeError):
            metin = govde.decode("utf-8", "replace").strip() or f"HTTP {durum}"
        return hata_metni(metin, model)
    hata = yanit.error()
    if hata == _HATA.NoError:
        return None
    if hata in (_HATA.ConnectionRefusedError, _HATA.HostNotFoundError):
        return (
            f"Ollama'ya ulaşılamıyor ({adres}). Ollama çalışmıyor olabilir; terminalde "
            "“systemctl start ollama” ya da “ollama serve” komutuyla başlatıp yeniden deneyin."
        )
    if hata in (_HATA.TimeoutError, _HATA.OperationCanceledError):
        return "Ollama zamanında yanıt vermedi. Model yükleniyor olabilir; biraz sonra yeniden deneyin."
    return f"Ollama'ya bağlanırken hata oluştu: {yanit.errorString()}"


class Ollama(QObject):
    def __init__(self, ayarlar: dict, parent=None):
        super().__init__(parent)
        self.ayarlar = ayarlar
        self._ag = QNetworkAccessManager(self)
        # Ollama'nın istem önbelleği yalnız belirli noktalardan devam edebiliyor (gemma'nın kayan pencere dikkati);
        # hızlı çevirinin önbellek dışı kısmı farklı noktadan işlenince çıktı değişebiliyor. Son istek önden yükleme,
        # sınır isteği ya da hızlı çeviriyse True; Detaylı/denetim/kalın isteğinden sonra False
        # (hızlı çeviri önce sınır isteği gönderir). Bkz. doc/olcum/tutarlilik-inceleme.md.
        self.onbellek_sinirda = False

    @property
    def adres(self) -> str:
        return self.ayarlar["ollama_adresi"].rstrip("/")

    def _istek(self, yol: str) -> QNetworkRequest:
        istek = QNetworkRequest(QUrl(self.adres + yol))
        istek.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json")
        istek.setTransferTimeout(BEKLEME_MS)
        return istek

    def _secenekler(self) -> dict:
        secenek = {"temperature": 0, "seed": TOHUM, "num_ctx": BAGLAM}
        if self.ayarlar["yalniz_cpu"]:
            secenek["num_gpu"] = 0
        return secenek

    def _gonder(self, yol: str, govde: dict) -> QNetworkReply:
        return self._ag.post(self._istek(yol), json.dumps(govde).encode("utf-8"))

    def cevir(self, mesajlar: list[dict], bicim: dict | None = None, hizli: bool = False,
              secenek: dict | None = None) -> "Akis":
        """mesajlar: sistem istemi ve çevrilecek metin. bicim: verilirse cevap bu JSON şemasına zorlanır.
        hizli: hızlı çeviri isteği (önbellek durumunu bozmaz)."""
        self.onbellek_sinirda = hizli
        model = self.ayarlar["model"]
        govde = {
            "model": model,
            "stream": True,
            # Düşünen modeller (gemma4 vb.) aksi hâlde çeviriden önce uzun süre düşünür.
            "think": False,
            "keep_alive": self.ayarlar["keep_alive"],
            "options": {**self._secenekler(), **(secenek or {})},
            "messages": mesajlar,
        }
        if bicim is not None:
            govde["format"] = bicim
        yanit = self._gonder("/api/chat", govde)
        return Akis(yanit, model, self.adres, self)

    def sinir(self, sistem: str) -> "Akis":
        """Önbellek sınırı isteği (istem.sinir_istemi; tek token üretir)."""
        akis = self.cevir([{"role": "system", "content": sistem}, {"role": "user", "content": "."}],
                          secenek={"num_predict": 1})
        self.onbellek_sinirda = True
        return akis

    def onden_yukle(self, sistem: str) -> "Yanit":
        """Modeli belleğe alır ve sistem istemini önbelleğe işler; ilk çeviri beklemez.
        sistem: istem.sinir_istemi() (önbellek sınırda kalır)."""
        self.onbellek_sinirda = True
        model = self.ayarlar["model"]
        yanit = self._gonder("/api/chat", {
            "model": model,
            "stream": False,
            "think": False,
            "keep_alive": self.ayarlar["keep_alive"],
            "options": {**self._secenekler(), "num_predict": 1},
            "messages": [{"role": "system", "content": sistem}, {"role": "user", "content": "."}],
        })
        return Yanit(yanit, model, self.adres, self)

    def modeller(self) -> "Yanit":
        """Kurulu yerel modeller. tamam sinyali ad listesi taşır; bulut modelleri dışarıda kalır."""
        yanit = self._ag.get(self._istek("/api/tags"))
        sonuc = Yanit(yanit, self.ayarlar["model"], self.adres, self)
        sonuc.donustur = lambda d: sorted(m["name"] for m in d.get("models", []) if not m.get("remote_host"))
        return sonuc


class Yanit(QObject):
    """Tek parça JSON yanıtı dönen istek."""

    tamam = Signal(object)
    hata = Signal(str)

    def __init__(self, yanit: QNetworkReply, model: str, adres: str, parent):
        super().__init__(parent)
        self._yanit, self._model, self._adres = yanit, model, adres
        self.donustur = lambda d: d
        yanit.finished.connect(self._bitti)

    def iptal(self) -> None:
        self._yanit.finished.disconnect(self._bitti)
        self._yanit.abort()
        self._yanit.deleteLater()
        self.deleteLater()

    def _bitti(self) -> None:
        yanit = self._yanit
        govde = bytes(yanit.readAll())
        mesaj = _yanit_hatasi(yanit, govde, self._model, self._adres)
        yanit.deleteLater()
        self.deleteLater()
        if mesaj:
            self.hata.emit(mesaj)
            return
        try:
            self.tamam.emit(self.donustur(json.loads(govde)))
        except (ValueError, KeyError, TypeError, AttributeError):
            self.hata.emit("Ollama'dan beklenmeyen bir yanıt geldi.")


class Akis(QObject):
    """Akışlı /api/chat isteği. Her içerik parçası `parca` ile gelir."""

    parca = Signal(str)
    bitti = Signal()
    hata = Signal(str)

    def __init__(self, yanit: QNetworkReply, model: str, adres: str, parent):
        super().__init__(parent)
        self._yanit, self._model, self._adres = yanit, model, adres
        self._tampon = b""
        self._iptal = False
        self._sonlandi = False
        yanit.readyRead.connect(self._oku)
        yanit.finished.connect(self._kapandi)

    def durdur(self) -> None:
        if not self._sonlandi:
            self._iptal = True
            self._sonlandi = True
            self._yanit.abort()

    def _sonlan(self, hata: str | None = None) -> None:
        if self._sonlandi:
            return
        self._sonlandi = True
        if hata:
            self.hata.emit(hata)
        else:
            self.bitti.emit()

    def _http_hatasi(self) -> bool:
        durum = self._yanit.attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute)
        return bool(durum and durum >= 400)

    def _oku(self) -> None:
        self._tampon += bytes(self._yanit.readAll())
        if self._http_hatasi():
            return  # gövde hata mesajıdır; bitince işlenir
        *satirlar, self._tampon = self._tampon.split(b"\n")
        for satir in satirlar:
            self._isle(satir)

    def _isle(self, satir: bytes) -> None:
        if self._sonlandi or not satir.strip():
            return
        try:
            veri = json.loads(satir)
        except ValueError:
            return
        if "error" in veri:
            self._sonlan(hata_metni(str(veri["error"]), self._model))
            self._yanit.abort()
            return
        icerik = veri.get("message", {}).get("content", "")
        if icerik:
            self.parca.emit(icerik)
        if veri.get("done"):
            self._sonlan()

    def _kapandi(self) -> None:
        yanit = self._yanit
        yanit.deleteLater()
        self.deleteLater()
        if self._sonlandi:
            return
        self._tampon += bytes(yanit.readAll())
        mesaj = _yanit_hatasi(yanit, self._tampon, self._model, self._adres)
        if mesaj:
            self._sonlan(mesaj)
            return
        self._isle(self._tampon)
        self._sonlan()
