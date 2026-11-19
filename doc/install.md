# Installing PolyglotDesk

*Türkçe: [install.tr.md](install.tr.md)*

This guide covers the base installation, which gives you **quick translation** (Hızlı çeviri). **Detailed Translation** (Detaylı Çevir) additionally needs a local PostgreSQL knowledge pack; that is described separately in [detailed-setup.md](detailed-setup.md). Quick translation works without PostgreSQL.

## Tested environment

| Component | Version used during development |
|---|---|
| OS | Ubuntu 26.04 LTS (Linux desktop, Wayland) |
| Python | 3.14 (any Python ≥ 3.10 should work) |
| PySide6 (Qt for Python) | 6.10 |
| psycopg | 3.3 (only for Detailed Translation) |
| Ollama | 0.30.7 |
| Model | `gemma4:12b-it-qat` |

Only Ubuntu has been tested. Other Linux distributions, macOS and Windows may work but have not been tried.

## 1. Get the code

```bash
git clone https://github.com/asunode/PolyglotDesk.git
cd PolyglotDesk
```

## 2. Python packages

Choose **one** of the two options.

**Option A — Ubuntu packages (no virtual environment):**

```bash
sudo apt install python3-pyside6.qtwidgets python3-pyside6.qtnetwork python3-pyside6.qtsvg python3-psycopg
```

**Option B — pip, in a virtual environment:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`psycopg` is only needed for Detailed Translation. Without it the application still starts and quick translation works.

## 3. Ollama and the model

PolyglotDesk talks to a local [Ollama](https://ollama.com) server (default `http://127.0.0.1:11434`). Install Ollama following the instructions on [ollama.com/download](https://ollama.com/download) (on Linux this sets up a `systemd` service), then download the default model:

```bash
ollama pull gemma4:12b-it-qat
```

The download is about **7.2 GB**. The model is not part of this repository; it is subject to its own licence and terms of use (Gemma terms).

Check that the server is running:

```bash
systemctl status ollama
```

### CPU-only by default

The setting "Yalnız işlemciyi (CPU) kullan" (use CPU only) is **on** by default. On the development machine the GPU (an older card with 4 GB VRAM) could hold only about a quarter of the 12B model; splitting the model between GPU and CPU made the first words appear about 2 seconds *later* than running on the CPU alone, with the same generation speed. If you have a GPU that can hold the whole model, turn this setting off in **Ayarlar** (Settings).

### Optional: TranslateGemma

`translategemma:12b` (~8.1 GB) was evaluated and can be selected in Settings, but it is **not** recommended and not the default: in tests it reversed the meaning of a technical sentence in 4 out of 4 attempts. Install it only if you want to compare:

```bash
ollama pull translategemma:12b
```

## 4. Run

```bash
./calistir.sh
```

or equivalently `python3 -m cevirmen`. (The Python package keeps its original name, `cevirmen`.)

- Paste text into the left panel: quick translation starts immediately; while typing it starts 1 second after you stop.
- **Detaylı Çevir** button or **Ctrl+Enter**: Detailed Translation (needs the knowledge pack, see [detailed-setup.md](detailed-setup.md)).
- **Esc**: stop.

## Files the application creates

| Path | Content |
|---|---|
| `~/.config/cevirmen/ayarlar.json` | Settings: model, Ollama address, CPU-only, last direction, database connection |
| `~/.config/cevirmen/sozluk.txt` | Term glossary (editable; Settings → "Sözlüğü aç"). Changes take effect on the next translation. |

## Tests

The unit tests need neither Ollama nor PostgreSQL:

```bash
python3 -m unittest discover -s tests
```

## Troubleshooting

- *"Ollama'ya ulaşılamıyor"* (cannot reach Ollama): start the service with `systemctl start ollama` or `ollama serve`.
- *"… modeli Ollama'da bulunamadı"* (model not found): run `ollama pull gemma4:12b-it-qat` or choose an installed model in Settings.
- The first translation after start-up can take longer while the model is loaded into memory.
