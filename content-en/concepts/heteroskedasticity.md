---
title: "Lecture 4: Heteroskedasticity"
type: concept
status: mature
tags: [heteroskedasticity, robust-standard-errors, linear-regression, model-diagnostics]
sources: ["[[sources/slides-4-heteroskedasticity]]"]
related: ["[[concepts/linear-regression-model]]", "[[concepts/multicollinearity]]"]
lecture: 4
assignment: ["Assignment 3: Heteroskedasticity"]
updated: 2026-09-04
---

> **How to read this page**: this is the patch page for OLS's **A4 assumption (Homoskedasticity)** — if you're not yet clear on what A4 is and why it matters, read sections 4 and 6 of [[concepts/linear-regression-model]] first.
> The key point to keep in mind throughout this page: heteroskedasticity does **not** make the regression coefficient wrong — it makes **the measure of uncertainty around that coefficient** (SE, and hence the t-test, F-test, p-value, confidence interval) unreliable.
> This is a problem of **statistical inference**, not a problem of **estimation accuracy**.

**Lecture 4** in the syllabus (CO Topic 4) — Assignment 3: Heteroskedasticity.

## Intuition first — what is heteroskedasticity

Imagine a model predicting **household expenditure** (`expense`) based on **income** (`income`).
For low-income households, their spending choices are fairly constrained — most of their income must go toward essential needs, so these households' actual expenditure tends to sit **close** to the model's predicted level, with small errors.
In contrast, for high-income households, the range of choices is much wider: some households save most of their income, others spend lavishly, far beyond the "average" level the model predicts — the prediction errors for this group **fluctuate much more widely**.

In other words: **the magnitude of the prediction error (residual) is not uniform across observations** — it tends to "balloon" as some variable (here, income, or the predicted value $\hat y$) increases.
This is exactly **heteroskedasticity** ("hetero" = different, "skedasticity" = dispersion).
Conversely, if the magnitude of the prediction error is uniform regardless of the observation — no household is systematically predicted "further off" than another — that is **homoskedasticity**, OLS's A4 assumption (see [[concepts/linear-regression-model]] section 4).

A concrete numerical example illustrating exactly this phenomenon appears in sections 4–5 below — using the very same household expenditure dataset that the original slides use throughout.

## Formal definition

The **A4 (Homoskedasticity)** assumption of the CLRM (Classical Linear Regression Model) states that the error variance is **constant**, unchanging across observations:

$$Var(\varepsilon_i) = \sigma^2 \quad \text{for all } i, \qquad \text{equivalently } Var(\varepsilon|X) = \sigma^2 I$$

where $I$ is the $n\times n$ identity matrix — meaning not only that the variance is equal across all observations, but also that the error at one observation is uncorrelated with the error at another observation (the off-diagonal elements of the error VCV matrix are zero).

**Heteroskedasticity** is when this assumption is **violated**:

$$Var(\varepsilon_i) \neq \sigma^2 \quad \text{(the error variance changes with } i\text{)}, \qquad \text{i.e. } Var(\varepsilon|X) \neq \sigma^2 I$$

The "standard" VCV and SE that OLS reports by default (including in R's `summary(lm(...))`) are computed **assuming A4 holds** — this is why violating A4 makes those numbers suspect (see section 6).

## Sources of heteroskedasticity

The slides list three common sources, not mutually exclusive:

1. **Outliers in the data**: a few extreme observations can pull the error variance up abnormally high in the region of the data containing that outlier.
2. **Wrong functional form**: for example the true model is nonlinear (log, quadratic…) but is estimated as linear — this "omitted nonlinearity" can manifest as non-uniform error variance. (See also [[concepts/functional-forms]].)
3. **Mixing different groups of observations** — for example mixing high-income and low-income households in the same sample (exactly as in the intuition example in section 1): each group may inherently have a different "noise" level, and once pooled together, the overall error variance is no longer uniform.

## Running example: 2020 Ho Chi Minh City household expenditure survey

The slides use a dataset surveying married couples in Ho Chi Minh City in 2020 (`https://econometrics.site/public/mcl.csv`) — **the same dataset** used in [[concepts/multicollinearity]], but serving two different diagnostic purposes (see the "Connections" section at the end of the page).

|Variable |Meaning |Unit |
|---|---|---|
| `expense` |Household expenditure — **dependent variable** |million VND/month |
| `income` |Household income |million VND/month |
| `age_wife` |Wife's age |years |
| `age_husband` |Husband's age |years |
| `hhsize` |Household size (number of members) |persons |
| `children` |% of children in household | % |

After removing observations with missing data (NA) and households with `income = 0`, the remaining sample is $n=470$.

**Descriptive statistics** (to get a feel for scale before reading the coefficients):

|Variable | n | mean | sd | median | min | max |
|---|---|---|---|---|---|---|
| `expense` | 470 | 12.02 | 11.16 | 10.0 | 1.0 | 180.00 |
| `income` | 470 | 17.03 | 17.00 | 12.5 | 0.4 | 180.00 |
| `age_wife` | 470 | 44.91 | 10.86 | 45.0 | 22.0 | 86.00 |
| `age_husband` | 470 | 48.36 | 10.73 | 49.0 | 26.0 | 84.81 |
| `hhsize` | 470 | 4.72 | 2.32 | 4.0 | 1.0 | 25.00 |
| `children` | 470 | 7.88 | 13.06 | 0.0 | 0.0 | 60.00 |

Notice right away from the descriptive table: `expense` has a standard deviation (sd = 11.16) close to its mean (mean = 12.02), and the max (180) is very far from the median (10) — an early sign that the expenditure distribution is strongly right-skewed, which often comes together with heteroskedasticity in linear regression.

**Full OLS regression results** (`expense ~ income + age_wife + age_husband + hhsize + children`) — this table of numbers is reused throughout the BP test, robust SE, and Wald F-test sections below:

|Variable | Estimate |Std. Error (usual) | t value | Pr(>\|t\|) |
|---|---|---|---|---|
| (Intercept) | 0.13924 | 2.22451 | 0.063 | 0.950 |
| `income` | 0.42851 | 0.02368 | 18.094 | < 2e-16 *** |
| `age_wife` | 0.11018 | 0.09317 | 1.183 | 0.238 |
| `age_husband` | −0.08587 | 0.09351 | −0.918 | 0.359 |
| `hhsize` | 0.69243 | 0.16934 | 4.089 | 5.11e-05 *** |
| `children` | 0.06613 | 0.03092 | 2.139 | 0.033 * |

Residual SE = 8.394 on 464 df; $R^2=0.4399$, Adjusted $R^2=0.4338$; F-statistic = 72.88 on 5 and 464 df, p-value < 2.2e-16.

Quick read: `income` and `hhsize` have a very clear effect on expenditure (very small p); `children` is statistically significant at the 5% level (but — see section 9 — this **will change** once robust SE is used); `age_wife` and `age_husband` are not statistically significant.
This is the "usual" results table — meaning it uses SE computed under the A4 assumption.
The question that arises: does the A4 assumption actually hold here?

## Graphical detection (visual, before formal testing)

The slides illustrate two residual plots from the model above:

- **Density plot of the residuals** (`plot(density(data$u))`): the residual distribution has a sharp peak around 0 but a **very long right tail**, extending past 100 (while most of the mass sits within [−20, 20]) — a sign that the residuals are asymmetric, suggesting both a normality issue (A5) and the possibility of outliers/heteroskedasticity.
- **Residuals vs. Predicted values** (`plot(data$yh, data$u)`, x-axis = "Predicted monthly expense", y-axis = "Residuals"): this is the classic heteroskedasticity diagnostic plot.
  When the predicted value is still low (around 0–20 million VND), the residual points cluster very tightly around 0.
  But as the predicted value increases (40–80 million VND), the residual points **spread out much more widely** — ranging from about −40 to nearly +100.
  This "megaphone" shape (fan-out/cone shape) — the spread of the residuals increasing with the predicted value — is the standard visual signature of heteroskedasticity, and matches exactly the intuition from section 1 (households with high predicted expenditure — i.e. high-income households — have prediction errors that fluctuate much more widely).

The plots only give a **visual hint**, not formal statistical evidence — the formal tests in sections 7–8 are needed to reach a firm conclusion.

## Consequences of heteroskedasticity — the most commonly misunderstood point

This is the **most important** part of the entire topic, because it is the source of the most common exam trap (see section 11, trap #1).

**What heteroskedasticity does NOT do**: the OLS estimated coefficient $b=(X'X)^{-1}X'y$ **remains unbiased and consistent**.
The underlying reason: OLS's unbiasedness/consistency rests only on assumptions A1–A3 (linearity, full rank, exogeneity) — see [[concepts/linear-regression-model]] section 4.
A4 (homoskedasticity) is **not** among the conditions required for unbiasedness/consistency; it only pertains to **efficiency** and the **VCV/SE formula**.
Violating A4 does not touch A1–A3 at all, so $b$ remains a correct estimator, just no longer "best" in the sense below.

**What heteroskedasticity ACTUALLY does**, through two lines of consequence:

1. **Losing "Best" in BLUE**: the Gauss-Markov theorem says OLS is the **B**est **L**inear **U**nbiased **E**stimator — but the word "Best" (smallest variance among unbiased linear estimators) only holds **when A4 holds**.
   When heteroskedasticity occurs, OLS remains Linear and Unbiased, but **is no longer Best** — there exists another estimator (GLS/WLS with appropriate weights) that is more efficient than OLS in this setting.
   In other words: OLS is still correct "on average" but is no longer "as tight as possible".
2. **The standard VCV/SE formula becomes wrong**: the standard VCV is computed under the A4 assumption:
   and SE is the square root of the diagonal elements of this VCV.
   This formula **is only correct when $Var(\varepsilon)=\sigma^2$ is constant**.
   When A4 is violated, the formula above no longer correctly reflects the true uncertainty of $b$ — in the words the original slide uses: "VCV and SE are biased".
   *Interpretive note*: the slide's use of the word "biased" here is more of an intuitive description than a technically rigorous statement about the sampling distribution of SE; the precise thing to understand is that **the usual SE formula is no longer a valid (invalid/not appropriate) estimate of the true uncertainty of $b$** when A4 is wrong — the computed SE can be too small or too large relative to reality, with no fixed direction.

**Chain-reaction consequence**: since the t-statistic $=\dfrac{b_j-c}{SE(b_j)}$ and the F-statistic (via the Wald test, see section 10) are both built directly on SE/VCV, when SE is wrong then **the t-statistic is wrong, the p-value is wrong, the confidence interval is wrong** — the entire chain of statistical inference becomes unreliable, **even though the coefficient $b$ itself is still correct**.

> **The most common misunderstanding trap of the whole topic**: many learners mistakenly believe that "heteroskedasticity makes the regression coefficient biased".
> This is **WRONG**.
> Heteroskedasticity only makes **SE/VCV** (and hence statistical inference) unreliable — the coefficient $b$ itself is not affected at all.
> This is why the "solution" for heteroskedasticity (section 9) only needs to fix the SE formula, **not** re-estimate the coefficients with a different method.

## Formal detection: the Breusch-Pagan (BP) test

### Intuition

If the error variance is truly uniform (homoskedastic), then the magnitude of the residual (measured by $e^2$, an estimate of the error variance at each observation) **should not** have any systematic relationship with the explanatory variables $X$.
Conversely, if $e^2$ **does** have a clear relationship with $X$ (for example $e^2$ increases as $X$ increases — exactly as in the "megaphone" plot in section 5), that is evidence of heteroskedasticity.
The idea of the BP test: **regress $e^2$ on the original explanatory variables themselves**, then test whether this auxiliary regression is statistically significant.

### Formula

Given the original regression equation $y=\beta_0+\beta_1X_1+\cdots+\beta_kX_k+e$, let $e^2$ be the estimate of the error variance. Consider the **auxiliary regression**:

$$e^2 = \alpha_0+\alpha_1X_1+\cdots+\alpha_kX_k+u$$

If homoskedastic, $e^2$ must be independent of the regressors — that is, $\alpha_1=\cdots=\alpha_k=0$. We test:

$$H_0: \alpha_1=\alpha_2=\cdots=\alpha_k=0 \qquad (\text{this is an F-test on the auxiliary regression})$$

- **Fail to reject $H_0$** → no evidence of heteroskedasticity.
- **Reject $H_0$** → evidence of heteroskedasticity.

### Numerical example — household expenditure case study

Applying this to the `expense ~ income + age_wife + age_husband + hhsize + children` model from section 4, using the `lmtest::bptest(model)` function in R (the **studentized Breusch-Pagan test** version):

$$BP = 167.46, \quad df=5, \quad \text{p-value} < 2.2\text{e-}16$$

An extremely small p-value → **strongly reject** $H_0$ (homoskedastic) → very clear evidence that the household expenditure model has heteroskedasticity — exactly as suggested by the "megaphone" plot in section 5.

## White's test

### Intuition and the difference from the BP test

The BP test only regresses $e^2$ on the $X$ variables **in their original linear form** — meaning it only catches heteroskedasticity that depends on $X$ in a simple linear way.
But if the relationship between the error variance and $X$ is more complex (nonlinear, or dependent on **interactions** between variables), the BP test may miss it.
**White's test** generalizes this idea by adding the **square** of each explanatory variable and the **cross-product** between every pair of variables into the auxiliary regression — thanks to this, White's test **does not need to assume a specific form** of heteroskedasticity in advance, making it more flexible than the BP test.

### Formula

1. Regress $e^2$ on: the original regressors $X_1,\dots,X_k$, their squares $X_1^2,\dots,X_k^2$, and the pairwise cross-products $X_iX_j$ ($i\neq j$).
2. Take $R^2$ from this auxiliary regression, multiplied by the number of observations $n$:
   where $df$ = the number of estimated coefficients in the auxiliary regression (including the original variables, squares, and cross-products).
3. Under $H_0$ (homoskedastic), the statistic $nR^2$ follows a Chi-square distribution with the corresponding $df$.

**Reject $H_0$** → evidence of heteroskedasticity; **fail to reject** → no evidence.

**Summary of the BP vs. White difference**:

| | Breusch-Pagan (BP) | White's test |
|---|---|---|
|Auxiliary regression on |$X_1,\dots,X_k$ (original linear form) |$X_1,\dots,X_k$ + squares + pairwise cross-products |
|Assumption about the form of heteroskedasticity |Requires a simple linear form in $X$ |No need to assume a specific form — more general |
|Test statistic |F-test (in theory) or Chi-square (studentized version, `bptest()` in R) | $nR^2 \sim \chi^2$ |
|Flexibility |Lower |**Higher** — catches nonlinear/interaction forms of heteroskedasticity that BP misses |

## Solution: Robust Standard Errors (White/Huber-White)

### Intuitive mechanism

The root problem from section 6 is that the formula $VCV=(X'X)^{-1}\sigma^2$ assumes $\sigma^2$ is **a single** constant common to every observation — this is exactly what A4 asserts and what heteroskedasticity denies.
The idea behind **robust standard errors** is very direct: **instead of assuming** $Var(\varepsilon)=\sigma^2I$ is constant, we **directly estimate** the error variance at *each* observation using that observation's own squared residual $\hat\varepsilon_i^2$ — with no need to know in advance what specific form the heteroskedasticity takes (increasing with income? with hhsize? in what shape?).
This is why robust SE is the most common "fix" used in practice: it **does not require knowing the correct form of heteroskedasticity** — one only needs to know that heteroskedasticity *might* be present, and the formula automatically adjusts correctly.

### Formula

The standard VCV (under A4): $VCV=(X'X)^{-1}\sigma^2$.
If we **do not** assume $Var(\varepsilon)=\sigma^2$ is constant, and instead directly estimate the matrix $Var(\varepsilon)$ — a diagonal matrix with elements $\hat\varepsilon_i^2$ (estimated from the model's own residuals):

$$Var(\varepsilon) = \begin{pmatrix}\hat\varepsilon_1^2 & 0 & \cdots & 0\\ 0 & \hat\varepsilon_2^2 & \cdots & 0\\ \vdots & & \ddots & \vdots\\ 0 & 0 & \cdots & \hat\varepsilon_n^2\end{pmatrix}$$

then the general VCV becomes:

$$VCV = (X'X)^{-1}X'\,Var(\varepsilon)\,X(X'X)^{-1}$$

This is called **White's heteroskedasticity-consistent (HC) VCV**.
SE computed from HC-VCV (the square root of the diagonal elements of HC-VCV) is called **robust standard errors** (also called White SE or Huber-White SE) — usable **regardless** of whether heteroskedasticity is present or not (if truly homoskedastic, robust SE and the usual SE will give nearly identical results), so in practice it is often used **by default**, even when one is not yet sure whether heteroskedasticity is present.

### Numerical example — comparing usual SE vs. robust SE

In R, robust SE is computed via `coeftest(model, vcov = sandwich)` (packages `lmtest` + `sandwich`). Results for the household expenditure model:

|Variable | Estimate |usual SE | SE robust |robust/usual ratio | t (robust) | p (robust) |
|---|---|---|---|---|---|---|
| (Intercept) | 0.1392 | 2.2245 | 3.4777 | ×1.56 | 0.0400 | 0.968 |
| `income` | 0.4285 | 0.0237 | 0.1323 | **×5.59** | 3.2391 | 0.0013 ** |
| `age_wife` | 0.1102 | 0.0932 | 0.1067 | ×1.15 | 1.0325 | 0.302 |
| `age_husband` | −0.0859 | 0.0935 | 0.1083 | ×1.16 | −0.7928 | 0.428 |
| `hhsize` | 0.6924 | 0.1693 | 0.2091 | ×1.24 | 3.3110 | 0.0010 ** |
| `children` | 0.0661 | 0.0309 | 0.0446 | ×1.44 | 1.4814 | **0.139** |

Two points deserve special attention:

1. **The SE of `income` increases nearly 5.6-fold** (from 0.0237 to 0.1323) — a very large change, consistent with the residuals-vs-fitted plot in section 5 showing the error variance ballooning most strongly in the high expenditure/income region.
   Even so, `income` remains statistically significant under robust SE (p=0.0013), it's just that the t-statistic drops sharply from 18.094 to 3.2391 — the evidence is still there but much "weaker" than what the (wrong) usual SE had shown.
2. **`children` completely flips the conclusion**: with the usual SE, `children` is statistically significant at the 5% level (p=0.033, marked `*`); with robust SE, the p-value rises to 0.139 — **no longer statistically significant** at any conventional $\alpha$ threshold.
   This is the clearest, most concrete example showing that **robust SE can reverse a research conclusion** — if one used only the usual SE (without checking for heteroskedasticity), the researcher would wrongly conclude that the % of children in the household has a significant effect on expenditure, when in fact there isn't sufficient evidence for that.

## Wald F-test using robust VCV

### Why a separate Wald test is needed

The "ordinary" F-statistic (computed from $RSS_r, RSS_u$ — see [[concepts/linear-regression-model]] section 8) **keeps the same value** under heteroskedasticity, because that formula relies only on RSS (the residual sum of squares), not directly on SE/VCV.
However, in practice, the F-test is often carried out via the **Wald test** (mathematically equivalent to the F-test when the standard VCV is correct), and the Wald test **uses VCV directly** in its formula — so when the standard VCV is replaced with the HC-VCV (robust), the Wald test result **will change**.

### Formula

$$H_0: R\beta=0, \qquad W = (Rb)'\big[R\cdot VCV\cdot R'\big]^{-1}(Rb) \sim \chi^2_q$$

where $R$ is the restriction matrix (specifying which coefficients are being tested), and $q$ is the number of coefficients tested jointly. The F-statistic is derived from the Wald statistic:

$$F = \frac{W}{q}$$

This approach is called the **Wald F-test**.
Because the $VCV$ in the Wald formula can be either the standard VCV or the HC-VCV (robust), **the Wald F statistic and p-value will differ** depending on which VCV is used — this is why it is always necessary to **clearly specify which VCV is being used** when reporting test results (especially important when writing a thesis).

### Numerical example — jointly testing `hhsize` and `children`

Testing $H_0:\beta_{hhsize}=\beta_{children}=0$ on the household expenditure model, using `car::linearHypothesis()`:

**Usual F-test (standard VCV):**

| | Res.Df | RSS | Df | Sum of Sq | F | Pr(>F) |
|---|---|---|---|---|---|---|
| Model 1 (restricted) | 466 | 34406 | | | | |
| Model 2 (unrestricted) | 464 | 32689 | 2 | 1716.6 | **12.183** | **6.97e-06 \*\*\*** |

**Wald F-test with robust VCV (`white.adjust = "hc1"`):**

| | Res.Df | Df | F | Pr(>F) |
|---|---|---|---|---|
| Model 1 (restricted) | 466 | | | |
| Model 2 (unrestricted) | 464 | 2 | **11.274** | **1.655e-05 \*\*\*** |

Observation: the F-statistic changes from 12.183 to 11.274, the p-value changes from 6.97e-06 to 1.655e-05 — **two clearly different numbers**, exactly as theory predicts.
In this particular case, **the final conclusion does not change** (both reject $H_0$ at any conventional $\alpha$ threshold — both carry `***`) — but this is only a **coincidence of this particular dataset**, not a general rule.
With `children` in section 9.3, we already saw a clear case where switching the VCV **did** change the conclusion (from significant to not significant) — so one cannot assume in advance that "using robust VCV probably just changes the numbers, not the conclusion".

## Exam traps

1. **Concluding that the OLS coefficient is biased due to heteroskedasticity — WRONG.**
   This is the most common trap in the whole topic (see section 6, the warning box).
   Heteroskedasticity only makes SE/VCV/statistical inference unreliable; the coefficient $b$ remains **unbiased and consistent** because this property depends only on A1–A3, not on A4.
2. **Confusing the loss of "Best" (efficiency) with the loss of "Unbiased"** due to heteroskedasticity — these are two different concepts within BLUE.
   Heteroskedasticity makes OLS lose the *Best* property (no longer the most efficient), but it still keeps *Linear* and *Unbiased*.
3. **High or low pairwise correlation in the correlation matrix has nothing to do with heteroskedasticity** — that is a diagnostic of [[concepts/multicollinearity]] (affecting A2/full rank), a problem entirely independent from heteroskedasticity (affecting A4).
4. **Forgetting that the "raw" F-statistic (based on RSS) usually does not change under heteroskedasticity, but when the F-test is carried out via the Wald test (the common approach in practice), the statistic and p-value CAN change** when switching from the standard VCV to a robust VCV — see the numerical example in section 10.3.
5. **Treating the BP test and White's test as the same thing** — the BP test uses a simple linear auxiliary regression on the original $X$, while White's test is more general (adding squares and cross-products), not requiring a specific form of heteroskedasticity to be assumed in advance.
6. **Neglecting to check which type of VCV is being used** when reading/reporting t-test or F-test results — because the two types of VCV (usual vs. robust) can lead to different conclusions (for example `children` in section 9.3: statistically significant with the usual SE, not significant with robust SE) — one must always state clearly which type of SE/VCV is being used.
7. **Assuming robust SE is always larger than the usual SE** — in theory, robust SE can be larger or smaller than the usual SE depending on the specific form of heteroskedasticity in the data; there is no rule that "robust SE always increases".
   (In the example in section 9.3, every coefficient has a robust SE larger than the usual SE, but this is a feature of this particular dataset, not a general theorem.)
8. **Treating "using robust SE" as a substitute for choosing the correct functional form or checking for outliers** — robust SE only fixes the SE formula, it cannot fix the model if the heteroskedasticity actually originates from a wrong functional form or outliers (section 3) — in those cases, one should consider fixing the model before merely "patching" it with robust SE.

## Connections to the rest of the course

- A violation of **A4 (Homoskedasticity)** from [[concepts/linear-regression-model]] — see sections 4 and 6 of that page to understand where A4 sits within the full A1–A5 "rules of the game" for OLS.
- **The same illustrative dataset** (2020 Ho Chi Minh City household expenditure survey) as [[concepts/multicollinearity]], but **two entirely independent issues**: multicollinearity affects A2 (full rank)/efficiency through correlation among the explanatory variables; heteroskedasticity affects A4/the reliability of SE — a model can suffer from both, either one, or neither, independently of each other.
- [[concepts/fixed-random-effects-model]] (Topic 12, panel data) extends the concept of heteroskedasticity to the panel data setting (heteroskedasticity **across panels/groups**, typically denoted A4a/A4b/A4c in the panel data slides) — the same root logic (non-uniform error variance) but applied along the "across cross-sectional units" dimension instead of "across observations" as on this page.
- The **robust standard errors** technique here is the foundation for "cluster-robust SE" techniques that will reappear in panel data — the same philosophy: no need to know the exact form of the error variance, just estimate it directly from the data.

## Real-world application references

Three recent papers illustrating heteroskedasticity in real-world economic research (Lecture 4 syllabus):

- Li, W., & He, W. (2024). Revenue-increasing effect of rural e-commerce: A perspective of farmers' market integration and employment growth. *Economic Analysis and Policy*, 81, 482-493. https://doi.org/10.1016/j.eap.2023.12.015
- Zhou, Y., & Shi, X. (2025). How Does Digital Technology Adoption Affect Corporate Employment? Evidence from China. *Economic Modelling*, 107045. https://doi.org/10.1016/j.econmod.2025.107045
- Tang, Y., Sun, Y., & He, Z. (2025). Air pollution and firms' robot adoption: Evidence from China. *Economic Modelling*, 143, 106957. https://doi.org/10.1016/j.econmod.2024.106957
