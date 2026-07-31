#!/usr/bin/env python3
"""
Generate title page and copyright page PDFs for Affinity placement.
"""

import os
import sys

# Add the skills directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'skills', 'kdp-print'))

from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Georgia font family
pdfmetrics.registerFont(TTFont('Georgia', 'C:/Windows/Fonts/georgia.ttf'))
pdfmetrics.registerFont(TTFont('Georgia-Bold', 'C:/Windows/Fonts/georgiab.ttf'))
pdfmetrics.registerFont(TTFont('Georgia-Italic', 'C:/Windows/Fonts/georgiai.ttf'))

# Constants
TRIM_W = 6.0 * inch
TRIM_H = 9.0 * inch
NAVY = HexColor("#1B2A4A")
DGRAY = HexColor("#333333")
MGRAY = HexColor("#666666")
LGRAY = HexColor("#999999")

# Output directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'individual')


def generate_title_page():
    """Generate title page PDF."""
    filepath = os.path.join(OUTPUT_DIR, 'title-page.pdf')
    c = canvas.Canvas(filepath, pagesize=(TRIM_W, TRIM_H))
    
    lm = 0.5 * inch
    rm = 0.3 * inch
    uw = TRIM_W - lm - rm
    
    # Title
    y = TRIM_H * 0.65
    c.setFillColor(NAVY)
    c.setFont("Georgia-Bold", 28)
    c.drawCentredString(TRIM_W / 2, y, "NOTARY PUBLIC")
    y -= 36
    c.drawCentredString(TRIM_W / 2, y, "RECORD JOURNAL")
    
    # Accent line
    y -= 24
    c.setStrokeColor(HexColor("#BBBBBB"))
    c.setLineWidth(1)
    c.line(lm + uw * 0.25, y, lm + uw * 0.75, y)
    
    # Subtitle
    y -= 28
    c.setFillColor(MGRAY)
    c.setFont("Georgia-Italic", 12)
    c.drawCentredString(TRIM_W / 2, y, "Official Log of Notarial Acts")
    
    # Volume placeholder
    y -= 48
    c.setFillColor(DGRAY)
    c.setFont("Georgia", 11)
    c.drawString(lm + 80, y, "Volume")
    c.setStrokeColor(LGRAY)
    c.setLineWidth(0.5)
    c.line(lm + 126, y - 2, lm + 180, y - 2)
    c.drawString(lm + 190, y, "of")
    c.line(lm + 210, y - 2, lm + 264, y - 2)
    
    # Year placeholder
    y -= 32
    c.drawString(lm + 100, y, "Year:")
    c.line(lm + 142, y - 2, lm + 264, y - 2)
    
    c.save()
    return filepath


def generate_copyright_page():
    """Generate copyright/disclaimer page PDF."""
    filepath = os.path.join(OUTPUT_DIR, 'copyright-page.pdf')
    c = canvas.Canvas(filepath, pagesize=(TRIM_W, TRIM_H))
    
    lm = 0.5 * inch
    rm = 0.3 * inch
    uw = TRIM_W - lm - rm
    
    y = TRIM_H - 0.45 * inch - 20
    
    # Copyright notice
    c.setFillColor(MGRAY)
    c.setFont("Georgia", 8)
    c.drawString(lm, y, "Copyright \u00a9 2026 Meridian Press. All rights reserved.")
    y -= 20
    
    c.setFont("Georgia", 7.5)
    lines = [
        "No part of this publication may be reproduced, distributed, or transmitted",
        "in any form or by any means without prior written permission.",
        "",
        "This journal is designed for recording notarial acts. The publisher assumes",
        "no responsibility for errors, omissions, or damages arising from the use of",
        "this journal. Users should comply with their state's notarial requirements.",
        "",
        "Printed in the United States of America.",
        "",
        "Meridian Press",
        "El Bayadh, Algeria",
        "kaprikika8@gmail.com",
    ]
    for line in lines:
        c.drawString(lm, y, line)
        y -= 12
    
    # Disclaimer box
    y -= 20
    c.setStrokeColor(LGRAY)
    c.setLineWidth(0.5)
    box_h = 80
    c.rect(lm, y - box_h, uw, box_h, fill=0, stroke=1)
    
    c.setFillColor(MGRAY)
    c.setFont("Georgia-Bold", 7)
    c.drawString(lm + 8, y - 12, "DISCLAIMER")
    c.setFont("Georgia", 6.5)
    disclaimer_lines = [
        "This journal is provided as-is for recording notarial acts.",
        "It does not constitute legal advice. Users are responsible",
        "for ensuring compliance with all applicable state and federal",
        "notarial laws and regulations. The publisher makes no guarantees",
        "regarding the legal validity of entries made in this journal.",
    ]
    dy = y - 24
    for line in disclaimer_lines:
        c.drawString(lm + 8, dy, line)
        dy -= 10
    
    c.save()
    return filepath


def main():
    """Generate front matter PDFs."""
    print(f"Generating front matter PDFs in: {OUTPUT_DIR}")
    print("-" * 60)
    
    title_path = generate_title_page()
    size_kb = os.path.getsize(title_path) / 1024
    print(f"  title-page.pdf ({size_kb:.1f} KB)")
    
    copyright_path = generate_copyright_page()
    size_kb = os.path.getsize(copyright_path) / 1024
    print(f"  copyright-page.pdf ({size_kb:.1f} KB)")
    
    print("-" * 60)
    print("Generated 2 front matter PDFs")


if __name__ == '__main__':
    main()
