# Lab 61 — Data Cleaning with Pandas: Handling Missing Data

Runnable solutions to all five tasks in the supplied Al Nafi Lab 61 brief, plus a complete configuration-driven cleaning pipeline and tests.

## Setup (Ubuntu / Windows / macOS)

Use **Python 3.9+**:

```bash
python3 -m venv .venv
source .venv/bin/activate                  # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Run

```bash
python pandas_lab.py
python -m unittest -v test_pandas_lab.py
```

The script prints demonstrations and writes 11 CSV files to an ignored `output/` directory. To use a different output folder: `python pandas_lab.py --output-dir demo-results`.

## Lab coverage

| Task | Implementation |
| --- | --- |
| 1 — Missing values | `isna`, counts/percentages, median/mean/mode/forward fill, `dropna` variations |
| 2 — Duplicates | `duplicated`, all-column and subset-based `drop_duplicates`, first/last occurrence |
| 3 — Data types | Numeric, dates, correct string-to-boolean conversion; `errors='coerce'` on invalid strings |
| 4 — Scaling | Min-max, Z-score and IQR/median robust scaling, including zero-spread handling |
| 5 — Categories | Ordinal mapping, scikit-learn `LabelEncoder` example, one-hot encoding, city frequency and target means |
| Final — Cleaning pipeline | Configurable missing values, duplicates, conversions, scaling and categorical encoding |

## Notes

- The lab's `pd.to_numeric(..., errors='ignore')` example is deprecated in modern Pandas; this project retains the raw column separately and demonstrates `errors='coerce'`.
- `astype(bool)` on the string `'False'` yields `True`. The `parse_boolean` helper explicitly maps text to true/false instead.
- Ordinal values have meaningful order; `LabelEncoder`'s alphabetical codes should **not** be interpreted as an ordinal ranking. The mapped columns preserve the intended order.
- The high-cardinality sample has **one row per city**, so frequency is always 1 and in-sample mean target encoding equals the target. For real ML, use out-of-fold target encoding to avoid leakage.
- The supplied lab brief ends mid-expression in its final pipeline normalization example; the completed pipeline is an implementation based on its five documented tasks, not a verbatim continuation of missing source text.
- Each dataset uses **synthetic demonstration records**; generated CSVs are not real personal data.