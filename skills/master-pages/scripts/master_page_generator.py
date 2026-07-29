#!/usr/bin/env python3
"""
Master Page Generator — KDP Interior Design Tool
Generates left (verso) and right (recto) template pages for layout review.

Usage:
    python master_page_generator.py              # Generate masters + render PNGs
    python master_page_generator.py --pdf-only   # Generate PDFs only
    python master_page_generator.py --png-only   # Render existing PDFs only
"""

import os
import sys
import argparse

# Import from single source of truth (in kdp-print skill)
kdp_print_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "kdp-print")
sys.path.insert(0, kdp_print_dir)

from entry_page import (
    TRIM_W, TRIM_H, draw_entry_page, DGRAY, MGRAY, LGRAY,
    HEADER_BG, BAR_COLOR, BAR_TEXT_COLOR
)

from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


def generate_master_pages(output_dir, entry_count=110):
    """
    Generate master page pair (left + right) for design review.
    Returns (left_pdf, right_pdf) paths.
    """
    os.makedirs(output_dir, exist_ok=True)

    left_pdf = os.path.join(output_dir, "master-left.pdf")
    right_pdf = os.path.join(output_dir, "master-right.pdf")

    # Left master = Page 3 = ODD = RECTO (gutter on LEFT)
    cl = canvas.Canvas(left_pdf, pagesize=(TRIM_W, TRIM_H))
    cl.setTitle("Master Left Page (Recto — Page 3)")
    cl.setAuthor("Meridian Press")
    cl.setSubject("Design Template — Left Page")
    cl.setCreator("Master Pages Skill v1.0")
    draw_entry_page(cl, TRIM_W, TRIM_H, entry_no=1, phys_page=3)
    cl.save()

    # Right master = Page 4 = EVEN = VERSO (gutter on RIGHT)
    cr = canvas.Canvas(right_pdf, pagesize=(TRIM_W, TRIM_H))
    cr.setTitle("Master Right Page (Verso — Page 4)")
    cr.setAuthor("Meridian Press")
    cr.setSubject("Design Template — Right Page")
    cr.setCreator("Master Pages Skill v1.0")
    draw_entry_page(cr, TRIM_W, TRIM_H, entry_no=2, phys_page=4)
    cr.save()

    print(f"Master pages generated:")
    print(f"  Left (recto, p3):  {left_pdf}")
    print(f"  Right (verso, p4): {right_pdf}")
    return left_pdf, right_pdf


def render_pdf_to_png(pdf_path, output_dir, prefix="page"):
    """Render PDF pages to PNGs. Requires PyMuPDF."""
    try:
        import fitz
    except ImportError:
        print("ERROR: PyMuPDF not installed. Run: pip install PyMuPDF")
        return []

    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    rendered = []

    for i in range(len(doc)):
        page = doc[i]
        mat = fitz.Matrix(200/72, 200/72)  # 200 DPI
        pix = page.get_pixmap(matrix=mat)
        out_path = os.path.join(output_dir, f"{prefix}-{i+1:03d}.png")
        pix.save(out_path)
        rendered.append(out_path)
        print(f"  Rendered: {out_path}")

    doc.close()
    return rendered


def main():
    parser = argparse.ArgumentParser(
        description="KDP Master Page Generator — design templates for interior layouts"
    )
    parser.add_argument("--pdf-only", action="store_true",
                        help="Generate PDFs only (no PNG renders)")
    parser.add_argument("--png-only", action="store_true",
                        help="Render existing master PDFs to PNG only")
    parser.add_argument("--output-dir", type=str, default=None,
                        help="Output directory")
    parser.add_argument("--entries", type=int, default=110,
                        help="Entry count for page numbering (default: 110)")
    args = parser.parse_args()

    # Default: books/notary-log-book/master-pages/ (repo root)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Navigate up: scripts -> master-pages -> skills -> repo root
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
    default_output = os.path.join(repo_root, "books", "notary-log-book", "master-pages")
    output_dir = args.output_dir or default_output

    if args.png_only:
        # Render existing PDFs
        left_pdf = os.path.join(output_dir, "master-left.pdf")
        right_pdf = os.path.join(output_dir, "master-right.pdf")
        render_dir = os.path.join(output_dir, "renders")

        if not os.path.exists(left_pdf):
            print(f"ERROR: {left_pdf} not found. Run without --png-only first.")
            sys.exit(1)

        print("Rendering master pages to PNG...")
        render_pdf_to_png(left_pdf, render_dir, prefix="master-left")
        render_pdf_to_png(right_pdf, render_dir, prefix="master-right")
        print(f"\nDone! Review PNGs in: {render_dir}")
    else:
        # Generate master PDFs
        left_pdf, right_pdf = generate_master_pages(output_dir, args.entries)

        if not args.pdf_only:
            # Also render to PNG
            render_dir = os.path.join(output_dir, "renders")
            print("\nRendering to PNG...")
            render_pdf_to_png(left_pdf, render_dir, prefix="master-left")
            render_pdf_to_png(right_pdf, render_dir, prefix="master-right")
            print(f"\nDone! Review PNGs in: {render_dir}")


if __name__ == "__main__":
    main()
