#!/usr/bin/env python3
"""
Master Page Generator — KDP Interior Design Tool
Generates left (verso) and right (recto) template pages for layout review.
Like InDesign master pages — iterate without regenerating 120+ pages.

Usage:
    python master_page_generator.py              # Generate masters + render PNGs
    python master_page_generator.py --pdf-only   # Generate PDFs only
    python master_page_generator.py --png-only   # Render existing PDFs only
"""

import os
import sys
import argparse

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white

# ─── Design Tokens (edit these to iterate) ────────────────────────────────────
# Grey palette (professional, minimal)
BAR_COLOR = HexColor("#E8E8E8")        # Light grey section bars
BAR_TEXT_COLOR = HexColor("#444444")    # Dark grey text on bars
HEADER_BG = HexColor("#F5F5F5")        # Very light grey for headers
ACCENT_LINE = HexColor("#CCCCCC")      # Subtle accent lines
DGRAY = HexColor("#333333")            # Primary text
MGRAY = HexColor("#666666")            # Secondary text
LGRAY = HexColor("#B8C0CC")            # Light accents

# Page dimensions
TRIM_W = 6 * inch
TRIM_H = 9 * inch
TOP_MARGIN = 0.625 * inch
BOTTOM_MARGIN = 0.375 * inch
FOOTER_BASELINE = 21
FOOTER_GUARD = 36


# ─── Helper Functions ──────────────────────────────────────────────────────────

def _margins_for_page(phys_page):
    """Mirror margins: gutter always on binding edge."""
    gutter = 0.5 * inch
    outside = 0.3 * inch
    if phys_page % 2 == 1:  # Odd = verso (left page, gutter on right)
        return outside, gutter, False
    else:  # Even = recto (right page, gutter on left)
        return gutter, outside, True


def _section_bar(c, x, y, width, text):
    """Light grey section bar with dark text."""
    h = 13
    c.setFillColor(BAR_COLOR)
    c.rect(x, y, width, h, fill=1, stroke=0)
    c.setFillColor(BAR_TEXT_COLOR)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 4, y + 3, text)


def _writeline(c, x, y, width):
    """Writing line for fill-in fields."""
    c.setStrokeColor(HexColor("#DDDDDD"))
    c.setLineWidth(0.4)
    c.line(x, y, x + width, y)


def _checkbox(c, x, y, size=8):
    """Empty checkbox square."""
    c.setStrokeColor(DGRAY)
    c.setLineWidth(0.5)
    c.rect(x, y, size, size, fill=0, stroke=1)


def _thumbprint(c, x, y, size):
    """Thumbprint box with label."""
    c.setStrokeColor(DGRAY)
    c.setLineWidth(0.8)
    c.rect(x, y, size, size, fill=0, stroke=1)
    c.setFillColor(MGRAY)
    c.setFont("Helvetica", 7)
    c.drawCentredString(x + size/2, y + size/2 + 4, "RIGHT")
    c.drawCentredString(x + size/2, y + size/2 - 6, "THUMB")
    c.setFont("Helvetica", 6)
    c.drawCentredString(x + size/2, y - 10, "Signer's Right Thumbprint")


def _seal(c, cx, cy, r=28):
    """Official seal placeholder (dashed circle)."""
    c.setStrokeColor(DGRAY)
    c.setLineWidth(0.8)
    c.setDash(3, 3)
    c.circle(cx, cy, r, fill=0, stroke=1)
    c.setDash()
    c.setFillColor(MGRAY)
    c.setFont("Helvetica", 6.5)
    c.drawCentredString(cx, cy + 3, "OFFICIAL")
    c.drawCentredString(cx, cy - 7, "SEAL")


def draw_page_number(c, W, phys_page):
    """Centered page number at bottom."""
    c.setFillColor(LGRAY)
    c.setFont("Helvetica", 7)
    c.drawCentredString(W / 2, FOOTER_BASELINE, str(phys_page))


# ─── Entry Page ────────────────────────────────────────────────────────────────

def draw_entry_page(c, W, H, entry_no, phys_page):
    """Draw a single notary entry page."""
    lm, rm, outer_right = _margins_for_page(phys_page)
    top = TOP_MARGIN
    uw = W - lm - rm
    RH = 16  # row height

    # Header bar
    hb_h = 24
    y = H - top - hb_h
    c.setFillColor(HEADER_BG)
    c.rect(lm, y, uw, hb_h, fill=1, stroke=0)
    c.setFillColor(DGRAY)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(lm + 6, y + 8, "NOTARIAL ACT RECORD")
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(lm + uw - 6, y + 8, f"Entry No. {entry_no:03d}")
    y -= 12

    # A — Date & Time
    _section_bar(c, lm, y - 13, uw, "A — DATE & TIME")
    y -= 13 + 6
    c.setFillColor(DGRAY)
    c.setFont("Helvetica", 8.5)
    c.drawString(lm, y, "Date:")
    _writeline(c, lm + 45, y - 2, 130)
    c.drawString(lm + 190, y, "Time:")
    _writeline(c, lm + 220, y - 2, 60)
    _checkbox(c, lm + 290, y - 1)
    c.drawString(lm + 301, y, "AM")
    _checkbox(c, lm + 324, y - 1)
    c.drawString(lm + 335, y, "PM")
    y -= RH + 3

    # B — Type of Notarial Act
    _section_bar(c, lm, y - 13, uw, "B — TYPE OF NOTARIAL ACT")
    y -= 13 + 6
    c.setFillColor(DGRAY)
    c.setFont("Helvetica", 8)
    row1 = ["Acknowledgment", "Oath / Affirmation", "Copy Certification"]
    cx = lm
    for a in row1:
        _checkbox(c, cx, y - 1)
        c.drawString(cx + 11, y, a)
        cx += 11 + c.stringWidth(a, "Helvetica", 8) + 18
    y -= RH
    row2 = ["Signature Witnessing", "Jurat"]
    cx = lm
    for a in row2:
        _checkbox(c, cx, y - 1)
        c.drawString(cx + 11, y, a)
        cx += 11 + c.stringWidth(a, "Helvetica", 8) + 18
    _checkbox(c, cx, y - 1)
    c.drawString(cx + 11, y, "Other:")
    _writeline(c, cx + 11 + c.stringWidth("Other:", "Helvetica", 8) + 6, y - 2, lm + uw - cx - 60)
    y -= RH + 3

    # C — Document Information
    _section_bar(c, lm, y - 13, uw, "C — DOCUMENT INFORMATION")
    y -= 13 + 6
    for lbl in ["Document Type:", "Document Date / No. of Pages:", "Description / Title:"]:
        c.setFillColor(DGRAY)
        c.setFont("Helvetica", 8.5)
        c.drawString(lm, y, lbl)
        lw = c.stringWidth(lbl, "Helvetica", 8.5)
        _writeline(c, lm + lw + 6, y - 2, uw - lw - 8)
        y -= RH
    y -= 3

    # D — Signer Information
    _section_bar(c, lm, y - 13, uw, "D — SIGNER INFORMATION")
    y -= 13 + 6
    for lbl in ["Full Name:", "Address:", "ID Type / Number / Exp.:", "Signer's Signature:"]:
        c.setFillColor(DGRAY)
        c.setFont("Helvetica", 8.5)
        c.drawString(lm, y, lbl)
        lw = c.stringWidth(lbl, "Helvetica", 8.5)
        _writeline(c, lm + lw + 6, y - 2, uw - lw - 8)
        y -= RH
    y -= 3

    # E — Witness + F — Thumbprint
    e_top = y
    ew = uw * 0.58
    ex = lm if outer_right else (lm + uw - ew)
    _section_bar(c, ex, e_top - 13, ew, "E — WITNESS (IF APPLICABLE)")
    thumb = 72
    thumb_x = (lm + uw - thumb) if outer_right else lm
    _thumbprint(c, thumb_x, e_top - 15 - thumb, thumb)
    yw = e_top - 13 - 8
    for lbl in ["Witness Name:", "Signature:"]:
        c.setFillColor(DGRAY)
        c.setFont("Helvetica", 8.5)
        c.drawString(ex, yw, lbl)
        lw = c.stringWidth(lbl, "Helvetica", 8.5)
        _writeline(c, ex + lw + 4, yw - 2, ew - lw - 6)
        yw -= RH
    y = e_top - 98

    # G — Fees
    _section_bar(c, lm, y - 13, uw, "G — FEES")
    y -= 13 + 6
    c.setFillColor(DGRAY)
    c.setFont("Helvetica", 8.5)
    c.drawString(lm, y, "Fee Charged: $")
    _writeline(c, lm + 78, y - 2, 80)
    cx = lm + 175
    for p in ["Cash", "Check", "Elec.", "Waived"]:
        _checkbox(c, cx, y - 1)
        c.drawString(cx + 11, y, p)
        cx += 11 + c.stringWidth(p, "Helvetica", 8.5) + 12
    y -= RH + 3

    # H — Notary Certification & Signature
    _section_bar(c, lm, y - 13, uw, "H — NOTARY CERTIFICATION & SIGNATURE")
    y -= 13 + 6
    c.setFillColor(MGRAY)
    c.setFont("Helvetica-Oblique", 7)
    c.drawString(lm, y, "I certify that the signer personally appeared before me on the date stated above.")
    y -= 14
    seal_cx = (lm + uw - 34) if outer_right else (lm + 34)
    _seal(c, seal_cx, y - 22, r=28)
    sig_w = uw - 76
    sig_x = lm if outer_right else (lm + 76)
    for lbl in ["Notary Name:", "Commission # / Exp.:", "Notary Signature:"]:
        c.setFillColor(DGRAY)
        c.setFont("Helvetica", 8.5)
        c.drawString(sig_x, y, lbl)
        lw = c.stringWidth(lbl, "Helvetica", 8.5)
        _writeline(c, sig_x + lw + 4, y - 2, sig_w - lw - 6)
        y -= RH
    y -= 3

    # I — Remarks
    _section_bar(c, lm, y - 13, uw, "I — REMARKS")
    y -= 13 + 8
    for _ in range(3):
        _writeline(c, lm, y - 2, uw)
        y -= RH

    # Footer
    draw_page_number(c, W, phys_page)
    c.showPage()


# ─── Master Page Generator ────────────────────────────────────────────────────

def generate_master_pages(output_dir, entry_count=110):
    """
    Generate master page pair (left + right) for design review.
    Returns (left_pdf, right_pdf) paths.
    """
    os.makedirs(output_dir, exist_ok=True)

    left_pdf = os.path.join(output_dir, "master-left.pdf")
    right_pdf = os.path.join(output_dir, "master-right.pdf")

    # Left master (verso — odd page, gutter on RIGHT)
    cl = canvas.Canvas(left_pdf, pagesize=(TRIM_W, TRIM_H))
    cl.setTitle("Master Left Page (Verso)")
    cl.setAuthor("Meridian Press")
    cl.setSubject("Design Template — Left Page")
    cl.setCreator("Master Pages Skill v1.0")
    draw_entry_page(cl, TRIM_W, TRIM_H, entry_no=1, phys_page=3)
    cl.save()

    # Right master (recto — even page, gutter on LEFT)
    cr = canvas.Canvas(right_pdf, pagesize=(TRIM_W, TRIM_H))
    cr.setTitle("Master Right Page (Recto)")
    cr.setAuthor("Meridian Press")
    cr.setSubject("Design Template — Right Page")
    cr.setCreator("Master Pages Skill v1.0")
    draw_entry_page(cr, TRIM_W, TRIM_H, entry_no=2, phys_page=4)
    cr.save()

    print(f"Master pages generated:")
    print(f"  Left (verso):  {left_pdf}")
    print(f"  Right (recto): {right_pdf}")
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


# ─── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="KDP Master Page Generator — design templates for interior layouts"
    )
    parser.add_argument("--pdf-only", action="store_true",
                        help="Generate PDFs only (no PNG renders)")
    parser.add_argument("--png-only", action="store_true",
                        help="Render existing master PDFs to PNG only")
    parser.add_argument("--output-dir", type=str, default=None,
                        help="Output directory (default: books/notary-log-book/master-pages)")
    parser.add_argument("--entries", type=int, default=110,
                        help="Entry count for page numbering (default: 110)")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    default_output = os.path.join(base_dir, "books", "notary-log-book", "master-pages")
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
        print(f"\nDone! Review in: {render_dir}")
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
