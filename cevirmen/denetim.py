"""Denetim geçişinin kararını uygulama ve güvenlik kontrolü (kodla; modele bırakılmaz).

Model metni yeniden yazmaz: JSON ile "hata yok" ya da hata listesi verir. Her hata taslaktan birebir
alınmış kısa bir parça ve onun düzeltmesidir. Hata yoksa taslak olduğu gibi kalır. Kalın yazı ayrıca
"bold" listesiyle (taslaktan birebir parçalar) verilir; `**` işaretlerini kod koyar (`bicim.kalin_uygula`).
Her düzeltme uygulanmadan önce denetlenir; şu durumlarda geri alınır:
- biçim düzeltmesi kelimeleri değiştiriyorsa,
- yalnız unvan ya da hitap ekliyor, çıkarıyor ya da değiştiriyorsa (Bay, Hanım, Sayın, Dr., Mr. …; hata sayılmaz),
- metinde yan yana tekrarlanan bir kelime oluşturuyorsa ("Do not not start"),
- taslaktaki olumsuzluk sayısı kaynaktakine zaten ulaşmışken olumsuzluk ekliyorsa,
- İngilizce çıktıya Türkçe kesme işaretli ek ekliyorsa ("log'lar"),
- kaynak dildeki bir kelimeyi çevirmeden ekliyorsa (sözlük terimi, sayı, kısaltma ve kod hariç; "Ms."),
- taslakta olmayan ve kaynakta sözlük karşılığı bulunmayan bir kelime ekliyorsa
  (olumsuzluk düzeltmelerinde bu son denetim yapılmaz: olumsuzluk eki kelimeyi değiştirir).
"""

import json
import re
from dataclasses import dataclass, field
from typing import Callable

from .bicim import kalinsiz, olumsuz_sayisi

TURLER = {"meaning", "negation", "missing", "addition", "format"}
_KELIME = re.compile(r"[^\W_]+(?:['’][^\W_]+)?")
# İngilizce kısaltmalar dışında kesme işaretinden sonra gelen harfler Türkçe ektir.
_TR_EKI = re.compile(r"[^\W_]['’](?!(?:s|t|re|ve|ll|d|m)\b)[a-zçğıöşü]+", re.I)
# Unvan ve hitaplar (küçük harf, noktasız): bunları eklemek, çıkarmak ya da değiştirmek hata sayılmaz.
UNVANLAR = {"bay", "bayan", "bey", "beyefendi", "hanım", "hanımefendi", "sayın", "sevgili", "dr", "prof", "doç",
            "mr", "mrs", "ms", "miss", "mx", "sir", "madam", "madame", "dear"}


@dataclass
class Uygulama:
    metin: str
    karar: dict | str                                  # çözülmüş JSON ya da "geçersiz yanıt: …"
    uygulanan: list[dict] = field(default_factory=list)
    geri_alinan: list[dict] = field(default_factory=list)   # güvenlik kontrolünün reddettikleri (neden ile)
    uygulanmayan: list[dict] = field(default_factory=list)  # taslakta bulunamayan / değişiklik getirmeyen


def _kucult(metin: str, dil: str) -> str:
    if dil == "tr":
        metin = metin.replace("I", "ı").replace("İ", "i")
    return metin.lower()


def _kelimeler(metin: str, dil: str) -> list[str]:
    return [_kucult(re.split(r"['’]", m.group())[0], dil) for m in _KELIME.finditer(metin)]


def _isaretsiz(metin: str) -> str:
    return " ".join(re.sub(r"[*_]", "", metin).split())


def unvan_degisikligi(eski: str, yeni: str, dil: str) -> bool:
    """Düzeltme yalnız unvan/hitap kelimelerini ekliyor, çıkarıyor ya da değiştiriyor mu."""
    e, y = _kelimeler(eski, dil), _kelimeler(yeni, dil)
    if e == y:
        return False
    return [w for w in e if w not in UNVANLAR] == [w for w in y if w not in UNVANLAR]


def karari_coz(ham: str) -> dict | str:
    try:
        karar = json.loads(ham)
    except ValueError:
        return f"geçersiz yanıt: {ham[:200]}"
    if not isinstance(karar, dict) or not isinstance(karar.get("errors", []), list):
        return f"geçersiz yanıt: {ham[:200]}"
    return karar


def _tekrarlar(metin: str, dil: str) -> set[str]:
    """Yan yana iki kez geçen kelimeler."""
    k = _kelimeler(kalinsiz(metin), dil)
    return {a for a, b in zip(k, k[1:]) if a == b}


def guvenlik(hata: dict, kaynak: str, kaynak_dil: str, hedef_dil: str, izinli: set[str],
             karsilik: Callable[[str], bool] | None, islev: set[str], once: str = "", sonra: str = "") -> str | None:
    """Düzeltme güvenli değilse nedenini döner. once/sonra: düzeltmeden önceki ve sonraki tüm metin."""
    tur, eski, yeni = hata.get("type"), hata.get("draft_text", ""), hata.get("corrected_text", "")
    if tur == "format" and _isaretsiz(eski) != _isaretsiz(yeni):
        return "biçim düzeltmesi kelimeleri değiştiriyor"
    if unvan_degisikligi(eski, yeni, hedef_dil):
        return "unvan/hitap değişikliği hata sayılmaz"
    if once and sonra:
        tekrar = _tekrarlar(sonra, hedef_dil) - _tekrarlar(once, hedef_dil)
        if tekrar:
            return f"yan yana tekrarlanan kelime oluşuyor: {', '.join(sorted(tekrar))}"
        k, o, s = olumsuz_sayisi(kaynak, kaynak_dil), olumsuz_sayisi(once, hedef_dil), olumsuz_sayisi(sonra, hedef_dil)
        if o >= k and s > o:
            return f"olumsuzluk ekleniyor ama taslakta kaynaktaki kadar olumsuzluk zaten var ({k})"
    if hedef_dil == "en":
        yeni_ek = set(m.group() for m in _TR_EKI.finditer(yeni)) - set(m.group() for m in _TR_EKI.finditer(eski))
        if yeni_ek:
            return f"İngilizce çıktıya Türkçe kesme işaretli ek eklendi: {', '.join(sorted(yeni_ek))}"
    eski_k = set(_kelimeler(eski, hedef_dil))
    kaynak_k = set(_kelimeler(kaynak, kaynak_dil))
    eklenen = [w for w in dict.fromkeys(_kelimeler(yeni, hedef_dil)) if w not in eski_k]
    for w in eklenen:
        kopya = w in kaynak_k or any(k.startswith(w) and len(k) - len(w) <= 2 and len(w) >= 3 for k in kaynak_k)
        if kopya and w not in izinli and not any(c.isdigit() for c in w):
            ozgun = re.search(rf"(?<!\w){re.escape(w)}", yeni, re.I)
            if not (ozgun and ozgun.group().isupper() and len(w) > 1):
                return f"kaynak dildeki kelime çevrilmeden eklendi: {w}"
    if tur in ("negation", "format") or karsilik is None:
        return None
    for w in eklenen:
        if len(w) <= 3 or w in islev or w in kaynak_k:
            continue
        if any(e[:3] == w[:3] for e in eski_k):  # aynı kelimenin başka çekimi
            continue
        if not karsilik(w):
            return f"taslakta olmayan ve kaynakta karşılığı bulunmayan kelime eklendi: {w}"
    return None


def uygula(taslak: str, kaynak: str, ham_karar: str, kaynak_dil: str, hedef_dil: str, izinli: set[str],
           karsilik: Callable[[str], bool] | None = None, islev: set[str] = frozenset()) -> Uygulama:
    karar = karari_coz(ham_karar)
    sonuc = Uygulama(taslak, karar)
    if isinstance(karar, str) or not karar.get("has_errors") or not karar.get("errors"):
        return sonuc  # hata yok (ya da cevap okunamadı): taslak olduğu gibi kalır
    for hata in karar["errors"]:
        if not isinstance(hata, dict):
            continue
        eski, yeni = hata.get("draft_text", ""), hata.get("corrected_text", "")
        if hata.get("type") not in TURLER:
            sonuc.uygulanmayan.append({**hata, "neden": "hata türü geçersiz"})
        elif not eski or eski == yeni:
            sonuc.uygulanmayan.append({**hata, "neden": "değişiklik getirmiyor"})
        elif eski not in sonuc.metin:
            sonuc.uygulanmayan.append({**hata, "neden": "taslakta bulunamadı"})
        else:
            sonra = sonuc.metin.replace(eski, yeni, 1)
            neden = guvenlik(hata, kaynak, kaynak_dil, hedef_dil, izinli, karsilik, islev, sonuc.metin, sonra)
            if neden:
                sonuc.geri_alinan.append({**hata, "neden": neden})
            else:
                sonuc.metin = sonra
                sonuc.uygulanan.append(hata)
    return sonuc
