#!/usr/bin/env python3
"""Extract the pure-English mirror of content/ into content-en/.

Source pages follow the bilingual convention: every VI sentence/bullet is
immediately followed by <br><span class="en">...</span>, and headings are
"VI - <span class="en">EN</span>" on one line. This mechanically extracts
the English half, dropping the VI half, keeping file structure identical
(so wikilinks resolve the same way in content/ and content-en/).
"""
import re
import shutil
import sys
from pathlib import Path

SRC = Path(sys.argv[1])
DEST = Path(sys.argv[2])

# Matches a single-line "... - <span class="en">EN</span>" (heading or frontmatter title),
# tolerating an optional backslash before the quotes (YAML-escaped in frontmatter).
SINGLE_LINE_EN_RE = re.compile(r'^(?P<prefix>.*?)\s-\s<span class=\\?"en\\?">(?P<en>.*?)</span>(?P<suffix>\\?"?)\s*$')

SPAN_OPEN_RE = re.compile(r'<br><span class=\\?"en\\?">')
# A handful of pages put a same-line span (usually a short parenthetical after a display
# equation) with no "<br>" prefix at all. Same handling as SPAN_OPEN_RE, just optional <br>.
ANY_SPAN_LINE_RE = re.compile(r'<span class=\\?"en\\?">')

# ECM-specific: unlike DBC/DAS, this wiki DOES translate markdown table cells inline,
# each cell as "<VI text><br><span class=\"en\">EN text</span>" (or, in some pages, using
# " - " / " / " as the separator instead of "<br>", matching the heading convention). A
# table row line can contain several such pairs (one per cell), so it needs cell-level
# substitution instead of the whole-line "discard VI, keep EN" logic used for paragraph/
# bullet/blockquote lines. The VI-text group is greedy so backtracking lands on the
# separator immediately before <span class="en">, not on a stray " - "/"/" inside the VI
# prose itself.
TABLE_ROW_RE = re.compile(r'^\s*\|')
TABLE_ROW_HAS_EN_RE = re.compile(r'class=\\?"en\\?"')
CELL_BILINGUAL_RE = re.compile(
    r'(?<=\|)[^|\n]*(?:<br>|\s[-/]\s)<span class=\\?"en\\?">(.*?)</span>', re.DOTALL
)

# Some pages translate an entire block (usually a table) as a standalone unit: the VI
# block, a blank line, then "<span class=\"en\">" alone on its own line, the EN block,
# and "</span>" alone on its own line. Detected and rewritten separately below, since it
# spans many lines and isn't a per-line pattern like the two cases above.
BLOCK_SPAN_OPEN_RE = re.compile(r'^<span class=\\?"en\\?">\s*$')
BLOCK_SPAN_CLOSE_RE = re.compile(r'^</span>\s*$')


def extract_table_row(line: str) -> str:
    return CELL_BILINGUAL_RE.sub(lambda m: m.group(1), line)


def extract_heading(line: str):
    m = re.match(r'^(#{1,6})\s+(.*)$', line)
    if not m:
        return None
    hashes, rest = m.group(1), m.group(2)
    m2 = SINGLE_LINE_EN_RE.match(rest)
    if not m2:
        return None
    return f"{hashes} {m2.group('en')}"


TITLE_EN_RE = re.compile(r'^title_en: "(.*)"$')


def extract_body(body: str) -> str:
    lines = body.split('\n')
    out = []
    pending = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        heading = extract_heading(line)
        if heading is not None:
            out.extend(pending)
            pending = []
            out.append(heading)
            i += 1
            continue
        if BLOCK_SPAN_OPEN_RE.match(line):
            out.extend(pending)
            pending = []
            # Discard the VI block this EN block mirrors: by construction (blank line,
            # then "<span class=\"en\">" alone), it's the contiguous non-blank block
            # immediately before the blank line that precedes this marker.
            while out and out[-1].strip() == '':
                out.pop()
            while out and out[-1].strip() != '':
                out.pop()
            i += 1
            block_lines = []
            while i < n and not BLOCK_SPAN_CLOSE_RE.match(lines[i]):
                block_lines.append(lines[i])
                i += 1
            i += 1  # skip the "</span>" line itself
            if out and out[-1].strip() != '':
                out.append('')
            out.extend(block_lines)
            continue
        if TABLE_ROW_RE.match(line) and TABLE_ROW_HAS_EN_RE.search(line):
            out.extend(pending)
            pending = []
            out.append(extract_table_row(line))
            i += 1
            continue
        if ANY_SPAN_LINE_RE.search(line):
            # the VI block's first line carries the real list marker (-, *, 1., ">", ...);
            # the span's own line only has continuation indent, so reuse the VI marker.
            marker_src = pending[0] if pending else line
            marker_m = re.match(r'^(\s*(?:>\s?|[-*]\s+|\d+\.\s+)?)', marker_src)
            marker = marker_m.group(1) if marker_m else ''
            pending = []  # discard the VI block this EN span pairs with
            span_text = line
            while '</span>' not in span_text:
                i += 1
                span_text += '\n' + lines[i]
            # Search anchored only at the end (not "^...match from start") so this also
            # handles the rarer case where the VI sentence and its "<br><span>" translation
            # sit on the SAME physical line (e.g. a blockquote intro) — any VI prose before
            # the span is simply discarded along with everything else outside the match.
            m = re.search(
                r'(?:<br>)?<span class=\\?"en\\?">(?P<en>.*)</span>\s*$',
                span_text, re.DOTALL,
            )
            en_content = m.group('en') if m else span_text
            out.append(f"{marker}{en_content}")
            i += 1
            continue
        if line.strip() == '':
            out.extend(pending)
            pending = []
            out.append(line)
        else:
            pending.append(line)
        i += 1
    out.extend(pending)
    return '\n'.join(out)


def process_file(src_path: Path, dest_path: Path):
    text = src_path.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_text(text, encoding='utf-8')
        return
    end = text.find('\n---\n', 4)
    if end == -1:
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_text(text, encoding='utf-8')
        return
    frontmatter_lines = text[4:end].split('\n')
    body = text[end + 5:]

    title_en = None
    for fl in frontmatter_lines:
        m = TITLE_EN_RE.match(fl)
        if m:
            title_en = m.group(1)
            break

    new_fm_lines = []
    for fl in frontmatter_lines:
        if fl.startswith('title: "') and title_en is not None:
            new_fm_lines.append(f'title: "{title_en}"')
        elif TITLE_EN_RE.match(fl):
            continue  # drop title_en from the EN mirror's own frontmatter
        else:
            new_fm_lines.append(fl)

    new_text = '---\n' + '\n'.join(new_fm_lines) + '\n---\n' + extract_body(body)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(new_text, encoding='utf-8')


def main():
    if DEST.exists():
        shutil.rmtree(DEST)
    count = 0
    for src_path in SRC.rglob('*.md'):
        rel = src_path.relative_to(SRC)
        process_file(src_path, DEST / rel)
        count += 1
    print(f"Extracted {count} files to {DEST}")


if __name__ == '__main__':
    main()
