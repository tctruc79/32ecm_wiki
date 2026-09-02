---
title: "Panel Data: Fixed Effects and Random Effects Model"
type: concept
status: mature
tags: [panel-data, fixed-effects, random-effects, hausman-test, gls, fgls]
sources: ["[[sources/slides-6-fixed-random-effects]]", "[[sources/slides-13-panel-data-variance-structures]]"]
related: ["[[concepts/linear-regression-model]]", "[[concepts/heteroskedasticity]]", "[[people/hausman]]", "[[concepts/iv-regression-panel-data]]", "[[concepts/dynamic-panel-data-models]]"]
updated: 2026-08-29
---

> Revision history: this page merges Topic 6 (`slides-6-iu.pdf`, introductory version) and Topic 12 (`slides-13-iu.pdf`, extended version with fuller variance structures — same company data example but adding GLS/FGLS and the SE types). The structure below follows the extended version.

> **How to read this page**: this is a direct extension of [[concepts/linear-regression-model]] to data with a **time dimension** — all the underlying concepts (PRE/SRE, OLS, assumptions A1–A5, t-test, F-test) still apply, just "detailed further" to fit the panel structure. This page is long because it merges 2 slide decks (basic Topic 6 + extended Topic 12) — so read it in order: (1) what panel data is and why it exists, (2) the expanded assumption set A3a/A3b, A4a/b/c, (3) four estimation methods (Pooled OLS, GLS/FGLS, FE, RE), (4) how to choose the correct SE, (5) the Hausman test for choosing between FE and RE.

## What panel data is — and why it exists

### Three types of data

- **Cross-sectional**: many units, **one** point in time — $y_i$, $i=1,\dots,N$. Example: a wage survey of 1,000 workers at a single point in time.
- **Time-series**: **one** unit, many points in time — $y_t$, $t=1,\dots,T$. Example: Vietnam's GDP year by year.
- **Panel data** (also called longitudinal data): many units **and** many points in time at once — $y_{it}$, $i=1,\dots,N$ (cross-sectional dimension), $t=1,\dots,T$ (time dimension). In other words, panel data = cross-sectional data **observed repeatedly** over time for the same set of units.

**Balanced panel**: every unit $i$ has all $T$ periods observed — total observations $=NT$. **Unbalanced panel**: some units are missing data in some periods — each unit's time index is $t=1,\dots,T_i$, total observations $=\sum_{i=1}^N T_i$.

### Illustrative example: an $N\times T$ mini-panel

The Topic 6 slide uses data from 58 Vietnamese provinces, 5 years (2007–2011) to illustrate the panel structure — each province is a unit $i$, each year is a point in time $t$. An excerpt of the original table (units exactly as the slide records them — see the source-contradiction note right below the table):

|province | year |rgdp (provincial GDP) |labfo (labor force, thousand people) |rinvest (investment) |pci (provincial competitiveness index, 0–100) |
|---|---|---|---|---|---|
| An Giang | 2007 | 22.000.000 | 1.221,3 | 5.600.000 | 66,47 |
| An Giang | 2008 | 25.000.000 | 1.244,9 | 4.600.000 | 61,12 |
| An Giang | 2009 | 25.000.000 | 1.227,3 | 4.800.000 | 58,18 |
| Bac Can | 2007 | 1.500.000 | 177,2 | 592.714 | 46,47 |
| Bac Can | 2008 | 2.000.000 | 179,8 | 1.100.000 | 39,78 |
| Bac Can | 2009 | 2.400.000 | 189,8 | 1.100.000 | 75,96 |
| … | … | … | … | … | … |

This is exactly the $y_{it}$ structure: each row is a pair $(i,t)$ — "An Giang, 2007" is a different observation from "An Giang, 2008" (same $i$, different $t$) and from "Bac Can, 2007" (different $i$, same $t$). $N$ here is the number of provinces (58 provinces per the original description — but the actual `plm` regression tables in later sections show `n = 43, T = 5, N = 215`, meaning only 43 provinces are used in the final balanced panel; the original slide does not explain why 58 dropped to 43 — this could be due to dropping observations with missing data to balance the panel, but this is an inference, not something the slide states explicitly).

> **Source-contradiction note**: the Topic 6 slide states the units of `rgdp` and `rinvest` **two different times** — the first time ("EXAMPLE DATA") as "bil. VND," the second time ("THE DATA") records the same two variables as "mil. VND." This is a genuine contradiction in the original slide, not an extraction error — it is recorded per the wiki's principle, without arbitrarily picking one. Judging by plausible magnitude (a province's GDP is on the order of a few tens of thousands of billion VND in the 2007–2011 period), reading it as "million VND" (mil. VND) gives a far more plausible figure than "billion VND" (bil. VND) — but this is only a reasonable inference, not something the slide confirms.

### Why panel data is useful for identification — connecting to the causal-identification problem

This is the single most important philosophical question of this entire page, and it flows directly from the **identification problem** discussed in [[concepts/econometrics-overview]] (section 8 of that page): to correctly estimate the causal effect of $X$ on $y$, one needs to isolate the part of the variation in $X$ that is **not** driven by confounders. The classic problem: if there is an **unobserved** factor $\alpha_i$ — e.g. a province's institutional quality, a firm's management capability, an individual's "innate ability" — that both affects $y$ and is correlated with $X$, then OLS on ordinary cross-sectional data will be **biased** (violating A3/exogeneity), because $\alpha_i$ gets "mixed" into the error term $\varepsilon_{it}$ and is correlated with $X$.

**The core insight of panel data**: if the unobserved confounding factor $\alpha_i$ is **time-invariant** (constant across years for the same province/firm/individual), then having **multiple observations over time for the same unit** lets us "subtract it away" purely algebraically, **without needing to know** what $\alpha_i$ is or how to measure it. This is exactly the mechanism of the FE estimator in section 9 — an **identification strategy** that needs no external instrument, unlike IV regression in [[concepts/endogeneity-iv-regression]]. In the language of [[concepts/econometrics-overview]]: panel data "uses the time dimension to control for unobserved, time-invariant confounders."

**An important limitation to remember from the start**: this mechanism handles **only** the time-invariant part of confounding. If the confounding factor **changes** over time (e.g. a sudden shock that affects only firm $i$ in a specific year $t$), panel FE does **not** solve it — IV or another design is still needed (see section 9.4 and [[concepts/iv-regression-panel-data]]).

## Advantages and disadvantages of panel data

|Advantages |Disadvantages |
|---|---|
|More observations ($NT$ instead of just $N$ or just $T$) |More costly to collect data (must track the same units across many periods) |
|More variability — e.g. can also capture seasonal effects |Risk of selectivity bias (which units remain in the sample for all $T$ periods may not be random) |
|Less multicollinearity among regressors | |
|Can also analyze time effects | |
|Reduces heterogeneity bias and endogeneity from time-invariant omitted variables (see section 1.3) | |

## Prerequisite: within-group variation

**The FE model requires within-group variation** — if an independent variable does not change over time for a given unit, it will be completely "absorbed" by the fixed effect $\alpha_i$ and **cannot be estimated**.

The slide's counterexample: regressing export volume from Vietnam to country $i$ in year $t$ on the geographic distance from Vietnam to country $i$:
Because geographic distance is **constant** over years (country $i$ is always a fixed distance from Vietnam), this variable has no within-group variation → it cannot be included in a fixed-effects model. This is exactly why FE **does not allow** a time-invariant regressor, while RE (section 10) does — one of the most important differences between the two models.

## The two illustrative datasets used throughout this page

Because this page merges two slide decks, **two** different illustrative datasets appear interleaved in the sections below — **not the same dataset** (this note supplements the "Revision history" line at the top of the page, which might mistakenly suggest "the same company data example"):

| |Topic 6 data (`slides-6-iu.pdf`) |Topic 12 data (`slides-13-iu.pdf`) |
|---|---|---|
|Observation unit |58 Vietnamese provinces (final balanced panel uses $n=43$) |300 firms |
|Number of periods |5 years (2007–2011) |5 years |
|Dependent variable |`log(rgdp)` — log provincial GDP |`log(output)` — log firm output value (million VND) |
|Independent variables |`log(labfo)` (log labor), `log(rinvest)` (log investment), `pci` (competitiveness index) |`log(capital)` (log physical capital), `log(labor)` (log number of workers), `training` (training hours/worker), `export` (export dummy), `credit` (credit-access dummy), `mediumtech`/`hightech` (technology dummies, base `lowtech`) |
|Total observations in the regression | $N=215$ ($n=43\times T=5$) | $N=1.500$ ($n=300\times T=5$) |

The Topic 6 data illustrates Pooled OLS, FE (within/LSDV), basic RE, and the Hausman test with concrete numbers. The Topic 12 data illustrates all **5 SE types** on the same model — since this is exactly the "variance structure" part that Topic 12 adds (see section 12).

## The basic model and its extension over time

$$y_{it}=\alpha_i+\beta x_{it}+\varepsilon_{it} \qquad \text{(one-way fixed effects model)}$$

Each unit $i$ has its own intercept $\alpha_i$ (a "fixed effect"), but the slope coefficient $\beta$ is the same for every unit.

This can be extended to also allow **time effects**:
where $\delta_t$ represents a linear time trend (a constant rate of change over time — e.g. economy-wide technological change). If the rate of change is not linear, use a more general set of time dummies:
where $t=1$ is the reference/base period. This is called the **two-way fixed effects model** — it simultaneously controls for both unit-specific characteristics ($\alpha_i$) and common shocks at each point in time ($\delta_t$, affecting all units equally in that period).

## The full assumption set: A1–A5 extended for panel data

| | Linear Regression Model (Topic 1) | Panel Data Model |
|---|---|---|
| A1 | Linear relationship |Linear relationship (unchanged) |
| A2 | Full rank |Full rank (unchanged) |
| A3 | Exogeneity $E(\varepsilon\vert X)=0$ | **A3a**: $E(X_{it}\varepsilon_{it})=0$ · **A3b**: $E(X_{it}\alpha_i)=0$ |
| A4 | Homoskedasticity $E(\varepsilon\varepsilon'\vert X)=\sigma^2I$ | **A4a**: individual homoskedasticity · **A4b**: no autocorrelation · **A4c**: no cross-sectional correlation |
| A5 | Normality |Normality (unchanged) |

**Why "detail out" A3 and A4?** In ordinary cross-sectional data (Topic 1), the error $\varepsilon_i$ has only **one dimension of variation** (across units). In panel data, the error $\varepsilon_{it}$ has **two dimensions** of variation (across units $i$, and over time $t$ within the same unit) — so a single "lumped" assumption like Topic 1's A3 or A4 is not detailed enough to describe all the possible kinds of violation. Splitting A3 → A3a/A3b and A4 → A4a/b/c is **the key to understanding the rest of this page**: each different model/estimator (Pooled OLS, FE, RE, GLS/FGLS) and each SE type (section 12) differs only in **which sub-assumptions are kept and which are relaxed**.

### A3 → A3a / A3b: two different sources of exogeneity

- **A3a**: $E(X_{it}\varepsilon_{it})=0$ — the independent variable is uncorrelated with the **idiosyncratic** error component (specific to each observation, varying with both $i$ and $t$). This is the "ordinary" exogeneity assumption, identical to the original A3 but applied to panel data.
- **A3b**: $E(X_{it}\alpha_i)=0$ — the independent variable is uncorrelated with the **time-invariant individual effect** $\alpha_i$ (e.g. a firm's management capability, a province's institutional quality). This assumption is **specific to panel data**, and has no counterpart in an ordinary cross-sectional model.

The practical meaning of this split: **A3a is always required** for every panel estimator (Pooled OLS, FE, RE) — if A3a is violated there is genuine endogeneity that no panel model can fix (IV is needed, see [[concepts/iv-regression-panel-data]]). But **A3b can be violated and estimation can still be consistent** — as long as the right estimator is used (FE, see section 9.4) instead of one that requires A3b (RE, see section 10).

### A4 → A4a / A4b / A4c: three dimensions of "constant variance, no correlation"

- **A4a** (individual homoskedasticity): $E(\varepsilon_{it}^2\vert X)=\sigma^2$ for all $i,t$ — the error variance is the same across **all** observations. Common violation: large firms have "noisier" errors than small firms.
- **A4b** (no autocorrelation within panel): $E(\varepsilon_{it}\varepsilon_{is}\vert X)=0$ for $t\neq s$ — the errors of the same unit at two different points in time are uncorrelated. Common violation: a good/bad shock to firm $i$ in year $t$ tends to "persist" into year $t+1$ (a firm's internal conditions are persistent). The most common form of violation is a first-order autoregressive process, **AR(1)**: $\varepsilon_{it}=\rho\varepsilon_{i,t-1}+u_{it}$, where $\rho$ is the correlation coefficient and $u_{it}$ is white noise (iid, mean zero, constant variance). Most panel software packages support only AR(1) since it is the simplest and most common form.
- **A4c** (no cross-sectional/contemporaneous correlation): $E(\varepsilon_{it}\varepsilon_{jt}\vert X)=0$ for $i\neq j$ — the errors of two **different** units at the **same** point in time are uncorrelated. Common violation: a macro shock (a financial crisis, a national policy change) affects many firms/provinces simultaneously.

## Pooled OLS Estimator

**Intuition**: the simplest way to use panel data — pool all $NT$ observations into one large cross-sectional sample, then run ordinary OLS, **treating the panel structure as if there were nothing special about it** (ignoring that multiple observations belong to the same unit).

$$y_{it}=\alpha+\beta X_{it}+u_{it}$$

Pooled OLS assumes **every** $\alpha_i$ is equal ($=$ a common $\alpha$ for all) — the regression coefficients are identical for every unit. If this assumption is wrong (units genuinely differ in unobserved characteristics), Pooled OLS produces **heterogeneity bias**.

**Numerical example** (province data, `pols = lm(log(rgdp) ~ log(labfo) + log(rinvest) + pci)`, $N=215$):

|Variable | Estimate | SE (conventional) | t-value | p-value |
|---|---|---|---|---|
| (Intercept) | 2.770256 | 0.528587 | 5.241 | <0.001 |
| log(labfo) | 0.490986 | 0.072717 | 6.752 | <0.001 |
| log(rinvest) | 0.623586 | 0.045691 | 13.648 | <0.001 |
| pci | 0.012884 | 0.004481 | 2.875 | 0.004 |

$R^2=0.783$, $R^2_{adj}=0.780$. Pooled OLS supports all 5 SE types in section 12 — the table above only uses the conventional SE; section 12.1 will re-run this same idea (but on the company data) with all 5 SE types for direct comparison.

## GLS / FGLS Estimator

**Intuition before the formula**: OLS treats every observation as "equally trustworthy" — each residual contributes equally to the objective function $\sum e_i^2$, regardless of whether that observation is "noisy" or "precise," independent or correlated with other observations. When the errors truly have different variances (heteroskedastic) or are correlated with each other (autocorrelated/clustered), treating them "as equals" the way OLS does **wastes information** — OLS still gives an unbiased estimate (if exogeneity holds), but is no longer the most **efficient** estimator possible. **GLS (Generalized Least Squares)** fixes this by "reweighting" observations: down-weighting noisy/redundant observations (because they're correlated with others), up-weighting clean/independent observations — using the true error covariance matrix to do this optimally.

On the formula: ordinary OLS $b=(X'X)^{-1}X'y$ implicitly assumes the error covariance matrix is $\sigma^2I$ (constant variance, no correlation across observations — exactly the original A4). **GLS** generalizes this, allowing any covariance structure $\Omega$:
$$\beta_{GLS}=(X'\Omega^{-1}X)^{-1}X'\Omega^{-1}y$$

**Problem**: $\Omega$ **cannot be determined without knowing $\beta$ first** (this is a "chicken and egg" problem — $\beta$ is needed to compute residuals, residuals are needed to estimate $\Omega$, but $\Omega$ is needed to compute $\beta_{GLS}$). Solution: **Feasible GLS (FGLS)**, with two approaches:
- Use $\hat\beta_{OLS}$ (from ordinary OLS, still unbiased even if inefficient) to estimate $\Omega$ first, then compute GLS with that $\hat\Omega$ — called **classical FGLS**.
- Estimate $\Omega$ and $\beta$ simultaneously using **Maximum Likelihood (ML)** — another variant of FGLS.

**The FGLS variants correspond to different $\Omega$ structures** — each variant relaxes A4a/A4b/A4c in a different way, and **no variant solves all three at once**:

|$\Omega$ specification |Handles |Does not handle |
|---|---|---|
|No specification (baseline) |— |**Identical to Pooled OLS** since the covariance structure is unspecified |
|Individual heteroskedasticity (unit-specific variance) |A4a, unit by unit |Requires very heavy computational resources with panel data |
|Period/year heteroskedasticity (year-specific variance) |Heteroskedasticity by year |Serial correlation, cross-sectional dependence |
| AR(1) | Autocorrelation (A4b) |Heteroskedasticity, cross-sectional dependence |
|Time heteroskedasticity + AR(1) combined |Both of the above at once |Cross-sectional dependence (A4c) still not handled |

None of the FGLS variants above fully handles all three (A4a+A4b+A4c) at once at the **estimation** level — something Driscoll-Kraay SE (section 12) does, but only at the **inference** level, i.e. it corrects the SE rather than changing how $\beta$ is estimated.

## Fixed Effects (FE) Model

$$y_{it}=\alpha_i+\beta X_{it}+u_{it}$$

This model allows **each unit to have its own intercept** $\alpha_i$ ("fixed effect," representing that unit's entire set of characteristics that do not change over time), while the slope coefficient $\beta$ remains the same for every unit. There are **two** equivalent ways to estimate it (not two different models — just different computations, yielding the same $\beta$).

### Within-group (demeaning) estimator

**Intuition before the formula**: if $\alpha_i$ is a constant **that does not change over time** for unit $i$, then the time average of $y_{it}$ for that unit also contains $\alpha_i$ intact. When $y_{it}$ is subtracted by that unit's own time average $\bar y_i$, $\alpha_i$ appears in both terms and **cancels completely** — this is exactly the mathematical mechanism embodying the idea "subtracting each individual's own mean removes the fixed effect" mentioned in section 1.3. What remains is only the **variation around each unit's own mean** — this explains why section 3 says FE requires "within-group variation": if $X_{it}$ does not vary around its own mean, the subtraction cancels $X$ too, leaving nothing to estimate $\beta$ from.

On the formula: starting from the original model
take the time average for each unit (note $\alpha_i,\beta$ do not change with $t$, so they are unaffected by averaging):
Subtracting (2) from (1):
$\alpha_i$ has been completely eliminated — running OLS on this "demeaned" equation estimates $\beta$, but does **not** estimate $\alpha_i$ (lost through the subtraction, exactly as the intuition above suggested).

**Numerical example** (province data, `plm(model = "within")`, $n=43$, $T=5$, $N=215$):

|Variable | Estimate | SE (conventional) | t-value | p-value |
|---|---|---|---|---|
| log(labfo) | 1.0781368 | 0.1820954 | 5.9207 | <0.001 |
| log(rinvest) | 0.2658911 | 0.0475283 | 5.5944 | <0.001 |
| pci | 0.0056793 | 0.0019995 | 2.8404 | 0.005 |

$R^2=0.4433$ — much lower than Pooled OLS ($R^2=0.783$) because FE uses only the **within-group** variation, discarding all the **between-group** variation that Pooled OLS exploits — this directly explains why FE is less efficient (section 11).

### Least Squares Dummy Variable (LSDV) estimator

A second way to estimate the same FE model: include $N$ dummy variables, one per unit:
Run ordinary OLS on this equation. **The $\beta$ coefficient is identical to the within-group estimator** (not an approximation — identical to many decimal places, see the numerical example below), but LSDV **also estimates $\alpha_j$** (each dummy's coefficient is exactly that unit's fixed effect). Trade-off: LSDV is **infeasible when $N$ is large** (an extra $N$ parameters must be estimated).

**Numerical example confirming "identical"** (`fe1 = lm(log(rgdp) ~ log(labfo) + log(rinvest) + pci + factor(province))`):

|Variable | LSDV Estimate |Within-group Estimate (section 9.1) |
|---|---|---|
| log(labfo) | 1.078137 | 1.0781368 |
| log(rinvest) | 0.265891 | 0.2658911 |
| pci | 0.005679 | 0.0056793 |

A perfect match. LSDV additionally gives `(Intercept) = 4.932273` and 42 province dummy coefficients (e.g. `factor(province)3 = -0.613103`) that within-group cannot produce.

### Two-way FE

Adding time dummies to LSDV:
controls simultaneously for unit-specific characteristics and common shocks at each point in time. Numerical example (`fe2` adds `factor(year)`, $N=215$): `factor(year)2008 = 0.098326` (p<0.001), `factor(year)2011 = 0.431488` (p<0.001) — showing that provincial GDP tends to rise steadily by year beyond what is already explained by $X$, $R^2=0.9918$.

### FE's consistency property and its limitations

**FE's most important property**: the FE estimator is **consistent even when A3b is violated** ($E(X_{it}\alpha_i)\neq0$, i.e. $\alpha_i$ is correlated with $X$) — this is exactly why FE is preferred when a time-invariant confounder correlated with the explanatory variable is suspected (exactly the mechanism explained in section 1.3: $\alpha_i$ is eliminated algebraically, so no matter how strongly it is correlated with $X$, it no longer affects the estimated $\beta$). But **A3a is still required** — if A3a is violated (the idiosyncratic error $u_{it}$ is correlated with $X_{it}$), FE still has endogeneity; no "magic" can fix this. **FE's SE is unbiased only if A4a, A4b, A4c all hold** — otherwise robust/clustered/DK SE is needed (section 12).

**FE's limitation**: the FE model solves endogeneity from a **time-invariant omitted variable**, but remains "fragile" against endogeneity from other sources: measurement error (in $X$), reverse causality ($y$ also affects $X$ back), simultaneity ($X$ and $y$ are determined jointly). These cases need other tools — see [[concepts/endogeneity-iv-regression]] and [[concepts/iv-regression-panel-data]].

## Random Effects (RE) Model

**The core philosophical difference from FE**: instead of treating $\alpha_i$ as a fixed constant unique to each unit (as FE does), RE treats $\alpha_i$ as a **random variable** — a "chance" component drawn from a common distribution, (assumed) independent of $X$. Since $\alpha_i$ is no longer something to be algebraically "eliminated," but part of the error structure that must be **modeled**, RE is estimated by GLS rather than demeaning.

$$y_{it}=\alpha_0+\alpha_i+\beta X_{it}+\varepsilon_{it}, \qquad \alpha_i\sim N(0,\sigma_\alpha^2),\;\; \varepsilon_{it}\sim N(0,\sigma_\varepsilon^2)$$

The composite error $u_{it}=\alpha_i+\varepsilon_{it}$ has two components: $\alpha_i$ — the individual specific random component, and $\varepsilon_{it}$ — the idiosyncratic disturbance. In RE, $\alpha_i$ is **not estimated separately for each unit** as in LSDV — instead, only $\sigma_\alpha^2$ (the variance of $\alpha_i$) is estimated. Since $\alpha_i$ is not "subtracted away" as in FE, **RE allows a time-invariant regressor** — the most important practical difference from FE (section 3).

**Why RE is more efficient than FE when correct, but biased when wrong**: RE is **consistent only if A3b holds** ($E(X_{it}\alpha_i)=0$ — the random component $\alpha_i$ is uncorrelated with $X$; A3a is still needed as with every other model). If A3b truly holds, RE is **more efficient than FE** because it does not "spend" degrees of freedom estimating $N$ separate intercepts as LSDV does — it only needs to estimate a single parameter $\sigma_\alpha^2$, retaining more degrees of freedom, hence smaller SE, more precise estimates. But if A3b is **wrong** (indeed a common case in practice — e.g. a firm's management capability affects $y$ and is also correlated with the investment decision $X$), RE's "random, independent of $X$" assumption is violated → the RE estimate is **biased and inconsistent**, no matter how large the sample. **RE's SE is unbiased only if A4a, A4b, A4c hold.**

**Numerical example** (province data, `plm(model = "random")`, Swamy-Arora's transformation, $n=43$, $T=5$, $N=215$):

|Variable | Estimate | SE (conventional) | z-value | p-value |
|---|---|---|---|---|
| (Intercept) | 5.1685242 | 0.7005398 | 7.3779 | <0.001 |
| log(labfo) | 0.8689746 | 0.1078362 | 8.0583 | <0.001 |
| log(rinvest) | 0.3390771 | 0.0444305 | 7.6316 | <0.001 |
| pci | 0.0054236 | 0.0020291 | 2.6729 | 0.008 |

Variance components: idiosyncratic $\sigma_\varepsilon^2=0.02524$ (12.4% of total variance), individual $\sigma_\alpha^2=0.17900$ (87.6%) — showing that most of the error variation comes from **between-province** differences (unobserved), not from year-to-year movement within the same province. $R^2=0.564$.

Compared with FE (section 9.1): RE's `log(labfo)` coefficient (0.869) differs quite a bit from FE's (1.078); `log(rinvest)` also differs (0.339 vs. 0.266). This is exactly the kind of discrepancy the Hausman test (section 13) is designed to check — whether it is "systematic" or just sampling noise.

## FE vs. RE — decision summary table

| | FE | RE |
|---|---|---|
|Assumption about $\alpha_i$ |Fixed, allowed to correlate with $X$ in any way |Random, assumed uncorrelated with $X$ |
|Consistency requires |A3a (A3b not needed) |A3a **and** A3b |
|Allows a time-invariant regressor? |No |Yes |
|Efficiency |Lower (spends degrees of freedom estimating $N$ intercepts if using LSDV) |Higher (more degrees of freedom) if A3b holds |
|Risk if the assumption is wrong |No added risk (FE stays consistent even if A3b is wrong) |Biased, inconsistent if A3b is wrong |

**In short**: RE is more efficient but can be inconsistent if A3b is wrong; FE is less efficient but more robust (does not need A3b). Rule of thumb: **only use RE if the estimated coefficients do not differ systematically from FE** — this question is formally answered by the Hausman test (section 13).

## Five types of standard errors — common to Pooled OLS, FE, RE

The A4a/A4b/A4c assumption set (section 6.2) determines **which formula is correct for computing the SE** — choosing the wrong SE type does not change the estimated coefficient $\beta$ (an important point to remember, see the numerical example in section 12.1), but it can completely mislead the conclusion about statistical significance.

|SE type |Assumption being "patched" (relaxed) |Robust to |When to use |
|---|---|---|---|
|Conventional (default) |Nothing relaxed — keeps A4a+A4b+A4c intact |Nothing |Only when there is reason to believe all three hold — rare in real panel data |
| Robust (heteroskedasticity-robust) | A4a | Heteroskedasticity |Error variance is suspected to be non-constant across observations (e.g. large firms "noisier" than small firms), but there is no reason to suspect correlation over time or across units |
| (One-way) Clustered | A4a + A4b |Heteroskedasticity + autocorrelation within the same unit |The most common default choice in modern panel-data practice — reasonable when errors of the same unit may be correlated over time |
| Two-way clustered | A4a + A4b + A4c |All three, including cross-sectional dependence |A common time shock affecting many units simultaneously is suspected (crisis, macro policy change) — but **$T$ must be large enough**; a small $T$ gives unreliable estimates and may even trigger a non-positive-definite VCV matrix warning (see the numerical example in section 12.1) |
| Driscoll-Kraay (DKSE) | A4a + A4b + A4c |All three, HAC-style (Heteroskedasticity and Autocorrelation Consistent) |A panel with relatively large $T$, cross-sectional dependence is suspected but conditions are insufficient for reliable two-way clustering; assumes autocovariance decays over lags |

### Numerical example: the same model, 5 different SE types (Pooled OLS, company data)

Model `log(output) ~ log(capital) + log(labor) + training + export + credit + mediumtech + hightech`, $N=1,500$ (300 firms × 5 years). **The key point to notice**: the estimated coefficients (Estimate column) are **identical across all 5 columns** — only the SE (and hence t-value, p-value) changes:

|Variable | Estimate | SE Conventional | SE Robust | SE Clustered (id) | SE Two-way clustered (id & year) | SE Driscoll-Kraay (L=1) |
|---|---|---|---|---|---|---|
| log(capital) | 0,257119 | 0,015124 | 0,014443 | 0,013814 | 0,023524 | 0,015417 |
| log(labor) | 0,041700 | 0,023417 | 0,023621 | 0,023191 | 0,024146 | 0,025055 |
| training | 0,053184 | 0,003101 | 0,003119 | 0,003350 | 0,002318 | 0,001230 |
| export | 0,030659 | 0,029467 | 0,028805 | 0,031019 | 0,029538 | 0,031529 |
| credit | 0,019788 | 0,027438 | 0,027688 | 0,027974 | 0,029791 | 0,025060 |
| mediumtech | −0,055506 | 0,030407 | 0,030790 | 0,030565 | 0,034516 | 0,026808 |
| hightech | 0,142140 | 0,037643 | 0,036466 | 0,036085 | 0,048573 | 0,036757 |

**A notable observation**: `hightech` is always statistically significant across all 5 SE types, but the p-value widens considerably — from $<2\times10^{-16}$ (conventional) to $0.043$ (two-way clustered), then $0.018$ (DK) — still rejecting $H_0$ at $\alpha=5\%$, but with a much narrower safety margin. `training`'s SE **drops sharply** under Driscoll-Kraay (0.00330 → 0.00123, t-value jumping from 17 to 43) — illustrating that a "more robust" SE **does not mean a larger SE**; the direction of change depends entirely on the data's true correlation structure, with no rule that "more robust always means more conservative." This same pattern repeats in the FE numerical example below — reinforcing: **the SE type must be chosen based on understanding the data structure (is there autocorrelation? a common yearly shock?), not by picking whichever type gives the "nicest" p-value.**

For the two-way clustered SE table, R actually outputs the warning: `Warning message: The VCOV matrix is not positive definite and was 'fixed'` — another manifestation of the same numerical issue that will reappear in the Hausman test (section 13.3): estimating a covariance matrix from too little independent information ($T=5$ here is fairly small for two-way clustering) can produce a matrix that is not truly invertible.

### Numerical example: within-group FE with 5 SE types (company data)

The same model but estimated with within-group FE instead of Pooled OLS — once again, the coefficients **do not change** across the 5 SE types (this is exactly the "identical to LSDV estimator" property mentioned in section 9.2):

|Variable | Estimate | SE Conventional | SE Robust | SE Clustered | SE Driscoll-Kraay |
|---|---|---|---|---|---|
| log(capital) | 0,25858 | 0,01104 | 0,00988 | 0,01107 | 0,00532 |
| log(labor) | 0,02277 | 0,01677 | 0,01460 | 0,01587 | 0,01307 |
| training | 0,04368 | 0,00228 | 0,00207 | 0,00229 | 0,00185 |
| export | 0,02262 | 0,02160 | 0,01969 | 0,02306 | 0,01803 |
| credit | 0,06515 | 0,01980 | 0,01819 | 0,02124 | 0,00919 |
| mediumtech | −0,01277 | 0,02203 | 0,02005 | 0,02362 | 0,02524 |
| hightech | 0,18311 | 0,02740 | 0,02413 | 0,02665 | 0,03728 |

`log(labor)` is not statistically significant under any SE type (p ranges 0.082–0.175); `credit` goes from strongly significant (conventional/robust/clustered SE, p<0.004) to **still significant but with a much smaller SE** under Driscoll-Kraay (0.00919 vs. ~0.02) — once again confirming: there is no "certain" direction of change when switching SE types; the data structure must be understood first before choosing.

## Hausman Test (FE vs. RE)

**Intuition**: the Hausman test resolves the question "should FE or RE be used?" by **comparing two estimates** of the same $\beta$. The core logic: FE is always **consistent** regardless of whether A3b holds (section 9.4); RE is only **more efficient** (more precise) **if** A3b holds, but is **inconsistent** if A3b is wrong (section 10). So if A3b truly holds, the FE and RE estimates — though differing in efficiency — must, in expectation, **give the same value** (both are consistent, and the observed difference is just sampling noise). Conversely, if A3b is wrong, RE is biased while FE is not — the two estimates will differ **systematically**, something sampling noise alone cannot explain. The Hausman test is exactly the statistical test for this "systematic difference."

$H_0: \beta_{RE}$ does not differ systematically from $\beta_{FE}$ (equivalently: both are consistent), $H_a$: RE is inconsistent
$$H = (\hat\beta_{FE}-\hat\beta_{RE})'\big[V(\hat\beta_{FE})-V(\hat\beta_{RE})\big]^{-1}(\hat\beta_{FE}-\hat\beta_{RE}) \sim \chi^2_{k}$$

where $k$ = the number of regressors being tested, $V(\beta)$ is the covariance matrix. **Decision rule**: reject $H_0$ if the p-value is small.
- **Reject $H_0$**: the RE and FE estimates differ systematically → **FE is consistent, RE is not** → use FE.
- **Fail to reject $H_0$**: RE and FE do not differ meaningfully → both are "good" (in the sense of being consistent), but **RE is more efficient** — RE should be preferred (recalling the principle "failing to reject ≠ proving true" from [[concepts/linear-regression-model]] section 7.5 — it only means "insufficient evidence against RE," not "RE has been confirmed absolutely correct").

**Numerical example** (Topic 6, province data, `phtest(fe, re)`):
$p=0.0005 \ll 0.05$ → **strongly reject** $H_0$ → use FE for this data. This result is consistent with the observation in section 10: FE's and RE's `log(labfo)` and `log(rinvest)` coefficients really do differ substantially (1.078 vs. 0.869; 0.266 vs. 0.339) — the Hausman test confirms this gap is **systematic**, not random noise.

### Three important notes when using the Hausman test

1. **Can only be tested with the same set of regressors.** If RE has a time-invariant variable (impossible in FE, since FE demeans/absorbs it entirely, see section 3), the Hausman test **cannot be performed** — the two models no longer have "the same $k$ coefficients" to compare.
2. **The Hausman test only checks whether the two estimates are equal** — it does not independently judge the absolute correctness of either model.
3. **The most important exam trap**: if any regressor is correlated with the error in a way that violates **A3a** (genuine endogeneity, not just an A3b violation), **both FE and RE are biased** — the Hausman test cannot save this case, since it only compares FE with RE on the premise that A3a already holds for both. IV for panel data is needed instead — see [[concepts/iv-regression-panel-data]].

### "Vb-VB is not positive definite" — a practical note

When running `phtest()` (or an equivalent command) in R, one sometimes encounters the warning:
> **"Vb-VB is not positive definite"**

This warning means the covariance-matrix difference $V(\hat\beta_{FE})-V(\hat\beta_{RE})$ is **not truly invertible** in the mathematical sense — so the test statistic $H$ **cannot be computed correctly** (the formula requires inverting this matrix). Fixes according to the original slide:
- Check for **outliers** in the data.
- Check for **multicollinearity** (see [[concepts/multicollinearity]]).
- **Rescale** the variables.
- Try a different **functional form** for the model.

A connecting note: this is **not** an isolated phenomenon — in section 12.1, the two-way clustered SE example for Pooled OLS hit a similar warning ("The VCOV matrix is not positive definite and was 'fixed'"). Both are manifestations of the same underlying numerical issue: **estimating a covariance matrix from too little independent information** (e.g. small $T$, few clusters, or collinearity among variables) easily produces a matrix that is numerically singular or near-singular, even though the "true" matrix is always invertible in theory.

## Summary of exam traps

1. Treating "failing to reject the Hausman test" as absolute proof RE is "correct" — it only means "insufficient evidence against RE," consistent with the general principle for interpreting "failing to reject $H_0$" discussed in [[concepts/linear-regression-model]].
2. Running the Hausman test when the two models have different regressor sets (e.g. RE has a time-invariant variable that FE cannot have) — the test is invalid.
3. Forgetting that if A3a is violated (not just A3b), **both FE and RE are biased** — a switch to IV is needed, not just choosing between FE/RE via the Hausman test.
4. Confusing the 5 SE types (conventional/robust/clustered/two-way clustered/DK) — each relaxes a different subset of A4a/b/c, **not** "the more robust the better, always use the strongest type" — two-way clustered and DK need a sufficiently large $T$ to be reliable, and as the numerical examples in section 12 show, a "more robust" SE can be **larger or smaller** than the original SE depending on the data's true structure.
5. Thinking that changing the SE type changes the estimated coefficient $\beta$ — SE only affects **statistical inference** (t-test, p-value, confidence interval), not the point estimate (see the numerical examples in sections 12.1–12.2, where Estimate stays fixed across all 5 columns).
6. Including a time-invariant variable (e.g. fixed geographic distance) in an FE model — this variable will be completely "absorbed" by the fixed effect and cannot be estimated (section 3).
7. Treating FE as always "safer" than RE in every case — FE still needs A3a like every other model, and is always less efficient than RE when A3b truly holds; defaulting to FE without testing wastes efficiency unnecessarily.
8. Confusing Pooled OLS being "still consistent" when A4 (in any form) is violated, with its "SE still being correct" — these are entirely different things: violating A4a/b/c does not bias the coefficient, but does make the default SE wrong, leading to incorrect statistical-inference conclusions (in the same spirit as [[concepts/heteroskedasticity]]).

## Connections to the rest of the course

This page extends [[concepts/linear-regression-model]] to panel data — the A3a/A3b and A4a/b/c triads here are the "detailed" version of the original A3, A4, stemming directly from the identification question raised in [[concepts/econometrics-overview]] (section 1.3 of this page). [[people/hausman]] appears both here and in [[concepts/endogeneity-iv-regression]] (Wu-Hausman test) — the same logic of comparing two estimators, one always consistent and one only efficient under $H_0$. This is the direct foundation for [[concepts/iv-regression-panel-data]] (when A3a is violated — both FE and RE are powerless, and an instrumental variable is needed) and [[concepts/dynamic-panel-data-models]] (when a lagged $y$ is added to the right-hand side, creating a new form of endogeneity that the within-group estimator cannot handle). The problem of choosing the correct SE type (section 12) is a direct variant of [[concepts/heteroskedasticity]], extended for the two-dimensional (unit × time) structure specific to panel data.
