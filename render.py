#!/usr/bin/env python3
"""
render.py - Anand Agro Agencies Instagram posters, 1080x1350 JPEG.

Usage:
    python3 render.py specs/2026-11-15.json    # writes posters/Day-NN.jpg, exit code 1 if any overflow

A spec file is a JSON list. Each item:
    {"day": 31, "kind": "tip",      "kicker": "शेती सल्ला", "title": "...", "points": ["...", "..."], "cta": "..."}
    {"day": 32, "kind": "offer",    "kicker": "बुकिंग सुरू", "title": "...", "highlight": "₹16 प्रति रोप", "points": [...], "cta": "..."}
    {"day": 33, "kind": "question", "kicker": "तुमचं मत",   "title": "...", "options": ["केळी", "ऊस"], "cta": "कमेंटमध्ये लिहा"}
    {"day": 34, "kind": "message",  "kicker": "आमच्याविषयी", "title": "...", "body": "...", "cta": "..."}

Rules the text must follow (checked by a human before Status = Ready):
  - no pesticide or fertiliser doses (say "लेबलवरील प्रमाणानुसार" instead)
  - no yield or income guarantees, no health claims
  - points: 2 to 5, each short (under ~40 characters reads best)
Text that does not fit is shrunk automatically; if it still overflows the script reports it.
"""
import html
import json
import pathlib
import sys
import urllib.request

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent
FONTS = ROOT / "fonts"
OUT = ROOT / "posters"
FONT_URL = ("https://raw.githubusercontent.com/notofonts/notofonts.github.io/main/"
            "fonts/NotoSansDevanagari/hinted/ttf/NotoSansDevanagari-{}.ttf")


def ensure_fonts():
    """Fonts live in fonts/. If a fresh checkout lacks them, fetch them (OFL licence)."""
    FONTS.mkdir(exist_ok=True)
    for weight in ("Regular", "SemiBold", "Bold"):
        path = FONTS / f"NotoSansDevanagari-{weight}.ttf"
        if not path.exists() or path.stat().st_size < 100_000:
            urllib.request.urlretrieve(FONT_URL.format(weight), path)

SHOP = "आनंद अ‍ॅग्रो एजन्सीज"
PLACE = "शेलगाव (वांगी), ता. करमाळा"
PHONE = "9284188428"

GREEN = "#1E5631"      # main brand colour
LEAF = "#3C8D40"       # secondary green, used for small marks
CREAM = "#F7F3E6"      # background
ACCENT = "#E8A317"     # turmeric yellow, the single accent
INK = "#22261F"
SOFT = "#4A5145"

LEAF_SVG = f"""<svg viewBox="0 0 120 120" width="96" height="96">
<path d="M60 110 C60 80 60 55 60 30" stroke="{CREAM}" stroke-width="7" fill="none" stroke-linecap="round"/>
<path d="M60 62 C30 62 16 44 14 22 C38 22 56 36 60 62 Z" fill="{ACCENT}"/>
<path d="M60 48 C88 48 104 30 106 8 C80 8 63 22 60 48 Z" fill="{CREAM}"/></svg>"""

PHONE_SVG = f"""<svg viewBox="0 0 24 24" width="40" height="40"><path fill="{ACCENT}"
d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>"""

CSS = f"""
@font-face {{ font-family: Deva; src: url('file://{FONTS}/NotoSansDevanagari-Regular.ttf'); font-weight: 400; }}
@font-face {{ font-family: Deva; src: url('file://{FONTS}/NotoSansDevanagari-SemiBold.ttf'); font-weight: 600; }}
@font-face {{ font-family: Deva; src: url('file://{FONTS}/NotoSansDevanagari-Bold.ttf'); font-weight: 700; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1350px; background: {CREAM}; }}
body {{ font-family: Deva, sans-serif; color: {INK}; position: relative; overflow: hidden; --s: 1; }}
.top {{ position: absolute; left: 0; right: 0; top: 0; height: 170px; background: {GREEN};
        display: flex; align-items: center; justify-content: space-between; padding: 0 72px; }}
.shop {{ color: {CREAM}; font-weight: 700; font-size: 50px; line-height: 1.2; }}
.place {{ color: #CFE3C9; font-weight: 400; font-size: 30px; margin-top: 4px; }}
.wrap {{ position: absolute; left: 72px; right: 72px; top: 230px; bottom: 210px;
         display: flex; flex-direction: column; justify-content: center; }}
.kicker {{ align-self: flex-start; background: {ACCENT}; color: {INK}; font-weight: 700;
           font-size: calc(36px * var(--s)); padding: 8px 28px; border-radius: 40px; margin-bottom: calc(34px * var(--s)); }}
h1 {{ font-weight: 700; color: {GREEN}; font-size: calc(86px * var(--s)); line-height: 1.32; text-wrap: balance; }}
.points {{ list-style: none; margin-top: calc(44px * var(--s)); }}
.points li {{ display: flex; align-items: flex-start; font-weight: 600; font-size: calc(48px * var(--s));
              line-height: 1.38; color: {INK}; padding: calc(14px * var(--s)) 0; }}
.points .n {{ flex: 0 0 auto; width: calc(66px * var(--s)); height: calc(66px * var(--s)); border-radius: 50%;
              background: {GREEN}; color: {CREAM}; font-size: calc(36px * var(--s)); display: flex;
              align-items: center; justify-content: center; margin-right: 28px; margin-top: calc(2px * var(--s)); }}
.highlight {{ margin-top: calc(36px * var(--s)); font-weight: 700; font-size: calc(124px * var(--s)); line-height: 1.15;
              color: {ACCENT}; -webkit-text-stroke: 2px {GREEN}; }}
.body {{ margin-top: calc(40px * var(--s)); font-weight: 400; font-size: calc(50px * var(--s)); line-height: 1.55; color: {SOFT}; }}
.options {{ display: flex; flex-wrap: wrap; gap: calc(26px * var(--s)); margin-top: calc(56px * var(--s)); }}
.options span {{ border: 5px solid {GREEN}; border-radius: 28px; padding: calc(16px * var(--s)) calc(40px * var(--s));
                 font-weight: 700; font-size: calc(54px * var(--s)); color: {GREEN}; background: #fff; }}
.cta {{ margin-top: calc(48px * var(--s)); font-weight: 700; font-size: calc(46px * var(--s)); color: {LEAF}; }}
.foot {{ position: absolute; left: 0; right: 0; bottom: 0; height: 150px; background: {GREEN};
         display: flex; align-items: center; padding: 0 72px; gap: 22px; }}
.foot .ph {{ color: {CREAM}; font-weight: 700; font-size: 48px; letter-spacing: 1px; }}
.foot .lbl {{ color: #CFE3C9; font-weight: 400; font-size: 32px; margin-left: auto; }}
"""


def esc(t):
    return html.escape(str(t), quote=False)


def body_for(spec):
    kind = spec.get("kind", "tip")
    parts = []
    if spec.get("kicker"):
        parts.append(f'<div class="kicker">{esc(spec["kicker"])}</div>')
    parts.append(f'<h1>{esc(spec["title"])}</h1>')
    if kind == "offer" and spec.get("highlight"):
        parts.append(f'<div class="highlight">{esc(spec["highlight"])}</div>')
    if kind in ("tip", "offer") and spec.get("points"):
        lis = "".join(f'<li><span class="n">{i}</span><span>{esc(p)}</span></li>'
                      for i, p in enumerate(spec["points"], 1))
        parts.append(f'<ul class="points">{lis}</ul>')
    if kind == "question" and spec.get("options"):
        parts.append('<div class="options">' + "".join(f"<span>{esc(o)}</span>" for o in spec["options"]) + "</div>")
    if kind == "message" and spec.get("body"):
        parts.append(f'<div class="body">{esc(spec["body"])}</div>')
    if spec.get("cta"):
        parts.append(f'<div class="cta">{esc(spec["cta"])}</div>')
    return "".join(parts)


def page(spec):
    return f"""<!doctype html><html lang="mr"><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="top"><div><div class="shop">{SHOP}</div><div class="place">{PLACE}</div></div>{LEAF_SVG}</div>
<div class="wrap">{body_for(spec)}</div>
<div class="foot">{PHONE_SVG}<span class="ph">{PHONE}</span><span class="lbl">कॉल / WhatsApp</span></div>
</body></html>"""


FIT_JS = """() => {
  const w = document.querySelector('.wrap');
  let s = 1;
  const fits = () => w.scrollHeight <= w.clientHeight + 1 && w.scrollWidth <= w.clientWidth + 1;
  while (!fits() && s > 0.6) { s -= 0.04; document.body.style.setProperty('--s', s.toFixed(2)); }
  return {scale: Number(s.toFixed(2)), fits: fits()};
}"""


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    specs = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    ensure_fonts()
    OUT.mkdir(exist_ok=True)
    bad = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        pg = browser.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for spec in specs:
            name = f"Day-{int(spec['day']):02d}.jpg"
            tmp = OUT / f".{name}.html"
            tmp.write_text(page(spec), encoding="utf-8")
            pg.goto(tmp.as_uri())
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(250)
            fit = pg.evaluate(FIT_JS)
            pg.screenshot(path=str(OUT / name), type="jpeg", quality=88)
            tmp.unlink()
            status = "ok" if fit["fits"] else "OVERFLOW"
            bad += 0 if fit["fits"] else 1
            print(f"{name}: {status} (scale {fit['scale']})")
        browser.close()
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
