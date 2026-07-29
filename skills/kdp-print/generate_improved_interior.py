#!/usr/bin/env python3
"""
Improved Notary Public Record Journal - Interior Generator
Fixes all issues identified in INTERIOR_ANALYSIS.md

Layout is defined in entry_page.py (single source of truth).
This file handles cover, instructions, index, notes, and full generation.
"""

import os
import sys

from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white, Color

# Import from single source of truth
from entry_page import (
    TRIM_W, TRIM_H, GUTTER, OUTER, TOP_MARGIN, BOTTOM_MARGIN,
    FOOTER_BASELINE, FOOTER_GUARD,
    DGRAY, MGRAY, LGRAY, BAR_COLOR, BAR_TEXT_COLOR, HEADER_BG, ACCENT_LINE,
    _margins_for_page, _writeline, _checkbox, _section_bar, _thumbprint, _seal,
    draw_page_number, draw_entry_page
)

# ─── Legacy color aliases (used by cover/instructions pages) ──────────────────
NAVY = HexColor("#1B2A4A")
STEEL = HexColor("#3A5A8C")
GREEN = HexColor("#2D5A27")
GOLD = HexColor("#D4AF37")


def _writeline(c, x, y, w):
    """Draw a light gray writing line."""
    c.setStrokeColor(LGRAY)
    c.setLineWidth(0.5)
    c.line(x, y, x + w, y)


# Logo function removed — HyperAgent found broken rendering on B&W interior


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
    c.setCreator("KDP Print Skill v2.2")
    c.setKeywords("notary journal, notarial acts, record keeping")
    
    # Page 1: Cover page with metadata
    draw_cover_page(c, TRIM_W, TRIM_H)
    
    # Page 2: Instructions with state-specific requirements and fee schedule
    draw_instructions_page(c, TRIM_W, TRIM_H)
    
    # Pages 3-112: 110 notary entries (uses single source of truth)
    phys = 3
    for e in range(1, entries + 1):
        draw_entry_page(c, TRIM_W, TRIM_H, e, phys)
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


if __name__ == "__main__":
    output = r"C:\Users\Admin\Projects\active\kdp-publishing-copilot\books\notary-log-book\interior_improved.pdf"
    generate_improved_interior(output, entries=110, total_pages=120)
