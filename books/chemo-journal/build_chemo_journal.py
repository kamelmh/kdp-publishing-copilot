#!/usr/bin/env python3
"""
Chemotherapy Treatment Journal — Interior PDF Builder
Builds 130-page interior for Amazon KDP (8.5 × 11 inches)
Based on Chemo-Journal-Content-Specification.md
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Register Georgia font family from Windows system fonts
FONTS_DIR = "C:/Windows/Fonts"
pdfmetrics.registerFont(TTFont("Georgia", f"{FONTS_DIR}/georgia.ttf"))
pdfmetrics.registerFont(TTFont("Georgia-Bold", f"{FONTS_DIR}/georgiab.ttf"))
pdfmetrics.registerFont(TTFont("Georgia-Italic", f"{FONTS_DIR}/georgiai.ttf"))
pdfmetrics.registerFont(TTFont("Georgia-BoldItalic", f"{FONTS_DIR}/georgiaz.ttf"))

# === CONSTANTS ===
PAGE_W, PAGE_H = letter  # 612 × 792 pts
MARGIN = 0.6 * inch
CONTENT_W = PAGE_W - 2 * MARGIN
CONTENT_H = PAGE_H - 2 * MARGIN

# Colors from spec
IVORY = HexColor("#FBF7F1")
SAGE = HexColor("#8CA396")
BLUSH = HexColor("#E3B8B0")
SLATE = HexColor("#A9BFC9")
CHARCOAL = HexColor("#3F3A36")
TAUPE = HexColor("#D8D0C7")
WHITE = HexColor("#FFFFFF")

# Typography sizes
HEADER_PT = 21
SECTION_PT = 12
FIELD_LABEL_PT = 11
BODY_PT = 11
FOOTNOTE_PT = 9
SMALL_PT = 10

# Line spacing
WRITING_LINE_SPACING = 0.4 * inch  # ~29pt, generous for fatigue/neuropathy
CHECKBOX_SIZE = 0.18 * inch

# Output
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PDF = os.path.join(OUTPUT_DIR, "Chemo-Journal-Interior.pdf")


def draw_page_bg(c, color=IVORY):
    """Fill page background with color."""
    c.setFillColor(color)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)


def draw_header(c, text, y, color=CHARCOAL, font_size=HEADER_PT, accent=None):
    """Draw a page header, returns y position below header."""
    c.setFont("Georgia-Bold", font_size)
    c.setFillColor(color)
    c.drawString(MARGIN, y, text)
    y -= 6
    if accent:
        c.setStrokeColor(accent)
        c.setLineWidth(1.5)
        c.line(MARGIN, y, PAGE_W - MARGIN, y)
        y -= 8
    return y - font_size


def draw_section_band(c, text, y, accent=SAGE, width=CONTENT_W):
    """Draw a colored section band with white text."""
    band_h = 22
    c.setFillColor(accent)
    c.roundRect(MARGIN, y - band_h + 4, width, band_h, 3, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Georgia-Bold", SECTION_PT)
    c.drawString(MARGIN + 8, y - band_h + 10, text)
    return y - band_h - 6


def draw_field(c, label, x, y, field_w=2.5 * inch, value=""):
    """Draw a labeled field with underline. Returns y below field."""
    c.setFont("Georgia", FIELD_LABEL_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(x, y, label)
    label_w = c.stringWidth(label, "Georgia", FIELD_LABEL_PT)
    line_start = x + label_w + 6
    line_end = x + field_w
    if line_end > line_start:
        c.setStrokeColor(TAUPE)
        c.setLineWidth(0.5)
        c.line(line_start, y - 2, line_end, y - 2)
    return y - 20


def draw_field_row(c, fields, y, row_w=CONTENT_W):
    """Draw multiple fields on one row. fields = [(label, width), ...]"""
    x = MARGIN
    for label, w in fields:
        y_out = draw_field(c, label, x, y, field_w=w)
        x += w + 12
    return y - 20


def draw_checkbox(c, label, x, y, checked=False):
    """Draw a checkbox with label. Returns y below."""
    c.setStrokeColor(CHARCOAL)
    c.setLineWidth(0.8)
    c.rect(x, y - 2, CHECKBOX_SIZE, CHECKBOX_SIZE, fill=0, stroke=1)
    c.setFont("Georgia", SMALL_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(x + CHECKBOX_SIZE + 4, y, label)
    return y - CHECKBOX_SIZE - 4


def draw_checkbox_row(c, items, x, y, col_w=2.0 * inch):
    """Draw checkboxes in columns. items = list of label strings."""
    col_x = x
    row_h = CHECKBOX_SIZE + 6
    for i, item in enumerate(items):
        draw_checkbox(c, item, col_x, y)
        col_x += col_w
        if col_x + col_w > MARGIN + CONTENT_W:
            col_x = x
            y -= row_h
    return y


def draw_writing_lines(c, x, y, width, count, spacing=WRITING_LINE_SPACING):
    """Draw ruled writing lines. Returns y below last line.
    Stops early if lines would go below page margin."""
    c.setStrokeColor(TAUPE)
    c.setLineWidth(0.4)
    drawn = 0
    for _ in range(count):
        if y - spacing < MARGIN:
            break
        c.line(x, y, x + width, y)
        y -= spacing
        drawn += 1
    return y


def draw_table(c, headers, rows, y, col_widths=None, row_h=20):
    """Draw a table with headers and rows. Returns y below table."""
    n_cols = len(headers)
    if col_widths is None:
        col_w = CONTENT_W / n_cols
        col_widths = [col_w] * n_cols

    # Header row
    c.setFillColor(SLATE)
    c.rect(MARGIN, y - row_h + 4, CONTENT_W, row_h, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Georgia-Bold", SMALL_PT)
    x = MARGIN
    for i, h in enumerate(headers):
        c.drawString(x + 4, y - row_h + 10, h)
        x += col_widths[i]
    y -= row_h + 2

    # Data rows
    c.setFillColor(CHARCOAL)
    c.setFont("Georgia", SMALL_PT)
    for row in rows:
        c.setStrokeColor(TAUPE)
        c.setLineWidth(0.3)
        c.line(MARGIN, y - 2, MARGIN + CONTENT_W, y - 2)
        x = MARGIN
        for i, cell in enumerate(row):
            c.drawString(x + 4, y - 12, str(cell))
            x += col_widths[i]
        y -= row_h
    return y


def draw_empty_table_rows(c, count, y, row_h=20):
    """Draw empty table rows with dividing lines. Stops if rows would overflow page."""
    for _ in range(count):
        if y - row_h < MARGIN:
            break
        c.setStrokeColor(TAUPE)
        c.setLineWidth(0.3)
        c.line(MARGIN, y - 2, MARGIN + CONTENT_W, y - 2)
        y -= row_h
    return y


# ============================================================
# FRONT MATTER PAGES
# ============================================================

def build_title_page(c):
    """Page 1: Title / Ownership page."""
    draw_page_bg(c)
    y = PAGE_H - 1.8 * inch

    # Main header
    c.setFont("Georgia-Bold", 28)
    c.setFillColor(CHARCOAL)
    c.drawCentredString(PAGE_W / 2, y, "Chemotherapy Treatment Journal")
    y -= 30

    # Accent line
    c.setStrokeColor(SAGE)
    c.setLineWidth(2)
    c.line(PAGE_W / 2 - 1.5 * inch, y, PAGE_W / 2 + 1.5 * inch, y)
    y -= 30

    # Subtitle
    c.setFont("Georgia-Italic", 14)
    c.setFillColor(CHARCOAL)
    c.drawCentredString(PAGE_W / 2, y, "A Personal Tracker for Your Journey")
    y -= 50

    # "This Journal Belongs To"
    c.setFont("Georgia-Bold", 18)
    c.drawCentredString(PAGE_W / 2, y, "This Journal Belongs To")
    y -= 35

    # Fields
    fields = ["Name", "Start Date", "This journal was given to me by"]
    for f in fields:
        c.setFont("Georgia", FIELD_LABEL_PT)
        c.setFillColor(CHARCOAL)
        c.drawString(MARGIN + 0.8 * inch, y, f + ":")
        c.setStrokeColor(TAUPE)
        c.setLineWidth(0.5)
        line_x = MARGIN + 0.8 * inch + c.stringWidth(f + ": ", "Georgia", FIELD_LABEL_PT)
        c.line(line_x, y - 2, PAGE_W - MARGIN - 0.8 * inch, y - 2)
        y -= 28

    # Gift line (optional)
    y -= 10
    c.setFont("Georgia-Italic", 10)
    c.setFillColor(TAUPE)
    c.drawCentredString(PAGE_W / 2, y, "(because ___)")
    y -= 40

    # Graphic placeholder (small, centered)
    c.setFont("Georgia-Italic", 9)
    c.setFillColor(TAUPE)
    c.drawCentredString(PAGE_W / 2, y, "[Line art: Patient illustration]")

    # Copyright block at bottom
    y_bottom = MARGIN + 40
    c.setFont("Georgia", 8)
    c.setFillColor(TAUPE)
    c.drawCentredString(PAGE_W / 2, y_bottom + 12, "Meridian Press")
    c.drawCentredString(PAGE_W / 2, y_bottom, "© 2026 All Rights Reserved")
    c.drawCentredString(PAGE_W / 2, y_bottom - 12,
                        "This journal is a personal tracking tool and does not provide medical advice.")
    c.drawCentredString(PAGE_W / 2, y_bottom - 24,
                        "Always follow the guidance of your healthcare team.")

    c.showPage()


def build_how_to_use(c):
    """Page 2: How to Use This Journal."""
    draw_page_bg(c)
    y = PAGE_H - MARGIN
    y = draw_header(c, "Before You Begin", y, accent=SAGE)

    c.setFont("Georgia-Italic", 13)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN, y,
                 "You don't have to fill in every box. This book works for you, not the other way around.")
    y -= 30

    paragraphs = [
        "This journal is organized into color-coded sections to help you find what you need quickly:",
        "  • Sage green (●) — Treatment Tracking: chemo cycles, daily symptoms, medications, appointments",
        "  • Soft blue (●) — Reference & Logistics: care team, insurance, lab results, doctor questions",
        "  • Dusty rose (●) — Emotional Support: affirmations, reflections, gratitude",
        "",
        "Each page has an entry number instead of a page number, so you can skip around,",
        "use pages out of order, or come back to ones you skipped — no rules.",
        "",
        "A few things to know:",
        "  • This is a tracking tool, not medical advice. Always follow your care team's guidance.",
        "  • It's okay to skip days. It's okay to write messily. It's okay to leave things blank.",
        "  • The symptom checklist on the Quick Reference page (pages 8–9) is cross-referenced",
        "    with the Daily Symptom Log, so the two work as one system.",
        "  • The checkboxes are pre-labeled so you don't have to invent categories while tired.",
        "",
        "However this goes, you are not walking through it unseen."
    ]

    c.setFont("Georgia", BODY_PT)
    c.setFillColor(CHARCOAL)
    for line in paragraphs:
        c.drawString(MARGIN, y, line)
        y -= 18

    c.showPage()


def build_diagnosis_snapshot(c):
    """Page 3: My Diagnosis & Treatment Snapshot."""
    draw_page_bg(c)
    y = PAGE_H - MARGIN
    y = draw_header(c, "My Diagnosis & Treatment Plan", y, accent=SLATE)

    fields = [
        ("Diagnosis", 4.5 * inch),
        ("Date of Diagnosis", 4.5 * inch),
        ("Stage (if known)", 4.5 * inch),
        ("Oncologist", 4.5 * inch),
        ("Treatment Center", 4.5 * inch),
        ("Regimen Name", 4.5 * inch),
        ("Planned Number of Cycles", 4.5 * inch),
        ("Cycle Length", 4.5 * inch),
        ("Treatment Start Date", 4.5 * inch),
        ("Estimated End Date", 4.5 * inch),
    ]

    for label, w in fields:
        y = draw_field(c, label, MARGIN, y, field_w=w)

    y -= 10
    c.setFont("Georgia", FIELD_LABEL_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN, y, "Treatment Goal")
    y -= 6
    c.setFont("Georgia-Italic", 9)
    c.setFillColor(TAUPE)
    c.drawString(MARGIN + 4, y,
                 "(curative, maintenance, palliative — write what your team told you)")
    y -= 16
    draw_writing_lines(c, MARGIN, y, CONTENT_W, 2)

    c.showPage()


def build_care_team(c):
    """Page 4: Care Team Directory."""
    draw_page_bg(c)
    y = PAGE_H - MARGIN
    y = draw_header(c, "My Care Team", y, accent=SLATE)

    headers = ["Role", "Name", "Phone", "Email / Notes"]
    col_widths = [1.6 * inch, 1.5 * inch, 1.3 * inch, CONTENT_W - 4.4 * inch]
    rows = [
        ("Oncologist", "", "", ""),
        ("Oncology Nurse / Navigator", "", "", ""),
        ("Infusion Nurse", "", "", ""),
        ("Primary Care Doctor", "", "", ""),
        ("Pharmacist", "", "", ""),
        ("Social Worker / Counselor", "", "", ""),
        ("", "", "", ""),
        ("", "", "", ""),
        ("", "", "", ""),
    ]
    y = draw_table(c, headers, rows, y, col_widths)

    c.showPage()


def build_emergency_contacts(c):
    """Page 5: Emergency Contacts & When to Call for Help."""
    draw_page_bg(c)
    y = PAGE_H - MARGIN
    y = draw_header(c, "Emergency Contacts", y, accent=BLUSH)

    # Personal contacts
    c.setFont("Georgia-Bold", FIELD_LABEL_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN, y, "Personal Contacts")
    y -= 16

    for i in range(1, 3):
        c.setFont("Georgia", FIELD_LABEL_PT)
        c.drawString(MARGIN, y, f"Contact {i}:")
        y = draw_field(c, "Name", MARGIN + 0.7 * inch, y, field_w=2 * inch)
        y = draw_field(c, "Relationship", MARGIN + 0.7 * inch, y, field_w=2 * inch)
        y = draw_field(c, "Phone", MARGIN + 0.7 * inch, y, field_w=2 * inch)
        y = draw_field(c, "Alt Phone", MARGIN + 0.7 * inch, y, field_w=2 * inch)
        y -= 8

    # Emergency callout box
    y -= 10
    box_h = 180
    c.setStrokeColor(BLUSH)
    c.setLineWidth(1.5)
    c.roundRect(MARGIN, y - box_h, CONTENT_W, box_h, 5, fill=0, stroke=1)

    c.setFont("Georgia-Bold", 12)
    c.setFillColor(BLUSH)
    c.drawString(MARGIN + 10, y - 18, "Call your care team or 911 if you have:")

    emergency_items = [
        "Fever of 100.4°F (38°C) or higher",
        "Uncontrolled bleeding",
        "Severe shortness of breath",
        "Signs of an allergic reaction (swelling, difficulty breathing, rash)",
        "Confusion or fainting",
        "Pain not relieved by your medication",
    ]
    ey = y - 36
    c.setFont("Georgia", SMALL_PT)
    c.setFillColor(CHARCOAL)
    for item in emergency_items:
        c.drawString(MARGIN + 20, ey, "•  " + item)
        ey -= 16

    c.setFont("Georgia-Italic", 8)
    c.setFillColor(TAUPE)
    c.drawString(MARGIN + 10, y - box_h + 14,
                 "Confirm your exact thresholds with your oncology team; every regimen is different.")

    c.showPage()


def build_insurance(c):
    """Page 6: Insurance & Billing Quick Reference."""
    draw_page_bg(c)
    y = PAGE_H - MARGIN
    y = draw_header(c, "Insurance & Billing", y, accent=SLATE)

    fields = [
        ("Insurance Provider", 4.5 * inch),
        ("Policy / Member ID", 4.5 * inch),
        ("Group #", 4.5 * inch),
        ("Customer Service Phone", 4.5 * inch),
        ("Prior Authorization Contact", 4.5 * inch),
        ("Hospital Financial Counselor", 4.5 * inch),
        ("Copay Per Visit", 4.5 * inch),
    ]
    for label, w in fields:
        y = draw_field(c, label, MARGIN, y, field_w=w)

    y -= 10
    c.setFont("Georgia", FIELD_LABEL_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN, y, "Notes on Coverage")
    y -= 6
    draw_writing_lines(c, MARGIN, y, CONTENT_W, 3)
    y -= 10

    # Bills tracking table
    y = draw_section_band(c, "Bills & Statements", y, accent=SLATE)
    headers = ["Date", "From", "Amount", "Status"]
    col_widths = [1.2 * inch, 2.2 * inch, 1.2 * inch, CONTENT_W - 4.6 * inch]
    y = draw_table(c, headers, [("", "", "", "")] * 6, y, col_widths)

    c.showPage()


# ============================================================
# QUICK-REFERENCE TOOLS
# ============================================================

def build_symptom_reference(c, page_num):
    """Pages 7-8: Symptom & Side-Effect Quick Reference (2-page spread)."""
    # Page 1: Header + first 3 categories
    draw_page_bg(c)
    y = PAGE_H - MARGIN
    y = draw_header(c, "What to Watch For", y, accent=SAGE)

    # Severity key
    c.setFont("Georgia-Bold", SMALL_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN, y, "Severity:  None  ·  Mild  ·  Moderate  ·  Severe  ·  Call my care team")
    y -= 18

    categories_p1 = [
        ("Digestive", [
            "Nausea", "Vomiting", "Loss of appetite", "Mouth sores",
            "Taste changes", "Diarrhea", "Constipation"
        ]),
        ("Skin, Hair & Nails", [
            "Hair loss", "Dry or itchy skin", "Nail changes", "Sun sensitivity"
        ]),
        ("Energy & Sleep", [
            "Fatigue", "Trouble sleeping", "Needing more rest than usual"
        ]),
    ]

    for cat_name, items in categories_p1:
        y = draw_section_band(c, cat_name, y, accent=SAGE, width=CONTENT_W / 2 - 6)
        # Split items into two balanced columns
        mid = (len(items) + 1) // 2
        col1 = items[:mid]
        col2 = items[mid:]
        col_w = (CONTENT_W / 2 - 20) / 2
        x1 = MARGIN
        x2 = MARGIN + CONTENT_W / 2 + 10
        iy1 = y
        iy2 = y
        for item in col1:
            draw_checkbox(c, item, x1, iy1)
            iy1 -= CHECKBOX_SIZE + 6
        for item in col2:
            draw_checkbox(c, item, x2, iy2)
            iy2 -= CHECKBOX_SIZE + 6
        y = min(iy1, iy2) - 10

    c.showPage()

    # Page 2: Remaining categories
    draw_page_bg(c)
    y = PAGE_H - MARGIN
    y = draw_header(c, "What to Watch For (continued)", y, accent=SAGE)

    c.setFont("Georgia-Bold", SMALL_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN, y, "Severity:  None  ·  Mild  ·  Moderate  ·  Severe  ·  Call my care team")
    y -= 18

    categories_p2 = [
        ("Nerve & Muscle", [
            "Numbness or tingling (hands/feet)", "Joint or muscle aches"
        ]),
        ("Emotional & Cognitive", [
            "Anxiety", "Low mood", "Irritability", "Chemo brain / trouble focusing"
        ]),
        ("Other", [
            "Fever or chills", "Easy bruising or bleeding", "Shortness of breath"
        ]),
    ]

    for cat_name, items in categories_p2:
        y = draw_section_band(c, cat_name, y, accent=SAGE, width=CONTENT_W / 2 - 6)
        mid = (len(items) + 1) // 2
        col1 = items[:mid]
        col2 = items[mid:]
        col_w = (CONTENT_W / 2 - 20) / 2
        x1 = MARGIN
        x2 = MARGIN + CONTENT_W / 2 + 10
        iy1 = y
        iy2 = y
        for item in col1:
            draw_checkbox(c, item, x1, iy1)
            iy1 -= CHECKBOX_SIZE + 6
        for item in col2:
            draw_checkbox(c, item, x2, iy2)
            iy2 -= CHECKBOX_SIZE + 6
        y = min(iy1, iy2) - 10

    c.showPage()


def build_medication_master(c):
    """Page 9: Medication Master List."""
    draw_page_bg(c)
    y = PAGE_H - MARGIN
    y = draw_header(c, "My Medications at a Glance", y, accent=SLATE)

    headers = ["Medication", "Purpose", "Dose", "Frequency", "Doctor", "Notes"]
    col_widths = [1.1 * inch, 0.9 * inch, 0.7 * inch, 0.8 * inch, 0.9 * inch, CONTENT_W - 4.4 * inch]
    rows = [("", "", "", "", "", "")] * 16
    y = draw_table(c, headers, rows, y, col_widths)

    c.showPage()


def build_doctor_questions(c):
    """Pages 10-12: Doctor Questions Checklist (3 identical templates)."""
    questions = {
        "About Treatment": [
            "What type of chemotherapy am I receiving and how does it work?",
            "How many cycles are planned, and how long is each?",
            "How will we know if treatment is working?",
            "What should I do if I miss a dose or session?",
        ],
        "About Side Effects": [
            "What side effects are most common with this regimen?",
            "Which side effects need an immediate call?",
            "What can I take for nausea or pain, and what should I avoid?",
            "Will this affect my ability to work, drive, or care for myself?",
        ],
        "About Daily Life": [
            "Are there foods or activities I should avoid?",
            "Can I exercise, and how much?",
            "Is it safe to be around others, including children or pets?",
            "What precautions should I take with my immune system?",
        ],
        "About Logistics": [
            "Who do I contact after hours or on weekends?",
            "What should I bring to each appointment?",
            "Will I need labs before every session?",
            "How should I plan transportation for treatment days?",
        ],
        "Emotional / Support": [
            "Is what I'm feeling normal at this stage?",
            "Are there support groups or counselors you'd recommend?",
            "How can my family or caregiver best support me?",
        ],
    }

    for template_num in range(3):
        draw_page_bg(c)
        y = PAGE_H - MARGIN
        y = draw_header(c, "Questions for My Next Appointment", y, accent=SLATE)

        # Date field
        y = draw_field(c, "Appointment Date", MARGIN, y, field_w=3 * inch)
        y -= 6

        for cat_name, q_list in questions.items():
            c.setFont("Georgia-Bold", FIELD_LABEL_PT)
            c.setFillColor(SAGE)
            c.drawString(MARGIN, y, cat_name)
            y -= 12

            for q in q_list:
                # Checkbox
                c.setStrokeColor(CHARCOAL)
                c.setLineWidth(0.6)
                c.rect(MARGIN, y - 2, CHECKBOX_SIZE, CHECKBOX_SIZE, fill=0, stroke=1)
                # Question text
                c.setFont("Georgia", SMALL_PT)
                c.setFillColor(CHARCOAL)
                c.drawString(MARGIN + CHECKBOX_SIZE + 5, y, q)
                y -= 12
                # Answer line
                c.setStrokeColor(TAUPE)
                c.setLineWidth(0.3)
                c.line(MARGIN + CHECKBOX_SIZE + 5, y, PAGE_W - MARGIN, y)
                y -= 10
            y -= 2

        # Blank lines for own questions
        c.setFont("Georgia-Bold", FIELD_LABEL_PT)
        c.setFillColor(SAGE)
        c.drawString(MARGIN, y, "My Own Questions:")
        y -= 10
        for _ in range(3):
            c.setStrokeColor(TAUPE)
            c.setLineWidth(0.3)
            c.line(MARGIN, y, PAGE_W - MARGIN, y)
            y -= 18

        c.showPage()


# ============================================================
# CALENDARS
# ============================================================

def build_monthly_calendar(c, month_num):
    """Monthly undated calendar page."""
    draw_page_bg(c)
    y = PAGE_H - MARGIN

    # Header with month/year fields
    c.setFont("Georgia-Bold", HEADER_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN, y, f"Month: ________    Year: ________")
    y -= 16

    # Legend
    c.setFont("Georgia", SMALL_PT)
    c.setFillColor(CHARCOAL)
    legend_y = y
    c.setStrokeColor(SAGE)
    c.setFillColor(SAGE)
    c.rect(MARGIN, legend_y - 3, 8, 8, fill=1, stroke=0)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN + 12, legend_y, "Chemo Day")
    c.setStrokeColor(SLATE)
    c.setFillColor(SLATE)
    c.rect(MARGIN + 90, legend_y - 3, 8, 8, fill=1, stroke=0)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN + 102, legend_y, "Appointment")
    c.setStrokeColor(BLUSH)
    c.setFillColor(BLUSH)
    c.rect(MARGIN + 210, legend_y - 3, 8, 8, fill=1, stroke=0)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN + 222, legend_y, "Lab Draw")
    y -= 20

    # Calendar grid (7 cols × 5 rows)
    col_w = CONTENT_W / 7
    row_h = (y - MARGIN - 50) / 5  # Leave room for notes at bottom

    # Day headers
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    c.setFont("Georgia-Bold", SMALL_PT)
    c.setFillColor(SLATE)
    for i, d in enumerate(days):
        c.drawCentredString(MARGIN + i * col_w + col_w / 2, y, d)
    y -= 10

    # Grid cells
    c.setStrokeColor(TAUPE)
    c.setLineWidth(0.4)
    for row in range(5):
        for col in range(7):
            x = MARGIN + col * col_w
            cell_y = y - row * row_h
            c.rect(x, cell_y - row_h, col_w, row_h, fill=0, stroke=1)

    y -= 5 * row_h + 8

    # Notes strip
    c.setFont("Georgia-Bold", FIELD_LABEL_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN, y, "Notes:")
    y -= 6
    draw_writing_lines(c, MARGIN, y, CONTENT_W, 2, spacing=18)

    c.showPage()


# ============================================================
# TREATMENT TRACKING
# ============================================================

def build_chemo_cycle_tracker(c, cycle_num):
    """Chemo Cycle Tracker page."""
    draw_page_bg(c)
    y = PAGE_H - MARGIN
    y = draw_header(c, f"Cycle #{cycle_num} of ___", y, accent=SAGE)

    # Top fields
    fields_top = [("Date", 2.5 * inch), ("Infusion Location", 2.5 * inch)]
    y = draw_field_row(c, fields_top, y)

    y = draw_field(c, "Drugs Administered (from my chart)", MARGIN, y, field_w=CONTENT_W)
    y = draw_field(c, "Pre-Medications Given", MARGIN, y, field_w=CONTENT_W)
    y = draw_field(c, "Infusion Nurse", MARGIN, y, field_w=3 * inch)
    y -= 8

    # Energy level
    c.setFont("Georgia-Bold", FIELD_LABEL_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN, y, "Energy Level:  Before (1–10) → After (1–10)")
    y -= 6
    c.setStrokeColor(TAUPE)
    c.setLineWidth(0.5)
    c.line(MARGIN, y, MARGIN + 3 * inch, y)
    y -= 16

    # How I felt during infusion
    c.setFont("Georgia-Bold", FIELD_LABEL_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN, y, "How I Felt During Infusion:")
    y -= 6
    y = draw_writing_lines(c, MARGIN, y, CONTENT_W, 4)

    y -= 8

    # Symptoms in following 48 hours
    c.setFont("Georgia-Bold", FIELD_LABEL_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN, y, "Symptoms in the Following 48 Hours:")
    y -= 14

    symptom_cats = [
        ("Digestive", ["Nausea", "Vomiting", "Appetite loss", "Mouth sores"]),
        ("Energy", ["Fatigue", "Sleep issues", "Low mood"]),
        ("Other", ["Pain", "Numbness", "Fever", "Skin changes"]),
    ]

    for cat_name, items in symptom_cats:
        c.setFont("Georgia-Bold", 9)
        c.setFillColor(SAGE)
        c.drawString(MARGIN, y, cat_name + ":")
        cat_w = c.stringWidth(cat_name + ": ", "Georgia-Bold", 9)
        ix = MARGIN + cat_w
        for item in items:
            item_w = c.stringWidth(item, "Georgia", 8) + CHECKBOX_SIZE + 10
            # Wrap to next line if item won't fit
            if ix + item_w > PAGE_W - MARGIN:
                ix = MARGIN + cat_w
                y -= 12
            c.setStrokeColor(CHARCOAL)
            c.setLineWidth(0.5)
            c.rect(ix, y - 2, CHECKBOX_SIZE - 4, CHECKBOX_SIZE - 4, fill=0, stroke=1)
            c.setFont("Georgia", 8)
            c.setFillColor(CHARCOAL)
            c.drawString(ix + CHECKBOX_SIZE, y, item)
            ix += item_w
        y -= 14

    # Next cycle & notes
    y -= 4
    y = draw_field(c, "Next Cycle Date", MARGIN, y, field_w=3 * inch)
    y = draw_field(c, "Notes", MARGIN, y, field_w=CONTENT_W)

    c.showPage()


def build_daily_symptom_log(c, day_num):
    """Daily Symptom Log page."""
    draw_page_bg(c)
    y = PAGE_H - MARGIN
    y = draw_header(c, f"Day #{day_num}", y, accent=SAGE)

    # Top strip
    y = draw_field(c, "Date", MARGIN, y, field_w=2 * inch)
    y = draw_field(c, "Cycle Day (Day ___ of Cycle ___)", MARGIN + 2.2 * inch, y, field_w=3 * inch)
    y -= 4

    # Overall feeling
    c.setFont("Georgia-Bold", FIELD_LABEL_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN, y, "Overall Feeling Today (1–10):  ① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩")
    y -= 18

    # Symptom grid
    c.setFont("Georgia-Bold", FIELD_LABEL_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN, y, "Symptoms")
    y -= 4

    # Severity key
    c.setFont("Georgia", 8)
    c.setFillColor(TAUPE)
    c.drawString(MARGIN, y - 8, "None    Mild    Moderate    Severe    Call team")
    y -= 18

    symptoms = [
        "Nausea / Vomiting", "Appetite changes", "Mouth sores", "Taste changes",
        "Fatigue", "Trouble sleeping", "Hair loss", "Skin / nail changes",
        "Numbness / tingling", "Joint / muscle aches", "Anxiety / low mood",
        "Chemo brain", "Fever / chills", "Bruising / bleeding", "Shortness of breath",
        "Constipation / Diarrhea",
    ]

    col_w = CONTENT_W / 2
    x1 = MARGIN
    x2 = MARGIN + col_w
    for i, sym in enumerate(symptoms):
        cx = x1 if i < 8 else x2
        sy = y - (i % 8) * 14
        c.setFont("Georgia", SMALL_PT)
        c.setFillColor(CHARCOAL)
        c.drawString(cx, sy, sym)
        # Severity dots
        for j in range(5):
            c.setStrokeColor(TAUPE)
            c.setLineWidth(0.4)
            dot_x = cx + col_w - 70 + j * 14
            c.circle(dot_x, sy + 2, 4, fill=0, stroke=1)

    y -= 8 * 14 + 10

    # Bottom section
    y = draw_field(c, "Sleep Hours", MARGIN, y, field_w=1.5 * inch)
    y = draw_field(c, "Mood", MARGIN + 2 * inch, y, field_w=1.5 * inch)
    y -= 4

    c.setFont("Georgia-Italic", FIELD_LABEL_PT)
    c.setFillColor(SAGE)
    c.drawString(MARGIN, y, "One good thing today:")
    y -= 6
    draw_writing_lines(c, MARGIN, y, CONTENT_W, 1, spacing=20)

    c.showPage()


def build_medication_log(c, entry_num):
    """Medication & Dose Log page."""
    draw_page_bg(c)
    y = PAGE_H - MARGIN
    y = draw_header(c, "Medication Log", y, accent=SAGE)

    y = draw_field(c, "Date", MARGIN, y, field_w=3 * inch)
    y -= 6

    headers = ["Time", "Medication", "Dose", "Purpose", "How I Felt After"]
    col_widths = [0.8 * inch, 1.3 * inch, 0.7 * inch, 1.0 * inch, CONTENT_W - 3.8 * inch]
    rows = [("", "", "", "", "")] * 10
    y = draw_table(c, headers, rows, y, col_widths, row_h=22)

    y -= 8

    # Checkboxes
    c.setFont("Georgia-Bold", FIELD_LABEL_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN, y, "Taken as scheduled:")
    draw_checkbox(c, "Yes", MARGIN + 130, y)
    draw_checkbox(c, "No", MARGIN + 170, y)
    y -= 16
    c.drawString(MARGIN, y, "Missed a dose:")
    draw_checkbox(c, "Yes", MARGIN + 100, y)
    draw_checkbox(c, "No", MARGIN + 140, y)
    y -= 18

    c.setFont("Georgia-Italic", FIELD_LABEL_PT)
    c.setFillColor(SAGE)
    c.drawString(MARGIN, y, "Question for my pharmacist:")
    y -= 6
    draw_writing_lines(c, MARGIN, y, CONTENT_W, 2, spacing=18)

    c.showPage()


def build_appointment_log(c, entry_num):
    """Appointment Log page."""
    draw_page_bg(c)
    y = PAGE_H - MARGIN
    y = draw_header(c, f"Appointment Log — Entry #{entry_num}", y, accent=SLATE)

    y = draw_field(c, "Date & Time", MARGIN, y, field_w=3 * inch)
    y = draw_field(c, "Type of Visit", MARGIN, y, field_w=3 * inch)
    y -= 4

    # Visit type checkboxes
    visit_types = ["Oncologist", "Infusion", "Scan", "Lab Draw", "Other"]
    c.setFont("Georgia", SMALL_PT)
    c.setFillColor(CHARCOAL)
    x = MARGIN
    for vt in visit_types:
        draw_checkbox(c, vt, x, y)
        x += 1.2 * inch
    y -= 18

    y = draw_field(c, "Who I Saw", MARGIN, y, field_w=4 * inch)
    y -= 4

    c.setFont("Georgia-Bold", FIELD_LABEL_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN, y, "What We Discussed:")
    y -= 6
    y = draw_writing_lines(c, MARGIN, y, CONTENT_W, 6)

    c.setFont("Georgia-Bold", FIELD_LABEL_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN, y, "Questions I Asked & Answers:")
    y -= 6
    y = draw_writing_lines(c, MARGIN, y, CONTENT_W, 4)

    y -= 6
    y = draw_field(c, "Next Steps", MARGIN, y, field_w=CONTENT_W)
    y = draw_field(c, "Next Appointment Date", MARGIN, y, field_w=3 * inch)

    c.showPage()


# ============================================================
# WELLNESS TRACKING
# ============================================================

def build_hydration_nutrition(c, entry_num):
    """Hydration & Nutrition Log page."""
    draw_page_bg(c)
    y = PAGE_H - MARGIN
    y = draw_header(c, "Hydration & Nutrition", y, accent=SAGE)

    y = draw_field(c, "Date", MARGIN, y, field_w=3 * inch)
    y -= 6

    # Water tracker
    c.setFont("Georgia-Bold", FIELD_LABEL_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN, y, "Water Intake (8oz glasses):")
    y -= 12
    glass_x = MARGIN
    for i in range(10):
        c.setStrokeColor(SLATE)
        c.setLineWidth(0.8)
        c.circle(glass_x + 10, y + 4, 8, fill=0, stroke=1)
        c.setFont("Georgia", 7)
        c.setFillColor(TAUPE)
        c.drawCentredString(glass_x + 10, y - 8, str(i + 1))
        glass_x += 24
    y -= 28

    # Meals
    c.setFont("Georgia-Bold", FIELD_LABEL_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN, y, "Meals:")
    y -= 12
    meals = ["Breakfast", "Lunch", "Dinner", "Snacks"]
    for meal in meals:
        y = draw_field(c, meal, MARGIN, y, field_w=CONTENT_W)
    y -= 6

    # Appetite
    c.setFont("Georgia-Bold", FIELD_LABEL_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN, y, "Appetite Level:")
    appetite_options = ["None", "Some", "Normal", "Good"]
    ax = MARGIN + 100
    for opt in appetite_options:
        draw_checkbox(c, opt, ax, y)
        ax += 1.1 * inch
    y -= 16

    y = draw_field(c, "Foods That Helped", MARGIN, y, field_w=CONTENT_W)
    y = draw_field(c, "Foods That Didn't Sit Well", MARGIN, y, field_w=CONTENT_W)
    y -= 4

    c.setFont("Georgia", FIELD_LABEL_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN, y, "Supplements Taken:")
    draw_checkbox(c, "Cleared with care team?", MARGIN + 130, y)

    c.showPage()


def build_lab_results(c, entry_num):
    """Lab Results Tracker page."""
    draw_page_bg(c)
    y = PAGE_H - MARGIN
    y = draw_header(c, "Lab Results", y, accent=SLATE)

    y = draw_field(c, "Date", MARGIN, y, field_w=3 * inch)
    y -= 8

    headers = ["Test", "Result", "Reference Range", "Notes"]
    col_widths = [1.4 * inch, 1.0 * inch, 1.6 * inch, CONTENT_W - 4.0 * inch]
    lab_tests = [
        ("WBC", "", "", ""),
        ("ANC", "", "", ""),
        ("RBC", "", "", ""),
        ("Hemoglobin", "", "", ""),
        ("Hematocrit", "", "", ""),
        ("Platelets", "", "", ""),
        ("ALT (Liver)", "", "", ""),
        ("AST (Liver)", "", "", ""),
        ("Creatinine (Kidney)", "", "", ""),
    ]
    y = draw_table(c, headers, lab_tests, y, col_widths, row_h=22)

    y -= 8
    c.setFont("Georgia-Italic", 8)
    c.setFillColor(TAUPE)
    c.drawString(MARGIN, y,
                 "Ask your care team to explain any number outside your reference range.")
    c.drawString(MARGIN, y - 12,
                 "This page is for tracking trends, not for interpreting results on your own.")

    c.showPage()


def build_sleep_energy(c, entry_num):
    """Sleep & Energy Log page."""
    draw_page_bg(c)
    y = PAGE_H - MARGIN
    y = draw_header(c, "Sleep & Energy", y, accent=SAGE)

    y = draw_field(c, "Date", MARGIN, y, field_w=3 * inch)
    y -= 8

    y = draw_field(c, "Hours Slept", MARGIN, y, field_w=2 * inch)
    y -= 4

    c.setFont("Georgia-Bold", FIELD_LABEL_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN, y, "Sleep Quality:")
    sq_options = ["Poor", "Fair", "Good"]
    sx = MARGIN + 100
    for opt in sq_options:
        draw_checkbox(c, opt, sx, y)
        sx += 1 * inch
    y -= 18

    c.setFont("Georgia-Bold", FIELD_LABEL_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN, y, "Naps:")
    draw_checkbox(c, "Yes", MARGIN + 50, y)
    draw_checkbox(c, "No", MARGIN + 90, y)
    y = draw_field(c, "Duration", MARGIN + 140, y, field_w=1.5 * inch)
    y -= 6

    c.setFont("Georgia-Bold", FIELD_LABEL_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN, y, "Energy Level (1–10):")
    y -= 14
    for period in ["Morning", "Afternoon", "Evening"]:
        c.setFont("Georgia", FIELD_LABEL_PT)
        c.setFillColor(CHARCOAL)
        c.drawString(MARGIN + 20, y, f"{period}:  ① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩")
        y -= 16

    y -= 10
    c.setFont("Georgia-Bold", FIELD_LABEL_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN, y, "What Helped Me Rest:")
    y -= 6
    y = draw_writing_lines(c, MARGIN, y, CONTENT_W, 3)

    c.showPage()


# ============================================================
# EMOTIONAL SUPPORT
# ============================================================

def build_affirmation_page(c, affirmation_num):
    """Single affirmation page with illustration space and reflection line."""
    affirmations = [
        "You do not have to feel brave to be brave.",
        "Rest is not giving up — it's part of getting through this.",
        "This treatment is temporary. You are not defined by it.",
        "It's okay to have a hard day. Tomorrow is a new one.",
        "You are allowed to ask for help.",
        "Small steps still move you forward.",
        "Your body is working hard. Be gentle with it.",
        "You are more than your diagnosis.",
        "It's okay to not be okay today.",
        "You've made it through every hard day so far. That's worth noting.",
        "Healing isn't a straight line, and neither is courage.",
        "You're allowed to feel scared and strong in the same breath.",
        "One appointment, one day, one breath at a time.",
        "The people who love you are stronger with you in the room.",
        "However this goes, you are not walking through it unseen.",
    ]

    draw_page_bg(c, color=HexColor("#FDF6F3"))  # Slightly warmer for emotional pages

    y = PAGE_H / 2 + 40

    # Affirmation text (large, centered)
    text = affirmations[affirmation_num - 1]
    c.setFont("Georgia-Italic", 18)
    c.setFillColor(CHARCOAL)

    # Simple word-wrap
    words = text.split()
    lines = []
    current_line = ""
    max_w = CONTENT_W - 1 * inch
    for word in words:
        test = current_line + " " + word if current_line else word
        if c.stringWidth(test, "Georgia-Italic", 18) < max_w:
            current_line = test
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    for line in lines:
        c.drawCentredString(PAGE_W / 2, y, line)
        y -= 26

    # Small graphic placeholder
    y -= 30
    c.setFont("Georgia-Italic", 9)
    c.setFillColor(TAUPE)
    c.drawCentredString(PAGE_W / 2, y, "[Line art: Small illustration]")

    # Reflection line
    y -= 40
    c.setFont("Georgia-Italic", 10.5)
    c.setFillColor(TAUPE)
    c.drawCentredString(PAGE_W / 2, y, "This means _________________________ to me today")
    y -= 12
    c.setStrokeColor(TAUPE)
    c.setLineWidth(0.3)
    line_w = 3 * inch
    c.line(PAGE_W / 2 - line_w / 2, y, PAGE_W / 2 + line_w / 2, y)

    c.showPage()


def build_reflection_prompt(c, prompt_num):
    """Reflection & Journal Prompt page."""
    prompts = [
        "What does today's body feel like? What does it need?",
        "Write about a moment this week when someone showed you care.",
        "What's one worry you're carrying that you haven't said out loud?",
        "What's something small that felt good today?",
        "If you could tell your doctor one thing you haven't yet, what would it be?",
        "Write a note to the version of you who started this journey.",
        "What are you learning about your own strength?",
        "Who do you want beside you today, even just in thought?",
        "What does \"good enough\" look like for today?",
        "Describe a place that feels safe, even if only in memory.",
        "What's one thing you're proud of this week, no matter how small?",
        "If today had a color, what would it be, and why?",
        "What do you want the people around you to understand right now?",
        "Write about something you're looking forward to, big or small.",
        "What would you tell someone else just starting this?",
    ]

    draw_page_bg(c, color=HexColor("#FDF6F3"))
    y = PAGE_H - MARGIN - 20

    # Header
    c.setFont("Georgia-Bold", HEADER_PT)
    c.setFillColor(BLUSH)
    c.drawCentredString(PAGE_W / 2, y, "Take a Moment")
    y -= 30

    # Prompt
    text = prompts[prompt_num - 1]
    c.setFont("Georgia-Italic", 13)
    c.setFillColor(CHARCOAL)

    # Word wrap
    words = text.split()
    lines = []
    current_line = ""
    max_w = CONTENT_W - 0.5 * inch
    for word in words:
        test = current_line + " " + word if current_line else word
        if c.stringWidth(test, "Georgia-Italic", 13) < max_w:
            current_line = test
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    for line in lines:
        c.drawCentredString(PAGE_W / 2, y, line)
        y -= 20

    y -= 20

    # Writing lines
    draw_writing_lines(c, MARGIN, y, CONTENT_W, 18)

    c.showPage()


def build_gratitude_log(c, entry_num):
    """Gratitude Log page."""
    draw_page_bg(c, color=HexColor("#FDF6F3"))
    y = PAGE_H - MARGIN - 20

    c.setFont("Georgia-Bold", HEADER_PT)
    c.setFillColor(BLUSH)
    c.drawCentredString(PAGE_W / 2, y, "Today I'm Grateful For")
    y -= 40

    for i in range(1, 6):
        c.setFont("Georgia-Bold", 14)
        c.setFillColor(BLUSH)
        c.drawString(MARGIN, y, f"{i}.")
        y -= 4
        draw_writing_lines(c, MARGIN + 20, y, CONTENT_W - 20, 2, spacing=22)
        y -= 50

    c.showPage()


# ============================================================
# MILESTONES, CAREGIVER & CLOSING
# ============================================================

def build_milestone_flexible(c):
    """Milestone: A Milestone Worth Marking."""
    draw_page_bg(c, color=HexColor("#FDF6F3"))
    y = PAGE_H - MARGIN - 20

    c.setFont("Georgia-Bold", 22)
    c.setFillColor(SAGE)
    c.drawCentredString(PAGE_W / 2, y, "A Milestone Worth Marking")
    y -= 35

    c.setFont("Georgia-Italic", 12)
    c.setFillColor(CHARCOAL)
    c.drawCentredString(PAGE_W / 2, y,
                        "Something happened today worth remembering.")
    y -= 18
    c.drawCentredString(PAGE_W / 2, y,
                        "Here's what it was, and how I feel.")
    y -= 30

    draw_writing_lines(c, MARGIN, y, CONTENT_W, 20)

    c.showPage()


def build_milestone_halfway(c):
    """Milestone: Halfway Point."""
    draw_page_bg(c, color=HexColor("#FDF6F3"))
    y = PAGE_H - MARGIN - 20

    c.setFont("Georgia-Bold", 22)
    c.setFillColor(SAGE)
    c.drawCentredString(PAGE_W / 2, y, "Halfway Point")
    y -= 35

    c.setFont("Georgia-Italic", 12)
    c.setFillColor(CHARCOAL)
    c.drawCentredString(PAGE_W / 2, y, "You're halfway through your planned treatment.")
    y -= 18
    c.drawCentredString(PAGE_W / 2, y, "What has this journey taught you so far?")
    y -= 30

    draw_writing_lines(c, MARGIN, y, CONTENT_W, 20)

    c.showPage()


def build_milestone_final(c):
    """Milestone: Final Treatment Day."""
    draw_page_bg(c, color=HexColor("#FDF6F3"))
    y = PAGE_H - MARGIN - 20

    c.setFont("Georgia-Bold", 22)
    c.setFillColor(SAGE)
    c.drawCentredString(PAGE_W / 2, y, "Final Treatment Day")
    y -= 35

    c.setFont("Georgia-Italic", 12)
    c.setFillColor(CHARCOAL)
    c.drawCentredString(PAGE_W / 2, y, "Today was your last scheduled treatment.")
    y -= 18
    c.drawCentredString(PAGE_W / 2, y, "Write about this moment — what it means to you.")
    y -= 30

    y = draw_writing_lines(c, MARGIN, y, CONTENT_W, 14)

    # Signature line
    y -= 20
    c.setFont("Georgia-Italic", 10)
    c.setFillColor(TAUPE)
    c.drawString(MARGIN, y, "Optional — a nurse, friend, or loved one can sign:")
    y -= 14
    c.setStrokeColor(TAUPE)
    c.setLineWidth(0.4)
    c.line(MARGIN, y, MARGIN + 3 * inch, y)
    c.setFont("Georgia", 8)
    c.drawString(MARGIN + 3 * inch + 10, y - 2, "Date")

    c.showPage()


def build_milestone_one_month(c):
    """Milestone: One Month Since Treatment Ended."""
    draw_page_bg(c, color=HexColor("#FDF6F3"))
    y = PAGE_H - MARGIN - 20

    c.setFont("Georgia-Bold", 22)
    c.setFillColor(SAGE)
    c.drawCentredString(PAGE_W / 2, y, "One Month Since Treatment Ended")
    y -= 35

    c.setFont("Georgia-Italic", 12)
    c.setFillColor(CHARCOAL)
    c.drawCentredString(PAGE_W / 2, y, "It's been one month since your last treatment.")
    y -= 18
    c.drawCentredString(PAGE_W / 2, y, "How are you doing? What's changed?")
    y -= 30

    draw_writing_lines(c, MARGIN, y, CONTENT_W, 20)

    c.showPage()


def build_message_from_loved_one(c, msg_num):
    """Messages from Loved Ones page."""
    draw_page_bg(c, color=HexColor("#FDF6F3"))
    y = PAGE_H - MARGIN - 20

    c.setFont("Georgia-Bold", 22)
    c.setFillColor(BLUSH)
    c.drawCentredString(PAGE_W / 2, y, "A Message For You")
    y -= 35

    y = draw_field(c, "From", MARGIN, y, field_w=CONTENT_W)
    y = draw_field(c, "Relationship", MARGIN, y, field_w=CONTENT_W)
    y -= 10

    draw_writing_lines(c, MARGIN, y, CONTENT_W, 18)

    c.showPage()


def build_notes_page(c):
    """Blank ruled notes page."""
    draw_page_bg(c)
    y = PAGE_H - MARGIN

    c.setFont("Georgia-Bold", HEADER_PT)
    c.setFillColor(CHARCOAL)
    c.drawString(MARGIN, y, "Notes")
    y -= 20

    draw_writing_lines(c, MARGIN, y, CONTENT_W, 28)

    c.showPage()


def build_closing_page(c):
    """Closing / Completion page."""
    draw_page_bg(c, color=HexColor("#FDF6F3"))
    y = PAGE_H - MARGIN - 60

    c.setFont("Georgia-Bold", 26)
    c.setFillColor(SAGE)
    c.drawCentredString(PAGE_W / 2, y, "You Did This")
    y -= 30

    c.setFont("Georgia-Italic", 12)
    c.setFillColor(CHARCOAL)
    c.drawCentredString(PAGE_W / 2, y, "Date: ___________________")
    y -= 35

    c.setFont("Georgia-Italic", 13)
    c.drawCentredString(PAGE_W / 2, y,
                        "Looking back at this journal, what do you want to remember?")
    y -= 30

    draw_writing_lines(c, MARGIN, y, CONTENT_W, 16)

    c.showPage()


# ============================================================
# MAIN BUILD
# ============================================================

def build_journal():
    """Build the complete 130-page journal interior."""
    c = canvas.Canvas(OUTPUT_PDF, pagesize=letter)
    c.setTitle("Chemotherapy Treatment Journal")
    c.setAuthor("Meridian Press")

    page = 0

    print("Building front matter...")
    # Front matter (6 pages)
    build_title_page(c); page += 1
    build_how_to_use(c); page += 1
    build_diagnosis_snapshot(c); page += 1
    build_care_team(c); page += 1
    build_emergency_contacts(c); page += 1
    build_insurance(c); page += 1

    print("Building quick-reference tools...")
    # Quick-reference tools (6 pages)
    build_symptom_reference(c, 1); page += 2  # 2-page spread
    build_medication_master(c); page += 1
    build_doctor_questions(c); page += 3

    print("Building calendars...")
    # Calendars (6 pages)
    for i in range(6):
        build_monthly_calendar(c, i + 1); page += 1

    print("Building treatment tracking...")
    # Treatment tracking (58 pages)
    for i in range(12):
        build_chemo_cycle_tracker(c, i + 1); page += 1
    for i in range(26):
        build_daily_symptom_log(c, i + 1); page += 1
    for i in range(10):
        build_medication_log(c, i + 1); page += 1
    for i in range(10):
        build_appointment_log(c, i + 1); page += 1

    print("Building wellness tracking...")
    # Wellness tracking (24 pages)
    for i in range(12):
        build_hydration_nutrition(c, i + 1); page += 1
    for i in range(6):
        build_lab_results(c, i + 1); page += 1
    for i in range(6):
        build_sleep_energy(c, i + 1); page += 1

    print("Building emotional support...")
    # Emotional support (20 pages)
    for i in range(10):
        build_affirmation_page(c, i + 1); page += 1
    for i in range(6):
        build_reflection_prompt(c, i + 1); page += 1
    for i in range(4):
        build_gratitude_log(c, i + 1); page += 1

    print("Building milestones & closing...")
    # Milestones, caregiver & closing (10 pages)
    build_milestone_flexible(c); page += 1
    build_milestone_halfway(c); page += 1
    build_milestone_final(c); page += 1
    build_milestone_one_month(c); page += 1
    for i in range(3):
        build_message_from_loved_one(c, i + 1); page += 1
    for i in range(2):
        build_notes_page(c); page += 1
    build_closing_page(c); page += 1

    c.save()
    print(f"\nDone! Generated {page} pages")
    print(f"Output: {OUTPUT_PDF}")
    return page


if __name__ == "__main__":
    total = build_journal()
    print(f"\nExpected: 130 pages | Actual: {total} pages")
