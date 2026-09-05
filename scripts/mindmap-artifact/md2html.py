#!/usr/bin/env python3
r"""
md2html.py — Markdown -> HTML converter for the ECM wiki Mindmap Artifact.

Converts one concepts/*.md page's BODY (post-frontmatter markdown text,
already bilingual VI/EN with inline <br><span class="en">...</span> markup)
into a list of (heading_html, content_html) pairs, one per top-level `##`
section, plus an `intro_html` for any content preceding the first `##`.

Design notes / known edge cases handled (see wiki/CLAUDE.md §5.3 for the
full bug history this converter must not regress on):

 1. Table-cell splitting is math-aware: `|` inside `$...$` does not split
    a column.
 2. The literal (unescaped) R-output header `Pr(>|t|)` is protected as a
    special case before column-splitting (it has no `$` around it).
 3. Inline `code` spans are protected (extracted to placeholders) BEFORE
    the math regex runs, so a code span containing a literal `$`
    (e.g. `` `$ME.0` ``) can never be mistaken for an opening math
    delimiter.
 4. Bold/italic (`**`/`*`) is parsed with a stateful single-pass emphasis
    parser, not a naive regex pairing -- so R significance stars
    (`0.0012**`, `2.71e-09 ***`, a lone `*` for the 10% level) do not
    swallow unrelated text between two independent stars.
 5. All already-rendered HTML (math, code, wikilinks) is protected behind
    opaque placeholders BEFORE the emphasis parser runs (and restored
    only afterwards), so a literal `*` inside math (`t^*`, `y^*`) is never
    seen by the emphasis parser at all.
 6. Deliberate existing HTML in the source (`<br>`, `<span class="en">`,
    `</span>`) is protected behind placeholders BEFORE stray `<`/`&`/`>`
    escaping runs, then restored after -- so genuine markup survives
    while stray characters like `p < 2e-16` or `Anderson & Hsiao` get
    escaped correctly.
 7. A backslash-escaped pipe `\|` inside math (`$E(\varepsilon\|X)=0$`)
    or inside a table cell (`Pr(>\|t\|)`, `No \| 1-2/month`) is unescaped
    to a literal `|` -- for math, so KaTeX renders a single conditioning
    bar rather than its `\|` double-bar-norm command; for table cells, so
    the literal pipe displays correctly.
 8. Bare, unterminated `$1`-style currency amounts (a `$` immediately
    followed by digits and then whitespace, with no closing `$` -- e.g.
    "mỗi $1 tăng thêm") are detected and isolated behind a placeholder
    BEFORE the general math regex runs, so they can never pair with a
    later unrelated `$` and swallow real content into one bogus formula.
"""

import re

# ---------------------------------------------------------------------------
# Placeholder store
# ---------------------------------------------------------------------------

PH_START = ""
PH_END = ""
PH_RE = re.compile(re.escape(PH_START) + r"(\d+)" + re.escape(PH_END))

# Fixed sentinels for the wiki's own deliberate bilingual HTML markup.
FIX_BR = ""
FIX_SPAN_OPEN = ""
FIX_SPAN_CLOSE = ""


class Ctx:
    """Per-page placeholder store + wikilink resolver."""

    def __init__(self, resolve_wikilink):
        self.items = []
        self.resolve_wikilink = resolve_wikilink

    def add(self, html):
        idx = len(self.items)
        self.items.append(html)
        return f"{PH_START}{idx}{PH_END}"

    def restore(self, text):
        text = PH_RE.sub(lambda m: self.items[int(m.group(1))], text)
        text = (
            text.replace(FIX_BR, "<br>")
            .replace(FIX_SPAN_OPEN, '<span class="en">')
            .replace(FIX_SPAN_CLOSE, "</span>")
        )
        return text


def html_escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------------------
# Step 0: protect the wiki's own deliberate <br>/<span class="en"> markup
# ---------------------------------------------------------------------------

def protect_br_span(text):
    text = text.replace("<br>", FIX_BR)
    text = text.replace('<span class="en">', FIX_SPAN_OPEN)
    text = text.replace("</span>", FIX_SPAN_CLOSE)
    return text


# ---------------------------------------------------------------------------
# Step 1: protect inline code spans (edge case 3)
# ---------------------------------------------------------------------------

CODE_SPAN_RE = re.compile(r"`([^`\n]+)`")


def protect_code_spans(text, ctx):
    def repl(m):
        return ctx.add("<code>" + html_escape(m.group(1)) + "</code>")

    return CODE_SPAN_RE.sub(repl, text)


# ---------------------------------------------------------------------------
# Step 2: protect math spans (edge cases 7, 8)
# ---------------------------------------------------------------------------

DISPLAY_MATH_RE = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
INLINE_MATH_RE = re.compile(r"\$(.+?)\$", re.DOTALL)
# A `$` immediately followed by digits and then whitespace, with nothing
# currently protecting it -- this is a bare currency amount, not the start
# of a LaTeX span (real math in this corpus never has a space directly
# after an opening "$<digits>", e.g. "$1-P_i$" but never "$1 P_i$").
BARE_CURRENCY_RE = re.compile(r"\$(\d+)(?=\s)")


def _unescape_pipe(body):
    return body.replace("\\|", "|")


def protect_bare_currency(text, ctx):
    def repl(m):
        return ctx.add(html_escape("$" + m.group(1)))

    return BARE_CURRENCY_RE.sub(repl, text)


def protect_math(text, ctx):
    def repl_display(m):
        body = _unescape_pipe(m.group(1))
        return ctx.add('<span class="math-display">$$' + html_escape(body) + "$$</span>")

    text = DISPLAY_MATH_RE.sub(repl_display, text)
    text = protect_bare_currency(text, ctx)

    def repl_inline(m):
        body = _unescape_pipe(m.group(1))
        return ctx.add('<span class="math-inline">$' + html_escape(body) + "$</span>")

    text = INLINE_MATH_RE.sub(repl_inline, text)
    return text


# ---------------------------------------------------------------------------
# Step 3: protect wikilinks
# ---------------------------------------------------------------------------

WIKILINK_RE = re.compile(r"\[\[([a-zA-Z0-9_/\-]+)(?:\|([^\]]+))?\]\]")


def protect_wikilinks(text, ctx):
    def repl(m):
        target = m.group(1)
        label = m.group(2)
        html = ctx.resolve_wikilink(target, label)
        return ctx.add(html)

    return WIKILINK_RE.sub(repl, text)


# ---------------------------------------------------------------------------
# Step 4: escape stray HTML in whatever plain prose remains
# ---------------------------------------------------------------------------

def escape_stray_html(text):
    return html_escape(text)


# ---------------------------------------------------------------------------
# Step 5: stateful single-pass emphasis parser (edge cases 4, 5)
# ---------------------------------------------------------------------------


# Deliberately requires a decimal point (optionally + exponent): this is what
# distinguishes a genuine R p-value/coefficient tail ("0.0012**", "2.71e-09
# ***") from an ordinary bare integer ending a prose sentence ("one of the
# 3 **warning signs**", "bằng 0 **theo định nghĩa**") which must NOT be
# treated as a literal significance marker -- bare integers are extremely
# common in this corpus's prose and are never how the wiki writes p-values.
NUM_TAIL_RE = re.compile(r"(?:^|[^A-Za-z0-9_])-?\d+\.\d+(?:[eE][+-]?\d+)?\s*$")


def parse_emphasis(text):
    out = []
    i = 0
    n = len(text)
    bold_open = False
    italic_open = False
    while i < n:
        ch = text[i]
        if ch == "*":
            j = i
            while j < n and text[j] == "*":
                j += 1
            run_len = j - i
            preceding = "".join(out)
            is_num_tail = bool(NUM_TAIL_RE.search(preceding))
            # A run of exactly 3 stars is never a genuine bold+italic combo
            # anywhere in this corpus (verified empirically) -- it is always
            # an R triple-star significance marker (p<0.001), even when the
            # number it follows is hidden inside an already-protected math
            # placeholder (e.g. "$p=1.889\times10^{-8}$ ***"), where the
            # digit-tail check below can no longer see the digit directly.
            if not bold_open and not italic_open and (is_num_tail or run_len == 3):
                # Literal significance-star marker (0.05*, 2.71e-09 ***, ...)
                out.append("*" * run_len)
                i = j
                continue
            remaining = run_len
            while remaining > 0:
                if remaining >= 2:
                    if not bold_open:
                        out.append("<strong>")
                        bold_open = True
                    else:
                        out.append("</strong>")
                        bold_open = False
                    remaining -= 2
                else:
                    if not italic_open:
                        out.append("<em>")
                        italic_open = True
                    else:
                        out.append("</em>")
                        italic_open = False
                    remaining -= 1
            i = j
        else:
            out.append(ch)
            i += 1
    if italic_open:
        out.append("</em>")
    if bold_open:
        out.append("</strong>")
    return "".join(out)


# ---------------------------------------------------------------------------
# inline(): full pipeline for one run of text (paragraph, list item, table
# cell, heading, blockquote line). Returns text with placeholders still
# UNRESOLVED -- callers must run ctx.restore() once at the end, after all
# inline() calls for a page are done.
# ---------------------------------------------------------------------------

def inline(text, ctx):
    text = protect_br_span(text)
    text = protect_code_spans(text, ctx)
    text = protect_math(text, ctx)
    text = protect_wikilinks(text, ctx)
    text = escape_stray_html(text)
    text = parse_emphasis(text)
    return text


# ---------------------------------------------------------------------------
# Block-level parsing
# ---------------------------------------------------------------------------

LIST_ITEM_RE = re.compile(r"^(\s*)([-]|\d+\.)\s+(.*)$")
SUBHEAD_RE = re.compile(r"^(#{3,6})\s+(.*)$")
SEP_ROW_RE = re.compile(r"^\|?[\s:|\-]+\|?$")


def mask_pipes_for_split(line):
    """Mask `|` characters that must NOT act as column separators:
    those inside `$...$` math, inside `` `code` `` spans, backslash-escaped
    `\\|`, and the literal unescaped `Pr(>|t|)`-style R output header."""
    # Special-case literal unescaped Pr(>|x|) (edge case 2), before masking.
    line = re.sub(
        r"Pr\(>\|(\w+)\|\)", lambda m: "Pr(>\x01" + m.group(1) + "\x01)", line
    )
    out = []
    i = 0
    n = len(line)
    in_math = False
    in_code = False
    while i < n:
        ch = line[i]
        if ch == "\\" and i + 1 < n and line[i + 1] == "|":
            out.append("\x01")
            i += 2
            continue
        if ch == "`" and not in_math:
            in_code = not in_code
            out.append(ch)
            i += 1
            continue
        if ch == "$" and not in_code:
            in_math = not in_math
            out.append(ch)
            i += 1
            continue
        if ch == "|" and (in_math or in_code):
            out.append("\x01")
            i += 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def split_table_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    masked = mask_pipes_for_split(line)
    parts = masked.split("|")
    return [p.replace("\x01", "|").strip() for p in parts]


def render_table(lines, ctx):
    header_cells = split_table_row(lines[0])
    body_lines = lines[1:]
    if body_lines and SEP_ROW_RE.match(body_lines[0].strip()):
        body_lines = body_lines[1:]
    html = ['<div class="table-wrap"><table><thead><tr>']
    for c in header_cells:
        html.append(f"<th>{inline(c, ctx)}</th>")
    html.append("</tr></thead><tbody>")
    for l in body_lines:
        if not l.strip():
            continue
        cells = split_table_row(l)
        html.append("<tr>")
        for c in cells:
            html.append(f"<td>{inline(c, ctx)}</td>")
        html.append("</tr>")
    html.append("</tbody></table></div>")
    return "".join(html)


def render_list(lines, ctx):
    pos = [0]

    def parse_at(min_indent):
        tag = None
        cur_indent = None
        items_html = []
        while pos[0] < len(lines):
            line = lines[pos[0]]
            m = LIST_ITEM_RE.match(line)
            if not m:
                break
            indent = len(m.group(1))
            if indent < min_indent:
                break
            if tag is None:
                tag = "ol" if m.group(2)[0].isdigit() else "ul"
                cur_indent = indent
            if indent != cur_indent:
                break
            text0 = m.group(3)
            pos[0] += 1
            item_lines = [text0]
            nested_html = ""
            while pos[0] < len(lines):
                nxt = lines[pos[0]]
                mm = LIST_ITEM_RE.match(nxt)
                if mm:
                    nindent = len(mm.group(1))
                    if nindent > cur_indent:
                        nested_html += parse_at(nindent)
                        continue
                    else:
                        break
                else:
                    item_lines.append(nxt.strip())
                    pos[0] += 1
            item_html = inline(" ".join(item_lines), ctx)
            items_html.append(f"<li>{item_html}{nested_html}</li>")
        if tag is None:
            return ""
        return f"<{tag}>" + "".join(items_html) + f"</{tag}>"

    return parse_at(0)


def classify_and_render_chunk(chunk_text, ctx):
    lines = [l for l in chunk_text.split("\n") if l.strip() != ""]
    if not lines:
        return ""

    # Standalone placeholder (e.g. an extracted fenced code block) -- pass
    # through untouched, to be resolved by the final ctx.restore() pass.
    if len(lines) == 1 and PH_RE.fullmatch(lines[0].strip()):
        return lines[0].strip()

    m = SUBHEAD_RE.match(lines[0])
    if m and len(lines) == 1:
        level = len(m.group(1))
        text = inline(m.group(2), ctx)
        tag = "h4" if level == 3 else "h5"
        return f'<{tag} class="subhead">{text}</{tag}>'

    if all(l.lstrip().startswith(">") for l in lines):
        inner = " ".join(re.sub(r"^\s*>\s?", "", l) for l in lines)
        return f"<blockquote>{inline(inner, ctx)}</blockquote>"

    if len(lines) >= 2 and all(l.strip().startswith("|") for l in lines):
        return render_table(lines, ctx)

    if LIST_ITEM_RE.match(lines[0]):
        return render_list(lines, ctx)

    joined = " ".join(l.strip() for l in lines)
    return f"<p>{inline(joined, ctx)}</p>"


def render_blocks(text, ctx):
    text = text.strip("\n")
    if not text.strip():
        return ""
    chunks = re.split(r"\n[ \t]*\n", text)
    out = []
    for chunk in chunks:
        chunk = chunk.strip("\n")
        if not chunk.strip():
            continue
        out.append(classify_and_render_chunk(chunk, ctx))
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Fenced code blocks (extracted globally, before section split)
# ---------------------------------------------------------------------------

FENCE_RE = re.compile(r"```([a-zA-Z]*)\n(.*?)\n```", re.DOTALL)


def extract_fenced_code(text, ctx):
    def repl(m):
        code = m.group(2)
        return ctx.add(f'<pre class="code-block"><code>{html_escape(code)}</code></pre>')

    return FENCE_RE.sub(repl, text)


# ---------------------------------------------------------------------------
# Top-level page conversion
# ---------------------------------------------------------------------------

SECTION_SPLIT_RE = re.compile(r"(?m)^## (.*)$")


def convert_page(body_text, resolve_wikilink):
    """Convert a concepts/*.md page's body (post-frontmatter) into
    (intro_html, [(heading_html, content_html), ...])."""
    ctx = Ctx(resolve_wikilink)
    text = extract_fenced_code(body_text, ctx)
    parts = SECTION_SPLIT_RE.split(text)
    intro_raw = parts[0]
    sections = []
    i = 1
    while i < len(parts):
        heading_raw = parts[i]
        body_raw = parts[i + 1] if i + 1 < len(parts) else ""
        heading_html = ctx.restore(inline(heading_raw.strip(), ctx))
        content_html = ctx.restore(render_blocks(body_raw, ctx))
        sections.append((heading_html, content_html))
        i += 2
    intro_html = ctx.restore(render_blocks(intro_raw, ctx))
    return intro_html, sections


# ---------------------------------------------------------------------------
# Frontmatter parsing (hand-rolled, no external yaml dependency)
# ---------------------------------------------------------------------------

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def parse_frontmatter(raw_text):
    m = FRONTMATTER_RE.match(raw_text)
    if not m:
        return {}, raw_text
    fm_text = m.group(1)
    body = raw_text[m.end():]
    fm = {}
    title_m = re.search(r'^title:\s*"(.*)"\s*$', fm_text, re.MULTILINE)
    if title_m:
        fm["title"] = title_m.group(1)
    lecture_m = re.search(r"^lecture:\s*(\d+)\s*$", fm_text, re.MULTILINE)
    if lecture_m:
        fm["lecture"] = int(lecture_m.group(1))
    assignment_m = re.search(r"^assignment:\s*\[(.*)\]\s*$", fm_text, re.MULTILINE)
    if assignment_m:
        inner = assignment_m.group(1).strip()
        items = re.findall(r'"([^"]*)"', inner)
        fm["assignment"] = items
    else:
        fm["assignment"] = []
    return fm, body
