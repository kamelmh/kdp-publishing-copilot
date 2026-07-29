---
name: book-illustration-concepts
description: >
  A structured workflow for generating book illustration and cover-art concepts that stay
  coherent across a whole book — same world, same hand, same characters. Use when the user
  wants illustration ideas, concept art, character designs, storyboards, picture-book spreads,
  or illustrated cover key-art. Bakes in model selection (Nano Banana 2 / Nano Banana Pro /
  GPT Image 2), the character/style CONSISTENCY method (reference images + a style bible), and
  a storyboard assembler for presentation. Pairs with logo-design and kdp-print.
---

# Book Illustration Concepts — Workflow Skill

A book is not a picture; it is a **visual system**. Any single image is easy — the craft is making
every spread feel like one hand drew one world with the same characters. This skill is built around
that: lock a **style bible** and a **cast of reference portraits**, then render everything against them.

Generation uses the **GenerateImage** tool (not a script). This skill supplies the method, the
model choices, the consistency technique, and a `storyboard.py` assembler for the final review deck.

## Files
- `storyboard.py` — assemble concept frames into a contact-sheet PNG (+ optional storyboard PDF).
- `style_bible_template.json` — the consistency backbone; fill once per book, quote it in every prompt.

## Model selection (baked in)
| Need | Model | Notes |
|---|---|---|
| Fast exploration, moodboards, most scenes | **Nano Banana 2** (`gemini-3.1-flash-image`, default) | cheap, Pro-level, up to 4K, up to 14 reference images |
| Hero character sheets, key-art / covers | **Nano Banana Pro** (`gemini-3-pro-image`) | max fidelity; use for canonical references |
| Any legible TEXT inside the image (signage, in-world words) | **GPT Image 2** (`openai/gpt-image-2`) | best text rendering; caps ~1.5K |
| Real-world grounding before inventing | **SearchImages** | pull real references, then diverge |

Rule of thumb: explore on Nano Banana 2, cast heroes on Pro, put words on GPT Image 2. Never bake
the book title or large copy into AI art — set type as vector in the layout tool.

## The consistency keystone (the part that matters most)
1. **Cast first.** Generate a canonical **hero portrait** per character on Nano Banana Pro (2–3 options; pick one).
2. **Reuse everywhere.** Pass that portrait as `referenceImages` (or `inputImages`) in EVERY scene the
   character appears in. This is what stops the face/outfit drifting page to page.
3. **Accumulate references.** Feed an approved scene back in as an additional reference so lighting,
   palette, and atmosphere carry forward to the next scene.
4. **Write it down.** Fill `style_bible_template.json` (palette, medium, line, light, shapes, characters,
   do/don't) and quote its values in every prompt. Same idea as the logo-design `design_tokens.json`.

## Workflow

**Phase 1 — Art brief.** Distill the manuscript to one page: audience, tone, 4–6 emotional beats,
recurring motifs, 3 must-draw scenes. Commit to a concrete *register* (not "nice illustration" but
"gouache storybook, warm dusk palette, rounded shapes, soft grain").

**Phase 2 — Moodboard & style exploration.** `SearchImages` for 4–6 real anchors, then fan out 3
divergent directions on Nano Banana 2. Example:
> "Children's picture-book illustration: a small fox with a paper lantern in a moonlit birch forest —
> gouache texture, warm amber + deep teal, rounded friendly shapes, soft paper grain." … then the same
> scene as "flat cut-paper collage, 4-color palette" … and "loose watercolor + ink, lots of white space."
Pick a lane.

**Phase 3 — Write the style bible.** Lock the winner into `style_bible_template.json`.

**Phase 4 — Cast the characters.** Nano Banana Pro hero portrait per character (front + 3/4 views,
neutral background), 2–3 options, choose one. This becomes the reference for all scenes.

**Phase 5 — Render scene concepts (storyboard).** For each beat, `GenerateImage({ inputImages:
[heroPortrait, styleAnchor], prompt: "<action>, <camera/composition>, <style-bible descriptors>" })`.
Vary composition deliberately: wide establishing / intimate close-up / dynamic action.

**Phase 6 — Refine by editing, not re-rolling.** Iterate on a chosen frame with targeted edits
("keep everything, make the expression more playful, warm the light"). Switch to GPT Image 2 if a
frame needs real words.

**Phase 7 — Present & iterate.** Download the chosen frames (FetchStoredFile), then:
```bash
python storyboard.py --images s1.png s2.png s3.png \
    --captions "Opening" "Discovery" "Climax" \
    --title "Working Title — Concept Storyboard" --cols 3 --out storyboard.png --pdf storyboard.pdf
```
Share for feedback; version and iterate. For an illustrated **cover**, hand the final key-art to the
`kdp-print` cover builder (`--front`), which lays vector title/author/spine at 300 DPI with correct bleed.

## Artistic tips
One clear focal point per spread · strong value contrast (squint test) · limited 3–4 color palette ·
give each character a distinct silhouette · leading lines toward the subject.

## Technical tips
Lock the aspect ratio to the page early · keep a "reference kit" folder (hero portraits + 1–2 hero
scenes) and feed it into every generation · concept at ~150 DPI, finalize covers at 300 DPI via kdp-print.

## Pairs with
`logo-design` (emblems/marks, design tokens) and `kdp-print` (print-ready interior + cover assembly).
