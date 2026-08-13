#!/usr/bin/env python3
"""
KDP Paperback Cover Template Generator
Generates correct cover templates with bleed for Amazon KDP.

Usage:
  python kdp_cover_template.py --interior 8.5x11 --pages 130 --output cover_template.pdf

KDP Requirements:
  - Bleed: 0.125" (3.2mm) on all outer edges
  - Spine: calculated from page count (white paper = 0.002252" per page)
  - Interior margins: 0.375" (9.52mm) for books with bleed
"""

import argparse
import math
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
import os

# KDP Specs
BLEED = 0.125 * inch  # 9 pts
PAGES_PER_INCH_WHITE = 1 / 0.002252  # ~444 pages per inch for white paper
PAGES_PER_INCH_CREAM = 1 / 0.002518  # ~397 pages per inch for cream paper

# Colors
TEMPLATE_BG = HexColor("#E8E8E8")  # Light gray for template
BLEED_ZONE = HexColor("#FFE0E0")   # Light red for bleed areas
SAFE_ZONE = HexColor("#E0FFE0")    # Light green for safe area
SPINE_COLOR = HexColor("#D0D0FF")  # Light blue for spine
GUIDE_COLOR = HexColor("#FF6666")  # Red for fold lines
TEXT_COLOR = HexColor("#333333")


def get_spine_width(pages, paper="white"):
    """Calculate spine width from page count."""
    if paper == "white":
        return pages / PAGES_PER_INCH_WHITE
    else:
        return pages / PAGES_PER_INCH_CREAM


def get_trim_size(interior_size):
    """Parse interior size string to (width, height) in inches."""
    parts = interior_size.lower().split("x")
    return float(parts[0]), float(parts[1])


def draw_cover_template(c, interior_w_in, interior_h_in, pages, paper="white", show_guides=True):
    """Draw a complete KDP cover template with bleed, trim, and safe zones.
    
    Args:
        interior_w_in: Interior width in INCHES (e.g., 8.5)
        interior_h_in: Interior height in INCHES (e.g., 11.0)
    """
    
    spine_in = get_spine_width(pages, paper)
    
    # Convert everything to POINTS for consistent calculations
    iw = interior_w_in * inch   # interior width in pts
    ih = interior_h_in * inch   # interior height in pts
    sp = spine_in * inch        # spine width in pts
    
    # Full cover dimensions (with bleed on all outer edges)
    cover_w = BLEED + iw + sp + iw + BLEED
    cover_h = BLEED + ih + BLEED
    
    # Set page size to match cover
    c.setPageSize((cover_w, cover_h))
    
    # Background
    c.setFillColor(TEMPLATE_BG)
    c.rect(0, 0, cover_w, cover_h, fill=1, stroke=0)
    
    if show_guides:
        # === BLEED ZONES (red-tinted) ===
        c.setFillColor(BLEED_ZONE)
        c.rect(0, 0, BLEED, cover_h, fill=1, stroke=0)           # Left
        c.rect(cover_w - BLEED, 0, BLEED, cover_h, fill=1, stroke=0)  # Right
        c.rect(0, cover_h - BLEED, cover_w, BLEED, fill=1, stroke=0)  # Top
        c.rect(0, 0, cover_w, BLEED, fill=1, stroke=0)           # Bottom
        
        # === TRIM BOX (the actual book size) ===
        c.setStrokeColor(GUIDE_COLOR)
        c.setLineWidth(2)
        c.setDash(6, 3)
        # Back cover trim
        c.rect(BLEED, BLEED, iw, ih, fill=0, stroke=1)
        # Front cover trim
        front_x = BLEED + iw + sp
        c.rect(front_x, BLEED, iw, ih, fill=0, stroke=1)
        c.setDash()
        
        # === SAFE ZONE (green-tinted, 0.375" inside trim) ===
        SAFE = 0.375 * inch
        c.setFillColor(SAFE_ZONE)
        c.rect(BLEED + SAFE, BLEED + SAFE, iw - 2*SAFE, ih - 2*SAFE, fill=1, stroke=0)
        c.rect(front_x + SAFE, BLEED + SAFE, iw - 2*SAFE, ih - 2*SAFE, fill=1, stroke=0)
        
        # === SPINE ===
        c.setFillColor(SPINE_COLOR)
        c.rect(BLEED + iw, BLEED, sp, ih, fill=1, stroke=0)
        
        # Spine text (if wide enough)
        if sp > 0.3 * inch:
            c.setFillColor(TEXT_COLOR)
            c.setFont("Helvetica-Bold", 8)
            c.saveState()
            c.translate(BLEED + iw + sp/2, BLEED + ih/2)
            c.rotate(90)
            c.drawCentredString(0, 0, "CHEMOTHERAPY TREATMENT JOURNAL")
            c.restoreState()
        
        # === FOLD LINES (dashed) ===
        c.setStrokeColor(GUIDE_COLOR)
        c.setLineWidth(1.5)
        c.setDash(4, 4)
        c.line(BLEED + iw, 0, BLEED + iw, cover_h)
        c.line(BLEED + iw + sp, 0, BLEED + iw + sp, cover_h)
        c.setDash()
        
        # === LABELS ===
        c.setFillColor(TEXT_COLOR)
        
        # Bleed dimension labels
        c.setFont("Helvetica", 6)
        c.drawCentredString(BLEED/2, cover_h/2, f"Bleed\n{BLEED/inch:.3f}\"")
        c.drawCentredString(cover_w - BLEED/2, cover_h/2, f"Bleed\n{BLEED/inch:.3f}\"")
        c.drawCentredString(cover_w/2, BLEED/2, f"Bleed: {BLEED/inch:.3f}\"")
        c.drawCentredString(cover_w/2, cover_h - BLEED/2, f"Bleed: {BLEED/inch:.3f}\"")
        
        # Trim size labels
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(BLEED + iw/2, BLEED + 10, f"Back Cover\n{interior_w_in}\" x {interior_h_in}\"")
        c.drawCentredString(front_x + iw/2, BLEED + 10, f"Front Cover\n{interior_w_in}\" x {interior_h_in}\"")
        
        # Spine label
        c.setFont("Helvetica", 7)
        c.drawCentredString(BLEED + iw + sp/2, BLEED + 10, f"Spine: {spine_in:.3f}\" ({pages} pages)")
        
        # Safe zone label
        c.setFont("Helvetica", 7)
        c.drawCentredString(front_x + iw/2, BLEED + ih - 15, "Safe Zone (0.375\" inside trim)")
        
        # Overall dimensions
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(cover_w/2, cover_h - 5, f"Full Cover: {cover_w/inch:.2f}\" x {cover_h/inch:.2f}\"")
        
        # Title placeholder on front cover
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(TEXT_COLOR)
        c.drawCentredString(front_x + iw/2, cover_h/2 + 20, "TITLE HERE")
        c.setFont("Helvetica", 10)
        c.drawCentredString(front_x + iw/2, cover_h/2 - 10, "Author Name")
        
        # Back cover placeholder
        c.setFont("Helvetica", 9)
        c.drawCentredString(BLEED + iw/2, cover_h/2, "Back cover content\n(barcode area, description, etc.)")
        
        # Barcode area (bottom right of back cover)
        barcode_w = 2 * inch
        barcode_h = 1.2 * inch
        c.setStrokeColor(TEXT_COLOR)
        c.setLineWidth(0.5)
        c.setDash(2, 2)
        c.rect(BLEED + iw - barcode_w - SAFE, BLEED + SAFE, barcode_w, barcode_h, fill=0, stroke=1)
        c.setDash()
        c.setFont("Helvetica", 7)
        c.drawCentredString(BLEED + iw - barcode_w/2 - SAFE, BLEED + SAFE + barcode_h/2, "ISBN Barcode\n(120 mil x 120 mil min)")
    
    return cover_w, cover_h


def main():
    parser = argparse.ArgumentParser(description="KDP Cover Template Generator")
    parser.add_argument("--interior", default="8.5x11", help="Interior trim size (e.g., 8.5x11)")
    parser.add_argument("--pages", type=int, default=130, help="Number of interior pages")
    parser.add_argument("--paper", default="white", choices=["white", "cream"], help="Paper type")
    parser.add_argument("--output", default="kdp_cover_template.pdf", help="Output PDF filename")
    parser.add_argument("--no-guides", action="store_true", help="Generate clean template without guide overlays")
    
    args = parser.parse_args()
    
    interior_w, interior_h = get_trim_size(args.interior)
    spine = get_spine_width(args.pages, args.paper)
    
    print(f"Interior: {interior_w}\" × {interior_h}\"")
    print(f"Pages: {args.pages}")
    print(f"Paper: {args.paper}")
    print(f"Spine: {spine:.4f}\" ({spine*25.4:.2f}mm)")
    print(f"Bleed: {BLEED/inch:.3f}\" on all sides")
    
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.output)
    c = canvas.Canvas(output_path)
    
    cover_w, cover_h = draw_cover_template(
        c, interior_w, interior_h, args.pages, args.paper, 
        show_guides=not args.no_guides
    )
    
    c.save()
    
    print(f"\nGenerated: {output_path}")
    print(f"Full cover: {cover_w/inch:.2f}\" × {cover_h/inch:.2f}\"")
    print(f"Full cover: {cover_w/inch*25.4:.1f}mm × {cover_h/inch*25.4:.1f}mm")
    print(f"\nKDP Upload Checklist:")
    print(f"  [OK] Cover includes 0.125\" bleed on all outer edges")
    print(f"  [OK] Spine width calculated for {args.pages} pages ({args.paper} paper)")
    print(f"  [OK] Safe zone marked (0.375\" inside trim)")
    print(f"  [OK] Barcode area reserved on back cover")


if __name__ == "__main__":
    main()
