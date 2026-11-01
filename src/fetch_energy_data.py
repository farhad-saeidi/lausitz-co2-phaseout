import requests
import pandas as pd

url = "https://api.energy-charts.info/v2/public_power"

for year in range(2019, 2025):
    print(f"\nProcessing year: {year}")
    params = {
        "country": "de",
        "start": f"{year}-01-01",
        "end": f"{year}-12-31"
    }

    response = requests.get(url, params=params, timeout=30)

    print(response.status_code)

    data = response.json()

    print(data.keys())
    print("Unit:", data["unit"])
    print("Resolution:", data["resolution"])
    print("Series type:", type(data["series"]))
    print("Number of series:", len(data["series"]))

    print("\nFirst 5 energy series:")
    for series in data["series"][:5]:
        print(series)

    print("\nFirst data record:")
    print(data["data"][0])
    values = data["data"][0]["values"]

    lignite = values["fossil_brown_coal_lignite"]
    wind = values["wind_onshore"] + values["wind_offshore"]
    solar = values["solar"]

    print("\nElectricity generation (MW):")
    print("Lignite:", lignite)
    print("Wind:", wind)
    print("Solar:", solar)
    records = []

    for row in data["data"]:
        values = row["values"]

        records.append({
            "timestamp": row["timestamp"],
            "lignite_mw": values["fossil_brown_coal_lignite"],
            "wind_mw": values["wind_onshore"] + values["wind_offshore"],
            "solar_mw": values["solar"]
        })

    df = pd.DataFrame(records)

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nDataFrame shape:")
    print(df.shape)

    # p(mw) * 0.25h(15m=0.25h) = E(mwh)
    interval_hours = data["interval_minutes"] / 60

    df["lignite_mwh"] = df["lignite_mw"] * interval_hours
    df["wind_mwh"] = df["wind_mw"] * interval_hours
    df["solar_mwh"] = df["solar_mw"] * interval_hours

    print("\nElectricity generation in MWh:")
    print(df[["timestamp", "lignite_mwh", "wind_mwh", "solar_mwh"]].head())
    total_lignite = df["lignite_mwh"].sum()
    total_wind = df["wind_mwh"].sum()
    total_solar = df["solar_mwh"].sum()

    print("\nTotal electricity generation (MWh):")
    print("Lignite:", round(total_lignite, 2))
    print("Wind:", round(total_wind, 2))
    print("Solar:", round(total_solar, 2))
    print("\nTotal electricity generation:")

    for source in ["lignite", "wind", "solar"]:
        total_mwh = df[f"{source}_mwh"].sum()

        total_gwh = total_mwh / 1000
        total_twh = total_mwh / 1_000_000

        print(f"{source}: {total_gwh:.2f} GWh | {total_twh:.4f} TWh")

        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

    print("\nMissing values:")
    print(df.isna().sum())

    print("\nDuplicate timestamps:")
    print(df["timestamp"].duplicated().sum())

    print("\nTime gaps:")
    time_gaps = df["timestamp"].sort_values().diff().dropna()
    print((time_gaps != pd.Timedelta(minutes=data["interval_minutes"])).sum())

    df.to_csv(f"data/processed/energy_generation_{year}.csv", index=False)

    print("\nCSV file saved successfully!")
    print("\nData coverage:")
    print("First timestamp:", df["timestamp"].min())
    print("Last timestamp:", df["timestamp"].max())
    print("Available from:", data["available_from"])
    print("Available until:", data["available_until"])