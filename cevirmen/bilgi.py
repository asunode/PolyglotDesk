"""Bilgi paketi araması: yerel PostgreSQL (`cevirmen` veritabanı, yalnız okuma rolü).

Bir metin için üç tür kayıt döner:
- kalıp/deyim: kelimelerinin madde anahtarları metinde sırayla ve yakın geçenler. Metindeki kelimenin
  anahtarları: kendisi, Wiktionary çekim tablosundaki maddeleri ve (sözlükte bulunmayan deyim kelimeleri
  için) Snowball kökü. Böylece "ipin ucunu da kaçırma" gibi çekimli kullanım "ipin ucunu kaçırmak"ı bulur.
  Türkçe deyimdeki ismin hal eki ve iyeliği metindekiyle uyuşmalı ("başa çıkmak" ≠ "başına çıktı").
  İngilizcede yalnız işlev kelimelerinden oluşan kalıp ("for you", "in one") yalnız Wiktionary onu edat,
  bağlaç ya da zarf sayıyorsa ("as for") ya da Türkçe karşılık veriyorsa ve kelimeleri metinde bitişikse
  gönderilir; "Used other than
  figuratively or idiomatically" açıklaması gönderilmez.
- çok anlamlı kelime: metindeki kelime maddenin kendisiyle birebir aynıysa ya da maddenin çekim
  tablosunda geçiyorsa (yalnız kök benzerliği eşleşme sayılmaz). Birden çok aday madde varsa Tatoeba madde
  sıklığına göre en olası madde seçilir ("bitti" → bitmek, "ayın" → ay); belirsizse kayıt gönderilmez.
  En sık kelimeler aranmaz; önce farklı kökenli ya da uzak anlamlı kelimeler gelir; metin teknikse teknik
  anlamlar öne alınır ve veride hiç teknik anlamı olmayan ad ve sıfatların kaydı gönderilmez.
- örnek cümle: metnin cümlelerine pg_trgm benzerliğiyle en yakın Tatoeba çiftleri; örnek, metin cümlesiyle
  en az bir içerik maddesini paylaşmalı (yalnız harf benzerliği yetmez: "yüz" ≠ "yüzmemeye").
Kaba, argo ya da müstehcen etiketli anlamlar ve kalıplar, metin açıkça o bağlamda değilse gönderilmez.

Sınırlar istemin gereksiz uzamaması için sabittir; hiçbir test cümlesine göre ayarlanmamıştır.
"""

import os
import re
from dataclasses import dataclass, field

from . import ayarlar
from .sozluk import _TR_EK

# Ortam değişkeni → ayar anahtarı. Şifre libpq ile okunur (~/.pgpass ya da PGPASSWORD); burada tutulmaz.
ORTAM = {"POLYGLOTDESK_PG_HOST": "pg_host", "POLYGLOTDESK_PG_PORT": "pg_port",
         "POLYGLOTDESK_PG_DB": "pg_veritabani", "POLYGLOTDESK_PG_USER": "pg_kullanici"}


def baglanti_ayarlari() -> dict:
    """Bağlantı ayarları: ortam değişkenleri > ~/.config/cevirmen/ayarlar.json > varsayılan (127.0.0.1:5432)."""
    a = ayarlar.yukle()
    sonuc = {k: a.get(k, ayarlar.VARSAYILAN[k]) for k in ORTAM.values()}
    sonuc.update({anahtar: os.environ[ad] for ad, anahtar in ORTAM.items() if os.environ.get(ad)})
    return sonuc


def dsn() -> str:
    from psycopg.conninfo import make_conninfo
    a = baglanti_ayarlari()
    return make_conninfo(host=a["pg_host"], port=str(a["pg_port"]), dbname=a["pg_veritabani"], user=a["pg_kullanici"],
                         connect_timeout=3, application_name="polyglotdesk", options="-c statement_timeout=10000")

EN_COK_KALIP = 5
EN_COK_KELIME = 6
EN_COK_ANLAM = 4         # kelime başına
ANLAM_UZUNLUGU = 70      # bir anlam açıklamasının en çok karakteri
KALIP_UZUNLUGU = 160
EN_COK_ORNEK = 5
CUMLE_BASINA_ORNEK = 2
BENZERLIK_ESIGI = 0.3    # pg_trgm varsayılanı
KALIP_PENCERESI = 3      # kalıp kelimeleri arasına girebilecek en fazla kelime
SIK_KELIME_SIRASI = 250  # Tatoeba'da en sık geçen bu kadar kelime çok anlamlı kelime olarak aranmaz
ISLEV_TURLERI = {"conj", "postp", "particle", "det", "pron", "num", "article", "prep"}
GERI_PLAN_ETIKETLERI = {"obsolete", "archaic", "dialectal", "rare", "historical", "Ottoman"}
TEKNIK = re.compile(r"\b(comput\w*|electronic\w*|electric\w*|engineering|software|hardware|program\w*|digital|"
                    r"network\w*|circuit\w*|telecommunication\w*|internet|technolog\w*|signal processing)\b", re.I)
EN_IYELIK = {"one's", "ones", "my", "your", "his", "her", "its", "our", "their"}
SIKLIK_ORANI = 3         # birden çok aday maddede en sık olan, ikinciden en az bu kat sık değilse kelime belirsiz
KABA = {"vulgar", "slang", "offensive", "derogatory", "slur", "obscene"}
KABA_DESEN = r"\m(" + "|".join(sorted(KABA)) + r")\M"
# Metin teknikse, veride hiç teknik anlamı olmayan kelimenin anlam kaydı gönderilmez (fiiller hariç;
# ölçüm: doc/olcum/teknik-kural-olcum.md). Ölçüm betiği bu ayarları değiştirebilir.
TEKNIK_KURALI = True
TEKNIK_KURALI_FIILLER = False
KULLANIM_DISI = re.compile(r"^Used other than figuratively or idiomatically\b", re.I)
# İngilizce işlev kelimeleri (kapalı sınıf): yalnız bunlardan oluşan kalıplar çoğunlukla gürültüdür.
EN_ISLEV = set("""
a an the this that these those i you he she it we they me him her us them my your his its our their one ones
oneself myself yourself himself herself itself ourselves themselves someone something
is am are was were be been being do does did have has had will would shall should can could may might must
of in on at to for from by with about as into onto over under up down out off through than then so and or
but nor if not no all any some each every both either neither what which who whom whose there here
""".split())

KAYNAK_ADI = {1: "Wiktionary", 2: "Tatoeba"}
_KELIME = re.compile(r"[^\W_]+(?:['’][^\W_]+)?")
_CUMLE = re.compile(r"[^.!?…\n]+[.!?…]*")
_EK = re.compile(_TR_EK + r"$")


class BilgiHatasi(Exception):
    pass


@dataclass
class Kayit:
    tur: str        # "kalip" | "anlam" | "ornek" | "sozluk"
    kaynak: str     # "Wiktionary" | "Tatoeba" | "kullanıcı sözlüğü"
    lisans: str
    baslik: str     # ekranda kısa başlık
    istem: str      # modele giden satır
    ayrinti: dict = field(default_factory=dict)


def _kisalt(metin: str, uzunluk: int) -> str:
    return metin if len(metin) <= uzunluk else metin[:uzunluk - 1].rstrip(" ,;") + "…"


def _kucult(metin: str, dil: str) -> str:
    if dil == "tr":
        metin = metin.replace("I", "ı").replace("İ", "i")
    return metin.lower()


def _kelimeler(metin: str, dil: str) -> list[str]:
    # Kesme işaretli biçimde ("reset'i") yalnız ilk kısım alınır.
    return [_kucult(re.split(r"['’]", m.group())[0], dil) for m in _KELIME.finditer(metin)]


def baglan():
    try:
        import psycopg
    except ImportError as e:
        raise BilgiHatasi("PostgreSQL sürücüsü (psycopg) kurulu değil; Detaylı Çevir kullanılamıyor.") from e
    a = baglanti_ayarlari()
    try:
        return psycopg.connect(dsn())
    except psycopg.OperationalError as e:
        raise BilgiHatasi(
            f"Bilgi veritabanına (PostgreSQL, {a['pg_host']}:{a['pg_port']}) ulaşılamıyor. Hızlı çeviri çalışmaya devam "
            "ediyor; Detaylı Çevir için PostgreSQL'in çalıştığından emin olun "
            f"(terminalde: pg_isready -h {a['pg_host']} -p {a['pg_port']})."
        ) from e


def ara(metin: str, kaynak_dil: str, hedef_dil: str, teknik: bool = False) -> list[Kayit]:
    """teknik: metinde sözlükteki bir teknik bağlam tetikleyicisi geçiyor (çok anlamlı kelimelerde teknik anlam
    öne alınır)."""
    import psycopg
    kelimeler = _kelimeler(metin, kaynak_dil)
    if not kelimeler:
        return []
    with baglan() as b:
        try:
            lisans = dict(b.execute("SELECT id, lisans FROM bilgi.kaynak").fetchall())
            sik = {r[0] for r in b.execute("SELECT kelime FROM bilgi.siklik WHERE dil = %s AND sira <= %s",
                                           (kaynak_dil, SIK_KELIME_SIRASI))}
            maddeler = _maddeler(b, kaynak_dil, kelimeler)
            kaba = _kaba_baglam(b, kaynak_dil, kelimeler, maddeler)
            kayitlar, kapsanan = _kaliplar(b, kaynak_dil, kelimeler, maddeler, kaba, lisans)
            kayitlar += _cok_anlamlilar(b, kaynak_dil, kelimeler, maddeler, kapsanan, teknik, kaba, sik, lisans)
            kayitlar += _ornekler(b, kaynak_dil, metin, kelimeler, maddeler, sik, lisans)
        except psycopg.errors.UndefinedTable as e:
            raise BilgiHatasi("Bilgi paketi yüklenmemiş (veritabani/yukle.py çalıştırılmalı).") from e
        except psycopg.Error as e:
            raise BilgiHatasi(f"Bilgi veritabanı sorgusu başarısız: {e}") from e
    return kayitlar


def _en_olasi(adaylar: set, siklik: dict) -> set:
    """Aday maddelerden en olası olan (tek elemanlı küme) ya da belirsizse boş küme."""
    if len(adaylar) <= 1:
        return set(adaylar)
    sirali = sorted(adaylar, key=lambda a: (-siklik.get(a, 0), a))
    ilk, ikinci = siklik.get(sirali[0], 0), siklik.get(sirali[1], 0)
    return {sirali[0]} if ilk > 0 and ilk >= SIKLIK_ORANI * ikinci else set()


def _maddeler(b, dil: str, kelimeler: list[str]) -> list[dict]:
    """Her metin kelimesi için {'tum': bütün aday maddeler, 'secilen': en olası madde (belirsizse boş),
    'kok': Snowball kökü}. Aday: kelime madde başlığıysa kendisi + çekim tablosundaki maddeleri; değilse
    çekim tablosundaki maddeleri + (Türkçede) başlık + ad eki tahmini. Birden çok aday varsa Tatoeba madde
    sıklığı karar verir."""
    benzersiz = sorted(set(kelimeler))
    basliklar = {r[0] for r in b.execute("SELECT kelime FROM bilgi.madde WHERE dil = %s AND kelime = ANY(%s)",
                                         (dil, benzersiz))}
    bicimden: dict[str, set] = {}
    for bicim, kelime in b.execute("SELECT bicim, kelime FROM bilgi.bicim WHERE dil = %s AND bicim = ANY(%s)",
                                   (dil, benzersiz)):
        bicimden.setdefault(bicim, set()).add(kelime)
    ekten: dict[str, set] = {}
    if dil == "tr":
        # Başlık + Türkçe ad eki ("erkenden" = "erken" + "den"); ek kalıbı sozluk._TR_EK ile aynı
        onekler = {w: [w[:i] for i in range(3, len(w)) if _EK.fullmatch(w[i:])] for w in benzersiz}
        tumu = sorted({o for v in onekler.values() for o in v})
        var = {r[0] for r in b.execute("SELECT kelime FROM bilgi.madde WHERE dil = 'tr' AND kelime = ANY(%s)", (tumu,))}
        ekten = {w: {o for o in v if o in var} for w, v in onekler.items()}
    kokler = dict(b.execute("SELECT t, bilgi.kok(%s, t) FROM unnest(%s::text[]) t", (dil, benzersiz)).fetchall())
    tum = {w: ({w} & basliklar) | bicimden.get(w, set()) | ekten.get(w, set()) for w in benzersiz}
    secim = {w: ({w} | bicimden.get(w, set())) if w in basliklar else (bicimden.get(w, set()) | ekten.get(w, set()))
             for w in benzersiz}
    istenen = sorted({a for v in secim.values() if len(v) > 1 for a in v})
    siklik = dict(b.execute("SELECT kelime, sayi FROM bilgi.madde_siklik WHERE dil = %s AND kelime = ANY(%s)",
                            (dil, istenen)).fetchall()) if istenen else {}
    return [{"tum": tum[w], "secilen": _en_olasi(secim[w], siklik), "kok": kokler.get(w)} for w in kelimeler]


def _anahtarlar(dil: str, w: str, m: dict) -> set:
    anahtar = {w} | m["tum"] | {"~" + (m["kok"] or w)}
    if dil == "en" and w in EN_IYELIK:
        anahtar.add("<poss>")
    return anahtar


def _sirali_konumlar(aranan: list, anahtarlar: list[set]) -> list[int] | None:
    """Kalıbın anahtarları metinde bu sırayla, aralarında en fazla KALIP_PENCERESI kelimeyle geçiyor mu?
    None anahtar (yer tutucu: someone, something) atlanır. Dönen: dolu anahtarların metindeki kelime sıraları."""
    dolu = [a for a in aranan if a is not None]
    if not dolu:
        return None
    for bas, k in enumerate(anahtarlar):
        if dolu[0] not in k:
            continue
        konumlar = [bas]
        for a in dolu[1:]:
            sonraki = next((j for j in range(konumlar[-1] + 1, min(len(anahtarlar), konumlar[-1] + 2 + KALIP_PENCERESI))
                            if a in anahtarlar[j]), None)
            if sonraki is None:
                break
            konumlar.append(sonraki)
        if len(konumlar) == len(dolu):
            return konumlar
    return None


def _sirali_yakin(aranan: list, anahtarlar: list[set]) -> tuple[int, int] | None:
    """Dönen: (ilk, son) kelime sırası."""
    konumlar = _sirali_konumlar(aranan, anahtarlar)
    return (konumlar[0], konumlar[-1]) if konumlar else None


# Türkçe ad çekimi: (çoğul) + (iyelik) + (hal). Deyimdeki isimle metindeki aynı hal ve iyelik durumunda olmalı.
_IYELIK = ("ımız imiz umuz ümüz ınız iniz unuz ünüz mız miz muz müz nız niz nuz nüz ları leri "
           "ım im um üm ın in un ün sı si su sü ı i u ü m n").split()
_IYELIK_3 = {"ı", "i", "u", "ü", "sı", "si", "su", "sü", "ları", "leri"}
_HAL = {"yalın": [""], "yönelme": "ya ye na ne a e".split(), "belirtme": "yı yi yu yü nı ni nu nü ı i u ü".split(),
        "bulunma": "nda nde da de ta te".split(), "ayrılma": "ndan nden dan den tan ten".split(),
        "ilgi": "nın nin nun nün ın in un ün".split(), "vasıta": "yla yle la le".split()}


def _ad_cekimleri(ek: str) -> set[tuple[str, bool]]:
    """Ad ekinin olası çözümlemeleri: {(hal, iyelikli mi)}. Çözümlenemezse boş küme."""
    sonuc = set()
    for cogul in ("", "lar", "ler"):
        if not ek.startswith(cogul):
            continue
        kalan = ek[len(cogul):]
        for iyelik in [""] + _IYELIK:
            if not kalan.startswith(iyelik):
                continue
            son = kalan[len(iyelik):]
            for hal, ekler in _HAL.items():
                # "-na, -nda, -nı" kaynaştırması yalnız 3. kişi iyeliğinden sonra gelir ("başına"); ilgi eki serbest
                if son in ekler and not (son.startswith("n") and hal != "ilgi" and iyelik not in _IYELIK_3):
                    sonuc.add((hal, bool(iyelik)))
    return sonuc


def _ad_eki(bicim: str, madde: str) -> str | None:
    """Biçimin madde başlığından sonraki eki (ünsüz yumuşaması ve ünlü düşmesi dahil); fiil ya da uymayan biçimde None."""
    if madde.endswith(("mak", "mek")) or len(madde) < 2:
        return None
    if bicim.startswith(madde):
        return bicim[len(madde):]
    if bicim[:len(madde) - 1] == madde[:-1] and madde[-1] in "pçtk" and bicim[len(madde) - 1:len(madde)] in ("b", "c", "d", "ğ", "g"):
        return bicim[len(madde):]
    if len(madde) >= 3 and madde[-2] in "ıiuü" and bicim.startswith(madde[:-2] + madde[-1]):
        return bicim[len(madde) - 1:]
    return None


def _hal_uyumlu(ifade_kucuk: str, aranan: list, konumlar: list[int], kelimeler: list[str]) -> bool:
    """Türkçe deyimdeki isimlerin hal eki ve iyeliği metindeki kelimeyle uyuşuyor mu (çözümlenemeyen kelime engel olmaz)."""
    deyim = [w for w in re.split(r"[^\w'’]+", ifade_kucuk) if w]
    if len(deyim) != len(aranan) or None in aranan:
        return True
    for dw, madde, konum in zip(deyim, aranan, konumlar):
        if madde.startswith("~"):
            continue
        ek_d, ek_m = _ad_eki(dw, madde), _ad_eki(kelimeler[konum], madde)
        if ek_d is None or ek_m is None:
            continue
        d, m = _ad_cekimleri(ek_d), _ad_cekimleri(ek_m)
        if d and m and not d & m:
            return False
    return True


def _islev_kalibi(ifade: str) -> bool:
    kelimeler = [re.sub(r"['’]s$", "", w) for w in re.split(r"[^\w'’]+", ifade.lower()) if w]
    return bool(kelimeler) and all(w in EN_ISLEV for w in kelimeler)


def _kullanim_disi_temizle(anlam: str) -> str:
    return "; ".join(p for p in anlam.split("; ") if p.strip() and not KULLANIM_DISI.match(p.strip()))


def _kaba_baglam(b, dil: str, kelimeler: list[str], maddeler: list[dict]) -> bool:
    """Metinde bütün anlamları kaba/argo etiketli bir kelime var mı (metin açıkça o bağlamda)."""
    aday = sorted({w for w in kelimeler} | {a for m in maddeler for a in m["secilen"]})
    if dil == "tr":
        sorgu = ("SELECT 1 FROM bilgi.tr_anlam WHERE kelime = ANY(%s) GROUP BY kelime "
                 "HAVING bool_and(coalesce(etiketler && %s, false)) LIMIT 1")
        return b.execute(sorgu, (aday, sorted(KABA))).fetchone() is not None
    sorgu = ("SELECT 1 FROM bilgi.en_ceviri WHERE lower(en_kelime) = ANY(%s) GROUP BY lower(en_kelime) "
             "HAVING bool_and(anlam ~* %s OR coalesce(etiketler && %s, false)) LIMIT 1")
    return b.execute(sorgu, (aday, KABA_DESEN, sorted(KABA))).fetchone() is not None


def _kaliplar(b, dil: str, kelimeler: list[str], maddeler: list[dict], kaba: bool,
              lisans: dict) -> tuple[list[Kayit], set]:
    anahtarlar = [_anahtarlar(dil, w, m) for w, m in zip(kelimeler, maddeler)]
    kume = sorted(set().union(*anahtarlar))
    satirlar = b.execute(
        "SELECT ifade, ifade_kucuk, tur, anlam, karsilik, notlar, anahtarlar, kaynak_id FROM bilgi.kalip "
        "WHERE dil = %s AND array_remove(anahtarlar, NULL) <@ %s::text[] "
        "ORDER BY cardinality(array_remove(anahtarlar, NULL)) DESC, ifade",
        (dil, kume)).fetchall()
    uygun = []
    for ifade, ifade_kucuk, tur, anlam, karsilik, notlar, k, kaynak_id in satirlar:
        islev = dil == "en" and _islev_kalibi(ifade)
        if dil == "en":
            anlam = _kullanim_disi_temizle(anlam)
            if not anlam or (islev and tur not in ("prep", "conj", "adv") and not karsilik):
                continue
        if not kaba and notlar and {n.strip() for n in notlar.split(",")} & KABA:
            continue
        konumlar = _sirali_konumlar(k, anahtarlar)
        if konumlar is None or (dil == "tr" and not _hal_uyumlu(ifade_kucuk, k, konumlar, kelimeler)):
            continue
        if islev and konumlar[-1] - konumlar[0] != len(konumlar) - 1:
            continue  # işlev kelimeleri arasına kelime girmişse kalıp değildir ("for you to" ≠ "for to")
        uygun.append((islev, ifade, tur, anlam, karsilik, notlar, kaynak_id, konumlar))
    # Yalnız işlev kelimelerinden oluşan kalıplar ("as for") içerikli deyimlerden sonra gelir
    uygun.sort(key=lambda x: x[0])
    sonuc, kapsanan = [], set()
    for islev, ifade, tur, anlam, karsilik, notlar, kaynak_id, konumlar in uygun[:EN_COK_KALIP]:
        kapsanan |= set(range(konumlar[0], konumlar[-1] + 1))
        parca = [f'"{ifade}" ({tur}): {_kisalt(anlam, KALIP_UZUNLUGU)}']
        if notlar:
            parca.append(f"[{notlar}]")
        if karsilik:
            parca.append(f"→ Turkish: {karsilik}")
        sonuc.append(Kayit("kalip", KAYNAK_ADI[kaynak_id], lisans[kaynak_id], ifade, " ".join(parca),
                           {"ifade": ifade, "anlam": anlam, "karsilik": karsilik, "notlar": notlar}))
    return sonuc, kapsanan


def _cok_anlamlilar(b, dil: str, kelimeler: list[str], maddeler: list[dict], kapsanan: set,
                    teknik: bool, kaba: bool, sik: set, lisans: dict) -> list[Kayit]:
    # Deyimin içindeki kelimeler, en sık kelimeler, kısa kelimeler ve maddesi belirsiz kelimeler aranmaz.
    adaylar = [(i, w, m["secilen"]) for i, (w, m) in enumerate(zip(kelimeler, maddeler))
               if i not in kapsanan and w not in sik and len(w) >= 3 and m["secilen"]]
    if not adaylar:
        return []
    istenen = sorted({a for _, _, k in adaylar for a in k})
    if dil == "tr":
        satirlar = b.execute("SELECT kelime, anlamlar, etimoloji_sayisi, tur_sayisi FROM bilgi.tr_cok_anlamli "
                             "WHERE kelime = ANY(%s)", (istenen,)).fetchall()
        bilgiler = {k: (a, (e >= 2) * 2 + (t >= 2)) for k, a, e, t in satirlar}
    else:
        satirlar = b.execute("SELECT kelime, anlamlar FROM bilgi.en_cok_anlamli WHERE kelime = ANY(%s)",
                             (istenen,)).fetchall()
        bilgiler = {k: (a, _en_uzaklik(a)) for k, a in satirlar}
    sirali, goruldu = [], set()
    for i, w, maddeler_w in adaylar:
        for madde in sorted(maddeler_w):
            if madde in bilgiler and madde not in goruldu:
                goruldu.add(madde)
                anlamlar, uzaklik = bilgiler[madde]
                sirali.append((-uzaklik, i, madde, anlamlar, w))
    # Önce uzaklık (farklı köken > farklı tür / ayrık karşılıklar), sonra metindeki sıra
    sirali.sort(key=lambda x: (x[0], x[1]))
    sonuc, kullanilan_konum = [], set()
    for eksi_uzaklik, i, kelime, anlamlar, metindeki in sirali:
        if len(sonuc) >= EN_COK_KELIME:
            break
        if i in kullanilan_konum:
            continue  # aynı metin kelimesine ikinci madde eklenmez
        icerik = [a for a in anlamlar if a.get("tur") not in ISLEV_TURLERI]
        if not kaba:
            icerik = [a for a in icerik if not _kaba_mi(a)]
        on_plan = [a for a in icerik if not set(a.get("etiketler") or []) & GERI_PLAN_ETIKETLERI] or icerik
        if len({a["anlam"] for a in on_plan}) < 2:
            continue
        if teknik and TEKNIK_KURALI and not any(_teknik_mi(a) for a in anlamlar):
            fiil = any(a.get("tur") == "verb" for a in on_plan)
            if TEKNIK_KURALI_FIILLER or not fiil:
                continue
        if teknik:
            on_plan = sorted(on_plan, key=lambda a: not _teknik_mi(a))  # kararlı sıralama: teknikler öne
        secilen = on_plan[:EN_COK_ANLAM]
        if dil == "tr":
            metin = "; ".join(f"({a['tur']}) {_kisalt(a['anlam'], ANLAM_UZUNLUGU)}" for a in secilen)
        else:
            metin = "; ".join(f"({a['tur']}) {_kisalt(a['anlam'], ANLAM_UZUNLUGU)} → {', '.join(a['tr'][:3])}"
                              for a in secilen)
        kullanilan_konum.add(i)
        sonuc.append(Kayit("anlam", "Wiktionary", lisans[1], kelime, f"{kelime}: {metin}",
                           {"kelime": kelime, "anlamlar": secilen, "metindeki": metindeki, "uzaklik": -eksi_uzaklik}))
    return sonuc


def _kaba_mi(anlam: dict) -> bool:
    return bool(anlam.get("kaba")) or bool(set(anlam.get("etiketler") or []) & KABA)


def _teknik_mi(anlam: dict) -> bool:
    konular = " ".join(anlam.get("konular") or []) + " " + " ".join(anlam.get("etiketler") or [])
    return bool(TEKNIK.search(konular) or TEKNIK.search(anlam.get("anlam", "")))


def _en_uzaklik(anlamlar: list[dict]) -> int:
    """İngilizce kelimenin anlamlarından en az ikisinin Türkçe karşılık kümeleri ayrıksa 1."""
    kumeler = [set(a.get("tr") or []) for a in anlamlar if a.get("tur") not in ISLEV_TURLERI]
    for i, a in enumerate(kumeler):
        for c in kumeler[i + 1:]:
            if a and c and not a & c:
                return 1
    return 0


def _icerik(w: str, dil: str, sik: set) -> bool:
    return len(w) >= 3 and w not in sik and not (dil == "en" and w in EN_ISLEV)


def _ornekler(b, dil: str, metin: str, kelimeler: list[str], maddeler: list[dict], sik: set,
              lisans: dict) -> list[Kayit]:
    sutun, karsi = ("tr", "en") if dil == "tr" else ("en", "tr")
    # Metin kelimesinin maddesi: seçilen madde (belirsizse yalnız kendisi)
    metin_maddesi = {w: m["secilen"] | {w} for w, m in zip(kelimeler, maddeler)}
    adaylar = []
    for no, m in enumerate(_CUMLE.finditer(metin)):
        cumle = m.group().strip()
        if len(_KELIME.findall(cumle)) < 3:
            continue
        cumle_maddeleri = {a for w in _kelimeler(cumle, dil) if _icerik(w, dil, sik) for a in metin_maddesi.get(w, {w})}
        for tr_id, en_id, kaynakta, karsilik, benzerlik in b.execute(
                f"SELECT tr_id, en_id, {sutun}, {karsi}, similarity({sutun}, %s) FROM bilgi.cumle "
                f"ORDER BY {sutun} <-> %s LIMIT %s", (cumle, cumle, CUMLE_BASINA_ORNEK)):
            if benzerlik >= BENZERLIK_ESIGI:
                adaylar.append((benzerlik, no, tr_id, en_id, kaynakta, karsilik, cumle_maddeleri))
    if not adaylar:
        return []
    # Örnek, metin cümlesiyle en az bir içerik maddesini paylaşmalı (yalnız harf benzerliği yetmez)
    ornek_kelimeleri = {a[4]: [w for w in _kelimeler(a[4], dil) if _icerik(w, dil, sik)] for a in adaylar}
    tumu = sorted({w for v in ornek_kelimeleri.values() for w in v})
    ornek_maddesi = {w: m["tum"] | {w} for w, m in zip(tumu, _maddeler(b, dil, tumu))} if tumu else {}
    adaylar = [a[:6] for a in adaylar
               if a[6] & {x for w in ornek_kelimeleri[a[4]] for x in ornek_maddesi[w]}]
    adaylar.sort(key=lambda x: -x[0])
    sonuc, goruldu = [], set()
    ad = {"tr": "Turkish", "en": "English"}
    for benzerlik, no, tr_id, en_id, kaynakta, karsilik in adaylar:
        if len(sonuc) >= EN_COK_ORNEK or kaynakta in goruldu:
            continue
        goruldu.add(kaynakta)
        sonuc.append(Kayit("ornek", "Tatoeba", lisans[2], kaynakta,
                           f"{ad[sutun]}: {kaynakta} | {ad[karsi]}: {karsilik}",
                           {"tr_id": tr_id, "en_id": en_id, "benzerlik": round(benzerlik, 2)}))
    return sonuc


def istem_blogu(kayitlar: list[Kayit]) -> str:
    """Kayıtların sistem istemine eklenecek hâli (kullanıcı sözlüğü terimleri ayrıca terim listesinde)."""
    gruplar = [
        ("kalip", "Idioms and set phrases that occur in the text:"),
        ("anlam", "Words with several meanings (choose the meaning that fits the context):"),
        ("ornek", "Similar example sentence pairs (hints for wording only; never copy them):"),
    ]
    satirlar = []
    for tur, baslik in gruplar:
        secilen = [k for k in kayitlar if k.tur == tur]
        if secilen:
            satirlar.append(baslik)
            satirlar += [f"- {k.istem}" for k in secilen]
    if not satirlar:
        return ""
    return ("Reference information from dictionaries for this text. These are hints, not translations to copy: "
            "use them only where they fit the context, and never copy them into the output.\n" + "\n".join(satirlar))


def karsilik_var_mi(b, kaynak_dil: str, kaynak_kelimeleri: list[str], eklenen: str) -> bool:
    """Denetimin eklediği hedef dil kelimesinin kaynakta sözlük karşılığı var mı (güvenlik kontrolü)."""
    if kaynak_dil == "en":
        # Hedef Türkçe: eklenen kelimenin maddeleri, kaynak kelimelerin (ve çekimlerinin maddelerinin) Türkçe çevirilerinde mi
        maddeler = {eklenen} | {r[0] for r in b.execute(
            "SELECT kelime FROM bilgi.bicim WHERE dil = 'tr' AND bicim = %s", (eklenen,))}
        trler = {w for (t,) in b.execute(
            "SELECT tr_kelime FROM bilgi.en_ceviri WHERE lower(en_kelime) = ANY(%(k)s) "
            "UNION SELECT c.tr_kelime FROM bilgi.en_ceviri c JOIN bilgi.bicim f "
            "  ON f.dil = 'en' AND f.kelime = lower(c.en_kelime) WHERE f.bicim = ANY(%(k)s)",
            {"k": kaynak_kelimeleri}) for w in _kelimeler(t, "tr")}
        return any(m in trler or (len(m) >= 4 and any(t[:4] == m[:4] for t in trler)) for m in maddeler)
    # Hedef İngilizce: eklenen kelime, kaynak Türkçe kelimelerin maddelerinin açıklamalarında geçiyor mu
    maddeler_tr = {a for w, m in zip(kaynak_kelimeleri, _maddeler(b, "tr", kaynak_kelimeleri)) for a in m["tum"] | {w}}
    aciklama = " ".join(r[0] for r in b.execute(
        "SELECT anlam FROM bilgi.tr_anlam WHERE kelime = ANY(%s)", (sorted(maddeler_tr),))).lower()
    kok = eklenen[:max(4, len(eklenen) - 3)]
    return re.search(rf"\b{re.escape(kok)}", aciklama) is not None
