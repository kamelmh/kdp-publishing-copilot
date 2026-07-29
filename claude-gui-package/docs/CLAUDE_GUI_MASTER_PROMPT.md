# KDP Publishing — Claude GUI Master Prompt

> **Purpose:** Complete context package for Claude GUI to review and enhance the Notary Public Record Journal.

---

## PROJECT IDENTITY

| Field | Value |
|-------|-------|
| Publisher | Meridian Press (pen name; account under Oumkeltoum Djerjour) |
| Contact | kamelmahi71@gmail.com |
| Account | KDP ID: A2JDT3KR1A59T5 |
| Book | Notary Public Record Journal |
| Status | KDP upload in progress (Paperback Details complete) |

---

## WHAT WE'VE BUILT

### Book 1: Notary Public Record Journal

| Spec | Value |
|------|-------|
| Trim | 6" × 9" |
| Pages | 120 |
| Entries | 110 pre-numbered |
| Paper | White, B&W interior |
| Cover | Matte, green/gold (Meridian Press brand) |
| Price | $12.99 |
| Royalty | 60% ($5.35 net per sale) |
| ISBN | KDP-free ISBN |

### Interior Structure

```
Page 1:     Cover page (title, notary info, seal placeholder)
Page 2:     Instructions (how to use, sequential numbering, storage)
Pages 3-112: Entry pages (110 entries, 1 per page)
Pages 113-116: Summary Index (table for quick reference)
Pages 117-120: Notes pages
```

### Entry Page Layout (Each of 110 Pages)

```
┌─────────────────────────────────────────────────────────┐
│ NOTARIAL ACT RECORD                    Entry No. [XXX]  │
├─────────────────────────────────────────────────────────┤
│ SECTION A — Date & Time                                 │
│ Date: ____________  Time: ________  [ ]AM  [ ]PM        │
├─────────────────────────────────────────────────────────┤
│ SECTION B — Type of Notarial Act                        │
│ [ ] Acknowledgment  [ ] Jurat  [ ] Oath/Affirmation    │
│ [ ] Copy Certification  [ ] Signature Witnessing        │
│ [ ] Other: ___________                                  │
├─────────────────────────────────────────────────────────┤
│ SECTION C — Document Information                        │
│ Document Type: ____________________  Date: ____________ │
│ Pages: ______  Description: _________________________  │
├─────────────────────────────────────────────────────────┤
│ SECTION D — Signer Information                          │
│ Name: ________________________________________________ │
│ Address: _____________________________________________ │
│ ID Type: [ ] DL  [ ] Passport  [ ] State ID  [ ] Other │
│ ID #: _____________  Expires: ____________              │
│ Signature: _________________________  Date: __________ │
├─────────────────────────────────────────────────────────┤
│ SECTION E — Witness Information                         │
│ Name: ____________________  ID#: ________  Sig: ______ │
├──────────────────────────────┬──────────────────────────┤
│ SECTION F — Thumbprint       │ SECTION G — Fees         │
│ ┌────────────────┐          │ Fee: $_______            │
│ │                │          │ Payment: [ ] Cash         │
│ │  RIGHT THUMB   │          │   [ ] Check  [ ] E-Trans │
│ │                │          │ Ref#: ___________        │
│ └────────────────┘          │                          │
├──────────────────────────────┴──────────────────────────┤
│ SECTION H — Notary Certification                        │
│ I certify the signer appeared before me.                │
│ Name: ________  Commission#: ________  Expires: _______ │
│ State: ________  County: ________                       │
│ Signature: ________________________  Date: ____________ │
│              [ OFFICIAL SEAL ]                          │
├─────────────────────────────────────────────────────────┤
│ SECTION I — Remarks                                     │
│ ________________________________________________________│
│ ________________________________________________________│
│ ________________________________________________________│
└─────────────────────────────────────────────────────────┘
```

---

## DELIVERABLES INVENTORY

### PDFs (Ready to Upload)
| File | Path | Status |
|------|------|--------|
| Interior | `books/notary-log-book/interior.pdf` | ✅ Ready |
| Cover (Official) | `books/notary-log-book/cover-wrap-green.pdf` | ✅ Ready |
| Cover (Burgundy) | `books/notary-log-book/cover-wrap-burgundy.pdf` | ✅ Alternate |
| Cover (Vector) | `books/notary-log-book/cover-wrap-vector.pdf` | ✅ Alternate |
| Cover (Proof) | `books/notary-log-book/cover-wrap-PROOF.pdf` | ❌ Do not upload |

### Documentation
| File | Purpose |
|------|---------|
| MASTER_REFERENCE.md | Complete specs and rules |
| PUBLISHING_PLAYBOOK.md | Upload walkthrough |
| MARKET_ANALYSIS.md | Competitor research |
| CLAUDE_GUI_MASTER_PROMPT.md | This file |

### Skills
| Skill | Purpose |
|-------|---------|
| kdp-print | Interior/cover PDF generation |
| notary-journal | Premium 1-entry-per-page design |
| logo-design | Meridian Press brand assets |
| book-illustration-concepts | Cover concept workflow |

---

## QUESTIONS FOR CLAUDE GUI

### Interior Design Enhancement

1. **Typography:** We used Helvetica (built-in ReportLab). Should we consider a more professional font? What fonts are KDP-safe?

2. **Section Headers:** Currently navy blue bars with white text. Is this optimal for a professional legal document?

3. **Thumbprint Box:** Currently 1"×1" on outer edge. Is this positioned correctly for left-handed notaries?

4. **Line Spacing:** Currently 0.27" (19.4pt) for write-in lines. Is this comfortable for handwriting?

5. **Entry Numbering:** Currently "Entry No. [XXX]" in header. Should we add page numbers too?

6. **Summary Index:** Currently 4 pages at the back. Should we add a "quick reference" section for common notarial acts?

7. **Paper Weight:** KDP uses 50-61lb (74-90 gsm) for white paper. Is this sufficient for pen writing without bleed-through?

8. **Margins:** Gutter 0.5", outer 0.375", top/bottom 0.5". Any adjustments for better handwriting comfort?

### Content Enhancement

9. **Instructions Page:** Currently basic. Should we add state-specific notary requirements?

10. **Fee Schedule:** Should we include a sample fee schedule by state?

11. **Common Notarial Acts:** Should we add a quick reference guide for acknowledgment vs jurat vs oath?

12. **ID Verification Guide:** Should we add a visual guide for checking IDs?

### Brand Enhancement

13. **Meridian Press:** Should we create a more distinctive brand identity beyond the current green/gold theme?

14. **Back Cover Copy:** Currently 3 bullet points. Should we add testimonials or "as seen in" badges?

15. **Interior Branding:** Should we add Meridian Press logo to each entry page header?

### KDP Optimization

16. **A+ Content:** Should we create Enhanced Brand Content for the product page?

17. **Author Central:** Should we set up an Author Central page for Meridian Press?

18. **Series Setup:** Should we set up a "Meridian Press Professional Logs" series now, even though Book 1 is standalone?

---

## STRATEGIC CONTEXT

### What Worked
- MiMo V2.5 handled all generation
- HyperAgent provided quality review
- OpenCode routing worked for complex tasks
- 138 files created in one session

### What to Improve
- Interior typography could be more professional
- Content could include more educational elements
- Brand identity could be stronger
- A+ Content would boost conversions

### Next Steps
1. Upload to KDP (interior + cover)
2. Launch Previewer (verify no errors)
3. Set pricing ($12.99, 60% royalty)
4. Publish (24-72 hour review)
5. Post-launch: A+ Content, Author Central, social assets

---

## WHAT WE NEED FROM CLAUDE GUI

1. **Interior Review:** Open `interior.pdf` and provide specific enhancement recommendations
2. **Typography Audit:** Recommend KDP-safe fonts for professional legal documents
3. **Content Gaps:** Identify what's missing from the current 120-page interior
4. **Brand Strategy:** Recommend how to strengthen Meridian Press identity
5. **A+ Content Plan:** Outline Enhanced Brand Content for the product page
6. **Post-Launch Checklist:** What to do after the book goes live

---

*This prompt package contains everything Claude GUI needs to understand and enhance the KDP Publishing project.*
