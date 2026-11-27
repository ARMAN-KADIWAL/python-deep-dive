# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set display options for better output
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 50)

print("Libraries imported successfully!")
print(f"Pandas version: {pd.__version__}")
print(f"NumPy version: {np.__version__}")

# Load the sales dataset
try:
    # Primary dataset - Sales data
    sales_df = pd.read_csv('data/sales_data.csv')
    
    # Secondary dataset - Customer information
    customers_df = pd.read_csv('data/customer_data.csv')
    
    # Product information dataset
    products_df = pd.read_csv('data/product_data.csv')
    
    print("Datasets loaded successfully!")
    print(f"Sales data shape: {sales_df.shape}")
    print(f"Customer data shape: {customers_df.shape}")
    print(f"Product data shape: {products_df.shape}")
    
except FileNotFoundError:
    print("Sample data files not found. Creating synthetic dataset...")
    # Create synthetic data for demonstration
    np.random.seed(42)
    
    # Generate sales data
    n_sales = 1000
    sales_df = pd.DataFrame({
        'sale_id': range(1, n_sales + 1),
        'customer_id': np.random.randint(1, 201, n_sales),
        'product_id': np.random.randint(1, 51, n_sales),
        'sale_date': pd.date_range('2023-01-01', periods=n_sales, freq='h'),
        'quantity': np.random.randint(1, 10, n_sales),
        'unit_price': np.round(np.random.uniform(10, 500, n_sales), 2),
        'discount': np.round(np.random.uniform(0, 0.3, n_sales), 2)
    })
    
    # Generate customer data
    n_customers = 200
    customers_df = pd.DataFrame({
        'customer_id': range(1, n_customers + 1),
        'customer_name': [f'Customer_{i}' for i in range(1, n_customers + 1)],
        'age': np.random.randint(18, 80, n_customers),
        'city': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'], n_customers),
        'registration_date': pd.date_range('2022-01-01', periods=n_customers, freq='D')
    })
    
    # Generate product data
    n_products = 50
    categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports']
    products_df = pd.DataFrame({
        'product_id': range(1, n_products + 1),
        'product_name': [f'Product_{i}' for i in range(1, n_products + 1)],
        'category': np.random.choice(categories, n_products),
        'cost_price': np.round(np.random.uniform(5, 200, n_products), 2)
    })
    
    print("Synthetic datasets created successfully!")

# Explore sales data
print("=== SALES DATA OVERVIEW ===")
print(f"Shape: {sales_df.shape}")
print(f"Columns: {list(sales_df.columns)}")
print("\nFirst 5 rows:")
print(sales_df.head())
print("\nData types:")
print(sales_df.dtypes)
print("\nBasic statistics:")
print(sales_df.describe())

print("\n" + "="*50)

# Explore customer data
print("=== CUSTOMER DATA OVERVIEW ===")
print(f"Shape: {customers_df.shape}")
print(f"Columns: {list(customers_df.columns)}")
print("\nFirst 5 rows:")
print(customers_df.head())

print("\n" + "="*50)

# Explore product data
print("=== PRODUCT DATA OVERVIEW ===")
print(f"Shape: {products_df.shape}")
print(f"Columns: {list(products_df.columns)}")
print("\nFirst 5 rows:")
print(products_df.head())

# Function to analyze data quality
def analyze_data_quality(df, dataset_name):
    print(f"=== DATA QUALITY ANALYSIS: {dataset_name.upper()} ===")
    
    # Check for missing values
    missing_values = df.isnull().sum()
    print(f"Missing values:\n{missing_values[missing_values > 0]}")
    
    # Check for duplicates
    duplicates = df.duplicated().sum()
    print(f"Duplicate rows: {duplicates}")
    
    # Check data types
    print(f"\nData types:\n{df.dtypes}")
    
    # Check for negative values in numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        negative_count = (df[col] < 0).sum()
        if negative_count > 0:
            print(f"Negative values in {col}: {negative_count}")
    
    print("\n" + "="*50 + "\n")

# Analyze all datasets
analyze_data_quality(sales_df, "Sales Data")
analyze_data_quality(customers_df, "Customer Data")
analyze_data_quality(products_df, "Product Data")

# Introduce missing values and duplicates for demonstration
print("Introducing realistic data quality issues...")

# Add missing values to sales data
sales_df.loc[10:15, 'discount'] = np.nan
sales_df.loc[50:55, 'unit_price'] = np.nan

# Add duplicate rows
duplicate_row = sales_df.iloc[0].copy()
sales_df = pd.concat([sales_df, pd.DataFrame([duplicate_row])], ignore_index=True)

# Add missing values to customer data
customers_df.loc[5:10, 'age'] = np.nan
customers_df.loc[20:22, 'city'] = np.nan

# Add inconsistent city names
customers_df.loc[100, 'city'] = 'new york'  # lowercase
customers_df.loc[101, 'city'] = 'NEW YORK'  # uppercase
customers_df.loc[102, 'city'] = 'New York '  # trailing space

print("Data quality issues introduced successfully!")

# Clean sales data missing values
print("=== CLEANING SALES DATA ===")

# Check missing values before cleaning
print("Missing values before cleaning:")
print(sales_df.isnull().sum())

# Handle missing discount values - fill with 0 (no discount)
sales_df['discount'] = sales_df['discount'].fillna(0)
print("Filled missing discount values with 0")

# Handle missing unit_price values - fill with median price by product
sales_df['unit_price'] = sales_df.groupby('product_id')['unit_price'].transform(
    lambda x: x.fillna(x.median())
)
print("Filled missing unit_price values with median by product")

# Verify cleaning
print("Missing values after cleaning:")
print(sales_df.isnull().sum())

print("\n" + "="*30 + "\n")

# Clean customer data missing values
print("=== CLEANING CUSTOMER DATA ===")

print("Missing values before cleaning:")
print(customers_df.isnull().sum())

# Handle missing age values - fill with median age
median_age = customers_df['age'].median()
customers_df['age'] = customers_df['age'].fillna(median_age)
print(f"Filled missing age values with median: {median_age}")

# Handle missing city values - fill with most common city
most_common_city = customers_df['city'].mode()[0]
customers_df['city'] = customers_df['city'].fillna(most_common_city)
print(f"Filled missing city values with most common: {most_common_city}")

# Verify cleaning
print("Missing values after cleaning:")
print(customers_df.isnull().sum())

# Remove duplicates from sales data
print("=== REMOVING DUPLICATES ===")
print(f"Sales data shape before: {sales_df.shape}")
sales_df = sales_df.drop_duplicates()
print(f"Sales data shape after: {sales_df.shape}")

# Standardize city names in customer data
print("\n=== STANDARDIZING CITY NAMES ===")
print("Unique cities before standardization:")
print(customers_df['city'].unique())

# Standardize city names
customers_df['city'] = customers_df['city'].str.strip().str.title()
print("Unique cities after standardization:")
print(customers_df['city'].unique())

# Reset indices after cleaning
sales_df = sales_df.reset_index(drop=True)
customers_df = customers_df.reset_index(drop=True)
products_df = products_df.reset_index(drop=True)

print("\nData cleaning completed successfully!")

# Convert date columns to datetime
print("=== CONVERTING DATA TYPES ===")

# Convert sale_date to datetime
sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'])
print("Converted sale_date to datetime")

# Convert registration_date to datetime
customers_df['registration_date'] = pd.to_datetime(customers_df['registration_date'])
print("Converted registration_date to datetime")

# Ensure numeric columns are proper numeric types
sales_df['quantity'] = sales_df['quantity'].astype(int)
sales_df['unit_price'] = sales_df['unit_price'].astype(float)
sales_df['discount'] = sales_df['discount'].astype(float)

customers_df['age'] = customers_df['age'].astype(int)
products_df['cost_price'] = products_df['cost_price'].astype(float)

print("Data type conversions completed!")
print("\nFinal data types:")
print("Sales data:", sales_df.dtypes.to_dict())
print("Customer data:", customers_df.dtypes.to_dict())
print("Product data:", products_df.dtypes.to_dict())

# Create calculated columns in sales data
print("=== CREATING CALCULATED COLUMNS ===")

# Calculate total amount before discount
sales_df['gross_amount'] = sales_df['quantity'] * sales_df['unit_price']

# Calculate discount amount
sales_df['discount_amount'] = sales_df['gross_amount'] * sales_df['discount']

# Calculate net amount after discount
sales_df['net_amount'] = sales_df['gross_amount'] - sales_df['discount_amount']

# Extract date components for time-based analysis
sales_df['sale_year'] = sales_df['sale_date'].dt.year
sales_df['sale_month'] = sales_df['sale_date'].dt.month
sales_df['sale_day'] = sales_df['sale_date'].dt.day
sales_df['sale_weekday'] = sales_df['sale_date'].dt.day_name()

print("Calculated columns created:")
print("- gross_amount: quantity × unit_price")
print("- discount_amount: gross_amount × discount")
print("- net_amount: gross_amount - discount_amount")
print("- Date components: year, month, day, weekday")

# Display sample of enhanced data
print("\nSample of enhanced sales data:")
print(sales_df[['sale_id', 'quantity', 'unit_price', 'gross_amount', 'net_amount']].head())

# Merge sales data with customer information
print("=== MERGING DATASETS ===")

# Merge sales with customers
sales_with_customers = pd.merge(
    sales_df, 
    customers_df, 
    on='customer_id', 
    how='left'
)
print(f"Sales + Customers merged shape: {sales_with_customers.shape}")

# Merge with product information
complete_sales_data = pd.merge(
    sales_with_customers,
    products_df,
    on='product_id',
    how='left'
)
print(f"Complete dataset shape: {complete_sales_data.shape}")

# Calculate profit margin
complete_sales_data['profit'] = complete_sales_data['net_amount'] - (
    complete_sales_data['quantity'] * complete_sales_data['cost_price']
)
complete_sales_data['profit_margin'] = (
    complete_sales_data['profit'] / complete_sales_data['net_amount'] * 100
).round(2)

print("Complete dataset with profit calculations created!")
print("\nSample of complete dataset:")
print(complete_sales_data[['customer_name', 'product_name', 'category', 'net_amount', 'profit']].head())

# Sales analysis by customer
print("=== SALES ANALYSIS BY CUSTOMER ===")
customer_analysis = complete_sales_data.groupby('customer_name').agg({
    'net_amount': ['sum', 'mean', 'count'],
    'quantity': 'sum',
    'profit': 'sum'
}).round(2)

# Flatten column names
customer_analysis.columns = ['total_sales', 'avg_order_value', 'order_count', 'total_quantity', 'total_profit']
customer_analysis = customer_analysis.sort_values('total_sales', ascending=False)

print("Top 10 customers by total sales:")
print(customer_analysis.head(10))

print("\n" + "="*50)

# Sales analysis by product category
print("=== SALES ANALYSIS BY CATEGORY ===")
category_analysis = complete_sales_data.groupby('category').agg({
    'net_amount': ['sum', 'mean'],
    'quantity': 'sum',
    'profit': 'sum',
    'profit_margin': 'mean'
}).round(2)

category_analysis.columns = ['total_sales', 'avg_sale_amount', 'total_quantity', 'total_profit', 'avg_profit_margin']
category_analysis = category_analysis.sort_values('total_sales', ascending=False)

print("Sales by product category:")
print(category_analysis)

print("\n" + "="*50)

# Time-based analysis
print("=== TIME-BASED ANALYSIS ===")
monthly_sales = complete_sales_data.groupby(['sale_year', 'sale_month']).agg({
    'net_amount': 'sum',
    'quantity': 'sum',
    'sale_id': 'count'
}).round(2)

monthly_sales.columns = ['total_sales', 'total_quantity', 'order_count']
print("Monthly sales summary:")
print(monthly_sales)

# Weekday analysis
weekday_sales = complete_sales_data.groupby('sale_weekday').agg({
    'net_amount': ['sum', 'mean'],
    'sale_id': 'count'
}).round(2)

weekday_sales.columns = ['total_sales', 'avg_sale_amount', 'order_count']
# Reorder by weekday
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_sales = weekday_sales.reindex(weekday_order)

print("\nSales by weekday:")
print(weekday_sales)

# Customer segmentation based on purchase behavior
print("=== CUSTOMER SEGMENTATION ===")

# Calculate customer metrics
customer_metrics = complete_sales_data.groupby('customer_id').agg({
    'net_amount': ['sum', 'mean'],
    'sale_id': 'count',
    'sale_date': ['min', 'max']
}).round(2)

customer_metrics.columns = ['total_spent', 'avg_order_value', 'order_frequency', 'first_purchase', 'last_purchase']

# Calculate days since last purchase
customer_metrics['days_since_last_purchase'] = (
    datetime.now() - customer_metrics['last_purchase']
).dt.days

# Create customer segments
def segment_customers(row):
    if row['total_spent'] >= 1000 and row['order_frequency'] >= 5:
        return 'VIP'
    elif row['total_spent'] >= 500 and row['order_frequency'] >= 3:
        return 'Regular'
    elif row['days_since_last_purchase'] > 90:
        return 'At Risk'
    else:
        return 'New/Occasional'

customer_metrics['segment'] = customer_metrics.apply(segment_customers, axis=1)

print("Customer segmentation results:")
print(customer_metrics['segment'].value_counts())

print("\n" + "="*50)

# Product performance analysis
print("=== PRODUCT PERFORMANCE ANALYSIS ===")

product_performance = complete_sales_data.groupby('product_name').agg({
    'net_amount': 'sum',
    'quantity': 'sum',
    'profit': 'sum',
    'profit_margin': 'mean'
}).round(2)

product_performance.columns = ['total_revenue', 'units_sold', 'total_profit', 'avg_profit_margin']
product_performance = product_performance.sort_values('total_profit', ascending=False)

print("Top 10 products by profit:")
print(product_performance.head(10))

# Identify underperforming products
underperforming = product_performance[
    (product_performance['total_profit'] < 0) | 
    (product_performance['avg_profit_margin'] < 10)
]

print(f"\nUnderperforming products (negative profit or <10% margin): {len(underperforming)}")
if len(underperforming) > 0:
    print(underperforming.head())

# Set up visualization environment
print("=== SETTING UP VISUALIZATIONS ===")

# Configure matplotlib
plt.style.use('default')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
sns.set_palette("husl")

# Create output directory for saving plots
import os
os.makedirs('visualizations', exist_ok=True)

print("Visualization environment configured!")

# Sales trend over time
print("Creating sales trend visualization...")

fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Sales Performance Analysis', fontsize=16, fontweight='bold')

# 1. Monthly sales trend
monthly_sales_plot = complete_sales_data.groupby(['sale_year', 'sale_month'])['net_amount'].sum()
axes[0, 0].plot(range(len(monthly_sales_plot)), monthly_sales_plot.values, marker='o', linewidth=2)
axes[0, 0].set_title('Monthly Sales Trend')
axes[0, 0].set_xlabel('Month')
axes[0, 0].set_ylabel('Sales Amount ($)')
axes[0, 0].grid(True, alpha=0.3)

# 2. Sales by weekday
weekday_sales_viz = complete_sales_data.groupby('sale_weekday')['net_amount'].sum()
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_sales_viz = weekday_sales_viz.reindex(weekday_order)
axes[0, 1].bar(weekday_sales_viz.index, weekday_sales_viz.values, color='skyblue')
axes[0, 1].set_title('Sales by Weekday')
axes[0, 1].set_xlabel('Day of Week')
axes[0, 1].set_ylabel('Sales Amount ($)')
axes[0, 1].tick_params(axis='x', rotation=45)

# 3. Sales by category
category_sales = complete_sales_data.groupby('category')['net_amount'].sum().sort_values(ascending=True)
axes[1, 0].barh(category_sales.index, category_sales.values, color='lightcoral')
axes[1, 0].set_title('Sales by Product Category')
axes[1, 0].set_xlabel('Sales Amount ($)')

# 4. Top customers
top_customers = complete_sales_data.groupby('customer_name')['net_amount'].sum().nlargest(10)
axes[1, 1].bar(range(len(top_customers)), top_customers.values, color='lightgreen')
axes[1, 1].set_title('Top 10 Customers by Sales')
axes[1, 1].set_xlabel('Customer Rank')
axes[1, 1].set_ylabel('Sales Amount ($)')

plt.tight_layout()
plt.savefig('visualizations/sales_performance.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()

print("Sales performance visualizations created!")

# Customer analysis visualizations
print("Creating customer analysis visualizations...")

fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Customer Analysis Dashboard', fontsize=16, fontweight='bold')

# 1. Customer age distribution
axes[0, 0].hist(customers_df['age'], bins=20, color='purple', alpha=0.7, edgecolor='black')
axes[0, 0].set_title('Customer Age Distribution')
axes[0, 0].set_xlabel('Age')
axes[0, 0].set_ylabel('Number of Customers')
axes[0, 0].axvline(customers_df['age'].mean(), color='red', linestyle='--', 
                   label=f'Mean: {customers_df["age"].mean():.1f}')
axes[0, 0].legend()

# 2. Customer distribution by city
city_counts = customers_df['city'].value_counts()
axes[0, 1].pie(city_counts.values, labels=city_counts.index, autopct='%1.1f%%', startangle=90)
axes[0, 1].set_title('Customer Distribution by City')

# 3. Customer segments
segment_counts = customer_metrics['segment'].value_counts()
axes[1, 0].bar(segment_counts.index, segment_counts.values, color=['gold', 'silver', 'orange', 'lightblue'])
axes[1, 0].set_title('Customer Segmentation')
axes[1, 0].set_xlabel('Customer Segment')
axes[1, 0].set_ylabel('Number of Customers')
axes[1, 0].tick_params(axis='x', rotation=45)

# 4. Customer lifetime value distribution
axes[1, 1].hist(customer_metrics['total_spent'], bins=20, color='teal', alpha=0.7, edgecolor='black')
axes[1, 1].set_title('Customer Lifetime Value Distribution')
axes[1, 1].set_xlabel('Total Spent ($)')
axes[1, 1].set_ylabel('Number of Customers')
axes[1, 1].axvline(customer_metrics['total_spent'].mean(), color='red', linestyle='--',
                   label=f'Mean: ${customer_metrics["total_spent"].mean():.2f}')
axes[1, 1].legend()

plt.tight_layout()
plt.savefig('visualizations/customer_analysis.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()

print("Customer analysis visualizations created!")

# Product and profitability analysis
print("Creating product analysis visualizations...")

fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Product Performance & Profitability Analysis', fontsize=16, fontweight='bold')

# 1. Profit by category
category_profit = complete_sales_data.groupby('category')['profit'].sum().sort_values(ascending=False)
axes[0, 0].bar(category_profit.index, category_profit.values, color='lightseagreen')
axes[0, 0].set_title('Total Profit by Category')
axes[0, 0].set_xlabel('Product Category')
axes[0, 0].set_ylabel('Profit ($)')
axes[0, 0].tick_params(axis='x', rotation=45)

# 2. Profit margin distribution
axes[0, 1].hist(complete_sales_data['profit_margin'], bins=30, color='coral', alpha=0.7, edgecolor='black')
axes[0, 1].set_title('Profit Margin Distribution')
axes[0, 1].set_xlabel('Profit Margin (%)')
axes[0, 1].set_ylabel('Number of Sales')
axes[0, 1].axvline(complete_sales_data['profit_margin'].mean(), color='red', linestyle='--',
                   label=f'Mean: {complete_sales_data["profit_margin"].mean():.1f}%')
axes[0, 1].legend()

# 3. Quantity vs Profit scatter plot
axes[1, 0].scatter(complete_sales_data['quantity'], complete_sales_data['profit'], alpha=0.6, color='navy')
axes[1, 0].set_title('Quantity vs Profit Relationship')
axes[1, 0].set_xlabel('Quantity Sold')
axes[1, 0].set_ylabel('Profit ($)')
axes[1, 0].grid(True, alpha=0.3)

# 4. Top products by revenue
top_products = complete_sales_data.groupby('product_name')['net_amount'].sum().nlargest(10)
axes[1, 1].barh(range(len(top_products)), top_products.values, color='gold')
axes[1, 1].set_yticks(range(len(top_products)))
axes[1, 1].set_yticklabels([name[:15] + '...' if len(name) > 15 else name for name in top_products.index])
axes[1, 1].set_title('Top 10 Products by Revenue')
axes[1, 1].set_xlabel('Revenue ($)')

plt.tight_layout()
plt.savefig('visualizations/product_analysis.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()

print("Product analysis visualizations created!")

# Advanced correlation analysis
print("Creating correlation analysis...")

# Select numeric columns for correlation
numeric_columns = ['quantity', 'unit_price', 'discount', 'gross_amount', 'net_amount', 'profit', 'profit_margin', 'age']
correlation_data = complete_sales_data[numeric_columns].corr()

# Create correlation heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_data, annot=True, cmap='coolwarm', center=0, 
            square=True, linewidths=0.5, cbar_kws={"shrink": .8})
plt.title('Correlation Matrix of Key Variables', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/correlation_analysis.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()

print("Correlation analysis visualization created!")

# Summary statistics visualization
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Key Performance Indicators Summary', fontsize=16, fontweight='bold')

# Total sales by month
monthly_totals = complete_sales_data.groupby(['sale_year', 'sale_month'])['net_amount'].sum()
axes[0].plot(range(len(monthly_totals)), monthly_totals.values, marker='o', linewidth=3, markersize=8)
axes[0].set_title('Monthly Sales Trend')
axes[0].set_xlabel('Month')
axes[0].set_ylabel('Sales ($)')
axes[0].grid(True, alpha=0.3)

# Average order value by category
avg_order_by_category = complete_sales_data.groupby('category')['net_amount'].mean()
axes[1].bar(avg_order_by_category.index, avg_order_by_category.values)
axes[1].set_title('Average Order Value by Category')
axes[1].tick_params(axis='x', rotation=45)
profit_by_month = complete_sales_data.groupby(['sale_year', 'sale_month'])['profit'].sum()
axes[2].plot(range(len(profit_by_month)), profit_by_month.values, marker='o')
axes[2].set_title('Monthly Profit')
plt.tight_layout()
plt.savefig('visualizations/kpi_summary.png', dpi=150, bbox_inches='tight')
plt.show()
plt.close()


# Task 5: Report generation and export (reconstructed)
from pathlib import Path
from html import escape
output = Path("reports")
output.mkdir(exist_ok=True)
complete_sales_data.to_csv(output / "cleaned_sales.csv", index=False)
customer_analysis.to_csv(output / "customer_analysis.csv")
category_analysis.to_csv(output / "category_analysis.csv")
monthly_sales.to_csv(output / "monthly_sales.csv")
product_performance.to_csv(output / "product_performance.csv")
summary = {
    "records": len(complete_sales_data),
    "revenue": float(complete_sales_data["net_amount"].sum()),
    "profit": float(complete_sales_data["profit"].sum()),
}
import json
(output / "summary.json").write_text(json.dumps(summary, indent=2))
html = "<h1>Sales Analysis Report</h1>" + "".join(
    f"<p>{escape(k)}: {v:,.2f}</p>" for k, v in summary.items()
)
html += category_analysis.to_html()
for image in sorted(Path("visualizations").glob("*.png")):
    html += f'<img src="../visualizations/{image.name}" width="800" alt="{image.stem}">'
(output / "report.html").write_text(html, encoding="utf-8")
assert len(complete_sales_data) > 0
assert not complete_sales_data["sale_id"].duplicated().any()
print("Report and CSV exports created.")
