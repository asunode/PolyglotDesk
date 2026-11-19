"""Adım 4 ölçümü: hızlı çeviri (Cevirici) ve Detaylı Çevir (DetayliCevirici), uygulamanın gerçek yolu.

Kullanım: python3 doc/olcum/bench_v4.py <çıktı.json> [--mod hizli|detayli|ikisi] [test kimlikleri…]
Setler: test-seti-v1 (T1–T8), kontrol-seti-v1 (H1–H3), kontrol-seti-v2 (G1–G3).
Varsayılan ayarlar ve paketteki varsayılan sözlük kullanılır. Her çeviri boş önbellekli yeni bir
nesneyle çalışır; T4 her modda art arda iki kez çevrilir (T10).
"""

import argparse
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
from cevirmen.detayli import DetayliCevirici  # noqa: E402
from cevirmen.istem import sistem_istemi  # noqa: E402
from cevirmen.ollama import Ollama  # noqa: E402
from cevirmen.sozluk import VARSAYILAN, Sozluk  # noqa: E402

SETLER = ("test-seti-v1.md", "kontrol-seti-v1.md", "kontrol-seti-v2.md")


def testleri_oku() -> list[dict]:
    testler = []
    for ad in SETLER:
        metin = (KOK / "doc/olcum" / ad).read_text(encoding="utf-8")
        for m in re.finditer(r"^## ([THG]\d+) · (TR|EN)→(TR|EN)[^\n]*\n\n```text\n(.*?)\n```", metin, re.S | re.M):
            testler.append({"id": m[1], "kaynak": m[2].lower(), "hedef": m[3].lower(), "metin": m[4]})
    return testler


def bekle(sinyaller: dict):
    dongu = QEventLoop()
    sonuc = {}
    for ad, sinyal in sinyaller.items():
        sinyal.connect(lambda *a, ad=ad: (sonuc.setdefault("olay", (ad, a)), dongu.quit()))
    dongu.exec()
    return sonuc["olay"]


def main() -> None:
    app = QCoreApplication(sys.argv)
    ap = argparse.ArgumentParser()
    ap.add_argument("cikti", type=Path)
    ap.add_argument("--mod", default="ikisi", choices=["hizli", "detayli", "ikisi"])
    ap.add_argument("testler", nargs="*")
    a = ap.parse_args()
    ayar = dict(ayarlar.VARSAYILAN)
    ollama = Ollama(ayar)
    sozluk = Sozluk(VARSAYILAN)

    t = time.time()
    on = ollama.onden_yukle(sistem_istemi("tr", "en"))
    print("önden yükleme", round(time.time() - t, 1), bekle({"tamam": on.tamam, "hata": on.hata})[0], flush=True)

    def hizli(test: dict) -> dict:
        c = Cevirici(ollama, sozluk)
        t0 = time.time()
        c.baslat(test["metin"], test["kaynak"], test["hedef"])
        olay = bekle({"bitti": c.bitti, "hata": c.hata}) if c.calisiyor else ("bitti", ())
        return {"ilk_parca": round(c.ilk_parca_suresi or 0, 2), "toplam": round(time.time() - t0, 2),
                "parca": c.parca_sayisi, "durum": olay[0] if olay[0] == "bitti" else f"hata: {olay[1]}",
                "terimler": [str(x) for x in sozluk.eslesenler(test["metin"], test["kaynak"], test["hedef"])],
                "cikti": c.metin()}

    def detayli(test: dict) -> dict:
        d = DetayliCevirici(ollama, sozluk)
        t0 = time.time()
        d.baslat(test["metin"], test["kaynak"], test["hedef"])
        olay = bekle({"bitti": d.bitti, "hata": d.hata})
        parcalar = [s for s in d.sonuclar if s]
        return {
            "ilk_parca": round(d.ilk_parca_suresi or 0, 2), "toplam": round(time.time() - t0, 2),
            "sure": {a: round(sum(s.sure.get(a, 0) for s in parcalar), 2) for a in ("arama", "ceviri", "denetim")},
            "parca": d.parca_sayisi, "durum": olay[0] if olay[0] == "bitti" else f"hata: {olay[1]}",
            "cikti": d.metin(),
            "taslak": "\n\n".join(s.taslak for s in parcalar),
            "sorunlar_once": [p for s in parcalar for p in s.sorunlar_once],
            "sorunlar_sonra": [p for s in parcalar for p in s.sorunlar_sonra],
            "kayitlar": [{"tur": k.tur, "kaynak": k.kaynak, "lisans": k.lisans, "istem": k.istem,
                          "ayrinti": k.ayrinti} for k in d.tum_kayitlar()],
        }

    sonuclar = {}
    for test in testleri_oku():
        if a.testler and test["id"] not in a.testler:
            continue
        kayit = sonuclar.setdefault(test["id"], {})
        for mod, islev in (("hizli", hizli), ("detayli", detayli)):
            if a.mod not in (mod, "ikisi"):
                continue
            kayit[mod] = islev(test)
            r = kayit[mod]
            print(test["id"], mod, r["ilk_parca"], r["toplam"], r.get("sure", ""), r["durum"], flush=True)
            if test["id"] == "T4":
                sonuclar.setdefault("T4-2", {})[mod] = islev(test)
                r = sonuclar["T4-2"][mod]
                print("T4-2", mod, r["ilk_parca"], r["toplam"], r.get("sure", ""), r["durum"], flush=True)
        a.cikti.write_text(json.dumps({"ayarlar": ayar, "sonuclar": sonuclar}, ensure_ascii=False, indent=2), encoding="utf-8")
    app.quit()


if __name__ == "__main__":
    main()
