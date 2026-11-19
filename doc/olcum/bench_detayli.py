"""Adım 5: Detaylı Çevir test seti v1 — ham kayıt.

Kullanım:
    python3 doc/olcum/bench_detayli.py calistir doc/olcum/detayli-test-v1-ham.json
    python3 doc/olcum/bench_detayli.py rapor doc/olcum/detayli-test-v1-ham.json doc/olcum/detayli-test-v1-sonuc.md

Gerçek kullanım sırası: uygulamadaki gibi açılışta model yüklenir; tek bir hızlı çevirici ve tek bir
Detaylı çevirici nesnesi kullanılır; her testte önce hızlı çeviri, hemen ardından aynı metne
Detaylı Çevir. D1'den D10'a sırayla. Varsayılan ayarlar (yalnız CPU) ve paketteki varsayılan sözlük.
"""

import difflib
import json
import re
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK))
SET = KOK / "doc/olcum/detayli-test-seti-v1.md"


def testleri_oku() -> list[dict]:
    metin = SET.read_text(encoding="utf-8")
    desen = r"^## (D\d+) · (TR|EN)→(TR|EN)\n\n```text\n(.*?)\n```\n\nDikkat: ([^\n]*)"
    return [{"id": m[1], "kaynak": m[2].lower(), "hedef": m[3].lower(), "metin": m[4], "dikkat": m[5]}
            for m in re.finditer(desen, metin, re.S | re.M)]


def calistir(cikti: Path) -> None:
    from PySide6.QtCore import QCoreApplication, QEventLoop

    from cevirmen import ayarlar
    from cevirmen.cevirici import Cevirici
    from cevirmen.detayli import DetayliCevirici
    from cevirmen.istem import sistem_istemi
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
    hizli = Cevirici(ollama, sozluk)
    detayli = DetayliCevirici(ollama, sozluk)
    t = time.time()
    on = ollama.onden_yukle(sistem_istemi("tr", "en"))
    print("önden yükleme", round(time.time() - t, 1), bekle({"tamam": on.tamam, "hata": on.hata})[0], flush=True)

    kayit = {"baslangic": time.strftime("%Y-%m-%d %H:%M:%S %z"), "ayarlar": ayar, "testler": []}
    for test in testleri_oku():
        t0 = time.time()
        hizli.baslat(test["metin"], test["kaynak"], test["hedef"])
        olay = bekle({"bitti": hizli.bitti, "hata": hizli.hata}) if hizli.calisiyor else ("bitti", ())
        h = {"ilk_metin": round(hizli.ilk_parca_suresi or 0, 2), "toplam": round(time.time() - t0, 2),
             "durum": olay[0] if olay[0] == "bitti" else f"hata: {olay[1]}", "cikti": hizli.metin()}

        t0 = time.time()
        detayli.baslat(test["metin"], test["kaynak"], test["hedef"])
        olay = bekle({"bitti": detayli.bitti, "hata": detayli.hata})
        parcalar = [s for s in detayli.sonuclar if s]
        d = {
            "ilk_metin": round(detayli.ilk_parca_suresi or 0, 2), "toplam": round(time.time() - t0, 2),
            "sure": {a: round(sum(s.sure.get(a, 0) for s in parcalar), 2) for a in ("arama", "ceviri", "denetim")},
            "durum": olay[0] if olay[0] == "bitti" else f"hata: {olay[1]}",
            "parca_sayisi": detayli.parca_sayisi,
            "taslak": "\n\n".join(s.taslak for s in parcalar),
            "son": detayli.metin(),
            "sorunlar_once": [p for s in parcalar for p in s.sorunlar_once],
            "sorunlar_sonra": [p for s in parcalar for p in s.sorunlar_sonra],
            "kayitlar": [{"tur": k.tur, "kaynak": k.kaynak, "lisans": k.lisans, "baslik": k.baslik, "istem": k.istem}
                         for k in detayli.tum_kayitlar()],
        }
        kayit["testler"].append({**test, "hizli": h, "detayli": d})
        print(test["id"], "hızlı", h["toplam"], h["durum"], "| detaylı", d["toplam"], d["sure"], d["durum"], flush=True)
        cikti.write_text(json.dumps(kayit, ensure_ascii=False, indent=2), encoding="utf-8")
    kayit["bitis"] = time.strftime("%Y-%m-%d %H:%M:%S %z")
    cikti.write_text(json.dumps(kayit, ensure_ascii=False, indent=2), encoding="utf-8")
    app.quit()


# ------------------------------------------------------------------ rapor
TUR_ADI = {"kalip": "kalıp/deyim", "anlam": "çok anlamlı kelime", "ornek": "örnek cümle", "sozluk": "sözlük terimi"}


def _kucult(metin: str) -> str:
    return metin.replace("İ", "i").lower()


def _dikkat_ogeleri(satir: str) -> list[tuple[str, str]]:
    """(satırdaki yazım, aranan biçim): parantez içi not aranmaz ("oh great (alay)" → "oh great")."""
    return [(o.strip(), re.sub(r"\s*\([^)]*\)", "", o).strip()) for o in satir.split(",") if o.strip()]


def _ulasti_mi(oge: str, kayitlar: list[dict]) -> list[dict]:
    desen = re.compile(rf"(?<!\w){re.escape(_kucult(oge))}(?!\w)")
    return [k for k in kayitlar if desen.search(_kucult(k["istem"])) or _kucult(k["baslik"]) == _kucult(oge)]


def _blok(metin: str) -> str:
    return "```text\n" + metin + "\n```"


def rapor(ham: Path, hedef: Path) -> None:
    v = json.loads(ham.read_text(encoding="utf-8"))
    L = ["# Detaylı Çevir test seti v1 — sonuçlar (ham kayıt)", "",
         f"Test seti: `doc/olcum/detayli-test-seti-v1.md`. Betik: `doc/olcum/bench_detayli.py`. Ham veri: `doc/olcum/{ham.name}`.",
         f"Koşu: {v['baslangic']} – {v.get('bitis', '?')}. Model {v['ayarlar']['model']}, yalnız CPU (num_gpu 0), num_ctx 8192, "
         "temperature 0, seed 42. Uygulamanın çeviri yolu: hızlı çeviri `Cevirici`, Detaylı Çevir `DetayliCevirici` "
         "(bilgi araması PostgreSQL `cevirmen`, `cevirmen_okur` rolüyle). Her testte önce hızlı çeviri, hemen ardından Detaylı Çevir; D1'den D10'a sırayla.",
         "",
         "Notlar:",
         "- Bütün çıktılar ham kayıttan birebir alınmıştır; düzeltilmemiş, kısaltılmamıştır.",
         "- \"İlk metin\": çeviri başlatıldıktan sonra ekranda ilk çeviri metninin görünmesine kadar geçen süre.",
         "- \"Denetimin değiştirdikleri\": taslak ile son çıktı arasındaki satır farkı (`-` taslaktaki satır, `+` son çıktıdaki satır).",
         "- \"Kod denetimi\": `cevirmen/bicim.py`. \"Denetimden önce\" bulunanlar denetim geçişinde modele bildirildi; \"denetimden sonra\" son çıktıda kalanlardır.",
         "- \"Dikkat kelimeleri modele ulaştı mı\": mekanik denetim. Kelime ya da ifade, bir bilgi kaydının başlığıyla aynıysa ya da kaydın modele giden metninde "
         "ayrı kelime olarak geçiyorsa \"evet\" (eşleşen kayıtlar yanında). Parantez içindeki notlar aranmaz. Çekimli/yalın biçim farkı eşleşme sayılmaz.",
         ""]
    for t in v["testler"]:
        h, d = t["hizli"], t["detayli"]
        yon = f"{t['kaynak'].upper()}→{t['hedef'].upper()}"
        L += [f"## {t['id']} · {yon}", "", "**Kaynak metin**", "", _blok(t["metin"]), "",
              f"**Hızlı çeviri** — ilk metin {h['ilk_metin']:.2f} s, toplam {h['toplam']:.2f} s ({h['durum']})", "", _blok(h["cikti"]), "",
              "**Detaylı Çevir — denetimden önceki taslak**", "", _blok(d["taslak"]), "",
              f"**Detaylı Çevir — son çıktı** ({d['durum']})", "", _blok(d["son"]), "",
              "**Denetimin taslakta değiştirdikleri**", ""]
        fark = [s for s in difflib.unified_diff(d["taslak"].split("\n"), d["son"].split("\n"), lineterm="", n=0)
                if not s.startswith(("---", "+++", "@@"))]
        L += (["```diff"] + fark + ["```"]) if fark else ["Değişiklik yok (taslak ile son çıktı aynı)."]
        L += ["", "**Kod denetiminin bulduğu biçim sorunları**", "",
              "- Denetimden önce (modele bildirilen): " + (" / ".join(d["sorunlar_once"]) if d["sorunlar_once"] else "yok"),
              "- Denetimden sonra (son çıktıda kalan): " + (" / ".join(d["sorunlar_sonra"]) if d["sorunlar_sonra"] else "yok"), ""]
        bilgi = [k for k in d["kayitlar"] if k["tur"] != "sozluk"]
        sozluk = [k for k in d["kayitlar"] if k["tur"] == "sozluk"]
        L += [f"**Modele giden bilgi kayıtları ({len(bilgi)})**", ""]
        L += [f"- [{k['kaynak']} · {TUR_ADI[k['tur']]}] {k['istem']}" for k in bilgi] or ["- yok"]
        L += ["", f"**Modele giden sözlük terimleri ({len(sozluk)})**", ""]
        L += [f"- [kullanıcı sözlüğü] {k['istem']}" for k in sozluk] or ["- yok"]
        L += ["", f"**Dikkat kelimeleri modele ulaştı mı** (Dikkat: {t['dikkat']})", ""]
        for yazim, aranan in _dikkat_ogeleri(t["dikkat"]):
            eslesen = _ulasti_mi(aranan, d["kayitlar"])
            if eslesen:
                L.append(f"- {yazim}: evet — " + "; ".join(f"{k['baslik']} [{TUR_ADI[k['tur']]}, {k['kaynak']}]" for k in eslesen))
            else:
                L.append(f"- {yazim}: hayır")
        L += ["", "**Süreler**", "",
              "| | Arama | Çeviri | Denetim | Toplam | İlk metin |", "|---|---|---|---|---|---|",
              f"| Hızlı çeviri | — | — | — | {h['toplam']:.2f} s | {h['ilk_metin']:.2f} s |",
              f"| Detaylı Çevir | {d['sure']['arama']:.2f} s | {d['sure']['ceviri']:.2f} s | {d['sure']['denetim']:.2f} s | {d['toplam']:.2f} s | {d['ilk_metin']:.2f} s |", ""]
    L += ["## Süre tablosu", "",
          "| Test | Yön | Hızlı ilk metin | Hızlı toplam | Detaylı arama | Detaylı çeviri | Detaylı denetim | Detaylı toplam | Detaylı ilk metin |",
          "|---|---|---|---|---|---|---|---|---|"]
    for t in v["testler"]:
        h, d = t["hizli"], t["detayli"]
        L.append(f"| {t['id']} | {t['kaynak'].upper()}→{t['hedef'].upper()} | {h['ilk_metin']:.2f} s | {h['toplam']:.2f} s | "
                 f"{d['sure']['arama']:.2f} s | {d['sure']['ceviri']:.2f} s | {d['sure']['denetim']:.2f} s | {d['toplam']:.2f} s | {d['ilk_metin']:.2f} s |")
    hedef.write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    if sys.argv[1] == "calistir":
        calistir(Path(sys.argv[2]))
    else:
        rapor(Path(sys.argv[2]), Path(sys.argv[3]))
