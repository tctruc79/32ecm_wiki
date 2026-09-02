---
title: "Cragg & Donald"
type: person
role: "Econometricians — thống kê Cragg-Donald F kiểm định weak instruments dưới homoskedasticity"
tags: [cragg-donald, weak-instruments, iv-regression]
---

John G. Cragg & Stephen G. Donald (1993, *"Testing Identifiability and Specification in Instrumental Variable Models"*, Econometric Theory) developed the **Cragg-Donald (CD) F-statistic** — a statistic generalizing the first-stage F to the case of multiple endogenous regressors at once (using the smallest eigenvalue of a matrix related to the first-stage equations), used to test **weak identification**: rejecting underidentification doesn't mean the instruments are strong enough — the CD F-statistic must be compared to a critical value.

With exactly 1 endogenous regressor, CD-F coincides with the usual first-stage F. Underlying assumption: **homoskedasticity**. The critical values for evaluating CD-F are provided by [[people/stock-yogo|Stock & Yogo]]; a common rule of thumb in practice: CD F-statistic > 10.

When the homoskedasticity assumption fails, the robust alternative is the **Kleibergen-Paap rk Wald F (KP-F)** — but KP-F **cannot** be directly compared to the Stock-Yogo critical values (which were designed specifically for CD-F, under homoskedasticity).

## Xuất hiện trong

- [[concepts/endogeneity-iv-regression]]
- [[concepts/iv-regression-panel-data]]
