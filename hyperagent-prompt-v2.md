# HyperAgent Master Prompt — KDP Notary Cover Design v2

## Project Context

We are building a **print-ready Amazon KDP paperback cover** for a Notary Public Record Journal. This is the **cover wrap** (full spread: back cover + spine + front cover).

**Previous attempt had incorrect specs.** This prompt contains **verified, correct specifications**.

## Verified KDP Specifications

### Cover Dimensions (120pp, 6×9, white paper)
```python
# KDP Cover Specs — VERIFIED
TRIM_W = 6.0 * inch          # Trim width (single page)
TRIM_H = 9.0 * inch          # Trim height
BLEED = 0.125 * inch         # Bleed on all sides
SPINE = 0.3302 * inch        # Spine width (120pp × 0.002252" + 0.06")
PAPER_THICKNESS = 0.002252   # White paper inches per page
SPINE_ALLOWANCE = 0.06       # Extra for glue/print shift

# Full cover wrap (with bleed)
COVER_W = (TRIM_W * 2) + SPINE + (BLEED * 2)  # = 12.5802"
COVER_H = TRIM_H + (BLEED * 2)                 # = 9.25"
```

### Zone Positions (from left edge)
```python
BACK_X = 0                              # Back cover starts at 0
BACK_W = TRIM_W                         # Back cover width = 6.0"
SPINE_X = TRIM_W                        # Spine starts at 6.0"
SPINE_W = SPINE                         # Spine width = 0.3302"
FRONT_X = TRIM_W + SPINE                # Front starts at 6.3302"
FRONT_W = TRIM_W                        # Front width = 6.0"
```

### Safe Zones
```python
SAFE_MARGIN = 0.25 * inch   # KDP minimum safe zone from trim
BLEED_SAFE = 0.125 * inch  # Bleed extends beyond trim
```

### Color Palette
```python
# Primary colors
NAVY = "#1B2A4A"           # Main background
GOLD = "#D4AF37"           # Accent (title underline, tagline)
WHITE = "#FFFFFF"           # Text on dark background

# Secondary colors
STEEL = "#3A5A8C"          # Secondary navy elements
LIGHT_BLUE = "#E8F4FD"     # Light background accents
MGRAY = "#666666"          # Secondary text
LGRAY = "#999999"          # Light accents
DGRAY = "#333333"          # Dark text
```

### Typography
```python
# Font family (Georgia only)
TITLE_FONT = "Georgia-Bold"
BODY_FONT = "Georgia"
ITALIC_FONT = "Georgia-Italic"

# Font sizes
TITLE_SIZE = 36            # "NOTARY PUBLIC" (dominant)
SUBTITLE_SIZE = 20         # "RECORD JOURNAL" (secondary)
TAGLINE_SIZE = 9           # "100+ PRE-NUMBERED ENTRIES..."
AUTHOR_SIZE = 14           # "Meridian Press"
SPINE_SIZE = 8             # Spine text (max for thin spines)
BACK_HEADLINE = 16         # Back cover headline
BACK_BULLETS = 10          # Back cover bullets
```

## Design Recommendations

### Front Cover
1. **Title Hierarchy:** "NOTARY PUBLIC" at 36pt (dominant), "RECORD JOURNAL" at 20pt (secondary)
2. **Remove redundant subtitle:** "RECORD JOURNAL" under title is redundant
3. **Emblem position:** Move scales of justice higher (above center) or make smaller
4. **Author name:** "Meridian Press" at 14pt, positioned above barcode area
5. **Tagline:** Keep "100+ PRE-NUMBERED ENTRIES · 6" × 9"" at bottom

### Spine
1. **Text:** "NOTARY PUBLIC RECORD JOURNAL" (fits at 8pt)
2. **Orientation:** Rotated 90° (read from top to bottom)
3. **Position:** Centered vertically and horizontally

### Back Cover
1. **Headline:** "Keep a compliant, court-ready record of every notarial act." (1 line)
2. **Bullets (4 items):**
   - 100+ pre-numbered entry pages — sequential numbering deters tampering
   - One complete notarial act per page: date, act type, signer ID, fee, signature
   - Right-thumbprint box and official-seal area on every entry
   - Portable 6 × 9 inch format for the desk, briefcase, or mobile signings
3. **Author bio:** Add 1-2 lines about Meridian Press
4. **Barcode:** KDP auto-generates — use placeholder only
5. **"Independently published"** text at bottom

## Deliverables

### 1. Cover Wrap PDF (`cover-wrap-final.pdf`)
- Full spread: back cover + spine + front cover
- Dimensions: 12.5802" × 9.25"
- Includes bleed (0.125" on all sides)
- RGB color space
- 300 DPI
- PDF 1.4 format

### 2. Affinity Publisher Template (`cover-template.afpub`)
- Single page document (12.5802" × 9.25")
- Guide layers showing zones (back, spine, front)
- Safe zone guides (0.25" from trim)
- Bleed guides (0.125" from trim)
- Editable text layers

### 3. Front Cover Image (`front-cover.png`)
- Trim size: 6" × 9" (1800 × 2700px @300DPI)
- RGB color space
- PNG with transparency (if needed)

### 4. Back Cover Image (`back-cover.png`)
- Trim size: 6" × 9" (1800 × 2700px @300DPI)
- RGB color space
- PNG with transparency (if needed)

## Reference Files Included

### Assets
- `assets/covers/front.png` — Front cover artwork (8.8 MB)
- `assets/covers/front_titled.png` — Front with title (6.8 MB)
- `assets/covers/clean_navy_bg.png` — Navy background texture
- `assets/covers/emblems/seal-scales.png` — Scales of justice emblem
- `assets/brand/imprint_lockup_white.png` — White imprint lockup

### Generated Files
- `books/notary-log-book/interior-final.pdf` — 120-page interior (7.8 MB)
- `books/notary-log-book/cover-wrap-final.pdf` — Cover wrap (11 MB)
- `books/notary-log-book/cover-template.pdf` — Zone guide template (62 KB)

### Code Reference
- `skills/kdp-print/kdp_print.py` — Production generator (shows specs)
- `skills/kdp-print/entry_page.py` — Interior design tokens (matching style)

## Constraints

1. **KDP specifications** — All dimensions must match exactly
2. **Georgia font family only** — No other fonts
3. **RGB color space** — KDP converts to CMYK internally
4. **No bleed on interior** — Cover only has bleed
5. **Spine text max 8pt** — For readability on thin spines
6. **Safe zones** — All important content ≥0.25" from trim
7. **Barcode placeholder** — KDP adds real barcode automatically

## Task

Using the verified specs and design recommendations above, generate:

1. **Updated cover wrap PDF** with:
   - Fixed title hierarchy ("NOTARY PUBLIC" dominant)
   - Removed redundant subtitle
   - Repositioned emblem
   - Added author bio to back cover
   - Tightened back cover headline

2. **Affinity Publisher template** with:
   - Correct document setup (12.5802" × 9.25")
   - Zone guide layers
   - Safe zone guides
   - Editable text layers

3. **Individual cover images** (front and back) for:
   - Customization in Affinity
   - Preview purposes
   - Social media mockups

## Quality Checklist

- [ ] Cover dimensions: 12.5802" × 9.25"
- [ ] Spine width: 0.3302" (99px @300DPI)
- [ ] Bleed: 0.125" on all sides
- [ ] Safe zones: ≥0.25" from trim
- [ ] Title hierarchy: "NOTARY PUBLIC" dominant
- [ ] No redundant subtitle
- [ ] Emblem positioned appropriately
- [ ] Back cover: 4 bullets + author bio
- [ ] Spine text: ≤8pt, readable
- [ ] RGB color space
- [ ] 300 DPI
- [ ] PDF 1.4 format
- [ ] Georgia font family only
