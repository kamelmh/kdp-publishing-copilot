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

    recto_pdf = os.path.join(output_dir, "master-recto.pdf")
    verso_pdf = os.path.join(output_dir, "master-verso.pdf")

    # Recto master = Page 3 = ODD = right-hand page (gutter on LEFT)
    cr = canvas.Canvas(recto_pdf, pagesize=(TRIM_W, TRIM_H))
    cr.setTitle("Master Recto Page (Page 3)")
    cr.setAuthor("Meridian Press")
    cr.setSubject("Design Template — Right-hand Page")
    cr.setCreator("Master Pages Skill v1.0")
    draw_entry_page(cr, TRIM_W, TRIM_H, entry_no=1, phys_page=3)
    cr.save()

    # Verso master = Page 4 = EVEN = left-hand page (gutter on RIGHT)
    cv = canvas.Canvas(verso_pdf, pagesize=(TRIM_W, TRIM_H))
    cv.setTitle("Master Verso Page (Page 4)")
    cv.setAuthor("Meridian Press")
    cv.setSubject("Design Template — Left-hand Page")
    cv.setCreator("Master Pages Skill v1.0")
    draw_entry_page(cv, TRIM_W, TRIM_H, entry_no=2, phys_page=4)
    cv.save()

    print(f"Master pages generated:")
    print(f"  Recto (p3, gutter LEFT):  {recto_pdf}")
    print(f"  Verso (p4, gutter RIGHT): {verso_pdf}")
    return recto_pdf, verso_pdf


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
        recto_pdf = os.path.join(output_dir, "master-recto.pdf")
        verso_pdf = os.path.join(output_dir, "master-verso.pdf")
        render_dir = os.path.join(output_dir, "renders")

        if not os.path.exists(recto_pdf):
            print(f"ERROR: {recto_pdf} not found. Run without --png-only first.")
            sys.exit(1)

        print("Rendering master pages to PNG...")
        render_pdf_to_png(recto_pdf, render_dir, prefix="master-recto")
        render_pdf_to_png(verso_pdf, render_dir, prefix="master-verso")
        print(f"\nDone! Review PNGs in: {render_dir}")
    else:
        # Generate master PDFs
        recto_pdf, verso_pdf = generate_master_pages(output_dir, args.entries)

        if not args.pdf_only:
            # Also render to PNG
            render_dir = os.path.join(output_dir, "renders")
            print("\nRendering to PNG...")
            render_pdf_to_png(recto_pdf, render_dir, prefix="master-recto")
            render_pdf_to_png(verso_pdf, render_dir, prefix="master-verso")
            print(f"\nDone! Review PNGs in: {render_dir}")


if __name__ == "__main__":
    main()
