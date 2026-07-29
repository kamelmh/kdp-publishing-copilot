---
name: master-pages
description: >
  Master page system for KDP low-content book design. Generates left (verso) and right (recto) 
  template pages for visual review before full interior generation. Like InDesign master pages — 
  iterate on layout, alignment, colors, and spacing without regenerating 120+ pages each time. 
  Includes PNG rendering for quick visual inspection. Use when designing or refining interior 
  layouts for print-ready books.
---

# Master Pages Skill (v1.0)

Design-time master page generator for KDP book interiors. Produces left/right template pair
for layout review before committing to full 120-page generation.

## Why Master Pages?

Regenerating a 120-page PDF + rendering PNGs takes ~30 seconds per iteration.
Master pages reduce this to ~2 seconds for a single left/right pair.
Design changes can be reviewed in under 5 seconds.

## Requirements
```bash
pip install reportlab pymupdf   # pymupdf only for PNG rendering
```

## Commands
```bash
# Generate master pages (left + right) + render to PNG
python generate_improved_interior.py --masters --render

# Generate master pages only (PDFs)
python generate_improved_interior.py --masters

# Render existing PDF to PNG
python generate_improved_interior.py --render  # (when called with a PDF)

# Generate full interior (after master approval)
python generate_improved_interior.py --full --entries 110 --pages 120

# Custom entry count
python generate_improved_interior.py --masters --entries 50
```

## Output Structure
```
books/notary-log-book/master-pages/
├── master-left.pdf        ← Page 3 template (verso, gutter on RIGHT)
├── master-right.pdf       ← Page 4 template (recto, gutter on LEFT)
└── renders/
    ├── master-left-001.png   ← Visual preview (200 DPI)
    └── master-right-001.png  ← Visual preview (200 DPI)
```

## How It Works

### Left Master (Verso — odd page)
- Gutter on RIGHT (binding edge)
- Thumbprint on LEFT (outer edge)
- Seal on RIGHT
- Entry number: 001

### Right Master (Recto — even page)
- Gutter on LEFT (binding edge)
- Thumbprint on RIGHT (outer edge)
- Seal on LEFT
- Entry number: 002

Both pages share identical layout structure:
- **Header:** NOTARIAL ACT RECORD + Entry No.
- **A:** Date & Time (aligned labels, AM/PM checkboxes)
- **B:** Type of Notarial Act (checkboxes)
- **C:** Document Information (labels with writelines)
- **D:** Signer Information (labels with writelines)
- **E:** Witness (if applicable)
- **F:** Thumbprint (on outer edge)
- **G:** Fees (checkboxes)
- **H:** Notary Certification & Signature (dashed seal)
- **I:** Remarks (ruled lines)

### Design Tokens
| Token | Value | Purpose |
|-------|-------|---------|
| `BAR_COLOR` | `#E8E8E8` | Light grey section bars |
| `BAR_TEXT_COLOR` | `#444444` | Dark grey text on bars |
| `HEADER_BG` | `#F5F5F5` | Very light grey headers |
| `ACCENT_LINE` | `#CCCCCC` | Subtle accent lines |
| `DGRAY` | `#333333` | Primary text color |
| `MGRAY` | `#666666` | Secondary text |

### Print-Safety Features (inherited from kdp-print)
- **Footer guard:** `FOOTER_BASELINE=21`, `FOOTER_GUARD=36` — no collision with page numbers
- **Inset bars:** Never edge-to-edge — prevents trim variance slivers
- **Mirrored margins:** Gutter always on binding edge
- **Bottom margin:** 0.287" (above KDP 0.25" minimum)

## Workflow

### 1. Design Phase
```bash
# Edit generate_improved_interior.py (colors, spacing, alignment)
# Then regenerate masters
python generate_improved_interior.py --masters --render

# Review PNGs in master-pages/renders/
# Iterate until satisfied
```

### 2. Approval Phase
```bash
# Once masters look good, generate full interior
python generate_improved_interior.py --full --entries 110 --pages 120

# Run preflight
python preflight.py --interior interior_improved.pdf --size 6x9

# Visual inspection
python render_pages.py interior_improved.pdf --pages 1-5
```

### 3. Upload Phase
```bash
# Upload to KDP
# interior_improved.pdf + cover-wrap-green.pdf
```

## Integration with Other Skills

### kdp-print
Master pages share the same layout engine as `kdp-print`'s interior generator.
Any design change in master pages can be applied to the full interior by running `--full`.

### preflight
Master page PDFs can be preflighted individually:
```bash
python preflight.py --interior master-left.pdf --size 6x9
```

### render-pages
Master pages use the same PNG rendering pipeline:
```bash
python render_pages.py master-left.pdf --pages 1
```

## HyperAgent Review Package

The `hyperagent-package/` directory contains:
- `MASTER_PROMPT.md` — Updated prompt for reviewing master pages
- `skills/master-pages/` — This skill
- `pdfs/` — Master PDFs for review
- `visual-inspection/` — PNG renders

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Bars too heavy | Change `BAR_COLOR` to lighter hex (e.g. `#F0F0F0`) |
| Text misaligned | Check `_writeline()` x-position after labels |
| Thumbprint wrong side | Check `outer_right` logic in `_margins_for_page()` |
| Page number missing | Check `draw_page_number()` and `FOOTER_BASELINE` |
| PNG blurry | Increase render DPI in `render_pdf_pages()` (default 200) |

## Change History
- **v1.0** — Initial master page generator with left/right pair, PNG rendering, design tokens
