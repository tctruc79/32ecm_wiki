---
title: "Lecture 9: Binary Response Models (LPM, Logit, Probit)"
type: concept
status: mature
tags: [binary-response, logit, probit, limited-dependent-variable, marginal-effects]
sources: ["[[sources/slides-7-binary-response-models]]", "[[sources/slides-310-binary-response-models-logit-probit]]"]
related: ["[[concepts/linear-regression-model]]", "[[concepts/multinomial-logit-model]]", "[[concepts/ordinal-response-models]]"]
lecture: 9
assignment: ["Assignment 10: Binary Response Model: Logit/Probit"]
updated: 2026-09-04
---

> **How to read this page**: this is the opening page of **Part 2: Models for Limited Dependent Variables** — the rest of the course (Topic 8–11) are all variants of the ML/latent-variable framework built here.
> If [[concepts/linear-regression-model]] is the "rulebook" for continuous $y$, this page is the "rulebook" for when $y$ can only be 0 or 1.
> The theory in this lecture is illustrated with two different datasets: a COVID-19 vaccine decision dataset (with real R output) and an e-wallet dataset (mostly text/formulas, with no concrete R output).

**Lecture 9** in the syllabus (CO Topic 7) — Assignment 10: Binary Response Model: Logit/Probit.
> Every numerical example on this page is drawn from the vaccine dataset; the e-wallet dataset is used only to illustrate that the theory applies to any binary outcome.

## The original problem: when the dependent variable can only be 0 or 1

Many economic questions do not have a continuous number as the outcome, but rather a **binary choice** — yes/no, occurs/does not occur.
A series of representative examples:

- Whether a loan application is approved or not.
- Whether a borrower can repay the debt or not.
- Whether a person owns a credit card or not.
- (The running example throughout this page) Whether a person decides to get a COVID-19 vaccine or not (`dself`).
- (The example from the parallel dataset) Whether a person uses an e-wallet or not (`ewallet`).

Call this variable $y_i \in \{0,1\}$. The natural question: **why not just run OLS directly** on $y = \beta X + u$ the way [[concepts/linear-regression-model]] does?

The problem lies in the very nature of $y$. In probability theory, when $y$ is binary, its expected value **is itself a probability**:

$$E(y_i|X_i) = 1\cdot Pr(y_i=1|X_i) + 0\cdot Pr(y_i=0|X_i) = Pr(y_i=1|X_i)$$

In other words, regressing $y$ on $X$ is essentially an attempt to model $Pr(y=1|X)$ — and a probability is **always bounded within [0,1]**. But the right-hand side of a linear regression equation $X\beta$ is **unbounded** — it can range from $-\infty$ to $+\infty$ depending on the value of $X$. This is precisely the foundational contradiction that all of Part 2 of the course exists to resolve: we need a function that transforms $X\beta$ (unbounded) into a number that always lies in [0,1] (a valid probability).

The problem is formalized with a general density function:

$$Pr(Y_i=1) = F(X_i\beta), \qquad Pr(Y_i=0) = 1-F(X_i\beta)$$

$F(\cdot)$ here is called the **link function** — its job is simply to "squeeze" $X\beta$ into [0,1]. The difference between LPM, Logit, and Probit **lies purely in the choice of what function $F$ is** — this is the idea to grasp before diving into each specific model.

## Illustrative datasets

### COVID-19 vaccine dataset (used for every numerical example on this page)

A survey of 377 people in Ho Chi Minh City in 2020 (data made public by EEPSEA), asking whether they would decide to get a hypothetical COVID-19 vaccine.

|Variable |Meaning |
|---|---|
| `dself` (dep var) |1 = decides to get vaccinated for themselves |
| `efficacy80` |1 = vaccine efficacy 80%, 0 = 50% |
| `duration3` |1 = immunity duration 3 years, 0 = 1 year |
| `priceUS` (USD) |vaccine price (2 doses) |
| `pbenefit` |1 = was given information about the externality of vaccination |
|`hhincomeUS` (USD/month) |total household income |
| `hhsize` |household size |
|`age` (years) |respondent's age |
| `edu` (categorical 1–6) |education level |
| `male` | 1 = nam / 1 = male |
| `risk` (ordinal 1–5) |perceived risk of COVID-19 infection: "Very unlikely" → "Very likely" |

### E-wallet dataset (used only to illustrate the concept, no extractable R output)

|Variable |Meaning |
|---|---|
| `ewallet` (dep var) |1 = uses an e-wallet |
|`income` (million VND/month) |monthly disposable income |
|`age`, `schooling` (years) |age, years of schooling |
| `male` | 1 = nam / 1 = male |
| `risklover` |1 = self-identifies as a risk lover |
| `freq` → `weekly`, `daily` (dummy) |frequency of online shopping (base: "monthly" — less than weekly) |

The two datasets differ completely in context, but share **the same problem structure**: a 0/1 outcome to be explained by a mixed set of independent variables (continuous, dummy, categorical) — exactly the type of problem LPM/Logit/Probit are designed to handle.

## General framework: choices for $F(X\beta)$

There are 5 common choices of link function (the first 3 are the focus of the course):

|Model | $F(X_i,\beta)$ |
|---|---|
| **Linear Probability Model (LPM)** | $X_i\beta$ |
| **Logit** | $\Lambda(X_i\beta) = \dfrac{1}{1+e^{-X_i\beta}}$ |
| **Probit** | $\Phi(X_i\beta) = \displaystyle\int_{-\infty}^{X_i\beta}\phi(t)\,dt = \int_{-\infty}^{X_i\beta}\frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{1}{2}\left(\frac{t-\mu}{\sigma}\right)^2}dt$ |
| Gumbel | $e^{-e^{-X_i\beta}}$ |
| Complementary log-log | $1-e^{-e^{X_i\beta}}$ |

"And many other variants" — Gumbel/cloglog are outside this course's focus and are named here only to show that LPM/Logit/Probit are 3 out of many possible choices, not the entire universe of binary response models.

## Linear Probability Model (LPM)

### Intuition

The "easiest" way to choose $F$: set $F(X\beta)=X\beta$ — that is, **no transformation at all**, simply run an ordinary OLS regression with $y$ (0/1) as the dependent variable:

$$Pr(y_i=1) = X_i\beta = \beta_0+\beta_1X_{1i}+\cdots$$

Since $y_i=1$ coincides with $Pr(y_i=1)=1$, we can use the observed $y$ directly as the dependent variable and run OLS as usual — mechanically, nothing differs from [[concepts/linear-regression-model]]. But **an important note**: the left-hand side is fundamentally a probability, not $y$ itself — this determines how the coefficients are read (section 4.3) and is also the root of every problem LPM has.

### A visual example using the vaccine data

Suppose we estimate an LPM for `dself` on `priceUS` (holding the other variables fixed at their reference levels). Because LPM forces $Pr(dself=1)$ to be linear in price, the regression line is **a straight line**, with no inflection point and no natural bound.
If the coefficient on `priceUS` is negative and steep enough (the higher the price, the fewer people want to get vaccinated), then at a sufficiently high price (e.g. 300–500 USD, outside the observed data range but still a valid $X$ value to plug into the formula), this straight line **can perfectly well go below 0** — meaning the model "predicts" a *negative* probability of getting vaccinated, which is logically meaningless (negative probability does not exist).
Similarly, at a very low price (negative, or with control variables at extreme levels), the prediction can exceed 1. This is exactly disadvantage #1 below, and it is not a "theoretically rare" situation — it happens whenever $X$ is far enough from the central region of the sample data.

### Interpreting the coefficients

Since the left-hand side is $Pr(y=1)$, the coefficient $\beta_j$ in LPM is read exactly like an ordinary LRM: $\beta_j$ is the change in the **probability** that $y=1$ when $X_j$ increases by 1 unit, holding the other variables constant — and most importantly, **this change is constant**, independent of the starting value of $X_j$ or of any other variable. This is the point where LPM differs fundamentally from Logit/Probit (see section 9).

### The four drawbacks of LPM — and why each one is a real problem

There are exactly 4 main drawbacks; below explains **why** each one matters, not just names them:

1. **The predicted value $Pr(y=1)$ can fall outside [0,1].** This is not a cosmetic flaw — it breaks the very definition of a probability. A policymaker seeing "the probability of getting vaccinated is −8%" or "112%" cannot interpret the result, and cannot use that number for any subsequent probability calculation (expectation, simulation…).

2. **LPM assumes $Pr(y=1)$ is linearly related to $X$ regardless of the starting value of $X$.** Economically, this is often implausible: when the vaccine price is already very low (near 0 USD), an additional 1 USD barely changes anyone's decision — most people willing to get vaccinated have already "locked in" their decision. Conversely, when the price is in the range where people are still "on the fence" (probability near 50%), a 1 USD increase can sway many people's decisions. LPM forces this sensitivity to be **identical at every price level** — an unnatural assumption. (Section 9 will quantify this difference precisely with real data.)

3. **The error $\varepsilon$ has "inherently" heteroskedastic variance.** Because $y$ takes only 2 values, the residual $\varepsilon_i = y_i - X_i\beta$ also takes only 2 possible values: $1-X_i\beta$ (when $y_i=1$) or $-X_i\beta$ (when $y_i=0$). It can be shown that $Var(\varepsilon_i|X_i) = X_i\beta(1-X_i\beta)$ — this variance **always changes with $X_i$**, it is not constant, meaning LPM always violates assumption A4 (homoskedasticity) of [[concepts/linear-regression-model]]. Direct consequence: the standard errors computed from the usual OLS formula are typically wrong, and every t-test/F-test based on those SEs is **unreliable** — see [[concepts/heteroskedasticity]] for the mechanism and the fix (robust SE).

4. **Violates the assumption that $\varepsilon$ is normally distributed (A5).** Since the residual only takes the 2 discrete values above, it clearly cannot follow a continuous normal distribution. In small samples, this strips exact inference (t-test, F-test based on the t/F distribution) of its theoretical basis.

**Key point to remember**: these 4 drawbacks are why the course moves on to Logit/Probit — not because LPM is "wrong" in a mathematical sense (OLS still produces a valid $b$), but because the binary nature of $y$ causes the foundational assumptions of OLS ([[concepts/linear-regression-model]] section 4) to be violated **systematically**, not randomly.

## The Logit model

### Intuition: why use the logistic function

The core problem with LPM is using a straight line to model a quantity bounded in [0,1]. The natural solution: use a function shaped like an **S** (sigmoid) — flat near 0 when $X\beta$ is very small (very negative), flat near 1 when $X\beta$ is very large (very positive), and steepest in the middle region. The **logistic** function is a classic choice for this shape:

$$Pr(Y_i=1) = P_i = \frac{1}{1+e^{-\beta X_i}}$$

Since $-\infty < X_i\beta < +\infty$ but the exponent $e^{-\beta X_i}$ is always positive, the denominator $1+e^{-\beta X_i}$ is always greater than 1, so $P_i$ **always lies strictly within (0,1)** — never touching 0 or 1, and never going outside that range, **no matter how large or small $X\beta$ is**. This is precisely how Logit thoroughly fixes drawback #1 of LPM: not by forcibly "clipping" the predicted value to [0,1], but by choosing a function whose entire range *automatically* lies within [0,1].

### Derivation: from odds ratio to log-odds

This is the technical part needed to understand why Logit "differs" from LPM in substance, not just in graph shape. Starting from $P_i = \dfrac{1}{1+e^{-\beta X_i}}$, we have the "does not occur" probability:

$$1-P_i = \frac{e^{-\beta X_i}}{1+e^{-\beta X_i}}$$

**Odds ratio** is a concept familiar from betting: the ratio between the probability of "occurring" and the probability of "not occurring." For example, odds = 3 means "occurring" is 3 times as likely as "not occurring" ($P=0.75$, $1-P=0.25$, $0.75/0.25=3$). For Logit:

$$\frac{P_i}{1-P_i} = \frac{1/(1+e^{-\beta X_i})}{e^{-\beta X_i}/(1+e^{-\beta X_i})} = \frac{1}{e^{-\beta X_i}} = e^{\beta X_i}$$

Taking the log of both sides gives the **logit** (log-odds):

$$\ln\left(\frac{P_i}{1-P_i}\right) = \beta X_i$$

This is the core distinction: **LPM assumes $P_i$ is linear in $X_i$; Logit assumes the log-odds (not $P_i$) is linear in $X_i$**. Since $\ln(P/(1-P))$ is a nonlinear transformation of $P$, $P_i$ itself still changes nonlinearly with $X_i$ even though its logit changes linearly — this is precisely the origin of the "non-constant marginal effect" in section 9.

### Properties of the Logit model

- $P_i$ always lies within (0,1), while the logit $L_i=\ln(P_i/(1-P_i))$ ranges from $-\infty$ to $+\infty$.
- $L_i$ is a linear function of $X_i$, but $P_i$ is **not** — this is a direct consequence of the log-odds transformation.
- Interpreting the coefficient $\beta_j$: it is the change in the **log-odds ratio** when $X_j$ increases by 1 unit, holding the other variables constant; the **sign** of $\beta_j$ tells the direction of change of $P_i$ (positive → an increase in $X_j$ increases $P$; negative → the opposite) — but **$\beta_j$ itself does not tell the magnitude** of the effect on the probability. This is the biggest difference from OLS coefficients in LPM/LRM, and is the source of a very common exam trap (see section 12).
- In LPM, the marginal effect of $X_j$ is constant. In Logit, the marginal effect **changes with the value of $X$** (details + real data in section 9).

### Estimation: Maximum Likelihood (ML) — the intuitive idea

OLS cannot be applied directly to Logit because the problem is no longer "minimize the sum of squared residuals" in the linear sense. Instead, Logit/Probit use **Maximum Likelihood (ML)**.

**Intuitive idea** (no need for a full mathematical proof): for each choice of coefficient $\beta$, the model "predicts" a probability $P_i$ for each observation. We ask the reverse question: *if this $\beta$ were true, what is the probability of observing exactly the sequence of 0/1 outcomes we actually see in the sample?* ML chooses $\beta$ so that the probability of "reproducing" the observed data is **maximized**. In other words: OLS asks "which $\beta$ makes the predicted line closest to the data" (by squared distance); ML asks "which $\beta$ makes the observed data *most likely*".

The log-likelihood function to be maximized:

$$\log L = \sum_{i=1}^n\Big[Y_i\log P_i + (1-Y_i)\log(1-P_i)\Big], \qquad P_i=\frac{1}{1+e^{-\beta X_i}}$$

For each observation with $Y_i=1$, only the term $\log P_i$ "contributes" to the sum (the other term is multiplied by $1-Y_i=0$ and vanishes); conversely for $Y_i=0$, only $\log(1-P_i)$ contributes. Intuition: if the model predicts a high $P_i$ for an observation that truly has $Y_i=1$ (correct, confident prediction), $\log P_i$ is close to 0 (a good contribution); if the model predicts a low $P_i$ for an observation with $Y_i=1$ (a wrong prediction), $\log P_i$ is very negative (heavily penalized). There is no closed-form solution like $b=(X'X)^{-1}X'y$ for OLS — $\beta$ is found by numerical optimization (e.g. Newton-Raphson), carried out by statistical software (R, Stata…).

## The Probit model

Probit uses the same framework $Pr(Y_i=1)=F(X_i\beta)$ but replaces the logistic function with the **cumulative distribution function (CDF) of the normal distribution**:

$$Pr(Y_i=1)=P_i=\Phi(\beta X_i)=\frac{1}{\sqrt{2\pi}}\int_{-\infty}^{\beta X_i}e^{-z^2/2}\,dz$$

In other words: Logit assumes the error $u$ follows a **logistic distribution**; Probit assumes $u$ follows a **normal distribution**. Both have an S shape, both are automatically bounded in (0,1) — the only difference is the **shape of the tails** of the two distributions:

- The logistic distribution has slightly **fatter tails** than the normal distribution.
- Consequence: $P_i$ converges to 0 and 1 **more slowly** in Logit than in Probit — for the same change in $X\beta$ in the extreme region (far from 0), Logit still "holds back" a bit of probability that has not fully converged to the boundary, while Probit converges faster.

**Which one to choose, and when?** In principle, there is no clear theoretical reason to strictly prefer one over the other — with the same dataset, the two models give substantively equivalent conclusions (same sign, same statistical significance level on most variables — see the real data in section 8). The practical reason **Logit is usually preferred**: Logit's marginal effect has a closed form, computable directly with an algebraic formula; Probit's marginal effect requires the derivative of the normal distribution function (no simple closed form, must be computed numerically). In addition, Logit also has the **odds ratio** interpretation (section 10) — a tool familiar in health/epidemiology — for which Probit has no direct equivalent.

## Real estimation on the vaccine data — Logit and Probit side by side

Here is the full estimation results table (`stargazer(logit, probit)`), $N=377$:

|Variable | Logit $\hat\beta$ (SE) | Probit $\hat\beta$ (SE) |
|---|---|---|
| `efficacy80` | 0.1584 (0.2704) | 0.0821 (0.1542) |
| `duration3` | −0.2807 (0.2712) | −0.1603 (0.1544) |
| `priceUS` | −0.0318*** (0.0092) | −0.0184*** (0.0053) |
| `pbenefit` | 0.1423 (0.2689) | 0.0561 (0.1530) |
| `hhincomeUS` | 0.0005** (0.0002) | 0.0002* (0.0001) |
| `hhsize` | −0.0513 (0.0542) | −0.0225 (0.0317) |
| `age` | −0.0282*** (0.0101) | −0.0161*** (0.0057) |
| `male` | −0.3854 (0.2809) | −0.2281 (0.1614) |
| `riskNeither` | 0.0862 (0.5062) | 0.0229 (0.2788) |
| `riskUnlikely` | −0.6386 (0.4933) | −0.3494 (0.2764) |
| `riskVery likely` | 0.5589 (1.1846) | 0.2528 (0.6126) |
| `riskVery unlikely` | −0.9552* (0.4950) | −0.5516** (0.2798) |
| Constant | 3.5867*** (0.7870) | 2.1075*** (0.4356) |
| Log-likelihood | −175.1115 | −175.7007 |
| AIC | 376.2230 | 377.4013 |

(The `risk` base category is "Likely" — the 4 dummies `riskNeither/riskUnlikely/riskVery likely/riskVery unlikely` measure the difference relative to this group.)

**Notable observation, consistent across both models**: same sign and same level of statistical significance on nearly every variable — `priceUS` and `age` are strongly significant (p<0.01) in both, `hhincomeUS` is weakly significant (p<0.1 probit, p<0.05 logit), `riskVery unlikely` is significant in both. This illustrates exactly the point made in section 6 that "there is no obvious reason to choose strictly one over the other."

**Rule of thumb for coefficient magnitude**: Logit coefficients are typically about **1.6–1.8 times** larger than their corresponding Probit coefficients (because the standardized logistic distribution's standard deviation differs from the standardized normal distribution's — the theoretical ratio is approximately $\pi/\sqrt3\approx1.814$). Verified with the data above: $-0.0318/-0.0184\approx1.73$ (`priceUS`); $-0.0282/-0.0161\approx1.75$ (`age`) — fairly close to the rule of thumb. **This is why Logit and Probit coefficients should not be compared directly in magnitude** — only their sign, statistical significance, or converted marginal effects/predicted probabilities can be compared (sections 9, 11).

## Hypothesis testing after Logit/Probit: the LR test and Wald test

### Intuition: two different ways of testing

Both tests answer the same type of question ("is this group of coefficients statistically significant?") but by two different routes — in the same spirit as the F-test in [[concepts/linear-regression-model]] section 8, but replacing RSS with log-likelihood since Logit/Probit are estimated by ML, not OLS:

- **Likelihood Ratio (LR) test**: estimate **twice** — once the full/unrestricted model (log-likelihood $LL_F$), once the model constrained by $H_0$ (restricted, log-likelihood $LL_R$, usually dropping the variables being tested entirely). Compare how well each model "rationalizes the data" — if removing a variable makes the log-likelihood drop a lot, that variable really matters.
- **Wald test**: only needs to be estimated **once** — the full model. It directly uses the estimated coefficients $\hat\beta$ and the covariance matrix (VCV) of the full model to infer whether the $H_0$ constraint is "plausible," without re-estimating the restricted model — in spirit, it is like an extended t-test/F-test, based on the "distance" between the estimate and the hypothesized value, measured in units of SE.

The two tests are **asymptotically equivalent** when the sample size is large enough, but **do not give the same number in finite samples** — the real data below clearly illustrates this.

The LR test formula:

$$LR = 2(LL_F - LL_R) \sim \chi^2_q$$

where $q$ = the number of coefficients being tested. A useful technical point to remember: $\log L = -\text{deviance}/2$ — i.e. deviance (which often appears directly in R's `glm()` output) is just the log-likelihood multiplied by $-2$, so `anova(model, test="Chisq")` (comparing deviance) and `lrtest()` (comparing log-likelihood) are essentially computing the same number.

### Real data — testing overall significance (all slope coefficients, excluding the intercept)

| | Logit | Probit |
|---|---|---|
| Null deviance (376 df) | 392.32 | 392.32 |
| Residual deviance (364 df) | 350.22 | 351.40 |
| $\Delta$Deviance, df=12 | 42.096 | 40.918 |
| p-value | 3.209e-05 | 5.057e-05 |

Both strongly reject $H_0:\beta_1=\cdots=\beta_{12}=0$ — there is evidence that the explanatory variables, taken jointly, are not all irrelevant (read exactly as in section 8.5 of [[concepts/linear-regression-model]] — an overall F-test/LR-test only says "at least one," not "all").

**Self-check using $\log L=-\text{deviance}/2$**: for Logit, $LL_{full}=-175.1115$ (from the table in section 7), so $LL_{null}=-392.32/2=-196.16$; $2(LL_F-LL_R)=2(-175.1115-(-196.16))=42.097\approx42.096$ ✅ matches (small discrepancy due to rounding). For Probit, $LL_{full}=-175.7007$, $2(-175.7007-(-196.16))=40.919\approx40.918$ ✅ also matches — a quick way to check the internal consistency of a numbers table when working by hand.

### Real data — testing the `risk` variable group separately (4 dummies at once)

$H_0: \beta_{riskNeither}=\beta_{riskUnlikely}=\beta_{riskVery\,likely}=\beta_{riskVery\,unlikely}=0$ (the `risk` variable has no effect at all, considering all 4 levels jointly):

| | LR test | Wald test |
|---|---|---|
|**Logit**: $LL_F=-175.11$ (13 parameters) vs $LL_R=-180.92$ (9 parameters) | $\chi^2=11.618$, df=4, p=0.02043 | $\chi^2=11.067$, df=4, p=0.02582 |
|**Probit**: $LL_F=-175.70$ (13 parameters) vs $LL_R=-181.01$ (9 parameters) | $\chi^2=10.626$, df=4, p=0.03111 | $\chi^2=10.452$, df=4, p=0.03346 |

All 4 tests reject $H_0$ at the 5% level — there is evidence that the perceived risk of COVID-19 infection jointly affects the vaccination decision. **Point to remember**: LR and Wald give the **same conclusion** (reject at 5%) but the **test statistics do not match exactly** (11.618 ≠ 11.067; 10.626 ≠ 10.452) — this is a normal consequence of the two tests being only *asymptotically* equivalent (as $n\to\infty$), not identical in finite samples ($n=377$ here).

## Marginal effects — the hardest part, why it is not a constant

### Intuition via the shape of the sigmoid curve

This is the most important difference between LPM and Logit/Probit, and also the source of the most common exam trap (section 12). In LPM, the regression line is **a straight line** — the slope is constant at every point, so the marginal effect $=\beta_j$, a single constant. In Logit/Probit, the predicted curve of $P_i$ against $X_i$ has an **S shape** — and the slope of an S-shaped curve **is not uniform along the curve**:

- At the two ends (when $P_i$ is already near 0 or near 1), the curve is nearly **flat** — because most individuals in this region have already "locked in" their decision (nearly certainly yes or nearly certainly no), so one more unit of $X$ barely changes anyone's decision. The marginal effect here is very **small**.
- In the middle region (when $P_i$ is near 0.5 — the "fence-sitting" group, still undecided), the curve is **steepest** — a small change in $X$ can sway the decision of many people at the margin. The marginal effect here is **largest**.

This is precisely the formalization of LPM drawback #2 (section 4.4): LPM assumes the same sensitivity at every level of $X$; Logit/Probit allow the sensitivity to **change depending on position along the curve**, matching economic intuition much better.

Formula (the derivative of $P_i$ with respect to $X_i$, for Logit):

$$\frac{\partial P_i}{\partial X_i} = \frac{\partial}{\partial X_i}\left(\frac{1}{1+e^{-\beta X_i}}\right) = \beta_i\cdot\underbrace{\frac{1}{1+e^{-\beta X_i}}\Big(1-\frac{1}{1+e^{-\beta X_i}}\Big)}_{=P_i(1-P_i)} = \beta_i\cdot P_i(1-P_i)$$

The term $P_i(1-P_i)$ is a bell-shaped "weight," reaching a maximum $=0.25$ at $P_i=0.5$ and approaching 0 as $P_i\to0$ or $P_i\to1$ — this is precisely the rigorous formalization of the "steepest in the middle, flat at the ends" intuition just described. **The marginal effect in Logit/Probit is not a fixed number — it is a function that depends on the specific value of $X$ (through $P_i$)**.

### Illustration with numbers computed by hand from the Logit coefficients (vaccine data)

Using the Logit coefficient from section 7 ($\beta_{priceUS}=-0.0318$; other variables fixed at: `efficacy80=1, duration3=1, pbenefit=0, hhincomeUS=700, hhsize=4, age=30, male=1, risk="Very likely"` — the same reference values used to plot the predicted-probability graph in section 10), computing by hand with the formula above to clearly see the S shape and how the marginal effect changes with vaccine price:

| `priceUS` (USD) |predicted |Marginal effect ($\partial P/\partial X$, pp per $1 increase) |
|---|---|---|
| 0 | ≈ 0.950 | ≈ −0.152 |
| 50 | ≈ 0.794 | ≈ −0.521 |
|(point where $P=0.5$) | = 0.500 |**(steepest)** |
| 100 | ≈ 0.440 | ≈ −0.783 |
| 150 | ≈ 0.138 | ≈ −0.378 |

*(The figures in this table were hand-computed from the coefficients rounded to 4 decimal places in the stargazer table of section 7 — intended only to illustrate the curve's shape, and may differ slightly from numbers output directly by R using full-precision coefficients.)*

Clearly: the marginal effect is not a single number, but changes from about −0.15 percentage points (at a price of 0 USD, when most are already willing to vaccinate) up to nearly −0.8 percentage points (at a price around 90 USD, the "fence-sitting" region), then falls back to about −0.38 percentage points (at a price of 150 USD, when most have already refused). This is direct numerical evidence for LPM drawback #2.

### MEM (Marginal Effect at the Mean) vs. AME (Average Marginal Effect)

Since the marginal effect changes with $X$, a practical question arises: when reporting results (e.g. in a thesis regression table), which **single number** for the marginal effect should be reported for each variable? There are two standard approaches:

- **MEM — Marginal Effect at the Mean**: computes the marginal effect at **a single point** — the point where every $X$ variable is set to its sample mean ($\bar X$). In R: `logitmfx(..., atmean=TRUE)`. Conceptual drawback: this "average observation" often **does not exist in reality** — for example, if the sample mean of `male` is 0.55, the "average person" is 55% male, a nonexistent individual. For dummy or categorical variables, the notion of a "mean value" becomes ambiguous to interpret.
- **AME — Average Marginal Effect**: computes the marginal effect **at each observation** (using that observation's actual $X_i$ values), then takes the **arithmetic mean** of all $N$ individual marginal effects. In R: `logitmfx(..., atmean=FALSE)`. Advantage: correctly reflects the real heterogeneity present in the sample, without relying on any "hypothetical individual."

**Why is AME usually recommended over MEM in modern practice?** Because AME respects the actual distribution of the data — it is the average of N real marginal effects, rather than the marginal effect at an artificial point that may lie in a sparse or unrepresentative region of the data. This is also the default choice in many modern statistical tools (e.g. Stata's `margins, dydx(*)` computes AME by default). MEM is still useful when the specific research question is "the effect of X on an individual with average characteristics" — but for most general-purpose regression reporting, AME is the safer, more preferred choice.

### Real data — MEM and AME for the same model

**Logit — MEM (`atmean=TRUE`)**, listing only the statistically significant variables:

|Variable | dF/dx | SE | p-value |
|---|---|---|---|
| `priceUS` | −4.7433e-03 | 1.3804e-03 | 0.0006 *** |
| `age` | −4.2117e-03 | 1.3341e-03 | 0.0016 ** |

**Logit — AME (`atmean=FALSE`)**:

|Variable | dF/dx | SE | p-value |
|---|---|---|---|
| `priceUS` | −4.7423e-03 | 1.5302e-03 | 0.00194 ** |
| `age` | −4.2108e-03 | 1.4774e-03 | 0.00437 ** |

**Probit — MEM**: `priceUS` dF/dx = −4.9899e-03 (SE 1.4710e-03, p=0.0007***); `age` dF/dx = −4.3804e-03 (SE 1.3546e-03, p=0.0012**).
**Probit — AME**: `priceUS` dF/dx = −4.8133e-03 (SE 1.3684e-03, p=0.0004***); `age` dF/dx = −4.2254e-03 (SE 1.2813e-03, p=0.0010***).

The remaining variables (`efficacy80`, `duration3`, `pbenefit`, `hhincomeUS`, `hhsize`, `male`, the levels of `risk`) are not statistically significant for the marginal effect under either method, even though a few (`hhincomeUS`) are weakly significant in the raw coefficient (section 7) — this itself is a point worth noting: **the statistical significance of the raw coefficient and of the marginal effect do not necessarily match completely**.

**Reading the specific number**: the AME of `priceUS` (Logit) is −0.0047423 — meaning, **on average across the whole sample**, each additional 1 USD in vaccine price reduces the probability of deciding to vaccinate by about **0.474 percentage points**. Compared to the hand-computed table in section 9.2 (ranging from −0.15 to −0.80 percentage points depending on the price level), the AME is essentially a "weighted average" of all those varying individual marginal effects — a single number summarizing an inherently heterogeneous phenomenon.

**Remark on the MEM vs. AME difference in this example**: the two dF/dx numbers are very close in magnitude (−4.7433e-03 vs −4.7423e-03 for `priceUS`) — because the distribution of the variables in this sample is not too skewed/extreme, so the "average observation" is not too different from the "average of the observations." The SEs differ more noticeably (1.3804e-03 MEM vs 1.5302e-03 AME for `priceUS`) — illustrating that the two methods differ not only in the point estimate but also in the associated uncertainty.

### Marginal effect at a specific point — the discrete difference method

Besides the analytical derivative, there is a more **practical** way of computing the marginal effect — especially useful when we want the effect at a specific data point, or when the independent variable is not continuous (dummy, categorical) and the analytical derivative does not apply directly: predict the probability at **two points** that differ by exactly 1 unit of the variable of interest, then take the difference.

Illustrative example for `hhincomeUS`: hold all other variables fixed (`priceUS=50, efficacy80=1, duration3=1, pbenefit=0, hhsize=4, age=30, male=1, risk="Very likely"`), and change only household income from 700 to 701 USD/month:

- **Probit**: the corresponding difference $=6.806759\times10^{-5}$

That is, at this data point, increasing household income by 1 USD/month only increases the probability of deciding to vaccinate by about **0.0076 percentage points** (Logit) — very small, consistent with the `hhincomeUS` coefficient already being tiny (0.0005) and not statistically significant at the marginal-effect level (section 9.4). This discrete-difference method is exactly how R/Stata compute the marginal effect for dummy variables (e.g. `male`, `efficacy80`) — since the concept of a "derivative" has no meaning for a variable that only takes the value 0 or 1.

## Predicted probability and prediction accuracy

### The predicted probability curve

Holding the other variables at their reference levels (as in section 9.2), letting `priceUS` range from 0 to 150 USD and plotting the predicted $\hat P_i$ — the graph produces exactly the expected S shape: starting near 0.94–0.95 at price zero, decreasing and steepest in the middle price range (about 70–100 USD), then flattening out to about 0.13–0.14 as the price reaches 150 USD — fully consistent with the hand-computed table in section 9.2 and with the theoretical sigmoid shape described in section 9.1.

### Prediction accuracy (correct prediction rate) — Probit example

Using the threshold $\hat P_i>0.5$ to classify the prediction as "vaccinate"/"not vaccinate," compared against the actual outcome:

| |Actual: `dself=0` |Actual: `dself=1` |
|---|---|---|
|Predicted: not vaccinate (FALSE) | 9 | 7 |
|Predicted: vaccinate (TRUE) | 72 | 289 |

Overall correct prediction rate: $\dfrac{9+289}{377} = 0.7904509$ (≈79.05%).

**A point to note when interpreting this number** (computed additionally from the table above — a direct arithmetic consequence): in the sample, the total number of people who actually chose "vaccinate" is $7+289=296/377\approx78.5\%$. This means a "naive" model that simply always predicts "vaccinate" for everyone (without knowing anything about $X$) would already achieve about 78.5% accuracy — close to the 79.05% the Probit model achieves. The model correctly identifies only 9/81 (≈11%) of the truly "not vaccinate" cases — showing that **the overall correct-prediction rate can be misleading when the outcome is imbalanced** — a point to be cautious about when evaluating binary response models in practice, rather than stopping at a single "% correct" number.

## Logit or Probit? — a direct comparison via the predicted-probability graph

Overlaying the two predicted-probability curves (Logit and Probit) on the same `priceUS` variable: the two lines **nearly coincide** across the entire 0–150 USD price range, diverging only very slightly in the middle region — the Logit line sits a bit higher than Probit in the low/middle price region, consistent with the observation in section 6 that Logit's $P_i$ "converges to 0 and 1 more slowly" than Probit. This is visual evidence that **the substantive conclusion (predicted probability) of the two models is nearly equivalent** even though their raw coefficients differ by about 1.6–1.8 times (section 7) — the two facts are not contradictory, because Logit/Probit raw coefficients are not comparable on their own, only the probabilities/marginal effects derived from them are comparable.

## Logistic regression with Odds Ratio

Another common way of presenting Logit results — especially in health/epidemiology — is to report the **odds ratio** directly instead of the raw coefficient. Since $\dfrac{P_i}{1-P_i}=e^{\beta X_i}$ (section 5.2) already holds, the odds ratio of each variable is exactly $e^{\hat\beta_j}$ — confirmed with real data: `exp(coef(logit))` produces exactly the "OddsRatio" column in the `logitor()` table.

|Variable | Odds Ratio | p-value |Interpretation |
|---|---|---|---|
| `priceUS` | 0.9687 | 0.0005 *** |each $1 increase in price **decreases** the odds of deciding to vaccinate by **about 3.13%** ($(0.9687-1)\times100\%$), holding other variables constant |
| `age` | 0.9722 | 0.0053 ** |each additional year of age decreases the odds of deciding to vaccinate by about 2.78% |
| `hhincomeUS` | 1.00046 | 0.0428 * |each additional $1 of household income increases the odds by about 0.046% (very small, though weakly statistically significant) |
| `riskVery unlikely` | 0.3847 | 0.0536 . |relative to the "Likely" (base) group, the group who feel infection is "very unlikely" have odds of deciding to vaccinate only about 38.5% as large (at a marginal significance level, p≈0.054) |

**Rule for reading an odds ratio**: $OR>1$ → the variable **increases** the odds (and hence increases $P$); $OR<1$ → **decreases** the odds; $OR=1$ → no effect. The percentage change in odds $=(OR-1)\times100\%$. Note: this is still a statement about **odds**, not a direct statement about the probability $P$ or the marginal effect — converting back from odds ratio to probability still requires applying the formula $P=OR/(1+OR)$ in the right context; the odds ratio cannot be read directly as a percentage-change number for $P$.

## Summary comparison: LPM vs Logit vs Probit

|Criterion | LPM | Logit | Probit |
|---|---|---|---|
|Link function $F(X\beta)$ | $X\beta$ | $\dfrac{1}{1+e^{-X\beta}}$ |$\Phi(X\beta)$ (normal CDF) |
|Is predicted $Pr(y=1)$ bounded in [0,1] |No |Yes |Yes |
| Marginal effect |Constant ($=\beta_j$) |Changes with $X$ (via $P(1-P)$) |Changes with $X$ (via $\phi(X\beta)$) |
|Estimation | OLS | Maximum Likelihood | Maximum Likelihood |
| Heteroskedasticity |Inherent, always violates A4 |Not an issue in the same way (does not use the OLS framework) |Similar to Logit |
|Interpreting the raw coefficient |Direct = change in probability |Gives only the **sign** (direction), not the magnitude — need the marginal effect or odds ratio |Gives only the **sign**, not the magnitude — need the marginal effect |
|Advantage |Simple, easy to interpret, can use familiar OLS tools |Marginal effect has a closed form; also has the odds-ratio interpretation |Theoretical foundation tied to the normal distribution — often used when modeling a latent variable with $u\sim N(0,1)$ (e.g. extensions to Tobit, Heckman) |
|Disadvantage |The 4 drawbacks in section 4.4 |Fatter tails than normal — converges to 0/1 more slowly |Marginal effect must be computed numerically (no simple closed form) |
|When to use |When an extremely fast, extremely simple interpretation is needed, or as a baseline model for comparison; rarely used as the formal model in modern research |The most common choice in practice — especially when the odds ratio is needed (health, credit) |When the theory/extended model requires the normal-distribution assumption (e.g. linking to censored/truncated models in Topic 11) |

## Exam traps

1. **Interpreting a raw Logit/Probit coefficient as if it were a direct % change in probability** — the single most common mistake in all of Topic 7. The raw coefficient ($\hat\beta_j$) only tells you the **direction** of the change in $P$ (positive/negative sign), **not the magnitude**. To know the magnitude of the effect on probability, you must compute the **marginal effect** (section 9); to interpret via odds, use $e^{\hat\beta_j}$ (section 12) — and even then, an odds ratio is a statement about odds, not a direct statement about a percentage change in probability.
2. **Treating the Logit/Probit marginal effect as a single constant, like the LPM** — wrong. The marginal effect depends on the value of $X$ (via $P_i(1-P_i)$ or $\phi(X\beta)$) — a report must state clearly whether it uses **MEM** or **AME**, never a generic "the marginal effect of variable X is...".
3. **Assuming MEM and AME are two computation methods that give the same number** — in practice they are often close (as in the example in section 9.4) but **not mathematically identical**, especially when $X$'s sample distribution is strongly skewed. Always state clearly which one is being used when reporting results.
4. **Directly comparing the raw coefficient magnitudes between Logit and Probit** without rescaling — the two models have different scales (normalized variances); Logit coefficients are mechanically about 1.6–1.8 times larger than Probit's, which does not reflect a genuinely "stronger" effect — a meaningful economic comparison requires comparing predicted probabilities or marginal effects instead.
5. **Expecting the LR test and Wald test to give exactly the same statistic** — the two tests are only **asymptotically equivalent**, not identical in finite samples (see the real numbers in section 8.3: 11.618 vs. 11.067).
6. **Using the % correct prediction rate as the sole measure of model quality** when the outcome is imbalanced — as in the example in section 10.2, a "naive" model that always predicts the majority class already achieves accuracy close to that of the actual Probit model; you also need to look at the ability to correctly identify the minority class (only 11% here), not just the overall number.
7. **Treating the fact that the LPM "still runs fine via OLS" as meaning the LPM is valid for statistical inference** — the LPM always violates A4 (heteroskedasticity, section 4.4) systematically (not randomly, as in an ordinary LRM), so OLS's default SE applied to an LPM should always be treated with suspicion, even though the model still "runs" and produces coefficients.
8. **Forgetting that an odds ratio > 1 or < 1 carries a different meaning than a positive/negative raw coefficient** — $OR=1$ (not $OR=0$) is the "no effect" point; misreading $OR<1$ as "a small negative effect" instead of correctly computing the percentage change $(OR-1)\times100\%$ is a common mistake for those new to odds ratios.

## Connections to the rest of the course

This page is the foundation for all of **Part 2: Models for Limited Dependent Variables**:

- The ML + latent-variable + LR/Wald test + marginal effects (MEM/AME) framework built here is **reused almost unchanged** in [[concepts/multinomial-logit-model]] (extended to multiple unordered choices — softmax replacing two-choice logistic) and [[concepts/ordinal-response-models]] (extended to ordered choices — a latent variable with multiple cutpoints).
- [[concepts/count-data-models]] and [[concepts/censored-regression-tobit]] also share the same "use ML instead of OLS" philosophy once the dependent variable is no longer "cleanly" continuous in the classical LRM sense.
- The LPM in section 4 is a direct point of comparison back to [[concepts/linear-regression-model]] — the same OLS tool, but applied to a binary variable clearly exposes the limits of the linear framework, exactly as the "5 assumptions A1–A5" section of that page warned in advance.
- The LPM's "built-in" heteroskedasticity problem (section 4.4, drawback #3) is a concrete, empirical illustration of the entire theoretical content in [[concepts/heteroskedasticity]] — worth reading alongside it for a deeper understanding of why robust SE is necessary.

## Real-world application references

Three recent papers illustrating binary response models (Logit/Probit) in real-world economic research (Lecture 9 syllabus):

- Wagner, J., Bühner, C., Gölz, S., Trommsdorff, M., & Jürkenbeck, K. (2024). Factors influencing the willingness to use agrivoltaics: A quantitative study among German farmers. *Applied Energy*, 361, 122934. https://doi.org/10.1016/j.apenergy.2024.122934
- Alfano, V., De Simone, E., D'Uva, M., & Gaeta, G. L. (2022). Exploring motivations behind the introduction of tourist accommodation taxes: The case of the Marche region in Italy. *Land Use Policy*, 113, 105903. https://doi.org/10.1016/j.landusepol.2021.105903
- Mahn, D., Best, R., Wang, C., & Abiona, O. (2024). What drives solar energy adoption in developing countries? Evidence from household surveys across countries. *Energy Economics*, 138, 107815. https://doi.org/10.1016/j.eneco.2024.107815
