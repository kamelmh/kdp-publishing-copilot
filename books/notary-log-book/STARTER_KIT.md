# Book 1: Simple Notary Log Book — Starter Kit

## Quick Start

```bash
# 1. Calculate specs
python skills/kdp-print/kdp_print.py specs --size 6x9 --pages 120

# 2. Generate interior
python skills/kdp-print/kdp_print.py interior --type notary --size 6x9 --pages 120 --output books/notary-log-book/interior.pdf

# 3. Build cover (after designing front/back images)
python skills/kdp-print/kdp_print.py cover --front books/notary-log-book/cover-front.png --back books/notary-log-book/cover-back.png --size 6x9 --pages 120 --output books/notary-log-book/cover-wrap.pdf
```

## Book Specifications

| Field | Value |
|-------|-------|
| **Title** | Simple Notary Log Book: Official Record of Notarial Acts |
| **Subtitle** | 120 Pages for Recording Notarizations |
| **Trim Size** | 6 × 9 inches |
| **Page Count** | 120 pages |
| **Paper** | White (0.002252" per page) |
| **Spine Width** | 0.33 inches (120 × 0.002252 + 0.06) |
| **Cover Size** | 12.56 × 9.25 inches (with bleed) |
| **Interior** | Notary record entries |
| **Price** | $12.99 |
| **Royalty (40%)** | $4.50 per sale |

## KDP Metadata

### Title & Subtitle
```
Title: Simple Notary Log Book
Subtitle: Official Record of Notarial Acts — 120 Pages for Recording Notarizations
```

### Book Description (HTML)
```html
<b>Simple Notary Log Book</b> is a professional record-keeping journal designed for Notary Publics to document every notarial act performed.

Each entry page includes fields for:
<ul>
<li><b>Date & Time</b> of the notarial act</li>
<li><b>Notarial Act Type</b> (acknowledgment, jurat, oath, affirmation, copy certification)</li>
<li><b>Signer Name(s)</b> and signature line</li>
<li><b>ID Verification</b> (type of ID, ID number, expiration)</li>
<li><b>Document Description</b> being notarized</li>
<li><b>Fee Charged</b> for the notarial act</li>
<li><b>Notary Signature & Seal</b> area</li>
</ul>

<b>Features:</b>
<ul>
<li>120 entry pages (2 entries per page = 240 total notarial acts)</li>
<li>6×9 inch portable format — fits in a briefcase or desk drawer</li>
<li>Clean, professional layout with clear headers</li>
<li>Page numbers on every page for easy reference</li>
<li>Heavy-duty matte cover for daily use</li>
</ul>

<b>Perfect for:</b> Notary Publics, legal professionals, mobile notaries, real estate closings, loan signing agents, and anyone needing to maintain official notarial records.

<b>Note:</b> This log book meets record-keeping requirements for most US states. Check your state's specific notary journal requirements for compliance.
```

### Keywords (7 slots)
```
1. notary journal
2. notary log book
3. notary public record
4. notarial acts
5. notary book
6. notary stamp log
7. notary public journal
```

### Categories (BISAC)
```
1. LAW / Notarial Practice
2. REFERENCE / General
3. BUSINESS & ECONOMICS / Personal Finance / General
```

### Pricing
```
List Price: $12.99
Royalty: 40% = $5.20 per sale
Printing Cost: ~$2.80 (120 pages, 6×9, white paper)
Net Profit: ~$2.40 per sale
```

## Interior Layout

### Entry Form Fields
```
┌─────────────────────────────────────────────┐
│ NOTARY PUBLIC — RECORD OF NOTARIAL ACTS     │
├─────────────────────────────────────────────┤
│ Date: _____________                         │
│ Notarial Act Type: _______________________  │
│ Signer Name(s): __________________________  │
│ ID Verified (Type/No.): __________________  │
│ Document Description: ____________________  │
│ Fee Charged: $________                       │
│                                             │
│ Notary Signature & Seal    Entry #___       │
└─────────────────────────────────────────────┘
```

### Page Structure
- **Pages 1-2:** Title page, copyright, instructions
- **Pages 3-120:** Notary record entries (2 per page = 236 entries)
- **Total capacity:** 236 notarial acts recorded

## Cover Design

### Front Cover Elements
- Title: "Simple Notary Log Book"
- Subtitle: "Official Record of Notarial Acts"
- Design: Professional blue/gold theme, scales of justice or seal icon
- Author: Oumkeltoum Djerjour

### Back Cover Elements
- Brief description of features
- Bullet points of what's included
- Barcode area (KDP adds this automatically)
- "Made in USA" or "Printed in USA" (optional)

### Spine
- Title: "Notary Log Book"
- Author: "Oumkeltoum Djerjour"
- Width: 0.33 inches

## Canva Setup Guide

### Front Cover Template
1. Create custom size: **1256 × 925 pixels** (12.56 × 9.25 inches @ 300 DPI)
2. Set bleed guides: **37.5 pixels** (0.125 inches) on all sides
3. Safe area: Inside the bleed guides
4. Spine area: Center 99 pixels (0.33 inches wide)

### Export Settings
1. File → Download → PDF Print
2. Color profile: RGB (KDP converts to CMYK)
3. Resolution: 300 DPI
4. Include bleed: Yes
5. Marks and bleed: Trim marks ON

## Pre-Upload Checklist

- [ ] Interior PDF: 300 DPI, correct trim size, no bleed marks
- [ ] Cover PDF: Full wrap (front+spine+back), 300 DPI, 0.125" bleed
- [ ] Page count: 120 pages (must be multiple of 2 for cover wrap)
- [ ] No blank pages at start/end (unless intentional)
- [ ] Text is readable at 100% zoom
- [ ] No copyright page claiming © Amazon or KDP
- [ ] No "draft" or "sample" watermarks
- [ ] ISBN: Use KDP-free ISBN or your own
- [ ] Keywords: All 7 slots filled
- [ ] Categories: 2 BISAC codes selected
- [ ] Description: HTML formatted, no external links
- [ ] Pricing: $12.99 set, 40% royalty selected

## KDP Upload Steps

1. Go to [kdp.amazon.com](https://kdp.amazon.com)
2. Sign in with Oumkeltoum's account (kaprikika8@gmail.com)
3. Click "Create" → "Paperback"
4. Enter book details (title, subtitle, author, description)
5. Upload interior PDF
6. Upload cover PDF
7. Use KDP's ISBN (free) or enter your own
8. Set pricing: $12.99, 40% royalty
9. Click "Publish" (review takes 24-72 hours)
