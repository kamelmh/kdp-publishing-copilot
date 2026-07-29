#!/usr/bin/env python3
"""
Single source of truth for notary interior layout.
Imported by both master_page_generator.py and kdp_print.py.

Parity convention (publishing standard):
  - Odd pages = RECTO (right-hand) → gutter on LEFT
  - Even pages = VERSO (left-hand) → gutter on RIGHT
"""

from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black

# ─── Design Tokens ─────────────────────────────────────────────────────────────
# POD-safe grey palette (all tints ≥12% for reliable B&W reproduction)
BAR_COLOR = HexColor("#DCDCDC")        # ~14% grey — section bars
BAR_TEXT_COLOR = HexColor("#333333")   # Dark grey text on bars
HEADER_BG = HexColor("#C8C8C8")       # ~21% grey — header bar (darker than sections)
ACCENT_LINE = HexColor("#BBBBBB")     # ~29% grey — accent lines
DGRAY = HexColor("#333333")           # Primary text
MGRAY = HexColor("#666666")           # Secondary text
LGRAY = HexColor("#999999")           # Light accents (page numbers)

# Navy palette for front-matter elements (cover, instructions, index headers)
NAVY = HexColor("#1B2A4A")
STEEL = HexColor("#3A5A8C")

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
    
    Returns (left_margin_pt, right_margin_pt, outer_is_right).
    """
    return _margins_for_page_raw(phys_page, GUTTER, OUTER)


def _margins_for_page_raw(phys_page, gutter_pt, outer_pt):
    """
    Mirror margins with explicit gutter/outer values (in points).
    
    Returns (left_margin_pt, right_margin_pt, outer_is_right).
    """
    if phys_page % 2 == 1:  # Odd = RECTO (right-hand)
        return gutter_pt, outer_pt, True   # gutter LEFT, outer RIGHT
    else:  # Even = VERSO (left-hand)
        return outer_pt, gutter_pt, False  # outer LEFT, gutter RIGHT


def _writeline(c, x, y, w):
    """Draw a light gray writing line."""
    c.setStrokeColor(ACCENT_LINE)
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


def draw_entry_page(c, W, H, entry_no, phys_page, gutter_in=None, outer_in=None):
    """
    Draw a single notary entry page.
    
    This is the single source of truth for entry page layout.
    Both master generator and full interior generator call this function.
    
    Parameters:
        gutter_in: Optional override for gutter margin in inches (default: use GUTTER constant)
        outer_in: Optional override for outer margin in inches (default: use OUTER constant)
    """
    gutter_pt = (gutter_in * inch) if gutter_in is not None else GUTTER
    outer_pt = (outer_in * inch) if outer_in is not None else OUTER
    lm, rm, outer_right = _margins_for_page_raw(phys_page, gutter_pt, outer_pt)
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
    _section_bar(c, thumb_x, e_top - 13, thumb, "F — THUMB")
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


def draw_cover_page(c, W, H, meta=None):
    """Title page — no bleed, all elements inset ≥0.25" from trim."""
    lm = 0.7 * inch
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # Top rule (INSET — never edge-to-edge)
    c.setFillColor(NAVY)
    c.rect(lm, H - 0.45 * inch, W - 2 * lm, 0.12 * inch, fill=1, stroke=0)
    # Title
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(W / 2, H - 1.7 * inch, "NOTARY PUBLIC")
    c.drawCentredString(W / 2, H - 2.1 * inch, "RECORD JOURNAL")
    # Subtitle
    c.setFillColor(STEEL)
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(W / 2, H - 2.5 * inch, "Official Log of Notarial Acts")
    # Seal
    _seal(c, W / 2, H - 3.5 * inch, r=48)
    # Fields
    y = H - 4.7 * inch
    c.setFillColor(black)
    c.setFont("Helvetica", 10)
    for lbl in ["Notary's Full Name:", "Commission Number:", "State / Jurisdiction:",
                "Office / Employer:", "Commission Expires:"]:
        c.drawString(lm, y, lbl)
        lw = c.stringWidth(lbl, "Helvetica", 10)
        _writeline(c, lm + lw + 6, y - 2, W - lm - (lm + lw + 6))
        y -= 0.42 * inch
    # Volume line
    c.drawString(lm, y, "Volume _______ of _______")
    c.drawRightString(W - lm, y, "Year: __________")
    y -= 0.5 * inch
    # Disclaimer bar (INSET)
    c.setFillColor(NAVY)
    c.rect(lm, 0.6 * inch, W - 2 * lm, 0.75 * inch, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Oblique", 7.5)
    c.drawCentredString(W / 2, 1.02 * inch,
        "This journal is the exclusive property of the notary named above and is")
    c.drawCentredString(W / 2, 0.86 * inch,
        "maintained in compliance with applicable state law.")
    c.showPage()


def _para(c, x, y, width, head, body, lead=14, size=9.5):
    """Bold lead-in head + body text, word-wrapped within `width`. Returns next y."""
    c.setFont("Helvetica-Bold", size)
    c.setFillColor(NAVY)
    c.drawString(x, y, head)
    hw = c.stringWidth(head + "  ", "Helvetica-Bold", size)
    c.setFont("Helvetica", size)
    c.setFillColor(black)
    startx, avail, line, cy = x + hw, width - hw, "", y
    for w in body.split():
        t = (line + " " + w).strip()
        if c.stringWidth(t, "Helvetica", size) <= avail:
            line = t
        else:
            c.drawString(startx, cy, line)
            cy -= lead
            startx = x
            avail = width
            line = w
    if line:
        c.drawString(startx, cy, line)
    return cy - lead - 7


def draw_instructions_page(c, W, H):
    """How-to-use instructions with state references and fee schedule."""
    lm = 0.65 * inch
    uw = W - 2 * lm
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # Header bar (INSET)
    c.setFillColor(NAVY)
    c.rect(lm, H - 0.9 * inch, uw, 0.5 * inch, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(lm + 6, H - 0.72 * inch, "How to Use This Journal")
    # Instructions
    items = [
        ("Sequential numbering.",
         "Entries are pre-numbered from 001 onward. Never skip, remove, or reorder a page. "
         "Sequential numbering deters tampering and satisfies most state record-keeping requirements."),
        ("One act per entry.",
         "Record a single notarial act on each numbered page. Complete every applicable field at "
         "the time of the act, in permanent ink."),
        ("Identification.",
         "Note the signer's ID type, number, and expiration date. Capture the signer's right "
         "thumbprint in the box on the outer edge when your state requires it."),
        ("Fees.",
         "Record the fee charged, or mark it Waived, to stay within your state's fee schedule."),
        ("When full.",
         "Store completed journals securely for your state's retention period (often 7 to 10 years). "
         "Begin a new volume and update the Volume ___ of ___ line on the cover."),
        ("Index.",
         "Use the summary index at the back of this journal to locate entries quickly."),
    ]
    y = H - 1.45 * inch
    for head, body in items:
        y = _para(c, lm, y, uw, head, body)
    # Reference boxes anchored from FOOTER_GUARD
    ROW, HDR, PAD = 13, 18, 8
    states = [
        ("California:", "Thumbprint required. Journal required by law. 4-year retention."),
        ("Florida:", "Thumbprint optional. No journal requirement (recommended)."),
        ("New York:", "No journal requirement. 10-year retention recommended."),
        ("Texas:", "No journal requirement. 5-year retention recommended."),
        ("Illinois:", "No journal requirement. 5-year retention recommended."),
        ("Pennsylvania:", "No journal requirement. 10-year retention recommended."),
    ]
    fees = [
        ("Acknowledgment:", "$5 - $15"), ("Oath / Affirmation:", "$5 - $10"),
        ("Jurat:", "$5 - $15"), ("Copy Certification:", "$5 - $10"),
        ("Signature Witnessing:", "$5 - $15"), ("Proof of Execution:", "$5 - $20"),
    ]
    def _refbox(bottom, rows, title):
        h = HDR + len(rows) * ROW + PAD
        c.setFillColor(HexColor("#EDF2F8"))
        c.setStrokeColor(NAVY)
        c.setLineWidth(1)
        c.rect(lm, bottom, uw, h, fill=1, stroke=1)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(lm + 10, bottom + h - 14, title)
        ty = bottom + h - HDR - 12
        for label, val in rows:
            c.setFillColor(black)
            c.setFont("Helvetica-Bold", 7.5)
            c.drawString(lm + 18, ty, label)
            lw = c.stringWidth(label, "Helvetica-Bold", 7.5)
            c.setFont("Helvetica", 7.5)
            c.drawString(lm + 18 + lw + 5, ty, val)
            ty -= ROW
        return h
    fee_bottom = FOOTER_GUARD + 4
    fee_h = _refbox(fee_bottom, fees, "TYPICAL FEE SCHEDULE (US)")
    state_bottom = fee_bottom + fee_h + 14
    _refbox(state_bottom, states, "STATE-SPECIFIC REQUIREMENTS")
    # Footer
    c.setFillColor(LGRAY)
    c.setFont("Helvetica", 6)
    c.drawCentredString(W / 2, FOOTER_BASELINE, "2")
    c.showPage()


def draw_index_pages(c, W, H, total_entries, start_phys_page, gutter_in, outer_in, top_in=0.4):
    """Summary index pages (28 entries per page). Returns next physical page number."""
    per_page = 28
    entry = 1
    phys = start_phys_page
    while entry <= total_entries:
        lm, rm, _ = _margins_for_page_raw(phys, gutter_in * inch, outer_in * inch)
        uw = W - lm - rm
        # Header (INSET)
        c.setFillColor(NAVY)
        c.rect(lm, H - 0.85 * inch, uw, 0.45 * inch, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 13)
        c.drawCentredString(lm + uw / 2, H - 0.68 * inch, "JOURNAL INDEX / SUMMARY")
        # 6 columns: No. / Date / Signer Name / Doc Type / Act Type / Fee
        cols = [lm + x * inch for x in (0, 0.45, 1.30, 2.65, 3.65, 4.65)]
        hdrs = ["No.", "Date", "Signer Name", "Doc Type", "Act Type", "Fee"]
        y = H - 1.15 * inch
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(STEEL)
        for i, hd in enumerate(hdrs):
            c.drawString(cols[i] + 2, y, hd)
        y -= 4
        c.setStrokeColor(STEEL)
        c.setLineWidth(0.8)
        c.line(lm, y, lm + uw, y)
        y -= 15
        rh = (y - FOOTER_GUARD) / per_page
        for _ in range(per_page):
            if entry > total_entries:
                break
            c.setFillColor(black)
            c.setFont("Helvetica-Bold", 8)
            c.drawString(cols[0] + 2, y, f"{entry:03d}")
            c.setStrokeColor(LGRAY)
            c.setLineWidth(0.4)
            c.line(lm, y - 3, lm + uw, y - 3)
            for i in range(1, len(cols)):
                c.setStrokeColor(HexColor("#E2E6EC"))
                c.setLineWidth(0.4)
                c.line(cols[i], y - 3, cols[i], y + 10)
            entry += 1
            y -= rh
        c.setFillColor(LGRAY)
        c.setFont("Helvetica", 6)
        c.drawCentredString(W / 2, FOOTER_BASELINE, f"{phys}")
        c.showPage()
        phys += 1
    return phys


def draw_notes_page(c, W, H, phys_page, gutter_in, outer_in, top_in=0.4):
    """Notes page with lined writing area."""
    lm, rm, _ = _margins_for_page_raw(phys_page, gutter_in * inch, outer_in * inch)
    uw = W - lm - rm
    # Header (INSET)
    c.setFillColor(NAVY)
    c.rect(lm, H - 0.8 * inch, uw, 0.4 * inch, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(lm + 6, H - 0.65 * inch, "NOTES / ADDITIONAL RECORDS")
    # Lined area
    y = H - 1.1 * inch
    while y > (top_in + 0.3) * inch:
        _writeline(c, lm, y, uw)
        y -= 0.32 * inch
    # Footer
    c.setFillColor(LGRAY)
    c.setFont("Helvetica", 6)
    c.drawCentredString(W / 2, FOOTER_BASELINE, f"{phys_page}")
    c.showPage()
