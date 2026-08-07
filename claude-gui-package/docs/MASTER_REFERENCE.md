# KDP Publishing Copilot — Complete Reference

> **Purpose:** Master reference for building and publishing notary journals on Amazon KDP. HyperAgent reads this to learn the complete workflow.

---

## ACCOUNT INFORMATION

| Field | Value |
|-------|-------|
| Publisher | Oumkeltoum Djerjour |
| Email | kaprikika8@gmail.com |
| Account ID | A2JDT3KR1A59T5 |
| Tax Status | W-8BEN signed, 30% US withholding |
| Payment | Check payments only |
| Contact | kamelmahi71@gmail.com |

---

## KDP SPECIFICATIONS (LOCKED RULES)

### Trim Sizes
| Size | Use Case |
|------|----------|
| 5×8 | Small format |
| 5.06×7.81 | US Trade |
| 5.5×8.5 | Medium format |
| **6×9** | **Journals, log books (RECOMMENDED)** |
| 7×10 | Large format |
| 8.5×11 | Workbooks, planners |
| 4.75×6.75 | Pocket size |

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
- Minimum: 24 pages
- Maximum: 828 pages

---

## NOTARY JOURNAL DESIGN SPECIFICATIONS

### Document Specs
| Property | Value |
|----------|-------|
| Trim size | 6" × 9" (default) or 5.5" × 8.5" (compact) |
| Page size in points | 432 × 648 pt (6×9) or 396 × 612 pt (5.5×8.5) |
| Inner (gutter) margin | 0.5" = 36 pt (KDP min 0.375" at 120pp) |
| Outer margin | 0.375" = 27 pt |
| Top/Bottom margin | 0.5" = 36 pt |
| Line spacing (write-in) | 0.27" ≈ 19.4 pt |
| Thumbprint box | Minimum 72 × 72 pt (1" × 1"), placed on outer edge |
| Font | Helvetica / Helvetica-Bold (built-in ReportLab) |
| Section border weight | 0.75 pt – 1 pt |
| Divider line weight | 0.5 pt |
| Border color | Dark gray: RGB(51, 51, 51) — 80% black |
| Background | White |

### Color Palette
```python
NAVY  = (0.106, 0.165, 0.290)  # Header bars
STEEL = (0.227, 0.353, 0.549)  # Section bars
DGRAY = (0.200, 0.200, 0.200)  # Borders, lines
LGRAY = (0.800, 0.800, 0.800)  # Light lines
```

### Journal Structure

#### 1. Cover Page
- Title: **"Notary Public Record Journal"**
- Subtitle: *Official Log of Notarial Acts*
- Office name, Notary's full name, Commission number
- State / jurisdiction, Year
- "Volume _____ of _____" line
- Official seal placeholder: dashed circle (50 pt radius)
- Bottom disclaimer bar

#### 2. Instructions Page (Page 2)
- How to use the journal
- Sequential numbering requirement (tamper prevention)
- What to do when journal is full
- Storage and retention note

#### 3. Entry Pages (one per notarial act, pre-numbered)

**HEADER BAR (navy #1B2A4A, white text):**
```
NOTARIAL ACT RECORD                              Entry No. [XXX]
```

**SECTION A — Date & Time:**
```
Date: ________________________   Time: __________  [ ] AM  [ ] PM
```

**SECTION B — Type of Notarial Act:**
```
[ ] Acknowledgment    [ ] Oath / Affirmation    [ ] Copy Certification
[ ] Signature Witnessing    [ ] Jurat    [ ] Other: ___________________
```

**SECTION C — Document Information:**
```
Document Type: ___________________________________________________
Document Date: ___________________________
Number of Pages: _________________
Description / Title: ______________________________________________
```

**SECTION D — Signer Information:**
```
Full Name: _______________________________________________________
Address: ________________________________________________________
Phone / Email (optional): _________________________________________
ID Type:  [ ] Driver's License   [ ] Passport   [ ] State ID   [ ] Other: _______
ID Number: _________________________   Issued by: ________________
Expiration Date: _________________
Signer's Signature: _________________________________  Date: _______
```

**SECTION E — Witness Information:**
```
Witness Name: ___________________________________________________
ID Number: ______________________   Signature: ___________________
```

**SECTION F — Thumbprint:**
- Placed on **outer edge** of page (away from gutter/spine)
- Minimum 1" × 1" (72 × 72 pt) box
- Label: *"Signer's Right Thumbprint"*

**SECTION G — Fees:**
```
Fee Charged: $_______________
Payment:  [ ] Cash   [ ] Check   [ ] Electronic Transfer   [ ] Waived
Check / Reference #: ___________________
```

**SECTION H — Notary Certification & Signature Block:**
```
I certify that the signer personally appeared before me on the date stated above.

Notary Name: ____________________________________________________
Commission #: ___________________   Expiration: __________________
State of: ______________________   County of: ____________________
Notary Signature: ________________________________  Date: _________

               [  OFFICIAL SEAL  ]   ← dashed circle, 36 pt radius
```

**SECTION I — Remarks:**
- Three blank write-in lines for notes

#### 4. Summary / Index Page (back of journal)

| Entry # | Date | Signer Name | Document Type | Act Type | Fee |
|---------|------|-------------|---------------|----------|-----|
| 001 | | | | | |
| 002 | | | | | |

- One pre-numbered row per entry
- Row height ≥ 0.27" for legible writing
- Spans 2–4 pages for 110 entries

---

## COVER DESIGN RULES

### Full Wrap Layout
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

### Front Cover (Official = Green/Gold)
- Title: "Notary Public Record Journal" (large, bold)
- Subtitle: "Official Log of Notarial Acts"
- Design: Professional green/gold theme (Meridian Press)
- Imagery: Notary seal with scales of justice (vector emblem)
- Byline: "Meridian Press" (bottom)
- Color scheme: Deep green + Gold + White

### Back Cover
- Brief description (3-4 bullet points)
- "110 pre-numbered entry pages for recording notarial acts"
- "Professional 6×9 inch portable format"
- "Perfect for Notary Publics, legal professionals, mobile notaries"
- Barcode area (KDP adds automatically)

### Spine
- Text: "NOTARY PUBLIC RECORD JOURNAL"
- Width: 0.33 inches (99 pixels @ 300 DPI)
- Color: Deep green matching front

---

## METADATA & PUBLISHING

### Title & Subtitle
```
Title: Notary Public Record Journal
Subtitle: Official Log of Notarial Acts — 110 Pre-Numbered Entry Pages
```

### Book Description (HTML)
```html
<b>Notary Public Record Journal</b> is a professional record-keeping journal designed for Notary Publics to document every notarial act performed.

Each entry page includes fields for:
<ul>
<li><b>Date & Time</b> of the notarial act</li>
<li><b>Notarial Act Type</b> (acknowledgment, jurat, oath, affirmation, copy certification)</li>
<li><b>Signer Name(s)</b> and signature line</li>
<li><b>ID Verification</b> (type of ID, ID number, expiration)</li>
<li><b>Document Description</b> being notarized</li>
<li><b>Fee Charged</b> for the notarial act</li>
<li><b>Thumbprint Box</b> for signer's right thumbprint</li>
<li><b>Notary Signature & Seal</b> area</li>
</ul>

<b>Features:</b>
<ul>
<li>110 pre-numbered entry pages (sequential numbering for tamper prevention)</li>
<li>One complete notarial act per page for thorough documentation</li>
<li>6×9 inch portable format — fits in a briefcase or desk drawer</li>
<li>Clean, professional layout with clear headers</li>
<li>Summary index at the back for quick reference</li>
<li>Heavy-duty matte cover for daily use</li>
</ul>

<b>Perfect for:</b> Notary Publics, legal professionals, mobile notaries, real estate closings, loan signing agents, and anyone needing to maintain official notarial records.

<b>Note:</b> This log book meets record-keeping requirements for most US states. Check your state's specific notary journal requirements for compliance.
```

### Keywords (7 slots — optimized for Amazon search + hidden category triggers)
```
1. notary journal official log notarial acts records
2. notary log book sequential numbered entries tamper
3. notary public record book professional accessories
4. real estate closing document loan signing agent
5. mobile notary supplies bag stamp seal equipment
6. compact travel pocket small desk notary book
7. updated 2026 guidelines state compliant rules
```

**Keyword Strategy:**
- Slots 1-3: Primary search terms (exact match for "notary journal", "notary log book", "notary record book")
- Slot 4: Buyer intent — real estate closings (high-value audience)
- Slot 5: Buyer intent — mobile notary supplies (triggers "office supplies" hidden category)
- Slot 6: Format/size — triggers "compact" and "travel" browse nodes
- Slot 7: Timeliness + compliance — "updated 2026" signals current edition

### Categories (3 Amazon Store Categories — not BISAC)

Since 2023, KDP uses Amazon's own category system. You select 3 categories from Amazon's store tree. BISAC codes are now derived automatically.

**Slot 1 (Primary — most specific):**
```
Books > Law > Notarial Practice
```
*If "Notarial Practice" isn't visible, search for it in the category picker. This is the most specific niche — low competition, high relevance.*

**Slot 2 (Secondary — broader professional):**
```
Books > Reference > Handbooks & Manuals
```
*Broader reach — positions the book as a professional reference, not just a notary item.*

**Slot 3 (Tertiary — business/office):**
```
Books > Business & Money > Office Management
```
*Triggers office/business audience — mobile notaries, real estate offices, law firms.*

**Alternative categories (if primary slots unavailable):**
- Books > Law > Legal Profession
- Books > Business & Money > Industries > Real Estate
- Books > Self-Help > Personal Growth > Journaling

**Hidden categories triggered by keywords:**
- "notary journal" → Notary Supplies (Office Products)
- "real estate closing" → Real Estate (Business & Money)
- "loan signing agent" → Loan Signing (Law)
- "compact travel" → Travel Accessories (Travel)

### Pricing (Corrected)
```
List Price: $12.99
Royalty: 60% Amazon = $5.35 per sale
Printing Cost: ~$2.44 (120 pages, 6×9, white paper)
Net Profit: ~$5.35 per Amazon sale
Expanded Distribution: 40% = $2.76 per sale
```

---

## KDP BACKEND KEYWORDS (copy-paste ready, 50 chars max each)

**Slot 1:**
```
notary journal official log notarial acts records
```

**Slot 2:**
```
notary log book sequential numbered entries tamper
```

**Slot 3:**
```
notary public record book professional accessories
```

**Slot 4:**
```
real estate closing document loan signing agent
```

**Slot 5:**
```
mobile notary supplies bag stamp seal equipment
```

**Slot 6:**
```
compact travel pocket small desk notary book
```

**Slot 7:**
```
updated 2026 guidelines state compliant rules
```

### Why These Keywords Work

| Slot | Purpose | Triggers |
|------|---------|----------|
| 1 | Exact match "notary journal" | Notary Supplies browse node |
| 2 | Exact match "notary log book" | Log Books browse node |
| 3 | Exact match "notary record book" | Record Keeping browse node |
| 4 | Buyer intent — real estate | Real Estate, Loan Signing nodes |
| 5 | Buyer intent — mobile notary | Office Supplies, Notary Equipment |
| 6 | Format/size modifier | Compact, Travel, Portable nodes |
| 7 | Timeliness + compliance | Updated 2026, State Rules nodes |

### Amazon's Keyword Rules (2026)
- Each slot: phrase up to **50 characters**
- **No** punctuation, symbols, or capitalization needed
- **Don't** repeat words across slots (wastes characters)
- **Do** use natural buyer language
- **Do** include location terms (state names) if relevant
- **Do** include "gifts for" variants if applicable

### Low-Content Book Checkbox (KDP Form)

The form asks: *"Does this book classify as any of these types?"*

**Check:** ✅ Low-content book (e.g., journals, notebooks, and planners)

**Why:** Our notary journal IS low-content — the buyer writes in it. Checking this:
- Correctly classifies the book
- Prevents Amazon from flagging it as misategorized
- May limit some category options (trade-off for accuracy)

**Do NOT check:** ❌ Large-print book (our font is standard size)

---

## CANVA GUIDE (If Rebuilding Cover)

### Full Wrap Canvas (Corrected — 300 DPI)
1. Open Canva → Create custom size
2. Enter: **3774 × 2775 pixels** (= 12.58 × 9.25 in @ 300 DPI)
3. Set bleed guides: **37.5 pixels** (0.125") from each edge
4. Spine: Center strip **99 pixels** wide (0.3302 in)
5. Panels: back = left 1837 px, spine = center 99 px, front = right 1837 px

### Design Elements
- Background: Deep green (official) or dark blue
- Title: White or gold, bold, large
- Subtitle: White, smaller
- Byline: "Meridian Press" (NOT author name)
- Imagery: Notary seal with scales of justice (vector emblem)

### Export Settings
- File → Download → PDF Print
- Include bleed: ✅
- Color: RGB (KDP converts to CMYK)
- Quality: 300 DPI

### Export Settings
1. File → Download → PDF Print
2. Color profile: RGB
3. Resolution: 300 DPI
4. Include bleed: Yes ✓
5. Crop marks and bleed: ON

---

## PRE-UPLOAD CHECKLIST

- [ ] Interior PDF: 120 pages, 6×9 inches, 300 DPI
- [ ] Interior has NO bleed marks or crop marks
- [ ] Cover PDF: Full wrap (front+spine+back), 300 DPI
- [ ] Cover has 0.125" bleed on all sides
- [ ] Cover spine width matches calculation (0.33")
- [ ] All text readable at 100% zoom
- [ ] No "© Amazon" or "© KDP" on copyright page
- [ ] No "draft" or "sample" watermarks
- [ ] ISBN assigned (KDP-free or your own)
- [ ] All 7 keyword slots filled
- [ ] 2 BISAC categories selected
- [ ] Description formatted with HTML
- [ ] No external links in description
- [ ] Price set to $12.99, 60% royalty selected
- [ ] Previewer checked — no errors

---

## KDP UPLOAD STEPS

1. Go to **kdp.amazon.com**
2. Sign in with Oumkeltoum's account (kaprikika8@gmail.com)
3. Click **"Create"** → **"Paperback"**
4. Enter book details:
   - Language: English
   - Book Title: Notary Public Record Journal
   - Subtitle: Official Log of Notarial Acts — 110 Pre-Numbered Entry Pages
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

## REVENUE PROJECTIONS (Corrected: $5.35 net per Amazon sale)

| Month | Sales | Revenue | Profit |
|-------|-------|---------|--------|
| Month 1 | 10 | $129.90 | $53.50 |
| Month 2 | 20 | $259.80 | $107.00 |
| Month 3 | 30 | $389.70 | $160.50 |
| Month 6 | 50 | $649.50 | $267.50 |
| Month 12 | 100 | $1,299.00 | $535.00 |

Break-even: ~5 sales/month covers basic expenses.

---

## PUBLISHING STRATEGY

### Series vs Standalone Decision

**Verdict: STANDALONE — each book is a separate product in a different niche.**

KDP "series" means sequential fiction (Book 1 → Book 2 → Book 3 of the same story). Our books are unrelated professional logbooks — Amazon's algorithm won't link them as a series. Instead, use **catalog depth**: dominate one niche with multiple related titles.

### 2026 KDP Strategy (Research-Backed)

| Old Way (Dead) | New Way (Works) |
|---|---|
| Publish in many random niches | Dominate one niche deeply |
| Scatter approach | Build topical authority |
| Unrelated books | Related product lines |
| 1 book = try and see | 5-10 books minimum per niche |
| Price doesn't matter | Price affects ranking + conversion |

**Minimum serious approach:** 5-10 books per niche. Amazon rewards catalogs of related books over random standalone titles.

### Niche Expansion Plan

**NICHE 1: Notary/Professional (validate first)**
| Priority | Book | Status |
|---|---|---|
| 1 | Notary Public Record Journal (6×9, 110 entries) | ⏳ Publishing now |
| 2 | Notary Receipt & Fee Log | 🔲 Design |
| 3 | Notary Appointment Scheduler | 🔲 Design |
| 4 | Notary Journal — Compact (5.5×8.5) | 🔲 Design |
| 5 | Notary Journal — Large Print (8.5×11) | 🔲 Design |
| 6 | Notary Public Starter Kit (bundled) | 🔲 Future |

**NICHE 2: Personal Security (separate line)**
| Priority | Book | Status |
|---|---|---|
| 1 | Password Log Book (5.06×7.81) | 🔲 Book 2 |
| 2 | Password Log — Travel Size | 🔲 Future |
| 3 | Family Password Organizer | 🔲 Future |

**NICHE 3: Fitness (separate line)**
| Priority | Book | Status |
|---|---|---|
| 1 | Running Log Book (6×9) | 🔲 Book 3 |
| 2 | Marathon Training Journal | 🔲 Future |
| 3 | Race Results Tracker | 🔲 Future |

### Validation-First Approach

1. **Publish Book 1 (Notary Journal)** — standalone, $12.99, green cover
2. **Wait 30-60 days** — track sales, BSR, reviews
3. **If BSR < 100,000 within 30 days** → expand notary line immediately
4. **If BSR 100,000-500,000** → still viable, expand slowly
5. **If BSR > 500,000 after 90 days** → pivot niche or revise cover/description

### Cross-Promotion (Within Each Niche)

In each book's description, add:
```html
<b>Also from Meridian Press:</b>
<ul>
<li>Notary Receipt & Fee Log — track fees and expenses</li>
<li>Notary Appointment Scheduler — manage your signing calendar</li>
</ul>
```

### Branded Line (Future)

After 3+ notary books, create **"Meridian Press Professional Logs"** branded line:
- Consistent cover design (green/gold theme)
- Unified back-matter cross-promotion
- Amazon "Also Bought" algorithm links related titles

---

## FAST-FOLLOW BOOKS (After Book 1 Validation)

### Book 2: Password Log Book
- Trim: 5.06×7.81 in | Pages: 120 | Spine: 0.33"
- Price: $9.99 | Royalty: $3.55 (60% of $9.99 − $2.44)
- Interior: Password entry fields (website, username, password, security Q, notes)
- Keywords: password log book, password organizer, internet login tracker
- **Note:** Different niche — publish as standalone, not series

### Book 3: Running Log Book
- Trim: 6×9 in | Pages: 120 | Spine: 0.33"
- Price: $12.99 | Royalty: $5.35 (60% of $12.99 − $2.44)
- Interior: Running entries (date, distance, time, pace, weather, notes)
- Keywords: running log book, running journal, workout tracker
- **Note:** Different niche — publish as standalone, not series

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

*Complete Reference v2.1 — KDP Publishing Copilot*
*Last Updated: 2026-07-28*
*Strategy: Standalone per niche, catalog depth, validation-first*
