# Detailed Translation setup (PostgreSQL knowledge pack)

*Türkçe: [detailed-setup.tr.md](detailed-setup.tr.md)*

**Detailed Translation** (Detaylı Çevir) looks up idioms, set phrases, words with several meanings and example sentence pairs in a local PostgreSQL database before translating, and then runs a review pass. This guide shows how to build that database on your own machine. Complete the [base installation](install.md) first.

**Without PostgreSQL, quick translation still works.** If the database cannot be reached, only Detailed Translation is unavailable and the application shows a message explaining this.

## Requirements

| | |
|---|---|
| PostgreSQL | tested with 18; needs the `pg_trgm` extension (included in the standard Ubuntu packages). Any recent version that supports trusted `pg_trgm` (13+) should work. |
| psycopg | `python3-psycopg` (apt) or `pip install "psycopg[binary]"` |
| Download | ~3.1 GB (Wiktionary raw data ~3.1 GB + Tatoeba ~40 MB) |
| Database | ~566 MB after loading; while reloading, the new copy is built next to the old one, so plan for about twice that |
| Loading time | ~3 minutes (measured on an Intel i5-11600K) |

All data stays on your machine. Nothing is sent to the internet during translation.

## 1. Install PostgreSQL

```bash
sudo apt install postgresql
pg_isready -h 127.0.0.1
```

## 2. Create the database and the roles

Two roles are used:

- an **owner role** (`cevirmen`) that owns the database and is used only by the loader script, and
- a **read-only role** (`cevirmen_okur`) that the application uses to connect.

Open a superuser session, for example with `sudo -u postgres psql`, and run (choose your own passwords):

```sql
-- owner role and database
CREATE ROLE cevirmen LOGIN PASSWORD 'choose-an-owner-password';
CREATE DATABASE cevirmen OWNER cevirmen;

-- read-only role for the application
CREATE ROLE cevirmen_okur LOGIN PASSWORD 'choose-a-reader-password'
    NOSUPERUSER NOCREATEDB NOCREATEROLE;
ALTER ROLE cevirmen_okur SET default_transaction_read_only = on;
GRANT CONNECT ON DATABASE cevirmen TO cevirmen_okur;
```

`SELECT` rights on the tables are granted by the loader script every time it loads the data (step 5). The `pg_trgm` extension is created by the loader as the database owner (it is a trusted extension).

**Optional helper:** instead of the last block, `veritabani/okur_rol.sh` creates the read-only role with a random password and writes it to your `~/.pgpass`. Run it as your own user with an administrator connection given through the standard `PG*` variables, e.g. `PGHOST=127.0.0.1 PGUSER=postgres veritabani/okur_rol.sh`.

## 3. Passwords

The application and the loader never store passwords; they are read by libpq. The simplest way is a `~/.pgpass` file (mode 600):

```text
127.0.0.1:5432:cevirmen:cevirmen:choose-an-owner-password
127.0.0.1:5432:cevirmen:cevirmen_okur:choose-a-reader-password
```

```bash
chmod 600 ~/.pgpass
```

Alternatively set `PGPASSWORD` for a single command.

## 4. Connection settings

Defaults: host `127.0.0.1`, port `5432`, database `cevirmen`, application role `cevirmen_okur`. They can be changed in `~/.config/cevirmen/ayarlar.json`:

```json
{
  "pg_host": "127.0.0.1",
  "pg_port": 5432,
  "pg_veritabani": "cevirmen",
  "pg_kullanici": "cevirmen_okur"
}
```

Environment variables take precedence over the settings file: `POLYGLOTDESK_PG_HOST`, `POLYGLOTDESK_PG_PORT`, `POLYGLOTDESK_PG_DB`, `POLYGLOTDESK_PG_USER`. The loader also reads `POLYGLOTDESK_PG_OWNER` (owner role) and accepts the same values as command-line options (`--host`, `--port`, `--vt`, `--sahip`, `--okur`).

## 5. Download the data and load it

Put the four files in one directory, for example `~/.cache/cevirmen/indirilen`:

| File | Source | Licence |
|---|---|---|
| `raw-wiktextract-data.jsonl.gz` (~3.1 GB) | [kaikki.org raw data](https://kaikki.org/dictionary/rawdata.html) — wiktextract extraction of the English Wiktionary: <https://kaikki.org/dictionary/raw-wiktextract-data.jsonl.gz> | CC BY-SA 4.0 (also GFDL) |
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

`-I` is recommended because downloaded files are untrusted data. The script streams the Wiktionary file, loads everything into a temporary schema `bilgi_yeni`, builds the indexes, grants read access to the application role and then swaps it with `bilgi` in one transaction. If loading is interrupted, the previous data stays untouched. A few malformed translation lines are dropped by general rules (no record is selected by hand). When it finishes, it prints the row counts and the database size.

Restart PolyglotDesk (or just press **Detaylı Çevir**); the "Kullanılan bilgiler" (information used) panel shows which records were sent to the model, with their source and licence.

## What the `bilgi` schema contains

Row counts are from the loading run used during development (Wiktionary dump 2026-10-01, Tatoeba export 2026-11-14).

| Table | Content | Rows |
|---|---|---|
| `kaynak` | Data sources with licence, URL and data date; every record points here | 2 |
| `tr_anlam` | Senses of Turkish Wiktionary entries (English glosses, tags, topics, one example) | 33 181 |
| `bicim` | Inflected form → headword, from Wiktionary inflection tables (Turkish and English) | 2 001 786 tr / 46 462 en |
| `en_ceviri` | Turkish translations listed in English Wiktionary entries, per sense | 50 964 |
| `kalip` | Idioms and set phrases in both languages, with the headword keys of each word | 1 432 tr / 18 492 en |
| `tr_cok_anlamli`, `en_cok_anlamli` | Words with at least two senses, with distance information (different etymologies / disjoint translations) and a flag for vulgar or slang senses | 6 042 / 4 601 |
| `cumle` | Turkish–English sentence pairs from Tatoeba (trigram index for similarity search) | 660 592 |
| `siklik` | The 2 000 most frequent words per language in Tatoeba | 4 000 |
| `madde` | All headwords (both languages) | 53 184 |
| `madde_siklik` | Headword frequency in Tatoeba, counted only from forms that belong to a single headword | 22 005 |

## How Detailed Translation uses it

For each paragraph-sized part of the text:

1. **Search** (in a background thread, read-only role):
   - *idioms and set phrases* whose words occur in the text in order and close together; Turkish noun case and possessive must match ("başa çıkmak" is not "başına çıkmak"); English phrases made only of function words are sent only if Wiktionary lists them as a preposition, conjunction or adverb or gives a Turkish translation;
   - *words with several meanings*: the headword is chosen from the inflection tables, and when a form belongs to several headwords the most frequent one is chosen (if none clearly dominates, nothing is sent for that word); very frequent words are skipped; in technical text technical senses come first; vulgar or slang senses are not sent unless the text is clearly in that register;
   - *example sentence pairs* similar to the text (`pg_trgm`), only if they share at least one content headword with the text sentence.
   At most 5 phrases, 6 words × 4 senses and 5 examples are sent.
2. **Translation** with these records added to the prompt as hints, together with the matching glossary terms.
3. **Review**: the model compares source and draft and answers in JSON ("no error" or a list of errors, each an exact passage of the draft and its correction). The code applies the corrections and rejects unsafe ones (for example changes of titles or forms of address, untranslated source words, words without a dictionary equivalent in the source — checked against `en_ceviri` / `tr_anlam`). Bold text is placed by code.

Search usually takes under a second; the measured total for Detailed Translation was ~34–70 seconds per paragraph on the CPU.
