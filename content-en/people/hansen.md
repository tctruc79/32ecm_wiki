---
title: "Hansen (L. P.)"
type: person
role: "Econometrician — GMM framework and the generalized overidentifying-restrictions test (Hansen's J test)"
tags: [hansen-j-test, gmm, overidentification, iv-regression]
---

Lars Peter Hansen (1982, *"Large Sample Properties of Generalized Method of Moments Estimators"*, Econometrica) built the **Generalized Method of Moments (GMM)** framework — a family of estimators that generalizes both OLS and 2SLS/IV as special cases, based on choosing an optimal weight for the moment conditions. This contribution earned the 2013 Nobel Prize in Economics.

**Hansen's J test** is the overidentifying-restrictions test built on that GMM framework: $J=n\cdot g(\hat\beta)'W^{-1}g(\hat\beta)$, distributed $\chi^2_{h-k}$ — essentially a generalization of the [[people/sargan|Sargan test]] that allows for **heteroskedasticity** (Sargan is only valid under homoskedasticity). When the data is truly homoskedastic, the two tests coincide.

**Interpretation note common to both tests**: failing to reject $H_0$ only means "no evidence found against instrument validity", **not** "instrument validity has been proven" — validity must always be argued through the research design (the exclusion restriction); the test only supports, never replaces, that argument.

## Appears in

- [[concepts/endogeneity-iv-regression]]
- [[concepts/iv-regression-panel-data]]
