# PolyglotDesk kurulumu

*English: [install.md](install.md)*

Bu belge temel kurulumu anlatır; temel kurulumla **hızlı çeviri** çalışır. **Detaylı Çevir** ayrıca yerel bir PostgreSQL bilgi paketi gerektirir; o kurulum ayrı belgededir: [detailed-setup.tr.md](detailed-setup.tr.md). Hızlı çeviri PostgreSQL olmadan da çalışır.

## Denenen ortam

| Bileşen | Geliştirmede kullanılan sürüm |
|---|---|
| İşletim sistemi | Ubuntu 26.04 LTS (Linux masaüstü, Wayland) |
| Python | 3.14 (Python ≥ 3.10 ile çalışması beklenir) |
| PySide6 (Qt for Python) | 6.10 |
| psycopg | 3.3 (yalnız Detaylı Çevir için) |
| Ollama | 0.30.7 |
| Model | `gemma4:12b-it-qat` |

Yalnız Ubuntu'da denendi. Diğer Linux dağıtımlarında, macOS'ta ve Windows'ta çalışabilir ama denenmedi.

## 1. Kodu indirin

```bash
git clone https://github.com/asunode/PolyglotDesk.git
cd PolyglotDesk
```

## 2. Python paketleri

İki seçenekten **birini** kullanın.

**Seçenek A — Ubuntu paketleri (sanal ortam gerekmez):**

```bash
sudo apt install python3-pyside6.qtwidgets python3-pyside6.qtnetwork python3-pyside6.qtsvg python3-psycopg
```

**Seçenek B — pip ile, sanal ortamda:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`psycopg` yalnız Detaylı Çevir için gerekir. Kurulu değilse uygulama yine açılır ve hızlı çeviri çalışır.

## 3. Ollama ve model

PolyglotDesk yerel bir [Ollama](https://ollama.com) sunucusuyla çalışır (varsayılan `http://127.0.0.1:11434`). Ollama'yı [ollama.com/download](https://ollama.com/download) sayfasındaki talimatla kurun (Linux'ta bir `systemd` servisi kurar), sonra varsayılan modeli indirin:

```bash
ollama pull gemma4:12b-it-qat
```

İndirme yaklaşık **7.2 GB**'tır. Model bu depoda yer almaz; kendi lisansına ve kullanım koşullarına (Gemma koşulları) tabidir.

Sunucunun çalıştığını kontrol edin:

```bash
systemctl status ollama
```

### Varsayılan: yalnız işlemci

"Yalnız işlemciyi (CPU) kullan" ayarı varsayılan olarak **açıktır**. Geliştirme makinesinde ekran kartı (4 GB VRAM'li eski bir kart) 12B modelin ancak dörtte birini alabiliyordu; modelin GPU ile CPU arasında bölünmesi ilk kelimeleri yalnız CPU'ya göre yaklaşık 2 saniye *geç* getiriyordu, üretim hızı ise aynıydı. Modelin tamamını alabilen bir ekran kartınız varsa bu ayarı **Ayarlar**'dan kapatın.

### İsteğe bağlı: TranslateGemma

`translategemma:12b` (~8.1 GB) denendi ve Ayarlar'dan seçilebilir, ama **önerilmez** ve varsayılan değildir: testlerde bir teknik cümlenin anlamını 4 denemenin 4'ünde tersine çevirdi. Yalnız karşılaştırmak isterseniz kurun:

```bash
ollama pull translategemma:12b
```

## 4. Çalıştırma

```bash
./calistir.sh
```

ya da aynı işi yapan `python3 -m cevirmen`. (Python paketi özgün adıyla, `cevirmen` olarak kalır.)

- Sol panele metin yapıştırın: hızlı çeviri hemen başlar; yazarken yazmayı bıraktıktan 1 saniye sonra başlar.
- **Detaylı Çevir** düğmesi ya da **Ctrl+Enter**: Detaylı Çevir (bilgi paketi gerekir, bkz. [detailed-setup.tr.md](detailed-setup.tr.md)).
- **Esc**: durdur.

## Uygulamanın oluşturduğu dosyalar

| Yol | İçerik |
|---|---|
| `~/.config/cevirmen/ayarlar.json` | Ayarlar: model, Ollama adresi, yalnız CPU, son yön, veritabanı bağlantısı |
| `~/.config/cevirmen/sozluk.txt` | Terim sözlüğü (düzenlenebilir; Ayarlar → "Sözlüğü aç"). Değişiklik sonraki çeviride geçerli olur. |

## Testler

Birim testleri Ollama ya da PostgreSQL gerektirmez:

```bash
python3 -m unittest discover -s tests
```

## Sorun giderme

- *"Ollama'ya ulaşılamıyor"*: servisi `systemctl start ollama` ya da `ollama serve` ile başlatın.
- *"… modeli Ollama'da bulunamadı"*: `ollama pull gemma4:12b-it-qat` çalıştırın ya da Ayarlar'dan kurulu bir model seçin.
- Açılıştan sonraki ilk çeviri, model belleğe yüklenirken daha uzun sürebilir.
