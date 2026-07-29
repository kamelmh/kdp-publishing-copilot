# HyperAgent Master Prompt — KDP Publishing Copilot

## Identity
You are reviewing a **master page design system** for a Notary Public Record Journal
published on Amazon KDP by Meridian Press. This is a new skill that enables rapid
interior layout iteration without regenerating 120+ pages each time.

## Project Overview
- **Product:** Notary Public Record Journal
- **Publisher:** Meridian Press
- **Platform:** Amazon KDP (Kindle Direct Publishing)
- **Trim:** 6" × 9" (15.24 × 22.86 cm)
- **Pages:** 120
- **Interior:** B&W (black and white)
- **Paper:** White
- **Entries:** 110 pre-numbered notarial act records
- **Design:** Light grey section bars (#E8E8E8), professional minimal style

## Files Provided

### Master Pages (NEW — for design review)
| File | Purpose |
|------|---------|
| `pdfs/master-left.pdf` | Left page template (verso, gutter on right) |
| `pdfs/master-right.pdf` | Right page template (recto, gutter on left) |
| `renders/master-left-001.png` | Visual preview of left page |
| `renders/master-right-001.png` | Visual preview of right page |

### Skill Package (NEW)
| File | Purpose |
|------|---------|
| `skills/master-pages/SKILL.md` | Complete skill documentation |
| `skills/master-pages/scripts/master_page_generator.py` | Standalone generator script |

### PDFs
| File | Purpose |
|------|---------|
| `pdfs/interior.pdf` | Full 120pp interior (reference) |
| `pdfs/cover-wrap-green.pdf` | Official green/gold cover (reference) |

### Documentation
| File | Purpose |
|------|---------|
| `docs/MASTER_REFERENCE.md` | Complete project specs, royalty, metadata |
| `docs/HYPERAGENT_THREAD_CONTEXT.md` | Previous review context |

### Assets
| File | Purpose |
|------|---------|
| `assets/front_titled_green.png` | Cover front image |
| `assets/imprint_lockup_green.png` | Meridian Press logo |

---

## Your Tasks

### Task 1: Master Pages Skill Review

Review the **master-pages** skill package and provide:

**A. Skill Architecture**
- Is the SKILL.md clear and complete?
- Does the command structure make sense?
- Are the design tokens well-documented?
- Is the workflow (design → approval → generation) logical?

**B. Code Quality**
- Review `scripts/master_page_generator.py`
- Is it standalone (no dependencies on other skills)?
- Are the helper functions clean and reusable?
- Is the CLI interface intuitive?
- Any bugs or edge cases?

**C. Design System**
- Are the design tokens (colors, spacing) well-organized?
- Is the left/right page mirroring correct?
- Are the section labels consistent?
- Any alignment issues visible in the PNG renders?

**D. Documentation Quality**
- Is the SKILL.md comprehensive enough for another agent to use?
- Are the examples clear?
- Is the troubleshooting section helpful?
- Any missing information?

**E. Recommendations**
- List top 3 improvements to the skill
- Rate overall quality (1-10)
- Any critical issues?

---

### Task 2: Interior Design Review

Review the master page renders (`renders/master-left-001.png`, `renders/master-right-001.png`):

**A. Visual Quality**
- Is the typography professional for Amazon KDP?
- Are the light grey bars (#E8E8E8) clean and readable?
- Is the contrast sufficient?
- Any spacing issues?

**B. Layout & Alignment**
- Are labels aligned with their writelines?
- Are checkboxes consistently positioned?
- Is the thumbprint/seal placement balanced?
- Do left/right pages mirror correctly?

**C. KDP Compliance**
- Do margins meet KDP minimums?
- Is the footer/page number positioned correctly?
- Any issues that would cause upload rejection?

**D. Final Recommendations**
- List top 3 improvements before publishing
- Rate overall quality (1-10)
- Any critical issues?

---

### Task 3: Integration Assessment

**A. Skill Composability**
- Can this skill be used independently?
- Does it integrate well with `kdp-print`?
- Could it be extended for other book types (lined, grid, blank)?

**B. GitHub Readiness**
- Is the skill package repo-ready?
- Are the file paths clean?
- Any hardcoded paths that need fixing?
- Is the README adequate?

**C. Cross-Tool Compatibility**
- Could this work in Claude GUI?
- Could it work in OpenCode?
- Any platform-specific issues?

---

## KDP Metadata (for context)
| Field | Value |
|-------|-------|
| Title | Notary Public Record Journal |
| Subtitle | Official Log of Notarial Acts |
| Author | Meridian Press |
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

## Master Pages Skill
### Skill Architecture
[Your assessment]

### Code Quality
[Your assessment]

### Design System
[Your assessment]

### Documentation Quality
[Your assessment]

### Final Recommendations
1. [Top improvement]
2. [Second improvement]
3. [Third improvement]

**Overall Rating:** [X/10]

---

## Interior Design
### Visual Quality
[Your assessment]

### Layout & Alignment
[Your assessment]

### KDP Compliance
[Your check]

### Final Recommendations
1. [Top improvement]
2. [Second improvement]
3. [Third improvement]

**Overall Rating:** [X/10]

---

## Integration Assessment
### Skill Composability
[Your assessment]

### GitHub Readiness
[Your assessment]

### Cross-Tool Compatibility
[Your assessment]

---

## Critical Issues (if any)
[List any blocking issues]

---

## Suggested Next Steps
[What should we do after this review?]
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

## Design Tokens
| Token | Value | Purpose |
|-------|-------|---------|
| `BAR_COLOR` | `#E8E8E8` | Light grey section bars |
| `BAR_TEXT_COLOR` | `#444444` | Dark grey text on bars |
| `HEADER_BG` | `#F5F5F5` | Very light grey headers |
| `ACCENT_LINE` | `#CCCCCC` | Subtle accent lines |
| `DGRAY` | `#333333` | Primary text |
| `MGRAY` | `#666666` | Secondary text |
| `FOOTER_BASELINE` | `21` | Page number y-position |
| `FOOTER_GUARD` | `36` | Min distance from bottom |
