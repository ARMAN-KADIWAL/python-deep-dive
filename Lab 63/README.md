# Lab 63 — Data Visualization with Pandas & Matplotlib

Build charts from a **reproducible synthetic sales dataset**: 12 months, three products, marketing spend, and customer counts. A single CLI command generates all plots, correlation tables and a four-panel sales dashboard.

> **Scope:** This is an educational lab with simulated data. Correlation is not causation, and a trend line from 12 observations is not a business-impact estimate.

## What you will learn

| Lab task | Topic | Examples |
|---|---|---|
| 1 | Environment and libraries | Python, NumPy, Pandas, Matplotlib, Seaborn |
| 2 | Basic Pandas charts | Line, multi-line, vertical and horizontal bar |
| 3 | Plot customization | Titles, axis labels, markers, colors, legends and bar labels |
| 4 | Advanced charts | Histograms, scatter plots and linear trend line |
| 5 | Correlation | Pearson correlation matrix, two heatmaps, unique pair strengths |
| 6 | Exports and dashboards | Four-panel dashboard, PNG/JPG/PDF, verification |

## Quick start (Linux, cloud VM, Windows or macOS)

Python 3.9+ recommended. Create and activate a virtual environment:

~~~bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 lab_63.py
~~~

On Windows PowerShell, activate the environment with:

~~~powershell
.venv\Scripts\Activate.ps1
~~~

The script uses Matplotlib's **Agg** backend, so it works without a graphical desktop. Do **not** paste Jupyter's %matplotlib inline into a Python script.

Customize output location or resolution:

~~~bash
python3 lab_63.py --output-dir outputs --dpi 160
python3 lab_63.py --output-dir /tmp/lab63-review --dpi 100
~~~

Results are written under **outputs/** by default. This directory is ignored by Git: generated reports belong in the workflow artifact, not in source control.

## Outputs (18 files)

**Raw data:** sales_data.csv

**Basic charts:** product_a_sales.png, all_products_sales.png, annual_sales_bar.png, marketing_spend_barh.png

**Customized charts:** customized_line_chart.png, customized_bar_chart.png

**Advanced charts:** histograms.png, scatter_plots.png

**Correlation:** correlation_matrix.csv, correlation_heatmaps.png, correlation_strengths.png

**Final deliverables:** sales_dashboard.png, sales_dashboard.jpg, sales_dashboard.pdf, monthly_sales_trends.png, marketing_effectiveness.png, sales_distributions.png

The program validates all expected files, their sizes, and image/PDF signatures before printing success.

## Tests

~~~bash
python3 -m unittest -v test_lab_63.py
~~~

Tests check deterministic data, correlation properties, CLI parameter validation and **end-to-end export of all 18 files**. Continuous integration runs the same checks and uploads the generated charts as a GitHub Actions artifact.

## How to interpret the figures

- **Line charts:** monthly trends within one metric. These are simulated sales amounts.
- **Bar charts:** compare categories and totals on a common scale.
- **Histograms:** show the distribution of numerical observations; bins matter.
- **Scatter plots:** reveal possible linear associations; outliers and small samples matter.
- **Heatmaps:** Pearson r ranges from -1 to +1, with the diagonal equal to +1. A rule of thumb such as |r| > 0.5 is context dependent.
- **Dashboard:** combines different questions into one page for communication, but visual consistency does not validate a causal story.

## Project structure

~~~text
Lab 63/
├── lab_63.py             # Six tasks, reproducible charts and export checks
├── test_lab_63.py        # Unittest suite
├── requirements.txt      # Four plotting/data libraries
├── .gitignore            # Generated assets and environment ignored
└── README.md             # This guide
~~~

**Important:** The GitHub version is a clean, independently reproducible implementation aligned to the lab objectives. It is not an inspected copy of the learner's local lab_63.py.
