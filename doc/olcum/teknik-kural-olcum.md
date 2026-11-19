# Teknik bağlam kuralı — ölçüm (Adım 7, C5)

Kural (Adım 7 talebi): metin teknikse ve bir kelimenin veride hiç teknik anlamı yoksa, o kelimenin çok anlamlı kelime kaydı gönderilmez. Amaç "banner → bandı" türü yanıltmaları önlemek. Talep: kuralın gündelik fiillerde (keep, run vb.) yararlı kayıtları gereksiz yere düşürüp düşürmediğini ölçmek.

- Betik: `doc/olcum/teknik_kural.py`; ham çıktı: `doc/olcum/teknik-kural-ham.txt` (her cümlede kural kapalıyken giden kayıtların tam metni ve her ayarda düşenler).
- Cümleler: bu ölçüm için yazılmış 14 teknik cümle (8 EN→TR, 6 TR→EN); hiçbiri test ya da doğrulama setlerinden değil. Hepsinde sözlükten teknik terim geçiyor (teknik bağlam: evet).
- "Teknik anlam": anlamın konu/etiket alanında ya da açıklamasında teknik alan kelimesi (`bilgi.TEKNIK`: comput…, electr…, program…, software, hardware, digital, network…, circuit…, telecommunication…, internet, technolog…, signal processing).
- Ölçüm zamanı: 2026-11-19, bilgi paketi yeniden yüklendikten sonra (17:36).

## Sonuç

| Ayar | Gönderilen anlam kaydı (14 cümle) |
|---|---|
| Kural kapalı (Adım 6) | 57 |
| Kural açık, fiil anlamı olan kelimeler muaf | 40 |
| Kural açık, fiiller dahil | 14 |

**Fiiller dahil edildiğinde** gündelik fiillerin yararlı kayıtları düşüyor: keep ("to continue → -ip durmak, devam etmek"), run, release ("to let go of → bırakmak"), drop, fire, set, turn, go, build, show, block ("to prevent passing → engellemek"), raise ("to cause to rise → kaldırmak"); Türkçede bağlamak, kaymak, takmak, okumak, kopmak, saklamak, göndermek, geçmek, yazmak, yapmak. Bu fiillerin hiçbirinin veride teknik etiketli anlamı yok; kayıtları teknik metinde de doğru anlamı (devam etmek, kaldırmak, engellemek …) içeriyor. 57 kaydın 43'ü düşüyor.

**Uygulamadaki ayar: fiiller muaf** (`bilgi.TEKNIK_KURALI = True`, `TEKNIK_KURALI_FIILLER = False`). Bir kelimenin gönderilecek anlamları arasında fiil anlamı varsa kural uygulanmaz; yalnız ad, sıfat ve zarf kayıtları düşer. Bu ayarda düşen 17 kayıt:

- Yanıltıcı ya da gereksiz olduğu görülenler: high ("of meat: slightly tainted"), rate ("taksit / ücret"), broker, late ("euphemism for dead"), payload ("uçuş yükü"), mount ("horse"), check (yalnız ad anlamları: "bill", "chess"), yeniden ("anew; again"), kart (sözlük zaten board veriyor), hattına (çekim açıklaması), uyku.
- Yararlı olabilecekler (veride teknik etiket olmadığı için düşüyor): directory ("simulated folder → dizin, klasör"), level ("degree or amount → düzey, seviye"), mod ("mode; mood"), ayar ("setting; adjustment"), döngü ("cycle, loop"). Türkçe maddelerde konu etiketi çok seyrek olduğundan Türkçe teknik kelimeler bu kurala daha çok takılıyor.

İlk ölçümde teknik anlam tanıyıcısı daha dardı ("programming", "technology" tam kelime): "loop: programmed sequence of instructions → döngü" ve "ekran: screen (display of a technological device)" de teknik sayılmıyor ve düşüyordu (fiiller muaf: 38 kayıt). Tanıyıcı kelime kökleriyle genişletildi (program…, technolog…, digital); bu iki kayıt artık gönderiliyor (40 kayıt).

## Sınırlama

Kural verideki teknik etiketlerin kalitesine bağlı. Etiketsiz teknik anlamlar (directory, mod, ayar, döngü) düşüyor; etiketsiz ve teknik metinde yanıltıcı ad anlamları (banner, payload) da düşüyor. Ölçüm 14 cümleyle sınırlı; "yararlı/yanıltıcı" ayrımı kayıt metnine bakılarak yapılmış tek değerlendirici (AI) yargısıdır.
