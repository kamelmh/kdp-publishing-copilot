#!/usr/bin/env python3
"""
Single source of truth for notary entry page layout.
Imported by both master_page_generator.py and generate_improved_interior.py.

Parity convention (publishing standard):
  - Odd pages = RECTO (right-hand) → gutter on LEFT
  - Even pages = VERSO (left-hand) → gutter on RIGHT
"""

from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor

# ─── Design Tokens ─────────────────────────────────────────────────────────────
# POD-safe grey palette (all tints ≥12% for reliable B&W reproduction)
BAR_COLOR = HexColor("#DCDCDC")        # ~14% grey — section bars
BAR_TEXT_COLOR = HexColor("#333333")   # Dark grey text on bars
HEADER_BG = HexColor("#C8C8C8")       # ~21% grey — header bar (darker than sections)
ACCENT_LINE = HexColor("#BBBBBB")     # ~29% grey — accent lines
DGRAY = HexColor("#333333")           # Primary text
MGRAY = HexColor("#666666")           # Secondary text
LGRAY = HexColor("#999999")           # Light accents (page numbers)

# ─── KDP Spec Constants ────────────────────────────────────────────────────────
TRIM_W = 6.0 * inch
TRIM_H = 9.0 * inch
GUTTER = 0.5 * inch
OUTER = 0.3 * inch
TOP_MARGIN = 0.625 * inch
BOTTOM_MARGIN = 0.375 * inch
FOOTER_BASELINE = 21
FOOTER_GUARD = 36


def _margins_for_page(phys_page):
    """
    Mirror margins: gutter always on binding edge.
    
    Publishing convention:
      - Odd page number = RECTO (right-hand page) → gutter on LEFT
      - Even page number = VERSO (left-hand page) → gutter on RIGHT
    
    Returns (left_margin, right_margin, outer_is_right).
    """
    if phys_page % 2 == 1:  # Odd = RECTO (right-hand)
        return GUTTER, OUTER, True   # gutter LEFT, outer RIGHT
    else:  # Even = VERSO (left-hand)
        return OUTER, GUTTER, False  # outer LEFT, gutter RIGHT


def _writeline(c, x, y, w):
    """Draw a light gray writing line."""
    c.setStrokeColor(HexColor("#CCCCCC"))
    c.setLineWidth(0.4)
    c.line(x, y, x + w, y)


def _checkbox(c, x, y, s=8):
    """Draw a checkbox."""
    c.setStrokeColor(DGRAY)
    c.setLineWidth(0.5)
    c.rect(x, y, s, s, fill=0, stroke=1)


def _section_bar(c, x, y, w, title, h=13):
    """Draw a section header bar — light grey, professional."""
    c.setFillColor(BAR_COLOR)
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.setFillColor(BAR_TEXT_COLOR)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 4, y + 3, title)


def _thumbprint(c, x, y, s=72):
    """Draw thumbprint box."""
    c.setStrokeColor(DGRAY)
    c.setLineWidth(0.8)
    c.rect(x, y, s, s, fill=0, stroke=1)
    c.setFillColor(MGRAY)
    c.setFont("Helvetica", 7)
    c.drawCentredString(x + s/2, y + s/2 + 4, "RIGHT")
    c.drawCentredString(x + s/2, y + s/2 - 6, "THUMB")
    c.setFont("Helvetica", 6)
    c.drawCentredString(x + s/2, y - 10, "Signer's Right Thumbprint")


def _seal(c, cx, cy, r=28):
    """Draw official seal circle (dashed)."""
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


def draw_entry_page(c, W, H, entry_no, phys_page):
    """
    Draw a single notary entry page.
    
    This is the single source of truth for entry page layout.
    Both master generator and full interior generator call this function.
    """
    lm, rm, outer_right = _margins_for_page(phys_page)
    top = TOP_MARGIN
    uw = W - lm - rm
    RH = 16  # row height

    # ─── Header bar ────────────────────────────────────────────────────────────
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

    # ─── A — Date & Time ──────────────────────────────────────────────────────
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

    # ─── B — Type of Notarial Act ─────────────────────────────────────────────
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

    # ─── C — Document Information ──────────────────────────────────────────────
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

    # ─── D — Signer Information ────────────────────────────────────────────────
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

    # ─── E — Witness ───────────────────────────────────────────────────────────
    e_top = y
    ew = uw * 0.58
    ex = lm if outer_right else (lm + uw - ew)
    _section_bar(c, ex, e_top - 13, ew, "E — WITNESS (IF APPLICABLE)")
    yw = e_top - 13 - 8
    for lbl in ["Witness Name:", "Signature:"]:
        c.setFillColor(DGRAY)
        c.setFont("Helvetica", 8.5)
        c.drawString(ex, yw, lbl)
        lw = c.stringWidth(lbl, "Helvetica", 8.5)
        _writeline(c, ex + lw + 4, yw - 2, ew - lw - 6)
        yw -= RH

    # ─── F — Thumbprint (on outer edge) ────────────────────────────────────────
    thumb = 72
    thumb_x = (lm + uw - thumb) if outer_right else lm
    thumb_y = e_top - 15 - thumb
    _section_bar(c, thumb_x, e_top - 13, thumb, "F — THUMBPRINT")
    _thumbprint(c, thumb_x, thumb_y, thumb)
    y = e_top - 98

    # ─── G — Fees ──────────────────────────────────────────────────────────────
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

    # ─── H — Notary Certification & Signature ──────────────────────────────────
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

    # ─── I — Remarks ───────────────────────────────────────────────────────────
    _section_bar(c, lm, y - 13, uw, "I — REMARKS")
    y -= 13 + 8
    for _ in range(3):
        _writeline(c, lm, y - 2, uw)
        y -= RH

    # ─── Footer ────────────────────────────────────────────────────────────────
    draw_page_number(c, W, phys_page)
    c.showPage()
