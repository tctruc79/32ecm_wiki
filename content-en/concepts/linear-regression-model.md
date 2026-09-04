---
title: "Lecture 1: Linear Regression Model"
type: concept
status: mature
tags: [linear-regression, ols, hypothesis-testing, foundations]
sources: ["[[sources/slides-1-linear-regression-model]]"]
related: ["[[concepts/econometrics-overview]]", "[[concepts/functional-forms]]", "[[concepts/multicollinearity]]", "[[concepts/heteroskedasticity]]", "[[concepts/endogeneity-iv-regression]]"]
lecture: 1
assignment: []
updated: 2026-09-04
---

> **How to read this page**: this is the foundational page for the entire course — every later topic (Topic 2–14) is a variant of, or a patch for, the model presented here. If you only have time to carefully read one page while reviewing for the exam or thesis, read this one first. The reasoning behind "why we need ceteris paribus, correlation ≠ causation" is discussed in more depth in [[concepts/econometrics-overview]] — this page focuses on the **technical mechanics**: what OLS is, how it is estimated, and how to know whether that estimate is trustworthy.

**Lecture 1** in the syllabus (CO Topic 1) — no dedicated assignment yet.

## Why do we need a "model"? — PRE and SRE

The starting point is not a formula, but an **economic question** that needs to be answered through theory. The example the professor uses as an opener: Mincer (1974) theorized that wages depend positively on education (and possibly work experience too). Econometrics is not "blindly drawing a straight line through data points" — it is a tool to **test and quantify** an existing theory.

To test the idea "education → wages," we formalize it into an equation:

$$y_i = \beta_0 + \beta_1 X_{1i} + \beta_2 X_{2i} + \cdots + \beta_k X_{ki} + \varepsilon_i$$

This is called the **Population Regression Equation (PRE)** — the equation at the **population** level, i.e. the "true" theoretical relationship we want to know but can never observe directly, since no one has data on the *entire* population. Each component:

- $y_i$: the dependent variable (outcome) of individual/unit $i$ — for example, wages.
- $X_{1i}, X_{2i}, \dots$: the independent variables, which must have a **theoretical basis** (not just thrown in arbitrarily) — for example, years of schooling, years of experience.
- $\beta_0$: the intercept — the expected value of $y$ when all $X=0$.
- $\beta_1, \beta_2, \dots$: the slope coefficients — also called **marginal effects**, measuring the change in $y$ when the corresponding $X$ increases by 1 unit, holding other variables constant.
- $\varepsilon_i$: the error term — every influence on $y_i$ that the model **cannot observe**.

Because $\beta$ can never be observed directly, in practice we only have a **sample** of data, and we use it to estimate. The corresponding equation at the sample level:

$$y_i = b_0 + b_1 X_{1i} + \cdots + b_k X_{ki} + e_i, \qquad e_i = y_i - \hat y_i$$

is called the **Sample Regression Equation (SRE)**. The core difference to keep in mind:

| |Level |Coefficient notation |Error/residual notation |Observable? |
|---|---|---|---|---|
| PRE |Population |$\beta$ (Greek) | $\varepsilon$ |No — exists only in theory |
| SRE |Sample |$b$ (Latin, sometimes written $\hat\beta$) |$e$ (residual) |Yes — computable from data |

$b$ is precisely the **best guess** of the unobserved $\beta$, based on the sample data at hand. The next, natural question: **how do we estimate $b$?**

## The OLS Estimator — intuition first, formula second

### Intuition

For any choice of $b$, we can compute the predicted value $\hat y_i = bX_i$ for each observation and compare it to the true value $y_i$. The distance between these two values is the **residual**:

$$e_i = y_i - \hat y_i = y_i - bX_i$$

Picture it on a graph: this is exactly the vertical gap between the true data point and the regression line. **OLS (Ordinary Least Squares)** chooses $b$ so that these gaps, taken together across the whole sample, are **as small as possible**:

$$\min_b \sum_{i=1}^N e_i^2 = \sum_{i=1}^N (y_i - bX_i)^2$$

Why **square** the residuals instead of summing them directly or taking absolute values? Two intuitive reasons: (1) if summed directly, positive and negative residuals would cancel each other out, so a "bad" line (deviating a lot but evenly on both sides) could look like a "good" line; (2) squaring penalizes large errors more heavily — one observation that deviates far is penalized much more than many observations that deviate slightly, which matches the intuition of "wanting the predicted line to track the data closely overall".

### Closed-form solution (graduate level)

Rewrite the minimization problem in matrix form, with $e'e$ as the sum of squared residuals:

$$e'e = (y-Xb)'(y-Xb) = y'y - 2bX'y + b'X'Xb$$

Take the derivative with respect to $b$ and set it to 0 to find the minimum (the first order condition):

$$\frac{\partial e'e}{\partial b} = -2X'y + 2X'Xb = 0 \;\;\Rightarrow\;\; X'Xb = X'y$$

Solving gives the closed-form solution — this is precisely the **OLS estimator**:

$$b = (X'X)^{-1}X'y$$

There's no need to memorize the derivation if you haven't studied matrix algebra in depth — what matters is remembering that OLS is not an arbitrary "trick," but the **unique solution** to the optimization problem of "minimizing the sum of squared residuals." The condition for this solution to exist (the matrix $X'X$ being invertible) is precisely the content of assumption A2 below.

## Running example: Forest coverage & Storm damages

This is the dataset Professor Thụy uses throughout the Topic 1 slides to illustrate every concept — it's important to understand it in order to follow the numerical examples in later sections.

**Research context**: storm damage causes major losses for communities. There are two groups of policy levers: natural protection (forest) and human preparedness (response plans). Forests are expected to reduce damage because they block wind/flooding; response plans (early warning, evacuation plans) are also expected to reduce damage.

> Note from the original slide: the variables in this dataset were constructed based on disaster economics research but have been simplified — the data serves teaching purposes only and may omit explanatory variables that matter in practice. Variable names also follow the course's own technical convention, not a recommended naming scheme for your real-world work.

**Unit of analysis**: communities that experienced at least 1 storm in the past year.

|Variable |Meaning |Unit |Causal or non-causal? |
|---|---|---|---|
| `pdamages` |Property damage (excluding loss of life) — **dependent variable** |thousand USD | — |
| `aforest` |Forest coverage area | ha | **Causal** |
| `dplan` |Whether the community has a response plan (early warning, evacuation…) | dummy (1/0) | **Causal** |
| `cgdp` |GDP per capita |thousand USD/year | Non-causal |
| `pdens` |Population density |thousand people/km² | Non-causal |
| `curban` |Whether the community is urban | dummy (1/0) | Non-causal |
| `cterrain` |Terrain: lowland (base), highland, coastal → generates 2 dummies `chighland`, `ccoastal` | categorical | Non-causal |

Distinguishing **causal vs. non-causal** here is not arbitrary — it determines the *language* allowed when interpreting coefficients (see section 5). `aforest` and `dplan` are treated as causal because the slide assumes a direct causal mechanism that is theoretically plausible (forest physically blocks wind/flooding; a response plan physically reduces losses); the remaining variables are merely **controls** — included to "clean up noise" rather than being the object of study.

**Notable descriptive statistics** (to get a feel for the scale before reading the regression coefficients):

- `pdamages`: ranges 38–116 (thousand USD) — some communities suffer far more damage than others.
- `aforest`: mean ≈ 1.51 ha, ranging 0–6.3 — some communities have no forest at all, others have substantial forest coverage.
- `dplan`: only 28% of communities have a response plan.

**Full OLS regression results** (this table of numbers will be reused throughout the t-test and F-test sections below):

|Variable |Estimated coefficient ($b$) |Matches theoretical expectation? |
|---|---|---|
| `aforest` (causal) | −5.363 |✅ more forest → less damage |
| `dplan` (causal) | −1.99 |✅ having a response plan → less damage |
| `cgdp` (non-causal) | +0.450 |✅ higher GDP → higher damage (more assets to lose) |
| `pdens` (non-causal) | −2.62 |❌ contrary to the initial expectation (higher density yet lower damage) |
| `curban` (non-causal) | +0.426 | — |
| `chighland` (non-causal) | −0.194 | — |
| `ccoastal` (non-causal) | +2.24 |✅ coastal areas are more exposed to storms |

OLS only gives us **these numbers** — it doesn't yet tell us which numbers are "statistically reliable." That is why we need the OLS assumptions (section 4) and hypothesis tests (sections 6–8).

## The five OLS assumptions (A1–A5) — the "rules of the game"

OLS always produces a number $b$, regardless of whether the data is good or bad — the question is whether that number is **trustworthy**. Assumptions A1–A5 are exactly the "rules of the game" that determine this, along three dimensions:

- **Consistency**: as sample size → ∞, the estimate converges to the true value. In other words — the more data, the closer the estimate gets to reality.
- **Efficiency**: among unbiased estimators, the one with the smallest variance is the most efficient — it uses the data in the "best" way, producing the most precise, most accurate estimate.
- **Inference**: allows t-tests, F-tests, and confidence intervals to be constructed reliably.

| # |Assumption |Content |If violated |
|---|---|---|---|
| A1 | **Linearity** |The model is linear in the **parameters** $\beta$ (the $X$ variables can be nonlinear — quadratic, log-log — as long as $\beta$ still enters linearly) |See [[concepts/functional-forms]] |
| A2 | **Full rank** |The columns of matrix $X$ are linearly independent (no variable is a perfect linear combination of the others) |Perfect collinearity → $X'X$ is not invertible → $b$ cannot be determined (the formula $b=(X'X)^{-1}X'y$ "breaks"); imperfect collinearity (near-collinear) → see [[concepts/multicollinearity]] |
| A3 | **Exogeneity** | $E(\varepsilon\|$E(\varepsilon\|X)=0$ — the error term carries no systematic information related to $X$, equivalently $X'E(\varepsilon)=0$ |If violated → **endogeneity**, see [[concepts/endogeneity-iv-regression]] |
| A4 | **Homoskedasticity** | $Var(\varepsilon\|X) = E(\varepsilon\varepsilon'\|$Var(\varepsilon\|X) = E(\varepsilon\varepsilon'\|X) = \sigma^2 I$ — the error variance is constant across observations |If violated → see [[concepts/heteroskedasticity]] |
| A5 | **Normality** | $e \sim N(0,\sigma^2)$ |Needed for exact inference in small samples; in large samples the Central Limit Theorem means A5 is not required |

**A quick way to remember, by the "value" each assumption provides**: A1–A3 ensure consistency; A4 adds efficiency (and simplifies the variance/VCV formula — see section 7); A5 allows exact inference in small samples. In practice, **A3 and A4 are the two assumptions most often violated** — this is exactly why the course goes on to teach **robust standard errors** (patching A4) and **instrumental variable (IV) regression** (patching A3) in later topics.

## Interpreting regression coefficients

How to read a coefficient $b_j$ depends on the **type of variable**:

- **Continuous variable** (e.g. `aforest`, `cgdp`): $b_j$ is the change in $y$ when the independent variable increases by 1 unit, holding other variables constant.
- **Dummy variable** (e.g. `dplan`, `curban`): $b_j$ is the **difference** in average $y$ between the group valued 1 and the group valued 0.
- **Categorical variable** (e.g. `cterrain`): each generated dummy (`chighland`, `ccoastal`) measures the difference in $y$ between the group in question and the **base category** (here, `lowland`).

And a second, **independent** set of rules from the variable type above — the rules about **interpretive language**:

- **Causal** variables → may be interpreted using causal language ("decreases," "increases," "causes").
- **Non-causal** variables → may only be interpreted using associative language ("is associated with") — **never** use "cause," no matter how statistically significant the coefficient is.

**Correct/incorrect examples — this is the professor's most common exam trap, recurring throughout most of the later topics:**

- ✅ (causal, `aforest`): "The data show evidence that increasing forest by 1 ha decreases damage by 5.363 thousand USD, on average."
- ✅ (causal, `dplan`): "There is evidence that having a response plan decreases storm damage by 1.99 thousand USD, on average."
- ✅ (non-causal, `cgdp`): "There is evidence that a community with GDP per capita 1 thousand USD higher is associated with damage that is 0.45 thousand USD higher, on average."
- ✅ (non-causal, `curban`): "There is evidence that urban communities experience storm damage that is on average 0.426 thousand USD higher than rural communities."
- ✅ (non-causal, `ccoastal`, acceptable): "Coastal communities have storm damage that is on average 2.24 thousand USD higher than lowland communities."
- ❌ (proof claim): "The data **prove** that being coastal increases damage by exactly 2.24 thousand USD." — wrong because no test can "prove" anything absolutely, only provide "evidence."
- ❌ (causal claim for a non-causal variable): "Being coastal **increases** damage." — wrong because `ccoastal` is a non-causal variable; even though the coefficient is positive and statistically significant, one may only say it "is associated with" damage.

## Uncertainty of the estimate: the VCV matrix and Standard Error

Before hypothesis testing, we need an intermediate question: OLS gives us a number $b$ (a point estimate), but if we drew a **different** sample of data (same population, different observations), $b$ would come out **different**. So how do we measure this degree of "fluctuation"?

### Variance-covariance (VCV) matrix — graduate level

$$Var(b) = \sigma^2(X'X)^{-1} = \begin{pmatrix} Var(b_1) & \cdots & Cov(b_1,b_k) \\ \vdots & \ddots & \vdots \\ Cov(b_k,b_1) & \cdots & Var(b_k) \end{pmatrix}, \qquad \hat\sigma^2 = \frac{e'e}{n-k}$$

This is a $k\times k$ matrix: the diagonal elements are the variances of each $b_j$; the off-diagonal elements are the covariances between pairs of estimates. This simple formula $\sigma^2(X'X)^{-1}$ **only holds under assumption A4 (homoskedasticity)** — this is why A4 matters: it simplifies the VCV/SE formula considerably; when A4 is violated, robust SE must be used instead (see [[concepts/heteroskedasticity]]).

### Standard Error (SE) — and why it differs from Standard Deviation (SD)

$$SE(b_j) = \sqrt{Var(b_j)}$$

This is the point beginners confuse most often: **SD and SE measure two different things**.

- **Standard Deviation (SD)**: measures the dispersion of the **observed data** ($y$, $X$) — for example, the SD of `pdamages` tells us how much or how little damage varies *across communities* in the sample.
- **Standard Error (SE)**: measures the dispersion of the **estimate** $b$ *if the sampling were repeated many times* — the SE of $b_{aforest}$ tells us how much the estimated forest effect would fluctuate if we drew a different sample of data from the same population.

A small SE → a precise estimate; a large SE → a "noisy," less reliable estimate. SE is exactly the "measure of uncertainty" used in every hypothesis test in the following sections.

## Hypothesis testing for a single coefficient: the t-test

### Why we use the language of "evidence" instead of "proof"

In statistics, we can **never prove** a theory to be absolutely true — because that would require absolute certainty, while sample data always contains random noise. Instead, we look for **evidence against** the opposite hypothesis. Specifically, to find out "does X affect Y?", we test the opposite hypothesis — **no effect** — called the **null hypothesis** $H_0$; its opposite is the **alternative hypothesis** $H_a$: X has an effect. If the data allow us to **reject** $H_0$, we say there is evidence supporting $H_a$ — we **never** say "we have proven $H_a$ is true."

The deeper reason: every statistical test is based on probability. Even when we reject $H_0$, there is always a small probability that we are wrong — mistakenly rejecting an $H_0$ that is actually true, called **Type I error**.

> **The professor's metaphor** (worth remembering since it recurs throughout the course): rejecting $H_0$ is like finding a fingerprint at the crime scene — strong evidence the suspect is not innocent, but not "absolute proof" of guilt. **Failing to reject** $H_0$ is like finding no fingerprint — it does not mean the suspect is innocent, only that there isn't enough evidence to convict.

### Formula and distribution

Testing $H_0: \beta_j = c$ against $H_a: \beta_j \neq c$ (the most general form; the most common case is $c=0$, i.e. "this variable has no effect at all"). The test statistic:

$$t = \frac{b_j - c}{SE(b_j)} \sim t_{N-k}$$

The t-statistic measures the distance between the estimate $b_j$ and the hypothesized value $c$, expressed in **SE units** — the larger |t| is, the more unusually "far" $b_j$ is from $c$ (unlikely to occur by chance), and the stronger the evidence against $H_0$. Under $H_0$ being true and assumptions A1–A5 holding, $t$ follows a Student's t distribution with degrees of freedom $df=N-k$ ($N$ = number of observations, $k$ = number of estimated coefficients including the intercept).

Because $\beta_j$ (the true value) is unobservable, we must use the estimate $b_j$ and its SE to compute the test statistic — this is why both the t-test and the F-test are always built on $b$, never directly on $\beta$.

### Three forms of the test — and why the direction of $H_a$ matters

The same t-statistic can lead to **three different conclusions**, depending on what question $H_a$ poses. Illustrated with $b_{aforest}$ itself (t = −16.567, $df=945$):

**(a) Two-tailed test** — the question "does X have any effect at all, regardless of direction?" ($H_0: \beta=0$ vs. $H_a: \beta\neq0$). Reject if $|t|>t^*$.
- With $\alpha=5\%$, $df=945$: $t^*=1.96$.
- $|-16.567| > 1.96$ → **reject** $H_0$.
- Conclusion: there is evidence that forest coverage affects storm damage (direction unspecified).

**(b) Right-tailed test** — the question "does X **increase** Y?" ($H_0: \beta\le0$ vs. $H_a: \beta>0$). Reject if $t>t^*$.
- With $\alpha=5\%$, $df=945$ (one-tailed): $t^*=1.65$.
- $t=-16.567$, is **not** greater than $1.65$ → **fail to reject** $H_0$.
- Conclusion: forest coverage does **not** increase damage — (makes sense, since the coefficient is negative, not positive).

**(c) Left-tailed test** — the question "does X **decrease** Y?" ($H_0: \beta\ge0$ vs. $H_a: \beta<0$). Reject if $t<-t^*$.
- $t=-16.567 < -1.65$ → **reject** $H_0$.
- Conclusion: there is evidence that forest coverage **decreases** damage — consistent with the original theoretical expectation.

**The most important lesson from this example**: the *same* t-statistic (−16.567) yields three different conclusions depending on what question ($H_a$) is posed. Choosing the wrong test form (e.g. using right-tailed for an effect that is actually negative) leads to the conclusion "no evidence" even though there actually *is* evidence — just evidence for the opposite direction of the question posed. Always pose the research question **first**, then choose the corresponding test form — never choose the test form after having seen the sign of the coefficient (that is p-hacking).

### p-value

**Definition**: the p-value is the probability of observing a test statistic **at least as extreme as** the one observed, *given that* $H_0$ is true. The smaller the p-value → the less likely it is to occur if $H_0$ is true → the stronger the evidence against $H_0$. **Decision rule**: reject $H_0$ when p-value $<\alpha$.

**Example 1 — two $\alpha$ thresholds yield two different conclusions** ($b_{pdens}$, two-tailed, $H_0:\beta_{pdens}=0$): $t=-1.932$, p-value $=0.0537$.

- Direct interpretation of the number: if the true effect of population density is 0, the probability of observing a t-statistic as extreme as $-1.932$ (or more) is only about 5.4%.
- At $\alpha=5\%$: $0.0537 > 0.05$ → **fail to reject** $H_0$.
- At $\alpha=10\%$: $0.0537 < 0.10$ → **reject** $H_0$.
- Lesson: the conclusion of "statistically significant or not" **depends on the $\alpha$ threshold chosen in advance** — a result may be "significant at 10%" but "not significant at 5%." Always state clearly which $\alpha$ is being used.

**Example 2 — one-tailed p-values, same variable, two opposite directions** ($b_{cgdp}$, $t_{obs}=2.113$, $df=945$):

- Right-tailed ($H_0:\beta_{cgdp}\le0$ vs. $H_a:\beta_{cgdp}>0$): p-value $=0.017 < 0.05$ → **reject** $H_0$ → there is evidence that communities with higher GDP per capita experience higher storm damage.
- Left-tailed ($H_0:\beta_{cgdp}\ge0$ vs. $H_a:\beta_{cgdp}<0$, same $t_{obs}=2.113$): p-value $=0.9826 > 0.05$ → **fail to reject** $H_0$ → not enough evidence that higher GDP goes with lower damage.
- Technical note: the two opposite one-tailed p-values ($0.017$ and $0.9826$) for the same $t_{obs}$ always sum to approximately 1 (here $0.017+0.9826=0.9996\approx1$, the small discrepancy due to rounding) — a quick self-check when calculating by hand.

### Testing with $c\neq0$ — testing a specific claim, not just "is there an effect"

The general form $H_0:\beta_j=c$ is useful when the research question is a **specific quantitative claim**, not just "is there an effect" — this is precisely the kind of question that comes up when writing a thesis ("whether the effect is exactly equal to/greater than/less than a specific threshold according to theory or prior research").

**Example**: "Does each ha of forest reduce damage by exactly 5 thousand USD?" — i.e. $c=-5$ (not $c=0$).

$$t_{obs} = \frac{b_{aforest}-c}{SE} = \frac{-5.363-(-5)}{0.32} \approx -1.12$$

- **Two-tailed** ($H_0:\beta=-5$ vs. $H_a:\beta\neq-5$): p-value $=0.26>0.05$ → fail to reject $H_0$ → the data are **consistent** with the hypothesis "each ha of forest reduces damage by exactly 5 thousand USD".
- **Right-tailed** ($H_0:\beta\le-5$ vs. $H_a:\beta>-5$, i.e. testing "reduces by less than 5 thousand USD"): p-value $=0.868>0.05$ → fail to reject → the data are consistent with "each ha of forest reduces damage by **at least** 5 thousand USD".
- **Left-tailed** ($H_0:\beta\ge-5$ vs. $H_a:\beta<-5$, i.e. testing "reduces by more than 5 thousand USD"): p-value $=0.131>0.05$ → fail to reject → the data are consistent with "each ha of forest reduces damage by **at most** 5 thousand USD".

**Key interpretive lesson**: all three conclusions above are "fail to reject $H_0$" — but **failing to reject does not mean $H_0$ has been proven true**, it only means the data are **consistent** with that hypothesis, while still potentially being consistent with many other hypotheses. This is the most common interpretive error in thesis writing: turning "failed to reject" into "confirmed."

## Testing multiple coefficients jointly: the F-test

### Why we need the F-test

The t-test only handles **one coefficient at a time**. But many research questions require testing **several coefficients simultaneously** — for example: "does terrain affect storm damage at all?" — this question involves **both** dummies `chighland` and `ccoastal` at once, not each one separately.

$$H_0: \beta_{chighland} = \beta_{ccoastal} = 0 \qquad H_a: \text{ít nhất một hệ số} \neq 0$$

### Formula

Compare two models: **unrestricted** (the full model, with all variables) and **restricted** (the model with the coefficients under test forced to the value hypothesized in $H_0$ — usually 0).

$$F = \frac{(RSS_r - RSS_u)/q}{RSS_u/(N-k)} \sim F_{q,\,N-k}$$

- $RSS_r$: the residual sum of squares (RSS) of the **restricted** model.
- $RSS_u$: the RSS of the **unrestricted** model.
- $q$: the number of coefficients being tested jointly (in the example above, $q=2$).

**Intuition**: if forcing the coefficients to 0 makes RSS increase **a lot** ($RSS_r$ much larger than $RSS_u$), it means those variables really do contribute to explaining $y$ → evidence against $H_0$ → a large F. If forcing them to 0 leaves RSS nearly unchanged, those variables "aren't doing much" → a small F, $H_0$ cannot be rejected.

### General form — not just testing "= 0"

The F-test can test **any linear restriction** on the coefficients, not just forcing them to 0:

$$H_0: R\beta = r$$

where $R$ is the restriction matrix and $r$ is a constant vector. Two illustrative examples (question forms commonly seen in empirical thesis work):

- **Constant returns to scale** (a production-function model): $H_0: \beta_K + \beta_L = 1$.
- **Equality of effects** (two variables having equal effects): $H_0: \beta_{aforest} = \beta_{dplan}$ — for example, testing whether 1 ha of forest and 1 unit of "having a response plan" reduce damage by the same amount.

### Interpreting F-test results — a correct/acceptable/wrong table

This is the part of the whole F-test section richest in exam traps, so it is presented as a comparison table:

**When the F-test is statistically significant:**

|Statement |Correct/Wrong |Why |
|---|---|---|
|"There is sufficient evidence that at least one of the coefficients under test is nonzero." |✅ Correct |This is exactly what the F-test tests |
|"The test result proves both coefficients are statistically nonzero." |❌ Wrong |The F-test only says "at least one," not "both" — to know about each coefficient individually, one must go back to the t-test for each variable |

**When the F-test is not statistically significant:**

|Statement |Correct/Wrong |Why |
|---|---|---|
|"There is not enough reliable evidence that this group of variables has a joint effect." |✅ Correct |Accurate interpretation |
|"It has been proven that both coefficients are individually nonzero." |❌ Wrong |Completely contrary to the result — an insignificant F-test means there is *no* evidence, let alone "proof" |

### Special case: the F-test for overall significance

A special case when $q=k$ (testing **all** slope coefficients jointly, excluding the intercept):

$$H_0: \beta_1=\beta_2=\cdots=\beta_k=0$$

A statistically significant F here **only** tells us: the explanatory variables are **not all** meaningless — it **cannot** test (and therefore **must not** be interpreted as):

- Whether the model has the **correct specification** — correct functional form, no important omitted variables, linear in parameters.
- Whether the chosen variables are the "right" ones to include — variable selection must be based on **theory**, not on the F-test.
- Whether the OLS assumptions (A1–A5) are satisfied — the F-test does not check exogeneity, homoskedasticity...
- Whether the model is **useful for forecasting or policy** — the F-test does not measure forecast accuracy or policy relevance.

In short: **"the F-test is significant" ≠ "the model is appropriate"** — this is one of the most overused phrases when writing up research results, even in published papers.

## R² and Adjusted R² — measuring fit, not correctness

$$R^2 = 1 - \frac{RSS}{TSS}, \qquad TSS=\sum_{i=1}^N y_i^2 - \frac{\left(\sum_{i=1}^N y_i\right)^2}{N}, \qquad 0 \le R^2 \le 1$$

$R^2$ measures the **proportion of variation in $y$ explained by the regression model**. The closer to 1, the more variation in the data the model explains; the closer to 0, the less it explains.

**The problem**: $R^2$ **never decreases** when a variable is added to the model — even when that variable is completely meaningless in theory. This makes $R^2$ unfair when comparing two models with **different numbers of variables** — a model with more variables always has $R^2$ ≥ a model with fewer variables, even though it isn't actually "better."

**Solution — Adjusted R²**, which penalizes added variables:

$$R^2_{adj} = 1-(1-R^2)\frac{n-1}{n-k}$$

Unlike ordinary $R^2$, $R^2_{adj}$ **can decrease** if a newly added variable doesn't contribute enough to offset the "penalty" of losing an additional degree of freedom. This makes $R^2_{adj}$ a more appropriate measure when **comparing models with different numbers of variables**.

**The most important point to remember**: both $R^2$ and $R^2_{adj}$ only measure **fit** — how closely the model "traces" the observed data — they do **not** measure the **validity** of the estimated coefficients at all. A model can have a very high $R^2$ but coefficients that are completely biased due to a violation of A3 (endogeneity); conversely, a model with low $R^2$ can still yield accurately estimated $\beta$ coefficients if the assumptions are satisfied. **A high $R^2$ is not the goal of econometrics** — the goal is to correctly estimate the causal/associative effect that the research sets out to answer.

## Summary of exam traps

1. Interpreting a **non-causal** variable's coefficient using causal language ("causes," "increases/decreases") instead of associative language ("is associated with").
2. Using the word "prove/proof" instead of "there is evidence" — applies to both the t-test and F-test, no exceptions.
3. Treating "fail to reject $H_0$" as "$H_0$ has been proven true" — it only means "the data are consistent with $H_0$," without ruling out other hypotheses.
4. Treating a statistically significant overall F-test as meaning "the model is correct/appropriate" — the F-test does not check model specification, does not check the OLS assumptions, and does not measure usefulness for forecasting/policy.
5. Comparing $R^2$ (rather than $R^2_{adj}$) between two models with different numbers of variables.
6. Choosing the test direction (two-/right-/left-tailed) **after** seeing the sign of the estimated coefficient, instead of posing the research question first and then choosing the test form — this is a form of p-hacking.
7. Confusing Standard Error (the uncertainty of the estimate $b$ across different samples) with Standard Deviation (the dispersion of the data itself).
8. Interpreting "the F-test for a group of variables is significant" as "every coefficient in the group is individually significant" — the F-test only guarantees "at least one."

## Connections to the rest of the course

This is the foundational model — every violation of assumptions A1–A4 opens up its own topic in the course:

- **A1 (Linearity)** is relaxed toward nonlinear forms → [[concepts/functional-forms]].
- **A2 (Full rank)** is nearly violated (imperfect collinearity) → [[concepts/multicollinearity]].
- **A3 (Exogeneity)** is violated → endogeneity → [[concepts/endogeneity-iv-regression]] (and extended to panel data in [[concepts/iv-regression-panel-data]]).
- **A4 (Homoskedasticity)** is violated → [[concepts/heteroskedasticity]].
- The entire PRE/SRE, OLS, t-test, F-test framework on this page is also **extended to data with a time dimension** in [[concepts/fixed-random-effects-model]] (panel data) and **to non-continuous dependent variables** in [[concepts/binary-response-models]] and related pages.

The foundational philosophical question "why do we need to identify the causal effect, not just compute a coefficient" is discussed in depth in [[concepts/econometrics-overview]] — worth reading alongside this page if you need to review the big picture before diving into individual techniques.

## Real-world application references

Three recent papers illustrating how the linear regression model is used in real-world economic research (Lecture 1 syllabus):

- Peng, Y., Yang, J., Shen, J., & Gou, Q. (2025). Financial outreach, bank deposits, and economic growth. *Journal of Economic Behavior & Organization*, 171, 105036. https://doi.org/10.1016/j.jedc.2025.105036
- Su, Y., Huang, Q., Shu, Q., Wang, Y., & Qi, X. (2025). Mechanism of land trusteeship promoting farmers' collective action: A study based on social-ecological systems framework. *Journal of Rural Studies*, 116, 103622. https://doi.org/10.1016/j.jrurstud.2025.103622
- Yokying, P. (2025). Domestic and international migration, landownership, and rice farming in Cambodia. *Journal of Rural Studies*, 114, 103532. https://doi.org/10.1016/j.jrurstud.2024.103532
