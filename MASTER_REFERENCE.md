# KDP Publishing Copilot — Complete Reference (v2, CORRECTED)

> **Purpose:** Master reference for building and publishing notary journals on Amazon KDP.
> **v2 corrects v1 errors:** royalty model (60% not 40%), printing cost, Canva DPI, gutter margin,
> entry/page counts, byline (Meridian Press imprint), and official cover color. Figures below match
> the actual delivered files (`interior.pdf`, `cover-wrap-green.pdf`).

---

## ACCOUNT INFORMATION

| Field | Value |
|-------|-------|
| Legal account name | Oumkeltoum Djerjour |
| Email | kaprikika8@gmail.com |
| Account ID | A2JDT3KR1A59T5 |
| Backup contact | kamelmahi71@gmail.com |
| **Cover byline / KDP Author (pen name)** | **Meridian Press** |
| **Publisher / imprint** | **Meridian Press** |
| Tax | W-8BEN signed; no US–Algeria treaty → 30% US withholding |
| Payment | Check payments only (no EFT bank on file) |

> The imprint is what prints on covers and lists on KDP. Account, tax, and royalty checks stay under
> the legal name. The KDP **Author field locks after publishing** — set "Meridian Press" before upload.

---

## KDP SPECIFICATIONS (LOCKED RULES)

### Trim sizes
6×9 (journals/logs — recommended) · 5×8 · 5.06×7.81 (US Trade) · 5.5×8.5 · 8.5×11 (workbooks) · 4.75×6.75 (pocket).

### Margins (KDP requirements, by page count)
- **Gutter (inside):** 0.375" (≤150pp) · 0.5" (151–300) · 0.625" (301–500) · 0.75" (501+).
- **Outside / top / bottom:** 0.25" minimum.
- **Our comfort setting** (baked into the generator): **0.5" gutter, 0.3" outside** on the notary interior — exceeds the KDP minimum for a clean binding edge.

### Bleed
- **Interior:** none (white borders fine).
- **Cover:** 0.125" on all sides (top, bottom, outer).

### Spine formula
`spine = (pages × thickness) + 0.06"` — white 0.002252"/pg, cream 0.0025"/pg, color 0.002347"/pg.
Example: 120 × 0.002252 + 0.06 = **0.3302"** (99 px @ 300 DPI).

### Resolution & color
300 DPI; RGB (KDP converts to CMYK); print-ready PDF, no password. Even page count, 24–828.

---

## NOTARY JOURNAL DESIGN (as built)

| Property | Value |
|----------|-------|
| Trim | 6" × 9" (432 × 648 pt) |
| Inner (gutter) margin | **0.5" (≈36 pt)** — mirrored to the binding edge per page |
| Outer margin | **0.3" (≈21.6 pt)** |
| Top / bottom margin | 0.4" (≈28.8 pt) |
| Thumbprint box | 1" × 1" (72 × 72 pt) on the **outer** edge |
| Font | Helvetica / Helvetica-Bold (built-in) |
| Palette | NAVY #1B2A4A · STEEL #3A5A8C · GOLD #C9A227 · DGRAY #333 · LGRAY |
| Structure | Title page → Instructions → **110 pre-numbered entries** → **4-page index** → **4 notes pages** = **120 pages** |

**Entry page sections (one act per page):** A Date & Time · B Act Type (checkboxes) · C Document Info ·
D Signer Info · E Witness · **F Thumbprint (outer edge)** · G Fees · H Notary Certification + dashed seal · I Remarks.

---

## COVER DESIGN (as built)

### Full wrap
`(2 × 6") + 0.3302" spine + (2 × 0.125" bleed)` = **12.58" × 9.25"** = **3774 × 2775 px @ 300 DPI**.

### Official cover — Deep Green / Gold
- Background: deep green (#123A2C) guilloché; **gold scales-of-justice seal** emblem (vector).
- Title: "NOTARY PUBLIC RECORD JOURNAL" (white serif) · Subtitle: "Official Log of Notarial Acts" (gold).
- **Byline: MERIDIAN PRESS** (imprint — not a personal name).
- Spine text: "NOTARY PUBLIC RECORD JOURNAL" · Back: blurb + bullets + white barcode-safe box.
- **Alternate colorways on file:** navy AI-art, navy vector, burgundy/cream (all same layout).
- Upload the clean wrap; **never upload `cover-wrap-PROOF.pdf`** (it carries alignment guides).

---

## METADATA (copy-paste)

**Title:** Notary Public Record Journal
**Subtitle:** Official Log of Notarial Acts — 110 Pre-Numbered Entry Pages
**Author / pen name:** Meridian Press · **Publisher:** Meridian Press

**Description (HTML):**
```html
<b>Notary Public Record Journal</b> — a professional, tamper-resistant logbook for documenting every notarial act you perform.
<br><br>
Each pre-numbered entry page captures:
<ul>
<li><b>Date & time</b> of the notarial act</li>
<li><b>Act type</b> — acknowledgment, jurat, oath/affirmation, copy certification, signature witnessing</li>
<li><b>Signer details</b> and signature, with <b>ID type, number & expiration</b></li>
<li><b>Document description</b> and <b>fee charged</b></li>
<li><b>Right-thumbprint box</b> and <b>notary seal & signature</b> area</li>
</ul>
<b>Features</b>
<ul>
<li>110 pre-numbered entry pages — sequential numbering deters tampering</li>
<li>One complete act per page for thorough records</li>
<li>Summary index at the back for fast lookups</li>
<li>Portable 6×9 inch format for desk, briefcase, or mobile signings</li>
</ul>
<b>Perfect for</b> notaries public, mobile notaries, loan signing agents, and real-estate closings.
<br><br>
<i>Note: record-keeping rules vary by state — confirm your state's notary journal requirements.</i>
```

**7 keywords:** notary journal · notary log book · notary public record · notarial acts · notary book · notary public journal · notary record book

**Categories (KDP allows 3):** LAW / Reference · BUSINESS & ECONOMICS / Office Management · REFERENCE / Handbooks & Manuals (also use the "notary" browse path).

**Backend keyword strings:**
```
california texas florida state compliant rules
mobile public loan signing agent supplies bag
sequential numbered records tamper proof logbook
official notarial act register ledger log diary
real estate closing legal document tracking book
compact travel size pocket portable small desk
updated 2026 guidelines professional accessories
```

---

## PRICING & ROYALTY (CORRECTED — this is where v1 was wrong)

KDP **paperback** royalty is **NOT a flat 40%**:
- **Amazon marketplaces:** `list × 60% − printing cost` (drops to **50%** if list is below the marketplace threshold — rule since Jun-2025).
- **Expanded Distribution:** `list × 40% − printing cost`.
- eBook 70%/35% tiers do **not** apply to paperbacks.

**Printing (US, B&W, >108pp):** ≈ `$1.00 + $0.012 × pages` → **$2.44** for 120 pages.

| List | Amazon (60%) net | Exp. Dist. (40%) net |
|------|------------------|----------------------|
| $11.99 | $4.75 | $2.36 |
| **$12.99** | **$5.35** | $2.76 |
| $14.99 | $6.55 | $3.56 |

*v1 said "40% = $5.20, printing $2.80" — both wrong. Correct: 60% Amazon, printing $2.44, net $5.35.*

---

## CANVA GUIDE (CORRECTED DPI)

- **Custom canvas:** **3774 × 2775 px** (= 12.58 × 9.25 in @ **true 300 DPI**). *(v1's "1256×925 @300 DPI" was only 100 DPI.)*
- **Bleed:** 37.5 px (0.125") inset on all four edges.
- **Spine:** center strip **99 px** (0.3302"); spine text ≥ ~19 px from each fold.
- Panels: back 1837 px | spine 99 px | front 1837 px (each incl. outer bleed).
- **Export:** PDF Print · include bleed · RGB · 300 DPI. The delivered cover is already print-ready — Canva only needed for edits.

---

## PRE-UPLOAD CHECKLIST

- [ ] Interior: **120 pages**, 6×9, 300 DPI, **no bleed**, no crop/trim marks
- [ ] Cover: full wrap 12.58 × 9.25", 0.125" bleed, spine 0.3302"; uploaded the **green** wrap (not PROOF)
- [ ] Back-cover lower-right left clear for KDP barcode
- [ ] Author/Publisher = **Meridian Press**; title/subtitle spelled exactly; HTML valid; no external links
- [ ] 7 keywords filled; **3 categories** chosen
- [ ] Price $12.99, **60% royalty (Amazon)** — not "40%"
- [ ] KDP Previewer: zero errors

---

## KDP UPLOAD STEPS

1. Sign in at kdp.amazon.com (kaprikika8@gmail.com).
2. Create → **Paperback**.
3. **Details:** English; Title + Subtitle; **Author = Meridian Press** (pen name); **Publisher = Meridian Press**; paste description HTML; "I own the copyright"; 7 keywords; 3 categories.
4. **Content:** KDP free ISBN; trim 6×9; white paper, B&W; no bleed; matte cover.
5. Upload **interior.pdf**, then **cover-wrap-green.pdf**.
6. Run **KDP Previewer**; fix warnings.
7. **Pricing:** US $12.99, 60% royalty; add marketplaces as desired.
8. Publish → review 24–72 h.

---

## FAST-FOLLOW BOOKS (royalties corrected to 60% Amazon)

- **Book 2 — Password Log Book:** 5.06×7.81, 100pp, $9.99 → printing ≈ $2.20, net ≈ **$3.79**. Keywords: password log book, password organizer, internet login tracker.
- **Book 3 — Running Log Book:** 6×9, 120pp, $12.99 → net **$5.35**. Keywords: running log book, running journal, workout tracker.

*(Pipeline per MARKET_ANALYSIS Phase 2. Confirm before building.)*

---

## MEMORY RULES

1. Account/legal name LOCKED; cover byline = **Meridian Press** imprint.
2. Paperback royalty = **60% − printing** on Amazon (50% below threshold), 40% Expanded Distribution — **never a flat 40%**.
3. B&W printing ≈ $1.00 + $0.012/page.
4. Canva full-wrap at true 300 DPI = 3774×2775 px.
5. Notary interior = one act/page, 0.5" gutter, 72pt thumbprint, 110 entries → 120 pages.
6. Interior no bleed; cover 0.125" bleed; even page count; 300 DPI; RGB.
7. No Canva/KDP API — design + upload are manual.
8. Algeria: 30% US withholding; check payments only.

---

*Complete Reference v2 (corrected) — KDP Publishing Copilot · Last updated 2026-07-28*
