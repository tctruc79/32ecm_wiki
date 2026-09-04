---
title: "Sargan (J. D.)"
type: person
role: "Econometrician — the original overidentifying-restrictions test for IV/GMM under homoskedasticity"
tags: [sargan-test, overidentification, iv-regression]
---

Denis Sargan (1958, *"The Estimation of Economic Relationships using Instrumental Variables"*, Econometrica) proposed the first overidentifying-restrictions test for IV models: when the number of instruments $h$ exceeds the number of endogenous regressors $k$ (overidentified), the Sargan test checks whether the IV residuals are correlated with the full instrument set $Z$ — $J=nR^2$ from regressing the residuals on $Z$, distributed $\chi^2_{h-k}$.

Underlying assumption: **homoskedasticity**. When this assumption fails, [[people/hansen|Hansen's J test]] is the generalization (using the efficient GMM weight matrix instead of $nR^2$), coinciding with Sargan when the data is truly homoskedastic.

**Interpretation note common to both tests**: failing to reject $H_0$ only means "no evidence found against instrument validity", **not** "instrument validity has been proven" — validity must always be argued through the research design (the exclusion restriction); the test only supports, never replaces, that argument.

## Appears in

- [[concepts/endogeneity-iv-regression]]
- [[concepts/iv-regression-panel-data]]
- [[concepts/dynamic-panel-data-models]]
