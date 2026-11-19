"""Kontrol seti v2'nin (G1–G3) v3 hızlı çeviri karşılığı (Adım 4'te, karşılaştırma için).

v3 hızlı yolunun istemi Adım 4'te değişmedi (istem.SURUM 3, sistem_istemi aynı). v3'ü birebir
kurmak için yalnız üç fark geri alınır:
- Adım 3 varsayılan sözlüğü: doc/olcum/sozluk_v3.txt (sha256 68fa459e…, kullanıcıya dağıtılan dosya)
- Adım 3 eşleştirmesi: Türkçe kaynakta terim kelime başına göre (önek) aranır
- Kodla boş satır düzeltmesi yok
Kullanım: python3 doc/olcum/bench_v3_kontrol2.py <çıktı.json>
"""
import json
import re
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK))
sys.path.insert(0, str(KOK / "doc/olcum"))

from PySide6.QtCore import QCoreApplication  # noqa: E402

import bench_v4  # noqa: E402
from cevirmen import ayarlar, cevirici, sozluk  # noqa: E402
from cevirmen.istem import sistem_istemi  # noqa: E402
from cevirmen.ollama import Ollama  # noqa: E402


def _desen_v3(terim: str, kaynak_dil: str) -> re.Pattern:
    govde = r"\s+".join(re.escape(p) for p in terim.split())
    if terim.upper() == terim and any(c.isalpha() for c in terim):
        return re.compile(rf"(?<!\w){govde}(?![^\W\d_])")
    if kaynak_dil == "tr":
        return re.compile(rf"(?<!\w){sozluk._kucult(govde)}")
    return re.compile(rf"(?<!\w){sozluk._kucult(govde)}(?:s|es|'s|’s)?(?!\w)")


sozluk._desen = _desen_v3
cevirici.bos_satirlari_duzelt = lambda kaynak, ceviri: ceviri

app = QCoreApplication(sys.argv)
ollama = Ollama(dict(ayarlar.VARSAYILAN))
sz = sozluk.Sozluk(KOK / "doc/olcum/sozluk_v3.txt")
on = ollama.onden_yukle(sistem_istemi("tr", "en"))
bench_v4.bekle({"tamam": on.tamam, "hata": on.hata})
sonuclar = {}
for test in bench_v4.testleri_oku():
    if not test["id"].startswith("G"):
        continue
    c = cevirici.Cevirici(ollama, sz)
    t0 = time.time()
    c.baslat(test["metin"], test["kaynak"], test["hedef"])
    olay = bench_v4.bekle({"bitti": c.bitti, "hata": c.hata})
    sonuclar[test["id"]] = {"ilk_parca": round(c.ilk_parca_suresi or 0, 2), "toplam": round(time.time() - t0, 2),
                            "durum": olay[0], "cikti": c.metin(),
                            "terimler": [str(x) for x in sz.eslesenler(test["metin"], test["kaynak"], test["hedef"])]}
    print(test["id"], sonuclar[test["id"]]["ilk_parca"], sonuclar[test["id"]]["toplam"], flush=True)
Path(sys.argv[1]).write_text(json.dumps({"sonuclar": sonuclar}, ensure_ascii=False, indent=2), encoding="utf-8")
