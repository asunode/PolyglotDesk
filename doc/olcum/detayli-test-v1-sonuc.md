# Detaylı Çevir test seti v1 — sonuçlar (ham kayıt)

Test seti: `doc/olcum/detayli-test-seti-v1.md`. Betik: `doc/olcum/bench_detayli.py`. Ham veri: `doc/olcum/detayli-test-v1-ham.json`.
Koşu: 2026-11-18 23:00:35 +0300 – 2026-11-18 23:09:15 +0300. Model gemma4:12b-it-qat, yalnız CPU (num_gpu 0), num_ctx 8192, temperature 0, seed 42. Uygulamanın çeviri yolu: hızlı çeviri `Cevirici`, Detaylı Çevir `DetayliCevirici` (bilgi araması PostgreSQL `cevirmen`, `cevirmen_okur` rolüyle). Her testte önce hızlı çeviri, hemen ardından Detaylı Çevir; D1'den D10'a sırayla.

Notlar:
- Bütün çıktılar ham kayıttan birebir alınmıştır; düzeltilmemiş, kısaltılmamıştır.
- "İlk metin": çeviri başlatıldıktan sonra ekranda ilk çeviri metninin görünmesine kadar geçen süre.
- "Denetimin değiştirdikleri": taslak ile son çıktı arasındaki satır farkı (`-` taslaktaki satır, `+` son çıktıdaki satır).
- "Kod denetimi": `cevirmen/bicim.py`. "Denetimden önce" bulunanlar denetim geçişinde modele bildirildi; "denetimden sonra" son çıktıda kalanlardır.
- "Dikkat kelimeleri modele ulaştı mı": mekanik denetim. Kelime ya da ifade, bir bilgi kaydının başlığıyla aynıysa ya da kaydın modele giden metninde ayrı kelime olarak geçiyorsa "evet" (eşleşen kayıtlar yanında). Parantez içindeki notlar aranmaz. Çekimli/yalın biçim farkı eşleşme sayılmaz.

## D1 · TR→EN

**Kaynak metin**

```text
Sabahtan beri yüzü gülmüyordu ama gül bahçesine girince yüzünde bir gülümseme belirdi. Ağabeyim de ona "Gözün aydın, sonunda bahçe bitti!" dedi.
```

**Hızlı çeviri** — ilk metin 3.54 s, toplam 10.77 s (bitti)

```text
He hadn't smiled since this morning, but a smile appeared on his face as soon as he entered the rose garden. My older brother also said to him, "Good news, the garden is finally finished!"
```

**Detaylı Çevir — denetimden önceki taslak**

```text
He hadn't smiled since this morning, but a smile appeared on his face when he entered the rose garden. My brother also said to him, "Congratulations! The garden is finally finished!"
```

**Detaylı Çevir — son çıktı** (bitti)

```text
He hadn't been smiling since the morning, but a smile appeared on his face when he entered the rose garden. My older brother also said to him, "Congratulations! The garden is finally finished!"
```

**Denetimin taslakta değiştirdikleri**

```diff
-He hadn't smiled since this morning, but a smile appeared on his face when he entered the rose garden. My brother also said to him, "Congratulations! The garden is finally finished!"
+He hadn't been smiling since the morning, but a smile appeared on his face when he entered the rose garden. My older brother also said to him, "Congratulations! The garden is finally finished!"
```

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (9)**

- [Wiktionary · kalıp/deyim] "gözün aydın" (phrase): congratulations!
- [Wiktionary · çok anlamlı kelime] sabah: (adv) in the morning; (noun) morning; (noun) dawn prayer, fajr
- [Wiktionary · çok anlamlı kelime] yüz: (noun) face; (noun) lining; (noun) face, surface, cutting edge; (noun) side, aspect
- [Wiktionary · çok anlamlı kelime] gülle: (noun) A spherical cannonball made out of stone or metal.; (noun) A modern tank or artillery shell that is cylindrical with a pointy en…; (noun) The iron ball used for shot put games; a shot.
- [Wiktionary · çok anlamlı kelime] girmek: (verb) to enter, to go in; (verb) to go in for, to take; (verb) (a season, time &c.) to arrive
- [Wiktionary · çok anlamlı kelime] bir: (adv) only, solely, merely; (noun) mono; (adj) one; (adj) Used to emphasize a particular quality about something
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
| Hızlı çeviri | — | — | — | 10.77 s | 3.54 s |
| Detaylı Çevir | 0.94 s | 19.70 s | 16.65 s | 37.30 s | 13.96 s |

## D2 · TR→EN

**Kaynak metin**

```text
Öğleden sonra dolu yağdı; bahçedeki domatesler mahvoldu.
Depo dolu, yarın sabah erkenden yola çıkabiliriz.
Bu akşam yüz kişilik bir yemek var, çay kenarındaki salonda.
```

**Hızlı çeviri** — ilk metin 3.54 s, toplam 11.91 s (bitti)

```text
It rained heavily this afternoon; the tomatoes in the garden were ruined.
The warehouse is full, we can hit the road early tomorrow morning.
There's a dinner for a hundred people this evening, in the hall by the tea area.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Hail fell this afternoon; the tomatoes in the garden were ruined.
The warehouse is full, we can head out early tomorrow morning.
There is a dinner for a hundred people this evening, in the hall by the tea area.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Hail fell this afternoon; the tomatoes in the garden were ruined.
The warehouse is full, we can head out early tomorrow morning.
There is a dinner for a hundred people this evening, in the hall by the tea area.
```

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (11)**

- [Wiktionary · çok anlamlı kelime] sonra: (noun) aftermath; (adv) later, after, afterwards, post-; (adv) thereafter, subsequently, following; (adv) hereafter, in the future
- [Wiktionary · çok anlamlı kelime] dolu: (adj) full; (noun) hail
- [Wiktionary · çok anlamlı kelime] yar: (noun) cliff, scarp, precipice; (noun) love, beloved
- [Wiktionary · çok anlamlı kelime] sabah: (adv) in the morning; (noun) morning; (noun) dawn prayer, fajr
- [Wiktionary · çok anlamlı kelime] erke: (noun) energy; (noun) power for success
- [Wiktionary · çok anlamlı kelime] yol: (noun) path, road, way; (noun) voyage
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
- çay: hayır

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 11.91 s | 3.54 s |
| Detaylı Çevir | 1.00 s | 19.80 s | 18.42 s | 39.22 s | 12.62 s |

## D3 · EN→TR

**Kaynak metin**

```text
It's not that I don't trust you; I just don't want to put all my eggs in one basket. Let's not jump the gun and wait for the final numbers.
```

**Hızlı çeviri** — ilk metin 3.75 s, toplam 10.02 s (bitti)

```text
Sana güvenmediğimden değil; sadece tüm yumurtalarımı aynı sepete koymak istemiyorum. Henüz acele etmeyelim ve son rakamları bekleyelim.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Sana güvenmediğimden değil; sadece tüm yumurtalarımı bir sepete koymak istemiyorum. Acele edip son rakamları bekleyelim.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Sana güvenmediğimden değil; sadece tüm yumurtalarımı bir sepete koymak istemiyorum. Acele etmeyelim ve son rakamları bekleyelim.
```

**Denetimin taslakta değiştirdikleri**

```diff
-Sana güvenmediğimden değil; sadece tüm yumurtalarımı bir sepete koymak istemiyorum. Acele edip son rakamları bekleyelim.
+Sana güvenmediğimden değil; sadece tüm yumurtalarımı bir sepete koymak istemiyorum. Acele etmeyelim ve son rakamları bekleyelim.
```

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (12)**

- [Wiktionary · kalıp/deyim] "don't put all your eggs in one basket" (proverb): Do not dedicate all your resources to one project.; Do not count on any one thing to safeguard what is valuable.
- [Wiktionary · kalıp/deyim] "jump the gun" (verb): To begin a race too soon, before the starting gun goes off.; To act or begin too soon or without due caution.; To trade securities based on information that is… [idiomatic]
- [Wiktionary · çok anlamlı kelime] trust: (noun) a group of businessmen or traders → tröst; (noun) confidence in or reliance on some person or quality → güven, güvenç, itibar; (verb) to place confidence in → güvenmek
- [Wiktionary · çok anlamlı kelime] want: (noun) desire, wish, longing → istek; (verb) to desire → istemek
- [Wiktionary · çok anlamlı kelime] basket: (noun) basketball: act of putting the ball through the basket → basket; (noun) container → sele, sepet; (noun) notional place to store items before ordering them online → sepet
- [Wiktionary · çok anlamlı kelime] jump: (verb) cause oneself to leave an elevated location and fall downward → atlamak; (verb) propel oneself rapidly upward such that momentum causes the body to b… → sekmek, zıplamak
- [Wiktionary · çok anlamlı kelime] gun: (noun) less portable, long weapon → tüfek; (noun) military: cannon with relatively long barrel, operating with relative… → top; (noun) military: cannon with tube length 30 calibers or more → top; (noun) portable, short weapon, for hand use → tabanca
- [Wiktionary · çok anlamlı kelime] final: (noun) sports: last round in a contest → final; (noun) test or examination given at the end of a term or class → final
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
| Hızlı çeviri | — | — | — | 10.02 s | 3.75 s |
| Detaylı Çevir | 0.76 s | 24.64 s | 15.55 s | 40.95 s | 19.53 s |

## D4 · EN→TR

**Kaynak metin**

```text
Make sure the board is **not** powered while you solder the header pins. If the brownout detector keeps firing, the issue is rarely the firmware itself.
```

**Hızlı çeviri** — ilk metin 3.65 s, toplam 10.36 s (bitti)

```text
Header pinlerini lehimlerken kartın güç almadığından emin olun. Eğer brownout dedektörü ateşlemeye devam ediyorsa, sorun nadiren firmware'nin kendisidir.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Header pinlerini lehimlerken tahtanın güç almadığından emin olun. Eğer brownout dedektörü ateşlemeye devam ediyorsa, sorun nadiren firmware'in kendisidir.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Header pinlerini lehimlerken tahtanın güç almadığından **emin olun**. Eğer brownout dedektörü ateşlemeye devam ediyorsa, sorun nadiren firmware'in kendisidir.
```

**Denetimin taslakta değiştirdikleri**

```diff
-Header pinlerini lehimlerken tahtanın güç almadığından emin olun. Eğer brownout dedektörü ateşlemeye devam ediyorsa, sorun nadiren firmware'in kendisidir.
+Header pinlerini lehimlerken tahtanın güç almadığından **emin olun**. Eğer brownout dedektörü ateşlemeye devam ediyorsa, sorun nadiren firmware'in kendisidir.
```

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): The source has 1 bold passage(s) (**not**) but the draft has 0. Mark the corresponding words in the translation as bold with **…**.
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (7)**

- [Wiktionary · çok anlamlı kelime] board: (noun) long, wide and thin piece of wood or other material → tahta; (noun) managing committee → heyet, kurul; (noun) short for blackboard, whiteboard, etc. → tahta; (noun) side of a ship → borda, sancak
- [Wiktionary · çok anlamlı kelime] power: (noun) ability to affect or influence → güç, kuvvet; (noun) electricity, electricity supply → güç; (noun) maths: product of equal factors → kuvvet, üs; (noun) people in charge of legal or political power → iktidar
- [Wiktionary · çok anlamlı kelime] solder: (noun) any of various alloys that are used to join small pieces of metal tog… → lehim; (verb) to join with solder → lehimlemek
- [Wiktionary · çok anlamlı kelime] keep: (verb) of livestock: to raise; to care for → bakmak; (verb) to continue → -ip durmak, devam etmek; (verb) to maintain possession of → saklamak, tutmak; (verb) to maintain the condition of; to preserve → saklamak
- [Wiktionary · çok anlamlı kelime] fire: (noun) damaging occurrence of fire → yangın; (noun) heater or stove used in place of real fire → ocak; (noun) oxidation reaction → ateş, od; (verb) intransitive: to shoot → ateş etmek
- [Tatoeba · örnek cümle] English: You'd better not do that while Tom is here. | Turkish: Tom buradayken bunu yapmasan iyi olur.
- [Tatoeba · örnek cümle] English: I wanted to make sure you were here. | Turkish: Burada olduğundan emin olmak istedim.

**Modele giden sözlük terimleri (2)**

- [kullanıcı sözlüğü] firmware: keep in English
- [kullanıcı sözlüğü] brownout: keep in English

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: board, rarely)

- board: evet — board [çok anlamlı kelime, Wiktionary]
- rarely: hayır

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 10.36 s | 3.65 s |
| Detaylı Çevir | 0.75 s | 21.65 s | 18.85 s | 41.24 s | 14.97 s |

## D5 · TR→EN

**Kaynak metin**

```text
Kartı yeniden flash'ladım ama watchdog yine tetiklendi. Hatayı log'lardan buldum: stack overflow. Kartın yanındaki kartvizitte yazan numarayı arayıp destek istedim.
```

**Hızlı çeviri** — ilk metin 4.37 s, toplam 11.23 s (bitti)

```text
I flashed the board again, but the watchdog was triggered again. I found the error in the logs: stack overflow. I called the number on the business card next to the board and asked for support.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
I flashed the board again, but the watchdog was triggered again. I found the error in the logs: stack overflow. I called the number on the business card next to the board and asked for support.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
I flashed the board again, but the watchdog was triggered again. I found the error in the log'lar: stack overflow. I called the number on the business card next to the board and asked for support.
```

**Denetimin taslakta değiştirdikleri**

```diff
-I flashed the board again, but the watchdog was triggered again. I found the error in the logs: stack overflow. I called the number on the business card next to the board and asked for support.
+I flashed the board again, but the watchdog was triggered again. I found the error in the log'lar: stack overflow. I called the number on the business card next to the board and asked for support.
```

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (6)**

- [Wiktionary · çok anlamlı kelime] kart: (adj) hoary, old; (noun) card
- [Wiktionary · çok anlamlı kelime] yeniden: (adv) anew; (adv) again
- [Wiktionary · çok anlamlı kelime] bulmak: (verb) to find; (verb) to discover; (verb) to invent; (verb) to reach (a place, a time)
- [Wiktionary · çok anlamlı kelime] yazmak: (verb) to write, write down, inscribe; (verb) to burn (CD, DVD); (verb) to compose; (verb) to enroll, register; to enlist, sign, record, note down
- [Wiktionary · çok anlamlı kelime] numara: (noun) number; (noun) shtick; (noun) stunt
- [Wiktionary · çok anlamlı kelime] aramak: (verb) to seek, to look for, to search; (verb) to phone, to telephone, to ring

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
| Hızlı çeviri | — | — | — | 11.23 s | 4.37 s |
| Detaylı Çevir | 1.08 s | 17.36 s | 17.06 s | 35.50 s | 11.49 s |

## D6 · EN→TR

**Kaynak metin**

```text
Dear Ms. Demir, we regret to inform you that the shipment scheduled for 3 December will be delayed by approximately two weeks. We would be grateful for your understanding.
```

**Hızlı çeviri** — ilk metin 3.10 s, toplam 9.67 s (bitti)

```text
Sayın Bayan Demir, 3 Aralık için planlanan sevkiyatın yaklaşık iki hafta gecikeceğini üzülerek bildirmek isteriz. Anlayışınız için teşekkür ederiz.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Sayın Bayan Demir, 3 Aralık için planlanan sevkiyatın yaklaşık iki hafta gecikeceğini üzülerek bildirmek isteriz. Anlayışınız için teşekkür ederiz.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Sayın Ms. Demir, 3 Aralık için planlanan sevkiyatın yaklaşık iki hafta gecikeceğini üzülerek bildirmek isteriz. Anlayışınız için minnettar oluruz.
```

**Denetimin taslakta değiştirdikleri**

```diff
-Sayın Bayan Demir, 3 Aralık için planlanan sevkiyatın yaklaşık iki hafta gecikeceğini üzülerek bildirmek isteriz. Anlayışınız için teşekkür ederiz.
+Sayın Ms. Demir, 3 Aralık için planlanan sevkiyatın yaklaşık iki hafta gecikeceğini üzülerek bildirmek isteriz. Anlayışınız için minnettar oluruz.
```

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (7)**

- [Wiktionary · çok anlamlı kelime] dear: (adj) an informal way of addressing the recipient in a letter's opening line → sevgili; (adj) formal way of addressing → sayın; (adj) loved; lovable → sevgili, sevimli
- [Wiktionary · çok anlamlı kelime] informal: (adj) language: reflecting everyday, non-ceremonious usage → senli benli, teklifsiz; (adj) not formal or ceremonious → teklifsiz; (adj) not in accord with the usual regulations → gayriresmî
- [Wiktionary · çok anlamlı kelime] shipment: (noun) load of goods → parti; (noun) the act of transporting goods → taşınma
- [Wiktionary · çok anlamlı kelime] delay: (noun) period of time before an event occurs; act of delaying → gecikme, rötar; (verb) to put off until a later time → ertelemek
- [Wiktionary · çok anlamlı kelime] weekly: (adj) happening once a week or every week → haftalık; (adv) every week → her hafta; (adv) once every week → haftada bir
- [Wiktionary · çok anlamlı kelime] would: (verb) indicating a possible (but not definite) future action or state → We sat on the bench; (verb) indicating an action in the past that happened repeatedly or commonly → In the winters; (verb) indicating an action or state that is conditional on another → daha sıcak olurduk!
- [Tatoeba · örnek cümle] English: Thank you for your understanding. | Turkish: Anlayışın için teşekkür ederim.

**Modele giden sözlük terimleri (0)**

- yok

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: Ms., regret to inform)

- Ms.: hayır
- regret to inform: hayır

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 9.67 s | 3.10 s |
| Detaylı Çevir | 0.81 s | 20.63 s | 16.91 s | 38.35 s | 14.56 s |

## D7 · TR→EN

**Kaynak metin**

```text
Güncelleme sırasında kartın gücünü **kesmeyin**; aksi halde bootloader bozulabilir ve kartı yeniden canlandırmak için UART üzerinden flash'lamanız gerekir.
```

**Hızlı çeviri** — ilk metin 4.04 s, toplam 10.12 s (bitti)

```text
Do not **cut** the power to the board during the update; otherwise, the bootloader may be corrupted and you will need to flash it via UART to revive the board.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Do not **cut** the power to the board during the update; otherwise, the bootloader may be corrupted and you will need to flash it via UART to revive the board.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Do not **cut** the power to the board during the update; otherwise, the bootloader may be corrupted and you will need to flash it via UART to revive the board.
```

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (6)**

- [Wiktionary · çok anlamlı kelime] sıra: (noun) row; (noun) order, sequence; (noun) turn; (noun) desk
- [Wiktionary · çok anlamlı kelime] güç: (adv) with difficulty, in a hard way; (adj) hard, difficult; (noun) strength, force; (noun) power
- [Wiktionary · çok anlamlı kelime] kesmek: (verb) to cut; (verb) to cut off, interrupt; (verb) to stop (talking, crying, etc.); (verb) to shave beard or moustache
- [Wiktionary · çok anlamlı kelime] akis: (noun) reverse; (noun) reflection, echo; (noun) opposite
- [Wiktionary · çok anlamlı kelime] hal: (noun) covered market; (noun) solution
- [Wiktionary · çok anlamlı kelime] bozulmak: (verb) to break, to stop working; (verb) to go bad, to spoil; (verb) to deteriorate; (verb) to sulk, to take offense

**Modele giden sözlük terimleri (3)**

- [kullanıcı sözlüğü] bootloader: keep in English
- [kullanıcı sözlüğü] UART: keep in English
- [kullanıcı sözlüğü] kart → board

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: kesmek, canlandırmak)

- kesmek: evet — kesmek [çok anlamlı kelime, Wiktionary]
- canlandırmak: hayır

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 10.12 s | 4.04 s |
| Detaylı Çevir | 0.55 s | 16.68 s | 15.64 s | 32.86 s | 10.99 s |

## D8 · EN→TR

**Kaynak metin**

```text
## Before you start

- Back up the NVS partition; you **cannot** recover it later.
- Don't cut corners on the power supply: a cheap adapter is often the root cause.

Once the board boots, keep an eye on the serial log for the first few minutes.
```

**Hızlı çeviri** — ilk metin 4.75 s, toplam 16.07 s (bitti)

```text
## Başlamadan önce

- NVS partition'ını yedekleyin; daha sonra geri **alamazsınız**.
- Güç kaynağı konusunda kestirme yollara başvurmayın: ucuz bir adaptör genellikle temel nedendir.

Kart açıldıktan sonra, ilk birkaç dakika boyunca seri log'u takip edin.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
## Başlamadan önce

- NVS partition'ını yedekleyin; daha sonra geri **alamazsınız**.
- Güç kaynağı konusunda kestirme yollara başvurmayın: ucuz bir adaptör genellikle temel nedendir.

Kart açıldıktan sonra, ilk birkaç dakika boyunca seri log'u gözlemleyin.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
## Başlamadan önce

- NVS partition'ını yedekleyin; daha sonra geri **alamazsınız**.
- Güç kaynağı konusunda kestirme yollara başvurmayın: ucuz bir adaptör genellikle temel nedendir.

Kart açıldıktan sonra, ilk birkaç dakika boyunca seri log'u gözlemleyin.
```

**Denetimin taslakta değiştirdikleri**

Değişiklik yok (taslak ile son çıktı aynı).

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (15)**

- [Wiktionary · kalıp/deyim] "cut corners" (verb): To bypass a prescribed route so as to gain competitive advantage or to circumvent traffic signals or other rules of the road.; To do a less-than-thorough or in… [idiomatic]
- [Wiktionary · kalıp/deyim] "keep an eye on" (verb): To watch and pay attention to, in case of misbehaviour or mishap. [idiomatic]
- [Wiktionary · kalıp/deyim] "keep an eye out" (verb): To watch for or look out for. [idiomatic]
- [Wiktionary · kalıp/deyim] "root cause" (noun): An initiating cause of a chain of events which leads to an outcome or effect of interest. [idiomatic]
- [Wiktionary · çok anlamlı kelime] start: (noun) beginning of an activity → başlangıç; (noun) beginning point of a race → start; (verb) to begin → başlamak
- [Wiktionary · çok anlamlı kelime] back: (adj) near the rear → arka; (adv) to or in a previous condition or place → geri; (noun) that which is farthest away from the front — see also rear → arka; (noun) the rear of body → sırt
- [Wiktionary · çok anlamlı kelime] cut: (adj) having been cut → kesik; (noun) act of cutting → kesme; (noun) act of dividing a deck of playing cards → kesmek; (noun) manner or style a garment is fashioned in → kesim
- [Wiktionary · çok anlamlı kelime] corner: (noun) intersection of two streets → kavşak; (noun) space in the angle between converging lines or walls → bucak, köşe
- [Wiktionary · çok anlamlı kelime] power: (noun) ability to affect or influence → güç, kuvvet; (noun) electricity, electricity supply → güç; (noun) maths: product of equal factors → kuvvet, üs; (noun) people in charge of legal or political power → iktidar
- [Wiktionary · çok anlamlı kelime] supply: (noun) act of supplying → arz, teklif; (noun) amount supplied → arz, zahire; (noun) provisions → zahire
- [Tatoeba · örnek cümle] English: I'll phone you before I start. | Turkish: Ayrılmadan önce seni ararım.
- [Tatoeba · örnek cümle] English: You start. | Turkish: Sen başla.
- [Tatoeba · örnek cümle] English: Could you keep an eye on my suitcase for a few minutes? | Turkish: Beş dakika için valizime göz kulak olabilir misin?
- [Tatoeba · örnek cümle] English: Can I call you back later? | Turkish: Seni sonra tekrar arayabilir miyim?
- [Tatoeba · örnek cümle] English: Can you call back later? | Turkish: Daha sonra tekrar arayabilir misin?

**Modele giden sözlük terimleri (3)**

- [kullanıcı sözlüğü] partition: keep in English
- [kullanıcı sözlüğü] NVS: keep in English
- [kullanıcı sözlüğü] power supply → güç kaynağı

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: cut corners, root cause, keep an eye on)

- cut corners: evet — cut corners [kalıp/deyim, Wiktionary]
- root cause: evet — root cause [kalıp/deyim, Wiktionary]
- keep an eye on: evet — keep an eye on [kalıp/deyim, Wiktionary]; Could you keep an eye on my suitcase for a few minutes? [örnek cümle, Tatoeba]

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 16.07 s | 4.75 s |
| Detaylı Çevir | 1.31 s | 34.65 s | 23.91 s | 59.88 s | 23.72 s |

## D9 · TR→EN

**Kaynak metin**

```text
Bu işi yarına bırakma, sonra dokuz doğurursun. Ayağımıza kadar gelmiş fırsatı tepmek olmaz; nabzına göre şerbet ver ama ipin ucunu da kaçırma.
```

**Hızlı çeviri** — ilk metin 3.75 s, toplam 13.67 s (bitti)

```text
Don't put off until tomorrow what you can do today, or you'll end up making excuses later. We shouldn't let an opportunity that has come all the way to us slip away; be tactful and adapt to the situation, but don't lose your grip on things either.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Don't put off today's work until tomorrow, or you'll end up with a mountain of trouble later. You shouldn't turn down an opportunity that's right at your doorstep; treat people according to their temperament, but don't overdo it.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Don't put off today's work until tomorrow, or you'll end up with a mountain of trouble later. You shouldn't turn down an opportunity that's right at your doorstep; treat people according to their temperament, but don't lose your grip on the situation.
```

**Denetimin taslakta değiştirdikleri**

```diff
-Don't put off today's work until tomorrow, or you'll end up with a mountain of trouble later. You shouldn't turn down an opportunity that's right at your doorstep; treat people according to their temperament, but don't overdo it.
+Don't put off today's work until tomorrow, or you'll end up with a mountain of trouble later. You shouldn't turn down an opportunity that's right at your doorstep; treat people according to their temperament, but don't lose your grip on the situation.
```

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (8)**

- [Wiktionary · çok anlamlı kelime] iş: (noun) work, task, deed; (noun) energy expended on moving an object, force times distance; (noun) job, employment; (noun) matter, affair, business, activity
- [Wiktionary · çok anlamlı kelime] yar: (noun) cliff, scarp, precipice; (noun) love, beloved
- [Wiktionary · çok anlamlı kelime] bırakmak: (verb) to let go, release, relinquish; (verb) to abandon, to leave; (verb) to leave, to cause or allow something to remain as available; (verb) to put, put down; to postpone, put off
- [Wiktionary · çok anlamlı kelime] sonra: (noun) aftermath; (adv) later, after, afterwards, post-; (adv) thereafter, subsequently, following; (adv) hereafter, in the future
- [Wiktionary · çok anlamlı kelime] doğurmak: (verb) to breed, to give birth; (verb) to give rise to
- [Wiktionary · çok anlamlı kelime] ayak: (noun) foot; (noun) pillar, tower; (noun) stand, footrest; (noun) leg (support of a furniture)
- [Tatoeba · örnek cümle] Turkish: Bugünün işini yarına bırakma. | English: A stitch in time saves nine.
- [Tatoeba · örnek cümle] Turkish: Bugünkü işini yarına bırakma. | English: Never put off till tomorrow what you can do today.

**Modele giden sözlük terimleri (0)**

- yok

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: dokuz doğurmak, ayağına kadar gelmek, nabzına göre şerbet vermek, ipin ucunu kaçırmak)

- dokuz doğurmak: hayır
- ayağına kadar gelmek: hayır
- nabzına göre şerbet vermek: hayır
- ipin ucunu kaçırmak: hayır

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 13.67 s | 3.75 s |
| Detaylı Çevir | 0.86 s | 23.16 s | 20.70 s | 44.72 s | 14.18 s |

## D10 · EN→TR

**Kaynak metin**

```text
Oh great, the build failed again. I'll look into it after lunch, but don't hold your breath — I've run out of ideas.
```

**Hızlı çeviri** — ilk metin 3.55 s, toplam 8.04 s (bitti)

```text
Harika, build yine başarısız oldu. Öğleden sonra bakacağım ama pek umut etme; fikirlerim tükendi.
```

**Detaylı Çevir — denetimden önceki taslak**

```text
Harika, build yine başarısız oldu. Öğle yemeğinden sonra bakacağım ama pek umut etme; fikirlerim tükendi.
```

**Detaylı Çevir — son çıktı** (bitti)

```text
Harika, build yine başarısız oldu. Öğle yemeğinden sonra bakacağım ama nefesini tutma; fikirlerim tükendi.
```

**Denetimin taslakta değiştirdikleri**

```diff
-Harika, build yine başarısız oldu. Öğle yemeğinden sonra bakacağım ama pek umut etme; fikirlerim tükendi.
+Harika, build yine başarısız oldu. Öğle yemeğinden sonra bakacağım ama nefesini tutma; fikirlerim tükendi.
```

**Kod denetiminin bulduğu biçim sorunları**

- Denetimden önce (modele bildirilen): yok
- Denetimden sonra (son çıktıda kalan): yok

**Modele giden bilgi kayıtları (11)**

- [Wiktionary · kalıp/deyim] "don't hold your breath" (phrase): Don't wait. Said cynically to suggest that what has just been mentioned is unlikely to happen soon or at all. [idiomatic]
- [Wiktionary · çok anlamlı kelime] great: (adj) very big, large scale → büyük, çok büyük; (noun) person of major significance, accomplishment or acclaim → ünlü
- [Wiktionary · çok anlamlı kelime] build: (noun) physique → çerçeve; (verb) (transitive) to form by combining materials or parts → inşa etmek, kurmak, yapmak
- [Wiktionary · çok anlamlı kelime] fail: (verb) cause to fail → sınıfta bırakmak; (verb) to receive one or more non-passing grades in academic pursuits → sınıfta kalmak
- [Wiktionary · çok anlamlı kelime] look: (noun) 1. action of looking → bakma, bakış; (noun) 2. physical appearance — see also aspect, appearance, image, air, dem… → görüntü, görünüm, görünüş; (noun) 3. facial expression — see also facial expression, expression, physio… → bakış; (verb) to appear, to seem — see also seem, look like → görünmek
- [Wiktionary · çok anlamlı kelime] breath: (noun) act or process of breathing → nefes, soluk; (noun) air expelled from the lungs → nefes; (noun) single act of breathing in and out → nefes
- [Wiktionary · çok anlamlı kelime] run: (noun) act of running → koşma, koşu; (verb) to move quickly on two feet → koşmak
- [Tatoeba · örnek cümle] English: Tom failed again. | Turkish: Tom yine başarısız oldu.
- [Tatoeba · örnek cümle] English: The peace talks failed again. | Turkish: Barış görüşmeleri yine başarısız oldu.
- [Tatoeba · örnek cümle] English: Don't hold your breath. | Turkish: Nefesini tutma.
- [Tatoeba · örnek cümle] English: I'll talk to you about it after lunch. | Turkish: Öğle yemeğinden sonra seninle o konuda konuşacağım.

**Modele giden sözlük terimleri (0)**

- yok

**Dikkat kelimeleri modele ulaştı mı** (Dikkat: oh great (alay), look into, don't hold your breath, run out of)

- oh great (alay): hayır
- look into: hayır
- don't hold your breath: evet — don't hold your breath [kalıp/deyim, Wiktionary]; Don't hold your breath. [örnek cümle, Tatoeba]
- run out of: hayır

**Süreler**

| | Arama | Çeviri | Denetim | Toplam | İlk metin |
|---|---|---|---|---|---|
| Hızlı çeviri | — | — | — | 8.04 s | 3.55 s |
| Detaylı Çevir | 0.73 s | 22.52 s | 14.72 s | 37.97 s | 17.93 s |

## Süre tablosu

| Test | Yön | Hızlı ilk metin | Hızlı toplam | Detaylı arama | Detaylı çeviri | Detaylı denetim | Detaylı toplam | Detaylı ilk metin |
|---|---|---|---|---|---|---|---|---|
| D1 | TR→EN | 3.54 s | 10.77 s | 0.94 s | 19.70 s | 16.65 s | 37.30 s | 13.96 s |
| D2 | TR→EN | 3.54 s | 11.91 s | 1.00 s | 19.80 s | 18.42 s | 39.22 s | 12.62 s |
| D3 | EN→TR | 3.75 s | 10.02 s | 0.76 s | 24.64 s | 15.55 s | 40.95 s | 19.53 s |
| D4 | EN→TR | 3.65 s | 10.36 s | 0.75 s | 21.65 s | 18.85 s | 41.24 s | 14.97 s |
| D5 | TR→EN | 4.37 s | 11.23 s | 1.08 s | 17.36 s | 17.06 s | 35.50 s | 11.49 s |
| D6 | EN→TR | 3.10 s | 9.67 s | 0.81 s | 20.63 s | 16.91 s | 38.35 s | 14.56 s |
| D7 | TR→EN | 4.04 s | 10.12 s | 0.55 s | 16.68 s | 15.64 s | 32.86 s | 10.99 s |
| D8 | EN→TR | 4.75 s | 16.07 s | 1.31 s | 34.65 s | 23.91 s | 59.88 s | 23.72 s |
| D9 | TR→EN | 3.75 s | 13.67 s | 0.86 s | 23.16 s | 20.70 s | 44.72 s | 14.18 s |
| D10 | EN→TR | 3.55 s | 8.04 s | 0.73 s | 22.52 s | 14.72 s | 37.97 s | 17.93 s |
