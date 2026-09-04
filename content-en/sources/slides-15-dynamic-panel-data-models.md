---
title: "Lecture 8: Dynamic Models for Panel Data"
type: source
raw_file: "raw/SLIDES/slides-15-iu.pdf"
pages: 64
topic: 14
lecture: 8
status: current
ingested: 2026-07-29
concepts: ["[[concepts/dynamic-panel-data-models]]"]
---

## Role

Topic 14 slide deck (end of the course) — extends panel data to dynamic models (a lagged $y$ on the right-hand side). The theoretically densest lecture in the whole course (64 pages, almost pure formulas + prose, very few pure-image pages) — extracted almost entirely via text.

## Example data

The same 300-firm setting as Topic 12–13, but with the observation window extended to **10 years** (vs. 5 years in Topic 12–13) — necessary because dynamic models and GMM need a long enough time series to have enough lags to use as instruments. `training` continues to play the endogenous-variable role, `subeligible`/`localbudget` are external instruments.

## Related readings (from the Course Outline)

Anderson & Hsiao (1981, 1982); Arellano & Bond (1991); Arellano & Bover (1995); Blundell & Bond (1998); Stata documentation for `xtabond`, `xtdpdsys`, `xtdpd`.

All content has been synthesized into `[[concepts/dynamic-panel-data-models]]`.
