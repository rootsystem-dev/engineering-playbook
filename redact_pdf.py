# -*- coding: utf-8 -*-
import fitz  # PyMuPDF
import re
import argparse
import os

def redact_pdf(input_path, output_path, redact_terms):
    doc = fitz.open(input_path)
    
    for page in doc:
        full_text = page.get_text("text")
        
        for term in redact_terms:
            if not term.strip():
                continue
            for match in re.finditer(re.escape(term), full_text, re.IGNORECASE):
                to_redact = match.group(0).strip()
                if to_redact:
                    for rect in page.search_for(to_redact):
                        page.add_redact_annot(rect, fill=(0, 0, 0))
        
        page.apply_redactions()
    
    doc.save(output_path, garbage=1, deflate=True, clean=1)
    doc.close()
    print(f"[OK] Created: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="redact_pdf.py",
        description="PDF Redactor — Permanently black-out terms from a list.\n"
                    "Works on one PDF or an entire folder.\n"
                    "Creates new files only (never touches originals).",
        epilog="""Examples:

  Single PDF:
    python3.9 redact_pdf.py "MyDocument.pdf" redact.txt

  Entire folder:
    python3.9 redact_pdf.py "/Users/xxx/Documents/PDFs" redact.txt

How to make redact.txt:
  One term per line (case doesn't matter):
    John Doe
    1200 fairfield ave, bronx, ny 10012
    085-111-1111
    0851111111
    Stealthware Inc.
    TaxPrep Masters

The script will create:
    MyDocument-redacted.pdf
    AnotherFile-redacted.pdf
    ... etc.

Tip: Run this script again anytime — it skips any file that already ends with -redacted.pdf""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("pdf_path", 
                        help="Single PDF file OR folder containing PDFs")
    parser.add_argument("list_file", 
                        help="Plain text file with one redaction term per line")

    args = parser.parse_args()

    # Read the list
    with open(args.list_file, "r", encoding="utf-8") as f:
        redact_terms = [line.strip() for line in f if line.strip()]

    print(f"Loaded {len(redact_terms)} term(s) to redact.")

    if os.path.isfile(args.pdf_path) and args.pdf_path.lower().endswith(".pdf"):
        base, ext = os.path.splitext(args.pdf_path)
        output = base + "-redacted" + ext
        redact_pdf(args.pdf_path, output, redact_terms)

    elif os.path.isdir(args.pdf_path):
        for filename in os.listdir(args.pdf_path):
            if filename.lower().endswith(".pdf") and not filename.lower().endswith("-redacted.pdf"):
                input_file = os.path.join(args.pdf_path, filename)
                base, ext = os.path.splitext(filename)
                output_file = os.path.join(args.pdf_path, base + "-redacted" + ext)
                redact_pdf(input_file, output_file, redact_terms)
    else:
        print("Error: Please provide a PDF file or a folder containing PDFs.")