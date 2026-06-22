import sqlite3
import glob, os
import pandas as pd

RAW = "data/raw"
DB_PATH = "data/processed/transfers.db"
PNL_CSV = "data/processed/club_pnl.csv"
CLEAN_CSV = "data/processed/transfers_clean.csv"

# ---------- 1. LOAD + STACK ALL LEAGUES ----------
files = glob.glob(f"{RAW}/*.csv")
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
print("raw rows (all leagues):", len(df))

# ---------- 2. CLEAN ----------
# drop loans: a loan isn't a buy or a sell, so it can't be trading P&L.
# this removes "loan transfer", "Loan fee:€..", and "End of loan.." rows.
df = df[~df["fee"].str.contains("loan", case=False, na=False)]

# keep only rows with a usable numeric fee (drops "?", "-", blanks).
# free transfers (fee_cleaned == 0) are real permanent moves — we keep them.
df["fee_cleaned"] = pd.to_numeric(df["fee_cleaned"], errors="coerce")
df = df.dropna(subset=["fee_cleaned"])

# scope to the modern era through the data's end (2022/23 season).
df = df[df["year"].between(2010, 2023)]

# remove any fully-identical duplicate rows from stacking files.
df = df.drop_duplicates()

# keep only the columns we need, tidy them.
cols = ["club_name", "player_name", "position", "club_involved_name",
        "fee_cleaned", "transfer_movement", "transfer_period",
        "league_name", "year", "season", "country"]
df = df[cols].copy()
print("clean permanent transfers (2010-2023):", len(df))

# ---------- 3. LOAD CLEAN TABLE INTO SQLITE ----------
conn = sqlite3.connect(DB_PATH)
df.to_sql("transfers", conn, if_exists="replace", index=False)

# ---------- 4. CLUB P&L (SQL) ----------
# fee_cleaned is in € millions. "in" = money spent buying, "out" = money received selling.
query = """
SELECT
    club_name,
    league_name,
    country,
    ROUND(SUM(CASE WHEN transfer_movement='in'  THEN fee_cleaned ELSE 0 END), 1) AS total_spent_m,
    ROUND(SUM(CASE WHEN transfer_movement='out' THEN fee_cleaned ELSE 0 END), 1) AS total_received_m,
    ROUND(SUM(CASE WHEN transfer_movement='out' THEN fee_cleaned ELSE 0 END)
        - SUM(CASE WHEN transfer_movement='in'  THEN fee_cleaned ELSE 0 END), 1) AS net_profit_m,
    SUM(CASE WHEN transfer_movement='in'  THEN 1 ELSE 0 END) AS n_buys,
    SUM(CASE WHEN transfer_movement='out' THEN 1 ELSE 0 END) AS n_sells
FROM transfers
GROUP BY club_name, league_name, country
"""
pnl = pd.read_sql(query, conn)
pnl.to_sql("club_pnl", conn, if_exists="replace", index=False)

# ---------- 5. EXPORT ----------
df.to_csv(CLEAN_CSV, index=False)
pnl.to_csv(PNL_CSV, index=False)
conn.close()

# ---------- 6. SUMMARY ----------
pd.options.display.float_format = "{:,.1f}".format
print("\nclubs analyzed:", len(pnl))

active = pnl[(pnl["n_buys"] + pnl["n_sells"]) >= 10]  # ignore barely-active clubs in the ranking
show = ["club_name", "country", "total_spent_m", "total_received_m", "net_profit_m", "n_buys", "n_sells"]

print("\n=== TOP 15 TRADING PROFITS (sell > buy) ===")
print(active.sort_values("net_profit_m", ascending=False)[show].head(15).to_string(index=False))

print("\n=== TOP 15 NET SPENDERS (buy > sell) ===")
print(active.sort_values("net_profit_m")[show].head(15).to_string(index=False))