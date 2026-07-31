# HyperAgent Task: Embed Front Cover Artwork

## Objective

Modify `make_covers.py` to embed the high-resolution front cover artwork into the cover wrap PDF.

## Current Problem

- Current covers: **115 KB** (vector-only, no artwork)
- Original cover-wrap.pdf: **10.5 MB** (with embedded artwork)
- Need: Professional covers with embedded artwork (~10+ MB)

## What to Do

1. Load `assets/covers/front.png` (8.8 MB) as background layer
2. Place it in the FRONT cover zone (right panel)
3. Keep all vector elements ON TOP:
   - Title text ("NOTARY PUBLIC" + "RECORD JOURNAL")
   - Emblem (scales of justice)
   - Keyline frames
   - Author name
   - Tagline
4. Do NOT embed artwork on back cover or spine (those stay vector)
5. Output: `books/notary-log-book/cover-wrap-final.pdf`

## Expected Output

- File size: ~10+ MB (with embedded artwork)
- Quality: 300 DPI, RGB, PDF 1.4
- Front cover: High-resolution artwork with vector text overlay
- Back cover: Vector only
- Spine: Vector only

## Reference

- Front artwork: `assets/covers/front.png` (8.8 MB, 300 DPI)
- Current script: `books/notary-log-book/hyperagent-covers/make_covers.py`
- Output location: `books/notary-log-book/cover-wrap-final.pdf`
