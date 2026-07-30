# HyperAgent Master Prompt — KDP Notary Interior Templates

## Context

We are building **print-ready Amazon KDP paperback interiors** for a Notary Public Record Journal. The project uses a **section-by-section approach** — each section of the interior gets its own standalone Affinity Publisher template (.afpub) with consistent styling and logic.

We have already completed the **entry page template** and refined it through multiple iterations. Now we need templates for the remaining sections.

## What We Built (Entry Pages)

The entry page (`entry_page.py`) is the **single source of truth** for layout. Key design decisions:

### Design Tokens
```python
# Colors (POD-safe, all tints ≥12% for B&W reproduction)
BAR_COLOR = "#DCDCDC"        # ~14% grey — section bars
BAR_TEXT_COLOR = "#333333"   # Dark grey text on bars
HEADER_BG = "#C8C8C8"       # ~21% grey — header bar
ACCENT_LINE = "#BBBBBB"     # ~29% grey — writing lines
DGRAY = "#333333"           # Primary text
MGRAY = "#666666"           # Secondary text
LGRAY = "#999999"           # Light accents
NAVY = "#1B2A4A"            # Navy — cover, instructions, index headers
STEEL = "#3A5A8C"           # Steel blue — secondary navy elements

# Spacing
RH = 16        # row height
BAR_H = 13     # section bar height
BAR_GAP = 13   # gap between section bar and its content
SEC_GAP = 6    # gap between sections

# KDP Spec
TRIM_W = 6.0 * inch
TRIM_H = 9.0 * inch
GUTTER = 0.5 * inch    # inside margin (binding edge)
OUTER = 0.3 * inch     # outside margin
TOP_MARGIN = 0.45 * inch
BOTTOM_MARGIN = 0.375 * inch
FOOTER_BASELINE = 21
FOOTER_GUARD = 36
```

### Typography
- **Font:** Georgia (registered from TTF: `C:/Windows/Fonts/georgia.ttf`)
- **Georgia-Bold** — section headers, bar text, entry header
- **Georgia** — body text, labels, field names
- **Georgia-Italic** — certification text ("I certify that...")

### Layout Rules
1. **No page numbers** — Affinity handles pagination
2. **No remarks section** — removed for cleaner layout
3. **2 witnesses** — expanded section E with Witness 1 + Witness 2
4. **Official seal** — r=32, positioned to the right of signature lines
5. **Bar-to-content gap** — 13pt minimum
6. **Section-to-section gap** — 6pt minimum
7. **All decorative bars INSET** — never edge-to-edge (no-bleed safe)
8. **Footer guard** — nothing bottom-anchored below y=36pt from bottom

### Sections (Entry Page)
- Header bar: "NOTARIAL ACT RECORD" + "Entry No. XXX"
- A — Date & Time
- B — Type of Notarial Act (checkboxes)
- C — Document Information
- D — Signer Information
- E — Witness (2 witnesses, name + signature each)
- F — Thumbprint (1×1" box on outer edge)
- G — Fees (checkboxes: Cash/Check/Elec./Waived)
- H — Notary Certification & Signature (seal + 3 fields)

## What We Need Now

Create **4 more Affinity Publisher templates** matching the entry page's visual language:

### 1. Cover Page Template (`cover-template.afpub`)
- Full-bleed navy header bar (inset from trim)
- Title: "NOTARY PUBLIC RECORD JOURNAL" (Georgia-Bold, 22pt)
- Subtitle: "Official Log of Notarial Acts" (Georgia-Italic, 11pt)
- Official seal (r=48, dashed circle)
- Fields: Notary's Full Name, Commission Number, State/Jurisdiction, Office/Employer, Commission Expires
- Volume line: "Volume _______ of _______" + "Year: __________"
- Disclaimer bar at bottom (navy background, white italic text)
- **No page number**

### 2. Instructions Page Template (`instructions-template.afpub`)
- Navy header bar: "How to Use This Journal" (Georgia-Bold, 14pt)
- 6 instruction items with bold head + body text (Georgia, 9.5pt)
- Two reference boxes anchored from footer guard:
  - "TYPICAL FEE SCHEDULE (US)" — 6 fee acts with price ranges
  - "STATE-SPECIFIC REQUIREMENTS" — 6 states with rules
- Boxes: light blue fill `#EDF2F8`, navy border, navy bold headers
- **No page number**

### 3. Index Page Template (`index-template.afpub`)
- Navy header bar: "JOURNAL INDEX / SUMMARY" (Georgia-Bold, 13pt)
- 6-column table: No. | Date | Signer Name | Doc Type | Act Type | Fee
- Column offsets: 0, 0.45, 1.30, 2.65, 3.65, 4.65 inches
- Steel blue headers, ruled lines between rows
- 28 entries per page
- **No page number**

### 4. Notes Page Template (`notes-template.afpub`)
- Navy header bar: "NOTES / ADDITIONAL RECORDS" (Georgia-Bold, 12pt)
- Lined writing area (0.32" between lines)
- **No page number**

## Deliverables

For each template, provide:
1. The Affinity Publisher .afpub file
2. A Python function that generates the PDF version (for verification)
3. A rendered PNG preview

## Constraints

- **KDP no-bleed interior** — all elements inset ≥0.25" from trim
- **Georgia font family only** — no Helvetica, no Times
- **POD-safe tints** — all greys ≥12% for B&W reproduction
- **Navy `#1B2A4A`** for header bars (not grey — grey is for entry page section bars only)
- **Mirrored margins** — gutter always on binding edge (odd=LEFT, even=RIGHT)
- **6×9 inch trim** — all templates must match this size exactly

## Files Included

- `entry_page.py` — Single source of truth for entry page layout (reference for style)
- `kdp_print.py` — Production generator (shows how all pages fit together)
- `SKILL.md` — KDP Print skill documentation
- `master-recto.pdf` — Right-hand entry page template (page 3)
- `master-verso.pdf` — Left-hand entry page template (page 4)
- `master-recto-v9.png` — Rendered preview of final entry page
- `interior.pdf` — Full 120-page interior (for reference)
- `cover-wrap-green.pdf` — Cover wrap (for reference)

## Question

Review the entry page design and create the remaining 4 templates with matching visual language. Focus on:
1. Consistent typography (Georgia family)
2. Consistent spacing (BAR_GAP=13, SEC_GAP=6)
3. Consistent color usage (navy headers, grey section bars)
4. KDP print safety (inset bars, footer guard, no bleed)
5. Professional legal document appearance
