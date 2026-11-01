from pathlib import Path
import pandas as pd

files = list(Path("data/raw/eu_ets").rglob("CITL*.xlsx"))

for file in files:
    print("File:", file.name)

    excel = pd.ExcelFile(file)
    print("Sheets:", excel.sheet_names)
    df = pd.read_excel(file, sheet_name="Sheet1", nrows=5)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.to_string(index=False))    