---
title: "Multicollinearity"
type: concept
status: mature
tags: [multicollinearity, vif, linear-regression, model-diagnostics]
sources: ["[[sources/slides-3-multicollinearity]]"]
related: ["[[concepts/linear-regression-model]]"]
updated: 2026-08-29
---

> **How to read this page**: multicollinearity is the first "bug-fix" issue in the course's topic sequence — it relates to assumption **A2 (Full rank)** of [[concepts/linear-regression-model]], but only in a "near-violation" form, not a full violation. You should reread section 4 (the five OLS assumptions) and sections 6–7 (VCV matrix, Standard Error, t-test) of that page first, because every consequence of multicollinearity on this page only makes sense once you understand what SE and the t-statistic actually measure.

## Intuition: what multicollinearity is — and is NOT

The most common point of confusion for beginners: multicollinearity is **not** about an independent variable ($X$) correlating with the dependent variable ($y$) — that is actually **desirable**, indeed the very reason we include $X$ in the model in the first place. Multicollinearity is about **two (or more) independent variables being strongly correlated with EACH OTHER**.

A concrete example — taken directly from the case study running through this page (section 4 below): in a 2020 survey of 470 married couples in Ho Chi Minh City, wife's age (`age_wife`) and husband's age (`age_husband`) correlate at $r=0.921$ (section 8.1) — which makes sociological sense: people tend to marry someone of a similar age. Both variables could plausibly have their own effect on household expenditure (`expense`), but because they almost always "move together" in the sample (a household with an older wife almost certainly also has an older husband), OLS has almost no **independent variation** left to disentangle: did expenditure rise because the wife is older, because the husband is older, or both? The result (see the actual numbers in section 5): the model can still be estimated, but the separate estimates for each age variable are very "shaky," not confident enough to reject the hypothesis that the coefficient is zero — even though, in theory, age could well affect expenditure.

**Visual metaphor**: picture two highly correlated independent variables as two Venn diagram circles that overlap almost completely. Each variable's "unique, non-overlapping information" (the non-overlapping sliver) is very small — and OLS can only use that *unique* sliver of information to estimate each variable's *own* coefficient. The overlapping part (the shared information, where both variables move together) does not help distinguish which variable's effect is which — it is "wasted" in a statistical sense.

## Perfect collinearity vs. Imperfect collinearity (multicollinearity)

The Classical Linear Regression Model (CLRM) assumes **A2 — Full rank**: no perfect linear relationship among the regressors. The slide clearly distinguishes two types of collinearity, and this is a point that's often conflated during exam review:

- **Perfect collinearity**: a **perfect** linear relationship between 2+ variables (e.g., $X_2=2X_1$ holding for *every* observation). This is a **complete** violation of A2 — not "an issue to weigh" but a **technical error that stops the model from running at all**.
- **Imperfect collinearity (multicollinearity)**: the regressors are highly correlated but **not perfectly** — the model still estimates normally, just less reliably (larger SE). This is a "near-violation" of A2, not a full violation.

### Why perfect collinearity "breaks" OLS — an algebraic proof

With $y=\beta_0+\beta_1X_1+\beta_2X_2$ and $X_2=2X_1$ (a perfect linear relationship), substituting into the model:

$$y=\beta_0+\beta_1X_1+\beta_2(2X_1)=\beta_0+(\beta_1+2\beta_2)X_1=\beta_0+\gamma X_1, \qquad \gamma=\beta_1+2\beta_2$$

The original model "collapses" into a model with only one variable $X_1$ and coefficient $\gamma$. The problem: for **one** estimated value of $\gamma$, there are **infinitely many** pairs $(\beta_1,\beta_2)$ satisfying the equation $\gamma=\beta_1+2\beta_2$. The slide illustrates this with $\gamma=1$:

- if $\beta_1=2$ then $\beta_2=-0.5$;
- if $\beta_1=3$ then $\beta_2=-1$;
- … (and infinitely many other pairs).

There is no unique solution → $\beta_1,\beta_2$ are **individually unidentifiable** → in matrix terms, $X'X$ becomes **non-invertible** (uninvertible), so the OLS estimator formula $b=(X'X)^{-1}X'y$ (see [[concepts/linear-regression-model]] section 2.2) cannot be computed. The required fix: **one of the two perfectly collinear variables must be dropped** — there is no option to "keep both and accept some error".

Quite unlike perfect collinearity, **imperfect collinearity (multicollinearity)** does not make $X'X$ non-invertible — the OLS formula still produces a normal value of $b$. The problem lies in the **reliability** of that value, not in whether it can be computed at all. The rest of this page is about this case.

## Sources of multicollinearity

The slide lists four mechanisms that make regressors highly correlated in practice:

1. **Inherent relationships**: some variables are naturally correlated with each other — e.g., education and income; the labor and capital inputs in a production function.
2. **Repeated measures**: using multiple variables to measure the same concept, or closely related concepts — e.g., assets and income.
3. **Sampling issue**: the way data is collected from a population where some variables already naturally co-vary can inadvertently create multicollinearity in the sample.
4. **Mathematical derivation**: a variable is created directly from another variable — e.g., using both a variable and its square in the same model. This connects directly to the quadratic form of [[concepts/functional-forms]]: when both $X$ and $X^2$ are included in the same model to capture a nonlinear effect, these two variables are almost certainly highly correlated.

## Running example: Household Expenditure Survey (Married Couples, Ho Chi Minh City, 2020)

This is the dataset Professor Thụy uses to illustrate the entire process of detecting and addressing multicollinearity — from here on, every number on this page is taken from this case study.

**Unit of analysis**: households that are married couples, surveyed in 2020 in Ho Chi Minh City. Data source: `https://econometrics.site/public/mcl.csv`.

|Variable |Meaning |Unit |
|---|---|---|
| `expense` |Household expenditure — **dependent variable** |million VND/month |
| `income` |Monthly household income |million VND/month |
| `age_wife` |Wife's age (or female partner) |years |
| `age_husband` |Husband's age (or male partner) |years |
| `hhsize` |Household size |number of members |
| `children` |% of children in the household |percent |

> Note from the slide: observations with NA values and households with `income = 0` were removed, leaving $n=470$ observations.

**Descriptive statistics** (after cleaning, $n=470$ for every variable):

|Variable | mean | sd | median | min | max |
|---|---|---|---|---|---|
| `expense` | 12.02 | 11.16 | 10.0 | 1.0 | 180.00 |
| `income` | 17.03 | 17.00 | 12.5 | 0.4 | 180.00 |
| `age_wife` | 44.91 | 10.86 | 45.0 | 22.0 | 86.00 |
| `age_husband` | 48.36 | 10.73 | 49.0 | 26.0 | 84.81 |
| `hhsize` | 4.72 | 2.32 | 4.0 | 1.0 | 25.00 |
| `children` | 7.88 | 13.06 | 0.0 | 0.0 | 60.00 |

## Full OLS regression results — the consequence, visible right away

Estimated model: $\log(\text{expense}) = \beta_0+\beta_1\log(\text{income})+\beta_2\,\text{age\_wife}+\beta_3\,\text{age\_husband}+\beta_4\,\text{hhsize}+\beta_5\,\text{children}+\varepsilon$

|Variable | $b$ | SE | $t$ | $p$-value |Significance (5%) |
|---|---|---|---|---|---|
| (Intercept) | 0.8105 | 0.1649 | 4.916 | 1.23e-06 | *** |
| `log(income)` | 0.4231 | 0.0297 | 14.240 | < 2e-16 | *** |
| `age_wife` | 0.0066 | 0.0054 | 1.236 | 0.2172 |no |
| `age_husband` | −0.0053 | 0.0054 | −0.980 | 0.3277 |no |
| `hhsize` | 0.0720 | 0.0097 | 7.400 | 6.46e-13 | *** |
| `children` | 0.0036 | 0.0018 | 2.007 | 0.0453 | * |

$n=470$; Residual SE $=0.4821$ on $464$ degrees of freedom; $R^2=0.3829$; $R^2_{adj}=0.3762$; $F=57.57$ on $(5,464)$ df, $p<2.2\times10^{-16}$.

**The most noteworthy point** (and the reason this page uses exactly this example): both `age_wife` and `age_husband` are **not statistically significant** at the 5% level ($p=0.217$ and $p=0.328$), even though household age could in theory well affect expenditure. This is precisely the classic sign of multicollinearity: two highly correlated variables make **both** t-statistics small, even though (as will be seen in section 8) together they still carry a lot of information. $R^2=0.38$ in this model is **not high** — this must be clearly distinguished from the $R^2$ of the *auxiliary regression* in section 8.2, which is the number actually directly relevant to multicollinearity (exam trap #9 in section 10).

## Consequences of multicollinearity

- $R^2$ **can** be very high even though few coefficients are individually statistically significant (note: this is a *possible* consequence, not one that always happens — in the case study in section 5, the overall $R^2$ is only a moderate 0.38, yet both age variables still lose statistical significance together).
- In some cases, the expected sign of an estimated coefficient can be wrong (wrong expected sign).
- **The OLS estimator remains consistent** — this is the single most important point to remember, and the one most often misunderstood (see exam trap #3): multicollinearity does **not** make coefficients biased or inconsistent, it only gives one or more coefficients a **large SE**, which makes the t-statistic small and the p-value large.
- Because the t-statistic is small, an analyst can easily draw the **misleading** conclusion that the true value of these coefficients is no different from 0 — when in fact the variable *may* genuinely have an effect, it's just that the data lacks enough "independent variation" to prove it with statistical confidence.

**Linking back to the t-test** ([[concepts/linear-regression-model]] section 7): recall $t=\dfrac{b_j-c}{SE(b_j)}$. When $SE(b_j)$ is "inflated" by multicollinearity, the denominator of $t$ increases while the numerator ($b_j$) doesn't change much → $|t|$ shrinks → it becomes harder to cross the threshold for rejecting $H_0$. In other words, multicollinearity reduces the **power** of the t-test — raising the risk of a **Type II error** (failing to reject $H_0$ even though $H_0$ is false, i.e., missing a genuinely existing effect). This is the specific statistical mechanism behind the "misleading conclusion" consequence mentioned above.

## Variance Inflation Factor (VIF)

### Formula

With a two-regressor model $y_i=\beta_0+\beta_1X_1+\beta_2X_2+u$, the variance of each estimated coefficient:

$$Var(\hat\beta_1)=\frac{\sigma^2}{(1-r_{12}^2)\sum(X_1-\bar X_1)^2}=\frac{\sigma^2}{\sum(X_1-\bar X_1)^2}\cdot VIF_1, \qquad Var(\hat\beta_2)=\frac{\sigma^2}{(1-r_{12}^2)\sum(X_2-\bar X_2)^2}=\frac{\sigma^2}{\sum(X_2-\bar X_2)^2}\cdot VIF_2$$

where $\sigma^2$ is the variance of the error $u_i$, and $r_{12}$ is the correlation coefficient between $X_1$ and $X_2$. With two regressors:

$$VIF=\frac{1}{1-r_{12}^2}$$

VIF measures **how much the variance of the OLS estimator is "inflated"** by multicollinearity, relative to the case where $X_1,X_2$ are completely uncorrelated ($r_{12}=0$, in which case $VIF=1$, no inflation at all).

### Intuition: why high $r_{12}$ (high VIF) → large SE

Look at the denominator $(1-r_{12}^2)$: as $r_{12}\to1$ (the two variables move together almost perfectly), the denominator $\to0$, so $Var(\hat\beta_1)\to\infty$. The economic intuition behind the formula: $\sum(X_1-\bar X_1)^2$ measures the **total variation** of $X_1$ present in the sample — but when $X_1$ and $X_2$ are highly correlated, most of that variation is "duplicated" with $X_2$; the portion of variation that is **truly independent, unique to $X_1$** (not shared with $X_2$) is very small. OLS can only use that "unique" variation to disentangle the effect of $X_1$ from the effect of $X_2$ — the less unique variation there is, the more wildly the estimate $\hat\beta_1$ tends to swing if you switched to a different sample → large SE. This is exactly the mathematical mechanism behind the "overlapping Venn diagram" metaphor in section 1.

### Commonly used thresholds

Rule of thumb per the slide: **$VIF>5$** is treated as serious in one place in the slide ("Signs of Multicollinearity"), while the slide states "$VIF>5$ (or 10)" elsewhere — i.e., it acknowledges that both the 5 and 10 thresholds are commonly used in practice, without committing to a single number. See more on this inconsistency in exam trap #7 (section 10).

## Detection

The slide lists three groups of detection tools, with an important distinction: only VIF is considered a **confirmation**, while the other two tools are merely a **sign** — suggestive but not certain.

|Sign |Interpretation |Level of certainty |
|---|---|---|
|Coefficient sign is wrong relative to expectation, but $R^2$ is high |Suggests multicollinearity |Sign |
|High $R^2$ but few significant t-ratios |Suggests multicollinearity |Sign |
|High pairwise correlation matrix values (commonly used threshold $\pm0.8$) |Suggests multicollinearity |**Only a sign, not a confirmation** — low correlation also does not guarantee the absence of multicollinearity (it could be multivariate multicollinearity, which doesn't show up in any single pairwise correlation) |
|Auxiliary regression: regressing each regressor on all other regressors |High $R^2$ of the auxiliary regression (>0.8) or a significant F-test |Sign — same logic: high suggests it, low does not guarantee it's ruled out |
|VIF > 5 (or 10) |Treated by the slide as **confirming** serious multicollinearity |Confirmation |

Applying all three tools to the case study in sections 4–5:

### Correlation matrix

Correlation matrix among $\log(\text{income})$, `age_wife`, `age_husband`, `hhsize`, `children`:

| | log(income) | age_wife | age_husband | hhsize | children |
|---|---|---|---|---|---|
| **log(income)** | 1.000 | −0.369 | −0.320 | −0.019 | −0.018 |
| **age_wife** | −0.369 | 1.000 | **0.921** | −0.039 | −0.220 |
| **age_husband** | −0.320 | **0.921** | 1.000 | −0.058 | −0.236 |
| **hhsize** | −0.019 | −0.039 | −0.058 | 1.000 | 0.156 |
| **children** | −0.018 | −0.220 | −0.236 | 0.156 | 1.000 |

The correlation between `age_wife` and `age_husband` is $r=0.921$ — far exceeding the $\pm0.8$ threshold mentioned by the slide — this is the clearest **sign** of multicollinearity in the table. All other pairs have $|r|<0.4$, which is not a concern.

### Auxiliary regression

Regressing `age_wife` on all other regressors: $\text{age\_wife} = \beta_0+\beta_1\log(\text{income})+\beta_2\,\text{age\_husband}+\beta_3\,\text{hhsize}+\beta_4\,\text{children}+u$

|Variable | $b$ | SE | $t$ | $p$-value |
|---|---|---|---|---|
| (Intercept) | 3.8438 | 1.4107 | 2.725 | 0.00668 ** |
| `log(income)` | −1.1221 | 0.2509 | −4.472 | 9.76e-06 *** |
| `age_husband` | 0.9030 | 0.0195 | 46.203 | < 2e-16 *** |
| `hhsize` | 0.0639 | 0.0838 | 0.762 | 0.44622 |
| `children` | −0.0112 | 0.0154 | −0.731 | 0.46541 |

Residual SE $=4.158$ on 465 df; $R^2=0.8548$; $R^2_{adj}=0.8536$; $F=684.4$ on $(4,465)$ df, $p<2.2\times10^{-16}$.

$R^2=0.8548$ (>0.8, the threshold stated by the slide) and an extremely significant F-test — both confirm multicollinearity by the slide's criteria. Notably: `age_husband` alone has $t=46.2$ in this auxiliary regression — `age_husband` on its own explains most of the variation in `age_wife`, exactly matching the intuition in section 1.

### VIF

The slide only gives the VIF formula for the 2-regressor case ($VIF=1/(1-r_{12}^2)$), but the `car::vif()` results table in section 9.2 (5 regressors) shows the slide applies the more general formula: $VIF_j=1/(1-R_j^2)$, where $R_j^2$ is precisely the $R^2$ of the auxiliary regression for variable $X_j$ — this is how the `car::vif()` function in R actually computes it, and matches the "auxiliary regression" logic the slide presented in section 8.2.

> **Note on the source**: the specific VIF number below is **not printed directly by the slide** for the original (5-variable) model — it is derived here by applying the slide's own formula $VIF_j=1/(1-R_j^2)$ to the $R^2=0.8548$ that the slide computed in the auxiliary regression in section 8.2. Noted explicitly to distinguish it from the VIF numbers the slide prints directly (section 9.2).

$$VIF_{\text{age\_wife}}=\frac{1}{1-0.8548}=\frac{1}{0.1452}\approx 6.89$$

With the $VIF>5$ threshold, the figure $\approx6.89$ confirms serious multicollinearity involving `age_wife` (and correspondingly, `age_husband`) — but it does not exceed the $10$ threshold if that alternative threshold is used (see exam trap #7).

## Solutions

### General rule: it doesn't always need to be fixed

The slide clearly states **"General Rules of Thumb: DO NOT WORRY IF"**:

- the coefficients are still statistically significant, **and**
- the coefficients still have the correct expected signs.

Reason: multicollinearity is only a **practical** problem when it actually undermines the ability to answer the research question (coefficients become insignificant or have the wrong sign). If the coefficients remain significant and correctly signed despite a high VIF, that means there is still *enough* independent variation for a reliable estimate — "fixing" a problem that isn't actually causing harm (e.g., just to make the VIF look nicer) can create a new problem (omitted variable bias, see below) without any real benefit.

**If a fix is needed**, the slide offers two directions, each with its own trade-off:

### Solution 1 — Restructure the model (transform regressors)

**Idea**: find an alternative specification or functional form such that the new regressors are less correlated while still preserving the economic content of the original model.

**Example 1 (slide, production function)**: with $y=F(\text{labor},\text{land},\text{capital})$, if `labor` and `capital` are highly correlated across observations (e.g., larger farms have both more labor and more capital), both sides can be divided by `land`:

$$\frac{y}{\text{land}}=F\left(\frac{\text{labor}}{\text{land}},\ \text{land},\ \frac{\text{capital}}{\text{land}}\right)$$

Normalizing by land area reduces the correlation between the inputs, because the variables now measure *input intensity per unit of land*, no longer jointly driven by "farm size" as before.

**Example 2 (case study, actually applied)**: instead of using both `age_wife` and `age_husband` (correlation $r=0.921$), the slide creates a new variable `age_diff = age_wife − age_husband` and replaces `age_husband` with `age_diff` in the model: $\log(\text{expense})=\beta_0+\beta_1\log(\text{income})+\beta_2\,\text{age\_wife}+\beta_3\,\text{age\_diff}+\beta_4\,\text{hhsize}+\beta_5\,\text{children}+\varepsilon$

|Variable | $b$ | SE | $t$ | $p$-value |
|---|---|---|---|---|
| (Intercept) | 0.8105 | 0.1649 | 4.916 | 1.23e-06 *** |
| `log(income)` | 0.4231 | 0.0297 | 14.240 | < 2e-16 *** |
| `age_wife` | 0.0014 | 0.0023 | 0.599 | 0.5492 |
| `age_diff` | 0.0053 | 0.0054 | 0.980 | 0.3277 |
| `hhsize` | 0.0720 | 0.0097 | 7.400 | 6.46e-13 *** |
| `children` | 0.0036 | 0.0018 | 2.007 | 0.0453 * |

Residual SE $=0.4821$; $R^2=0.3829$; $R^2_{adj}=0.3762$; $F=57.57$ — **exactly identical** to the original model in section 5. This is no coincidence: `age_diff = age_wife − age_husband` is a linear combination of the two original variables, so $\{\text{age\_wife},\ \text{age\_diff}\}$ spans exactly the same space as $\{\text{age\_wife},\ \text{age\_husband}\}$ — the *overall* predictive model is unchanged (same $\hat y$, same $R^2$, same $F$), only the way the effect is "split" across the individual coefficients changes.

And `car::vif(model2)` gives the result:

| `log(income)` | `age_wife` | `age_diff` | `hhsize` | `children` |
|---|---|---|---|---|
| 1.175 | 1.288 | 1.068 | 1.027 | 1.094 |

All VIF values are now below 1.3 — multicollinearity has almost disappeared.

**Further analysis (derived algebraically from the slide's own coefficients, not verbatim from the slide)**: since $\text{age\_husband}=\text{age\_wife}-\text{age\_diff}$, substituting into the original model $\beta_2\,\text{age\_wife}+\beta_3\,\text{age\_husband}=\beta_2\,\text{age\_wife}+\beta_3(\text{age\_wife}-\text{age\_diff})=(\beta_2+\beta_3)\text{age\_wife}-\beta_3\,\text{age\_diff}$. Checking against the actual numbers: the original `age_wife` coefficient $(0.0066)$ plus the original `age_husband` coefficient $(-0.0053)$ equals $0.0013\approx0.0014$ (the new `age_wife` coefficient, rounding error); and $-(-0.0053)=0.0053$ equals exactly the new `age_diff` coefficient. Economic meaning: the **new** `age_wife` coefficient is no longer "the effect of the wife's age, holding the husband's age fixed" (something almost impossible to estimate precisely in this data, since the two ages rarely vary independently), but rather **the effect of both spouses aging by 1 year together** (holding the age gap fixed); while the `age_diff` coefficient is **the effect of widening the age gap**, holding the wife's age fixed. This is a reinterpretation that fits the actual variation present in the data — rather than trying to estimate an effect the data has almost no information to answer.

**Trade-off of the restructure solution**: all of the original information is retained (no variable is lost), but (a) it isn't always possible to find a transformation that both reduces correlation and has a clear economic meaning for interpretation (dividing by `land` makes sense in a production function; taking the age difference makes sense since both are in the same "years" unit — but not every pair of collinear variables has a similarly natural transformation); (b) the transformed coefficients must be reinterpreted carefully, since they no longer carry the same "holding the other variable fixed" meaning as the original coefficients (see exam trap #8).

### Solution 2 — Drop correlated regressors

Remove the highly correlated regressor(s) from the model.

**Trade-off**: simple, solves multicollinearity immediately (reduces VIF), but carries the risk of **omitted variable bias** — if the dropped variable genuinely belongs in the model theoretically (i.e., truly affects $y$ and is correlated with the remaining variables), removing it will make the remaining coefficients **biased**, losing not just efficiency (as with multicollinearity) but also validity. In other words, this is a trade-off between **bias and variance**: multicollinearity causes a variance problem (large SE) — dropping a variable "cures" the variance by accepting the risk of bias, and should only be done when there is a solid theoretical reason to believe that variable isn't really needed, not just to make the "VIF look nicer".

## Exam traps

1. **Confusing perfect and imperfect (multicollinearity)**: saying "multicollinearity makes $X'X$ non-invertible" is **wrong** — that is a consequence of **perfect** collinearity. Multicollinearity (imperfect) does not make $X'X$ non-invertible; the model still estimates normally, only the SE is inflated.
2. **Confusing what's correlated with what**: multicollinearity is correlation **among the independent variables themselves**, not between an independent variable and the dependent variable.
3. Thinking multicollinearity makes the OLS coefficients biased or inconsistent — wrong. OLS remains unbiased/consistent under multicollinearity (as long as A1–A3 still hold); multicollinearity only causes a loss of **efficiency** (larger SE). Easily confused with omitted variable bias or endogeneity — those are the problems that actually cause bias.
4. Treating a high/low pairwise correlation as **conclusive evidence** of the presence/absence of multicollinearity — the slide only treats this as a "sign," not a "confirmation." A low pairwise correlation **does not guarantee** the absence of multicollinearity (it could be multivariate multicollinearity — 3+ variables jointly dependent on each other without any single pair individually showing a high correlation).
5. "Fixing" multicollinearity even when the coefficients are still significant and correctly signed — unnecessary, and goes against the slide's "General Rule of Thumb" (section 9.1).
6. Dropping a variable to reduce multicollinearity **without weighing omitted variable bias** — this is not a "free fix" but a genuine bias-variance trade-off.
7. Confusing the VIF threshold: the slide uses both "$VIF>5$" and "$VIF>5$ (or 10)" in two different places, without settling on a single threshold — when answering exam questions, always state clearly which threshold is being used, since the same VIF (e.g., $\approx6.89$ in the case study) can be "serious" under the threshold of 5 but "not yet serious" under the threshold of 10.
8. After restructuring the model (e.g., replacing `age_husband` → `age_diff`), forgetting to reinterpret the coefficients: the **new** `age_wife` coefficient no longer means "the effect of the wife's age, holding the husband's age fixed" — since the data has almost no independent variation to answer that question — but rather "the effect of both spouses aging together".
9. Confusing the $R^2$ of the **main model** (measuring fit to $y$) with the $R^2$ of the **auxiliary regression** (measuring how much one $X_j$ is explained by the remaining $X$'s). In the case study, the main model's $R^2$ is only 0.38 (not high), but the auxiliary regression's $R^2$ for `age_wife` reaches 0.85 — only the second number is directly relevant to confirming multicollinearity.
10. Using the language of "proving" when talking about VIF/correlation matrix/auxiliary regression — these tools should properly only be said to "confirm" or "suggest" multicollinearity, consistent with the statistical-inference language convention stated in [[concepts/linear-regression-model]] section 7.1.

## Connections to the rest of the course

- Multicollinearity is a "near-violation" case of **A2 (Full rank)** of [[concepts/linear-regression-model]] — quite unlike perfect collinearity (a complete violation of A2, which makes $b$ unidentifiable).
- Unlike [[concepts/heteroskedasticity]] (a violation of **A4**): multicollinearity does not cause a loss of consistency, only a loss of efficiency (larger SE, but the VCV formula $\sigma^2(X'X)^{-1}$ is in principle still the correct form); heteroskedasticity, on the other hand, makes that standard VCV formula itself **entirely wrong**, requiring robust SE — two completely different mechanisms, even though both, in their most basic form, "only affect SE, without causing bias".
- Unlike a violation of **A3 (Exogeneity)** ([[concepts/endogeneity-iv-regression]]): multicollinearity does not cause bias/inconsistency; endogeneity does cause bias. A coefficient with the "wrong expected sign" could be due to multicollinearity **or** to an omitted variable/endogeneity — the correct corresponding diagnostic toolkit must be used (VIF/correlation matrix for multicollinearity; separate tests for endogeneity) before concluding the cause.
- The fourth source of multicollinearity ("mathematical derivation" — one variable is a function of another, e.g., a variable and its square) connects directly to the quadratic/polynomial form in [[concepts/functional-forms]].
- The "large SE → small t-statistic → hard to reject $H_0$" mechanism in section 6 is a direct application of the t-test framework learned in [[concepts/linear-regression-model]] section 7 — the case study on this page (`age_wife`, `age_husband` both with $|t|<2$) is a concrete numerical illustration of how an inflated SE reduces the power of a test, leading to the risk of a Type II error.
