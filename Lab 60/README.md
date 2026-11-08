# Lab 60: Introduction to Pandas - Working with DataFrames

## Objectives
- Install and import Pandas and NumPy.
- Create DataFrames from dictionaries and lists of lists.
- Create, save, and load CSV data with Pandas.
- Explore DataFrame columns, rows, index, shape, data types, and statistics.
- Select data using column names, `iloc`, and `loc`.
- Filter rows using boolean conditions and `isin()`.
- Add columns, modify values, group data, calculate summaries, and sort top records.

## Requirements
Python 3.8+.

Install packages:

    python3 -m pip install -r requirements.txt

If your Linux environment blocks global pip installation, use a virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt

## Files
- `pandas_lab.py`: complete end-to-end lab script.
- `dataframe_creation.py`: DataFrames from a dictionary and list of lists.
- `csv_operations.py`: create and load the sample sales CSV.
- `dataframe_exploration.py`: inspect DataFrame structure and statistics.
- `data_selection_filtering.py`: column selection, loc/iloc, filtering, modification, grouping, and top sales.
- `sales_data.csv`: sample sales dataset with 10 rows.
- `requirements.txt`: Pandas and NumPy dependencies.
- `test_lab60.py`: automated tests.

## Run the complete lab

    python3 pandas_lab.py

Run individual tasks from this directory:

    python3 dataframe_creation.py
    python3 csv_operations.py
    python3 dataframe_exploration.py
    python3 data_selection_filtering.py

The CSV task writes `sales_data.csv` in the current working directory. The supplied CSV is included so that the data can also be inspected or loaded directly.

## Run automated tests

    python3 -m unittest -v

## Key concepts
- `DataFrame`: Pandas two-dimensional labelled table.
- `head()` / `tail()`: preview the first or last rows.
- `columns`, `shape`, `index`, `dtypes`, `describe()`, and `info()`: DataFrame inspection.
- `iloc`: integer-position indexing.
- `loc`: label-based indexing.
- Boolean indexing and `isin()`: filter rows.
- `groupby()` and `agg()`: group records and calculate summaries.

## Implementation note
The lab updates Mouse unit prices to 29.99 and then recalculates the derived `Total_Sales` and `Sales_Category` columns, ensuring the summaries use the updated price values.
