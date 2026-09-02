---
title: "Course Outline — Applied Econometrics (2026)"
type: source
raw_file: "raw/SLIDES/VNP2026-CO.pdf"
pages: 12
topic: null
status: current
ingested: 2026-07-29
concepts: ["[[concepts/econometrics-overview]]"]
---

## Role of this document

The syllabus for **Applied Econometrics for Master Programme in Economics (2026)**, taught by **[[people/truong-dang-thuy|Trương Đăng Thụy]]** (UEH University — VNP). This is a "meta" document defining the whole course structure — used to build the topic map for the whole wiki (see the table in `index.md` and `CLAUDE.md` §3).

## Course description

This course teaches how economists use econometric models to analyze data, test economic hypotheses, and derive policy implications. Focus: model estimation + result interpretation, not just running commands.

## Prerequisites

- Familiarity with basic econometric models and functional forms
- Differential calculus
- Matrix algebra (matrix operations)
- A computer with R, RStudio, Rtools, Stata installed

## Main materials

1. Gujarati D. (2014) *Econometrics by Example*, Palgrave Macmillan — **main textbook**, cited as the "Reading" for each topic.
2. The dynamic-panel paper series: Anderson & Hsiao (1981, 1982), Arellano & Bond (1991), Arellano & Bover (1995), Blundell & Bond (1998), Roodman (2009), Windmeijer (2005) — the theoretical foundation for Topic 14 (Dynamic panel data models).

## Software

- **R/RStudio**: used for most of the course.
- **Stata** (v15+): used specifically only for the panel data models section.

## Course evaluation (50/25/25 split — see the note on the data mismatch in CLAUDE.md §7)

- Practice assignments: 25% (done on the econometrics.site online learning platform)
- In-class assignments: 50% — the CO states "10 assignments × 5%"; the Introduction slide states "5 assignments × 10%". Both add up to 50%, they only differ in how it's broken down — not a contradiction in the total.
- Individual project: 25% — must use **panel data**, ~10-page report, graded on: quality of the research question, data handling, model specification, estimation technique, and result interpretation.

## Topics (15 topics, numbered 0–14)

The CO states "16 topics" in Section VII's opening line but only defines 15 topics (0 through 14) — treated as a source-level inconsistency, **not** guessed into a 16th topic.

The full table (topic, content, slide file, reading) has been moved to `index.md` (the "Course map" section) since that is the shared navigation table for the whole wiki — avoiding duplication here.

Important for ingesting later slides: **slide filenames don't match the Topic numbers in the CO** (e.g., Topic 12 lives in `slides-13-iu.pdf`, not `slides-12`). Full detail in `CLAUDE.md` §3.

## Schedule

22 lecture/practice sessions (~2 hours + Q&A each), room H-204. 4 sessions are Tutorials (R/RStudio practice); the Panel data models section takes up the final 6 sessions (sessions 18–22, including 2 sessions for panel IV and 2 for Dynamic panel).
