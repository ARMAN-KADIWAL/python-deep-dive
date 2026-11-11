
import sys
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

print("LAB 63 - Data Visualization")
print("Python:", sys.version.split()[0])
print("Pandas:", pd.__version__)
print("NumPy:", np.__version__)
print("Matplotlib:", matplotlib.__version__)
print("Seaborn:", sns.__version__)

np.random.seed(42)

months = [
    "Jan", "Feb", "Mar", "Apr",
    "May", "Jun", "Jul", "Aug",
    "Sep", "Oct", "Nov", "Dec"
]

data = {
    "Month": months,
    "Product_A_Sales": np.random.randint(1000, 5000, 12),
    "Product_B_Sales": np.random.randint(800, 4500, 12),
    "Product_C_Sales": np.random.randint(1200, 3800, 12),
    "Marketing_Spend": np.random.randint(500, 2000, 12),
    "Customer_Count": np.random.randint(100, 800, 12)
}

sales_df = pd.DataFrame(data)

print("\nSales Dataset:")
print(sales_df)
print("\nDataset Shape:", sales_df.shape)

fig, ax = plt.subplots(figsize=(10, 6))

sales_df.plot(
    x="Month",
    y="Product_A_Sales",
    kind="line",
    marker="o",
    ax=ax
)

ax.set_title("Product A - Monthly Sales")
ax.set_xlabel("Month")
ax.set_ylabel("Sales ($)")
ax.grid(True, alpha=0.3)

plt.tight_layout()
fig.savefig("product_a_sales.png", dpi=200)
plt.close(fig)

print("\nGraph saved: product_a_sales.png")
print("Task 1 and first line chart completed!")



fig, ax = plt.subplots(figsize=(12, 6))

sales_df.set_index("Month")[
    ["Product_A_Sales", "Product_B_Sales", "Product_C_Sales"]
].plot(
    kind="line",
    marker="o",
    ax=ax
)

ax.set_title("Monthly Sales Comparison - All Products")
ax.set_xlabel("Month")
ax.set_ylabel("Sales ($)")
ax.legend(title="Products")
ax.grid(True, alpha=0.3)

plt.xticks(rotation=45)
plt.tight_layout()
fig.savefig("all_products_sales.png", dpi=200)
plt.close(fig)

print("Saved: all_products_sales.png")


product_totals = pd.Series({
    "Product A": sales_df["Product_A_Sales"].sum(),
    "Product B": sales_df["Product_B_Sales"].sum(),
    "Product C": sales_df["Product_C_Sales"].sum()
})

fig, ax = plt.subplots(figsize=(10, 6))

product_totals.plot(
    kind="bar",
    ax=ax
)

ax.set_title("Total Annual Sales by Product")
ax.set_xlabel("Products")
ax.set_ylabel("Total Sales ($)")
ax.tick_params(axis="x", rotation=0)
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
fig.savefig("annual_sales_bar.png", dpi=200)
plt.close(fig)

print("Saved: annual_sales_bar.png")



fig, ax = plt.subplots(figsize=(12, 7))

sales_df.set_index("Month")["Marketing_Spend"].plot(
    kind="barh",
    ax=ax
)

ax.set_title("Monthly Marketing Spend")
ax.set_xlabel("Marketing Spend ($)")
ax.set_ylabel("Month")
ax.grid(axis="x", alpha=0.3)

plt.tight_layout()
fig.savefig("marketing_spend_barh.png", dpi=200)
plt.close(fig)

print("Saved: marketing_spend_barh.png")




fig, ax = plt.subplots(figsize=(14, 8))

ax.plot(
    sales_df["Month"],
    sales_df["Product_A_Sales"],
    color="#2E86AB",
    linewidth=5,
    marker="D",
    markersize=8,
    linestyle="-",
    label="Product A"
)

ax.plot(
    sales_df["Month"],
    sales_df["Product_B_Sales"],
    color="#A23B72",
    linewidth=3,
    marker="s",
    markersize=8,
    linestyle="--",
    label="Product B"
)

ax.plot(
    sales_df["Month"],
    sales_df["Product_C_Sales"],
    color="#F18F01",
    linewidth=3,
    marker="^",
    markersize=8,
    linestyle="-.",
    label="Product C"
)

ax.set_title(
    "Monthly Sales Performance Analysis",
    fontsize=18,
    fontweight="bold",
    pad=20
)

ax.set_xlabel("Month", fontsize=13)
ax.set_ylabel("Sales Amount ($)", fontsize=13)

ax.legend(loc="upper right", title="Products")
ax.grid(True, alpha=0.3, linestyle=":")

ax.set_facecolor("#F8F9FA")
ax.tick_params(axis="x", rotation=45)

plt.tight_layout()
fig.savefig("customized_line_chart.png", dpi=200)
plt.close(fig)

print("Saved: customized_line_chart.png")



fig, ax = plt.subplots(figsize=(16, 8))

x = np.arange(len(sales_df["Month"]))
bar_width = 0.25

bars1 = ax.bar(
    x - bar_width,
    sales_df["Product_A_Sales"],
    bar_width,
    label="Product A",
    color="#FF6B6B"
)

bars2 = ax.bar(
    x,
    sales_df["Product_B_Sales"],
    bar_width,
    label="Product B",
    color="#4ECDC4"
)

bars3 = ax.bar(
    x + bar_width,
    sales_df["Product_C_Sales"],
    bar_width,
    label="Product C",
    color="#45B7D1"
)

ax.set_title(
    "Monthly Sales Comparison by Product",
    fontsize=18,
    fontweight="bold"
)

ax.set_xlabel("Month")
ax.set_ylabel("Sales ($)")

ax.set_xticks(x)
ax.set_xticklabels(sales_df["Month"], rotation=45)

ax.legend(title="Products")
ax.grid(axis="y", alpha=0.3)
ax.set_axisbelow(True)

maximum = sales_df[
    ["Product_A_Sales", "Product_B_Sales", "Product_C_Sales"]
].to_numpy().max()

ax.set_ylim(0, maximum * 1.18)

for bars in (bars1, bars2, bars3):
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 35,
            f"{height:,.0f}",
            ha="center",
            fontsize=8
        )

plt.tight_layout()
fig.savefig("customized_bar_chart.png", dpi=200)
plt.close(fig)

print("Saved: customized_bar_chart.png")



rng = np.random.default_rng(42)

customer_ages = rng.normal(35, 12, 1000)
customer_spending = rng.exponential(200, 1000)

fig, axes = plt.subplots(2, 2, figsize=(15, 12))

axes[0, 0].hist(
    customer_ages,
    bins=30,
    color="skyblue",
    edgecolor="black",
    alpha=0.7
)
axes[0, 0].set_title("Customer Age Distribution")
axes[0, 0].set_xlabel("Age")
axes[0, 0].set_ylabel("Frequency")

axes[0, 1].hist(
    customer_spending,
    bins=30,
    color="lightcoral",
    edgecolor="black"
)
axes[0, 1].set_title("Customer Spending Distribution")
axes[0, 1].set_xlabel("Spending ($)")
axes[0, 1].set_ylabel("Frequency")

axes[1, 0].hist(
    sales_df["Product_A_Sales"],
    bins=8,
    color="lightgreen",
    edgecolor="black"
)
axes[1, 0].set_title("Product A Monthly Sales Distribution")
axes[1, 0].set_xlabel("Sales ($)")
axes[1, 0].set_ylabel("Frequency")

axes[1, 1].hist(
    sales_df["Marketing_Spend"],
    bins=8,
    color="gold",
    edgecolor="black"
)
axes[1, 1].set_title("Marketing Spend Distribution")
axes[1, 1].set_xlabel("Marketing Spend ($)")
axes[1, 1].set_ylabel("Frequency")

for ax in axes.flat:
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)

plt.tight_layout()
fig.savefig("histograms.png", dpi=200)
plt.close(fig)

print("Saved: histograms.png")



total_sales = (
    sales_df["Product_A_Sales"]
    + sales_df["Product_B_Sales"]
    + sales_df["Product_C_Sales"]
)

fig, axes = plt.subplots(2, 2, figsize=(15, 12))

x = sales_df["Marketing_Spend"].to_numpy()
y = sales_df["Product_A_Sales"].to_numpy()

axes[0, 0].scatter(x, y, alpha=0.7, s=100)

z = np.polyfit(x, y, 1)
p = np.poly1d(z)

order = np.argsort(x)
axes[0, 0].plot(
    x[order],
    p(x[order]),
    "r--",
    linewidth=2,
    label="Trend line"
)

axes[0, 0].set_title("Marketing Spend vs Product A Sales")
axes[0, 0].set_xlabel("Marketing Spend ($)")
axes[0, 0].set_ylabel("Product A Sales ($)")
axes[0, 0].legend()

axes[0, 1].scatter(
    sales_df["Customer_Count"],
    total_sales,
    alpha=0.7,
    s=100
)
axes[0, 1].set_title("Customer Count vs Total Sales")
axes[0, 1].set_xlabel("Customer Count")
axes[0, 1].set_ylabel("Total Sales ($)")

axes[1, 0].scatter(
    sales_df["Product_A_Sales"],
    sales_df["Product_B_Sales"],
    alpha=0.7,
    s=100
)
axes[1, 0].set_title("Product A vs Product B Sales")
axes[1, 0].set_xlabel("Product A Sales ($)")
axes[1, 0].set_ylabel("Product B Sales ($)")

scatter = axes[1, 1].scatter(
    sales_df["Product_A_Sales"],
    sales_df["Product_C_Sales"],
    c=sales_df["Marketing_Spend"],
    s=sales_df["Customer_Count"] / 2,
    alpha=0.7,
    cmap="viridis"
)
axes[1, 1].set_title("Product A vs Product C")
axes[1, 1].set_xlabel("Product A Sales ($)")
axes[1, 1].set_ylabel("Product C Sales ($)")

fig.colorbar(
    scatter,
    ax=axes[1, 1],
    label="Marketing Spend ($)"
)

for ax in axes.flat:
    ax.grid(True, alpha=0.3)

plt.tight_layout()
fig.savefig("scatter_plots.png", dpi=200)
plt.close(fig)

print("Saved: scatter_plots.png")



columns = [
    "Product_A_Sales",
    "Product_B_Sales",
    "Product_C_Sales",
    "Marketing_Spend",
    "Customer_Count"
]

correlation_data = sales_df[columns].copy()

correlation_matrix = correlation_data.corr()

print("\nTASK 5.1 - Correlation Matrix:")
print(correlation_matrix.round(3))

correlation_matrix.round(3).to_csv(
    "correlation_matrix.csv"
)

print("Saved: correlation_matrix.csv")



fig, axes = plt.subplots(
    1, 2, figsize=(19, 8)
)

im = axes[0].imshow(
    correlation_matrix,
    cmap="coolwarm",
    vmin=-1,
    vmax=1
)

axes[0].set_title(
    "Correlation Heatmap - Matplotlib"
)

axes[0].set_xticks(range(len(columns)))
axes[0].set_yticks(range(len(columns)))

axes[0].set_xticklabels(
    columns, rotation=45, ha="right"
)
axes[0].set_yticklabels(columns)

for i in range(len(columns)):
    for j in range(len(columns)):
        value = correlation_matrix.iloc[i, j]

        axes[0].text(
            j, i, f"{value:.2f}",
            ha="center",
            va="center",
            fontsize=10
        )

fig.colorbar(
    im, ax=axes[0], shrink=0.7
)

sns.heatmap(
    correlation_matrix,
    ax=axes[1],
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    vmin=-1,
    vmax=1,
    center=0,
    linewidths=0.5,
    cbar_kws={"shrink": 0.7}
)

axes[1].set_title(
    "Correlation Heatmap - Seaborn"
)
axes[1].tick_params(
    axis="x", labelrotation=45
)

plt.tight_layout()

fig.savefig(
    "correlation_heatmaps.png",
    dpi=200,
    bbox_inches="tight"
)

plt.close(fig)

print("Saved: correlation_heatmaps.png")



pairs = []

for i in range(len(columns)):
    for j in range(i + 1, len(columns)):

        value = correlation_matrix.iloc[i, j]

        pairs.append((
            columns[i],
            columns[j],
            float(value)
        ))

pairs.sort(
    key=lambda item: abs(item[2]),
    reverse=True
)

strong = [
    (a, b, r)
    for a, b, r in pairs
    if abs(r) > 0.5
]

print("\nStrong Correlations (|r| > 0.5):")

if strong:
    for a, b, r in strong:
        direction = (
            "Positive" if r > 0 else "Negative"
        )

        print(
            f"{a} vs {b}: {r:+.3f} "
            f"({direction})"
        )
else:
    print("No pairs exceed the threshold.")

labels = [
    f"{a} vs {b}"
    for a, b, r in pairs
]

values = [
    r for a, b, r in pairs
]

bar_colors = [
    "#4F8571" if r > 0.5
    else "#C77969" if r < -0.5
    else "#9AA3A4"
    for r in values
]

fig, ax = plt.subplots(figsize=(13, 7))

ax.barh(
    labels,
    values,
    color=bar_colors
)

ax.invert_yaxis()
ax.set_xlim(-1, 1)

ax.axvline(0, color="black")
ax.axvline(0.5, linestyle="--")
ax.axvline(-0.5, linestyle="--")

ax.set_xlabel(
    "Pearson Correlation Coefficient (r)"
)

ax.set_title(
    "Variable Pair Correlations"
)

ax.grid(axis="x", alpha=0.2)

plt.tight_layout()

fig.savefig(
    "correlation_strengths.png",
    dpi=200,
    bbox_inches="tight"
)

plt.close(fig)

print("Saved: correlation_strengths.png")



product_cols = [
    "Product_A_Sales",
    "Product_B_Sales",
    "Product_C_Sales"
]

total_sales = sales_df[product_cols].sum(axis=1)

correlation_matrix = sales_df[
    product_cols + ["Marketing_Spend", "Customer_Count"]
].corr()

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

sales_df.set_index("Month")[product_cols].plot(
    kind="line",
    marker="o",
    ax=axes[0, 0]
)

axes[0, 0].set_title("Monthly Sales Trends")
axes[0, 0].set_ylabel("Sales ($)")
axes[0, 0].legend(title="Products", fontsize=8)
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].tick_params(axis="x", rotation=45)

product_totals = sales_df[product_cols].sum()
product_totals.index = [
    "Product A", "Product B", "Product C"
]

product_totals.plot(
    kind="bar",
    ax=axes[0, 1],
    color=["#D98264", "#7BA78E", "#789EB3"]
)

axes[0, 1].set_title("Total Annual Sales by Product")
axes[0, 1].set_ylabel("Sales ($)")
axes[0, 1].tick_params(axis="x", rotation=0)
axes[0, 1].grid(axis="y", alpha=0.3)

axes[1, 0].scatter(
    sales_df["Marketing_Spend"],
    sales_df["Product_A_Sales"],
    alpha=0.7,
    s=80
)

axes[1, 0].set_title(
    "Marketing Spend vs Product A Sales"
)
axes[1, 0].set_xlabel("Marketing Spend ($)")
axes[1, 0].set_ylabel("Product A Sales ($)")
axes[1, 0].grid(True, alpha=0.3)

sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    vmin=-1,
    vmax=1,
    center=0,
    ax=axes[1, 1]
)

axes[1, 1].set_title("Correlation Matrix")
axes[1, 1].tick_params(axis="x", labelrotation=45)

fig.suptitle(
    "Sales Data Analysis Dashboard",
    fontsize=18,
    fontweight="bold"
)

fig.tight_layout(rect=[0, 0, 1, 0.96])

for ext in ["png", "jpg", "pdf"]:
    filename = f"sales_dashboard.{ext}"

    fig.savefig(
        filename,
        dpi=220,
        bbox_inches="tight",
        facecolor="white"
    )

    print(f"Saved: {filename}")

plt.close(fig)




fig, ax = plt.subplots(figsize=(12, 6))

for product in product_cols:
    ax.plot(
        sales_df["Month"],
        sales_df[product],
        marker="o",
        linewidth=2,
        label=product.replace("_", " ")
    )

ax.set_title("Monthly Sales Trends Analysis")
ax.set_xlabel("Month")
ax.set_ylabel("Sales ($)")
ax.legend()
ax.grid(True, alpha=0.3)
ax.tick_params(axis="x", rotation=45)

fig.tight_layout()

fig.savefig(
    "monthly_sales_trends.png",
    dpi=220,
    bbox_inches="tight"
)

plt.close(fig)

print("Saved: monthly_sales_trends.png")




x = sales_df["Marketing_Spend"].to_numpy()
y = total_sales.to_numpy()

fig, ax = plt.subplots(figsize=(10, 6))

ax.scatter(
    x, y,
    s=100,
    alpha=0.7,
    color="orange"
)

z = np.polyfit(x, y, 1)
p = np.poly1d(z)

order = np.argsort(x)

ax.plot(
    x[order],
    p(x[order]),
    "r--",
    linewidth=2,
    label="Trend Line"
)

ax.set_title("Marketing Spend vs Total Sales")
ax.set_xlabel("Marketing Spend ($)")
ax.set_ylabel("Total Sales ($)")
ax.legend()
ax.grid(True, alpha=0.3)

fig.tight_layout()

fig.savefig(
    "marketing_effectiveness.png",
    dpi=220,
    bbox_inches="tight"
)

plt.close(fig)

print("Saved: marketing_effectiveness.png")




fig, axes = plt.subplots(
    1, 3, figsize=(18, 6)
)

colors = [
    "skyblue",
    "lightcoral",
    "lightgreen"
]

for i, product in enumerate(product_cols):

    axes[i].hist(
        sales_df[product],
        bins=6,
        color=colors[i],
        edgecolor="black",
        alpha=0.7
    )

    axes[i].set_title(
        product.replace("_", " ") + " Distribution"
    )

    axes[i].set_xlabel("Sales ($)")
    axes[i].set_ylabel("Frequency")
    axes[i].grid(axis="y", alpha=0.3)

fig.suptitle("Sales Distribution Analysis")

fig.tight_layout()

fig.savefig(
    "sales_distributions.png",
    dpi=220,
    bbox_inches="tight"
)

plt.close(fig)

print("Saved: sales_distributions.png")




from pathlib import Path

expected_files = [
    "sales_dashboard.png",
    "sales_dashboard.jpg",
    "sales_dashboard.pdf",
    "monthly_sales_trends.png",
    "marketing_effectiveness.png",
    "sales_distributions.png"
]

print("\n--- Task 6 File Verification ---")

missing = []

for filename in expected_files:
    path = Path(filename)

    if path.is_file() and path.stat().st_size > 0:
        size = path.stat().st_size / 1024

        print(
            f"OK: {filename} ({size:.1f} KB)"
        )
    else:
        print(f"MISSING: {filename}")
        missing.append(filename)

if missing:
    print("Task 6 incomplete - check missing files.")
else:
    print("\nSUCCESS: All 6 files generated!")
    print("LAB 63 TASK 6 COMPLETED!")

