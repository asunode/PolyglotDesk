"""Kaynak ile çeviri arasında kodla yapılan biçim denetimi (modele bırakılmaz).

- `bos_satirlari_duzelt`: kaynakta olmayan boş satırları kaldırır; satır sayısı tutuyorsa
  boş satırları kaynaktaki yerlerine koyar.
- `denetle`: kaybolan **kalın** / *italik* işaretlerini, kalın yazının yerini (olumsuzluk vurgusu
  Türkçede olumsuz fiile, İngilizcede "not"a gider) ve satır yapısı farklarını bulur.
  Bulunanlar Detaylı Çevir'in denetim geçişinde modele açıkça bildirilir.
- Kalın yazı düzeltmesi (hızlı çeviride de): model metni yeniden yazmaz; yalnız çeviriden birebir alınmış
  parçaları söyler, `**` işaretlerini `kalin_uygula` koyar. Kaynakta kalın olan olumsuzlukta kod önce kendisi
  dener (`kalin_kodla`): kaynaktaki kaçıncı olumsuzluksa çevirideki aynı sıradaki olumsuzluk kalın olur.
"""

import re

_KALIN = re.compile(r"\*\*(.+?)\*\*|__(.+?)__", re.S)
_ITALIK = re.compile(r"(?<![*\w])\*(?![*\s])(.+?)(?<![*\s])\*(?![*\w])|(?<![_\w])_(?![_\s])(.+?)(?<![_\s])_(?![_\w])", re.S)
_LISTE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s")
_OLUMSUZ_EN = re.compile(r"(?<!\w)(?:not|never|no|cannot|none|nothing|nobody|neither|nor|\w+n['’]t)(?!\w)", re.I)
# Türkçe olumsuzluk: yüklem olan "değil", "yok" ("yoksa" değil) ya da fiildeki olumsuzluk eki (-ma/-me + y, -maz/-mez,
# -madı, -mam, -masın, -mıyor, -amaz). Ad-fiil ekleri sayılmaz: "-maya/-meye", "-mayı/-meyi" (yönelme/belirtme),
# "-mak" (mastar), "-malı", "-ması/-mesini/-mesine".
_OLUMSUZ_TR_FIIL = re.compile(
    r"(?<!\w)(?:değil\w*|yok(?:tu[rk]?|muş|um|uz)?(?!\w)"
    r"|(?!tamam|hamam)\w{2,}?(?:m[ae](?:z|d[ıiuü]|y(?![ae](?!\w)|[ıi](?!\w))|m)[\w'’]*"
    r"|m[ae]s[ıi]n(?:l[ae]r)?(?!\w)|m[ıiuü]yor[\w'’]*|[ae]m[ae][zd][\w'’]*))", re.I)
# Ayrı olumsuzluk kelimeleri (asla, hiç): olumsuzluk sayılır ama kalın yazı olumsuz fiile gider.
_OLUMSUZ_TR = re.compile(r"(?<!\w)(?:asla|hiç|hiçbir)(?!\w)|" + _OLUMSUZ_TR_FIIL.pattern, re.I)
_KELIME = re.compile(r"[^\W_]+(?:['’][^\W_]+)?")


def olumsuz_mu(metin: str, dil: str) -> bool:
    return bool((_OLUMSUZ_TR if dil == "tr" else _OLUMSUZ_EN).search(metin))


def olumsuz_sayisi(metin: str, dil: str) -> int:
    return len(_olumsuz_yerler(kalinsiz(metin), dil))


def _olumsuz_yerler(metin: str, dil: str) -> list[tuple[int, int]]:
    """Kalın yazının gideceği olumsuzluk kelimeleri: İngilizcede not/never/don't…, Türkçede olumsuz fiil."""
    if dil == "tr":
        return [m.span() for m in _KELIME.finditer(metin) if _OLUMSUZ_TR_FIIL.fullmatch(m.group())]
    return [m.span() for m in _OLUMSUZ_EN.finditer(metin)]


def _dolu_satirlar(metin: str) -> list[str]:
    return [s for s in metin.split("\n") if s.strip()]


def bos_satirlari_duzelt(kaynak: str, ceviri: str) -> str:
    kaynak_satirlar = kaynak.split("\n")
    dolu_kaynak = _dolu_satirlar(kaynak)
    dolu_ceviri = _dolu_satirlar(ceviri)
    if len(dolu_kaynak) == len(dolu_ceviri):
        # Satırlar birebir: boş satırlar kaynaktaki yerlerine
        sira = iter(dolu_ceviri)
        return "\n".join(next(sira) if s.strip() else "" for s in kaynak_satirlar)
    if len(dolu_kaynak) == len(kaynak_satirlar):
        # Kaynakta hiç boş satır yok: çevirideki boş satırlar modelin eklemesi
        return "\n".join(dolu_ceviri)
    return ceviri


def _isaretler(desen: re.Pattern, metin: str) -> list[str]:
    return [next(g for g in m.groups() if g is not None) for m in desen.finditer(metin)]


def kalinsiz(metin: str) -> str:
    """Kalın yazı işaretleri kaldırılmış metin (italik ve diğer biçim kalır)."""
    return _KALIN.sub(lambda m: next(g for g in m.groups() if g is not None), metin)


def kalin_parcalari(metin: str) -> list[str]:
    return _isaretler(_KALIN, metin)


def kalin_sorunlari(kaynak: str, ceviri: str, kaynak_dil: str | None = None, hedef_dil: str | None = None) -> list[str]:
    """Kalın yazı kaybı ve (diller verilirse) olumsuzlukta kalının yanlış yeri."""
    k, c = kalin_parcalari(kaynak), kalin_parcalari(ceviri)
    if len(c) < len(k):
        ornek = ", ".join(f"**{x}**" for x in k)
        return [f"The source has {len(k)} bold passage(s) ({ornek}) but the draft has {len(c)}."]
    sorunlar = []
    if kaynak_dil and hedef_dil:
        for x, y in zip(k, c):
            if olumsuz_mu(x, kaynak_dil) and not _olumsuz_yerler(y, hedef_dil):
                yer = "the negated Turkish verb" if hedef_dil == "tr" else "the English negation word (not, never, don't …)"
                sorunlar.append(f"The bold passage **{x}** in the source is a negation, but in the draft the bold is on "
                                f"**{y}**, which is not {yer}.")
    return sorunlar


def kalin_kodla(kaynak: str, ceviri: str, kaynak_dil: str, hedef_dil: str) -> str | None:
    """Kaynaktaki kalın parçaların hepsi olumsuzluksa kalın yazıyı kod yerleştirir: kaynakta kaçıncı olumsuzluk
    kalınsa çeviride aynı sıradaki olumsuzluk kelimesi kalın olur. Olumsuzluk sayıları tutmazsa None (model karar verir)."""
    if not kaynak_dil or not hedef_dil:
        return None
    k = kalin_parcalari(kaynak)
    if not k or not all(olumsuz_mu(x, kaynak_dil) for x in k):
        return None
    # Kaynakta kalın parçaların yerleri (işaretsiz metinde)
    duz, yerler, konum = "", [], 0
    for m in _KALIN.finditer(kaynak):
        duz += kaynak[konum:m.start()]
        icerik = next(g for g in m.groups() if g is not None)
        yerler.append((len(duz), len(duz) + len(icerik)))
        duz += icerik
        konum = m.end()
    duz += kaynak[konum:]
    k_olumsuz = _olumsuz_yerler(duz, kaynak_dil)
    hedef = kalinsiz(ceviri)
    c_olumsuz = _olumsuz_yerler(hedef, hedef_dil)
    if not k_olumsuz or len(k_olumsuz) != len(c_olumsuz):
        return None
    siralar = set()
    for bas, son in yerler:
        sira = next((i for i, (a, b) in enumerate(k_olumsuz) if a < son and bas < b), None)
        if sira is None:
            return None
        siralar.add(sira)
    for i in sorted(siralar, reverse=True):
        a, b = c_olumsuz[i]
        hedef = f"{hedef[:a]}**{hedef[a:b]}**{hedef[b:]}"
    return hedef


def kalin_uygula(ceviri: str, parcalar, kaynak: str, kaynak_dil: str, hedef_dil: str) -> tuple[str | None, str]:
    """Modelin söylediği parçaları (çeviriden birebir) kalın yapar. Dönen: (yeni metin ya da None, neden)."""
    k = kalin_parcalari(kaynak)
    if not isinstance(parcalar, list) or not all(isinstance(p, str) for p in parcalar):
        return None, "parça listesi yok"
    parcalar = [p.replace("**", "").strip() for p in parcalar]
    if len(parcalar) != len(k) or not all(parcalar):
        return None, f"kaynakta {len(k)} kalın parça var, {len(parcalar)} parça verildi"
    hedef = kalinsiz(ceviri)
    secilen: list[tuple[int, int]] = []
    for x, p in zip(k, parcalar):
        if len(_KELIME.findall(p)) > max(3, 2 * len(_KELIME.findall(x)) + 1):
            return None, f"parça çok uzun: {p}"
        yer = next((m.span() for m in re.finditer(rf"(?<!\w){re.escape(p)}(?!\w)", hedef)
                    if not any(a < m.end() and m.start() < b for a, b in secilen)), None)
        if yer is None:
            return None, f"parça çeviride birebir yok: {p}"
        if kaynak_dil and hedef_dil and olumsuz_mu(x, kaynak_dil) and not _olumsuz_yerler(p, hedef_dil):
            return None, f"kaynakta kalın olan olumsuzluk, parça olumsuzluk değil: {p}"
        secilen.append(yer)
    for a, b in sorted(secilen, reverse=True):
        hedef = f"{hedef[:a]}**{hedef[a:b]}**{hedef[b:]}"
    return hedef, ""


def denetle(kaynak: str, ceviri: str, kaynak_dil: str | None = None, hedef_dil: str | None = None) -> list[str]:
    """Bulunan biçim sorunları (modele gidecek İngilizce cümleler). Sorun yoksa boş liste.
    Diller verilirse kalın yazının yeri de denetlenir."""
    sorunlar = kalin_sorunlari(kaynak, ceviri, kaynak_dil, hedef_dil)
    k, c = _isaretler(_ITALIK, kaynak), _isaretler(_ITALIK, ceviri)
    if len(c) < len(k):
        ornek = ", ".join(f"*{x}*" for x in k)
        sorunlar.append(f"The source has {len(k)} italic passage(s) ({ornek}) but the draft has {len(c)}. "
                        "Mark the corresponding words in the translation as italic with *…*.")
    dk, dc = _dolu_satirlar(kaynak), _dolu_satirlar(ceviri)
    if len(dk) != len(dc):
        sorunlar.append(
            f"The source has {len(dk)} non-empty lines but the draft has {len(dc)}. "
            "Keep the line structure of the source: one translated line for each source line."
        )
    lk = sum(bool(_LISTE.match(s)) for s in dk)
    lc = sum(bool(_LISTE.match(s)) for s in dc)
    if lk != lc:
        sorunlar.append(f"The source has {lk} list items but the draft has {lc}. Keep the list markers.")
    return sorunlar
