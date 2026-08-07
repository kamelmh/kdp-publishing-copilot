# KDP Notary Log Book — Complete Feed Loop

> **Purpose:** Paste this entire document into Claude Desktop → KDP Publishing project → Instructions. This is the single source of truth for building and publishing the Notary Log Book.

---

## ACCOUNT & IDENTITY

- **Publisher:** Oumkeltoum Djerjour
- **Email:** kaprikika8@gmail.com
- **KDP Account ID:** A2JDT3KR1A59T5
- **Tax Status:** W-8BEN signed, 30% US withholding (Algeria has NO US tax treaty)
- **Payment:** Check payments only (no bank account on file)
- **Author on Cover:** Oumkeltoum Djerjour
- **Contact:** kamelmahi71@gmail.com

---

## BOOK 1: SIMPLE NOTARY LOG BOOK

### Trim & Physical Specs

| Spec | Value | Notes |
|------|-------|-------|
| Trim Size | 6 × 9 inches | Most popular for journals |
| Page Count | 120 pages | Multiple of 2 ✓ |
| Paper | White | 0.002252" per page |
| Gutter Margin | 0.375 inches | For ≤150 pages |
| Outside Margin | 0.5 inches | Comfortable reading |
| Top/Bottom Margin | 0.5 inches | Comfortable reading |
| Bleed | 0.125 inches | Cover only — interior has NO bleed |
| Spine Width | 0.3302 inches | (120 × 0.002252) + 0.06 |
| Spine Pixels | 99 pixels @ 300 DPI | |
| Cover Total | 12.58 × 9.25 inches | (6×2) + 0.33 + (0.125×2) = 12.58 wide |
| Cover Pixels | 3774 × 2775 @ 300 DPI | |

### Interior Layout

**Page Structure:**
- Page 1: Title page ("Simple Notary Log Book")
- Page 2: Copyright & disclaimer page
- Pages 3-120: Notary record entries (2 per page = 236 total entries)

**Each Entry Contains:**
```
┌─────────────────────────────────────────────────────┐
│ NOTARY PUBLIC — RECORD OF NOTARIAL ACTS             │
│ Page X of 120                                       │
├─────────────────────────────────────────────────────┤
│ Date: _______________                               │
│ Notarial Act Type: _______________________________  │
│ Signer Name(s): __________________________________  │
│ ID Verified (Type/No.): __________________________  │
│ Document Description: ____________________________  │
│ Fee Charged: $_________                             │
│                                                     │
│ Notary Signature & Seal      Entry #___             │
└─────────────────────────────────────────────────────┘
```

**Notarial Act Types (for reference):**
1. Acknowledgment
2. Jurat
3. Oath or Affirmation
4. Copy Certification
5. Signature Witnessing
6. Proof of Execution
7. protests (less common)

**Entry Capacity:**
- 2 entries per page × 118 pages of entries = 236 entries
- Pages 1-2 are title/copyright (no entries)
- Total notarial acts recordable: 236

### Interior Design Rules

1. **Header:** Dark blue bar (#1a365d) with white text "NOTARY PUBLIC — RECORD OF NOTARIAL ACTS"
2. **Page numbers:** Top right corner, "Page X of 120"
3. **Field labels:** Bold, 6.5pt Helvetica
4. **Entry lines:** Light gray (#cbd5e0), 0.3pt weight
5. **Entry borders:** Light gray rectangle around each entry
6. **Signature area:** Bottom of entry with "Notary Signature & Seal" label
7. **Entry number:** Bottom right of each entry ("Entry #1", "Entry #2", etc.)
8. **Colors:** Professional blue (#1a365d), gray lines (#cbd5e0), black text
9. **Font:** Helvetica (clean, professional, KDP-compatible)
10. **No decorative elements** — clean, official, functional

### Cover Design Rules

**Front Cover:**
- Title: "Simple Notary Log Book" (large, bold)
- Subtitle: "Official Record of Notarial Acts" (smaller, below title)
- Design: Professional blue/gold theme
- Imagery: Scales of justice, notary seal, or quill pen (subtle, professional)
- Author: "Oumkeltoum Djerjour" (bottom)
- Color scheme: Dark blue (#1a365d) + Gold (#d4af37) + White

**Back Cover:**
- Brief description of features (3-4 bullet points)
- "120 entry pages for recording notarial acts"
- "Professional 6×9 inch format"
- "Perfect for Notary Publics, legal professionals, mobile notaries"
- Barcode area (KDP adds automatically)

**Spine:**
- Text: "Notary Log Book — Oumkeltoum Djerjour"
- Width: 0.33 inches (99 pixels @ 300 DPI)
- Color: Dark blue matching front

**Full Wrap Layout:**
```
┌──────────────────┬──────────┬──────────────────┐
│                  │  NOTARY  │                  │
│   BACK COVER     │   LOG    │  FRONT COVER     │
│                  │   BOOK   │                  │
│  (description)   │ (author) │  (main art)      │
│                  │          │                  │
└──────────────────┴──────────┴──────────────────┘
├──── 6" ──────────┤─ 0.33" ──┤──── 6" ─────────┤
├─ 0.125" bleed ───┤          ├── 0.125" bleed ──┤
Total: 12.58" wide × 9.25" tall
```

---

## KDP SPECIFICATIONS (LOCKED RULES)

### Trim Sizes Available
| Size | Use Case |
|------|----------|
| 5×8 | Small format |
| 5.06×7.81 | US Trade |
| 5.5×8.5 | Medium format |
| **6×9** | **Journals, log books (RECOMMENDED)** |
| 7×10 | Large format |
| 8.5×11 | Workbooks, planners |
| 4.75×6.75 | Pocket size |
| 8.25×8.25 | Square format |

### Margins (KDP Requirements)
- **Gutter (inside):**
  - 24-150 pages: 0.375"
  - 151-300 pages: 0.5"
  - 301-500 pages: 0.625"
  - 501+ pages: 0.75"
- **Outside:** 0.25" minimum (0.5" recommended)
- **Top/Bottom:** 0.25" minimum (0.5" recommended)

### Bleed Rules
- **Interior:** NO bleed needed (white borders are fine)
- **Cover:** MUST include 0.125" bleed on ALL sides
- Bleed is for artwork that extends to the edge of the page

### Spine Formula
```
spine_width = (page_count × paper_thickness) + 0.06" allowance

White paper: 0.002252" per page
Cream paper: 0.0025" per page

Example: 120 pages × 0.002252 + 0.06 = 0.3302"
```

### Resolution & Color
- Interior PDF: 300 DPI (vector text preferred)
- Cover: 300 DPI minimum
- Color space: RGB (KDP converts to CMYK automatically)
- PDF format: Print-ready, no password protection

### Page Count Rules
- Must be multiple of 2 (for cover wrap)
- Minimum: 24 pages (for perfect bound)
- Maximum: 828 pages

---

## METADATA & PUBLISHING

### Title & Subtitle
```
Title: Simple Notary Log Book
Subtitle: Official Record of Notarial Acts — 120 Pages for Recording Notarizations
```

### Book Description (HTML — paste into KDP)
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

### ISBN
- Use KDP-free ISBN (no cost)
- Or provide your own if you have one

---

## PRE-UPLOAD CHECKLIST

- [ ] Interior PDF: 120 pages, 6×9 inches, 300 DPI
- [ ] Interior has NO bleed marks or crop marks
- [ ] Cover PDF: Full wrap (front+spine+back), 300 DPI
- [ ] Cover has 0.125" bleed on all sides
- [ ] Cover spine width matches calculation (0.33")
- [ ] No blank pages at start or end
- [ ] All text readable at 100% zoom
- [ ] No "© Amazon" or "© KDP" on copyright page
- [ ] No "draft" or "sample" watermarks
- [ ] ISBN assigned (KDP-free or your own)
- [ ] All 7 keyword slots filled
- [ ] 2 BISAC categories selected
- [ ] Description formatted with HTML
- [ ] No external links in description
- [ ] Price set to $12.99, 40% royalty selected
- [ ] Previewer checked — no errors

---

## KDP UPLOAD STEPS

1. Go to **kdp.amazon.com**
2. Sign in with Oumkeltoum's account (kaprikika8@gmail.com)
3. Click **"Create"** → **"Paperback"**
4. Enter book details:
   - Language: English
   - Book Title: Simple Notary Log Book
   - Subtitle: Official Record of Notarial Acts — 120 Pages for Recording Notarizations
   - Author: Oumkeltoum Djerjour
   - Description: (paste HTML from above)
   - Publishing Rights: I own the copyright
   - Keywords: (paste all 7)
   - Categories: (select 2 BISAC codes)
5. Upload **interior PDF**
6. Upload **cover PDF**
7. Click "Upload your paperback cover file"
8. Use **KDP's ISBN** (free)
9. Set pricing:
   - List Price: $12.99
   - Royalty: 40%
   - Marketplaces: US (default)
10. Click **"Publish"**
11. Review takes **24-72 hours**

---

## CANVA GUIDE (If Designing Cover There)

### Front Cover Template
1. Open Canva → Create custom size
2. Enter: **1256 × 925 pixels** (12.56 × 9.25 inches @ 300 DPI)
3. Set bleed guides: **37.5 pixels** (0.125") from each edge
4. Safe area: Everything inside the bleed guides
5. Spine area: Center 99 pixels (0.33" wide)

### Design Elements
- Background: Dark blue (#1a365d) or gradient
- Title: White or gold (#d4af37), bold, large
- Subtitle: White, smaller
- Author: White, bottom
- Imagery: Scales of justice, seal, quill (subtle)

### Export Settings
1. File → Download → PDF Print
2. Color profile: RGB
3. Resolution: 300 DPI
4. Include bleed: Yes ✓
5. Crop marks and bleed: ON

---

## REVENUE PROJECTIONS

| Month | Sales | Revenue | Profit |
|-------|-------|---------|--------|
| Month 1 | 10 | $52.00 | $24.00 |
| Month 2 | 20 | $104.00 | $48.00 |
| Month 3 | 30 | $156.00 | $72.00 |
| Month 6 | 50 | $260.00 | $120.00 |
| Month 12 | 100 | $520.00 | $240.00 |

Break-even: ~15 sales/month covers basic expenses.

---

## FAST-FOLLOW BOOKS

### Book 2: Password Log Book
- Trim: 5.06×7.81 in | Pages: 100 | Spine: 0.29"
- Price: $9.99 | Royalty: $3.50
- Interior: Password entry fields (website, username, password, security Q, notes)
- Keywords: password log book, password organizer, internet login tracker

### Book 3: Running Log Book
- Trim: 6×9 in | Pages: 120 | Spine: 0.33"
- Price: $12.99 | Royalty: $5.20
- Interior: Running entries (date, distance, time, pace, weather, notes)
- Keywords: running log book, running journal, workout tracker

---

## MEMORY RULES

1. **Account details are LOCKED** — never change without user confirmation
2. **Book specs are LOCKED** — trim, pages, price stay consistent
3. **Canva has NO API** — provide dimensions and walkthrough, not integration
4. **KDP has NO API** — publishing is manual via kdp.amazon.com
5. **30% withholding** — Algeria has no US tax treaty, applies to all US sales
6. **Check payments only** — no bank account on file
7. **Interior has NO bleed** — only cover needs bleed
8. **Page count must be even** — multiple of 2 for cover wrap
9. **300 DPI minimum** — for all print-ready files
10. **RGB color** — KDP converts to CMYK automatically

---

## RESPONSE STYLE

When responding about this book:
- Concise, actionable, no filler
- Exact specifications with units
- Copy-paste ready text
- Checklist format for workflows
- Status indicators: ✅ done | ⏳ in progress | ❌ blocked

---

*Feed Loop v1.0 — KDP Publishing Copilot — Notary Log Book*
*Last Updated: 2026-07-28*
