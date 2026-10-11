"""Create a page-level text audit from official Union Budget PDFs.

Place source PDFs in budget_pdfs/ and run this script from the repository root.
It does not attempt to silently convert table text into validated numbers.
Scanned PDFs may need OCR; all extracted figures require manual/source validation.
"""
from pathlib import Path
import fitz
import pandas as pd

PDF_DIR = Path("budget_pdfs")
rows = []
for pdf in sorted(PDF_DIR.glob("*.pdf")):
    with fitz.open(pdf) as doc:
        for page_no, page in enumerate(doc, start=1):
            text = page.get_text("text")
            if text.strip():
                rows.append({
                    "Source_File": pdf.name,
                    "Page_Number": page_no,
                    "Extracted_Text": text
                })

out = Path("pdf_page_text_audit.jsonl")
pd.DataFrame(rows).to_json(out, orient="records", lines=True, force_ascii=False)
print(f"Saved {len(rows)} text-bearing pages to {out}. Verify figures and page references.")
