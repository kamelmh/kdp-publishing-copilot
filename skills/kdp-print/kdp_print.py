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


# ─── Drawing helpers (interior) — imported from entry_page.py ─────────────────
# Single source of truth: entry_page.py
from entry_page import (
    draw_entry_page, draw_cover_page, draw_instructions_page,
    draw_index_pages, draw_notes_page, draw_page_number,
    NAVY, STEEL, DGRAY, MGRAY, LGRAY,
    FOOTER_BASELINE, FOOTER_GUARD,
)


# ─── Legacy helper aliases (used by draw_notary_entry) ────────────────────────
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


# ─── Notary entry page — legacy wrapper ────────────────────────────────────────
def draw_notary_entry(c, W, H, entry_no, total, phys_page, gutter_in, outer_in,
                      top_in=0.4, bottom_in=0.4):
    """Legacy wrapper — delegates to draw_entry_page from entry_page.py."""
    draw_entry_page(c, W, H, entry_no, phys_page, gutter_in=gutter_in, outer_in=outer_in)


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
    # --- PDF metadata (KDP reads these) ---
    c.setTitle("Notary Public Record Journal")
    c.setAuthor("Meridian Press")
    c.setSubject("Official Log of Notarial Acts")
    c.setKeywords("notary journal, notarial acts, record keeping")
    c.setCreator("KDP Print Skill v2.2")
    draw_cover_page(c, W, H)              # page 1 (meta param ignored by entry_page version)
    draw_instructions_page(c, W, H)       # page 2
    phys = 3
    for e in range(1, entries + 1):
        draw_entry_page(c, W, H, e, phys, gutter_in=gutter, outer_in=outer)
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
    SPINE_SAFE = 0.0625 * inch                 # KDP max print shift per fold
    if spine >= 2 * SPINE_SAFE + 8 and spine_text:
        size = min(8.0, (spine - 2 * SPINE_SAFE) * 0.9)   # cap 8pt, never breach safe zone
        c.saveState()
        c.translate(spine_x0 + spine / 2, CH / 2)
        c.rotate(90)
        c.setFillColor(text); c.setFont(title_font, size)
        c.drawCentredString(0, -size * 0.36, spine_text)  # optical centering
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
