# Thread Context

Key facts and notes for this thread. Updated by agent, survives context compaction.

## Numbers & Values

Account: Oumkeltoum Djerjour, kaprikika8@gmail.com, Account ID A2JDT3KR1A59T5, El Bayadh Algeria. Backup contact kamelmahi71@gmail.com. Tax: 30% US withholding (no US–Algeria treaty). Payout: check only.

Book 1 (Notary Public Record Journal): 6x9 in, 120 pages, white paper, B&W interior.
- Spine width = 120 x 0.002252 + 0.06 = 0.330 in (99 px @ 300 DPI).
- Full wrap cover = 12.58 in x 9.25 in = 3774 x 2775 px @ 300 DPI (bleed 37.5 px, spine 99 px).
- Interior trim = 6 x 9 in = 1800 x 2700 px @ 300 DPI.
- Gutter required 0.375 in at 120pp; using 0.5 in for comfort. Outside/top/bottom 0.25 in min.
- List $12.99. Printing ~$2.44 (1.00 + 120 x 0.012). Net @ 60% Amazon ≈ $5.35; @ 40% Expanded Distribution ≈ $2.76.

KDP royalty rule (verified 2026): paperback = 60% of list − printing on Amazon (50% if list below marketplace threshold, since Jun 2025); 40% − printing on Expanded Distribution. eBook 70%/35% tiers do not apply to paperback.

## Corrections

Errors found in the user's existing project files, to fix during execution:

- Royalty model: docs say flat 40%. Correct: Amazon paperback 60% − printing (50% below price threshold); 40% is Expanded Distribution only.
- Printing cost: doc says ~$2.80 for 100pp. Correct formula ~$1.00 + $0.012/page → 120pp ≈ $2.44.
- Canva canvas: MASTER_REFERENCE says 1256x925 px at 300 DPI — that is only 100 DPI. Correct 300 DPI = 3774x2775 px. (Bleed 37.5px and spine 99px were already correct.)
- Gutter: HYPERAGENT_MASTER_PROMPT says 0.625 in required; notary-journal SKILL.md also uses 0.625. KDP requires only 0.375 in at 120pp. Standardize on 0.5 in.
- kdp_print.py bug 1: build_cover_wrap uses specs["spine_thickness_px"], which does not exist (calculate_specs returns "spine_thickness"). Guaranteed KeyError crash.
- kdp_print.py bug 2: generate_notary_interior computes gutter but applies outside_margin (0.25 in) on both sides, so binding edge is too tight; also no mirrored odd/even margins.
- kdp_print.py gap: generate_notary_interior is a simple 2-per-page form with no cover/instructions/index/thumbprint/seal, unlike the premium design documented in notary-journal SKILL.md.
- Pipeline mismatch: original brief Books 2/3 = Gratitude Journal (5x8/90pp) + Grammar Workbook (8.5x11/150pp); files Books 2/3 = Password Log + Running Log. Needs user confirmation.

## Decisions

- Book 1 structure: 120 pages = title page + instructions + 110 pre-numbered entries + 4 index pages + 4 notes pages. Marketed as "100+ pre-numbered entries."
- Interior: premium one-entry-per-page, sections A–I, 72pt (1 inch) thumbprint on the outer edge, dashed official-seal area, mirrored margins (gutter 0.5 in, outer 0.3 in). Helvetica.
- Cover: built in reportlab (vector text over raster art). Front art = navy guilloché + gold seal/scales emblem (Nano Banana Pro, 4K). Title set in Times-Bold (built-in, no external font dependency). Upload file has NO printed guides; a separate PROOF file has magenta trim/spine/bleed guides.
- Cover dims: 12.58 x 9.25 in (3774 x 2775 px @300DPI), spine 0.3302 in (99 px).
- Corrected economics: printing ~$2.44; net at $12.99 = $5.35 (60% Amazon) / $2.76 (40% Expanded Distribution).
- kdp_print.py fully rewritten at skills/kdp-print/kdp_print.py; both original bugs fixed; royalty()/printing_cost helpers added.
- Books 2 and 3: user skipped the pipeline question; finalize specs once they pick brief (Gratitude + Grammar) vs files (Password + Running).

- Official Book 1 cover = GREEN/GOLD (cover-wrap-green.pdf), chosen by user 2026-07-28. Upload interior.pdf + cover-wrap-green.pdf. Other colorways (navy AI, navy vector, burgundy/cream) kept as alternates.
- Still pending (user initiated, not yet run): live book-illustration-concepts demo — awaiting the user's story premise.

- Imprint FINALIZED: "Meridian Press" (pen name) — set as green-cover byline (cover-wrap-green.pdf rebuilt); KDP Author + Publisher = Meridian Press; account/W-8BEN/royalties remain under Oumkeltoum Djerjour; Author field locks after publish. Logo set in assets/brand/ (transparent + navy/green/white lockups + monogram M). Playbook (doc + .md) and README updated; project zip rebuilt (38 files).

- GitHub: connected as kamelmh; repo kamelmh/kdp-publishing-copilot (default branch = master, NOT main). Repo pre-existed with its own lineage (kdp_print.py 30952b, generate_improved_interior.py, 4 ad-hoc verify scripts, claude-gui-package/, hyperagent-package/, verify_hyperagent.py).
- Chose safe path: branch hyperagent/v2.2-fixes + PR #1 (https://github.com/kamelmh/kdp-publishing-copilot/pull/1). Pushed 12 TEXT files in one commit (7287fbb); verified byte-exact via git blob SHA match. User's generate_improved_interior.py / check_notes.py / render_pages.py / verify_fixes.py / verify_interior.py preserved unchanged.
- Binary PDFs NOT pushed: MCP github push_files/create_or_update_file take content as a text string, so binary would corrupt. User must add interior.pdf + 4 covers via GitHub web UI or git CLI. Also flagged repo-root hyperagent-package.zip still holds the OLD interior.

## Notes




--- Design revision (user request) ---
User wants: (1) "mitigate the logo" on the cover — the current emblem has an inappropriate sun/crescent-moon motif for a notary book; redesign to a restrained, notary-appropriate emblem, placed well; (2) create a reusable logo-design skill for the copilot; (3) integrate "calibrative design artifacts" = calibrated, reusable, spec-correct design assets (emblem variants + palette + placement) that plug into the cover builder. Action: regenerate 2 cleaner cover treatments now (no sun/moon), rebuild the wrap with the chosen one; then propose + confirm the logo-design skill and calibrated design-kit before formalizing.


--- Design revision DONE ---
- Cover logo fixed: replaced the sun/moon AI emblem with a proper notary seal (star ring + scales of justice). Two cover options exist: (A) AI-art emblem cover-wrap.pdf; (B) fully-calibrated cover-wrap-vector.pdf = clean navy bg + vector emblem overlay. Awaiting user pick for Book 1's official cover.
- New skill: logo-design (skills/logo-design/logo_design.py + design_tokens.json). Generates transparent, print-DPI vector emblems (seal-scales/seal-star/seal-quill/monogram). design_tokens.json = calibrated brand artifacts (palette, typography, emblem placement).
- Integrated: kdp-print cover builder now takes --emblem/--emblem-scale/--emblem-y to overlay a vector emblem on a clean background. Also replaced hard scrims with gradient scrims (no seam).
- Skill drafts awaiting save: logo-design (8ghfUTzY) and kdp-print FINAL (V1nzZOZD, supersedes earlier a8z20t9i). All project files zipped for the user's local folder.


--- New skill: book-illustration-concepts ---
Created (draft SKILLCONFIG_WVOZdfPE) at skills/book-illustration-concepts/. Files: SKILL.md (phased workflow), storyboard.py (contact-sheet + storyboard-PDF assembler, tested OK), style_bible_template.json (consistency backbone). Bakes in model selection (NB2 explore / NB2 Pro hero / GPT Image 2 for text) and the consistency keystone (cast hero portrait -> reuse as referenceImages -> accumulate -> style bible). Copilot has skillScope=all so it auto-discovers once saved. Copilot now has 3 skills: kdp-print, logo-design, book-illustration-concepts. Still pending from earlier pivots: 2 cover colorways (green/gold, burgundy/cream) and the final deliverables zip (kdp_print.py --text feature finished).


--- Colorways + zip DONE ---
kdp_print.py --text feature fully wired (compiles OK). Built 2 colorway covers via the calibrated pipeline (recolored guilloche bg + gold vector seal): cover-wrap-green.pdf (deep green/gold, white text) and cover-wrap-burgundy.pdf (burgundy, cream text). Book 1 now has 4 cover options: navy AI (cover-wrap.pdf), navy vector (cover-wrap-vector.pdf), green/gold, burgundy/cream. Exported playbook to books/notary-log-book/PUBLISHING_PLAYBOOK.md and added README.md. Rebuilt project zip (30 files, mirrors folder) -> [[FILE_iklmk6ix]]. All pivots now resolved.


--- QA / consolidation review (2026-07-28) ---
Reviewed user's 4 consolidated docs. Verified actual PDFs: interior=120pp/6x9 with pre-numbered entries; cover-wrap-green=12.58x9.25/spine 0.3302, contains "MERIDIAN PRESS", no "Djerjour". FINDING: attached MASTER_REFERENCE.md was stale v1 (still had 40% royalty/$2.80 printing, 0.625" gutter, 1256x925 "300 DPI" Canva, 100 entries, Djerjour byline, navy). Wrote corrected MASTER_REFERENCE.md v2 (60% royalty/$2.44/$5.35, 0.5" gutter, 3774x2775, 110 entries/120pp, Meridian Press, green official, 3 categories, corrected fast-follow royalties). PUBLISHING_PLAYBOOK.md was accurate; fixed 2 nits (upload step author->Meridian Press; added official-green row). MARKET_ANALYSIS.md is sound and aligned (uses correct 60%/$2.44); its market figures (search volumes, competitor stats, 500+ reviews) are estimates to verify live if needed. Rebuilt zip (43 files) with corrected reference + market analysis. Live playbook doc Upload Steps fixed.

## Plan Overview

Revised approach after reviewing your project: adopt your existing work as the foundation instead of starting over. Your HYPERAGENT_MASTER_PROMPT, MASTER_REFERENCE, kdp_print.py, and the two skill docs are a strong base. I will harden and correct them, implement the premium notary design you documented but have not yet coded, produce a genuinely print-ready Book 1, then stand up the copilot as a real Hyperagent named agent with the skill registered and your account context saved as memory.

Issues I found while reading the files, and how I will resolve each:

1. Cover wrap generator is broken. build_cover_wrap reads a spine_thickness_px key, but calculate_specs only returns spine_thickness, so it crashes with a KeyError. The front, spine, and back layout math and bleed placement are also off. I will fix the key, correct the layout, and validate output dimensions.

2. Interior gutter margin is never applied. generate_notary_interior computes the gutter but then uses the 0.25 inch outside margin on both left and right, so the binding edge is too tight for KDP. I will apply proper mirrored inner and outer margins per page.

3. Documented premium design is not implemented. The notary-journal skill describes one full entry per page with sections A to I, a thumbprint box, an official seal, plus cover, instructions, and index pages. The actual kdp_print output is a simpler two entries per page form with no front matter. I will implement the premium design in code so the output matches the promise.

4. Royalty model is mislabeled. Your docs use a flat 40 percent royalty. Verified against 2026 KDP rules: paperbacks earn 60 percent of list minus printing cost on Amazon, and 40 percent minus printing cost only on Expanded Distribution. As of June 2025 the Amazon rate drops to 50 percent if list price is below a marketplace threshold. I will correct the model and recompute.

5. Pricing numbers refined. Verified B&W printing cost is about 1.00 fixed plus 0.012 per page, so a 120 page 6 by 9 book costs about 2.44 to print. At 12.99 and 60 percent, net is about 5.35 per Amazon sale, not the 5.20 your doc estimated.

6. Canva canvas size is at the wrong DPI. MASTER_REFERENCE says a 1256 by 925 pixel canvas at 300 DPI, but that pixel size is only 100 DPI. At true 300 DPI the full wrap is 3774 by 2775 pixels. The bleed of 37.5 pixels and spine of 99 pixels are already correct. I will fix the canvas size.

7. Gutter value conflict. The master prompt lists a 0.625 inch gutter while the reference and code use 0.375 inch for 120 pages. KDP requires only 0.375 inch at this page count. I will standardize on a comfortable 0.5 inch inside margin and note the rule.

8. Books 2 and 3 mismatch. Your original brief listed a Daily Gratitude Journal at 5 by 8 and an English Grammar Workbook at 8.5 by 11. Your files instead list a Password Log Book and a Running Log Book. I need you to confirm which two are the real pipeline before I finalize the fast-follow specs.

Copilot build: I will create the Hyperagent named agent from your corrected master prompt, register the fixed kdp-print skill in the knowledge base, save your account details and locked rules as memory, and enable the tools it needs, which are image generation for covers, web search for keyword and category research, browser for the KDP dashboard walkthrough, and documents and tables for playbooks and the pipeline tracker.

## Plan Tasks

- [x] Lock reconciled specs and corrected royalty model (Books 2 and 3 pipeline still pending user confirmation).
- [x] Rewrite the notary interior generator to the premium one entry per page design (cover, instructions, A–I, thumbprint, seal, index), mirrored margins.
- [x] Fix the cover wrap builder crash and layout (front, spine, back at 300 DPI, correct bleed, no printed guides on the upload file).
- [x] Regenerate and validate the Book 1 interior PDF (120 pages, checked visually).
- [x] Design Book 1 cover art and assemble the print-ready wrap + a proof with guides.
- [x] Corrected Canva setup (true 300 DPI canvas) and a social media asset set (square mockup + vertical pin).
- [x] Corrected Book 1 publishing playbook (pricing, royalty, keywords, categories, description, checklist, upload steps, Algeria tax).
- [x] Register the corrected kdp-print skill (draft awaiting user save).
- [x] Create the KDP Publishing Copilot agent (draft awaiting user save) + account memory draft.
- [x] Package Book 1 deliverables. PENDING: user to confirm Books 2 and 3 so I can finalize their specs.
