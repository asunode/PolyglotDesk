# Detaylı Çevir kurulumu (PostgreSQL bilgi paketi)

*English: [detailed-setup.md](detailed-setup.md)*

**Detaylı Çevir**, çeviriden önce yerel bir PostgreSQL veritabanında deyimleri, kalıpları, çok anlamlı kelimeleri ve örnek cümle çiftlerini arar, ardından bir denetim geçişi yapar. Bu belge o veritabanını kendi makinenizde nasıl kuracağınızı anlatır. Önce [temel kurulumu](install.tr.md) tamamlayın.

**PostgreSQL olmadan da hızlı çeviri çalışır.** Veritabanına ulaşılamazsa yalnız Detaylı Çevir kullanılamaz ve uygulama bunu açıklayan bir mesaj gösterir.

## Gereksinimler

| | |
|---|---|
| PostgreSQL | 18 ile denendi; `pg_trgm` eklentisi gerekir (Ubuntu'nun standart paketlerinde vardır). Güvenilir (trusted) `pg_trgm` destekleyen güncel sürümlerle (13+) çalışması beklenir. |
| psycopg | `python3-psycopg` (apt) ya da `pip install "psycopg[binary]"` |
| İndirme | ~3.1 GB (Wiktionary ham verisi ~3.1 GB + Tatoeba ~40 MB) |
| Veritabanı | Yüklemeden sonra ~566 MB; yeniden yüklemede yeni kopya eskisinin yanında kurulduğu için bunun yaklaşık iki katı yer gerekir |
| Yükleme süresi | ~3 dakika (Intel i5-11600K'de ölçüldü) |

Bütün veri sizin makinenizde kalır. Çeviri sırasında internete hiçbir şey gönderilmez.

## 1. PostgreSQL kurulumu

```bash
sudo apt install postgresql
pg_isready -h 127.0.0.1
```

## 2. Veritabanı ve roller

İki rol kullanılır:

- veritabanının sahibi olan ve yalnız yükleme betiğinin kullandığı **sahip rol** (`cevirmen`),
- uygulamanın bağlandığı **yalnız okuma rolü** (`cevirmen_okur`).

Bir süper kullanıcı oturumu açın (örneğin `sudo -u postgres psql`) ve şunları çalıştırın (şifreleri kendiniz seçin):

```sql
-- sahip rol ve veritabanı
CREATE ROLE cevirmen LOGIN PASSWORD 'sahip-sifresi-secin';
CREATE DATABASE cevirmen OWNER cevirmen;

-- uygulama için yalnız okuma rolü
CREATE ROLE cevirmen_okur LOGIN PASSWORD 'okur-sifresi-secin'
    NOSUPERUSER NOCREATEDB NOCREATEROLE;
ALTER ROLE cevirmen_okur SET default_transaction_read_only = on;
GRANT CONNECT ON DATABASE cevirmen TO cevirmen_okur;
```

Tablolardaki `SELECT` yetkisini yükleme betiği her yüklemede verir (5. adım). `pg_trgm` eklentisini yükleyici veritabanı sahibi olarak oluşturur (güvenilir bir eklentidir).

**İsteğe bağlı yardımcı:** son blok yerine `veritabani/okur_rol.sh` yalnız okuma rolünü rastgele bir şifreyle oluşturur ve şifreyi `~/.pgpass` dosyanıza yazar. Kendi kullanıcınızla, yönetici bağlantısını standart `PG*` değişkenleriyle vererek çalıştırın; örneğin `PGHOST=127.0.0.1 PGUSER=postgres veritabani/okur_rol.sh`.

## 3. Şifreler

Uygulama ve yükleyici şifre saklamaz; şifreleri libpq okur. En basit yol `~/.pgpass` dosyasıdır (izin 600):

```text
127.0.0.1:5432:cevirmen:cevirmen:sahip-sifresi-secin
127.0.0.1:5432:cevirmen:cevirmen_okur:okur-sifresi-secin
```

```bash
chmod 600 ~/.pgpass
```

Tek bir komut için `PGPASSWORD` da kullanılabilir.

## 4. Bağlantı ayarları

Varsayılanlar: sunucu `127.0.0.1`, port `5432`, veritabanı `cevirmen`, uygulama rolü `cevirmen_okur`. `~/.config/cevirmen/ayarlar.json` içinde değiştirilebilir:

```json
{
  "pg_host": "127.0.0.1",
  "pg_port": 5432,
  "pg_veritabani": "cevirmen",
  "pg_kullanici": "cevirmen_okur"
}
```

Ortam değişkenleri ayar dosyasından önce gelir: `POLYGLOTDESK_PG_HOST`, `POLYGLOTDESK_PG_PORT`, `POLYGLOTDESK_PG_DB`, `POLYGLOTDESK_PG_USER`. Yükleyici ayrıca `POLYGLOTDESK_PG_OWNER`'ı (sahip rol) okur ve aynı değerleri komut satırı seçenekleriyle de alır (`--host`, `--port`, `--vt`, `--sahip`, `--okur`).

## 5. Verinin indirilmesi ve yüklenmesi

Dört dosyayı tek bir klasöre koyun, örneğin `~/.cache/cevirmen/indirilen`:

| Dosya | Kaynak | Lisans |
|---|---|---|
| `raw-wiktextract-data.jsonl.gz` (~3.1 GB) | [kaikki.org ham veri](https://kaikki.org/dictionary/rawdata.html) — İngilizce Vikisözlük'ün wiktextract çıkarımı: <https://kaikki.org/dictionary/raw-wiktextract-data.jsonl.gz> | CC BY-SA 4.0 (ayrıca GFDL) |
| `tur_sentences.tsv.bz2` | <https://downloads.tatoeba.org/exports/per_language/tur/tur_sentences.tsv.bz2> | CC BY 2.0 FR |
| `eng_sentences.tsv.bz2` | <https://downloads.tatoeba.org/exports/per_language/eng/eng_sentences.tsv.bz2> | CC BY 2.0 FR |
| `tur-eng_links.tsv.bz2` | <https://downloads.tatoeba.org/exports/per_language/tur/tur-eng_links.tsv.bz2> | CC BY 2.0 FR |

```bash
mkdir -p ~/.cache/cevirmen/indirilen && cd ~/.cache/cevirmen/indirilen
wget https://kaikki.org/dictionary/raw-wiktextract-data.jsonl.gz
wget https://downloads.tatoeba.org/exports/per_language/tur/tur_sentences.tsv.bz2
wget https://downloads.tatoeba.org/exports/per_language/eng/eng_sentences.tsv.bz2
wget https://downloads.tatoeba.org/exports/per_language/tur/tur-eng_links.tsv.bz2
cd -
python3 -I veritabani/yukle.py --kaynak ~/.cache/cevirmen/indirilen
```

İndirilen dosyalar güvenilmeyen veri sayıldığı için `-I` önerilir. Betik Wiktionary dosyasını akış hâlinde okur, her şeyi geçici `bilgi_yeni` şemasına yükler, dizinleri kurar, uygulama rolüne okuma yetkisi verir ve tek işlemde `bilgi` ile yer değiştirir. Yükleme yarıda kalırsa önceki veri olduğu gibi kalır. Birkaç bozuk çeviri satırı genel kurallarla ayıklanır (elle seçilmiş kayıt yoktur). Bitince satır sayılarını ve veritabanı boyutunu yazar.

PolyglotDesk'i yeniden başlatın (ya da yalnız **Detaylı Çevir**'e basın); "Kullanılan bilgiler" bölümü modele hangi kayıtların gittiğini kaynak ve lisanslarıyla gösterir.

## `bilgi` şemasındaki tablolar

Satır sayıları geliştirmede kullanılan yüklemeden alınmıştır (Wiktionary dökümü 2026-10-01, Tatoeba dışa aktarımı 2026-11-14).

| Tablo | İçerik | Satır |
|---|---|---|
| `kaynak` | Veri kaynakları (lisans, adres, veri tarihi); her kayıt buraya bağlanır | 2 |
| `tr_anlam` | Türkçe Wiktionary maddelerinin anlamları (İngilizce açıklama, etiket, konu, bir örnek) | 33 181 |
| `bicim` | Çekimli biçim → madde başlığı; Wiktionary çekim tablolarından (Türkçe ve İngilizce) | 2 001 786 tr / 46 462 en |
| `en_ceviri` | İngilizce Wiktionary maddelerinde anlam başına verilen Türkçe çeviriler | 50 964 |
| `kalip` | İki dilde deyim ve kalıplar, her kelimenin madde anahtarıyla | 1 432 tr / 18 492 en |
| `tr_cok_anlamli`, `en_cok_anlamli` | En az iki anlamı olan kelimeler; uzaklık bilgisi (farklı köken / ayrık karşılıklar) ve kaba/argo anlam işareti | 6 042 / 4 601 |
| `cumle` | Tatoeba'dan Türkçe–İngilizce cümle çiftleri (benzerlik araması için trigram dizini) | 660 592 |
| `siklik` | Tatoeba'da dil başına en sık 2 000 kelime | 4 000 |
| `madde` | Bütün madde başlıkları (iki dil) | 53 184 |
| `madde_siklik` | Madde başlıklarının Tatoeba sıklığı; yalnız tek maddeye bağlanan biçimlerden sayılır | 22 005 |

## Detaylı Çevir bunları nasıl kullanır

Metnin her paragraf boyutundaki parçası için:

1. **Arama** (arka planda, yalnız okuma rolüyle):
   - kelimeleri metinde sırayla ve yakın geçen *deyim ve kalıplar*; Türkçede ismin hal eki ve iyeliği uyuşmalı ("başa çıkmak" ≠ "başına çıkmak"); yalnız işlev kelimelerinden oluşan İngilizce kalıplar yalnız Wiktionary onları edat, bağlaç ya da zarf sayıyorsa ya da Türkçe karşılık veriyorsa gönderilir;
   - *çok anlamlı kelimeler*: madde çekim tablolarından bulunur; bir biçim birden çok maddeye bağlanıyorsa en sık madde seçilir (açık bir fark yoksa o kelime için kayıt gönderilmez); çok sık kelimeler atlanır; teknik metinde teknik anlamlar öne alınır; kaba ya da argo anlamlar, metin açıkça o üslupta değilse gönderilmez;
   - metne benzeyen *örnek cümle çiftleri* (`pg_trgm`); yalnız metin cümlesiyle en az bir içerik maddesini paylaşanlar.
   En çok 5 kalıp, 6 kelime × 4 anlam ve 5 örnek gönderilir.
2. **Çeviri**: bu kayıtlar ipucu olarak, eşleşen sözlük terimleriyle birlikte isteme eklenir.
3. **Denetim**: model kaynakla taslağı karşılaştırır ve JSON ile cevap verir ("hata yok" ya da her biri taslaktan birebir bir parça ve düzeltmesi olan hata listesi). Düzeltmeleri kod uygular, güvenli olmayanları geri alır (örneğin unvan/hitap değişikliği, çevrilmeden eklenen kaynak kelimesi, kaynakta sözlük karşılığı olmayan kelime — `en_ceviri` / `tr_anlam` ile denetlenir). Kalın yazıyı kod yerleştirir.

Arama çoğunlukla bir saniyenin altında sürer; Detaylı Çevir'in ölçülen toplam süresi CPU'da paragraf başına ~34–70 saniyeydi.
