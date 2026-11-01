# CO₂ Emissions & Coal Phase-Out in Lusatia (2015–2025)

## Project Overview

This project investigates changes in public net electricity generation in Germany and verified CO₂ emissions from three lignite power plants in Lusatia between 2015 and 2025.

## Key Findings

- Lignite electricity generation decreased by 51.90%.
- Wind electricity generation increased by 65.88%.
- Solar electricity generation increased by 99.16%.
- Combined verified emissions from the three power plants decreased by 42.76%.

## Limitations

- The 2015 electricity dataset is missing the first hour.
- Changes in emissions cannot be attributed solely to coal phase-out policies.
- Plant-level CO₂ intensity was not calculated due to the lack of matching generation data.

## Data Sources

### Electricity Generation
- Source: Fraunhofer ISE Energy-Charts API
- URL: https://api.energy-charts.info/
- Period: 2015–2025
- Country: Germany
- Variables: Lignite, onshore wind, offshore wind, and solar generation

### CO2 Emissions
- Source: European Commission — EU Emissions Trading System (EU ETS)
- URL: https://climate.ec.europa.eu/areas-action/carbon-markets/eu-emissions-trading-system-eu-ets/union-registry_en
- Dataset: Verified Emissions 2025
- Period: 2015–2025
- Power plants: Boxberg, Jänschwalde, Schwarze Pumpe

## Methodology

1. Electricity generation data were retrieved using the Energy-Charts API.
2. Power values (MW) were converted into energy (MWh) using the time interval of each record.
3. Annual electricity generation was calculated in TWh.
4. Verified emissions were extracted from EU ETS installation-level records.
5. Emissions from Boxberg Werk III and Werk IV were combined.
6. Percentage changes between 2015 and 2025 were calculated.
7. Trends were visualized using Matplotlib.

## Results and Visualizations

### 1. Electricity Generation Trends (2015–2025)

![Electricity Generation Trends](figures/generation_trends.png)

### 2. Verified CO2 Emissions in Lusatia

![CO2 Emissions Trends](figures/plant_emissions_trends.png)

### 3. Power Plant Emissions Comparison (2015 vs 2025)

![CO2 Emissions Comparison](figures/plant_emissions_comparison.png)
