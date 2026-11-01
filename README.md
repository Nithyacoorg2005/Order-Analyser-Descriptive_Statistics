# Order Analyzer Pipeline

A robust, modular, configuration-driven Python pipeline designed to perform automated descriptive analytics on transactional data. This engine ingests raw order exports, calculates key statistical metrics (central tendency, dispersion, percentile-based VIP tiers), generates visual charts, and compiles a daily executive health report.

## Features

* **Decoupled Architecture:** Separation of concerns across data ingestion (`data_loader`), mathematics (`calculator`), and charting (`visualizer`).

* **Configuration-Driven:** All schema mappings, file paths, and logging settings are centrally managed via `config.yaml`, requiring zero code changes to swap datasets.

* **Automated Reporting:** Dynamically generates human-readable Markdown (`.md`) reports summarizing total revenue, average order values, and category breakdowns.

* **Visual Asset Generation:** Automatically outputs high-resolution Seaborn and Matplotlib charts (Distribution, Box Plots, and Category Revenue).

* **Environment Optimized:** Built and tested for native Windows execution via the MSYS2/UCRT64 environment.

## Project Structure

```
Order-Analyser/
├── data/
│   └── raw/                    # Drop raw CSV exports here (e.g., daily_orders.csv)
├── outputs/
│   ├── charts/                 # Auto-generated .png visual assets
│   └── reports/                # Auto-generated .md daily health reports
├── src/
│   ├── __init__.py
│   ├── data_loader.py          # Handles CSV ingestion and datetime parsing
│   ├── calculator.py           # Descriptive statistics and percentile engine
│   └── visualizer.py           # Matplotlib/Seaborn charting logic
├── config.yaml                 # Centralized configuration and schema mapping
├── main.py                     # Pipeline orchestrator
└── requirements.txt            # Dependency list

```

## Environment Setup (MSYS2 / UCRT64)

This project utilizes heavy data science libraries that require C++ compilation. For Windows users utilizing the **MSYS2 MinGW-w64 (UCRT64)** environment, it is highly recommended to use pre-compiled system binaries to avoid `lto-wrapper` and `COFF object format mismatch` compilation failures.

**1. Install System-Level Dependencies via Pacman**
Open your MSYS2 UCRT64 terminal and run:

```
pacman -S mingw-w64-ucrt-x86_64-python-pandas mingw-w64-ucrt-x86_64-python-numpy mingw-w64-ucrt-x86_64-python-matplotlib mingw-w64-ucrt-x86_64-python-seaborn mingw-w64-ucrt-x86_64-python-yaml

```

**2. Create an Environment with System Site-Packages**
Create an isolated virtual environment that inherits the pre-compiled C++ binaries:

```
python -m venv venv --system-site-packages

```

**3. Activate the Environment**

```
source venv/bin/activate

```

## Configuration

Before running the pipeline, map your specific CSV headers to the engine using `config.yaml`.

```
# config.yaml
data_schema:
  id_column: "Order ID"
  date_columns: 
    - "Order Time"
  category_column: "Category"
  value_column: "Price"

analysis:
  vip_percentiles: [50, 75, 90, 99] # Used for calculating spend thresholds

```

## Usage

With your virtual environment active and your configuration set, execute the orchestrator script:

```
python main.py

```

**Execution Flow:**

1. **Initialization:** Reads `config.yaml` and initializes the custom logger.

2. **Ingestion:** Loads the target CSV from `data/raw/`.

3. **Calculation:** Computes total revenue, means, medians, and percentile tiers.

4. **Visualization:** Saves `distribution.png`, `outliers_box.png`, and `category_revenue.png`.

5. **Reporting:** Compiles all math and file paths into a dated `.md` report.

## Expected Outputs

Upon successful execution, check the `outputs/` directory.

**1. Daily Markdown Report (`outputs/reports/health_report_YYYYMMDD.md`)**
Provides a clean, readable executive summary of the day's transactions, perfect for pasting into Notion, Slack, or a command center dashboard.

**2. Visual Assets (`outputs/charts/`)**

* `distribution.png`: Histogram visualizing the spread of order values.

* `outliers_box.png`: Box plot identifying median values and high-ticket outlier purchases.

* `category_revenue.png`: Bar chart breaking down total revenue by category.

## Logging

All pipeline events, warnings, and errors are logged both to the terminal console and to a persistent log file (configurable in `config.yaml`, defaulting to `logs/pipeline.log`).