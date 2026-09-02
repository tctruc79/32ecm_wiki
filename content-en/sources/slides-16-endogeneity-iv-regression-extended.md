---
title: "Endogeneity and Instrumental Variable Regression (extended)"
type: source
raw_file: "raw/SLIDES/slides-16-iu.pdf"
pages: 70
topic: 5
status: current
ingested: 2026-07-29
concepts: ["[[concepts/endogeneity-iv-regression]]"]
---

## Role

The refined/extended version of Topic 5, replacing `slides-5-iu.pdf` (see `[[sources/slides-5-endogeneity-iv-regression]]`) as the **canonical** source. Same example data (wage, schooling, fatheredu/motheredu) and the same technical tools (2SLS, LIML/Fuller, GMM, Sargan/Hansen, Wu-Hausman), but:

- More precise terminology: OLS under endogeneity is **inconsistent** (the slides-5 version says "biased" in places, which is less precise).
- Adds an entirely new section, **"Robust inference under weak instruments"**: the Anderson-Rubin (AR) test and Stock-Wright (SW) LM test — coefficient tests that stay valid even under weak instruments (as long as the model isn't underidentified and the instruments are valid).
- The recomputed Wu-Hausman statistic = 3.8 (vs. 3.63 in the older version) — the difference comes from using `ivreg2r::ivreg2()` with a robust VCV; the slide explicitly notes the test result depends on the VCV choice.

All merged content (including the new section) has been synthesized into `[[concepts/endogeneity-iv-regression]]`.
