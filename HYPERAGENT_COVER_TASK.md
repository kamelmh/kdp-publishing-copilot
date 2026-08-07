# HyperAgent Task: Generate KDP Cover Wrap

## Objective

Generate a **print-ready KDP paperback cover wrap** for "Notary Public Record Journal" using Python + ReportLab.

## Verified KDP Specifications

```python
# COVER DIMENSIONS (120pp, 6×9, white paper)
TRIM_W = 6.0 * inch          # Single page trim width
TRIM_H = 9.0 * inch          # Trim height
BLEED = 0.125 * inch         # Bleed on all sides
SPINE = 0.3302 * inch        # Spine width (120pp × 0.002252" + 0.06")

# FULL COVER WRAP (with bleed)
COVER_W = (TRIM_W * 2) + SPINE + (BLEED * 2)  # = 12.5802"
COVER_H = TRIM_H + (BLEED * 2)                 # = 9.25"

# ZONE POSITIONS (from left edge) — CORRECTED: includes bleed
BACK_X = 0                              # Back cover starts at 0
BACK_W = TRIM_W                         # Back cover width = 6.0"
SPINE_X = BLEED + TRIM_W                # Spine starts at 6.125" (bleed + trim)
SPINE_W = SPINE                         # Spine width = 0.3302"
FRONT_X = BLEED + TRIM_W + SPINE        # Front starts at 6.4552"
FRONT_W = TRIM_W                        # Front width = 6.0"

# SAFE ZONES
SAFE_MARGIN = 0.25 * inch   # KDP minimum safe zone from trim
```

## Color Palette

```python
NAVY = "#1B2A4A"           # Main background
GOLD = "#D4AF37"           # Accent (title underline, tagline)
WHITE = "#FFFFFF"           # Text on dark background
STEEL = "#3A5A8C"          # Secondary navy elements
MGRAY = "#666666"          # Secondary text
LGRAY = "#999999"          # Light accents
DGRAY = "#333333"          # Dark text
```

## Typography

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

## Cover Layout

### Front Cover (Right Zone)
```
NOTARY PUBLIC          (36pt, Georgia Bold, dominant)
RECORD JOURNAL         (20pt, Georgia Regular, secondary)

Official Log of Notarial Acts   (12pt, Georgia Italic)

[Emblem: scales of justice, centered, 2" diameter]

Meridian Press         (14pt, Georgia Regular)
100+ PRE-NUMBERED ENTRIES · 6" × 9"   (9pt, Georgia)
```

### Spine (Center Zone)
```
NOTARY PUBLIC RECORD JOURNAL   (8pt, Georgia Bold, rotated 90°)
```

### Back Cover (Left Zone)
```
Keep a compliant, court-ready
record of every notarial act.   (16pt, Georgia Bold)

• 100+ pre-numbered entry pages — sequential numbering deters tampering
• One complete notarial act per page: date, act type, signer ID, fee, signature
• Right-thumbprint box and official-seal area on every entry
• Portable 6 × 9 inch format for the desk, briefcase, or mobile signings   (10pt, Georgia)

Meridian Press is an independent publisher
of legal and professional journals.   (9pt, Georgia Italic)

[Barcode placeholder: 2" × 1.2", white box]    Independently published
```

## Deliverables

1. **cover-wrap-final.pdf** — Full spread (12.5802" × 9.25"), RGB, 300dpi, PDF 1.4
2. **cover-template.afpub** — Affinity template with zone guides
3. **front-cover.png** — Front only (6" × 9", 1800×2700px @300dpi)
4. **back-cover.png** — Back only (6" × 9", 1800×2700px @300dpi)

## Reference Files

| File | Purpose |
|------|---------|
| `skills/kdp-print/kdp_print.py` | Existing generator (shows specs) |
| `assets/covers/front.png` | Front cover artwork (8.8 MB) |
| `assets/covers/emblems/seal-scales.png` | Scales of justice emblem |
| `assets/brand/imprint_lockup_white.png` | White imprint lockup |
| `books/notary-log-book/interior-final.pdf` | Interior (for reference) |

## Constraints

1. **Georgia font family only** — registered from `C:/Windows/Fonts/georgia*.ttf`
2. **RGB color space** — KDP converts to CMYK internally
3. **No bleed on interior** — Cover only has bleed
4. **Spine text max 8pt** — For readability on thin spines
5. **Safe zones** — All important content ≥0.25" from trim
6. **Barcode placeholder** — KDP adds real barcode automatically

## Design Variations

Generate **3 color variations** of the same cover design:

### Variation 1: Navy/Gold (Classic)
```python
BG_COLOR = "#1B2A4A"        # Navy — authoritative, trustworthy
ACCENT_COLOR = "#D4AF37"    # Gold — premium, classic
TEXT_COLOR = "#FFFFFF"       # White text
SUBTITLE_COLOR = "#D8DEE9"  # Light grey for secondary text
```

### Variation 2: Charcoal/Silver (Modern)
```python
BG_COLOR = "#2D2D2D"        # Charcoal — sophisticated, elegant
ACCENT_COLOR = "#C0C0C0"    # Silver — modern, clean
TEXT_COLOR = "#FFFFFF"       # White text
SUBTITLE_COLOR = "#B0B0B0"  # Light silver for secondary text
```

### Variation 3: Midnight Blue/Copper (Profound)
```python
BG_COLOR = "#0D1B2A"        # Midnight blue — deep, contemplative
ACCENT_COLOR = "#B87333"    # Copper — warm, wise, touching
TEXT_COLOR = "#FFFFFF"       # White text
SUBTITLE_COLOR = "#D4E4F7"  # Light blue for secondary text
```

## Task

Generate a Python script that creates **3 cover wrap PDFs** (one per variation):

1. Creates the full cover wrap PDF (12.5802" × 9.25") for each variation
2. Applies background color with accent color
3. Places front cover artwork (from `assets/covers/front.png`)
4. Adds title hierarchy ("NOTARY PUBLIC" dominant)
5. Positions emblem (centered, 2" diameter)
6. Adds spine text (rotated 90°)
7. Adds back cover content (headline, bullets, author bio)
8. Adds barcode placeholder (2" × 1.2")
9. Exports as PDF 1.4, RGB, 300dpi

## Output Files

Save to: `books/notary-log-book/`
- `cover-wrap-navy-gold.pdf` — Variation 1 (Classic)
- `cover-wrap-charcoal-silver.pdf` — Variation 2 (Modern)
- `cover-wrap-midnight-copper.pdf` — Variation 3 (Profound)
- `cover-wrap-final.pdf` — Best variation (default: Navy/Gold)
