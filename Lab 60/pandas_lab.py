#!/usr/bin/env python3
"""Lab 60: Introduction to Pandas - Working with DataFrames."""
import numpy as np
import pandas as pd

from dataframe_creation import create_product_dataframe, create_student_dataframe
from csv_operations import create_sample_csv, load_sales_csv
from dataframe_exploration import explore_dataframe
from data_selection_filtering import select_filter_modify


def main():
    print("=" * 60)
    print("Lab 60: Introduction to Pandas - Working with DataFrames")
    print("=" * 60)

    print(f"\nPandas version: {pd.__version__}")
    print(f"NumPy version: {np.__version__}")
    print("Pandas imported successfully!")

    print("\n" + "=" * 50)
    print("TASK 2: Creating DataFrames")
    print("=" * 50)
    print("\nDataFrame from dictionary:")
    print(create_student_dataframe())
    print("\nDataFrame from list of lists:")
    print(create_product_dataframe())

    print("\n" + "=" * 50)
    print("TASK 3: CSV File Operations")
    print("=" * 50)
    create_sample_csv()
    sales = load_sales_csv()
    print("\nFirst 5 rows:")
    print(sales.head())
    print("\nFirst 3 rows:")
    print(sales.head(3))
    print("\nLast 3 rows:")
    print(sales.tail(3))

    print("\n" + "=" * 50)
    print("TASK 4: DataFrame Attributes")
    print("=" * 50)
    explore_dataframe(sales)

    print("\n" + "=" * 50)
    print("TASK 5: Data Selection, Filtering, and Modification")
    print("=" * 50)
    select_filter_modify(sales)

    print("\n" + "=" * 60)
    print("Lab completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
