# Union Budget Big Data Analytics

**Project:** A Decade of Departmental Spending and Sectoral Priorities  
**Tools:** Python, PySpark, Pandas, Matplotlib, Jupyter Notebook, Excel

This repository contains code, an exploratory dataset, summary tables, and a report draft for studying Union Budget departmental spending.

## Start here

1. Clone or download this repository.
2. Install dependencies with `pip install -r requirements.txt`.
3. Restore the CSV from the encoded parts:
   ```bash
   python code/restore_dataset.py
   ```
4. Run the PySpark analysis:
   ```bash
   python code/pyspark_analysis.py
   ```
5. Regenerate the 10 exploratory charts:
   ```bash
   python code/generate_graphs.py
   ```
   Alternatively, open `Union_Budget_PySpark_Analysis.ipynb` in Jupyter (with Java/PySpark installed).

The full working CSV is also available as `data/Union_Budget_Analytical_Dataset.csv.gz`. The numbered `dataset_csv_gzip_b64_part_*.txt` files provide a text-only reconstruction method for `code/restore_dataset.py`.

## Repository contents

- `Union_Budget_PySpark_Analysis.ipynb` — PySpark notebook with data checks and exploratory analysis.
- `code/pyspark_analysis.py` — runnable PySpark analysis.
- `code/generate_graphs.py` — generates ten charts into `graphs/`.
- `code/extract_budget_pdfs.py` — page-level text audit utility for source PDFs.
- `code/restore_dataset.py` — restores the CSV from the encoded compressed archive parts.
- `data/Union_Budget_Analytical_Dataset.csv.gz` — compressed 1,115-row working table.
- `annual_summary.csv`, `sector_summary.csv` — exploratory summaries of recorded extracted values.
- `docs/PROJECT_REPORT.md` — report draft and interpretation limits.
- `requirements.txt` — Python dependencies.

The Excel workbook, Word report draft, and the original packaged PNG chart set are available in the accompanying project ZIP, but are not uploaded as binary assets in this repository. The charts can be recreated with the included script.

## Data quality and limitations — important

This is a **preliminary, not fully validated extraction**. The current working table has 1,115 records across 11 represented financial years: 2014–15 and 2016–17 through 2025–26. The supplied PDFs for 2013–14 and 2015–16 are not represented in the extracted demand rows. Numeric values are missing from some columns, and budget-basis consistency between years has not been fully verified.

- Missing values are kept as nulls; do not automatically replace them with zero.
- The figures are not reconciled row by row to the official source PDFs and page numbers.
- Check the source PDF, page, unit and budget basis (Actual, BE, RE) before making final claims.
- Sector groupings are exploratory keyword-based categories, not official ministry classifications.
- Annual sums represent recorded extracted rows, not complete official consolidated Union Budget totals.
- The represented years are not contiguous, so year-on-year growth must be interpreted cautiously.

## Source portal

Government of India Union Budget portal: https://www.indiabudget.gov.in/

The project is intended as a transparent starting point for further extraction, validation, and analysis—not as a claim that all budget PDFs have been completely or perfectly parsed.
