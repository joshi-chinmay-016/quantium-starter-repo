#!/usr/bin/env python3
"""
Robust CSV‑only data‑processing script.

Adds diagnostics and removes the leading '$' from the price column
so conversion to float succeeds.
"""

import csv
import pathlib
import sys
from typing import List, Dict

DATA_DIR = pathlib.Path(__file__).parent / "data"
OUTPUT_FILE = pathlib.Path(__file__).parent / "formatted_output.csv"


def read_csv(path: pathlib.Path) -> List[Dict[str, str]]:
    """Read a CSV file and return rows as dictionaries."""
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def filter_and_transform(rows: List[Dict[str, str]], src_name: str) -> List[Dict[str, str]]:
    """Apply the filtering logic with detailed diagnostics."""
    kept = []
    total = len(rows)
    kept_cnt = 0

    for i, row in enumerate(rows, start=1):
        # Verify required columns exist
        missing = [k for k in ("product", "quantity", "price", "date", "region") if k not in row]
        if missing:
            print(f"[{src_name}] Row {i}/{total}: missing columns {missing} → skipped")
            continue

        # Keep only pink morsel (case‑insensitive)
        if row["product"].strip().lower() != "pink morsel":
            continue

        try:
            quantity = float(row["quantity"])
            # Strip leading '$' if present before conversion
            price_str = row["price"].replace("$", "").strip()
            price = float(price_str)
        except ValueError:
            print(f"[{src_name}] Row {i}: non‑numeric quantity/price → skipped")
            continue

        sales = quantity * price
        kept.append(
            {
                "sales": f"{sales:.2f}",
                "date": row["date"],
                "region": row["region"],
            }
        )
        kept_cnt += 1

    print(f"[{src_name}] Processed {total} rows – kept {kept_cnt}")
    return kept


def write_output(all_rows: List[Dict[str, str]]) -> None:
    """Write the merged output CSV."""
    fieldnames = ["sales", "date", "region"]
    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)


def main() -> None:
    csv_paths = list(DATA_DIR.glob("*.csv"))
    if not csv_paths:
        print(f"No CSV files found in {DATA_DIR}")
        sys.exit(1)

    merged: List[Dict[str, str]] = []
    for p in csv_paths:
        rows = read_csv(p)
        merged.extend(filter_and_transform(rows, p.name))

    write_output(merged)
    print(f"\n✅ Finished – {len(merged)} rows written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
