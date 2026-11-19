"""Kullanıcı ayarları: ~/.config/cevirmen/ayarlar.json"""

import json
import os
from pathlib import Path

VARSAYILAN = {
    "model": "gemma4:12b-it-qat",
    "ollama_adresi": "http://127.0.0.1:11434",
    # Ölçüm makinesinde (4 GB VRAM'li eski bir GPU, Vulkan) model GPU'ya sığmıyor; yalnız CPU ilk kelimeyi
    # ~2 sn daha erken getiriyor.
    "yalniz_cpu": True,
    "keep_alive": "15m",
    "kaynak_dil": "tr",
    # Detaylı Çevir'in bilgi veritabanı (PostgreSQL). Şifre libpq ile (~/.pgpass ya da PGPASSWORD) okunur.
    # Ortam değişkenleri ayar dosyasından önce gelir: POLYGLOTDESK_PG_HOST, _PORT, _DB, _USER.
    "pg_host": "127.0.0.1",
    "pg_port": 5432,
    "pg_veritabani": "cevirmen",
    "pg_kullanici": "cevirmen_okur",
}


def dosya_yolu() -> Path:
    taban = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    return taban / "cevirmen" / "ayarlar.json"


def yukle() -> dict:
    ayarlar = dict(VARSAYILAN)
    try:
        ayarlar.update(json.loads(dosya_yolu().read_text(encoding="utf-8")))
    except (OSError, ValueError):
        pass
    if ayarlar["kaynak_dil"] not in ("tr", "en"):
        ayarlar["kaynak_dil"] = "tr"
    return ayarlar


def kaydet(ayarlar: dict) -> None:
    yol = dosya_yolu()
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text(json.dumps(ayarlar, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
