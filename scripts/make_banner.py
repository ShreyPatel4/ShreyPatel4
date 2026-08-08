#!/usr/bin/env python3
"""Generate the light and dark profile banners.

Two files, one source of truth. Run after editing copy or numbers:

    python scripts/make_banner.py

Everything is presentation attributes, no <style> block and no external font,
because GitHub proxies README images through camo and renders them in an <img>.
"""

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

FONT = "ui-sans-serif,-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"

THEMES = {
    "light": {
        "bg": "#FBF8F3",
        "card": "#F2ECE2",
        "rule": "#E2D9CA",
        "ink": "#17161A",
        "muted": "#6E6862",
        "faint": "#9A938B",
        "bad": "#B94F36",
        "good": "#2E7D5B",
        "chip": "#EDE5D9",
    },
    "dark": {
        "bg": "#0F0F13",
        "card": "#191921",
        "rule": "#2A2A34",
        "ink": "#ECE8E1",
        "muted": "#9C958D",
        "faint": "#6E6862",
        "bad": "#E07557",
        "good": "#4FB185",
        "chip": "#22222C",
    },
}

W, H = 1280, 300

# kvwarden Gate-2 result: A100-SXM4, Llama-3.1-8B, vLLM 0.19.1, two tenants,
# 300s sustained. Quiet-tenant TTFT p99. Bars are linear, which is the point.
ROWS = [
    ("solo, no contention", 53.9, "good"),
    ("FIFO under flooder", 1585.0, "bad"),
    ("kvwarden token-bucket", 61.5, "good"),
]

BAR_X, BAR_MAX = 918, 152
PEAK = max(v for _, v, _ in ROWS)


def ms(v):
    return f"{v:,.0f} ms" if v >= 1000 else f"{v:.1f} ms"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size, fill, weight="400", family=FONT, spacing=None, anchor="start"):
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    an = f' text-anchor="{anchor}"' if anchor != "start" else ""
    return (
        f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}"{ls}{an}>{esc(s)}</text>'
    )


def build(theme_name):
    c = THEMES[theme_name]
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" '
        f'aria-label="Shrey Patel, systems and inference infrastructure">',
        f'<rect width="{W}" height="{H}" rx="18" fill="{c["bg"]}"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="17.5" '
        f'fill="none" stroke="{c["rule"]}"/>',
    ]

    # Left column.
    p.append(text(64, 74, "BOSTON, MA   ·   OPEN TO SYSTEMS + INFRA ROLES",
                  15, c["faint"], "600", spacing="1.6"))
    p.append(text(62, 148, "Shrey Patel", 66, c["ink"], "700", spacing="-1.6"))
    p.append(text(64, 194, "Systems and inference infrastructure.",
                 26, c["muted"], "500"))

    chips = ["Rust", "C++20", "Python", "Go", "vLLM / SGLang", "Kubernetes", "AWS"]
    x = 64
    for label in chips:
        w = int(len(label) * 8.4) + 22
        p.append(f'<rect x="{x}" y="{220}" width="{w}" height="30" rx="15" '
                 f'fill="{c["chip"]}"/>')
        p.append(text(x + 11, 240, label, 14, c["muted"], "500", family=MONO))
        x += w + 9

    # Right column: the kvwarden hero result, drawn honestly on a linear scale.
    p.append(f'<rect x="736" y="34" width="{W-736-30}" height="{H-68}" rx="14" '
             f'fill="{c["card"]}"/>')
    p.append(text(766, 72, "QUIET-TENANT TTFT p99", 13, c["faint"], "700",
                  spacing="1.4"))
    p.append(text(766, 94, "one A100, two tenants, Llama-3.1-8B on vLLM",
                 13, c["faint"], "400"))

    y = 138
    for label, value, tone in ROWS:
        w = max(8, round(BAR_MAX * value / PEAK))
        p.append(text(766, y + 5, label, 14, c["muted"], "500"))
        p.append(f'<rect x="{BAR_X}" y="{y-8}" width="{w}" height="16" rx="4" '
                 f'fill="{c[tone]}"/>')
        p.append(text(1222, y + 5, ms(value), 14, c["ink"], "600",
                      family=MONO, anchor="end"))
        y += 48

    p.append("</svg>")
    return "\n".join(p)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name in THEMES:
        path = OUT / f"banner-{name}.svg"
        path.write_text(build(name), encoding="utf-8")
        print(f"wrote {path}")
