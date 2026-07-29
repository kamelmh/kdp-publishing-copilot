#!/usr/bin/env python3
"""
Improved Notary Public Record Journal - Interior Generator
Fixes all issues identified in INTERIOR_ANALYSIS.md
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white, Color
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ─── Colors ──────────────────────────────────────────────────────────────────
NAVY = HexColor("#1B2A4A")
STEEL = HexColor("#3A5A8C")
DGRAY = HexColor("#333333")
MGRAY = HexColor("#666666")
LGRAY = HexColor("#B8C0CC")
GREEN = HexColor("#2D5A27")  # Meridian Press green
GOLD = HexColor("#D4AF37")

# ─── Professional Design Colors (light grey, minimal) ────────────────────────
BAR_COLOR = HexColor("#E8E8E8")      # Light grey for section bars
BAR_TEXT_COLOR = HexColor("#444444")  # Dark grey text on bars
HEADER_BG = HexColor("#F5F5F5")      # Very light grey for headers
ACCENT_LINE = HexColor("#CCCCCC")    # Subtle accent lines

# ─── KDP Spec Constants ──────────────────────────────────────────────────────
TRIM_W = 6.0 * inch
TRIM_H = 9.0 * inch
GUTTER = 0.5 * inch
OUTER = 0.3 * inch
TOP_MARGIN = 0.4 * inch
BOTTOM_MARGIN = 0.5 * inch  # Increased to clear KDP 0.25" minimum


def _writeline(c, x, y, w):
    """Draw a light gray writing line."""
    c.setStrokeColor(LGRAY)
    c.setLineWidth(0.5)
    c.line(x, y, x + w, y)


def _checkbox(c, x, y, s=8):
    """Draw a checkbox."""
    c.setStrokeColor(DGRAY)
    c.setLineWidth(0.7)
    c.rect(x, y, s, s, fill=0, stroke=1)


def _section_bar(c, x, y, w, title, h=13):
    """Draw a section header bar — light grey, professional."""
    c.setFillColor(BAR_COLOR)
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.setFillColor(BAR_TEXT_COLOR)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 5, y + 3.5, title.upper())


def _seal(c, cx, cy, r=30):
    """Draw official seal circle."""
    c.setStrokeColor(DGRAY)
    c.setLineWidth(1)
    c.setDash(4, 3)
    c.circle(cx, cy, r, fill=0, stroke=1)
    c.setDash()
    c.setFillColor(MGRAY)
    c.setFont("Helvetica", 6.5)
    c.drawCentredString(cx, cy - 3, "OFFICIAL")
    c.drawCentredString(cx, cy - 11, "SEAL")


def _thumbprint(c, x, y, s=64):
    """Draw thumbprint box."""
    c.setStrokeColor(DGRAY)
    c.setLineWidth(1)
    c.rect(x, y, s, s, fill=0, stroke=1)
    c.setFillColor(MGRAY)
    c.setFont("Helvetica", 6)
    c.drawCentredString(x + s / 2, y + s / 2 + 3, "RIGHT")
    c.drawCentredString(x + s / 2, y + s / 2 - 6, "THUMB")
    c.setFont("Helvetica", 5.5)
    c.drawCentredString(x + s / 2, y - 8, "Signer's Right Thumbprint")


def _margins_for_page(phys_page):
    """Return (left_margin, right_margin, outer_is_right)."""
    if phys_page % 2 == 1:  # recto
        return GUTTER, OUTER, True
    return OUTER, GUTTER, False


# Logo function removed — HyperAgent found broken rendering on B&W interior


def draw_page_number(c, W, phys_page):
    """Draw page number at bottom center."""
    c.setFillColor(LGRAY)
    c.setFont("Helvetica", 8)
    c.drawCentredString(W / 2, 18, f"{phys_page}")


def draw_cover_page(c, W, H):
    """Page 1: Cover/title page with metadata."""
    lm = 0.7 * inch
    uw = W - 2 * lm  # inset width for bars
    
    # Background
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    # Top rule — subtle grey (inset)
    c.setFillColor(ACCENT_LINE)
    c.rect(lm, H - 0.45 * inch, uw, 0.08 * inch, fill=1, stroke=0)
    
    # Meridian Press at top
    c.setFillColor(MGRAY)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(W / 2, H - 0.35 * inch, "MERIDIAN PRESS")
    
    # Title
    c.setFillColor(DGRAY)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(W / 2, H - 1.7 * inch, "NOTARY PUBLIC")
    c.drawCentredString(W / 2, H - 2.1 * inch, "RECORD JOURNAL")
    
    # Subtitle
    c.setFillColor(MGRAY)
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(W / 2, H - 2.5 * inch, "Official Log of Notarial Acts")
    
    # Seal
    _seal(c, W / 2, H - 3.5 * inch, r=48)
    
    # Fields
    y = H - 4.7 * inch
    c.setFillColor(DGRAY)
    c.setFont("Helvetica", 10)
    for lbl in ["Notary's Full Name:", "Commission Number:", "State / Jurisdiction:",
                "Office / Employer:", "Commission Expires:"]:
        c.drawString(lm, y, lbl)
        lw = c.stringWidth(lbl, "Helvetica", 10)
        _writeline(c, lm + lw + 6, y - 2, uw - lw - 6)
        y -= 0.42 * inch
    
    # Volume line
    c.drawString(lm, y, "Volume _______ of _______")
    c.drawRightString(W - lm, y, "Year: __________")
    
    # Disclaimer bar — subtle grey (inset)
    c.setFillColor(HEADER_BG)
    c.rect(lm, 0.6 * inch, uw, 0.75 * inch, fill=1, stroke=0)
    c.setFillColor(MGRAY)
    c.setFont("Helvetica-Oblique", 7.5)
    c.drawCentredString(W / 2, 1.02 * inch, "This journal is the exclusive property of the notary named above and is")
    c.drawCentredString(W / 2, 0.86 * inch, "maintained in compliance with applicable state law.")
    
    c.showPage()


def draw_instructions_page(c, W, H):
    """Page 2: Instructions with state-specific requirements and fee schedule."""
    lm = 0.65 * inch
    uw = W - 2 * lm
    
    # Background
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    # Header — subtle grey (inset)
    c.setFillColor(HEADER_BG)
    c.rect(lm, H - 0.9 * inch, uw, 0.5 * inch, fill=1, stroke=0)
    c.setFillColor(DGRAY)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(lm + 5, H - 0.72 * inch, "How to Use This Journal")
    
    # Main instructions
    items = [
        ("Sequential numbering.", "Entries are pre-numbered from 001 onward. Never skip, remove, or reorder a page. Sequential numbering deters tampering and satisfies most state record-keeping requirements."),
        ("One act per entry.", "Record a single notarial act on each numbered page. Complete every applicable field at the time of the act, in permanent ink."),
        ("Identification.", "Note the signer's ID type, number, and expiration date. Capture the signer's right thumbprint in the box on the outer edge when your state requires it."),
        ("Fees.", "Record the fee charged, or mark it Waived, to stay within your state's fee schedule."),
        ("When full.", "Store completed journals securely for your state's retention period (often 7 to 10 years). Begin a new volume and update the Volume ___ of ___ line on the cover."),
        ("Index.", "Use the summary index at the back of this journal to locate entries quickly."),
    ]
    
    y = H - 1.45 * inch
    for head, body in items:
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(DGRAY)
        c.drawString(lm, y, head)
        hw = c.stringWidth(head + "  ", "Helvetica-Bold", 9.5)
        c.setFont("Helvetica", 9.5)
        c.setFillColor(DGRAY)
        startx, avail, line, cy = lm + hw, uw - hw, "", y
        for w in body.split():
            t = (line + " " + w).strip()
            if c.stringWidth(t, "Helvetica", 9.5) <= avail:
                line = t
            else:
                c.drawString(startx, cy, line)
                cy -= 14
                startx = lm
                avail = uw
                line = w
        if line:
            c.drawString(startx, cy, line)
        y = cy - 21
    
    # ─── State-Specific Requirements Box ─────────────────────────────────────
    y -= 10
    c.setFillColor(HexColor("#F0F4F8"))
    c.rect(lm, y - 130, uw, 130, fill=1, stroke=0)
    c.setStrokeColor(STEEL)
    c.setLineWidth(1)
    c.rect(lm, y - 130, uw, 130, fill=0, stroke=1)
    
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(lm + 10, y - 15, "STATE-SPECIFIC REQUIREMENTS")
    c.setFont("Helvetica", 8)
    c.setFillColor(black)
    
    states = [
        ("California:", " Thumbprint required. Journal required by law. 4-year retention."),
        ("Florida:", " Thumbprint optional. No journal requirement (recommended)."),
        ("New York:", " No journal requirement. 10-year retention recommended."),
        ("Texas:", " No journal requirement. 5-year retention recommended."),
        ("Illinois:", " No journal requirement. 5-year retention recommended."),
        ("Pennsylvania:", " No journal requirement. 10-year retention recommended."),
    ]
    
    sy = y - 30
    for state, req in states:
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(lm + 15, sy, state)
        c.setFont("Helvetica", 7.5)
        c.drawString(lm + 15 + c.stringWidth(state, "Helvetica-Bold", 7.5) + 4, sy, req)
        sy -= 14
    
    # ─── Fee Schedule Reference ───────────────────────────────────────────────
    y = y - 150
    c.setFillColor(HexColor("#F0F4F8"))
    c.rect(lm, y - 110, uw, 110, fill=1, stroke=0)
    c.setStrokeColor(STEEL)
    c.setLineWidth(1)
    c.rect(lm, y - 110, uw, 110, fill=0, stroke=1)
    
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(lm + 10, y - 15, "TYPICAL FEE SCHEDULE (US)")
    c.setFont("Helvetica", 8)
    c.setFillColor(black)
    
    fees = [
        ("Acknowledgment:", "$5 - $15"),
        ("Oath / Affirmation:", "$5 - $10"),
        ("Jurat:", "$5 - $15"),
        ("Copy Certification:", "$5 - $10"),
        ("Signature Witnessing:", "$5 - $15"),
        ("Proof of Execution:", "$5 - $20"),
    ]
    
    fy = y - 30
    for fee_type, fee_range in fees:
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(lm + 15, fy, fee_type)
        c.setFont("Helvetica", 7.5)
        c.drawString(lm + 15 + c.stringWidth(fee_type, "Helvetica-Bold", 7.5) + 4, fy, fee_range)
        fy -= 14
    
    # Footer
    c.setFillColor(LGRAY)
    c.setFont("Helvetica", 6)
    c.drawCentredString(W / 2, 18, "2")
    
    c.showPage()


def draw_notary_entry(c, W, H, entry_no, total, phys_page):
    """Draw a single notary entry page."""
    lm, rm, outer_right = _margins_for_page(phys_page)
    top = TOP_MARGIN
    uw = W - lm - rm
    RH = 16  # row height
    
    # Header bar — subtle grey (inset from edges)
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
    
    # A — Date & Time (aligned layout)
    _section_bar(c, lm, y - 13, uw, "A — Date & Time")
    y -= 13 + 6
    c.setFillColor(DGRAY)
    c.setFont("Helvetica", 8.5)
    # Date row — aligned
    c.drawString(lm, y, "Date:")
    _writeline(c, lm + 45, y - 2, 130)
    c.drawString(lm + 190, y, "Time:")
    _writeline(c, lm + 220, y - 2, 60)
    _checkbox(c, lm + 290, y - 1)
    c.drawString(lm + 301, y, "AM")
    _checkbox(c, lm + 324, y - 1)
    c.drawString(lm + 335, y, "PM")
    y -= RH + 3
    
    # B — Type of Notarial Act (aligned checkboxes)
    _section_bar(c, lm, y - 13, uw, "B — Type of Notarial Act")
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
    
    # C — Document Information (aligned with consistent line start)
    _section_bar(c, lm, y - 13, uw, "C — Document Information")
    y -= 13 + 6
    for lbl in ["Document Type:", "Document Date / No. of Pages:", "Description / Title:"]:
        c.setFillColor(DGRAY)
        c.setFont("Helvetica", 8.5)
        c.drawString(lm, y, lbl)
        lw = c.stringWidth(lbl, "Helvetica", 8.5)
        _writeline(c, lm + lw + 6, y - 2, uw - lw - 8)
        y -= RH
    y -= 3
    
    # D — Signer Information (aligned with consistent line start)
    _section_bar(c, lm, y - 13, uw, "D — Signer Information")
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
    _section_bar(c, ex, e_top - 13, ew, "E — Witness (if applicable)")
    thumb = 72
    thumb_x = (lm + uw - thumb) if outer_right else lm
    _thumbprint(c, thumb_x, e_top - 15 - thumb, thumb)
    yw = e_top - 13 - 8
    for lbl in ["Witness Name:", "Signature:"]:
        c.setFillColor(black)
        c.setFont("Helvetica", 8.5)
        c.drawString(ex, yw, lbl)
        lw = c.stringWidth(lbl, "Helvetica", 8.5)
        _writeline(c, ex + lw + 4, yw - 2, ew - lw - 6)
        yw -= RH
    y = e_top - 98
    
    # G — Fees
    _section_bar(c, lm, y - 13, uw, "G — Fees")
    y -= 13 + 6
    c.setFillColor(black)
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
    _section_bar(c, lm, y - 13, uw, "H — Notary Certification & Signature")
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
        c.setFillColor(black)
        c.setFont("Helvetica", 8.5)
        c.drawString(sig_x, y, lbl)
        lw = c.stringWidth(lbl, "Helvetica", 8.5)
        _writeline(c, sig_x + lw + 4, y - 2, sig_w - lw - 6)
        y -= RH
    y -= 3
    
    # I — Remarks
    _section_bar(c, lm, y - 13, uw, "I — Remarks")
    y -= 13 + 8
    for _ in range(3):
        _writeline(c, lm, y - 2, uw)
        y -= RH
    
    # Footer page number
    draw_page_number(c, W, phys_page)
    
    c.showPage()


def draw_index_pages(c, W, H, total_entries, start_phys_page):
    """Draw index pages with "Document Type" column added."""
    per_page = 28
    entry = 1
    phys = start_phys_page
    
    while entry <= total_entries:
        lm, rm, _ = _margins_for_page(phys)
        uw = W - lm - rm
        
        # Header bar — subtle grey (inset)
        c.setFillColor(HEADER_BG)
        c.rect(lm, H - 0.85 * inch, uw, 0.45 * inch, fill=1, stroke=0)
        c.setFillColor(DGRAY)
        c.setFont("Helvetica-Bold", 13)
        c.drawCentredString(W / 2, H - 0.68 * inch, "JOURNAL INDEX / SUMMARY")
        
        # Column headers (now with Document Type column)
        cols = [
            lm,                    # No.
            lm + 0.45 * inch,     # Date
            lm + 1.25 * inch,     # Signer Name
            lm + 2.65 * inch,     # Document Type (NEW!)
            lm + 3.85 * inch,     # Act Type
            lm + 4.85 * inch,     # Fee
        ]
        hdrs = ["No.", "Date", "Signer Name", "Doc Type", "Act Type", "Fee"]
        
        y = H - 1.15 * inch
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(STEEL)
        for i, hd in enumerate(hdrs):
            c.drawString(cols[i] + 2, y, hd)
        y -= 4
        
        # Header line
        c.setStrokeColor(STEEL)
        c.setLineWidth(0.8)
        c.line(lm, y, lm + uw, y)
        y -= 15
        
        # Row height
        rh = (y - (TOP_MARGIN + 0.3) * inch) / per_page
        
        for _ in range(per_page):
            if entry > total_entries:
                break
            
            # Entry number
            c.setFillColor(black)
            c.setFont("Helvetica-Bold", 7.5)
            c.drawString(cols[0] + 2, y, f"{entry:03d}")
            
            # Row line
            c.setStrokeColor(LGRAY)
            c.setLineWidth(0.4)
            c.line(lm, y - 3, lm + uw, y - 3)
            
            # Column dividers
            c.setStrokeColor(HexColor("#E2E6EC"))
            c.setLineWidth(0.4)
            for i in range(1, len(cols)):
                c.line(cols[i], y - 3, cols[i], y + 10)
            
            entry += 1
            y -= rh
        
        # Footer page number
        draw_page_number(c, W, phys)
        
        c.showPage()
        phys += 1
    
    return phys


def draw_notes_page(c, W, H, phys_page):
    """Draw Notes page with ruled lines for writing."""
    lm, rm, _ = _margins_for_page(phys_page)
    uw = W - lm - rm
    
    # Header bar — subtle grey (inset)
    c.setFillColor(HEADER_BG)
    c.rect(lm, H - 0.8 * inch, uw, 0.4 * inch, fill=1, stroke=0)
    c.setFillColor(DGRAY)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(lm + 5, H - 0.65 * inch, "NOTES / ADDITIONAL RECORDS")
    
    # Ruled lines for writing (start below header, end above footer)
    y = H - 1.1 * inch
    footer_y = BOTTOM_MARGIN + 0.25 * inch  # clear the page number
    while y > footer_y:
        _writeline(c, lm, y, uw)
        y -= 0.32 * inch
    
    # Footer page number
    draw_page_number(c, W, phys_page)
    
    c.showPage()


def generate_improved_interior(output_path, entries=110, total_pages=120):
    """Generate improved interior with all fixes."""
    c = canvas.Canvas(output_path, pagesize=(TRIM_W, TRIM_H))
    
    # Set PDF metadata
    c.setTitle("Notary Public Record Journal")
    c.setAuthor("Meridian Press")
    c.setSubject("Official Log of Notarial Acts")
    c.setCreator("KDP Print Skill v2.1")
    c.setKeywords("notary journal, notarial acts, record keeping")
    
    # Page 1: Cover page with metadata
    draw_cover_page(c, TRIM_W, TRIM_H)
    
    # Page 2: Instructions with state-specific requirements and fee schedule
    draw_instructions_page(c, TRIM_W, TRIM_H)
    
    # Pages 3-112: 110 notary entries
    phys = 3
    for e in range(1, entries + 1):
        draw_notary_entry(c, TRIM_W, TRIM_H, e, entries, phys)
        phys += 1
    
    # Pages 113-116: Index with Document Type column
    phys = draw_index_pages(c, TRIM_W, TRIM_H, entries, phys)
    
    # Pages 117-120: Notes with ruled lines
    while phys <= total_pages:
        draw_notes_page(c, TRIM_W, TRIM_H, phys)
        phys += 1
    
    c.save()
    print(f"Generated: {output_path}")
    print(f"  6x9 | {entries} entries | {phys - 1} total pages")
    return output_path, phys - 1


def generate_master_pages(output_dir):
    """
    Generate master page pair (left + right) for design review.
    Like InDesign master pages — one verso (left), one recto (right).
    Left page: gutter on right, outer edge on left
    Right page: gutter on left, outer edge on right
    """
    os.makedirs(output_dir, exist_ok=True)
    
    left_pdf = os.path.join(output_dir, "master-left.pdf")
    right_pdf = os.path.join(output_dir, "master-right.pdf")
    
    # Left master page (verso — odd page, gutter on RIGHT)
    cl = canvas.Canvas(left_pdf, pagesize=(TRIM_W, TRIM_H))
    cl.setTitle("Master Left Page (Verso)")
    cl.setAuthor("Meridian Press")
    draw_notary_entry(cl, TRIM_W, TRIM_H, entry_no=1, total=110, phys_page=3)
    cl.save()
    
    # Right master page (recto — even page, gutter on LEFT)
    cr = canvas.Canvas(right_pdf, pagesize=(TRIM_W, TRIM_H))
    cr.setTitle("Master Right Page (Recto)")
    cr.setAuthor("Meridian Press")
    draw_notary_entry(cr, TRIM_W, TRIM_H, entry_no=2, total=110, phys_page=4)
    cr.save()
    
    print(f"Master pages generated:")
    print(f"  Left (verso):  {left_pdf}")
    print(f"  Right (recto): {right_pdf}")
    return left_pdf, right_pdf


def render_pdf_pages(pdf_path, output_dir, page_indices=None, prefix="page"):
    """
    Render PDF pages to PNGs for visual review.
    Requires PyMuPDF (fitz).
    """
    try:
        import fitz
    except ImportError:
        print("ERROR: PyMuPDF not installed. Run: pip install PyMuPDF")
        return []
    
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    
    if page_indices is None:
        page_indices = range(len(doc))
    
    rendered = []
    for i in page_indices:
        if i >= len(doc):
            break
        page = doc[i]
        # Render at 200 DPI for crisp preview
        mat = fitz.Matrix(200/72, 200/72)
        pix = page.get_pixmap(matrix=mat)
        out_path = os.path.join(output_dir, f"{prefix}-{i+1:03d}.png")
        pix.save(out_path)
        rendered.append(out_path)
        print(f"  Rendered: {out_path}")
    
    doc.close()
    return rendered


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Notary Interior Generator")
    parser.add_argument("--masters", action="store_true",
                        help="Generate master pages only (left + right)")
    parser.add_argument("--render", action="store_true",
                        help="Render master pages to PNG for review")
    parser.add_argument("--full", action="store_true",
                        help="Generate full 120-page interior")
    parser.add_argument("--entries", type=int, default=110,
                        help="Number of entries (default: 110)")
    parser.add_argument("--pages", type=int, default=120,
                        help="Total pages (default: 120)")
    args = parser.parse_args()
    
    base_dir = r"C:\Users\Admin\Projects\active\kdp-publishing-copilot\books\notary-log-book"
    
    if args.masters or args.render:
        # Generate master pages
        master_dir = os.path.join(base_dir, "master-pages")
        left_pdf, right_pdf = generate_master_pages(master_dir)
        
        if args.render:
            # Render to PNGs
            render_dir = os.path.join(master_dir, "renders")
            print("\nRendering master pages to PNG...")
            render_pdf_pages(left_pdf, render_dir, page_indices=[0], prefix="master-left")
            render_pdf_pages(right_pdf, render_dir, page_indices=[0], prefix="master-right")
            print(f"\nDone! Review renders in: {render_dir}")
    else:
        # Generate full interior
        output = os.path.join(base_dir, "interior_improved.pdf")
        generate_improved_interior(output, entries=args.entries, total_pages=args.pages)
