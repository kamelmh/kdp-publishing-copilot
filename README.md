# KDP Publishing Copilot

> Meridian Press — Amazon KDP Self-Publishing System

## Overview
Complete system for publishing print-ready books on Amazon KDP.
Currently: **Notary Public Record Journal** (Book 1 of notary niche).

## Structure

```
kdp-publishing-copilot/
├── README.md                          ← You are here
├── docs/                              ← Documentation
│   ├── MASTER_REFERENCE.md            ← Complete specs
│   ├── MARKET_ANALYSIS.md             ← Competitor research
│   ├── CLAUDE_GUI_MASTER_PROMPT.md    ← Claude GUI context
│   ├── HYPERAGENT_MASTER_PROMPT.md    ← HyperAgent context
│   └── ...
│
├── books/
│   └── notary-log-book/               ← Final deliverables
│       ├── interior.pdf               ← 120pp, 6x9, enhanced
│       ├── interior_improved.pdf      ← Backup of enhanced version
│       ├── cover-wrap-green.pdf       ← OFFICIAL cover
│       ├── cover-wrap-burgundy.pdf    ← Alternate cover
│       ├── cover-wrap-vector.pdf      ← Alternate cover
│       └── PUBLISHING_PLAYBOOK.md     ← Upload walkthrough
│
├── skills/                            ← Python generators
│   ├── kdp-print/
│   │   ├── kdp_print.py              ← Main generator
│   │   ├── generate_improved_interior.py ← Enhanced interior
│   │   ├── verify_interior.py        ← Verification script
│   │   └── SKILL.md                  ← Skill documentation
│   ├── notary-journal/
│   │   └── SKILL.md                  ← Notary journal skill
│   ├── logo-design/
│   │   ├── logo_design.py            ← Logo generator
│   │   └── SKILL.md                  ← Skill documentation
│   └── book-illustration-concepts/
│       ├── storyboard.py             ← Storyboard generator
│       └── SKILL.md                  ← Skill documentation
│
├── assets/                            ← Brand + cover assets
│   ├── brand/                         ← Meridian Press logos
│   ├── covers/                        ← Cover images + emblems
│   └── social/                        ← Social media mockups
│
├── hyperagent-package/                ← For HyperAgent review
│   ├── MASTER_PROMPT.md              ← Task instructions
│   ├── pdfs/                          ← PDFs to review
│   ├── docs/                          ← Reference docs
│   └── assets/                        ← Visual references
│
└── claude-gui-package/                ← For Claude GUI review
    ├── INTERIOR_ANALYSIS.md           ← Technical analysis
    ├── FIXES_APPLIED.md               ← Fixes we applied
    ├── pdfs/                          ← PDFs to review
    ├── docs/                          ← Reference docs
    ├── assets/                        ← Visual references
    └── visual-inspection/             ← Rasterized pages
```

## Quick Start

### 1. Review Interior
```bash
# Open in HyperAgent
Upload: hyperagent-package/

# Or open in Claude GUI
Upload: claude-gui-package/
```

### 2. Upload to KDP
```bash
# Follow the playbook
Open: books/notary-log-book/PUBLISHING_PLAYBOOK.md

# Files to upload:
# - interior.pdf (120pp, 6x9)
# - cover-wrap-green.pdf (official cover)
```

### 3. Generate New Interior
```bash
cd skills/kdp-print
python generate_improved_interior.py
```

## KDP Specs

| Property | Value |
|----------|-------|
| Trim | 6" × 9" |
| Pages | 120 |
| Gutter | 0.5" |
| Paper | White |
| Interior | B&W |
| Cover | Full color (RGB) |
| Royalty | 60% − printing |
| List Price | $12.99 |
| Net Royalty | ~$2.35/sale |

## Publishing Strategy
- **Standalone titles** (not series)
- **Catalog depth > series breadth**
- **Target:** 5-6 notary titles before expanding
- **Validation:** BSR < 100K = expand immediately

## Next Steps
1. ✅ Interior enhanced (7 fixes applied)
2. ⏳ HyperAgent review (cover + interior)
3. ⏳ KDP upload (interior + cover)
4. ⏳ Post-launch (A+ Content, Author Central)

---

**Publisher:** Meridian Press
**Author:** Oumkeltoum Djerjour
**Platform:** Amazon KDP
