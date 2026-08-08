#!/usr/bin/env python3
"""Generate the light and dark profile banners.

Two files, one source of truth. Run after editing copy or numbers:

    python scripts/make_banner.py

Design notes, so the next edit does not undo them:

* The viewBox is 1000 wide on purpose. GitHub renders README content at roughly
  900px, so any type below about 1.5% of the viewBox width lands under 13px and
  stops being readable. Nothing here goes below 16.
* No <style> block, no external font, no inline <svg> in the README. GitHub
  proxies README images through camo and renders them inside an <img>, so the
  file has to stand alone on presentation attributes.
* Palette and mark are lifted from coconutlabs.org so the profile and the site
  read as one thing.
"""

import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

FONT = "ui-sans-serif,-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"

THEMES = {
    "light": {
        "bg": "#F7F3E8",
        "panel": "#EFE9DA",
        "rule": "#DCD2BE",
        "ink": "#1A1611",
        "muted": "#6C6252",
        "faint": "#94897A",
        "accent": "#9B6B1F",
        "green": "#4A5B49",
    },
    "dark": {
        "bg": "#161310",
        "panel": "#1E1A15",
        "rule": "#332C23",
        "ink": "#F2EDE0",
        "muted": "#A99E8C",
        "faint": "#7A7062",
        "accent": "#D0A04A",
        "green": "#8FA98C",
    },
}

W, H = 1000, 384

# The axis is log10 seconds, one nanosecond to one second.
LO, HI = -9.0, 0.0
AX_L, AX_R = 62, 938
AX_Y = 326

TICKS = [(-9, "1 ns"), (-6, "1 µs"), (-3, "1 ms"), (0, "1 s")]

# Two markers, not three. A third at 667 ns (1.5M ev/s inverted) collided with
# the 37 ns caption at render width, and it was the one derived number on an
# axis where everything else is measured directly. The span between these two
# is the point anyway.
MARKS = [
    (37e-9, "37 ns", "pre-trade risk gate"),
    (61.5e-3, "61.5 ms", "TTFT p99 under load"),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size, fill, weight="400", family=FONT, spacing=None,
         anchor="start"):
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    an = f' text-anchor="{anchor}"' if anchor != "start" else ""
    return (
        f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}"{ls}{an}>{esc(s)}</text>'
    )


def at(seconds):
    """Map a duration onto the axis."""
    f = (math.log10(seconds) - LO) / (HI - LO)
    return AX_L + f * (AX_R - AX_L)


def mark(x, y, scale, color):
    """The Coconut Labs mark: four dots in brackets, dotted dividers between.

    Native viewBox is 100x30. It reads as a queue of slots, which is a
    reasonable thing to carry on a profile that is mostly about scheduling.
    """
    g = [f'<g transform="translate({x},{y}) scale({scale})" fill="{color}">']
    for d in ("M 6,3 L 0,3 L 0,27 L 6,27", "M 94,3 L 100,3 L 100,27 L 94,27"):
        g.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2"/>')
    for cx in (17, 39, 61, 83):
        g.append(f'<circle cx="{cx}" cy="15" r="3"/>')
    for cx in (28, 50, 72):
        for cy in (6, 10.5, 15, 19.5, 24):
            g.append(f'<circle cx="{cx}" cy="{cy}" r="1.2"/>')
    g.append("</g>")
    return "".join(g)


def build(theme):
    c = THEMES[theme]
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" aria-label="Shrey Patel. '
        f'Systems and inference infrastructure. Work measured from 37 '
        f'nanoseconds to 61.5 milliseconds.">',
        f'<rect width="{W}" height="{H}" rx="16" fill="{c["bg"]}"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="15.5" '
        f'fill="none" stroke="{c["rule"]}"/>',
        mark(62, 40, 0.62, c["accent"]),
        text(62, 148, "Shrey Patel", 66, c["ink"], "700", spacing="-1.8"),
        text(64, 190, "Systems and inference infrastructure.", 27, c["muted"],
             "500"),
        text(64, 238, "TIME PER OPERATION, ACROSS WHAT I BUILD", 16, c["faint"],
             "700", spacing="1.8"),
    ]

    # Axis. The stretch my work actually spans gets the accent weight.
    p.append(f'<line x1="{AX_L}" y1="{AX_Y}" x2="{AX_R}" y2="{AX_Y}" '
             f'stroke="{c["rule"]}" stroke-width="2"/>')
    p.append(f'<line x1="{at(MARKS[0][0]):.1f}" y1="{AX_Y}" '
             f'x2="{at(MARKS[-1][0]):.1f}" y2="{AX_Y}" '
             f'stroke="{c["accent"]}" stroke-width="2" opacity="0.45"/>')
    for exp, label in TICKS:
        x = at(10 ** exp)
        anchor = "start" if exp == -9 else "end" if exp == 0 else "middle"
        p.append(f'<line x1="{x:.1f}" y1="{AX_Y-6}" x2="{x:.1f}" y2="{AX_Y+6}" '
                 f'stroke="{c["rule"]}" stroke-width="2"/>')
        p.append(text(f"{x:.1f}", AX_Y + 30, label, 17, c["faint"], "500",
                      family=MONO, anchor=anchor))

    # Markers, labelled above so they never collide with the tick row.
    for seconds, value, caption in MARKS:
        x = at(seconds)
        p.append(f'<line x1="{x:.1f}" y1="{AX_Y-22}" x2="{x:.1f}" y2="{AX_Y}" '
                 f'stroke="{c["accent"]}" stroke-width="2"/>')
        p.append(f'<circle cx="{x:.1f}" cy="{AX_Y}" r="7" fill="{c["accent"]}"/>')
        p.append(f'<circle cx="{x:.1f}" cy="{AX_Y}" r="3" fill="{c["bg"]}"/>')
        p.append(text(f"{x:.1f}", AX_Y - 32, value, 23, c["ink"], "700",
                      family=MONO, anchor="middle"))
        p.append(text(f"{x:.1f}", AX_Y - 54, caption, 16, c["muted"], "500",
                      anchor="middle"))

    p.append("</svg>")
    return "\n".join(p)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name in THEMES:
        path = OUT / f"banner-{name}.svg"
        path.write_text(build(name), encoding="utf-8")
        print(f"wrote {path}")
