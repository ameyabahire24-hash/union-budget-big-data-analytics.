"""Generate 10 exploratory plots from the restored Union Budget working CSV.

Run from any directory: python code/generate_graphs.py
Outputs are written to graphs/. Charts summarize recorded rows only; they are not
complete official budget totals. Null values are not silently changed to zero.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "Union_Budget_Analytical_Dataset.csv"
OUT = ROOT / "graphs"
OUT.mkdir(exist_ok=True)

if not DATA.exists():
    raise FileNotFoundError("CSV missing. Run 'python code/restore_dataset.py' first.")

df = pd.read_csv(DATA)
for col in ["Revenue_Cr", "Capital_Cr", "Total_Cr"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

years = sorted(df["Financial_Year"].dropna().astype(str).unique())
annual = (df.groupby("Financial_Year")["Total_Cr"].sum(min_count=1)
          .reindex(years).rename("recorded_total_cr").reset_index())
annual["yoy_pct"] = annual["recorded_total_cr"].pct_change() * 100
latest_year = years[-1]
latest = df[df["Financial_Year"].astype(str) == latest_year].copy()
latest = latest.dropna(subset=["Total_Cr"])

def save(fig, filename):
    fig.tight_layout()
    fig.savefig(OUT / filename, dpi=180, bbox_inches="tight")
    plt.close(fig)

# 1. Annual recorded extracted totals.
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(annual["Financial_Year"], annual["recorded_total_cr"] / 1000, marker="o")
ax.set_title("Recorded Extracted Budget by Financial Year")
ax.set_ylabel("Recorded total (₹ thousand crore)")
ax.set_xlabel("Financial year")
ax.tick_params(axis="x", rotation=45)
ax.grid(True, alpha=.25)
save(fig, "01_ten_year_budget_trend.png")

# 2. Year-on-year change in the available recorded totals.
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(annual["Financial_Year"], annual["yoy_pct"])
ax.axhline(0, linewidth=1)
ax.set_title("Change in Recorded Extracted Total vs Previous Listed Year")
ax.set_ylabel("Change (%)")
ax.set_xlabel("Financial year")
ax.tick_params(axis="x", rotation=45)
ax.grid(True, axis="y", alpha=.25)
save(fig, "02_yoy_growth.png")

# 3. Top 15 departments/demands in the latest represented year.
top = latest.nlargest(15, "Total_Cr").sort_values("Total_Cr")
fig, ax = plt.subplots(figsize=(11, 7))
ax.barh(top["Demand_or_Department"], top["Total_Cr"] / 1000)
ax.set_title(f"Top 15 Recorded Demands — {latest_year}")
ax.set_xlabel("Recorded total (₹ thousand crore)")
save(fig, "03_top15_departments.png")

# 4. Largest absolute first-to-last available changes by department.
ordered = df.sort_values("Financial_Year")
changes = []
for name, grp in ordered.groupby("Demand_or_Department"):
    valid = grp.dropna(subset=["Total_Cr"])
    if len(valid) >= 2:
        first, last = valid.iloc[0], valid.iloc[-1]
        changes.append({"department": name, "change_cr": last["Total_Cr"] - first["Total_Cr"],
                        "first_year": first["Financial_Year"], "last_year": last["Financial_Year"]})
change_df = pd.DataFrame(changes)
if not change_df.empty:
    top_changes = change_df.reindex(change_df["change_cr"].abs().sort_values(ascending=False).index).head(15).sort_values("change_cr")
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.barh(top_changes["department"], top_changes["change_cr"] / 1000)
    ax.set_title("Largest Absolute Changes Between First and Last Available Records")
    ax.set_xlabel("Change in recorded total (₹ thousand crore)")
    save(fig, "04_largest_changes.png")

# 5. Heatmap for 20 highest latest-year demands, leaving missing cells masked.
selected = latest.nlargest(20, "Total_Cr")["Demand_or_Department"].tolist()
pivot = df[df["Demand_or_Department"].isin(selected)].pivot_table(
    index="Demand_or_Department", columns="Financial_Year", values="Total_Cr", aggfunc="sum")
pivot = pivot.reindex(index=selected, columns=years)
fig, ax = plt.subplots(figsize=(12, 8))
masked = np.ma.masked_invalid(pivot.to_numpy(dtype=float) / 1000)
im = ax.imshow(masked, aspect="auto", interpolation="nearest")
ax.set_yticks(range(len(pivot.index)), pivot.index)
ax.set_xticks(range(len(pivot.columns)), pivot.columns, rotation=45, ha="right")
ax.set_title("Recorded Demand Totals by Year (blank cells are missing)")
ax.set_xlabel("Financial year")
fig.colorbar(im, ax=ax, label="₹ thousand crore")
save(fig, "05_department_year_heatmap.png")

# 6. Sector trends from the exploratory keyword-based sector field.
sector_year = df.groupby(["Financial_Year", "Sector"])["Total_Cr"].sum(min_count=1).reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
for sector, grp in sector_year.groupby("Sector"):
    grp = grp.set_index("Financial_Year").reindex(years)
    ax.plot(years, grp["Total_Cr"] / 1000, marker="o", label=sector)
ax.set_title("Recorded Sector Totals (Exploratory Categories)")
ax.set_ylabel("Recorded total (₹ thousand crore)")
ax.tick_params(axis="x", rotation=45)
ax.legend(fontsize=8)
ax.grid(True, alpha=.25)
save(fig, "06_sector_trends.png")

# 7. Sector composition for the latest represented year.
sector_latest = latest.groupby("Sector")["Total_Cr"].sum(min_count=1).dropna().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(8, 8))
if not sector_latest.empty:
    ax.pie(sector_latest.values, labels=sector_latest.index, autopct="%1.1f%%", startangle=90)
    ax.set_title(f"Recorded Sector Composition — {latest_year}")
save(fig, "07_sector_composition.png")

# 8. Index of annual recorded totals; first available listed year = 100.
base = annual["recorded_total_cr"].iloc[0] if not annual.empty else np.nan
annual["index_100"] = annual["recorded_total_cr"] / base * 100 if pd.notna(base) and base != 0 else np.nan
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(annual["Financial_Year"], annual["index_100"], marker="o")
ax.set_title("Index of Recorded Extracted Total (First Listed Year = 100)")
ax.set_ylabel("Index")
ax.tick_params(axis="x", rotation=45)
ax.grid(True, alpha=.25)
save(fig, "08_growth_index.png")

# 9. Cumulative recorded allocation share of the largest departments in the latest year.
conc = latest.groupby("Demand_or_Department")["Total_Cr"].sum(min_count=1).dropna().sort_values(ascending=False)
if not conc.empty and conc.sum() != 0:
    shares = conc / conc.sum() * 100
    cumulative = shares.cumsum().reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(range(1, len(cumulative) + 1), cumulative, marker=".")
    ax.axvline(min(10, len(cumulative)), linestyle="--", linewidth=1)
    ax.set_title(f"Concentration of Recorded Totals — {latest_year}")
    ax.set_xlabel("Departments/demands, ranked by recorded total")
    ax.set_ylabel("Cumulative share (%)")
    ax.set_ylim(0, 102)
    ax.grid(True, alpha=.25)
    save(fig, "09_budget_concentration.png")

# 10. Observed endpoint growth versus variability in available annual totals.
metrics = []
for name, grp in ordered.groupby("Demand_or_Department"):
    s = grp.dropna(subset=["Total_Cr"]).set_index("Financial_Year")["Total_Cr"]
    if len(s) < 3:
        continue
    base_val, end_val = s.iloc[0], s.iloc[-1]
    growth_pct = ((end_val / base_val) - 1) * 100 if base_val != 0 else np.nan
    pct = s.pct_change().replace([np.inf, -np.inf], np.nan).dropna()
    metrics.append({"department": name, "growth_pct": growth_pct,
                    "change_volatility_pct": pct.std() * 100 if len(pct) >= 2 else np.nan,
                    "latest_total": end_val})
m = pd.DataFrame(metrics).dropna(subset=["growth_pct", "change_volatility_pct"])
if not m.empty:
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(m["change_volatility_pct"], m["growth_pct"], alpha=.7)
    labels = m.nlargest(8, "latest_total")
    for _, row in labels.iterrows():
        ax.annotate(row["department"], (row["change_volatility_pct"], row["growth_pct"]), fontsize=7)
    ax.set_title("Departmental Endpoint Growth vs Observed Change Variability")
    ax.set_xlabel("Standard deviation of observed percentage changes (%)")
    ax.set_ylabel("Change from first to last available record (%)")
    ax.grid(True, alpha=.25)
    save(fig, "10_growth_vs_consistency.png")

print(f"Generated exploratory charts in {OUT}. Validate all figures against source PDFs before interpreting.")
