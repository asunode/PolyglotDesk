import unittest

from cevirmen.bicim import bos_satirlari_duzelt, denetle, kalin_kodla, kalin_sorunlari, kalin_uygula


class BicimTesti(unittest.TestCase):
    def test_kaynakta_olmayan_bos_satir_kalkar(self):
        kaynak = "Birinci cümle.\nİkinci cümle."
        self.assertEqual(bos_satirlari_duzelt(kaynak, "First sentence.\n\nSecond sentence."),
                         "First sentence.\nSecond sentence.")

    def test_bos_satirlar_kaynaktaki_yerine(self):
        kaynak = "Başlık\n\nBir.\nİki.\n\nSon."
        cevir = "Title\nOne.\n\nTwo.\nEnd."
        self.assertEqual(bos_satirlari_duzelt(kaynak, cevir), "Title\n\nOne.\nTwo.\n\nEnd.")

    def test_satir_sayisi_tutmazsa_dokunulmaz(self):
        kaynak = "Bir.\n\nİki.\nÜç."
        cevir = "One. Two.\n\nThree."
        self.assertEqual(bos_satirlari_duzelt(kaynak, cevir), cevir)

    def test_kaybolan_kalin_bildirilir(self):
        sorunlar = denetle("Do **not** touch it.", "Ona dokunmayın.")
        self.assertEqual(len(sorunlar), 1)
        self.assertIn("**not**", sorunlar[0])
        self.assertEqual(denetle("Do **not** touch it.", "Ona **dokunmayın**."), [])

    def test_kalin_yeri_olumsuzlukta(self):
        self.assertTrue(denetle("Güç **kesmeyin**.", "Do not **cut** the power.", "tr", "en"))
        self.assertEqual(denetle("Güç **kesmeyin**.", "Do **not** cut the power.", "tr", "en"), [])
        self.assertTrue(denetle("It is **not** powered.", "Güç almadığından **emin olun**.", "en", "tr"))
        self.assertEqual(denetle("It is **not** powered.", "Güç **almadığından** emin olun.", "en", "tr"), [])

    def test_kalin_kodla_olumsuzluk_sirasi(self):
        # kaynakta 1. olumsuzluk kalın → çevirideki 1. olumsuzluk kalın (2. olumsuzluk değil)
        self.assertEqual(kalin_kodla("Fişi **çekmeyin**; yoksa ayar kaydedilmeyebilir.",
                                     "Do not **unplug** it; otherwise the setting may not be saved.", "tr", "en"),
                         "Do **not** unplug it; otherwise the setting may not be saved.")
        self.assertEqual(kalin_kodla("The fan will **not** start.", "Fan çalışmaya başlamayacak.", "en", "tr"),
                         "Fan çalışmaya **başlamayacak**.")
        # olumsuzluk sayıları tutmazsa karar modele kalır
        self.assertIsNone(kalin_kodla("Fişi **çekmeyin**.", "Never, ever unplug it, do not.", "tr", "en"))
        # kalın parça olumsuzluk değilse kod karar vermez
        self.assertIsNone(kalin_kodla("Kapatmadan **önce** kaydedin.", "Save before closing.", "tr", "en"))

    def test_kalin_uygula_birebir_parca(self):
        kaynak = "Kapatmadan **önce** kaydedin."
        self.assertEqual(kalin_uygula("Save it before you close.", ["before"], kaynak, "tr", "en")[0],
                         "Save it **before** you close.")
        # parça çeviride birebir yoksa uygulanmaz (model metni yeniden yazamaz)
        self.assertIsNone(kalin_uygula("Save it before you close.", ["prior to"], kaynak, "tr", "en")[0])
        # kelimenin yarısı kalın olmaz
        self.assertIsNone(kalin_uygula("Save it beforehand.", ["before"], kaynak, "tr", "en")[0])
        # parça sayısı kaynaktaki kalın sayısına eşit olmalı
        self.assertIsNone(kalin_uygula("Save it before you close.", [], kaynak, "tr", "en")[0])
        # yanlış yerdeki kalın kaldırılıp yenisi konur
        self.assertEqual(kalin_uygula("**Save** it before you close.", ["before"], kaynak, "tr", "en")[0],
                         "Save it **before** you close.")

    def test_kalin_uygula_olumsuzluk_kurali(self):
        kaynak = "Güç **kesmeyin**."
        self.assertEqual(kalin_uygula("Do not cut the power.", ["not"], kaynak, "tr", "en")[0], "Do **not** cut the power.")
        self.assertIsNone(kalin_uygula("Do not cut the power.", ["cut"], kaynak, "tr", "en")[0])
        self.assertEqual(kalin_uygula("Cihaz kabul etmeyecek.", ["etmeyecek"], "It will **not** accept.", "en", "tr")[0],
                         "Cihaz kabul **etmeyecek**.")

    def test_turkce_olumsuz_fiil_ayrimi(self):
        self.assertTrue(kalin_sorunlari("It is **not** ready.", "Hazır **olmak**.", "en", "tr"))      # mastar
        self.assertTrue(kalin_sorunlari("It is **not** ready.", "Okumaya **başladı**.", "en", "tr"))  # -maya
        self.assertFalse(kalin_sorunlari("It is **not** ready.", "Hazır **değil**.", "en", "tr"))
        # ad-fiil ekleri olumsuzluk sayılmaz: güncellemesini, güncellemeyi; -masın, -meyin sayılır
        self.assertEqual(kalin_kodla("Güncellemesini **başlatmayın**; güncellemeyi sonra yapın.",
                                     "Do not **start** the update; do it later.", "tr", "en"),
                         "Do **not** start the update; do it later.")
        self.assertTrue(kalin_sorunlari("Do **not** go.", "**gelmesin**", "en", "tr") == [])
        self.assertTrue(kalin_sorunlari("Do **not** go.", "**gelmeyin**", "en", "tr") == [])

    def test_italik_ve_satir_sayisi(self):
        sorunlar = denetle("It is *very* old.\nKeep it.", "Çok eski. Sakla.")
        self.assertEqual(len(sorunlar), 2)

    def test_liste_isaretleri(self):
        self.assertTrue(denetle("- bir\n- iki", "one\ntwo"))
        self.assertEqual(denetle("- bir\n- iki", "- one\n- two"), [])


if __name__ == "__main__":
    unittest.main()
