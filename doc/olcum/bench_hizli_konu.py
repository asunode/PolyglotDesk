"""Adım 8: hızlı çeviri konu testi v1 — yalnız hızlı çeviri, iki koşu (ham kayıt).

Kullanım:
    python3 doc/olcum/bench_hizli_konu.py calistir doc/olcum/hizli-konu-testi-v1-ham.json
    python3 doc/olcum/bench_hizli_konu.py rapor doc/olcum/hizli-konu-testi-v1-ham.json doc/olcum/hizli-konu-testi-v1-sonuc.md

Uygulamanın hızlı çeviri yolu (`Cevirici`), varsayılan ayarlar (yalnız CPU), paketteki varsayılan sözlük.
Açılıştaki gibi model önden yüklenir (`istem.sinir_istemi`). 1. koşu K1 → E12, 2. koşu E12 → K1.
Her koşu yeni bir `Cevirici` nesnesiyle yapılır: aynı nesne 2. koşuda parçaları bellekteki önbellekten
verirdi (uygulamada aynı metin yeniden çevrilmez). Ollama nesnesi ve modelin önbelleği iki koşuda ortaktır.
"""

import difflib
import json
import re
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK))
SET = KOK / "doc/olcum/hizli-konu-seti-v1.md"


def testleri_oku() -> list[dict]:
    desen = r"^## ([KE]\d+) · (TR|EN)→(TR|EN) · ([^\n]*)\n\n```text\n(.*?)\n```\n\nDikkat: ([^\n]*)"
    return [{"id": m[1], "kaynak": m[2].lower(), "hedef": m[3].lower(), "konu": m[4], "metin": m[5], "dikkat": m[6]}
            for m in re.finditer(desen, SET.read_text(encoding="utf-8"), re.S | re.M)]


def calistir(cikti: Path) -> None:
    from PySide6.QtCore import QCoreApplication, QEventLoop

    from cevirmen import ayarlar
    from cevirmen.cevirici import Cevirici
    from cevirmen.istem import sinir_istemi
    from cevirmen.ollama import Ollama
    from cevirmen.sozluk import VARSAYILAN, Sozluk

    app = QCoreApplication(sys.argv)

    def bekle(sinyaller: dict):
        dongu = QEventLoop()
        sonuc = {}
        for ad, sinyal in sinyaller.items():
            sinyal.connect(lambda *a, ad=ad: (sonuc.setdefault("olay", (ad, a)), dongu.quit()))
        dongu.exec()
        return sonuc["olay"]

    ayar = dict(ayarlar.VARSAYILAN)
    ollama = Ollama(ayar)
    sozluk = Sozluk(VARSAYILAN)
    on = ollama.onden_yukle(sinir_istemi())
    print("önden yükleme", bekle({"tamam": on.tamam, "hata": on.hata})[0], flush=True)
    testler = testleri_oku()
    kayit = {"baslangic": time.strftime("%Y-%m-%d %H:%M:%S %z"), "ayarlar": ayar, "testler": testler, "kosular": {}}
    for kosu, sira in (("1", testler), ("2", list(reversed(testler)))):
        hizli = Cevirici(ollama, sozluk)
        kayit["kosular"][kosu] = {}
        for test in sira:
            t0 = time.time()
            hizli.baslat(test["metin"], test["kaynak"], test["hedef"])
            olay = bekle({"bitti": hizli.bitti, "hata": hizli.hata}) if hizli.calisiyor else ("bitti", ())
            kayit["kosular"][kosu][test["id"]] = {
                "zaman": time.strftime("%H:%M:%S"), "ilk_metin": round(hizli.ilk_parca_suresi or 0, 2),
                "toplam": round(time.time() - t0, 2), "durum": olay[0] if olay[0] == "bitti" else f"hata: {olay[1]}",
                "cikti": hizli.metin(), "parca_sayisi": hizli.parca_sayisi,
                "terimler": [str(x) for x in sozluk.eslesenler(test["metin"], test["kaynak"], test["hedef"])],
                "kalin_istegi": hizli.kalin_istegi, "kalin": list(hizli.kalin_kaydi), "sinir_istegi": hizli.sinir_istegi}
            print(kosu, test["id"], kayit["kosular"][kosu][test["id"]]["toplam"], olay[0], flush=True)
            cikti.write_text(json.dumps(kayit, ensure_ascii=False, indent=2), encoding="utf-8")
    kayit["bitis"] = time.strftime("%Y-%m-%d %H:%M:%S %z")
    cikti.write_text(json.dumps(kayit, ensure_ascii=False, indent=2), encoding="utf-8")
    app.quit()


def _blok(metin: str) -> str:
    return "```text\n" + metin + "\n```"


def _not(r: dict) -> str:
    notlar = []
    if r["kalin"]:
        notlar.append(f"kalın yazı düzeltmesi (ek istek: {r['kalin_istegi']}): " + " / ".join(r["kalin"]))
    if r["sinir_istegi"]:
        notlar.append(f"sınır isteği: {r['sinir_istegi']}")
    return "; ".join(notlar) or "yok"


def rapor(ham: Path, hedef: Path) -> None:
    v = json.loads(ham.read_text(encoding="utf-8"))
    k1, k2 = v["kosular"]["1"], v["kosular"]["2"]
    L = ["# Hızlı çeviri konu testi v1 — sonuçlar (ham kayıt)", "",
         f"Set: `doc/olcum/hizli-konu-seti-v1.md` (K1–K12 TR→EN, E1–E12 EN→TR). Betik: `doc/olcum/bench_hizli_konu.py`. "
         f"Ham veri: `doc/olcum/{ham.name}`.",
         f"Koşu: {v['baslangic']} – {v.get('bitis', '?')}. Model {v['ayarlar']['model']}, yalnız CPU (num_gpu 0), num_ctx 8192, "
         "temperature 0, seed 42. Yalnız hızlı çeviri: uygulamanın çeviri yolu (`Cevirici`), paketteki varsayılan sözlük; "
         "açılıştaki gibi model önden yüklendi (sınır istemiyle). 1. koşu K1 → E12, 2. koşu E12 → K1; her koşu yeni bir "
         "`Cevirici` nesnesiyle (aynı nesne 2. koşuda parçaları bellekteki önbellekten verirdi). Yön her metinde setteki gibi.",
         "",
         "Notlar:",
         "- Bütün çıktılar ham kayıttan birebir alınmıştır; düzeltilmemiş, kısaltılmamıştır.",
         "- \"İlk metin\": çeviri başlatıldıktan sonra ekranda ilk çeviri metninin görünmesine kadar geçen süre.",
         "- \"Farklı satırlar\": 1. ve 2. koşu çıktıları arasındaki satır farkı (`-` 1. koşu, `+` 2. koşu).",
         "- \"Kalın yazı düzeltmesi\" ve \"sınır isteği\": uygulamanın hızlı çeviri yolundaki ek işlemler (Adım 7).", ""]
    for t in v["testler"]:
        a, b = k1[t["id"]], k2[t["id"]]
        L += [f"## {t['id']} · {t['kaynak'].upper()}→{t['hedef'].upper()} · {t['konu']}", "",
              "**Kaynak metin**", "", _blok(t["metin"]), "",
              f"Dikkat (yalnız değerlendirme için, modele gitmedi): {t['dikkat']}", "",
              f"**1. koşu** ({a['durum']})", "", _blok(a["cikti"]), "",
              f"**2. koşu** ({b['durum']})", "", _blok(b["cikti"]), ""]
        if a["cikti"] == b["cikti"]:
            L += ["**İki çıktı aynı mı:** evet", ""]
        else:
            fark = [s for s in difflib.unified_diff(a["cikti"].split("\n"), b["cikti"].split("\n"), lineterm="", n=0)
                    if not s.startswith(("---", "+++", "@@"))]
            L += ["**İki çıktı aynı mı:** hayır — farklı satırlar:", "", "```diff"] + fark + ["```", ""]
        L += ["**Modele giden sözlük terimleri:** " + ("; ".join(a["terimler"]) if a["terimler"] else "yok"), "",
              f"**Ek işlemler:** 1. koşu: {_not(a)} · 2. koşu: {_not(b)}", "",
              "| | İlk metin | Toplam |", "|---|---|---|",
              f"| 1. koşu | {a['ilk_metin']:.2f} s | {a['toplam']:.2f} s |",
              f"| 2. koşu | {b['ilk_metin']:.2f} s | {b['toplam']:.2f} s |", ""]
    L += ["## Süre tablosu", "",
          "| Metin | Yön | 1. koşu ilk metin | 1. koşu toplam | 2. koşu ilk metin | 2. koşu toplam |",
          "|---|---|---|---|---|---|"]
    for t in v["testler"]:
        a, b = k1[t["id"]], k2[t["id"]]
        L.append(f"| {t['id']} | {t['kaynak'].upper()}→{t['hedef'].upper()} | {a['ilk_metin']:.2f} s | {a['toplam']:.2f} s | "
                 f"{b['ilk_metin']:.2f} s | {b['toplam']:.2f} s |")
    ayni = sum(k1[t["id"]]["cikti"] == k2[t["id"]]["cikti"] for t in v["testler"])
    L += ["", f"**İki koşuda aynı çıkan metin sayısı:** {ayni} / {len(v['testler'])}"]
    hedef.write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    if sys.argv[1] == "calistir":
        calistir(Path(sys.argv[2]))
    else:
        rapor(Path(sys.argv[2]), Path(sys.argv[3]))
