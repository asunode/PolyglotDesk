import unittest

from cevirmen import parcala as p


def birlestir(parcalar):
    return "".join(x.icerik + x.ayrac for x in parcalar)


class ParcalaTesti(unittest.TestCase):
    def test_birlesim_kaynagi_birebir_verir(self):
        ornekler = [
            "Tek satır.",
            "\n\nBaşta boşluk.\n\n\nSonda boşluk.\n\n",
            "Paragraf.\n```\nkod\n\nkod2\n```\nSonra.\n",
            "## Başlık\n\n1. bir\n2. iki\n   girinti\n\n> alıntı\n> devam",
        ]
        for metin in ornekler:
            self.assertEqual(birlestir(p.parcala(metin)), metin, metin)

    def test_kisa_paragraflar_birlesir_uzunlar_ayrilir(self):
        uzun = "Bu bir cümle. " * 40  # ~560 karakter
        metin = f"Kısa bir.\n\nKısa iki.\n\n{uzun.strip()}\n\n{uzun.strip()}"
        parcalar = p.parcala(metin)
        self.assertEqual(len(parcalar), 2)
        self.assertTrue(parcalar[0].icerik.startswith("Kısa bir.\n\nKısa iki.\n\nBu bir cümle."))

    def test_kod_blogu_cevrilmez_ve_bolunmez(self):
        metin = "Açıklama.\n\n```\na = 1\n\nb = 2\n```\n\nSon."
        parcalar = p.parcala(metin)
        kod = [x for x in parcalar if not x.cevrilsin and x.icerik]
        self.assertEqual(len(kod), 1)
        self.assertEqual(kod[0].icerik, "```\na = 1\n\nb = 2\n```")

    def test_liste_bolunmez(self):
        liste = "\n".join(f"{i}. Madde numarası {i} için açıklama metni." for i in range(1, 40))
        parcalar = p.parcala("Giriş.\n\n" + liste)
        self.assertTrue(any(liste in x.icerik for x in parcalar))

    def test_cok_uzun_paragraf_cumleden_bolunur(self):
        metin = " ".join(f"Cümle numarası {i} burada bitiyor." for i in range(200))
        parcalar = p.parcala(metin)
        self.assertGreater(len(parcalar), 1)
        self.assertTrue(all(len(x.icerik) <= p.EN_COK for x in parcalar))
        self.assertTrue(all(x.icerik.endswith(".") for x in parcalar))
        self.assertEqual(birlestir(parcalar), metin)


if __name__ == "__main__":
    unittest.main()
