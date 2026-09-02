---
title: "The Linear Regression Model"
type: source
raw_file: "raw/SLIDES/slides-1-iu.pdf"
pages: 51
topic: 1
status: current
ingested: 2026-07-29
concepts: ["[[concepts/linear-regression-model]]"]
---

## Role

Topic 1 slide deck — the estimation foundation of the whole course: PRE/SRE, OLS, the 5 assumptions, coefficient interpretation, t-test, F-test, R². All formulas were extracted from the PDF's text layer (no need for visual page reads) — the sparse-looking pages in the original are section-divider slides, not hidden formulas.

## Running example dataset

The **"Forest coverage and storm damages"** dataset: dependent variable `pdamages` (asset losses, thousand US$); independent variables `aforest` [causal] (forest area, ha), `dplan` [causal] (has a resilience plan or not), and the non-causal variables `cgdp`, `pdens`, `curban`, `cterrain` (lowland/highland/coastal). The professor explicitly notes the dataset is **simplified for learning purposes** and may omit important regressors — not for real-world inference.

All content has been synthesized into `[[concepts/linear-regression-model]]`.
