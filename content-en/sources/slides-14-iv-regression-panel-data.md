---
title: "Lecture 7: Instrumental Variable Regression for Panel Data"
type: source
raw_file: "raw/SLIDES/slides-14-iu.pdf"
pages: 56
topic: 13
lecture: 7
status: current
ingested: 2026-07-29
concepts: ["[[concepts/iv-regression-panel-data]]"]
---

## Role

Topic 13 slide deck (file numbered 14). Applies the IV/2SLS/LIML/Fuller/GMM framework from Topic 5 ([[concepts/endogeneity-iv-regression]]) to a panel-data setting — handling an endogenous regressor **together with** individual fixed effects. The theory extracted fully via text; the R-output illustration pages (each SE type for FD-IV, FE-IV, LIML, Fuller) all have prose annotations captured via text.

## Example data

The same 300-firm × 5-year dataset as Topic 12: `output`, `capital`, `labor`, with `training` (training hours/worker) treated as **endogenous**, using instruments `subeligible` (eligible for a training subsidy) and `localbudget` (local government training budget).

## Note on content not taught

The CO lists "**2SLS RE estimator**" and "**G2GLS estimator**" as items under Topic 13 — but the slide **states explicitly**: "RE (Random Effects) IV regression (Generalized 2SLS, **not covered**)." This is a gap explicitly confirmed by the slide itself (unlike earlier gaps that had to be inferred from absence) — noted verbatim, no further inference.

All content has been synthesized into `[[concepts/iv-regression-panel-data]]`.
