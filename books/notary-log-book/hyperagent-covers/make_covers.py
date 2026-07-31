#!/usr/bin/env python3
"""
KDP Cover Wrap Generator — "Notary Public Record Journal" (Meridian Press)

Builds a print-ready 12.5802" x 9.25" paperback cover wrap in three colourways.

    python make_covers.py                     # all 3 variations + PNGs
    python make_covers.py --variation navy    # one variation
    python make_covers.py --proof             # extra copy with fold/safe guides
    python make_covers.py --verify            # measure the output against KDP rules

⚠ SPEC CORRECTION (see ZONES below)
   HYPERAGENT_COVER_TASK.md defines the zone origins without bleed:
       SPINE_X = TRIM_W            -> 6.0000"
       FRONT_X = TRIM_W + SPINE    -> 6.3302"
   Those sum to 6.0 + 0.3302 + 6.0 = 12.3302", but COVER_W is 12.5802".
   The missing 0.25" is the two 0.125" bleeds. Used literally, the spine lands
   0.125" left of true centre: the fold lines miss the spine and spine text
   creeps onto the back cover. The corrected origins below include the leading
   bleed and reconcile exactly to COVER_W.
"""

import argparse
import io
import os
import sys

from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


# ══════════════════════════════════════════════════════════════════════════════
#  FONTS — cross-platform Georgia with a metric-compatible fallback
# ══════════════════════════════════════════════════════════════════════════════
def register_fonts(font_dir=None):
    """Georgia if present; otherwise Gelasio (metric-compatible, OFL)."""
    here = os.path.dirname(os.path.abspath(__file__))
    faces = {
        "Georgia":            ["georgia.ttf", "Georgia.ttf", "Gelasio-Regular.ttf"],
        "Georgia-Bold":       ["georgiab.ttf", "Georgia Bold.ttf", "Gelasio-Bold.ttf"],
        "Georgia-Italic":     ["georgiai.ttf", "Georgia Italic.ttf", "Gelasio-Italic.ttf"],
        "Georgia-BoldItalic": ["georgiaz.ttf", "Georgia Bold Italic.ttf", "Gelasio-BoldItalic.ttf"],
    }
    roots = [font_dir, os.path.join(here, "fonts"), "C:/Windows/Fonts",
             "/Library/Fonts", os.path.expanduser("~/Library/Fonts"),
             "/usr/share/fonts", "/usr/local/share/fonts", os.path.expanduser("~/.fonts")]
    roots = [r for r in roots if r and os.path.isdir(r)]
    substituted = []
    for name, files in faces.items():
        for root in roots:
            hit = None
            for fn in files:
                p = os.path.join(root, fn)
                if os.path.exists(p):
                    hit = p
                    break
            if hit is None:
                for dp, _, fs in os.walk(root):
                    for fn in files:
                        if fn in fs:
                            hit = os.path.join(dp, fn)
                            break
                    if hit:
                        break
            if hit:
                pdfmetrics.registerFont(TTFont(name, hit))
                if "gelasio" in os.path.basename(hit).lower():
                    substituted.append(name)
                break
        else:
            raise RuntimeError(f"No font file found for {name} (looked in {roots})")
    pdfmetrics.registerFontFamily("Georgia", normal="Georgia", bold="Georgia-Bold",
                                  italic="Georgia-Italic", boldItalic="Georgia-BoldItalic")
    if substituted:
        print("  [fonts] Georgia unavailable — using Gelasio (Georgia-metric) for: "
              + ", ".join(substituted))


# ══════════════════════════════════════════════════════════════════════════════
#  GEOMETRY  (verified — reconciles exactly to COVER_W / COVER_H)
# ══════════════════════════════════════════════════════════════════════════════
TRIM_W, TRIM_H = 6.0 * inch, 9.0 * inch
BLEED = 0.125 * inch
SPINE = 0.3302 * inch                      # 120pp x 0.002252" + 0.06"
SAFE = 0.25 * inch                         # KDP minimum from trim

COVER_W = TRIM_W * 2 + SPINE + BLEED * 2   # 12.5802"
COVER_H = TRIM_H + BLEED * 2               # 9.25"

BACK_X = BLEED                             # back trim starts after the left bleed
SPINE_X = BLEED + TRIM_W                   # 6.125"   (spec said 6.0000")
FRONT_X = BLEED + TRIM_W + SPINE           # 6.4552"  (spec said 6.3302")
TRIM_B, TRIM_T = BLEED, BLEED + TRIM_H     # vertical trim edges

SPINE_TEXT_SAFE = 0.0625 * inch            # KDP max print shift per fold


# ══════════════════════════════════════════════════════════════════════════════
#  COLOURWAYS
# ══════════════════════════════════════════════════════════════════════════════
VARIATIONS = {
    "navy": dict(
        slug="navy-gold", label="Navy / Gold (Classic)",
        bg="#1B2A4A", accent="#D4AF37", text="#FFFFFF", subtitle="#D8DEE9",
        recolor_art=False,   # front.png is already navy
    ),
    "charcoal": dict(
        slug="charcoal-silver", label="Charcoal / Silver (Modern)",
        bg="#2D2D2D", accent="#C0C0C0", text="#FFFFFF", subtitle="#B0B0B0",
        recolor_art=True,    # duotone the navy artwork to charcoal/silver
    ),
    "midnight": dict(
        slug="midnight-copper", label="Midnight Blue / Copper (Profound)",
        bg="#0D1B2A", accent="#B87333", text="#FFFFFF", subtitle="#D4E4F7",
        recolor_art=True,    # duotone the navy artwork to midnight/copper
    ),
}

# ── Copy ──────────────────────────────────────────────────────────────────────
TITLE_1, TITLE_2 = "NOTARY PUBLIC", "RECORD JOURNAL"
SUBTITLE = "Official Log of Notarial Acts"
IMPRINT = "Meridian Press"
TAGLINE = '100+ PRE-NUMBERED ENTRIES  ·  6" × 9"'
SPINE_TEXT = "NOTARY PUBLIC RECORD JOURNAL"
BACK_HEADLINE = ["Keep a compliant, court-ready", "record of every notarial act."]
BACK_BULLETS = [
    "100+ pre-numbered entry pages — sequential numbering deters tampering",
    "One complete notarial act per page: date, act type, signer ID, fee, signature",
    "Right-thumbprint box and official-seal area on every entry",
    'Portable 6 × 9 inch format for the desk, briefcase, or mobile signings',
]
BACK_BIO = ["Meridian Press is an independent publisher",
            "of legal and professional journals."]


# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def wrap(c, text, font, size, max_w):
    """Word-wrap to max_w, returning a list of lines."""
    out, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if c.stringWidth(t, font, size) <= max_w:
            cur = t
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def tint_emblem(path, hex_color, px=900):
    """
    Recolour the emblem line-art to the variation's accent, preserving alpha.
    Without this the gold seal clashes on the silver and copper covers.
    Returns an ImageReader, or None if unavailable.
    """
    if not (HAS_PIL and path and os.path.exists(path)):
        return None
    src = Image.open(path).convert("RGBA")
    if src.size != (px, px):
        src = src.resize((px, px), Image.LANCZOS)
    rgb = tuple(int(hex_color.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    solid = Image.new("RGBA", src.size, rgb + (255,))
    solid.putalpha(src.split()[-1])          # keep original transparency
    buf = io.BytesIO()
    solid.save(buf, format="PNG")
    buf.seek(0)
    return ImageReader(buf)


def prepare_front_art(path, v, target_w_pt, target_h_pt, art_dpi=400):
    """
    Load the high-res front artwork, centre-crop it to the target aspect (never
    stretch), and duotone it into the variation's palette when the source hue
    doesn't belong there.

    front.png is navy, so it ships as-is on the Navy/Gold cover. On Charcoal and
    Midnight it would clash, so its luminance is remapped onto that colourway's
    background→accent ramp. Texture survives, palette matches.
    """
    if not (HAS_PIL and path and os.path.exists(path)):
        return None, None
    Image.MAX_IMAGE_PIXELS = None
    src = Image.open(path).convert("RGB")

    # ── centre-crop to the exact target aspect (no distortion) ───────────────
    tgt = target_w_pt / target_h_pt
    sw, sh = src.size
    if sw / sh > tgt:                       # source too wide -> trim sides
        new_w = int(round(sh * tgt))
        off = (sw - new_w) // 2
        src = src.crop((off, 0, off + new_w, sh))
    elif sw / sh < tgt:                     # source too tall -> trim top/bottom
        new_h = int(round(sw / tgt))
        off = (sh - new_h) // 2
        src = src.crop((0, off, sw, off + new_h))

    # ── resample to the target print resolution ─────────────────────────────
    # The source lands at ~547 DPI on this panel. A 300 DPI press cannot use
    # that, and the extra pixels cost ~12 MB of PDF. 400 DPI keeps a comfortable
    # margin over the KDP minimum at roughly half the bytes. --art-dpi 0 keeps
    # the native resolution.
    if art_dpi and art_dpi > 0:
        want_w = int(round(art_dpi * target_w_pt / 72))
        want_h = int(round(art_dpi * target_h_pt / 72))
        if want_w < src.width:
            src = src.resize((want_w, want_h), Image.LANCZOS)

    # ── duotone for the non-navy colourways ─────────────────────────────────
    if v.get("recolor_art"):
        try:
            import numpy as np
        except ImportError:
            print("  [art] numpy unavailable — using artwork un-recoloured")
        else:
            lum = np.asarray(src.convert("L"), dtype=np.float32)
            lo_v, hi_v = float(lum.min()), float(lum.max())
            t = (lum - lo_v) / max(1.0, hi_v - lo_v)          # normalise contrast
            bg = np.array([int(v["bg"].lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32)
            ac = np.array([int(v["accent"].lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32)
            lo = bg * 0.62                                     # deep shadow end
            hi = ac                                            # accent highlights
            out = lo[None, None, :] + t[:, :, None] * (hi - lo)[None, None, :]
            src = Image.fromarray(np.clip(out, 0, 255).astype("uint8"))

    eff_dpi = min(src.width / (target_w_pt / 72), src.height / (target_h_pt / 72))
    buf = io.BytesIO()
    src.save(buf, format="PNG", compress_level=6)
    buf.seek(0)
    return ImageReader(buf), eff_dpi


def gradient_scrim(c, x, y, w, h, rgb, max_alpha, dark_at_top):
    """Soft vertical scrim so text stays legible over artwork (no hard seam)."""
    steps = 64
    bh = h / steps
    c.setFillColorRGB(*rgb)
    for i in range(steps):
        t = i / (steps - 1)
        c.setFillAlpha(max_alpha * (t if dark_at_top else (1 - t)))
        c.rect(x, y + i * bh, w, bh + 0.8, fill=1, stroke=0)
    c.setFillAlpha(1)


def draw_emblem_fallback(c, cx, cy, r, accent):
    """Vector scales-of-justice seal, used when the PNG asset is missing."""
    import math
    c.setStrokeColor(accent)
    c.setLineWidth(1.4)
    c.circle(cx, cy, r, fill=0, stroke=1)
    c.setLineWidth(0.8)
    c.circle(cx, cy, r * 0.88, fill=0, stroke=1)
    c.setFillColor(accent)
    for k in range(24):                                    # star ring
        a = math.pi / 2 + k * 2 * math.pi / 24
        sx, sy = cx + r * 0.79 * math.cos(a), cy + r * 0.79 * math.sin(a)
        pts = []
        for i in range(10):
            rr = r * 0.035 if i % 2 == 0 else r * 0.015
            aa = -math.pi / 2 + i * math.pi / 5
            pts.append((sx + rr * math.cos(aa), sy + rr * math.sin(aa)))
        p = c.beginPath()
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        p.close()
        c.drawPath(p, fill=1, stroke=0)
    w = r * 0.58                                           # balance scales
    top, base = cy + w * 0.52, cy - w * 0.62
    lw = max(1.0, r * 0.035)
    c.setStrokeColor(accent)
    c.setLineWidth(lw)
    c.line(cx, top, cx, base + w * 0.14)
    c.line(cx - w, top, cx + w, top)
    for sx in (cx - w, cx + w):
        py = top - w * 0.34
        c.setLineWidth(max(0.7, lw - 0.4))
        c.line(sx, top, sx - w * 0.30, py)
        c.line(sx, top, sx + w * 0.30, py)
        c.setLineWidth(lw)
        c.arc(sx - w * 0.34, py - w * 0.30, sx + w * 0.34, py + w * 0.30, 190, 160)
    c.line(cx - w * 0.42, base + w * 0.14, cx + w * 0.42, base + w * 0.14)
    c.line(cx - w * 0.30, base, cx + w * 0.30, base)


# ══════════════════════════════════════════════════════════════════════════════
#  PANELS
# ══════════════════════════════════════════════════════════════════════════════
def draw_front(c, v, emblem_path, front_art=None, force_emblem=False):
    accent, text, sub = HexColor(v["accent"]), HexColor(v["text"]), HexColor(v["subtitle"])
    x0, cx = FRONT_X, FRONT_X + TRIM_W / 2
    safe_w = TRIM_W - 2 * SAFE - 0.2 * inch

    # ══ LAYER 1: embedded high-res artwork, full bleed on the front panel ════
    # Spans FRONT_X to the right edge and the full height, so the trim can shift
    # ±0.0625" without exposing a white sliver.
    art_w = COVER_W - FRONT_X
    has_art = front_art is not None
    if has_art:
        c.drawImage(front_art, FRONT_X, 0, width=art_w, height=COVER_H,
                    preserveAspectRatio=False, mask=None)
        # scrims keep the vector type readable over whatever the artwork does
        bg_rgb = tuple(int(v["bg"].lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4))
        gradient_scrim(c, FRONT_X, COVER_H - 2.85 * inch, art_w, 2.85 * inch, bg_rgb, 0.55, True)
        gradient_scrim(c, FRONT_X, 0, art_w, 1.85 * inch, bg_rgb, 0.62, False)

    # ══ LAYER 2+: vector elements, all on top of the artwork ═════════════════
    # keyline frame — classic legal-document device, inset well inside safe
    c.setStrokeColor(accent)
    c.setLineWidth(0.9)
    m = 0.42 * inch
    c.rect(x0 + m, TRIM_B + m, TRIM_W - 2 * m, TRIM_H - 2 * m, fill=0, stroke=1)
    c.setLineWidth(0.4)
    m2 = m + 0.055 * inch
    c.rect(x0 + m2, TRIM_B + m2, TRIM_W - 2 * m2, TRIM_H - 2 * m2, fill=0, stroke=1)

    # ── Title block ───────────────────────────────────────────────────────────
    y = TRIM_T - 1.30 * inch
    c.setFillColor(text)
    size = 36
    while c.stringWidth(TITLE_1, "Georgia-Bold", size) > safe_w and size > 18:
        size -= 0.5
    c.setFont("Georgia-Bold", size)
    c.drawCentredString(cx, y, TITLE_1)
    y -= 0.42 * inch

    c.setFillColor(sub)
    c.setFont("Georgia", 20)
    c.drawCentredString(cx, y, TITLE_2)
    y -= 0.30 * inch

    c.setStrokeColor(accent)                       # accent rule
    c.setLineWidth(1.1)
    c.line(cx - 1.35 * inch, y, cx + 1.35 * inch, y)
    y -= 0.28 * inch

    c.setFillColor(accent)
    c.setFont("Georgia-Italic", 12)
    c.drawCentredString(cx, y, SUBTITLE)

    # ── Emblem (2" diameter, optically centred in the open field) ─────────────
    # front.png ALREADY carries a gold scales seal at its centre — drawing ours
    # on top produces two overlapping seals. When artwork is embedded the vector
    # emblem is suppressed unless explicitly forced.
    if has_art and not force_emblem:
        pass
    else:
        d = 2.0 * inch
        ecy = TRIM_B + TRIM_H * 0.47
        art = tint_emblem(emblem_path, v["accent"])
        if art is not None:
            c.drawImage(art, cx - d / 2, ecy - d / 2, width=d, height=d, mask="auto")
        else:
            draw_emblem_fallback(c, cx, ecy, d / 2, accent)

    # ── Imprint + tagline ─────────────────────────────────────────────────────
    c.setFillColor(text)
    c.setFont("Georgia", 14)
    c.drawCentredString(cx, TRIM_B + 1.15 * inch, IMPRINT)
    c.setFillColor(accent)
    c.setFont("Georgia", 9)
    c.drawCentredString(cx, TRIM_B + 0.88 * inch, TAGLINE)


def draw_spine(c, v):
    """Rotated spine text, only if it clears KDP's ±1/16in fold tolerance."""
    accent, text = HexColor(v["accent"]), HexColor(v["text"])
    cx = SPINE_X + SPINE / 2
    size = 8
    if SPINE < 2 * SPINE_TEXT_SAFE + size:
        return False
    c.saveState()
    c.translate(cx, TRIM_B + TRIM_H / 2)
    c.rotate(90)
    c.setFillColor(text)
    c.setFont("Georgia-Bold", size)
    c.drawCentredString(0, -size * 0.36, SPINE_TEXT)
    c.restoreState()
    # accent pips top and bottom of the spine
    c.setFillColor(accent)
    for yy in (TRIM_T - 0.55 * inch, TRIM_B + 0.55 * inch):
        c.circle(cx, yy, 1.6, fill=1, stroke=0)
    return True


def draw_back(c, v):
    accent, text, sub = HexColor(v["accent"]), HexColor(v["text"]), HexColor(v["subtitle"])

    # Matching keyline frame — mirrors the front and gives the copy a container,
    # so the generous space around it reads as composed rather than empty.
    m = 0.42 * inch
    c.setStrokeColor(accent)
    c.setLineWidth(0.9)
    c.rect(BACK_X + m, TRIM_B + m, TRIM_W - 2 * m, TRIM_H - 2 * m, fill=0, stroke=1)
    c.setLineWidth(0.4)
    m2 = m + 0.055 * inch
    c.rect(BACK_X + m2, TRIM_B + m2, TRIM_W - 2 * m2, TRIM_H - 2 * m2, fill=0, stroke=1)

    pad = m + 0.20 * inch
    x0 = BACK_X + pad
    inner_w = TRIM_W - 2 * pad

    y = TRIM_T - 1.15 * inch
    c.setFillColor(text)
    c.setFont("Georgia-Bold", 16)
    for line in BACK_HEADLINE:
        c.drawString(x0, y, line)
        y -= 0.26 * inch
    y -= 0.10 * inch

    c.setStrokeColor(accent)
    c.setLineWidth(0.9)
    c.line(x0, y, x0 + 1.6 * inch, y)
    y -= 0.30 * inch

    for b in BACK_BULLETS:
        c.setFillColor(accent)
        c.setFont("Georgia", 10)
        c.drawString(x0, y, "•")
        c.setFillColor(sub)
        for ln in wrap(c, b, "Georgia", 10, inner_w - 16):
            c.drawString(x0 + 16, y, ln)
            y -= 0.195 * inch
        y -= 0.105 * inch

    y -= 0.16 * inch
    c.setFillColor(sub)
    c.setFont("Georgia-Italic", 9)
    for line in BACK_BIO:
        c.drawString(x0, y, line)
        y -= 0.17 * inch

    # ── Barcode reserve: KDP prints its barcode here, keep it clear ───────────
    # Kept inside the keyline frame so the panel still reads as one composition.
    bw, bh = 2.0 * inch, 1.2 * inch
    bx = BACK_X + TRIM_W - pad - bw
    by = TRIM_B + pad + 0.06 * inch
    c.setFillColor(white)
    c.rect(bx, by, bw, bh, fill=1, stroke=0)
    c.setFillColor(HexColor("#666666"))
    c.setFont("Georgia", 6.5)
    c.drawCentredString(bx + bw / 2, by + bh / 2 - 2, "Barcode area — added by KDP")

    # bottom anchor: short accent rule + imprint line
    c.setStrokeColor(accent)
    c.setLineWidth(0.6)
    c.line(x0, by + 0.46 * inch, x0 + 1.15 * inch, by + 0.46 * inch)
    c.setFillColor(sub)
    c.setFont("Georgia", 8)
    c.drawString(x0, by + 0.24 * inch, "Independently published")


def draw_guides(c):
    """Magenta fold / trim / safe guides. PROOF ONLY — never upload."""
    c.setStrokeColor(HexColor("#FF00AA"))
    c.setLineWidth(0.5)
    c.setDash(4, 3)
    for gx in (BLEED, SPINE_X, FRONT_X, FRONT_X + TRIM_W):
        c.line(gx, 0, gx, COVER_H)
    c.line(0, TRIM_B, COVER_W, TRIM_B)
    c.line(0, TRIM_T, COVER_W, TRIM_T)
    c.setStrokeColor(HexColor("#00B0FF"))
    for x0 in (BACK_X, FRONT_X):
        c.rect(x0 + SAFE, TRIM_B + SAFE, TRIM_W - 2 * SAFE, TRIM_H - 2 * SAFE, fill=0, stroke=1)
    c.setDash()


# ══════════════════════════════════════════════════════════════════════════════
#  BUILD
# ══════════════════════════════════════════════════════════════════════════════
def build_cover(key, outdir, emblem_path=None, proof=False,
                front_art_path=None, force_emblem=False, art_dpi=400):
    v = VARIATIONS[key]
    suffix = "-PROOF" if proof else ""
    path = os.path.join(outdir, f"cover-wrap-{v['slug']}{suffix}.pdf")
    os.makedirs(outdir, exist_ok=True)

    # front panel target: trim width + right bleed, full wrap height
    front_art, eff_dpi = prepare_front_art(front_art_path, v, COVER_W - FRONT_X, COVER_H, art_dpi)

    c = canvas.Canvas(path, pagesize=(COVER_W, COVER_H), pdfVersion=(1, 4))
    c.setTitle(f"Notary Public Record Journal — cover ({v['label']})")
    c.setAuthor("Meridian Press")
    c.setSubject("KDP paperback cover wrap, 6x9, 120pp")
    c.setCreator("make_covers.py")

    c.setFillColor(HexColor(v["bg"]))              # background across full bleed
    c.rect(0, 0, COVER_W, COVER_H, fill=1, stroke=0)

    draw_back(c, v)
    spine_ok = draw_spine(c, v)
    draw_front(c, v, emblem_path, front_art=front_art, force_emblem=force_emblem)
    if proof:
        draw_guides(c)

    c.showPage()
    c.save()
    return path, spine_ok, eff_dpi


def export_panels(pdf_path, outdir, slug, dpi=300):
    """Front-only and back-only PNGs at 1800x2700 (6x9 @300dpi)."""
    try:
        import fitz
    except ImportError:
        print("  [png] PyMuPDF not installed — skipping panel PNGs")
        return []
    made = []
    d = fitz.open(pdf_path)
    page = d[0]
    panels = {"front": fitz.Rect(FRONT_X, COVER_H - TRIM_T, FRONT_X + TRIM_W, COVER_H - TRIM_B),
              "back": fitz.Rect(BACK_X, COVER_H - TRIM_T, BACK_X + TRIM_W, COVER_H - TRIM_B)}
    for name, clip in panels.items():
        out = os.path.join(outdir, f"{name}-cover-{slug}.png")
        page.get_pixmap(dpi=dpi, clip=clip).save(out)
        made.append(out)
    d.close()
    return made


# ══════════════════════════════════════════════════════════════════════════════
#  VERIFY
# ══════════════════════════════════════════════════════════════════════════════
def verify(pdf_path):
    """Measure the finished PDF against KDP cover rules."""
    try:
        import fitz
    except ImportError:
        print("  [verify] PyMuPDF not installed")
        return True
    d = fitz.open(pdf_path)
    p = d[0]
    ok = True
    w_in, h_in = p.rect.width / 72, p.rect.height / 72
    checks = []
    checks.append(("page count == 1", d.page_count == 1, str(d.page_count)))
    checks.append(("wrap 12.5802 x 9.2500 in",
                   abs(w_in - COVER_W / 72) < 0.002 and abs(h_in - COVER_H / 72) < 0.002,
                   f"{w_in:.4f} x {h_in:.4f}"))
    checks.append(("zones reconcile to COVER_W",
                   abs((BLEED * 2 + TRIM_W * 2 + SPINE) - COVER_W) < 1e-6,
                   f"{(BLEED*2+TRIM_W*2+SPINE)/72:.4f}in"))
    # text safe zones + spine clearance
    # sentinels must be in POINTS — a bare 9.0 is 0.125in and can never be beaten
    worst_panel, worst_spine, spine_seen = 9.0 * inch, 9.0 * inch, False
    for b in p.get_text("blocks"):
        if not b[4].strip():
            continue
        x0, y0, x1, y1 = b[0], COVER_H - b[3], b[2], COVER_H - b[1]
        v_gap = min(y0 - TRIM_B, TRIM_T - y1)
        if x1 <= SPINE_X + 1:
            worst_panel = min(worst_panel, x0 - BACK_X, (BACK_X + TRIM_W) - x1, v_gap)
        elif x0 >= FRONT_X - 1:
            worst_panel = min(worst_panel, x0 - FRONT_X, (FRONT_X + TRIM_W) - x1, v_gap)
        else:
            spine_seen = True
            worst_spine = min(worst_spine, x0 - SPINE_X, (SPINE_X + SPINE) - x1)
    checks.append((f'panel text >= {SAFE/72:.2f}" from trim', worst_panel >= SAFE,
                   f"{worst_panel/72:.3f}in"))
    if spine_seen:
        checks.append((f'spine text >= {SPINE_TEXT_SAFE/72:.4f}" from folds',
                       worst_spine >= SPINE_TEXT_SAFE, f"{worst_spine/72:.4f}in"))
    fonts = sorted({f[3].split("+")[-1] for f in p.get_fonts()})
    used = set()
    for blk in p.get_text("dict")["blocks"]:
        for ln in blk.get("lines", []):
            for sp in ln["spans"]:
                used.add(sp["font"])
    checks.append(("all rendered text is Georgia/Gelasio",
                   all(u.startswith(("Georgia", "Gelasio")) for u in used), ", ".join(sorted(used))))
    magenta = sum(1 for dr in p.get_drawings()
                  for k in ("color", "fill")
                  if (col := dr.get(k)) and col[0] > 0.8 and col[1] < 0.35 and col[2] > 0.4)
    checks.append(("no proof guides in upload file", magenta == 0, f"{magenta} magenta ops"))
    for label, passed, detail in checks:
        print(f"    [{'PASS' if passed else 'FAIL'}] {label}  — {detail}")
        ok &= passed
    d.close()
    return ok


def main():
    ap = argparse.ArgumentParser(description="KDP cover wrap generator (3 colourways)")
    ap.add_argument("--variation", choices=list(VARIATIONS) + ["all"], default="all")
    ap.add_argument("--outdir", default="books/notary-log-book")
    ap.add_argument("--emblem", default="assets/covers/emblems/seal-scales.png")
    ap.add_argument("--front-art", default="assets/covers/front.png",
                    help="high-res front artwork to embed (use 'none' for vector-only)")
    ap.add_argument("--force-emblem", action="store_true",
                    help="draw the vector emblem even when artwork is embedded")
    ap.add_argument("--art-dpi", type=int, default=400,
                    help="resample embedded artwork to this DPI (0 = keep native ~547)")
    ap.add_argument("--font-dir", default=None)
    ap.add_argument("--proof", action="store_true", help="also emit a guides copy")
    ap.add_argument("--no-png", action="store_true")
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()

    register_fonts(a.font_dir)
    emblem = a.emblem if (a.emblem and os.path.exists(a.emblem)) else None
    if emblem is None:
        print(f"  [emblem] {a.emblem} not found — drawing the vector seal instead")

    art = None if str(a.front_art).lower() in ("none", "") else a.front_art
    if art and not os.path.exists(art):
        print(f"  [art] {art} not found — building vector-only covers")
        art = None

    keys = list(VARIATIONS) if a.variation == "all" else [a.variation]
    default_src = None
    for k in keys:
        v = VARIATIONS[k]
        path, spine_ok, art_dpi = build_cover(k, a.outdir, emblem, proof=False,
                                              front_art_path=art, force_emblem=a.force_emblem,
                                              art_dpi=a.art_dpi)
        mb = os.path.getsize(path) / 1e6
        print(f"\n  {v['label']}\n    {path}  ({mb:.1f} MB)")
        if art_dpi:
            print(f"    artwork embedded at {art_dpi:.0f} DPI effective"
                  + ("  (duotoned to this palette)" if v.get("recolor_art") else ""))
        if not spine_ok:
            print("    [spine] too narrow for text at 8pt — omitted")
        if a.proof:
            pp, _, _ = build_cover(k, a.outdir, emblem, proof=True,
                                   front_art_path=art, force_emblem=a.force_emblem,
                                   art_dpi=a.art_dpi)
            print(f"    {pp}   (guides — DO NOT UPLOAD)")
        if not a.no_png:
            for f in export_panels(path, a.outdir, v["slug"]):
                print(f"    {f}")
        if a.verify:
            verify(path)
        if k == "navy":
            default_src = path

    # cover-wrap-final.pdf = the recommended default (Navy/Gold)
    if default_src and a.variation in ("all", "navy"):
        final = os.path.join(a.outdir, "cover-wrap-final.pdf")
        with open(default_src, "rb") as s, open(final, "wb") as d:
            d.write(s.read())
        print(f"\n  default -> {final}  (Navy/Gold)")


if __name__ == "__main__":
    main()
