---
name: kdp-print
description: >
  Generate print-ready Amazon KDP paperback interiors and full cover wraps, and compute exact KDP
  specs, spine width, and CORRECT paperback royalties. Interiors are laid out with a footer collision
  guard, mirrored gutter margins, and no ink at the trim edge (no-bleed safe). Cover builder supports
  a calibrated emblem overlay and self-scaling spine text that respects KDP's fold tolerance.
  Use for KDP interior/cover PDFs, spine/bleed/gutter math, and paperback pricing.
---

# KDP Print Skill (v3.0)

Print-ready interiors and full cover wraps for Amazon KDP low-content books, plus a spec/royalty
calculator. Pure Python (ReportLab + Pillow); English; no external fonts required; all-vector output.

## Architecture

**Single source of truth:** `entry_page.py` contains ALL layout functions. `kdp_print.py` imports
from it — never draw layout directly. `preflight.py` verifies output. This avoids duplicate code
that silently diverges.

```
skills/kdp-print/
├── entry_page.py     # SINGLE SOURCE: draw_entry_page, draw_cover_page, draw_instructions_page,
│                     #   draw_index_pages, draw_notes_page, design tokens, helpers
├── kdp_print.py      # CLI entry point + production generator (imports from entry_page.py)
├── preflight.py      # 27-check verifier + text assertions (run before every upload)
├── render_pages.py   # Render individual pages as PNGs via PyMuPDF
└── SKILL.md          # This file
```

### Shared source with master-pages skill
`skills/master-pages/scripts/master_page_generator.py` also imports from `entry_page.py` for
consistency. Both generator scripts share identical layout functions.

## Requirements
```bash
pip install reportlab pymupdf Pillow   # pymupdf only for PNG previews / verification
```

## Commands
```bash
# specs + correct pricing
python kdp_print.py specs --size 6x9 --pages 120 --paper white --price 12.99

# premium notary interior (title + instructions + entries + index + notes, padded to exact page count)
python kdp_print.py interior --type notary --size 6x9 --entries 110 --total-pages 120 --output interior.pdf

# lined / grid / blank interior
python kdp_print.py interior --type lined --size 6x9 --pages 120 --output lined.pdf

# full cover wrap (add --proof for a guides copy you must NOT upload)
python kdp_print.py cover --front bg.png --size 6x9 --pages 120 \
  --subtitle "Official Log of Notarial Acts" --author "MERIDIAN PRESS" \
  --spine-text "NOTARY PUBLIC RECORD JOURNAL" \
  --bg "#123A2C" --accent "#C9A227" --text "#FFFFFF" \
  --emblem emblem.png --emblem-scale 0.40 --emblem-y 0.44 \
  --output cover-wrap.pdf
```

## Print-safety features (v3.0 — each fixes a real, shipped defect)

### 1. Footer collision guard
```python
FOOTER_BASELINE = 21   # page-number baseline (0.29" ink clearance — above KDP's 0.25" min)
FOOTER_GUARD    = 36   # nothing bottom-anchored may sit below this
```
Every page number uses `FOOTER_BASELINE`. Bottom-anchored blocks are laid out *up* from
`FOOTER_GUARD`, so a box can never overlap the page number. Verified: bottom margin **0.287″**
on all pages.

### 2. Inset bars — no ink at the trim edge
All decorative bars are drawn `c.rect(lm, y, uw, h)` — **never** `c.rect(0, y, W, h)`. On a
no-bleed interior, ink running to the trim edge gets cut by ±0.0625″ trim variance, producing
white slivers or uneven bars. Verified: **0 pages** with colored ink at any trim edge.

### 3. Six-column index
`No. | Date | Signer Name | Doc Type | Act Type | Fee` — column x-offsets `(0, 0.45, 1.30, 2.65,
3.65, 4.65)"` summing to the 5.2″ text block. "Doc Type" is what buyers reach for most when
auditing records.

### 4. Reference boxes on the instructions page
Two bordered boxes rendered by the internal `_refbox(bottom, rows, title)` helper, both anchored
above `FOOTER_GUARD`:
- **STATE-SPECIFIC REQUIREMENTS** — California, Florida, New York, Texas, Illinois, Pennsylvania
  (thumbprint + journal + retention rules)
- **TYPICAL FEE SCHEDULE (US)** — acknowledgment, oath/affirmation, jurat, copy certification,
  signature witnessing, proof of execution

### 5. Adaptive spine text
```python
SPINE_SAFE = 0.0625 * inch                          # KDP max print shift per fold
size = min(8.0, (spine - 2 * SPINE_SAFE) * 0.9)     # cap 8pt, never breach the safe zone
```
Self-scales for thinner/thicker books. At 120 pp this resolves to 8 pt with 0.087″ clearance.

### 6. Page-2 clearance
The first entry page has its box bottom at 40.0pt while the page-number top is at 27.5pt
(+12.5pt clearance) — prevents the entry box from colliding with the page number.

### 7. PDF metadata
`setTitle` / `setAuthor` / `setSubject` / `setKeywords` / `setCreator` are set on the canvas.

### 8. Parameterized margins
`_margins_for_page_raw(page_num, trim_w, trim_h, gutter)` supports master-page use with
arbitrary trim dimensions while sharing identical logic with `entry_page.py`.

## KDP specs (verified 2026, baked in)
| Spec | Rule |
|---|---|
| Gutter (inside) | 0.375″ (≤150 pp) · 0.5″ (151–300) · 0.625″ (301–500) · 0.75″ (501+); generator uses ≥0.5″ |
| Outside / top / bottom | 0.25″ minimum |
| Bleed | 0.125″ — **cover only**; interiors need none |
| Spine | `pages × thickness + 0.06″` (white 0.002252, cream 0.0025, color 0.002347) |
| Resolution / color | 300 DPI, RGB (KDP converts to CMYK) |
| Page count | even, 24–828 |

## Paperback royalty (the part most guides get wrong)
- **Amazon marketplaces:** `list × 60% − printing` (drops to **50%** below the marketplace price
  threshold, rule since Jun-2025).
- **Expanded Distribution:** `list × 40% − printing`.
- A flat "40% royalty" is the ED rate, **not** Amazon's. eBook 70/35 tiers don't apply to paperbacks.
- B&W printing (US, >108 pp) ≈ `$1.00 + $0.012 × pages`.
- Example — 6×9 / 120 pp / $12.99 → printing $2.44 → **$5.35** net on Amazon, $2.76 on ED.
  (If withholding applies — e.g. no US tax treaty — cash received is lower than the reported royalty.)

## Notary interior structure (`--type notary`)
Title page (seal + notary/commission/state/office/volume fields + disclaimer) → instructions +
the two reference boxes → **pre-numbered entry pages**, one act each, sections **A** Date & Time,
**B** Act Type (checkboxes), **C** Document Info, **D** Signer Info, **E** Witness, **F** 1″×1″
right-thumbprint box on the **outer** edge, **G** Fees, **H** Notary Certification + dashed seal,
**I** Remarks → 6-column index → ruled notes pages padding to an exact `--total-pages`.
Margins **mirror** by recto/verso so the gutter is always on the binding edge.

Other interior types: `lined` (0.3″ rule), `grid` (0.2″), `blank`.

## Cover wrap builder
Canvas = `(2 × trim) + spine + (2 × bleed)` wide × `trim + (2 × bleed)` tall. Front art fills the
front panel into the bleed; **gradient** scrims (not hard-edged rectangles) keep title/author legible
over any artwork; gold accent rule; adaptive spine text; back blurb + bullets; white barcode-safe box
at the lower-right of the back panel. `--emblem` overlays a transparent emblem PNG (from the
`logo-design` skill) at a calibrated position via `--emblem-scale` / `--emblem-y`.
Normal output has **no printed guides**; `--proof` adds magenta trim/spine/bleed guides for checking
only — never upload the proof.

## Preflight — ALWAYS run before uploading

`preflight.py` measures the actual PDFs and exits non-zero on any failure, so it can gate a build.

```bash
pip install pymupdf numpy

# both files (page count auto-detected from the interior)
python preflight.py --interior interior.pdf --cover cover-wrap.pdf --size 6x9

# other books
python preflight.py --interior i.pdf --size 5x8 --paper cream
python preflight.py --cover c.pdf --size 8.5x11 --pages 150      # cover-only needs --pages
python preflight.py --interior i.pdf --size 6x9 --sample 10      # every 10th page (fast)
python preflight.py --interior i.pdf --cover c.pdf --size 6x9 --json report.json
```

**27 checks.** Interior: opens · even page count · 24–828 · uniform size · trim matches · no bleed ·
metadata title/author · fonts base-14-or-embedded · raster DPI ≥ 300 · bottom/top/gutter/outer
margins (gutter threshold auto-selected from page count) · no blank pages · no ink at trim edge ·
no box below the footer guard · no text straddling a box border.
Cover: opens · single page · wrap size · spine width · front/back text safe zone · spine fold
clearance · **PROOF-file detection** · barcode zone clear.

**Text assertions** (for repeatable QA of specific content):
```bash
# Verify required content present
python preflight.py --interior interior.pdf --size 6x9 \
  --expect-text "STATE-SPECIFIC" --expect-text "FEE SCHEDULE" \
  --expect-text "Doc Type"

# Verify prohibited content absent
python preflight.py --cover cover-wrap.pdf --size 6x9 \
  --forbid-text "MERIDIAN PRESS"
```

Two checks worth calling out:
- **PROOF-file detection** — scans for magenta guide ops and fails if found. Uploading the proof by
  mistake is the single easiest way to ship a ruined cover; this makes it impossible to miss.
- **Barcode zone** — samples the lower-right of the back panel and warns if it isn't ~85%+ light,
  since KDP prints its barcode there and will cover any artwork you put underneath.

Margins are measured from **visible ink** at `--dpi` (default 300), never from font-metric bounding
boxes — bbox includes empty descender space and reports margins ~0.03″ pessimistically, which
produces false failures.

Exit codes: `0` = cleared, `1` = at least one FAIL. Warnings never fail the run.
After a clean preflight, still run **KDP Previewer** — it catches press-side issues no local tool sees.

## Change history
- **v3.0** — consolidated architecture: single source of truth in `entry_page.py` (all layout
  functions shared with `master-pages` skill); deleted `generate_improved_interior.py`; fixed
  index regression (12→114 entries); fixed page-2 collision (40pt vs 27.5pt); added text
  assertions; deleted stale verification scripts; standardized gutter to 0.5″.
- **v2.2** — footer guard + unified page-number baseline; inset all bars; 6-column index; state &
  fee reference boxes; adaptive spine text; PDF metadata.
- **v2.1** — gradient scrims; `--emblem` overlay; `--text` color.
- **v2.0** — fixed cover-builder crash (missing spine-pixels key); fixed unapplied gutter margin;
  removed printed guides from the upload file; corrected the royalty model.

## Pairs with
`logo-design` (calibrated emblems + design tokens) · `book-illustration-concepts` (cover/illustration concepts) · `master-pages` (recto/verso template generator).
