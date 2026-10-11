# Union Budget Big Data Analytics

**Project:** A Decade of Departmental Spending and Sectoral Priorities  
**Tools:** Python, PySpark, Pandas, Matplotlib, Jupyter Notebook, Excel

This repository contains a preliminary analysis package for exploring Indian Union Budget departmental spending over the available financial years.

## Repository structure

- `Union_Budget_Analytical_Dataset.csv` — working extracted data for PySpark.
- `Union_Budget_Analytical_Dataset.xlsx` — dataset workbook.
- `Union_Budget_PySpark_Analysis.ipynb` — notebook for quality checks and exploratory analysis.
- `code/pyspark_analysis.py` — PySpark starter analysis script.
- `code/extract_budget_pdfs.py` — page-level PDF text extraction audit utility.
- `graphs/` — ten exploratory charts.
- `annual_summary.csv` and `sector_summary.csv` — derived summary tables.
- `Final_Project_Report_Draft.docx` — report draft with chart explanations and limitations.

## Getting started

1. Install Python 3.10+, Java, and Jupyter.
2. Install libraries:

   ```bash
   pip install pandas openpyxl matplotlib pyspark pymupdf jupyter python-docx
   ```

3. Open `Union_Budget_PySpark_Analysis.ipynb` in Jupyter, or run:

   ```bash
   python code/pyspark_analysis.py
   ```

   Make sure the CSV path in the script points to `Union_Budget_Analytical_Dataset.csv`.

## Data quality and limitations — read before interpreting results

This is a **preliminary, not fully validated extraction**. The current working table has 1,115 records across 11 represented financial years. The source PDFs for 2013–14 and 2015–16 are not represented in these demand rows. Some numeric values are missing, and category/budget-basis consistency between years has not been fully verified.

- Missing values are kept as nulls; they must not automatically be treated as zero.
- Figures and source PDF page references should be reconciled against official Union Budget documents before making final conclusions.
- Sector groupings are exploratory keyword-based categories, not official ministry classifications.
- Charts summarize the currently recorded extracted rows and should not be described as complete official Union Budget totals.

## Source documents

Use the official Union Budget portal for source verification: https://www.indiabudget.gov.in/

## Purpose

The code and visuals are intended as a transparent starting point for departmental trend analysis and data-quality validation, not as a claim that all budget PDFs have been completely or perfectly extracted.