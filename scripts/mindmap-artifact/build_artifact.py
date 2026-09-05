#!/usr/bin/env python3
"""
build_artifact.py — assembles the ECM wiki Mindmap Artifact (single
self-contained HTML file) from the current concepts/*.md + index.md.

Usage:
    python3 build_artifact.py <wiki_dir> <output_html_path>

Tab order: Introduction (econometrics-overview) -> R Basics (r-basics) ->
Lecture 1..13 (ordered by each page's `lecture:` frontmatter, read live --
never hardcoded), plus Guide / All / Quiz tabs.
"""

import html
import os
import re
import sys

import md2html
import lecture_data
import quiz_data
import build_shell

CONCEPT_FILES = [
    "econometrics-overview.md",
    "r-basics.md",
    "linear-regression-model.md",
    "functional-forms.md",
    "multicollinearity.md",
    "heteroskedasticity.md",
    "endogeneity-iv-regression.md",
    "binary-response-models.md",
    "ordinal-response-models.md",
    "multinomial-logit-model.md",
    "count-data-models.md",
    "censored-regression-tobit.md",
    "fixed-random-effects-model.md",
    "iv-regression-panel-data.md",
    "dynamic-panel-data-models.md",
]

# The course's 3 parts (for the "All" tab). Lecture numbers only -- titles
# are always read live from parsed frontmatter, never hardcoded here.
PARTS = [
    ("Phần I — Nền tảng OLS và vi phạm giả định", "Part I — OLS Foundations & Assumption Violations", [1, 2, 3, 4, 5]),
    ("Phần II — Mô hình dữ liệu bảng", "Part II — Panel Data Models", [6, 7, 8]),
    ("Phần III — Mô hình biến phụ thuộc giới hạn", "Part III — Limited Dependent Variable Models", [9, 10, 11, 12, 13]),
]


def slug_of(fname):
    return fname[:-3]


def load_pages(wiki_dir):
    """Returns list of dicts: {slug, fm, body, raw}."""
    pages = []
    concepts_dir = os.path.join(wiki_dir, "concepts")
    for fname in CONCEPT_FILES:
        path = os.path.join(concepts_dir, fname)
        raw = open(path, encoding="utf-8").read()
        fm, body = md2html.parse_frontmatter(raw)
        pages.append({"slug": slug_of(fname), "fm": fm, "body": body})
    return pages


def order_pages(pages):
    by_slug = {p["slug"]: p for p in pages}
    order = ["econometrics-overview", "r-basics"]
    lecture_pages = [p for p in pages if p["fm"].get("lecture") is not None]
    lecture_pages.sort(key=lambda p: p["fm"]["lecture"])
    order += [p["slug"] for p in lecture_pages]
    assert set(order) == set(by_slug.keys()), (set(order), set(by_slug.keys()))
    return [by_slug[s] for s in order]


SHORT_TITLE_RE = re.compile(r"^Lecture \d+:\s*")


def short_title(full_title):
    return SHORT_TITLE_RE.sub("", full_title).strip()


def make_resolver(slug_title_map):
    def resolve(target, label):
        if target.startswith("concepts/"):
            slug = target[len("concepts/"):]
            disp = label if label else slug_title_map.get(slug, slug.replace("-", " ").title())
            return f'<label for="tab-{slug}" class="wikilink" tabindex="0">{md2html.html_escape(disp)}</label>'
        else:
            slug = target.split("/")[-1]
            disp = label if label else slug.replace("-", " ").title()
            return f'<span class="ref-link">{md2html.html_escape(disp)}</span>'

    return resolve


def render_lecture_info_card(lec_num, lec_d):
    if lec_d is None:
        return ""
    parts = ['<div class="lecture-info">']
    parts.append(f'<span class="tag">Lecture info</span>')
    parts.append("<dl>")
    parts.append("<dt>Summary</dt>")
    parts.append(f"<dd>{html.escape(lec_d['summary'])}</dd>")
    parts.append("<dt>Key topics</dt>")
    parts.append(f"<dd>{html.escape(lec_d['key_topics'])}</dd>")
    parts.append("<dt>Practice assignment</dt>")
    if lec_d["assignment_list"]:
        parts.append('<dd><ul class="refs">')
        for a in lec_d["assignment_list"]:
            parts.append(f"<li>{html.escape(a)}</li>")
        parts.append("</ul></dd>")
    else:
        parts.append(f"<dd>{html.escape(lec_d['assignment'] or 'none numbered yet.')}</dd>")
    if lec_d["references"]:
        parts.append("<dt>References</dt>")
        parts.append('<dd><ul class="refs">')
        for r in lec_d["references"]:
            parts.append(f"<li>{html.escape(r)}</li>")
        parts.append("</ul></dd>")
    parts.append("</dl></div>")
    return "".join(parts)


def render_page_panel(page, slug_title_map, lectures):
    slug = page["slug"]
    fm = page["fm"]
    title = fm.get("title", slug)
    resolver = make_resolver(slug_title_map)
    intro_html, sections = md2html.convert_page(page["body"], resolver)

    parts = [f'<div class="panel" id="panel-{slug}">']
    parts.append('<div class="root-card">')
    parts.append(f"<h2>{html.escape(title)}</h2>")
    lec_num = fm.get("lecture")
    if lec_num is not None:
        parts.append(f'<div class="meta">Lecture {lec_num}</div>')
    else:
        parts.append('<div class="meta">Unnumbered — read before Lecture 1</div>')
    parts.append("</div>")

    if intro_html.strip():
        parts.append(f'<div class="page-intro">{intro_html}</div>')

    if lec_num is not None:
        parts.append(render_lecture_info_card(lec_num, lectures.get(lec_num)))

    for heading_html, content_html in sections:
        parts.append(
            f'<details class="node" open><summary>{heading_html}</summary>'
            f'<div class="node-body">{content_html}</div></details>'
        )

    parts.append("</div>")
    return "".join(parts)


GUIDE_HTML = """
<div class="panel" id="panel-guide">
<div class="root-card">
<h2>Hướng dẫn sử dụng - <span class="en">How to use this page</span></h2>
</div>
<div class="guide-card">
<p>Đây là bản tóm lược đầy đủ (full-detail) toàn bộ 15 trang <code>concepts/*.md</code> của wiki Kinh tế lượng, trình bày dưới dạng các tab và mục có thể mở/đóng, dùng để ôn thi hoặc ôn luận văn.
<br><span class="en">This is a full-detail rendering of all 15 <code>concepts/*.md</code> pages of the Econometrics wiki, laid out as tabs and collapsible sections, for exam or thesis review.</span></p>
<p><strong>Tab</strong>: dải nút phía trên (dính khi cuộn trang) chuyển giữa các trang — thứ tự Giới thiệu → R Basics → Lecture 1–13 → Guide/All/Quiz.
<br><span class="en"><strong>Tabs</strong>: the sticky button bar at the top switches between pages — ordered Introduction → R Basics → Lecture 1–13 → Guide/All/Quiz.</span></p>
<p><strong>Mục mở/đóng</strong>: mỗi phần (<code>##</code> heading gốc trong file markdown) là một khối có thể bấm để thu gọn/mở rộng — mặc định tất cả đều <strong>mở sẵn</strong> để đọc liên tục từ đầu đến cuối.
<br><span class="en"><strong>Collapsible sections</strong>: each part (a top-level <code>##</code> heading in the source markdown) is a block that can be collapsed/expanded by clicking — by default everything is <strong>already open</strong> for continuous start-to-end reading.</span></p>
<p><strong>Liên kết chéo</strong>: chữ có gạch chân màu terracotta (ví dụ <code>[[concepts/multicollinearity]]</code> trong văn bản gốc) là một liên kết nhảy sang tab tương ứng — bấm vào sẽ tự động chuyển tab, không cần cuộn tìm.
<br><span class="en"><strong>Cross-links</strong>: text underlined in terracotta (from a <code>[[concepts/slug]]</code> wikilink in the source) jumps to the corresponding tab when clicked — no scrolling needed.</span></p>
<p><strong>Công thức toán</strong>: mọi công thức LaTeX (<code>$...$</code> và <code>$$...$$</code>) được render trực tiếp bằng KaTeX (tự chứa, không cần mạng).
<br><span class="en"><strong>Math</strong>: every LaTeX formula (<code>$...$</code> and <code>$$...$$</code>) is rendered directly with KaTeX (self-hosted, no network required).</span></p>
<p><strong>Thẻ "Lecture info"</strong>: mỗi tab Lecture 1–13 có một thẻ tóm tắt màu xanh lam nhạt ở đầu (Summary/Key topics/Assignment/References), lấy trực tiếp từ <code>index.md</code>, trước khi vào nội dung chi tiết.
<br><span class="en"><strong>"Lecture info" card</strong>: each Lecture 1–13 tab has a pale-blue summary card at the top (Summary/Key topics/Assignment/References), sourced directly from <code>index.md</code>, before the detailed content.</span></p>
<p><strong>Màu sắc</strong>: terracotta đánh dấu nội dung nhân quả/bác bỏ $H_0$ (causal, reject-$H_0$); xanh slate đánh dấu nội dung liên kết/không bác bỏ $H_0$ (associational, fail-to-reject) — phản ánh phân biệt causal-vs-associational xuyên suốt khóa học.
<br><span class="en"><strong>Color</strong>: terracotta marks causal / reject-$H_0$ content; slate blue marks associational / fail-to-reject content — mirroring the causal-vs-associational distinction that runs through the whole course.</span></p>
<p>Tab <strong>All</strong> gom 13 Lecture theo 3 phần của khóa học; tab <strong>🧪 Quiz</strong> có 13 câu hỏi bấm-để-xem-đáp-án, mỗi câu lấy từ một bẫy thi thật trong wiki.
<br><span class="en">The <strong>All</strong> tab clusters the 13 lectures by the course's 3 parts; the <strong>🧪 Quiz</strong> tab has 13 click-to-reveal questions, each drawn from a real exam trap in the wiki.</span></p>
</div>
</div>
"""


def render_all_tab(pages_by_slug, slug_title_map, lectures):
    parts = ['<div class="panel" id="panel-all">']
    parts.append('<div class="root-card"><h2>Toàn bộ khóa học theo 3 phần - <span class="en">The whole course, by its 3 parts</span></h2></div>')

    resolver = make_resolver(slug_title_map)

    intro_part = '<div class="all-part"><h3>Trước Lecture 1 - <span class="en part-en">Before Lecture 1</span></h3><ul>'
    for slug in ("econometrics-overview", "r-basics"):
        title = slug_title_map.get(slug, slug)
        intro_part += f'<li>{resolver("concepts/" + slug, None)} — {html.escape(title)}</li>'
    intro_part += "</ul></div>"
    parts.append(intro_part)

    lecture_to_slug = {}
    for slug, p in pages_by_slug.items():
        lec = p["fm"].get("lecture")
        if lec is not None:
            lecture_to_slug[lec] = slug

    for title_vi, title_en, lecs in PARTS:
        block = [f'<div class="all-part"><h3>{html.escape(title_vi)} - <span class="en part-en">{html.escape(title_en)}</span></h3><ul>']
        for lec in lecs:
            slug = lecture_to_slug[lec]
            d = lectures.get(lec, {})
            key_topics = d.get("key_topics", "")
            link_html = resolver("concepts/" + slug, None)
            block.append(f'<li>{link_html} <span class="topics">({html.escape(key_topics)})</span></li>')
        block.append("</ul></div>")
        parts.append("".join(block))

    parts.append("</div>")
    return "".join(parts)


def wrap_math(text):
    """Wrap bare $...$/$$...$$ in quiz_data.py's hand-authored HTML strings
    with the same math-inline/math-display span classes md2html.py uses,
    so KaTeX auto-render finds them consistently and validate_final.py's
    "no raw LaTeX outside math spans" check covers them too."""
    text = re.sub(
        r"\$\$(.+?)\$\$",
        lambda m: '<span class="math-display">$$' + m.group(1) + "$$</span>",
        text,
        flags=re.DOTALL,
    )
    text = re.sub(
        r"\$(.+?)\$",
        lambda m: '<span class="math-inline">$' + m.group(1) + "$</span>",
        text,
        flags=re.DOTALL,
    )
    return text


def render_quiz_tab(slug_title_map):
    resolver = make_resolver(slug_title_map)

    def prep(s):
        s = wrap_math(s)
        s = md2html.WIKILINK_RE.sub(lambda m: resolver(m.group(1), m.group(2)), s)
        return s

    parts = ['<div class="panel" id="panel-quiz">']
    parts.append('<div class="root-card"><h2>🧪 Quiz — 13 câu hỏi bẫy thi - <span class="en">🧪 Quiz — 13 exam-trap questions</span></h2></div>')
    for q in quiz_data.QUIZ:
        q_vi, q_en, a_vi, a_en = (prep(q[k]) for k in ("q_vi", "q_en", "a_vi", "a_en"))
        parts.append('<details class="quiz-card">')
        parts.append(f'<summary><span class="quiz-num">Lecture {q["lecture"]}</span><div class="quiz-q">{q_vi}<br><span class="en">{q_en}</span></div></summary>')
        parts.append(f'<div class="quiz-a">{a_vi}<br><span class="en">{a_en}</span></div>')
        parts.append("</details>")
    parts.append("</div>")
    return "".join(parts)


def build(wiki_dir, out_path):
    pages = load_pages(wiki_dir)
    ordered = order_pages(pages)
    pages_by_slug = {p["slug"]: p for p in pages}

    slug_title_map = {p["slug"]: short_title(p["fm"].get("title", p["slug"])) for p in pages}

    index_text = open(os.path.join(wiki_dir, "index.md"), encoding="utf-8").read()
    lectures = lecture_data.parse_lectures(index_text)

    tab_ids = [p["slug"] for p in ordered] + ["guide", "all", "quiz"]

    tabbar_labels = []
    for p in ordered:
        slug = p["slug"]
        title = p["fm"].get("title", slug)
        tabbar_labels.append((slug, title))

    panels_html = []
    for p in ordered:
        panels_html.append(render_page_panel(p, slug_title_map, lectures))
    panels_html.append(GUIDE_HTML)
    panels_html.append(render_all_tab(pages_by_slug, slug_title_map, lectures))
    panels_html.append(render_quiz_tab(slug_title_map))

    # ---- radios ----
    radios = []
    for i, tid in enumerate(tab_ids):
        checked = " checked" if i == 0 else ""
        radios.append(f'<input type="radio" name="tab" class="tabctl" id="tab-{tid}"{checked}>')

    # ---- tabbar labels ----
    tabbar = ['<nav class="tabbar">']
    for slug, title in tabbar_labels:
        tabbar.append(f'<label for="tab-{slug}">{html.escape(title)}</label>')
    tabbar.append('<label for="tab-guide" class="special">Guide</label>')
    tabbar.append('<label for="tab-all" class="special">All</label>')
    tabbar.append('<label for="tab-quiz" class="special">🧪 Quiz</label>')
    tabbar.append("</nav>")

    # ---- per-tab show/highlight CSS ----
    tab_css = []
    for tid in tab_ids:
        tab_css.append(
            f'#tab-{tid}:checked ~ .shell #panel-{tid} {{ display: block; }}\n'
            f'#tab-{tid}:checked ~ .shell .tabbar label[for="tab-{tid}"] '
            f'{{ background: var(--ink); color: var(--paper); border-color: var(--ink); }}'
        )
    tab_css_text = "\n".join(tab_css)

    plex_css = build_shell.get_plex_css()
    katex_css = build_shell.get_katex_css()
    page_css = build_shell.get_page_css()
    katex_js = build_shell.get_katex_js()
    autorender_js = build_shell.get_katex_autorender_js()

    doc = f"""<title>Econometrics Wiki — Mindmap</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
{plex_css}
{katex_css}
{page_css}
{tab_css_text}
</style>
{''.join(radios)}
<div class="shell">
  <div class="masthead">
    <h1>Econometrics — Mindmap Artifact</h1>
    <div class="sub">Bilingual (VI/EN) full-detail review companion cho wiki Kinh tế lượng — 15 trang concept, đầy đủ công thức, bảng, và bẫy thi.
    <br><span class="en">Bilingual (VI/EN) full-detail review companion for the Econometrics wiki — 15 concept pages, full formulas, tables, and exam traps.</span></div>
    <div class="legend">
      <span class="swatch"><span class="dot terracotta"></span>Causal / reject H₀</span>
      <span class="swatch"><span class="dot slate"></span>Associational / fail to reject H₀</span>
    </div>
  </div>
  {''.join(tabbar)}
  {''.join(panels_html)}
  <footer class="credits">Econometrics Wiki (GS Trương Đăng Thụy, UEH-VNP) — Mindmap Artifact, rebuilt {BUILD_DATE}.</footer>
</div>
<script>{katex_js}</script>
<script>{autorender_js}</script>
<script>
document.addEventListener("DOMContentLoaded", function() {{
  renderMathInElement(document.body, {{
    delimiters: [
      {{left: "$$", right: "$$", display: true}},
      {{left: "$", right: "$", display: false}}
    ],
    throwOnError: false
  }});
}});
</script>
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(doc)
    return out_path


BUILD_DATE = "2026-09-05"

if __name__ == "__main__":
    wiki_dir = sys.argv[1]
    out_path = sys.argv[2]
    p = build(wiki_dir, out_path)
    print("Wrote", p, os.path.getsize(p), "bytes")
