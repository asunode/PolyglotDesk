import json, sys, time, requests

URL = "http://127.0.0.1:11434"
SYSTEM = (
    "You are a professional translator. Translate the user's text from {src} to {dst}. "
    "Output only the translation itself: no explanations, no notes, no quotation marks, "
    "no introductory phrases. Preserve meaning, tone, line breaks and punctuation. "
    "Render idioms with natural equivalents in {dst}."
)
TESTS = [
    ("tr", "günlük", "Yarın sabah erkenden markete gidip ekmek ve süt alacağım, sonra da çocukları okula bırakacağım."),
    ("tr", "teknik", "Uygulama, yerel ağdaki sunucuya HTTP üzerinden bağlanır ve yanıtı akış hâlinde işler. Bağlantı zaman aşımına uğrarsa istemci üç kez yeniden dener; her denemede bekleme süresi iki katına çıkar. Önbellekteki veriler şifrelenmiş olarak diskte saklanır."),
    ("tr", "deyim", "Toplantıda herkes ağzına geleni söyledi, ben de sabrımın taştığını hissettim; neyse ki müdür işi tatlıya bağladı."),
    ("en", "günlük", "I'm running a bit late, so could you please save me a seat and order me a coffee?"),
    ("en", "teknik", "The garbage collector periodically scans the heap for objects that are no longer reachable and reclaims their memory. To reduce pause times, modern runtimes use generational collection, which assumes that most objects die young. Developers can tune the heap size through configuration flags."),
    ("en", "deyim", "We were all on the fence about the new plan, but when the manager finally spilled the beans about the budget cuts, it was the last straw."),
]
NAMES = {"tr": "Turkish", "en": "English"}


def run(model, src, text):
    dst = "en" if src == "tr" else "tr"
    body = {
        "model": model, "stream": True, "think": False, "keep_alive": "10m",
        "options": {"temperature": 0.2},
        "messages": [
            {"role": "system", "content": SYSTEM.format(src=NAMES[src], dst=NAMES[dst])},
            {"role": "user", "content": text},
        ],
    }
    t0 = time.time(); ttft = None; out = ""
    with requests.post(URL + "/api/chat", json=body, stream=True, timeout=600) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            d = json.loads(line)
            c = d.get("message", {}).get("content", "")
            if c and c.strip() and ttft is None:
                ttft = time.time() - t0
            out += c
            if d.get("done"):
                break
    return ttft, time.time() - t0, out.strip()


for model in sys.argv[1:]:
    t = time.time()
    requests.post(URL + "/api/generate", json={"model": model, "prompt": "", "keep_alive": "10m"}, timeout=600)
    load = time.time() - t
    ps = requests.get(URL + "/api/ps").json()["models"]
    info = next((m for m in ps if m["name"] == model), {})
    gpu = info.get("size_vram", 0) / max(info.get("size", 1), 1) * 100
    print(f"\n######## {model}  yükleme={load:.1f}s  GPU payı=%{gpu:.0f}", flush=True)
    for src, kind, text in TESTS:
        ttft, total, out = run(model, src, text)
        print(f"--- {src}->{'en' if src=='tr' else 'tr'} {kind}: ilk={ttft:.2f}s toplam={total:.2f}s", flush=True)
        print(out, flush=True)
    requests.post(URL + "/api/generate", json={"model": model, "keep_alive": 0}, timeout=60)
