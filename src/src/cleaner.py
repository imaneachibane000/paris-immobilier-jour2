import json, re, argparse, pandas as pd, os, numpy as np

def to_float(s):
    s = str(s).replace("\u00a0"," ").replace(",", ".")
    s = re.sub(r"[^\d.]", "", s)
    m = re.findall(r"\d+(?:\.\d+)?", s)
    return float(m[0]) if m else np.nan

def surf_m2(s):
    m = re.search(r"(\d+(?:[.,]\d+)?)\s*(?:m²|m2)", str(s))
    return to_float(m.group(1)) if m else np.nan

def rooms_n(s):
    m = re.search(r"(\d+)\s*pi(?:è|e)ce", str(s), flags=re.I)
    return to_float(m.group(1)) if m else np.nan

def main(inp, outp):
    with open(inp, "r", encoding="utf-8") as f:
        raw = json.load(f)
    df = pd.DataFrame(raw)
    for c in ["title","price","surface","rooms","location","url","source"]:
        if c not in df.columns: df[c] = None
    df["price_eur"]   = df["price"].apply(to_float)
    df["surface_m2"]  = df["surface"].apply(surf_m2)
    df["rooms_n"]     = df["rooms"].apply(rooms_n)
    df["price_per_m2"]= (df["price_eur"]/df["surface_m2"]).round(2)
    df = df[["title","location","rooms","surface","price",
             "price_eur","surface_m2","rooms_n","price_per_m2","url","source"]]
    os.makedirs(os.path.dirname(outp), exist_ok=True)
    df.to_csv(outp, index=False, encoding="utf-8")
    print(f"✔ cleaned -> {outp} ({len(df)} lignes)")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input",  default="data/raw_data.json")
    ap.add_argument("--output", default="data/cleaned_data.csv")
    args = ap.parse_args()
    main(args.input, args.output)
