"""Terim sözlüğü: ~/.config/cevirmen/sozluk.txt

Düz metin dosyasıdır (biçim dosyanın başında anlatılır). Her çeviride dosyanın
değişip değişmediğine bakılır; değiştiyse yeniden okunur.
"""

import hashlib
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from . import ayarlar

VARSAYILAN = Path(__file__).parent / "sozluk_varsayilan.txt"
# Önceki sürümlerin varsayılan sözlükleri. Kullanıcının kopyası bunlardan biriyle aynıysa
# (hiç düzenlenmemişse) yeni varsayılanla değiştirilir; düzenlenmiş kopyaya dokunulmaz.
ESKI_VARSAYILANLAR = {
    "68fa459e2b390b46f8cc8949080020a52cda41f328c869715f69fc4907c84f3e",  # Adım 3
    "cc411a828b01fe19cfef853ae7c72366cd7635c1503bf8aecf56969a476d07c2",  # Adım 4–6
    "c0f06a919d2b5b10fb13aa8addff78a48e5086f72e2fdb260dacc2948d818895",  # Adım 7–8
}

# Türkçe ad ekleri (çoğul, iyelik, hâl, ilgi, ek-fiil). Terimden sonra yalnız bunlar gelebilir:
# "kartı", "karta", "kartlarındaki" eşleşir; "kartal", "kartvizit", "kayıtsız" eşleşmez.
_EKLER = sorted("""
lar ler ları leri
ım im um üm ın in un ün ı i u ü m n
sı si su sü ımız imiz umuz ümüz mız miz muz müz ınız iniz unuz ünüz nız niz nuz nüz
yı yi yu yü nı ni nu nü a e ya ye na ne
da de ta te nda nde dan den tan ten ndan nden
nın nin nun nün la le yla yle ca ce ça çe ki
dır dir dur dür tır tir tur tür dı di du dü tı ti tu tü ydı ydi ydu ydü
""".split(), key=len, reverse=True)
_TR_EK = r"(?:['’]?(?:" + "|".join(_EKLER) + r"){0,4})"


@dataclass(frozen=True)
class Terim:
    kaynak: str
    hedef: str | None  # None: İngilizce kalsın

    def __str__(self) -> str:
        return self.kaynak if self.hedef is None else f"{self.kaynak} → {self.hedef}"


def dosya_yolu() -> Path:
    return ayarlar.dosya_yolu().with_name("sozluk.txt")


def _kucult(metin: str) -> str:
    return metin.replace("İ", "i").lower()


def _bolum(baslik: str) -> str | None:
    b = _kucult(baslik).replace(" ", "").replace("->", "→")
    teknik = "-teknik" if "teknik" in b else ""
    if "tetikleyici" in b:
        return "tetik"
    if "kalsın" in b or "kalsin" in b:
        return "kalsin"
    if b.startswith(("ingilizce→türkçe", "ingilizce→turkce", "en→tr")):
        return "en-tr" + teknik
    if b.startswith(("türkçe→ingilizce", "turkce→ingilizce", "tr→en")):
        return "tr-en" + teknik
    return None


def _kisaltma(terim: str) -> bool:
    return terim.upper() == terim and any(c.isalpha() for c in terim)


def _desen(terim: str, kaynak_dil: str) -> re.Pattern:
    govde = r"\s+".join(re.escape(p) for p in terim.split())
    if _kisaltma(terim):
        # Kısaltma: birebir; ardından harf gelmesin (GPIO9, OTA'yı olur; OTAMATIK olmaz).
        return re.compile(rf"(?<!\w){govde}(?![^\W\d_])")
    if kaynak_dil == "tr":
        return re.compile(rf"(?<!\w){_kucult(govde)}{_TR_EK}(?!\w)")
    return re.compile(rf"(?<!\w){_kucult(govde)}(?:s|es|'s|’s)?(?!\w)")


def _yerler(yazimlar: tuple[str, ...], metin: str, kucuk: str, kaynak_dil: str) -> list[tuple[int, int]]:
    """Terimin metindeki geçişleri (başlangıç, bitiş)."""
    return [m.span() for y in yazimlar for m in _desen(y, kaynak_dil).finditer(metin if _kisaltma(y) else kucuk)]


def _icinde(yer: tuple[int, int], uzun: tuple[int, int]) -> bool:
    return uzun[0] <= yer[0] and yer[1] <= uzun[1] and uzun[1] - uzun[0] > yer[1] - yer[0]


class Sozluk:
    def __init__(self, yol: Path | None = None):
        self.yol = yol or dosya_yolu()
        self._imza = None
        self._kalsin: list[str] = []
        self._tetik: list[str] = []    # teknik bağlam tetikleyicileri
        # yön → [(yazımlar, hedef)]; çiftler yalnız yazıldıkları yönde çalışır.
        # "-teknik" yönleri yalnız metinde bir teknik bağlam tetikleyicisi varsa
        self._ciftler: dict[str, list[tuple[tuple[str, ...], str]]] = {}

    def hazirla(self) -> Path:
        """Kullanıcı sözlüğü yoksa (ya da hiç düzenlenmemiş eski varsayılansa) varsayılanı kopyalar."""
        if self.yol.exists() and self.yol != VARSAYILAN:
            try:
                if hashlib.sha256(self.yol.read_bytes()).hexdigest() in ESKI_VARSAYILANLAR:
                    shutil.copyfile(VARSAYILAN, self.yol)
            except OSError:
                pass
        if not self.yol.exists():
            self.yol.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(VARSAYILAN, self.yol)
        return self.yol

    def guncelle(self) -> None:
        try:
            durum = self.hazirla().stat()
        except OSError:
            return
        imza = (durum.st_mtime_ns, durum.st_size)
        if imza == self._imza:
            return
        self._imza = imza
        self._oku(self.yol.read_text(encoding="utf-8", errors="replace"))

    def _oku(self, metin: str) -> None:
        self._kalsin, self._tetik = [], []
        self._ciftler = {}
        bolum, tetik_bolumu = None, False
        for satir in metin.splitlines():
            satir = satir.strip()
            if not satir or satir.startswith("#"):
                continue
            if satir.startswith("[") and satir.endswith("]"):
                bolum = _bolum(satir[1:-1])
                tetik_bolumu |= bolum == "tetik"
                continue
            if bolum == "kalsin":
                self._kalsin.append(satir)
            elif bolum == "tetik":
                self._tetik.append(satir)
            elif bolum and "=" in satir:
                kaynak, hedef = (p.strip() for p in satir.split("=", 1))
                yazimlar = tuple(y.strip() for y in kaynak.split("|") if y.strip())
                if yazimlar and hedef:
                    self._ciftler.setdefault(bolum, []).append((yazimlar, hedef))
        if not tetik_bolumu and self.yol != VARSAYILAN:
            # Tetikleyici bölümü olmayan (eski, düzenlenmiş) sözlük: paketteki varsayılan liste kullanılır
            varsayilan = Sozluk(VARSAYILAN)
            varsayilan._oku(VARSAYILAN.read_text(encoding="utf-8"))
            self._tetik = varsayilan._tetik

    def teknik_mi(self, metin: str, kaynak_dil: str) -> bool:
        """Metinde bir teknik bağlam tetikleyicisi (donanım/elektronik terimi) geçiyor mu."""
        kucuk = _kucult(metin)
        return any(_yerler((t,), metin, kucuk, kaynak_dil) for t in self._tetik)

    def eslesenler(self, metin: str, kaynak_dil: str, hedef_dil: str) -> list[Terim]:
        """Metinde geçen sözlük terimleri (sözlükteki sırayla).

        Bir terimin geçişlerinden biri daha uzun bir terimin içindeyse ("SD kartı" içindeki "kart") o terim
        gönderilmez; metinde ayrıca tek başına geçse de karar modele bırakılır."""
        kucuk = _kucult(metin)
        yon = f"{kaynak_dil}-{hedef_dil}"
        adaylar: list[tuple[Terim, list]] = []
        goruldu = set()

        def ekle(yazimlar: tuple[str, ...], hedef: str | None) -> None:
            yerler = _yerler(yazimlar, metin, kucuk, kaynak_dil)
            if yerler and _kucult(yazimlar[0]) not in goruldu:
                goruldu.add(_kucult(yazimlar[0]))
                adaylar.append((Terim(yazimlar[0], hedef), yerler))

        for t in self._kalsin:
            ekle((t,), None)
        for yazimlar, hedef in self._ciftler.get(yon, []):
            ekle(yazimlar, hedef)
        # Gündelik anlamı da olan kelimeler (kart, kayıt, board): yalnız bir teknik bağlam tetikleyicisi de geçiyorsa
        if self.teknik_mi(metin, kaynak_dil):
            for yazimlar, hedef in self._ciftler.get(yon + "-teknik", []):
                ekle(yazimlar, hedef)
        tum_yerler = [y for _, yerler in adaylar for y in yerler]
        return [t for t, yerler in adaylar
                if not any(_icinde(y, u) for y in yerler for u in tum_yerler)]
