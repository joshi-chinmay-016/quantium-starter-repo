#!/usr/bin/env python3
"""
Robust pandas version with diagnostics.

Removes the leading '$' from the price column before conversion.
"""

import pathlib
import sys

import pandas as pd

DATA_DIR = pathlib.Path(__file__).parent / "data"
OUTPUT_FILE = pathlib.Path(__file__).parent / "formatted_output.csv"


def main() -> None:
    csv_paths = list(DATA_DIR.glob("*.csv"))
    if not csv_paths:
        print(f"No CSV files found in {DATA_DIR}")
        sys.exit(1)

    # Load each CSV separately so we can report per‑file row counts
    df_list = []
    for p in csv_paths:
        df = pd.read_csv(p)
        print(f"[{p.name}] Loaded {len(df)} rows")
        df_list.append(df)

    df = pd.concat(df_list, ignore_index=True)
    print(f"\nCombined dataframe size: {len(df)} rows")

    # 1️⃣ Filter product
    mask = df["product"].str.strip().str.lower() == "pink morsel"
    print(f"Rows matching product 'pink morsel': {mask.sum()}")
    df = df[mask]

    # 2️⃣ Clean price column (remove $) and convert to numeric
    df["price"] = df["price"].astype(str).str.replace("$", "", regex=False)
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    before_drop = len(df)
    df = df.dropna(subset=["quantity", "price"])
    print(f"Dropped {before_drop - len(df)} rows with invalid quantity/price")

    # 3️⃣ Compute sales
    df["sales"] = df["quantity"] * df["price"]
    print(f"Computed sales for {len(df)} rows")

    # 4️⃣ Keep only required columns in the exact order
    final_df = df[["sales", "date", "region"]].copy()
    final_df["sales"] = final_df["sales"].round(2)

    final_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n✅ Finished – {len(final_df)} rows written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
