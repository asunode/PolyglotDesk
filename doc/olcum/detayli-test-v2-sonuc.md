# Detaylı Çevir ölçümü v2 — sonuçlar (ham kayıt)

Setler: `doc/olcum/detayli-test-seti-v1.md` (D1–D10), `doc/olcum/dogrulama-seti-v1.md` (V1–V5), `doc/olcum/kontrol-seti-v2.md` (G1–G3). Betik: `doc/olcum/bench_detayli_v2.py`. Ham veri: `doc/olcum/detayli-test-v2-ham.json`. v1 Detaylı çıktıları: `doc/olcum/detayli-test-v1-ham.json` (Adım 5).
Koşu: 2026-11-19 00:13:23 +0300 – 2026-11-19 00:30:01 +0300. Model gemma4:12b-it-qat, yalnız CPU (num_gpu 0), num_ctx 8192, temperature 0, seed 42. Uygulamanın çeviri yolu: hızlı çeviri `Cevirici`, Detaylı Çevir `DetayliCevirici` (bilgi araması PostgreSQL `cevirmen`, `cevirmen_okur` rolüyle). Her testte önce hızlı çeviri, hemen ardından Detaylı Çevir; D1–D10, V1–V5, G1–G3 sırasıyla.

Notlar:
- Bütün çıktılar ham kayıttan birebir alınmıştır; düzeltilmemiş, kısaltılmamıştır.
- "İlk metin": çeviri başlatıldıktan sonra ekranda ilk çeviri metninin görünmesine kadar geçen süre.
- "Denetimin değiştirdikleri": taslak ile son çıktı arasındaki satır farkı (`-` taslaktaki satır, `+` son çıktıdaki satır).
- "Kod denetimi": `cevirmen/bicim.py`. "Denetimden önce" bulunanlar denetim geçişinde modele bildirildi; "denetimden sonra" son çıktıda kalanlardır.
- "Denetimin kararı": modelin JSON cevabı birebir. Düzeltmeleri kod uygular (`cevirmen/denetim.py`): "uygulanan", "geri alınan" (güvenlik kontrolünün reddettiği, nedeniyle) ve "uygulanamayan" (taslakta bulunamayan vb.) ayrı listelenir.
- "Dikkat kelimeleri modele ulaştı mı": mekanik denetim. Dikkat satırı virgül/noktalı virgülle öğelere ayrılır; öğede tırnak içi varsa o, yoksa "=" işaretinin solu aranır; parantez içi notlar ve sondaki noktalama aranmaz. Aranan, bir bilgi kaydının başlığıyla aynıysa ya da kaydın modele giden metninde ayrı kelime olarak geçiyorsa "evet" (eşleşen kayıtlar yanında). Çekimli/yalın biçim farkı eşleşme sayılmaz.

## D1 · TR→EN (detayli-test-seti-v1)

**Kaynak metin**

```text
Sabahtan beri yüzü gülmüyordu ama gül bahçesine girince yüzünde bir gülümseme belirdi. Ağabeyim de ona "Gözün aydın, sonunda bahçe bitti!" dedi.
```

**Hızlı çeviri** — ilk metin 13.04 s, toplam 20.26 s (bitti)

```text
He hadn't smiled since this morning, but a smile appeared on his face as soon as he entered the rose garden. My older brother also said to him, "Good news, the garden is finally finished!"
```

**v1 Detaylı Çevir — son çıktı (Adım 5)**

```text
He hadn't been smiling since the morning, but a smile appeared on his face when he entered the rose garden. My older brother also said to him, "Congratulations! The garden is finally finished!"
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
  "errors": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

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
- [Wiktionary · çok anlamlı kelime] bit: (noun) louse belonging to genus Pediculus; (noun) a sucking insect parasitic on plants or animals, including true lice…; (noun) bit
- [Wiktionary · çok anlamlı kelime] sabah: (adv) in the morning; (noun) morning; (noun) dawn prayer, fajr
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
| Hızlı çeviri | — | — | — | 20.26 s | 13.04 s |
| Detaylı Çevir | 0.89 s | 22.89 s | 15.62 s | 39.40 s | 16.76 s |

## D2 · TR→EN (detayli-test-seti-v1)

**Kaynak metin**

```text
Öğleden sonra dolu yağdı; bahçedeki domatesler mahvoldu.
Depo dolu, yarın sabah erkenden yola çıkabiliriz.
Bu akşam yüz kişilik bir yemek var, çay kenarındaki salonda.
```

**Hızlı çeviri** — ilk metin 3.93 s, toplam 11.94 s (bitti)

```text
It hailed this afternoon; the tomatoes in the garden were ruined.
The warehouse is full, we can hit the road early tomorrow morning.
There's a dinner for a hundred people this evening, in the hall by the tea area.
```

**v1 Detaylı Çevir — son çıktı (Adım 5)**

```text
Hail fell this afternoon; the tomatoes in the garden were ruined.
The warehouse is full, we can head out early tomorrow morning.
There is a dinner for a hundred people this evening, in the hall by the tea area.
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
  "errors": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (13)**

- [Wiktionary · kalıp/deyim] "bu yüzden" (conj): for this reason, therefore, hence; as a result, thus, consequently
- [Wiktionary · kalıp/deyim] "öğleden sonra" (adv): in the afternoon, p.m.
- [Wiktionary · çok anlamlı kelime] dolu: (adj) full; (noun) hail
- [Wiktionary · çok anlamlı kelime] çay: (noun) tea (plant); (noun) tea (the dried leaves or buds of the tea plant); (noun) tea (the drink made by infusing these dried leaves or buds in hot wat…; (noun) A small river, a brook.
- [Wiktionary · çok anlamlı kelime] kişilik: (adj) divided by a certain number of people, made for a certain number of p…; (noun) personality, character, identity; (noun) synonym of yabanlık; (adj) made up of or consisting of a certain number of people
- [Wiktionary · çok anlamlı kelime] yağ: (noun) oil; (noun) fat, grease
- [Wiktionary · çok anlamlı kelime] yol: (noun) path, road, way; (noun) voyage
- [Wiktionary · çok anlamlı kelime] çıkmak: (verb) to leave, exit, quit, get out; (verb) to get out; (verb) to happen, occur; (verb) to climb
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
| Hızlı çeviri | — | — | — | 11.94 s | 3.93 s |
| Detaylı Çevir | 1.00 s | 25.81 s | 16.37 s | 43.18 s | 18.65 s |

## D3 · EN→TR (detayli-test-seti-v1)

**Kaynak metin**

```text
It's not that I don't trust you; I just don't want to put all my eggs in one basket. Let's not jump the gun and wait for the final numbers.
```

**Hızlı çeviri** — ilk metin 3.95 s, toplam 9.95 s (bitti)

```text
Sana güvenmediğimden değil, sadece tüm yumurtalarımı aynı sepete koymak istemiyorum. Henüz acele etmeyelim ve son rakamları bekleyelim.
```

**v1 Detaylı Çevir — son çıktı (Adım 5)**

```text
Sana güvenmediğimden değil; sadece tüm yumurtalarımı bir sepete koymak istemiyorum. Acele etmeyelim ve son rakamları bekleyelim.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Sana güvenmediğimden değil; sadece tüm yumurtalarımı aynı sepete koymak istemiyorum. Acele edip işi bozmayalım, son rakamları bekleyelim.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Sana güvenmediğimden değil; sadece tüm yumurtalarımı aynı sepete koymak istemiyorum. Acele edip işi bozmayalım, son rakamları bekleyelim.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (10)**

- [Wiktionary · kalıp/deyim] "put all one's eggs in one basket" (verb): To rely on a single source (as of income), rather than diversifying. [idiomatic]
- [Wiktionary · kalıp/deyim] "jump the gun" (verb): To begin a race too soon, before the starting gun goes off.; To act or begin too soon or without due caution.; To trade securities based on information that is… [idiomatic]
- [Wiktionary · kalıp/deyim] "all's one" (phrase): It is just the same; it makes no difference.
- [Wiktionary · kalıp/deyim] "and finally" (noun): A light news story reserved for the end of a bulletin when there is a lack of more important items; typically involving animals or other features supposed to b… [colloquial, idiomatic]
- [Wiktionary · kalıp/deyim] "in one" (prep_phrase): In a single attempt.; Performed downstage between the frontmost pieces of scenery.
- [Wiktionary · çok anlamlı kelime] trust: (noun) a group of businessmen or traders → tröst; (noun) confidence in or reliance on some person or quality → güven, güvenç, itibar; (verb) to place confidence in → güvenmek
- [Tatoeba · örnek cümle] English: Don't put all your eggs in one basket. | Turkish: Tüm kaynaklarını aynı işe yatırma.
- [Tatoeba · örnek cümle] English: Let's not wait for the others. | Turkish: Diğerlerini beklemeyelim.
- [Tatoeba · örnek cümle] English: Let's not jump the gun. | Turkish: Acele etmeyelim.
- [Tatoeba · örnek cümle] English: Put all your eggs in one basket and then watch that basket. | Turkish: Bütün yumurtalarını bir sepete koy ve sonra sepeti izle.

**Modele giden sözlük terimleri (0)**

- yok

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: not that, put all my eggs in one basket, jump the gun)

- not that: hayır
- put all my eggs in one basket: hayır
- jump the gun: evet — jump the gun [kalıp/deyim, Wiktionary]; Let's not jump the gun. [örnek cümle, Tatoeba]

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 9.95 s | 3.95 s |
| Detaylı Çevir | 0.81 s | 25.27 s | 15.88 s | 41.96 s | 19.20 s |

## D4 · EN→TR (detayli-test-seti-v1)

**Kaynak metin**

```text
Make sure the board is **not** powered while you solder the header pins. If the brownout detector keeps firing, the issue is rarely the firmware itself.
```

**Hızlı çeviri** — ilk metin 3.98 s, toplam 11.19 s (bitti)

```text
Header pinlerini lehimlerken kartın **güç almadığından** emin olun. Eğer brownout dedektörü ateşlemeye devam ediyorsa, sorun nadiren firmware'nin kendisidir.
```

**v1 Detaylı Çevir — son çıktı (Adım 5)**

```text
Header pinlerini lehimlerken tahtanın güç almadığından **emin olun**. Eğer brownout dedektörü ateşlemeye devam ediyorsa, sorun nadiren firmware'in kendisidir.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Header pinlerini lehimlerken kartın güç almadığından emin olun. Eğer brownout dedektörü ateşlemeye devam ediyorsa, sorun nadiren firmware'in kendisidir.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Header pinlerini lehimlerken kartın güç almadığından emin olun. Eğer brownout dedektörü ateşlemeye devam ediyorsa, sorun nadiren firmware'in kendisidir.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": true,
  "errors": [
    {
      "type": "format",
      "draft_text": "kartın güç almadığından",
      "corrected_text": "**güç almadığından**",
      "reason": "The source has a bold word (**not**) that is missing in the draft."
    }
  ]
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- (format) “kartın güç almadığından” → “**güç almadığından**” — neden: biçim düzeltmesi kelimeleri değiştiriyor

**Uygulanamayan düzeltmeler**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): The source has 1 bold passage(s) (**not**) but the draft has 0. Mark the corresponding words in the translation as bold with **…**.
- Denetimden sonra (son çıktıda kalan): The source has 1 bold passage(s) (**not**) but the draft has 0. Mark the corresponding words in the translation as bold with **…**.

**Modele giden bilgi kayıtları (8)**

- [Wiktionary · kalıp/deyim] "is it" (intj): Used other than figuratively or idiomatically: see is, it.; really? is that so?
- [Wiktionary · çok anlamlı kelime] board: (noun) long, wide and thin piece of wood or other material → tahta; (noun) managing committee → heyet, kurul; (noun) short for blackboard, whiteboard, etc. → tahta; (noun) side of a ship → borda, sancak
- [Wiktionary · çok anlamlı kelime] solder: (noun) any of various alloys that are used to join small pieces of metal tog… → lehim; (verb) to join with solder → lehimlemek
- [Wiktionary · çok anlamlı kelime] pin: (noun) personal identification number → PIN kodu; (noun) slender object specially designed for use in bowling → kuka, labut, lobut; (noun) small nail → karfiçe; (verb) to fasten/attach with a pin → iliştirmek, pinlemek, sabitlemek
- [Wiktionary · çok anlamlı kelime] keep: (verb) of livestock: to raise; to care for → bakmak; (verb) to continue → -ip durmak, devam etmek; (verb) to maintain possession of → saklamak, tutmak; (verb) to maintain the condition of; to preserve → saklamak
- [Wiktionary · çok anlamlı kelime] fire: (noun) damaging occurrence of fire → yangın; (noun) heater or stove used in place of real fire → ocak; (noun) oxidation reaction → ateş, od; (verb) intransitive: to shoot → ateş etmek
- [Tatoeba · örnek cümle] English: You'd better not do that while Tom is here. | Turkish: Tom buradayken bunu yapmasan iyi olur.
- [Tatoeba · örnek cümle] English: I wanted to make sure you were here. | Turkish: Burada olduğundan emin olmak istedim.

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
| Hızlı çeviri | — | — | — | 11.19 s | 3.98 s |
| Detaylı Çevir | 0.74 s | 26.88 s | 27.13 s | 54.76 s | 20.36 s |

## D5 · TR→EN (detayli-test-seti-v1)

**Kaynak metin**

```text
Kartı yeniden flash'ladım ama watchdog yine tetiklendi. Hatayı log'lardan buldum: stack overflow. Kartın yanındaki kartvizitte yazan numarayı arayıp destek istedim.
```

**Hızlı çeviri** — ilk metin 4.52 s, toplam 11.00 s (bitti)

```text
I flashed the board again, but the watchdog was triggered again. I found the error in the logs: stack overflow. I called the number on the business card next to the board and asked for support.
```

**v1 Detaylı Çevir — son çıktı (Adım 5)**

```text
I flashed the board again, but the watchdog was triggered again. I found the error in the log'lar: stack overflow. I called the number on the business card next to the board and asked for support.
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
  "errors": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (6)**

- [Wiktionary · çok anlamlı kelime] kart: (adj) hoary, old; (noun) card
- [Wiktionary · çok anlamlı kelime] yeniden: (adv) anew; (adv) again
- [Wiktionary · çok anlamlı kelime] bulmak: (verb) to find; (verb) to discover; (verb) to invent; (verb) to reach (a place, a time)
- [Wiktionary · çok anlamlı kelime] numara: (noun) number; (noun) shtick; (noun) stunt
- [Wiktionary · çok anlamlı kelime] aramak: (verb) to seek, to look for, to search; (verb) to phone, to telephone, to ring
- [Wiktionary · çok anlamlı kelime] destek: (noun) fulcrum; (noun) support; (noun) solidarity

**Modele giden sözlük terimleri (3)**

- [kullanıcı sözlüğü] watchdog: keep in English
- [kullanıcı sözlüğü] stack: keep in English
- [kullanıcı sözlüğü] kart → board

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: kart, kartvizit)

- kart: evet — kart → board [sözlük terimi, kullanıcı sözlüğü]; kart [çok anlamlı kelime, Wiktionary]
- kartvizit: hayır

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 11.00 s | 4.52 s |
| Detaylı Çevir | 1.16 s | 18.78 s | 15.70 s | 35.64 s | 12.96 s |

## D6 · EN→TR (detayli-test-seti-v1)

**Kaynak metin**

```text
Dear Ms. Demir, we regret to inform you that the shipment scheduled for 3 December will be delayed by approximately two weeks. We would be grateful for your understanding.
```

**Hızlı çeviri** — ilk metin 3.51 s, toplam 9.99 s (bitti)

```text
Sayın Bayan Demir,
3 Aralık için planlanan sevkiyatın yaklaşık iki hafta gecikeceğini üzülerek bildirmek isteriz. Anlayışınız için teşekkür ederiz.
```

**v1 Detaylı Çevir — son çıktı (Adım 5)**

```text
Sayın Ms. Demir, 3 Aralık için planlanan sevkiyatın yaklaşık iki hafta gecikeceğini üzülerek bildirmek isteriz. Anlayışınız için minnettar oluruz.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Sayın Bayan Demir, 3 Aralık için planlanan sevkiyatın yaklaşık iki hafta gecikeceğini üzülerek bildirmek isteriz. Anlayışınız için teşekkür ederiz.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Sayın Demir, 3 Aralık için planlanan sevkiyatın yaklaşık iki hafta gecikeceğini üzülerek bildirmek isteriz. Anlayışınız için teşekkür ederiz.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": true,
  "errors": [
    {
      "type": "meaning",
      "draft_text": "Sayın Bayan Demir",
      "corrected_text": "Sayın Demir",
      "reason": "In Turkish, 'Bayan' is not used as a title before a surname in formal correspondence; it is redundant and unnatural. The standard equivalent for 'Ms.' is simply the name or 'Hanımefendi'."
    }
  ]
}
```

**Kodun uyguladığı düzeltmeler**

- (meaning) “Sayın Bayan Demir” → “Sayın Demir”

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Denetimin taslakta değiştirdikleri**

```diff
-Sayın Bayan Demir, 3 Aralık için planlanan sevkiyatın yaklaşık iki hafta gecikeceğini üzülerek bildirmek isteriz. Anlayışınız için teşekkür ederiz.
+Sayın Demir, 3 Aralık için planlanan sevkiyatın yaklaşık iki hafta gecikeceğini üzülerek bildirmek isteriz. Anlayışınız için teşekkür ederiz.
```

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (6)**

- [Wiktionary · kalıp/deyim] "for you" (prep_phrase): Used as an intensifier to emphasize typicality of behavior; Used other than figuratively or idiomatically: see for, you.
- [Wiktionary · kalıp/deyim] "to the" (phrase): used in rap songs between the letters of a word being spelled; separates words [slang]
- [Wiktionary · çok anlamlı kelime] dear: (adj) an informal way of addressing the recipient in a letter's opening line → sevgili; (adj) formal way of addressing → sayın; (adj) loved; lovable → sevgili, sevimli
- [Wiktionary · çok anlamlı kelime] shipment: (noun) load of goods → parti; (noun) the act of transporting goods → taşınma
- [Wiktionary · çok anlamlı kelime] delay: (noun) period of time before an event occurs; act of delaying → gecikme, rötar; (verb) to put off until a later time → ertelemek
- [Tatoeba · örnek cümle] English: Thank you for your understanding. | Turkish: Anlayışın için teşekkür ederim.

**Modele giden sözlük terimleri (0)**

- yok

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: Ms., regret to inform)

- Ms.: hayır
- regret to inform: hayır

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 9.99 s | 3.51 s |
| Detaylı Çevir | 0.79 s | 20.80 s | 29.03 s | 50.62 s | 14.74 s |

## D7 · TR→EN (detayli-test-seti-v1)

**Kaynak metin**

```text
Güncelleme sırasında kartın gücünü **kesmeyin**; aksi halde bootloader bozulabilir ve kartı yeniden canlandırmak için UART üzerinden flash'lamanız gerekir.
```

**Hızlı çeviri** — ilk metin 4.80 s, toplam 10.77 s (bitti)

```text
Do not **cut** the power to the board during the update; otherwise, the bootloader may be corrupted and you will need to flash it via UART to revive the board.
```

**v1 Detaylı Çevir — son çıktı (Adım 5)**

```text
Do not **cut** the power to the board during the update; otherwise, the bootloader may be corrupted and you will need to flash it via UART to revive the board.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Do not **cut** the power to the board during the update; otherwise, the bootloader may break and you will need to flash it via UART to revive the board.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Do not **cut** the power to the board during the update; otherwise, the bootloader may break and you will need to flash it via UART to revive the board.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": true,
  "errors": [
    {
      "type": "format",
      "draft_text": "**cut**",
      "corrected_text": "not **cut**",
      "reason": "The bold passage in the source is a negation, but in the draft the bold is on 'cut', which is not the negation. Move the bold on 'not' (the negation word); do not add or change any words."
    }
  ]
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- (format) “**cut**” → “not **cut**” — neden: biçim düzeltmesi kelimeleri değiştiriyor

**Uygulanamayan düzeltmeler**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): The bold passage **kesmeyin** in the source is a negation, but in the draft the bold is on **cut**, which is not the negation. Move the bold on "not" (the negation word); do not add or change any words.
- Denetimden sonra (son çıktıda kalan): The bold passage **kesmeyin** in the source is a negation, but in the draft the bold is on **cut**, which is not the negation. Move the bold on "not" (the negation word); do not add or change any words.

**Modele giden bilgi kayıtları (6)**

- [Wiktionary · çok anlamlı kelime] kart: (adj) hoary, old; (noun) card
- [Wiktionary · çok anlamlı kelime] güç: (adj) hard, difficult; (adv) with difficulty, in a hard way; (noun) strength, force; (noun) power
- [Wiktionary · çok anlamlı kelime] aksi: (adj) contrary, opposite; (adj) stubborn
- [Wiktionary · çok anlamlı kelime] bozulmak: (verb) to break, to stop working; (verb) to go bad, to spoil; (verb) to deteriorate; (verb) to sulk, to take offense
- [Wiktionary · çok anlamlı kelime] yeniden: (adv) anew; (adv) again
- [Wiktionary · çok anlamlı kelime] canlandırmak: (verb) to bring to life; (verb) to bring to consciousness; (verb) to revive; (verb) to resurrect

**Modele giden sözlük terimleri (3)**

- [kullanıcı sözlüğü] bootloader: keep in English
- [kullanıcı sözlüğü] UART: keep in English
- [kullanıcı sözlüğü] kart → board

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: kesmek, canlandırmak)

- kesmek: hayır
- canlandırmak: evet — canlandırmak [çok anlamlı kelime, Wiktionary]

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 10.77 s | 4.80 s |
| Detaylı Çevir | 0.58 s | 18.21 s | 30.96 s | 49.75 s | 12.73 s |

## D8 · EN→TR (detayli-test-seti-v1)

**Kaynak metin**

```text
## Before you start

- Back up the NVS partition; you **cannot** recover it later.
- Don't cut corners on the power supply: a cheap adapter is often the root cause.

Once the board boots, keep an eye on the serial log for the first few minutes.
```

**Hızlı çeviri** — ilk metin 5.24 s, toplam 16.92 s (bitti)

```text
## Başlamadan önce

- NVS partition'ı yedekleyin; daha sonra onu kurtarmanız **mümkün değildir**.
- Güç kaynağı konusunda kestirmeden gitmeyin: ucuz bir adaptör genellikle temel nedendir.

Kart boot olduktan sonra, ilk birkaç dakika boyunca seri kayıt'ı takip edin.
```

**v1 Detaylı Çevir — son çıktı (Adım 5)**

```text
## Başlamadan önce

- NVS partition'ını yedekleyin; daha sonra geri **alamazsınız**.
- Güç kaynağı konusunda kestirme yollara başvurmayın: ucuz bir adaptör genellikle temel nedendir.

Kart açıldıktan sonra, ilk birkaç dakika boyunca seri log'u gözlemleyin.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
## Başlamadan önce

- NVS partition'ı yedekleyin; daha sonra onu kurtaramazsınız.
- Güç kaynağı konusunda kestirme yollara başvurmayın: ucuz bir adaptör genellikle temel nedendir.

Kart boot olduktan sonra, ilk birkaç dakika boyunca seri kayıt ekranını gözlemleyin.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
## Başlamadan önce

- NVS partition'ı yedekleyin; daha sonra onu **kurtaramazsınız**.
- Güç kaynağı konusunda kestirme yollara başvurmayın: ucuz bir adaptör genellikle temel nedendir.

Kart boot olduktan sonra, ilk birkaç dakika boyunca seri kayıt ekranını gözlemleyin.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": true,
  "errors": [
    {
      "type": "format",
      "draft_text": "kurtaramazsınız",
      "corrected_text": "**kurtaramazsınız**",
      "reason": "The source text has bold formatting on 'cannot' which is missing in the draft."
    }
  ]
}
```

**Kodun uyguladığı düzeltmeler**

- (format) “kurtaramazsınız” → “**kurtaramazsınız**”

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Denetimin taslakta değiştirdikleri**

```diff
-- NVS partition'ı yedekleyin; daha sonra onu kurtaramazsınız.
+- NVS partition'ı yedekleyin; daha sonra onu **kurtaramazsınız**.
```

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): The source has 1 bold passage(s) (**cannot**) but the draft has 0. Mark the corresponding words in the translation as bold with **…**.
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (16)**

- [Wiktionary · kalıp/deyim] "keep an eye on" (verb): To watch and pay attention to, in case of misbehaviour or mishap. [idiomatic]
- [Wiktionary · kalıp/deyim] "on the cheap" (prep_phrase): Synonym of cheaply or economically.; Too cheaply or economically, inexpensive and affordable to the point of substandard quality. [informal]
- [Wiktionary · kalıp/deyim] "back up" (verb): To move backwards, especially for a vehicle to do so.; To move a vehicle backwards.; To undo one's actions. [idiomatic, informal] → Turkish: yedeklemek
- [Wiktionary · kalıp/deyim] "cut corners" (verb): To bypass a prescribed route so as to gain competitive advantage or to circumvent traffic signals or other rules of the road.; To do a less-than-thorough or in… [idiomatic]
- [Wiktionary · kalıp/deyim] "keep on" (verb): To persist or continue.; To persist in talking about a subject, perhaps to the annoyance of the listener.; To cause or allow to remain in an existing position. [idiomatic]
- [Wiktionary · çok anlamlı kelime] start: (noun) beginning of an activity → başlangıç; (noun) beginning point of a race → start; (verb) to begin → başlamak
- [Wiktionary · çok anlamlı kelime] root: (noun) arithmetic: number or expression which when raised to a power gives t… → kök; (noun) linguistic morphology: primary lexical unit of a word → kök; (noun) of a tooth → kök; (noun) part of a hair under the skin → kök
- [Wiktionary · çok anlamlı kelime] board: (noun) long, wide and thin piece of wood or other material → tahta; (noun) managing committee → heyet, kurul; (noun) short for blackboard, whiteboard, etc. → tahta; (noun) side of a ship → borda, sancak
- [Wiktionary · çok anlamlı kelime] boot: (noun) heavy shoe that covers part of the leg → çizme; (verb) to start a system → başlatma
- [Wiktionary · çok anlamlı kelime] log: (noun) (computer) an append-only sequence of records written to disk → kütük; (noun) bulky piece of timber → tomruk; (noun) chronological record → kütük; (noun) trunk of dead tree, cleared of branches → kütük
- [Wiktionary · çok anlamlı kelime] adapter: (noun) device allowing plug to fit in an outlet of different type → adaptör, priz adaptörü; (noun) device that converts AC to DC for battery-powered gadgets → adaptör; (noun) device to allow compatibility (in general) → adaptör
- [Tatoeba · örnek cümle] English: I'll phone you before I start. | Turkish: Ayrılmadan önce seni ararım.
- [Tatoeba · örnek cümle] English: You start. | Turkish: Sen başla.
- [Tatoeba · örnek cümle] English: Could you keep an eye on my suitcase for a few minutes? | Turkish: Beş dakika için valizime göz kulak olabilir misin?
- [Tatoeba · örnek cümle] English: Can I call you back later? | Turkish: Seni sonra tekrar arayabilir miyim?
- [Tatoeba · örnek cümle] English: Can you call back later? | Turkish: Daha sonra tekrar arayabilir misin?

**Modele giden sözlük terimleri (5)**

- [kullanıcı sözlüğü] partition: keep in English
- [kullanıcı sözlüğü] NVS: keep in English
- [kullanıcı sözlüğü] power supply → güç kaynağı
- [kullanıcı sözlüğü] board → kart
- [kullanıcı sözlüğü] log → kayıt

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: cut corners, root cause, keep an eye on)

- cut corners: evet — cut corners [kalıp/deyim, Wiktionary]
- root cause: hayır
- keep an eye on: evet — keep an eye on [kalıp/deyim, Wiktionary]; Could you keep an eye on my suitcase for a few minutes? [örnek cümle, Tatoeba]

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 16.92 s | 5.24 s |
| Detaylı Çevir | 1.56 s | 41.92 s | 29.11 s | 72.59 s | 31.13 s |

## D9 · TR→EN (detayli-test-seti-v1)

**Kaynak metin**

```text
Bu işi yarına bırakma, sonra dokuz doğurursun. Ayağımıza kadar gelmiş fırsatı tepmek olmaz; nabzına göre şerbet ver ama ipin ucunu da kaçırma.
```

**Hızlı çeviri** — ilk metin 3.73 s, toplam 12.60 s (bitti)

```text
Don't put off today's work for tomorrow, or you might end up with nine babies later on. You can't just kick away an opportunity that has reached your feet; give the right answer to the situation, but don't lose your grip either.
```

**v1 Detaylı Çevir — son çıktı (Adım 5)**

```text
Don't put off today's work until tomorrow, or you'll end up with a mountain of trouble later. You shouldn't turn down an opportunity that's right at your doorstep; treat people according to their temperament, but don't lose your grip on the situation.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Don't put off today's work until tomorrow, or you'll end up with a mountain of trouble later. You shouldn't turn down an opportunity that has come right to our doorstep; treat people according to their needs, but don't lose control of the situation.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Don't put off today's work until tomorrow, or you'll end up with a mountain of trouble later. You shouldn't turn down an opportunity that has come right to our doorstep; treat people according to their needs, but don't lose control of the situation.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (9)**

- [Wiktionary · kalıp/deyim] "ipin ucunu kaçırmak" (verb): to lose control of a situation, to lose one's grip on things; to go too far [idiomatic]
- [Wiktionary · çok anlamlı kelime] ayak: (noun) foot; (noun) pillar, tower; (noun) stand, footrest; (noun) leg (support of a furniture)
- [Wiktionary · çok anlamlı kelime] yarın: (adv) tomorrow; (noun) tomorrow; (noun) morrow, the next or following day; (noun) future
- [Wiktionary · çok anlamlı kelime] iş: (noun) work, task, deed; (noun) energy expended on moving an object, force times distance; (noun) job, employment; (noun) matter, affair, business, activity
- [Wiktionary · çok anlamlı kelime] doğurmak: (verb) to breed, to give birth; (verb) to give rise to
- [Wiktionary · çok anlamlı kelime] gelmek: (verb) to come, move closer; (verb) to come, to appear, to manifest; (verb) to weigh (have a certain weight); (verb) to seem, to appear
- [Wiktionary · çok anlamlı kelime] tepmek: (verb) to kick, especially for an animal; (verb) to tread on, trample (something); (verb) to decline, turn down, reject (something); to throw away (an opportun…; (verb) (for a gun) to kick, recoil.
- [Tatoeba · örnek cümle] Turkish: Bugünkü işini yarına bırakma. | English: Never put off till tomorrow what you can do today.
- [Tatoeba · örnek cümle] Turkish: Bugünün işini yarına bırakma. | English: A stitch in time saves nine.

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
| Hızlı çeviri | — | — | — | 12.60 s | 3.73 s |
| Detaylı Çevir | 2.35 s | 27.65 s | 16.66 s | 46.66 s | 19.81 s |

## D10 · EN→TR (detayli-test-seti-v1)

**Kaynak metin**

```text
Oh great, the build failed again. I'll look into it after lunch, but don't hold your breath — I've run out of ideas.
```

**Hızlı çeviri** — ilk metin 3.30 s, toplam 8.04 s (bitti)

```text
Harika, build yine başarısız oldu. Öğleden sonra bakacağım ama çok da umutlanma; artık fikirlerim tükendi.
```

**v1 Detaylı Çevir — son çıktı (Adım 5)**

```text
Harika, build yine başarısız oldu. Öğle yemeğinden sonra bakacağım ama nefesini tutma; fikirlerim tükendi.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Harika, build yine başarısız oldu. Öğle yemeğinden sonra bakacağım ama pek umut etme; fikirlerim tükendi.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Harika, build yine başarısız oldu. Öğle yemeğinden sonra bakacağım ama pek umut etme; fikirlerim tükendi.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (10)**

- [Wiktionary · kalıp/deyim] "hold one's breath" (verb): Used other than figuratively or idiomatically: see hold, one's, breath. To keep air in one's lungs, pausing noticeably before exhaling after previously inhalin… [idiomatic] → Turkish: nefesini tutmak; soluğunu tutmak; nefesini tutup beklemek
- [Wiktionary · kalıp/deyim] "look into" (verb): To investigate, explore, or consider.; Used other than figuratively or idiomatically: look into. [idiomatic]
- [Wiktionary · kalıp/deyim] "run out" (verb): To use up or consume all; To expire; to come to an end.; To be completely used up or consumed. [idiomatic] → Turkish: bitmek; tükenmek
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
| Hızlı çeviri | — | — | — | 8.04 s | 3.30 s |
| Detaylı Çevir | 0.79 s | 22.86 s | 15.24 s | 38.90 s | 18.34 s |

## V1 · TR→EN (dogrulama-seti-v1)

**Kaynak metin**

```text
Çocuğa bu kadar yüz verme, sonra başına çıkar.
```

**Hızlı çeviri** — ilk metin 2.93 s, toplam 6.66 s (bitti)

```text
Don't let the child have their way with you so much; they'll cause trouble for you later.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Don't give that kid so much leeway, or it'll come back to haunt you.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Don't give that kid so much leeway, or it'll come back to haunt you.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (5)**

- [Wiktionary · kalıp/deyim] "başa çıkmak" (verb): to deal with, to handle, to tackle, to overcome [idiomatic]
- [Wiktionary · kalıp/deyim] "bu yüzden" (conj): for this reason, therefore, hence; as a result, thus, consequently
- [Wiktionary · çok anlamlı kelime] çocuk: (noun) child; (noun) a male around dating age
- [Wiktionary · çok anlamlı kelime] vermek: (verb) to give; (verb) to consent for sex, to put out; (verb) to give out, to donate; (verb) to attribute
- [Tatoeba · örnek cümle] Turkish: Bu öğleden sonra yüzmemeye karar verdim. | English: I've decided not to swim this afternoon.

**Modele giden sözlük terimleri (0)**

- yok

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: yüz vermek, başına çıkmak)

- yüz vermek: hayır
- başına çıkmak: hayır

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 6.66 s | 2.93 s |
| Detaylı Çevir | 0.37 s | 14.21 s | 14.51 s | 29.09 s | 11.11 s |

## V2 · EN→TR (dogrulama-seti-v1)

**Kaynak metin**

```text
Flash the board only after the bootloader prints its banner; otherwise the upload will **not** take effect.
```

**Hızlı çeviri** — ilk metin 3.71 s, toplam 9.18 s (bitti)

```text
Board'u sadece bootloader kendi banner'ını yazdırdıktan sonra flashlayın; aksi takdirde yükleme geçerli **olmayacaktır**.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Kartı sadece bootloader bandı yazdırdıktan sonra flashlayın; aksi takdirde yükleme **geçerli olmayacaktır**.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Kartı sadece bootloader bandı yazdırdıktan sonra flashlayın; aksi takdirde yükleme **geçerli olmayacaktır**.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (4)**

- [Wiktionary · çok anlamlı kelime] board: (noun) long, wide and thin piece of wood or other material → tahta; (noun) managing committee → heyet, kurul; (noun) short for blackboard, whiteboard, etc. → tahta; (noun) side of a ship → borda, sancak
- [Wiktionary · çok anlamlı kelime] banner: (noun) flag → bandıra, bayrak, sancak; (noun) large piece of cloth with a slogan or emblem carried in a demonstrati… → pankart
- [Wiktionary · çok anlamlı kelime] otherwise: (adv) differently, in another way → aksi; (adv) under different circumstances → yoksa
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
| Hızlı çeviri | — | — | — | 9.18 s | 3.71 s |
| Detaylı Çevir | 0.50 s | 17.65 s | 14.79 s | 32.95 s | 12.94 s |

## V3 · TR→EN (dogrulama-seti-v1)

**Kaynak metin**

```text
Bankada sıra çok uzundu, ben de dışarıdaki banka oturup bekledim. Dönüşte yağmur değil kar yağıyordu.
```

**Hızlı çeviri** — ilk metin 3.58 s, toplam 8.88 s (bitti)

```text
The queue at the bank was very long, so I sat on a bench outside and waited. When I returned, it wasn't raining; it was snowing.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
The line at the bank was very long, so I sat on a bench outside and waited. On the way back, it wasn't raining; it was snowing.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
The line at the bank was very long, so I sat on a bench outside and waited. On the way back, it wasn't raining; it was snowing.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

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
- [Tatoeba · örnek cümle] Turkish: Kar yağıyordu. | English: It was snowing.
- [Tatoeba · örnek cümle] Turkish: Bir banka oturup bekledim. | English: I sat on a bench and waited.
- [Tatoeba · örnek cümle] Turkish: Tom otuz dakika dışarıda bekledi. | English: Tom waited outside for thirty minutes.

**Modele giden sözlük terimleri (0)**

- yok

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: banka (bank / oturak), kar)

- banka (bank / oturak): evet — Bir banka oturup bekledim. [örnek cümle, Tatoeba]
- kar: evet — kar yağıyor [kalıp/deyim, Wiktionary]; Kar yağıyordu. [örnek cümle, Tatoeba]

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 8.88 s | 3.58 s |
| Detaylı Çevir | 0.68 s | 22.14 s | 15.53 s | 38.34 s | 17.03 s |

## V4 · EN→TR (dogrulama-seti-v1)

**Kaynak metin**

```text
Dear Mr. Aksoy, please find attached the revised invoice. Should you have any questions, do not hesitate to contact us.
```

**Hızlı çeviri** — ilk metin 3.38 s, toplam 9.78 s (bitti)

```text
Sayın Bay Aksoy, revize edilmiş faturayı ekte bulabilirsiniz. Herhangi bir sorunuz olması durumunda bizimle iletişime geçmekten çekinmeyiniz.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Sayın Bay Aksoy, revize edilmiş faturayı ekte bulabilirsiniz. Herhangi bir sorunuz olması durumunda bizimle iletişime geçmekten çekinmeyin.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Sayın Aksoy, revize edilmiş faturayı ekte bulabilirsiniz. Herhangi bir sorunuz olması durumunda bizimle iletişime geçmekten çekinmeyin.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": true,
  "errors": [
    {
      "type": "addition",
      "draft_text": "Sayın Bay Aksoy",
      "corrected_text": "Sayın Aksoy",
      "reason": "In Turkish, 'Sayın' already functions as a formal title; using both 'Sayın' and 'Bay' is redundant and unnatural."
    }
  ]
}
```

**Kodun uyguladığı düzeltmeler**

- (addition) “Sayın Bay Aksoy” → “Sayın Aksoy”

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Denetimin taslakta değiştirdikleri**

```diff
-Sayın Bay Aksoy, revize edilmiş faturayı ekte bulabilirsiniz. Herhangi bir sorunuz olması durumunda bizimle iletişime geçmekten çekinmeyin.
+Sayın Aksoy, revize edilmiş faturayı ekte bulabilirsiniz. Herhangi bir sorunuz olması durumunda bizimle iletişime geçmekten çekinmeyin.
```

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
| Hızlı çeviri | — | — | — | 9.78 s | 3.38 s |
| Detaylı Çevir | 0.76 s | 21.52 s | 26.30 s | 48.57 s | 15.58 s |

## V5 · TR→EN (dogrulama-seti-v1)

**Kaynak metin**

```text
Log'ları temizledim ama SD karttaki kayıtlar hâlâ duruyor; kartı formatlamadan önce yedek alacağım.
```

**Hızlı çeviri** — ilk metin 4.67 s, toplam 8.92 s (bitti)

```text
I cleared the logs, but the records on the SD card are still there; I will take a backup before formatting the board.
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
  "has_errors": false,
  "errors": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (5)**

- [Wiktionary · çok anlamlı kelime] kart: (adj) hoary, old; (noun) card
- [Wiktionary · çok anlamlı kelime] yedek: (noun) replacement; (adj) auxiliary; (adj) spare; (noun) spare, substitute
- [Wiktionary · çok anlamlı kelime] kayıt: (noun) record, recording; (noun) registration, registry; (noun) caring, paying attention; (noun) check-in
- [Wiktionary · çok anlamlı kelime] durmak: (verb) to stop; (verb) to stand; to sit still; to remain; (verb) to be (at a certain place); (verb) to last; to continue to be, to keep being
- [Wiktionary · çok anlamlı kelime] almak: (verb) to take; (verb) to buy; (verb) to get, to obtain, to receive; (verb) to receive (a radio signal)

**Modele giden sözlük terimleri (4)**

- [kullanıcı sözlüğü] SD kart → SD card
- [kullanıcı sözlüğü] kart → board
- [kullanıcı sözlüğü] kayıtlar → logs
- [kullanıcı sözlüğü] kayıt → log

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: kart (burada SD kart), kayıtlar)

- kart (burada SD kart): evet — SD kart → SD card [sözlük terimi, kullanıcı sözlüğü]; kart → board [sözlük terimi, kullanıcı sözlüğü]; kart [çok anlamlı kelime, Wiktionary]
- kayıtlar: evet — kayıtlar → logs [sözlük terimi, kullanıcı sözlüğü]

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 8.92 s | 4.67 s |
| Detaylı Çevir | 0.48 s | 16.91 s | 14.78 s | 32.18 s | 13.01 s |

## G1 · TR→EN (kontrol-seti-v2)

**Kaynak metin**

```text
Ocak ayında ocağın başında oturup kestane közledik.
Bağ evinin bahçesinde ayakkabımın bağı çözüldü.
Kapı çalındığında komşunun oğlu gitar çalıyordu.
```

**Hızlı çeviri** — ilk metin 4.06 s, toplam 11.69 s (bitti)

```text
We sat down at the beginning of January and roasted chestnuts over an open fire.
My shoelace came undone in the garden of the country house.
The neighbor's son was playing guitar when someone knocked on the door.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
We sat by the stove in January and roasted chestnuts.
My shoelace came undone in the garden of the vineyard house.
The neighbor's son was playing the guitar when there was a knock at the door.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
We sat by the stove in January and roasted chestnuts.
My shoelace came undone in the garden of the vineyard house.
The neighbor's son was playing the guitar when there was a knock at the door.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

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
| Hızlı çeviri | — | — | — | 11.69 s | 4.06 s |
| Detaylı Çevir | 0.99 s | 23.75 s | 16.09 s | 40.83 s | 17.00 s |

## G2 · EN→TR (kontrol-seti-v2)

**Kaynak metin**

```text
The results were not half bad for a first attempt.
I can't help but notice that the fan never stops spinning.
The flash write does **not** start until the erase cycle has completed.
```

**Hızlı çeviri** — ilk metin 3.69 s, toplam 11.83 s (bitti)

```text
İlk deneme için sonuçlar hiç de kötü değildi.
Fanın hiç durmadan dönmediğini fark etmemek elde değil.
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
      "reason": "The source says 'never stops spinning' (continuously spinning), but the draft translates it as 'doesn't spin without stopping', which reverses the meaning."
    }
  ]
}
```

**Kodun uyguladığı düzeltmeler**

- (meaning) “Vantilatörün hiç durmadan dönmediğini fark etmemek elde değil.” → “Vantilatörün hiç durmadan döndüğünü fark etmemek elde değil.”

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

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
| Hızlı çeviri | — | — | — | 11.83 s | 3.69 s |
| Detaylı Çevir | 1.11 s | 31.30 s | 32.97 s | 65.38 s | 23.06 s |

## G3 · TR→EN (kontrol-seti-v2)

**Kaynak metin**

```text
Kartın brownout reset'i sık sık tetikleniyor; kondansatörü değiştirdikten sonra bile log'larda aynı hata var. Kartı kredi kartı boyutunda bir kutuya koyacağım.
```

**Hızlı çeviri** — ilk metin 4.25 s, toplam 10.65 s (bitti)

```text
The board's brownout reset is triggered frequently; even after replacing the capacitor, the same error appears in the logs. I will put the board into a box the size of a credit card.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
The board's brownout reset is triggered often; the same error is in the logs even after replacing the capacitor. I will put the board in a box the size of a credit card.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
The board's brownout reset is triggered often; the same error is in the logs even after replacing the capacitor. I will put the board in a box the size of a credit card.
```

**Denetimin kararı (modelin JSON cevabı)**

```json
{
  "has_errors": false,
  "errors": []
}
```

**Kodun uyguladığı düzeltmeler**

- yok

**Kod güvenlik kontrolünün geri aldığı değişiklikler**

- yok

**Uygulanamayan düzeltmeler**

- yok

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (6)**

- [Wiktionary · kalıp/deyim] "sık sık" (adv): often
- [Wiktionary · çok anlamlı kelime] kart: (adj) hoary, old; (noun) card
- [Wiktionary · çok anlamlı kelime] kutu: (noun) box; (noun) vagina
- [Wiktionary · çok anlamlı kelime] koymak: (verb) to put; (verb) to put, to add; (verb) to prepare or serve a food or a drink; (verb) to appoint, to assign
- [Tatoeba · örnek cümle] Turkish: Bunu kutuya koyacağım. | English: I'll put it in the box.
- [Tatoeba · örnek cümle] Turkish: Bu boyutta bir kutuya ihtiyacım var. | English: I need a box of this size.

**Modele giden sözlük terimleri (2)**

- [kullanıcı sözlüğü] brownout: keep in English
- [kullanıcı sözlüğü] kart → board

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: ilk "kart" = board, "kredi kartı" = credit card (aynı metinde ikisi de var).)

- ilk "kart" = board: evet — kart → board [sözlük terimi, kullanıcı sözlüğü]; kart [çok anlamlı kelime, Wiktionary]
- "kredi kartı" = credit card (aynı metinde ikisi de var).: hayır

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 10.65 s | 4.25 s |
| Detaylı Çevir | 0.90 s | 20.00 s | 15.90 s | 36.80 s | 14.24 s |

## Süre tablosu

| Test | Yön | Hızlı ilk metin | Hızlı toplam | Detaylı arama | Detaylı çeviri | Detaylı denetim | Detaylı toplam | Detaylı ilk metin |
|---|---|---|---|---|---|---|---|---|
| D1 | TR→EN | 13.04 s | 20.26 s | 0.89 s | 22.89 s | 15.62 s | 39.40 s | 16.76 s |
| D2 | TR→EN | 3.93 s | 11.94 s | 1.00 s | 25.81 s | 16.37 s | 43.18 s | 18.65 s |
| D3 | EN→TR | 3.95 s | 9.95 s | 0.81 s | 25.27 s | 15.88 s | 41.96 s | 19.20 s |
| D4 | EN→TR | 3.98 s | 11.19 s | 0.74 s | 26.88 s | 27.13 s | 54.76 s | 20.36 s |
| D5 | TR→EN | 4.52 s | 11.00 s | 1.16 s | 18.78 s | 15.70 s | 35.64 s | 12.96 s |
| D6 | EN→TR | 3.51 s | 9.99 s | 0.79 s | 20.80 s | 29.03 s | 50.62 s | 14.74 s |
| D7 | TR→EN | 4.80 s | 10.77 s | 0.58 s | 18.21 s | 30.96 s | 49.75 s | 12.73 s |
| D8 | EN→TR | 5.24 s | 16.92 s | 1.56 s | 41.92 s | 29.11 s | 72.59 s | 31.13 s |
| D9 | TR→EN | 3.73 s | 12.60 s | 2.35 s | 27.65 s | 16.66 s | 46.66 s | 19.81 s |
| D10 | EN→TR | 3.30 s | 8.04 s | 0.79 s | 22.86 s | 15.24 s | 38.90 s | 18.34 s |
| V1 | TR→EN | 2.93 s | 6.66 s | 0.37 s | 14.21 s | 14.51 s | 29.09 s | 11.11 s |
| V2 | EN→TR | 3.71 s | 9.18 s | 0.50 s | 17.65 s | 14.79 s | 32.95 s | 12.94 s |
| V3 | TR→EN | 3.58 s | 8.88 s | 0.68 s | 22.14 s | 15.53 s | 38.34 s | 17.03 s |
| V4 | EN→TR | 3.38 s | 9.78 s | 0.76 s | 21.52 s | 26.30 s | 48.57 s | 15.58 s |
| V5 | TR→EN | 4.67 s | 8.92 s | 0.48 s | 16.91 s | 14.78 s | 32.18 s | 13.01 s |
| G1 | TR→EN | 4.06 s | 11.69 s | 0.99 s | 23.75 s | 16.09 s | 40.83 s | 17.00 s |
| G2 | EN→TR | 3.69 s | 11.83 s | 1.11 s | 31.30 s | 32.97 s | 65.38 s | 23.06 s |
| G3 | TR→EN | 4.25 s | 10.65 s | 0.90 s | 20.00 s | 15.90 s | 36.80 s | 14.24 s |
