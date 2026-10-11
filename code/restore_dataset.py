"""Reconstruct the project CSV from base64-encoded gzip parts committed in data/.

Run from any directory:
    python code/restore_dataset.py

This uses only Python's standard library and writes data/Union_Budget_Analytical_Dataset.csv.
"""
import base64
import gzip
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
parts = sorted(DATA.glob("dataset_csv_gzip_b64_part_*.txt"))
if not parts:
    raise FileNotFoundError("Dataset parts not found in data/. Check the repository download.")
encoded = "".join(p.read_text(encoding="ascii").strip() for p in parts)
compressed = base64.b64decode(encoded, validate=True)
csv_bytes = gzip.decompress(compressed)
out = DATA / "Union_Budget_Analytical_Dataset.csv"
out.write_bytes(csv_bytes)
print(f"Restored {out} ({len(csv_bytes):,} bytes) from {len(parts)} encoded parts.")
