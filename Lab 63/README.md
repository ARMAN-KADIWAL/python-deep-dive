# Lab 63 — Data Visualization with Pandas and Matplotlib

Six completed tasks, the learner's submitted Python code, and a permanent visual proof gallery in GitHub.

**[Open the full Lab 63 proof gallery](proof/README.md)** · **[View submitted Python source](lab_63.py)**

## Learning summary

| Task | What it covers | Proof |
|---|---|---|
| 1 | Environment and libraries | Printed library versions |
| 2 | Pandas line charts, bar charts | Four PNG files |
| 3 | Chart style, legend, axis labels, markers | Two PNG files |
| 4 | Histograms and scatter plots | Two PNG files |
| 5 | Pearson correlation matrices and heatmaps | One CSV and two PNG files |
| 6 | Four-panel dashboard, export and verification | Three dashboard formats and three individual PNG files |

## Run the exact submitted plotting logic

The uploaded lab_63.py has been used as the project source. **74 Python comment lines were removed**, and no new comment lines were added. Plot commands, sample data and output names were preserved.

Install and run from inside this folder:

~~~bash
python3 -m pip install -r requirements.txt
python3 lab_63.py
python3 -m unittest -v test_lab_63.py
~~~

The script saves charts in the current working directory. To keep them organized:

~~~bash
mkdir -p proof
cd proof
python3 ../lab_63.py
~~~

The Agg backend works in a Linux/cloud terminal without a graphical desktop.

## Visual proof

The [proof folder](proof/) contains all **17 generated outputs**: 14 PNG charts, one JPG dashboard, one PDF dashboard, and one correlation CSV file.

A GitHub Actions workflow independently executes the comment-free source, validates results and publishes proof files into the repository. The gallery images are **regenerated from the uploaded script**, rather than byte-identical copies of uploaded images. Differences in fonts and plotting-library versions can change image bytes.

Five automated tests validate syntax/comment removal, execution, output names, file signatures and correlation matrix properties.

## How to interpret the results

- Product A has the highest total annual sales **in the synthetic sample**.
- Product A and Product B have a negative sample correlation of approximately -0.71.
- Correlation is an association, not evidence of cause and effect.
- The marketing-spend trend line is exploratory, not a proven marketing effect.
- All monthly sales values were created from seeded random numbers, not real sales.

## Project files

~~~text
Lab 63/
├── lab_63.py
├── test_lab_63.py
├── requirements.txt
├── .gitignore
├── README.md
└── proof/
    ├── README.md
    ├── sales_dashboard.png
    ├── sales_dashboard.jpg
    ├── sales_dashboard.pdf
    ├── correlation_matrix.csv
    └── 13 additional PNG images
~~~
