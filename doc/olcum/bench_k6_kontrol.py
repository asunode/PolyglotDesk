"""Adım 9: K6 düzeltmesinin kontrolü — yalnız hızlı çeviri (ham kayıt).

Kullanım:
    python3 doc/olcum/bench_k6_kontrol.py doc/olcum/k6-kontrol-ham.json doc/olcum/k6-kontrol-sonuc.md

Teknik bağlam kuralları (kart → board, kayıt → log) artık yalnız sözlüğün [Teknik bağlam tetikleyicileri]
bölümündeki donanım/elektronik terimleriyle açılıyor. K6'da (Wi-Fi) kural açılmamalı; D5, W1, W3, G3 ve V5'te
hâlâ açılmalı. Uygulamanın hızlı çeviri yolu (`Cevirici`), yalnız CPU, paketteki varsayılan sözlük; açılıştaki
gibi önden yükleme.
"""

import json
import re
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK))
METINLER = [("hizli-konu-seti-v1.md", "K6"), ("detayli-test-seti-v1.md", "D5"), ("dogrulama-seti-v2.md", "W1"),
            ("dogrulama-seti-v2.md", "W3"), ("kontrol-seti-v2.md", "G3"), ("dogrulama-seti-v1.md", "V5")]
ESKI = {"K6": ("hizli-konu-testi-v1-ham.json", "Adım 8, 1. koşu"), "D5": ("detayli-test-v3-ham.json", "Adım 7"),
        "W1": ("detayli-test-v3-ham.json", "Adım 7"), "W3": ("detayli-test-v3-ham.json", "Adım 7"),
        "G3": ("detayli-test-v3-ham.json", "Adım 7"), "V5": ("detayli-test-v3-ham.json", "Adım 7")}


def oku(set_adi: str, kimlik: str) -> dict:
    metin = (KOK / "doc/olcum" / set_adi).read_text(encoding="utf-8")
    m = re.search(rf"^## {kimlik} · (TR|EN)→(TR|EN)[^\n]*\n\n```text\n(.*?)\n```\n\nDikkat: ([^\n]*)", metin, re.S | re.M)
    return {"id": kimlik, "set": set_adi, "kaynak": m[1].lower(), "hedef": m[2].lower(), "metin": m[3], "dikkat": m[4]}


def eski_cikti(kimlik: str) -> str:
    v = json.loads((KOK / "doc/olcum" / ESKI[kimlik][0]).read_text(encoding="utf-8"))
    if "kosular" in v:
        return v["kosular"]["1"][kimlik]["cikti"]
    return next(t["hizli"]["cikti"] for t in v["testler"] if t["id"] == kimlik)


def main(ham: Path, sonuc: Path) -> None:
    from PySide6.QtCore import QCoreApplication, QEventLoop

    from cevirmen import ayarlar
    from cevirmen.cevirici import Cevirici
    from cevirmen.istem import sinir_istemi
    from cevirmen.ollama import Ollama
    from cevirmen.sozluk import VARSAYILAN, Sozluk

    app = QCoreApplication(sys.argv)

    def bekle(sinyaller: dict):
        dongu = QEventLoop()
        olay = {}
        for ad, sinyal in sinyaller.items():
            sinyal.connect(lambda *a, ad=ad: (olay.setdefault("o", (ad, a)), dongu.quit()))
        dongu.exec()
        return olay["o"]

    ollama = Ollama(dict(ayarlar.VARSAYILAN))
    sozluk = Sozluk(VARSAYILAN)
    sozluk.guncelle()
    on = ollama.onden_yukle(sinir_istemi())
    bekle({"tamam": on.tamam, "hata": on.hata})
    hizli = Cevirici(ollama, sozluk)
    kayit = {"baslangic": time.strftime("%Y-%m-%d %H:%M:%S %z"), "testler": []}
    for set_adi, kimlik in METINLER:
        t = oku(set_adi, kimlik)
        t0 = time.time()
        hizli.baslat(t["metin"], t["kaynak"], t["hedef"])
        olay = bekle({"bitti": hizli.bitti, "hata": hizli.hata}) if hizli.calisiyor else ("bitti", ())
        t.update({"durum": olay[0], "cikti": hizli.metin(), "ilk_metin": round(hizli.ilk_parca_suresi or 0, 2),
                  "toplam": round(time.time() - t0, 2), "teknik": sozluk.teknik_mi(t["metin"], t["kaynak"]),
                  "terimler": [str(x) for x in sozluk.eslesenler(t["metin"], t["kaynak"], t["hedef"])],
                  "kalin": list(hizli.kalin_kaydi), "sinir_istegi": hizli.sinir_istegi, "eski": eski_cikti(kimlik)})
        kayit["testler"].append(t)
        print(kimlik, t["toplam"], t["durum"], flush=True)
    kayit["bitis"] = time.strftime("%Y-%m-%d %H:%M:%S %z")
    ham.write_text(json.dumps(kayit, ensure_ascii=False, indent=2), encoding="utf-8")

    L = ["# K6 düzeltmesi kontrolü — hızlı çeviri (ham kayıt)", "",
         f"Betik: `doc/olcum/bench_k6_kontrol.py`. Ham veri: `doc/olcum/{ham.name}`. Koşu: {kayit['baslangic']} – {kayit['bitis']}. "
         "gemma4:12b-it-qat, yalnız CPU, temperature 0, seed 42; uygulamanın hızlı çeviri yolu, paketteki varsayılan sözlük.",
         "Değişiklik (Adım 9): teknik bağlam kuralları yalnız sözlüğün `[Teknik bağlam tetikleyicileri]` bölümündeki "
         "donanım/elektronik terimleriyle açılır (önceden sözlükteki herhangi bir terim, ör. Wi-Fi, açıyordu).", ""]
    for t in kayit["testler"]:
        L += [f"## {t['id']} · {t['kaynak'].upper()}→{t['hedef'].upper()} ({t['set'].removesuffix('.md')})", "",
              "```text", t["metin"], "```", "", f"Dikkat: {t['dikkat']}", "",
              f"**Önceki hızlı çeviri ({ESKI[t['id']][1]})**", "", "```text", t["eski"], "```", "",
              f"**Yeni hızlı çeviri** ({t['durum']}; ilk metin {t['ilk_metin']:.2f} s, toplam {t['toplam']:.2f} s)", "",
              "```text", t["cikti"], "```", "",
              f"- Teknik bağlam tetiklendi: {'evet' if t['teknik'] else 'hayır'}",
              "- Modele giden sözlük terimleri: " + ("; ".join(t["terimler"]) or "yok"),
              "- Kalın yazı düzeltmesi: " + (" / ".join(t["kalin"]) or "yok") + f"; sınır isteği: {t['sinir_istegi']}", ""]
    sonuc.write_text("\n".join(L), encoding="utf-8")
    app.quit()


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
