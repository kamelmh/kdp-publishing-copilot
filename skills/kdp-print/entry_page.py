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
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Georgia font family for readability at small sizes
pdfmetrics.registerFont(TTFont('Georgia', 'C:/Windows/Fonts/georgia.ttf'))
pdfmetrics.registerFont(TTFont('Georgia-Bold', 'C:/Windows/Fonts/georgiab.ttf'))
pdfmetrics.registerFont(TTFont('Georgia-Italic', 'C:/Windows/Fonts/georgiai.ttf'))
pdfmetrics.registerFont(TTFont('Georgia-BoldItalic', 'C:/Windows/Fonts/georgiaz.ttf'))

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

# ─── Front-matter constants ────────────────────────────────────────────────────
BAR_GAP = 13          # gap between a bar and its content  (matches entry page)
SEC_GAP = 6           # gap between stacked sections       (matches entry page)
BOX_FILL = HexColor("#F0F0F0")   # reference-box fill (light grey, POD-safe)
ROW_RULE = HexColor("#E2E6EC")   # faint column dividers in the index

# ─── KDP Spec Constants ────────────────────────────────────────────────────────
TRIM_W = 6.0 * inch
TRIM_H = 9.0 * inch
GUTTER = 0.5 * inch
OUTER = 0.3 * inch
TOP_MARGIN = 0.45 * inch
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
    c.setFont("Georgia-Bold", 8)
    c.drawString(x + 4, y + 3, title)


def _thumbprint(c, x, y, s=72):
    """Draw thumbprint box."""
    c.setStrokeColor(DGRAY)
    c.setLineWidth(0.8)
    c.rect(x, y, s, s, fill=0, stroke=1)
    c.setFillColor(MGRAY)
    c.setFont("Georgia", 7)
    c.drawCentredString(x + s/2, y + s/2 + 4, "RIGHT")
    c.drawCentredString(x + s/2, y + s/2 - 6, "THUMB")
    c.setFont("Georgia", 6)
    c.drawCentredString(x + s/2, y - 10, "Signer's Right Thumbprint")


def _seal(c, cx, cy, r=28):
    """Draw official seal circle (dashed)."""
    c.setStrokeColor(DGRAY)
    c.setLineWidth(0.8)
    c.setDash(3, 3)
    c.circle(cx, cy, r, fill=0, stroke=1)
    c.setDash()
    c.setFillColor(MGRAY)
    c.setFont("Georgia", 6.5)
    c.drawCentredString(cx, cy + 3, "OFFICIAL")
    c.drawCentredString(cx, cy - 7, "SEAL")


def draw_page_number(c, W, phys_page):
    """Centered page number at bottom."""
    c.setFillColor(LGRAY)
    c.setFont("Georgia", 7)
    c.drawCentredString(W / 2, FOOTER_BASELINE, str(phys_page))


def _header_bar(c, x, y, w, title, size=13, h=None, align="left", pad=8):
    """
    Grey header bar with dark Georgia-Bold text, vertically centred.
    Matches the entry page HEADER_BG style.
    Height auto-derives from the type size unless overridden.
    """
    h = h if h is not None else size + 16
    c.setFillColor(HEADER_BG)
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.setFillColor(BAR_TEXT_COLOR)
    c.setFont("Georgia-Bold", size)
    baseline = y + (h - size * 0.72) / 2 + 1
    if align == "center":
        c.drawCentredString(x + w / 2, baseline, title)
    else:
        c.drawString(x + pad, baseline, title)
    return h


def _fit_lines(c, text, font, size, max_w):
    """Break text into lines that fit max_w (keeps whole words)."""
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if c.stringWidth(t, font, size) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def _labelled_rule(c, x, y, w, label, size=9.5, gap=6):
    """'Label:' followed by a writing rule filling the remaining width."""
    c.setFillColor(DGRAY)
    c.setFont("Georgia", size)
    c.drawString(x, y, label)
    lw = c.stringWidth(label, "Georgia", size)
    _writeline(c, x + lw + gap, y - 2, w - lw - gap)


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
    BAR_H = 13  # section bar height
    BAR_GAP = 13  # gap between section bar and its content
    SEC_GAP = 6  # gap between sections

    # ─── Header bar ────────────────────────────────────────────────────────────
    hb_h = 24
    y = H - top - hb_h
    c.setFillColor(HEADER_BG)
    c.rect(lm, y, uw, hb_h, fill=1, stroke=0)
    c.setFillColor(DGRAY)
    c.setFont("Georgia-Bold", 10)
    c.drawString(lm + 6, y + 8, "NOTARIAL ACT RECORD")
    c.setFont("Georgia-Bold", 9)
    c.drawRightString(lm + uw - 6, y + 8, f"Entry No. {entry_no:03d}")
    y -= 14

    # ─── A — Date & Time ──────────────────────────────────────────────────────
    _section_bar(c, lm, y - BAR_H, uw, "A — DATE & TIME")
    y -= BAR_H + BAR_GAP
    c.setFillColor(DGRAY)
    c.setFont("Georgia", 8.5)
    c.drawString(lm, y, "Date:")
    _writeline(c, lm + 45, y - 2, 130)
    c.drawString(lm + 190, y, "Time:")
    _writeline(c, lm + 220, y - 2, 60)
    _checkbox(c, lm + 290, y - 1)
    c.drawString(lm + 301, y, "AM")
    _checkbox(c, lm + 324, y - 1)
    c.drawString(lm + 335, y, "PM")
    y -= RH + SEC_GAP

    # ─── B — Type of Notarial Act ─────────────────────────────────────────────
    _section_bar(c, lm, y - BAR_H, uw, "B — TYPE OF NOTARIAL ACT")
    y -= BAR_H + BAR_GAP
    c.setFillColor(DGRAY)
    c.setFont("Georgia", 8)
    row1 = ["Acknowledgment", "Oath / Affirmation", "Copy Certification"]
    cx = lm
    for a in row1:
        _checkbox(c, cx, y - 1)
        c.drawString(cx + 11, y, a)
        cx += 11 + c.stringWidth(a, "Georgia", 8) + 18
    y -= RH
    row2 = ["Signature Witnessing", "Jurat"]
    cx = lm
    for a in row2:
        _checkbox(c, cx, y - 1)
        c.drawString(cx + 11, y, a)
        cx += 11 + c.stringWidth(a, "Georgia", 8) + 18
    _checkbox(c, cx, y - 1)
    c.drawString(cx + 11, y, "Other:")
    _writeline(c, cx + 11 + c.stringWidth("Other:", "Georgia", 8) + 6, y - 2, lm + uw - cx - 60)
    y -= RH + SEC_GAP

    # ─── C — Document Information ──────────────────────────────────────────────
    _section_bar(c, lm, y - BAR_H, uw, "C — DOCUMENT INFORMATION")
    y -= BAR_H + BAR_GAP
    for lbl in ["Document Type:", "Document Date / No. of Pages:", "Description / Title:"]:
        c.setFillColor(DGRAY)
        c.setFont("Georgia", 8.5)
        c.drawString(lm, y, lbl)
        lw = c.stringWidth(lbl, "Georgia", 8.5)
        _writeline(c, lm + lw + 6, y - 2, uw - lw - 8)
        y -= RH
    y -= SEC_GAP

    # ─── D — Signer Information ────────────────────────────────────────────────
    _section_bar(c, lm, y - BAR_H, uw, "D — SIGNER INFORMATION")
    y -= BAR_H + BAR_GAP
    for lbl in ["Full Name:", "Address:", "ID Type / Number / Exp.:", "Signer's Signature:"]:
        c.setFillColor(DGRAY)
        c.setFont("Georgia", 8.5)
        c.drawString(lm, y, lbl)
        lw = c.stringWidth(lbl, "Georgia", 8.5)
        _writeline(c, lm + lw + 6, y - 2, uw - lw - 8)
        y -= RH
    y -= SEC_GAP

    # ─── E — Witness ───────────────────────────────────────────────────────────
    e_top = y
    ew = uw * 0.58
    ex = lm if outer_right else (lm + uw - ew)
    _section_bar(c, ex, e_top - BAR_H, ew, "E — WITNESS (IF APPLICABLE)")
    yw = e_top - BAR_H - BAR_GAP
    for lbl in ["Witness 1 Name:", "Witness 1 Signature:", "Witness 2 Name:", "Witness 2 Signature:"]:
        c.setFillColor(DGRAY)
        c.setFont("Georgia", 8.5)
        c.drawString(ex, yw, lbl)
        lw = c.stringWidth(lbl, "Georgia", 8.5)
        _writeline(c, ex + lw + 4, yw - 2, ew - lw - 6)
        yw -= RH

    # ─── F — Thumbprint (on outer edge) ────────────────────────────────────────
    thumb = 72
    thumb_x = (lm + uw - thumb) if outer_right else lm
    thumb_y = e_top - 15 - thumb
    _section_bar(c, thumb_x, e_top - BAR_H, thumb, "F — THUMB")
    _thumbprint(c, thumb_x, thumb_y, thumb)
    y = e_top - 118

    # ─── G — Fees ──────────────────────────────────────────────────────────────
    _section_bar(c, lm, y - BAR_H, uw, "G — FEES")
    y -= BAR_H + BAR_GAP
    c.setFillColor(DGRAY)
    c.setFont("Georgia", 8.5)
    c.drawString(lm, y, "Fee Charged: $")
    _writeline(c, lm + 78, y - 2, 80)
    cx = lm + 175
    for p in ["Cash", "Check", "Elec.", "Waived"]:
        _checkbox(c, cx, y - 1)
        c.drawString(cx + 11, y, p)
        cx += 11 + c.stringWidth(p, "Georgia", 8.5) + 12
    y -= RH + SEC_GAP

    # ─── H — Notary Certification & Signature ──────────────────────────────────
    _section_bar(c, lm, y - BAR_H, uw, "H — NOTARY CERTIFICATION & SIGNATURE")
    y -= BAR_H + BAR_GAP
    c.setFillColor(MGRAY)
    c.setFont("Georgia-Italic", 7)
    c.drawString(lm, y, "I certify that the signer personally appeared before me on the date stated above.")
    y -= 20

    # Seal sits to the right of signature lines
    seal_cx = (lm + uw - 38) if outer_right else (lm + 38)
    _seal(c, seal_cx, y - 14, r=32)

    # Signature fields to the left of the seal
    sig_w = uw - 82
    sig_x = lm if outer_right else (lm + 82)
    for lbl in ["Notary Name:", "Commission # / Exp.:", "Notary Signature:"]:
        c.setFillColor(DGRAY)
        c.setFont("Georgia", 8.5)
        c.drawString(sig_x, y, lbl)
        lw = c.stringWidth(lbl, "Georgia", 8.5)
        _writeline(c, sig_x + lw + 4, y - 2, sig_w - lw - 6)
        y -= RH
    y -= SEC_GAP

    # ─── Footer ────────────────────────────────────────────────────────────────
    # No page number — Affinity handles pagination
    c.showPage()


def draw_cover_page(c, W, H, meta=None, phys_page=1):
    """
    Title page: grey masthead, seal, commission fields, volume line,
    grey disclaimer bar. No page number.
    """
    lm, rm, _ = _margins_for_page(phys_page)
    uw = W - lm - rm
    y = H - TOP_MARGIN

    # ─── Masthead: grey band containing the title ────────────────────────────
    TITLE, T_SIZE = "NOTARY PUBLIC RECORD JOURNAL", 22
    lines = _fit_lines(c, TITLE, "Georgia-Bold", T_SIZE, uw - 24)
    band_h = 22 + len(lines) * (T_SIZE + 6)
    band_y = y - band_h
    c.setFillColor(HEADER_BG)
    c.rect(lm, band_y, uw, band_h, fill=1, stroke=0)
    c.setFillColor(BAR_TEXT_COLOR)
    c.setFont("Georgia-Bold", T_SIZE)
    ty = band_y + band_h - 20 - T_SIZE * 0.28
    for ln in lines:
        c.drawCentredString(lm + uw / 2, ty, ln)
        ty -= T_SIZE + 6
    y = band_y - 22

    # ─── Subtitle ────────────────────────────────────────────────────────────
    c.setFillColor(DGRAY)
    c.setFont("Georgia-Italic", 11)
    c.drawCentredString(lm + uw / 2, y, "Official Log of Notarial Acts")
    y -= 18

    # thin accent rule under the subtitle
    c.setStrokeColor(ACCENT_LINE)
    c.setLineWidth(0.6)
    c.line(lm + uw * 0.30, y, lm + uw * 0.70, y)
    y -= 16

    # ─── Disclaimer bar: measure first so the middle block can be centred ────
    disc = ("This journal is the exclusive property of the notary named above and is "
            "maintained in compliance with applicable state law.")
    d_lines = _fit_lines(c, disc, "Georgia-Italic", 7.5, uw - 24)
    d_h = 14 + len(d_lines) * 11
    d_y = FOOTER_GUARD + 6

    # ─── Centre the seal + fields + volume block in the space that remains ───
    seal_r, FIELD_RH = 48, 26
    fields = [
        "Notary's Full Name:",
        "Commission Number:",
        "State / Jurisdiction:",
        "Office / Employer:",
        "Commission Expires:",
    ]
    seal_gap = 34
    block_h = 2 * seal_r + seal_gap + len(fields) * FIELD_RH + 8 + 14
    avail = y - (d_y + d_h)
    y -= max(0, (avail - block_h) / 2)

    _seal(c, lm + uw / 2, y - seal_r, r=seal_r)
    y -= 2 * seal_r + seal_gap

    for label in fields:
        _labelled_rule(c, lm, y, uw, label, size=9.5)
        y -= FIELD_RH

    # ─── Volume / Year ───────────────────────────────────────────────────────
    y -= 4
    c.setFillColor(DGRAY)
    c.setFont("Georgia", 9.5)
    c.drawString(lm, y, "Volume")
    _writeline(c, lm + 42, y - 2, 52)
    c.drawString(lm + 100, y, "of")
    _writeline(c, lm + 116, y - 2, 52)
    c.drawRightString(lm + uw - 60, y, "Year:")
    _writeline(c, lm + uw - 56, y - 2, 56)

    # ─── Disclaimer bar ──────────────────────────────────────────────────────
    c.setFillColor(HEADER_BG)
    c.rect(lm, d_y, uw, d_h, fill=1, stroke=0)
    c.setFillColor(BAR_TEXT_COLOR)
    c.setFont("Georgia-Italic", 7.5)
    dy = d_y + d_h - 12
    for ln in d_lines:
        c.drawCentredString(lm + uw / 2, dy, ln)
        dy -= 11

    c.showPage()


def _para(c, x, y, width, head, body, lead=14, size=9.5):
    """Bold lead-in head + body text, word-wrapped within `width`. Returns next y."""
    c.setFont("Georgia-Bold", size)
    c.setFillColor(NAVY)
    c.drawString(x, y, head)
    hw = c.stringWidth(head + "  ", "Georgia-Bold", size)
    c.setFont("Georgia", size)
    c.setFillColor(black)
    startx, avail, line, cy = x + hw, width - hw, "", y
    for w in body.split():
        t = (line + " " + w).strip()
        if c.stringWidth(t, "Georgia", size) <= avail:
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


def draw_instructions_page(c, W, H, phys_page=2):
    """
    How-to-use page: grey header, six instruction items, and two reference
    boxes anchored up from the footer guard so they can never collide with
    the page edge. No page number.
    """
    lm, rm, _ = _margins_for_page(phys_page)
    uw = W - lm - rm

    # ─── Grey header bar ────────────────────────────────────────────────────
    bar_h = 30
    y = H - TOP_MARGIN - bar_h
    _header_bar(c, lm, y, uw, "How to Use This Journal", size=14, h=bar_h)
    y -= BAR_GAP + 8

    # ─── Instruction items ───────────────────────────────────────────────────
    items = [
        ("Sequential numbering.", "Entries are pre-numbered from 001 onward. Never skip, "
         "remove, or reorder a page — sequential numbering deters tampering and satisfies "
         "most state record-keeping requirements."),
        ("One act per entry.", "Record a single notarial act on each numbered page. Complete "
         "every applicable field at the time of the act, in permanent ink."),
        ("Identification.", "Note the signer's ID type, number, and expiration date. Capture "
         "the signer's right thumbprint in the box on the outer edge when your state requires it."),
        ("Fees.", "Record the fee charged, or mark it Waived, to stay within your state's "
         "fee schedule."),
        ("When full.", "Store completed journals securely for your state's retention period "
         "(often 7 to 10 years). Begin a new volume and update the Volume ___ of ___ line."),
        ("Index.", "Use the summary index at the back of this journal to locate entries quickly."),
    ]
    for head, body in items:
        y = _para(c, lm, y, uw, head, body, lead=13, size=9.5)

    # ─── Reference boxes — FLOW after the text, then CLAMP to the guard ──────
    ROW, HDR, PAD = 13, 20, 8

    def _refbox(bottom, title, rows):
        h = HDR + len(rows) * ROW + PAD
        c.setFillColor(BOX_FILL)
        c.setStrokeColor(BAR_TEXT_COLOR)
        c.setLineWidth(0.8)
        c.rect(lm, bottom, uw, h, fill=1, stroke=1)
        c.setFillColor(BAR_TEXT_COLOR)
        c.setFont("Georgia-Bold", 9.5)
        c.drawString(lm + 10, bottom + h - 15, title)
        ry = bottom + h - HDR - 11
        for label, value in rows:
            c.setFillColor(DGRAY)
            c.setFont("Georgia-Bold", 7.5)
            c.drawString(lm + 18, ry, label)
            lw = c.stringWidth(label, "Georgia-Bold", 7.5)
            c.setFont("Georgia", 7.5)
            c.drawString(lm + 18 + lw + 5, ry, value)
            ry -= ROW
        return h

    fees = [
        ("Acknowledgment:", "$5 – $15"), ("Oath / Affirmation:", "$5 – $10"),
        ("Jurat:", "$5 – $15"), ("Copy Certification:", "$5 – $10"),
        ("Signature Witnessing:", "$5 – $15"), ("Proof of Execution:", "$5 – $20"),
    ]
    states = [
        ("California:", "Thumbprint required. Journal required by law. 4-year retention."),
        ("Florida:", "Thumbprint optional. No journal requirement (recommended)."),
        ("New York:", "No journal requirement. 10-year retention recommended."),
        ("Texas:", "No journal requirement. 5-year retention recommended."),
        ("Illinois:", "No journal requirement. 5-year retention recommended."),
        ("Pennsylvania:", "No journal requirement. 10-year retention recommended."),
    ]

    BOX_GAP = 14
    state_h = HDR + len(states) * ROW + PAD
    fee_h = HDR + len(fees) * ROW + PAD

    # natural flow: state box first, fee box beneath it
    state_bottom = y - (SEC_GAP * 3) - state_h
    fee_bottom = state_bottom - BOX_GAP - fee_h
    # clamp: if the lower box would breach the guard, lift both together
    lift = max(0, (FOOTER_GUARD + 4) - fee_bottom)
    state_bottom += lift
    fee_bottom += lift

    _refbox(state_bottom, "STATE-SPECIFIC REQUIREMENTS", states)
    _refbox(fee_bottom, "TYPICAL FEE SCHEDULE (US)", fees)

    c.showPage()


# ─── Index page constants ──────────────────────────────────────────────────────
INDEX_COLS_IN = (0, 0.45, 1.30, 2.65, 3.65, 4.65)   # inches from the text-block left
INDEX_HDRS = ("No.", "Date", "Signer Name", "Doc Type", "Act Type", "Fee")
INDEX_ROWS_PER_PAGE = 28


def draw_index_page(c, W, H, phys_page, start_entry=1, rows=INDEX_ROWS_PER_PAGE,
                    last_entry=None, gutter_in=None, outer_in=None):
    """
    ONE index page — 6-column journal summary. Template-friendly: draws exactly
    `rows` rows starting at `start_entry`, never overflowing the page.
    Returns the next entry number. No page number.
    """
    gutter_pt = (gutter_in * inch) if gutter_in is not None else GUTTER
    outer_pt = (outer_in * inch) if outer_in is not None else OUTER
    lm, rm, _ = _margins_for_page_raw(phys_page, gutter_pt, outer_pt)
    uw = W - lm - rm

    # ─── Grey header bar (centred) ──────────────────────────────────────────
    bar_h = 28
    y = H - TOP_MARGIN - bar_h
    _header_bar(c, lm, y, uw, "JOURNAL INDEX / SUMMARY", size=13, h=bar_h, align="center")
    y -= BAR_GAP + 4

    # ─── Column headers (steel) ──────────────────────────────────────────────
    cols = [lm + x * inch for x in INDEX_COLS_IN]
    c.setFillColor(STEEL)
    c.setFont("Georgia-Bold", 8)
    for i, hd in enumerate(INDEX_HDRS):
        c.drawString(cols[i] + 2, y, hd)
    y -= 5
    c.setStrokeColor(STEEL)
    c.setLineWidth(0.8)
    c.line(lm, y, lm + uw, y)
    y -= 3

    # ─── Rows: fit evenly between the header rule and the footer guard ───────
    top_of_rows = y
    row_h = (top_of_rows - FOOTER_GUARD) / rows
    entry = start_entry
    for i in range(rows):
        if last_entry is not None and entry > last_entry:
            break
        ry = top_of_rows - (i + 1) * row_h + 4
        c.setFillColor(DGRAY)
        c.setFont("Georgia", 8)
        c.drawString(cols[0] + 2, ry, f"{entry:03d}")
        # faint column dividers
        c.setStrokeColor(ROW_RULE)
        c.setLineWidth(0.4)
        for cx in cols[1:]:
            c.line(cx, ry - 4, cx, ry + 9)
        # row rule
        c.setStrokeColor(ACCENT_LINE)
        c.setLineWidth(0.4)
        c.line(lm, ry - 4, lm + uw, ry - 4)
        entry += 1

    c.showPage()
    return entry


def draw_index_pages(c, W, H, total_entries, start_phys_page, gutter_in, outer_in,
                     top_in=0.4):
    """
    Multi-page wrapper kept for kdp_print.py compatibility.
    Delegates to draw_index_page so pagination lives in one place.
    Returns the next physical page number.
    """
    entry, phys = 1, start_phys_page
    while entry <= total_entries:
        entry = draw_index_page(c, W, H, phys, start_entry=entry,
                                rows=INDEX_ROWS_PER_PAGE, last_entry=total_entries,
                                gutter_in=gutter_in, outer_in=outer_in)
        phys += 1
    return phys


# ─── Notes page ────────────────────────────────────────────────────────────────
NOTES_LINE_GAP = 0.32 * inch


def draw_notes_page(c, W, H, phys_page, gutter_in=None, outer_in=None, top_in=0.4):
    """
    Lined writing page: grey header, ruled lines at 0.32" down to the footer
    guard. No page number.
    """
    gutter_pt = (gutter_in * inch) if gutter_in is not None else GUTTER
    outer_pt = (outer_in * inch) if outer_in is not None else OUTER
    lm, rm, _ = _margins_for_page_raw(phys_page, gutter_pt, outer_pt)
    uw = W - lm - rm

    bar_h = 26
    y = H - TOP_MARGIN - bar_h
    _header_bar(c, lm, y, uw, "NOTES / ADDITIONAL RECORDS", size=12, h=bar_h)
    y -= BAR_GAP + 10

    while y > FOOTER_GUARD:
        _writeline(c, lm, y, uw)
        y -= NOTES_LINE_GAP

    c.showPage()
