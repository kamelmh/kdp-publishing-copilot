---
name: logo-design
description: >
  Generate clean, calibrated vector-style emblems and logos for book covers and brand use —
  notary/legal seals (scales, star, quill) and ring monograms — exported as transparent, print-DPI
  PNGs that drop onto any background. Pairs with a design-tokens file (brand palette, typography,
  emblem placement) so covers stay on-brand. Use for cover logos, seals, emblems, brand marks,
  monograms, or when an AI-generated logo needs a crisp, reproducible, on-spec replacement.
---

# Logo / Emblem Design Skill

Produce **calibrated design artifacts** — one emblem, generated at a known size and DPI on a
transparent field, reusable across covers, spines, social posts, and A+ content. Pure Pillow,
supersampled (4×) for crisp edges. No AI, fully reproducible, recolorable.

Why this exists: AI cover art can bake in an off-brief logo (e.g. a sun/moon motif on a legal
book) that you can't edit. This skill gives you a controllable, on-spec emblem you place exactly
where you want via the `kdp-print` cover builder.

## Files
- `logo_design.py` — emblem generator (CLI below).
- `design_tokens.json` — brand palette, typography, and emblem placement ratios. The single source
  of truth shared with `kdp-print`.

## Generate an emblem
```bash
python logo_design.py --motif seal-scales --size 1200 --out emblem.png --preview-bg "#1B2A4A"
python logo_design.py --motif seal-star   --gold "#C9A227" --out star.png
python logo_design.py --motif monogram --initials "OD" --out monogram.png
```
- **Motifs:** `seal-scales` (balance scales in a star-ring seal — default, best for notary/legal),
  `seal-star`, `seal-quill`, `monogram` (ring + initials).
- **Output:** transparent RGBA PNG at `--size` px. `--preview-bg` also writes a flattened preview.
- `--gold` / `--ink` set colors; pull the exact brand hexes from `design_tokens.json`.

## Put it on a cover (integration with kdp-print)
The `kdp-print` cover builder accepts the emblem as a calibrated overlay:
```bash
python ../kdp-print/kdp_print.py cover --front clean_navy_bg.png --size 6x9 --pages 120 \
  --subtitle "Official Log of Notarial Acts" --author "Author Name" \
  --spine-text "NOTARY PUBLIC RECORD JOURNAL" \
  --emblem emblem.png --emblem-scale 0.40 --emblem-y 0.44 \
  --output cover-wrap.pdf
```
- `--emblem-scale` = emblem width as a fraction of trim width (default 0.34).
- `--emblem-y` = emblem center height as a fraction of cover height (default 0.42, i.e. lower-middle).
- Use a clean background (no baked-in emblem) as `--front`, then overlay the vector emblem. This
  keeps the mark swappable and perfectly on-brand.

## Design tokens (calibrated)
`design_tokens.json` holds: brand palette (navy #1B2A4A, gold #C9A227, steel, paper, ink),
typography (serif title / sans body), emblem defaults (motif, front scale, y-ratio, 300 DPI,
transparent), and cover settings (bleed, scrim alphas, safe margin, barcode clear zone). Read from
it so every book in the catalog shares one visual system.

## Notes / roadmap
- v1 draws seals via primitives (rings, star ring, line-art scales/quill, monogram). Extend with new
  `_draw_*` motif helpers (e.g. embosser, column, document-and-ribbon) as niches expand.
- For true infinite scaling, a future version can emit SVG; PNG at 300 DPI is already print-safe.
