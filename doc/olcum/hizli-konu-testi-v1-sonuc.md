# Hızlı çeviri konu testi v1 — sonuçlar (ham kayıt)

Set: `doc/olcum/hizli-konu-seti-v1.md` (K1–K12 TR→EN, E1–E12 EN→TR). Betik: `doc/olcum/bench_hizli_konu.py`. Ham veri: `doc/olcum/hizli-konu-testi-v1-ham.json`.
Koşu: 2026-11-19 19:35:20 +0300 – 2026-11-19 19:48:14 +0300. Model gemma4:12b-it-qat, yalnız CPU (num_gpu 0), num_ctx 8192, temperature 0, seed 42. Yalnız hızlı çeviri: uygulamanın çeviri yolu (`Cevirici`), paketteki varsayılan sözlük; açılıştaki gibi model önden yüklendi (sınır istemiyle). 1. koşu K1 → E12, 2. koşu E12 → K1; her koşu yeni bir `Cevirici` nesnesiyle (aynı nesne 2. koşuda parçaları bellekteki önbellekten verirdi). Yön her metinde setteki gibi.

Notlar:
- Bütün çıktılar ham kayıttan birebir alınmıştır; düzeltilmemiş, kısaltılmamıştır.
- "İlk metin": çeviri başlatıldıktan sonra ekranda ilk çeviri metninin görünmesine kadar geçen süre.
- "Farklı satırlar": 1. ve 2. koşu çıktıları arasındaki satır farkı (`-` 1. koşu, `+` 2. koşu).
- "Kalın yazı düzeltmesi" ve "sınır isteği": uygulamanın hızlı çeviri yolundaki ek işlemler (Adım 7).

## K1 · TR→EN · Rehber, yol tarifi

**Kaynak metin**

```text
Otelden çıkınca sağa dönün ve yaklaşık 300 metre düz yürüyün. İkinci trafik ışığından sola sapın; müze sol tarafta, eczanenin hemen yanında. Yürüyerek 10 dakika sürer ama yokuş biraz dik. Pazartesi günleri müze kapalı, bunu unutmayın.
```

Dikkat (yalnız değerlendirme için, modele gitmedi): sağ/sol, 300 metre, ikinci ışık, pazartesi kapalı

**1. koşu** (bitti)

```text
Turn right after leaving the hotel and walk straight for about 300 meters. Turn left at the second traffic light; the museum is on the left, right next to the pharmacy. It takes about 10 minutes to walk, but the hill is a bit steep. Don't forget that the museum is closed on Mondays.
```

**2. koşu** (bitti)

```text
Turn right after leaving the hotel and walk straight for about 300 meters. Turn left at the second traffic light; the museum is on the left, right next to the pharmacy. It takes about 10 minutes to walk, but the hill is a bit steep. Don't forget that the museum is closed on Mondays.
```

**İki çıktı aynı mı:** evet

**Modele giden sözlük terimleri:** yok

**Ek işlemler:** 1. koşu: yok · 2. koşu: yok

| | İlk metin | Toplam |
|---|---|---|
| 1. koşu | 4.27 s | 15.98 s |
| 2. koşu | 3.85 s | 15.48 s |

## K2 · TR→EN · Öğretmen, fen dersi

**Kaynak metin**

```text
Bitkiler güneş ışığını kullanarak kendi besinlerini üretir; buna fotosentez diyoruz. Yapraklardaki yeşil renk, klorofil adı verilen bir maddeden gelir. Işık olmadan bu süreç gerçekleşmez. Yarın bu konuyu bir deneyle göstereceğim, defterlerinizi getirmeyi unutmayın.
```

Dikkat (yalnız değerlendirme için, modele gitmedi): "ışık olmadan gerçekleşmez", öğretmen üslubu

**1. koşu** (bitti)

```text
Plants produce their own food using sunlight; we call this photosynthesis. The green color in leaves comes from a substance called chlorophyll. This process does not occur without light. I will show this topic with an experiment tomorrow, don't forget to bring your notebooks.
```

**2. koşu** (bitti)

```text
Plants produce their own food using sunlight; we call this photosynthesis. The green color in leaves comes from a substance called chlorophyll. This process does not occur without light. I will show this topic with an experiment tomorrow, don't forget to bring your notebooks.
```

**İki çıktı aynı mı:** evet

**Modele giden sözlük terimleri:** yok

**Ek işlemler:** 1. koşu: yok · 2. koşu: yok

| | İlk metin | Toplam |
|---|---|---|
| 1. koşu | 3.83 s | 12.74 s |
| 2. koşu | 3.95 s | 12.84 s |

## K3 · TR→EN · Hava durumu spikeri

**Kaynak metin**

```text
İyi akşamlar. Yarın Marmara Bölgesi'nde parçalı bulutlu bir hava bekleniyor. İstanbul'da sıcaklık gündüz 14, gece 8 derece civarında olacak. Kuzeydoğudan saatte 30 kilometreye varan rüzgâr esecek; öğleden sonra sağanak yağış ihtimali yüzde 40. Hafta sonuna doğru sıcaklıklar mevsim normallerinin altına düşecek.
```

Dikkat (yalnız değerlendirme için, modele gitmedi): 14/8 derece, kuzeydoğu, 30 km, %40, normallerin altına

**1. koşu** (bitti)

```text
Good evening. Partly cloudy weather is expected in the Marmara Region tomorrow. In Istanbul, temperatures will be around 14 degrees during the day and 8 degrees at night. Winds will blow from the northeast reaching up to 30 kilometers per hour; there is a 40 percent chance of showers in the afternoon. Temperatures will drop below seasonal norms towards the weekend.
```

**2. koşu** (bitti)

```text
Good evening. Partly cloudy weather is expected in the Marmara Region tomorrow. In Istanbul, temperatures will be around 14 degrees during the day and 8 degrees at night. Winds will blow from the northeast reaching up to 30 kilometers per hour; there is a 40 percent chance of showers in the afternoon. Temperatures will drop below seasonal norms towards the weekend.
```

**İki çıktı aynı mı:** evet

**Modele giden sözlük terimleri:** yok

**Ek işlemler:** 1. koşu: yok · 2. koşu: yok

| | İlk metin | Toplam |
|---|---|---|
| 1. koşu | 4.40 s | 17.49 s |
| 2. koşu | 4.65 s | 17.75 s |

## K4 · TR→EN · Satış elemanı, ürün tanıtımı

**Kaynak metin**

```text
Bu model hem hafif hem de çok sessiz çalışıyor. Bataryası tek şarjla yaklaşık 8 saat dayanıyor, iki yıl garantisi de var. Fiyatı 12.499 TL ama bu hafta peşin alana yüzde 10 indirim yapıyoruz. Beğenmezseniz 14 gün içinde iade edebilirsiniz.
```

Dikkat (yalnız değerlendirme için, modele gitmedi): 12.499 TL → 12,499, %10, peşin, 14 gün

**1. koşu** (bitti)

```text
This model is both lightweight and runs very quietly. Its battery lasts about 8 hours on a single charge, and it also comes with a two-year warranty. The price is 12,499 TL, but we are offering a 10 percent discount for those who pay in cash this week. If you don't like it, you can return it within 14 days.
```

**2. koşu** (bitti)

```text
This model is both lightweight and runs very quietly. Its battery lasts about 8 hours on a single charge, and it also comes with a two-year warranty. The price is 12,499 TL, but we are offering a 10 percent discount for those who pay in cash this week. If you don't like it, you can return it within 14 days.
```

**İki çıktı aynı mı:** evet

**Modele giden sözlük terimleri:** yok

**Ek işlemler:** 1. koşu: yok · 2. koşu: yok

| | İlk metin | Toplam |
|---|---|---|
| 1. koşu | 4.12 s | 18.24 s |
| 2. koşu | 4.03 s | 18.13 s |

## K5 · TR→EN · Garson, menü önerisi

**Kaynak metin**

```text
Bugünün çorbası mercimek, yanında limon ve kızarmış ekmekle geliyor. Ana yemek olarak ızgara levrek öneririm, çok taze. Acı sevmiyorsanız sosu ayrı getirebilirim. Tatlı olarak künefemiz meşhurdur ama biraz beklemeniz gerekir, sıcak hazırlanıyor.
```

Dikkat (yalnız değerlendirme için, modele gitmedi): levrek, "acı sevmiyorsanız", künefe

**1. koşu** (bitti)

```text
Today's soup is lentil, served with lemon and toasted bread. I recommend grilled sea bass for the main course; it's very fresh. If you don't like spicy food, I can bring the sauce on the side. Our kunefe is famous for dessert, but you'll have to wait a bit as it's prepared hot.
```

**2. koşu** (bitti)

```text
Today's soup is lentil, served with lemon and toasted bread. I recommend grilled sea bass for the main course; it's very fresh. If you don't like spicy food, I can bring the sauce on the side. Our kunefe is famous for dessert, but you'll have to wait a bit as it's prepared hot.
```

**İki çıktı aynı mı:** evet

**Modele giden sözlük terimleri:** yok

**Ek işlemler:** 1. koşu: yok · 2. koşu: yok

| | İlk metin | Toplam |
|---|---|---|
| 1. koşu | 3.82 s | 16.82 s |
| 2. koşu | 4.02 s | 16.56 s |

## K6 · TR→EN · Otel resepsiyonu

**Kaynak metin**

```text
Hoş geldiniz! Odanız üçüncü katta, deniz manzaralı. Kahvaltı sabah 7 ile 10 arasında lobinin yanındaki restoranda veriliyor. Çıkış saati öğlen 12, isterseniz eşyalarınızı resepsiyonda bırakabilirsiniz. Wi-Fi şifresi kartın arkasında yazıyor.
```

Dikkat (yalnız değerlendirme için, modele gitmedi): "kart" burada oda kartı (board olmamalı), saatler

**1. koşu** (bitti)

```text
Welcome! Your room is on the third floor with a sea view. Breakfast is served in the restaurant next to the lobby between 7 and 10 AM. Check-out time is 12 PM; if you wish, you can leave your belongings at the reception. The Wi-Fi password is written on the back of the board.
```

**2. koşu** (bitti)

```text
Welcome! Your room is on the third floor with a sea view. Breakfast is served in the restaurant next to the lobby between 7 and 10 AM. Check-out time is 12 PM; if you wish, you can leave your belongings at the reception. The Wi-Fi password is written on the back of the board.
```

**İki çıktı aynı mı:** evet

**Modele giden sözlük terimleri:** Wi-Fi; kart → board

**Ek işlemler:** 1. koşu: yok · 2. koşu: yok

| | İlk metin | Toplam |
|---|---|---|
| 1. koşu | 4.58 s | 16.95 s |
| 2. koşu | 4.75 s | 16.83 s |

## K7 · TR→EN · Taksi şoförü, sohbet

**Kaynak metin**

```text
Bu saatte köprü çok kalabalık oluyor, ben sahil yolundan gideyim. Biraz uzun ama trafiğe takılmayız. Siz buralı değilsiniz galiba? İstanbul'un en güzel mevsimi bence sonbahar.
```

Dikkat (yalnız değerlendirme için, modele gitmedi): konuşma dili, "buralı değilsiniz galiba"

**1. koşu** (bitti)

```text
The bridge gets very crowded at this hour, so I'll take the coastal road. It's a bit longer, but we won't get stuck in traffic. You aren't from around here, are you? I think autumn is the best season in Istanbul.
```

**2. koşu** (bitti)

```text
The bridge gets very crowded at this hour, so I'll take the coastal road. It's a bit longer, but we won't get stuck in traffic. You aren't from around here, are you? I think autumn is the best season in Istanbul.
```

**İki çıktı aynı mı:** evet

**Modele giden sözlük terimleri:** yok

**Ek işlemler:** 1. koşu: yok · 2. koşu: yok

| | İlk metin | Toplam |
|---|---|---|
| 1. koşu | 3.66 s | 12.87 s |
| 2. koşu | 3.46 s | 12.87 s |

## K8 · TR→EN · Eczacı, ilaç kullanımı

**Kaynak metin**

```text
Bu ilacı günde iki kez, sabah ve akşam yemekten sonra alın. Tedaviyi yedi gün boyunca bırakmadan sürdürün, kendinizi iyi hissetseniz bile. Alkolle birlikte kullanmayın. Herhangi bir döküntü olursa ilacı kesip doktorunuza başvurun.
```

Dikkat (yalnız değerlendirme için, modele gitmedi): olumsuzluklar, "iyi hissetseniz bile", "ilacı kesip"

**1. koşu** (bitti)

```text
Take this medication twice a day, after breakfast and dinner. Continue the treatment for seven days without interruption, even if you feel better. Do not use it with alcohol. If any rash occurs, stop taking the medication and consult your doctor.
```

**2. koşu** (bitti)

```text
Take this medication twice a day, after breakfast and dinner. Continue the treatment for seven days without interruption, even if you feel better. Do not use it with alcohol. If any rash occurs, stop taking the medication and consult your doctor.
```

**İki çıktı aynı mı:** evet

**Modele giden sözlük terimleri:** yok

**Ek işlemler:** 1. koşu: yok · 2. koşu: yok

| | İlk metin | Toplam |
|---|---|---|
| 1. koşu | 3.80 s | 12.01 s |
| 2. koşu | 3.84 s | 12.05 s |

## K9 · TR→EN · Emlakçı, daire tanıtımı

**Kaynak metin**

```text
Daire 2+1, 95 metrekare ve binanın beşinci katında. Güney cephe olduğu için gün boyu güneş alıyor. Aidat aylık 1.200 TL, otopark ücretsiz. Metroya beş dakika yürüme mesafesinde; tek eksiği asansörün biraz eski olması.
```

Dikkat (yalnız değerlendirme için, modele gitmedi): 2+1, 95 m², güney, aidat, 1.200 TL

**1. koşu** (bitti)

```text
The apartment is a 2+1, 95 square meters, and located on the fifth floor of the building. Since it faces south, it gets sunlight all day long. The monthly maintenance fee is 1,200 TL, and parking is free. It's a five-minute walk to the metro; the only downside is that the elevator is a bit old.
```

**2. koşu** (bitti)

```text
The apartment is a 2+1, 95 square meters, and located on the fifth floor of the building. Since it faces south, it gets sunlight all day long. The monthly maintenance fee is 1,200 TL, and parking is free. It's a five-minute walk to the metro; the only downside is that the elevator is a bit old.
```

**İki çıktı aynı mı:** evet

**Modele giden sözlük terimleri:** yok

**Ek işlemler:** 1. koşu: yok · 2. koşu: yok

| | İlk metin | Toplam |
|---|---|---|
| 1. koşu | 4.00 s | 17.46 s |
| 2. koşu | 4.06 s | 17.48 s |

## K10 · TR→EN · Tamirci, araba

**Kaynak metin**

```text
Arabanızın balataları bitmiş, önce onları değiştirmemiz lazım. Motor yağı da azalmış ama acil değil, bir sonraki bakımda yaparız. Fren sesi bu yüzden geliyordu. Yarın öğlene kadar hazır olur, işçilikle birlikte toplam 3.800 TL tutar.
```

Dikkat (yalnız değerlendirme için, modele gitmedi): balata = brake pads, "acil değil", 3.800 TL

**1. koşu** (bitti)

```text
Your car's brake pads are worn out; we need to replace them first. The engine oil is also low, but it's not urgent; we can do that during the next service. That's where the braking noise was coming from. It will be ready by tomorrow noon, and the total cost including labor is 3,800 TL.
```

**2. koşu** (bitti)

```text
Your car's brake pads are worn out; we need to replace them first. The engine oil is also low, but it's not urgent; we can do that during the next service. That's where the braking noise was coming from. It will be ready by tomorrow noon, and the total cost including labor is 3,800 TL.
```

**İki çıktı aynı mı:** evet

**Modele giden sözlük terimleri:** yok

**Ek işlemler:** 1. koşu: yok · 2. koşu: yok

| | İlk metin | Toplam |
|---|---|---|
| 1. koşu | 3.77 s | 16.47 s |
| 2. koşu | 3.74 s | 16.44 s |

## K11 · TR→EN · Spor hocası

**Kaynak metin**

```text
Isınmadan başlamayın, sakatlanırsınız. Önce on dakika hafif tempoda koşun, sonra esneme hareketlerine geçeceğiz. Nefesinizi tutmayın, hareket sırasında düzenli nefes alın. Bugün ağırlıkları biraz artırıyoruz, zorlanırsanız hemen söyleyin.
```

Dikkat (yalnız değerlendirme için, modele gitmedi): olumsuz emirler, "nefesinizi tutmayın" (burada gerçek anlamda)

**1. koşu** (bitti)

```text
Don't start without warming up; you'll get injured. First, jog at a light pace for ten minutes, then we'll move on to stretching exercises. Don't hold your breath; breathe steadily while moving. We're increasing the weights a bit today; let me know immediately if you struggle.
```

**2. koşu** (bitti)

```text
Don't start without warming up; you'll get injured. First, jog at a light pace for ten minutes, then we'll move on to stretching exercises. Don't hold your breath; breathe steadily while moving. We're increasing the weights a bit today; let me know immediately if you struggle.
```

**İki çıktı aynı mı:** evet

**Modele giden sözlük terimleri:** yok

**Ek işlemler:** 1. koşu: yok · 2. koşu: yok

| | İlk metin | Toplam |
|---|---|---|
| 1. koşu | 3.63 s | 14.77 s |
| 2. koşu | 3.64 s | 14.79 s |

## K12 · TR→EN · Arkadaş daveti

**Kaynak metin**

```text
Cumartesi akşamı bizde ufak bir toplantı var, sen de gelsene. Fazla kalabalık olmayacak, beş altı kişiyiz. Bir şey getirmene gerek yok, yemekler bizden. Gelemezsen de dert etme, haber vermen yeter.
```

Dikkat (yalnız değerlendirme için, modele gitmedi): samimi üslup, "yemekler bizden", "dert etme"

**1. koşu** (bitti)

```text
We're having a small gathering at our place on Saturday evening; why don't you come too? It won't be too crowded, just about five or six of us. No need to bring anything, the food is on us. If you can't make it, don't worry about it, just let me know.
```

**2. koşu** (bitti)

```text
We're having a small gathering at our place on Saturday evening; why don't you come too? It won't be too crowded, just about five or six of us. No need to bring anything, the food is on us. If you can't make it, don't worry about it, just let me know.
```

**İki çıktı aynı mı:** evet

**Modele giden sözlük terimleri:** yok

**Ek işlemler:** 1. koşu: yok · 2. koşu: yok

| | İlk metin | Toplam |
|---|---|---|
| 1. koşu | 3.65 s | 15.67 s |
| 2. koşu | 3.81 s | 15.82 s |

## E1 · EN→TR · Tur rehberi, tarih

**Kaynak metin**

```text
This palace was built in the 15th century and served as the sultan's residence for nearly 400 years. On your left you can see the old kitchens, which once fed up to 4,000 people a day. Please don't touch the tiles; they're original and very fragile. We'll meet back here in 45 minutes.
```

Dikkat (yalnız değerlendirme için, modele gitmedi): 15. yüzyıl, 4,000 → 4.000, sol, olumsuz rica, 45 dakika

**1. koşu** (bitti)

```text
Bu saray 15. yüzyılda inşa edilmiş ve yaklaşık 400 yıl boyunca sultanın ikametgahı olarak hizmet vermiştir. Solunuzda, bir zamanlar günde 4.000 kişiye yemek veren eski mutfağı görebilirsiniz. Lütfen çinilere dokunmayın; bunlar orijinal ve çok kırılgandır. 45 dakika sonra burada buluşacağız.
```

**2. koşu** (bitti)

```text
Bu saray 15. yüzyılda inşa edilmiş ve yaklaşık 400 yıl boyunca sultanın ikametgahı olarak hizmet vermiştir. Solunuzda, bir zamanlar günde 4.000 kişiye yemek veren eski mutfağı görebilirsiniz. Lütfen çinilere dokunmayın; bunlar orijinal ve çok kırılgandır. 45 dakika sonra burada buluşacağız.
```

**İki çıktı aynı mı:** evet

**Modele giden sözlük terimleri:** yok

**Ek işlemler:** 1. koşu: yok · 2. koşu: yok

| | İlk metin | Toplam |
|---|---|---|
| 1. koşu | 4.34 s | 19.55 s |
| 2. koşu | 4.31 s | 19.47 s |

## E2 · EN→TR · Öğretmen, matematik

**Kaynak metin**

```text
Before we start, let me remind you that the exam is next Thursday, not Friday. Today we'll look at fractions: when you add them, the bottom numbers have to be the same. If they aren't, you need to find a common denominator first. Don't worry if this seems confusing at first; we'll practice it together.
```

Dikkat (yalnız değerlendirme için, modele gitmedi): "Thursday, not Friday", payda, olumsuzluklar

**1. koşu** (bitti)

```text
Başlamadan önce size sınavın Cuma değil, önümüzdeki Perşembe olduğunu hatırlatayım. Bugün kesirleri inceleyeceğiz: onları toplarken paydaların aynı olması gerekir. Eğer aynı değillerse, önce ortak bir payda bulmanız gerekir. İlk başta kafa karıştırıcı gelirse endişelenmeyin; birlikte pratik yapacağız.
```

**2. koşu** (bitti)

```text
Başlamadan önce size sınavın Cuma değil, önümüzdeki Perşembe olduğunu hatırlatayım. Bugün kesirleri inceleyeceğiz: onları toplarken paydaların aynı olması gerekir. Eğer aynı değillerse, önce ortak bir payda bulmanız gerekir. İlk başta kafa karıştırıcı gelirse endişelenmeyin; birlikte pratik yapacağız.
```

**İki çıktı aynı mı:** evet

**Modele giden sözlük terimleri:** yok

**Ek işlemler:** 1. koşu: yok · 2. koşu: yok

| | İlk metin | Toplam |
|---|---|---|
| 1. koşu | 3.90 s | 16.60 s |
| 2. koşu | 3.86 s | 16.62 s |

## E3 · EN→TR · Hava durumu spikeri

**Kaynak metin**

```text
Good evening. A cold front moving in from the northwest will bring heavy rain to most of the region tomorrow morning. Temperatures will struggle to reach 10 degrees, and winds could gust up to 60 kilometres per hour along the coast. Things should clear up by Sunday, though it'll stay chilly.
```

Dikkat (yalnız değerlendirme için, modele gitmedi): kuzeybatı, "struggle to reach 10", 60 km/s, "clear up"

**1. koşu** (bitti)

```text
İyi akşamlar. Kuzeybatıdan gelen bir soğuk cephe, yarın sabah bölgenin büyük kısmına şiddetli yağış getirecek. Sıcaklıklar 10 dereceye ulaşmakta zorlanacak ve kıyı şeridinde rüzgar saatte 60 kilometreye kadar esebilecek. Pazar gününe kadar hava açılsa da soğuk seyredecek.
```

**2. koşu** (bitti)

```text
İyi akşamlar. Kuzeybatıdan gelen bir soğuk cephe, yarın sabah bölgenin büyük kısmına şiddetli yağış getirecek. Sıcaklıklar 10 dereceye ulaşmakta zorlanacak ve kıyı şeridinde rüzgar saatte 60 kilometreye kadar esebilecek. Pazar gününe kadar hava açılsa da soğuk seyredecek.
```

**İki çıktı aynı mı:** evet

**Modele giden sözlük terimleri:** yok

**Ek işlemler:** 1. koşu: yok · 2. koşu: yok

| | İlk metin | Toplam |
|---|---|---|
| 1. koşu | 3.86 s | 18.61 s |
| 2. koşu | 3.79 s | 18.53 s |

## E4 · EN→TR · Satış elemanı

**Kaynak metin**

```text
This one's our best-seller. It's not the cheapest, but the battery lasts twice as long as the others. It comes with a two-year warranty, and if you buy it today, we'll throw in a free case. Would you like to try it?
```

Dikkat (yalnız değerlendirme için, modele gitmedi): "not the cheapest", "twice as long", "throw in"

**1. koşu** (bitti)

```text
Bu bizim en çok satan ürünümüz. En ucuzu değil ama bataryası diğerlerinin iki katı süre gidiyor. İki yıl garantisi var ve eğer bugün satın alırsanız yanına ücretsiz bir kılıf hediye ediyoruz. Denemek ister misiniz?
```

**2. koşu** (bitti)

```text
Bu bizim en çok satan ürünümüz. En ucuzu değil ama bataryası diğerlerinin iki katı süre gidiyor. İki yıl garantisi var ve eğer bugün satın alırsanız yanına ücretsiz bir kılıf hediye ediyoruz. Denemek ister misiniz?
```

**İki çıktı aynı mı:** evet

**Modele giden sözlük terimleri:** yok

**Ek işlemler:** 1. koşu: yok · 2. koşu: yok

| | İlk metin | Toplam |
|---|---|---|
| 1. koşu | 3.63 s | 13.25 s |
| 2. koşu | 3.61 s | 13.20 s |

## E5 · EN→TR · Havalimanı anonsu

**Kaynak metin**

```text
Ladies and gentlemen, flight TK1984 to Istanbul is now boarding at gate 12. Passengers seated in rows 20 to 35 are kindly asked to board first. Please have your boarding pass and passport ready. Due to strong headwinds, our flight time will be about 20 minutes longer than scheduled.
```

Dikkat (yalnız değerlendirme için, modele gitmedi): TK1984, kapı 12, sıra 20–35, "headwinds", 20 dakika

**1. koşu** (bitti)

```text
Sayın hanımefendiler ve beyefendiler, İstanbul'a gidecek TK1984 sefer sayılı uçuşumuz şu anda 12 numaralı kapıda uçağa alınıyor. 20 ile 35 arasındaki sıralarda oturan yolcularımızın öncelikli olarak uçağa binmeleri rica olunur. Lütfen biniş kartınızı ve pasaportunuzu hazır bulundurun. Güçlü karşı rüzgarlar nedeniyle uçuş süremiz planlanandan yaklaşık 20 dakika daha uzun sürecektir.
```

**2. koşu** (bitti)

```text
Sayın hanımefendiler ve beyefendiler, İstanbul'a gidecek TK1984 sefer sayılı uçuşumuz şu anda 12 numaralı kapıda uçağa alınıyor. 20 ile 35 arasındaki sıralarda oturan yolcularımızın öncelikli olarak uçağa binmeleri rica olunur. Lütfen biniş kartınızı ve pasaportunuzu hazır bulundurun. Güçlü karşı rüzgarlar nedeniyle uçuş süremiz planlanandan yaklaşık 20 dakika daha uzun sürecektir.
```

**İki çıktı aynı mı:** evet

**Modele giden sözlük terimleri:** yok

**Ek işlemler:** 1. koşu: yok · 2. koşu: yok

| | İlk metin | Toplam |
|---|---|---|
| 1. koşu | 3.77 s | 23.77 s |
| 2. koşu | 3.73 s | 23.74 s |

## E6 · EN→TR · Müşteri hizmetleri

**Kaynak metin**

```text
Thanks for calling. I can see your order was shipped yesterday, so it should arrive within two to three business days. If it doesn't show up by Friday, just give us a call back and we'll send a replacement at no extra cost. Is there anything else I can help you with?
```

Dikkat (yalnız değerlendirme için, modele gitmedi): iş günü, "if it doesn't show up", ücretsiz yenisi

**1. koşu** (bitti)

```text
Aradığınız için teşekkürler. Siparişinizin dün kargolandığını görebiliyorum, bu yüzden iki ila üç iş günü içinde ulaşması gerekir. Eğer Cuma gününe kadar gelmezse, bizi tekrar arayın; ek bir ücret ödemeden yerine yenisini göndeririz. Yardımcı olabileceğim başka bir şey var mı?
```

**2. koşu** (bitti)

```text
Aradığınız için teşekkürler. Siparişinizin dün kargolandığını görebiliyorum, bu yüzden iki ila üç iş günü içinde ulaşması gerekir. Eğer Cuma gününe kadar gelmezse, bizi tekrar arayın; ek bir ücret ödemeden yerine yenisini göndeririz. Yardımcı olabileceğim başka bir şey var mı?
```

**İki çıktı aynı mı:** evet

**Modele giden sözlük terimleri:** yok

**Ek işlemler:** 1. koşu: yok · 2. koşu: yok

| | İlk metin | Toplam |
|---|---|---|
| 1. koşu | 3.75 s | 15.89 s |
| 2. koşu | 3.80 s | 15.97 s |

## E7 · EN→TR · Doktor

**Kaynak metin**

```text
It looks like a mild sprain, nothing's broken. Try to keep weight off that ankle for a few days and put ice on it for 15 minutes at a time. If the swelling hasn't gone down by next week, come back and we'll take an X-ray.
```

Dikkat (yalnız değerlendirme için, modele gitmedi): "nothing's broken", "keep weight off", "hasn't gone down"

**1. koşu** (bitti)

```text
Hafif bir burkulma gibi görünüyor, kırık yok. Birkaç gün boyunca o bileğine ağırlık vermemeye çalış ve her seferinde 15 dakika boyunca buz uygula. Eğer önümüzdeki haftaya kadar şişlik inmezse geri gel, röntgen çekeriz.
```

**2. koşu** (bitti)

```text
Hafif bir burkulma gibi görünüyor, kırık yok. Birkaç gün boyunca o bileğine ağırlık vermemeye çalış ve her seferinde 15 dakika boyunca buz uygula. Eğer önümüzdeki haftaya kadar şişlik inmezse geri gel, röntgen çekeriz.
```

**İki çıktı aynı mı:** evet

**Modele giden sözlük terimleri:** yok

**Ek işlemler:** 1. koşu: yok · 2. koşu: yok

| | İlk metin | Toplam |
|---|---|---|
| 1. koşu | 3.98 s | 14.77 s |
| 2. koşu | 3.90 s | 14.68 s |

## E8 · EN→TR · Aşçı, yemek programı

**Kaynak metin**

```text
First, chop the onions finely and fry them until they're golden, not brown. Add the garlic last, because it burns quickly. Then pour in the tomatoes and let it simmer for about 20 minutes. Season to taste, and don't forget a pinch of sugar to balance the acidity.
```

Dikkat (yalnız değerlendirme için, modele gitmedi): "golden, not brown", "simmer", "season to taste"

**1. koşu** (bitti)

```text
Öncelikle soğanları ince ince doğrayın ve kahverengiye dönmeden altın rengi alana kadar kavurun. Sarımsağı en son ekleyin çünkü çabuk yanar. Ardından domatesleri dökün ve yaklaşık 20 dakika kısık ateşte pişirin. Damak tadınıza göre baharatlandırın ve asiditeyi dengelemek için bir tutam şekeri unutmayın.
```

**2. koşu** (bitti)

```text
Öncelikle soğanları ince ince doğrayın ve kahverengiye dönmeden altın rengi alana kadar kavurun. Sarımsağı en son ekleyin çünkü çabuk yanar. Ardından domatesleri dökün ve yaklaşık 20 dakika kısık ateşte pişirin. Damak tadınıza göre baharatlandırın ve asiditeyi dengelemek için bir tutam şekeri unutmayın.
```

**İki çıktı aynı mı:** evet

**Modele giden sözlük terimleri:** yok

**Ek işlemler:** 1. koşu: yok · 2. koşu: yok

| | İlk metin | Toplam |
|---|---|---|
| 1. koşu | 3.70 s | 19.00 s |
| 2. koşu | 3.75 s | 19.03 s |

## E9 · EN→TR · Emlak danışmanı

**Kaynak metin**

```text
The flat is on the third floor and gets plenty of natural light in the afternoon. The kitchen was renovated last year, but the bathroom could use some work. Rent is £1,450 a month, bills not included. The landlord doesn't allow pets, I'm afraid.
```

Dikkat (yalnız değerlendirme için, modele gitmedi): £1,450, "bills not included", "could use some work", evcil hayvan yasağı

**1. koşu** (bitti)

```text
Daire üçüncü katta ve öğleden sonraları bolca doğal ışık alıyor. Mutfak geçen yıl yenilendi ancak banyonun biraz tadilat görmesi gerekiyor. Kira aylık 1.450 sterlin, faturalar dahil değil. Maalesef ev sahibi evcil hayvanlara izin vermiyor.
```

**2. koşu** (bitti)

```text
Daire üçüncü katta ve öğleden sonraları bolca doğal ışık alıyor. Mutfak geçen yıl yenilendi ancak banyonun biraz tadilat görmesi gerekiyor. Kira aylık 1.450 sterlin, faturalar dahil değil. Maalesef ev sahibi evcil hayvanlara izin vermiyor.
```

**İki çıktı aynı mı:** evet

**Modele giden sözlük terimleri:** yok

**Ek işlemler:** 1. koşu: yok · 2. koşu: yok

| | İlk metin | Toplam |
|---|---|---|
| 1. koşu | 3.61 s | 15.29 s |
| 2. koşu | 3.79 s | 15.43 s |

## E10 · EN→TR · Antrenör, takım konuşması

**Kaynak metin**

```text
Great effort out there today, but we can't keep giving away easy goals. Our defence needs to stay tighter in the second half. Don't panic if they score first; we've come back from worse. Let's go out and enjoy it.
```

Dikkat (yalnız değerlendirme için, modele gitmedi): "giving away easy goals", "we've come back from worse"

**1. koşu** (bitti)

```text
Bugün harika bir çaba gösterdiniz ama kolay goller yemeye devam edemeyiz. Savunmamız ikinci yarıda daha sıkı durmalı. İlk golü onlar atarsa panik yapmayın; daha kötü durumlardan geri döndük. Hadi çıkalım ve tadını çıkaralım.
```

**2. koşu** (bitti)

```text
Bugün harika bir çaba gösterdiniz ama kolay goller yemeye devam edemeyiz. Savunmamız ikinci yarıda daha sıkı durmalı. İlk golü onlar atarsa panik yapmayın; daha kötü durumlardan geri döndük. Hadi çıkalım ve tadını çıkaralım.
```

**İki çıktı aynı mı:** evet

**Modele giden sözlük terimleri:** yok

**Ek işlemler:** 1. koşu: yok · 2. koşu: yok

| | İlk metin | Toplam |
|---|---|---|
| 1. koşu | 3.52 s | 14.13 s |
| 2. koşu | 3.66 s | 14.28 s |

## E11 · EN→TR · Komşu sohbeti

**Kaynak metin**

```text
Morning! Did you hear they're finally fixing the road next week? It's going to be noisy for a few days, but it's about time. By the way, your parcel came while you were out, so I took it in for you.
```

Dikkat (yalnız değerlendirme için, modele gitmedi): "it's about time", "took it in", samimi üslup

**1. koşu** (bitti)

```text
Günaydın! Önümüzdeki hafta sonunda yolu nihayet tamir edeceklerini duydun mu? Birkaç gün gürültülü olacak ama artık vakti gelmişti. Bu arada, sen dışarıdayken paketin geldi, o yüzden senin için içeri aldım.
```

**2. koşu** (bitti)

```text
Günaydın! Önümüzdeki hafta sonunda yolu nihayet tamir edeceklerini duydun mu? Birkaç gün gürültülü olacak ama artık vakti gelmişti. Bu arada, sen dışarıdayken paketin geldi, o yüzden senin için içeri aldım.
```

**İki çıktı aynı mı:** evet

**Modele giden sözlük terimleri:** yok

**Ek işlemler:** 1. koşu: yok · 2. koşu: yok

| | İlk metin | Toplam |
|---|---|---|
| 1. koşu | 3.51 s | 13.26 s |
| 2. koşu | 3.39 s | 13.14 s |

## E12 · EN→TR · Klinikten sesli mesaj

**Kaynak metin**

```text
Hi, this is Sarah from the dental clinic calling to confirm your appointment on Tuesday the 3rd at 2:30 pm. If you can't make it, please let us know at least 24 hours in advance, otherwise there may be a cancellation fee. See you then!
```

Dikkat (yalnız değerlendirme için, modele gitmedi): 3'ü salı, 2:30 pm → 14.30, 24 saat, iptal ücreti

**1. koşu** (bitti)

```text
Merhaba, ben diş kliniğinden Sarah; 3 Salı günü saat 14:30'daki randevunuzu onaylamak için arıyorum. Eğer gelemiyorsanız lütfen bize en az 24 saat önceden haber verin, aksi takdirde bir iptal ücreti uygulanabilir. O zaman görüşmek üzere!
```

**2. koşu** (bitti)

```text
Merhaba, ben diş kliniğinden Sarah; 3 Salı günü saat 14:30'daki randevunuzu onaylamak için arıyorum. Eğer gelemiyorsanız lütfen bize en az 24 saat önceden haber verin, aksi takdirde bir iptal ücreti uygulanabilir. O zaman görüşmek üzere!
```

**İki çıktı aynı mı:** evet

**Modele giden sözlük terimleri:** yok

**Ek işlemler:** 1. koşu: yok · 2. koşu: yok

| | İlk metin | Toplam |
|---|---|---|
| 1. koşu | 3.69 s | 15.71 s |
| 2. koşu | 3.61 s | 15.71 s |

## Süre tablosu

| Metin | Yön | 1. koşu ilk metin | 1. koşu toplam | 2. koşu ilk metin | 2. koşu toplam |
|---|---|---|---|---|---|
| K1 | TR→EN | 4.27 s | 15.98 s | 3.85 s | 15.48 s |
| K2 | TR→EN | 3.83 s | 12.74 s | 3.95 s | 12.84 s |
| K3 | TR→EN | 4.40 s | 17.49 s | 4.65 s | 17.75 s |
| K4 | TR→EN | 4.12 s | 18.24 s | 4.03 s | 18.13 s |
| K5 | TR→EN | 3.82 s | 16.82 s | 4.02 s | 16.56 s |
| K6 | TR→EN | 4.58 s | 16.95 s | 4.75 s | 16.83 s |
| K7 | TR→EN | 3.66 s | 12.87 s | 3.46 s | 12.87 s |
| K8 | TR→EN | 3.80 s | 12.01 s | 3.84 s | 12.05 s |
| K9 | TR→EN | 4.00 s | 17.46 s | 4.06 s | 17.48 s |
| K10 | TR→EN | 3.77 s | 16.47 s | 3.74 s | 16.44 s |
| K11 | TR→EN | 3.63 s | 14.77 s | 3.64 s | 14.79 s |
| K12 | TR→EN | 3.65 s | 15.67 s | 3.81 s | 15.82 s |
| E1 | EN→TR | 4.34 s | 19.55 s | 4.31 s | 19.47 s |
| E2 | EN→TR | 3.90 s | 16.60 s | 3.86 s | 16.62 s |
| E3 | EN→TR | 3.86 s | 18.61 s | 3.79 s | 18.53 s |
| E4 | EN→TR | 3.63 s | 13.25 s | 3.61 s | 13.20 s |
| E5 | EN→TR | 3.77 s | 23.77 s | 3.73 s | 23.74 s |
| E6 | EN→TR | 3.75 s | 15.89 s | 3.80 s | 15.97 s |
| E7 | EN→TR | 3.98 s | 14.77 s | 3.90 s | 14.68 s |
| E8 | EN→TR | 3.70 s | 19.00 s | 3.75 s | 19.03 s |
| E9 | EN→TR | 3.61 s | 15.29 s | 3.79 s | 15.43 s |
| E10 | EN→TR | 3.52 s | 14.13 s | 3.66 s | 14.28 s |
| E11 | EN→TR | 3.51 s | 13.26 s | 3.39 s | 13.14 s |
| E12 | EN→TR | 3.69 s | 15.71 s | 3.61 s | 15.71 s |

**İki koşuda aynı çıkan metin sayısı:** 24 / 24
