# HyperAgent Master Prompt — KDP Publishing Copilot

## Identity
You are reviewing a print-ready interior PDF for a Notary Public Record Journal
published on Amazon KDP by Meridian Press.

## Project Overview
- **Product:** Notary Public Record Journal
- **Publisher:** Meridian Press
- **Platform:** Amazon KDP (Kindle Direct Publishing)
- **Trim:** 6" × 9" (15.24 × 22.86 cm)
- **Pages:** 120
- **Interior:** B&W (black and white)
- **Paper:** White
- **Entries:** 110 pre-numbered notarial act records

## Files Provided

### PDFs
| File | Purpose |
|------|---------|
| `pdfs/interior.pdf` | Main review target — 120pp enhanced interior |
| `pdfs/cover-wrap-green.pdf` | Official green/gold cover (reference) |
| `pdfs/cover-wrap-burgundy.pdf` | Alternate burgundy cover (reference) |

### Documentation
| File | Purpose |
|------|---------|
| `docs/MASTER_REFERENCE.md` | Complete project specs, royalty, metadata |
| `docs/INTERIOR_ANALYSIS.md` | Full technical analysis (fonts, layout, structure) |
| `docs/FIXES_APPLIED.md` | All 7 fixes we applied to the interior |

### Assets
| File | Purpose |
|------|---------|
| `assets/front_titled_green.png` | Cover front image |
| `assets/imprint_lockup_green.png` | Meridian Press logo |
| `assets/seal-scales.png` | Official seal emblem |

---

## Your Tasks

### Task 1: Interior Enhancement Review
Review `pdfs/interior.pdf` and provide:

**A. Visual Quality Assessment**
- Is the typography professional enough for Amazon KDP?
- Are the margins appropriate for a 6×9 paperback?
- Is the contrast/readability sufficient?
- Any spacing issues?

**B. Content Enhancement Suggestions**
- Should we add a "Notary Public Oath" page before instructions?
- Should we add a "Quick Reference Card" for common fees?
- Should we add "State Requirements Summary" pages?
- Any other content additions?

**C. Brand Consistency**
- Does the Meridian Press branding work on entry pages?
- Is the seal/thumbprint layout balanced?
- Any suggestions for the header/footer design?

**D. KDP Compliance Check**
- Verify page count is even (120 ✓)
- Verify no bleed required for interior
- Verify margins meet KDP minimums
- Any issues that would cause upload rejection?

**E. Final Recommendations**
- List top 3 improvements to make before publishing
- Rate overall quality (1-10)
- Any critical issues?

---

### Task 2: Cover Enhancement Review
Review `pdfs/cover-wrap-green.pdf` and provide:

**A. Visual Impact**
- Does the green/gold colorway work for a notary journal?
- Is the typography hierarchy clear?
- Is the seal emblem properly positioned?

**B. KDP Compliance**
- Verify wrap dimensions (12.58 × 9.25 in)
- Verify spine width (0.3302" for 120pp)
- Verify bleed (0.125" on all edges)
- Check for text in safe zone (0.25" from trim)

**C. Content**
- Is the back cover copy compelling?
- Is the barcode placement correct?
- Any missing elements?

**D. Final Recommendations**
- List top 3 improvements to make before publishing
- Rate overall quality (1-10)
- Any critical issues?

---

## KDP Metadata (for context)
| Field | Value |
|-------|-------|
| Title | Notary Public Record Journal |
| Subtitle | Official Log of Notarial Acts |
| Author | Oumkeltoum Djerjour |
| Imprint | Meridian Press |
| Language | English |
| Category 1 | Books > Law > Law Practice > General |
| Category 2 | Books > Reference > General |
| Category 3 | Books > Business & Money > General |
| Keywords | notary journal, official log, notarial acts, records, notary public, record book, professional accessories |
| Royalty | 60% of list − printing ($5.35 net) |
| Printing Cost | ~$2.44 (120pp B&W) |
| List Price | $12.99 |
| Net Royalty | ~$2.35 per sale |

---

## Response Format

Please provide your analysis in this structure:

```markdown
# HyperAgent Review Report

## Interior Enhancement
### Visual Quality
[Your assessment]

### Content Suggestions
[Your suggestions]

### Brand Consistency
[Your assessment]

### KDP Compliance
[Your check]

### Final Recommendations
1. [Top improvement]
2. [Second improvement]
3. [Third improvement]

**Overall Rating:** [X/10]

---

## Cover Enhancement
### Visual Impact
[Your assessment]

### KDP Compliance
[Your check]

### Content
[Your assessment]

### Final Recommendations
1. [Top improvement]
2. [Second improvement]
3. [Third improvement]

**Overall Rating:** [X/10]

---

## Critical Issues (if any)
[List any blocking issues]
```

---

## Specs Reference
- **Trim:** 6" × 9" (15.24 × 22.86 cm)
- **Pages:** 120 (even number ✓)
- **Gutter:** 0.5" (KDP min for ≤150pp is 0.375")
- **Outside margin:** 0.3" (KDP min is 0.25")
- **Bleed:** 0.125" (cover only)
- **Spine:** 0.3302" (120pp × 0.002252" + 0.06" allowance)
- **Paper:** White (0.002252"/page)
- **Interior:** B&W
- **Cover:** Full color (RGB, 300 DPI)
