#!/usr/bin/env python3
"""
Storyboard / concept-sheet assembler for the book-illustration-concepts workflow.

Turns a set of generated concept images into the Phase 7 "present & iterate" deliverable:
  (a) a contact-sheet PNG grid with numbered captions and a title bar, and
  (b) an optional one-frame-per-page storyboard PDF.

The image GENERATION happens with the GenerateImage tool (Nano Banana 2 / Pro / GPT Image 2).
This script only lays out the results for review — download the frames first (FetchStoredFile),
then point this at them.

Usage:
  python storyboard.py --images s1.png s2.png s3.png \
      --captions "Opening" "Discovery" "Climax" \
      --title "The Lantern Fox - Concept Storyboard" --cols 3 --out storyboard.png --pdf storyboard.pdf
  python storyboard.py --manifest frames.json --title "..." --out sheet.png
      # frames.json: [{"image":"s1.png","caption":"Opening spread"}, ...]
"""
import argparse
import json
import os
from PIL import Image, ImageDraw, ImageFont


def _font(size):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def load_items(args):
    if args.manifest:
        data = json.load(open(args.manifest))
        return [(d["image"], d.get("caption", "")) for d in data]
    caps = args.captions or []
    return [(img, caps[i] if i < len(caps) else "") for i, img in enumerate(args.images)]


def contact_sheet(items, cols, out, title, cell=560, pad=24,
                  bg=(18, 20, 26), fg=(235, 235, 240)):
    n = len(items)
    rows = (n + cols - 1) // cols
    cap_h, title_h = 48, (84 if title else 0)
    cw, ch = cell, cell + cap_h
    W = cols * cw + pad * (cols + 1)
    H = title_h + rows * ch + pad * (rows + 1)
    sheet = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(sheet)
    if title:
        d.text((pad, pad + 8), title, font=_font(38), fill=fg)
    tf = _font(24)
    for idx, (img, cap) in enumerate(items):
        r, c = divmod(idx, cols)
        x = pad + c * (cw + pad)
        y = title_h + pad + r * (ch + pad)
        try:
            im = Image.open(img).convert("RGB")
        except Exception:
            im = Image.new("RGB", (cell, cell), (60, 60, 66))
            ImageDraw.Draw(im).text((12, 12), "missing:\n" + os.path.basename(img),
                                    font=tf, fill=(210, 120, 120))
        im.thumbnail((cw, cell), Image.LANCZOS)
        ox, oy = x + (cw - im.width) // 2, y + (cell - im.height) // 2
        d.rectangle([x - 2, y - 2, x + cw + 2, y + cell + 2], outline=(70, 74, 84), width=2)
        sheet.paste(im, (ox, oy))
        label = f"{idx + 1}. {cap}" if cap else f"{idx + 1}."
        d.text((x, y + cell + 12), label[:64], font=tf, fill=fg)
    sheet.save(out)
    print(f"Contact sheet: {out}  ({W}x{H}px, {n} frames)")
    return out


def storyboard_pdf(items, out, title):
    from reportlab.lib.pagesizes import landscape, letter
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    W, H = landscape(letter)
    c = canvas.Canvas(out, pagesize=(W, H))
    for idx, (img, cap) in enumerate(items):
        c.setFillColorRGB(0.07, 0.08, 0.10)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        try:
            ir = ImageReader(img)
            iw, ih = ir.getSize()
            ar = iw / ih
            maxw, maxh = W - 2 * inch, H - 1.8 * inch
            w = min(maxw, maxh * ar)
            h = w / ar
            c.drawImage(ir, (W - w) / 2, (H - h) / 2 + 0.2 * inch, width=w, height=h,
                        preserveAspectRatio=True, mask="auto")
        except Exception:
            pass
        c.setFillColorRGB(0.92, 0.92, 0.94)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(0.6 * inch, 0.6 * inch, f"{idx + 1}. {cap}")
        if title:
            c.setFont("Helvetica", 9)
            c.drawRightString(W - 0.6 * inch, 0.6 * inch, title)
        c.showPage()
    c.save()
    print(f"Storyboard PDF: {out}  ({len(items)} pages)")


def main():
    p = argparse.ArgumentParser(description="Assemble concept images into a storyboard/contact sheet.")
    p.add_argument("--images", nargs="*", default=[])
    p.add_argument("--captions", nargs="*", default=[])
    p.add_argument("--manifest", help="JSON list of {image, caption}")
    p.add_argument("--title", default="")
    p.add_argument("--cols", type=int, default=3)
    p.add_argument("--out", required=True, help="contact-sheet PNG path")
    p.add_argument("--pdf", help="also write a one-frame-per-page storyboard PDF")
    a = p.parse_args()
    items = load_items(a)
    if not items:
        p.error("no images provided (use --images or --manifest)")
    contact_sheet(items, a.cols, a.out, a.title)
    if a.pdf:
        storyboard_pdf(items, a.pdf, a.title)


if __name__ == "__main__":
    main()
