# Union Budget Big Data Analytics
## A Decade of Departmental Spending and Sectoral Priorities

### Aim
Explore extracted Union Budget demand-level spending over the financial years represented in the working table, using data-quality checks, descriptive statistics, and visual analysis with Python and PySpark.

### Tools
Python, PySpark, Pandas, Matplotlib, Jupyter Notebook, Excel, and PyMuPDF for page-level PDF text auditing.

### Current dataset profile
The current working table has 1,115 rows and 144 unique department/demand labels across 11 represented financial years: 2014–15 and 2016–17 through 2025–26. The provided PDFs for 2013–14 and 2015–16 are not represented in this extracted table.

The numeric columns contain missing values: Revenue_Cr has 19, Capital_Cr has 200, and Total_Cr has 9. Missing cells remain null rather than being treated as zero. There are no duplicate Financial_Year + Demand_No keys in the current table, but that check alone does not establish source accuracy.

### Exploratory observations
The accompanying annual summary shows the *recorded extracted total* rising from about ₹1,765,141.96 crore in 2014–15 to about ₹5,065,345.04 crore in 2025–26. These are sums over the currently recorded rows, not verified consolidated Union Budget totals. The years 2015–16 is absent, so the growth series is not a complete contiguous decade.

Keyword-based sector summaries indicate growth in several recorded categories, including defence and infrastructure. The broad “Other/Unclassified” bucket is large, which limits precision and reflects the exploratory nature of the sector labels. These categories are not official ministry classifications.

### Visualizations
The project package produced ten exploratory plots: recorded annual trend; year-on-year change; top departments; largest observed changes; department/year heatmap; sector trends; sector composition; indexed growth; budget concentration; and growth versus consistency. Read them as exploratory summaries of the current data, not final findings about all government spending.

### Data limitations
- Extraction is preliminary and has not been fully reconciled to the official source PDFs.
- 2013–14 and 2015–16 source PDFs are not present in the extracted demand-level rows.
- Budget basis and classifications may differ across years.
- Missing values are retained as nulls and must be checked against source tables.
- Sector assignment uses exploratory keyword rules.
- Individual figures should be checked against their source PDF, relevant page, budget basis (Actual/BE/RE), and units before final submission.

### Next steps before submission
1. Extract or manually reconcile missing financial years.
2. Record source PDF and page for each numeric observation and validate the unit/crores conversion.
3. Standardize the budget basis and compare like with like (Actual, BE, and RE must not be conflated).
4. Audit missing values and department-name changes against the original statements.
5. Rerun the PySpark analysis and regenerate all plots from the reconciled dataset.

### Official starting point
Government of India Union Budget portal: https://www.indiabudget.gov.in/
