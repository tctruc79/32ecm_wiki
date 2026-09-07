#!/usr/bin/env python3
"""
build_shell.py — CSS, fonts, and KaTeX embedding for the ECM Mindmap Artifact.

Visual identity ("graph-paper", cool palette): IBM Plex Sans/Mono, a pale
cool-grey graph-paper background with a faint grid, terracotta accent for
causal / reject-H0 content, slate blue accent for associational / fail-to-
reject content. Deliberately distinct from the sibling DBC ("journal":
warm olive/serif) and DAS ("terminal": graphite/monospace) artifacts.
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def get_katex_css():
    return read(os.path.join(ASSETS, "katex_embedded.css"))


def get_katex_js():
    return read(os.path.join(ASSETS, "katex", "katex.min.js"))


def get_katex_autorender_js():
    return read(os.path.join(ASSETS, "katex", "contrib", "auto-render.min.js"))


def get_plex_css():
    return read(os.path.join(ASSETS, "plex_embedded.css"))


PAGE_CSS = r"""
/* ============================= Design tokens ============================= */
:root {
  --bg: #eef2f5;
  --bg-grid-line: rgba(52, 84, 112, 0.07);
  --bg-grid-size: 28px;
  --paper: #ffffff;
  --paper-soft: #f6f8fa;
  --ink: #1c2733;
  --ink-soft: #51616f;
  --ink-faint: #7c8b98;
  --border: #cdd8e0;
  --border-soft: #e1e8ed;
  --terracotta: #b95a2e;
  --terracotta-bg: #f6e6db;
  --terracotta-border: #e0b393;
  --slate: #3f5f8a;
  --slate-bg: #e2e9f2;
  --slate-border: #a9bdd6;
  --accent: #2f6f6a;
  --code-bg: #eef1e9;
  --shadow: 0 1px 2px rgba(28, 39, 51, 0.06), 0 4px 14px rgba(28, 39, 51, 0.05);
  --radius: 10px;
  --font-sans: "IBM Plex Sans", -apple-system, "Segoe UI", sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, "SFMono-Regular", Menlo, monospace;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #12181f;
    --bg-grid-line: rgba(140, 170, 200, 0.06);
    --paper: #1a222b;
    --paper-soft: #202a34;
    --ink: #e4ebf1;
    --ink-soft: #aebdc9;
    --ink-faint: #7e8f9d;
    --border: #33414d;
    --border-soft: #263039;
    --terracotta: #e2915e;
    --terracotta-bg: #3a2a20;
    --terracotta-border: #6b492f;
    --slate: #8fb0da;
    --slate-bg: #202d3f;
    --slate-border: #3a5170;
    --accent: #62b3ac;
    --code-bg: #202822;
    --shadow: 0 1px 2px rgba(0, 0, 0, 0.3), 0 4px 16px rgba(0, 0, 0, 0.25);
  }
}
:root[data-theme="dark"] {
  --bg: #12181f;
  --bg-grid-line: rgba(140, 170, 200, 0.06);
  --paper: #1a222b;
  --paper-soft: #202a34;
  --ink: #e4ebf1;
  --ink-soft: #aebdc9;
  --ink-faint: #7e8f9d;
  --border: #33414d;
  --border-soft: #263039;
  --terracotta: #e2915e;
  --terracotta-bg: #3a2a20;
  --terracotta-border: #6b492f;
  --slate: #8fb0da;
  --slate-bg: #202d3f;
  --slate-border: #3a5170;
  --accent: #62b3ac;
  --code-bg: #202822;
  --shadow: 0 1px 2px rgba(0, 0, 0, 0.3), 0 4px 16px rgba(0, 0, 0, 0.25);
}
:root[data-theme="light"] {
  --bg: #eef2f5;
  --bg-grid-line: rgba(52, 84, 112, 0.07);
  --paper: #ffffff;
  --paper-soft: #f6f8fa;
  --ink: #1c2733;
  --ink-soft: #51616f;
  --ink-faint: #7c8b98;
  --border: #cdd8e0;
  --border-soft: #e1e8ed;
  --terracotta: #b95a2e;
  --terracotta-bg: #f6e6db;
  --terracotta-border: #e0b393;
  --slate: #3f5f8a;
  --slate-bg: #e2e9f2;
  --slate-border: #a9bdd6;
  --accent: #2f6f6a;
  --code-bg: #eef1e9;
  --shadow: 0 1px 2px rgba(28, 39, 51, 0.06), 0 4px 14px rgba(28, 39, 51, 0.05);
}

/* ============================= Reset & base ============================= */
* { box-sizing: border-box; }
html, body {
  margin: 0; padding: 0;
  background:
    linear-gradient(var(--bg-grid-line) 1px, transparent 1px) 0 0 / var(--bg-grid-size) var(--bg-grid-size),
    linear-gradient(90deg, var(--bg-grid-line) 1px, transparent 1px) 0 0 / var(--bg-grid-size) var(--bg-grid-size),
    var(--bg);
  color: var(--ink);
  font-family: var(--font-sans);
  font-size: 16px;
  line-height: 1.6;
  /* Deliberately NOT setting overflow-x (or any overflow) here: doing so
     forces the UA to compute the other axis as "auto" too (CSS Overflow
     spec), turning html/body into an extra scroll container. A `position:
     sticky` descendant (the .tabbar below) then sticks relative to THAT
     container instead of the true viewport, which -- especially inside the
     Artifact iframe's own scroll handling -- makes it silently fail to
     stay pinned while the page visibly scrolls. Wide content is instead
     contained per-element (.table-wrap, pre.code-block have their own
     overflow-x: auto) so nothing here needs to be a scroll container at
     all, keeping the viewport the single, unambiguous sticky reference.
     Long unbroken tokens are guarded against separately via
     overflow-wrap below. */
}
body { min-height: 100vh; }
a { color: var(--slate); }
code, .math-inline, .math-display { font-family: var(--font-mono); }
p, li, td, th, blockquote, dd, summary { overflow-wrap: break-word; }

/* ============================= Shell layout ============================= */
.shell {
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 clamp(16px, 3vw, 48px) 64px;
}
.masthead {
  padding: 28px 4px 14px;
}
.masthead h1 {
  font-family: var(--font-sans);
  font-weight: 700;
  font-size: 1.7rem;
  letter-spacing: -0.01em;
  margin: 0 0 6px;
  text-wrap: balance;
}
.masthead .sub {
  color: var(--ink-soft);
  font-size: 0.95rem;
  max-width: 65ch;
}
.masthead .sub .en { color: var(--ink-faint); }
.legend {
  display: flex; gap: 14px; flex-wrap: wrap;
  margin-top: 12px; font-size: 0.82rem; color: var(--ink-soft);
}
.legend .swatch { display: inline-flex; align-items: center; gap: 6px; }
.legend .dot { width: 10px; height: 10px; border-radius: 3px; display: inline-block; }
.legend .dot.terracotta { background: var(--terracotta); }
.legend .dot.slate { background: var(--slate); }

/* ============================= Tab bar (CSS-radio, no JS) ============================= */
.tabbar {
  position: sticky; top: 0; z-index: 50;
  /* Fully opaque (not a translucent/backdrop-blur treatment): this bar
     must completely hide scrolled-under content, not just tint it. */
  background: var(--bg);
  border-bottom: 1px solid var(--border);
  padding: 8px 4px;
  display: flex; flex-wrap: wrap; gap: 6px;
  margin: 0 -4px 18px;
}
.tabbar label {
  font-family: var(--font-mono);
  font-size: 0.74rem;
  letter-spacing: 0.01em;
  padding: 5px 10px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: var(--paper);
  color: var(--ink-soft);
  cursor: pointer;
  user-select: none;
  white-space: nowrap;
  transition: background 0.12s ease, color 0.12s ease, border-color 0.12s ease;
}
.tabbar label:hover { border-color: var(--slate); color: var(--ink); }
.tabbar label.special { border-style: dashed; }

/* radio inputs: visually hidden but keyboard-focusable */
.tabctl { position: absolute; opacity: 0; pointer-events: none; }
.tabctl:focus-visible + label,
.tabctl:focus-visible ~ .tabbar label[for="__never__"] { outline: 2px solid var(--accent); }

.panel { display: none; }

/* Each radio, when checked, shows its matching panel and highlights its label.
   Generated pairs (input#tab-X:checked ~ .tabbar label[for="tab-X"], etc.)
   are emitted per-tab in build_artifact.py since the tab id list is dynamic. */

/* ============================= Root / lead card ============================= */
.root-card {
  background: var(--paper);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 18px 20px;
  margin-bottom: 18px;
}
.root-card h2 {
  margin: 0 0 4px;
  font-size: 1.28rem;
  font-weight: 700;
  text-wrap: balance;
}
.root-card .meta {
  font-family: var(--font-mono);
  font-size: 0.76rem;
  color: var(--ink-faint);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.page-intro blockquote {
  margin: 0 0 18px;
  padding: 12px 16px;
  background: var(--paper-soft);
  border-left: 3px solid var(--accent);
  border-radius: 0 8px 8px 0;
  color: var(--ink-soft);
  font-size: 0.95rem;
}
.page-intro p { color: var(--ink-soft); }

/* ============================= Lecture info card ============================= */
.lecture-info {
  background: var(--slate-bg);
  border: 1px solid var(--slate-border);
  border-radius: var(--radius);
  padding: 16px 20px;
  margin-bottom: 18px;
}
.lecture-info .tag {
  display: inline-block;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--slate);
  background: var(--paper);
  border: 1px solid var(--slate-border);
  border-radius: 999px;
  padding: 2px 9px;
  margin-bottom: 8px;
}
.lecture-info dl { margin: 8px 0 0; }
.lecture-info dt {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--ink-soft);
  margin-top: 10px;
}
.lecture-info dd { margin: 3px 0 0; }
.lecture-info ul.refs { margin: 4px 0 0; padding-left: 20px; }
.lecture-info ul.refs li { margin-bottom: 4px; font-size: 0.92rem; }

/* ============================= Details / summary nodes ============================= */
details.node {
  background: var(--paper);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  margin-bottom: 10px;
  overflow: hidden;
}
details.node > summary {
  list-style: none;
  cursor: pointer;
  padding: 12px 16px;
  font-weight: 600;
  font-size: 1.02rem;
  background: var(--paper-soft);
  border-bottom: 1px solid transparent;
  display: flex; align-items: baseline; gap: 8px;
}
details.node[open] > summary { border-bottom-color: var(--border-soft); }
details.node > summary::-webkit-details-marker { display: none; }
details.node > summary::before {
  content: "▸";
  color: var(--accent);
  font-size: 0.8em;
  transition: transform 0.15s ease;
  flex: none;
}
details.node[open] > summary::before { transform: rotate(90deg); }
details.node > summary .en { font-weight: 500; color: var(--ink-soft); font-size: 0.86em; }
.node-body { padding: 14px 18px 16px; }
.node-body > *:first-child { margin-top: 0; }
.node-body > *:last-child { margin-bottom: 0; }

.subhead { margin: 18px 0 6px; font-size: 1rem; font-weight: 700; color: var(--ink); }
.subhead .en { color: var(--ink-soft); font-weight: 500; }

/* ============================= Prose ============================= */
p { margin: 0 0 12px; }
strong { font-weight: 700; }
em { font-style: italic; }
.en { color: var(--ink-soft); }
blockquote {
  margin: 12px 0;
  padding: 10px 14px;
  background: var(--paper-soft);
  border-left: 3px solid var(--slate);
  border-radius: 0 8px 8px 0;
  color: var(--ink-soft);
}
ul, ol { margin: 0 0 12px; padding-left: 24px; }
li { margin-bottom: 6px; }
li > ul, li > ol { margin-top: 6px; }

code {
  background: var(--code-bg);
  border: 1px solid var(--border-soft);
  border-radius: 4px;
  padding: 0.1em 0.35em;
  font-size: 0.88em;
}
pre.code-block {
  background: var(--code-bg);
  border: 1px solid var(--border-soft);
  border-radius: 8px;
  padding: 12px 14px;
  overflow-x: auto;
  margin: 0 0 14px;
}
pre.code-block code {
  background: none; border: none; padding: 0; font-size: 0.86rem;
}

.table-wrap { overflow-x: auto; margin: 0 0 14px; }
table {
  border-collapse: collapse;
  width: 100%;
  font-size: 0.9rem;
}
th, td {
  border: 1px solid var(--border-soft);
  padding: 6px 10px;
  text-align: left;
  vertical-align: top;
  font-variant-numeric: tabular-nums;
}
th {
  background: var(--paper-soft);
  font-family: var(--font-mono);
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  color: var(--ink-soft);
}
tr:nth-child(even) td { background: color-mix(in srgb, var(--paper-soft) 55%, transparent); }

.math-display { display: block; overflow-x: auto; margin: 10px 0; text-align: center; }
.wikilink {
  color: var(--terracotta);
  border-bottom: 1px dashed var(--terracotta-border);
  cursor: pointer;
  font-weight: 500;
}
.wikilink:hover { background: var(--terracotta-bg); }
.ref-link { color: var(--ink-soft); font-style: italic; }

/* ============================= Guide / All / Quiz tabs ============================= */
.guide-card, .all-part, .quiz-card {
  background: var(--paper);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 16px 20px;
  margin-bottom: 14px;
}
.all-part h3 {
  font-size: 1.05rem;
  margin: 0 0 4px;
  color: var(--terracotta);
}
.all-part .part-en { color: var(--ink-faint); font-size: 0.85rem; font-weight: 500; }
.all-part ul { padding-left: 20px; }
.all-part li { margin-bottom: 8px; }
.all-part .topics { color: var(--ink-faint); font-size: 0.88rem; }

.quiz-card summary {
  cursor: pointer;
  font-weight: 600;
  padding: 4px 0;
}
.quiz-card .quiz-q { margin-bottom: 4px; }
.quiz-card .quiz-a {
  margin-top: 10px;
  padding: 10px 14px;
  background: var(--terracotta-bg);
  border: 1px solid var(--terracotta-border);
  border-radius: 8px;
}
.quiz-card .quiz-num {
  display: inline-block;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--ink-faint);
  margin-bottom: 4px;
}

footer.credits {
  text-align: center;
  color: var(--ink-faint);
  font-size: 0.78rem;
  margin-top: 32px;
}

@media (max-width: 560px) {
  .shell { padding: 0 10px 48px; }
  .masthead h1 { font-size: 1.35rem; }
}
"""


def get_page_css():
    return PAGE_CSS
