#!/usr/bin/env python3
"""
lecture_data.py — parses wiki/index.md's "## Lectures (course order)" section
into structured per-lecture data (Summary / Key topics / Assignment(s) /
References), used to build each lecture tab's lead "Lecture info" card.

Nothing here is hardcoded per-lecture text -- it is all mechanically
extracted from index.md at build time, so if index.md changes, the next
rebuild picks it up automatically.
"""

import re

LECTURE_BLOCK_RE = re.compile(r"(?m)^### Lecture (\d+):\s*(.*)$")


def parse_lectures(index_md_text):
    """Returns {lecture_num: {"title": str, "summary": str,
    "key_topics": str, "assignment": str_or_None,
    "assignment_list": [str, ...], "references": [str, ...]}}"""

    # Restrict to the "## Lectures (course order)" section so we don't
    # accidentally pick up the later "## Course map" table.
    section_m = re.search(
        r"(?m)^## Lectures \(course order\)\s*$(.*?)(?=^## )", index_md_text, re.DOTALL
    )
    section_text = section_m.group(1) if section_m else index_md_text

    matches = list(LECTURE_BLOCK_RE.finditer(section_text))
    result = {}
    for i, m in enumerate(matches):
        num = int(m.group(1))
        title = m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(section_text)
        block = section_text[start:end]

        summary_m = re.search(r"\*\*Summary:\*\*\s*(.*?)(?:\n\s*\n|\Z)", block, re.DOTALL)
        summary = re.sub(r"\s+", " ", summary_m.group(1)).strip() if summary_m else ""

        keytopics_m = re.search(r"\*\*Key topics:\*\*\s*(.*?)(?:\n\s*\n|\Z)", block, re.DOTALL)
        key_topics = re.sub(r"\s+", " ", keytopics_m.group(1)).strip() if keytopics_m else ""

        assignment = None
        assignment_list = []
        single_m = re.search(r"\*\*Practice assignment:\*\*\s*(.*?)(?:\n\s*\n|\Z)", block, re.DOTALL)
        if single_m:
            assignment = re.sub(r"\s+", " ", single_m.group(1)).strip()
        else:
            list_m = re.search(
                r"\*\*Practice assignments:\*\*\s*\n((?:\s*-\s*.*\n?)+)", block
            )
            if list_m:
                assignment_list = [
                    l.strip("- ").strip()
                    for l in list_m.group(1).splitlines()
                    if l.strip().startswith("-")
                ]

        refs_m = re.search(r"\*\*References:\*\*\s*\n((?:\s*-\s*.*\n?)+)", block)
        references = []
        if refs_m:
            references = [
                l.strip("- ").strip()
                for l in refs_m.group(1).splitlines()
                if l.strip().startswith("-")
            ]

        result[num] = {
            "title": title,
            "summary": summary,
            "key_topics": key_topics,
            "assignment": assignment,
            "assignment_list": assignment_list,
            "references": references,
        }
    return result


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "index.md"
    text = open(path, encoding="utf-8").read()
    data = parse_lectures(text)
    print(f"Parsed {len(data)} lectures")
    for n in sorted(data):
        d = data[n]
        print(f"--- Lecture {n}: {d['title']} ---")
        print("summary:", d["summary"][:80], "...")
        print("key_topics:", d["key_topics"][:80], "...")
        print("assignment:", d["assignment"])
        print("assignment_list:", d["assignment_list"])
        print("references:", len(d["references"]))
