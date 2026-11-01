import pandas as pd
import matplotlib.pyplot as plt

annual_results = []

for year in range(2015, 2026):
    df = pd.read_csv(f"data/processed/energy_generation_{year}.csv")

    annual_results.append({
        "year": year,
        "lignite_twh": df["lignite_mwh"].sum() / 1_000_000,
        "wind_twh": df["wind_mwh"].sum() / 1_000_000,
        "solar_twh": df["solar_mwh"].sum() / 1_000_000
    })

annual_df = pd.DataFrame(annual_results)

print(annual_df.round(2))

annual_df.to_csv(
    "data/processed/annual_generation_2015_2025.csv",
    index=False
)

print("Annual summary saved successfully!")

print("\nPercentage change (2015–2025):")

for source in ["lignite", "wind", "solar"]:
    first = annual_df[f"{source}_twh"].iloc[0]
    last = annual_df[f"{source}_twh"].iloc[-1]

    change = (last - first) / first * 100

    print(f"{source}: {change:.2f}%")

plt.figure(figsize=(10, 6))

plt.plot(annual_df["year"], annual_df["lignite_twh"],
         marker="o", label="Lignite")

plt.plot(annual_df["year"], annual_df["wind_twh"],
         marker="o", label="Wind")

plt.plot(annual_df["year"], annual_df["solar_twh"],
         marker="o", label="Solar")

plt.title("Public Net Electricity Generation in Germany (2015–2025)")
plt.xlabel("Year")
plt.ylabel("Electricity Generation (TWh)")

plt.xticks(annual_df["year"])
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("figures/generation_trends.png", dpi=300)
plt.show()