#!/usr/bin/env python3
"""
Logo / Emblem Design Skill — generate clean, calibrated vector-style emblems for
book covers and brand use. Pure Pillow, supersampled for crisp edges, exported as
transparent RGBA PNG at print DPI so the same emblem drops onto any background.

These are "calibrated design artifacts": one emblem, produced at a known size/DPI on a
transparent field, reusable across covers, spines, social assets, and A+ content.

Usage:
    python logo_design.py --motif seal-scales --size 1200 --out emblem.png
    python logo_design.py --motif seal-star   --gold "#C9A227" --out star.png --preview-bg "#1B2A4A"
    python logo_design.py --motif monogram --initials "ND" --out monogram.png

Motifs: seal-scales | seal-star | seal-quill | monogram
"""

import argparse
import math
from PIL import Image, ImageDraw, ImageFont

SS = 4  # supersample factor for smooth edges


def _hex(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def _star_points(cx, cy, r_out, r_in, n=5, rot=-math.pi / 2):
    pts = []
    for i in range(n * 2):
        r = r_out if i % 2 == 0 else r_in
        a = rot + i * math.pi / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def _draw_ring(d, cx, cy, r, width, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=width)


def _draw_star_ring(d, cx, cy, radius, star_r, n, color):
    for k in range(n):
        a = -math.pi / 2 + k * 2 * math.pi / n
        sx, sy = cx + radius * math.cos(a), cy + radius * math.sin(a)
        d.polygon(_star_points(sx, sy, star_r, star_r * 0.42), fill=color)


def _draw_scales(d, cx, cy, w, color, lw):
    """Elegant balance-scales line-art with hanging bowl pans, centered at (cx, cy)."""
    top = cy - w * 0.50          # beam height
    base_y = cy + w * 0.60
    beam = w * 0.50
    pan = w * 0.22
    thin = max(1, lw - 1)
    # finial (small diamond) + central post
    d.polygon(_star_points(cx, top - w * 0.11, w * 0.06, w * 0.028, 4, 0), fill=color)
    d.line([(cx, top - w * 0.05), (cx, base_y - w * 0.14)], fill=color, width=lw)
    # beam + center knob
    d.line([(cx - beam, top), (cx + beam, top)], fill=color, width=lw)
    d.ellipse([cx - lw, top - lw, cx + lw, top + lw], fill=color)
    # hanging bowl pans
    for sx in (cx - beam, cx + beam):
        py = top + w * 0.34
        d.line([(sx, top), (sx - pan * 0.9, py)], fill=color, width=thin)
        d.line([(sx, top), (sx + pan * 0.9, py)], fill=color, width=thin)
        d.arc([sx - pan, py - pan * 0.55, sx + pan, py + pan * 0.95], start=12, end=168,
              fill=color, width=lw)
    # base
    d.line([(cx - w * 0.30, base_y - w * 0.14), (cx + w * 0.30, base_y - w * 0.14)], fill=color, width=lw)
    d.line([(cx - w * 0.30, base_y - w * 0.14), (cx - w * 0.20, base_y)], fill=color, width=thin)
    d.line([(cx + w * 0.30, base_y - w * 0.14), (cx + w * 0.20, base_y)], fill=color, width=thin)
    d.line([(cx - w * 0.22, base_y), (cx + w * 0.22, base_y)], fill=color, width=lw + 1)


def _draw_quill(d, cx, cy, w, color, lw):
    """Feather quill on a diagonal."""
    x0, y0 = cx - w * 0.42, cy + w * 0.5
    x1, y1 = cx + w * 0.42, cy - w * 0.5
    d.line([(x0, y0), (x1, y1)], fill=color, width=lw)             # shaft
    steps = 14
    for i in range(1, steps):
        t = i / steps
        bx, by = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        barb = w * 0.22 * (1 - t) + w * 0.03
        nx, ny = -(y1 - y0), (x1 - x0)
        L = math.hypot(nx, ny)
        nx, ny = nx / L, ny / L
        d.line([(bx, by), (bx + nx * barb, by + ny * barb)], fill=color, width=max(1, lw - 2))
    d.line([(x0, y0), (x0 - w * 0.06, y0 + w * 0.10)], fill=color, width=lw)  # nib


def _center_text(d, cx, cy, text, font, color):
    l, t, r, b = d.textbbox((0, 0), text, font=font)
    d.text((cx - (r - l) / 2 - l, cy - (b - t) / 2 - t), text, font=font, fill=color)


def make_emblem(motif="seal-scales", size=1200, gold="#C9A227", ink="#1B2A4A",
                initials="ND", out="emblem.png", preview_bg=None):
    S = size * SS
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    g = _hex(gold)
    cx = cy = S / 2
    R = S * 0.46
    lw = max(2, int(S * 0.006))

    if motif.startswith("seal"):
        _draw_ring(d, cx, cy, R, lw + 2, g)
        _draw_ring(d, cx, cy, R * 0.90, lw, g)
        _draw_star_ring(d, cx, cy, R * 0.79, S * 0.018, 32, g)
        _draw_ring(d, cx, cy, R * 0.68, lw, g)
        core = R * 0.60
        if motif == "seal-scales":
            _draw_scales(d, cx, cy, core, g, lw + 1)
        elif motif == "seal-quill":
            _draw_quill(d, cx, cy, core, g, lw + 1)
        else:  # seal-star
            d.polygon(_star_points(cx, cy, core * 0.6, core * 0.26), fill=g)
    elif motif == "monogram":
        _draw_ring(d, cx, cy, R, lw + 2, g)
        _draw_ring(d, cx, cy, R * 0.90, lw, g)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", int(S * 0.34))
        except Exception:
            font = ImageFont.load_default()
        _center_text(d, cx, cy, initials.upper(), font, g)
    else:
        raise ValueError(f"Unknown motif: {motif}")

    img = img.resize((size, size), Image.LANCZOS)
    img.save(out)
    print(f"Emblem: {out}  ({size}x{size}px RGBA, motif={motif})")

    if preview_bg:
        bg = Image.new("RGBA", (size, size), _hex(preview_bg) + (255,))
        bg.alpha_composite(img)
        pv = out.rsplit(".", 1)[0] + "_preview.png"
        bg.convert("RGB").save(pv)
        print(f"Preview: {pv}  (on {preview_bg})")
    return out


def main():
    p = argparse.ArgumentParser(description="Logo/Emblem generator (transparent PNG)")
    p.add_argument("--motif", default="seal-scales",
                   choices=["seal-scales", "seal-star", "seal-quill", "monogram"])
    p.add_argument("--size", type=int, default=1200, help="output px (square)")
    p.add_argument("--gold", default="#C9A227")
    p.add_argument("--ink", default="#1B2A4A")
    p.add_argument("--initials", default="ND")
    p.add_argument("--out", required=True)
    p.add_argument("--preview-bg", default=None, help="hex bg for a flattened preview")
    a = p.parse_args()
    make_emblem(a.motif, a.size, a.gold, a.ink, a.initials, a.out, a.preview_bg)


if __name__ == "__main__":
    main()
