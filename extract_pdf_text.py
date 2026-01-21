#!/usr/bin/env python3
"""
Extract embedded text from PDF files.
Uses PyMuPDF (fitz) for fast, reliable text extraction without OCR.
"""
import sys
import argparse
from pathlib import Path

try:
    import fitz
except ImportError:
    print("Error: PyMuPDF not installed. Run: pip install PyMuPDF")
    sys.exit(1)


def extract_text(pdf_path: str, output_path: str = None) -> str:
    """
    Extract all embedded text from a PDF file.

    Args:
        pdf_path: Path to the PDF file
        output_path: Optional path to save extracted text

    Returns:
        Extracted text content
    """
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if not pdf_path.suffix.lower() == ".pdf":
        raise ValueError(f"File is not a PDF: {pdf_path}")

    doc = fitz.open(str(pdf_path))
    text_parts = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        page_text = page.get_text()
        if page_text.strip():
            text_parts.append(f"--- Page {page_num + 1} ---\n{page_text}")

    doc.close()

    full_text = "\n\n".join(text_parts)

    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(full_text, encoding="utf-8")
        print(f"Text extracted to: {output_path}")

    return full_text


def main():
    parser = argparse.ArgumentParser(
        description="Extract embedded text from PDF files (no OCR)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.pdf
  %(prog)s document.pdf -o output.txt
  %(prog)s document.pdf --stdout
        """
    )
    parser.add_argument("pdf", help="Path to PDF file")
    parser.add_argument("-o", "--output", help="Output file path (default: <pdf>.txt)")
    parser.add_argument("--stdout", action="store_true", help="Print to stdout instead of file")

    args = parser.parse_args()

    try:
        if args.stdout:
            text = extract_text(args.pdf)
            print(text)
        else:
            output_path = args.output or str(Path(args.pdf).with_suffix(".txt"))
            extract_text(args.pdf, output_path)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
