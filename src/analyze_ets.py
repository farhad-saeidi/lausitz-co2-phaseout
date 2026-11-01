import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

file = next(Path("data/raw/eu_ets").rglob("verified_emissions_2025_en*.xlsx"))

df = pd.read_excel(file, sheet_name="data", header=2)

plant_ids = ["1453", "1454", "1456", "1459"]

plants = df[
    (df["REGISTRY_CODE"] == "DE") &
    (df["INSTALLATION_IDENTIFIER"].astype(str).isin(plant_ids))
]

print(plants[[
    "INSTALLATION_NAME",
    "INSTALLATION_IDENTIFIER",
    "VERIFIED_EMISSIONS_2025"
]].to_string(index=False))

emission_columns = [
    col for col in df.columns
    if str(col).startswith("VERIFIED_EMISSIONS_")
]

print("\nAvailable emission columns:")
print(emission_columns)
columns = [
    f"VERIFIED_EMISSIONS_{year}"
    for year in range(2015, 2026)
]

emissions = plants.set_index("INSTALLATION_NAME")[columns].T

emissions.index = range(2015, 2026)

emissions = emissions.apply(pd.to_numeric, errors="coerce")

print("\nAnnual verified emissions (tonnes CO2e):")
print(emissions.to_string())

print("\nMissing values:")
print(emissions.isna().sum())
annual_emissions = pd.DataFrame(index=emissions.index)

annual_emissions["boxberg_mt"] = (
    emissions["Kraftwerk Boxberg Werk III"]
    + emissions["Kraftwerk Boxberg Werk IV"]
) / 1_000_000

annual_emissions["jaenschwalde_mt"] = (
    emissions["Kraftwerk Jänschwalde"] / 1_000_000
)

annual_emissions["schwarze_pumpe_mt"] = (
    emissions["Kraftwerk Schwarze Pumpe"] / 1_000_000
)

annual_emissions.index.name = "year"

print("\nAnnual CO2 emissions (Mt):")
print(annual_emissions.round(2))
annual_emissions["total_mt"] = annual_emissions.sum(axis=1)

annual_emissions.to_csv(
    "data/processed/annual_plant_emissions_2015_2025.csv"
)

print("\nTotal annual CO2 emissions (Mt):")
print(annual_emissions["total_mt"].round(2))

print("\nCSV saved successfully!")

print("\nCO2 emissions change (2015–2025):")

for plant in ["boxberg_mt", "jaenschwalde_mt", "schwarze_pumpe_mt", "total_mt"]:
    first = annual_emissions.loc[2015, plant]
    last = annual_emissions.loc[2025, plant]

    change = (last - first) / first * 100

    print(f"{plant}: {change:.2f}%")

plt.figure(figsize=(10, 6))

plt.plot(annual_emissions.index,
         annual_emissions["boxberg_mt"],
         marker="o", label="Boxberg")

plt.plot(annual_emissions.index,
         annual_emissions["jaenschwalde_mt"],
         marker="o", label="Jaenschwalde")

plt.plot(annual_emissions.index,
         annual_emissions["schwarze_pumpe_mt"],
         marker="o", label="Schwarze Pumpe")

plt.title("Verified CO2 Emissions in Lusatia (2015–2025)")
plt.xlabel("Year")
plt.ylabel("Verified Emissions (Mt CO2e)")

plt.xticks(annual_emissions.index)
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("figures/plant_emissions_trends.png", dpi=300)
plt.show()

comparison = annual_emissions.loc[
    [2015, 2025],
    ["boxberg_mt", "jaenschwalde_mt", "schwarze_pumpe_mt"]
].T

comparison.index = ["Boxberg", "Jaenschwalde", "Schwarze Pumpe"]

comparison.plot(kind="bar", figsize=(9, 5), rot=0)

plt.title("Power Plant CO2 Emissions: 2015 vs 2025")
plt.xlabel("Power Plant")
plt.ylabel("Verified Emissions (Mt CO2e)")
plt.legend(title="Year")
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("figures/plant_emissions_comparison.png", dpi=300)
plt.show()