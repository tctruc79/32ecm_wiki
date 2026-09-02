---
title: "Binary Response Models (vaccine example)"
type: source
raw_file: "raw/SLIDES/slides-7-iu.pdf"
pages: 48
topic: 7
status: current
ingested: 2026-07-29
concepts: ["[[concepts/binary-response-models]]"]
---

## Role

Topic 7 slide deck — opens Part 2 (Models for Limited Dependent Variables), where the dependent variable is binary. A parallel deck, `slides-310-iu.pdf`, uses different example data (see `[[sources/slides-310-binary-response-models-logit-probit]]`) but **the same theoretical content** — not an old/new pair like Topic 5, but two illustrative datasets for the same lecture.

## Example data

A survey of the (hypothetical) COVID-19 vaccination decision of 377 people in Ho Chi Minh City, 2020 (source: EEPSEA). Dependent variable `dself` (1 = decided to vaccinate); independent variables `efficacy80`, `duration3`, `priceUS`, `pbenefit`, `hhincomeUS`, `hhsize`, `age`, `edu`, `male`, `risk`.

The R-results pages (LR test, Wald test, marginal effects) were visually verified to pull real illustrative numbers — those numbers were carried into `[[concepts/binary-response-models]]`.
