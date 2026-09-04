---
title: "Lecture 13: Censored Regression: The Tobit Model"
type: source
raw_file: "raw/SLIDES/slides-11-iu.pdf"
pages: 35
topic: 11
lecture: 13
status: current
ingested: 2026-07-29
concepts: ["[[concepts/censored-regression-tobit]]"]
---

## Role

Topic 11 slide deck — the dependent variable is **censored** (the true value exists but gets "clamped" at a threshold when recorded). All formulas (the model, probability, marginal effects, log-likelihood) extracted fully via text.

## Example data

Credit card balance (`balance`, US$ — censored at 0, since non-cardholders are recorded with balance=0), explained by the interest rate (`interest`), `age`, `male`, `edu`.

## Note on content missing relative to the Course Outline

The CO lists "the Heckman selection model (if time allowed)" as an item under Topic 11 — but it **does not appear** anywhere in this deck's 35 pages. This may simply reflect the time constraint the CO itself hedged for ("if time allowed"). Noted, no attempt to reconstruct Heckman-model content.

All content has been synthesized into `[[concepts/censored-regression-tobit]]`.
