"""çevirmen bilgi paketini PostgreSQL'e yükler (Wiktionary + Tatoeba, tr-en).

Kullanım (indirilen dosyalar güvenilmeyen veri sayıldığı için -I ile):
    python3 -I veritabani/yukle.py --kaynak ~/.cache/cevirmen/indirilen
        [--host 127.0.0.1] [--port 5432] [--vt cevirmen] [--sahip cevirmen] [--okur cevirmen_okur]

Kaynak dizininde beklenen dosyalar:
    raw-wiktextract-data.jsonl.gz   https://kaikki.org/dictionary/rawdata.html
    tur_sentences.tsv.bz2, eng_sentences.tsv.bz2, tur-eng_links.tsv.bz2
                                    https://downloads.tatoeba.org/exports/per_language/

Sahip rolle (varsayılan cevirmen) bağlanır; şifreyi libpq okur (~/.pgpass ya da PGPASSWORD). Bağlantı
ayarlarının varsayılanları ortam değişkenlerinden alınır: POLYGLOTDESK_PG_HOST, POLYGLOTDESK_PG_PORT,
POLYGLOTDESK_PG_DB, POLYGLOTDESK_PG_OWNER (sahip rol), POLYGLOTDESK_PG_USER (yalnız okuma rolü). Veri önce `bilgi_yeni`
şemasına yüklenir, dizinler kurulur, cevirmen_okur'a okuma yetkisi verilir, sonra tek
işlemde `bilgi` ile yer değiştirir. Yükleme yarıda kalırsa eski veri olduğu gibi kalır.

Veri olduğu gibi kullanılır: hiçbir kayıt test ya da kontrol cümlelerine göre seçilmez.
Bozuk kayıtlar tek tek değil, genel kurallarla ayıklanır (bkz. AYIKLAMA).
"""

import argparse
import bz2
import gzip
import json
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path

import psycopg
import psycopg.sql
from psycopg.conninfo import make_conninfo

TR_ATLA = {"name", "character", "symbol", "punct", "romanization", "suffix", "prefix", "infix",
           "interfix", "circumfix", "affix", "contraction"}
# Kalıp/deyim sayılan çok kelimeli maddeler; birleşik adlar (ör. "video game") kalıp değildir.
# Çok kelimeli edat ve bağlaçlar ("as for", "so that") dilbilgisi birimidir; onlar da alınır.
EN_KALIP_TUR = {"phrase", "proverb", "prep_phrase", "intj", "prep", "conj"}
TR_KALIP_TUR = {"phrase", "proverb", "intj", "verb", "adv", "conj", "postp"}
DEYIM_ETIKETI = {"idiomatic", "figuratively"}
FORM_ATLA = {"table-tags", "inflection-template", "romanization", "class"}
SIKLIK_SAKLA = 2000     # dil başına en sık kelime sayısı (sıra ile)
# Kaba, argo, müstehcen anlam etiketleri (Wiktionary)
KABA = ["vulgar", "slang", "offensive", "derogatory", "slur", "obscene"]

KAYNAKLAR = [
    ("wiktionary", "Wiktionary (İngilizce Vikisözlük; kaikki.org / wiktextract çıkarımı)",
     "CC BY-SA 4.0 (ayrıca GFDL)", "https://kaikki.org/dictionary/rawdata.html"),
    ("tatoeba", "Tatoeba (Türkçe–İngilizce cümle çiftleri)", "CC BY 2.0 FR", "https://tatoeba.org"),
]

SEMA = """
CREATE EXTENSION IF NOT EXISTS pg_trgm;
DROP SCHEMA IF EXISTS bilgi_yeni CASCADE;
CREATE SCHEMA bilgi_yeni;
SET search_path = bilgi_yeni, public;

CREATE TABLE kaynak (
    id smallint PRIMARY KEY,
    kod text UNIQUE NOT NULL,
    ad text NOT NULL,
    lisans text NOT NULL,
    url text NOT NULL,
    veri_tarihi text NOT NULL,
    yukleme_zamani timestamptz NOT NULL DEFAULT now()
);

-- Türkçe maddelerin anlamları (İngilizce açıklamalı). Bir satır = bir anlam.
CREATE TABLE tr_anlam (
    kelime text NOT NULL,
    tur text NOT NULL,
    etimoloji smallint NOT NULL,
    sira smallint NOT NULL,
    anlam text NOT NULL,
    etiketler text[],
    konular text[],
    ornek_tr text,
    ornek_en text,
    kaynak_id smallint NOT NULL REFERENCES kaynak
);

-- Çekimli biçim → madde (Wiktionary çekim tabloları; iki dil)
CREATE TABLE bicim (dil text NOT NULL, bicim text NOT NULL, kelime text NOT NULL);

-- İngilizce maddelerdeki Türkçe çeviriler
CREATE TABLE en_ceviri (
    en_kelime text NOT NULL,
    tur text NOT NULL,
    anlam text NOT NULL,
    tr_kelime text NOT NULL,
    etiketler text[],
    kaynak_id smallint NOT NULL REFERENCES kaynak
);

-- Kalıplar ve deyimler (iki yönde)
CREATE TABLE kalip (
    id serial PRIMARY KEY,
    dil text NOT NULL CHECK (dil IN ('tr', 'en')),
    ifade text NOT NULL,
    ifade_kucuk text NOT NULL,
    tur text NOT NULL,
    anlam text NOT NULL,
    karsilik text,
    notlar text,
    anahtarlar text[],       -- kelime başına madde anahtarı (bkz. kelime_anahtari)
    kaynak_id smallint NOT NULL REFERENCES kaynak
);

-- Örnek cümle çiftleri
CREATE TABLE cumle (
    tr_id integer PRIMARY KEY,
    tr text NOT NULL,
    en_id integer NOT NULL,
    en text NOT NULL,
    kaynak_id smallint NOT NULL REFERENCES kaynak
);

-- Tatoeba'da kelimelerin geçtiği cümle sayısı (en sık SIKLIK_SAKLA kelime)
CREATE TABLE siklik (dil text NOT NULL, kelime text NOT NULL, sayi integer NOT NULL, sira integer NOT NULL,
                     PRIMARY KEY (dil, kelime));

-- Snowball kökü: yalnız sözlükte bulunmayan deyim kelimeleri için yedek anahtar. Durak kelimede NULL.
CREATE FUNCTION kok(dil text, kelime text) RETURNS text
LANGUAGE sql IMMUTABLE PARALLEL SAFE AS $$
    SELECT (ts_lexize(CASE dil WHEN 'tr' THEN 'turkish_stem'::regdictionary
                               ELSE 'english_stem'::regdictionary END, kelime))[1]
$$;
"""

# İngilizce deyimlerde yer tutucular: iyelik sözcükleri birbirinin yerine geçer ("one's" = my/your/…),
# "someone/something" herhangi bir kelimeyi tutar (anahtar NULL → eşleşmede boşluk sayılır).
EN_IYELIK = ["one's", "ones", "my", "your", "his", "her", "its", "our", "their"]
EN_YER_TUTUCU = ["someone", "somebody", "something", "oneself", "someone's", "somebody's", "something's", "somewhere"]

TURETILMIS = """
SET search_path = bilgi_yeni, public;
SET maintenance_work_mem = '512MB';
CREATE INDEX ON bicim (dil, bicim);
CREATE INDEX ON bicim (dil, kelime);
CREATE INDEX ON tr_anlam (kelime);
CREATE INDEX ON en_ceviri (lower(en_kelime));

-- Sözlük maddeleri (iki dil): bir kelime madde başlığıysa yalnız kendisiyle eşleşir.
CREATE TABLE madde AS
SELECT DISTINCT 'tr'::text AS dil, kelime FROM tr_anlam
UNION SELECT 'en', lower(en_kelime) FROM en_ceviri
UNION SELECT dil, kelime FROM bicim;
CREATE INDEX ON madde (dil, kelime);
"""

AYIKLAMA = """
SET search_path = bilgi_yeni, public;
-- Kural 1: Ünlem, kalıp ve özel ad dışındaki maddelerde karşılık bir terim olmalı; ! ya da ? içeren ya da
--          birden çok kelimeden oluşup noktayla biten satır örnek cümle parçasıdır ("1." gibi sıra sayıları kalır).
-- Kural 2: kelimelerinin yarıdan fazlası Türkçe sözlükte (madde + çekim) bulunmayan ve Türkçe olmayan bir
--          İngilizce işlev kelimesi içeren karşılık İngilizce metin parçasıdır ("We sat on the bench").
CREATE TEMP TABLE ayiklanan AS
WITH k AS (
    SELECT e.ctid AS satir, regexp_replace(t, '[''’].*$', '') AS t
      FROM en_ceviri e,
           regexp_split_to_table(lower(replace(replace(e.tr_kelime, 'İ', 'i'), 'I', 'ı')), '[^[:alpha:]''’]+') t
     WHERE length(regexp_replace(t, '[''’].*$', '')) > 1),
o AS (
    SELECT satir, count(*) AS n,
           count(*) FILTER (WHERE NOT EXISTS (SELECT 1 FROM madde m WHERE m.dil = 'tr' AND m.kelime = k.t)) AS bilinmeyen,
           bool_or(t = ANY (ARRAY['the','an','of','to','in','on','at','is','are','was','were','be','we','you',
                                  'he','she','they','it','this','that','would','will','and','or','for','with','by',
                                  'from','as','his','her','their','our'])
                   AND NOT EXISTS (SELECT 1 FROM madde m WHERE m.dil = 'tr' AND m.kelime = k.t)) AS ingilizce
      FROM k GROUP BY satir)
SELECT e.ctid AS satir, e.en_kelime, e.tr_kelime,
       CASE WHEN o.ingilizce AND o.bilinmeyen * 2 > o.n THEN 'ingilizce_parca' ELSE 'noktalama' END AS neden
  FROM en_ceviri e LEFT JOIN o ON o.satir = e.ctid
 WHERE (e.tur NOT IN ('intj', 'phrase', 'proverb', 'prep_phrase', 'name')
        AND e.tr_kelime ~ '[!?]|\\S\\s+\\S.*\\.\\s*$')
    OR (o.ingilizce AND o.bilinmeyen * 2 > o.n);
DELETE FROM en_ceviri WHERE ctid IN (SELECT satir FROM ayiklanan);
"""

TURETILMIS_2 = """
SET search_path = bilgi_yeni, public;

-- Bir kelimenin madde anahtarı: madde başlığıysa kendisi; değilse çekim tablosundaki maddesi (ilk üç
-- harfi tutan ve en uzun olan); ikisi de yoksa '~' + Snowball kökü. İngilizce iyelik sözcükleri '<poss>'.
-- Metin tarafında kelimenin bütün maddeleri anahtar sayıldığı için deyim yine bulunur.
CREATE FUNCTION kelime_anahtari(dil text, w text) RETURNS text
LANGUAGE sql STABLE PARALLEL SAFE AS $$
    SELECT CASE
        WHEN dil = 'en' AND w = ANY (%(iyelik)s) THEN '<poss>'
        WHEN dil = 'en' AND w = ANY (%(yer_tutucu)s) THEN NULL
        WHEN EXISTS (SELECT 1 FROM bilgi_yeni.madde m WHERE m.dil = $1 AND m.kelime = w) THEN w
        ELSE coalesce(
            (SELECT b.kelime FROM bilgi_yeni.bicim b WHERE b.dil = $1 AND b.bicim = w
              ORDER BY (left(b.kelime, 3) = left(w, 3)) DESC, length(b.kelime) DESC, b.kelime LIMIT 1),
            '~' || coalesce(bilgi_yeni.kok(dil, w), w))
    END
$$;

UPDATE kalip k SET anahtarlar = (
    SELECT array_agg(kelime_anahtari(k.dil, t.w) ORDER BY t.n)
      FROM regexp_split_to_table(k.ifade_kucuk, '[^[:alnum:]''’çğıöşü]+') WITH ORDINALITY AS t(w, n)
     WHERE t.w <> '');
DELETE FROM kalip WHERE cardinality(array_remove(anahtarlar, NULL)) < 2;
CREATE INDEX ON kalip USING gin (anahtarlar);
CREATE INDEX ON kalip (dil);

-- Çok anlamlı Türkçe kelimeler: en az iki farklı anlamı olanlar. Uzaklık: etimoloji ve içerik türü sayısı.
CREATE TABLE tr_cok_anlamli AS
SELECT kelime,
       count(DISTINCT anlam) AS anlam_sayisi,
       count(DISTINCT etimoloji) AS etimoloji_sayisi,
       count(DISTINCT tur) FILTER (WHERE tur NOT IN ('conj','postp','particle','det','pron','num','article','prep')) AS tur_sayisi,
       jsonb_agg(jsonb_build_object('tur', tur, 'etimoloji', etimoloji, 'anlam', anlam,
                                    'etiketler', etiketler, 'konular', konular)
                 ORDER BY etimoloji, sira) AS anlamlar
  FROM tr_anlam
 GROUP BY kelime
HAVING count(DISTINCT anlam) >= 2;
CREATE INDEX ON tr_cok_anlamli (kelime);

-- Çok anlamlı İngilizce kelimeler (anlamı belirtilmiş Türkçe çevirileriyle).
-- Uzaklık: anlamların Türkçe karşılık kümeleri birbirinden ayrık mı.
-- kaba: anlam açıklaması kaba/argo diyorsa ya da bütün Türkçe karşılıkları kaba/argo etiketliyse.
CREATE TABLE en_cok_anlamli AS
SELECT lower(en_kelime) AS kelime,
       count(DISTINCT anlam) AS anlam_sayisi,
       count(DISTINCT trler[1]) AS karsilik_sayisi,
       jsonb_agg(jsonb_build_object('tur', tur, 'anlam', anlam, 'tr', trler, 'kaba', kaba) ORDER BY tur, anlam) AS anlamlar
  FROM (SELECT en_kelime, tur, anlam, array_agg(DISTINCT tr_kelime ORDER BY tr_kelime) AS trler,
               anlam ~* %(kaba_desen)s OR bool_and(coalesce(etiketler && %(kaba)s, false)) AS kaba
          FROM en_ceviri WHERE anlam <> '' AND en_kelime !~ '\\s'
         GROUP BY en_kelime, tur, anlam) s
 GROUP BY lower(en_kelime)
HAVING count(DISTINCT anlam) >= 2;
CREATE INDEX ON en_cok_anlamli (kelime);

-- Madde sıklığı (Tatoeba): yalnız tek maddeye bağlanan biçimler sayılır ("bitti" yalnız bitmek'e bağlıysa).
-- Bir biçim birden çok maddeye bağlanıyorsa (ayın → ay / ayı) arama en sık maddeyi seçer.
-- Ara tablolar ANALYZE edilir (yeni tablolarda istatistik yokken planlayıcı çok yavaş bir plan seçiyordu).
CREATE TEMP TABLE kelime_sayi AS
SELECT 'tr'::text AS dil, w, count(*)::integer AS n
  FROM cumle, regexp_split_to_table(lower(replace(replace(tr, 'İ', 'i'), 'I', 'ı')), '[^[:alpha:]''’]+') x,
       regexp_replace(x, '[''’].*$', '') w
 WHERE w <> '' GROUP BY w
UNION ALL
SELECT 'en', w, count(*)
  FROM cumle, regexp_split_to_table(lower(en), '[^[:alpha:]''’]+') x, regexp_replace(x, '[''’].*$', '') w
 WHERE w <> '' GROUP BY w;
CREATE TEMP TABLE bicim_madde AS
SELECT dil, kelime AS bicim, kelime FROM madde UNION SELECT dil, bicim, kelime FROM bicim;
ANALYZE kelime_sayi;
ANALYZE bicim_madde;
CREATE TEMP TABLE okuma AS
SELECT t.dil, t.w, t.n, m.kelime FROM kelime_sayi t JOIN bicim_madde m ON m.dil = t.dil AND m.bicim = t.w;
ANALYZE okuma;
CREATE TABLE madde_siklik AS
SELECT o.dil, o.kelime, sum(o.n)::integer AS sayi
  FROM okuma o JOIN (SELECT dil, w FROM okuma GROUP BY dil, w HAVING count(*) = 1) tek USING (dil, w)
 GROUP BY o.dil, o.kelime;
CREATE INDEX ON madde_siklik (dil, kelime);
DROP TABLE kelime_sayi, bicim_madde, okuma;

CREATE INDEX cumle_tr_trgm ON cumle USING gist (tr gist_trgm_ops);
CREATE INDEX cumle_en_trgm ON cumle USING gist (en gist_trgm_ops);
"""


def kucult(metin: str, dil: str) -> str:
    if dil == "tr":
        metin = metin.replace("I", "ı").replace("İ", "i")
    return metin.lower()


def gunluk(mesaj: str) -> None:
    print(time.strftime("%H:%M:%S"), mesaj, flush=True)


def wiktionary(dsn: str, yol: Path) -> dict:
    """Tek geçişte dört tabloya yazar. psycopg bir bağlantıda aynı anda tek COPY'ye izin
    verdiği için her tablo kendi bağlantısını kullanır (şema önceden işlenmiş olmalı)."""
    sayac = {"tr_madde": 0, "tr_anlam": 0, "tr_bicim": 0, "en_bicim": 0, "en_ceviri": 0, "kalip_tr": 0, "kalip_en": 0}
    en_kalip: dict[tuple, dict] = {}
    b1, b2, b3, b4 = (psycopg.connect(dsn) for _ in range(4))
    with b1, b2, b3, b4, \
         b1.cursor().copy("COPY bilgi_yeni.tr_anlam (kelime, tur, etimoloji, sira, anlam, etiketler, konular, ornek_tr, ornek_en, kaynak_id) FROM STDIN") as c_anlam, \
         b2.cursor().copy("COPY bilgi_yeni.bicim (dil, bicim, kelime) FROM STDIN") as c_bicim, \
         b3.cursor().copy("COPY bilgi_yeni.en_ceviri (en_kelime, tur, anlam, tr_kelime, etiketler, kaynak_id) FROM STDIN") as c_ceviri, \
         b4.cursor().copy("COPY bilgi_yeni.kalip (dil, ifade, ifade_kucuk, tur, anlam, karsilik, notlar, kaynak_id) FROM STDIN") as c_kalip:
        with gzip.open(yol, "rt", encoding="utf-8") as f:
            for n, satir in enumerate(f, 1):
                if n % 2_000_000 == 0:
                    gunluk(f"  wiktionary satır {n:,}: {sayac}")
                if ('"lang_code": "tr"' not in satir and '"code": "tr"' not in satir
                        and not ('"lang_code": "en"' in satir and _en_kalip_adayi(satir))):
                    continue
                d = json.loads(satir)
                kod = d.get("lang_code")
                if kod == "tr":
                    _tr_madde(d, sayac, c_anlam, c_bicim, c_kalip)
                elif kod == "en":
                    _en_madde(d, sayac, c_ceviri, c_bicim, en_kalip)
        for (ifade, tur), k in en_kalip.items():
            if not k["anlam"]:
                k["anlam"] = "; ".join(dict.fromkeys(k["tr"]))[:500]
            karsilik = "; ".join(dict.fromkeys(k["tr"])) or None
            c_kalip.write_row(("en", ifade, kucult(ifade, "en"), tur, k["anlam"], karsilik, k["notlar"] or None, 1))
            sayac["kalip_en"] += 1
    return sayac


def _en_kalip_adayi(satir: str) -> bool:
    """Türkçe çevirisi olmayan İngilizce satırlardan kalıp/deyim olabilecekleri (ucuz ön eleme)."""
    return '"idiomatic"' in satir or '"figuratively"' in satir or any(f'"pos": "{t}"' in satir for t in EN_KALIP_TUR)


def _anlam_metni(s: dict) -> str | None:
    if s.get("form_of") or s.get("alt_of"):
        return None
    etiketler = set(s.get("tags") or [])
    if etiketler & {"form-of", "alt-of", "abbreviation-of", "misspelling"}:
        return None
    glosses = s.get("glosses") or s.get("raw_glosses")
    if not glosses:
        return None
    return glosses[-1].strip()[:300]


def _bicimler(d: dict, dil: str, kucuk: str, c_bicim) -> int:
    sayi, goruldu = 0, {kucuk}
    for f in d.get("forms") or []:
        bicim = (f.get("form") or "").strip()
        if not bicim or " " in bicim or set(f.get("tags") or []) & FORM_ATLA:
            continue
        b = kucult(bicim, dil)
        if b not in goruldu:
            goruldu.add(b)
            c_bicim.write_row((dil, b, kucuk))
            sayi += 1
    return sayi


def _tr_madde(d: dict, sayac: dict, c_anlam, c_bicim, c_kalip) -> None:
    kelime = d.get("word", "").strip()
    tur = d.get("pos") or ""
    if not kelime or tur in TR_ATLA:
        return
    etim = int(d.get("etymology_number") or 0)
    anlamlar = []
    for sira, s in enumerate(d.get("senses") or []):
        anlam = _anlam_metni(s)
        if not anlam:
            continue
        ornek_tr = ornek_en = None
        for o in s.get("examples") or []:
            en = o.get("english") or o.get("translation")
            if o.get("text") and en:
                ornek_tr, ornek_en = o["text"][:300], en[:300]
                break
        c_anlam.write_row((kelime, tur, etim, sira, anlam, s.get("tags"), s.get("topics"), ornek_tr, ornek_en, 1))
        anlamlar.append((anlam, s.get("tags") or []))
        sayac["tr_anlam"] += 1
    if not anlamlar:
        return
    sayac["tr_madde"] += 1
    kucuk = kucult(kelime, "tr")
    deyim = any(set(e) & DEYIM_ETIKETI for _, e in anlamlar)
    if " " in kelime:
        if tur in TR_KALIP_TUR or deyim:
            notlar = sorted({t for _, e in anlamlar for t in e if t in
                             {"idiomatic", "figuratively", "colloquial", "informal", "formal", "proverb",
                              "slang", "dated", "humorous", "vulgar", "literally"}})
            c_kalip.write_row(("tr", kelime, kucuk, tur, "; ".join(a for a, _ in anlamlar[:3])[:500], None,
                               ", ".join(notlar) or None, 1))
            sayac["kalip_tr"] += 1
        return
    sayac["tr_bicim"] += _bicimler(d, "tr", kucuk, c_bicim)


def _en_madde(d: dict, sayac: dict, c_ceviri, c_bicim, en_kalip: dict) -> None:
    kelime = d.get("word", "").strip()
    tur = d.get("pos") or ""
    if not kelime:
        return
    senses = d.get("senses") or []
    kalip = " " in kelime and (tur in EN_KALIP_TUR or any(set(s.get("tags") or []) & DEYIM_ETIKETI for s in senses))
    trler = []
    for t in d.get("translations") or []:
        if t.get("code") != "tr" and t.get("lang_code") != "tr":
            continue
        tr = (t.get("word") or "").strip()
        if not tr:
            continue
        c_ceviri.write_row((kelime, tur, (t.get("sense") or "")[:300], tr, t.get("tags"), 1))
        sayac["en_ceviri"] += 1
        trler.append(tr)
    if " " not in kelime:
        sayac["en_bicim"] += _bicimler(d, "en", kucult(kelime, "en"), c_bicim)
    if not kalip:
        return
    # İngilizce kalıp/deyim: Türkçe çevirisi olmasa da anlamıyla alınır
    anlamlar = [a for a in (_anlam_metni(s) for s in senses) if a]
    if not anlamlar and not trler:
        return
    k = en_kalip.setdefault((kelime, tur), {"anlam": "", "tr": [], "notlar": ""})
    k["tr"] += trler
    if anlamlar and not k["anlam"]:
        k["anlam"] = "; ".join(anlamlar[:3])[:500]
        etiket = sorted({t for s in senses for t in (s.get("tags") or [])
                         if t in {"idiomatic", "figuratively", "colloquial", "informal", "formal", "slang", "humorous"}})
        k["notlar"] = ", ".join(etiket)


_KELIME = re.compile(r"[^\W_]+(?:['’][^\W_]+)?")


def tatoeba(baglanti, dizin: Path) -> dict:
    def oku(ad: str, dil: str) -> dict[int, str]:
        sonuc = {}
        with bz2.open(dizin / ad, "rt", encoding="utf-8") as f:
            for satir in f:
                p = satir.rstrip("\n").split("\t")
                if len(p) >= 3 and p[1] == dil:
                    sonuc[int(p[0])] = p[2].strip()
        return sonuc

    tr = oku("tur_sentences.tsv.bz2", "tur")
    en = oku("eng_sentences.tsv.bz2", "eng")
    gunluk(f"  tatoeba: {len(tr):,} Türkçe, {len(en):,} İngilizce cümle")
    ciftler: dict[int, int] = {}
    with bz2.open(dizin / "tur-eng_links.tsv.bz2", "rt", encoding="utf-8") as f:
        for satir in f:
            p = satir.split("\t")
            if len(p) < 2:
                continue
            t, e = int(p[0]), int(p[1])
            if t in tr and e in en and (t not in ciftler or e < ciftler[t]):
                ciftler[t] = e
    goruldu = set()
    sayi = 0
    with baglanti.cursor() as cur, cur.copy("COPY bilgi_yeni.cumle (tr_id, tr, en_id, en, kaynak_id) FROM STDIN") as c:
        for t in sorted(ciftler):
            if tr[t] in goruldu:
                continue
            goruldu.add(tr[t])
            c.write_row((t, tr[t], ciftler[t], en[ciftler[t]], 2))
            sayi += 1
    # Sıklık: kelimenin geçtiği cümle sayısı (tüm Tatoeba cümleleri, dil başına)
    with baglanti.cursor() as cur, cur.copy("COPY bilgi_yeni.siklik (dil, kelime, sayi, sira) FROM STDIN") as c:
        for dil, cumleler in (("tr", tr), ("en", en)):
            sayac = Counter()
            for metin in cumleler.values():
                sayac.update({kucult(re.split(r"['’]", m.group())[0], dil) for m in _KELIME.finditer(metin)})
            for sira, (kelime, n) in enumerate(sayac.most_common(SIKLIK_SAKLA), 1):
                c.write_row((dil, kelime, n, sira))
    return {"cumle": sayi}


def _sql_dizi(ogeler: list[str]) -> str:
    return "ARRAY[" + ",".join("'" + x.replace("'", "''") + "'" for x in ogeler) + "]"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kaynak", type=Path, required=True)
    ortam = os.environ.get
    ap.add_argument("--host", default=ortam("POLYGLOTDESK_PG_HOST", "127.0.0.1"))
    ap.add_argument("--port", default=ortam("POLYGLOTDESK_PG_PORT", "5432"))
    ap.add_argument("--vt", default=ortam("POLYGLOTDESK_PG_DB", "cevirmen"))
    ap.add_argument("--sahip", default=ortam("POLYGLOTDESK_PG_OWNER", "cevirmen"), help="veritabanının sahibi olan rol")
    ap.add_argument("--okur", default=ortam("POLYGLOTDESK_PG_USER", "cevirmen_okur"), help="uygulamanın yalnız okuma rolü")
    ap.add_argument("--wiktionary-tarihi", default="enwiktionary dökümü 2026-10-01, kaikki.org çıkarımı 2026-10-30")
    ap.add_argument("--tatoeba-tarihi", default="Tatoeba dışa aktarımı 2026-11-14")
    a = ap.parse_args()
    dsn = make_conninfo(host=a.host, port=a.port, dbname=a.vt, user=a.sahip, application_name="polyglotdesk_yukle")
    okur = psycopg.sql.Identifier(a.okur)
    baslangic = time.time()
    with psycopg.connect(dsn) as baglanti:
        gunluk(f"bağlandı: {a.vt}")
        # Ara şema işlenir; yarıda kalan yükleme yalnız bilgi_yeni'yi bırakır, bilgi'ye dokunmaz.
        baglanti.execute(SEMA)
        tarihler = {"wiktionary": a.wiktionary_tarihi, "tatoeba": a.tatoeba_tarihi}
        for i, (kod, ad, lisans, url) in enumerate(KAYNAKLAR, 1):
            baglanti.execute("INSERT INTO bilgi_yeni.kaynak (id, kod, ad, lisans, url, veri_tarihi) VALUES (%s,%s,%s,%s,%s,%s)",
                             (i, kod, ad, lisans, url, tarihler[kod]))
        baglanti.commit()
        gunluk("wiktionary okunuyor (akış hâlinde)…")
        sayac = wiktionary(dsn, a.kaynak / "raw-wiktextract-data.jsonl.gz")
        gunluk(f"wiktionary: {sayac}")
        gunluk("tatoeba okunuyor…")
        gunluk(f"tatoeba: {tatoeba(baglanti, a.kaynak)}")
        gunluk("madde ve biçim dizinleri…")
        baglanti.execute(TURETILMIS)
        gunluk("bozuk kayıtlar ayıklanıyor (genel kurallar)…")
        baglanti.execute(AYIKLAMA)
        ayiklanan = baglanti.execute("SELECT neden, count(*) FROM ayiklanan GROUP BY neden ORDER BY 1").fetchall()
        ornekler = baglanti.execute("SELECT en_kelime, tr_kelime, neden FROM ayiklanan ORDER BY en_kelime").fetchall()
        gunluk(f"ayıklanan: {ayiklanan}; örnekler: {ornekler}")
        gunluk("kalıp anahtarları, çok anlamlı kelimeler, cümle dizinleri…")
        baglanti.execute(TURETILMIS_2 % {"iyelik": _sql_dizi(EN_IYELIK), "yer_tutucu": _sql_dizi(EN_YER_TUTUCU),
                                         "kaba": _sql_dizi(KABA),
                                         "kaba_desen": "'\\m(" + "|".join(KABA) + ")\\M'"})
        baglanti.execute("ANALYZE")
        if baglanti.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (a.okur,)).fetchone():
            for komut in ("GRANT USAGE ON SCHEMA bilgi_yeni TO {}", "GRANT SELECT ON ALL TABLES IN SCHEMA bilgi_yeni TO {}",
                          "GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA bilgi_yeni TO {}"):
                baglanti.execute(psycopg.sql.SQL(komut).format(okur))
        else:
            gunluk(f"uyarı: {a.okur} rolü yok; okuma yetkisi verilmedi (veritabani/okur_rol.sh)")
        baglanti.execute("DROP SCHEMA IF EXISTS bilgi_eski CASCADE")
        if baglanti.execute("SELECT 1 FROM pg_namespace WHERE nspname = 'bilgi'").fetchone():
            baglanti.execute("ALTER SCHEMA bilgi RENAME TO bilgi_eski")
        baglanti.execute("ALTER SCHEMA bilgi_yeni RENAME TO bilgi")
        # Fonksiyon gövdeleri şema adını içeriyor; yer değiştirmeden sonra bilgi şemasına göre yeniden tanımlanır.
        govde = baglanti.execute("SELECT pg_get_functiondef('bilgi.kelime_anahtari(text,text)'::regprocedure)").fetchone()[0]
        baglanti.execute(govde.replace("bilgi_yeni.", "bilgi."))
        baglanti.execute("DROP SCHEMA IF EXISTS bilgi_eski CASCADE")
        baglanti.commit()
        ozet = baglanti.execute("""
            SELECT (SELECT count(*) FROM bilgi.tr_anlam), (SELECT count(*) FROM bilgi.tr_cok_anlamli),
                   (SELECT count(*) FROM bilgi.bicim WHERE dil = 'tr'), (SELECT count(*) FROM bilgi.bicim WHERE dil = 'en'),
                   (SELECT count(*) FROM bilgi.en_ceviri), (SELECT count(*) FROM bilgi.en_cok_anlamli),
                   (SELECT count(*) FROM bilgi.kalip WHERE dil = 'tr'), (SELECT count(*) FROM bilgi.kalip WHERE dil = 'en'),
                   (SELECT count(*) FROM bilgi.cumle), pg_size_pretty(pg_database_size(current_database()))""").fetchone()
    etiketler = ["tr_anlam", "tr_cok_anlamli", "tr_bicim", "en_bicim", "en_ceviri", "en_cok_anlamli", "kalip_tr", "kalip_en",
                 "cumle", "vt_boyutu"]
    gunluk("bitti: " + ", ".join(f"{e}={v}" for e, v in zip(etiketler, ozet)) + f" ({time.time() - baslangic:.0f} s)")


if __name__ == "__main__":
    sys.exit(main())
