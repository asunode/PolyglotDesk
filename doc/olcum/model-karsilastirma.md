# Model ölçümü — ham çıktı (2026-11-18 19:33 +03)

Betik: Ollama /api/chat, stream, think=false, temperature=0.2, varsayılan GPU yerleşimi (Vulkan, kısmi). "ilk" = ilk boş olmayan parçaya kadar geçen süre (model önceden yüklü).

```

######## gemma3:4b  yükleme=9.1s  GPU payı=%31
--- tr->en günlük: ilk=2.86s toplam=4.23s
I'll go to the market early tomorrow morning to buy bread and milk, and then I’ll drop off the children at school.
--- tr->en teknik: ilk=2.61s toplam=5.36s
The application connects to the server on the local network via HTTP and processes the response in real-time. If the connection times out, the client retries three times; with each retry, the waiting time doubles. Data cached in the cache is stored encrypted on disk.
--- tr->en deyim: ilk=2.55s toplam=3.95s
Everyone was saying whatever came to their mouths at the meeting, and I felt my patience running out; luckily, the manager smoothed things over.
--- en->tr günlük: ilk=2.73s toplam=3.87s
Biraz geç kalıyorum, lütfen yerimi ayırır ve bir kahve de sipariş verir misin?
--- en->tr teknik: ilk=2.41s toplam=7.13s
Çöp toplayıcı, artık erişilemeyen nesneler için düzenli aralıklarla yığın (heap) taraması yapar ve belleğini geri kazanır. Bekleme sürelerini azaltmak için modern çalışma zamanları (runtimes), çoğu nesnenin genç olduğunu varsayan nesil koleksiyonunu (generational collection) kullanır. Geliştiriciler, yapılandırma bayrakları aracılığıyla yığın boyutunu ayarlayabilirler.
--- en->tr deyim: ilk=2.60s toplam=3.95s
Hepimiz yeni plana karşıydık, ama yönetici sonunda bütçe kesintilerini açığa çıkarınca son damla oldu.

######## llama3.1:8b  yükleme=5.6s  GPU payı=%42
--- tr->en günlük: ilk=2.71s toplam=4.92s
Tomorrow morning early I'll go to the market and buy bread and milk, then I'll drop off the children at school.
--- tr->en teknik: ilk=2.69s toplam=7.34s
The application connects to the server on the local network via HTTP and processes the response in a streaming manner. If the connection times out, the client attempts three retries; each attempt increases the waiting time by twice. Data stored in the cache is encrypted and saved to disk.
--- tr->en deyim: ilk=2.24s toplam=4.91s
At the meeting everyone said what was on their mind, and I felt my patience wearing thin; fortunately the manager managed to sweeten things over.
--- en->tr günlük: ilk=2.53s toplam=5.89s
Biraz geç kaldım, lütfen bana bir yer ayırmayı ve bir kahve sipariş etmenizi istirham ederim.
--- en->tr teknik: ilk=2.35s toplam=8.51s
Atık toplatıcı, düzenli olarak bellekte ulaşılamayan objeleri tarar ve belleklerini geri alır. Hafıza kesintilerini azaltmak için modern çalışma zamanları nesiller arası toplama kullanır, çoğu objenin genç öldüğünü varsayar. Geliştiriciler bellek boyutunu yapılandırma bayraklarıyla ayarlar.
--- en->tr deyim: ilk=2.18s toplam=6.19s
Yeni planla ilgili hepimiz bir nebze de olsa tereddüt içindeydik ama yönetici nihayet bütçe kesintilerini açıkladığında, son çubuk oldu.

######## gemma4:12b-it-qat  yükleme=10.4s  GPU payı=%23
--- tr->en günlük: ilk=5.36s toplam=9.34s
I will go to the market early tomorrow morning to get bread and milk, and then I will drop the children off at school.
--- tr->en teknik: ilk=5.13s toplam=13.30s
The application connects to the server on the local network via HTTP and processes the response in a stream. If the connection times out, the client retries three times; the wait time doubles with each attempt. Cached data is stored on the disk in an encrypted format.
--- tr->en deyim: ilk=4.58s toplam=8.59s
Everyone said whatever came to mind at the meeting, and I felt my patience running out; fortunately, the manager smoothed things over.
--- en->tr günlük: ilk=5.09s toplam=8.80s
Biraz gecikeceğim, bu yüzden lütfen bana bir yer ayırıp bir kahve sipariş eder misin?
--- en->tr teknik: ilk=4.90s toplam=19.67s
Çöp toplayıcı (garbage collector), artık erişilemeyen nesneleri tespit etmek için periyodik olarak yığını tarar ve bunların belleğini geri kazanır. Duraklama sürelerini azaltmak için modern çalışma zamanları, çoğu nesnenin kısa ömürlü olduğunu varsayan nesil tabanlı toplama yöntemini kullanır. Geliştiriciler, yapılandırma bayrakları aracılığıyla yığın boyutunu optimize edebilirler.
--- en->tr deyim: ilk=5.18s toplam=9.85s
Yeni plan konusunda hepimiz kararsızdık ama müdür sonunda bütçe kesintilerini açıkladığında artık sabrımız taştı.

######## qwen2.5-coder:7b  yükleme=5.5s  GPU payı=%44
--- tr->en günlük: ilk=2.26s toplam=4.46s
I'll go to the market early tomorrow morning to buy bread and milk, then I'll drop off my children at school.
--- tr->en teknik: ilk=2.29s toplam=7.02s
The application connects to the server on the local network via HTTP and processes the response in a stream. If the connection times out, the client retries three times; with each attempt, the wait time doubles. The data cached in memory is stored encrypted on the disk.
--- tr->en deyim: ilk=1.99s toplam=4.78s
Everyone said what came to mind at the meeting, and I felt my patience wearing thin; well, the boss tied it up with a bow.
--- en->tr günlük: ilk=2.34s toplam=5.49s
Ben biraz geçiyorum, bu yüzden lütfen bir yere bana yer ayıracak ve kahve sipariş edin.
--- en->tr teknik: ilk=1.88s toplam=13.13s
Atık toplayıcı, zaman içinde atık alanını tarama yapar ve erişilemeyen nesneleri bulur ve hafızalarını geri alır. Duraklama sürelerini azaltmak için, modern çalışma zamanları generasyonel toplama kullanır, bu da çoğu nesne genç yaşlardan ölüyorduğunu varsayar. Geliştiriciler, yapılandırma bayraklarını aracılığıyla atık alanının boyutunu ayarlayabilirler.
--- en->tr deyim: ilk=1.97s toplam=6.28s
Tümüne yeni plan hakkında duydugumuz benimseyişliydi ama yöneticinin bütçe kesintilerini açıklamasını sonunda bilekten kurtulduk.

######## qwen2.5-coder:14b  yükleme=8.2s  GPU payı=%25
--- tr->en günlük: ilk=4.77s toplam=9.16s
I'll go to the market early tomorrow morning to buy bread and milk, then I'll drop the kids off at school.
--- tr->en teknik: ilk=4.67s toplam=13.65s
The application connects to the local server via HTTP and processes the response in a streaming fashion. If the connection times out, the client retries three times; with each attempt, the wait time doubles. Data stored in the cache is encrypted and saved on disk.
--- tr->en deyim: ilk=4.05s toplam=10.02s
At the meeting, everyone said what was on their minds, and I felt my patience wearing thin; at least the job of being a manager is sweetened by that.
--- en->tr günlük: ilk=4.50s toplam=10.23s
biraz gecikeceğim için lütfen bana bir koltuk ayır ve benim için bir kahve sipariş et?
--- en->tr teknik: ilk=3.92s toplam=19.30s
Atık toplayıcı düzenli olarak erişilemeyen nesneleri için belleği serbest bırakır. Duraklama sürelerini azaltmak için modern çalışma zamanları, çoğu nesnenin genççe ölmesini varsayan nesil tabanlı toplama kullanır. Geliştiriciler yapılandırma bayraklarını kullanarak yığın boyutunu ayarlayabilirler.
--- en->tr deyim: ilk=3.88s toplam=12.08s
Yeni plan hakkında hepsi kafamızda dengede duruyordu, ama yöneticinin nihayetinde bütçe kesintilerini açıklayışında, son kelepçeydi.
```
