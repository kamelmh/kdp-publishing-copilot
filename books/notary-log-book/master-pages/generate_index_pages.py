#!/usr/bin/env python3
"""
Generate 4 index PDFs with correct entry ranges for Affinity placement.
Index 1: entries 001-028
Index 2: entries 029-056
Index 3: entries 057-084
Index 4: entries 085-110
"""

import os
import sys

# Add the skills directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'skills', 'kdp-print'))

from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from entry_page import draw_index_page_aff, TRIM_W, TRIM_H

# Output directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'individual')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_index_pdf(start_entry, last_entry, filename):
    """Generate a single index PDF."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    c = canvas.Canvas(filepath, pagesize=(TRIM_W, TRIM_H))
    
    # Calculate rows needed
    rows = last_entry - start_entry + 1
    
    # Draw the index page
    draw_index_page_aff(c, TRIM_W, TRIM_H, start_entry=start_entry, rows=rows, last_entry=last_entry)
    
    c.save()
    return filepath

def main():
    """Generate all 4 index PDFs."""
    print(f"Generating 4 index PDFs in: {OUTPUT_DIR}")
    print("-" * 60)
    
    # Index page ranges
    index_pages = [
        (1, 28, "index-001-028.pdf"),
        (29, 56, "index-029-056.pdf"),
        (57, 84, "index-057-084.pdf"),
        (85, 110, "index-085-110.pdf"),
    ]
    
    for start, last, filename in index_pages:
        filepath = generate_index_pdf(start, last, filename)
        size_kb = os.path.getsize(filepath) / 1024
        print(f"  {filename}: entries {start:03d}-{last:03d} ({size_kb:.1f} KB)")
    
    print("-" * 60)
    print("Generated 4 index PDFs")
    print(f"Location: {OUTPUT_DIR}")

if __name__ == '__main__':
    main()
