#!/usr/bin/env python3
"""
KDP Preflight — verify a print-ready interior and/or cover wrap BEFORE uploading to KDP.

Measures the actual PDF (geometry, visible-ink margins, fonts, image DPI, trim-edge ink,
footer collisions, spine safe zones) rather than trusting a changelog. Exits non-zero on
any FAIL so it can gate a build step.

Usage:
    python preflight.py --interior interior.pdf --cover cover-wrap.pdf --size 6x9
    python preflight.py --interior interior.pdf --size 5x8 --paper cream
    python preflight.py --cover cover.pdf --size 8.5x11 --pages 150
    python preflight.py --interior i.pdf --cover c.pdf --size 6x9 --json report.json
    python preflight.py --interior i.pdf --size 6x9 --sample 10     # every 10th page (fast)

Notes:
  * Page count is auto-detected from the interior; --pages is only needed for a cover-only run.
  * Margins are measured from VISIBLE INK at --dpi (default 300). Font-metric bounding boxes
    include empty descender space and report margins ~0.03" pessimistically — don't use them.
  * Requires: pymupdf, numpy.  (pip install pymupdf numpy)
"""

import argparse
import json
import os
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("ERROR: pymupdf not installed. Run: pip install pymupdf")
try:
    import numpy as np
except ImportError:
    sys.exit("ERROR: numpy not installed. Run: pip install numpy")

# ─── Spec constants (mirrors kdp_print.py; kept local so preflight runs standalone) ──────
PAPER_THICKNESS = {"white": 0.002252, "cream": 0.0025, "color": 0.002347}
SPINE_ALLOWANCE = 0.06
BLEED = 0.125
MIN_MARGIN = 0.25          # KDP minimum outside/top/bottom
SPINE_SAFE = 0.0625        # KDP max print shift per fold
FOOTER_GUARD_PT = 36       # bottom-anchored elements should sit above this
BASE14 = {
    "Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Helvetica-BoldOblique",
    "Courier", "Courier-Bold", "Courier-Oblique", "Courier-BoldOblique",
    "Times-Roman", "Times-Bold", "Times-Italic", "Times-BoldItalic",
    "Symbol", "ZapfDingbats",
}
TRIM_SIZES = {
    "5x8": (5.0, 8.0), "5.06x7.81": (5.06, 7.81), "5.25x8": (5.25, 8.0),
    "5.5x8.5": (5.5, 8.5), "6x9": (6.0, 9.0), "6.14x9.21": (6.14, 9.21),
    "6.69x9.61": (6.69, 9.61), "7x10": (7.0, 10.0), "7.44x9.69": (7.44, 9.69),
    "7.5x9.25": (7.5, 9.25), "8x10": (8.0, 10.0), "8.5x11": (8.5, 11.0),
    "4.75x6.75": (4.75, 6.75), "8.5x8.5": (8.5, 8.5), "8.25x8.25": (8.25, 8.25),
}


def required_gutter(pages):
    if pages <= 150:
        return 0.375
    if pages <= 300:
        return 0.5
    if pages <= 500:
        return 0.625
    return 0.75


def spine_width(pages, paper="white"):
    return pages * PAPER_THICKNESS.get(paper, PAPER_THICKNESS["white"]) + SPINE_ALLOWANCE


# ─── Result collector ────────────────────────────────────────────────────────────────────
class Report:
    def __init__(self):
        self.rows = []

    def add(self, section, label, status, detail=""):
        self.rows.append({"section": section, "check": label, "status": status, "detail": detail})

    def ok(self, s, l, d=""):    self.add(s, l, "PASS", d)
    def bad(self, s, l, d=""):   self.add(s, l, "FAIL", d)
    def warn(self, s, l, d=""):  self.add(s, l, "WARN", d)
    def chk(self, s, l, cond, d="", warn_only=False):
        (self.ok if cond else (self.warn if warn_only else self.bad))(s, l, d)
        return cond

    @property
    def fails(self):
        return [r for r in self.rows if r["status"] == "FAIL"]

    @property
    def warns(self):
        return [r for r in self.rows if r["status"] == "WARN"]

    def render(self):
        cur = None
        icon = {"PASS": "PASS", "FAIL": "FAIL", "WARN": "WARN"}
        for r in self.rows:
            if r["section"] != cur:
                cur = r["section"]
                print(f"\n{'=' * 62}\n  {cur}\n{'=' * 62}")
            d = f"  — {r['detail']}" if r["detail"] else ""
            print(f"  [{icon[r['status']]}]  {r['check']}{d}")
        n = len(self.rows)
        print(f"\n{'=' * 62}")
        if self.fails:
            print(f"  {len(self.fails)} FAILED / {len(self.warns)} warnings / {n} checks — DO NOT UPLOAD")
            for r in self.fails:
                print(f"     -> {r['check']}: {r['detail']}")
        else:
            extra = f" ({len(self.warns)} warning(s) to review)" if self.warns else ""
            print(f"  ALL {n} CHECKS PASSED — CLEARED FOR UPLOAD{extra}")
        print("=" * 62)


# ─── Ink measurement ─────────────────────────────────────────────────────────────────────
def ink_bounds(page, dpi):
    """Return (left, right, top, bottom) inches from page edge to nearest visible ink,
    or None for a blank page."""
    pm = page.get_pixmap(dpi=dpi, colorspace=fitz.csGRAY)
    a = np.frombuffer(pm.samples, dtype=np.uint8).reshape(pm.height, pm.width)
    mask = a < 245
    if not mask.any():
        return None
    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]
    ppi = dpi
    return (cols[0] / ppi,
            (pm.width - 1 - cols[-1]) / ppi,
            rows[0] / ppi,
            (pm.height - 1 - rows[-1]) / ppi)


# ─── Interior checks ─────────────────────────────────────────────────────────────────────
def check_interior(path, size, paper, dpi, sample, rep):
    S = "INTERIOR"
    d = fitz.open(path)
    n = d.page_count
    rep.ok(S, "file opens as PDF", f"{os.path.basename(path)}, {os.path.getsize(path)//1024} KB")
    rep.chk(S, "page count is even", n % 2 == 0, f"{n} pages")
    rep.chk(S, "page count within 24–828", 24 <= n <= 828, f"{n}")

    sizes = {(round(p.rect.width, 1), round(p.rect.height, 1)) for p in d}
    rep.chk(S, "uniform page size", len(sizes) == 1, f"{len(sizes)} distinct size(s)")
    w_in, h_in = d[0].rect.width / 72, d[0].rect.height / 72

    if size:
        tw, th = TRIM_SIZES[size]
        rep.chk(S, f"trim matches {size}", abs(w_in - tw) < 0.02 and abs(h_in - th) < 0.02,
                f'{w_in:.3f} x {h_in:.3f}"')
        rep.chk(S, "no bleed (page == trim size)",
                abs(w_in - (tw + BLEED)) > 0.02 and abs(w_in - (tw + 2 * BLEED)) > 0.02,
                "interiors must not carry bleed")
    else:
        rep.warn(S, "trim size not asserted", f'detected {w_in:.3f} x {h_in:.3f}" (pass --size to verify)')
        tw, th = w_in, h_in

    m = d.metadata or {}
    rep.chk(S, "PDF metadata title set", bool(m.get("title")) and m["title"].lower() != "untitled",
            repr(m.get("title")), warn_only=True)
    rep.chk(S, "PDF metadata author set", bool(m.get("author")) and m["author"].lower() != "anonymous",
            repr(m.get("author")), warn_only=True)

    # fonts: base-14 or embedded
    bad_fonts = set()
    for p in d:
        for f in p.get_fonts(full=True):
            base, emb = f[3], f[1]
            clean = base.split("+")[-1]
            if clean not in BASE14 and not emb:
                bad_fonts.add(clean)
    rep.chk(S, "fonts base-14 or embedded", not bad_fonts, f"non-embedded: {sorted(bad_fonts)}" if bad_fonts else "")

    # raster image effective DPI
    low_dpi = []
    total_imgs = 0
    for pno, p in enumerate(d, 1):
        for info in p.get_image_info(xrefs=True):
            total_imgs += 1
            bb = fitz.Rect(info["bbox"])
            if bb.width <= 0 or bb.height <= 0:
                continue
            eff = min(info["width"] / (bb.width / 72), info["height"] / (bb.height / 72))
            if eff < 300:
                low_dpi.append((pno, round(eff)))
    if total_imgs == 0:
        rep.ok(S, "raster images >= 300 DPI", "0 rasters (all-vector — ideal)")
    else:
        rep.chk(S, "raster images >= 300 DPI", not low_dpi,
                f"{total_imgs} image(s); low-DPI: {low_dpi[:5]}" if low_dpi else f"{total_imgs} image(s)")

    # ── margins from visible ink ──
    pages = range(1, n + 1) if sample <= 1 else list(range(1, n + 1, sample))
    worst = {"bottom": (9, 0), "top": (9, 0), "gutter": (9, 0), "outer": (9, 0)}
    blanks = []
    for pno in pages:
        b = ink_bounds(d[pno - 1], dpi)
        if b is None:
            blanks.append(pno)
            continue
        left, right, top, bot = b
        gutter, outer = (left, right) if pno % 2 == 1 else (right, left)
        for k, v in (("bottom", bot), ("top", top), ("gutter", gutter), ("outer", outer)):
            if v < worst[k][0]:
                worst[k] = (v, pno)
    req_g = required_gutter(n)
    rep.chk(S, f'bottom margin >= {MIN_MARGIN}"', worst["bottom"][0] >= MIN_MARGIN,
            f'{worst["bottom"][0]:.3f}" (p{worst["bottom"][1]})')
    rep.chk(S, f'top margin >= {MIN_MARGIN}"', worst["top"][0] >= MIN_MARGIN,
            f'{worst["top"][0]:.3f}" (p{worst["top"][1]})')
    rep.chk(S, f'gutter >= {req_g}" (for {n}pp)', worst["gutter"][0] >= req_g,
            f'{worst["gutter"][0]:.3f}" (p{worst["gutter"][1]})')
    rep.chk(S, f'outer margin >= {MIN_MARGIN}"', worst["outer"][0] >= MIN_MARGIN,
            f'{worst["outer"][0]:.3f}" (p{worst["outer"][1]})')
    rep.chk(S, "no unintentionally blank pages", not blanks,
            f"blank: {blanks[:8]}" if blanks else "", warn_only=True)

    # ── ink at trim edge (no-bleed interiors must not have any) ──
    W, H = d[0].rect.width, d[0].rect.height
    edge = []
    for pno, p in enumerate(d, 1):
        for dr in p.get_drawings():
            f = dr.get("fill")
            if not f or all(c > 0.95 for c in f):
                continue
            r = dr["rect"]
            if r.x0 <= 1 or r.x1 >= W - 1 or r.y0 <= 1 or r.y1 >= H - 1:
                edge.append(pno)
                break
    rep.chk(S, "no colored ink at trim edge", not edge,
            f"{len(set(edge))} page(s): {sorted(set(edge))[:8]}" if edge else "")

    # ── footer collisions: any large box bottom below the guard, or text crossing a box edge ──
    low_boxes, crossings = [], []
    for pno, p in enumerate(d, 1):
        boxes = [dr["rect"] for dr in p.get_drawings()
                 if dr["rect"].width > W * 0.4 and 30 < dr["rect"].height < H * 0.6]
        for r in boxes:
            if (H - r.y1) < FOOTER_GUARD_PT:
                low_boxes.append((pno, round(H - r.y1, 1)))
            for b in p.get_text("blocks"):
                if not b[4].strip():
                    continue
                # text vertically straddling the box's bottom edge, horizontally inside it
                if b[1] < r.y1 < b[3] and b[0] >= r.x0 - 2 and b[2] <= r.x1 + 2:
                    crossings.append((pno, b[4].strip()[:18]))
    rep.chk(S, f"no box bottom below footer guard ({FOOTER_GUARD_PT}pt)", not low_boxes,
            f"{low_boxes[:5]}" if low_boxes else "")
    rep.chk(S, "no text straddling a box border", not crossings,
            f"{crossings[:5]}" if crossings else "")
    d.close()


# ─── Cover checks ────────────────────────────────────────────────────────────────────────
def check_cover(path, size, paper, pages, dpi, rep):
    S = "COVER WRAP"
    d = fitz.open(path)
    rep.ok(S, "file opens as PDF", f"{os.path.basename(path)}, {os.path.getsize(path)//1024} KB")
    rep.chk(S, "single page", d.page_count == 1, f"{d.page_count} page(s)")
    p = d[0]
    cw, ch = p.rect.width / 72, p.rect.height / 72

    if not size or not pages:
        rep.warn(S, "geometry not asserted", f'detected {cw:.4f} x {ch:.4f}" (need --size and page count)')
        d.close()
        return
    tw, th = TRIM_SIZES[size]
    sp = spine_width(pages, paper)
    exp_w, exp_h = tw * 2 + sp + BLEED * 2, th + BLEED * 2
    rep.chk(S, f'wrap size {exp_w:.4f} x {exp_h:.4f}"',
            abs(cw - exp_w) < 0.01 and abs(ch - exp_h) < 0.01, f'{cw:.4f} x {ch:.4f}"')
    rep.ok(S, f"spine width for {pages}pp {paper}", f'{sp:.4f}" ({sp*300:.0f}px @300DPI)')

    s0, s1 = BLEED + tw, BLEED + tw + sp
    trim_top, trim_bot = BLEED, BLEED + th

    # text safe zones
    worst_panel, worst_spine = 9.0, 9.0
    spine_found = False
    for b in p.get_text("blocks"):
        if not b[4].strip():
            continue
        x0, y0, x1, y1 = b[0] / 72, b[1] / 72, b[2] / 72, b[3] / 72
        v = min(y0 - trim_top, trim_bot - y1)
        if x1 <= s0 + 0.02:                       # back panel
            worst_panel = min(worst_panel, x0 - BLEED, (BLEED + tw) - x1, v)
        elif x0 >= s1 - 0.02:                     # front panel
            worst_panel = min(worst_panel, x0 - s1, (s1 + tw) - x1, v)
        else:                                     # spine
            spine_found = True
            worst_spine = min(worst_spine, x0 - s0, s1 - x1)
    rep.chk(S, f'front/back text >= {MIN_MARGIN}" from trim', worst_panel >= MIN_MARGIN,
            f'{worst_panel:.3f}"')
    if spine_found:
        rep.chk(S, f'spine text clearance >= {SPINE_SAFE}" per fold', worst_spine >= SPINE_SAFE,
                f'{worst_spine:.4f}" (KDP shift tolerance)')
        if sp < 0.35:
            rep.warn(S, "thin spine carries text", f'spine {sp:.3f}" — KDP advises caution under 0.35"')
    else:
        rep.warn(S, "no spine text detected", "fine for thin books, but check it was intended")

    # PROOF-file guard: magenta guides must never reach the upload
    magenta = 0
    for dr in p.get_drawings():
        for key in ("color", "fill"):
            c = dr.get(key)
            if c and c[0] > 0.8 and c[1] < 0.35 and c[2] > 0.4:
                magenta += 1
    rep.chk(S, "not a PROOF file (no magenta guides)", magenta == 0,
            f"{magenta} magenta ops — you may be uploading the proof!" if magenta else "")

    # barcode clear zone: lower-right of the BACK panel, ~2 x 1.2 in
    bz = fitz.Rect((s0 - 0.4 - 2.0) * 72, (trim_bot - 0.4 - 1.2) * 72, (s0 - 0.4) * 72, (trim_bot - 0.4) * 72)
    pm = p.get_pixmap(dpi=150, colorspace=fitz.csGRAY, clip=bz)
    arr = np.frombuffer(pm.samples, dtype=np.uint8).reshape(pm.height, pm.width)
    light = float((arr > 200).mean())
    rep.chk(S, "barcode zone kept clear (back, lower-right)", light > 0.85,
            f"{light*100:.0f}% light — KDP prints the barcode here", warn_only=True)
    d.close()


def main():
    ap = argparse.ArgumentParser(description="KDP preflight for interior and/or cover PDFs")
    ap.add_argument("--interior")
    ap.add_argument("--cover")
    ap.add_argument("--size", choices=sorted(TRIM_SIZES), help="trim size, e.g. 6x9")
    ap.add_argument("--paper", default="white", choices=["white", "cream", "color"])
    ap.add_argument("--pages", type=int, help="page count (auto-detected from --interior)")
    ap.add_argument("--dpi", type=int, default=300, help="ink-measurement DPI (default 300)")
    ap.add_argument("--sample", type=int, default=1, help="check every Nth page (default all)")
    ap.add_argument("--json", help="also write the report as JSON")
    a = ap.parse_args()
    if not a.interior and not a.cover:
        ap.error("provide --interior and/or --cover")

    rep = Report()
    pages = a.pages
    if a.interior:
        if not os.path.exists(a.interior):
            sys.exit(f"ERROR: not found: {a.interior}")
        pages = pages or fitz.open(a.interior).page_count
        check_interior(a.interior, a.size, a.paper, a.dpi, a.sample, rep)
    if a.cover:
        if not os.path.exists(a.cover):
            sys.exit(f"ERROR: not found: {a.cover}")
        check_cover(a.cover, a.size, a.paper, pages, a.dpi, rep)

    rep.render()
    if a.json:
        with open(a.json, "w") as f:
            json.dump({"checks": rep.rows,
                       "passed": len(rep.fails) == 0,
                       "fails": len(rep.fails),
                       "warns": len(rep.warns)}, f, indent=2)
        print(f"\nJSON report: {a.json}")
    sys.exit(1 if rep.fails else 0)


if __name__ == "__main__":
    main()
