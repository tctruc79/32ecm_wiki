---
title: "Panel Data Models with Covariance Structure"
type: source
raw_file: "raw/SLIDES/slides-13-iu.pdf"
pages: 61
topic: 12
status: current
ingested: 2026-07-29
concepts: ["[[concepts/fixed-random-effects-model]]"]
---

## Role

Topic 12 slide deck (numbered file 13 — see `CLAUDE.md` §3 for the numbering mismatch). An extended version of Topic 6 (`slides-6-iu.pdf`); its closing title slide reads "PANEL DATA MODELS WITH COVARIANCE STRUCTURE" — confirming this is indeed the Course Outline's "Panel data models with variance structures." Most of the theoretical content (assumptions A3a/A3b, A4a/b/c, GLS/FGLS, the SE types) extracted fully via text; the R-output example pages (POLS/FE/RE with each SE type) are images, only the sidebar-note prose extracted — enough to grasp the meaning of each SE type without needing the specific numbers.

## Example data

Data on 300 firms, 5 years: `output` (output value), `capital`, `training` (training hours/worker), `labor`, `export`, `credit`, `tech` (3 levels: lowtech/mediumtech/hightech). The same dataset is reused in Topic 13 (`slides-14-iu.pdf`) and Topic 14 (`slides-15-iu.pdf`) — a deliberate design choice: the same empirical setting, with complexity increasing across three consecutive panel-data lectures (basic FE/RE → panel IV → dynamic panel).

All content has been merged into `[[concepts/fixed-random-effects-model]]` (together with Topic 6).
