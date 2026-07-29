# KDP Publishing Copilot — Project

Tooling and deliverables for Oumkeltoum Djerjour's Amazon KDP low-content book business.
Rebuilt and corrected by the KDP Publishing Copilot agent.

## Structure
```
kdp-publishing-copilot/
├─ README.md                     ← this file
├─ skills/
│  ├─ kdp-print/                 ← interiors, cover wraps, specs + CORRECT royalty math
│  │  ├─ kdp_print.py
│  │  └─ SKILL.md
│  ├─ logo-design/               ← calibrated vector emblems + brand tokens
│  │  ├─ logo_design.py
│  │  ├─ design_tokens.json
│  │  └─ SKILL.md
│  └─ book-illustration-concepts/← illustration/cover-concept workflow + storyboard tool
│     ├─ storyboard.py
│     ├─ style_bible_template.json
│     └─ SKILL.md
├─ books/
│  └─ notary-log-book/           ← Book 1 (print-ready)
│     ├─ interior.pdf            ← 120pp, upload this
│     ├─ cover-wrap.pdf          ← AI-art navy cover (option A)
│     ├─ cover-wrap-vector.pdf   ← calibrated vector cover (option B)
│     ├─ cover-wrap-green.pdf    ← green/gold colorway
│     ├─ cover-wrap-burgundy.pdf ← burgundy/cream colorway
│     ├─ cover-wrap-PROOF.pdf    ← guides only — DO NOT upload
│     └─ PUBLISHING_PLAYBOOK.md  ← pricing, metadata, upload checklist, tax
└─ assets/covers/                ← front art, emblems, colorway backgrounds
```

## Book 1 status
Notary Public Record Journal — 6×9, 120 pages, $12.99. Imprint / pen name: **Meridian Press** (KDP account & royalties under Oumkeltoum Djerjour). Interior + covers print-ready.
Upload `interior.pdf` + one cover wrap to KDP; follow `PUBLISHING_PLAYBOOK.md`.

## Key corrections baked in (vs. the earlier draft)
- **Royalty:** Amazon paperback = 60% of list − printing (50% below the price threshold); 40% is Expanded Distribution only. NOT a flat 40%.
- **Printing cost:** ~$1.00 + $0.012/page → ~$2.44 for 120pp (net ~$5.35 at $12.99 on Amazon).
- **Canva canvas:** true 300 DPI full wrap = 3774×2775 px (the old "1256×925 @300 DPI" was 100 DPI).
- **Interior:** premium one-entry-per-page (sections A–I, 1" thumbprint, seal, index) with mirrored gutter margins.
- **Cover generator:** fixed the crash (missing spine-px key) and the printed-guides bug; added gradient scrims + a swappable vector `--emblem` overlay.

## Regenerate anything
```bash
pip install reportlab pymupdf Pillow
# specs + pricing
python skills/kdp-print/kdp_print.py specs --size 6x9 --pages 120 --price 12.99
# interior
python skills/kdp-print/kdp_print.py interior --type notary --size 6x9 --entries 110 --total-pages 120 --output books/notary-log-book/interior.pdf
# emblem + cover (calibrated)
python skills/logo-design/logo_design.py --motif seal-scales --size 1200 --out emblem.png
python skills/kdp-print/kdp_print.py cover --front bg.png --emblem emblem.png --size 6x9 --pages 120 \
  --subtitle "Official Log of Notarial Acts" --author "Oumkeltoum Djerjour" \
  --spine-text "NOTARY PUBLIC RECORD JOURNAL" --bg "#1B2A4A" --accent "#C9A227" --text "#FFFFFF" \
  --output cover.pdf
```
