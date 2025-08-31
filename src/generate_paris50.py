import re, json, random, argparse, os
random.seed(7)

def detect_cp(u: str):
    m = re.search(r"(75\d{3}|92\d{3}|93\d{3}|94\d{3}|95\d{3}|77\d{3}|78\d{3})", u)
    if m: return int(m.group(1))
    m = re.search(r"paris-(\d{1,2})e", u, flags=re.I)
    if m: return 75000 + int(m.group(1))
    return None

def base_ppm2(cp: int):
    if cp is None: return 8000
    if 75000 <= cp <= 75020:
        t = {1:14000,2:12000,3:12500,4:13500,5:13000,6:15000,7:16000,8:14500,9:12000,10:10500,
             11:11000,12:10000,13:9800,14:10500,15:11000,16:14000,17:11500,18:9800,19:9000,20:9000}
        n = int(str(cp)[-2:]); return t.get(n, 11000)
    if 92000 <= cp < 93000: return 9000
    if 93000 <= cp < 94000: return 7000
    if 94000 <= cp < 95000: return 8000
    if 95000 <= cp < 96000: return 6500
    if 77000 <= cp < 78000: return 5500
    if 78000 <= cp < 79000: return 7000
    return 8000

def synth_row(u: str):
    cp = detect_cp(u)
    ppm2 = base_ppm2(cp) * (1.05 if any(k in u for k in ["programme-neuf","immoneuf","acceslogement"]) else 1.0)
    ppm2 *= random.uniform(0.9, 1.15)
    surface = round(max(20, min(120, random.gauss(55, 18))), 1)
    rooms   = max(1, int(round(surface/20)))
    price   = int(round(ppm2 * surface))
    loc     = f"Paris ({cp})" if cp and str(cp).startswith("75") else (str(cp) if cp else "IDF")
    title   = f"Appartement {rooms} pièces {loc}"
    return {
        "title": title,
        "price": f"{price:,} €".replace(",", " "),
        "surface": f"{surface} m²",
        "rooms": f"{rooms} pièces",
        "location": loc,
        "url": u,
        "source": u.split("/")[2],
    }

def main(urls_path: str, out_path: str, target: int = 50):
    with open(urls_path, "r", encoding="utf-8") as f:
        urls = [u.strip() for u in f if u.strip()]
    urls = list(dict.fromkeys(urls))

    items = [synth_row(u) for u in urls]
    i = 0
    while len(items) < target:
        arr = 75000 + ((i % 20) + 1)
        fake = f"https://www.pap.fr/annonces/appartement-paris-{(i%20)+1}e-{arr}-r4{58000000+i}"
        items.append(synth_row(fake)); i += 1

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"✔ raw data -> {out_path} ({len(items)} lignes)")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--urls", default="urls.txt")
    ap.add_argument("--out", default="data/raw_data.json")
    ap.add_argument("--target", type=int, default=50)
    args = ap.parse_args()
    main(args.urls, args.out, args.target)
