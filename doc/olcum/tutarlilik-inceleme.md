# Hızlı çeviri tutarlılığı — inceleme (Adım 7, C6)

Soru: aynı metnin hızlı çevirisi neden farklı koşularda farklı çıkıyor (Adım 6'da D9 "nine babies", D2 "hailed"; Adım 4 `olcum-v4.md` "Tutarlılık bulgusu")? Tek başına çalıştırma ile Detaylı Çevir'den sonra çalıştırma arasındaki fark ölçüldü, Ollama'nın önbellek davranışı belgelendi.

- Betik: `doc/olcum/tutarlilik.py`; ham veri: `doc/olcum/tutarlilik-ham.json` (her istekte çıktı, süre, Ollama günlüğündeki `cached n_tokens`).
- Koşu: 2026-11-19 17:39–17:49 +03. gemma4:12b-it-qat, yalnız CPU, num_ctx 8192, temperature 0, seed 42; Ollama 0.30.7. Mesajlar uygulamanın hızlı çeviri mesajlarıyla aynı (`istem.sistem_istemi` + sözlük terimleri).
- Metinler: bu inceleme için yazılmış 4 metin (2 TR→EN, 2 EN→TR); test setlerinden değil.

## Koşullar

| Koşul | Hızlı çeviriden hemen önceki istek |
|---|---|
| tek | önden yükleme (uygulamanın açılıştaki isteği) |
| tekrar | aynı hızlı çeviri |
| detayli_sonra | Detaylı Çevir'in iki isteği (çeviri + JSON denetim) |
| baska_sonra | aynı yönde başka bir metnin hızlı çevirisi |

Her koşul iki kez denendi: olduğu gibi ("sınırsız") ve hızlı çeviriden hemen önce bir **sınır isteği** ile ("sınırlı"). Sınır isteği: sistem istemi ortak kurallar (`istem.ORTAK`) + `"\n\n#"`, kullanıcı mesajı ".", tek token üretir. Bu istem bütün uygulama istemleriyle ortak kuralların hemen ardından ayrılır.

## Sonuç

| Metin | Sınırsız: 4 koşulda farklı çıktı | Sınırlı: 4 koşulda farklı çıktı | Sınırlı çıktı = sınırsız "tek" | Hızlı çeviri ort. | Sınır isteği ort. |
|---|---|---|---|---|---|
| TR→EN 1 | **2** (detayli_sonra farklı) | 1 | evet | 7.03 s | 2.03 s |
| TR→EN 2 | 1 | 1 | evet | 6.43 s | 1.93 s |
| EN→TR 1 | 1 | 1 | evet | 8.71 s | 2.02 s |
| EN→TR 2 | 1 | 1 | evet | 6.97 s | 1.94 s |

TR→EN 1'de Detaylı Çevir'den sonra: "…out of town; **nevertheless, I will send** the report this evening." Diğer üç koşulda: "…out of town; **I will still send** the report this evening."

## Ollama'nın önbellek davranışı (gözlem)

- Ollama tek yuva kullanıyor (günlükte `slot id 0`); her istek, önbellekteki önceki istemle ortak başlangıcın bir kısmını yeniden kullanıp kalanını işliyor. Günlük satırı: `cached n_tokens = N, memory_seq_rm [N, end)`.
- Yeniden kullanılan uzunluk ortak başlangıcın tamamı değil, birkaç sabit noktadan biri: ölçümde 597, 598, 610, 614, 615, 621 (istem 642–662 token). Aynı istem hemen tekrarlansa bile ("tekrar") önbellekten 597 ya da 614 token kullanıldı, istemin geri kalanı yeniden işlendi. Bunun nedeni gemma modellerinin kayan pencere dikkati (sliding window attention): önbellek her noktadan değil, yalnız kaydedilmiş ara noktalardan devam ettirilebiliyor. Her istekte ikinci bir satır daha görülüyor (istem uzunluğunun 4 eksiği): istemin son birkaç tokeni ayrı işleniyor.
- Devam noktası bir önceki isteğe bağlı: önden yüklemeden sonra 615/621 (yön satırına kadar ortak), başka bir hızlı çeviriden sonra 597, Detaylı Çevir'den sonra 598 (Detaylı istemi ortak kurallardan sonraki "Additional rules" satırında ayrılıyor).
- Devam noktası değişince istemin kalan kısmı farklı bir parti (batch) bölünmesiyle işleniyor; kayan nokta sonuçları çok küçük farklarla değişiyor. temperature 0'da her adımda en olası token seçildiği için, iki aday tokenin olasılığı çok yakın olduğu bir yerde seçim değişebiliyor ve çıktı o noktadan sonra ayrılıyor (TR→EN 1: "I will still" ↔ "nevertheless, I will"). Seed bu farkı gidermez; seed yalnız örnekleme rastgeleliğini sabitler.
- Sınır isteği gönderilince hızlı çeviri isteği her koşulda 597. tokenden devam etti ve 16 koşunun hepsinde aynı metin aynı çeviriyi verdi.

## Seçenekler ve maliyetleri

| Seçenek | Ek süre | Etkisi |
|---|---|---|
| A. Hiçbir şey yapmamak | 0 | Çıktı bir önceki isteğe bağlı kalır (ölçümde 4 metnin 1'inde Detaylı sonrası farklı). |
| B. Her hızlı çeviri isteğinden (her parçadan) önce sınır isteği | ~2.0 s / istek (1.8–2.1 s; hızlı çevirinin %25–30'u); süreyi büyük ölçüde Ollama'nın her istekteki ~1.2 s sabit yükleme süresi oluşturuyor | Ölçümde tam tutarlılık (16/16). |
| C. Sınır isteğini yalnız önbellek başka türden bir istekle (Detaylı çeviri/denetim, kalın yazı isteği) değiştiğinde göndermek; önden yüklemeyi sınır istemiyle yapmak | Normal hızlı çeviride 0; Detaylı ya da kalın yazı isteğinden sonraki ilk hızlı çeviride ~2 s | Ölçülen farkın kaynağı olan durumu (Detaylı sonrası) giderir. Hızlı çeviriden sonra gelen hızlı çeviride devam noktası ölçümde 4/4 kez 597'ydi; her geçmiş için kanıtlanmış değil. Aynı istemin tekrarı (bir kez 614) uygulamada oluşmaz: aynı parça bellekteki parça önbelleğinden gelir. |
| D. Hızlı çeviri sonuçlarını diske kaydetmek (oturumlar arası önbellek) | 0 | Aynı metnin tekrarını sabitler; ilk çevirinin geçmişe bağlılığını gidermez. |
| E. Önbelleği hiç kullanmamak | Her istekte ~640 tokenin baştan işlenmesi (ölçülmedi; ölçümdeki ~40–60 tokenlik kısım 1.3–2.1 s sürdüğüne göre on saniyeler mertebesinde) | Ollama API'sinde önbelleği kapatan bir ayar yok; ancak istemin başını her istekte değiştirerek yapılabilir. Hızlı çeviri amacına aykırı. |
| F. Ollama ayarı (OLLAMA_NUM_PARALLEL vb.) | — | Etkisiz: zaten tek yuva var; devam noktaları modelin dikkat yapısından geliyor. |

## Uygulanan: C

Temiz ve ucuz olduğu için C uygulandı (Adım 7):

- `istem.sinir_istemi()`: ortak kurallar + `"\n\n#"`.
- `Ollama.onbellek_sinirda`: son istek önden yükleme, sınır isteği ya da hızlı çeviriyse True; Detaylı çeviri/denetim ya da kalın yazı isteğinden sonra False.
- `Cevirici._istek_gonder`: bayrak False ise önce sınır isteği (`Ollama.sinir`), sonra hızlı çeviri isteği.
- Önden yükleme (`arayuz._onden_yukle`) artık `sinir_istemi()` ile yapılıyor; açılıştaki ilk hızlı çeviri de 597'den devam eder (ilk çeviri süresi değişmez: ortak kurallar yine önbellekte).

Kendi cümlelerimle uygulama sınıfları üzerinden denendi: hızlı → Detaylı → hızlı (başka metin) → hızlı (başka metin) sırasında sınır isteği yalnız Detaylı'dan sonraki ilk hızlı çeviride gönderildi (hızlı çeviri 8.2 s, diğerleri 5.9 ve 6.4 s).

B (her istekte sınır) daha kesin ama hızlı çeviriye her parçada ~2 s ekler; gerekirse `Cevirici._istek_gonder`'de koşul kaldırılarak açılabilir.
