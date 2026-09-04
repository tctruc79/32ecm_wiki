---
title: "Lecture 12: Count Data Models (Poisson, Negative Binomial, ZINB)"
type: concept
status: mature
tags: [count-data, poisson, negative-binomial, zero-inflated, limited-dependent-variable]
sources: ["[[sources/slides-10-count-data-models]]"]
related: ["[[concepts/binary-response-models]]", "[[concepts/linear-regression-model]]"]
lecture: 12
assignment: []
updated: 2026-09-04
---

> **How to read this page**: Topic 10 continues the **Models for Limited Dependent Variables** thread opened in [[concepts/binary-response-models]] (Topic 7) — same Maximum Likelihood framework, same logic of "using a nonlinear link function because the nature of the dependent variable rules out a direct linear model".
> The one difference: in Topic 7 the dependent variable is binary (0/1) — "did it happen or not"; in Topic 10 the dependent variable is a **count** (0, 1, 2, 3, …) — "how many times did it happen".

**Lecture 12** in the syllabus (CO Topic 10) — no dedicated assignment yet.
> The example data running through this page is the **same COVID-19 vaccine survey** used in Topic 7 (377 respondents in Ho Chi Minh City), only swapping the dependent variable from `dself` (binary — whether the individual decided to get vaccinated) to `dhh` (count — the number of vaccine doses purchased for the members of the household).
> This is a direct illustration of the model-choice principle: **choose according to the nature of the dependent variable, not out of habit or whatever data happens to be available**.

## Why do we need a separate family of models for "count data"?

### What is count data?

**Count data** is a dependent variable that measures **the number of times an event occurs** within a given time period/unit of observation — always a **non-negative integer**:

$$y = 0, 1, 2, \dots, K$$

The original slide lists the classic examples in applied econometrics:

- The number of takeover bids a target firm receives.
- The number of unpaid credit installments.
- The number of accidents.
- The number of prepaid mortgage loans.

In the example running through this page (section 4): `dhh` — the number of COVID-19 vaccine doses a household decides to purchase for its members. What all these examples share: this is **the number of events occurring within a given time period**, not a continuous quantity that can be measured to any degree of precision.

### Why is OLS not appropriate?

OLS ([[concepts/linear-regression-model]]) implicitly assumes that $y$ is continuous, able to take any real value, with normally distributed errors and constant variance (A4, A5). All three implicit assumptions are "broken" by count data:

1. **Predictions can be negative or non-integer**: $\hat y_i = Xb$ in OLS is an unbounded linear function — nothing stops it from producing a result like $\hat y = -2.7$. For a count variable, "number of vaccines purchased = −2.7" is meaningless in practice.
2. **The normal distribution does not match small integers**: when most observations cluster at small values (0, 1, 2, 3…) with many observations at zero, the actual distribution's shape is right-skewed and discrete — quite unlike the symmetric, continuous bell curve that OLS/A5 assumes.
3. **Variance increases with the mean following a specific structure**: for most count data, an observation with a higher expected count also tends to fluctuate more around that expectation. This is not random heteroskedasticity as in [[concepts/heteroskedasticity]], but a **structural regularity** tied directly to the nature of counts — and this very regularity is what defines the Poisson distribution in section 2.

## The Poisson distribution — foundation

### Intuition

The **Poisson distribution** describes the probability that an event occurs exactly $k$ times within a given time period, given that the event's **mean rate** is $\lambda$:

$$Pr(y=k)=\frac{e^{-\lambda}\lambda^k}{k!}, \qquad \lambda\ge0$$

The entire Poisson distribution has only **one single parameter** $\lambda$ — and this parameter plays a dual role, serving as both the **mean** and the **variance**:

$$E[Y]=Var[Y]=\lambda$$

### Equidispersion — the "mean = variance" property

This is the **single most important, most defining feature of Poisson**, called **equidispersion**. Intuition: if $\lambda$ is small (a rare event, e.g. occurring once on average), Poisson simultaneously predicts that the fluctuation around that number is also small. If $\lambda$ is large (a common event, e.g. 100 times on average), Poisson predicts a correspondingly large fluctuation — **variance always grows at exactly the same pace as the mean, no faster, no slower**. This is precisely why the Poisson distribution solves problem #3 from section 1.2 (variance tied to the mean in a structured way) — but it is also its **core weakness**, which will be exploited in section 6.

**Why is equidispersion often violated in practice?** Because it is a very tight assumption: it requires *every* individual/unit with the same value of $X$ to have **exactly the same** $\lambda$ — with no discrepancy other than what $X$ explains. In reality there is always **unobserved heterogeneity** between individuals: two households identical on every $X$ variable in the model (income, household size, age…) can still have different tendencies to purchase vaccines for reasons that are not measured (trust in healthcare, degree of risk aversion, household-specific information…). This heterogeneity makes the *actual* variance of $y$ larger than what Poisson predicts at the same $\lambda$ — this is exactly the economic mechanism behind **overdispersion** (section 6).

## Modeling: the Poisson Model

To bring in explanatory variables $X$, we model $\lambda$ as a function of $X$:

$$E(y_i|X)=\lambda=e^{X_i\beta}$$

The exponential form $e^{X_i\beta}$ (rather than $X_i\beta$ directly) is used to guarantee $\lambda>0$ for **every** value of $X_i\beta$ (including negative ones) — the same logic of using a nonlinear link function to keep the predicted quantity within its valid domain, just as Logit/Probit keep probability within $[0,1]$ (see [[concepts/binary-response-models]]).

$$Pr(y=k)=\frac{e^{-\lambda}\lambda^k}{k!}=\frac{e^{-e^{X_i\beta}}\big(e^{X_i\beta}\big)^k}{k!}$$

**Log-likelihood function**:

$$\log L=\sum_{i=1}^N\Big[-e^{X_i\beta}+y_iX_i\beta-\log(y_i!)\Big]$$

**Estimation**: Maximum Likelihood (ML) — there is no closed-form solution like OLS ($b=(X'X)^{-1}X'y$); it requires numerical optimization, exactly like Logit/Probit.

### Marginal effect

$$\frac{\partial E(y_i|X)}{\partial X_i}=e^{X_i\beta}\cdot\beta=\lambda\cdot\beta$$

Exactly the same logic as Logit/Probit: the marginal effect **is not the constant** $\beta$ — it is proportional to the expected value $\lambda$ itself at the point being considered. Two important consequences:

- The marginal effect of $X$ on $y$ is **larger** for observations that already have a high $\lambda$, and **smaller** for observations with a low $\lambda$ — the same $\beta$ produces different absolute impacts depending on the observation's profile.
- One must choose to report the marginal effect at a specific point — **marginal effects at the mean (MEM)** or **average marginal effects (AME)** — see the numerical example in section 9.2.

## Illustrative dataset: COVID-19 vaccine demand (household count)

**Context**: demand for a hypothetical COVID-19 vaccine. Data: 377 respondents in Ho Chi Minh City (data file `EMP4.dta`) — **exactly the dataset used in Topic 7** ([[concepts/binary-response-models]]), only the dependent variable changes.

|Variable |Meaning |
|---|---|
| `dhh` |**Dependent variable (count)**: number of COVID-19 vaccine doses purchased for household members |
| `efficacy80` |1 = vaccine efficacy 80%, 0 = 50% |
| `duration3` |1 = duration of effect 3 years, 0 = 1 year |
| `priceUS` |Vaccine price (USD/2 doses) |
| `pbenefit` |1 = respondent was given information about the externality of vaccination |
| `hhincomeUS` |Total monthly household income (USD/month) |
| `hhsize` |Household size (number of members) |
| `age` |Respondent's age (years) |
| `male` |Gender, 1 = male, 0 = female |
| `risk` (ordinal) |Perceived risk of COVID-19 infection: "Very unlikely", "Unlikely", "Neither", "Likely", "Very likely" — converted into 4 dummies (`unlikely`, `neither`, `likely`, `verylikely`), with base group "Very unlikely" |

The example here reuses **exactly** the same vaccine survey as [[concepts/binary-response-models]] — only swapping the dependent variable from `dself` (binary, individual decision to get vaccinated or not) to `dhh` (count, number of doses purchased for the whole household): the same survey, two different research questions requiring two different model families.

### Descriptive statistics — and an "early warning" signal

|Variable | Mean | SD | Min | Max |
|---|---|---|---|---|
| `dhh` | 4.13 | 2.80 | 0 | 24 |
| `hhsize` | 4.69 | 2.51 | 1 | 25 |
| `age` | 43.32 | 14.00 | 18 | 86 |
| `priceUS` | 18.38 | 13.72 | 4.33 | 43.29 |
| `hhincomeUS` | 949.91 | 790.36 | 108.23 | 3787.88 |
| `pbenefit`, `efficacy80`, `duration3` | ≈0.49–0.50 | ≈0.50 | 0 | 1 |
| `male` | 0.32 | 0.47 | 0 | 1 |

Detailed distribution of `dhh` (n=377): 0→73, 1→1, 2→15, 3→35, 4→74, 5→82, 6→47, 7→16, 8→14, 9→10, 10→4, 11→4, 12→1, 24→1 (one clear outlier at 24). The histogram in the slide shows the shape **typical right-skew of count data**: the bulk of observations concentrate at 0–9, with a long, thin right tail.

Distribution of `risk` (n=377): Very unlikely 87, Unlikely 109, Neither 129, Likely 42, Very likely 10.

**An early warning signal, computable right here, before running any model**: $SD(dhh)=2.80 \Rightarrow Var(dhh)=2.80^2=7.84$, while $Mean(dhh)=4.13$. The ratio

$$\frac{Var(dhh)}{Mean(dhh)}=\frac{7.84}{4.13}\approx1.90$$

If Poisson holds (equidispersion), this ratio should be approximately 1. The figure ≈1.90 — raw variance nearly **double** the raw mean — is an early qualitative sign that this data is likely subject to **overdispersion**, before any formal test is needed (section 6.2). This is an illustrative calculation derived from the slide's descriptive statistics, not a figure the slide computes directly — but it is a sanity check worth doing as a habit before estimating a Poisson model.

## Estimating the Poisson model on the vaccine data

```r
poisson = glm(dhh ~ efficacy80+duration3+priceUS+pbenefit+hhincomeUS
              +hhsize+age+male+unlikely+neither+likely+verylikely,
              data=data, family="poisson")
```

|Variable | $\hat\beta$ | SE | p-value |
|---|---|---|---|
| (Intercept) | 1.401 | 0.1264 | <2e-16 *** |
| `efficacy80` | 0.04788 | 0.05161 | 0.354 |
| `duration3` | −0.03719 | 0.05146 | 0.470 |
| `priceUS` | −0.007833 | 0.001980 | 7.61e-05 *** |
| `pbenefit` | 0.08713 | 0.05117 | 0.089 . |
| `hhincomeUS` | 0.0001133 | 0.00003055 | 0.000207 *** |
| `hhsize` | 0.06796 | 0.007993 | <2e-16 *** |
| `age` | −0.009329 | 0.001905 | 9.75e-07 *** |
| `male` | −0.08896 | 0.05581 | 0.111 |
| `unlikely` | 0.06480 | 0.07301 | 0.375 |
| `neither` | 0.1073 | 0.07072 | 0.129 |
| `likely` | 0.05306 | 0.09525 | 0.578 |
| `verylikely` | 0.4176 | 0.1404 | 0.00293 ** |

Null deviance 906.53 (df=376); Residual deviance 742.67 (df=364); AIC 1813.1.

**Overall significance** ($H_0$: all slope coefficients = 0), via a deviance-based test: `1-pchisq(poisson$null.deviance-poisson$deviance, poisson$df.null-poisson$df.residual)` = **0** (rounded below computer precision, i.e. an extremely small p-value) → strongly reject $H_0$, the explanatory variables are jointly statistically significant.

**Test for joint significance** of the group of 4 `risk` dummies (Wald test, `Terms=10:13`): $X^2=9.6$, $df=4$, $p=0.048$ → reject $H_0$ at the 5% level (but very close to the threshold — this will be the crux of section 8.2).

## Overdispersion & Underdispersion — intuition

### When Poisson is "wrong"

Because Poisson forces $Var(y)=E(y)$, two kinds of violation can occur:

- **Overdispersion**: variance grows **faster** than the mean ($Var>Mean$) — **much more common** in practice. The typical mechanism: unobserved heterogeneity between individuals (section 2.2) — some households tend to "buy a lot of vaccine" in general (for unmeasured reasons), others tend to "buy little" in general; this hidden stratification makes the actual variation of $y$ larger than Poisson predicts. Another common mechanism: **excess zeros** (far more zero observations than predicted) — discussed in detail in section 10.
- **Underdispersion**: variance grows **slower** than the mean ($Var<Mean$) — noticeably less common. It usually occurs when there is a natural *regulating* mechanism that keeps counts more stable around the mean than pure randomness would — e.g. the number of buses departing per hour on a fixed schedule fluctuates much less than a pure Poisson process would, because the schedule "holds back" the variation.

### Formal test

```r
AER::dispersiontest(poisson)
```

Result: $z=3.3973$, $p=0.0003403$, $H_a$: "true dispersion is greater than 1", estimated dispersion $=1.366071$.

→ Strongly reject $H_0$ (equidispersion) at a very high significance level, confirming **overdispersion** — consistent with the qualitative signal already seen in section 4.1 (raw $Var/Mean$ ratio ≈1.90; the 1.366 figure here is a dispersion estimate *based on the fitted model* — the two numbers are conceptually related but not the same calculation, so they are not expected to match exactly).

**Direct consequence**: when overdispersion is present but Poisson is still used, the Poisson Standard Error is **underestimated** — because the Poisson SE formula implicitly assumes $Var=Mean$ holds. A smaller-than-true SE → a larger-than-true t/z-statistic → a smaller-than-true p-value → **an easy false conclusion of statistical significance when in fact there is none**. Section 8.2 illustrates this consequence with concrete numbers.

## Negative Binomial (NB) Model — relaxing equidispersion

### Intuition: how does NB "relax" the Poisson assumption?

Poisson forces every observation with the same $X$ to have exactly one $\lambda$, leaving no room for unobserved individual heterogeneity. **Negative Binomial (NB)** solves precisely that problem: it adds a **dispersion parameter** $\alpha \ge 0$, allowing variance to grow **faster** than the mean by an amount proportional to $\alpha$ — in essence, $\alpha$ measures the amount of unobserved heterogeneity remaining after controlling for the $X$ variables in the model. The larger $\alpha$ is, the more heterogeneity there is, and the more severe the overdispersion.

### Formula

$$Pr(y=k)=\frac{\Gamma(k+\theta)}{\Gamma(k+1)\Gamma(\theta)}p^\theta(1-p)^k, \qquad \theta=\frac{1}{\alpha},\; p=\frac{1}{1+\alpha\mu}$$

where $\Gamma(\cdot)$ is the Gamma function: for a non-negative integer $y$, $\Gamma(y)=(y-1)!$; more generally, $\Gamma(y)=\int_0^{+\infty}x^{y-1}e^{-x}dx$.

The mean is **unchanged** relative to Poisson: $E(y_i|X)=\lambda=e^{X_i\beta}$. But the **variance**:

$$Var(y_i|X)=\lambda+\alpha\lambda^2$$

### Why NB "nests" Poisson at $\alpha=0$

Looking at the variance formula: if $\alpha=0$, then $Var(y_i|X)=\lambda$ — **exactly equal to** the Poisson equidispersion assumption. In other words, **Poisson is a special case of NB, when $\alpha=0$** — this is called a **nesting** relationship (Poisson is "nested inside" NB as a restriction). The most practically important consequence: **testing "NB or Poisson" is exactly the statistical test $H_0:\alpha=0$** — if $H_0$ can be rejected, there is evidence NB fits better than Poisson (section 8.3).

## Estimating NB on the vaccine data + comparison with Poisson

```r
negbin = glm.nb(dhh ~ efficacy80+duration3+priceUS+pbenefit+hhincomeUS
                +hhsize+age+male+unlikely+neither+likely+verylikely,
                data=data)
```

(`init.theta = 6.680685757`, `link = log`)

|Variable | $\hat\beta$ (NB) | SE (NB) | p-value |SE compared to Poisson |
|---|---|---|---|---|
| (Intercept) | 1.361 | 0.1634 | <2e-16 *** | — |
| `efficacy80` | 0.05406 | 0.06618 | 0.414 | — |
| `duration3` | −0.03044 | 0.06606 | 0.645 | — |
| `priceUS` | −0.007658 | 0.002482 | 0.00204 ** |SE is **1.25×** Poisson |
| `pbenefit` | 0.08533 | 0.06558 | 0.193 | — |
| `hhincomeUS` | 0.0001039 | 0.00004166 | 0.01264 * |SE is **1.36×** Poisson |
| `hhsize` | 0.07759 | 0.01199 | 9.83e-11 *** |SE is **1.50×** Poisson |
| `age` | −0.009695 | 0.002433 | 6.73e-05 *** |SE is **1.28×** Poisson |
| `male` | −0.0860 | 0.07123 | 0.227 | — |
| `unlikely` | 0.05616 | 0.09340 | 0.548 |SE is **1.28×** Poisson |
| `neither` | 0.1206 | 0.09002 | 0.180 |SE is **1.27×** Poisson |
| `likely` | 0.1003 | 0.1209 | 0.407 |SE is **1.27×** Poisson |
| `verylikely` | 0.4376 | 0.1931 | 0.02348 * |SE is **1.38×** Poisson |

**The key point from the table above**: moving from Poisson to NB, the coefficients $\hat\beta$ barely change — but **SE consistently increases by 25–50%** across every variable. This is the direct, quantitative consequence of the overdispersion discussed in section 6.2: Poisson's SE is systematically underestimated.

### Overall significance (NB)

`1-pchisq(negbin$null.deviance-negbin$deviance, negbin$df.null-negbin$df.residual)` = $7.771561\times10^{-16}$ → strongly reject $H_0$ (all slope coefficients = 0).

### Test for joint significance — a conclusion completely reversed from Poisson

This is the single most important illustration on this entire page. It re-tests exactly the same question asked under Poisson (section 5) — whether the group of 4 `risk` dummies is jointly significant — but this time using NB:

- **LR test** (`lmtest::lrtest(negbin, c("unlikely","neither","likely","verylikely"))`): the full model (df=14, logLik=−877.77) versus the model dropping the 4 risk dummies (df=10, logLik=−880.71): $\chi^2=5.8759$, $df=4$, $p=0.2086$.
- **Wald test** (`aod::wald.test(..., Terms=10:13)`): $X^2=6.0$, $df=4$, $p=0.2$.

|Model |Statistic | df | p-value |Conclusion at $\alpha=5\%$ |
|---|---|---|---|---|
| Poisson (Wald) | $X^2=9.6$ | 4 | **0.048** |**Reject $H_0$** (risk is significant) |
| NB (LR) | $\chi^2=5.8759$ | 4 | **0.2086** |**Fail to reject $H_0$** (risk is no longer significant) |
| NB (Wald) | $X^2=6.0$ | 4 | **0.2** |**Fail to reject $H_0$** |

**The same research question, the same dataset — two models produce two opposite conclusions at the 5% significance level.** This is exactly the consequence warned about in section 6.2: Poisson's SE is underestimated because it ignores overdispersion, causing the Poisson test to "see" statistical significance that does not actually exist once the SE is correctly adjusted via NB.

### Formal test of NB versus Poisson

$$H_0: \alpha=0 \text{ (Poisson is sufficient)} \quad\text{vs.}\quad H_a: \alpha>0 \text{ (NB is needed)}$$

```r
lrtest(poisson, negbin)
```

Model 1 (Poisson, df=13, logLik=−893.57) versus Model 2 (NB, df=14, logLik=−877.77): $\chi^2=31.605$, $df=1$, $p=1.889\times10^{-8}$ *** → strongly reject $H_0:\alpha=0$ → **NB fits better than Poisson with very high statistical significance**, reconfirming the conclusion from `dispersiontest` (section 6.2) and from the SE comparison table in section 8.

## Interpreting coefficients: from the log scale to the Incidence Rate Ratio (IRR)

### Why $\hat\beta$ cannot be read directly

Because the model uses a log link ($\log\lambda = X\beta$, equivalent to $\lambda=e^{X\beta}$), the coefficient $\hat\beta_j$ measures **the change in the log of the expected count**, not a direct change in the count itself — entirely analogous to how a Logit coefficient measures log-odds rather than probability directly (see [[concepts/binary-response-models]]). To interpret it in an easily understandable unit, the coefficient must be exponentiated to get the **Incidence Rate Ratio (IRR)**:

$$IRR_j = e^{\hat\beta_j}$$

**Rule for reading IRR**:

- $IRR_j > 1$: increasing $X_j$ by 1 unit raises the expected count $\lambda$ by $(IRR_j-1)\times100\%$, holding other variables fixed.
- $IRR_j < 1$: increasing $X_j$ by 1 unit lowers $\lambda$ by $(1-IRR_j)\times100\%$.
- $IRR_j = 1$ ($\hat\beta_j=0$): $X_j$ has no effect.

### Numerical example — IRR from the NB model

|Variable | $\hat\beta$ (NB) | $IRR=e^{\hat\beta}$ |Interpretation |
|---|---|---|---|
| `priceUS` | −0.007658 | 0.9924 |Vaccine price increases by 1 USD → expected number of vaccines purchased **falls by 0.76%**, holding other variables fixed |
| `hhincomeUS` | 0.0001039 | 1.00010 |Household income increases by 1 USD → expected number of vaccines purchased **rises by 0.010%** (≈1.04% if income rises by 100 USD) |
| `hhsize` | 0.07759 | 1.0807 |Household gains 1 additional member → expected number of vaccines purchased **rises by 8.07%** |
| `age` | −0.009695 | 0.9904 |Age increases by 1 year → expected number of vaccines purchased **falls by 0.96%** |
|`verylikely` (relative to base "very unlikely") | 0.4376 | 1.5490 |A person who perceives the risk of infection as "very likely" has an expected vaccine purchase **54.9% higher** than someone who perceives it as "very unlikely" (base), holding other variables fixed |

Because `risk` is not explicitly labeled causal/non-causal by the slide the way the Forest/Storm dataset is in [[concepts/linear-regression-model]], the interpretation above uses only associational language ("associated with", "higher than") — **no causal claim is made** when the source does not clearly confirm a causal mechanism.

### Marginal effects on the count scale (supplementing IRR, not replacing it)

IRR tells us the **relative change (%)**; to know the **absolute** change in the count unit itself (number of vaccines), we need the marginal effect as in section 3.1, computed via `negbinmfx()` — and just as with Logit/Probit, one must choose MEM or AME:

|Variable |MEM: dF/dx (at the mean value) |AME: dF/dx (average of marginal effects) |
|---|---|---|
| `priceUS` | −0.0301 (p=0.00326 **) | −0.0318 (p=0.00506 **) |
| `hhincomeUS` | 0.000409 (p=0.01294 *) | 0.000431 (p=0.01562 *) |
| `hhsize` | 0.3054 (p=6.49e-06 ***) | 0.3220 (p=1.21e-06 ***) |
| `age` | −0.0382 (p=6.57e-06 ***) | −0.0402 (p=1.71e-05 ***) |
| `verylikely` |2.1355 (p=0.007715 **, discrete change 0→1) | 2.2458 (p=0.00782 **) |

Reading the `hhsize` example: at the average observation (MEM), adding 1 household member makes the expected number of vaccines purchased **rise by about 0.305 doses**, holding other variables at their sample mean — an absolute figure that supplements the relative figure of 8.07% in section 9.2 (the two numbers are conceptually consistent: 0.305 is approximately $\lambda \times (\text{IRR}-1)$ at the sample mean $\lambda$ ≈4.13, since $4.13\times0.0807\approx0.333$ — close but not an exact match because MEM/AME are computed differently from the simple analytic derivative formula).

### An easy point of confusion: `predict(..., type="link")` is not the expected count

The slide illustrates computing a "partial effect at a specific data point" by increasing `hhincomeUS` from 700 to 701 (holding other variables fixed) and taking the difference between the two predictions:

```r
nbpred1 = predict(negbin, newdata=point1, type="link")
nbpred2 = predict(negbin, newdata=point2, type="link")
nbpred2 - nbpred1
# = 0.0001038968
```

This figure $0.0001038968$ is **exactly equal to** $\hat\beta_{hhincomeUS}=0.0001039$ (rounded) — this is algebraically obvious: `type="link"` returns $X\beta$ (the log scale of $\lambda$), and because the model is linear in $X$ on the log scale, the difference in $X\beta$ when $X_j$ increases by exactly 1 unit is always **exactly equal to** $\hat\beta_j$ — there is no need to run `predict()` to know this number in advance. Similarly, the example of changing `risk` from "likely" to "very likely" gives a difference $\approx0.3374$, closely matching $\hat\beta_{verylikely}-\hat\beta_{likely}=0.4376-0.1003=0.3373$.

## Zero-Inflated Negative Binomial (ZINB) — the "excess zeros" problem

### Intuition: when are there "too many zeros"?

Right from the descriptive statistics (section 4.1): 73/377 ≈ **19.4%** of households purchase **0** vaccines. If Poisson with $\lambda=4.13$ (sample mean) held, the probability of observing $y=0$ would only be:

$$Pr(y=0)=\frac{e^{-4.13}(4.13)^0}{0!}=e^{-4.13}\approx0.0161 \;(\approx1.6\%)$$

The **actually observed** zero rate (≈19.4%) is **far larger** than the Poisson-predicted rate (≈1.6%) at the same mean — this is a direct illustration of the **excess zeros** problem (far more zero observations than a standard count distribution predicts). *(This is an illustrative calculation derived from the slide's descriptive data — the slide itself does not present this comparison directly, but it uses exactly the Poisson formula given by the slide in section 2 and the sample mean from section 4.1.)*

**Economic interpretation of excess zeros**: there may exist **two latent groups** in the population that the observed $X$ variables cannot fully distinguish:

1. The "never" group (always-zero / structural zero): households that will *always* purchase 0 vaccines by nature — e.g. they completely distrust vaccines, or already have enough vaccine from another source. For this group, $y=0$ is not because they "happened not to need to buy" but because they **are never in this market** at all.
2. The "potential buyer" group (count process / at-risk group): households that *could* purchase vaccine (the quantity follows a count process, e.g. NB), but may happen to purchase exactly 0 doses at this particular survey moment (e.g. because of a high price, low income at that time…) without it meaning they "never buy".

The original slide calls this a case of **"too many zeros, or two separate processes"**.

### Two-part structure

$$\lambda_i^{zinf} = \pi_i\times\{y_i=0\} + (1-\pi_i)\times\lambda_i$$

where:

- $\pi_i$: the probability that $y_i$ is a "structural zero", modeled using **logit**: $\pi_i=\dfrac{1}{1+e^{-\gamma Z}}$.
- $\lambda_i=e^{\beta X}$: the expectation coming from the **count process** (count process — the NB model).

**Key point**: in ZINB, the probability of observing $y=0$ comes from **two sources** added together:

1. The "always zero" group — probability $\pi_i$.
2. The group belonging to the count process but happening to yield a 0 outcome — probability $(1-\pi_i)\times Pr_{NB}(y=0)$.

The model simultaneously estimates three sets of parameters: $\beta$ (the count equation), $\gamma$ (the zero-inflation equation), and $\alpha$ (or $\theta=1/\alpha$, the dispersion parameter of the NB part).

**ZINB has two simultaneous equations**:

$$\pi_i = \frac{1}{1+e^{-\gamma Z}} \qquad \lambda_i = e^{\beta X}$$

## Estimating ZINB on the vaccine data

```r
library(pscl)
zinb = zeroinfl(dhh ~ efficacy80+duration3+priceUS+pbenefit+hhincomeUS+hhsize+age+male
                 | hhsize+age+male, data=data, dist="negbin")
```

**Count model coefficients (NB with log link)**:

|Variable | $\hat\beta$ | SE | p-value |
|---|---|---|---|
| (Intercept) | 1.234 | 0.1112 | <2e-16 *** |
| `efficacy80` | 0.03932 | 0.05282 | 0.4566 |
| `duration3` | 0.02925 | 0.05294 | 0.5806 |
| `priceUS` | −0.0007768 | 0.002039 | 0.7033 |
| `pbenefit` | 0.01382 | 0.05219 | 0.7911 |
| `hhincomeUS` | 0.00003168 | 0.00003750 | 0.3982 |
| `hhsize` | 0.09846 | 0.01958 | 4.94e-07 *** |
| `age` | −0.003792 | 0.002083 | 0.0687 . |
| `male` | 0.002423 | 0.06371 | 0.9697 |

**Zero-inflation model coefficients (binomial, logit link)**:

|Variable | $\hat\gamma$ | SE | p-value |
|---|---|---|---|
| (Intercept) | −3.39078 | 0.57675 | 4.13e-09 *** |
| `hhsize` | 0.04892 | 0.05009 | 0.32881 |
| `age` | 0.03318 | 0.01034 | 0.00134 ** |
| `male` | 0.45359 | 0.28784 | 0.11507 |

$\theta = 8{,}841{,}154.89$ (log-likelihood = −747.4, df=14).

### Interpreting the zero-inflation part

Because $\pi_i$ uses a logit link, the coefficient $\hat\gamma_j$ has the same meaning **exactly as a Logit coefficient** ([[concepts/binary-response-models]]): it only tells us the **direction** of the effect on the log-odds of belonging to the "always zero" group, **not directly the magnitude** — to get the magnitude one must compute a marginal effect or the odds ratio $e^{\hat\gamma}$, analogous to IRR but applied to a probability rather than a count.

In the results above, only `age` is statistically significant ($\hat\gamma=0.03318$, $p=0.00134$): the higher the age, the higher the log-odds of belonging to the "never buys vaccine for the household" group — i.e. older respondents tend more toward the "structural zero" group, holding `hhsize` and `male` fixed. `hhsize` and `male` are not statistically significant in this zero-inflation part.

### An interesting observation: what does an extremely large $\theta$ mean?

Comparing the two $\theta$ values (and $\alpha=1/\theta$) between the plain NB (section 8) and ZINB:

|Model | $\theta$ | $\alpha=1/\theta$ |
|---|---|---|
|NB (section 8, without separating zero-inflation) | 6.6807 | 0.1497 |
|ZINB — count part | 8,841,154.89 | ≈0.0000001 (≈0) |

$\alpha\approx0$ in ZINB is nearly equivalent to **pure Poisson** in the count part (recall section 7.3: $\alpha=0\Leftrightarrow$ NB collapses to Poisson). Intuitive interpretation: when the plain NB model (section 8) has to "carry" all the overdispersion — including the portion generated by excess zeros — into a single parameter $\alpha$, the estimated $\alpha$ turns out fairly large (0.1497). But once the "always zero" part is separated out into its own logit equation (ZINB), the remaining overdispersion in the count process nearly vanishes ($\alpha\to0$). This suggests that most of the overdispersion detected in sections 6–8 in this example **may come mainly from excess zeros**, rather than from individual heterogeneity spread evenly across all count levels. This is an observation derived from the slide's two numerical tables (not a conclusion the slide states directly), so it is presented as one way of reading the data, not a claim made by the instructor.

> Note: the slide does not present any formal test (e.g. a Vuong test) to directly compare whether NB and ZINB actually differ with statistical significance — the observation in section 11.2 is only a qualitative illustration, not a substitute for a formal test.

## Comprehensive exam traps

1. **Using Poisson without first checking for overdispersion.** If overdispersion is present, Poisson's SE is systematically underestimated, leading to wrong conclusions about statistical significance — the concrete numerical example in section 8.2: the same joint significance test of the `risk` group, Poisson gives $p=0.048$ (reject $H_0$) while NB gives $p\approx0.2$ (fail to reject) — **a completely reversed conclusion** simply from switching from Poisson to NB.
2. **Interpreting $\hat\beta$ directly as the unit change of $y$** — wrong, because the model uses a log link; the coefficient must be exponentiated to get IRR ($e^{\hat\beta}$) before it can be interpreted as a % change in the expected count (sections 9.1–9.2).
3. **Confusing ZINB with plain NB** when the data simply has many zeros due to the nature of the count distribution (e.g. a small $\lambda$ naturally generates many zeros), without evidence of a separate "structural" process (structural zero process) generating the zeros.
4. **Forgetting that the marginal effect of count models (like Logit/Probit) is not constant** — it always depends on the $X$ value being considered (because it is proportional to $\lambda$) — one must state clearly whether MEM or AME is being reported.
5. **Confusing `predict(..., type="link")` with `predict(..., type="response")`.** `type="link"` returns $X\beta$ (the log of the expected count); the difference between two predictions on this scale is simply the coefficient difference × the $X$ difference — **not** the actual impact on the expected count $\lambda$ (section 9.4).
6. **Interpreting the coefficient $\hat\gamma$ in the zero-inflation part (logit) the same way as the coefficient $\hat\beta$ in the count part (log-count).** The two parts have entirely different meanings: $\hat\gamma$ speaks to the log-odds of belonging to the "always zero" group; $\hat\beta$ speaks to the log of the expected count within the "at-risk" group. They must not be interpreted interchangeably (section 11.1).
7. **Directly comparing log-likelihood/AIC between two models that use different sets of independent variables** — as in the slide's example, ZINB drops the `risk` variable from the count part relative to the plain NB (section 11) — such a comparison is not "apples-to-apples", because the fit difference could come from the different variable sets, not necessarily from the model structure.
8. **Treating "NB fits significantly better than Poisson" (section 8.3) as conclusive evidence for a specific economic mechanism** (e.g. "definitely due to individual heterogeneity") — the test $H_0:\alpha=0$ only tells us overdispersion exists statistically, it does not automatically identify the **cause** of the overdispersion (pure individual heterogeneity, excess zeros, or both) — distinguishing between them requires trying ZINB as in sections 10–11.

## Connections with the rest of the course

Count data models share the same Maximum Likelihood framework with the whole of **Part 2: Models for Limited Dependent Variables**, opened at [[concepts/binary-response-models]] (Topic 7):

- **The same nonlinear link-function logic** to keep the predicted quantity within its valid domain: Logit/Probit keep probability within $[0,1]$; Poisson/NB keep $\lambda$ positive.
- **The same two-step coefficient-interpretation structure**: the raw coefficient only gives the *direction*; it must be transformed (odds ratio in Logit, IRR in Poisson/NB) before the *magnitude* becomes directly interpretable.
- **The same issue of a non-constant marginal effect**, and the same choice between MEM vs AME.
- **The same COVID-19 vaccine survey dataset**, only the dependent variable changes (`dself` binary in Topic 7 → `dhh` count in Topic 10) — illustrating the principle of choosing a model according to the nature of the dependent variable.

The concept of **nesting** (NB nests Poisson at $\alpha=0$, section 7.3) and the LR test based on comparing log-likelihood between the full/restricted model (sections 8.3, 8.1) reuse exactly the Likelihood Ratio test logic already built in [[concepts/binary-response-models]] — only the object being tested differs (a dispersion parameter $\alpha$ instead of a set of coefficients $\beta$).

## Real-world application references

Three recent papers illustrating count data models (Poisson, Negative Binomial) in real-world economic research (Lecture 12 syllabus):

- Meredith, N. R., Macy, A., & Meredith, A. (2022). Income elasticity of demand for tanning bed usage: evidence from survey data. *Journal of Applied Economics*, 25(1), 1156-1181. https://doi.org/10.1080/15140326.2022.2110640
- Hynes, S., O'Reilly, P., & Corless, R. (2015). An on-site versus a household survey approach to modelling the demand for recreational angling: Do welfare estimates differ? *Ecosystem Services*, 16, 136-145. https://doi.org/10.1016/j.ecoser.2015.10.013
- Xu, M., Ye, Q., Wang, X., & Wang, M. (2017). Assessing influence of online reputation on sales using a zero-inflated negative binomial model. *Procedia Computer Science*, 122, 1108-1113. https://doi.org/10.1016/j.procs.2017.11.480
