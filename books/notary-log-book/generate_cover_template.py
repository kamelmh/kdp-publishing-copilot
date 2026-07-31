#!/usr/bin/env python3
"""
Generate cover template PDF with guide marks for Affinity Publisher.
Shows zones: back cover, spine, front cover, bleed, safe areas.
"""

import os
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Georgia font
pdfmetrics.registerFont(TTFont('Georgia', 'C:/Windows/Fonts/georgia.ttf'))
pdfmetrics.registerFont(TTFont('Georgia-Bold', 'C:/Windows/Fonts/georgiab.ttf'))

# ─── KDP Cover Specs (120pp, 6×9, white paper) ───────────────────────────────
TRIM_W = 6.0 * inch
TRIM_H = 9.0 * inch
BLEED = 0.125 * inch
SPINE = 0.3302 * inch

# Full cover wrap dimensions (with bleed)
COVER_W = (TRIM_W * 2) + SPINE + (BLEED * 2)  # 12.5802"
COVER_H = TRIM_H + (BLEED * 2)                 # 9.25"

# Zone positions (from left edge)
BACK_X = 0
BACK_W = TRIM_W
SPINE_X = TRIM_W
FRONT_X = TRIM_W + SPINE
FRONT_W = TRIM_W

# Safe zones (0.25" from trim for KDP)
SAFE_MARGIN = 0.25 * inch

# Colors
NAVY = HexColor("#1B2A4A")
LIGHT_BLUE = HexColor("#E8F4FD")
LIGHT_GRAY = HexColor("#F5F5F5")
GUIDE_RED = HexColor("#FF0066")
GUIDE_GREEN = HexColor("#00CC66")
GUIDE_ORANGE = HexColor("#FF9900")
GUIDE_PURPLE = HexColor("#9933FF")

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def draw_cover_template(output_path):
    """Generate cover template PDF with guide marks."""
    c = canvas.Canvas(output_path, pagesize=(COVER_W, COVER_H))
    
    # ─── Background ────────────────────────────────────────────────────────
    c.setFillColor(white)
    c.rect(0, 0, COVER_W, COVER_H, fill=1, stroke=0)
    
    # ─── Zone fills (semi-transparent) ─────────────────────────────────────
    # Back cover zone
    c.setFillColor(LIGHT_BLUE)
    c.rect(BACK_X, 0, BACK_W, COVER_H, fill=1, stroke=0)
    
    # Spine zone
    c.setFillColor(HexColor("#FFE4B5"))
    c.rect(SPINE_X, 0, SPINE, COVER_H, fill=1, stroke=0)
    
    # Front cover zone
    c.setFillColor(Light_Green := HexColor("#E8FFE8"))
    c.rect(FRONT_X, 0, FRONT_W, COVER_H, fill=1, stroke=0)
    
    # ─── Trim lines (dashed) ───────────────────────────────────────────────
    c.setStrokeColor(GUIDE_RED)
    c.setLineWidth(1)
    c.setDash(6, 3)
    
    # Back trim (left edge of back)
    c.line(BACK_X, 0, BACK_X, COVER_H)
    
    # Back/Spine trim (right edge of back = left edge of spine)
    c.line(SPINE_X, 0, SPINE_X, COVER_H)
    
    # Spine/Front trim (right edge of spine = left edge of front)
    c.line(FRONT_X, 0, FRONT_X, COVER_H)
    
    # Front trim (right edge of front)
    c.line(FRONT_X + FRONT_W, 0, FRONT_X + FRONT_W, COVER_H)
    
    # Top/Bleed trim
    c.line(0, BLEED, COVER_W, BLEED)
    c.line(0, COVER_H - BLEED, COVER_W, COVER_H - BLEED)
    
    c.setDash()
    
    # ─── Bleed lines (dotted) ──────────────────────────────────────────────
    c.setStrokeColor(GUIDE_ORANGE)
    c.setLineWidth(0.5)
    c.setDash(2, 2)
    
    # Outer bleed boundary
    c.rect(0, 0, COVER_W, COVER_H, fill=0, stroke=1)
    
    c.setDash()
    
    # ─── Safe zone lines (dotted) ──────────────────────────────────────────
    c.setStrokeColor(GUIDE_GREEN)
    c.setLineWidth(0.5)
    c.setDash(4, 2)
    
    # Back safe zone
    safe_back_x = SAFE_MARGIN
    safe_back_w = TRIM_W - (SAFE_MARGIN * 2)
    c.rect(safe_back_x, BLEED + SAFE_MARGIN, safe_back_w, TRIM_H - (SAFE_MARGIN * 2), fill=0, stroke=1)
    
    # Front safe zone
    safe_front_x = FRONT_X + SAFE_MARGIN
    safe_front_w = TRIM_W - (SAFE_MARGIN * 2)
    c.rect(safe_front_x, BLEED + SAFE_MARGIN, safe_front_w, TRIM_H - (SAFE_MARGIN * 2), fill=0, stroke=1)
    
    c.setDash()
    
    # ─── Center line (spine center) ────────────────────────────────────────
    c.setStrokeColor(GUIDE_PURPLE)
    c.setLineWidth(0.5)
    c.setDash(8, 4)
    spine_center_x = SPINE_X + (SPINE / 2)
    c.line(spine_center_x, 0, spine_center_x, COVER_H)
    c.setDash()
    
    # ─── Labels ────────────────────────────────────────────────────────────
    c.setFillColor(NAVY)
    c.setFont("Georgia-Bold", 10)
    
    # Back cover label
    c.drawCentredString(BACK_X + BACK_W / 2, COVER_H / 2, "BACK COVER")
    c.setFont("Georgia", 7)
    c.drawCentredString(BACK_X + BACK_W / 2, COVER_H / 2 - 14, f"{BACK_W / inch:.2f}\" × {TRIM_H / inch:.2f}\"")
    
    # Spine label
    c.saveState()
    c.translate(SPINE_X + SPINE / 2, COVER_H / 2)
    c.rotate(90)
    c.setFont("Georgia-Bold", 8)
    c.drawCentredString(0, 0, "SPINE")
    c.setFont("Georgia", 6)
    c.drawCentredString(0, -12, f"{SPINE / inch:.4f}\"")
    c.restoreState()
    
    # Front cover label
    c.setFont("Georgia-Bold", 10)
    c.drawCentredString(FRONT_X + FRONT_W / 2, COVER_H / 2, "FRONT COVER")
    c.setFont("Georgia", 7)
    c.drawCentredString(FRONT_X + FRONT_W / 2, COVER_H / 2 - 14, f"{FRONT_W / inch:.2f}\" × {TRIM_H / inch:.2f}\"")
    
    # ─── Dimension annotations ─────────────────────────────────────────────
    c.setFillColor(DGRAY := HexColor("#333333"))
    c.setFont("Georgia", 6)
    
    # Top dimensions
    y_top = COVER_H - 6
    c.drawCentredString(BACK_X + BACK_W / 2, y_top, f"Back: {BACK_W / inch:.2f}\"")
    c.drawCentredString(SPINE_X + SPINE / 2, y_top, f"Spine: {SPINE / inch:.4f}\"")
    c.drawCentredString(FRONT_X + FRONT_W / 2, y_top, f"Front: {FRONT_W / inch:.2f}\"")
    
    # Bottom dimensions
    y_bot = 8
    c.drawCentredString(COVER_W / 2, y_bot, f"Total: {COVER_W / inch:.4f}\" × {COVER_H / inch:.2f}\" (with bleed)")
    
    # ─── Legend ─────────────────────────────────────────────────────────────
    legend_x = 10
    legend_y = 20
    c.setFont("Georgia", 5)
    
    c.setFillColor(GUIDE_RED)
    c.rect(legend_x, legend_y, 8, 3, fill=1, stroke=0)
    c.setFillColor(DGRAY)
    c.drawString(legend_x + 12, legend_y, "Trim line")
    
    c.setFillColor(GUIDE_ORANGE)
    c.rect(legend_x + 70, legend_y, 8, 3, fill=1, stroke=0)
    c.setFillColor(DGRAY)
    c.drawString(legend_x + 82, legend_y, "Bleed (0.125\")")
    
    c.setFillColor(GUIDE_GREEN)
    c.rect(legend_x + 160, legend_y, 8, 3, fill=1, stroke=0)
    c.setFillColor(DGRAY)
    c.drawString(legend_x + 172, legend_y, "Safe zone (0.25\")")
    
    c.setFillColor(GUIDE_PURPLE)
    c.rect(legend_x + 270, legend_y, 8, 3, fill=1, stroke=0)
    c.setFillColor(DGRAY)
    c.drawString(legend_x + 282, legend_y, "Spine center")
    
    c.save()
    print(f"Generated cover template: {output_path}")
    print(f"  {COVER_W / inch:.4f}\" × {COVER_H / inch:.2f}\" (with bleed)")
    print(f"  Spine: {SPINE / inch:.4f}\" ({SPINE * 300:.0f}px @300DPI)")
    return output_path


if __name__ == "__main__":
    output = os.path.join(OUTPUT_DIR, "cover-template.pdf")
    draw_cover_template(output)
