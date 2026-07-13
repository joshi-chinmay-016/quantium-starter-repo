# Quantium Starter Repo

## Overview

This repository contains a small data‑engineering and visualization pipeline built with Python. It demonstrates how to:

1. **Process raw CSV transaction data** – filter for the product "pink morsel", compute sales, and output a cleaned CSV.
2. **Visualize sales data** using a Dash web application, with a line chart and a region filter.
3. **Test the Dash app** with a Pytest suite leveraging `dash.testing`.
4. **Run automated tests in CI** via a bash helper script that activates a virtual environment and returns appropriate exit codes.

All code is written for clarity, with extensive comments and modern styling.

---

## Repository Structure

```
quantium-starter-repo/
│
├─ app.py                # Dash application entry point
├─ run_tests.sh          # CI helper script to run pytest
├─ test_app.py           # Pytest suite for the Dash app
├─ pandas_version.py     # Pandas‑based data‑processing script
├─ csv_version.py        # Pure‑csv (csv module) data‑processing script
├─ formatted_output.csv  # Final merged & cleaned data (output of the scripts)
├─ data/                 # Directory containing the three raw CSV files
├─ requirements.txt      # Python dependencies
└─ README.md             # **This file**
```

---

## 1. Data Processing

Two versions of the processing script are provided:

- **`pandas_version.py`** (recommended) – uses **pandas** for concise data manipulation.
- **`csv_version.py`** – uses the standard library `csv` module for environments without pandas.

Both scripts:
1. Locate all CSV files in `./data`.
2. Keep only rows where the `product` column equals `pink morsel` (case‑insensitive).
3. Compute a new column `sales = quantity * price`.
4. Export only the columns **sales**, **date**, **region** in that exact order to `formatted_output.csv`.

### Running the scripts

```bash
# Create a virtual environment (if you haven't already)
python -m venv venv
source venv/Scripts/activate   # Windows PowerShell / Git Bash

# Install dependencies
pip install -r requirements.txt

# Run the preferred script
python pandas_version.py   # or: python csv_version.py
```

The generated `formatted_output.csv` will be used by the Dash app.

---

## 2. Dash Application (`app.py`)

The app displays a **line chart** of sales over time for the product *Pink Morsel* and adds a **region filter**.

### Features
- **RadioItems** component with options: `north`, `east`, `south`, `west`, and `all`.
- Callback filters the data based on the selected region (or shows all data when `all` is chosen).
- Modern styling using inline CSS (clean, premium look with a dark background, subtle gradients, and smooth hover effects).

### Running the app

```bash
# Ensure the virtual environment is active
source venv/Scripts/activate

# Start the Dash server
python app.py
```

Open your browser at `http://127.0.0.1:8050` to view the dashboard.

---

## 3. Testing (`test_app.py`)

The test suite uses **pytest** together with **dash.testing** (`dash_duo` fixture) and checks:

1. The header element is present.
2. The sales line chart is rendered.
3. The region filter RadioItems component exists.

### Running the tests locally

```bash
source venv/Scripts/activate
pytest
```

---

## 4. CI Helper Script (`run_tests.sh`)

`run_tests.sh` automates the test execution for CI pipelines:

- Detects and activates the virtual environment (`./venv` or `./.venv`).
- Executes `pytest`.
- Returns **exit code 0** on success and **exit code 1** on any failure.

Make it executable and run it:

```bash
chmod +x run_tests.sh
./run_tests.sh
```

The script is already tracked in the repository and can be invoked in GitHub Actions, Azure Pipelines, etc.

---

## 5. Setup & Development Workflow

1. **Clone the repository**
   ```bash
   git clone https://github.com/joshi-chinmay-016/quantium-starter-repo.git
   cd quantium-starter-repo
   ```
2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/Scripts/activate   # PowerShell / Git Bash
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Process the raw CSVs** (produces `formatted_output.csv`)
   ```bash
   python pandas_version.py   # or csv_version.py
   ```
5. **Run the Dash dashboard**
   ```bash
   python app.py
   ```
6. **Run the test suite**
   ```bash
   ./run_tests.sh   # or simply `pytest`
   ```

---

## 6. Contributing

Feel free to fork the repo, open issues, or submit pull requests. When adding new features, consider:
- Writing unit or integration tests.
- Updating the README to reflect changes.
- Maintaining the same coding style and documentation standards.

---

## 7. License

This project is released under the **MIT License** – see the LICENSE file for details.
