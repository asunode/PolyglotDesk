import os
import tempfile
import time
import unittest
from pathlib import Path

from cevirmen.sozluk import Sozluk, Terim


class SozlukTesti(unittest.TestCase):
    def setUp(self):
        self.klasor = tempfile.TemporaryDirectory()
        self.yol = Path(self.klasor.name) / "sozluk.txt"
        self.sozluk = Sozluk(self.yol)
        self.sozluk.guncelle()  # varsayılan sözlük kopyalanır

    def tearDown(self):
        self.klasor.cleanup()

    def test_varsayilan_kopyalanir(self):
        self.assertTrue(self.yol.exists())

    def test_yalniz_metinde_gecenler(self):
        t = self.sozluk.eslesenler("The watchdog triggers a reset over UART.", "en", "tr")
        self.assertEqual([x.kaynak for x in t], ["watchdog", "UART"])

    def test_ingilizce_kaynakta_yalniz_cogul_eki(self):
        self.assertTrue(self.sozluk.eslesenler("Read the registers.", "en", "tr"))
        self.assertFalse(self.sozluk.eslesenler("Registered users only.", "en", "tr"))

    def test_turkce_ekli_bicimler_ve_cift_yonu(self):
        t = self.sozluk.eslesenler("Kartı deep sleep'e aldım, SD karta yazmıyor. Kayıtları inceledim, kaydı sildim.", "tr", "en")
        self.assertIn(Terim("deep sleep", None), t)
        self.assertNotIn(Terim("kart", "board"), t)  # "SD kart" da geçiyor: karar modelde
        self.assertIn(Terim("SD kart", "SD card"), t)
        self.assertIn(Terim("kayıtlar", "logs"), t)
        self.assertIn(Terim("kayıt", "log"), t)

    def test_baska_kelimeler_eslesmez(self):
        metin = "Watchdog açıkken kartal, kartvizit ve kayıtsız kaldı; kaydetmek gerekiyor."
        t = [x.kaynak for x in self.sozluk.eslesenler(metin, "tr", "en")]
        self.assertEqual(t, ["watchdog"])
        self.assertTrue(self.sozluk.eslesenler("Watchdog kartlarındaki hata.", "tr", "en")[-1] == Terim("kart", "board"))

    def test_gundelik_kelime_yalniz_teknik_baglamda(self):
        self.assertEqual(self.sozluk.eslesenler("Kartımı ve kayıtlarımı kaybettim.", "tr", "en"), [])
        t = self.sozluk.eslesenler("UART kartımı ve kayıtlarımı kaybettim.", "tr", "en")
        self.assertIn(Terim("kart", "board"), t)
        # Türkçe → İngilizce çifti ters yönde gönderilmez
        self.assertNotIn(Terim("kart", "board"), self.sozluk.eslesenler("Kartı aldım.", "en", "tr"))

    def test_ingilizce_turkce_teknik_bolum(self):
        t = self.sozluk.eslesenler("Flash the board after the bootloader starts.", "en", "tr")
        self.assertIn(Terim("board", "kart"), t)
        # teknik bağlam yoksa uygulanmaz
        self.assertNotIn(Terim("board", "kart"), self.sozluk.eslesenler("The board met today.", "en", "tr"))

    def test_ciftler_kendiliginden_ters_cevrilmez(self):
        # "kayıt = log" ters yönde "log → kayıt" olmaz; log İngilizce kalır
        t = self.sozluk.eslesenler("Check the boot log before you flash the firmware.", "en", "tr")
        self.assertIn(Terim("log", None), t)
        self.assertFalse([x for x in t if x.kaynak == "log" and x.hedef])
        self.yol.write_text("[Türkçe → İngilizce]\nçorba = soup\n", encoding="utf-8")
        st = self.yol.stat()
        os.utime(self.yol, ns=(st.st_atime_ns, st.st_mtime_ns + 1_000_000_000))
        self.sozluk.guncelle()
        self.assertEqual(self.sozluk.eslesenler("The soup is hot.", "en", "tr"), [])

    def test_uzun_terimin_icindeki_kisa_terim_gonderilmez(self):
        # yalnız "SD kart" içinde: kart gönderilmez
        t = self.sozluk.eslesenler("SD kartı firmware yazarken çıkardım.", "tr", "en")
        self.assertIn(Terim("SD kart", "SD card"), t)
        self.assertNotIn(Terim("kart", "board"), t)
        # hem içinde hem tek başına: yine gönderilmez (karar modelde)
        t = self.sozluk.eslesenler("SD kartı taktım ama kart tanınmadı, firmware eski.", "tr", "en")
        self.assertNotIn(Terim("kart", "board"), t)
        # yalnız tek başına: gönderilir
        t = self.sozluk.eslesenler("Kartı UART ile bağladım.", "tr", "en")
        self.assertIn(Terim("kart", "board"), t)
        # aynı kelimenin çekimi (kayıtlar / kayıt) iç içe sayılmaz
        t = self.sozluk.eslesenler("UART kayıtlarında hata var, kaydı sildim.", "tr", "en")
        self.assertIn(Terim("kayıtlar", "logs"), t)
        self.assertIn(Terim("kayıt", "log"), t)

    def test_gundelik_teknik_terim_tetiklemez(self):
        # Wi-Fi, HTTP gibi gündelik hayatta da geçen terimler teknik bağlam kurallarını açmaz
        t = self.sozluk.eslesenler("Wi-Fi şifresi kartın arkasında, kayıtlar resepsiyonda.", "tr", "en")
        self.assertIn(Terim("Wi-Fi", None), t)
        self.assertNotIn(Terim("kart", "board"), t)
        self.assertNotIn(Terim("kayıtlar", "logs"), t)
        self.assertFalse(self.sozluk.teknik_mi("Wi-Fi şifresi kartın arkasında.", "tr"))
        # donanım terimi açar
        self.assertTrue(self.sozluk.teknik_mi("Kartı USB'den çıkardım.", "tr"))
        self.assertIn(Terim("kart", "board"), self.sozluk.eslesenler("Kartı USB'den çıkardım.", "tr", "en"))

    def _yaz(self, metin):
        self.yol.write_text(metin, encoding="utf-8")
        st = self.yol.stat()
        os.utime(self.yol, ns=(st.st_atime_ns, st.st_mtime_ns + 1_000_000_000))
        self.sozluk.guncelle()

    def test_tetikleyici_listesi_duzenlenebilir(self):
        self._yaz("[Türkçe → İngilizce, teknik bağlamda]\nkart = board\n[Teknik bağlam tetikleyicileri]\nlehim\n")
        self.assertIn(Terim("kart", "board"), self.sozluk.eslesenler("Kartı lehimledim.", "tr", "en"))
        self.assertEqual(self.sozluk.eslesenler("Kartı USB'den çıkardım.", "tr", "en"), [])
        # bölümü olmayan eski sözlükte paketteki varsayılan tetikleyiciler kullanılır
        self._yaz("[Türkçe → İngilizce, teknik bağlamda]\nkart = board\n")
        self.assertEqual(self.sozluk.eslesenler("Kartı USB'den çıkardım.", "tr", "en"), [Terim("kart", "board")])

    def test_kisaltma_birebir(self):
        self.assertTrue(self.sozluk.eslesenler("OTA'yı başlat, GPIO9'a dokunma.", "tr", "en"))
        self.assertFalse(self.sozluk.eslesenler("Otamatik değil.", "tr", "en"))

    def test_duzenlenmemis_eski_varsayilan_guncellenir(self):
        import hashlib
        from cevirmen import sozluk as modul
        self.yol.write_text("eski", encoding="utf-8")
        modul.ESKI_VARSAYILANLAR.add(hashlib.sha256(b"eski").hexdigest())
        self.sozluk.hazirla()
        self.assertEqual(self.yol.read_text(encoding="utf-8"), modul.VARSAYILAN.read_text(encoding="utf-8"))
        self.yol.write_text("düzenlendi", encoding="utf-8")
        self.sozluk.hazirla()
        self.assertEqual(self.yol.read_text(encoding="utf-8"), "düzenlendi")

    def test_degisiklik_yeniden_baslatmadan_okunur(self):
        self.yol.write_text("[İngilizce kalsın]\nfoobar\n[Türkçe → İngilizce]\nçorba = soup\n", encoding="utf-8")
        st = self.yol.stat()
        os.utime(self.yol, ns=(st.st_atime_ns, st.st_mtime_ns + 1_000_000_000))
        self.sozluk.guncelle()
        self.assertEqual(self.sozluk.eslesenler("foobar ve çorbayı", "tr", "en"),
                         [Terim("foobar", None), Terim("çorba", "soup")])
        self.assertFalse(self.sozluk.eslesenler("watchdog", "en", "tr"))


if __name__ == "__main__":
    unittest.main()
