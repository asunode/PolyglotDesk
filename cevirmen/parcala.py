"""Metni anlamı bozmadan çeviri parçalarına böler.

- Boş satırla ayrılan paragraflar ayrı bloktur; liste, alıntı ve kod bloğu bölünmez.
- Kısa bloklar EN_AZ karaktere ulaşana kadar birleştirilir (her istekteki sabit
  bekleme toplam süreyi şişirmesin).
- EN_COK karakteri aşan tek paragraf cümle sınırlarından bölünür.
- ``` ile çevrili kod blokları çevrilmez, olduğu gibi kalır.

Parçaların `icerik + ayrac` birleşimi kaynak metni birebir verir.
"""

import re
from dataclasses import dataclass

EN_AZ = 400
EN_COK = 2000

_KOD = re.compile(r"^[ \t]*```[^\n]*\n.*?^[ \t]*```[ \t]*$", re.M | re.S)
_BOS_SATIR = re.compile(r"(\n(?:[ \t]*\n)+)")
_CUMLE_SONU = re.compile(r"(?<=[.!?…])(\s+)(?=\S)")
_LISTE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s")


@dataclass
class Parca:
    icerik: str
    ayrac: str = ""        # parçadan sonra gelen boşluk (satır sonları)
    cevrilsin: bool = True


def _tur(blok: str) -> str:
    ilk = blok.lstrip("\n").split("\n", 1)[0]
    if _LISTE.match(ilk):
        return "liste"
    if ilk.lstrip().startswith(">"):
        return "alinti"
    if ilk.lstrip().startswith("#"):
        return "baslik"
    return "metin"


def _bloklar(metin: str) -> list[list]:
    """[icerik, ayrac, tur] listesi; kod blokları tur='kod'."""
    bloklar: list[list] = []
    on_ek = ""

    def ekle(icerik: str, tur: str) -> None:
        nonlocal on_ek
        govde = icerik.rstrip()
        bosluk = icerik[len(govde):]
        bas = govde[:len(govde) - len(govde.lstrip("\n"))]  # baştaki satır sonları ayraca gider
        govde = govde[len(bas):]
        if bloklar:
            bloklar[-1][1] += bas
        else:
            on_ek += bas
        if not govde:
            if bloklar:
                bloklar[-1][1] += bosluk
            else:
                on_ek += bosluk
            return
        bloklar.append([govde, bosluk, tur])

    def bolge(metin_parcasi: str) -> None:
        nonlocal on_ek
        for i, p in enumerate(_BOS_SATIR.split(metin_parcasi)):
            if i % 2:  # ayraç
                if bloklar:
                    bloklar[-1][1] += p
                else:
                    on_ek += p
            else:
                ekle(p, _tur(p))

    konum = 0
    for m in _KOD.finditer(metin):
        bolge(metin[konum:m.start()])
        ekle(m.group(), "kod")
        konum = m.end()
    bolge(metin[konum:])
    if on_ek:
        bloklar.insert(0, ["", on_ek, "bosluk"])
    return bloklar


def _uzunu_bol(icerik: str, ayrac: str) -> list[list]:
    """EN_COK'u aşan paragrafı cümle sınırlarından böler."""
    parcalar = _CUMLE_SONU.split(icerik)
    sonuc: list[list] = []
    for i in range(0, len(parcalar), 2):
        cumle = parcalar[i]
        bosluk = parcalar[i + 1] if i + 1 < len(parcalar) else ayrac
        if sonuc and len(sonuc[-1][0]) + len(cumle) <= EN_COK:
            sonuc[-1][0] += sonuc[-1][1] + cumle
            sonuc[-1][1] = bosluk
        else:
            sonuc.append([cumle, bosluk])
    return sonuc


def parcala(metin: str) -> list[Parca]:
    parcalar: list[Parca] = []
    acik: Parca | None = None  # birleştirilmekte olan parça

    def kapat() -> None:
        nonlocal acik
        if acik is not None:
            parcalar.append(acik)
            acik = None

    for icerik, ayrac, tur in _bloklar(metin):
        if tur in ("kod", "bosluk"):
            kapat()
            parcalar.append(Parca(icerik, ayrac, cevrilsin=False))
            continue
        alt = _uzunu_bol(icerik, ayrac) if tur == "metin" and len(icerik) > EN_COK else [[icerik, ayrac]]
        for alt_icerik, alt_ayrac in alt:
            if acik is not None and len(acik.icerik) + len(acik.ayrac) + len(alt_icerik) > EN_COK:
                kapat()
            if acik is None:
                acik = Parca(alt_icerik, alt_ayrac)
            else:
                acik.icerik += acik.ayrac + alt_icerik
                acik.ayrac = alt_ayrac
            if len(acik.icerik) >= EN_AZ and tur != "baslik":
                kapat()
    kapat()
    return parcalar
