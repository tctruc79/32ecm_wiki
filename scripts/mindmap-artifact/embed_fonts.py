#!/usr/bin/env python3
"""
embed_fonts.py — produces self-hosted CSS with all fonts inlined as
data:font/woff2 base64 URIs (KaTeX's 20 math fonts + IBM Plex Sans/Mono),
so the final artifact makes zero external network calls.

Run once; writes katex_embedded.css and plex_embedded.css into assets/.
build_artifact.py reads those two output files directly.
"""

import base64
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")


def b64_of(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def embed_katex_css():
    css_path = os.path.join(ASSETS, "katex", "katex.min.css")
    fonts_dir = os.path.join(ASSETS, "katex", "fonts")
    css = open(css_path, encoding="utf-8").read()

    pattern = re.compile(
        r'url\(fonts/([^)]+?\.woff2)\) format\("woff2"\),'
        r'url\(fonts/[^)]+?\.woff\) format\("woff"\),'
        r'url\(fonts/[^)]+?\.ttf\) format\("truetype"\)'
    )

    count = [0]

    def repl(m):
        fname = m.group(1)
        fpath = os.path.join(fonts_dir, fname)
        data = b64_of(fpath)
        count[0] += 1
        return f'url(data:font/woff2;base64,{data}) format("woff2")'

    new_css = pattern.sub(repl, css)
    remaining = new_css.count("url(fonts/")
    print(f"KaTeX fonts embedded: {count[0]}, remaining unembedded url(fonts/): {remaining}")
    out_path = os.path.join(ASSETS, "katex_embedded.css")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(new_css)
    return out_path, count[0]


def embed_plex_css():
    css_path = os.path.join(ASSETS, "plex.css")
    fonts_dir = os.path.join(ASSETS, "plexfonts")
    css = open(css_path, encoding="utf-8").read()

    pattern = re.compile(r"url\((https://fonts\.gstatic\.com/[^)]+\.woff2)\) format\('woff2'\)")

    count = [0]

    def repl(m):
        url = m.group(1)
        fname = os.path.basename(url)
        fpath = os.path.join(fonts_dir, fname)
        data = b64_of(fpath)
        count[0] += 1
        return f"url(data:font/woff2;base64,{data}) format('woff2')"

    new_css = pattern.sub(repl, css)
    remaining = new_css.count("fonts.gstatic.com")
    print(f"Plex fonts embedded: {count[0]}, remaining external gstatic refs: {remaining}")
    out_path = os.path.join(ASSETS, "plex_embedded.css")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(new_css)
    return out_path, count[0]


if __name__ == "__main__":
    embed_katex_css()
    embed_plex_css()
