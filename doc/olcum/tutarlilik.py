"""Adım 7 (C6): hızlı çeviri tutarlılığı — Ollama istem önbelleğinin etkisi.

Kullanım:
    python3 doc/olcum/tutarlilik.py doc/olcum/tutarlilik-ham.json

Uygulamanın hızlı çeviri mesajlarıyla (istem.sistem_istemi + sözlük terimleri, aynı seçenekler) doğrudan
/api/chat istekleri gönderilir; her istekte çıktı, süre ve Ollama günlüğündeki "cached n_tokens" (önbellekten
kullanılan token sayısı) kaydedilir. Metinler bu inceleme için yazıldı; hiçbir test setinden alınmadı.

Koşullar (her metin için, aynı yönde başka bir metin "öteki"):
    tek            önden yükleme (uygulamanın açılıştaki isteği) → hızlı çeviri
    tekrar         aynı hızlı çeviri hemen yeniden
    detayli_sonra  Detaylı Çevir'in iki isteği (çeviri + denetim, bilgi bloğu boş) → hızlı çeviri
    baska_sonra    ötekinin hızlı çevirisi → hızlı çeviri
Her koşul bir de "sınır" isteğiyle denenir: hızlı çeviriden hemen önce, ortak kuralların (istem.ORTAK) hemen
ardından ayrılan kısa bir istek (num_predict 1). Böylece hızlı çeviri isteği önbelleği her koşulda aynı
noktadan sonra işler.
"""

import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK))

from cevirmen import ayarlar  # noqa: E402
from cevirmen.istem import ORTAK, DENETIM_SEMASI, denetim_istemi, denetim_mesaji, detayli_istem, sistem_istemi  # noqa: E402
from cevirmen.sozluk import VARSAYILAN, Sozluk  # noqa: E402

METINLER = [
    ("tr", "en", "Toplantıyı yarına erteledik çünkü proje yöneticisi şehir dışındaydı; yine de raporu bu akşam göndereceğim."),
    ("tr", "en", "Akşam yemeğinden sonra sahilde uzun bir yürüyüş yaptık ve eve dönerken yağmura yakalandık."),
    ("en", "tr", "If the sensor reading drifts after a few hours, recalibrate it and log the offset before restarting the task."),
    ("en", "tr", "She said she would call back after lunch, but nobody has heard from her since then."),
]

AYAR = dict(ayarlar.VARSAYILAN)
SECENEK = {"temperature": 0, "seed": 42, "num_ctx": 8192, "num_gpu": 0}


def istek(mesajlar: list[dict], num_predict: int | None = None, bicim: dict | None = None) -> dict:
    govde = {"model": AYAR["model"], "stream": False, "think": False, "keep_alive": AYAR["keep_alive"],
             "options": {**SECENEK, **({"num_predict": num_predict} if num_predict else {})}, "messages": mesajlar}
    if bicim:
        govde["format"] = bicim
    baslangic = time.time()
    r = json.loads(urllib.request.urlopen(urllib.request.Request(
        AYAR["ollama_adresi"].rstrip("/") + "/api/chat", json.dumps(govde).encode(),
        {"Content-Type": "application/json"}), timeout=900).read())
    sure = time.time() - baslangic
    gunluk = subprocess.run(["journalctl", "-u", "ollama", "--since", f"@{int(baslangic)}", "--no-pager", "-o", "cat"],
                            capture_output=True, text=True).stdout
    onbellek = [int(s.split("cached n_tokens = ")[1].split(",")[0]) for s in gunluk.splitlines() if "cached n_tokens" in s]
    return {"cikti": r["message"]["content"], "sure": round(sure, 2), "istem_token": r.get("prompt_eval_count"),
            "istem_sn": round(r.get("prompt_eval_duration", 0) / 1e9, 2), "yukleme_sn": round(r.get("load_duration", 0) / 1e9, 2),
            "uretilen_token": r.get("eval_count"), "onbellek_token": onbellek}


sozluk = Sozluk(VARSAYILAN)
sozluk.guncelle()


def hizli(k: str, h: str, metin: str) -> dict:
    return istek([{"role": "system", "content": sistem_istemi(k, h, sozluk.eslesenler(metin, k, h))},
                  {"role": "user", "content": metin}])


def onden_yukle(k: str, h: str) -> dict:
    return istek([{"role": "system", "content": sistem_istemi(k, h)}, {"role": "user", "content": "."}], num_predict=1)


def sinir() -> dict:
    return istek([{"role": "system", "content": ORTAK + "\n\n#"}, {"role": "user", "content": "."}], num_predict=1)


def detayli(k: str, h: str, metin: str) -> None:
    terimler = sozluk.eslesenler(metin, k, h)
    taslak = istek([{"role": "system", "content": detayli_istem(k, h, terimler, "")}, {"role": "user", "content": metin}])["cikti"]
    istek([{"role": "system", "content": denetim_istemi(k, h, terimler, "")},
           {"role": "user", "content": denetim_mesaji(k, h, metin, taslak, [])}], bicim=DENETIM_SEMASI)


def kosu(sinirli: bool) -> list[dict]:
    sonuc = []

    def olc(k, h, metin):
        s = sinir() if sinirli else None
        r = hizli(k, h, metin)
        if s:
            r["sinir_sure"] = s["sure"]
        return r

    for i, (k, h, metin) in enumerate(METINLER):
        oteki = next(m for j, (kk, hh, m) in enumerate(METINLER) if j != i and kk == k)
        t = {"metin": metin, "yon": f"{k}-{h}", "kosullar": {}}
        onden_yukle(k, h)
        t["kosullar"]["tek"] = olc(k, h, metin)
        t["kosullar"]["tekrar"] = olc(k, h, metin)
        detayli(k, h, metin)
        t["kosullar"]["detayli_sonra"] = olc(k, h, metin)
        olc(k, h, oteki)
        t["kosullar"]["baska_sonra"] = olc(k, h, metin)
        print("sınırlı" if sinirli else "sınırsız", i + 1, {c: v["sure"] for c, v in t["kosullar"].items()},
              len({v["cikti"] for v in t["kosullar"].values()}), "farklı çıktı", flush=True)
        sonuc.append(t)
    return sonuc


if __name__ == "__main__":
    cikti = Path(sys.argv[1])
    kayit = {"baslangic": time.strftime("%Y-%m-%d %H:%M:%S %z"), "model": AYAR["model"], "secenekler": SECENEK}
    onden_yukle("tr", "en")
    kayit["sinirsiz"] = kosu(False)
    kayit["sinirli"] = kosu(True)
    kayit["bitis"] = time.strftime("%Y-%m-%d %H:%M:%S %z")
    cikti.write_text(json.dumps(kayit, ensure_ascii=False, indent=2), encoding="utf-8")
