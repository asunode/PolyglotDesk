"""Model çıktısından çeviri dışındaki ekleri ayıklar.

İstem modele yalnız çeviriyi yazmasını söyler; bu modül yine de gelebilecek
"İşte çeviri:" gibi giriş cümlelerini, çeviriyi saran tırnakları ve sona
eklenen "Not:" paragraflarını çıkarır. Kaynakta tırnak varsa tırnaklara dokunmaz. Akış sırasında her parçada ham metnin
tamamı yeniden temizlenir, bu yüzden kararlar sonradan düzelebilir.
"""

import re

_TIRNAKLAR = {'"': '"', "'": "'", "“": "”", "”": "”", "‘": "’", "«": "»", "»": "«", "„": "“"}

# İlk satırda, "çeviri" sözcüğünü içeren ve iki noktayla biten giriş cümlesi.
_GIRIS = re.compile(r"\A[^\n]{0,100}?(?:translat|çevir|tercüme)[^\n]{0,60}?:[ \t]*\n*", re.IGNORECASE)
_GIRIS_BASLARI = (
    "here", "sure", "certainly", "of course", "translation", "below", "the translation",
    "işte", "tabii", "elbette", "aşağıda", "çeviri", "türkçe", "ingilizce", "english", "turkish",
)
_CEVIRI_LAFI = re.compile(r"translat|çevir|tercüme", re.IGNORECASE)

# Ayrı satırda başlayan açıklama: "Not:", "(Note: ...", "Açıklama:" ...
_NOT = re.compile(
    r"\n[ \t]*\n?[ \t]*[(\[]?[ \t]*(?:\*\*)?(?:notes?|not|açıklama|explanation|"
    r"translator'?s note|çevirmen(?:in)? notu)(?:\*\*)?[ \t]*:",
    re.IGNORECASE,
)


def _giris_olabilir(metin: str) -> bool:
    """Akış sürerken metin henüz bitmemiş bir giriş cümlesi olabilir mi?"""
    if not metin or "\n" in metin or ":" in metin or len(metin) > 100 or re.search(r"[.!?]", metin):
        return False
    bas = metin.replace("İ", "i").lower()
    return any(bas.startswith(s) or s.startswith(bas) for s in _GIRIS_BASLARI)


def temizle(ham: str, kaynak: str, son: bool) -> str:
    """Ham model çıktısından gösterilecek çeviriyi üretir.

    son=False akış sürerken çağrılır: giriş cümlesi olabilecek başlangıç
    netleşene kadar boş döner.
    """
    metin = ham.lstrip()
    kaynak = kaynak.strip()

    if not _CEVIRI_LAFI.search(kaynak):
        eslesme = _GIRIS.match(metin)
        if eslesme:
            metin = metin[eslesme.end():].lstrip()
        elif not son and _giris_olabilir(metin):
            return ""

    if not _NOT.search(kaynak):
        eslesme = _NOT.search(metin)
        if eslesme:
            metin = metin[:eslesme.start()]

    # Saran tırnak yalnız kaynakta hiç tırnak yoksa modelin eklemesidir.
    acilis = metin[:1]
    kaynakta_tirnak = any(t in kaynak for t in '"“”«»„')
    if acilis in _TIRNAKLAR and not kaynakta_tirnak and not kaynak.startswith(acilis):
        kapanis = _TIRNAKLAR[acilis]
        metin = metin[1:]
        govde = metin.rstrip()
        if govde.endswith(kapanis) and not kaynak.endswith(kapanis):
            metin = govde[:-1]

    return metin.strip() if son else metin
