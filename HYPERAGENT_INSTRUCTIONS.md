# HyperAgent Instructions — Cover Generation

## Where Are the Files?

### Core Files (HyperAgent Needs These)
```
C:\Users\Admin\projects\active\kdp-publishing-copilot\
├── HYPERAGENT_COVER_TASK.md          ← TASK DEFINITION (give this to HyperAgent)
├── hyperagent-prompt-v2.md           ← DETAILED SPECS (reference)
├── DESIGN_ANALYSIS.md                ← DESIGN RECOMMENDATIONS
├── COVER_QUICK_REFERENCE.md          ← ONE-PAGE CHEAT SHEET
│
├── assets\covers\
│   ├── front.png                     ← FRONT COVER ARTWORK (8.8 MB)
│   ├── front_titled.png              ← FRONT WITH TITLE (6.8 MB)
│   ├── clean_navy_bg.png             ← NAVY BACKGROUND TEXTURE
│   └── emblems\
│       └── seal-scales.png           ← SCALES OF JUSTICE EMBLEM
│
├── assets\brand\
│   └── imprint_lockup_white.png      ← WHITE IMPRINT LOCKUP
│
├── skills\kdp-print\
│   ├── kdp_print.py                  ← EXISTING GENERATOR (shows specs)
│   └── entry_page.py                 ← INTERIOR DESIGN TOKENS
│
└── books\notary-log-book\
    ├── interior-final.pdf            ← COMPLETED INTERIOR (7.8 MB)
    ├── cover-wrap-final.pdf          ← CURRENT COVER (to replace)
    └── cover-template.pdf            ← ZONE GUIDE TEMPLATE
```

### What to Tell HyperAgent

**Copy this prompt and send it:**

```
Using the verified specs in HYPERAGENT_COVER_TASK.md, generate a Python script that creates 3 KDP paperback cover wrap variations for "Notary Public Record Journal".

Key requirements:
1. Full cover wrap: 12.5802" × 9.25" (back + spine + front) for each variation
2. Color variations:
   - Navy/Gold: #1B2A4A + #D4AF37 (classic, authoritative)
   - Charcoal/Silver: #2D2D2D + #C0C0C0 (modern, sophisticated)
   - Midnight Blue/Copper: #0D1B2A + #B87333 (profound, touching)
3. Title: "NOTARY PUBLIC" (36pt) + "RECORD JOURNAL" (20pt)
4. Emblem: scales of justice (from assets/covers/emblems/seal-scales.png)
5. Spine text: "NOTARY PUBLIC RECORD JOURNAL" (8pt, rotated 90°)
6. Back cover: headline + 4 bullets + author bio
7. Barcode placeholder: 2" × 1.2" white box
8. Output: books/notary-log-book/
   - cover-wrap-navy-gold.pdf
   - cover-wrap-charcoal-silver.pdf
   - cover-wrap-midnight-copper.pdf
   - cover-wrap-final.pdf (default: navy/gold)

Reference files:
- assets/covers/front.png (front artwork)
- assets/covers/emblems/seal-scales.png (emblem)
- skills/kdp-print/kdp_print.py (existing generator)
```

## Quick Reference Card

| Spec | Value |
|------|-------|
| Cover width | 12.5802" |
| Cover height | 9.25" |
| Trim width | 6.0" (per page) |
| Trim height | 9.0" |
| Spine width | 0.3302" |
| Bleed | 0.125" all sides |
| Safe margin | 0.25" from trim |
| Background | Navy #1B2A4A |
| Accent | Gold #D4AF37 |
| Title font | Georgia-Bold |
| Body font | Georgia |

## Zone Layout

```
|←————— 6.0" ————→|←— 0.33" —→|←————— 6.0" ————→|
|                  |            |                  |
|    BACK COVER    |   SPINE    |   FRONT COVER    |
|    (blue zone)   | (orange)   |   (green zone)   |
|                  |            |                  |
|←— 0.125" bleed —→|            |←— 0.125" bleed —→|
```

## Files HyperAgent Should Generate

1. **cover-wrap-final.pdf** — Full spread for KDP upload
2. **cover-template.afpub** — Affinity template with guides
3. **front-cover.png** — Front only (for previews)
4. **back-cover.png** — Back only (for previews)

## After HyperAgent Finishes

1. Check `books/notary-log-book/cover-wrap-final.pdf`
2. Open in Affinity Publisher to verify
3. Upload to KDP with `interior-final.pdf`
