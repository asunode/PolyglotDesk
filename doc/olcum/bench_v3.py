"""Adım 3 ölçümü: uygulamanın gerçek çeviri yolu (cevirmen.cevirici.Cevirici) ile.

Kullanım: python3 doc/olcum/bench_v3.py <çıktı.json> [test kimlikleri…]
Test seti: doc/olcum/test-seti-v1.md + doc/olcum/kontrol-seti-v1.md. Varsayılan
ayarlar ve paketteki varsayılan sözlük kullanılır (kullanıcının ayar dosyası okunmaz).
Her test yeni bir Cevirici ile (boş önbellekle) çalışır; T4 art arda iki kez (T10).
"""

import json
import re
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK))

from PySide6.QtCore import QCoreApplication, QEventLoop  # noqa: E402

from cevirmen import ayarlar  # noqa: E402
from cevirmen.cevirici import Cevirici  # noqa: E402
from cevirmen.istem import sistem_istemi  # noqa: E402
from cevirmen.ollama import Ollama  # noqa: E402
from cevirmen.sozluk import VARSAYILAN, Sozluk  # noqa: E402


def testleri_oku() -> list[dict]:
    testler = []
    for ad in ("test-seti-v1.md", "kontrol-seti-v1.md"):
        metin = (KOK / "doc/olcum" / ad).read_text(encoding="utf-8")
        for m in re.finditer(r"^## ([TH]\d+) · (TR|EN)→(TR|EN)[^\n]*\n\n```text\n(.*?)\n```", metin, re.S | re.M):
            testler.append({"id": m[1], "kaynak": m[2].lower(), "hedef": m[3].lower(), "metin": m[4]})
    return testler


def main() -> None:
    app = QCoreApplication(sys.argv)
    cikti = Path(sys.argv[1])
    secili = set(sys.argv[2:])
    ayar = dict(ayarlar.VARSAYILAN)
    ollama = Ollama(ayar)
    sozluk = Sozluk(VARSAYILAN)

    def bekle(sinyaller) -> str | None:
        dongu = QEventLoop()
        sonuc = {}
        for ad, sinyal in sinyaller.items():
            sinyal.connect(lambda *a, ad=ad: (sonuc.setdefault("olay", (ad, a)), dongu.quit()))
        dongu.exec()
        return sonuc["olay"]

    # Uygulamadaki gibi: model yüklenir, ortak istem önbelleğe alınır.
    t = time.time()
    on = ollama.onden_yukle(sistem_istemi("tr", "en"))
    olay = bekle({"tamam": on.tamam, "hata": on.hata})
    print("önden yükleme", round(time.time() - t, 1), olay[0], flush=True)

    sonuclar = {}

    def calistir(test: dict) -> dict:
        cevirici = Cevirici(ollama, sozluk)
        t0 = time.time()
        cevirici.baslat(test["metin"], test["kaynak"], test["hedef"])
        if cevirici.calisiyor:
            olay = bekle({"bitti": cevirici.bitti, "hata": cevirici.hata})
        else:
            olay = ("bitti", ())
        return {
            "ilk_parca": round(cevirici.ilk_parca_suresi or 0, 2),
            "toplam": round(time.time() - t0, 2),
            "parca": cevirici.parca_sayisi,
            "istek": cevirici.istek_sayisi,
            "durum": olay[0] if olay[0] == "bitti" else f"hata: {olay[1]}",
            "terimler": [str(x) for x in sozluk.eslesenler(test["metin"], test["kaynak"], test["hedef"])],
            "cikti": cevirici.metin(),
        }

    for test in testleri_oku():
        if secili and test["id"] not in secili:
            continue
        sonuclar[test["id"]] = calistir(test)
        r = sonuclar[test["id"]]
        print(test["id"], r["ilk_parca"], r["toplam"], r["parca"], r["durum"], flush=True)
        if test["id"] == "T4":
            sonuclar["T4-2"] = calistir(test)
            r = sonuclar["T4-2"]
            print("T4-2", r["ilk_parca"], r["toplam"], r["parca"], r["durum"], flush=True)
    cikti.write_text(json.dumps({"ayarlar": ayar, "sonuclar": sonuclar}, ensure_ascii=False, indent=2), encoding="utf-8")
    app.quit()


if __name__ == "__main__":
    main()
