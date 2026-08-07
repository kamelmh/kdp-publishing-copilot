# KDP Publishing Copilot — Quick Start

## First Message to Claude

Copy and paste this as your first message in the KDP Publishing project:

```
KDP Publishing Copilot ready. Account: Oumkeltoum Djerjour (kaprikika8@gmail.com). 

Book 1: Simple Notary Log Book — 6×9, 120 pages, $12.99
- Interior: Notary record entries (date, act type, signer, ID, document, fee)
- Status: Interior PDF generated, needs cover design

Book 2: Password Log Book — 5.06×7.81, 100 pages, $9.99
- Status: NEXT

Book 3: Running Log Book — 6×9, 120 pages, $12.99
- Status: QUEUED

What should we do next?
```

## Commands

| Say This | Claude Will |
|----------|-------------|
| "Show specs" | Display all KDP specifications |
| "Generate interior" | Create print-ready interior PDF |
| "Build cover" | Calculate cover wrap dimensions |
| "Write metadata" | Generate title, description, keywords |
| "Price this book" | Calculate 40% royalty pricing |
| "Check before upload" | Run pre-flight checklist |
| "Publish book 1" | Walk through KDP upload steps |
| "Book 2" | Switch to Password Log Book |
| "Book 3" | Switch to Running Log Book |
| "What's next?" | Show pipeline status |

## Files

```
C:\Users\Admin\Projects\active\kdp-publishing-copilot\
├── FEED_LOOP.md                    ← Full context (paste into Instructions)
├── QUICK_START.md                  ← This file
├── CLAUDE_DESKTOP_MASTER_PROMPT.md ← Alternative master prompt
├── skills\kdp-print\kdp_print.py   ← Interior/cover generator
└── books\notary-log-book\
    ├── interior.pdf                ← Generated interior (120 pages)
    └── STARTER_KIT.md              ← Complete book guide
```

## KDP Account

- **Name:** Oumkeltoum Djerjour
- **Email:** kaprikika8@gmail.com
- **Account ID:** A2JDT3KR1A59T5
- **Tax:** 30% US withholding
- **Payment:** Check only
