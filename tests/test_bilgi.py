import unittest
from unittest import mock

from cevirmen import bilgi


class BilgiTesti(unittest.TestCase):
    def test_kelimeler_turkce_kucultme_ve_kesme(self):
        self.assertEqual(bilgi._kelimeler("IŞIK reset'i İzmir'de", "tr"), ["ışık", "reset", "izmir"])

    def test_kalip_sirali_ve_yakin(self):
        anahtar = [{"gözü", "göz"}, {"ve"}, {"attı", "atmak"}, {"kitap"}]
        self.assertEqual(bilgi._sirali_yakin(["göz", "atmak"], anahtar), (0, 2))
        self.assertIsNone(bilgi._sirali_yakin(["atmak", "göz"], anahtar))
        uzak = [{"göz"}] + [{"x"}] * (bilgi.KALIP_PENCERESI + 1) + [{"atmak"}]
        self.assertIsNone(bilgi._sirali_yakin(["göz", "atmak"], uzak))
        # yer tutucu (None) atlanır: "keep an eye on something"
        self.assertEqual(bilgi._sirali_yakin(["keep", "eye", None], [{"keep"}, {"an"}, {"eye"}]), (0, 2))

    def test_en_olasi_madde(self):
        self.assertEqual(bilgi._en_olasi({"bitmek", "bit"}, {"bitmek": 900, "bit": 40}), {"bitmek"})
        self.assertEqual(bilgi._en_olasi({"ay", "ayı"}, {"ay": 100, "ayı": 60}), set())  # belirsiz
        self.assertEqual(bilgi._en_olasi({"kalem"}, {}), {"kalem"})
        self.assertEqual(bilgi._en_olasi({"a", "b"}, {}), set())

    def test_deyimde_hal_ve_iyelik(self):
        # "başa çıkmak": metinde "başa" uyar, "başına" (iyelikli) uymaz
        self.assertTrue(bilgi._hal_uyumlu("başa çıkmak", ["baş", "çıkmak"], [0, 1], ["başa", "çıkamadım"]))
        self.assertFalse(bilgi._hal_uyumlu("başa çıkmak", ["baş", "çıkmak"], [0, 1], ["başına", "çıktı"]))
        # "gözden geçirmek" ↔ "göze": ayrılma ≠ yönelme
        self.assertFalse(bilgi._hal_uyumlu("gözden geçirmek", ["göz", "geçirmek"], [0, 1], ["göze", "geçirdi"]))
        # iyelikli deyim başka kişiyle de uyar ("gözünü korkutmak" ↔ "gözümü")
        self.assertTrue(bilgi._hal_uyumlu("gözünü korkutmak", ["göz", "korkutmak"], [0, 1], ["gözümü", "korkuttu"]))
        # ünsüz yumuşaması ve ünlü düşmesi
        self.assertEqual(bilgi._ad_eki("kitabı", "kitap"), "ı")
        self.assertEqual(bilgi._ad_eki("ağzına", "ağız"), "ına")
        self.assertIn(("yönelme", True), bilgi._ad_cekimleri("ına"))
        self.assertEqual(bilgi._ad_cekimleri("a"), {("yönelme", False)})

    def test_islev_kalibi_ve_kullanim_disi(self):
        self.assertTrue(bilgi._islev_kalibi("for you"))
        self.assertTrue(bilgi._islev_kalibi("all's one"))
        self.assertFalse(bilgi._islev_kalibi("in line with"))
        self.assertEqual(bilgi._kullanim_disi_temizle(
            "Used other than figuratively or idiomatically: see is, it.; really? is that so?"), "really? is that so?")
        self.assertEqual(bilgi._kullanim_disi_temizle("Used other than figuratively or idiomatically: see for, you."), "")

    def test_baglanti_ortam_degiskeniyle(self):
        with mock.patch.dict("os.environ", {"POLYGLOTDESK_PG_HOST": "db.example", "POLYGLOTDESK_PG_PORT": "6543"}):
            a = bilgi.baglanti_ayarlari()
            self.assertEqual((a["pg_host"], str(a["pg_port"])), ("db.example", "6543"))
            self.assertIn("host=db.example", bilgi.dsn())
        self.assertNotIn("password", bilgi.dsn())

    def test_istem_blogu_gruplar(self):
        kayitlar = [bilgi.Kayit("ornek", "Tatoeba", "CC BY 2.0 FR", "a", "Turkish: a | English: b"),
                    bilgi.Kayit("kalip", "Wiktionary", "CC BY-SA 4.0", "x y", '"x y" (phrase): z')]
        blok = bilgi.istem_blogu(kayitlar)
        self.assertLess(blok.index("Idioms"), blok.index("Similar example"))
        self.assertEqual(bilgi.istem_blogu([]), "")

    def test_ulasilamazsa_anlasilir_hata(self):
        with mock.patch.dict("os.environ", {"POLYGLOTDESK_PG_PORT": "1", "POLYGLOTDESK_PG_DB": "x"}):
            with self.assertRaises(bilgi.BilgiHatasi) as e:
                bilgi.ara("Bir deneme cümlesi.", "tr", "en")
        self.assertIn("ulaşılamıyor", str(e.exception))


if __name__ == "__main__":
    unittest.main()
