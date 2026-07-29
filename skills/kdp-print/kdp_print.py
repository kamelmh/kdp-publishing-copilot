#!/usr/bin/env python3
"""
KDP Print Skill — Generate print-ready interiors and cover wraps for Amazon KDP.

Verified against KDP Print guidelines (2026):
    - Bleed: 0.125" on top, bottom, outer edges (COVER only; interiors need no bleed)
    - Gutter (inside) margin by page count: 0.375" (<=150), 0.5" (151-300),
      0.625" (301-500), 0.75" (501+)
    - Outside margin: minimum 0.25"
    - Spine width: page_count * paper_thickness + 0.06" allowance
        white 0.002252"/pg, cream 0.0025"/pg, color 0.002347"/pg
    - Resolution: 300 DPI; color space RGB (KDP converts to CMYK)
    - Paperback royalty: 60% of list - printing (Amazon; 50% if list below
      marketplace threshold since Jun-2025), 40% - printing (Expanded Distribution).
      Flat "40% royalty" is NOT correct for Amazon sales.
    - B&W print cost (US, >108pp): ~$1.00 fixed + $0.012/page

Usage:
    python kdp_print.py specs   --size 6x9 --pages 120 [--paper white] [--price 12.99]
    python kdp_print.py interior --type notary --size 6x9 --entries 110 --total-pages 120 --output interior.pdf
    python kdp_print.py cover   --front front.png --size 6x9 --pages 120 --output cover.pdf \
                                --title "..." --subtitle "..." --author "..." [--proof]
"""

import argparse
import math
import os
import sys

try:
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import HexColor, black, white, Color
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


# ─── KDP Spec Constants ───────────────────────────────────────────────────────
PAPER_THICKNESS = {"white": 0.002252, "cream": 0.0025, "color": 0.002347}
SPINE_ALLOWANCE = 0.06
BLEED = 0.125
MIN_OUTSIDE_MARGIN = 0.25
DPI = 300

TRIM_SIZES = {
    "5x8": (5.0, 8.0), "5.06x7.81": (5.06, 7.81), "5.25x8": (5.25, 8.0),
    "5.5x8.5": (5.5, 8.5), "6x9": (6.0, 9.0), "6.14x9.21": (6.14, 9.21),
    "6.69x9.61": (6.69, 9.61), "7x10": (7.0, 10.0), "7.44x9.69": (7.44, 9.69),
    "7.5x9.25": (7.5, 9.25), "8x10": (8.0, 10.0), "8.5x11": (8.5, 11.0),
    "4.75x6.75": (4.75, 6.75), "8.5x8.5": (8.5, 8.5), "8.25x8.25": (8.25, 8.25),
}


def get_gutter(page_count: int) -> float:
    """KDP required inside/gutter margin based on page count."""
    if page_count <= 150:
        return 0.375
    elif page_count <= 300:
        return 0.5
    elif page_count <= 500:
        return 0.625
    return 0.75


def printing_cost_bw_us(page_count: int) -> float:
    """Approx US B&W paperback printing cost. ~$1.00 fixed + $0.012/page (>108pp)."""
    return round(1.00 + 0.012 * page_count, 2)


def royalty(list_price: float, page_count: int, rate: float = 0.60) -> dict:
    """KDP paperback royalty = list*rate - printing cost.
    rate 0.60 = Amazon (>= price threshold), 0.40 = Expanded Distribution."""
    pc = printing_cost_bw_us(page_count)
    return {
        "list_price": list_price,
        "printing_cost": pc,
        "rate": rate,
        "royalty": round(list_price * rate - pc, 2),
    }


# ─── Spec Calculator ──────────────────────────────────────────────────────────
def calculate_specs(trim_size: str, page_count: int, paper: str = "white") -> dict:
    if trim_size not in TRIM_SIZES:
        raise ValueError(f"Unknown trim size: {trim_size}. Available: {list(TRIM_SIZES.keys())}")
    w, h = TRIM_SIZES[trim_size]
    thickness = PAPER_THICKNESS.get(paper, PAPER_THICKNESS["white"])
    spine = (page_count * thickness) + SPINE_ALLOWANCE
    cover_w = (w * 2) + spine + (BLEED * 2)
    cover_h = h + (BLEED * 2)
    return {
        "trim_size": trim_size, "trim_width": w, "trim_height": h,
        "page_count": page_count, "paper": paper,
        "gutter_margin": get_gutter(page_count), "outside_margin": MIN_OUTSIDE_MARGIN,
        "bleed": BLEED,
        "spine_width_in": round(spine, 4),
        "spine_width_px": round(spine * DPI),
        "cover_width_in": round(cover_w, 4), "cover_height_in": round(cover_h, 4),
        "cover_width_px": round(cover_w * DPI), "cover_height_px": round(cover_h * DPI),
        "interior_width_px": round(w * DPI), "interior_height_px": round(h * DPI),
    }


# ─── Drawing helpers (interior) ───────────────────────────────────────────────
NAVY = HexColor("#1B2A4A")
STEEL = HexColor("#3A5A8C")
DGRAY = HexColor("#333333")
MGRAY = HexColor("#666666")
LGRAY = HexColor("#B8C0CC")


def _writeline(c, x, y, w):
    c.setStrokeColor(LGRAY); c.setLineWidth(0.5)
    c.line(x, y, x + w, y)


def _checkbox(c, x, y, s=8):
    c.setStrokeColor(DGRAY); c.setLineWidth(0.7)
    c.rect(x, y, s, s, fill=0, stroke=1)


def _section_bar(c, x, y, w, title, h=13):
    c.setFillColor(STEEL)
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 5, y + 3.5, title.upper())


def _seal(c, cx, cy, r=30):
    c.setStrokeColor(DGRAY); c.setLineWidth(1); c.setDash(4, 3)
    c.circle(cx, cy, r, fill=0, stroke=1)
    c.setDash()
    c.setFillColor(MGRAY); c.setFont("Helvetica", 6.5)
    c.drawCentredString(cx, cy - 3, "OFFICIAL")
    c.drawCentredString(cx, cy - 11, "SEAL")


def _thumbprint(c, x, y, s=64):
    c.setStrokeColor(DGRAY); c.setLineWidth(1)
    c.rect(x, y, s, s, fill=0, stroke=1)
    c.setFillColor(MGRAY); c.setFont("Helvetica", 6)
    c.drawCentredString(x + s / 2, y + s / 2 + 3, "RIGHT")
    c.drawCentredString(x + s / 2, y + s / 2 - 6, "THUMB")
    c.setFont("Helvetica", 5.5)
    c.drawCentredString(x + s / 2, y - 8, "Signer's Right Thumbprint")


def _margins_for_page(phys_page: int, gutter_in: float, outer_in: float):
    """Return (left_margin_pt, right_margin_pt, outer_is_right).
    Odd physical page = recto (binding on left → gutter left)."""
    g, o = gutter_in * inch, outer_in * inch
    if phys_page % 2 == 1:      # recto / right-hand page
        return g, o, True       # outer edge is on the right
    return o, g, False          # verso / left-hand page, outer edge on left


# ─── Notary entry page ────────────────────────────────────────────────────────
def draw_notary_entry(c, W, H, entry_no, total, phys_page, gutter_in, outer_in,
                      top_in=0.4, bottom_in=0.4):
    lm, rm, outer_right = _margins_for_page(phys_page, gutter_in, outer_in)
    top = top_in * inch
    uw = W - lm - rm
    RH = 16  # row height

    # Header bar
    hb_h = 24
    y = H - top - hb_h
    c.setFillColor(NAVY); c.rect(lm, y, uw, hb_h, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 10)
    c.drawString(lm + 6, y + 8, "NOTARIAL ACT RECORD")
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(lm + uw - 6, y + 8, f"Entry No. {entry_no:03d}")
    y -= 12

    # A — Date & Time
    _section_bar(c, lm, y - 13, uw, "A — Date & Time"); y -= 13 + 6
    c.setFillColor(black); c.setFont("Helvetica", 8.5)
    c.drawString(lm, y, "Date:"); _writeline(c, lm + 30, y - 2, 120)
    c.drawString(lm + 165, y, "Time:"); _writeline(c, lm + 195, y - 2, 55)
    _checkbox(c, lm + 258, y - 1); c.drawString(lm + 269, y, "AM")
    _checkbox(c, lm + 292, y - 1); c.drawString(lm + 303, y, "PM")
    y -= RH + 3

    # B — Type of Notarial Act
    _section_bar(c, lm, y - 13, uw, "B — Type of Notarial Act"); y -= 13 + 6
    c.setFillColor(black); c.setFont("Helvetica", 8)
    row1 = ["Acknowledgment", "Oath / Affirmation", "Copy Certification"]
    cx = lm
    for a in row1:
        _checkbox(c, cx, y - 1); c.drawString(cx + 11, y, a)
        cx += 11 + c.stringWidth(a, "Helvetica", 8) + 16
    y -= RH
    row2 = ["Signature Witnessing", "Jurat"]
    cx = lm
    for a in row2:
        _checkbox(c, cx, y - 1); c.drawString(cx + 11, y, a)
        cx += 11 + c.stringWidth(a, "Helvetica", 8) + 16
    _checkbox(c, cx, y - 1); c.drawString(cx + 11, y, "Other:")
    _writeline(c, cx + 11 + c.stringWidth("Other:", "Helvetica", 8) + 4, y - 2, lm + uw - (cx + 55))
    y -= RH + 3

    # C — Document Information
    _section_bar(c, lm, y - 13, uw, "C — Document Information"); y -= 13 + 6
    for lbl in ["Document Type:", "Document Date / No. of Pages:", "Description / Title:"]:
        c.setFillColor(black); c.setFont("Helvetica", 8.5)
        c.drawString(lm, y, lbl)
        lw = c.stringWidth(lbl, "Helvetica", 8.5)
        _writeline(c, lm + lw + 4, y - 2, uw - lw - 6); y -= RH
    y -= 3

    # D — Signer Information
    _section_bar(c, lm, y - 13, uw, "D — Signer Information"); y -= 13 + 6
    for lbl in ["Full Name:", "Address:", "ID Type / Number / Exp.:", "Signer's Signature:"]:
        c.setFillColor(black); c.setFont("Helvetica", 8.5)
        c.drawString(lm, y, lbl)
        lw = c.stringWidth(lbl, "Helvetica", 8.5)
        _writeline(c, lm + lw + 4, y - 2, uw - lw - 6); y -= RH
    y -= 3

    # E — Witness (inner side)  +  F — Thumbprint (outer edge), fixed-height band
    e_top = y
    ew = uw * 0.58
    ex = lm if outer_right else (lm + uw - ew)      # witness block on inner side
    _section_bar(c, ex, e_top - 13, ew, "E — Witness (if applicable)")
    thumb = 72                                       # KDP min 1" (72pt)
    thumb_x = (lm + uw - thumb) if outer_right else lm
    _thumbprint(c, thumb_x, e_top - 15 - thumb, thumb)
    yw = e_top - 13 - 8
    for lbl in ["Witness Name:", "Signature:"]:
        c.setFillColor(black); c.setFont("Helvetica", 8.5)
        c.drawString(ex, yw, lbl)
        lw = c.stringWidth(lbl, "Helvetica", 8.5)
        _writeline(c, ex + lw + 4, yw - 2, ew - lw - 6); yw -= RH
    y = e_top - 98                                   # clear the 72pt thumbprint + label

    # G — Fees
    _section_bar(c, lm, y - 13, uw, "G — Fees"); y -= 13 + 6
    c.setFillColor(black); c.setFont("Helvetica", 8.5)
    c.drawString(lm, y, "Fee Charged: $"); _writeline(c, lm + 78, y - 2, 80)
    cx = lm + 175
    for p in ["Cash", "Check", "Elec.", "Waived"]:
        _checkbox(c, cx, y - 1); c.drawString(cx + 11, y, p)
        cx += 11 + c.stringWidth(p, "Helvetica", 8.5) + 12
    y -= RH + 3

    # H — Notary Certification & Signature  (+ seal on outer side)
    _section_bar(c, lm, y - 13, uw, "H — Notary Certification & Signature"); y -= 13 + 6
    c.setFillColor(MGRAY); c.setFont("Helvetica-Oblique", 7)
    c.drawString(lm, y, "I certify that the signer personally appeared before me on the date stated above.")
    y -= 14
    seal_cx = (lm + uw - 34) if outer_right else (lm + 34)
    _seal(c, seal_cx, y - 22, r=28)
    sig_w = uw - 76  # leave room for seal
    sig_x = lm if outer_right else (lm + 76)
    for lbl in ["Notary Name:", "Commission # / Exp.:", "Notary Signature:"]:
        c.setFillColor(black); c.setFont("Helvetica", 8.5)
        c.drawString(sig_x, y, lbl)
        lw = c.stringWidth(lbl, "Helvetica", 8.5)
        _writeline(c, sig_x + lw + 4, y - 2, sig_w - lw - 6); y -= RH
    y -= 3

    # I — Remarks
    _section_bar(c, lm, y - 13, uw, "I — Remarks"); y -= 13 + 8
    for _ in range(3):
        _writeline(c, lm, y - 2, uw); y -= RH

    # footer page number (kept ~0.25" off the trim edge)
    c.setFillColor(LGRAY); c.setFont("Helvetica", 6)
    c.drawCentredString(W / 2, 18, f"{phys_page}")
    c.showPage()


def draw_cover_page(c, W, H, meta):
    lm = 0.7 * inch
    c.setFillColor(white); c.rect(0, 0, W, H, fill=1, stroke=0)
    # top rule
    c.setFillColor(NAVY); c.rect(0, H - 0.45 * inch, W, 0.12 * inch, fill=1, stroke=0)
    c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(W / 2, H - 1.7 * inch, "NOTARY PUBLIC")
    c.drawCentredString(W / 2, H - 2.1 * inch, "RECORD JOURNAL")
    c.setFillColor(STEEL); c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(W / 2, H - 2.5 * inch, "Official Log of Notarial Acts")
    # seal
    _seal(c, W / 2, H - 3.5 * inch, r=48)
    # fields
    y = H - 4.7 * inch
    c.setFillColor(black); c.setFont("Helvetica", 10)
    for lbl in ["Notary's Full Name:", "Commission Number:", "State / Jurisdiction:",
                "Office / Employer:", "Commission Expires:"]:
        c.drawString(lm, y, lbl)
        lw = c.stringWidth(lbl, "Helvetica", 10)
        _writeline(c, lm + lw + 6, y - 2, W - lm - (lm + lw + 6)); y -= 0.42 * inch
    # volume line
    c.drawString(lm, y, "Volume _______ of _______")
    c.drawRightString(W - lm, y, "Year: __________"); y -= 0.5 * inch
    # disclaimer bar
    c.setFillColor(NAVY); c.rect(0, 0.6 * inch, W, 0.75 * inch, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Helvetica-Oblique", 7.5)
    c.drawCentredString(W / 2, 1.02 * inch, "This journal is the exclusive property of the notary named above and is")
    c.drawCentredString(W / 2, 0.86 * inch, "maintained in compliance with applicable state law.")
    c.showPage()


def _para(c, x, y, width, head, body, lead=14, size=9.5):
    """Bold lead-in head + body text, word-wrapped within `width`. Returns next y."""
    c.setFont("Helvetica-Bold", size); c.setFillColor(NAVY)
    c.drawString(x, y, head)
    hw = c.stringWidth(head + "  ", "Helvetica-Bold", size)
    c.setFont("Helvetica", size); c.setFillColor(black)
    startx, avail, line, cy = x + hw, width - hw, "", y
    for w in body.split():
        t = (line + " " + w).strip()
        if c.stringWidth(t, "Helvetica", size) <= avail:
            line = t
        else:
            c.drawString(startx, cy, line)
            cy -= lead; startx = x; avail = width; line = w
    if line:
        c.drawString(startx, cy, line)
    return cy - lead - 7


def draw_instructions_page(c, W, H):
    lm = 0.65 * inch
    uw = W - 2 * lm
    c.setFillColor(white); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(NAVY); c.rect(0, H - 0.9 * inch, W, 0.5 * inch, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 14)
    c.drawString(lm, H - 0.72 * inch, "How to Use This Journal")
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
        y = _para(c, lm, y, uw, head, body)
    c.setFillColor(LGRAY); c.setFont("Helvetica", 6)
    c.drawCentredString(W / 2, 18, "2")
    c.showPage()


def draw_index_pages(c, W, H, total_entries, start_phys_page, gutter_in, outer_in, top_in=0.4):
    per_page = 28
    entry = 1
    phys = start_phys_page
    while entry <= total_entries:
        lm, rm, _ = _margins_for_page(phys, gutter_in, outer_in)
        uw = W - lm - rm
        c.setFillColor(NAVY); c.rect(0, H - 0.85 * inch, W, 0.45 * inch, fill=1, stroke=0)
        c.setFillColor(white); c.setFont("Helvetica-Bold", 13)
        c.drawCentredString(W / 2, H - 0.68 * inch, "JOURNAL INDEX / SUMMARY")
        cols = [lm, lm + 0.55 * inch, lm + 1.5 * inch, lm + 3.0 * inch, lm + 4.1 * inch]
        hdrs = ["No.", "Date", "Signer Name", "Act Type", "Fee"]
        y = H - 1.15 * inch
        c.setFont("Helvetica-Bold", 8); c.setFillColor(STEEL)
        for i, hd in enumerate(hdrs):
            c.drawString(cols[i] + 2, y, hd)
        y -= 4
        c.setStrokeColor(STEEL); c.setLineWidth(0.8); c.line(lm, y, lm + uw, y); y -= 15
        rh = (y - (top_in * inch)) / per_page
        for _ in range(per_page):
            if entry > total_entries:
                break
            c.setFillColor(black); c.setFont("Helvetica-Bold", 8)
            c.drawString(cols[0] + 2, y, f"{entry:03d}")
            c.setStrokeColor(LGRAY); c.setLineWidth(0.4)
            c.line(lm, y - 3, lm + uw, y - 3)
            for i in range(1, len(cols)):
                c.setStrokeColor(HexColor("#E2E6EC")); c.setLineWidth(0.4)
                c.line(cols[i], y - 3, cols[i], y + 10)
            entry += 1; y -= rh
        c.setFillColor(LGRAY); c.setFont("Helvetica", 6)
        c.drawCentredString(W / 2, top_in * inch * 0.5, f"{phys}")
        c.showPage(); phys += 1
    return phys


def draw_notes_page(c, W, H, phys_page, gutter_in, outer_in, top_in=0.4):
    lm, rm, _ = _margins_for_page(phys_page, gutter_in, outer_in)
    uw = W - lm - rm
    c.setFillColor(NAVY); c.rect(0, H - 0.8 * inch, W, 0.4 * inch, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 12)
    c.drawString(lm, H - 0.65 * inch, "NOTES / ADDITIONAL RECORDS")
    y = H - 1.1 * inch
    while y > (top_in + 0.3) * inch:
        _writeline(c, lm, y, uw); y -= 0.32 * inch
    c.setFillColor(LGRAY); c.setFont("Helvetica", 6)
    c.drawCentredString(W / 2, top_in * inch * 0.5, f"{phys_page}")
    c.showPage()


def generate_notary_interior(output_path, trim_size="6x9", entries=110, total_pages=None):
    if not HAS_REPORTLAB:
        sys.exit("ERROR: reportlab not installed. Run: pip install reportlab")
    specs = calculate_specs(trim_size, total_pages or (entries + 6))
    W, H = specs["trim_width"] * inch, specs["trim_height"] * inch
    gutter = get_gutter(total_pages or (entries + 6))
    # gentle bump for comfort (still >= KDP minimum)
    gutter = max(gutter, 0.5)
    outer = 0.3
    c = canvas.Canvas(output_path, pagesize=(W, H))
    draw_cover_page(c, W, H, {})          # page 1
    draw_instructions_page(c, W, H)       # page 2
    phys = 3
    for e in range(1, entries + 1):
        draw_notary_entry(c, W, H, e, entries, phys, gutter, outer)
        phys += 1
    phys = draw_index_pages(c, W, H, entries, phys, gutter, outer)
    if total_pages:
        while (phys - 1) < total_pages:
            draw_notes_page(c, W, H, phys, gutter, outer); phys += 1
    c.save()
    final = phys - 1
    print(f"Generated: {output_path}")
    print(f"  {trim_size} | {entries} entries | {final} total pages")
    return output_path, final


def generate_lined_interior(output_path, trim_size="6x9", page_count=120, line_type="ruled"):
    if not HAS_REPORTLAB:
        sys.exit("ERROR: reportlab not installed.")
    specs = calculate_specs(trim_size, page_count)
    W, H = specs["trim_width"] * inch, specs["trim_height"] * inch
    gutter = max(get_gutter(page_count), 0.5); outer = 0.3
    top = bottom = 0.5 * inch
    c = canvas.Canvas(output_path, pagesize=(W, H))
    for p in range(1, page_count + 1):
        lm, rm, _ = _margins_for_page(p, gutter, outer)
        uw = W - lm - rm
        if line_type == "grid":
            step = 0.2 * inch
            c.setStrokeColor(LGRAY); c.setLineWidth(0.3)
            x = lm
            while x <= lm + uw:
                c.line(x, bottom, x, H - top); x += step
            yy = bottom
            while yy <= H - top:
                c.line(lm, yy, lm + uw, yy); yy += step
        elif line_type != "blank":
            yy = H - top
            while yy > bottom:
                _writeline(c, lm, yy, uw); yy -= 0.3 * inch
        c.setFillColor(LGRAY); c.setFont("Helvetica", 7)
        c.drawCentredString(W / 2, bottom * 0.5, str(p))
        c.showPage()
    c.save()
    print(f"Generated: {output_path} ({page_count} pages, {trim_size}, {line_type})")
    return output_path, page_count


# ─── Cover wrap (reportlab, vector text over raster art) ──────────────────────
def _register_cover_fonts():
    """Try to register elegant TTFs; fall back to built-in Times/Helvetica."""
    title_font, body_font = "Times-Bold", "Helvetica"
    fonts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "fonts")
    try:
        reg = os.path.join(fonts_dir, "LibreBaskerville-Regular.ttf")
        bold = os.path.join(fonts_dir, "LibreBaskerville-Bold.ttf")
        if os.path.exists(bold):
            pdfmetrics.registerFont(TTFont("Baskerville-Bold", bold))
            title_font = "Baskerville-Bold"
        if os.path.exists(reg):
            pdfmetrics.registerFont(TTFont("Baskerville", reg))
    except Exception as e:
        print(f"  (font fallback: {e})")
    return title_font, body_font


def build_cover_wrap(front_path, output_path, trim_size="6x9", page_count=120,
                     paper="white", title="", subtitle="", author="",
                     spine_text="", back_bullets=None, bg_hex="#1B2A4A",
                     accent_hex="#D4AF37", proof=False,
                     emblem=None, emblem_scale=0.34, emblem_y=0.42, text_hex="#FFFFFF"):
    if not HAS_REPORTLAB:
        sys.exit("ERROR: reportlab not installed.")
    s = calculate_specs(trim_size, page_count, paper)
    CW, CH = s["cover_width_in"] * inch, s["cover_height_in"] * inch
    bleed = BLEED * inch
    tw, th = s["trim_width"] * inch, s["trim_height"] * inch
    spine = s["spine_width_in"] * inch
    title_font, body_font = _register_cover_fonts()
    bg, accent, text = HexColor(bg_hex), HexColor(accent_hex), HexColor(text_hex)

    c = canvas.Canvas(output_path, pagesize=(CW, CH))
    # full background (fills bleed)
    c.setFillColor(bg); c.rect(0, 0, CW, CH, fill=1, stroke=0)

    back_x0 = 0
    spine_x0 = bleed + tw
    front_x0 = bleed + tw + spine

    # ---- FRONT art (right panel, extends into outer/top/bottom bleed) ----
    if front_path and os.path.exists(front_path):
        c.drawImage(ImageReader(front_path), front_x0, 0, width=tw + bleed, height=CH,
                    preserveAspectRatio=False, mask=None)
    # smooth gradient scrims (no hard seam) so text stays legible over any art
    def _grad_scrim(x, y0, w, h, max_a, darkest_top):
        n = 80
        bh = h / n
        c.setFillColorRGB(0.04, 0.07, 0.13)
        for i in range(n):
            t = i / (n - 1)
            c.setFillAlpha(max_a * (t if darkest_top else (1 - t)))
            c.rect(x, y0 + i * bh, w, bh + 1, fill=1, stroke=0)
        c.setFillAlpha(1)
    _grad_scrim(front_x0, CH - 3.2 * inch, tw + bleed, 3.2 * inch, 0.42, True)   # top → title
    _grad_scrim(front_x0, 0, tw + bleed, 1.7 * inch, 0.60, False)                # bottom → author

    # calibrated emblem overlay (transparent PNG from the logo-design skill)
    if emblem and os.path.exists(emblem):
        ew = emblem_scale * tw
        ecx = front_x0 + (tw + bleed) / 2
        ecy = CH * emblem_y
        c.drawImage(ImageReader(emblem), ecx - ew / 2, ecy - ew / 2,
                    width=ew, height=ew, mask="auto")

    # front safe area inset 0.5" from trim
    fx = front_x0 + 0.5 * inch
    fsafe_w = tw - 0.9 * inch
    # title
    c.setFillColor(text); c.setFont(title_font, 30)
    _wrap_center(c, "NOTARY PUBLIC", front_x0 + (tw + bleed) / 2, CH - 1.15 * inch, title_font, 30)
    _wrap_center(c, "RECORD JOURNAL", front_x0 + (tw + bleed) / 2, CH - 1.7 * inch, title_font, 30)
    # accent rule
    c.setStrokeColor(accent); c.setLineWidth(2)
    c.line(fx + 0.4 * inch, CH - 1.95 * inch, front_x0 + tw + bleed - 0.9 * inch, CH - 1.95 * inch)
    c.setFillColor(accent); c.setFont(body_font + "-Oblique" if body_font == "Helvetica" else body_font, 12)
    c.drawCentredString(front_x0 + (tw + bleed) / 2, CH - 2.25 * inch, subtitle)
    # author at bottom
    c.setFillColor(text); c.setFont(body_font, 13)
    c.drawCentredString(front_x0 + (tw + bleed) / 2, 0.85 * inch, author)
    c.setFillColor(accent); c.setFont(body_font, 9)
    c.drawCentredString(front_x0 + (tw + bleed) / 2, 0.6 * inch, "100+ PRE-NUMBERED ENTRIES  ·  6\" × 9\"")

    # ---- SPINE ----
    c.setFillColor(bg); c.rect(spine_x0, 0, spine, CH, fill=1, stroke=0)
    if spine >= 0.28 * inch and spine_text:
        c.saveState()
        c.translate(spine_x0 + spine / 2, CH / 2)
        c.rotate(90)
        c.setFillColor(text); c.setFont(title_font, 10)
        c.drawCentredString(0, -3, spine_text)
        c.restoreState()

    # ---- BACK ----
    bx = 0.6 * inch
    c.setFillColor(text); c.setFont(title_font, 15)
    c.drawString(bx, CH - 1.15 * inch, "Keep a compliant, court-ready")
    c.drawString(bx, CH - 1.45 * inch, "record of every notarial act.")
    c.setFont(body_font, 9.5); c.setFillColor(HexColor("#D8DEE9"))
    bullets = back_bullets or []
    yy = CH - 1.95 * inch
    for b in bullets:
        c.setFillColor(accent); c.drawString(bx, yy, "•")
        c.setFillColor(HexColor("#D8DEE9"))
        for line in _wrap_text(b, body_font, 9.5, tw - 1.5 * inch, c):
            c.drawString(bx + 12, yy, line); yy -= 13
        yy -= 4
    # barcode placeholder (KDP adds real barcode)
    bc_w, bc_h = 2.0 * inch, 1.2 * inch
    bc_x, bc_y = spine_x0 - 0.4 * inch - bc_w, 0.55 * inch
    c.setFillColor(white); c.rect(bc_x, bc_y, bc_w, bc_h, fill=1, stroke=0)
    c.setFillColor(MGRAY); c.setFont(body_font, 6.5)
    c.drawCentredString(bc_x + bc_w / 2, bc_y + bc_h / 2, "Barcode area — KDP adds automatically")
    c.setFillColor(HexColor("#98A2B3")); c.setFont(body_font, 7.5)
    c.drawString(bx, 0.55 * inch, "Independently published")

    # ---- optional proof guides (magenta) — NEVER in the upload file ----
    if proof:
        c.setStrokeColor(HexColor("#FF00AA")); c.setLineWidth(0.5); c.setDash(3, 3)
        for gx in [bleed, spine_x0, front_x0, front_x0 + tw]:
            c.line(gx, 0, gx, CH)
        c.line(0, bleed, CW, bleed); c.line(0, CH - bleed, CW, CH - bleed)
        c.setDash()

    c.save()
    tag = " (PROOF w/ guides)" if proof else ""
    print(f"Generated cover wrap: {output_path}{tag}")
    print(f"  {s['cover_width_in']}\" x {s['cover_height_in']}\"  ({s['cover_width_px']}x{s['cover_height_px']}px @300DPI)")
    print(f"  spine {s['spine_width_in']}\" ({s['spine_width_px']}px)")
    return output_path


def _wrap_center(c, text, cx, y, font, size):
    c.setFont(font, size); c.drawCentredString(cx, y, text)


def _wrap_text(text, font, size, max_w, c):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if c.stringWidth(t, font, size) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ─── CLI ──────────────────────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(description="KDP Print Skill")
    sub = p.add_subparsers(dest="command")

    sp = sub.add_parser("specs")
    sp.add_argument("--size", required=True); sp.add_argument("--pages", type=int, required=True)
    sp.add_argument("--paper", default="white", choices=["white", "cream", "color"])
    sp.add_argument("--price", type=float, default=None)

    ip = sub.add_parser("interior")
    ip.add_argument("--type", required=True, choices=["notary", "lined", "grid", "blank"])
    ip.add_argument("--size", default="6x9"); ip.add_argument("--entries", type=int, default=110)
    ip.add_argument("--pages", type=int, default=120); ip.add_argument("--total-pages", type=int, default=None)
    ip.add_argument("--output", required=True)

    cp = sub.add_parser("cover")
    cp.add_argument("--front"); cp.add_argument("--size", default="6x9")
    cp.add_argument("--pages", type=int, default=120)
    cp.add_argument("--paper", default="white", choices=["white", "cream", "color"])
    cp.add_argument("--title", default=""); cp.add_argument("--subtitle", default="")
    cp.add_argument("--author", default=""); cp.add_argument("--spine-text", default="")
    cp.add_argument("--bg", default="#1B2A4A"); cp.add_argument("--accent", default="#D4AF37")
    cp.add_argument("--text", default="#FFFFFF", help="title/author/spine/back-headline text color")
    cp.add_argument("--emblem", default=None, help="transparent emblem PNG to overlay on the front")
    cp.add_argument("--emblem-scale", type=float, default=0.34, help="emblem width as fraction of trim width")
    cp.add_argument("--emblem-y", type=float, default=0.42, help="emblem center height as fraction of cover height")
    cp.add_argument("--output", required=True); cp.add_argument("--proof", action="store_true")

    a = p.parse_args()
    if a.command == "specs":
        s = calculate_specs(a.size, a.pages, a.paper)
        print("=" * 52)
        print(f"KDP SPECS  {a.size} | {a.pages}pp | {a.paper}")
        print("=" * 52)
        for k, v in s.items():
            print(f"  {k:20s}: {v}")
        if a.price:
            print("-" * 52)
            amz = royalty(a.price, a.pages, 0.60)
            ed = royalty(a.price, a.pages, 0.40)
            print(f"  printing cost       : ${amz['printing_cost']}")
            print(f"  royalty @60% Amazon : ${amz['royalty']}")
            print(f"  royalty @40% Exp.Dist: ${ed['royalty']}")
    elif a.command == "interior":
        if a.type == "notary":
            generate_notary_interior(a.output, a.size, a.entries, a.total_pages or a.pages)
        else:
            generate_lined_interior(a.output, a.size, a.pages, a.type)
    elif a.command == "cover":
        bullets = [
            "100+ pre-numbered entry pages — sequential numbering deters tampering.",
            "One complete notarial act per page: date, act type, signer ID, fee, signature.",
            "Right-thumbprint box and official-seal area on every entry.",
            "Summary index at the back for fast lookups.",
            "Portable 6 x 9 inch format for the desk, briefcase, or mobile signings.",
        ]
        build_cover_wrap(a.front, a.output, a.size, a.pages, a.paper, a.title, a.subtitle,
                         a.author, a.spine_text, bullets, a.bg, a.accent, a.proof,
                         a.emblem, a.emblem_scale, a.emblem_y, a.text)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
