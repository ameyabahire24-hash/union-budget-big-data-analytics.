"""Extract the compressed working CSV from data/.

Run from any directory:
    python code/restore_dataset.py

This uses only Python's standard library. The source is gzip-compressed CSV.
"""
import gzip
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
source = DATA / "Union_Budget_Analytical_Dataset.csv.gz"
out = DATA / "Union_Budget_Analytical_Dataset.csv"

if not source.is_file():
    raise FileNotFoundError(f"Compressed dataset not found: {source}")
with gzip.open(source, "rb") as compressed:
    out.write_bytes(compressed.read())
print(f"Restored {out}")
