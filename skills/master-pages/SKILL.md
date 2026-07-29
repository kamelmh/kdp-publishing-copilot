---
name: master-pages
description: >
  Master page system for KDP low-content book design. Generates recto (right-hand) and verso 
  (left-hand) template pages for visual review before full interior generation. Like InDesign 
  master pages — iterate on layout, alignment, colors, and spacing without regenerating 120+ 
  pages each time. Includes PNG rendering for quick visual inspection. Use when designing or 
  refining interior layouts for print-ready books.
---

# Master Pages Skill (v1.1)

Design-time master page generator for KDP book interiors. Produces recto/verso template pair
for layout review before committing to full 120-page generation.

## Why Master Pages?

Regenerating a 120-page PDF + rendering PNGs takes ~30 seconds per iteration.
Master pages reduce this to ~2 seconds for a single recto/verso pair.
Design changes can be reviewed in under 5 seconds.

## Requirements
```bash
pip install reportlab pymupdf   # pymupdf only for PNG rendering
```

## Commands
```bash
# Generate master pages (recto + verso) + render to PNG
python skills/master-pages/scripts/master_page_generator.py

# Generate master pages only (PDFs)
python skills/master-pages/scripts/master_page_generator.py --pdf-only

# Render existing PDFs to PNG only
python skills/master-pages/scripts/master_page_generator.py --png-only

# Custom output directory
python skills/master-pages/scripts/master_page_generator.py --output-dir /path/to/output
```

## Output Structure
```
books/notary-log-book/master-pages/
├── master-recto.pdf       ← Page 3 template (right-hand, gutter on LEFT)
├── master-verso.pdf       ← Page 4 template (left-hand, gutter on RIGHT)
└── renders/
    ├── master-recto-001.png   ← Visual preview (200 DPI)
    └── master-verso-001.png   ← Visual preview (200 DPI)
```

## Publishing Parity Convention

**This is critical — the skill will produce a backwards book if gotten wrong.**

| Page | Type | Hand | Gutter | Thumbprint |
|------|------|------|--------|------------|
| Odd (3, 5, 7…) | RECTO | Right-hand | LEFT | RIGHT (outer) |
| Even (4, 6, 8…) | VERSO | Left-hand | RIGHT | LEFT (outer) |

### Recto Master (Page 3)
- Gutter on LEFT (binding edge)
- Thumbprint on RIGHT (outer edge)
- Seal on RIGHT
- Entry number: 001

### Verso Master (Page 4)
- Gutter on RIGHT (binding edge)
- Thumbprint on LEFT (outer edge)
- Seal on LEFT
- Entry number: 002

Both pages share identical layout structure:
- **Header:** NOTARIAL ACT RECORD + Entry No.
- **A:** Date & Time (aligned labels, AM/PM checkboxes)
- **B:** Type of Notarial Act (checkboxes)
- **C:** Document Information (labels with writelines)
- **D:** Signer Information (labels with writelines)
- **E:** Witness (if applicable)
- **F:** THUMB (on outer edge)
- **G:** Fees (checkboxes)
- **H:** Notary Certification & Signature (dashed seal)
- **I:** Remarks (ruled lines)

### Design Tokens (POD-safe)
| Token | Value | Ink % | Purpose |
|-------|-------|-------|---------|
| `HEADER_BG` | `#C8C8C8` | 22% | Header bar (darkest) |
| `BAR_COLOR` | `#DCDCDC` | 14% | Section bars |
| `ACCENT_LINE` | `#BBBBBB` | 27% | Writelines |
| `BAR_TEXT_COLOR` | `#333333` | — | Dark grey text on bars |
| `DGRAY` | `#333333` | — | Primary text |
| `MGRAY` | `#666666` | — | Secondary text |

**Note:** All tints ≥12% for reliable B&W POD reproduction. Header is darker than section bars (proper hierarchy).

### Print-Safety Features (inherited from kdp-print)
- **Footer guard:** `FOOTER_BASELINE=21`, `FOOTER_GUARD=36` — no collision with page numbers
- **Inset bars:** Never edge-to-edge — prevents trim variance slivers
- **Mirrored margins:** Gutter always on binding edge
- **Bottom margin:** 0.287" (above KDP 0.25" minimum)

## Architecture

### Single Source of Truth
```
skills/kdp-print/entry_page.py       ← SHARED layout module
├── generate_improved_interior.py     ← imports from entry_page
└── master-pages/scripts/
    └── master_page_generator.py      ← imports from entry_page
```

Both generators call `draw_entry_page()` from `entry_page.py`. Design changes in one
automatically apply to the other. This is the guarantee that masters match the interior.

## Workflow

### 1. Design Phase
```bash
# Edit entry_page.py (colors, spacing, alignment)
# Then regenerate masters
python skills/master-pages/scripts/master_page_generator.py

# Review PNGs in master-pages/renders/
# Iterate until satisfied
```

### 2. Approval Phase
```bash
# Once masters look good, generate full interior
python skills/kdp-print/generate_improved_interior.py

# Run preflight
python skills/kdp-print/preflight.py --interior interior_improved.pdf --size 6x9
```

### 3. Upload Phase
```bash
# Upload to KDP
# interior_improved.pdf + cover-wrap-green.pdf
```

## Integration with Other Skills

### kdp-print
Master pages share the same layout engine via `entry_page.py`.
Any design change in master pages automatically applies to the full interior.

### preflight
Master page PDFs can be preflighted individually:
```bash
python skills/kdp-print/preflight.py --interior master-recto.pdf --size 6x9
```

## HyperAgent Review Package

The `hyperagent-package/` directory contains:
- `MASTER_PROMPT.md` — Updated prompt for reviewing master pages
- `skills/master-pages/` — This skill
- `pdfs/` — Master PDFs for review
- `renders/` — PNG renders

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Bars too heavy | Change `BAR_COLOR` to darker hex (e.g. `#D0D0D0`) |
| Text misaligned | Check `_writeline()` x-position after labels |
| Thumbprint wrong side | Check `outer_right` logic in `_margins_for_page()` |
| Page number missing | Check `draw_page_number()` and `FOOTER_BASELINE` |
| PNG blurry | Increase render DPI in `render_pdf_to_png()` (default 200) |
| Gutter on wrong edge | Verify odd=recto=gutter LEFT convention |

## Change History
- **v1.1** — Fixed parity, renamed to recto/verso, POD-safe tokens, single source of truth
- **v1.0** — Initial master page generator with left/right pair, PNG rendering
