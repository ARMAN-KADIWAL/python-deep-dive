"""Explore columns, rows, index, data types, and statistics."""
import pandas as pd
from csv_operations import create_sample_csv, load_sales_csv


def explore_dataframe(dataframe):
    print("Column names:")
    print(dataframe.columns.tolist())
    print(f"Number of columns: {len(dataframe.columns)}")
    print("\nColumn information:")
    dataframe.info()

    print(f"\nNumber of rows: {len(dataframe)}")
    print(f"DataFrame shape (rows, columns): {dataframe.shape}")
    print(f"Index: {dataframe.index}")
    if len(dataframe.index):
        print(f"Index range: {dataframe.index[0]} to {dataframe.index[-1]}")

    print("\nData types of each column:")
    print(dataframe.dtypes)
    print("\nBasic statistics for numerical columns:")
    print(dataframe.describe())

    return {
        "columns": dataframe.columns.tolist(),
        "row_count": len(dataframe),
        "column_count": len(dataframe.columns),
        "shape": dataframe.shape,
        "dtypes": dataframe.dtypes.to_dict(),
        "statistics": dataframe.describe(),
    }


def main():
    create_sample_csv()
    sales = load_sales_csv()
    explore_dataframe(sales)


if __name__ == "__main__":
    main()
