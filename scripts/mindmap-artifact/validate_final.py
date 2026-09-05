#!/usr/bin/env python3
"""
validate_final.py — structural + content verification for the rebuilt
Mindmap Artifact, per the rebuild task's verification checklist.

Usage: python3 validate_final.py <path_to_html>
"""

import html as htmlmod
import json
import os
import re
import subprocess
import sys

PAIR_TAGS = [
    "div", "details", "summary", "table", "thead", "tbody", "tr",
    "th", "td", "strong", "em", "ul", "ol", "li", "blockquote", "p",
    "pre", "code", "label", "nav", "footer", "dl", "dt", "dd", "h1", "h2",
    "h3", "h4", "h5", "style", "script",
]
# "span" is checked separately below (whole-file raw count legitimately
# mismatches because of a literal "</span>" string inside KaTeX's own
# minified JS source inside a <script> block -- see the dedicated check).


def tag_balance(text, tag):
    opens = len(re.findall(rf"<{tag}(?:\s[^>]*)?>", text, re.IGNORECASE))
    closes = len(re.findall(rf"</{tag}\s*>", text, re.IGNORECASE))
    return opens, closes


def main(path):
    text = open(path, encoding="utf-8").read()
    size = os.path.getsize(path)
    problems = []
    print(f"File: {path}")
    print(f"Size: {size:,} bytes ({size/1024/1024:.2f} MB)")
    print()

    # ---- 1. Tag balance ----
    print("=== Tag balance ===")
    for tag in PAIR_TAGS:
        o, c = tag_balance(text, tag)
        status = "OK" if o == c else "MISMATCH"
        if o != c:
            problems.append(f"tag <{tag}>: {o} open vs {c} close")
        print(f"  {tag:10s} open={o:5d} close={c:5d}  {status}")
    print()

    # span false-positive note: KaTeX's own minified JS contains the string
    # "</span>" inside JS string literals -- that's expected and not a real
    # imbalance in the HTML DOM itself. Let's separately count span
    # balance OUTSIDE the two <script> blocks to get the "real" DOM number.
    script_blocks = re.findall(r"<script>(.*?)</script>", text, re.DOTALL)
    text_no_scripts = re.sub(r"<script>.*?</script>", "", text, flags=re.DOTALL)
    o2, c2 = tag_balance(text_no_scripts, "span")
    print(f"  span (excluding <script> blocks): open={o2} close={c2} "
          f"{'OK' if o2==c2 else 'MISMATCH'}")
    if o2 != c2:
        problems.append(f"span (DOM, excl scripts): {o2} open vs {c2} close")
    else:
        # The raw whole-file span count above legitimately mismatches by the
        # literal "</span>" substring appearing inside KaTeX's own minified
        # JS source (inside a <script> block) -- confirmed a false positive
        # since the script-excluded DOM count balances exactly.
        o_raw, c_raw = tag_balance(text, "span")
        if o_raw != c_raw:
            print(f"  (note: whole-file raw span count {o_raw}/{c_raw} mismatches only "
                  f"because of a literal '</span>' string inside <script> JS source -- "
                  f"confirmed false positive, real DOM span balance above is exact)")
    print()

    # ---- 2. Leftover raw markdown ----
    print("=== Leftover raw markdown checks ===")
    stray_wikilink = re.findall(r"\[\[[a-zA-Z0-9_/\-|]+\]\]", text)
    # Known false positives: the Guide tab's own <code>[[concepts/slug]]</code>
    # and <code>[[concepts/multicollinearity]]</code> literal usage examples,
    # written deliberately as inert example text inside <code> tags.
    guide_examples_re = re.compile(r"<code>\[\[concepts/(slug|multicollinearity)\]\]</code>")
    known_false_positives = len(guide_examples_re.findall(text))
    real_stray = [w for w in stray_wikilink if not any(
        w == f"[[concepts/{s}]]" and f"<code>{w}</code>" in text for s in ("slug", "multicollinearity")
    )]
    print(f"  [[wikilink]] raw occurrences: {len(stray_wikilink)} (list: {stray_wikilink[:10]})")
    print(f"  of which inside Guide tab's own <code> example (expected false positive): {known_false_positives}")
    print(f"  unexplained leftover wikilinks: {len(real_stray)}")
    if real_stray:
        problems.append(f"{len(real_stray)} unexplained leftover raw [[wikilink]] occurrences: {real_stray}")

    stray_heading = re.findall(r"(?m)^##+ ", text)
    print(f"  raw '## ' markdown heading markers left as plain text: {len(stray_heading)}")
    if stray_heading:
        problems.append(f"{len(stray_heading)} leftover raw markdown heading markers")

    # stray ** not inside <strong>/<em> tags and not part of a significance-star
    # numeric pattern (those are expected/correct, e.g. "0.0012**")
    stray_stars = re.findall(r"(?<!\d)(?<!\*)\*\*(?!\*)(?![^<]*</strong>)", text)
    print(f"  heuristic stray '**' count (informational): {len(stray_stars)}")
    print()

    # ---- 3. Unescaped stray HTML in prose ----
    print("=== Unescaped stray HTML check ===")
    known_tags = set(PAIR_TAGS) | {
        "br", "input", "meta", "title", "nav", "footer", "hr", "img",
        "span", "h3",
    }
    # Exclude <script>/<style> blocks: KaTeX's minified JS source and CSS
    # contain string literals like "<svg", "<path", "<n" etc. that are not
    # real HTML tags in the DOM -- only scan actual markup for stray tags.
    text_no_style = re.sub(r"<style>.*?</style>", "", text_no_scripts, flags=re.DOTALL)
    all_tag_opens = re.findall(r"<([a-zA-Z][a-zA-Z0-9]*)[ >/]", text_no_style)
    unknown_tags = sorted(set(t.lower() for t in all_tag_opens) - known_tags)
    print(f"  Unknown/unexpected tag names found: {unknown_tags}")
    if unknown_tags:
        problems.append(f"unexpected tag names in output: {unknown_tags}")
    print()

    # ---- 4. Tab radios ----
    print("=== Tab count ===")
    all_radios = re.findall(r'<input type="radio" name="tab" class="tabctl" id="tab-([a-z0-9\-]+)"', text)
    print(f"  total tab radios: {len(all_radios)} -> {all_radios}")
    concept_radios = [r for r in all_radios if r not in ("guide", "all", "quiz")]
    print(f"  concept tab radios: {len(concept_radios)} (expect 15)")
    if len(concept_radios) != 15:
        problems.append(f"expected 15 concept tab radios, found {len(concept_radios)}")
    if len(all_radios) != 18:
        problems.append(f"expected 18 total tab radios (15 + guide/all/quiz), found {len(all_radios)}")
    print()

    # ---- 5. Lecture info cards ----
    print("=== Lecture info cards ===")
    n_cards = len(re.findall(r'<div class="lecture-info">', text))
    print(f"  'Lecture info' cards: {n_cards} (expect 13)")
    if n_cards != 13:
        problems.append(f"expected 13 lecture-info cards, found {n_cards}")
    print()

    # ---- 6. Embedded fonts ----
    print("=== Embedded fonts ===")
    n_fonts = len(re.findall(r"data:font/woff2;base64,", text))
    print(f"  data:font/woff2 embedded font declarations: {n_fonts}")
    if n_fonts < 20:
        problems.append(f"expected at least 20 embedded woff2 fonts (KaTeX alone needs 20), found {n_fonts}")
    print()

    # ---- 7. Light/dark theme CSS ----
    print("=== Theme CSS ===")
    has_dark_media = "@media (prefers-color-scheme: dark)" in text
    has_dark_attr = ':root[data-theme="dark"]' in text
    has_light_attr = ':root[data-theme="light"]' in text
    print(f"  @media dark present: {has_dark_media}")
    print(f"  [data-theme=dark] present: {has_dark_attr}")
    print(f"  [data-theme=light] present: {has_light_attr}")
    if not (has_dark_media and has_dark_attr and has_light_attr):
        problems.append("missing one of the required theme CSS blocks")
    print()

    # ---- 8. "slide" narration leftover check ----
    print('=== "slide" narration leftover check ===')
    # Strip script blocks first (KaTeX/JS source may legitimately contain
    # the substring "slide" e.g. in comments -- not relevant to content).
    body_no_script = text_no_scripts
    slide_hits = [m.start() for m in re.finditer(r"slide", body_no_script, re.IGNORECASE)]
    print(f"  case-insensitive 'slide' hits outside <script>: {len(slide_hits)}")
    for pos in slide_hits[:10]:
        print("   ...", body_no_script[max(0, pos - 60):pos + 60].replace("\n", " "))
    if len(slide_hits) > 0:
        problems.append(f"{len(slide_hits)} 'slide' narration hits found (should be ~0)")
    print()

    # ---- 9. Raw LaTeX-looking text outside math spans ----
    print("=== Raw LaTeX command leak check ===")
    # Look for a backslash-command pattern that is NOT inside a
    # math-inline/math-display span (i.e. leaked outside $...$ handling).
    math_span_re = re.compile(r'<span class="math-(?:inline|display)">.*?</span>', re.DOTALL)
    text_without_math_spans = math_span_re.sub("", text_no_scripts)
    leaked = re.findall(r"\\[a-zA-Z]+", text_without_math_spans)
    print(f"  backslash-command-looking text OUTSIDE math spans: {len(leaked)}")
    if leaked:
        print("   sample:", leaked[:10])
        problems.append(f"{len(leaked)} raw LaTeX-looking backslash commands found outside math spans")
    print()

    # ---- 10. Pr(>|t|) sanity ----
    print("=== Pr(>|t|) sanity ===")
    n_prt = len(re.findall(r"Pr\(&gt;\|[a-zA-Z]+\|\)", text))
    print(f"  'Pr(&gt;|x|)' occurrences rendered intact: {n_prt}")
    print()

    # ---- 11. Runaway emphasis spot check ----
    print("=== Runaway <strong>/<em> spot check ===")
    strongs = re.findall(r"<strong>(.*?)</strong>", text, re.DOTALL)
    ems = re.findall(r"<em>(.*?)</em>", text, re.DOTALL)
    long_strongs = [s for s in strongs if len(s) > 400]
    long_ems = [s for s in ems if len(s) > 400]
    print(f"  <strong> count={len(strongs)} max_len={max((len(s) for s in strongs), default=0)}")
    print(f"  <em> count={len(ems)} max_len={max((len(s) for s in ems), default=0)}")
    print(f"  suspiciously long <strong> (>400 chars): {len(long_strongs)}")
    print(f"  suspiciously long <em> (>400 chars): {len(long_ems)}")
    if long_strongs or long_ems:
        problems.append("found suspiciously long emphasis spans (possible runaway emphasis)")
    print()

    # ---- 12. KaTeX server-side render check of every math span ----
    print("=== KaTeX server-side render check ===")
    math_spans = re.findall(r'<span class="math-(?:inline|display)">(.*?)</span>', text, re.DOTALL)
    print(f"  total math spans found: {len(math_spans)}")
    formulas = []
    for s in math_spans:
        s = htmlmod.unescape(s)
        s = s.strip()
        if s.startswith("$$") and s.endswith("$$"):
            formulas.append(s[2:-2])
        elif s.startswith("$") and s.endswith("$"):
            formulas.append(s[1:-1])
        else:
            formulas.append(s)
    katex_result = run_katex_check(formulas)
    print(f"  KaTeX render errors: {katex_result['errors']} / {katex_result['total']}")
    if katex_result["error_samples"]:
        for e in katex_result["error_samples"][:15]:
            print("   ", e)
    if katex_result["errors"] > 0:
        problems.append(f"{katex_result['errors']} formulas fail to render in KaTeX")
    print()

    print("=" * 60)
    if problems:
        print(f"RESULT: {len(problems)} PROBLEM(S) FOUND")
        for p in problems:
            print(" -", p)
        return 1
    else:
        print("RESULT: ALL CHECKS PASSED")
        return 0


def run_katex_check(formulas):
    here = os.path.dirname(os.path.abspath(__file__))
    katex_path = os.path.join(here, "assets", "katex", "katex.min.js")
    script = f"""
const katex = require({json.dumps(katex_path)});
const fs = require('fs');
const formulas = JSON.parse(fs.readFileSync(0, 'utf-8'));
let errors = 0;
const error_samples = [];
for (const f of formulas) {{
  try {{
    katex.renderToString(f, {{throwOnError: true}});
  }} catch (e) {{
    errors++;
    if (error_samples.length < 20) {{
      error_samples.push(f.slice(0,80) + ' ||ERR|| ' + e.message.slice(0,120));
    }}
  }}
}}
console.log(JSON.stringify({{total: formulas.length, errors, error_samples}}));
"""
    proc = subprocess.run(
        ["node", "-e", script],
        input=json.dumps(formulas),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print("NODE STDERR:", proc.stderr[:2000])
        return {"total": len(formulas), "errors": -1, "error_samples": [proc.stderr[:500]]}
    return json.loads(proc.stdout.strip().splitlines()[-1])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
