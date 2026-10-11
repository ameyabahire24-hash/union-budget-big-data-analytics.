# Data folder

The full working CSV is stored as numbered base64 text parts containing a gzip-compressed CSV, to keep repository text uploads manageable. Run `python code/restore_dataset.py` to rebuild `data/Union_Budget_Analytical_Dataset.csv`. The rebuilt CSV is ignored by Git. Missing values remain null; see the root README and `docs/PROJECT_REPORT.md` for limitations.