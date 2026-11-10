# Lab 62 — Advanced Pandas Operations: Merging and Grouping Data

A complete, reproducible implementation of **Lab 62**, based on the supplied lab handout. Includes all five tasks and the comprehensive retail exercise.

## Covered topics

1. **Merge:** inner, left, right, and outer joins on `customer_id`.
2. **Concatenation:** vertical, horizontal, deduplicated columns, and keyed MultiIndex.
3. **GroupBy:** sums, means, counts, multiple grouping columns, custom aggregations.
4. **Pivot tables:** single/multiple metrics, multiple functions, margins, monthly analysis.
5. **MultiIndex:** hierarchical creation, lookups, `.xs()`, `.stack()`, `.unstack()`, `.reset_index()`, and pivoting.
6. **Retail exercise:** seeded 100-transaction dataset merged to customer demographics, store summaries, membership-level pivots, chronologically sorted monthly trends and customer segments.

**Important fix:** The handout's *Troubleshooting Common Issues* section includes non-executable placeholders such as `df1`, `df2`, `col1`, `large_file.csv` and `multi_index_df`. Those are explanatory examples, **not** commands to append to the actual lab. The executable lab uses defined DataFrames and demonstrates `.xs()` against `sales_multi`.

## Install and run (Ubuntu)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python lab_62.py
python -m unittest -v test_lab_62.py
```

Optionally export nine analysis CSV files with:

```bash
python lab_62.py --output-dir outputs
```

There is **no requirement for scikit-learn**. No external input CSV file is needed; datasets are created reproducibly in code. `LAB 62 COMPLETED SUCCESSFULLY!` prints at the *very end* of the script, not before potentially failing statements.

## Expected verification

`python -m unittest -v test_lab_62.py` checks joins, sales totals, pivot-table grand totals, MultiIndex operations, dataset integrity, reproducibility, month order, and optional exports. Test results depend on local Python/pandas versions, and should always be run after installation.
