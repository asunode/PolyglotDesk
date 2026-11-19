"""Adım 7 (C5): teknik bağlam kuralının ölçümü.

Kural: metin teknikse (sözlükten teknik terim geçiyorsa) ve bir kelimenin veride hiç teknik anlamı yoksa,
o kelimenin çok anlamlı kelime kaydı gönderilmez. Bu betik kuralı üç biçimde karşılaştırır:
    kapali         kural yok (Adım 6 davranışı)
    fiiller_muaf   kural açık, fiil anlamı olan kelimeler muaf (uygulamadaki ayar)
    fiiller_dahil  kural açık, fiiller de dahil
Cümleler bu ölçüm için yazıldı; hiçbir test setinden alınmadı.

Kullanım:
    python3 doc/olcum/teknik_kural.py > doc/olcum/teknik-kural-ham.txt
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from cevirmen import bilgi  # noqa: E402
from cevirmen.sozluk import VARSAYILAN, Sozluk  # noqa: E402

CUMLELER = [
    ("en", "tr", "Keep the reset line high while the bootloader runs, then release it."),
    ("en", "tr", "The scheduler will drop the task if the watchdog fires before the buffer is flushed."),
    ("en", "tr", "Set the baud rate on the UART and hold the button until the LED turns green."),
    ("en", "tr", "If the MQTT broker goes down, the gateway stores the payload and retries later."),
    ("en", "tr", "Run the script again after you clear the cache and the build directory on the router."),
    ("en", "tr", "The display shows a warning when the battery level falls below ten percent; the firmware then saves the state."),
    ("en", "tr", "Mount the sensor on the board and check the signal on the SPI bus with the oscilloscope."),
    ("en", "tr", "The interrupt handler must not block; it should only raise a flag for the main loop."),
    ("tr", "en", "Watchdog tetiklenirse task yeniden başlar ve buffer temizlenir."),
    ("tr", "en", "Kartı UART üzerinden bağlayıp firmware'i yeniden yükledim ama ekran açılmadı."),
    ("tr", "en", "Sensörü I2C hattına taktım; okuma değerleri birkaç dakika sonra kayıyor."),
    ("tr", "en", "Gateway, MQTT bağlantısı koparsa payload'u saklayıp daha sonra tekrar gönderir."),
    ("tr", "en", "Pil seviyesi düşünce sistem uyku moduna geçiyor ve ayarları NVS'e yazıyor."),
    ("tr", "en", "Interrupt içinde uzun işlem yapma; sadece bir bayrak kaldır ve ana döngüde işle."),
]

AYARLAR = {"kapali": (False, False), "fiiller_muaf": (True, False), "fiiller_dahil": (True, True)}


def main() -> None:
    sozluk = Sozluk(VARSAYILAN)
    sozluk.guncelle()
    toplam = {a: 0 for a in AYARLAR}
    for k, h, cumle in CUMLELER:
        teknik = bool(sozluk.eslesenler(cumle, k, h))
        sonuc = {}
        for ad, (kural, fiiller) in AYARLAR.items():
            bilgi.TEKNIK_KURALI, bilgi.TEKNIK_KURALI_FIILLER = kural, fiiller
            sonuc[ad] = {r.baslik: r.istem for r in bilgi.ara(cumle, k, h, teknik=teknik) if r.tur == "anlam"}
            toplam[ad] += len(sonuc[ad])
        print(f"## {k.upper()}→{h.upper()} · {cumle}")
        print(f"teknik bağlam: {'evet' if teknik else 'hayır'}")
        for ad in ("fiiller_muaf", "fiiller_dahil"):
            dusen = [b for b in sonuc["kapali"] if b not in sonuc[ad]]
            print(f"- {ad}: {len(sonuc[ad])}/{len(sonuc['kapali'])} kayıt; düşen: " + (", ".join(dusen) or "yok"))
        print("- kural kapalıyken gönderilen kayıtlar:")
        for b, istem in sonuc["kapali"].items():
            print(f"    {istem}")
        print()
    print("Toplam anlam kaydı:", ", ".join(f"{a} {n}" for a, n in toplam.items()))


if __name__ == "__main__":
    main()
