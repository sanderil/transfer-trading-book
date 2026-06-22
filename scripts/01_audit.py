import pandas as pd, glob, os

files = glob.glob("data/raw/*.csv")
print("files found:", [os.path.basename(f) for f in files])

dfs = []
for f in files:
    d = pd.read_csv(f)
    d["source_file"] = os.path.basename(f)
    dfs.append(d)
df = pd.concat(dfs, ignore_index=True)

print("\ntotal rows:", len(df))
print("columns:", list(df.columns))
print("\nfirst 5 rows:")
print(df.head().to_string())

# how many rows actually carry a usable fee?
if "fee_cleaned" in df.columns:
    print("\nrows with fee_cleaned > 0:", (pd.to_numeric(df["fee_cleaned"], errors="coerce") > 0).sum())

# do the stars show up with real fees?
name_col = "player_name" if "player_name" in df.columns else df.columns[0]
for n in ["Rice", "Isak", "Neymar", "Bale", "Griezmann", "Felix", "Enzo", "Ronaldo"]:
    hit = df[df[name_col].astype(str).str.contains(n, case=False, na=False)]
    print(f"\n--- {n}: {len(hit)} rows ---")
    if len(hit):
        cols = [c for c in [name_col,"club_name","club_involved_name","fee",
                            "fee_cleaned","transfer_movement","transfer_period","year","season"]
                if c in df.columns]
        print(hit[cols].head(8).to_string(index=False))