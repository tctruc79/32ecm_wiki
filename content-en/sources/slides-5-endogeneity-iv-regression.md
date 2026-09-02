---
title: "Endogeneity and Instrumental Variable Regression (basic)"
type: source
raw_file: "raw/SLIDES/slides-5-iu.pdf"
pages: 63
topic: 5
status: superseded
ingested: 2026-07-29
concepts: ["[[concepts/endogeneity-iv-regression]]"]
---

## Role

Topic 5 slide deck (original version) — a violation of A3 (exogeneity) of [[concepts/linear-regression-model]]. A more refined/extended version exists, `slides-16-iu.pdf` (see `[[sources/slides-16-endogeneity-iv-regression-extended]]`) — marked `status: superseded` but kept because it is a real ingested source, per CLAUDE.md §3.

## Running example dataset

A survey of workers in Ho Chi Minh City: `wage` (dependent variable), `schooling` (endogenous variable), `fatheredu`/`motheredu` (instruments), plus control variables `age`, `tenure`, `gender`, `origin`, `science`/`social`.

The full technical content (the definition of endogeneity, 2SLS, LIML/Fuller, GMM, the diagnostic tests) has been synthesized into `[[concepts/endogeneity-iv-regression]]`.
