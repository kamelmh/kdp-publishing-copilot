#!/usr/bin/env python3
"""
Chemotherapy Treatment Journal — Full Cover PDF Generator
Generates a styled KDP paperback cover (front + spine + back) with bleed.

Usage:
  python build_chemo_cover.py
"""

from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import math

# ── Fonts ──────────────────────────────────────────────────────────────
FONTS_DIR = "C:/Windows/Fonts"
pdfmetrics.registerFont(TTFont("Georgia", f"{FONTS_DIR}/georgia.ttf"))
pdfmetrics.registerFont(TTFont("Georgia-Bold", f"{FONTS_DIR}/georgiab.ttf"))
pdfmetrics.registerFont(TTFont("Georgia-Italic", f"{FONTS_DIR}/georgiai.ttf"))
pdfmetrics.registerFont(TTFont("Georgia-BoldItalic", f"{FONTS_DIR}/georgiaz.ttf"))

# ── KDP Print Specs ────────────────────────────────────────────────────
INTERIOR_W = 8.5 * inch
INTERIOR_H = 11.0 * inch
BLEED = 0.125 * inch
PAGES = 130
SPINE_PER_PAGE = 0.002252  # inches per page, white paper
SPINE_ALLOWANCE = 0.06     # inches
SPINE_IN = (PAGES * SPINE_PER_PAGE) + SPINE_ALLOWANCE
SPINE = SPINE_IN * inch

COVER_W = BLEED + INTERIOR_W + SPINE + INTERIOR_W + BLEED
COVER_H = BLEED + INTERIOR_H + BLEED

# ── Colors ─────────────────────────────────────────────────────────────
IVORY    = HexColor("#FBF7F1")
SAGE     = HexColor("#8CA396")
BLUSH    = HexColor("#E3B8B0")
SLATE    = HexColor("#A9BFC9")
CHARCOAL = HexColor("#3F3A36")
TAUPE    = HexColor("#D8D0C7")
WHITE    = HexColor("#FFFFFF")
SAGE_LIGHT = HexColor("#B5C9BC")
BLUSH_LIGHT = HexColor("#F0D9D3")

# ── Derived positions ──────────────────────────────────────────────────
BACK_X  = 0
SPINE_X = BLEED + INTERIOR_W
FRONT_X = BLEED + INTERIOR_W + SPINE

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PDF = os.path.join(OUTPUT_DIR, "Chemo-Journal-Cover.pdf")


# ═══════════════════════════════════════════════════════════════════════
#  FRONT COVER
# ═══════════════════════════════════════════════════════════════════════
def draw_front_cover(c):
    fx = FRONT_X
    fw = INTERIOR_W
    fh = INTERIOR_H

    # ── Background: soft ivory ──
    c.setFillColor(IVORY)
    c.rect(fx, 0, fw, fh, fill=1, stroke=0)

    # ── Decorative color blocks ──
    # Top sage band
    band_h = 2.2 * inch
    c.setFillColor(SAGE)
    c.rect(fx, fh - band_h, fw, band_h, fill=1, stroke=0)

    # Blush accent stripe below sage
    stripe_h = 0.35 * inch
    c.setFillColor(BLUSH)
    c.rect(fx, fh - band_h - stripe_h, fw, stripe_h, fill=1, stroke=0)

    # Slate bottom panel
    bottom_h = 1.8 * inch
    c.setFillColor(SLATE)
    c.rect(fx, 0, fw, bottom_h, fill=1, stroke=0)

    # Taupe divider above bottom panel
    c.setFillColor(TAUPE)
    c.rect(fx, bottom_h, fw, 0.25 * inch, fill=1, stroke=0)

    # ── Title text ──
    title_y = fh - 0.9 * inch
    c.setFillColor(WHITE)
    c.setFont("Georgia-Bold", 28)
    c.drawCentredString(fx + fw / 2, title_y, "CHEMOTHERAPY")
    c.drawCentredString(fx + fw / 2, title_y - 36, "TREATMENT JOURNAL")

    # ── Decorative line under title ──
    line_y = title_y - 55
    line_w = 3.5 * inch
    c.setStrokeColor(WHITE)
    c.setLineWidth(1.5)
    c.line(fx + fw / 2 - line_w / 2, line_y, fx + fw / 2 + line_w / 2, line_y)

    # ── Subtitle on sage band ──
    c.setFont("Georgia-Italic", 13)
    c.setFillColor(HexColor("#FFFFFFCC"))
    c.drawCentredString(fx + fw / 2, title_y - 75, "Tracking Symptoms · Medications · Appointments · Wellness")

    # ── Decorative dots on blush stripe ──
    c.setFillColor(WHITE)
    dot_y = fh - band_h - stripe_h / 2
    for i in range(7):
        dot_x = fx + fw / 2 + (i - 3) * 30
        c.circle(dot_x, dot_y, 3, fill=1, stroke=0)

    # ── Body area icons (on ivory section) ──
    icon_y = fh - band_h - stripe_h - 2.5 * inch
    c.setFillColor(CHARCOAL)
    c.setFont("Georgia", 11)

    # Section labels in the middle ivory area
    mid_x = fx + fw / 2
    sections = [
        ("📋", "Treatment Logs"),
        ("💊", "Medication Tracker"),
        ("📊", "Lab Results"),
        ("💭", "Reflections & Affirmations"),
    ]

    c.setFont("Georgia-Bold", 12)
    c.setFillColor(CHARCOAL)
    c.drawCentredString(mid_x, icon_y + 0.8 * inch, "What's Inside")

    c.setFont("Georgia", 10)
    c.setFillColor(HexColor("#5A5550"))
    y_offset = 0.4 * inch
    for emoji, label in sections:
        c.drawCentredString(mid_x, icon_y + y_offset - 0.05 * inch, label)
        y_offset -= 0.3 * inch

    # ── Author in bottom panel ──
    c.setFillColor(WHITE)
    c.setFont("Georgia-Bold", 14)
    c.drawCentredString(mid_x, bottom_h / 2 + 8, "MERIDIAN PRESS")

    # ── Decorative line in bottom panel ──
    c.setStrokeColor(WHITE)
    c.setLineWidth(0.75)
    line_bot_y = bottom_h / 2 - 8
    c.line(mid_x - 1.5 * inch, line_bot_y, mid_x + 1.5 * inch, line_bot_y)

    c.setFont("Georgia-Italic", 9)
    c.setFillColor(HexColor("#FFFFFFBB"))
    c.drawCentredString(mid_x, bottom_h / 2 - 25, "A Personal Journey Through Treatment")

    # ── Thin sage border around entire front cover ──
    c.setStrokeColor(SAGE)
    c.setLineWidth(2)
    inset = 0.2 * inch
    c.rect(fx + inset, inset, fw - 2 * inset, fh - 2 * inset, fill=0, stroke=1)


# ═══════════════════════════════════════════════════════════════════════
#  SPINE
# ═══════════════════════════════════════════════════════════════════════
def draw_spine(c):
    sx = SPINE_X
    sw = SPINE
    sh = INTERIOR_H

    # Background
    c.setFillColor(SAGE)
    c.rect(sx, 0, sw, sh, fill=1, stroke=0)

    # Title text (rotated)
    c.setFillColor(WHITE)
    c.setFont("Georgia-Bold", 9)
    c.saveState()
    c.translate(sx + sw / 2, sh / 2)
    c.rotate(90)
    c.drawCentredString(0, 4, "CHEMOTHERAPY TREATMENT JOURNAL")
    c.restoreState()

    # Author at spine bottom
    c.saveState()
    c.translate(sx + sw / 2, sh / 2)
    c.rotate(90)
    c.setFont("Georgia", 7)
    c.setFillColor(HexColor("#FFFFFFCC"))
    c.drawCentredString(0, -40, "MERIDIAN PRESS")
    c.restoreState()

    # Decorative thin lines at top and bottom
    c.setStrokeColor(WHITE)
    c.setLineWidth(0.5)
    c.line(sx, sh - 0.3 * inch, sx + sw, sh - 0.3 * inch)
    c.line(sx, 0.3 * inch, sx + sw, 0.3 * inch)


# ═══════════════════════════════════════════════════════════════════════
#  BACK COVER
# ═══════════════════════════════════════════════════════════════════════
def draw_back_cover(c):
    bx = BACK_X
    bw = INTERIOR_W
    bh = INTERIOR_H

    # Background
    c.setFillColor(IVORY)
    c.rect(bx, 0, bw, bh, fill=1, stroke=0)

    # Sage top bar (matches front)
    bar_h = 0.8 * inch
    c.setFillColor(SAGE)
    c.rect(bx, bh - bar_h, bw, bar_h, fill=1, stroke=0)

    # ── Title echo ──
    c.setFillColor(WHITE)
    c.setFont("Georgia-Bold", 16)
    c.drawCentredString(bx + bw / 2, bh - 0.55 * inch, "CHEMOTHERAPY TREATMENT JOURNAL")

    # ── Description block ──
    desc_y = bh - 1.5 * inch
    desc_x = bx + 0.6 * inch
    desc_w = bw - 1.2 * inch

    c.setFillColor(CHARCOAL)
    c.setFont("Georgia-Bold", 12)
    c.drawString(desc_x, desc_y, "A Thoughtful Companion Through Every Session")

    c.setFont("Georgia", 10)
    c.setFillColor(HexColor("#4A4540"))
    lines = [
        "Track treatments, medications, lab results, and how you",
        "feel — all in one organized, calming journal designed",
        "for clarity when you need it most.",
        "",
        "Featuring traffic-light symptom severity, daily logs,",
        "medication tracking, hydration and nutrition pages,",
        "reflection prompts, and milestone celebrations.",
    ]
    y = desc_y - 22
    for line in lines:
        c.drawString(desc_x, y, line)
        y -= 16

    # ── Features box ──
    feat_y = y - 0.3 * inch
    c.setFillColor(TAUPE)
    c.roundRect(desc_x, feat_y - 2.2 * inch, desc_w, 2.2 * inch, 6, fill=1, stroke=0)

    c.setFillColor(CHARCOAL)
    c.setFont("Georgia-Bold", 10)
    feat_title_y = feat_y - 0.2 * inch
    c.drawString(desc_x + 0.2 * inch, feat_title_y, "Inside This Journal:")

    c.setFont("Georgia", 9)
    features = [
        "✓  12 Chemo Cycle Trackers",
        "✓  26 Daily Symptom Logs (UKONS Traffic Light)",
        "✓  Medication & Appointment Trackers",
        "✓  Hydration, Nutrition & Sleep Pages",
        "✓  Lab Results with Flag Indicators",
        "✓  Reflection Prompts & Affirmations",
        "✓  Milestone Celebrations",
    ]
    fy = feat_title_y - 20
    for feat in features:
        c.drawString(desc_x + 0.3 * inch, fy, feat)
        fy -= 18

    # ── Blush accent stripe ──
    stripe_y = 2.8 * inch
    c.setFillColor(BLUSH)
    c.rect(bx, stripe_y, bw, 0.15 * inch, fill=1, stroke=0)

    # ── Barcode area ──
    barcode_w = 2.0 * inch
    barcode_h = 1.2 * inch
    barcode_x = bx + bw - barcode_w - 0.5 * inch
    barcode_y = 0.8 * inch

    c.setStrokeColor(CHARCOAL)
    c.setLineWidth(0.5)
    c.setDash(2, 2)
    c.rect(barcode_x, barcode_y, barcode_w, barcode_h, fill=0, stroke=1)
    c.setDash()

    c.setFillColor(HexColor("#888888"))
    c.setFont("Helvetica", 7)
    c.drawCentredString(barcode_x + barcode_w / 2, barcode_y + barcode_h / 2 + 5, "ISBN BARCODE")
    c.drawCentredString(barcode_x + barcode_w / 2, barcode_y + barcode_h / 2 - 8, "(KDP auto-generates)")

    # ── Price & category text ──
    c.setFillColor(CHARCOAL)
    c.setFont("Georgia", 8)
    c.drawString(0.5 * inch, 1.4 * inch, "8.5 × 11 in  •  130 Pages  •  B&W Interior")
    c.drawString(0.5 * inch, 1.05 * inch, "ISBN: (Free KDP ISBN)")
    c.drawString(0.5 * inch, 0.7 * inch, "Printed in the United States")

    # ── Thin sage border (matches front) ──
    c.setStrokeColor(SAGE)
    c.setLineWidth(2)
    inset = 0.2 * inch
    c.rect(bx + inset, inset, bw - 2 * inset, bh - 2 * inset, fill=0, stroke=1)


# ═══════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════
def main():
    c = canvas.Canvas(OUTPUT_PDF)
    c.setPageSize((COVER_W, COVER_H))

    draw_back_cover(c)
    draw_spine(c)
    draw_front_cover(c)

    c.save()

    print(f"Generated: {OUTPUT_PDF}")
    print(f"Full cover: {COVER_W/inch:.2f}\" × {COVER_H/inch:.2f}\"")
    print(f"Spine: {SPINE_IN:.3f}\" ({PAGES} pages)")
    print(f"Front panel: {INTERIOR_W/inch}\" × {INTERIOR_H/inch}\"")
    print(f"Back panel:  {INTERIOR_W/inch}\" × {INTERIOR_H/inch}\"")
    print()
    print("KDP Upload Checklist:")
    print("  [OK] Cover includes 0.125\" bleed on all outer edges")
    print("  [OK] Spine width calculated for white paper")
    print("  [OK] Front cover: title, author, subtitle")
    print("  [OK] Back cover: description, features, barcode area")
    print("  [OK] Spine: title + author text")
    print()
    print("Next: Upload both PDFs to KDP Paperback Content screen.")


if __name__ == "__main__":
    main()
