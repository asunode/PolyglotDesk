# Detaylı Çevir ölçümü v3 — sonuçlar (ham kayıt)

Setler: `doc/olcum/detayli-test-seti-v1.md` (D1–D10), `doc/olcum/dogrulama-seti-v1.md` (V1–V5), `doc/olcum/kontrol-seti-v2.md` (G1–G3), `doc/olcum/dogrulama-seti-v2.md` (W1–W8). Betik: `doc/olcum/bench_detayli_v3.py`. Ham veri: `doc/olcum/detayli-test-v3-ham.json`. v2 hızlı ve Detaylı çıktıları: `doc/olcum/detayli-test-v2-ham.json` (Adım 6).
Koşu: 2026-11-19 18:27:40 +0300 – 2026-11-19 18:52:07 +0300. Model gemma4:12b-it-qat, yalnız CPU (num_gpu 0), num_ctx 8192, temperature 0, seed 42. Uygulamanın çeviri yolu: hızlı çeviri `Cevirici`, Detaylı Çevir `DetayliCevirici` (bilgi araması PostgreSQL `cevirmen`, `cevirmen_okur` rolüyle). Her testte önce hızlı çeviri, hemen ardından Detaylı Çevir; D1–D10, V1–V5, G1–G3, W1–W8 sırasıyla.

Notlar:
- Bütün çıktılar ham kayıttan birebir alınmıştır; düzeltilmemiş, kısaltılmamıştır.
- "İlk metin": çeviri başlatıldıktan sonra ekranda ilk çeviri metninin görünmesine kadar geçen süre.
- "Denetimin değiştirdikleri": taslak ile son çıktı arasındaki satır farkı (`-` taslaktaki satır, `+` son çıktıdaki satır).
- "Kalın yazı düzeltmesi": kod denetimi kalın yazının kaybolduğunu ya da olumsuzlukta yanlış yerde olduğunu bulduğunda yapılanlar (kod yerleştirmesi ya da modelin söylediği birebir parçalar; hızlı çeviride ek istek sayısı ayrıca).
- "Kod denetimi": `cevirmen/bicim.py`. "Denetimden önce" bulunanlar denetim geçişinde modele bildirildi; "denetimden sonra" son çıktıda kalanlardır.
- "Denetimin kararı": modelin JSON cevabı birebir. Düzeltmeleri kod uygular (`cevirmen/denetim.py`): "uygulanan", "geri alınan" (güvenlik kontrolünün reddettiği, nedeniyle) ve "uygulanamayan" (taslakta bulunamayan vb.) ayrı listelenir.
- "Dikkat kelimeleri modele ulaştı mı": mekanik denetim. Dikkat satırı virgül/noktalı virgülle öğelere ayrılır; öğede tırnak içi varsa o, yoksa "=" işaretinin solu aranır; parantez içi notlar ve sondaki noktalama aranmaz. Aranan, bir bilgi kaydının başlığıyla aynıysa ya da kaydın modele giden metninde ayrı kelime olarak geçiyorsa "evet" (eşleşen kayıtlar yanında). Çekimli/yalın biçim farkı eşleşme sayılmaz.

## D1 · TR→EN (detayli-test-seti-v1)

**Kaynak metin**

```text
Sabahtan beri yüzü gülmüyordu ama gül bahçesine girince yüzünde bir gülümseme belirdi. Ağabeyim de ona "Gözün aydın, sonunda bahçe bitti!" dedi.
```

**Hızlı çeviri** — ilk metin 3.51 s, toplam 10.91 s (bitti)

```text
He hadn't smiled since this morning, but a smile appeared on his face as soon as he entered the rose garden. My older brother also said to him, "Good news, the garden is finally finished!"
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 0): yok

**v2 hızlı çeviri (Adım 6)**

```text
He hadn't smiled since this morning, but a smile appeared on his face as soon as he entered the rose garden. My older brother also said to him, "Good news, the garden is finally finished!"
```

**v2 Detaylı Çevir — son çıktı (Adım 6)**

```text
She hadn't smiled since this morning, but a smile appeared on her face when she entered the rose garden. My older brother also said to her, "Congratulations! The garden is finally finished!"
```

**Detaylı Çevir — denetimden önceki taslak**

```text
She hadn't smiled since this morning, but a smile appeared on her face when she entered the rose garden. My older brother also said to her, "Congratulations! The garden is finally finished!"
```

**Detaylı Çevir — son çıktı** (bitti)

```text
She hadn't smiled since this morning, but a smile appeared on her face when she entered the rose garden. My older brother also said to her, "Congratulations! The garden is finally finished!"
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": [],
  "bold": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Kalın yazı düzeltmesi (Detaylı)**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (11)**

- [Wiktionary · kalıp/deyim] "gözün aydın" (phrase): congratulations!
- [Wiktionary · kalıp/deyim] "güle güle" (adv): smilingly, laughingly; in happiness, with merriment, happily
- [Wiktionary · kalıp/deyim] "güle güle" (intj): Goodbye!, Bye!
- [Wiktionary · çok anlamlı kelime] yüz: (noun) face; (noun) lining; (noun) face, surface, cutting edge; (noun) side, aspect
- [Wiktionary · çok anlamlı kelime] sabah: (adv) in the morning; (noun) morning; (noun) dawn prayer, fajr
- [Wiktionary · çok anlamlı kelime] son: (adj) last, final; (noun) end, ending; (noun) consequence, result, conclusion; (noun) placenta
- [Wiktionary · çok anlamlı kelime] demek: (adv) so, that is to say; (verb) to say; (adj) to mean; (verb) to assume, to suppose
- [Wiktionary · çok anlamlı kelime] girmek: (verb) to enter, to go in; (verb) to go in for, to take; (verb) (a season, time &c.) to arrive
- [Wiktionary · çok anlamlı kelime] belirmek: (verb) to appear, to manifest; (verb) to become obvious or distinguishable, to form, to take shape; (verb) to become clear
- [Tatoeba · örnek cümle] Turkish: Onun yüzünde bir gülümseme yayılıyordu. | English: A smile spread across her face.
- [Tatoeba · örnek cümle] Turkish: Sonunda bitti. | English: It's finally over.

**Modele giden sözlük terimleri (0)**

- yok

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: gül, yüz, gözün aydın)

- gül: hayır
- yüz: evet — yüz [çok anlamlı kelime, Wiktionary]
- gözün aydın: evet — gözün aydın [kalıp/deyim, Wiktionary]

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 10.91 s | 3.51 s |
| Detaylı Çevir | 0.91 s | 22.60 s | 21.78 s | 45.29 s | 16.35 s |

## D2 · TR→EN (detayli-test-seti-v1)

**Kaynak metin**

```text
Öğleden sonra dolu yağdı; bahçedeki domatesler mahvoldu.
Depo dolu, yarın sabah erkenden yola çıkabiliriz.
Bu akşam yüz kişilik bir yemek var, çay kenarındaki salonda.
```

**Hızlı çeviri** — ilk metin 5.94 s, toplam 14.33 s (bitti)

```text
It rained heavily this afternoon; the tomatoes in the garden were ruined.
The warehouse is full, we can hit the road early tomorrow morning.
There's a dinner for a hundred people tonight, in the hall by the tea area.
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 0): yok

**v2 hızlı çeviri (Adım 6)**

```text
It hailed this afternoon; the tomatoes in the garden were ruined.
The warehouse is full, we can hit the road early tomorrow morning.
There's a dinner for a hundred people this evening, in the hall by the tea area.
```

**v2 Detaylı Çevir — son çıktı (Adım 6)**

```text
Hail fell this afternoon; the tomatoes in the garden were ruined.
The warehouse is full, we can head out early tomorrow morning.
There is a dinner for a hundred people this evening, in the hall by the brook.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Hail fell this afternoon; the tomatoes in the garden were ruined.
The warehouse is full, we can head out early tomorrow morning.
There is a dinner for a hundred people this evening, in the hall by the brook.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Hail fell this afternoon; the tomatoes in the garden were ruined.
The warehouse is full, we can head out early tomorrow morning.
There is a dinner for a hundred people this evening, in the hall by the brook.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": [],
  "bold": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Kalın yazı düzeltmesi (Detaylı)**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (12)**

- [Wiktionary · kalıp/deyim] "öğleden sonra" (adv): in the afternoon, p.m.
- [Wiktionary · çok anlamlı kelime] dolu: (adj) full; (noun) hail
- [Wiktionary · çok anlamlı kelime] çay: (noun) tea (plant); (noun) tea (the dried leaves or buds of the tea plant); (noun) tea (the drink made by infusing these dried leaves or buds in hot wat…; (noun) A small river, a brook.
- [Wiktionary · çok anlamlı kelime] kişilik: (adj) divided by a certain number of people, made for a certain number of p…; (noun) personality, character, identity; (noun) synonym of yabanlık; (adj) made up of or consisting of a certain number of people
- [Wiktionary · çok anlamlı kelime] yol: (noun) path, road, way; (noun) voyage
- [Wiktionary · çok anlamlı kelime] çıkmak: (verb) to leave, exit, quit, get out; (verb) to get out; (verb) to happen, occur; (verb) to climb
- [Wiktionary · çok anlamlı kelime] salon: (noun) living room; (noun) shop, store
- [Tatoeba · örnek cümle] Turkish: Yarın yola çıkabilirim. | English: I can head out tomorrow.
- [Tatoeba · örnek cümle] Turkish: Yola erken çıkabilir miyim? | English: Can I take off early?
- [Tatoeba · örnek cümle] Turkish: Bu öğleden sonra yağmur yağdı. | English: It rained this afternoon.
- [Tatoeba · örnek cümle] Turkish: Dün öğleden sonra yağmur yağdı. | English: It rained yesterday afternoon.
- [Tatoeba · örnek cümle] Turkish: Salonda yüz kişi vardı. | English: There were a hundred people in the hall.

**Modele giden sözlük terimleri (0)**

- yok

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: dolu, yüz, çay)

- dolu: evet — dolu [çok anlamlı kelime, Wiktionary]
- yüz: evet — Salonda yüz kişi vardı. [örnek cümle, Tatoeba]
- çay: evet — çay [çok anlamlı kelime, Wiktionary]

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 14.33 s | 5.94 s |
| Detaylı Çevir | 1.04 s | 24.53 s | 22.05 s | 47.63 s | 17.34 s |

## D3 · EN→TR (detayli-test-seti-v1)

**Kaynak metin**

```text
It's not that I don't trust you; I just don't want to put all my eggs in one basket. Let's not jump the gun and wait for the final numbers.
```

**Hızlı çeviri** — ilk metin 5.50 s, toplam 11.15 s (bitti)

```text
Sana güvenmediğimden değil; sadece tüm yumurtalarımı aynı sepete koymak istemiyorum. Acele edip son rakamları bekleyelim.
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 0): yok

**v2 hızlı çeviri (Adım 6)**

```text
Sana güvenmediğimden değil, sadece tüm yumurtalarımı aynı sepete koymak istemiyorum. Henüz acele etmeyelim ve son rakamları bekleyelim.
```

**v2 Detaylı Çevir — son çıktı (Adım 6)**

```text
Sana güvenmediğimden değil; sadece tüm yumurtalarımı aynı sepete koymak istemiyorum. Acele edip işi bozmayalım, son rakamları bekleyelim.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Sana güvenmediğimden değil, sadece tüm yumurtalarımı aynı sepete koymak istemiyorum. Acele edip işi bozmayalım ve son rakamları bekleyelim.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Sana güvenmediğimden değil, sadece tüm yumurtalarımı aynı sepete koymak istemiyorum. Acele edip işi bozmayalım ve son rakamları bekleyelim.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": [],
  "bold": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Kalın yazı düzeltmesi (Detaylı)**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (10)**

- [Wiktionary · kalıp/deyim] "put all one's eggs in one basket" (verb): To rely on a single source (as of income), rather than diversifying. [idiomatic]
- [Wiktionary · kalıp/deyim] "jump the gun" (verb): To begin a race too soon, before the starting gun goes off.; To act or begin too soon or without due caution.; To trade securities based on information that is… [idiomatic]
- [Wiktionary · kalıp/deyim] "and finally" (noun): A light news story reserved for the end of a bulletin when there is a lack of more important items; typically involving animals or other features supposed to b… [colloquial, idiomatic]
- [Wiktionary · kalıp/deyim] "not that" (conj): Used to indicate that the following clause is not true and that this negatively impacts the importance of the preceding clause.
- [Wiktionary · çok anlamlı kelime] trust: (noun) a group of businessmen or traders → tröst; (noun) confidence in or reliance on some person or quality → güven, güvenç, itibar; (verb) to place confidence in → güvenmek
- [Wiktionary · çok anlamlı kelime] number: (noun) abstract entity used to describe quantity → adet, rakam, sayı; (noun) mathematics: number → sayı; (noun) numeral → numara; (noun) quantity → sayı
- [Tatoeba · örnek cümle] English: Don't put all your eggs in one basket. | Turkish: Tüm kaynaklarını aynı işe yatırma.
- [Tatoeba · örnek cümle] English: Let's not wait for the others. | Turkish: Diğerlerini beklemeyelim.
- [Tatoeba · örnek cümle] English: Let's not jump the gun. | Turkish: Acele etmeyelim.
- [Tatoeba · örnek cümle] English: Put all your eggs in one basket and then watch that basket. | Turkish: Bütün yumurtalarını bir sepete koy ve sonra sepeti izle.

**Modele giden sözlük terimleri (0)**

- yok

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: not that, put all my eggs in one basket, jump the gun)

- not that: evet — not that [kalıp/deyim, Wiktionary]
- put all my eggs in one basket: hayır
- jump the gun: evet — jump the gun [kalıp/deyim, Wiktionary]; Let's not jump the gun. [örnek cümle, Tatoeba]

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 11.15 s | 5.50 s |
| Detaylı Çevir | 0.77 s | 24.39 s | 21.50 s | 46.66 s | 18.19 s |

## D4 · EN→TR (detayli-test-seti-v1)

**Kaynak metin**

```text
Make sure the board is **not** powered while you solder the header pins. If the brownout detector keeps firing, the issue is rarely the firmware itself.
```

**Hızlı çeviri** — ilk metin 5.71 s, toplam 12.88 s (bitti)

```text
Header pinlerini lehimlerken kartın güç **almadığından** emin olun. Eğer brownout dedektörü ateşlemeye devam ediyorsa, sorun nadiren firmware'nin kendisindedir.
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 0): kod (olumsuzluk sırası): Header pinlerini lehimlerken kartın güç **almadığından** emin olun. Eğer brownout dedektörü ateşlemeye devam ediyorsa, sorun nadiren firmware'nin kendisindedir.

**v2 hızlı çeviri (Adım 6)**

```text
Header pinlerini lehimlerken kartın **güç almadığından** emin olun. Eğer brownout dedektörü ateşlemeye devam ediyorsa, sorun nadiren firmware'nin kendisidir.
```

**v2 Detaylı Çevir — son çıktı (Adım 6)**

```text
Header pinlerini lehimlerken kartın güç almadığından emin olun. Eğer brownout dedektörü ateşlemeye devam ediyorsa, sorun nadiren firmware'in kendisidir.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Header pinlerini lehimlerken kartın güç almadığından emin olun. Eğer brownout dedektörü ateşlemeye devam ediyorsa, sorun nadiren firmware'in kendisidir.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Header pinlerini lehimlerken kartın güç **almadığından** emin olun. Eğer brownout dedektörü ateşlemeye devam ediyorsa, sorun nadiren firmware'in kendisidir.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": true,
  "errors": [
    {
      "type": "meaning",
      "draft_text": "güç almadığından",
      "corrected_text": "güç almıyor olduğundan",
      "reason": "The source says 'not powered', which means the power should be off. 'Güç almadığından' can mean it is not receiving power (but might still be on), whereas 'güç almıyor olduğundan' or 'enerji altında olmadığından' more accurately reflects that the power must be disconnected."
    }
  ],
  "bold": [
    "almadığından"
  ]
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- (meaning) “güç almadığından” → “güç almıyor olduğundan” — neden: taslakta bulunamadı

**Kalın yazı düzeltmesi (Detaylı)**

- kod (olumsuzluk sırası), denetimden önce: Header pinlerini lehimlerken kartın güç **almadığından** emin olun. Eğer brownout dedektörü ateşlemeye devam ediyorsa, sorun nadiren firmware'in kendisidir.

**Denetimin taslakta değiştirdikleri**

```diff
-Header pinlerini lehimlerken kartın güç almadığından emin olun. Eğer brownout dedektörü ateşlemeye devam ediyorsa, sorun nadiren firmware'in kendisidir.
+Header pinlerini lehimlerken kartın güç **almadığından** emin olun. Eğer brownout dedektörü ateşlemeye devam ediyorsa, sorun nadiren firmware'in kendisidir.
```

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (7)**

- [Wiktionary · çok anlamlı kelime] board: (noun) long, wide and thin piece of wood or other material → tahta; (noun) managing committee → heyet, kurul; (noun) short for blackboard, whiteboard, etc. → tahta; (noun) side of a ship → borda, sancak
- [Wiktionary · çok anlamlı kelime] power: (noun) electricity, electricity supply → güç; (noun) ability to affect or influence → güç, kuvvet; (noun) maths: product of equal factors → kuvvet, üs; (noun) people in charge of legal or political power → iktidar
- [Wiktionary · çok anlamlı kelime] solder: (noun) any of various alloys that are used to join small pieces of metal tog… → lehim; (verb) to join with solder → lehimlemek
- [Wiktionary · çok anlamlı kelime] pin: (noun) personal identification number → PIN kodu; (noun) slender object specially designed for use in bowling → kuka, labut, lobut; (noun) small nail → karfiçe; (verb) to fasten/attach with a pin → iliştirmek, pinlemek, sabitlemek
- [Wiktionary · çok anlamlı kelime] keep: (verb) of livestock: to raise; to care for → bakmak; (verb) to continue → -ip durmak, devam etmek; (verb) to maintain possession of → saklamak, tutmak; (verb) to maintain the condition of; to preserve → saklamak
- [Wiktionary · çok anlamlı kelime] fire: (noun) damaging occurrence of fire → yangın; (noun) heater or stove used in place of real fire → ocak; (noun) oxidation reaction → ateş, od; (verb) intransitive: to shoot → ateş etmek
- [Tatoeba · örnek cümle] English: You'd better not do that while Tom is here. | Turkish: Tom buradayken bunu yapmasan iyi olur.

**Modele giden sözlük terimleri (3)**

- [kullanıcı sözlüğü] firmware: keep in English
- [kullanıcı sözlüğü] brownout: keep in English
- [kullanıcı sözlüğü] board → kart

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: board, rarely)

- board: evet — board → kart [sözlük terimi, kullanıcı sözlüğü]; board [çok anlamlı kelime, Wiktionary]
- rarely: hayır

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 12.88 s | 5.71 s |
| Detaylı Çevir | 0.79 s | 24.18 s | 40.78 s | 65.75 s | 17.64 s |

## D5 · TR→EN (detayli-test-seti-v1)

**Kaynak metin**

```text
Kartı yeniden flash'ladım ama watchdog yine tetiklendi. Hatayı log'lardan buldum: stack overflow. Kartın yanındaki kartvizitte yazan numarayı arayıp destek istedim.
```

**Hızlı çeviri** — ilk metin 6.49 s, toplam 13.37 s (bitti)

```text
I flashed the board again, but the watchdog was triggered again. I found the error in the logs: stack overflow. I called the number on the business card next to the board and asked for support.
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 0): yok

**v2 hızlı çeviri (Adım 6)**

```text
I flashed the board again, but the watchdog was triggered again. I found the error in the logs: stack overflow. I called the number on the business card next to the board and asked for support.
```

**v2 Detaylı Çevir — son çıktı (Adım 6)**

```text
I flashed the board again, but the watchdog was triggered again. I found the error in the logs: stack overflow. I called the number on the business card next to the board and asked for support.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
I flashed the board again, but the watchdog was triggered again. I found the error in the logs: stack overflow. I called the number on the business card next to the board and asked for support.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
I flashed the board again, but the watchdog was triggered again. I found the error in the logs: stack overflow. I called the number on the business card next to the board and asked for support.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": [],
  "bold": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Kalın yazı düzeltmesi (Detaylı)**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (6)**

- [Wiktionary · çok anlamlı kelime] tetik: (noun) trigger; (adj) vigilant, watchful; (adj) requiring care and caution, delicate
- [Wiktionary · çok anlamlı kelime] bulmak: (verb) to find; (verb) to discover; (verb) to invent; (verb) to reach (a place, a time)
- [Wiktionary · çok anlamlı kelime] yazmak: (verb) to write, write down, inscribe; (verb) to burn (CD, DVD); (verb) to compose; (verb) to enroll, register; to enlist, sign, record, note down
- [Wiktionary · çok anlamlı kelime] aramak: (verb) to seek, to look for, to search; (verb) to phone, to telephone, to ring
- [Wiktionary · çok anlamlı kelime] destek: (noun) fulcrum; (noun) support; (noun) solidarity
- [Wiktionary · çok anlamlı kelime] istemek: (verb) to want, desire, wish; (verb) to ask for, seek, demand; (verb) to ask for (a woman) in marriage

**Modele giden sözlük terimleri (4)**

- [kullanıcı sözlüğü] watchdog: keep in English
- [kullanıcı sözlüğü] stack: keep in English
- [kullanıcı sözlüğü] log: keep in English
- [kullanıcı sözlüğü] kart → board

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: kart, kartvizit)

- kart: evet — kart → board [sözlük terimi, kullanıcı sözlüğü]
- kartvizit: hayır

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 13.37 s | 6.49 s |
| Detaylı Çevir | 1.05 s | 20.09 s | 21.55 s | 42.69 s | 14.01 s |

## D6 · EN→TR (detayli-test-seti-v1)

**Kaynak metin**

```text
Dear Ms. Demir, we regret to inform you that the shipment scheduled for 3 December will be delayed by approximately two weeks. We would be grateful for your understanding.
```

**Hızlı çeviri** — ilk metin 5.43 s, toplam 12.08 s (bitti)

```text
Sayın Bayan Demir, 3 Aralık için planlanan sevkiyatın yaklaşık iki hafta gecikeceğini üzülerek bildirmek isteriz. Anlayışınız için teşekkür ederiz.
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 0): yok

**v2 hızlı çeviri (Adım 6)**

```text
Sayın Bayan Demir,
3 Aralık için planlanan sevkiyatın yaklaşık iki hafta gecikeceğini üzülerek bildirmek isteriz. Anlayışınız için teşekkür ederiz.
```

**v2 Detaylı Çevir — son çıktı (Adım 6)**

```text
Sayın Demir, 3 Aralık için planlanan sevkiyatın yaklaşık iki hafta gecikeceğini üzülerek bildirmek isteriz. Anlayışınız için teşekkür ederiz.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Sayın Bayan Demir, 3 Aralık için planlanan sevkiyatın yaklaşık iki hafta gecikeceğini üzülerek bildirmek isteriz. Anlayışınız için teşekkür ederiz.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Sayın Bayan Demir, 3 Aralık için planlanan sevkiyatın yaklaşık iki hafta gecikeceğini üzülerek bildirmek isteriz. Anlayışınız için teşekkür ederiz.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": [],
  "bold": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Kalın yazı düzeltmesi (Detaylı)**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (4)**

- [Wiktionary · çok anlamlı kelime] dear: (adj) an informal way of addressing the recipient in a letter's opening line → sevgili; (adj) formal way of addressing → sayın; (adj) loved; lovable → sevgili, sevimli
- [Wiktionary · çok anlamlı kelime] shipment: (noun) load of goods → parti; (noun) the act of transporting goods → taşınma
- [Wiktionary · çok anlamlı kelime] delay: (noun) period of time before an event occurs; act of delaying → gecikme, rötar; (verb) to put off until a later time → ertelemek
- [Tatoeba · örnek cümle] English: Thank you for your understanding. | Turkish: Anlayışınız için teşekkür ederim.

**Modele giden sözlük terimleri (0)**

- yok

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: Ms., regret to inform)

- Ms.: hayır
- regret to inform: hayır

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 12.08 s | 5.43 s |
| Detaylı Çevir | 0.78 s | 17.32 s | 21.31 s | 39.41 s | 11.25 s |

## D7 · TR→EN (detayli-test-seti-v1)

**Kaynak metin**

```text
Güncelleme sırasında kartın gücünü **kesmeyin**; aksi halde bootloader bozulabilir ve kartı yeniden canlandırmak için UART üzerinden flash'lamanız gerekir.
```

**Hızlı çeviri** — ilk metin 5.98 s, toplam 12.14 s (bitti)

```text
Do **not** cut the power to the board during the update; otherwise, the bootloader may be corrupted and you will need to flash it via UART to revive the board.
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 0): kod (olumsuzluk sırası): Do **not** cut the power to the board during the update; otherwise, the bootloader may be corrupted and you will need to flash it via UART to revive the board.

**v2 hızlı çeviri (Adım 6)**

```text
Do not **cut** the power to the board during the update; otherwise, the bootloader may be corrupted and you will need to flash it via UART to revive the board.
```

**v2 Detaylı Çevir — son çıktı (Adım 6)**

```text
Do not **cut** the power to the board during the update; otherwise, the bootloader may break and you will need to flash it via UART to revive the board.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Do not **cut** the power to the board during the update; otherwise, the bootloader may break and you will need to flash it via UART to revive the board.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Do **not** cut the power to the board during the update; otherwise, the bootloader may break and you will need to flash it via UART to revive the board.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": [],
  "bold": [
    "not"
  ]
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Kalın yazı düzeltmesi (Detaylı)**

- kod (olumsuzluk sırası), denetimden önce: Do **not** cut the power to the board during the update; otherwise, the bootloader may break and you will need to flash it via UART to revive the board.

**Denetimin taslakta değiştirdikleri**

```diff
-Do not **cut** the power to the board during the update; otherwise, the bootloader may break and you will need to flash it via UART to revive the board.
+Do **not** cut the power to the board during the update; otherwise, the bootloader may break and you will need to flash it via UART to revive the board.
```

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (4)**

- [Wiktionary · çok anlamlı kelime] kesmek: (verb) to cut; (verb) to cut off, interrupt; (verb) to stop (talking, crying, etc.); (verb) to shave beard or moustache
- [Wiktionary · çok anlamlı kelime] bozulmak: (verb) to break, to stop working; (verb) to go bad, to spoil; (verb) to deteriorate; (verb) to sulk, to take offense
- [Wiktionary · çok anlamlı kelime] canlandırmak: (verb) to bring to life; (verb) to bring to consciousness; (verb) to revive; (verb) to resurrect
- [Wiktionary · çok anlamlı kelime] gerekmek: (verb) to be necessary, be needed, be required; (verb) to have (to do)

**Modele giden sözlük terimleri (3)**

- [kullanıcı sözlüğü] bootloader: keep in English
- [kullanıcı sözlüğü] UART: keep in English
- [kullanıcı sözlüğü] kart → board

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: kesmek, canlandırmak)

- kesmek: evet — kesmek [çok anlamlı kelime, Wiktionary]
- canlandırmak: evet — canlandırmak [çok anlamlı kelime, Wiktionary]

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 12.14 s | 5.98 s |
| Detaylı Çevir | 0.55 s | 17.23 s | 21.43 s | 39.21 s | 11.60 s |

## D8 · EN→TR (detayli-test-seti-v1)

**Kaynak metin**

```text
## Before you start

- Back up the NVS partition; you **cannot** recover it later.
- Don't cut corners on the power supply: a cheap adapter is often the root cause.

Once the board boots, keep an eye on the serial log for the first few minutes.
```

**Hızlı çeviri** — ilk metin 7.06 s, toplam 32.03 s (bitti)

```text
## Başlamadan önce

- NVS partition'ını yedekleyin; daha sonra geri **yükleyemezsiniz**.
- Güç kaynağı konusunda kestirme yollara başvurmayın: ucuz bir adaptör genellikle temel nedendir.

Kart açıldıktan sonra, ilk birkaç dakika boyunca serial log'u takip edin.
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 1): model parçaları ['yükleyemezsiniz'] uygulandı

**v2 hızlı çeviri (Adım 6)**

```text
## Başlamadan önce

- NVS partition'ı yedekleyin; daha sonra onu kurtarmanız **mümkün değildir**.
- Güç kaynağı konusunda kestirmeden gitmeyin: ucuz bir adaptör genellikle temel nedendir.

Kart boot olduktan sonra, ilk birkaç dakika boyunca seri kayıt'ı takip edin.
```

**v2 Detaylı Çevir — son çıktı (Adım 6)**

```text
## Başlamadan önce

- NVS partition'ı yedekleyin; daha sonra onu **kurtaramazsınız**.
- Güç kaynağı konusunda kestirme yollara başvurmayın: ucuz bir adaptör genellikle temel nedendir.

Kart boot olduktan sonra, ilk birkaç dakika boyunca seri kayıt ekranını gözlemleyin.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
## Başlamadan önce

- NVS partition'ı yedekleyin; daha sonra onu kurtaramazsınız.
- Güç kaynağı konusunda kestirme yollara başvurmayın: ucuz bir adaptör genellikle temel nedendir.

Kart boot olduktan sonra, ilk birkaç dakika boyunca serial log'u gözlemleyin.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
## Başlamadan önce

- NVS partition'ı yedekleyin; daha sonra onu **kurtaramazsınız**.
- Güç kaynağı konusunda kestirme yollara başvurmayın: ucuz bir adaptör genellikle temel nedendir.

Kart boot olduktan sonra, ilk birkaç dakika boyunca serial log'u gözlemleyin.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": [],
  "bold": [
    "kurtaramazsınız"
  ]
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Kalın yazı düzeltmesi (Detaylı)**

- model parçaları ['kurtaramazsınız'] uygulandı

**Denetimin taslakta değiştirdikleri**

```diff
-- NVS partition'ı yedekleyin; daha sonra onu kurtaramazsınız.
+- NVS partition'ı yedekleyin; daha sonra onu **kurtaramazsınız**.
```

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): The source has 1 bold passage(s) (**cannot**) but the draft has 0.
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (16)**

- [Wiktionary · kalıp/deyim] "keep an eye on" (verb): To watch and pay attention to, in case of misbehaviour or mishap. [idiomatic]
- [Wiktionary · kalıp/deyim] "on the cheap" (prep_phrase): Synonym of cheaply or economically.; Too cheaply or economically, inexpensive and affordable to the point of substandard quality. [informal]
- [Wiktionary · kalıp/deyim] "back up" (verb): To move backwards, especially for a vehicle to do so.; To move a vehicle backwards.; To undo one's actions. [idiomatic, informal] → Turkish: yedeklemek
- [Wiktionary · kalıp/deyim] "cut corners" (verb): To bypass a prescribed route so as to gain competitive advantage or to circumvent traffic signals or other rules of the road.; To do a less-than-thorough or in… [idiomatic]
- [Wiktionary · kalıp/deyim] "keep on" (verb): To persist or continue.; To persist in talking about a subject, perhaps to the annoyance of the listener.; To cause or allow to remain in an existing position. [idiomatic]
- [Wiktionary · çok anlamlı kelime] start: (noun) beginning of an activity → başlangıç; (noun) beginning point of a race → start; (verb) to begin → başlamak
- [Wiktionary · çok anlamlı kelime] root: (noun) arithmetic: number or expression which when raised to a power gives t… → kök; (noun) linguistic morphology: primary lexical unit of a word → kök; (noun) of a tooth → kök; (noun) part of a hair under the skin → kök
- [Wiktionary · çok anlamlı kelime] cause: (noun) source or reason of an event or action → neden, sebep; (verb) to set off an event or action → sebep olmak, uğratmak, yol açmak
- [Wiktionary · çok anlamlı kelime] board: (noun) long, wide and thin piece of wood or other material → tahta; (noun) managing committee → heyet, kurul; (noun) short for blackboard, whiteboard, etc. → tahta; (noun) side of a ship → borda, sancak
- [Wiktionary · çok anlamlı kelime] boot: (noun) heavy shoe that covers part of the leg → çizme; (verb) to start a system → başlatma
- [Wiktionary · çok anlamlı kelime] log: (noun) (computer) an append-only sequence of records written to disk → kütük; (noun) bulky piece of timber → tomruk; (noun) chronological record → kütük; (noun) trunk of dead tree, cleared of branches → kütük
- [Tatoeba · örnek cümle] English: I'll phone you before I start. | Turkish: Ayrılmadan önce seni ararım.
- [Tatoeba · örnek cümle] English: You start. | Turkish: Sen başla.
- [Tatoeba · örnek cümle] English: Could you keep an eye on my suitcase for a few minutes? | Turkish: Beş dakika için valizime göz kulak olabilir misin?
- [Tatoeba · örnek cümle] English: Can I call you back later? | Turkish: Seni sonra tekrar arayabilir miyim?
- [Tatoeba · örnek cümle] English: Can you call back later? | Turkish: Daha sonra tekrar arayabilir misin?

**Modele giden sözlük terimleri (5)**

- [kullanıcı sözlüğü] partition: keep in English
- [kullanıcı sözlüğü] NVS: keep in English
- [kullanıcı sözlüğü] log: keep in English
- [kullanıcı sözlüğü] power supply → güç kaynağı
- [kullanıcı sözlüğü] board → kart

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: cut corners, root cause, keep an eye on)

- cut corners: evet — cut corners [kalıp/deyim, Wiktionary]
- root cause: hayır
- keep an eye on: evet — keep an eye on [kalıp/deyim, Wiktionary]; Could you keep an eye on my suitcase for a few minutes? [örnek cümle, Tatoeba]

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 32.03 s | 7.06 s |
| Detaylı Çevir | 1.32 s | 38.26 s | 24.63 s | 64.21 s | 27.10 s |

## D9 · TR→EN (detayli-test-seti-v1)

**Kaynak metin**

```text
Bu işi yarına bırakma, sonra dokuz doğurursun. Ayağımıza kadar gelmiş fırsatı tepmek olmaz; nabzına göre şerbet ver ama ipin ucunu da kaçırma.
```

**Hızlı çeviri** — ilk metin 5.51 s, toplam 14.36 s (bitti)

```text
Don't put this off until tomorrow, or you'll end up with a mountain of work later. We shouldn't let an opportunity that's right at our doorstep slip away; play it by ear, but don't overdo it.
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 0): yok

**v2 hızlı çeviri (Adım 6)**

```text
Don't put off today's work for tomorrow, or you might end up with nine babies later on. You can't just kick away an opportunity that has reached your feet; give the right answer to the situation, but don't lose your grip either.
```

**v2 Detaylı Çevir — son çıktı (Adım 6)**

```text
Don't put off today's work until tomorrow, or you'll end up with a mountain of trouble later. You shouldn't turn down an opportunity that has come right to our doorstep; treat people according to their needs, but don't lose control of the situation.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Don't put off today's work until tomorrow, or you'll end up with a mountain of problems later. You shouldn't turn down an opportunity that has come right to our doorstep; treat people according to their temperament, but don't lose your grip on the situation.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Don't put off today's work until tomorrow, or you'll end up with a mountain of problems later. You shouldn't turn down an opportunity that has come right to our doorstep; treat people according to their temperament, but don't lose your grip on the situation.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": [],
  "bold": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Kalın yazı düzeltmesi (Detaylı)**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (9)**

- [Wiktionary · kalıp/deyim] "ipin ucunu kaçırmak" (verb): to lose control of a situation, to lose one's grip on things; to go too far [idiomatic]
- [Wiktionary · çok anlamlı kelime] ayak: (noun) foot; (noun) pillar, tower; (noun) stand, footrest; (noun) leg (support of a furniture)
- [Wiktionary · çok anlamlı kelime] iş: (noun) work, task, deed; (noun) energy expended on moving an object, force times distance; (noun) job, employment; (noun) matter, affair, business, activity
- [Wiktionary · çok anlamlı kelime] bırakmak: (verb) to let go, release, relinquish; (verb) to abandon, to leave; (verb) to leave, to cause or allow something to remain as available; (verb) to put, put down; to postpone, put off
- [Wiktionary · çok anlamlı kelime] doğurmak: (verb) to breed, to give birth; (verb) to give rise to
- [Wiktionary · çok anlamlı kelime] gelmek: (verb) to come, move closer; (verb) to come, to appear, to manifest; (verb) to weigh (have a certain weight); (verb) to seem, to appear
- [Wiktionary · çok anlamlı kelime] tepmek: (verb) to kick, especially for an animal; (verb) to tread on, trample (something); (verb) to decline, turn down, reject (something); to throw away (an opportun…; (verb) (for a gun) to kick, recoil.
- [Tatoeba · örnek cümle] Turkish: Bugünün işini yarına bırakma. | English: A stitch in time saves nine.
- [Tatoeba · örnek cümle] Turkish: Bugünkü işini yarına bırakma. | English: Never put off till tomorrow what you can do today.

**Modele giden sözlük terimleri (0)**

- yok

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: dokuz doğurmak, ayağına kadar gelmek, nabzına göre şerbet vermek, ipin ucunu kaçırmak)

- dokuz doğurmak: hayır
- ayağına kadar gelmek: hayır
- nabzına göre şerbet vermek: hayır
- ipin ucunu kaçırmak: evet — ipin ucunu kaçırmak [kalıp/deyim, Wiktionary]

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 14.36 s | 5.51 s |
| Detaylı Çevir | 0.91 s | 27.54 s | 21.87 s | 50.32 s | 17.91 s |

## D10 · EN→TR (detayli-test-seti-v1)

**Kaynak metin**

```text
Oh great, the build failed again. I'll look into it after lunch, but don't hold your breath — I've run out of ideas.
```

**Hızlı çeviri** — ilk metin 5.41 s, toplam 9.99 s (bitti)

```text
Harika, build yine başarısız oldu. Öğleden sonra bakacağım ama pek umutlanma; fikirlerim tükendi.
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 0): yok

**v2 hızlı çeviri (Adım 6)**

```text
Harika, build yine başarısız oldu. Öğleden sonra bakacağım ama çok da umutlanma; artık fikirlerim tükendi.
```

**v2 Detaylı Çevir — son çıktı (Adım 6)**

```text
Harika, build yine başarısız oldu. Öğle yemeğinden sonra bakacağım ama pek umut etme; fikirlerim tükendi.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Harika, build yine başarısız oldu. Öğle yemeğinden sonra konuyu inceleyeceğim ama pek umut etme; fikirlerim tükendi.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Harika, build yine başarısız oldu. Öğle yemeğinden sonra konuyu inceleyeceğim ama pek umut etme; fikirlerim tükendi.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": [],
  "bold": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Kalın yazı düzeltmesi (Detaylı)**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (11)**

- [Wiktionary · kalıp/deyim] "hold one's breath" (verb): To wait expectantly for something to happen soon. [idiomatic] → Turkish: nefesini tutmak; soluğunu tutmak; nefesini tutup beklemek
- [Wiktionary · kalıp/deyim] "look into" (verb): To investigate, explore, or consider. [idiomatic]
- [Wiktionary · kalıp/deyim] "run out" (verb): To use up or consume all; To expire; to come to an end.; To be completely used up or consumed. [idiomatic] → Turkish: bitmek; tükenmek
- [Wiktionary · kalıp/deyim] "out of" (prep): From the inside to the outside of.; So as no longer to be in a given condition or state.; From a thing or place as a source, place of origin etc. [informal]
- [Wiktionary · çok anlamlı kelime] great: (adj) very big, large scale → büyük, çok büyük; (noun) person of major significance, accomplishment or acclaim → ünlü
- [Wiktionary · çok anlamlı kelime] build: (noun) physique → çerçeve; (verb) (transitive) to form by combining materials or parts → inşa etmek, kurmak, yapmak
- [Wiktionary · çok anlamlı kelime] fail: (verb) cause to fail → sınıfta bırakmak; (verb) to receive one or more non-passing grades in academic pursuits → sınıfta kalmak
- [Tatoeba · örnek cümle] English: Tom failed again. | Turkish: Tom yine başarısız oldu.
- [Tatoeba · örnek cümle] English: The peace talks failed again. | Turkish: Barış görüşmeleri yine başarısız oldu.
- [Tatoeba · örnek cümle] English: Don't hold your breath. | Turkish: Nefesini tutma.
- [Tatoeba · örnek cümle] English: I'll talk to you about it after lunch. | Turkish: Öğle yemeğinden sonra seninle o konuda konuşacağım.

**Modele giden sözlük terimleri (0)**

- yok

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: oh great (alay), look into, don't hold your breath, run out of)

- oh great (alay): hayır
- look into: evet — look into [kalıp/deyim, Wiktionary]
- don't hold your breath: evet — Don't hold your breath. [örnek cümle, Tatoeba]
- run out of: hayır

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 9.99 s | 5.41 s |
| Detaylı Çevir | 0.70 s | 22.28 s | 21.02 s | 43.99 s | 17.06 s |

## V1 · TR→EN (dogrulama-seti-v1)

**Kaynak metin**

```text
Çocuğa bu kadar yüz verme, sonra başına çıkar.
```

**Hızlı çeviri** — ilk metin 4.56 s, toplam 7.96 s (bitti)

```text
Don't give the kid so much leeway, or he'll take advantage of you later.
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 0): yok

**v2 hızlı çeviri (Adım 6)**

```text
Don't let the child have their way with you so much; they'll cause trouble for you later.
```

**v2 Detaylı Çevir — son çıktı (Adım 6)**

```text
Don't give that kid so much leeway, or it'll come back to haunt you.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Don't give the kid so much leeway, or he'll take advantage of it later.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Don't give the kid so much leeway, or he'll take advantage of it later.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": [],
  "bold": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Kalın yazı düzeltmesi (Detaylı)**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (5)**

- [Wiktionary · çok anlamlı kelime] baş: (adj) first, primal, principal; (noun) head; (noun) leader of a group, chief; (noun) outset of something
- [Wiktionary · çok anlamlı kelime] çocuk: (noun) child; (noun) a male around dating age
- [Wiktionary · çok anlamlı kelime] vermek: (verb) to give; (verb) to consent for sex, to put out; (verb) to give out, to donate; (verb) to attribute
- [Wiktionary · çok anlamlı kelime] çıkmak: (verb) to leave, exit, quit, get out; (verb) to get out; (verb) to happen, occur; (verb) to climb
- [Tatoeba · örnek cümle] Turkish: Bu öğleden sonra yüzmemeye karar verdim. | English: I've decided not to swim this afternoon.

**Modele giden sözlük terimleri (0)**

- yok

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: yüz vermek, başına çıkmak)

- yüz vermek: hayır
- başına çıkmak: hayır

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 7.96 s | 4.56 s |
| Detaylı Çevir | 0.37 s | 14.00 s | 19.75 s | 34.13 s | 10.87 s |

## V2 · EN→TR (dogrulama-seti-v1)

**Kaynak metin**

```text
Flash the board only after the bootloader prints its banner; otherwise the upload will **not** take effect.
```

**Hızlı çeviri** — ilk metin 5.11 s, toplam 10.40 s (bitti)

```text
Kartı sadece bootloader banner'ını yazdırdıktan sonra flashlayın; aksi takdirde yükleme geçerli **olmayacaktır**.
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 0): yok

**v2 hızlı çeviri (Adım 6)**

```text
Board'u sadece bootloader kendi banner'ını yazdırdıktan sonra flashlayın; aksi takdirde yükleme geçerli **olmayacaktır**.
```

**v2 Detaylı Çevir — son çıktı (Adım 6)**

```text
Kartı sadece bootloader bandı yazdırdıktan sonra flashlayın; aksi takdirde yükleme **geçerli olmayacaktır**.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Kartı sadece bootloader kendi banner'ını yazdırdıktan sonra flashlayın; aksi takdirde yükleme **geçerli olmayacaktır**.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Kartı sadece bootloader kendi banner'ını yazdırdıktan sonra flashlayın; aksi takdirde yükleme **geçerli olmayacaktır**.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": [],
  "bold": [
    "geçerli olmayacaktır"
  ]
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Kalın yazı düzeltmesi (Detaylı)**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (3)**

- [Wiktionary · çok anlamlı kelime] board: (noun) long, wide and thin piece of wood or other material → tahta; (noun) managing committee → heyet, kurul; (noun) short for blackboard, whiteboard, etc. → tahta; (noun) side of a ship → borda, sancak
- [Wiktionary · çok anlamlı kelime] it: (noun) information technology → BT, İT; (noun) The person who chases others in the game of tag → ebe
- [Wiktionary · çok anlamlı kelime] effect: (noun) sound engineering: alteration in sound → efekt; (noun) result of an action → efekt, etki, tesir; (noun) special effect in film → efekt; (noun) state of being binding and enforceable → yürürlük

**Modele giden sözlük terimleri (2)**

- [kullanıcı sözlüğü] bootloader: keep in English
- [kullanıcı sözlüğü] board → kart

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: board, kalın yazı)

- board: evet — board → kart [sözlük terimi, kullanıcı sözlüğü]; board [çok anlamlı kelime, Wiktionary]
- kalın yazı: hayır

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 10.40 s | 5.11 s |
| Detaylı Çevir | 0.49 s | 16.25 s | 21.32 s | 38.06 s | 11.13 s |

## V3 · TR→EN (dogrulama-seti-v1)

**Kaynak metin**

```text
Bankada sıra çok uzundu, ben de dışarıdaki banka oturup bekledim. Dönüşte yağmur değil kar yağıyordu.
```

**Hızlı çeviri** — ilk metin 5.35 s, toplam 11.00 s (bitti)

```text
The line at the bank was very long, so I sat on an outside bench and waited. When I came back, it wasn't raining; it was snowing.
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 0): yok

**v2 hızlı çeviri (Adım 6)**

```text
The queue at the bank was very long, so I sat on a bench outside and waited. When I returned, it wasn't raining; it was snowing.
```

**v2 Detaylı Çevir — son çıktı (Adım 6)**

```text
The line at the bank was very long, so I sat on a bench outside and waited. On the way back, it wasn't raining; it was snowing.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
The line at the bank was very long, so I sat on a bench outside and waited. When I returned, it wasn't raining; it was snowing.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
The line at the bank was very long, so I sat on a bench outside and waited. When I returned, it wasn't raining; it was snowing.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": [],
  "bold": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Kalın yazı düzeltmesi (Detaylı)**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (11)**

- [Wiktionary · kalıp/deyim] "kar yağıyor" (phrase): it's snowing
- [Wiktionary · kalıp/deyim] "yağmur yağıyor" (phrase): it's raining
- [Wiktionary · çok anlamlı kelime] dışarı: (adv) outside; (noun) outside; (adv) outdoors; (noun) countryside (as opposed to major cities)
- [Wiktionary · çok anlamlı kelime] sıra: (noun) row; (noun) order, sequence; (noun) turn; (noun) desk
- [Wiktionary · çok anlamlı kelime] uzun: (adj) tall; (adj) long
- [Wiktionary · çok anlamlı kelime] oturmak: (verb) to sit; (verb) to sit down (on), sit (upon); (verb) to reside, dwell in; (verb) to fit on
- [Wiktionary · çok anlamlı kelime] beklemek: (verb) To wait for, to await.; (verb) To expect, to anticipate; (verb) To watch over something or someone; to guard, to keep an eye on.; (verb) To tarry, to hang about.
- [Tatoeba · örnek cümle] Turkish: Yağmur kara dönüştü. | English: The rain changed into snow.
- [Tatoeba · örnek cümle] Turkish: Yağmur yağıyordu. | English: It was raining.
- [Tatoeba · örnek cümle] Turkish: Bir banka oturup bekledim. | English: I sat on a bench and waited.
- [Tatoeba · örnek cümle] Turkish: Tom otuz dakika dışarıda bekledi. | English: Tom waited outside for thirty minutes.

**Modele giden sözlük terimleri (0)**

- yok

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: banka (bank / oturak), kar)

- banka (bank / oturak): evet — Bir banka oturup bekledim. [örnek cümle, Tatoeba]
- kar: evet — kar yağıyor [kalıp/deyim, Wiktionary]

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 11.00 s | 5.35 s |
| Detaylı Çevir | 0.67 s | 20.44 s | 21.23 s | 42.34 s | 15.32 s |

## V4 · EN→TR (dogrulama-seti-v1)

**Kaynak metin**

```text
Dear Mr. Aksoy, please find attached the revised invoice. Should you have any questions, do not hesitate to contact us.
```

**Hızlı çeviri** — ilk metin 5.23 s, toplam 11.73 s (bitti)

```text
Sayın Bay Aksoy, revize edilmiş faturayı ekte bulabilirsiniz. Herhangi bir sorunuz olması durumunda bizimle iletişime geçmekten çekinmeyiniz.
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 0): yok

**v2 hızlı çeviri (Adım 6)**

```text
Sayın Bay Aksoy, revize edilmiş faturayı ekte bulabilirsiniz. Herhangi bir sorunuz olması durumunda bizimle iletişime geçmekten çekinmeyiniz.
```

**v2 Detaylı Çevir — son çıktı (Adım 6)**

```text
Sayın Aksoy, revize edilmiş faturayı ekte bulabilirsiniz. Herhangi bir sorunuz olması durumunda bizimle iletişime geçmekten çekinmeyin.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Sayın Bay Aksoy, revize edilmiş faturayı ekte bulabilirsiniz. Herhangi bir sorunuz olması durumunda bizimle iletişime geçmekten çekinmeyin.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Sayın Bay Aksoy, revize edilmiş faturayı ekte bulabilirsiniz. Herhangi bir sorunuz olması durumunda bizimle iletişime geçmekten çekinmeyin.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": [],
  "bold": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Kalın yazı düzeltmesi (Detaylı)**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (7)**

- [Wiktionary · kalıp/deyim] "please find attached" (phrase): The following item or items are attached to this message. [formal]
- [Wiktionary · çok anlamlı kelime] dear: (adj) an informal way of addressing the recipient in a letter's opening line → sevgili; (adj) formal way of addressing → sayın; (adj) loved; lovable → sevgili, sevimli
- [Wiktionary · çok anlamlı kelime] question: (noun) sentence, phrase or word → sival, soru; (verb) ask questions of → sorgulamak; (verb) raise doubts about — see also doubt → sorgulamak
- [Tatoeba · örnek cümle] English: If you have any questions, please don't hesitate to contact me. | Turkish: Herhangi bir sorunuz varsa, lütfen benimle iletişime geçmekten çekinmeyin.
- [Tatoeba · örnek cümle] English: Please don't hesitate to contact me if you have any other questions. | Turkish: Başka sorunlarınız olursa benimle temas etmekten çekinmeyin.
- [Tatoeba · örnek cümle] English: Please check the attached file. | Turkish: Lütfen ekteki dosyayı kontrol edin.
- [Tatoeba · örnek cümle] English: Please fill out the attached application form. | Turkish: Lütfen ekteki başvuru formunu doldurun.

**Modele giden sözlük terimleri (0)**

- yok

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: Mr., do not hesitate)

- Mr.: hayır
- do not hesitate: hayır

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 11.73 s | 5.23 s |
| Detaylı Çevir | 0.75 s | 20.44 s | 21.22 s | 42.40 s | 14.38 s |

## V5 · TR→EN (dogrulama-seti-v1)

**Kaynak metin**

```text
Log'ları temizledim ama SD karttaki kayıtlar hâlâ duruyor; kartı formatlamadan önce yedek alacağım.
```

**Hızlı çeviri** — ilk metin 6.52 s, toplam 10.78 s (bitti)

```text
I cleared the logs, but the records on the SD card are still there; I will take a backup before formatting the card.
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 0): yok

**v2 hızlı çeviri (Adım 6)**

```text
I cleared the logs, but the records on the SD card are still there; I will take a backup before formatting the board.
```

**v2 Detaylı Çevir — son çıktı (Adım 6)**

```text
I cleared the logs, but the records on the SD card are still there; I will take a backup before formatting the card.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
I cleared the logs, but the records on the SD card are still there; I will take a backup before formatting the card.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
I cleared the logs, but the records on the SD card are still there; I will take a backup before formatting the card.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": true,
  "errors": [
    {
      "type": "meaning",
      "draft_text": "records",
      "corrected_text": "logs",
      "reason": "The source text uses 'kayıtlar' to refer back to 'Log'ları', and the term list specifies that 'kayıtlar' should be translated as 'logs'."
    }
  ],
  "bold": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- (meaning) “records” → “logs” — neden: taslakta olmayan ve kaynakta karşılığı bulunmayan kelime eklendi: logs

**Uygulanamayan düzeltmeler**

- yok

**Kalın yazı düzeltmesi (Detaylı)**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (2)**

- [Wiktionary · çok anlamlı kelime] durmak: (verb) to stop; (verb) to stand; to sit still; to remain; (verb) to be (at a certain place); (verb) to last; to continue to be, to keep being
- [Wiktionary · çok anlamlı kelime] almak: (verb) to take; (verb) to buy; (verb) to get, to obtain, to receive; (verb) to receive (a radio signal)

**Modele giden sözlük terimleri (4)**

- [kullanıcı sözlüğü] log: keep in English
- [kullanıcı sözlüğü] SD kart → SD card
- [kullanıcı sözlüğü] kayıtlar → logs
- [kullanıcı sözlüğü] kayıt → log

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: kart (burada SD kart), kayıtlar)

- kart (burada SD kart): evet — SD kart → SD card [sözlük terimi, kullanıcı sözlüğü]
- kayıtlar: evet — kayıtlar → logs [sözlük terimi, kullanıcı sözlüğü]

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 10.78 s | 6.52 s |
| Detaylı Çevir | 0.46 s | 14.19 s | 31.63 s | 46.28 s | 10.28 s |

## G1 · TR→EN (kontrol-seti-v2)

**Kaynak metin**

```text
Ocak ayında ocağın başında oturup kestane közledik.
Bağ evinin bahçesinde ayakkabımın bağı çözüldü.
Kapı çalındığında komşunun oğlu gitar çalıyordu.
```

**Hızlı çeviri** — ilk metin 5.80 s, toplam 14.00 s (bitti)

```text
We sat down at the beginning of January and roasted chestnuts over an open fire.
The lace of my shoe came undone in the garden of the country house.
When the door rang, the neighbor's son was playing the guitar.
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 0): yok

**v2 hızlı çeviri (Adım 6)**

```text
We sat down at the beginning of January and roasted chestnuts over an open fire.
My shoelace came undone in the garden of the country house.
The neighbor's son was playing guitar when someone knocked on the door.
```

**v2 Detaylı Çevir — son çıktı (Adım 6)**

```text
We sat by the stove in January and roasted chestnuts.
My shoelace came undone in the garden of the vineyard house.
The neighbor's son was playing the guitar when there was a knock at the door.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
We sat by the stove in January and roasted chestnuts.
My shoelace came undone in the garden of the vineyard house.
The neighbor's son was playing the guitar when there was a knock at the door.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
We sat by the fireplace in January and roasted chestnuts.
My shoelace came undone in the garden of the vineyard house.
The neighbor's son was playing the guitar when there was a knock at the door.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": true,
  "errors": [
    {
      "type": "meaning",
      "draft_text": "by the stove",
      "corrected_text": "by the fireplace",
      "reason": "In this context, 'ocağın başında' refers to sitting by a fireplace/hearth for roasting chestnuts in January, rather than a kitchen stove."
    }
  ],
  "bold": []
}
```

**Kodun uyguladığı düzeltmeler**

- (meaning) “by the stove” → “by the fireplace”

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Kalın yazı düzeltmesi (Detaylı)**

- yok

**Denetimin taslakta değiştirdikleri**

```diff
-We sat by the stove in January and roasted chestnuts.
+We sat by the fireplace in January and roasted chestnuts.
```

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (10)**

- [Wiktionary · çok anlamlı kelime] baş: (adj) first, primal, principal; (noun) head; (noun) leader of a group, chief; (noun) outset of something
- [Wiktionary · çok anlamlı kelime] bağ: (noun) connection; (noun) lace; (noun) nexus; (noun) relationship
- [Wiktionary · çok anlamlı kelime] ocak: (noun) stove, oven, fireplace; (noun) chimney; (noun) quarry; (noun) January
- [Wiktionary · çok anlamlı kelime] ayı: (noun) bear; (noun) a rude primitive person
- [Wiktionary · çok anlamlı kelime] oturmak: (verb) to sit; (verb) to sit down (on), sit (upon); (verb) to reside, dwell in; (verb) to fit on
- [Wiktionary · çok anlamlı kelime] kestane: (noun) chestnut, the edible nut-like fruit of the tree Castanea sativa; (noun) chestnut, a dark reddish-brown color, like that of chestnuts
- [Tatoeba · örnek cümle] Turkish: Kapı çalıyordu. | English: There was a knock at the door.
- [Tatoeba · örnek cümle] Turkish: Benim ayakkabı bağlarım çözüldü. | English: My shoelaces came undone.
- [Tatoeba · örnek cümle] Turkish: Ön kapı çalıyordu. | English: There was a knock at the front door.
- [Tatoeba · örnek cümle] Turkish: Evin içinde ayakkabı giyer misiniz? | English: Do you wear shoes inside your house?

**Modele giden sözlük terimleri (0)**

- yok

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: ocak (ay / soba), bağ (üzüm bağı / ayakkabı bağı), çalmak (kapı çalmak / müzik aleti çalmak).)

- ocak (ay / soba): evet — ocak [çok anlamlı kelime, Wiktionary]
- bağ (üzüm bağı / ayakkabı bağı): evet — bağ [çok anlamlı kelime, Wiktionary]
- çalmak (kapı çalmak / müzik aleti çalmak).: hayır

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 14.00 s | 5.80 s |
| Detaylı Çevir | 0.94 s | 22.18 s | 32.95 s | 56.07 s | 15.22 s |

## G2 · EN→TR (kontrol-seti-v2)

**Kaynak metin**

```text
The results were not half bad for a first attempt.
I can't help but notice that the fan never stops spinning.
The flash write does **not** start until the erase cycle has completed.
```

**Hızlı çeviri** — ilk metin 5.83 s, toplam 14.08 s (bitti)

```text
İlk deneme için sonuçlar hiç de kötü değildi.
Fanın hiç durmadan dönmediğini fark etmemek elde değil.
Flash yazma işlemi, silme döngüsü tamamlanana kadar **başlamaz**.
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 0): yok

**v2 hızlı çeviri (Adım 6)**

```text
İlk deneme için sonuçlar hiç de kötü değildi.
Fanın hiç durmadan dönmediğini fark etmemek elde değil.
Flash yazma işlemi, silme döngüsü tamamlanana kadar **başlamaz**.
```

**v2 Detaylı Çevir — son çıktı (Adım 6)**

```text
İlk deneme için sonuçlar hiç de fena değildi.
Vantilatörün hiç durmadan döndüğünü fark etmemek elde değil.
Flash yazma işlemi, silme döngüsü tamamlanana kadar **başlamaz**.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
İlk deneme için sonuçlar hiç de fena değildi.
Vantilatörün hiç durmadan dönmediğini fark etmemek elde değil.
Flash yazma işlemi, silme döngüsü tamamlanana kadar **başlamaz**.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
İlk deneme için sonuçlar hiç de fena değildi.
Vantilatörün hiç durmadan döndüğünü fark etmemek elde değil.
Flash yazma işlemi, silme döngüsü tamamlanana kadar **başlamaz**.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": true,
  "errors": [
    {
      "type": "meaning",
      "draft_text": "Vantilatörün hiç durmadan dönmediğini fark etmemek elde değil.",
      "corrected_text": "Vantilatörün hiç durmadan döndüğünü fark etmemek elde değil.",
      "reason": "The draft translates 'never stops spinning' as 'doesn't spin without stopping', which reverses the meaning. It should be 'always spins/never stops'."
    }
  ],
  "bold": [
    "başlamaz"
  ]
}
```

**Kodun uyguladığı düzeltmeler**

- (meaning) “Vantilatörün hiç durmadan dönmediğini fark etmemek elde değil.” → “Vantilatörün hiç durmadan döndüğünü fark etmemek elde değil.”

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Kalın yazı düzeltmesi (Detaylı)**

- yok

**Denetimin taslakta değiştirdikleri**

```diff
-Vantilatörün hiç durmadan dönmediğini fark etmemek elde değil.
+Vantilatörün hiç durmadan döndüğünü fark etmemek elde değil.
```

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (12)**

- [Wiktionary · kalıp/deyim] "not half bad" (adj): Pretty good, imperfect but more than OK. [idiomatic]
- [Wiktionary · çok anlamlı kelime] result: (noun) that which results → netice, sonuç; (verb) to proceed, spring, or rise, as a consequence → sonuçlanmak
- [Wiktionary · çok anlamlı kelime] attempt: (noun) attack → suikast; (noun) the action of trying at something → deneme, girişim, teşebbüs; (verb) to make a substantial but unsuccessful effort (to commit a crime) → girişmek, yeltenmek; (verb) to try → denemek, girişmek, kalkışmak
- [Wiktionary · çok anlamlı kelime] fan: (noun) admirer → hayran, taraftar; (noun) electrical device → vantilatör; (noun) hand-held device → yelpaze; (verb) to blow air on by means of a hand-held fan → yelpazelemek
- [Wiktionary · çok anlamlı kelime] stop: (noun) interruption of travel → mola; (noun) place to get on and off mass transport → durak; (verb) not to continue — see also cease, desist → durmak, kesmek; (verb) to cause to cease moving — see also detain → durdurmak
- [Wiktionary · çok anlamlı kelime] spin: (verb) to make yarn → eğirmek; (verb) to present a bias → yaldızlamak; (verb) to turn around quickly → dolanmak, dönmek
- [Wiktionary · çok anlamlı kelime] start: (noun) beginning of an activity → başlangıç; (noun) beginning point of a race → start; (verb) to begin → başlamak
- [Tatoeba · örnek cümle] English: The results were bad. | Turkish: Sonuçlar kötüydü.
- [Tatoeba · örnek cümle] English: The results were very bad. | Turkish: Sonuçlar çok kötüydü.
- [Tatoeba · örnek cümle] English: I can't believe I never noticed that before. | Turkish: Bunu daha önce fark etmediğime inanamıyorum.
- [Tatoeba · örnek cümle] English: I couldn't help but notice that you're in pain. | Turkish: Acı içinde olduğunu fark etmekten kendimi alamadım.
- [Tatoeba · örnek cümle] English: Please stay seated until the plane comes to a complete stop. | Turkish: Uçak tamamen durana kadar yerinizden kalkmayın.

**Modele giden sözlük terimleri (0)**

- yok

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: "not half bad" = gayet iyi; "can't help but" = elimde olmadan / fark etmeden edemiyorum; kalın yazı korunmalı.)

- "not half bad" = gayet iyi: evet — not half bad [kalıp/deyim, Wiktionary]
- "can't help but" = elimde olmadan / fark etmeden edemiyorum: hayır
- kalın yazı korunmalı.: hayır

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 14.08 s | 5.83 s |
| Detaylı Çevir | 1.14 s | 29.22 s | 39.58 s | 69.94 s | 20.92 s |

## G3 · TR→EN (kontrol-seti-v2)

**Kaynak metin**

```text
Kartın brownout reset'i sık sık tetikleniyor; kondansatörü değiştirdikten sonra bile log'larda aynı hata var. Kartı kredi kartı boyutunda bir kutuya koyacağım.
```

**Hızlı çeviri** — ilk metin 6.46 s, toplam 13.35 s (bitti)

```text
The board's brownout reset is being triggered frequently; the same error persists in the logs even after replacing the capacitor. I'm going to put the board in a credit card-sized box.
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 0): yok

**v2 hızlı çeviri (Adım 6)**

```text
The board's brownout reset is triggered frequently; even after replacing the capacitor, the same error appears in the logs. I will put the board into a box the size of a credit card.
```

**v2 Detaylı Çevir — son çıktı (Adım 6)**

```text
The board's brownout reset is triggered often; the same error is in the logs even after replacing the capacitor. I will put the board in a box the size of a credit card.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
The board's brownout reset is triggered often; the same error is in the logs even after replacing the capacitor. I will put the board in a credit card-sized box.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
The board's brownout reset is triggered often; the same error is in the logs even after replacing the capacitor. I will put the board in a credit card-sized box.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": [],
  "bold": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Kalın yazı düzeltmesi (Detaylı)**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (4)**

- [Wiktionary · kalıp/deyim] "sık sık" (adv): often
- [Wiktionary · çok anlamlı kelime] koymak: (verb) to put; (verb) to put, to add; (verb) to prepare or serve a food or a drink; (verb) to appoint, to assign
- [Tatoeba · örnek cümle] Turkish: Bunu kutuya koyacağım. | English: I'll put it in the box.
- [Tatoeba · örnek cümle] Turkish: Bu boyutta bir kutuya ihtiyacım var. | English: I need a box of this size.

**Modele giden sözlük terimleri (3)**

- [kullanıcı sözlüğü] brownout: keep in English
- [kullanıcı sözlüğü] log: keep in English
- [kullanıcı sözlüğü] kart → board

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: ilk "kart" = board, "kredi kartı" = credit card (aynı metinde ikisi de var).)

- ilk "kart" = board: evet — kart → board [sözlük terimi, kullanıcı sözlüğü]
- "kredi kartı" = credit card (aynı metinde ikisi de var).: hayır

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 13.35 s | 6.46 s |
| Detaylı Çevir | 0.75 s | 17.03 s | 21.44 s | 39.22 s | 11.45 s |

## W1 · TR→EN (dogrulama-seti-v2)

**Kaynak metin**

```text
Kartı USB'den **çıkarmayın**; firmware yazılırken bağlantı kesilirse kart açılmayabilir.
```

**Hızlı çeviri** — ilk metin 5.52 s, toplam 10.65 s (bitti)

```text
Do **not** unplug the board from the USB; if the connection is lost while the firmware is being written, the board may not boot.
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 0): kod (olumsuzluk sırası): Do **not** unplug the board from the USB; if the connection is lost while the firmware is being written, the board may not boot.

**Detaylı Çevir — denetimden önceki taslak**

```text
Do not remove the board from the USB; if the connection is lost while the firmware is being written, the board may not boot.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Do **not** remove the board from the USB; if the connection is lost while the firmware is being written, the board may not boot.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": [],
  "bold": [
    "not"
  ]
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Kalın yazı düzeltmesi (Detaylı)**

- kod (olumsuzluk sırası), denetimden önce: Do **not** remove the board from the USB; if the connection is lost while the firmware is being written, the board may not boot.

**Denetimin taslakta değiştirdikleri**

```diff
-Do not remove the board from the USB; if the connection is lost while the firmware is being written, the board may not boot.
+Do **not** remove the board from the USB; if the connection is lost while the firmware is being written, the board may not boot.
```

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (1)**

- [Wiktionary · çok anlamlı kelime] çıkarmak: (verb) to remove; (verb) to subtract; (verb) to make leave; (verb) to take off (clothes)

**Modele giden sözlük terimleri (2)**

- [kullanıcı sözlüğü] firmware: keep in English
- [kullanıcı sözlüğü] kart → board

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: kalın yazı "not" üzerinde olmalı, kart)

- kalın yazı "not" üzerinde olmalı: hayır
- kart: evet — kart → board [sözlük terimi, kullanıcı sözlüğü]

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 10.65 s | 5.52 s |
| Detaylı Çevir | 0.39 s | 12.46 s | 25.08 s | 37.93 s | 8.15 s |

## W2 · EN→TR (dogrulama-seti-v2)

**Kaynak metin**

```text
Check the boot log before you reflash; the device will **not** accept a new image while the partition table is locked.
```

**Hızlı çeviri** — ilk metin 5.43 s, toplam 11.24 s (bitti)

```text
Yeniden yükleme yapmadan önce boot log'unu kontrol edin; partition tablosu kilitliyken cihaz yeni bir imajı kabul **etmeyecektir**.
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 0): kod (olumsuzluk sırası): Yeniden yükleme yapmadan önce boot log'unu kontrol edin; partition tablosu kilitliyken cihaz yeni bir imajı kabul **etmeyecektir**.

**Detaylı Çevir — denetimden önceki taslak**

```text
Yeniden yüklemeden önce boot log'unu kontrol edin; partition tablosu kilitliyken cihaz yeni bir görüntü kabul etmeyecektir.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Yeniden yüklemeden önce boot log'unu kontrol edin; partition tablosu kilitliyken cihaz yeni bir görüntü **kabul etmeyecektir**.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": [],
  "bold": [
    "kabul etmeyecektir"
  ]
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Kalın yazı düzeltmesi (Detaylı)**

- model parçaları ['kabul etmeyecektir'] uygulandı

**Denetimin taslakta değiştirdikleri**

```diff
-Yeniden yüklemeden önce boot log'unu kontrol edin; partition tablosu kilitliyken cihaz yeni bir görüntü kabul etmeyecektir.
+Yeniden yüklemeden önce boot log'unu kontrol edin; partition tablosu kilitliyken cihaz yeni bir görüntü **kabul etmeyecektir**.
```

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): The source has 1 bold passage(s) (**not**) but the draft has 0.
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (5)**

- [Wiktionary · çok anlamlı kelime] boot: (noun) heavy shoe that covers part of the leg → çizme; (verb) to start a system → başlatma
- [Wiktionary · çok anlamlı kelime] log: (noun) (computer) an append-only sequence of records written to disk → kütük; (noun) bulky piece of timber → tomruk; (noun) chronological record → kütük; (noun) trunk of dead tree, cleared of branches → kütük
- [Wiktionary · çok anlamlı kelime] image: (noun) computing: file → görüntü; (verb) computing: to create a backup copy → görüntülemek; (noun) characteristic as perceived by others → imaj; (noun) graphical representation → resim
- [Wiktionary · çok anlamlı kelime] lock: (noun) a mutex or other token → kilit; (noun) length of hair → sümbül, zülüf; (noun) something used for fastening → kilit; (verb) to fasten with a lock → kilitlemek
- [Wiktionary · çok anlamlı kelime] accept: (verb) to agree to → kabul etmek; (verb) to receive with consent → kabul etmek

**Modele giden sözlük terimleri (2)**

- [kullanıcı sözlüğü] partition: keep in English
- [kullanıcı sözlüğü] log: keep in English

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: log İngilizce kalmalı, kalın yazı olumsuz fiilde)

- log İngilizce kalmalı: hayır
- kalın yazı olumsuz fiilde: hayır

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 11.24 s | 5.43 s |
| Detaylı Çevir | 0.49 s | 18.09 s | 22.42 s | 40.99 s | 13.09 s |

## W3 · TR→EN (dogrulama-seti-v2)

**Kaynak metin**

```text
SD kartı takınca kart tanınmadı; kayıtlarda okuma hatası görünüyor, kartı başka bir okuyucuda deneyeceğim.
```

**Hızlı çeviri** — ilk metin 6.04 s, toplam 11.37 s (bitti)

```text
The card wasn't recognized when I plugged in the SD card; a read error appears in the logs, so I will try the card in another reader.
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 0): yok

**Detaylı Çevir — denetimden önceki taslak**

```text
When I plugged in the SD card, it wasn't recognized; a read error appears in the logs, so I will try the card in another reader.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
When I plugged in the SD card, it wasn't recognized; a read error appears in the logs, so I will try the card in another reader.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": [],
  "bold": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Kalın yazı düzeltmesi (Detaylı)**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (2)**

- [Wiktionary · çok anlamlı kelime] takmak: (verb) to wear, put on; (verb) to attach, fasten, affix, put something on; to pin something to; to h…; (verb) to give (a name) to; (verb) to pick on, single someone out for harassment
- [Wiktionary · çok anlamlı kelime] okumak: (verb) to read; (verb) to study, peruse; (verb) to sing; to chant, recite; (verb) to announce

**Modele giden sözlük terimleri (3)**

- [kullanıcı sözlüğü] SD kart → SD card
- [kullanıcı sözlüğü] kayıtlar → logs
- [kullanıcı sözlüğü] kayıt → log

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: kart (burada SD kart), kayıtlar)

- kart (burada SD kart): evet — SD kart → SD card [sözlük terimi, kullanıcı sözlüğü]
- kayıtlar: evet — kayıtlar → logs [sözlük terimi, kullanıcı sözlüğü]

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 11.37 s | 6.04 s |
| Detaylı Çevir | 0.46 s | 15.36 s | 20.68 s | 36.50 s | 10.20 s |

## W4 · EN→TR (dogrulama-seti-v2)

**Kaynak metin**

```text
Dear Dr. Yıldız, thank you for your prompt reply. We will not proceed until we receive your written approval.
```

**Hızlı çeviri** — ilk metin 5.02 s, toplam 9.61 s (bitti)

```text
Sayın Dr. Yıldız, hızlı yanıtınız için teşekkür ederiz. Yazılı onayınızı alana kadar ilerlemeyeceğiz.
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 0): yok

**Detaylı Çevir — denetimden önceki taslak**

```text
Sayın Dr. Yıldız, hızlı cevabınız için teşekkür ederim. Yazılı onayınızı alana kadar ilerlemeyeceğiz.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Sayın Dr. Yıldız, hızlı cevabınız için teşekkür ederim. Yazılı onayınızı alana kadar ilerlemeyeceğiz.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": [],
  "bold": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Kalın yazı düzeltmesi (Detaylı)**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (7)**

- [Wiktionary · kalıp/deyim] "thank u" (intj): thank you
- [Wiktionary · kalıp/deyim] "thank you" (intj): An expression of gratitude or politeness in response to something done or given.; Used as a polite affirmative to accept an offer.; A polite dismissal; usually… → Turkish: sağ olun; sağ ol; teşekkür ederim; teşekkürler; mersi
- [Wiktionary · çok anlamlı kelime] dear: (adj) an informal way of addressing the recipient in a letter's opening line → sevgili; (adj) formal way of addressing → sayın; (adj) loved; lovable → sevgili, sevimli
- [Wiktionary · çok anlamlı kelime] proceed: (verb) go ahead → gitmek, ilerlemek; (verb) go on in an orderly or regulated manner → devam etmek, ilerlemek; (verb) pass from one point to another → ilerlemek
- [Tatoeba · örnek cümle] English: Thank you for your prompt reply. | Turkish: Çabuk cevabın için teşekkür ederim.
- [Tatoeba · örnek cümle] English: Your approval is not required. | Turkish: Benim onayım gerekli değil.
- [Tatoeba · örnek cümle] English: You will not receive the gifts. | Turkish: Sen hediye almayacaksın.

**Modele giden sözlük terimleri (0)**

- yok

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: Dr., olumsuzluk)

- Dr.: hayır
- olumsuzluk: hayır

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 9.61 s | 5.02 s |
| Detaylı Çevir | 0.67 s | 17.86 s | 20.72 s | 39.25 s | 13.69 s |

## W5 · TR→EN (dogrulama-seti-v2)

**Kaynak metin**

```text
Ders bitti, herkes bahçeye çıktı; ben de ayın son günü olduğu için kirayı yatırdım.
```

**Hızlı çeviri** — ilk metin 4.71 s, toplam 9.66 s (bitti)

```text
Class is over, everyone went out to the garden; and since it's the last day of the month, I paid the rent too.
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 0): yok

**Detaylı Çevir — denetimden önceki taslak**

```text
The lecture is over and everyone went out to the garden; I also paid the rent since it's the last day of the month.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
The lecture is over and everyone went out to the garden; I also paid the rent since it's the last day of the month.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": [],
  "bold": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Kalın yazı düzeltmesi (Detaylı)**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (4)**

- [Wiktionary · çok anlamlı kelime] ders: (noun) lecture; (noun) lesson (a section of learning or teaching)
- [Wiktionary · çok anlamlı kelime] bitmek: (verb) to end, to finish; (verb) to grow, to sprout; (verb) to cease; (verb) to run out of (of something)
- [Wiktionary · çok anlamlı kelime] çıkmak: (verb) to leave, exit, quit, get out; (verb) to get out; (verb) to happen, occur; (verb) to climb
- [Wiktionary · çok anlamlı kelime] yatırmak: (verb) to lay down; (verb) to put to sleep; (verb) to invest

**Modele giden sözlük terimleri (0)**

- yok

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: bitti, ayın)

- bitti: hayır
- ayın: hayır

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 9.66 s | 4.71 s |
| Detaylı Çevir | 0.46 s | 14.30 s | 20.25 s | 35.01 s | 10.03 s |

## W6 · TR→EN (dogrulama-seti-v2)

**Kaynak metin**

```text
Bu kadar işle tek başıma başa çıkamam, birinin elini taşın altına koyması lazım.
```

**Hızlı çeviri** — ilk metin 5.23 s, toplam 8.30 s (bitti)

```text
I can't handle all this work alone; someone needs to step up and take responsibility.
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 0): yok

**Detaylı Çevir — denetimden önceki taslak**

```text
I can't handle all these tasks alone; someone needs to step up and take responsibility.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
I can't handle all these tasks alone; someone needs to step up and take responsibility.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": [],
  "bold": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Kalın yazı düzeltmesi (Detaylı)**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (8)**

- [Wiktionary · kalıp/deyim] "tek başına" (adv): alone, by oneself
- [Wiktionary · çok anlamlı kelime] baş: (adj) first, primal, principal; (noun) head; (noun) leader of a group, chief; (noun) outset of something
- [Wiktionary · çok anlamlı kelime] el: (noun) hand; (noun) possession; (noun) round (stage of a sports competition); (noun) round (individual ammunition shell)
- [Wiktionary · çok anlamlı kelime] bir: (adj) one; (adv) only, solely, merely; (noun) mono; (noun) single
- [Wiktionary · çok anlamlı kelime] çıkmak: (verb) to leave, exit, quit, get out; (verb) to get out; (verb) to happen, occur; (verb) to climb
- [Wiktionary · çok anlamlı kelime] taşınmak: (verb) to be moved; (verb) to relocate, to move house; (verb) to frequent
- [Wiktionary · çok anlamlı kelime] alt: (noun) bottom; (noun) under
- [Tatoeba · örnek cümle] Turkish: Tom tek başına bu işle başa çıkamaz. | English: Tom can't handle this job on his own.

**Modele giden sözlük terimleri (0)**

- yok

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: başa çıkmak, elini taşın altına koymak)

- başa çıkmak: hayır
- elini taşın altına koymak: hayır

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 8.30 s | 5.23 s |
| Detaylı Çevir | 0.40 s | 15.97 s | 20.24 s | 36.60 s | 13.16 s |

## W7 · EN→TR (dogrulama-seti-v2)

**Kaynak metin**

```text
The splash screen shows a progress bar while the firmware image is being verified.
```

**Hızlı çeviri** — ilk metin 5.22 s, toplam 8.98 s (bitti)

```text
firmware imajı doğrulanırken açılış ekranında bir ilerleme çubuğu görünür.
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 0): yok

**Detaylı Çevir — denetimden önceki taslak**

```text
firmware görüntüsü doğrulanırken splash ekranı bir ilerleme çubuğu gösterir.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
firmware görüntüsü doğrulanırken splash ekranı bir ilerleme çubuğu gösterir.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": [],
  "bold": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Kalın yazı düzeltmesi (Detaylı)**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (6)**

- [Wiktionary · çok anlamlı kelime] screen: (noun) viewing area of electronic output device → ekran; (noun) movie viewing area → ekran; (noun) physical divider → paravan
- [Wiktionary · çok anlamlı kelime] show: (noun) broadcast program(me) → gösteri, program, şov; (noun) entertainment → gösteri, şov; (noun) exhibition — see also exhibition, exposition → şov; (verb) to display → göstermek
- [Wiktionary · çok anlamlı kelime] bar: (name) town → Bar; (noun) business licensed to sell intoxicating beverages → bar, meyhane; (noun) unit of pressure → bar; (verb) to lock or bolt with a bar → sürgülemek
- [Wiktionary · çok anlamlı kelime] image: (noun) computing: file → görüntü; (verb) computing: to create a backup copy → görüntülemek; (noun) characteristic as perceived by others → imaj; (noun) graphical representation → resim
- [Wiktionary · çok anlamlı kelime] splash: (verb) to hit or agitate liquid → sıçramak, sıçratmak; (verb) to splatter or spread around suddenly → sıçramak, sıçratmak
- [Wiktionary · çok anlamlı kelime] verify: (verb) to confirm or test the truth or accuracy of something → doğrulamak; (verb) to substantiate or prove the truth of something → doğrulamak

**Modele giden sözlük terimleri (1)**

- [kullanıcı sözlüğü] firmware: keep in English

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: splash screen, progress bar)

- splash screen: hayır
- progress bar: hayır

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 8.98 s | 5.22 s |
| Detaylı Çevir | 0.47 s | 16.75 s | 20.04 s | 37.26 s | 13.83 s |

## W8 · EN→TR (dogrulama-seti-v2)

**Kaynak metin**

```text
As for the results, they are in line with what we expected, for the most part.
```

**Hızlı çeviri** — ilk metin 5.07 s, toplam 8.65 s (bitti)

```text
Sonuçlara gelince, büyük ölçüde beklediklerimizle uyumlu durumdalar.
```

Hızlı çeviride kalın yazı düzeltmesi (ek istek: 0): yok

**Detaylı Çevir — denetimden önceki taslak**

```text
Sonuçlara gelince, çoğunlukla beklediğimizle uyumlu durumdalar.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Sonuçlara gelince, çoğunlukla beklediğimizle uyumlu durumdalar.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": [],
  "bold": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Kalın yazı düzeltmesi (Detaylı)**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (7)**

- [Wiktionary · kalıp/deyim] "for the most part" (adv): In most aspects; mostly; generally. [idiomatic]
- [Wiktionary · kalıp/deyim] "in line with" (prep_phrase): In agreement or accordance with.
- [Wiktionary · kalıp/deyim] "in line" (adj): Suitable or appropriate; keeping with expectations, norms, ideals, or rules.; In a queue, waiting one's turn.; Of three or more objects, positioned in a straig… [idiomatic]
- [Wiktionary · kalıp/deyim] "result in" (verb): To bring about; to lead to. [idiomatic]
- [Wiktionary · kalıp/deyim] "as for" (prep): Regarding; about; concerning.
- [Tatoeba · örnek cümle] English: For the most part, I agree with what he said. | Turkish: Çoğunlukla onun dediğine katılıyorum.
- [Tatoeba · örnek cümle] English: The test result isn't what I expected. | Turkish: Test sonucu umduğum gibi değil.

**Modele giden sözlük terimleri (0)**

- yok

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: as for, in line with, for the most part)

- as for: evet — as for [kalıp/deyim, Wiktionary]
- in line with: evet — in line with [kalıp/deyim, Wiktionary]
- for the most part: evet — for the most part [kalıp/deyim, Wiktionary]; For the most part, I agree with what he said. [örnek cümle, Tatoeba]

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 8.65 s | 5.07 s |
| Detaylı Çevir | 0.40 s | 14.73 s | 20.15 s | 35.29 s | 11.62 s |

## Süre tablosu

| Test | Yön | Hızlı ilk metin | Hızlı toplam | Detaylı arama | Detaylı çeviri | Detaylı denetim | Detaylı toplam | Detaylı ilk metin |
|---|---|---|---|---|---|---|---|---|
| D1 | TR→EN | 3.51 s | 10.91 s | 0.91 s | 22.60 s | 21.78 s | 45.29 s | 16.35 s |
| D2 | TR→EN | 5.94 s | 14.33 s | 1.04 s | 24.53 s | 22.05 s | 47.63 s | 17.34 s |
| D3 | EN→TR | 5.50 s | 11.15 s | 0.77 s | 24.39 s | 21.50 s | 46.66 s | 18.19 s |
| D4 | EN→TR | 5.71 s | 12.88 s | 0.79 s | 24.18 s | 40.78 s | 65.75 s | 17.64 s |
| D5 | TR→EN | 6.49 s | 13.37 s | 1.05 s | 20.09 s | 21.55 s | 42.69 s | 14.01 s |
| D6 | EN→TR | 5.43 s | 12.08 s | 0.78 s | 17.32 s | 21.31 s | 39.41 s | 11.25 s |
| D7 | TR→EN | 5.98 s | 12.14 s | 0.55 s | 17.23 s | 21.43 s | 39.21 s | 11.60 s |
| D8 | EN→TR | 7.06 s | 32.03 s | 1.32 s | 38.26 s | 24.63 s | 64.21 s | 27.10 s |
| D9 | TR→EN | 5.51 s | 14.36 s | 0.91 s | 27.54 s | 21.87 s | 50.32 s | 17.91 s |
| D10 | EN→TR | 5.41 s | 9.99 s | 0.70 s | 22.28 s | 21.02 s | 43.99 s | 17.06 s |
| V1 | TR→EN | 4.56 s | 7.96 s | 0.37 s | 14.00 s | 19.75 s | 34.13 s | 10.87 s |
| V2 | EN→TR | 5.11 s | 10.40 s | 0.49 s | 16.25 s | 21.32 s | 38.06 s | 11.13 s |
| V3 | TR→EN | 5.35 s | 11.00 s | 0.67 s | 20.44 s | 21.23 s | 42.34 s | 15.32 s |
| V4 | EN→TR | 5.23 s | 11.73 s | 0.75 s | 20.44 s | 21.22 s | 42.40 s | 14.38 s |
| V5 | TR→EN | 6.52 s | 10.78 s | 0.46 s | 14.19 s | 31.63 s | 46.28 s | 10.28 s |
| G1 | TR→EN | 5.80 s | 14.00 s | 0.94 s | 22.18 s | 32.95 s | 56.07 s | 15.22 s |
| G2 | EN→TR | 5.83 s | 14.08 s | 1.14 s | 29.22 s | 39.58 s | 69.94 s | 20.92 s |
| G3 | TR→EN | 6.46 s | 13.35 s | 0.75 s | 17.03 s | 21.44 s | 39.22 s | 11.45 s |
| W1 | TR→EN | 5.52 s | 10.65 s | 0.39 s | 12.46 s | 25.08 s | 37.93 s | 8.15 s |
| W2 | EN→TR | 5.43 s | 11.24 s | 0.49 s | 18.09 s | 22.42 s | 40.99 s | 13.09 s |
| W3 | TR→EN | 6.04 s | 11.37 s | 0.46 s | 15.36 s | 20.68 s | 36.50 s | 10.20 s |
| W4 | EN→TR | 5.02 s | 9.61 s | 0.67 s | 17.86 s | 20.72 s | 39.25 s | 13.69 s |
| W5 | TR→EN | 4.71 s | 9.66 s | 0.46 s | 14.30 s | 20.25 s | 35.01 s | 10.03 s |
| W6 | TR→EN | 5.23 s | 8.30 s | 0.40 s | 15.97 s | 20.24 s | 36.60 s | 13.16 s |
| W7 | EN→TR | 5.22 s | 8.98 s | 0.47 s | 16.75 s | 20.04 s | 37.26 s | 13.83 s |
| W8 | EN→TR | 5.07 s | 8.65 s | 0.40 s | 14.73 s | 20.15 s | 35.29 s | 11.62 s |
