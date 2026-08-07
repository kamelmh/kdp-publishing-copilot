#!/usr/bin/env python3
"""
Generate all 110 individual entry PDFs for Affinity placement.
Each PDF is a single page with correct entry number and margins.
"""

import os
import sys

# Add the skills directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'skills', 'kdp-print'))

from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from entry_page import draw_entry_page, TRIM_W, TRIM_H

# Output directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'individual')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_entry_pdf(entry_no, phys_page, filename):
    """Generate a single entry PDF."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    c = canvas.Canvas(filepath, pagesize=(TRIM_W, TRIM_H))
    
    # Draw the entry page
    draw_entry_page(c, TRIM_W, TRIM_H, entry_no, phys_page)
    
    c.save()
    return filepath

def main():
    """Generate all 110 entry PDFs."""
    print(f"Generating 110 entry PDFs in: {OUTPUT_DIR}")
    print("-" * 60)
    
    generated = 0
    
    for entry_no in range(1, 111):  # Entry 001 to 110
        # Each entry gets TWO physical pages (recto + verso)
        # Entry 1 = pages 3,4 in the book
        # Entry 2 = pages 5,6 in the book
        # etc.
        
        # For Affinity placement, we generate ONE PDF per entry
        # The PDF will be placed on the appropriate page
        
        filename = f"entry-{entry_no:03d}.pdf"
        filepath = generate_entry_pdf(entry_no, entry_no, filename)
        
        size_kb = os.path.getsize(filepath) / 1024
        print(f"  [{entry_no:03d}] {filename} ({size_kb:.1f} KB)")
        generated += 1
    
    print("-" * 60)
    print(f"Generated {generated} entry PDFs")
    print(f"Location: {OUTPUT_DIR}")

if __name__ == '__main__':
    main()
