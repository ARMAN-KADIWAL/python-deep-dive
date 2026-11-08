"""Create and load the sample sales CSV using Pandas."""
from pathlib import Path
import pandas as pd

SALES_DATA = {
    "Date": [
        "2024-01-15", "2024-01-16", "2024-01-17", "2024-01-18", "2024-01-19",
        "2024-01-20", "2024-01-21", "2024-01-22", "2024-01-23", "2024-01-24",
    ],
    "Product": [
        "Laptop", "Mouse", "Keyboard", "Monitor", "Laptop",
        "Headphones", "Mouse", "Keyboard", "Monitor", "Headphones",
    ],
    "Quantity": [2, 5, 3, 1, 1, 4, 8, 2, 2, 3],
    "Unit_Price": [999.99, 25.99, 79.99, 299.99, 999.99, 149.99, 25.99, 79.99, 299.99, 149.99],
    "Sales_Rep": ["John", "Sarah", "Mike", "Lisa", "John", "Sarah", "Mike", "Lisa", "John", "Sarah"],
}


def create_sample_csv(filepath="sales_data.csv"):
    """Write the sample sales records to a CSV file."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    dataframe = pd.DataFrame(SALES_DATA)
    dataframe.to_csv(path, index=False)
    print(f"Sample CSV file '{path}' created successfully!")
    return path


def load_sales_csv(filepath="sales_data.csv"):
    """Load sales records from a CSV file."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}. Run create_sample_csv() first.")
    dataframe = pd.read_csv(path)
    print("CSV file loaded successfully!")
    print(f"DataFrame shape: {dataframe.shape}")
    return dataframe


def demonstrate_csv_operations(filepath="sales_data.csv"):
    create_sample_csv(filepath)
    dataframe = load_sales_csv(filepath)
    print("\nFirst 5 rows of the sales data:")
    print(dataframe.head())
    print("\nFirst 3 rows of the sales data:")
    print(dataframe.head(3))
    print("\nLast 3 rows of the sales data:")
    print(dataframe.tail(3))
    return dataframe


if __name__ == "__main__":
    demonstrate_csv_operations()
