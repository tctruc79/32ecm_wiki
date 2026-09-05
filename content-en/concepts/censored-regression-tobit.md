---
title: "Lecture 13: Censored Regression: The Tobit Model"
type: concept
status: mature
tags: [tobit, censored-data, truncated-data, limited-dependent-variable]
sources: ["[[sources/slides-11-censored-regression-tobit]]"]
related: ["[[concepts/linear-regression-model]]", "[[concepts/binary-response-models]]"]
lecture: 13
assignment: []
updated: 2026-09-04
---

> **How to read this page**: this is the final lesson of Part 2 — Models for Limited Dependent Variables, after binary $y$ ([[concepts/binary-response-models]]), unordered multi-choice $y$ ([[concepts/multinomial-logit-model]]), ordered $y$ ([[concepts/ordinal-response-models]]) and count $y$ ([[concepts/count-data-models]]). Here $y$ goes back to being **continuous** as in [[concepts/linear-regression-model]] — but is "cut" at a threshold. **The hardest part, and per the review log the "highest-value exam trap" of this topic, is distinguishing the THREE types of predicted value/marginal effect after Tobit** (section 7) — if there is only time to read one section before the exam, read section 7. Section 2 (censored vs. truncated) is the mandatory foundation to master first, since it determines which model is allowed to be used.

**Lecture 13** in the syllabus (CO Topic 11) — no dedicated assignment yet. This is also the final lecture of the course.

## Why a dedicated model is needed — when $y$ is "cut" at a threshold

[[concepts/linear-regression-model|OLS]] assumes $y$ is a continuous variable, fluctuating freely without limit. But many economic variables have a **natural bound** — a threshold below (or above) which the true value is no longer recorded as it actually is, but instead "assigned" to a fixed constant. Four classic examples are:

- **Dividend**: equal to 0 until the company's profit reaches a certain threshold — below that threshold, the company pays no dividend, even though the company's latent "dividend-paying capacity" could differ, positive or negative.
- **Government-controlled price (price control)**: the "true" market price might want to rise above or fall below the ceiling/floor set by the government, but the observed price is held rigidly at that ceiling/floor.
- **Working hours**: equal to 0 for the unemployed — but their latent "desire to work" can still differ from one person to another, even though what is observed is 0 for all of them.
- **Loan**: equal to 0 if the loan application is rejected.

The common thread: there is a latent "desire" or "capacity" variable (not directly observable) — but the data only records it once it crosses a threshold; below the threshold, everything is "labeled" the same way (usually 0), regardless of how different the underlying latent value actually is.

**This lecture's running case study** (reused from section 5 onward): **credit card balance**. Many customers pay off their balance every month or do not use the card to borrow → the observed balance is exactly 0, even though their latent "borrowing tendency" (depending on interest rate, age, gender, education) can be very different.

## Censored vs. Truncated — distinguishing the two most commonly confused concepts

This is the most fundamental exam trap of the topic: the two concepts sound alike, and the data looks alike at a glance too (many values "disappearing" on one side), but the underlying nature — and the appropriate model — are completely different.

### Censored data — the ENTIRE sample is observed, values are "cut"

> Definition: "$y$ is censored if: we can observe all values of $y$, but only in a certain interval, values beyond the interval are recorded as a constant (e.g.: 0)."

Intuition: we **still have the full presence of every observation in the sample** — we still know $X_i$ (interest rate, age, gender, education...) for each person, including those who are "cut." Only the **value of $y$** for observations that fall outside a range is replaced by a fixed constant (usually 0), hiding the "true" latent value underneath.

- $y \ge k$: **censored from below** — every value below $k$ is assigned to $k$.
- $y \le k$: **censored from above** — every value above $k$ is assigned to $k$.

**Concrete example** (the credit card balance case study, censored from below at 0): in the sample of 2895 customers, we fully know the interest rate, age, gender, education of **all** 2895 people — including the 1018 people with `balance = 0`. We don't know "the balance they would have had if it were allowed to be negative" (e.g., an extremely financially cautious customer could have a very negative latent "borrowing tendency"), but we know for certain that they *exist in the sample* and we know their characteristics.

**Additional illustrative example** (a self-added example, same logic, familiar in econometrics — Tobin's 1958 original example on durable/luxury goods spending): a household's annual spending on luxury goods = 0 for households that buy nothing at all, but that household **is still in the survey sample**, we still know its income, household size, etc. — only its latent "willingness to spend" (which could be negative, e.g. an indebted household wanting to "spend negatively") is hidden by the 0 threshold.

### Truncated data — entire OBSERVATIONS outside the range vanish from the sample

> Definition: "$y$ is truncated if we can only observe it in the uncensored interval."

Intuition: completely unlike censored — here **it is not just the value of $y$ that is hidden**, but the **entire observation** (both $y$ and $X$) of units outside the range of interest **does not appear in the data at all**. We don't even know they exist, have no way to count how many were excluded, and certainly don't know their $X$ characteristics.

**Illustrative example** (a self-added example, same logic, consistent with the review hint): a survey **that only interviews households with income above a certain threshold** (e.g. a survey dedicated to "well-off households") — households with income below the threshold are not present in the dataset at all, not because their income was recorded as a fixed number, but because they **were never included in the sample**.

The difference is illustrated with 4 consecutive scatter plots, on the same underlying set $(x,y)$ with $x \in \{1,...,5\}$, $y \in \{1,...,9\}$:

1. **"No censoring or truncation"** — the full set of original data points, spread evenly from $y=1$ to $y=9$.
2. **"Censored from above"** (at $y=6$) — every point with $y>6$ in the original data is "piled" down to sit exactly at $y=6$ (many points overlapping at level 6), but the number of points per $x$ value **is unchanged** compared to the original plot.
3. **"Censored from below"** (at $y=5$) — similar but piled up to $y=5$ from below.
4. **"Truncated"** — only points with $x \ge 3$ remain visible on the plot; every point with $x=1,2$ **vanishes entirely**, without piling up anywhere.

The most important visual takeaway from these 4 plots: with censored, **point density by $x$ is unchanged** (only $y$ gets "flattened" at the threshold); with truncated, **point density itself also drops sharply** in the cut portion — because those observations no longer exist at all, not merely that their $y$ is hidden.

### Comparison table

|Criterion | Censored | Truncated |
|---|---|---|
|Sample size |Full, unchanged |Shrunk — observations outside the range are lost entirely |
|Independent variable $X$ |Observed for **every** unit, including cut units |Only observed for units that remain in the sample |
|Value of $y$ outside the range |Assigned to a fixed constant (usually 0) |Does not exist in the data — vanishes entirely, not a "0" |
|Do we know who was excluded? |Yes — we know exactly which units are censored and their $X$ characteristics |No — we don't know they exist, cannot count how many |
|Appropriate model | **Tobit** |Truncated regression model (a different model, not Tobit) |
|Running OLS directly on observed $y$ |Biased |Biased |

### Why Tobit CANNOT be applied to truncated data

> The precise statement to remember: **"Tobit can not be applied for truncated data."**

The intuitive reason: Tobit's log-likelihood (section 6) is built by adding two parts — a continuous density part for uncensored observations, and a **probability** part $\Phi(-X\beta/\sigma)$ for censored observations. To compute that probability part, Tobit **needs to know $X$ for the very observations that are censored** — exactly what censored data provides. With truncated data, observations outside the range are not present in the dataset at all, so there is no $X$ to plug into that formula — Tobit's likelihood function simply does not apply. This case needs a different likelihood function, conditioned on exactly "$y$ is only observed within the uncensored interval" — that is the **truncated regression model**, and further still, when "making it into the sample" is itself systematically correlated with $y$ (not merely a hard cutoff threshold on $y$), the **Heckman selection model** is used to handle it (see the scope note in section 9).

## Why not use OLS directly on a censored variable?

> The precise statement to remember: **"OLS with censored/truncated dependent variables is biased."**

The intuition for the censored case (applies similarly to truncated): in the credit card balance example, 1018/2895 ≈ 35.2% of customers have `balance = 0` — a large mass of data points piled exactly at $y=0$. There are two common "wrong" ways of trying to handle this with ordinary OLS:

1. **Run OLS on the whole sample, treating 0 as a "real" $y$ value** — OLS tries to draw a straight line through both the mass of points at 0 and the positive data above. Because the mass of points at 0 pulls the regression line "flat," the estimated coefficient is pulled closer to 0 than its true value — this is a form of **attenuation bias** (bias shrinking the magnitude of the coefficient).
2. **Drop the observations with $y=0$ entirely, and run OLS only on the rest ($y>0$)** — this looks reasonable at first (because "the remaining data are all real, uncut values") but is also biased: this is a form of **non-random sample exclusion** (the $y>0$ subsample is not a random subsample of the population — it systematically tends to include people with "more favorable" characteristics per the model), which is essentially equivalent to turning a censored sample into a truncated one right in the middle of the analysis.

Both approaches are biased, regardless of how much or how little censoring there is. Only full **maximum likelihood estimation per Tobit** — using all the information, including knowing $X$ for censored observations — yields a consistent estimator.

## The Tobit model — latent variable structure

$$y^*=X\beta+\varepsilon, \qquad y=\begin{cases}0 & \text{if } y^*\le0\\ y^* & \text{if } y^*>0\end{cases}$$

- $y^*$ is called the **index / latent variable** — the same mathematical structure as $y^*$ in [[concepts/ordinal-response-models]] (both are "a hidden continuous variable, observed through thresholds"). Important difference: in the ordinal model, there are **multiple cut thresholds** and those thresholds are usually **estimated** from the data; in Tobit "censoring at 0," there is only **a single threshold, fixed at 0**" (known in advance, not estimated).
- $y$ is the **observed variable** — the actual credit card balance recorded in the data.
- $\varepsilon$ is the random error, assumed $\varepsilon \sim N(0,\sigma^2)$, so $y^*\sim N(X\beta,\sigma^2)$.

Under this normality assumption, the probability that an observation is censored (i.e. $y=0$) is:

$$Pr(y=0)=Pr(y^*\le0)=\Phi\left(-\frac{X\beta}{\sigma}\right)=1-\Phi\left(\frac{X\beta}{\sigma}\right)$$

where $\Phi$ is the cumulative distribution function (CDF) of the standard normal distribution — the same notation, the same role as $\Phi$ in the Probit model in [[concepts/binary-response-models]]. This is not a coincidence: fundamentally, "censored or not" is itself a hidden binary decision inside Tobit, governed by exactly the Probit mechanism.

**General case** (censoring on both sides, at $a$ and $b$, e.g. a price controlled by both a ceiling and a floor):

$$y=\begin{cases}a & \text{if } y^*\le a\\ y^*=X\beta+\varepsilon & \text{if } a<y^*<b\\ b & \text{if } y^*\ge b\end{cases}$$

The probability of not being censored (falling within the open interval) becomes:

$$Pr(a<y^*<b)=\Phi\left(\frac{b-X\beta}{\sigma}\right)-\Phi\left(\frac{a-X\beta}{\sigma}\right)$$

Every predicted value/marginal effect formula in section 7 (written for the censoring-at-0 case) has a corresponding general version by replacing $\Phi(X\beta/\sigma)$ with this two-sided probability expression.

## Running case study: Credit card balance

**Dependent variable** (censored from below at 0): `balance` — credit card balance (USD).
**Independent variables**: `interest` (credit card interest rate, %), `age` (age, years), `male` (dummy, 1=male), `edu` (years of education).

**Descriptive statistics** ($N=2895$ observations, `psych::describe`):

|Variable | mean | sd | min | max |
|---|---|---|---|---|
| `balance` | 1917.27 | 9675.95 | 0 | 147917.53 |
| `interest` | 14.42 | 4.46 | 5 | 28.88 |
| `age` | 50.10 | 15.03 | 18 | 106 |
| `male` | 0.78 | 0.42 | 0 | 1 |
| `edu` | 14.39 | 2.56 | 6 | 23 |

The histogram of `balance` shows exactly the shape characteristic of a variable censored at 0: a very tall bar piled at 0, followed by a long right tail (right-skewed) with a few extremely large observations (max ≈ 147918 USD). Split by gender: female (`male=0`, $n=646$) has mean `balance` of 1049.82 USD; male (`male=1`, $n=2249$) has mean `balance` of 2166.44 USD — a large raw gap, matching the direction of the positive `male` coefficient in the Tobit regression below.

**Tobit regression results** (R, package `censReg`, `censReg(balance ~ interest + age + male + edu, left = 0, data = z)`):

```
Observations: Total 2895, Left-censored 1018, Uncensored 1877, Right-censored 0

Coefficients:
              Estimate   Std.error   t value    Pr(>|t|)
(Intercept)   31227.12    1877.00     16.640    < 2e-16 ***
interest       -321.25      54.01     -5.948    2.71e-09 ***
age            -349.21      17.39    -20.083    < 2e-16 ***
male           2531.38     587.30      4.310    1.63e-05 ***
edu            -941.30      94.73     -9.937    < 2e-16 ***
logSigma          9.368      0.016    572.704    < 2e-16 ***

Log-likelihood: -20732.56 on 6 Df
```

A few points worth noting when reading this table:

- **1018/2895 ≈ 35.2%** of observations are censored (left-censored at 0) — this is exactly the "mass of points piled at 0" mentioned in section 3. The remaining 1877 observations (64.8%) have positive `balance`, observed exactly.
- The package estimates **`logSigma`** instead of $\sigma$ directly (exactly as noted in section 6) — $\sigma = \exp(9.367847) \approx 11705.88$ (R recomputes this from `logSigma` when needed for the prediction/ME formulas in section 7).
- Signs of the coefficients: `interest` and `age` are negative (higher interest rate, higher age → lower latent borrowing tendency), `male` is positive, `edu` is negative (more education → lower latent borrowing tendency). These are $\beta$ coefficients on the **latent variable** $y^*$ — section 7 will show that these numbers are **not** the effect on observed `balance`.
- Since there is no clear identification strategy for this dataset (no discussion of the exogeneity of `interest`, `age`...), this page interprets the coefficients in **associational/descriptive language of the estimated model** ("the estimated model shows..."), without asserting strong causal language — following the same caution principle as in [[concepts/linear-regression-model]] section 5.

## Tobit's log-likelihood — the intuitive idea

**Core idea**: Tobit's log-likelihood is the **sum of two different types of contributions**, depending on whether an observation is censored or not:

- For the **1877 customers with positive `balance`** ($Y>0$, uncensored): we know the exact value $Y_i$. The contribution to the likelihood is identical to ordinary OLS/linear regression — using the normal distribution's **probability density** at exactly the point $Y_i$: "the probability (density) of observing exactly this value, if the model is correct."
- For the **1018 customers with `balance = 0`** ($Y=0$, censored): we **do not know** what the latent value $y^*_i$ truly is (it could be −50, it could be −50000 USD of "negative desired borrowing") — we only know for certain that $y^*_i \le 0$. Since the exact point is unknown, density at a single point cannot be used; instead the contribution to the likelihood is the **probability of an entire region**: $Pr(y^*_i\le0)=\Phi(-X_i\beta/\sigma)$.

The full formula (censoring-at-0 case), written as a sum over each observation $i$, with $\mathbb{1}(\cdot)$ the indicator function:

$$\log L(\beta,\sigma\mid X,Y)=\sum_i\left[-\mathbb{1}(Y_i>0)\left(\tfrac12\log(2\pi\sigma^2)+\tfrac{(Y_i-X_i\beta)^2}{2\sigma^2}\right)+\mathbb{1}(Y_i=0)\log\Phi\left(\tfrac{-X_i\beta}{\sigma}\right)\right]$$

The first term (multiplied by $\mathbb{1}(Y_i>0)$) is exactly the log of the normal density — familiar from OLS. The second term (multiplied by $\mathbb{1}(Y_i=0)$) is the log-probability of censoring. Maximizing this sum over $\beta,\sigma$ simultaneously "fits the regression line" to the fully observed part of the data, **and** "matches the censoring probability" to the actual censoring frequency in the data — this is why Tobit's MLE yields a consistent estimator while OLS (which only uses the first term, treating every observation as $Y>0$) does not.

**The general case** (censoring on both sides at $a,b$) extends this idea into three types of contributions: continuous density for $a<Y<b$, probability $\Phi\left(\frac{a-X\beta}{\sigma}\right)$ for $Y=a$, and probability $1-\Phi\left(\frac{b-X\beta}{\sigma}\right)$ for $Y=b$.

**Technical note**: many software packages (including `censReg` in the example above) estimate $\log\sigma$ instead of $\sigma$ directly during numerical optimization — since $\sigma$ must always be positive, estimating $\log\sigma$ (which can take any real value) and then taking $\exp(\cdot)$ at the final step automatically enforces this constraint without needing additional complex constraints in the optimization algorithm (here, Newton-Raphson, 30 iterations).

## Three types of predicted value and marginal effect after Tobit — the hardest part

This is the **most important and most confusable** part of the topic. The root reason: once there is censoring, "the effect of $X$ on $y$" is no longer a SINGLE number as in ordinary OLS ($\beta$) — it splits into **three different questions**, each with a different numeric answer, and exam questions often deliberately ask very specifically which of the three questions is meant, to test whether the learner can tell them apart.

### Latent prediction — $E(y^*\mid X)=X\beta$

This is the effect on the **unobserved latent variable** $y^*$ — i.e. the hidden "borrowing tendency," which can be negative and is not bounded by the 0 threshold.

$$E(y^*\mid X)=X\beta \qquad\Rightarrow\qquad \text{Marginal effect} = \beta \text{ (constant, exactly like ordinary OLS)}$$

**When to use**: when the research question is about the latent "tendency"/"index" itself — e.g. modeling a theoretical concept (creditworthiness, willingness to borrow) for which observed `balance` is just a cut-off manifestation. **This is NOT the effect on the actual credit card balance that an analyst/bank cares about** — it is only the effect on an intermediate mathematical structure. This is exactly why the raw $\beta$ from Tobit output **should not be interpreted directly as a real marginal effect** — the most common exam trap of this section (see section 9).

### Unconditional expected value — $E(y\mid X)$, accounting for the censoring probability

$$E(y\mid X)=\Phi\left(\frac{X\beta}{\sigma}\right)\left(X\beta+\sigma\lambda\right), \qquad \lambda=\frac{\phi(X\beta/\sigma)}{\Phi(X\beta/\sigma)}$$

$\lambda$ here is the **inverse Mills ratio** — although this name is not used directly, this is exactly the mathematical structure that will reappear in the Heckman selection model (section 9).

The corresponding marginal effect:

$$\frac{\partial E(y\mid X)}{\partial X} = \beta\,\Phi\left(\frac{X\beta}{\sigma}\right)$$

**Intuitive meaning**: this is the effect on the **average observed value of the ENTIRE sample** — including those who will (per the model) be censored to 0. In terms of the formula, it is exactly $\beta$ (the latent effect) **multiplied by the probability of not being censored** $\Phi(X\beta/\sigma)$ — always smaller than $|\beta|$ in magnitude (since $0<\Phi(\cdot)<1$), because part of the "latent effect" is "absorbed" by the mass of observations sitting at 0 (they don't respond at all, staying at $y=0$, even though their $y^*$ changed).

**When to use**: when the question is about the **aggregate** — e.g. "if the market-wide average interest rate rises 1%, how much does the average credit card balance per customer (including those with no debt) change?" — suited to questions at the level of **aggregate forecasting/macro-level policy**.

### Conditional expected value — $E(y\mid X, y>0)$, only over the uncensored group

$$E(y\mid X, y>0)=X\beta+\sigma\lambda$$

The corresponding marginal effect:

$$\frac{\partial E(y\mid y>0)}{\partial X}=\beta\left[1-\lambda\left(\lambda+\frac{X\beta}{\sigma}\right)\right]$$

**Intuitive meaning**: this is the effect on the average value **ONLY within the group already known not to be censored** — for the case study, only within the group of 1877 customers who actually have a positive balance. In other words: "among those ALREADY borrowing through their credit card, if their interest rate rises 1%, how much does the average balance of this group alone change?"

**When to use**: when the research question only cares about the **intensive margin** (the degree, within the group already participating) rather than the extensive margin (participating or not) — e.g. a bank wants to know "among customers currently carrying a balance, who will pay more/less if interest rates change," ignoring the question of "who will start/stop carrying a balance."

### (Supplement) Marginal effect on the probability of not being censored

$$\frac{\partial Pr(y>0\mid X)}{\partial X}=\frac{\phi(X\beta/\sigma)}{\sigma}\,\beta$$

This is not the effect on the *value* of $y$, but on the **probability** that $y$ is positive — for the case study: "the effect on the probability a customer carries a balance (rather than paying it off each month)." Structurally, this formula is identical to Probit's marginal effect ([[concepts/binary-response-models]]) applied exactly to the hidden indicator variable "$y^*>0$ or not."

### Illustrative numerical example — four types of effects, same four variables, one table

These numbers are precomputed (in R, at the sample mean $\bar X$) for the credit card balance case study — this is the clearest quantitative example to see just **how different the three types of prediction/marginal effect are for the same variable**:

|Variable |"raw") | Unconditional ME — $\partial E(y\mid X)/\partial X$ | Conditional ME — $\partial E(y\mid y{>}0)/\partial X$ |on $Pr(y>0)$ |
|---|---|---|---|---|
| `interest` (%) | −321.25 | −133.70 | −102.74 | −0.0107 |
|years) | −349.21 | −145.33 | −111.68 | −0.0116 |
| `male` (dummy) | +2531.38 | +1053.51 | +809.53 | +0.0844 |
|years of education) | −941.30 | −391.75 | −301.03 | −0.0314 |

Reading this table along the `interest` row (all evaluated at $\bar X$, i.e. at a customer with sample-average characteristics):

- $\beta_{interest}=-321.25$: this is the effect on the **latent variable** $y^*$ — it has no direct "actual USD balance" unit, since $y^*$ can be negative.
- Unconditional ME $=-133.70$: if interest rises 1 percentage point, **the average balance of ALL 2895 customers** (including the 1018 people currently at `balance=0`) falls by about 133.70 USD, per the estimated model.
- Conditional ME $=-102.74$: if interest rises 1 percentage point, **the average balance ONLY within the group of 1877 customers currently holding a positive balance** falls by about 102.74 USD.
- ME on $Pr(y>0)$ $=-0.0107$: if interest rises 1 percentage point, **the probability that a customer has a positive balance** (rather than `balance=0`) falls by about 1.07 percentage points.

**These three numbers (−321.25, −133.70, −102.74) all describe "the effect of interest" but answer three different questions — and cannot be used interchangeably.** This is exactly the biggest exam trap of the topic.

**A quick self-check** (in the same spirit as the "self-check" in [[concepts/linear-regression-model]] section 7.4): the ratio $\text{Unconditional ME}/\beta$ must be **the same for every variable**, since both share the common factor $\Phi(X\beta/\sigma)$, which depends only on the shared $\bar X$, not on any individual variable. Checking against the table above: $133.70/321.25\approx0.416$; $145.33/349.21\approx0.416$; $1053.51/2531.38\approx0.416$; $391.75/941.30\approx0.416$ — matches for all four variables. This tells us: at a customer with sample-average characteristics, the model-predicted probability of a positive balance is $\Phi(\bar X\beta/\sigma)\approx41.6\%$. Similarly, the ratio Conditional ME$/\beta\approx0.320$ for all four variables.

**A subtle point worth noting**: $41.6\%$ (the predicted probability *at* the average customer $\bar X$) differs from $1877/2895\approx64.8\%$ (the *actual* proportion uncensored in the whole sample). This is not a contradiction — because $\Phi(\cdot)$ is a nonlinear function, "the probability evaluated at the mean of $X$" generally differs from "the mean of the probability evaluated for each individual" (a form of Jensen's inequality). This is also exactly why **both versions** of each marginal effect are computed:

- **"At mean"**: compute the ME formula a single time, plugging in $X=\bar X$ (sample-average characteristics).
- **"Average" (average marginal effect — AME)**: compute the ME formula separately for **each observation** in the sample (using its own $X_i$), then take the average of the $N=2895$ resulting ME numbers.

For this case study, the two versions are close but not exactly identical — e.g. Unconditional ME of `interest`: "at mean" $=-133.70$ USD, "average" $=-136.74$ USD; Conditional ME of `interest`: "at mean" $=-102.74$ USD, "average" $=-107.21$ USD. The difference is small in this example, but in principle it could be much larger if $X$ is widely dispersed — always state clearly which version is being used when reporting results.

### Technical note: p-value of the marginal effect

There is no simple closed-form formula for the standard error/p-value of the ME's above (it requires the **delta method** — an advanced technique, outside the scope of by-hand computation in this course). A common approximation: treat the ratio $ME/SE(ME)$ as standard-normally distributed,

$$z=\frac{ME}{SE(ME)}, \qquad p=2\left(1-\Phi(|z|)\right)$$

## Testing after Tobit: the Likelihood Ratio (LR) test

Since Tobit is estimated by MLE (not OLS), testing **multiple coefficients jointly** does not use the F-test as in [[concepts/linear-regression-model]] section 8, but instead uses the **Likelihood Ratio (LR) test** — comparing the log-likelihood of the full (unrestricted) model against a model forced to exclude the variables being tested (restricted), in the same intuitive spirit as the F-test (if excluding variables causes "goodness of fit" to drop sharply, i.e. log-likelihood drops a lot, then those variables truly matter).

**Illustrative example** (`lmtest::lrtest`, jointly testing `age`, `male`, `edu`):

```
Model 1: balance ~ interest + age + male + edu     (unrestricted, LogLik = -20733, Df = 6)
Model 2: balance ~ interest                          (restricted, LogLik = -20998, Df = 3)

Chisq = 530.58, Df = 3, Pr(>Chisq) < 2.2e-16
```

$H_0: \beta_{age}=\beta_{male}=\beta_{edu}=0$. With $\chi^2=530.58$, $p<2.2\times10^{-16}$ → **strongly reject** $H_0$ → there is evidence that at least one of the three variables (`age`, `male`, `edu`) genuinely contributes to explaining the balance, beyond `interest`.

> Note: the LR test for overall significance (all slope coefficients at once) works the same way — simply put every variable of the model into `lmtest::lrtest`. The same interpretation caveat as the overall F-test in [[concepts/linear-regression-model]] section 8.5 applies: a statistically significant LR test **does not** prove the model is correctly specified, and does not test Tobit's assumptions (especially the normality assumption on $\varepsilon$, which matters far more than in OLS since the entire log-likelihood rests on this assumption).

## Consolidated exam traps — expanded

1. **Running OLS directly on a censored variable** (whether keeping the $y=0$ observations or dropping them) — always yields a biased estimate, regardless of whether the censoring rate is high or low (section 3).
2. **Applying Tobit to truncated data** (not censored) — Tobit is not appropriate, since its likelihood needs to know $X$ for the "cut" observations too, which is not available with truncated data (section 2.4).
3. **Confusing censored with truncated** when reading the exam question — check carefully: does the question say "we still know the characteristics of those excluded/assigned 0" (censored) or "we have absolutely no information about those excluded" (truncated)?
4. **The biggest trap: choosing the wrong type of prediction/marginal effect for the actual research question.** Specifically:
   - Using the raw $\beta$ (latent ME) to answer "the effect on the actual balance" — wrong, because $\beta$ is the effect on $y^*$ (the latent variable, which can be negative), not on the observed $y$. In the example, $\beta_{interest}=-321.25$ while the actual effect on `balance` is only about $-134$ to $-103$ depending on the type.
   - Using **Unconditional ME** when the question only asks about the group **already participating/already past the threshold** (should have used Conditional ME instead), or the reverse — using **Conditional ME** when the question asks about the **aggregate effect over the entire population/market** (should have used Unconditional ME instead). Keywords to catch in the question: "average over the whole sample/population" → Unconditional; "among those who already..." / "given that $y>0$" → Conditional.
   - Confusing **ME on the value of $y$** with **ME on the probability $Pr(y>0)$** — the two quantities have completely different units (USD per percentage point of interest, versus percentage points of probability per percentage point of interest).
5. **Confusing "at mean" and "average" (AME)** when citing a marginal effect number — the two numbers can differ (section 7.5); always state clearly which method was used when reporting.
6. **Treating a statistically significant LR test as "the model is correct/well-specified"** — the same interpretation error as the overall F-test in [[concepts/linear-regression-model]] section 8.5; the LR test does not test model specification or Tobit's normality assumption.
7. **(Scope note)** The Course Outline mentions the Heckman selection model for cases with a truncation/selection element "if time allowed" — but this content is **outside the taught scope** of this course. This concept page therefore stops at Tobit; if supplementary material on Heckman appears later, section 2.4/9 of this page could be expanded.

## Connections to the rest of the course

- The **latent variable** structure $y^*=X\beta+\varepsilon$ with a cut threshold is identical to [[concepts/ordinal-response-models]] — the difference is that Tobit has only one fixed threshold (at 0, or known $a,b$), while the ordinal model has multiple thresholds and those thresholds are usually estimated.
- Clearly distinguishing the **raw coefficient $\beta$ from the true marginal effect** (which always requires multiplying by a density/CDF function, not a constant) is a theme running throughout all of Part 2 — it appears identically in [[concepts/binary-response-models]] (Probit/Logit) and reappears more complex here with THREE types of ME instead of one.
- $\Phi(\cdot)$ and Tobit's "censoring probability" structure share the same mathematical tool (the normal CDF) with Probit in [[concepts/binary-response-models]] — fundamentally, "censored or not" is a hidden binary decision inside Tobit.
- The quantity $\lambda$ (inverse Mills ratio) appearing in the Unconditional/Conditional expected value (sections 7.2–7.3) is the same mathematical structure that will reappear in the **Heckman selection model** — the standard model for handling sample selection/truncation with a systematic element, but **outside the taught scope of this course** (see the scope note in section 9).
- This is the final lesson of **Part 2 (Models for Limited Dependent Variables)** — after this lesson, the course returns to **Panel Data** in Part 3, extending the OLS/panel framework learned in [[concepts/fixed-random-effects-model]] to more complex variance structures.

## Real-world application references

Three recent papers illustrating the Tobit model in real-world economic research (Lecture 13 syllabus):

- Liu, H., Wahl, T. I., Seale, J. L., & Bai, J. (2015). Household composition, income, and food-away-from-home expenditure in urban China. *Food Policy*, 51, 97-103. https://doi.org/10.1016/j.foodpol.2014.12.011
- Basnet, H. C., & Donou-Adonsou, F. (2016). Internet, consumer spending, and credit card balance: Evidence from US consumers. *Review of Financial Economics*, 30, 11-22. https://doi.org/10.1016/j.rfe.2016.01.002
- Jiang, H., Livingston, M., Room, R., & Callinan, S. (2016). Price elasticity of on- and off-premises demand for alcoholic drinks: A Tobit analysis. *Drug and Alcohol Dependence*, 163, 222-228. https://doi.org/10.1016/j.drugalcdep.2016.04.026
