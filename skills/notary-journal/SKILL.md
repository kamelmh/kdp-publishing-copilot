---
name: notary-journal
description: >
  Design and generate a professional notary public record journal as a print-ready PDF.
  Use this skill whenever the user asks to create, design, build, or generate a notary
  journal, notary record book, notary log, notary entry form, or any document used to
  log notarial acts. Also trigger when the user mentions notary entries, notary acts,
  acknowledgments, oaths, affirmations, copy certifications, signer records, notary
  fees, KDP notary book, or Amazon notary logbook. This skill produces a professional,
  English-language, KDP-ready PDF journal with pre-numbered entries, a thumbprint box,
  a summary/index page, and proper print margins.
---

# Notary Public Record Journal Skill

Generates a professional, English-only, print-ready notary public record journal as a PDF.
Designed to be KDP-compatible (Amazon self-publishing). One complete notarial act entry per page,
pre-numbered sequentially to prevent tampering, with a summary index at the back.

---

## Document Specifications

| Property | Value |
|---|---|
| Trim size | 6" × 9" (default) or 5.5" × 8.5" (compact) |
| Page size in points | 432 × 648 pt (6×9) or 396 × 612 pt (5.5×8.5) |
| Inner (gutter) margin | 0.625" = 45 pt |
| Outer margin | 0.375" = 27 pt |
| Top/Bottom margin | 0.5" = 36 pt |
| Line spacing (write-in) | 0.27" ≈ 19.4 pt |
| Thumbprint box | Minimum 72 × 72 pt (1" × 1"), placed on outer edge |
| Font | Helvetica / Helvetica-Bold (built-in ReportLab) |
| Section border weight | 0.75 pt – 1 pt |
| Divider line weight | 0.5 pt |
| Border color | Dark gray: RGB(51, 51, 51) — 80% black |
| Background | White |

---

## Journal Structure

### 1. Cover Page
- Large centered title: **"Notary Public Record Journal"**
- Subtitle: *Official Log of Notarial Acts*
- Office name (user-supplied)
- Notary's full name and commission number
- State / jurisdiction
- Year
- "Volume _____ of _____" line for multi-volume use
- Official seal placeholder: dashed circle (50 pt radius), labeled "OFFICIAL SEAL"
- Bottom bar with disclaimer:
  *"This journal is the exclusive property of the notary named above
  and is maintained in compliance with applicable state law."*

### 2. Instructions Page (Page 2)
Short paragraph explaining:
- How to use the journal
- Sequential numbering requirement (tamper prevention)
- What to do when the journal is full
- Storage and retention note

### 3. Entry Pages (one per notarial act, pre-numbered)

Each page has a full-width navy header bar, then labeled sections A–H:

#### HEADER BAR (navy #1B2A4A, white text)
```
NOTARIAL ACT RECORD                              Entry No. [XXX]
```
Entry number is **pre-printed** (001, 002, 003 … up to user-specified count).

#### SECTION A — Date & Time
```
Date: ________________________   Time: __________  [ ] AM  [ ] PM
```

#### SECTION B — Type of Notarial Act
Checkbox list (8×8 pt squares):
```
[ ] Acknowledgment    [ ] Oath / Affirmation    [ ] Copy Certification
[ ] Signature Witnessing    [ ] Jurat    [ ] Other: ___________________
```

#### SECTION C — Document Information
```
Document Type: ___________________________________________________
Document Date: ___________________________
Number of Pages: _________________
Description / Title: ______________________________________________
```

#### SECTION D — Signer Information
```
Full Name: _______________________________________________________
Address: ________________________________________________________
Phone / Email (optional): _________________________________________
ID Type:  [ ] Driver's License   [ ] Passport   [ ] State ID   [ ] Other: _______
ID Number: _________________________   Issued by: ________________
Expiration Date: _________________
Signer's Signature: _________________________________  Date: _______
```

#### SECTION E — Witness Information *(if applicable)*
```
Witness Name: ___________________________________________________
ID Number: ______________________   Signature: ___________________
```

#### SECTION F — Thumbprint
Placed on the **outer edge** of the page (away from the gutter/spine).
Minimum 1" × 1" (72 × 72 pt) box.
Label below: *"Signer's Right Thumbprint"*

#### SECTION G — Fees
```
Fee Charged: $_______________
Payment:  [ ] Cash   [ ] Check   [ ] Electronic Transfer   [ ] Waived
Check / Reference #: ___________________
```

#### SECTION H — Notary Certification & Signature Block
```
I certify that the signer personally appeared before me on the date stated above.

Notary Name: ____________________________________________________
Commission #: ___________________   Expiration: __________________
State of: ______________________   County of: ____________________
Notary Signature: ________________________________  Date: _________

               [  OFFICIAL SEAL  ]   ← dashed circle, 36 pt radius
```

#### SECTION I — Remarks
Three blank write-in lines for notes, refusals, or unusual circumstances.

---

### 4. Summary / Index Page (back of journal)

A pre-filled table listing all entry numbers for quick reference:

| Entry # | Date | Signer Name | Document Type | Act Type | Fee |
|---|---|---|---|---|---|
| 001 | | | | | |
| 002 | | | | | |
| ... | | | | | |

- One pre-numbered row per entry
- Row height ≥ 0.27" so notary can write legibly
- Spans as many pages as needed (typically 2–4 pages for 100 entries)

---

## Implementation Instructions

### Python Library Required
```bash
pip install reportlab --break-system-packages
```
Uses only ReportLab's built-in Helvetica fonts (English only — no external font files needed).

### Core Drawing Helpers
```python
from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas

W, H = 6 * inch, 9 * inch   # change to 5.5*inch, 8.5*inch for compact

INNER  = 0.625 * inch
OUTER  = 0.375 * inch
TOP    = 0.5   * inch
LINE_H = 0.27  * inch

NAVY  = (0.106, 0.165, 0.290)
STEEL = (0.227, 0.353, 0.549)
DGRAY = (0.200, 0.200, 0.200)
LGRAY = (0.800, 0.800, 0.800)

def draw_checkbox(c, x, y, size=8):
    c.setStrokeColorRGB(*DGRAY)
    c.setLineWidth(0.75)
    c.rect(x, y, size, size, fill=0, stroke=1)

def draw_writeline(c, x, y, width):
    c.setStrokeColorRGB(*DGRAY)
    c.setLineWidth(0.5)
    c.line(x, y, x + width, y)

def draw_section_bar(c, x, y, w, h, title):
    c.setFillColorRGB(*STEEL)
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 4, y + 3, title.upper())

def draw_seal(c, cx, cy, r=36):
    c.setStrokeColorRGB(*DGRAY)
    c.setLineWidth(1)
    c.setDash(4, 3)
    c.circle(cx, cy, r, fill=0, stroke=1)
    c.setDash()
    c.setFont("Helvetica", 7)
    c.drawCentredString(cx, cy - 4, "OFFICIAL SEAL")

def draw_thumbprint(c, x, y, size=72):
    c.setStrokeColorRGB(*DGRAY)
    c.setLineWidth(1)
    c.rect(x, y, size, size, fill=0, stroke=1)
    c.setFont("Helvetica", 6.5)
    c.drawCentredString(x + size/2, y + size/2 + 5, "RIGHT")
    c.drawCentredString(x + size/2, y + size/2 - 6, "THUMBPRINT")
    c.setFont("Helvetica", 6)
    c.drawCentredString(x + size/2, y - 9, "Signer's Right Thumbprint")
```

### Entry Page Function
```python
def draw_entry(c, num):
    is_odd   = num % 2 != 0
    lm       = INNER if is_odd else OUTER   # left margin
    rm       = OUTER if is_odd else INNER   # right margin
    uw       = W - lm - rm                  # usable width
    thumb_x  = (W - rm - 72) if is_odd else lm  # outer edge

    # ── Header ──
    c.setFillColorRGB(*NAVY)
    c.rect(0, H - TOP - 28, W, 28, fill=1, stroke=0)
    c.setFillColorRGB(1,1,1)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(lm, H - TOP - 19, "NOTARIAL ACT RECORD")
    c.drawRightString(W - rm, H - TOP - 19, f"Entry No. {num:03d}")

    y = H - TOP - 44

    # ── A: Date & Time ──
    draw_section_bar(c, lm, y - 13, uw, 13, "A — Date & Time")
    y -= 29
    c.setFont("Helvetica", 9); c.setFillColorRGB(0,0,0)
    c.drawString(lm, y, "Date:")
    draw_writeline(c, lm+34, y-2, 150)
    c.drawString(lm+200, y, "Time:")
    draw_writeline(c, lm+230, y-2, 55)
    draw_checkbox(c, lm+295, y-2); c.drawString(lm+306, y, "AM")
    draw_checkbox(c, lm+328, y-2); c.drawString(lm+339, y, "PM")
    y -= LINE_H + 4

    # ── B: Act Type ──
    draw_section_bar(c, lm, y - 13, uw, 13, "B — Type of Notarial Act")
    y -= 27
    acts = ["Acknowledgment", "Oath/Affirmation", "Copy Certification",
            "Sig. Witnessing", "Jurat"]
    cx = lm
    for act in acts:
        draw_checkbox(c, cx, y-2)
        c.setFont("Helvetica", 8); c.setFillColorRGB(0,0,0)
        c.drawString(cx+12, y, act)
        cx += c.stringWidth(act,"Helvetica",8) + 22
    y -= LINE_H
    draw_checkbox(c, lm, y-2); c.drawString(lm+12, y, "Other:")
    draw_writeline(c, lm+52, y-2, 100)
    y -= LINE_H + 4

    # ── C: Document Info ──
    draw_section_bar(c, lm, y-13, uw, 13, "C — Document Information")
    y -= 27
    for lbl in ["Document Type:", "Document Date:", "Description / Title:"]:
        c.setFont("Helvetica",9); c.setFillColorRGB(0,0,0)
        c.drawString(lm, y, lbl)
        lw = c.stringWidth(lbl,"Helvetica",9)
        draw_writeline(c, lm+lw+4, y-2, uw-lw-8)
        y -= LINE_H
    y -= 4

    # ── D: Signer Info ──
    draw_section_bar(c, lm, y-13, uw, 13, "D — Signer Information")
    y -= 27
    for lbl in ["Full Name:", "Address:", "ID Type & Number:", "Signer Signature:"]:
        c.setFont("Helvetica",9); c.setFillColorRGB(0,0,0)
        c.drawString(lm, y, lbl)
        lw = c.stringWidth(lbl,"Helvetica",9)
        draw_writeline(c, lm+lw+4, y-2, uw-lw-8)
        y -= LINE_H
    y -= 4

    # ── E: Witness (left portion) + F: Thumbprint (outer edge) ──
    draw_section_bar(c, lm, y-13, uw*0.62, 13, "E — Witness (if applicable)")
    y -= 27
    for lbl in ["Witness Name:", "Signature:"]:
        c.setFont("Helvetica",9); c.setFillColorRGB(0,0,0)
        c.drawString(lm, y, lbl)
        lw = c.stringWidth(lbl,"Helvetica",9)
        draw_writeline(c, lm+lw+4, y-2, uw*0.58-lw)
        y -= LINE_H
    draw_thumbprint(c, thumb_x, y - 30, size=72)
    y -= 4

    # ── G: Fees ──
    draw_section_bar(c, lm, y-13, uw, 13, "G — Fees")
    y -= 27
    c.setFont("Helvetica",9); c.setFillColorRGB(0,0,0)
    c.drawString(lm, y, "Fee Charged: $")
    draw_writeline(c, lm+88, y-2, 80)
    y -= LINE_H
    for p in ["Cash", "Check", "Electronic", "Waived"]:
        draw_checkbox(c, lm, y-2); c.drawString(lm+12, y, p)
        lm_next = lm + c.stringWidth(p,"Helvetica",9) + 28
        lm = lm_next
    lm = INNER if is_odd else OUTER   # reset
    y -= LINE_H + 4

    # ── H: Notary Block ──
    draw_section_bar(c, lm, y-13, uw, 13, "H — Notary Certification & Signature")
    y -= 22
    c.setFont("Helvetica",7.5); c.setFillColorRGB(0.3,0.3,0.3)
    c.drawString(lm, y, "I certify that the signer personally appeared before me on the date stated above.")
    y -= LINE_H
    for lbl in ["Notary Name:", "Commission # / Expiration:", "Notary Signature:"]:
        c.setFont("Helvetica",9); c.setFillColorRGB(0,0,0)
        c.drawString(lm, y, lbl)
        lw = c.stringWidth(lbl,"Helvetica",9)
        draw_writeline(c, lm+lw+4, y-2, uw*0.6-lw)
        y -= LINE_H
    draw_seal(c, W - rm - 54, y + LINE_H*1.8)
    y -= 8

    # ── I: Remarks ──
    draw_section_bar(c, lm, y-13, uw, 13, "I — Remarks")
    y -= 27
    for _ in range(3):
        draw_writeline(c, lm, y-2, uw)
        y -= LINE_H

    c.showPage()
```

### Index Page Function
```python
def draw_index(c, total):
    per_page = 28
    entry = 1
    cols  = [INNER, INNER+42, INNER+100, INNER+215, INNER+315, INNER+400]
    hdrs  = ["Entry #", "Date", "Signer Name", "Document Type", "Act Type", "Fee"]
    while entry <= total:
        c.setFillColorRGB(*NAVY)
        c.rect(0, H-50, W, 50, fill=1, stroke=0)
        c.setFillColorRGB(1,1,1)
        c.setFont("Helvetica-Bold", 13)
        c.drawCentredString(W/2, H-32, "JOURNAL INDEX / SUMMARY")
        y = H - 68
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColorRGB(*STEEL)
        for i, h in enumerate(hdrs):
            c.drawString(cols[i], y, h)
        y -= 14
        for _ in range(per_page):
            if entry > total: break
            c.setStrokeColorRGB(*LGRAY); c.setLineWidth(0.5)
            c.line(INNER, y-3, W-OUTER, y-3)
            c.setFont("Helvetica-Bold", 8); c.setFillColorRGB(0,0,0)
            c.drawString(cols[0], y, f"{entry:03d}")
            for xi in cols[1:]:
                next_x = cols[cols.index(xi)+1] if xi != cols[-1] else W-OUTER
                draw_writeline(c, xi, y-3, next_x - xi - 4)
            y -= LINE_H
            entry += 1
        c.showPage()
```

### Main Builder
```python
def build_journal(office, notary, commission, state, city, year, entries=100, trim="6x9"):
    global W, H
    W, H = (6*inch, 9*inch) if trim == "6x9" else (5.5*inch, 8.5*inch)
    path = "/mnt/user-data/outputs/notary_journal.pdf"
    c = canvas.Canvas(path, pagesize=(W, H))
    draw_cover(c, office, notary, commission, state, city, year)
    draw_instructions(c)
    for i in range(1, entries + 1):
        draw_entry(c, i)
    draw_index(c, entries)
    c.save()
    return path
```

---

## User Interaction Flow

1. Ask the user for:
   - **Office name**
   - **Notary's full name**
   - **Commission number**
   - **State / jurisdiction**
   - **City**
   - **Year** (default: current year)
   - **Number of entries** (default: 100; KDP books often use 200–400)
   - **Trim size**: 6"×9" (default) or 5.5"×8.5" (compact/travel)
2. Generate PDF and save to `/mnt/user-data/outputs/notary_journal.pdf`.
3. Present with `present_files`.
4. Offer adjustments: entry count, trim size, state-specific fields.

---

## KDP Publishing Notes

- Both 5.5"×8.5" and 6"×9" are standard KDP print trim sizes.
- Use black & white interior (most economical for a logbook).
- KDP requires at least 24 pages minimum.
- The 0.625" inner margin accounts for KDP's perfect-binding glue.
- Pre-printed sequential numbers comply with state tamper-prevention laws.
- Recommended entry count: 100–200 for good value-to-price ratio.

## KDP Backend Keywords (ready to paste into KDP listing)
1. `california texas florida state compliant rules`
2. `mobile public loan signing agent supplies bag`
3. `sequential numbered records tamper proof logbook`
4. `official notarial act register ledger log diary`
5. `real estate closing legal document tracking book`
6. `compact travel size pocket portable small desk`
7. `updated 2026 guidelines professional accessories`
