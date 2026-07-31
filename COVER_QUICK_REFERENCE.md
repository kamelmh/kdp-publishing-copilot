# Cover Design Quick Reference

## Current Status

**Interior:** ✅ COMPLETE — `interior-final.pdf` (7.8 MB, 120 pages)
**Cover:** 🔄 IN PROGRESS — Customizing in Affinity Publisher

## Cover Specs (Verified)

| Parameter | Value |
|-----------|-------|
| Total width | 12.5802" |
| Total height | 9.25" |
| Trim width (per page) | 6.0" |
| Trim height | 9.0" |
| Spine width | 0.3302" |
| Bleed | 0.125" all sides |
| Safe margin | 0.25" from trim |

## Zone Layout

```
|←————— 6.0" ————→|←— 0.33" —→|←————— 6.0" ————→|
|                  |            |                  |
|    BACK COVER    |   SPINE    |   FRONT COVER    |
|                  |            |                  |
|←— 0.125" bleed —→|            |←— 0.125" bleed —→|
```

## Color Variations

### Variation 1: Navy/Gold (Classic)
- **Background:** #1B2A4A (Navy)
- **Accent:** #D4AF37 (Gold)
- **Feeling:** Authoritative, trustworthy, classic

### Variation 2: Charcoal/Silver (Modern)
- **Background:** #2D2D2D (Charcoal)
- **Accent:** #C0C0C0 (Silver)
- **Feeling:** Sophisticated, elegant, modern

### Variation 3: Midnight Blue/Copper (Profound)
- **Background:** #0D1B2A (Midnight Blue)
- **Accent:** #B87333 (Copper)
- **Feeling:** Deep, contemplative, touching

## Title Recommendations

**Front Cover:**
```
NOTARY PUBLIC          (36pt, Georgia Bold, dominant)
RECORD JOURNAL         (20pt, Georgia Regular, secondary)

Official Log of Notarial Acts   (12pt, Georgia Italic)

[Emblem: scales of justice]

Meridian Press         (14pt, Georgia Regular)
100+ PRE-NUMBERED ENTRIES · 6" × 9"   (9pt, Georgia)
```

**Spine:**
```
NOTARY PUBLIC RECORD JOURNAL   (8pt, Georgia Bold, rotated 90°)
```

**Back Cover:**
```
Keep a compliant, court-ready
record of every notarial act.   (16pt, Georgia Bold)

• 100+ pre-numbered entry pages
• One complete notarial act per page
• Right-thumbprint box and official-seal area
• Portable 6 × 9 inch format       (10pt, Georgia)

Meridian Press is an independent publisher
of legal and professional journals.   (9pt, Georgia Italic)

[Barcode placeholder]    Independently published
```

## Files to Generate

1. **cover-wrap-final.pdf** — Full spread for KDP upload
2. **cover-template.afpub** — Affinity template with guides
3. **front-cover.png** — Front only (for previews)
4. **back-cover.png** — Back only (for previews)

## Export Settings (Affinity)

| Setting | Value |
|---------|-------|
| Preset | PDF (for print) |
| Raster DPI | 300 |
| Area | All Pages |
| Rasterize | Nothing |
| Compatibility | PDF 1.4 |
| Color Space | RGB |
| ICC profile | sRGB IEC61966-2.1 |
| Include bleed | ✓ |
| Embed fonts | All Fonts |
| Subset fonts | ✓ |

## KDP Upload Checklist

- [ ] Cover PDF: 12.5802" × 9.25"
- [ ] Interior PDF: 6×9", 120 pages
- [ ] Both PDFs: RGB, 300dpi, PDF 1.4
- [ ] No ISBN on cover (KDP auto-generates)
- [ ] No crop marks or printer marks
- [ ] Spine text readable at 100% zoom
- [ ] All text within safe zones (≥0.25" from trim)
- [ ] Bleed extends to edges (0.125" beyond trim)

## Asset Locations

| Asset | Path |
|-------|------|
| Front artwork | `assets/covers/front.png` |
| Navy background | `assets/covers/clean_navy_bg.png` |
| Scales emblem | `assets/covers/emblems/seal-scales.png` |
| White imprint | `assets/brand/imprint_lockup_white.png` |
| Interior PDF | `books/notary-log-book/interior-final.pdf` |
| Cover wrap | `books/notary-log-book/cover-wrap-final.pdf` |
| Cover template | `books/notary-log-book/cover-template.pdf` |

## Next Steps

1. **Customize cover in Affinity** using template guides
2. **Apply design recommendations** (title hierarchy, emblem position)
3. **Export final cover PDF** with correct settings
4. **Upload to KDP** (interior + cover)
5. **Set list price** ($12.99 recommended)
6. **Preview and publish**
