# Chemotherapy Treatment Journal — Complete Content & Design Specification
**Meridian Press · 8.5×11 · Target 120–160pp · Georgia family · Soft/calming palette**

---

## 0. What I checked before designing this

I opened the package before writing anything, so this spec builds on what you actually have rather than assuming.

**The 21-page PLR interior**, mapped page by page:
- 1 blank + 1 copyright + 1 "This Book Belongs To" ownership page
- 9 unique layouts, each duplicated once (18 pages): a title/owner/emergency-contact page, an undated monthly calendar, two different "daily log" designs, a cycle planner (4–6 mini weekly grids crammed onto one page), a medication/food-planner log, a "report tracker" with mood/vitals/diagnosis fields, a treatment-entry page, and an emergency-contacts page that duplicates the info on page 3

**Font/color reality check:** the original is set in Barlow Semi Condensed on pure white with flat gray section bands and gridlines — no color anywhere. It reads efficient, not calming. Your brief asks for Georgia + soft palette, which is the right call, but it means the front matter you keep should be **restyled to match**, not left as-is — mixing a condensed grayscale sans with a warm Georgia interior would read like two different books stitched together. I've written that restyle into the front-matter specs below.

**⚠️ License flag (read this before you upload anything):** the licensing PDF permits unlimited KDP products, uploading "as is," and using the templates inside another interior. It does **not** permit using the Pixel Pod Studio name "as part of your branding, marketing, or in connection with your products." Page 1 of the current interior reads *"COPYRIGHT © PIXEL POD STUDIO, 2020."* That line has to come out and be replaced with your own Meridian Press copyright line before this goes anywhere near KDP — leaving it in is a license violation, not a gray area. (The stricter "50% different" rule only applies to non-KDP platforms like IngramSpark/Etsy — for KDP you're clear on that front, and the expansion below blows past it anyway.)

**Graphics:** the five PNGs are clean single-line illustrations (no fill, no color) — a patient in bed, plus female/male/child variants and the "chemo machine." They'll drop cleanly onto any background color you choose. Good for a title page or section dividers; I'd use them sparingly rather than on every tracker page, to keep the calm/uncluttered feel your brief asks for.

Everything below is designed to fix the specific gaps I found (no lab tracking, no care-team directory, no insurance page, no doctor-question prep, blank/unlabeled checkboxes that force the patient to invent categories, cramped cycle-planner grids) rather than generic "here's what trackers usually have" advice.

---

## 1. Visual & Editorial System

**Typography (Georgia family):**
| Element | Spec |
|---|---|
| Page headers | Georgia Bold, 20–22pt |
| Section band labels | Georgia Bold, 12–13pt |
| Field labels | Georgia Regular, 10.5–11pt |
| Body/instructional text | Georgia Regular, 11pt, 1.4 line height |
| Small print / footnotes | Georgia Italic, 9pt |
| Writing lines | 0.38"–0.42" spacing (wider than typical — fatigue and mild neuropathy make small, tight lines hard to use) |

**Color system — soft, not clinical, not pink-washed:**
| Role | Color | Hex |
|---|---|---|
| Page background | Warm ivory | `#FBF7F1` |
| Primary accent — Tracking pages | Muted sage | `#8CA396` |
| Secondary accent — Emotional-support pages | Dusty blush | `#E3B8B0` |
| Tertiary accent — Logistics/reference pages | Soft slate blue | `#A9BFC9` |
| Text | Warm charcoal (not black) | `#3F3A36` |
| Gridlines/dividers | Warm taupe | `#D8D0C7` |

The three accents aren't just decoration — assign one per section (sage = tracking, blush = emotional support, slate = reference/logistics) and readers can flip to the right part of the book by color alone, which matters more here than in most journals since people will be using this while foggy or exhausted. Checkbox outlines and section bands carry the accent; keep large fill areas ivory so nothing feels heavy.

Avoid a pink-ribbon/breast-cancer-coded palette by default — your graphics pack already includes male, female, and child patient variants, so the design should read as usable by any patient, any cancer type, any gender.

**Accessibility notes:** minimum 10.5pt for any field a patient fills in themselves (not just headers), 4.5:1 contrast minimum text-to-background, generous whitespace between sections so a tired reader's eye doesn't have to hunt for the next field, checkboxes large enough to mark with a shaky hand (min 0.2" square).

---

## 2. Complete Page Inventory

Every tracking page type below is **one template, repeated** — you're not designing 26 different symptom logs, you're designing one and looping it in ReportLab the same way the notary journal build worked.

| Section | Page Type | Qty |
|---|---|---|
| **Front Matter** | Title / Ownership Page | 1 |
| | How to Use This Journal | 1 |
| | My Diagnosis & Treatment Snapshot | 1 |
| | Care Team Directory | 1 |
| | Emergency Contacts & When to Call for Help | 1 |
| | Insurance & Billing Quick Reference | 1 |
| **Quick-Reference Tools** | Symptom & Side-Effect Quick Reference | 2 |
| | Medication Master List | 1 |
| | Doctor Questions Checklist (reusable) | 3 |
| **Calendars** | Monthly Undated Calendar | 6 |
| **Treatment Tracking** | Chemo Cycle Tracker | 12 |
| | Daily Symptom Log | 26 |
| | Medication & Dose Log | 10 |
| | Appointment Log | 10 |
| **Wellness Tracking** | Hydration & Nutrition Log | 12 |
| | Lab Results Tracker | 6 |
| | Sleep & Energy Log | 6 |
| **Emotional Support** | Affirmation Page (1 per page) | 10 |
| | Reflection & Journal Prompt | 6 |
| | Gratitude Log | 4 |
| **— Core subtotal —** | | **120** |
| **Milestones, Caregiver & Closing** *(deluxe extension)* | Milestone Pages | 4 |
| | Messages from Loved Ones | 3 |
| | Blank Notes Pages | 2 |
| | Closing / Completion Page | 1 |
| **Deluxe total** | | **130** |

Recommendation: build the 130-page deluxe version. It's still comfortably inside your 120–160 target, still undercuts the 161–183pp competitors on print cost, and the milestone/caregiver pages are exactly the differentiation your "genuinely useful, not just another tracker" brief is asking for (Section 9 below explains why). If you need to hit exactly 120 for a spine-width calculation, trim Daily Symptom Logs to 20 and Medication & Dose Logs to 6 — every category here is a loop variable, not a fixed design.

---

## 3. Page-by-Page Content Specifications

### FRONT MATTER

**Title / Ownership Page** — ×1
- Header: *"This Journal Belongs To"*
- Fields: Name / Start Date / A short line for "This journal was given to me by ___" (optional, gift-market feature — see §10)
- Layout: Centered, generous margin, one line-art illustration (e.g., `Patient.png`) as a soft watermark-style graphic in the lower third
- Font: Header 24pt Georgia Bold; fields 12pt

**How to Use This Journal** — ×1
- Header: *"Before You Begin"*
- Body copy (~130 words): explain the color-coded sections, that entries are numbered (not paged) so skipping around is fine, that this is a **tracking tool, not medical advice** — always follow your care team's guidance — and permission to skip days or write messily
- Layout: Single column, generous line spacing, no fields
- Font: 11pt body, first line in 13pt italic as a pull-quote (e.g., "*You don't have to fill in every box. This book works for you, not the other way around.*")

**My Diagnosis & Treatment Snapshot** — ×1
- Header: *"My Diagnosis & Treatment Plan"*
- Fields: Diagnosis / Date of Diagnosis / Stage (if known) / Oncologist / Treatment Center / Regimen Name / Planned Number of Cycles / Cycle Length / Treatment Start Date / Estimated End Date / Treatment Goal (open line — deliberately not prescriptive; curative, maintenance, and palliative-intent patients all use this book)
- Layout: Two-column form, generous spacing, slate accent band
- Font: Labels 11pt bold, fields 12pt with 0.4" fill space

**Care Team Directory** — ×1
- Header: *"My Care Team"*
- Fields: table — Role | Name | Phone | Email | Notes, pre-labeled rows for Oncologist, Oncology Nurse / Nurse Navigator, Infusion Nurse, Primary Care Doctor, Pharmacist, Social Worker / Counselor, plus 3 blank rows
- Layout: Full-width table, slate accent header row
- Font: 10.5pt table text

**Emergency Contacts & When to Call for Help** — ×1
- Header: *"Emergency Contacts"*
- Fields: 2 personal contacts (Name / Relationship / Phone / Alt Phone)
- Boxed callout: *"Call your care team or 911 if you have:"* — Fever of 100.4°F (38°C) or higher · Uncontrolled bleeding · Severe shortness of breath · Signs of an allergic reaction · Confusion or fainting · Pain not relieved by your medication — footnote: *"confirm your exact thresholds with your oncology team; every regimen is different"*
- Layout: Contacts on left, red-adjacent (dusty rose, not alarming red) bordered callout box on right
- Font: Callout header 12pt bold, list 10.5pt

**Insurance & Billing Quick Reference** — ×1
- Header: *"Insurance & Billing"*
- Fields: Insurance Provider / Policy or Member ID / Group # / Customer Service Phone / Prior Authorization Contact / Hospital Financial Counselor Name & Phone / Copay Per Visit / Notes on Coverage / a small table for logging bills and Explanation-of-Benefits statements as they arrive (Date | From | Amount | Status)
- Layout: Form fields top half, tracking table bottom half
- Font: 11pt

### QUICK-REFERENCE TOOLS

**Symptom & Side-Effect Quick Reference** — ×2 (spread)
- Header: *"What to Watch For"*
- Content: organized by category, each item pre-printed (not blank) —
  - *Digestive:* Nausea, Vomiting, Loss of appetite, Mouth sores, Taste changes, Diarrhea, Constipation
  - *Skin, Hair & Nails:* Hair loss, Dry or itchy skin, Nail changes, Sun sensitivity
  - *Energy & Sleep:* Fatigue, Trouble sleeping, Needing more rest than usual
  - *Nerve & Muscle:* Numbness or tingling (hands/feet), Joint or muscle aches
  - *Emotional & Cognitive:* Anxiety, Low mood, Irritability, "Chemo brain" / trouble focusing
  - *Other:* Fever or chills, Easy bruising or bleeding, Shortness of breath
- Severity key printed once at the top: None · Mild · Moderate · Severe · **Call my care team** — this same key is reused on the Daily Symptom Log so the two pages work together
- Layout: 3-column checklist grid, sage accent category headers
- Font: Category headers 12pt bold, items 10.5pt

**Medication Master List** — ×1
- Header: *"My Medications at a Glance"*
- Fields: table — Medication Name | Purpose (Chemo / Anti-Nausea / Steroid / Pain / Growth Factor / Other) | Dose | Frequency | Prescribing Doctor | Pharmacy | Start Date | Notes — ~16 rows
- Layout: Full-page table
- Font: 10pt table text

**Doctor Questions Checklist** — ×3 (identical template, reusable across visits)
- Header: *"Questions for My Next Appointment"* + a blank line for the appointment date
- Pre-printed prompts grouped by category, each with a checkbox + a ruled line for the answer:
  - *Treatment:* What type of chemotherapy am I receiving and how does it work? · How many cycles are planned? · How will we know if it's working? · What happens if I miss a dose or session?
  - *Side Effects:* What side effects are most common with this regimen? · Which side effects mean I should call right away? · What can I take for nausea or pain, and what should I avoid?
  - *Daily Life:* Are there foods or activities to avoid? · Can I exercise, and how much? · Is it safe to be around others, including kids or pets?
  - *Logistics:* Who do I call after hours? · Do I need labs before every session? · What should I bring to appointments?
  - *Support:* Is what I'm feeling normal for this stage of treatment? · Are there support groups or counselors you'd recommend?
  - 4 blank lines for the patient's own questions
- Layout: Single column, checkbox + question + answer line
- Font: Questions 11pt, answer lines 10.5pt

### CALENDARS

**Monthly Undated Calendar** — ×6
- Header: *"Month:___ Year:___"* (blank fill, keeps it reusable regardless of when treatment starts)
- Layout: standard 5-week grid, each day cell large enough for a short note; small legend at top with three icons/marks for "Chemo Day," "Appointment," "Lab Draw"; Notes strip along the bottom
- Font: Day numbers 10pt, cell text 9pt (smallest text in the book, since it's glance-reference, not primary writing space)

### TREATMENT TRACKING

**Chemo Cycle Tracker** — ×12
- Header: *"Cycle #___ of ___"* (this is the entry ID — no page number)
- Fields: Date / Drugs Administered (from my chart) / Pre-Medications Given / Infusion Location & Nurse / Energy Level Before → After (1–10 scale) / How I Felt During Infusion (4-line writing area) / Symptoms in the Following 48 Hours (checkbox row pulling from the Quick-Reference list) / Next Cycle Date / Notes
- Layout: Top third fields, middle writing area, bottom checkbox row — one full page per cycle (the original's mistake was cramming 4–6 cycles onto one page with no writing room; don't repeat that)
- Font: Header 18pt, fields 11pt

**Daily Symptom Log** — ×26
- Header: *"Day #___"* (entry ID)
- Fields: Date / Cycle Day (Day ___ of Cycle ___) / Overall Feeling Today (1–10 scale or simple face-scale) / Symptom checkboxes with severity marks (None/Mild/Moderate/Severe), same list as the Quick-Reference spread / Sleep Hours / Mood / "One good thing today" (single line — small, sustainable gratitude touch, not a full separate exercise) / Notes
- Layout: Compact top strip for scales, symptom grid as the visual center, one generous writing line at the bottom
- Font: Header 18pt, symptom list 10pt, writing line 11pt

**Medication & Dose Log** — ×10
- Header: *"Medication Log"* + date field
- Fields: table — Time | Medication | Dose Taken | Purpose | How I Felt After — plus checkboxes: Taken as Scheduled (Yes/No), Missed a Dose (Yes/No) — plus one line: "Question for my pharmacist"
- Layout: Table-dominant, ~8 rows
- Font: 10.5pt table

**Appointment Log** — ×10
- Header: *"Appointment Log"* + Entry #
- Fields: Date & Time / Type of Visit (Oncologist / Infusion / Scan / Lab Draw / Other) / Who I Saw / What We Discussed (generous writing block) / Questions I Asked & Answers / Next Steps / Next Appointment Date
- Layout: Form strip top, large writing block center, next-steps strip bottom
- Font: Header 18pt, fields 11pt

### WELLNESS TRACKING

**Hydration & Nutrition Log** — ×12
- Header: *"Hydration & Nutrition"* + date
- Fields: Water intake — 10 glass icons to shade (8oz each; this is the one original-template element worth keeping, it works) / Meals: Breakfast, Lunch, Dinner, Snacks (short lines) / Appetite Level (None/Some/Normal/Good) / Foods That Helped / Foods That Didn't Sit Well / Supplements Taken + checkbox "Cleared with my care team?"
- Layout: Water tracker as a visual strip at top, meals as a simple table, two short columns for "helped / didn't help"
- Font: 11pt

**Lab Results Tracker** — ×6
- Header: *"Lab Results"* + date
- Fields: table — Date | WBC | ANC | RBC | Hemoglobin | Hematocrit | Platelets | ALT | AST | Creatinine | My Reference Range (blank — filled from the patient's own lab report, since normal ranges vary by lab and by person) | Notes
- Footnote: *"Ask your care team to explain any number outside your reference range — this page is for tracking trends, not for interpreting results on your own."*
- Layout: Wide table, 5 rows per page
- Font: 10pt table, 9pt footnote

**Sleep & Energy Log** — ×6
- Header: *"Sleep & Energy"* + date
- Fields: Hours Slept / Sleep Quality (Poor/Fair/Good) / Naps (Yes/No, duration) / Energy Level — Morning / Afternoon / Evening (1–10 each) / What Helped Me Rest / Notes
- Layout: Simple form, generous writing line at bottom
- Font: 11pt

### EMOTIONAL SUPPORT

**Affirmation Page** — ×10 (one affirmation per page, illustrated)
- Header: none — the affirmation itself is the header, large, centered
- Layout: single line-art graphic (small, corner-placed) + affirmation text set large (16–18pt) + small ruled space below: "This means ___ to me today" — makes it interactive rather than purely decorative
- Font: Affirmation 16–18pt Georgia Italic, reflection line 10.5pt

**Reflection & Journal Prompt** — ×6
- Header: *"Take a Moment"*
- Layout: one open-ended prompt at top (see §7 for the pool of 15 to choose from), full page of writing lines below
- Font: Prompt 13pt italic, lines standard spacing

**Gratitude Log** — ×4
- Header: *"Today I'm Grateful For"*
- Fields: 5 numbered lines
- Layout: Simple, blush accent, generous spacing
- Font: 12pt

---

## 4. Milestones, Caregiver & Closing (deluxe pages 121–130)

**Milestone Pages** — ×4, each its own design:
1. *"A Milestone Worth Marking"* — flexible, patient-defined: "Something happened today worth remembering. Here's what it was, and how I feel." (This one deliberately doesn't assume a "win" — a hard day worth marking counts too.)
2. *"Halfway Point"* — reflection prompt + writing space
3. *"Final Treatment Day"* — reflection + writing space + an optional signature line so a nurse or loved one can sign it
4. *"One Month Since Treatment Ended"* — reflection + writing space

**Messages from Loved Ones** — ×3, identical template: header *"A Message For You,"* a Name/Relationship line, and a full writing area. Meant to be left blank in the printed book so people close to the patient can fill them in — this is the single highest-leverage page for the gift market (see §10).

**Blank Notes Pages** — ×2, simple ruled pages, no fields.

**Closing / Completion Page** — ×1, header *"You Did This,"* a line for the date, and a short closing reflection prompt: "Looking back at this journal, what do you want to remember?"

---

## 5. Affirmations (15 — print your strongest 10, keep 5 in reserve)

1. You do not have to feel brave to be brave.
2. Rest is not giving up — it's part of getting through this.
3. This treatment is temporary. You are not defined by it.
4. It's okay to have a hard day. Tomorrow is a new one.
5. You are allowed to ask for help.
6. Small steps still move you forward.
7. Your body is working hard. Be gentle with it.
8. You are more than your diagnosis.
9. It's okay to not be okay today.
10. You've made it through every hard day so far. That's worth noting.
11. Healing isn't a straight line, and neither is courage.
12. You're allowed to feel scared and strong in the same breath.
13. One appointment, one day, one breath at a time.
14. The people who love you are stronger with you in the room.
15. However this goes, you are not walking through it unseen.

*(Deliberately avoids "beat this!" / guaranteed-cure language — not every reader is in curative-intent treatment, and false certainty reads as hollow to anyone who is not.)*

## 6. Reflection & Journal Prompts (15 — print your strongest 6, rotate the rest)

1. What does today's body feel like? What does it need?
2. Write about a moment this week when someone showed you care.
3. What's one worry you're carrying that you haven't said out loud?
4. What's something small that felt good today?
5. If you could tell your doctor one thing you haven't yet, what would it be?
6. Write a note to the version of you who started this journey.
7. What are you learning about your own strength?
8. Who do you want beside you today, even just in thought?
9. What does "good enough" look like for today?
10. Describe a place that feels safe, even if only in memory.
11. What's one thing you're proud of this week, no matter how small?
12. If today had a color, what would it be, and why?
13. What do you want the people around you to understand right now?
14. Write about something you're looking forward to, big or small.
15. What would you tell someone else just starting this?

---

## 7. Doctor Questions Checklist (consolidated — same content as §3's reusable pages)

**About Treatment:** What type of chemotherapy will I receive and how does it work? · How many cycles/sessions are planned, and how long is each? · How will we know if treatment is working? · What should I do if I miss a dose or session?

**About Side Effects:** What side effects are most common with this regimen? · Which side effects need an immediate call to your office? · What can I take for nausea or pain, and what should I avoid? · Will this affect my ability to work, drive, or care for myself?

**About Daily Life:** Are there foods or activities I should avoid? · Can I exercise, and how much? · Is it safe to be around others, including children, pets, or people who are sick? · What precautions should I take with my immune system?

**About Logistics:** Who do I contact after hours or on weekends? · What should I bring to each appointment? · Will I need labs before every session? · How should I plan transportation for treatment days?

**Emotional/Support:** Is what I'm feeling normal at this stage? · Are there support groups or counselors you'd recommend? · How can my family or caregiver best support me?

## 8. Side Effects Checklist (consolidated — same content as §3's Quick-Reference spread)

**Physical:** Fatigue · Nausea/vomiting · Appetite changes · Hair loss · Mouth sores · Taste changes · Constipation · Diarrhea · Numbness/tingling (hands/feet) · Skin/nail changes · Fever/chills · Easy bruising/bleeding · Shortness of breath · Joint/muscle aches

**Cognitive/Emotional:** "Chemo brain" (concentration/memory) · Sleep changes · Anxiety · Irritability · Low mood

Each item ships with the same five-point severity key used throughout the book: **None · Mild · Moderate · Severe · Call my care team.**

---

## 9. Design Improvements — what the category gets wrong, and what actually helps

**What the original template (and most competitors at this price point) get wrong:**
- Blank, unlabeled checkboxes that force the patient to invent categories every time — exactly the wrong ask when chemo brain and fatigue are reducing exactly that kind of executive-function capacity
- Cramming multiple weeks/entries onto one page to hit a page-count target, leaving no real writing room (your original Cycle Planner does this — 4-6 mini grids per page)
- Redundant sections that don't add function (your original repeats emergency contacts twice with no new information)
- A grayscale, dense, spreadsheet-like visual language sold as a "comfort" product
- Zero lab tracking, no care-team directory, no insurance/billing help, no appointment-prep tool — the practical logistics that actually eat a patient's mental energy
- Universally upbeat "beat this!" tone that doesn't fit every reader's treatment goal

**What makes this genuinely useful instead of "another tracker":**
- Every checkbox category is pre-labeled and clinically sensible, cross-referenced between the Quick-Reference spread and the Daily Log so the two work as one system
- Diagnosis/treatment info lives on its own dedicated snapshot page instead of being buried in a random daily log
- Lab tracking, insurance/billing, and a doctor-question prep tool address the *logistics* of cancer treatment, not just the symptoms — this is the gap every competitor in your table leaves open
- Milestone language doesn't presume a specific outcome, so it works for curative, maintenance, and palliative-intent readers alike

## 10. Gift Market Optimization

Most buyers of a book like this are family or friends purchasing *for* a patient, not the patient buying for themselves — design for that buyer as much as the end reader:
- The optional "This journal was given to me by ___, because ___" line on the title page turns the book into something personal at the moment of gifting
- The three "Messages from Loved Ones" pages are the single best gift-market feature here — they let the gifter (or several people) leave something in the book before handing it over
- Keep cover and interior language inclusive rather than gendered — your graphics pack already supports this (male/female/child/generic patient variants); don't default into pink-ribbon/breast-cancer-specific branding, since chemotherapy spans many cancer types and both sexes
- On the KDP listing itself (separate from interior design, but worth flagging): lead the description with the gifting use case, not just the tracking-tool use case — "a thoughtful gift for someone starting treatment" converts differently than "chemotherapy symptom tracker"

---

## 11. Legal & Compliance Notes

- Remove all "Pixel Pod Studio" branding, including the page-1 copyright line, before publishing — see §0. Replace with your standard Meridian Press copyright block.
- Add a one-line disclaimer to the copyright/legal page: *"This journal is a personal tracking tool and does not provide medical advice. Always follow the guidance of your healthcare team."* Standard practice for health-adjacent low-content books, and it protects you.
- You're publishing on KDP only per your brief, so the stricter "50% different from the original" rule (which only applies to IngramSpark/Etsy/etc.) doesn't technically apply — though expanding from 21 to 130 pages with a full font, color, and layout overhaul clears that bar many times over regardless.

## 12. Production Handoff

This spec is written to drop into the same pipeline you used for the notary journal: ReportLab for the interior build, this document as the content/field source of truth, cover design separately in Affinity Publisher or Canva once the interior is locked. Every repeating tracker above is one function + a loop variable for quantity — nothing here requires a new technical approach, just new field sets and the sage/blush/slate color system in place of the notary journal's navy/gold.

Suggested build order: front matter → quick-reference tools → calendars → the four treatment-tracking loops → the three wellness-tracking loops → emotional support → (if going deluxe) milestones/caregiver/closing.
