---
title: "Lecture 11: Ordinal Response Models (Ordered Logit/Probit)"
type: concept
status: mature
tags: [ordinal-response, ordered-probit, ordered-logit, brant-test, limited-dependent-variable]
sources: ["[[sources/slides-9-ordinal-response-models]]"]
related: ["[[concepts/binary-response-models]]", "[[concepts/multinomial-logit-model]]"]
lecture: 11
assignment: []
updated: 2026-09-04
---

> **How to read this page**: this is Topic 9, a direct continuation of [[concepts/binary-response-models]] (binary dependent variable, Topic 7) and a parallel to [[concepts/multinomial-logit-model]] (unordered categorical dependent variable, Topic 8). If you're not yet familiar with the idea "discrete dependent variable, estimated by Maximum Likelihood instead of OLS," read [[concepts/binary-response-models]] first — that page builds the log-likelihood framework, LR test, and marginal effects that this page reuses almost unchanged, adding only one extra layer of complexity: **order** among the categories.

**Lecture 11** in the syllabus (CO Topic 9) — no dedicated assignment yet.

## What is the ordinal response problem?

### What an "ordered" dependent variable means

Many outcome variables in economic/social surveys are **discrete** (taking only a finite number of values) **and naturally ordered**, but have **no measurement unit** — meaning the distance between levels has no clear numerical meaning.
Two opening examples:

- **Self-reported health status** on a Likert scale: poor / average / good / very good.
- **Level of agreement with a statement**: strongly disagree / disagree / neutral / agree / strongly agree.

The running example of this lecture (reused throughout every later section of this page): **weekly eating-out frequency** (`eatout`), first illustrated with 3 simple levels (0 = no times; 1 = 1–2 times/week; 2 = 3 or more times), later expanded by the practice dataset into 5 more detailed levels (see section 7).
What all these examples share: we know "more" or "less," but **we don't know whether the distance between 'poor' and 'average' equals the distance between 'average' and 'good'** — this is precisely the defining feature of "ordinal."

### Why not OLS, and why MNL "wastes" information

The question this raises: if this variable is the dependent variable, what do we estimate it with?

|Approach |Usable? |Why |
|---|---|---|
| **OLS** ([[concepts/linear-regression-model]]) |No |The variable has no measurement unit — running OLS directly on the codes 0/1/2/3/4 implicitly assumes the distance between every pair of levels is **equal** (distance "0→1" = distance "3→4"), an assumption that is almost never true for Likert or self-reported frequency data. The OLS coefficient in this case has no sound econometric interpretation. |
| **MNL** ([[concepts/multinomial-logit-model]]) |Technically usable, but not advisable |MNL treats each category as an independent choice, assuming no ordering at all — so it is **technically usable**, but (a) it is unnecessarily complex (estimating a separate coefficient set for each category relative to the base category — with 5 categories that's 4 separate coefficient sets) and (b) it **wastes the ordering information** already present in the data — we know "3–5 times/month" lies between "1–2 times" and "6–10 times," but MNL does not exploit that information. |
| **Ordered Probit / Ordered Logit** |The right tool |Purpose-built for discrete ordered variables: more parameter-efficient than MNL (only one shared coefficient set $\beta$ — see section 9) and does not impose the "equal distance" assumption the way OLS does. |

**Intuition to remember**: this problem sits **between** binary response (only 2 categories, no "order" to speak of since there is only one boundary) and MNL (many categories but no order).
Ordinal response is "many categories **and** ordered" — that allows a **single continuous index** to describe the entire phenomenon, instead of the multiple coefficient sets MNL requires. That is exactly the "latent variable" idea in section 2.

## Latent variable framework — the core (and hardest) idea

This is the foundational concept of the whole model, and also the point most likely to confuse newcomers. Intuition:

> Behind the discrete number $y$ that we *observe* (0, 1, 2, 3, 4…), there is a **continuous, unobserved** variable $y^*$ — called the **latent variable** or **index variable** — measuring the "true" degree/intensity of the phenomenon under study. When a survey forces the respondent to pick one of a finite set of levels, that continuous number gets "cut" into discrete intervals.

A concrete example with `eatout`: each individual has a "propensity to eat out" — influenced by income, age, marital status, personal preference — and this propensity is by nature a **continuous** quantity (no one truly "jumps" abruptly from level 0 to level 5 times/month; the propensity rises smoothly with its determinants). But when surveyed, we can only ask "how many times a month do you eat out, choose one of 5 bins" — the answer $y$ only tells us which interval that continuous propensity **falls into**, not its exact value.
Another, easier-to-picture example: a customer's "satisfaction level" is really a **continuous feeling** in that person's mind (could be very satisfied, mildly satisfied, moderately satisfied…) — but the survey form only allows "poor / average / good / very good," so the observed answer is just a **discretized version** of that continuous feeling.

Formally: $y^*$ is modeled as a linear function of $X$ plus an error term, exactly the same structure as the PRE in [[concepts/linear-regression-model]]:

$$y^*=\beta X+\varepsilon = \beta_1 x_1 + \cdots + \beta_k x_k + \varepsilon$$

The higher $y^*$, the higher the intensity/propensity of the phenomenon — matching observed $y$ in terms of *ordering*, but different in *nature*: $y^*$ is continuous and unbounded above/below, while $y$ takes only a finite number of integer values.

**Picturing it on a number line**: place $y^*$ on a continuous number line; the **cutpoints** (section 3) divide this line into segments — each segment corresponds to one level of observed $y$:

```
 y* : ───────────●────────────●────────────●────────────●───────────→
                 u1           u2           u3           u4
        y=0      │     y=1    │     y=2    │     y=3    │     y=4
       (No)      │  (1-2/th)  │  (3-5/th)  │ (5-10/th)  │  (11+/th)
```

Any individual whose $y^*$ falls between $u_2$ and $u_3$ will be observed as $y=2$, regardless of the exact value of $y^*$ within that segment — this is precisely why $y^*$ is called "latent": it exists theoretically, governs the observed behavior, but its own value is **never directly measurable**, exactly the way the (population) $\beta$ is never directly observed in the LRM — the only difference here is that the "unobservable" thing is the variable itself, not the coefficient.

## Cutpoints (threshold parameters)

With $J$ categories (e.g. $J=3$: $y\in\{0,1,2\}$ as first illustrated above), $J-1$ **cutpoints** $u_1<u_2<\cdots<u_{J-1}$ are needed to divide the $y^*$ axis into $J$ segments. The rule linking $y^*$ to the observed $y$ (illustrated with 3 categories):

(read: $y=0$ if $y^*\le u_1$; $y=1$ if $u_1<y^*\le u_2$; $y=2$ if $y^*> u_2$)

**What cutpoints mean**: they are **threshold parameters** — not an "intercept" in the usual OLS sense, even though R's software output lists them under the name **"Intercepts."** The model estimates $\beta$ **and** the cutpoints $u_j$ **simultaneously** by Maximum Likelihood (section 5) — both are unknown parameters, neither is given in advance.

**An important structural detail, easy to overlook**: the equation $y^*=\beta X+\varepsilon$ **has no separate intercept $\beta_0$** the way the LRM's PRE does. Reason: with only one cutpoint (the binary case, $J=2$), having both a free cutpoint *and* a free intercept would make the model **unidentified** (identification) — the two parameters "compete" for the role of shifting the number line in the same direction. The ordinal model resolves this by dropping $\beta_0$ entirely from $X\beta$, letting the cutpoints $u_j$ take over that "positioning" role.
This is clearly visible in the estimation code in the practical example (section 7): the model formula `eatout ~ age + whours + income + homeown + gender + inrelationship + married` has no intercept term, and R separately reports "No coefficients" for the intercept in the null model — only the "Intercepts:" section (i.e., the cutpoints) gets estimated.

**Cutpoints "in the raw"**: the null model (only cutpoints, no $X$ variables — `eatout ~ 1`) in the practical example section 7.3 is the clearest way to see cutpoints working independently of $\beta$ — since $X\beta=0$, the cutpoints estimated in the null model are exactly the thresholds delimiting the marginal/unconditional distribution of $y$, with no adjustment for individual characteristics.

## Probability of each category — deriving the formula

### Illustrative case: 3 categories, normal $\varepsilon$ assumption (Ordered Probit)

**$Pr(y=0)$**: using the rule from section 3,

$$Pr(y=0)=Pr(y^*\le u_1)=Pr(\beta X+\varepsilon\le u_1)=Pr(\varepsilon\le u_1-\beta X)=\Phi(u_1-\beta X)$$

where $\Phi(\cdot)$ is the cumulative distribution function (CDF) of the standard normal distribution.

**$Pr(y=2)$** (the highest category), by the same reasoning:

$$Pr(y=2)=Pr(y^*> u_2)=Pr(\varepsilon> u_2-\beta X)=Pr(\varepsilon\le \beta X-u_2)=\Phi(\beta X-u_2)$$

(the last step uses the symmetry of the normal distribution around 0).

**$Pr(y=1)$** (the middle category) — is the difference of two cumulative probabilities:

$$Pr(y=1)=Pr(u_1<y^*\le u_2)=Pr(y^*\le u_2)-Pr(y^*\le u_1)=\Phi(u_2-\beta X)-\Phi(u_1-\beta X)$$

**The sum always equals 1**: $\Phi(\beta X-u_2)=1-\Phi(u_2-\beta X)$ (symmetry), so $Pr(y=0)+Pr(y=1)+Pr(y=2)=\Phi(u_1-\beta X)+[\Phi(u_2-\beta X)-\Phi(u_1-\beta X)]+[1-\Phi(u_2-\beta X)]=1$ — a useful self-check of the formulas when computing by hand.

### Generalizing to $J$ categories

The theory above is illustrated with 3 categories, but the practical example in section 7 uses **5 categories** (`eatout` = No / 1–2 / 3–5 / 5–10 / 11+ times/month) — so the two need to be connected. With $J$ categories $y\in\{0,1,\dots,J-1\}$ and $J-1$ cutpoints $u_1<\cdots<u_{J-1}$, the same logic from section 4.1 generalizes to:

(the second line: $Pr(y=j)=\Phi(u_{j+1}-\beta X)-\Phi(u_j-\beta X)$ for $j=1,\dots,J-2$, i.e. the categories in between)

For `eatout` ($J=5$, cutpoints $u_1,u_2,u_3,u_4$):

$$Pr(No)=\Phi(u_1-X\beta),\quad Pr(1\text{–}2)=\Phi(u_2-X\beta)-\Phi(u_1-X\beta),\quad\dots,\quad Pr(11+)=1-\Phi(u_4-X\beta)$$

Exactly 5 probability formulas, each corresponding to one row in the "Intercepts" table R reports (section 7).

## Log-likelihood function

(where $Y_{ik}=1$ if $y_i=k$, and $0$ otherwise)

The structure is **exactly the same** as the log-likelihood of binary Logit/Probit ([[concepts/binary-response-models]]) and of MNL ([[concepts/multinomial-logit-model]]) — the only difference is how $Pr(y_i=k)$ is computed (here, the difference of two consecutive CDFs, instead of MNL's softmax formula or the simple binary formula). This is the "common thread" running through the entire Part 2 of the course, which the Connections section (section 12) will revisit: every discrete-choice model in the course is estimated by Maximum Likelihood on this same general log-likelihood framework, only swapping the formula for $Pr(y_i=k)$.

## Ordered Logit vs. Ordered Probit

The same logic that distinguishes binary Logit/Probit ([[concepts/binary-response-models]]) applies: the difference lies in the **assumed distribution of the error $\varepsilon$** in the equation $y^*=\beta X+\varepsilon$.

| |Distribution of $\varepsilon$ |Link function |e.g. $Pr(y=0)$ |
|---|---|---|---|
| **Ordered Probit** |Normal | $\Phi(\cdot)$ | $\Phi(u_1-\beta X)$ |
| **Ordered Logit** |Logistic | $\Lambda(x)=\dfrac{1}{1+e^{-x}}$ | $\Lambda(u_1-\beta X)$ |

**Difference from the binary case**: in the binary model, **Logit** is usually preferred (the marginal effect has a closed form, easier to compute than Probit). In the **ordinal** model, the practical convention runs the opposite direction: **"Probit is more popular"** in practice. There is no specific theoretical reason for this — note that this is a practical statement (convention), not a theorem.

## Full example: eating-out frequency (`eatout`)

### Data

|Variable |Meaning |
|---|---|
| `eatout` (depvar) |Eating-out frequency/month — ordinal, 5 levels: 0 = "No"; 1 = "1–2 times/month"; 2 = "3–5 times/month"; 3 = "6–10 times/month"; 4 = "11 times/month or more" |
| `age` |Age (years) |
| `whours` |Weekly working hours |
| `income` |Monthly income (million VND/month) |
| `homeown` |1 if homeowner, 0 otherwise |
| `gender` |1 if male, 0 otherwise |
| `marriage` |original text-valued variable: "single" / "inrelationship" / "married" → generates 2 dummies `inrelationship`, `married` (base group is "single") |

**Distribution of `eatout`** (`barplot(table(data$eatout))`): No ≈ 280 observations (largest), 1–2/month ≈ 160, 3–5/month ≈ 235, 5–10/month ≈ 220, 11+/month ≈ 50 (smallest) — a skewed distribution, concentrated heavily on "No" and the middle levels, thinning out at the highest level.

### Null model (cutpoints only, no X variables)

| Cutpoint | Value | Std. Error | t value |
|---|---|---|---|
| No \| 1-2/month | −0.5425 | 0.0431 | −12.59 |
| 1-2/month \| 3-5/month | −0.0918 | 0.0409 | −2.25 |
| 3-5/month \| 5-10/month | 0.5611 | 0.0432 | 12.98 |
| 5-10/month \| 11 or more | 1.6162 | 0.0675 | 23.94 |

Residual Deviance: 2834.382; AIC: 2842.382. This is exactly the "cutpoints in the raw" illustration mentioned in section 3 — with no explanatory variables at all, these thresholds simply reflect the marginal distribution of `eatout` in the sample.

### Full model (Ordered Probit)

**Coefficients $\beta$** (the effect on $y^*$, not yet on $Pr(y=k)$ — see section 8):

|Variable | Value | Std. Error | t value | p-value |
|---|---|---|---|---|
| `age` | −0.2900 | 0.0123 | −23.53 | 0.000 |
| `whours` | 0.0045 | 0.0025 | 1.81 | 0.071 |
| `income` | −0.0009 | 0.0049 | −0.19 | 0.849 |
| `homeown` | −2.8831 | 0.1307 | −22.06 | 0.000 |
| `gender` | −0.0760 | 0.0832 | −0.91 | 0.361 |
| `inrelationship` | 2.9727 | 0.1373 | 21.65 | 0.000 |
| `married` | 0.2040 | 0.1045 | 1.95 | 0.051 |

**Cutpoints (Intercepts):**

| Cutpoint | Value | Std. Error | t value |
|---|---|---|---|
| No \| 1-2/month | −9.4303 | 0.4167 | −22.63 |
| 1-2/month \| 3-5/month | −8.2827 | 0.3945 | −21.00 |
| 3-5/month \| 5-10/month | −6.5769 | 0.3602 | −18.26 |
| 5-10/month \| 11 or more | −3.7760 | 0.3215 | −11.74 |

Residual Deviance: 1446.688; AIC: 1468.688 (a sharp drop compared to the null model → adding explanatory variables substantially improves fit).

**Why do the full model's cutpoints "look very different" from the null model's** (jumping from roughly −0.5→1.6 to roughly −9.4→−3.8)? This is **not a contradiction** but a direct consequence of adding $X\beta$ to the formula: in the null model, $X\beta=0$ so the cutpoints are directly the thresholds of the marginal distribution; in the full model, variables like `age` (measured in years, not standardized) or `whours` contribute a large amount to $X\beta$, so the cutpoints must shift accordingly to keep the predicted probabilities sensible. Cutpoints and $\beta$ must always be read **together**, never separately.

**p-value** (two-tailed, computed from $t$ via the normal distribution — `pnorm`): at $\alpha=5\%$, the statistically significant variables are `age`, `homeown`, `inrelationship` (p<0.001); `married` is borderline (p=0.051, not significant at exactly 5% but significant at 10% — the same "the $\alpha$ threshold determines the conclusion" lesson as in [[concepts/linear-regression-model]] section 7.4); `whours`, `income`, `gender` are not statistically significant.

### LR test for overall significance — the OLS overall F-test equivalent

Comparing the null model (7.2) and the full model (7.3) with a likelihood-ratio test (`anova(OIM, oprobit)`):

$$LR = 2(LL_{full}-LL_{null}) \sim \chi^2_{q}$$

| Model | Resid. df | Resid. Dev |
|---|---|---|
| Null | 939 | 2834.382 |
| Full | 932 | 1446.688 |

$q=939-932=7$ (exactly the number of added variables), LR stat = 1387.694, $p\approx0$ (< 2.2e-16) → **strongly reject** $H_0$: all 7 slope coefficients = 0. This is the **Maximum-Likelihood version of the overall F-test** in [[concepts/linear-regression-model]] section 8.5 — the same "compare restricted vs. unrestricted" logic, only $RSS$ is replaced by deviance/log-likelihood. **The same interpretation lesson applies**: a significant LR test only says "not all coefficients are zero" — it does not say the model is correctly specified, and it cannot detect omitted variables.

### Predicted probabilities (fitted values)

For the first observation in the sample, the model produces 5 probabilities (summing exactly to 1):

$Pr(No)\approx0.0000115$, $Pr(1\text{–}2)\approx0.0010$, $Pr(3\text{–}5)\approx0.0829$, $Pr(5\text{–}10)\approx0.8385$, $Pr(11+)\approx0.0776$ — this individual almost certainly belongs to the "5–10 times/month" group (83.85% probability).

**Plot of $Pr(y=4)$ (eating out ≥11 times/month) against age**: the plot of predicted `Pr(11+)` against `age` shows a clearly **decreasing** relationship — probability near 1.0 at age ~18, dropping sharply past age 20 (~0.85), continuing to fall and reaching near 0 from around age 30 onward. This is a visual illustration of the **negative** sign of $\beta_{age}=-0.29$: the older a person is, the lower their propensity toward high-frequency eating out.

### Prediction and the confusion matrix

`predict(oprobit)` assigns each observation to the category with the highest predicted probability. The matrix cross-tabulating actual (rows) against predicted (columns):

|Actual \ Predicted | No | 1-2/mo | 3-5/mo | 5-10/mo | 11+ |
|---|---|---|---|---|---|
| **No** | 236 | 29 | 10 | 2 | 0 |
| **1-2/month** | 53 | 52 | 51 | 4 | 0 |
| **3-5/month** | 15 | 29 | 154 | 37 | 0 |
| **5-10/month** | 1 | 3 | 51 | 155 | 11 |
| **11 or more** | 0 | 0 | 0 | 21 | 29 |

Overall correct-prediction rate (`sum(diag(tab))/sum(tab)`): **0.6638** (66.4%). But this overall figure **hides large differences across categories**: the "No" group (236/277≈85%) and "5-10/month" (155/221≈70%) are predicted fairly well, while the "1-2/month" group is only correct 52/160≈32.5% of the time — the model frequently confuses this group with "No" (53 cases) or "3-5/month" (51 cases) — its two neighbors on the $y^*$ axis. This is why **the overall accuracy rate alone should not be the only thing reported** — the full confusion matrix should be presented too.

### Prediction for a specific individual

Prediction is illustrated for two hypothetical profiles, identical except for relationship status:

- `person1`: age=23, whours=60, income=30, homeown=0, gender=0, `inrelationship=0`, married=0 → predicted: **"5-10/month"**.
- `person2`: identical to person1 but `inrelationship=1` → predicted: **"11 or more"**.

Changing just **one** dummy variable (`inrelationship`: 0→1) is enough to push the predicted category up a full level — consistent with the large, strongly significant coefficient $\beta_{inrelationship}=2.97$ (section 7.3): having a partner substantially raises the eating-out propensity $y^*$, enough to cross the cutpoint $u_4=-3.776$ and fall into the highest group.

### Pseudo R² (rarely used)

`PseudoR2(oprobit, which=c("CoxSnell","Nagelkerke","McFadden"))`: CoxSnell = 0.770, Nagelkerke = 0.811, McFadden = 0.490. The title to remember: **"(RARELY USED)"** — these pseudo-R² measures do not have the same scale or interpretation as the linear $R^2$ in [[concepts/linear-regression-model]] section 9, and should not be used as the primary criterion for evaluating model fit.

### Testing the joint significance of a group of coefficients

Question: are `inrelationship` and `married` **jointly** significant? (`lmtest::lrtest(oprobit, c("inrelationship","married"))`) — comparing the full model with a model that drops these two variables:

| Model | #Df | LogLik |
|---|---|---|
|Full (includes `inrelationship`, `married`) | 11 | −723.34 |
|Restricted (drops both variables) | 9 | −1095.00 |

Chisq = 743.32, df=2, $p<2.2\times10^{-16}$ → strongly reject $H_0$: both coefficients are jointly zero. This is the ML version of the **F-test for a group of coefficients** in [[concepts/linear-regression-model]] section 8 (e.g. jointly testing `chighland`/`ccoastal`) — the same "force the coefficients to 0 (restricted) then compare against the full model (unrestricted)" logic, only the $F$ statistic based on $RSS$ is replaced by a $\chi^2$ statistic based on log-likelihood.

## Interpreting coefficients and marginal effects

### Why $\beta$ cannot be read directly

**The estimated coefficient $\beta$ is the marginal effect on the latent variable $y^*$, not on any probability $Pr(y=k)$.** Researchers almost never care directly about $\beta$ (since $y^*$ is unobserved, with no concrete measurement unit) — what actually matters is: as $X$ increases, how much does **the probability of falling into each specific category** change.

### Marginal effect formula

With $Pr(y=0)=\Phi(u_1-X\beta)$:

$$\frac{\partial Pr(y=0)}{\partial X_k}=-\beta_k\,\phi(u_1-X\beta)$$

($\phi$ is the probability density function — pdf — of the normal distribution). Each category $k$ has its **own** marginal-effect formula (the derivative of the difference of two $\Phi$'s for middle categories), and since $\phi(\cdot)>0$ is always positive, **the sign of the marginal effect on $Pr(y=0)$ is opposite to the sign of $\beta_k$** — this is the key point for understanding why the sign of the marginal effect can "flip" across categories.

### Numerical example — full marginal-effects table

|Variable |ME on Pr(No) |ME on Pr(1-2) |ME on Pr(3-5) |ME on Pr(5-10) |ME on Pr(11+) |
|---|---|---|---|---|---|
| `age` | +0.044 | +0.069 | −0.072 | −0.040 | 0.000 |
| `whours` | −0.001 | −0.001 | +0.001 | +0.001 | 0.000 |
| `income` | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| `homeown` | +0.689 | +0.152 | −0.528 | −0.312 | −0.001 |
| `gender` | +0.011 | +0.018 | −0.019 | −0.011 | 0.000 |
| `inrelationship` | −0.369 | −0.408 | +0.108 | +0.659 | +0.009 |
| `married` | −0.029 | −0.049 | +0.048 | +0.030 | 0.000 |

**Three important observations, illustrated directly with the numbers:**

1. **The sum of marginal effects across one row always approximates 0** (e.g. `age`: $0.044+0.069-0.072-0.040+0.000\approx0.001\approx0$, the small deviation from rounding to 3 decimal places). This is a necessary logical consequence: total probability always equals 1, so when $X$ changes, probability can only **shift/redistribute** among categories, never "create" new probability — the sum of the derivatives must equal 0.

2. **The sign of the marginal effect at the two ends (lowest/highest category) is usually opposite, and the sign at the middle can also differ**. For example `age` has $\beta_{age}=-0.29$ (negative — higher age → lower $y^*$, i.e. lower eating-out propensity), but the marginal effect on $Pr(No)$ is **positive** (+0.044: higher age → higher probability of "not eating out" — sensible, correct direction), while the marginal effect on $Pr(3\text{-}5)$ and $Pr(5\text{-}10)$ is **negative** (higher age → lower probability of falling into the mid-high levels). This is exactly the numerical example of the intuitive rule: a negative $\beta$ does not mean "decreases every probability" — it means **"pushes the probability distribution toward the lower categories,"** so probability at the low end rises while probability at the high end falls.

3. **`homeown`** ($\beta=-2.88$, strongly negative): the marginal effect on $Pr(No)$ is **+0.689** — extremely large; homeowners have a "not eating out" probability that is 68.9 percentage points higher than non-homeowners (holding other factors constant), while the marginal effect on $Pr(3\text{-}5)$ is −0.528 and on $Pr(5\text{-}10)$ is −0.312 — all consistent with the negative sign of $\beta$: homeowners have a lower eating-out propensity, so probability piles up toward the lower levels.

### Statistical inference on marginal effects (not just on $\beta$)

Each marginal effect also has its own SE, t-value, p-value — statistical significance can be tested **directly on the marginal effect**, not only on $\beta$. For example, the marginal effect on $Pr(No)$ (`$ME.0`): `age` = 0.044 (SE=0.004, t=10.62, p<0.001); `homeown` = 0.689 (SE=0.032, t=21.28, p<0.001); `inrelationship` = −0.369 (SE=0.027, t=−13.70, p<0.001) — all three are very strongly significant, matching the significance of their corresponding $\beta$. But note: **statistical significance of $\beta$ does not automatically guarantee statistical significance of the marginal effect in every category** — because the marginal-effect formula also depends on $\phi(\cdot)$ (which differs across categories and $X$ values), so in principle the SE of the marginal effect and of $\beta$ need not lead to the same test conclusion — even though in this specific example they do match.

## Ordered Logit — numerical example and comparison with Ordered Probit

Re-running the exact same equation from section 7.3 with `method="logistic"` instead of `"probit"`:

|Variable | $\beta$ (Logit) |$\beta$ (Probit, section 7.3) |Logit/Probit ratio |
|---|---|---|---|
| `age` | −0.5248 | −0.2900 | 1.81 |
| `whours` | 0.0076 | 0.0045 | 1.71 |
| `income` | −0.0016 | −0.0009 | 1.72 |
| `homeown` | −5.2108 | −2.8831 | 1.81 |
| `gender` | −0.1287 | −0.0760 | 1.69 |
| `inrelationship` | 5.3464 | 2.9727 | 1.80 |
| `married` | 0.3489 | 0.2040 | 1.71 |

**Cutpoints (Logit)**: $0|1=-17.10$, $1|2=-15.04$, $2|3=-11.95$, $3|4=-6.88$ (all increasing, strongly statistically significant).

> **Additional observation** (computed from the two coefficient tables above): the Logit/Probit coefficient ratio hovers fairly evenly around **1.7–1.8** for every variable. This matches a familiar rule of thumb in econometrics — the logistic distribution has variance $\pi^2/3\approx3.29$ while the standard normal has variance 1, so logit coefficients are typically about $\sqrt{\pi^2/3}\approx1.81$ times larger than their probit counterparts. This number should not be used to directly compare the **magnitude of effects** between the two models (as already noted in [[concepts/binary-response-models]]) — it is only useful as a quick check of whether the two models give "consistent" results (same signs, roughly constant coefficient ratio).

The sign and statistical significance level of every coefficient are **identical** between the two models (the same variables significant, the same variables not) — a good sign that the conclusions are not sensitive to the choice of Logit or Probit in this example.

## Parallel regression assumption (proportional odds assumption) and the Brant test

### What this assumption is, an intuitive understanding

Ordered Logit/Probit assumes **the same coefficient set $\beta$ for every category threshold (cutpoint)** — called the **parallel regression assumption** (sometimes also called the **proportional odds assumption**, especially in the ordered logit context). Recall the formula from section 4: each $Pr(y=j)$ uses **the same** $\beta X$ (only the cutpoint $u_j$ subtracted differs). In other words, the model assumes the effect of each variable $X_k$ on "the propensity to move up one level" is **the same, regardless of which boundary is being crossed** — the boundary between "No" and "1-2/month" is affected by `age` in exactly the same magnitude as the boundary between "5-10" and "11+".

**The name "parallel"** comes from the following picture: if each boundary $j$ is drawn as its own "regression line" against $X$ (of the form $u_j - X\beta$), these $J-1$ lines differ only in their **intercept** (cutpoint $u_j$) but share the **same slope** $\beta$ for every $X$ — i.e. they are **parallel** to one another. If this assumption is false — i.e. each boundary is actually affected differently by $X$ — forcing a shared $\beta$ will make the estimates **biased**, because the model is imposing a structure that does not match the real data.

### Brant test

- $H_0$ (null hypothesis) of the Brant test: **the parallel regression assumption holds** (i.e. $\beta$ is truly the same across every threshold).
- If $H_0$ is **rejected** → the assumption is violated → an alternative model should be considered — **MNL** is the commonly used alternative (does not constrain the coefficients to be the same across thresholds — in exchange, it loses the ordering information — see [[concepts/multinomial-logit-model]]). *(Generalized ordered logit and other models are outside the scope of this page.)*

**Numerical example** (`brant::brant(ologit)`, run on the Ordered Logit model from section 9):

| Test for | $\chi^2$ | df | p |
|---|---|---|---|
| Omnibus | 17.24 | 21 | 0.7 |
| age | 2.94 | 3 | 0.4 |
| whours | 5.98 | 3 | 0.1 |
| income | 1.28 | 3 | 0.7 |
| homeown | 1.18 | 3 | 0.7 |
| gender | 2.20 | 3 | 0.5 |
| inrelationship | 0.52 | 3 | 0.9 |
| married | 0.38 | 3 | 0.9 |

Every p-value (including Omnibus, the overall test for all coefficients jointly) is **greater than 0.05** → **fail to reject** $H_0$ → the conclusion: **"parallel regression assumption holds for all coefficients"** — the Ordered Logit estimates in this `eatout` example are reliable, no need to switch to MNL.

## Exam traps

1. Interpreting $\beta$ directly as the effect on $Pr(y=k)$ — wrong; $\beta$ is the effect on the **latent variable $y^*$**, the marginal effect must be computed separately for each probability (section 8.2).
2. Expecting the marginal effect's sign to be **the same across every category** for a given variable — wrong; the numerical example for `age` in section 8.3 shows the marginal effect can be **positive** at the lowest category and **negative** at the middle/higher categories, even though $\beta$ has only one sign.
3. Forgetting that a variable's marginal effects summed across **all** categories always approximate 0 (probability only shifts between levels, it isn't "created") — if a hand calculation's total is far from 0, the formula was likely applied incorrectly.
4. Treating "Intercepts" in R's output (`polr`) as OLS-style intercepts — wrong, they are **cutpoints/threshold parameters**; and their values are **not fixed** — they shift substantially depending on how many $X$ variables the model has and their scale (compare the null-model vs. full-model cutpoints in sections 7.2 and 7.3, despite sharing the same dependent variable).
5. Skipping the Brant test when reporting Ordered Logit/Probit — without testing it, there's no way to know whether the parallel regression assumption holds; if it's violated and an ordered model is still used, the estimated coefficients are biased.
6. Getting the direction of the Brant test's $H_0$ backwards: $H_0$ = **the assumption holds**, not "the assumption is violated". Rejecting $H_0$ is the sign of a **violation**; failing to reject means the assumption is fine (as in the numerical example in section 10.2, where every p>0.05 → the assumption holds).
7. Confusing an Ordinal response (ordered, uses Ordered Logit/Probit) with a Multinomial response (unordered, uses MNL) — see [[concepts/multinomial-logit-model]]; or running OLS directly on the ordinal variable's numeric codes, implicitly assuming the distance between levels is equal (section 1.2).
8. Using Pseudo R² (McFadden/CoxSnell/Nagelkerke) as the main fit criterion for the model — these measures are noted as **"rarely used"**, and have no scale/interpretation equivalent to linear $R^2$.
9. Reporting only the overall correct-prediction rate (e.g. 66.4% in section 7.6) without checking the full confusion matrix broken down by category — a model can "look good" overall while predicting a specific category very poorly (e.g. "1-2/month" is only correct ~32.5% of the time in this example).
10. Directly comparing Ordered Logit and Ordered Probit coefficient magnitudes as if they shared the same scale — the two models have different error-term scales (logistic vs. normal); only compare sign, significance level, or predicted probabilities, not raw coefficient magnitude directly (though the ~1.8× ratio in section 9 is a useful rule of thumb for checking consistency).

## Connections to the rest of the course

Ordinal response models sit between two other discrete-choice models in Part 2 of the course, all sharing the log-likelihood/Maximum Likelihood framework:

- **[[concepts/binary-response-models]]** (Topic 7): the special case $J=2$ — only 1 cutpoint is needed, and in practice that cutpoint is usually fixed (typically at 0) so an ordinary intercept $\beta_0$ can be estimated instead — this is why binary Logit/Probit "look like" they have an OLS-style intercept while the ordinal model doesn't (section 3). The LR test framework, the Wald test, and the Logit/Probit distinction by error-distribution assumption are all inherited unchanged by the ordinal model.
- **[[concepts/multinomial-logit-model]]** (Topic 8): applies when the categories are **unordered** — it is the fallback when the Brant test rejects the parallel regression assumption (section 10.2). MNL estimates a separate coefficient set for each category relative to the base category, "spending" more parameters but without the "parallel" constraint the ordinal model imposes.
- The log-likelihood framework $LL=\sum_i\sum_k Y_{ik}\ln Pr(y_i=k)$ (section 5) is the **common denominator** of all three models (binary, ordinal, MNL) — the only difference between them is the formula used to compute $Pr(y_i=k)$.

The foundational question "why is Maximum Likelihood needed instead of OLS when the dependent variable is discrete" is laid out in [[concepts/binary-response-models]] — worth reading that page first if you need to review from scratch before moving on to the more complex variants (ordinal, MNL, and the count models in Topic 10).

## Real-world application references

Three recent papers illustrating ordered logit/probit models in real-world economic research (Lecture 11 syllabus):

- Kolog, J. D., Asem, F. E., & Mensah-Bonsu, A. (2023). The state of food security and its determinants in Ghana: an ordered probit analysis of the household hunger scale and household food insecurity access scale. *Scientific African*, 19, e01579. https://doi.org/10.1016/j.sciaf.2023.e01579
- Chen, F., Yu, D., & Sun, Z. (2023). Investigating the associations of consumer financial knowledge and financial behaviors of credit card use. *Heliyon*, 9(1), E12713. https://doi.org/10.1016/j.heliyon.2022.e12713
- Ramachandran, R., Sudhir, S., & Unnithan, A. B. (2021). Exploring the relationship between emotionality and product star ratings in online reviews. *IIMB Management Review*, 33(4), 299-308. https://doi.org/10.1016/j.iimb.2021.12.002
