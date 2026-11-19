import json
import unittest

from cevirmen import denetim


def karar(*hatalar):
    return json.dumps({"has_errors": bool(hatalar), "errors": list(hatalar)})


def hata(tur, eski, yeni):
    return {"type": tur, "draft_text": eski, "corrected_text": yeni, "reason": "x"}


class DenetimTesti(unittest.TestCase):
    def test_hata_yoksa_taslak_aynen(self):
        u = denetim.uygula("Taslak metin.", "Draft text.", karar(), "en", "tr", set())
        self.assertEqual(u.metin, "Taslak metin.")
        self.assertEqual(u.uygulanan, [])

    def test_gecersiz_yanit_taslagi_korur(self):
        u = denetim.uygula("Taslak.", "Draft.", "bu json değil", "en", "tr", set())
        self.assertEqual(u.metin, "Taslak.")
        self.assertIsInstance(u.karar, str)

    def test_olumsuzluk_duzeltmesi_uygulanir(self):
        u = denetim.uygula("Acele edip bekleyelim.", "Let's not rush and wait.",
                           karar(hata("negation", "Acele edip", "Acele etmeyip")), "en", "tr", set(),
                           karsilik=lambda w: False)
        self.assertEqual(u.metin, "Acele etmeyip bekleyelim.")

    def test_ingilizceye_turkce_ek_geri_alinir(self):
        u = denetim.uygula("I found it in the logs.", "Log'lardan buldum.",
                           karar(hata("meaning", "the logs", "the log'lar")), "tr", "en", set())
        self.assertEqual(u.metin, "I found it in the logs.")
        self.assertIn("Türkçe kesme", u.geri_alinan[0]["neden"])

    def test_kaynak_kelimesi_cevrilmeden_eklenmez(self):
        u = denetim.uygula("Sayın Bayan Demir,", "Dear Ms. Demir,",
                           karar(hata("meaning", "Bayan", "Ms.")), "en", "tr", set())
        self.assertEqual(u.metin, "Sayın Bayan Demir,")
        self.assertTrue(u.geri_alinan)

    def test_unvan_hitap_degisikligi_hata_sayilmaz(self):
        for eski, yeni in (("Sayın Demir,", "Sayın Bayan Demir,"), ("Sayın Dr. Yılmaz", "Sayın Yılmaz"),
                           ("Ahmet Bey'e", "Ahmet'e")):
            u = denetim.uygula(f"{eski} rapor hazır.", "x", karar(hata("missing", eski, yeni)), "en", "tr", set(),
                               karsilik=lambda w: True)
            self.assertEqual(u.metin, f"{eski} rapor hazır.")
            self.assertIn("unvan", u.geri_alinan[0]["neden"])
        u = denetim.uygula("Dear Mr. Lee, thanks.", "x", karar(hata("addition", "Dear Mr. Lee", "Dear Lee")), "tr", "en", set())
        self.assertIn("unvan", u.geri_alinan[0]["neden"])

    def test_tekrarlanan_kelime_ve_fazla_olumsuzluk_geri_alinir(self):
        # kalın sorunu "negation" diye bildirilip "not" ikinci kez eklenirse
        u = denetim.uygula("Do not **start** it now.", "Şimdi **başlatmayın**.",
                           karar(hata("negation", "**start**", "not start")), "tr", "en", set())
        self.assertEqual(u.metin, "Do not **start** it now.")
        self.assertIn("tekrarlanan", u.geri_alinan[0]["neden"])
        u = denetim.uygula("Never start it now.", "Şimdi başlatmayın.",
                           karar(hata("negation", "start it", "do not start it")), "tr", "en", set())
        self.assertIn("olumsuzluk", u.geri_alinan[0]["neden"])
        # taslakta olumsuzluk eksikse olumsuzluk düzeltmesi uygulanır
        u = denetim.uygula("Start it now.", "Şimdi başlatmayın.",
                           karar(hata("negation", "Start it", "Do not start it")), "tr", "en", set())
        self.assertEqual(u.metin, "Do not start it now.")

    def test_bicim_duzeltmesi_kelime_degistiremez(self):
        u = denetim.uygula("Önyüklemede bağlamayın.", "Do **not** connect during boot.",
                           karar(hata("format", "bağlamayın", "**asla** bağlamayın")), "en", "tr", set())
        self.assertEqual(u.metin, "Önyüklemede bağlamayın.")
        u = denetim.uygula("Önyüklemede bağlamayın.", "Do **not** connect during boot.",
                           karar(hata("format", "bağlamayın", "**bağlamayın**")), "en", "tr", set())
        self.assertEqual(u.metin, "Önyüklemede **bağlamayın**.")

    def test_karsiligi_olmayan_kelime_geri_alinir(self):
        u = denetim.uygula("Sonuç iyiydi.", "The result was good.",
                           karar(hata("addition", "iyiydi", "kesinlikle mükemmeldi")), "en", "tr", set(),
                           karsilik=lambda w: w != "kesinlikle")
        self.assertEqual(u.metin, "Sonuç iyiydi.")
        self.assertIn("kesinlikle", u.geri_alinan[0]["neden"])

    def test_bulunamayan_parca(self):
        u = denetim.uygula("Bir metin.", "A text.", karar(hata("meaning", "yok böyle", "x")), "en", "tr", set())
        self.assertEqual(u.uygulanmayan[0]["neden"], "taslakta bulunamadı")


if __name__ == "__main__":
    unittest.main()
