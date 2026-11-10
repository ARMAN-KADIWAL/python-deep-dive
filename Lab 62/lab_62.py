"""Lab 62: Advanced Pandas Operations - Merging and Grouping Data.

Runnable examples adapted from the supplied Lab 62 handout. The handout's
troubleshooting snippets use intentionally undefined placeholders (df1,
large_file.csv, multi_index_df); those are not part of this executable lab.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def run_lab(output_dir: str | Path | None = None) -> dict[str, pd.DataFrame | pd.Series]:
    """Execute all five tasks and comprehensive analysis, optionally exporting CSVs."""

    # Task 1 - Merging DataFrames

    # Example 1
    # Create a DataFrame with customer information
    customers_df = pd.DataFrame({
        'customer_id': [101, 102, 103, 104, 105],
        'customer_name': ['Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson', 'Eva Brown'],
        'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
        'age': [28, 35, 42, 31, 29]
    })

    # Create a DataFrame with order information
    orders_df = pd.DataFrame({
        'order_id': [1001, 1002, 1003, 1004, 1005, 1006],
        'customer_id': [101, 102, 101, 103, 104, 102],
        'product': ['Laptop', 'Phone', 'Tablet', 'Laptop', 'Phone', 'Headphones'],
        'amount': [1200, 800, 400, 1200, 800, 150],
        'order_date': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19', '2024-01-20']
    })

    print("Customers DataFrame:")
    print(customers_df)
    print("\nOrders DataFrame:")
    print(orders_df)


    # Example 2
    # Inner join - only customers who have placed orders
    inner_merged = pd.merge(customers_df, orders_df, on='customer_id', how='inner')

    print("Inner Join Result:")
    print(inner_merged)
    print(f"\nShape: {inner_merged.shape}")


    # Example 3
    # Left join - all customers, with order info where available
    left_merged = pd.merge(customers_df, orders_df, on='customer_id', how='left')

    print("Left Join Result:")
    print(left_merged)
    print(f"\nShape: {left_merged.shape}")


    # Example 4
    # Right join - all orders, with customer info where available
    right_merged = pd.merge(customers_df, orders_df, on='customer_id', how='right')

    print("Right Join Result:")
    print(right_merged)
    print(f"\nShape: {right_merged.shape}")


    # Example 5
    # Outer join - all customers and all orders
    outer_merged = pd.merge(customers_df, orders_df, on='customer_id', how='outer')

    print("Outer Join Result:")
    print(outer_merged)
    print(f"\nShape: {outer_merged.shape}")



    # Task 2 - Concatenating DataFrames

    # Example 6
    # Create DataFrames representing sales data from different quarters
    q1_sales = pd.DataFrame({
        'month': ['Jan', 'Feb', 'Mar'],
        'sales': [50000, 55000, 48000],
        'quarter': ['Q1', 'Q1', 'Q1']
    })

    q2_sales = pd.DataFrame({
        'month': ['Apr', 'May', 'Jun'],
        'sales': [52000, 58000, 61000],
        'quarter': ['Q2', 'Q2', 'Q2']
    })

    q3_sales = pd.DataFrame({
        'month': ['Jul', 'Aug', 'Sep'],
        'sales': [63000, 59000, 57000],
        'quarter': ['Q3', 'Q3', 'Q3']
    })

    print("Q1 Sales:")
    print(q1_sales)
    print("\nQ2 Sales:")
    print(q2_sales)
    print("\nQ3 Sales:")
    print(q3_sales)


    # Example 7
    # Concatenate vertically (stack rows on top of each other)
    yearly_sales = pd.concat([q1_sales, q2_sales, q3_sales], ignore_index=True)

    print("Yearly Sales (Vertical Concatenation):")
    print(yearly_sales)
    print(f"\nShape: {yearly_sales.shape}")


    # Example 8
    # Create DataFrames with different metrics for the same months
    revenue_data = pd.DataFrame({
        'month': ['Jan', 'Feb', 'Mar'],
        'revenue': [45000, 50000, 43000]
    })

    expense_data = pd.DataFrame({
        'month': ['Jan', 'Feb', 'Mar'],
        'expenses': [30000, 32000, 28000]
    })

    # Concatenate horizontally (side by side)
    financial_data = pd.concat([revenue_data, expense_data], axis=1)

    print("Financial Data (Horizontal Concatenation):")
    print(financial_data)

    # Remove duplicate month column
    financial_data_clean = financial_data.loc[:, ~financial_data.columns.duplicated()]
    print("\nCleaned Financial Data:")
    print(financial_data_clean)


    # Example 9
    # Add keys to identify the source of each DataFrame
    sales_with_keys = pd.concat([q1_sales, q2_sales, q3_sales], keys=['Quarter1', 'Quarter2', 'Quarter3'])

    print("Sales Data with Keys:")
    print(sales_with_keys)
    print(f"\nIndex levels: {sales_with_keys.index.nlevels}")



    # Task 3 - Grouping and Aggregation

    # Example 10
    # Create a comprehensive sales dataset
    sales_data = pd.DataFrame({
        'salesperson': ['John', 'Sarah', 'Mike', 'John', 'Sarah', 'Mike', 'John', 'Sarah', 'Mike', 'John'],
        'region': ['North', 'South', 'East', 'North', 'South', 'East', 'North', 'South', 'East', 'North'],
        'product_category': ['Electronics', 'Clothing', 'Electronics', 'Clothing', 'Electronics', 'Clothing', 'Electronics', 'Clothing', 'Electronics', 'Clothing'],
        'sales_amount': [1500, 800, 2200, 1200, 950, 1800, 1700, 750, 2100, 1300],
        'units_sold': [3, 8, 4, 6, 5, 9, 3, 7, 4, 5],
        'month': ['Jan', 'Jan', 'Jan', 'Feb', 'Feb', 'Feb', 'Mar', 'Mar', 'Mar', 'Apr']
    })

    print("Sales Dataset:")
    print(sales_data)


    # Example 11
    # Group by salesperson and calculate total sales
    sales_by_person = sales_data.groupby('salesperson')['sales_amount'].sum()

    print("Total Sales by Salesperson:")
    print(sales_by_person)
    print(f"\nData type: {type(sales_by_person)}")

    # Convert to DataFrame for better formatting
    sales_by_person_df = sales_by_person.reset_index()
    print("\nAs DataFrame:")
    print(sales_by_person_df)


    # Example 12
    # Apply multiple aggregation functions
    sales_summary = sales_data.groupby('salesperson')['sales_amount'].agg(['sum', 'mean', 'count', 'min', 'max'])

    print("Sales Summary by Salesperson:")
    print(sales_summary)

    # Round the mean for better readability
    sales_summary['mean'] = sales_summary['mean'].round(2)
    print("\nRounded Sales Summary:")
    print(sales_summary)


    # Example 13
    # Group by multiple columns
    region_product_sales = sales_data.groupby(['region', 'product_category'])['sales_amount'].agg(['sum', 'mean', 'count'])

    print("Sales by Region and Product Category:")
    print(region_product_sales)

    # Reset index to make it easier to work with
    region_product_flat = region_product_sales.reset_index()
    print("\nFlattened Version:")
    print(region_product_flat)


    # Example 14
    # Define custom aggregation functions
    def sales_range(series):
        return series.max() - series.min()

    def top_performer_indicator(series):
        return "High" if series.sum() > 4000 else "Standard"

    # Apply custom functions
    custom_agg = sales_data.groupby('salesperson')['sales_amount'].agg([
        'sum',
        'mean',
        ('range', sales_range),
        ('performance', top_performer_indicator)
    ])

    print("Custom Aggregation Results:")
    print(custom_agg)



    # Task 4 - Pivot Tables

    # Example 15
    # Create a basic pivot table
    basic_pivot = sales_data.pivot_table(
        values='sales_amount',
        index='salesperson',
        columns='region',
        aggfunc='sum'
    )

    print("Basic Pivot Table - Sales Amount by Salesperson and Region:")
    print(basic_pivot)

    # Fill NaN values with 0 for better readability
    basic_pivot_filled = basic_pivot.fillna(0)
    print("\nPivot Table with NaN filled:")
    print(basic_pivot_filled)


    # Example 16
    # Pivot table with multiple value columns
    multi_value_pivot = sales_data.pivot_table(
        values=['sales_amount', 'units_sold'],
        index='salesperson',
        columns='region',
        aggfunc='sum',
        fill_value=0
    )

    print("Multi-Value Pivot Table:")
    print(multi_value_pivot)


    # Example 17
    # Pivot table with different aggregation functions
    multi_agg_pivot = sales_data.pivot_table(
        values='sales_amount',
        index='salesperson',
        columns='product_category',
        aggfunc=['sum', 'mean', 'count'],
        fill_value=0
    )

    print("Multi-Aggregation Pivot Table:")
    print(multi_agg_pivot)


    # Example 18
    # Pivot table with row and column totals
    pivot_with_totals = sales_data.pivot_table(
        values='sales_amount',
        index='salesperson',
        columns='region',
        aggfunc='sum',
        fill_value=0,
        margins=True,
        margins_name='Total'
    )

    print("Pivot Table with Totals:")
    print(pivot_with_totals)


    # Example 19
    # Create a more complex pivot table for monthly analysis
    monthly_pivot = sales_data.pivot_table(
        values=['sales_amount', 'units_sold'],
        index=['month', 'salesperson'],
        columns='product_category',
        aggfunc={'sales_amount': 'sum', 'units_sold': 'sum'},
        fill_value=0
    )

    print("Monthly Sales Analysis Pivot Table:")
    print(monthly_pivot)

    # Calculate average sales per unit
    monthly_pivot_copy = monthly_pivot.copy()
    print("\nAverage Price per Unit Analysis:")
    for category in ['Clothing', 'Electronics']:
        if ('sales_amount', category) in monthly_pivot_copy.columns and ('units_sold', category) in monthly_pivot_copy.columns:
            avg_price = monthly_pivot_copy[('sales_amount', category)] / monthly_pivot_copy[('units_sold', category)]
            avg_price = avg_price.replace([np.inf, -np.inf], 0)  # Handle division by zero
            print(f"\nAverage price per unit - {category}:")
            print(avg_price.round(2))



    # Task 5 - MultiIndex

    # Example 20
    # Create a multi-index DataFrame from scratch
    arrays = [
        ['Store A', 'Store A', 'Store A', 'Store B', 'Store B', 'Store B'],
        ['Electronics', 'Clothing', 'Books', 'Electronics', 'Clothing', 'Books']
    ]

    multi_index = pd.MultiIndex.from_arrays(arrays, names=['Store', 'Department'])

    sales_multi = pd.DataFrame({
        'Q1_Sales': [15000, 8000, 5000, 18000, 9000, 4500],
        'Q2_Sales': [16000, 8500, 5200, 19000, 9500, 4800],
        'Q3_Sales': [17000, 9000, 5500, 20000, 10000, 5000],
        'Q4_Sales': [18000, 9500, 5800, 21000, 10500, 5200]
    }, index=multi_index)

    print("Multi-Index DataFrame:")
    print(sales_multi)


    # Example 21
    # Access data using multi-index
    print("All data for Store A:")
    print(sales_multi.loc['Store A'])

    print("\nElectronics department data for all stores:")
    print(sales_multi.loc[(slice(None), 'Electronics'), :])

    print("\nSpecific cell - Store B, Clothing, Q2_Sales:")
    print(sales_multi.loc[('Store B', 'Clothing'), 'Q2_Sales'])


    # Example 22
    # Calculate total sales across all quarters
    sales_multi['Total_Sales'] = sales_multi.sum(axis=1)

    print("DataFrame with Total Sales:")
    print(sales_multi)

    # Group by store level
    store_totals = sales_multi.groupby(level='Store').sum()
    print("\nTotals by Store:")
    print(store_totals)

    # Group by department level
    dept_totals = sales_multi.groupby(level='Department').sum()
    print("\nTotals by Department:")
    print(dept_totals)


    # Example 23
    # Stack and unstack operations
    stacked = sales_multi.stack()
    print("Stacked DataFrame:")
    print(stacked.head(10))

    # Unstack to create a different view
    unstacked = sales_multi.unstack(level='Department')
    print("\nUnstacked DataFrame:")
    print(unstacked)


    # Example 24
    # Create multi-index using pivot_table
    pivot_multi = sales_data.pivot_table(
        values=['sales_amount', 'units_sold'],
        index=['region', 'salesperson'],
        columns='month',
        aggfunc='sum',
        fill_value=0
    )

    print("Multi-Index Pivot Table:")
    print(pivot_multi)

    # Access specific levels
    print("\nSales amount data only:")
    print(pivot_multi['sales_amount'])

    print("\nNorth region data only:")
    print(pivot_multi.loc['North'])



    # Practical Exercise - Comprehensive Retail Analysis

    # Example 25
    # Create a comprehensive retail dataset
    np.random.seed(42)  # For reproducible results

    retail_data = pd.DataFrame({
        'transaction_id': range(1001, 1101),
        'customer_id': np.random.choice(range(1, 21), 100),
        'product_category': np.random.choice(['Electronics', 'Clothing', 'Books', 'Home'], 100),
        'store_location': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston'], 100),
        'sales_amount': np.random.uniform(10, 500, 100).round(2),
        'quantity': np.random.randint(1, 10, 100),
        'discount_percent': np.random.choice([0, 5, 10, 15, 20], 100),
        'month': np.random.choice(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], 100)
    })

    # Create customer demographics
    customer_demographics = pd.DataFrame({
        'customer_id': range(1, 21),
        'age_group': np.random.choice(['18-25', '26-35', '36-45', '46-55', '55+'], 20),
        'gender': np.random.choice(['Male', 'Female'], 20),
        'membership_level': np.random.choice(['Bronze', 'Silver', 'Gold'], 20)
    })

    print("Retail Transaction Data (first 10 rows):")
    print(retail_data.head(10))
    print("\nCustomer Demographics:")
    print(customer_demographics.head(10))


    # Example 26
    # Step 1: Merge transaction data with customer demographics
    complete_data = pd.merge(retail_data, customer_demographics, on='customer_id', how='left')

    print("Merged Dataset (first 5 rows):")
    print(complete_data.head())

    # Step 2: Create summary statistics by multiple dimensions
    summary_analysis = complete_data.groupby(['store_location', 'product_category']).agg({
        'sales_amount': ['sum', 'mean', 'count'],
        'quantity': 'sum',
        'discount_percent': 'mean'
    }).round(2)

    print("\nSummary Analysis by Store and Category:")
    print(summary_analysis)

    # Step 3: Create a comprehensive pivot table
    comprehensive_pivot = complete_data.pivot_table(
        values=['sales_amount', 'quantity'],
        index=['store_location', 'product_category'],
        columns='membership_level',
        aggfunc='sum',
        fill_value=0,
        margins=True
    )

    print("\nComprehensive Pivot Analysis:")
    print(comprehensive_pivot)

    # Step 4: Monthly trend analysis
    monthly_trends = (complete_data.groupby(['month', 'store_location'])['sales_amount']
        .sum().unstack(fill_value=0)
        .reindex(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], fill_value=0))

    print("\nMonthly Sales Trends by Store:")
    print(monthly_trends)

    # Step 5: Customer segmentation analysis
    customer_analysis = complete_data.groupby(['age_group', 'gender']).agg({
        'sales_amount': ['sum', 'mean'],
        'transaction_id': 'count'
    }).round(2)

    customer_analysis.columns = ['Total_Sales', 'Avg_Transaction', 'Transaction_Count']
    print("\nCustomer Segmentation Analysis:")
    print(customer_analysis)

    # Demonstrate valid cross-section rather than undefined placeholder names.
    store_a = sales_multi.xs('Store A', level='Store')
    print("\nStore A cross-section:\n", store_a)

    results = {name: locals()[name] for name in ['customers_df', 'orders_df', 'inner_merged', 'left_merged', 'right_merged', 'outer_merged', 'q1_sales', 'q2_sales', 'q3_sales', 'yearly_sales', 'financial_data_clean', 'sales_with_keys', 'sales_data', 'sales_by_person', 'sales_summary', 'region_product_sales', 'custom_agg', 'basic_pivot_filled', 'multi_value_pivot', 'multi_agg_pivot', 'pivot_with_totals', 'monthly_pivot', 'sales_multi', 'store_totals', 'dept_totals', 'stacked', 'unstacked', 'pivot_multi', 'retail_data', 'customer_demographics', 'complete_data', 'summary_analysis', 'comprehensive_pivot', 'monthly_trends', 'customer_analysis']}
    results['store_a'] = store_a

    if output_dir is not None:
        directory = Path(output_dir)
        directory.mkdir(parents=True, exist_ok=True)
        for key in ('inner_merged', 'outer_merged', 'yearly_sales',
                    'financial_data_clean', 'sales_summary', 'sales_multi',
                    'complete_data', 'monthly_trends', 'customer_analysis'):
            results[key].to_csv(directory / f'{key}.csv')
        print(f"\nExported 9 CSV files to: {directory}")

    print("\nLAB 62 COMPLETED SUCCESSFULLY!")
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', default=None, help='Optional directory for CSV outputs')
    args = parser.parse_args()
    run_lab(output_dir=args.output_dir)
