import argparse, pandas as pd

def main(csv_path, min_rows):
    df=pd.read_csv(csv_path)
    req=["price_eur","surface_m2","rooms_n","price_per_m2"]
    for c in req:
        if c not in df.columns: raise SystemExit(f"❌ colonne manquante: {c}")
    if len(df)<min_rows: raise SystemExit(f"❌ lignes: {len(df)} < {min_rows}")
    if (df["price_eur"]<=0).any() or (df["surface_m2"]<=0).any() or (df["price_per_m2"]<=0).any():
        raise SystemExit("❌ valeurs négatives / nulles détectées")
    print("✔ validation OK")

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--csv",default="data/cleaned_data.csv")
    ap.add_argument("--min_rows",type=int,default=50)
    a=ap.parse_args(); main(a.csv,a.min_rows)
