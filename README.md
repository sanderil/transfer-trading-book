# Football's Trading Desks: Transfer-Market P&L Across Europe (2010–2023)

Treating football clubs as trading desks: which clubs run a **profitable transfer book** — buy low, develop, sell high — and which run **structural deficits** to acquire talent. Built from a 26,000-transfer dataset across seven European leagues, processed with Python and SQL, and visualised in Tableau.

**🔗 Live dashboard:** [View on Tableau Public](https://public.tableau.com/app/profile/riley.sanders3821/viz/FootballTransfersTradingDesks/Dashboard1)

I built this project to assess how profitable/detrimental business in the transfer market can be for European football clubs. I also wanted to highlight how certain clubs excel and thrive financially in the transfer market, while others drown in financial losses and seek their profits elsewhere.


## Key findings

**1. A small group of clubs consistently profit from trading players.**
Over 2010–2023, the clearest trading desks were developer-sellers, led by Benfica (**+€777M** net), Ajax (+€488M), Porto (+€435M), Lille (+€394M), and Sporting CP (+€291M). Their model is low spend, high sales — buy and develop cheap talent, sell it up the chain.

**2. The biggest spenders are the elite, and they run large deficits.**
Manchester United (**−€1.31bn**), Chelsea (−€1.21bn), Manchester City (−€1.20bn) and PSG (−€1.08bn) anchor the other end. They are net importers of talent, not traders of it.

**3. Volume and skill are different things.**
A spend-vs-receive view separates *how much* a club trades from *how well*. AS Monaco trades at huge volume (~€960M spent, ~€1.13bn received) yet stays **net positive** — a high-volume profitable trader. Chelsea trades at comparable volume but stays deeply negative. Same activity, opposite outcomes.

**4. At the national level, the market is a wealth pipeline.**
Aggregated to country, England's clubs net roughly **−€10.4bn** while Portugal and the Netherlands sit in positive territory. Money flows from developer leagues to the elite buying league.

-----

This correlates with the general idea that the most competitive leagues buy up expensive talents at top dollar from less competitive leagues.
The league that dominates this narrative is the English Premier League (EPL), who had a net transfer loss of €10.4bn. Leagues like the EPL absorb this through their commercial strength, far higher viewership, and TV broadcast revenue than the selling leagues.

-----

## Dashboard



The dashboard has three linked views (click any club to filter the others):
- **Club Trading P&L** — net transfer profit, top 15 traders vs. top 15 spenders.
- **Spend vs Receive** — every active club plotted against a break-even line; above = profitable, below = net spend.
- **Net Profit by Country** — the structural buyer/seller split across nations.

----

## Data

- **Source:** [ewenme/transfers](https://github.com/ewenme/transfers) — transfer records scraped from Transfermarkt, one file per league.
- **Leagues (7):** Premier League, La Liga, Serie A, Ligue 1, Bundesliga, Primeira Liga (Portugal), Eredivisie.
- **Scope:** filtered to the 2010–2023 window (data ends with the 2022/23 season).
- **Volume:** 138,224 raw rows → **26,549 clean permanent transfers** across **243 clubs**.
- Fees are in € millions (`fee_cleaned`).

---

## Methodology

A reproducible Python → SQL → Tableau pipeline:

1. **Ingest & stack** all seven league CSVs (pandas).
2. **Clean:** drop loans (a loan isn't a buy or sell), drop rows without a numeric fee, scope to 2010–2023, and de-duplicate cross-league records (a Benfica→Man City deal appears in both league files).
3. **Aggregate (SQL):** load the clean table into SQLite and compute per-club P&L — `SUM(out fees) − SUM(in fees)` — plus total spent, total received, and deal counts.
4. **Visualise:** export the club P&L table to CSV and build three linked Tableau views.

---

## Repository structure

```
transfer-trading-book/
├── data/
│   ├── raw/                  # seven ewenme league CSVs
│   └── processed/            # club_pnl.csv, transfers_clean.csv, transfers.db
├── scripts/
│   ├── 01_audit.py           # data verification (confirm fees/stars exist before building)
│   └── 02_phase0_build.py    # clean → SQLite → per-club P&L
├── requirements.txt
└── README.md
```

## Limitations

These are deliberate scoping choices, stated up front:

- **Trading P&L only — wages are excluded.** This measures transfer-fee profit, not club profit. Wages are a club's largest cost, so a "profitable trader" here is not necessarily a profitable business.
- **Data ends at 2022/23.** Clubs whose trading models peaked recently are understated — Brighton being the clearest case, as their major sales (Caicedo, Mac Allister, Cucurella) and the Saudi-league wave fall outside the window.
- **League selection shapes the national totals.** The analysis covers seven top divisions, so country-level figures describe these leagues, not all of global football. England's total is amplified by having more big-spending clubs in the sample than the single divisions used for Portugal or the Netherlands.
- **Loans and undisclosed fees are excluded;** free transfers are kept as €0.
- Clubs are grouped by name string, and the dataset inherits Transfermarkt's own fee estimates (some fees are reported, not official).

------

## Tech stack

Python (pandas) · SQLite / SQL · Tableau Public

## Room for Improvement

If I wanted to take this to the next step, I would add wages to the equation to see what players cost the club to get a bigger scope of how much a transfer costs the club. I could find a more up to date data set that runs up to 2026. I could then fully compare the true costs of the transfer market to how much the clubs profit in general, this could show how clubs vary and differ in the financial focuses and missions.
