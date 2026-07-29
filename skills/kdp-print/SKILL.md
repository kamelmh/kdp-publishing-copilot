---
name: kdp-print
description: >
  Generate print-ready Amazon KDP paperback interiors and full cover wraps for low-content
  books, and compute exact KDP print specs, spine width, and paperback royalties. Use whenever
  the user wants a KDP interior PDF (notary log, lined, grid, or blank), a full front+spine+back
  cover wrap at 300 DPI, correct margins/bleed/spine for a trim size and page count, or accurate
  paperback pricing/royalty math. Trigger on: notary journal, log book, low-content book, KDP
  interior, KDP cover, spine width, bleed, gutter margin, print-ready PDF, royalty, printing cost.
---

# KDP Print Skill

Generate print-ready interiors and full cover wraps for Amazon KDP low-content books, plus a
spec/royalty calculator. Pure Python (ReportLab + Pillow), English, no external fonts required.

## Requirements
```bash
pip install reportlab pymupdf Pillow   # pymupdf only needed for PNG previews/QA
```

## Commands

```bash
# 1) Calculate specs + pricing for a book
python kdp_print.py specs --size 6x9 --pages 120 --paper white --price 12.99

# 2) Generate a premium notary log interior (cover + instructions + entries + index + notes)
python kdp_print.py interior --type notary --size 6x9 --entries 110 --total-pages 120 \
    --output interior.pdf

# 3) Generate a lined / grid / blank interior
python kdp_print.py interior --type lined --size 6x9 --pages 120 --output lined.pdf

# 4) Build a full print-ready cover wrap (front + spine + back)
python kdp_print.py cover --front front.png --size 6x9 --pages 120 \
    --subtitle "Official Log of Notarial Acts" --author "Author Name" \
    --spine-text "NOTARY PUBLIC RECORD JOURNAL" --output cover-wrap.pdf
# add --proof to emit a copy WITH magenta trim/spine/bleed guides (never upload the proof)
```

## KDP Specs (verified 2026, baked into the code)

| Spec | Rule |
|---|---|
| Gutter (inside) margin | 0.375" (≤150pp), 0.5" (151–300), 0.625" (301–500), 0.75" (501+). Code bumps to a comfortable 0.5" min. |
| Outside / top / bottom | 0.25" minimum |
| Bleed | 0.125" top/bottom/outer — **cover only**; interiors need no bleed |
| Spine width | `pages × thickness + 0.06"` → white 0.002252", cream 0.0025", color 0.002347" |
| Resolution | 300 DPI; color space RGB (KDP converts to CMYK) |
| Page count | even number, 24–828 |

## Paperback royalty (this is the part most guides get wrong)

- **Amazon marketplaces:** `list × 60% − printing cost` (drops to **50%** if the list price is
  below the marketplace threshold, a rule introduced June 2025).
- **Expanded Distribution:** `list × 40% − printing cost`.
- A flat "40% royalty" is **not** the Amazon rate. The eBook 70%/35% tiers do **not** apply to paperbacks.
- B&W printing cost (US, >108pp) ≈ `$1.00 + $0.012 × pages`.
- Example — 6×9, 120pp, $12.99: printing ≈ $2.44 → **$5.35** net (Amazon 60%), $2.76 (ED 40%).

## Interior: premium notary log

`--type notary` produces one complete notarial act per page:
- **Title page** — title, subtitle, dashed OFFICIAL SEAL, notary/commission/state/office/volume/year fields, disclaimer bar.
- **Instructions page** — how to use, sequential-numbering/tamper note, retention guidance.
- **Entry pages** — pre-numbered `Entry No. NNN`; sections **A** Date & Time, **B** Act Type
  (checkboxes), **C** Document Info, **D** Signer Info, **E** Witness, **F** 1"×1" right-thumbprint
  box on the **outer** edge, **G** Fees, **H** Notary Certification + dashed seal, **I** Remarks.
- **Index / summary** pages — pre-numbered rows (No./Date/Signer/Act/Fee).
- **Notes** pages pad the book to an exact `--total-pages` count.
- Margins **mirror** by recto/verso so the gutter is always on the binding edge and the thumbprint on the outer edge.

Other interior types: `lined` (ruled 0.3"), `grid` (0.2"), `blank` (page numbers only).

## Cover wrap builder

- Full-bleed canvas at `(2×trim) + spine + 2×bleed` wide × `trim + 2×bleed` tall, filled with the
  background color so bleed is covered.
- Front art (`--front`, a PNG/JPG) is placed across the front panel and extended into the outer/top/bottom bleed.
- Vector title/subtitle/author (Times-Bold built-in; drops in `assets/fonts/LibreBaskerville-*.ttf` automatically if present), a gold accent rule, vertical spine text, back-cover blurb + bullets, and a white barcode-safe box (KDP prints the real barcode there).
- The normal output has **no printed guides**. `--proof` adds magenta trim/spine/bleed guides for visual checking only — never upload the proof file.

## Recommended workflow
1. `specs` to lock trim, spine, cover size, and pricing.
2. `interior` to build the manuscript PDF; preview with PyMuPDF and check margins.
3. Generate front-cover art (e.g. GenerateImage), then `cover` to assemble the wrap; check the `--proof`.
4. Upload interior + cover to KDP; paste metadata; set price; run KDP Previewer.

## Files
- `kdp_print.py` — specs/royalty calculator, interior generators, cover-wrap builder (CLI above).
