# ══════════════════════════════════════════════════════════════════════════════
#  FRONT-MATTER PAGE TEMPLATES  —  paste into entry_page.py
#  Replaces the existing draw_cover_page / draw_instructions_page /
#  draw_index_pages / draw_notes_page.
#
#  Matches the v9 entry-page visual language:
#    · Georgia family only          · BAR_GAP = 13, SEC_GAP = 6
#    · HEADER_BG #C8C8C8 bars      · margins 0.5" inside / 0.3" outside
#      (grey bars everywhere)        0.45" top / 0.375" bottom
#    · no page numbers              · nothing below FOOTER_GUARD (36pt)
# ══════════════════════════════════════════════════════════════════════════════

from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch

# Import from entry_page.py (must be on sys.path)
from entry_page import (draw_page_number, _seal, _writeline, _para,
                         _margins_for_page, _margins_for_page_raw,
                         HEADER_BG, BAR_TEXT_COLOR, BAR_COLOR, ACCENT_LINE,
                         DGRAY, MGRAY, LGRAY, NAVY, STEEL,
                         GUTTER, OUTER, TOP_MARGIN, FOOTER_BASELINE, FOOTER_GUARD)

# ─── Shared front-matter constants ────────────────────────────────────────────
BAR_GAP = 13          # gap between a bar and its content  (matches entry page)
SEC_GAP = 6           # gap between stacked sections       (matches entry page)
BOX_FILL = HexColor("#F0F0F0")   # reference-box fill (light grey, POD-safe)
ROW_RULE = HexColor("#E2E6EC")   # faint column dividers in the index


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


# ══════════════════════════════════════════════════════════════════════════════
#  1 — COVER PAGE
# ══════════════════════════════════════════════════════════════════════════════
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


# ══════════════════════════════════════════════════════════════════════════════
#  2 — INSTRUCTIONS PAGE
# ══════════════════════════════════════════════════════════════════════════════
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
    # Pure bottom-anchoring left a ~1.8" hole under the instructions. Flowing
    # them naturally and only pushing up if they'd breach FOOTER_GUARD keeps the
    # page visually continuous *and* print-safe.
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


# ══════════════════════════════════════════════════════════════════════════════
#  3 — INDEX PAGE
# ══════════════════════════════════════════════════════════════════════════════
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


# ══════════════════════════════════════════════════════════════════════════════
#  4 — NOTES PAGE
# ══════════════════════════════════════════════════════════════════════════════
NOTES_LINE_GAP = 0.32 * inch


def draw_notes_page(c, W, H, phys_page, gutter_in=None, outer_in=None, top_in=0.4):
    """
    Lined writing page: navy header, ruled lines at 0.32" down to the footer
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
