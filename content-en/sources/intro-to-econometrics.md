---
title: "Introduction to Econometrics"
type: source
raw_file: "raw/SLIDES/VNP2026-intro.pdf"
pages: 22
topic: 0
status: current
ingested: 2026-07-29
concepts: ["[[concepts/econometrics-overview]]"]
---

## Role of this document

The first lecture deck (Topic 0 in the Course Outline) by **[[people/truong-dang-thuy|Trương Đăng Thụy]]**. Lays the conceptual groundwork for the whole course: what econometrics is, why correlation ≠ causality, and the empirical research process. No estimation formulas in this deck — purely conceptual, with illustrative examples (electricity prices, storms, education–wages, firefighters, pirates).

## Content flow (narrative)

1. **Why econometrics?** — economics proposes theories about individual/firm/market behavior; data is needed to test those theories.
2. **What is econometrics?** — combines 3 elements: economic theory (proposes hypotheses) + mathematical models (formalizes them) + statistical methods (estimation, testing).
3. **Econometrics vs. Statistics** — statistics focuses on describing/predicting patterns in data; econometrics focuses on **economic mechanisms** and **causal inference**.
4. **Statistical association** — two variables "moving together" does not mean one causes the other.
5. **Association vs. Causality** — three reasons association can mislead: *confounding variables*, *reverse causality*, *coincidence* (each with a concrete illustrative example).
6. **Economic example**: `wage = β0 + β1·education + u` — ability, family, and social networks are confounders hidden inside `u`, making `education` correlated with the error term → `β̂1` ends up estimating a mix of the education effect and the ability effect.
7. **Ceteris paribus** — the effect of one variable holding the others constant; this is what every regression coefficient `bⱼ` tries to capture.
8. **Omitted variable bias** — leaving out an important (unobserved) variable biases the estimated coefficient.
9. **Identification problem** — the central problem of econometrics: finding the part of the variation in a regressor that is *not* driven by confounding factors. Example: only an across-the-board electricity price hike from government policy (independent of household characteristics) lets us identify the causal effect of price on consumption.
10. **Causal inference: economics vs. natural science** — natural science uses controlled experiments (random assignment) to isolate causality; economics can rarely do this (you cannot randomize years of schooling or a tax system) → it must rely on observational data and indirect identification strategies.
11. **Empirical research process** — 6 steps: (1) research question → (2) economic theory → (3) empirical model → (4) data → (5) econometric analysis → (6) interpretation & policy implications.
12. **3 foundational questions** for empirical research: What is the economic question? What is the economic mechanism? Can the causal effect be identified in the data?
13. **Common mistakes**: treating association as causation; assuming regression automatically produces a causal effect; focusing on estimation while forgetting the identification problem.
14. **Course preview** — 3 main parts: (a) the Linear Regression Model and its problems (OLS, multicollinearity, heteroskedasticity, endogeneity); (b) Models for Limited Dependent Variables (logit/probit, multinomial logit, Poisson/NB, ordinal, censored/truncated); (c) Panel data models (FE/RE, panel IV: 2SLS/LIML/GMM, dynamic panel).
15. **Course platform**: econometrics.site — practice, assignments, project submission.

## Note

All the conceptual content of this deck has been synthesized into `[[concepts/econometrics-overview]]` — that page holds the full synthesis (definitions, examples, comparison tables). This page only records provenance and the original slide's narrative flow.
