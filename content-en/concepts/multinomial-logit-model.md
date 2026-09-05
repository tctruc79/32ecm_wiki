---
title: "Lecture 10: Multinomial Logit Model (MNL)"
type: concept
status: mature
tags: [multinomial-logit, discrete-choice, limited-dependent-variable]
sources: ["[[sources/slides-8-multinomial-logit-model]]"]
related: ["[[concepts/binary-response-models]]", "[[concepts/ordinal-response-models]]"]
lecture: 10
assignment: []
updated: 2026-09-04
---

> **How to read this page**: MNL is the second link in the course's "limited dependent variable models" chain — after [[concepts/binary-response-models]] (Topic 7, 0/1 dependent variable) and before [[concepts/ordinal-response-models]] (Topic 9, ordered dependent variable). The most important thing to grasp **before** reading the formulas: MNL handles the case where the dependent variable is **one choice among several choices with NO natural order** — fundamentally different from both a binary variable and an ordinal one. This entire page reuses exactly one running case study (choice of healthcare provider, VHLSS 2012 data) — understanding this case study is necessary for following the numeric examples in the sections below.

**Lecture 10** in the syllabus (CO Topic 8) — no dedicated assignment yet.

## Positioning the problem: three model families for discrete dependent variables

Before diving into the formulas, we need to answer: how many "kinds" of discrete (categorical) dependent variable are there, and which one does MNL handle?


| $Y$ characteristic | Number of categories | Ordered? | Corresponding model | Wiki page |
|---|---|---|---|---|
| Binary | 2 (e.g., yes/no, alive/dead) | Not applicable | Binary Logit/Probit | [[concepts/binary-response-models]] |
| **Multi-category, unordered (nominal)** | $J>2$ (e.g., choice of car brand, occupation, hospital) | **No** — categories are on par, none is "higher/lower" than another | **Multinomial Logit (MNL)** ← this page | — |
| Multi-category, ordered (ordinal) | $J>2$ (e.g., low/medium/high satisfaction, credit rating) | **Yes** — categories have a natural order | Ordered Logit/Probit | [[concepts/ordinal-response-models]] |


The illustrative examples below clearly show MNL's "unordered" property:

- Long-term effects of radiation exposure: 1 = death by cancer, 2 = death by other cause, 3 = still alive — these three categories **cannot** be arranged along a meaningful "increasing/decreasing" axis.
- Choice of healthcare provider: public hospital, private hospital/clinic, traditional healer, self-treatment — no category is "better" than another on a common scale, they are simply different choices.
- Other examples: choice of car brand (Toyota, Honda, Suzuki, Mazda, KIA…), choice of field of study, choice of occupation.

**Why not use OLS?** For OLS to be valid, $Y$ must be a quantity with arithmetic meaning — the distance between two values must carry information (e.g., the gap between 3 and 1 years of schooling must equal the gap between 6 and 4 years of schooling). If we code "chose public hospital = 1, chose private hospital = 2, chose traditional healer = 3" and run OLS, the model implicitly assumes "traditional healer" is exactly as far from "private hospital" as "private hospital" is from "public hospital" — a meaningless assumption, since the numbers 1/2/3 are merely **labels**, not a scale.

**Why not use binary Logit/Probit?** Binary Logit/Probit ([[concepts/binary-response-models]]) can only handle exactly 2 categories. When $J>2$, we need a model that extends the probability structure to more than 2 outcomes while still guaranteeing every probability is non-negative and they sum to 1 — that is precisely the motivation behind MNL.

## Running case study: choice of healthcare provider (VHLSS 2012)

This is the dataset used throughout Lecture 10 — understanding it is necessary for following every numeric example in the sections below. Source: **Vietnam Household Living Standards Survey (VHLSS) 2012**, file `mnl.xlsx`.

**Dependent variable** `choice` — healthcare provider, 5 unordered categories:


| Original code | Category | Sample frequency |
|---|---|---|
| 1 | Commune health center | 434 |
| 2 | Public hospital | 2,320 |
| 3 | Private hospital | 522 |
| 4 | Lang y (traditional folk healer) | 34 |
| 5 | Individual health care provider | 165 |


Total $N = 3{,}475$ observations. **Public hospital dominates overwhelmingly** — 2,320/3,475 ≈ 66.8% of the sample — an important detail to remember since it explains several phenomena in the prediction and McFadden $R^2$ sections below.

> **Unit of analysis**: the same `id` can appear across several different `case` rows with different `choice` values (e.g. `id=1` has `case=1` choosing Public hospital and `case=2` choosing Lang y) — showing that the unit of analysis is actually **each choice occasion** (each time healthcare is needed), not one fixed choice per individual.

**Independent variables** (variable names kept as in the original dataset):


| Variable | Meaning | Unit/coding |
|---|---|---|
| `insurance` | Has health insurance or not | dummy (1 = yes, 0 = no) |
| `income` | Household income | million VND/year |
| `female` | Gender | dummy (1 = female, 0 = male) |
| `age` | Age | years |
| `edu` | Education level | categorical: 0 = below primary, 1 = primary, 2 = lower secondary, 3 = upper secondary, 4 = college/university or above |
| `urban` | Lives in an urban area or not | dummy (1 = urban, 0 = rural) |


`edu` is entered into the model as `factor(edu)`, generating 4 dummy variables (`edu1`–`edu4`, relative to the base `edu0` = below primary) — following exactly the categorical-variable logic already seen in [[concepts/linear-regression-model]] section 5.

## Base category — why it's needed, and which one to choose

### Intuition: why there cannot be $J$ independent equations

With $J$ categories, we have $J$ probabilities $p_{i1},\dots,p_{iJ}$, but they must satisfy the constraint $\sum_{j=1}^J p_{ij}=1$. This constraint means: if $J-1$ probabilities are known, the remaining one is **automatically determined** ($p_{iJ}=1-\sum_{j<J}p_{ij}$) — it is not an independent degree of freedom. So the model can only estimate **at most $(J-1)$ independent sets of coefficients**, not $J$ sets.

This is exactly the **"base category" logic** already seen for categorical variables in OLS ([[concepts/linear-regression-model]] section 5, the `cterrain` example with `lowland` as the base) — the same mathematical reason (avoiding perfect redundancy/collinearity, corresponding to assumption A2 — full rank). The difference: in OLS, the base category only affects **one** regression equation; in MNL, the base category governs **an entire system of $(J-1)$ log-odds equations** simultaneously.

### Case study: choosing Public hospital as the base

The following R command is used to make `Public hospital` (original code = 2) the base group:

```r
Z$choice = relevel(as.factor(Z$choice), ref = 2)
levels(Z$choice) = c("Public hospital", "Commune health center",
                      "Private hospital", "Lang y", "Ind. health care")
```

Choosing Public hospital (the largest group, 66.8% of the sample) as the base is a common, practical choice — it gives an easy-to-interpret "popular/default" reference point, and every comparison becomes "relative to choosing the public hospital".

> **A point that easily confuses theory and R code**: the general formula in section 4 below places category **$J$ (the last category under the numbering $1,\dots,J$)** as the base, with the convention $h_{iJ}=0$. But in R, the `nnet::multinom` function (used to estimate MNL) instead takes the **first level** of the factor variable as the base. That's why the code above must use `relevel()` and then reorder `levels()` to move "Public hospital" to the first position — this is not a contradiction between theory and practice, just two different numbering conventions (base = last in the math formula, base = first in how R organizes a factor). Worth noting when comparing the formula against R output.

**Key point to remember**: changing the base category does **not** change the fitted probabilities or the model's fit — it only changes how the coefficients are *displayed/interpreted* (a different reference point). This is purely a normalization, not a model assumption.

## Setup: log-odds relative to the base category

Dependent variable $Y_i = 1,2,\dots,J$ with corresponding probabilities $p_{i1},\dots,p_{iJ}$. Choosing category $J$ as the base, define the **logit** (log-odds ratio) relative to the base for each remaining category:

$$h_{ij} = \ln\frac{p_{ij}}{p_{iJ}} = \beta_j X_i \quad (j=1,\dots,J-1), \qquad h_{iJ} = \ln\frac{p_{iJ}}{p_{iJ}} = 0$$

With $J$ choices, there are **$(J-1)$ sets of $\beta$ coefficients** to estimate — each set $\beta_j$ describes the log-odds of choosing $j$ relative to the base, as its own separate linear function of $X$. In the case study ($J=5$), there are $(5-1)=4$ sets of coefficients: Commune health center vs. Public hospital, Private hospital vs. Public hospital, Lang y vs. Public hospital, Ind. health care vs. Public hospital.

## Deriving the probability formula (softmax)

This is the "derivation" part — going step by step from the logit definition in section 4 to the final probability formula.

**Step 1 — exponentiate both sides** of $\ln(p_j/p_J) = \beta_j X$:

$$p_{ij} = p_{iJ}\cdot e^{X_i\beta_j}$$

**Step 2 — use the constraint that probabilities sum to 1**: since $\sum_{j=1}^J p_{ij}=1$, we have

$$p_{iJ} = 1 - \sum_{j=1}^{J-1} p_{ij}$$

**Step 3 — substitute the expression from Step 1 into Step 2**:

$$p_{iJ} = 1 - \sum_{j=1}^{J-1} p_{iJ}\cdot e^{X_i\beta_j}$$

Solving this equation for $p_{iJ}$ (moving every term containing $p_{iJ}$ to one side):

$$p_{iJ} = \frac{1}{1+\sum_{j=1}^{J-1} e^{X_i\beta_j}}$$

**Step 4 — go back to Step 1** to compute the remaining $p_{ij}$:

$$p_{ij} = \frac{e^{X_i\beta_j}}{1+\sum_{k=1}^{J-1} e^{X_i\beta_k}} \quad (j=1,\dots,J-1)$$

**Combined form (softmax)** — if we adopt the convention $\beta_J = 0$ for the base category (consistent with $h_{iJ}=0$ in section 4), both $p_{iJ}$ and $p_{ij}$ above can be written as a single unified formula:

$$p_{ij} = \frac{e^{X_i\beta_j}}{\sum_{k=1}^{J} e^{X_i\beta_k}}$$

This is the familiar **softmax** form (also exactly the output activation function used in neural networks for multi-class classification — the same mathematical structure). The important property of this formula: **every $p_{ij} \in (0,1)$ and $\sum_j p_{ij}=1$ is automatically guaranteed**, regardless of what real values $X\beta_j$ takes — this is precisely why MNL "fixes" the problem that plagues OLS (not guaranteeing predicted probabilities fall within $[0,1]$).

## Estimation: Maximum Likelihood

Unlike OLS — which has a closed-form solution $b=(X'X)^{-1}X'y$ (see [[concepts/linear-regression-model]] section 2.2) — the softmax probability formula in section 5 is **nonlinear** in $\beta$, so no closed-form solution exists. MNL is estimated by **Maximum Likelihood (ML)**, maximizing the log-likelihood function:

(where $y_{ij}=1$ if $j$ is chosen by observation $i$, and $0$ otherwise)

This optimization is carried out via numerical iterative optimization (R uses a Newton-type algorithm), not a direct matrix computation as in OLS.

### Case study: the null model and the full model

**Null model (intercept only)** — `choice ~ 1` — estimates the average log-odds of each category relative to the base, with no explanatory variables:


| Category (relative to Public hospital) | Coefficient (intercept) | SE |
|---|---|---|
| Commune health center | −1.676278 | 0.05230 |
| Private hospital | −1.491655 | 0.04844 |
| Lang y | −4.222962 | 0.17275 |
| Ind. health care | −2.643377 | 0.08057 |


Residual Deviance = 6979.762, and since $LL=-\text{Deviance}/2$, $LL_{null} = -3489.881$.

> **An insight you can verify by hand**: with an intercept-only model, the estimated coefficient is exactly the **raw log-odds computed directly from the frequency table** — $\hat\beta_{0j} = \ln(n_j/n_{base})$. Check: $\ln(434/2320) = -1.676$, $\ln(522/2320)=-1.492$, $\ln(34/2320)=-4.223$, $\ln(165/2320)=-2.643$ — matches the table above exactly. This is the most intuitive way to understand what "log-odds" means: it is simply the logarithm of the frequency ratio between two groups.

**Full model** — `choice ~ insurance + income + female + age + factor(edu) + urban` — Residual Deviance = 6420.637, AIC = 6500.637, $LL_{full} = -3210.319$.

## Interpreting coefficients — the most error-prone part of MNL

### Principle

The coefficient $\beta_j$ measures the **change in the log-odds of choosing $j$ relative to the base category** when $X$ increases by 1 unit, holding other variables constant — **not** a direct change in the probability $P(Y=j)$. This is a fundamental difference from OLS coefficients ([[concepts/linear-regression-model]] section 5, where $b_j$ directly measures the change in $y$).

**Interpreting via the relative risk ratio (RRR)**: taking $e^{\beta_j}$ gives an easier-to-read number — by what multiple the odds of choosing $j$ (relative to the base) change when $X$ increases by 1 unit.

### Case study coefficient tables (two equations presented separately)

**Equation for Commune health center (relative to Public hospital):**


| Variable | Coef | SE | z | p-value |
|---|---|---|---|---|
| (Intercept) | −0.26287 | 0.22855 | −1.150 | 0.250 |
| insurance | 0.01678 | 0.11720 | 0.143 | 0.886 |
| income | −0.00535 | 0.00128 | −4.171 | 0.00003 |
| female | 0.14753 | 0.10900 | 1.353 | 0.176 |
| age | −0.01318 | 0.00326 | −4.043 | 0.00005 |
| edu1 | −0.26877 | 0.14169 | −1.897 | 0.058 |
| edu2 | −0.39115 | 0.14641 | −2.672 | 0.008 |
| edu3 | −0.73012 | 0.19925 | −3.664 | 0.00025 |
| edu4 | −0.89003 | 0.34122 | −2.608 | 0.009 |
| urban | −0.97947 | 0.16298 | −6.010 | <0.0001 |


**Equation for Private hospital (relative to Public hospital):**


| Variable | Coef | SE | z | p-value |
|---|---|---|---|---|
| (Intercept) | −0.33844 | 0.21710 | −1.559 | 0.119 |
| insurance | −1.20794 | 0.10718 | −11.270 | <0.0001 |
| income | 0.00210 | 0.00049 | 4.323 | 0.00002 |
| female | 0.16487 | 0.10213 | 1.614 | 0.106 |
| age | −0.01633 | 0.00332 | −4.926 | <0.0001 |
| edu1 | 0.14632 | 0.14578 | 1.004 | 0.316 |
| edu2 | −0.05282 | 0.14829 | −0.356 | 0.722 |
| edu3 | −0.38454 | 0.18512 | −2.077 | 0.038 |
| edu4 | 0.14029 | 0.22334 | 0.628 | 0.530 |
| urban | 0.08494 | 0.11546 | 0.736 | 0.462 |


**Example verbal interpretations (RRR)**:

- ✅ "$e^{-1.20794}\approx 0.299$ — having health insurance reduces the odds of choosing a private hospital (relative to a public hospital) to about 30% of the odds for someone without insurance, i.e., about a 70% relative-odds decrease, holding other factors constant." (This is a statement about **log-odds/relative odds** — valid.)
- ❌ "Having health insurance reduces the **probability** of choosing a private hospital by 70%." — wrong; the 70% figure only applies to the odds ratio relative to the base, it does **not** apply directly to the probability $P(\text{Private hospital})$ (see section 7.3 for why these two are fundamentally different).
- ✅ "$e^{-0.97947}\approx 0.375$ — living in an urban area lowers the odds of choosing a commune health center (relative to a public hospital) to only about 37.5% of those of living in a rural area (about a 62.5% relative-odds decrease)."

**The `insurance` coefficient across all 4 categories** — a consistent economic story, illustrating how to read the entire system of equations at once:


| Category (relative to Public hospital) | Coef `insurance` | p-value |
|---|---|---|
| Commune health center | +0.0168 | 0.886 (not statistically significant) |
| Private hospital | −1.2079 | <0.0001 |
| Lang y | −1.4630 | 0.0001 |
| Ind. health care | −1.8264 | <0.0001 |


Having health insurance is associated with **statistically significantly** lower odds for all 3 non-public options (private, traditional healer, self-treatment) relative to public hospital, while relative to the commune health center there is no significant difference — economically sensible if public health insurance mainly reimburses well at public facilities (public hospitals and possibly, to some extent, commune health centers).

### The subtlest trap: a positive coefficient does NOT mean "choice probability increases"

This is the most common and subtle point of confusion when first learning MNL — a concrete numeric example is needed to see it clearly.

**The starting paradox**: the `Public hospital` (base) category has its "$\beta$ coefficient" equal to 0 **by definition** (since $h_{iJ}=0$ — there is nothing to compare it against itself). If we naively infer "coefficient 0 → variable $X$ has no effect on choosing this category", we'd wrongly conclude that `insurance` has no effect on the probability of choosing Public hospital. In reality, when we compute the true **marginal effect** (using the `margins` package in R) — i.e., $\partial p_j/\partial x$, not $\partial h_j/\partial x$:


| Category | Average Marginal Effect of `insurance` on $P(\text{category})$ |
|---|---|
| **Public hospital (base, coefficient = 0)** | **+0.17** ← largest of all! |
| Commune health center (coefficient +0.0168, *not* statistically significant) | +0.03 |
| Private hospital (coefficient −1.2079, strongly significant) | −0.12 |


Having health insurance **increases the probability of choosing Public hospital the most** (+17 percentage points on average) — even though the log-odds coefficient of this very category is "0 by definition" because it is the base. Conversely, `Commune health center` has a log-odds coefficient close to zero and not statistically significant (p = 0.886) relative to the base, yet its actual probability still rises slightly (+0.03) with insurance.

**Why does this paradox occur?** It can be derived directly from the softmax formula in section 5. Taking the derivative of $p_{ij}$ with respect to any variable $x$ in $X$:

$$\frac{\partial p_{ij}}{\partial x} = p_{ij}\left(\beta_{jx} - \sum_{k=1}^{J} p_{ik}\,\beta_{kx}\right) = p_{ij}\left(\beta_{jx} - \bar\beta_x\right)$$

where $\bar\beta_x = \sum_k p_{ik}\beta_{kx}$ is the **probability-weighted average** of the coefficient $\beta_{kx}$ across **all** $J$ categories (including the base, with $\beta_{base,x}=0$). The marginal effect of $x$ on $p_{ij}$ depends on the **difference** between category $j$'s own $\beta_{jx}$ and $\bar\beta_x$ — the average across **all** categories — not on the absolute value of $\beta_{jx}$ alone. For the `insurance` variable: 3 of the 4 non-base categories have strongly negative coefficients (−1.208, −1.463, −1.826) and only 1 is near zero (+0.017), so $\bar\beta_{insurance} < 0$ quite clearly. For the base category (where $\beta_{base}=0$): $\partial p_{base}/\partial x = p_{base}(0-\bar\beta_x) = -p_{base}\bar\beta_x > 0$ — positive, exactly matching the observed figure (+0.17)!

**The core lesson**: the marginal effect on $P(Y=j)$ depends on the **entire** system of $(J-1)$ coefficient sets, not just $\beta_j$ alone. Therefore the sign or magnitude of a marginal effect **cannot** be inferred directly from the sign of a single log-odds coefficient — marginal effects must be computed separately (as R does with the `margins` package), similar to how [[concepts/binary-response-models]] distinguishes raw logit coefficients from marginal effects (MEM/AME).

## Post-estimation tests for MNL — paralleling OLS's t-test/F-test

### z-test for each coefficient

Since MNL is estimated by ML (not OLS with assumptions A1–A5), the test statistic for each coefficient uses the **asymptotic normal distribution** — denoted $z$ — rather than the finite-sample Student-$t$ distribution used in OLS:

(approximate, when $N$ is sufficiently large)

Reading the $p$-value and the rule for rejecting $H_0$ are exactly the same as the t-test in [[concepts/linear-regression-model]] section 7 — only the reference distribution differs.

### LR test for overall significance (replacing the F-test)

To test "whether all explanatory variables are jointly significant" (like the overall F-test in [[concepts/linear-regression-model]] section 8.5), MNL uses the **Likelihood Ratio (LR) test**, comparing the unrestricted (full) model against the restricted (null) model:

$$LR = -2(LL_{restricted}-LL_{unrestricted}) = \text{Deviance}_{restricted}-\text{Deviance}_{unrestricted} \sim \chi^2_q$$

where $q$ = the number of restrictions (the number of coefficients forced to 0). This is **exactly the same logical structure as the F-test** (comparing unrestricted vs. restricted) — only the test statistic differs (chi-square instead of F) because this is an MLE model, with no "residual variance" to normalize against as in OLS.

**Case study** — comparing the null model (intercept only, 4 parameters) with the full model (40 parameters):

$$LR = 6979.762 - 6420.637 = 559.125 \sim \chi^2_{36}, \quad p \approx 0$$

Strongly rejects $H_0$ (all slope coefficients = 0) → there is evidence that **at least one** of the explanatory variables affects the choice of healthcare provider — following exactly the same interpretation logic as the overall F-test (only "at least one", not "every variable").

### LR test for a subset of variables (like an F-test for a subset)

An additional case-study test: does dropping the variable group `{female, age, factor(edu), urban}` from the model significantly reduce fit? (28 restrictions: 1+1+4+1 coefficients × 4 equations)

$$LR = 6576.424 - 6420.637 = 155.787 \sim \chi^2_{28}, \quad p < 2.2\times10^{-16}$$

Strongly rejects $H_0$ → this group of demographic/geographic variables makes a statistically significant contribution to the model, even after controlling for `insurance` and `income`.

## Prediction and assessing fit through prediction

Predicted probabilities (fitted values) for the first observation in the sample: $P(\text{Public})=0.702$, $P(\text{Commune})=0.172$, $P(\text{Private})=0.100$, $P(\text{Lang y})=0.004$, $P(\text{Ind.})=0.022$ — summing exactly to 1, as guaranteed by the softmax constraint in section 5.

The commonly used prediction rule: pick the category with the **highest** fitted probability (argmax). Because `Public hospital` dominates the sample (66.8%), the model predicts "Public hospital" for **all of the first 5 observations** in the case study.

**Goodness-of-prediction test** (comparing the predicted distribution against the actual distribution, Pearson chi-square): $X^2=40.476$, $df=8$, $p=2.6\times10^{-6}$ — there is statistically significant evidence that the predicted distribution differs from the actual one (R also warns "Chi-squared approximation may be incorrect", most likely because some cells have too small an expected frequency — category `Lang y` has only 34/3475 observations).

> **A related trap**: an MNL model can "look correct" most of the time simply by always predicting the most popular category — that **does not** prove the model fits the minority categories well (Lang y, Ind. health care). One must also look at the goodness-of-prediction test, not just the raw proportion of correct predictions.

## McFadden R² (pseudo-R²)

### Formula and numeric example

$$R^2_{McFadden} = 1-\frac{LL_{full}}{LL_{null}} = \frac{LL_{null}-LL_{full}}{LL_{null}}$$

**Case study** (using exactly the $LL$ values computed in section 6.1): $LL_{null}=-3489.881$, $LL_{full}=-3210.319$

$$R^2_{McFadden} = \frac{-3489.881-(-3210.319)}{-3489.881} = \frac{-279.562}{-3489.881} \approx 0.0801$$

(Matches exactly the result computed directly in R: `0.08010663`.)

### How it differs from OLS $R^2$

OLS $R^2$ ([[concepts/linear-regression-model]] section 9) measures **the proportion of variance in $y$ explained** — a sum-of-squares decomposition (TSS = ESS + RSS) with a clear geometric meaning because $y$ is continuous. MNL has no analogous notion of "variance" for a **categorical** dependent variable — there is no TSS/RSS to decompose. Instead, McFadden $R^2$ measures **the degree of log-likelihood improvement** of the full model relative to the intercept-only model (null model) — a quantity living in probability/likelihood space, not variance space.

An important consequence: **the McFadden $R^2$ value cannot be directly compared on the same scale as OLS $R^2$**. An MNL model with $R^2_{McFadden}\approx 0.08$ — as in this case study — can perfectly well be a "good" model by the standards specific to ML models, even though this number looks very low compared to the familiar OLS expectation that "a good $R^2$ should be above 0.6–0.7".

### Commonly used evaluation thresholds

According to McFadden's classic guideline (widely cited in discrete-choice textbooks), $R^2_{McFadden}$ in the range **0.2–0.4** is already considered a **very good** fit — much lower than the familiar "good" threshold for OLS $R^2$.

**The most important point from the case study**: the MNL model here has $R^2_{McFadden}\approx 0.08$ — below even the 0.2 threshold — while the overall LR test (section 8.2) rejects $H_0$ extremely strongly ($p\approx 0$). This is a vivid illustration of the lesson already stated in [[concepts/linear-regression-model]] section 9: **"statistical significance" and "fit magnitude" are two completely different things** — a set of explanatory variables can have a genuine effect (LR test highly significant) yet still explain only a small fraction of the total log-likelihood that could be improved (because the behavior of choosing a healthcare provider also depends on many unobserved factors — the specific illness, actual geographic distance, perceived service quality…).

## Exam traps

1. 1. Interpreting a positive coefficient $\beta_j$ as "the probability of choosing $j$ increases" — wrong; $\beta_j$ only measures the change in **log-odds relative to the base category**, not a direct change in $P(Y=j)$ (see the numeric example in section 7.3 — a coefficient near 0 can still come with a clearly nonzero marginal effect, and vice versa).
2. 2. Thinking the base category is "unaffected" by $X$ because its coefficient is "0 by definition" — wrong; the marginal effect on $P(\text{base category})$ is usually **nonzero**, and in the case study it is even the **largest** marginal effect of all (insurance → +0.17 on $P(\text{Public hospital})$).
3. 3. Changing the base category and treating the coefficients "changing sign/magnitude" as a sign the model is "unstable" — wrong; changing the base only changes the interpretation reference point, the fitted probabilities do not change.
4. 4. Expecting McFadden $R^2$ to reach the high levels typical of OLS $R^2$ (0.6–0.9) — wrong comparison standard; McFadden $R^2$ in the range 0.2–0.4 is already considered a good fit, and even a model with a highly significant LR test can still have a low McFadden $R^2$ (case study: 0.08).
5. 5. Treating a statistically significant overall LR test as meaning "every coefficient in the model is individually significant" — wrong, exactly the same trap as the F-test in [[concepts/linear-regression-model]] section 8.4: the LR test only confirms "at least one" coefficient is nonzero; to know about each individual coefficient you must go back to the z-test.
6. 6. Confusing MNL (nominal, unordered) with the Ordinal response model (ordered) — the two models differ fundamentally both in the nature of the problem and in estimation; see [[concepts/ordinal-response-models]].
7. 7. Using the Student-$t$ distribution to compute the $p$-value for an MNL coefficient — wrong; MNL is estimated by ML, so it uses the asymptotic normal distribution ($z$-test), not OLS's finite-sample $t$-test.
8. 8. Treating a model that correctly predicts most observations (by always picking the most popular category) as evidence it fits every category well — ignoring the possibility that the model almost never predicts the minority categories correctly; this needs to be checked against the goodness-of-prediction test (section 9).
9. 9. Interpreting a statistically non-significant coefficient (large p, e.g. `insurance` for Commune health center, p=0.886) as "definitely zero/no effect at all" — it only means "insufficient evidence to reject $H_0:\beta=0$", not "$\beta=0$ has been proven" (the same principle as in [[concepts/linear-regression-model]] section 7.5).

## Connections to the rest of the course

- MNL is a **direct extension** of [[concepts/binary-response-models]]: when $J=2$, the softmax formula in section 5 collapses exactly into the familiar logistic function of binary Logit (the base category is precisely the outcome $=0$).
- Clearly distinguished from [[concepts/ordinal-response-models]] (Topic 9) — when categories **do** have a natural order, use Ordered Logit/Probit with a cutpoints mechanism instead of MNL-style base categories; wrongly using MNL for ordered data (or vice versa) either wastes ordering information or imposes an order that doesn't exist.
- The **LR test (unrestricted vs. restricted)** logic in section 8 parallels OLS's **F-test** entirely ([[concepts/linear-regression-model]] section 8) — the same model-comparison mindset, differing only in the test statistic because of the different estimation foundation (ML vs. OLS).
- **McFadden $R^2$** is a form of "pseudo-$R^2$" shared by every model estimated via Maximum Likelihood — this exact same logic (and the exact same "significance ≠ fit magnitude" lesson) will reappear in [[concepts/ordinal-response-models]] and the count data models covered later in the course.
- The way a **base category** forces every coefficient to be interpreted relatively is the same principle as categorical variables in OLS ([[concepts/linear-regression-model]] section 5) — the only difference is that MNL applies that principle to an *entire system* of $(J-1)$ equations simultaneously, instead of a single equation.

## Real-world application references

Three recent papers illustrating the multinomial logit model in real-world economic research (Lecture 10 syllabus):

- Alem, Y., Beyene, A. D., Köhlin, G., & Mekonnen, A. (2016). Modeling household cooking fuel choice: A panel multinomial logit approach. *Energy Economics*, 59, 129-137. https://doi.org/10.1016/j.eneco.2016.06.025
- Mostofi, H. (2022). The frequency use and the modal shift to ICT-based mobility services. *Resources, Environment and Sustainability*, 9. https://doi.org/10.1016/j.resenv.2022.100076
- Fikire, A. H. (2021). Determinants of urban housing choice in Debre Berhan Town, North Shewa zone, Amhara Region, Ethiopia. *Cogent Economics & Finance*, 9(1). https://doi.org/10.1080/23322039.2021.1885196
