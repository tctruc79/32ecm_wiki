---
title: "Lecture 6: Panel Data Models — Fixed and Random Effects (basic)"
type: source
raw_file: "raw/SLIDES/slides-6-iu.pdf"
pages: 38
topic: 6
lecture: 6
status: current
ingested: 2026-07-29
concepts: ["[[concepts/fixed-random-effects-model]]"]
---

## Role

Topic 6 slide deck — opens the Panel Data Models section, extending [[concepts/linear-regression-model]] to data with both a unit and a time dimension. A more extended/detailed panel-data deck is `slides-13-iu.pdf` (Topic 12 — see `[[sources/slides-13-panel-data-variance-structures]]`).

## Example data

Vietnamese province-level data, 2007–2011 (58 provinces × 5 years): `rgdp` (real GDP), `labfo` (labor force), `rinvest` (investment), `pci` (provincial competitiveness index). Model: $\ln(rgdp)_{it}=\alpha+\beta X_{it}+u$ with $X$ comprising $\ln(labfo)$, $\ln(rinvest)$, `pci`.

## Note on missing content

The first slide lists a 6-item outline whose last item is **"Between group estimator"** — but the deck's actual content (38 pages) **stops at "Notes on Hausman test"**, with no between-group estimator section ever presented. This mirrors the "16 vs. 15 topics" case in the Course Outline — the outline promises more than the actual content delivers. Noted, not guessed at.

Many pages are R/Stata output images (SUMMARY STATISTICS, POOLED OLS IN R, FE/RE with robust/clustered SE) not extractable via text, but the "Hausman test in R" and "Random vs Fixed Effects" pages (pp. 33–38) were visually verified to make sure no formula content was missed.

All conceptual content has been synthesized into `[[concepts/fixed-random-effects-model]]`.
