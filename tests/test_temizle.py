import unittest

from cevirmen.temizle import temizle


class TemizleTesti(unittest.TestCase):
    def test_temiz_cikti_aynen_kalir(self):
        self.assertEqual(temizle("Biraz gecikeceğim.", "I'll be a bit late.", son=True), "Biraz gecikeceğim.")

    def test_giris_cumlesi_ayiklanir(self):
        self.assertEqual(temizle("İşte çeviri:\n\nMerhaba dünya.", "Hello world.", son=True), "Merhaba dünya.")
        self.assertEqual(temizle("Here is the translation: Hello world.", "Merhaba dünya.", son=True), "Hello world.")

    def test_akista_giris_netlesene_kadar_beklenir(self):
        self.assertEqual(temizle("Here is the", "Merhaba dünya.", son=False), "")
        self.assertEqual(temizle("Here is the translation:\nHel", "Merhaba dünya.", son=False), "Hel")
        self.assertEqual(temizle("Tabii ki gelirim.", "Of course I'll come.", son=False), "Tabii ki gelirim.")

    def test_kaynakta_ceviri_lafi_varsa_dokunulmaz(self):
        kaynak = "Translation: the act of translating."
        self.assertEqual(temizle("Çeviri: çevirme eylemi.", kaynak, son=True), "Çeviri: çevirme eylemi.")

    def test_saran_tirnak_ayiklanir(self):
        self.assertEqual(temizle('"Merhaba dünya."', "Hello world.", son=True), "Merhaba dünya.")
        self.assertEqual(temizle("“Hello", "Merhaba", son=False), "Hello")
        self.assertEqual(temizle('"Merhaba" dedi.', '"Hello" he said.', son=True), '"Merhaba" dedi.')

    def test_kaynakta_tirnak_varsa_dokunulmaz(self):
        kaynak = 'Annem yemeği yaptı, ben de "Eline sağlık" dedim.'
        cikti = '"My mom cooked, and I said \'Thank you.\'"'
        self.assertEqual(temizle(cikti, kaynak, son=True), cikti)

    def test_sondaki_not_ayiklanir(self):
        ham = "Hepimiz kararsızdık.\n\nNot: \"on the fence\" kararsız olmak demektir."
        self.assertEqual(temizle(ham, "We were all on the fence.", son=True), "Hepimiz kararsızdık.")
        ham = "We were undecided.\n(Note: literal translation.)"
        self.assertEqual(temizle(ham, "Kararsızdık.", son=True), "We were undecided.")

    def test_satir_sonlari_korunur(self):
        self.assertEqual(temizle("Birinci satır.\nİkinci satır.", "Line one.\nLine two.", son=True),
                         "Birinci satır.\nİkinci satır.")


if __name__ == "__main__":
    unittest.main()
