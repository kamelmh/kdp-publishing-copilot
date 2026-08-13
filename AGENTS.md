# AGENTS.md — KDP Publishing Copilot

## Cross-Project Protocol

### Before Starting Work
1. Read this project's `UPDATES.md` for recent changes
2. Check sibling projects' `UPDATES.md` for changes that might affect this project:
   - `../digital-services-center/UPDATES.md` — if working on PDF generation
   - `../mahi-spiritual/UPDATES.md` — if working on spiritual content books

### After Finishing Work
1. Append an entry to this project's `UPDATES.md`
2. Include: date, what changed, files affected, breaking changes, alerts for other projects

### Alert System
If your work produces something other projects should know about:
- **Template changes** → Alert any project using the same templates
- **Dimension changes** → Alert any project generating KDP-compliant output
- **Font/encoding changes** → Alert DSC project (also generates PDFs)

## Project Context
- **Purpose:** Amazon KDP book publishing, cover design, layout
- **Key files:** Affinity Publisher templates, `book_template.py`
- **Dimensions:** Cover 6.25×9.25" (bleed), Interior 6×9"
