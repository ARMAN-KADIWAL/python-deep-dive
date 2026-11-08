"""Select, filter, modify, group, and sort Pandas DataFrame data."""
import pandas as pd
from csv_operations import create_sample_csv, load_sales_csv


def select_filter_modify(dataframe):
    """Return modified records and grouped summaries."""
    print("Product column:")
    print(dataframe["Product"])
    print("\nProduct and Quantity columns:")
    selected_columns = dataframe[["Product", "Quantity", "Unit_Price"]]
    print(selected_columns)

    print("\nFirst 3 rows using iloc:")
    print(dataframe.iloc[0:3])
    print("\nRows 1-3, columns 1-3 using iloc:")
    print(dataframe.iloc[1:4, 1:4])
    print("\nRows 0-2 using loc:")
    print(dataframe.loc[0:2])

    print("\nProducts with quantity greater than 3:")
    high_quantity = dataframe[dataframe["Quantity"] > 3]
    print(high_quantity)
    print("\nLaptop sales:")
    laptop_sales = dataframe[dataframe["Product"] == "Laptop"]
    print(laptop_sales)
    print("\nLaptop sales with quantity greater than 1:")
    laptop_high_qty = dataframe[
        (dataframe["Product"] == "Laptop") & (dataframe["Quantity"] > 1)
    ]
    print(laptop_high_qty)
    print("\nSales by John or Sarah:")
    specific_reps = dataframe[dataframe["Sales_Rep"].isin(["John", "Sarah"])]
    print(specific_reps)

    modified = dataframe.copy()
    modified["Total_Sales"] = modified["Quantity"] * modified["Unit_Price"]
    modified["Sales_Category"] = modified["Total_Sales"].apply(
        lambda value: "High" if value > 500 else "Medium" if value > 100 else "Low"
    )
    print("\nDataFrame with new Total_Sales column:")
    print(modified.head())
    print("\nDataFrame with Sales_Category column:")
    print(modified[["Product", "Total_Sales", "Sales_Category"]].head())

    modified.loc[modified["Product"] == "Mouse", "Unit_Price"] = 29.99
    modified["Total_Sales"] = modified["Quantity"] * modified["Unit_Price"]
    modified["Sales_Category"] = modified["Total_Sales"].apply(
        lambda value: "High" if value > 500 else "Medium" if value > 100 else "Low"
    )
    print("\nModified Mouse prices:")
    print(modified.loc[modified["Product"] == "Mouse", ["Product", "Unit_Price"]])

    print("\nSales summary by Product:")
    product_summary = modified.groupby("Product").agg({
        "Quantity": "sum",
        "Total_Sales": ["sum", "mean"],
        "Sales_Rep": "count",
    }).round(2)
    print(product_summary)

    print("\nSales summary by Sales Representative:")
    rep_summary = modified.groupby("Sales_Rep")["Total_Sales"].agg(
        ["sum", "count", "mean"]
    ).round(2)
    print(rep_summary)

    print("\nTop 5 sales by total amount:")
    top_sales = modified.nlargest(5, "Total_Sales")[
        ["Date", "Product", "Quantity", "Total_Sales"]
    ]
    print(top_sales)

    return {
        "modified": modified,
        "high_quantity": high_quantity,
        "laptop_sales": laptop_sales,
        "laptop_high_qty": laptop_high_qty,
        "specific_reps": specific_reps,
        "product_summary": product_summary,
        "rep_summary": rep_summary,
        "top_sales": top_sales,
        "selected_columns": selected_columns,
    }


def main():
    create_sample_csv()
    sales = load_sales_csv()
    select_filter_modify(sales)


if __name__ == "__main__":
    main()
