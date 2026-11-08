"""Automated tests for Lab 60 Pandas DataFrame exercises."""
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from dataframe_creation import create_product_dataframe, create_student_dataframe
from csv_operations import create_sample_csv, load_sales_csv
from dataframe_exploration import explore_dataframe
from data_selection_filtering import select_filter_modify


class PandasLabTests(unittest.TestCase):
    def test_dataframe_from_dictionary(self):
        students = create_student_dataframe()
        self.assertEqual(students.shape, (5, 5))
        self.assertEqual(students.loc[0, "Name"], "Alice Johnson")
        self.assertAlmostEqual(students.loc[3, "GPA"], 3.9)

    def test_dataframe_from_list_of_lists(self):
        products = create_product_dataframe()
        self.assertEqual(products.shape, (5, 4))
        self.assertEqual(products.loc[0, "Product"], "Laptop")
        self.assertEqual(products.loc[4, "Stock"], 100)

    def test_csv_create_and_load(self):
        with tempfile.TemporaryDirectory() as directory:
            csv_path = Path(directory) / "sales_data.csv"
            created_path = create_sample_csv(csv_path)
            self.assertTrue(created_path.exists())
            sales = load_sales_csv(csv_path)
            self.assertEqual(sales.shape, (10, 5))
            self.assertEqual(sales.iloc[0]["Product"], "Laptop")

    def test_csv_loader_missing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing.csv"
            with self.assertRaises(FileNotFoundError):
                load_sales_csv(missing)

    def test_dataframe_exploration(self):
        sample = pd.DataFrame({"Value": [10, 20, 30], "Label": ["a", "b", "c"]})
        info = explore_dataframe(sample)
        self.assertEqual(info["shape"], (3, 2))
        self.assertEqual(info["columns"], ["Value", "Label"])
        self.assertEqual(info["row_count"], 3)

    def test_selection_and_boolean_filters(self):
        sales = pd.DataFrame({
            "Date": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "Product": ["Laptop", "Mouse", "Laptop"],
            "Quantity": [2, 5, 1],
            "Unit_Price": [999.99, 25.99, 999.99],
            "Sales_Rep": ["John", "Sarah", "Mike"],
        })
        result = select_filter_modify(sales)
        self.assertEqual(len(result["high_quantity"]), 1)
        self.assertEqual(len(result["laptop_sales"]), 2)
        self.assertEqual(len(result["laptop_high_qty"]), 1)
        self.assertEqual(len(result["specific_reps"]), 2)

    def test_mouse_price_and_derived_columns(self):
        sales = pd.DataFrame({
            "Date": ["2024-01-01", "2024-01-02"],
            "Product": ["Mouse", "Laptop"],
            "Quantity": [5, 2],
            "Unit_Price": [25.99, 999.99],
            "Sales_Rep": ["Sarah", "John"],
        })
        result = select_filter_modify(sales)
        modified = result["modified"]
        mouse = modified.loc[modified["Product"] == "Mouse"].iloc[0]
        self.assertAlmostEqual(mouse["Unit_Price"], 29.99)
        self.assertAlmostEqual(mouse["Total_Sales"], 149.95)
        self.assertIn(mouse["Sales_Category"], {"Medium", "High", "Low"})
        self.assertEqual(len(result["top_sales"]), 2)

    def test_groupby_results(self):
        sales = load_sales_csv("sales_data.csv")
        result = select_filter_modify(sales)
        self.assertIn("Laptop", result["product_summary"].index)
        self.assertIn("John", result["rep_summary"].index)
        self.assertEqual(result["product_summary"].loc["Laptop", ("Quantity", "sum")], 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
