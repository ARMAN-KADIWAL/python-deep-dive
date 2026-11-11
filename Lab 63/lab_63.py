"""Lab 63: Data Visualization with Pandas and Matplotlib.

Run: python3 lab_63.py --output-dir outputs
The sales dataset is synthetic and reproducible (seed=42).
All plots use the non-interactive Agg backend for Linux/cloud machines.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
PRODUCTS = ["Product_A_Sales", "Product_B_Sales", "Product_C_Sales"]
COLUMNS = PRODUCTS + ["Marketing_Spend", "Customer_Count"]

EXPECTED_FILES = (
    "sales_data.csv",
    "product_a_sales.png",
    "all_products_sales.png",
    "annual_sales_bar.png",
    "marketing_spend_barh.png",
    "customized_line_chart.png",
    "customized_bar_chart.png",
    "histograms.png",
    "scatter_plots.png",
    "correlation_matrix.csv",
    "correlation_heatmaps.png",
    "correlation_strengths.png",
    "sales_dashboard.png",
    "sales_dashboard.jpg",
    "sales_dashboard.pdf",
    "monthly_sales_trends.png",
    "marketing_effectiveness.png",
    "sales_distributions.png",
)


def make_sales_data() -> pd.DataFrame:
    """Match the original lab's numpy random sequence."""
    rng = np.random.RandomState(42)
    return pd.DataFrame({
        "Month": MONTHS,
        "Product_A_Sales": rng.randint(1000, 5000, 12),
        "Product_B_Sales": rng.randint(800, 4500, 12),
        "Product_C_Sales": rng.randint(1200, 3800, 12),
        "Marketing_Spend": rng.randint(500, 2000, 12),
        "Customer_Count": rng.randint(100, 800, 12),
    })


def save(fig, folder: Path, filename: str, dpi: int) -> None:
    fig.savefig(folder / filename, dpi=dpi, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print(f"Saved: {filename}")


def task2(df: pd.DataFrame, folder: Path, dpi: int) -> None:
    """Pandas line, multiple-line, vertical-bar, and horizontal-bar plots."""
    fig, ax = plt.subplots(figsize=(10, 5))
    df.plot(x="Month", y=PRODUCTS[0], kind="line", marker="o", ax=ax)
    ax.set(title="Product A — Monthly Sales", xlabel="Month", ylabel="Sales ($)")
    ax.grid(alpha=.3)
    fig.tight_layout()
    save(fig, folder, "product_a_sales.png", dpi)

    fig, ax = plt.subplots(figsize=(12, 6))
    df.set_index("Month")[PRODUCTS].plot(kind="line", marker="o", ax=ax)
    ax.set(title="Monthly Sales Comparison", xlabel="Month", ylabel="Sales ($)")
    ax.legend(title="Products")
    ax.grid(alpha=.3)
    fig.tight_layout()
    save(fig, folder, "all_products_sales.png", dpi)

    totals = df[PRODUCTS].sum()
    totals.index = ["Product A", "Product B", "Product C"]
    fig, ax = plt.subplots(figsize=(9, 5))
    totals.plot(kind="bar", ax=ax)
    ax.set(title="Total Annual Sales by Product", xlabel="Product",
           ylabel="Sales ($)")
    ax.tick_params(axis="x", rotation=0)
    ax.grid(axis="y", alpha=.3)
    fig.tight_layout()
    save(fig, folder, "annual_sales_bar.png", dpi)

    fig, ax = plt.subplots(figsize=(10, 6))
    df.set_index("Month")["Marketing_Spend"].plot(kind="barh", ax=ax)
    ax.set(title="Monthly Marketing Spend", xlabel="Spend ($)",
           ylabel="Month")
    ax.grid(axis="x", alpha=.3)
    fig.tight_layout()
    save(fig, folder, "marketing_spend_barh.png", dpi)


def task3(df: pd.DataFrame, folder: Path, dpi: int) -> None:
    """Professional styling: legends, markers, labels, grids, and colors."""
    fig, ax = plt.subplots(figsize=(12, 6))
    styles = [
        ("#2E86AB", "o", "-", "Product A"),
        ("#A23B72", "s", "--", "Product B"),
        ("#F18F01", "^", "-.", "Product C"),
    ]
    for col, (color, marker, line, label) in zip(PRODUCTS, styles):
        ax.plot(df["Month"], df[col], color=color, marker=marker,
                linestyle=line, linewidth=2.5, label=label)
    ax.set(title="Monthly Sales Performance Analysis",
           xlabel="Month", ylabel="Sales ($)")
    ax.legend(title="Products")
    ax.grid(alpha=.3, linestyle=":")
    ax.tick_params(axis="x", rotation=45)
    ax.set_facecolor("#F8F9FA")
    fig.tight_layout()
    save(fig, folder, "customized_line_chart.png", dpi)

    fig, ax = plt.subplots(figsize=(14, 6))
    x = np.arange(len(df))
    width = .25
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1"]
    for i, col in enumerate(PRODUCTS):
        bars = ax.bar(x + (i - 1) * width, df[col], width,
                      label=f"Product {chr(65+i)}", color=colors[i])
        ax.bar_label(bars, padding=2, fontsize=7)
    ax.set_xticks(x, df["Month"], rotation=35)
    ax.set(title="Monthly Sales by Product", xlabel="Month",
           ylabel="Sales ($)")
    ax.set_ylim(0, df[PRODUCTS].to_numpy().max() * 1.18)
    ax.legend(title="Products")
    ax.grid(axis="y", alpha=.3)
    ax.set_axisbelow(True)
    fig.tight_layout()
    save(fig, folder, "customized_bar_chart.png", dpi)


def task4(df: pd.DataFrame, folder: Path, dpi: int) -> None:
    """Histograms reveal distributions; scatter plots reveal associations."""
    rng = np.random.default_rng(42)
    ages = rng.normal(35, 12, 1000)  # Synthetic; may include implausible ages.
    spend = rng.exponential(200, 1000)
    histograms = [
        (ages, 30, "Customer Age Distribution", "Age"),
        (spend, 30, "Customer Spending Distribution", "Spending ($)"),
        (df[PRODUCTS[0]], 8, "Product A Sales Distribution", "Sales ($)"),
        (df["Marketing_Spend"], 8, "Marketing Spend Distribution", "Spend ($)"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    for ax, (values, bins, title, xlabel) in zip(axes.flat, histograms):
        ax.hist(values, bins=bins, alpha=.8, edgecolor="black")
        ax.set(title=title, xlabel=xlabel, ylabel="Frequency")
        ax.grid(axis="y", alpha=.25)
    fig.tight_layout()
    save(fig, folder, "histograms.png", dpi)

    total = df[PRODUCTS].sum(axis=1)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    x = df["Marketing_Spend"].to_numpy()
    y = df[PRODUCTS[0]].to_numpy()
    axes[0, 0].scatter(x, y, alpha=.75)
    coeff = np.polyfit(x, y, 1)
    grid = np.linspace(x.min(), x.max(), 100)
    axes[0, 0].plot(grid, np.polyval(coeff, grid), "r--",
                    label="Linear trend")
    axes[0, 0].legend()
    axes[0, 0].set(title="Marketing vs Product A",
                   xlabel="Marketing Spend ($)", ylabel="Product A Sales ($)")
    axes[0, 1].scatter(df["Customer_Count"], total, alpha=.75)
    axes[0, 1].set(title="Customers vs Total Sales",
                   xlabel="Customer Count", ylabel="Total Sales ($)")
    axes[1, 0].scatter(df[PRODUCTS[0]], df[PRODUCTS[1]], alpha=.75)
    axes[1, 0].set(title="Product A vs Product B", xlabel="Product A",
                   ylabel="Product B")
    dots = axes[1, 1].scatter(df[PRODUCTS[0]], df[PRODUCTS[2]],
                              c=df["Marketing_Spend"],
                              s=df["Customer_Count"] / 2,
                              cmap="viridis", alpha=.75)
    axes[1, 1].set(title="Product A vs Product C", xlabel="Product A",
                   ylabel="Product C")
    fig.colorbar(dots, ax=axes[1, 1], label="Marketing Spend ($)")
    for ax in axes.flat:
        ax.grid(alpha=.2)
    fig.tight_layout()
    save(fig, folder, "scatter_plots.png", dpi)


def task5(df: pd.DataFrame, folder: Path, dpi: int) -> pd.DataFrame:
    """Compute Pearson r; plot two heatmaps and unique-pair strengths."""
    corr = df[COLUMNS].corr()
    corr.round(3).to_csv(folder / "correlation_matrix.csv")
    print("\nCorrelation matrix:\n", corr.round(3).to_string())
    print("Saved: correlation_matrix.csv")

    fig, axes = plt.subplots(1, 2, figsize=(17, 7))
    image = axes[0].imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    axes[0].set_xticks(range(len(COLUMNS)), COLUMNS, rotation=45, ha="right")
    axes[0].set_yticks(range(len(COLUMNS)), COLUMNS)
    axes[0].set_title("Matplotlib Correlation Heatmap")
    for row in range(len(COLUMNS)):
        for col in range(len(COLUMNS)):
            axes[0].text(col, row, f"{corr.iloc[row, col]:.2f}",
                         ha="center", va="center", fontsize=9)
    fig.colorbar(image, ax=axes[0], shrink=.7)
    sns.heatmap(corr, annot=True, fmt=".2f", vmin=-1, vmax=1,
                cmap="coolwarm", ax=axes[1], cbar_kws={"shrink": .7})
    axes[1].set_title("Seaborn Correlation Heatmap")
    axes[1].tick_params(axis="x", labelrotation=45)
    fig.tight_layout()
    save(fig, folder, "correlation_heatmaps.png", dpi)

    pairs = [(f"{a} vs {b}", float(corr.loc[a, b]))
             for i, a in enumerate(COLUMNS)
             for b in COLUMNS[i+1:]]
    pairs.sort(key=lambda p: abs(p[1]), reverse=True)
    print("\nStrong sample correlations (|r| > 0.5):")
    for label, r in pairs:
        if abs(r) > .5:
            print(f"  {label}: {r:+.3f}")
    fig, ax = plt.subplots(figsize=(12, 7))
    values = [v for _, v in pairs]
    colors = ["#4F8571" if r > .5 else "#C77969" if r < -.5
              else "#9AA3A4" for r in values]
    ax.barh([label for label, _ in pairs], values, color=colors)
    ax.invert_yaxis()
    ax.set_xlim(-1, 1)
    ax.axvline(0, color="black")
    for boundary in (-.5, .5):
        ax.axvline(boundary, linestyle="--", alpha=.5)
    ax.set(title="Unique Variable-Pair Correlations",
           xlabel="Pearson correlation coefficient (r)")
    ax.grid(axis="x", alpha=.2)
    fig.tight_layout()
    save(fig, folder, "correlation_strengths.png", dpi)
    return corr


def task6(df: pd.DataFrame, corr: pd.DataFrame,
          folder: Path, dpi: int) -> None:
    """A four-panel dashboard plus three independent exportable charts."""
    total = df[PRODUCTS].sum(axis=1)
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    df.set_index("Month")[PRODUCTS].plot(marker="o", ax=axes[0, 0])
    axes[0, 0].set(title="Monthly Sales Trends", xlabel="Month",
                   ylabel="Sales ($)")
    axes[0, 0].grid(alpha=.3)
    labels = pd.Series(df[PRODUCTS].sum().to_numpy(),
                       index=["Product A", "Product B", "Product C"])
    labels.plot(kind="bar", ax=axes[0, 1])
    axes[0, 1].set(title="Annual Product Sales", ylabel="Sales ($)")
    axes[0, 1].tick_params(axis="x", rotation=0)
    axes[1, 0].scatter(df["Marketing_Spend"], df[PRODUCTS[0]], alpha=.75)
    axes[1, 0].set(title="Marketing vs Product A Sales",
                   xlabel="Marketing Spend ($)", ylabel="Product A Sales ($)")
    sns.heatmap(corr, annot=True, fmt=".2f", vmin=-1, vmax=1,
                cmap="coolwarm", ax=axes[1, 1],
                cbar_kws={"shrink": .7})
    axes[1, 1].set_title("Correlation Matrix")
    axes[1, 1].tick_params(axis="x", labelrotation=45)
    fig.suptitle("Sales Data Analysis Dashboard", fontsize=18,
                 fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, .96))
    for extension in ("png", "jpg", "pdf"):
        fig.savefig(folder / f"sales_dashboard.{extension}", dpi=dpi,
                    bbox_inches="tight", facecolor="white")
        print(f"Saved: sales_dashboard.{extension}")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(12, 6))
    for col in PRODUCTS:
        ax.plot(df["Month"], df[col], marker="o",
                label=col.replace("_", " "))
    ax.set(title="Monthly Sales Trends", xlabel="Month", ylabel="Sales ($)")
    ax.legend()
    ax.grid(alpha=.3)
    fig.tight_layout()
    save(fig, folder, "monthly_sales_trends.png", dpi)

    x = df["Marketing_Spend"].to_numpy()
    y = total.to_numpy()
    coeff = np.polyfit(x, y, 1)
    grid = np.linspace(x.min(), x.max(), 100)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(x, y, alpha=.8)
    ax.plot(grid, np.polyval(coeff, grid), "r--", label="Linear trend")
    ax.set(title="Marketing Spend vs Total Sales", xlabel="Marketing Spend ($)",
           ylabel="Total Sales ($)")
    ax.legend()
    ax.grid(alpha=.3)
    fig.tight_layout()
    save(fig, folder, "marketing_effectiveness.png", dpi)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    for ax, col in zip(axes, PRODUCTS):
        ax.hist(df[col], bins=6, edgecolor="black", alpha=.8)
        ax.set(title=f"{col.replace('_', ' ')} Distribution",
               xlabel="Sales ($)", ylabel="Frequency")
        ax.grid(axis="y", alpha=.2)
    fig.tight_layout()
    save(fig, folder, "sales_distributions.png", dpi)


def verify_outputs(folder: Path) -> None:
    """Check every expected file exists and has a recognizable signature."""
    headers = {".png": b"\x89PNG\r\n\x1a\n", ".jpg": b"\xff\xd8",
               ".pdf": b"%PDF-", ".csv": b""}
    problems = []
    for filename in EXPECTED_FILES:
        path = folder / filename
        if not path.is_file() or path.stat().st_size == 0:
            problems.append(f"Missing/empty: {filename}")
            continue
        with path.open("rb") as file:
            if not file.read(8).startswith(headers[path.suffix]):
                problems.append(f"Invalid signature: {filename}")
        print(f"OK: {filename} ({path.stat().st_size:,} bytes)")
    if problems:
        raise RuntimeError("\n".join(problems))
    print(f"\nSUCCESS: {len(EXPECTED_FILES)} output files verified")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parent / "outputs")
    parser.add_argument("--dpi", type=int, default=160)
    args = parser.parse_args(argv)
    if not (40 <= args.dpi <= 600):
        parser.error("--dpi must be between 40 and 600")
    folder = args.output_dir.resolve()
    folder.mkdir(parents=True, exist_ok=True)
    print("Lab 63 — Data Visualization with Pandas and Matplotlib")
    print(f"Python: {sys.version.split()[0]}, Pandas: {pd.__version__}, "
          f"Matplotlib: {matplotlib.__version__}, NumPy: {np.__version__}")
    print(f"Outputs: {folder}\n")
    df = make_sales_data()
    print("Dataset shape:", df.shape, "\n", df.head().to_string(index=False))
    df.to_csv(folder / "sales_data.csv", index=False)
    print("Saved: sales_data.csv")
    task2(df, folder, args.dpi)
    task3(df, folder, args.dpi)
    task4(df, folder, args.dpi)
    corr = task5(df, folder, args.dpi)
    task6(df, corr, folder, args.dpi)
    verify_outputs(folder)
    print("Note: These are simulated monthly values, not real business metrics.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
