---
title: "Lecture 2: Functional Forms"
type: concept
status: mature
tags: [functional-forms, elasticity, interaction, linear-regression]
sources: ["[[sources/slides-2-functional-forms]]"]
related: ["[[concepts/linear-regression-model]]"]
lecture: 2
assignment: ["Assignment 1: Linear Regression Model with functional forms"]
updated: 2026-09-04
---

> **How to read this page**: this page directly extends assumption **A1 (Linearity)** from [[concepts/linear-regression-model]] — "linear regression model" means a model that is linear in the **parameters** $\beta$, **not necessarily** linear in the **variables** $X$ or $Y$. If you haven't read section 4 (the five OLS assumptions) of the linear regression page yet, read it first — every technique below (log-log, log-lin, lin-log, quadratic, interaction term) is simply a way of transforming $X$ and/or $Y$ before running the regression, so that the model *remains* linear in $\beta$ (so OLS still applies exactly as-is via the formula $b=(X'X)^{-1}X'y$) while still being able to represent nonlinear economic relationships found in reality.

**Lecture 2** in the syllabus (CO Topic 2) — Assignment 1: Linear Regression Model with functional forms.

## Why go beyond the linear form?

In the pure linear form $Y=\beta_0+\beta_1X+\varepsilon$, the coefficient $\beta_1$ implicitly imposes a fairly strong economic assumption: **each additional unit of $X$ always produces exactly $\beta_1$ units of change in $Y$, regardless of the starting level of $X$**. For example, if $\beta_{schooling}=2.26$ (thousand VND/hour) in a linear model, then going from 12 to 13 years of schooling raises the wage by exactly 2.26 thousand VND/hour, and going from 17 to 18 years of schooling also raises it by exactly 2.26 — the same **absolute** increase, regardless of whether the base wage is high or low.

Many economic relationships do not behave this way in reality:

- **Return to education is usually expressed in percentage terms, not in absolute monetary units.** "An extra year of schooling raises wages by x%" is a more natural way to express this than "an extra year of schooling raises wages by x thousand VND," because % automatically scales with the base wage level — for someone with a high wage, the same % increase corresponds to more money in absolute terms, which matches economic intuition.
- **Wages as a function of age are usually non-monotonic.** Wages tend to rise while workers are young (accumulating experience, skills) but may plateau or decline at older ages. A straight line cannot represent this "rise then fall" shape — this requires the **quadratic** form.
- **The effect of one variable may depend on the value of another variable.** For example, the return to education may differ between male and female workers. An additive linear model by default assumes every variable affects $Y$ **independently** of the others — it does not allow two variables to "interact." Testing for this requires an **interaction term**.

**The key point to keep in mind throughout this page**: no matter how "curved" or "nonlinear" the plot of $Y$ against $X$ looks, all the functional forms below **remain linear in $\beta$** — this is exactly the "trick" that lets the OLS tool (which can only solve linear problems) represent nonlinear economic relationships: we do not change the estimation tool, we only **transform the variables** ($\ln X$, $X^2$, $X_1\times X_2$...) before running the regression.

## Running example dataset: wages of young, skilled workers in Vietnam

The slide uses one real dataset throughout to illustrate every functional form — understanding it is necessary to follow the numerical examples in sections 3, 6, and 7 below.

**Data source description (verbatim from the slide)**: data collected from roughly 900–1000 young, skilled workers, across provinces/cities in Vietnam.

|Variable |Meaning |Unit/scale |
|---|---|---|
| `wage` |Wage — **dependent variable** |thousand VND/hour |
| `age` |Age |years |
| `schooling` |Years of schooling |years |
| `tenure` |Time worked for the current employer |months |
| `gender` |Gender |dummy (0 = female, 1 = male) |
| `origin` |Origin/background |dummy (0 = grew up in HCMC, 1 = migrant) |
| `spec` |Field of study: `technology` (base), `science` (natural science), `social` (social science) | categorical |
| `science` |Dummy derived from `spec` |dummy (1 = natural science major) |
| `social` |Dummy derived from `spec` |dummy (1 = social science major) |

**Descriptive statistics** (n = 998, from `psych::describe(data, fast = TRUE)`):

|Variable | n | mean | sd | median | min | max | range |
|---|---|---|---|---|---|---|---|
| `wage` | 998 | 75.02 | 41.81 | 65 | 10 | 302 | 292 |
| `age` | 998 | 23.94 | 4.96 | 24 | 10 | 43 | 33 |
| `schooling` | 998 | 14.03 | 1.58 | 14 | 12 | 18 | 6 |
| `tenure` | 998 | 25.02 | 12.75 | 24 | 1 | 83 | 82 |
| `gender` | 998 | 0.61 | 0.49 | 1 | 0 | 1 | 1 |
| `origin` | 998 | 0.40 | 0.49 | 0 | 0 | 1 | 1 |
| `science` | 998 | 0.31 | 0.46 | 0 | 0 | 1 | 1 |
| `social` | 998 | 0.55 | 0.50 | 1 | 0 | 1 | 1 |

A quick read of this table before moving to the regression coefficients: mean wage is 75.02 thousand VND/hour but varies widely (10–302, range 292 — suggesting a right-skewed distribution, one empirical reason `ln(wage)` is often used as the dependent variable instead of raw `wage`); 61% of workers in the sample are male; 40% are migrants; 31% majored in natural science, 55% in social science (the remainder — the `technology` base group — accounts for about 14%).

From this dataset, the slide runs six different regression models (the four basic functional forms in section 3, plus quadratic in section 6, plus interaction in section 7) on the same set of control variables — allowing a direct comparison of how differently each functional form "reads" the same data.

## Four basic functional forms

### Linear — the baseline

**When to use it**: when theory predicts that one additional unit of $X$ produces a **fixed, absolute** amount of change in $Y$, independent of the current level of $X$ or $Y$. This is the simplest form, requiring no transformation at all — but also the most "rigid" in terms of its economic assumption.

$$Y=\beta_0+\beta_1X+\varepsilon$$

- **Continuous regressor**: $X$ increases by 1 unit → $Y$ changes by $\beta_1$ units (exact, there is no notion of "approximation" here since the relationship is already linear).
- **Dummy regressor**: $\beta_1$ is the difference in mean $Y$ between the two groups defined by $X$ (identical to the dummy-variable interpretation already covered in [[concepts/linear-regression-model]]).

**Numerical example (from the slide, regression on the wage dataset)**:

```
wage ~ age + schooling + tenure + gender + origin + science + social
```

|Variable | Estimate | Std. Error | t value | Pr(>|t|) |
|---|---|---|---|---|
| (Intercept) | 63.22655 | 13.91486 | 4.544 | 6.21e-06 *** |
| `age` | 0.09858 | 0.26065 | 0.378 | 0.70536 |
| `schooling` | 2.25944 | 0.82103 | 2.752 | 0.00603 ** |
| `tenure` | −0.66558 | 0.10136 | −6.566 | 8.32e-11 *** |
| `gender` | 0.46931 | 2.65664 | 0.177 | 0.85981 |
| `origin` | −7.54529 | 2.64807 | −2.849 | 0.00447 ** |
| `science` | −2.55645 | 4.22214 | −0.605 | 0.54499 |
| `social` | −3.79893 | 3.94543 | −0.963 | 0.33585 |

Residual SE = 40.74 (df = 990); $R^2$ = 0.05744; $R^2_{adj}$ = 0.05077; F = 8.618 on (7, 990); p = 2.731e-10.

**Sample interpretation**: "an extra year of schooling raises the average wage by 2.259 thousand VND/hour, holding other variables constant" (statistically significant at the 1% level). This is exactly the number used for comparison in sections 3.2–3.4: same variable `schooling`, same data, but the way the coefficient is "read" changes completely as the functional form changes.

### Log-log (also called Log-linear, Cobb-Douglas)

**When to use it**: when theory predicts a **constant elasticity** relationship — the % change in $Y$ is a fixed proportion of the % change in $X$, regardless of the level of $X$. This is a familiar functional form in production theory (the Cobb-Douglas function $Q=AK^{\alpha}L^{\beta}$ is exactly log-log once both sides are logged) and in studies of return to education, demand for goods (price elasticity)...

$$\ln Y=\beta_0+\beta_1\ln X+\varepsilon$$

With $X$ a continuous variable, $\beta_1$ is exactly the **instantaneous elasticity** of $Y$ with respect to $X$ — a classic measure in microeconomics.

- **Approximate interpretation**: $X$ increases by 1% → $Y$ changes by $\beta_1$ percent.
- **Exact interpretation**: $X$ increases by 1% → $Y$ changes by $b=(1.01^{\beta_1}-1)\times100$ percent.

**Numerical example (from the slide, regression on the wage dataset)**:

```
log(wage) ~ log(age) + log(schooling) + log(tenure) + gender + origin + science + social
```

|Variable | Estimate | Std. Error | t value | Pr(>|t|) |
|---|---|---|---|---|
| (Intercept) | 3.70523 | 0.46038 | 8.048 | 2.39e-15 *** |
| `log(age)` | 0.03129 | 0.07559 | 0.414 | 0.67896 |
| `log(schooling)` | 0.36100 | 0.14695 | 2.457 | 0.01419 * |
| `log(tenure)` | −0.17078 | 0.02462 | −6.936 | 7.25e-12 *** |
| `gender` | 0.02054 | 0.03311 | 0.620 | 0.53521 |
| `origin` | −0.10287 | 0.03300 | −3.117 | 0.00188 ** |
| `science` | −0.02639 | 0.05259 | −0.502 | 0.61586 |
| `social` | −0.02822 | 0.04914 | −0.574 | 0.56595 |

Residual SE = 0.5076 (df = 990); $R^2$ = 0.06106; $R^2_{adj}$ = 0.05442; F = 9.197 on (7, 990); p = 4.704e-11.

$\beta_{\ln schooling}=0.361$ (significant at the 5% level):

- **Approximate**: a 1% increase in years of schooling → wage increases by approximately **0.361%**.
- **Exact**: $b=(1.01^{0.361}-1)\times100=0.360\%$ — very close to the approximate figure (as expected from the rule: the smaller $\beta_1$ is, the closer the approximate and exact values are).

> **Source note (internal inconsistency in the slide)**: on the exact slide presenting the "exact" calculation for log-log, the formula shown uses the exponent $\beta_1=0.297$ — i.e. $b=(1.01^{0.297}-1)\times100=0.296$ — which **does not match** the coefficient $\beta_{\ln schooling}=0.361$ that the same slide just stated on the "approximate" line right above it (and which is also the actual figure in the log-log regression table above: 0.36100). Even stranger: the verbal conclusion right after the calculation states "the result is 0.360 percent" — which matches exactly if $\beta_1=0.361$ (not 0.297) is used in the formula. This "0.297" figure is most likely a leftover from an older regression/dataset version that the slide forgot to update when it switched to the new data/coefficients (0.361), while the verbal conclusion was updated correctly. This wiki page notes the inconsistency rather than silently correcting the source, and **uses $\beta_1=0.361$ (matching the actual regression table) to recompute the "exact" calculation above with the correct method**, instead of repeating the erroneous 0.297 figure.

### Log-lin (semi-log, semi-elasticity)

**When to use it**: when $X$ is still measured in its natural units (years of schooling, age, a dummy variable...) but $Y$ responds in **percentage** terms — this is the most common functional form in wage studies (the original Mincer wage equation is exactly log-lin in `schooling`), because "return to education" is traditionally measured in %/year of schooling, not in monetary units/year of schooling.

$$\ln Y=\beta_0+\beta_1X+\varepsilon$$

The coefficient $\beta_1$ here is a **semi-elasticity** — a "half" elasticity: $Y$ is measured in %, while $X$ is still measured in its natural units.

**3.3.a — Continuous variable (e.g. `schooling`)**

- **Approximate**: $X$ increases by 1 unit → $Y$ changes by $\beta_1\times100$ percent.
- **Exact**: $X$ increases by 1 unit → $Y$ changes by $b=(e^{\beta_1}-1)\times100$ percent.

**Numerical example (from the slide, regression on the wage dataset)**:

```
log(wage) ~ age + schooling + tenure + gender + origin + science + social
```

|Variable | Estimate | Std. Error | t value | Pr(>|t|) |
|---|---|---|---|---|
| (Intercept) | 4.060887 | 0.172488 | 23.543 | < 2e-16 *** |
| `age` | 0.001358 | 0.003231 | 0.420 | 0.67441 |
| `schooling` | 0.026674 | 0.010178 | 2.621 | 0.00890 ** |
| `tenure` | −0.009561 | 0.001257 | −7.609 | 6.42e-14 *** |
| `gender` | 0.020419 | 0.032932 | 0.620 | 0.53537 |
| `origin` | −0.102151 | 0.032825 | −3.112 | 0.00191 ** |
| `science` | −0.019312 | 0.052338 | −0.369 | 0.71222 |
| `social` | −0.022739 | 0.048907 | −0.465 | 0.64208 |

Residual SE = 0.505 (df = 990); $R^2$ = 0.07053; $R^2_{adj}$ = 0.06396; F = 10.73 on (7, 990); p = 4.413e-13.

$\beta_{schooling}=0.02667$ (significant at the 1% level):

- **Approximate**: an extra year of schooling → wage increases by approximately $0.02667\times100=$ **2.667%**.
- **Exact**: $b=(e^{0.02667}-1)\times100=2.703\%\approx$ **2.700%** — very close to the approximate figure.

**3.3.b — Dummy variable (e.g. `gender`)**

- **Approximate**: the % difference between group $X=1$ and the base group $X=0$ is $\beta_1\times100$ percent.
- **Exact**: the difference between the two groups is $b=(e^{\beta_1}-1)\times100$ percent.

Example (from the slide, illustrated separately outside the full regression table above): $\beta_{gender}=0.02$ →

- **Approximate**: male wages are about **2.00%** higher than female wages.
- **Exact**: $b=(e^{0.02}-1)\times100=2.02\%$.

(This dummy example from the slide is **internally consistent** — no numerical contradiction like the ones in sections 3.2/3.3.a — and is used here as a clean reference point.)

> **Source note (similar inconsistency to section 3.2, occurring in exactly the `schooling` continuous-regressor example for log-lin)**: the slide writes "$b=(e^{0.297}-1)\times100=0.027$: the result is 2.700 percent" — the exponent $0.297$ here **also does not match** the $\beta_{schooling}=0.02667$ just stated (and matches the actual log-lin regression table above: 0.026674), and it is also missing the ×100 step when displaying the intermediate figure ($0.027$ instead of $2.7$). But the final conclusion "2.700 percent" once again matches exactly if $\beta_1=0.02667$ (not 0.297) is used. The same "0.297" figure appearing repeatedly in both places (log-log and log-lin) further supports the possibility that this is leftover data from an earlier version of the slide/dataset, rather than two independent random errors. Noted here, without silently correcting the source.

### Lin-log

**When to use it**: the reverse case of 3.3 — $Y$ is still measured in its natural units (e.g. thousand VND/hour), but $X$ responds in percentage terms. Less common than log-lin in wage studies, but useful when $X$ spans a very wide range of values (differing orders of magnitude) while $Y$ does not — taking the log of $X$ helps "compress" that range.

$$Y=\beta_0+\beta_1\ln X+\varepsilon$$

- **Approximate**: $X$ increases by 1% → $Y$ changes by $\beta_1\div100$ units.
- **Exact**: $X$ increases by 1% → $Y$ changes by $b=\beta_1\times\ln(1.01)$ units.

**Numerical example (from the slide, regression on the wage dataset)**:

```
wage ~ log(age) + log(schooling) + log(tenure) + gender + origin + science + social
```

|Variable | Estimate | Std. Error | t value | Pr(>|t|) |
|---|---|---|---|---|
| (Intercept) | 29.9728 | 37.0611 | 0.809 | 0.41886 |
| `log(age)` | 2.1460 | 6.0849 | 0.353 | 0.72441 |
| `log(schooling)` | 30.9070 | 11.8295 | 2.613 | 0.00912 ** |
| `log(tenure)` | −12.1797 | 1.9820 | −6.145 | 1.16e-09 *** |
| `gender` | 0.4929 | 2.6653 | 0.185 | 0.85333 |
| `origin` | −7.5937 | 2.6566 | −2.858 | 0.00435 ** |
| `science` | −3.0487 | 4.2336 | −0.720 | 0.47162 |
| `social` | −4.1834 | 3.9561 | −1.057 | 0.29057 |

Residual SE = 40.86 (df = 990); $R^2$ = 0.05185; $R^2_{adj}$ = 0.04515; F = 7.734 on (7, 990); p = 3.978e-9.

$\beta_{\ln schooling}=30.907$ (significant at the 1% level):

- **Approximate**: a 1% increase in years of schooling → wage increases by approximately $30.907\div100=$ **0.309 thousand VND/hour**.
- **Exact**: $b=30.907\times\ln(1.01)=30.907\times0.009950=$ **0.307 thousand VND/hour**.

This is an **internally consistent** example (no numerical contradiction like sections 3.2/3.3.a) — used as a "clean" reference point for understanding how the correct formula works.

## Summary table — coefficient interpretation cheat sheet

|Functional form |Equation |X increases by |Approximate interpretation of $\beta_1$ |Exact formula |
|---|---|---|---|---|
| **Linear** | $Y=\beta_0+\beta_1X+\varepsilon$ |1 unit |$Y$ changes by $\beta_1$ **units** |(already exact, no separate formula needed) |
| **Log-log** | $\ln Y=\beta_0+\beta_1\ln X+\varepsilon$ | 1% |$Y$ changes by $\beta_1$ **percent** (= elasticity) | $b=(1.01^{\beta_1}-1)\times100$ |
| **Log-lin** | $\ln Y=\beta_0+\beta_1X+\varepsilon$ |1 unit |$Y$ changes by $\beta_1\times100$ **percent** | $b=(e^{\beta_1}-1)\times100$ |
| **Lin-log** | $Y=\beta_0+\beta_1\ln X+\varepsilon$ | 1% |$Y$ changes by $\beta_1\div100$ **units** | $b=\beta_1\times\ln(1.01)$ |

**Quick mnemonic** (a memory aid, not quoted from the slide): look at **where "log" sits** in the name — whether "log" appears before $Y$ or $X$ (or both) determines the unit of measurement of the **change**, not of the **variable**:
- - `log` present on $X$ (log-log, lin-log) → refers to $X$ **increasing by 1%**.
- - No `log` on $X$ (linear, log-lin) → refers to $X$ **increasing by 1 unit**.
- - `log` present on $Y$ (log-log, log-lin) → $Y$ **changes in percentage terms**.
- - No `log` on $Y$ (linear, lin-log) → $Y$ **changes in its original unit of measurement**.

> **General rule on approximate vs. exact**: the two calculation methods are **close when $\beta_1$ is small** (loosely: $|\beta_1|<0.1$ usually gives a negligible difference); when $\beta_1$ is large, the two methods can diverge substantially — this is a classic exam trap (using the approximate formula when the question asks for the "exact effect," or vice versa). The four numerical examples in section 3 above all have relatively small $\beta_1$, so the approximate and exact values are always close — **do not conclude from this that the two methods always give close results**; with a large $\beta_1$ (e.g. above 0.5), the discrepancy can become substantial.

## Deriving the "exact" formula — step by step (self-study in the slide)

This part is marked by the slide as self-study — proving why the "exact" formula in sections 3 and 4 is correct, rather than just memorizing it mechanically.

### Log-log → the exact elasticity formula

Start from $\ln y=\beta_0+\beta_1\ln X$. When $X$ increases by 1% (i.e. the new $X$ is $1.01X$), the function value becomes:

$$\ln y' = \beta_0+\beta_1\ln(1.01X)$$

Take the difference between the two equations to isolate the change:

$$\ln y' - \ln y = \beta_1\ln(1.01X)-\beta_1\ln X = \beta_1\ln(1.01)$$

(since $\ln(1.01X)-\ln X=\ln\!\left(\frac{1.01X}{X}\right)=\ln(1.01)$, by the properties of logarithms). So $\ln\!\left(\frac{y'}{y}\right)=\beta_1\ln(1.01)$. Using the identity $e^{a\ln b}=b^a$ (exponentiating both sides with base $e$):

$$\frac{y'}{y}=1.01^{\beta_1}$$

Subtract 1 from both sides then multiply by 100 to convert from a ratio to a percentage:

$$\frac{y'-y}{y}\times100=(1.01^{\beta_1}-1)\times100$$

This is exactly the "exact" formula in sections 3.2/4.

### Log-lin → the exact semi-elasticity formula

Start from $\ln y=\beta_0+\beta_1X$. When $X$ increases by 1 unit:

$$\ln y_0=\beta_0+\beta_1X \qquad \ln y_1=\beta_0+\beta_1(X+1)$$

Taking the difference: $\ln y_1-\ln y_0=\beta_1$. So $\dfrac{y_1}{y_0}=e^{\beta_1}$, and:

$$\frac{y_1-y_0}{y_0}\times100=(e^{\beta_1}-1)\times100$$

This is exactly the "exact" formula in sections 3.3/4.

### Lin-log → the exact formula

Start from $y=\beta_0+\beta_1\ln X$. When $X$ increases by 1%:

$$y_0=\beta_0+\beta_1\ln X \qquad y_1=\beta_0+\beta_1\ln(1.01X)$$

Take the difference directly (no need to take logs again since $y$ is already linear):

$$y_1-y_0=\beta_1\big[\ln(1.01X)-\ln X\big]=\beta_1\ln(1.01)$$

This is exactly the "exact" formula in sections 3.4/4. Since $\ln(1.01)\approx0.01$, the approximate formula $\beta_1/100$ is simply a way of "rounding" $\ln(1.01)$ to $0.01$ — and the slide notes explicitly: **this approximation can deviate substantially from the exact figure if $\beta_1$ is large enough** (verbatim from the slide, section "EXACT EFFECTS FROM LIN-LOG").

## Quadratic functional form

**When to use it**: when theory predicts a **non-monotonic** relationship — rising up to a point then falling (or the reverse: falling then rising), instead of moving steadily in one direction across the entire range of $X$. Classic example: wages rise with age (accumulating experience) but start declining after a certain age.

$$\ln y = \beta_0 + \beta_1 \cdot age + \beta_2 \cdot age^2 + \cdots$$

**Intuition about the sign of $\beta_2$**: $\beta_2<0$ → downward-opening parabola → has a **maximum** point — matching the "rise then fall" story. $\beta_2>0$ → upward-opening parabola → has a **minimum** point — matching the "fall then rise" story (less common in the wage-age example, but common in cost relationships).

**Finding the extremum**: take the partial derivative with respect to `age` and set it to zero:

$$\frac{\partial \ln wage}{\partial age} = \beta_1 + 2\beta_2\cdot age = 0 \;\Rightarrow\; age^* = -\frac{\beta_1}{2\beta_2}$$

**Numerical example (from the slide, regression on the wage dataset)**:

```
log(wage) ~ age + I(age^2) + schooling + tenure + gender + origin + science + social
```

|Variable | Estimate | Std. Error | t value | Pr(>|t|) |
|---|---|---|---|---|
| (Intercept) | 3.9590078 | 0.3024932 | 13.088 | < 2e-16 *** |
| `age` | 0.0103682 | 0.0222095 | 0.467 | 0.64072 |
| `I(age^2)` | −0.0001830 | 0.0004462 | −0.410 | 0.68184 |
| `schooling` | 0.0263959 | 0.0102044 | 2.587 | 0.00983 ** |
| `tenure` | −0.0095798 | 0.0012579 | −7.616 | 6.12e-14 *** |
| `gender` | 0.0197287 | 0.0329885 | 0.598 | 0.54995 |
| `origin` | −0.1022937 | 0.0328411 | −3.115 | 0.00189 ** |
| `science` | −0.0186382 | 0.0523853 | −0.356 | 0.72207 |
| `social` | −0.0223893 | 0.0489354 | −0.458 | 0.64739 |

Residual SE = 0.5052 (df = 989); $R^2$ = 0.07069; $R^2_{adj}$ = 0.06317; F = 9.404 on (8, 989); p = 1.406e-12.

With $\beta_1=0.0103682$ and $\beta_2=-0.0001830$ ($\beta_2<0$ → this is a **maximum** point):

$$age^*=-\frac{0.0103682}{2\times(-0.0001830)}=28.3$$

**Before age 28.3**, $\ln wage$ increases with age; **after age 28.3**, it declines with age (according to this model).

### Testing significance: a t-test is not enough, a joint F-test is needed

Testing $\beta_2$ alone (the question "does the quadratic term contribute additional information beyond the linear term?") uses an ordinary **t-test**. But the broader question — "does the variable `age` (overall, both the linear and quadratic terms) have any effect on wages at all?" — **cannot** be answered using only the t-test of $\beta_1$ or of $\beta_2$ alone, because the two coefficients jointly describe one variable; a **joint F-test** must be used:

$$H_0: \beta_1=\beta_2=0$$

**Actual F-test result from the slide** (`car::linearHypothesis`, comparing the model with and without `age`, `I(age^2)`):

```
Model 1: restricted model (không có age, age^2)
Model 2: log(wage) ~ age + I(age^2) + schooling + tenure + gender + origin + science + social

  Res.Df   RSS Df Sum of Sq      F Pr(>F)
1    991 252.52
2    989 252.44  2  0.087956 0.1723 0.8418
```

F = 0.1723, p = 0.8418 → **fail to reject** $H_0$. In other words: in this exact dataset, **`age` (even allowing for a quadratic relationship) has no statistically significant effect on wages**, despite having computed a "nice-looking" extremum at age 28.3.

> **The most important point in section 6 — easy to miss when reviewing for exams**: computing an extremum $age^*=28.3$ **does not automatically mean that relationship is statistically significant**. The formula $age^*=-\beta_1/2\beta_2$ always produces a number as long as $\beta_2\neq0$ — even when both $\beta_1$ and $\beta_2$ are completely non-significant (as in this very example: $p_{\beta_1}=0.64$, $p_{\beta_2}=0.68$, and the joint F-test $p=0.84$). Before interpreting the extremum in economic terms ("wages peak at age 28.3"), you must check whether the joint F-test is significant — if it is not, the $age^*$ figure is merely a mathematical artefact of this particular sample, not a reliable economic finding.

## Interaction terms

**When to use it**: when the research question is "does the effect of variable A on $Y$ differ across groups/values of variable B?" — i.e. suspecting that the **slope** (not just the intercept) of the A→Y relationship depends on B. The slide's example: whether **return to education** differs between male and female workers.

$$\ln wage = \beta_1\cdot schooling + \beta_2\cdot schooling\times gender$$

Define "return to education" as the partial derivative of $\ln wage$ with respect to `schooling`:

$$\frac{\partial \ln wage}{\partial schooling} = \beta_1+\beta_2\cdot gender$$

- - **Female** workers ($gender=0$): return to education $=\beta_1$.
- - **Male** workers ($gender=1$): return to education $=\beta_1+\beta_2$.
- - **Male − female difference** $=\beta_2$ — exactly the coefficient of the interaction term $schooling\times gender$.

**Interpreting the sign of $\beta_2$**: $\beta_2>0$ → men have a higher return to education than women; $\beta_2<0$ → men have a lower return to education than women; $\beta_2=0$ → no difference between the two genders.

### Real numerical example (from the slide, regression on the wage dataset)

The actual model the slide runs is more complete than the simplified formula above — it adds control variables, and the R syntax `schooling*gender` automatically adds both main effects (`schooling`, `gender`) as well as the interaction term `schooling:gender`:

```
log(wage) ~ age + schooling*gender + tenure + origin + science + social
```

|Variable | Estimate | Std. Error | t value | Pr(>|t|) |
|---|---|---|---|---|
| (Intercept) | 3.730489 | 0.250296 | 14.904 | < 2e-16 *** |
| `age` | 0.001279 | 0.003227 | 0.396 | 0.69192 |
| `schooling` | 0.050169 | 0.016433 | 3.053 | 0.00233 ** |
| `gender` | 0.553769 | 0.294931 | 1.878 | 0.06073 . |
| `tenure` | −0.009512 | 0.001255 | −7.578 | 8.07e-14 *** |
| `origin` | −0.101775 | 0.032788 | −3.104 | 0.00196 ** |
| `science` | −0.018045 | 0.052281 | −0.345 | 0.73005 |
| `social` | −0.023645 | 0.048853 | −0.484 | 0.62849 |
| `schooling:gender` | −0.037944 | 0.020852 | −1.820 | 0.06910 . |

Residual SE = 0.5044 (df = 989); $R^2$ = 0.07363; $R^2_{adj}$ = 0.06614; F = 9.827 on (8, 989); p = 3.298e-13.

**Interpretation**:

- - Return to education for **female** workers ($\beta_1$): $0.050169$ → an extra year of schooling raises female wages by approximately **5.02%**, significant at the 1% level.
- - Return to education for **male** workers ($\beta_1+\beta_2$): $0.050169+(-0.037944)=0.012225$ → an extra year of schooling raises male wages by only approximately **1.22%**.
- - **Male − female difference** ($\beta_2=-0.037944$): the return to education for men is **lower** than for women by about 3.79 percentage points in this sample. This coefficient has $p=0.069$ — **significant at the 10% level, but NOT significant at the 5% level** (the `.` symbol in the R table, not `*`). This is a point to be careful about when reporting: if the assignment/thesis specifies $\alpha=5\%$, the correct conclusion should be "**there is not enough evidence** at the 5% significance level that the return to education differs between men and women," even though the sign and magnitude of $\beta_2$ ("men lower than women by ~3.8 percentage points") is still worth reporting descriptively.

> **Methodological note (not a slide error, but a point to keep in mind when running your own interaction models)**: the simplified formula at the start of section 7 ($\ln wage=\beta_1\cdot schooling+\beta_2\cdot schooling\times gender$) has only two terms, used to quickly illustrate how to take the partial derivative — but the actual R model that produced the table above **includes the full main effects** of both `schooling` and `gender` (because the R syntax `schooling*gender` automatically expands to `schooling + gender + schooling:gender`), plus the other control variables. This is an important general rule in econometrics (not specific to this slide): **when adding an interaction term to a model, both original variables (main effects) must always be kept in the model**, otherwise the interaction term's coefficient will be biased because it ends up absorbing the omitted main effect of the other variable.

## Comparing $R^2$ across functional forms — and why it should not be used to "pick the best form"

Combining the fit of the six models run on the same dataset in sections 3, 6, and 7 (figures taken directly from the slide, not a new compilation):

|Functional form | $Y$ | $R^2$ | $R^2_{adj}$ | F | df | p-value |
|---|---|---|---|---|---|---|
| Linear | `wage` | 0.05744 | 0.05077 | 8.618 | (7, 990) | 2.731e-10 |
| Log-log | `log(wage)` | 0.06106 | 0.05442 | 9.197 | (7, 990) | 4.704e-11 |
| Log-lin | `log(wage)` | 0.07053 | 0.06396 | 10.730 | (7, 990) | 4.413e-13 |
| Lin-log | `wage` | 0.05185 | 0.04515 | 7.734 | (7, 990) | 3.978e-9 |
| Quadratic | `log(wage)` | 0.07069 | 0.06317 | 9.404 | (8, 989) | 1.406e-12 |
| Interaction | `log(wage)` | 0.07363 | 0.06614 | 9.827 | (8, 989) | 3.298e-13 |

> **Important note (general econometrics knowledge, not content this specific slide deck directly teaches)**: the slide does **not** present this comparison table as a procedure for "picking the best functional form using $R^2$" — the table above is simply this wiki page's compilation of figures already scattered throughout the slide, for ease of review. Technically, this table **should not** be used to conclude that "log-lin or interaction is the best form" by directly comparing $R^2$: the models with dependent variable `wage` (linear, lin-log) and the models with dependent variable `log(wage)` (log-log, log-lin, quadratic, interaction) compute $TSS$ (and hence $R^2=1-RSS/TSS$) on **two different scales** — $R^2$ across these two groups **cannot be compared directly**. Choosing a functional form must be based on **economic theory** (which relationship form is economically sensible) and **appropriate statistical tests** (t-test/F-test for each coefficient, specification tests where applicable), not simply looking at which one has a higher $R^2$.

## Comprehensive exam traps

1. **Confusing the approximate formula with the exact formula across functional forms** — especially when the question explicitly asks for "exact effect"/"instantaneous elasticity" but the approximate formula is used, or vice versa. The discrepancy grows as $|\beta_1|$ grows (see section 4).
2. **Confusing the interpretation direction of log-lin with log-log**: log-lin → coefficient $\times100$ = %Δ$y$ when $X$ changes by **1 unit**; log-log → coefficient (no further multiplication) = %Δ$y$ when $X$ changes by **1%**. Mixing up these two directions is the most common error in this section.
3. **Forgetting to multiply by 100 when converting from a proportion to a percent** — both in the exact formula ($e^{\beta_1}-1$ or $1.01^{\beta_1}-1$ both yield a proportion, which must be multiplied by 100 to get %) and when reading R output (the regression coefficient of $\ln y$ on $X$ is already a small proportion, e.g. $0.02667$, not already in percentage form as $2.667$).
4. **For quadratic forms, using only a t-test for $\beta_2$ while forgetting that the question "does variable $X$ have any effect at all" (not just "is the quadratic term needed") requires a joint F-test of both $\beta_1$ and $\beta_2$** — see section 6.1.
5. **Interpreting the extremum of a quadratic as a certain economic finding, even when the joint F-test is not statistically significant** — the formula $age^*=-\beta_1/2\beta_2$ always produces a mathematical number, which does not automatically guarantee that relationship is statistically significant (see the real example in section 6: $age^*=28.3$ but the F-test $p=0.84$).
6. **Adding an interaction term to a model while omitting one or both main effects** — this biases the interaction coefficient, because it ends up "absorbing" the omitted main effect (see section 7.1).
7. **Interpreting an interaction term coefficient that is significant at one $\alpha$ level as a firm conclusion at a stricter $\alpha$ level** — for example $\beta_2$ (interaction schooling×gender) has $p=0.069$: correct at the 10% level but **incorrect** if reported as "statistically significant" when the question specifies $\alpha=5\%$.
8. **Comparing $R^2$ between models with dependent variables on different scales** (e.g. `wage` versus `log(wage)`) to conclude "which form is better" — technically invalid because $TSS$ is computed on two different scales (see section 8).
9. **Choosing the wrong functional form and then interpreting the coefficient using the "default formula" of a different form** — e.g. running log-lin (`log(y) ~ X`) but interpreting the coefficient the lin-log way (dividing by 100 instead of multiplying by 100), a common error when working quickly without carefully checking which side has `log`.

## Connections to the rest of the course

This page is a direct extension of assumption **A1 (Linearity — linear in parameters)** in [[concepts/linear-regression-model]] — everything covered here (log-log, log-lin, lin-log, quadratic, interaction) is not a different class of model, but still ordinary OLS, differing only in the variable-transformation step before running the regression. Therefore every assumption A2–A5, and every inference tool (t-test, F-test, VCV/SE) already covered in [[concepts/linear-regression-model]] applies unchanged to the models on this page — only the **way the coefficients are interpreted** changes with the functional form.

Two noteworthy connections to later topics in the course:

- - **Interaction terms increase the risk of multicollinearity** between the interaction term and the original variables that compose it (e.g. `schooling` and `schooling:gender` are often fairly highly correlated) — this is why interaction terms tend to have larger-than-expected standard errors, directly related to the topic covered in [[concepts/linear-regression-model]] section A2, and discussed further in the multicollinearity part of the course.
- - **Choosing the wrong functional form** (e.g. using linear when the true relationship is log-log) is a form of **model misspecification** — it does not directly violate A1 (the model remains linear in $\beta$ regardless of which form is chosen), but it can cause the estimated coefficients to lose their correct economic meaning even though the model still "runs" fine statistically. This is why the course always emphasizes: the choice of functional form must come from **economic theory** about the underlying nature of the relationship between variables, not from picking whichever form gives the highest $R^2$ (see section 8) or whichever form "produces a nice-looking p-value."

## Real-world application references

Three recent papers illustrating how functional forms (log-log, log-lin, quadratic, interaction) are used in real-world economic research (Lecture 2 syllabus):

- Yang, F., & Zhan, J. (2025). Economic impact of cooperative management behavior on citrus production performance. *Finance Research Letters*, 107042. https://doi.org/10.1016/j.frl.2025.107042
- Xia, H., Li, C., Zhou, D., Zhang, Y., & Xu, J. (2020). Peasant households' land use decision-making analysis using social network analysis: A case of Tantou Village, China. *Journal of Rural Studies*, 80, 452-468. https://doi.org/10.1016/j.jrurstud.2020.07.004
- Gonzales, J. T. (2023). Implications of AI innovation on economic growth: A panel data study. *Journal of Economic Structures*, 12(1), 13. https://doi.org/10.1186/s40008-023-00307-w
