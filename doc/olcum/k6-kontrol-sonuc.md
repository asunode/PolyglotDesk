# K6 düzeltmesi kontrolü — hızlı çeviri (ham kayıt)

Betik: `doc/olcum/bench_k6_kontrol.py`. Ham veri: `doc/olcum/k6-kontrol-ham.json`. Koşu: 2026-11-19 20:21:06 +0300 – 2026-11-19 20:22:13 +0300. gemma4:12b-it-qat, yalnız CPU, temperature 0, seed 42; uygulamanın hızlı çeviri yolu, paketteki varsayılan sözlük.
Değişiklik (Adım 9): teknik bağlam kuralları yalnız sözlüğün `[Teknik bağlam tetikleyicileri]` bölümündeki donanım/elektronik terimleriyle açılır (önceden sözlükteki herhangi bir terim, ör. Wi-Fi, açıyordu).

## K6 · TR→EN (hizli-konu-seti-v1)

```text
Hoş geldiniz! Odanız üçüncü katta, deniz manzaralı. Kahvaltı sabah 7 ile 10 arasında lobinin yanındaki restoranda veriliyor. Çıkış saati öğlen 12, isterseniz eşyalarınızı resepsiyonda bırakabilirsiniz. Wi-Fi şifresi kartın arkasında yazıyor.
```

Dikkat: "kart" burada oda kartı (board olmamalı), saatler

**Önceki hızlı çeviri (Adım 8, 1. koşu)**

```text
Welcome! Your room is on the third floor with a sea view. Breakfast is served in the restaurant next to the lobby between 7 and 10 AM. Check-out time is 12 PM; if you wish, you can leave your belongings at the reception. The Wi-Fi password is written on the back of the board.
```

**Yeni hızlı çeviri** (bitti; ilk metin 4.90 s, toplam 17.78 s)

```text
Welcome! Your room is on the third floor with a sea view. Breakfast is served in the restaurant next to the lobby between 7 and 10 AM. Check-out time is at 12 PM; if you'd like, you can leave your belongings at the reception. The Wi-Fi password is written on the back of the card.
```

- Teknik bağlam tetiklendi: hayır
- Modele giden sözlük terimleri: Wi-Fi
- Kalın yazı düzeltmesi: yok; sınır isteği: 0

## D5 · TR→EN (detayli-test-seti-v1)

```text
Kartı yeniden flash'ladım ama watchdog yine tetiklendi. Hatayı log'lardan buldum: stack overflow. Kartın yanındaki kartvizitte yazan numarayı arayıp destek istedim.
```

Dikkat: kart, kartvizit

**Önceki hızlı çeviri (Adım 7)**

```text
I flashed the board again, but the watchdog was triggered again. I found the error in the logs: stack overflow. I called the number on the business card next to the board and asked for support.
```

**Yeni hızlı çeviri** (bitti; ilk metin 4.20 s, toplam 11.21 s)

```text
I flashed the board again, but the watchdog was triggered again. I found the error in the logs: stack overflow. I called the number on the business card next to the board and asked for support.
```

- Teknik bağlam tetiklendi: evet
- Modele giden sözlük terimleri: watchdog; stack; log; kart → board
- Kalın yazı düzeltmesi: yok; sınır isteği: 0

## W1 · TR→EN (dogrulama-seti-v2)

```text
Kartı USB'den **çıkarmayın**; firmware yazılırken bağlantı kesilirse kart açılmayabilir.
```

Dikkat: kalın yazı "not" üzerinde olmalı, kart

**Önceki hızlı çeviri (Adım 7)**

```text
Do **not** unplug the board from the USB; if the connection is lost while the firmware is being written, the board may not boot.
```

**Yeni hızlı çeviri** (bitti; ilk metin 3.70 s, toplam 8.99 s)

```text
Do **not** unplug the board from the USB; if the connection is lost while the firmware is being written, the board may not boot.
```

- Teknik bağlam tetiklendi: evet
- Modele giden sözlük terimleri: firmware; kart → board
- Kalın yazı düzeltmesi: kod (olumsuzluk sırası): Do **not** unplug the board from the USB; if the connection is lost while the firmware is being written, the board may not boot.; sınır isteği: 0

## W3 · TR→EN (dogrulama-seti-v2)

```text
SD kartı takınca kart tanınmadı; kayıtlarda okuma hatası görünüyor, kartı başka bir okuyucuda deneyeceğim.
```

Dikkat: kart (burada SD kart), kayıtlar

**Önceki hızlı çeviri (Adım 7)**

```text
The card wasn't recognized when I plugged in the SD card; a read error appears in the logs, so I will try the card in another reader.
```

**Yeni hızlı çeviri** (bitti; ilk metin 3.87 s, toplam 9.29 s)

```text
The card wasn't recognized when I plugged in the SD card; a read error appears in the logs, so I will try the card in another reader.
```

- Teknik bağlam tetiklendi: evet
- Modele giden sözlük terimleri: SD kart → SD card; kayıtlar → logs; kayıt → log
- Kalın yazı düzeltmesi: yok; sınır isteği: 0

## G3 · TR→EN (kontrol-seti-v2)

```text
Kartın brownout reset'i sık sık tetikleniyor; kondansatörü değiştirdikten sonra bile log'larda aynı hata var. Kartı kredi kartı boyutunda bir kutuya koyacağım.
```

Dikkat: ilk "kart" = board, "kredi kartı" = credit card (aynı metinde ikisi de var).

**Önceki hızlı çeviri (Adım 7)**

```text
The board's brownout reset is being triggered frequently; the same error persists in the logs even after replacing the capacitor. I'm going to put the board in a credit card-sized box.
```

**Yeni hızlı çeviri** (bitti; ilk metin 4.22 s, toplam 11.25 s)

```text
The board's brownout reset is being triggered frequently; the same error persists in the logs even after replacing the capacitor. I'm going to put the board in a credit card-sized box.
```

- Teknik bağlam tetiklendi: evet
- Modele giden sözlük terimleri: brownout; log; kart → board
- Kalın yazı düzeltmesi: yok; sınır isteği: 0

## V5 · TR→EN (dogrulama-seti-v1)

```text
Log'ları temizledim ama SD karttaki kayıtlar hâlâ duruyor; kartı formatlamadan önce yedek alacağım.
```

Dikkat: kart (burada SD kart), kayıtlar

**Önceki hızlı çeviri (Adım 7)**

```text
I cleared the logs, but the records on the SD card are still there; I will take a backup before formatting the card.
```

**Yeni hızlı çeviri** (bitti; ilk metin 4.13 s, toplam 8.50 s)

```text
I cleared the logs, but the records on the SD card are still there; I will take a backup before formatting the card.
```

- Teknik bağlam tetiklendi: evet
- Modele giden sözlük terimleri: log; SD kart → SD card; kayıtlar → logs; kayıt → log
- Kalın yazı düzeltmesi: yok; sınır isteği: 0
