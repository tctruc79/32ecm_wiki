---
title: "Stock & Yogo"
type: person
role: "Econometricians — critical-value tables for testing weak instruments"
tags: [stock-yogo, weak-instruments, iv-regression]
---

James H. Stock & Motohiro Yogo (2005, *"Testing for Weak Instruments in Linear IV Regression"*, in *Identification and Inference for Econometric Models*) provide a table of **critical values** for evaluating the [[people/cragg-donald|Cragg-Donald (CD) F]] statistic — answering the question "how large does CD-F need to be to call the instruments not weak?".

The Stock-Yogo thresholds are built on **two different criteria**, which are commonly confused with each other:

- **Maximum relative bias**: a threshold such that 2SLS's bias relative to OLS does not exceed an allowed proportion (e.g. 10%).
- **Maximum size distortion**: a threshold such that a nominal 5% Wald test's actual size distortion does not exceed an allowed level (e.g. the test's true size is 10% or 15% instead of 5%).

An instrument can meet one criterion but not the other — state clearly which criterion is being used when reporting results, not just a generic "exceeds the Stock-Yogo threshold." The table was designed only for CD-F (homoskedastic assumption); it is not formally valid for the Kleibergen-Paap F (robust to heteroskedasticity), though in practice people still compare them informally.

## Appears in

- [[concepts/endogeneity-iv-regression]]
- [[concepts/iv-regression-panel-data]]
