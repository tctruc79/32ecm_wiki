---
title: "Endogeneity and Instrumental Variable (IV) Regression"
type: concept
status: mature
tags: [endogeneity, instrumental-variables, 2sls, gmm, liml, hausman-test]
sources: ["[[sources/slides-5-endogeneity-iv-regression]]", "[[sources/slides-16-endogeneity-iv-regression-extended]]"]
related: ["[[concepts/linear-regression-model]]", "[[concepts/econometrics-overview]]", "[[people/hausman]]"]
updated: 2026-08-29
---

> **How to read this page**: this page resolves the violation of assumption **A3 (exogeneity)** of [[concepts/linear-regression-model]] — arguably the single most important topic in the course, because it goes straight at the question "when does a regression coefficient actually measure a causal relationship?" The page merges `slides-5-iu.pdf` (original version, 63 slides) and `slides-16-iu.pdf` (extended version, 70 slides, used as the canonical structure). Main difference between the two versions: slides-16 corrects the terminology "biased" → "inconsistent" for greater precision, and adds an entirely new section — **robust inference under weak instruments** (Anderson-Rubin, Stock-Wright) — absent from slides-5. Specific numerical discrepancies between the two versions are noted exactly where they occur in the text, never silently reconciled.

## What is endogeneity? — intuition before formulas

### Illustrative story: education, ability, and wages

Suppose you want to answer the classic labor-economics question: "how much does wage increase for one extra year of schooling?" You regress $\ln(wage)$ on `schooling` (number of years of education) and a few other control variables. OLS produces a positive, statistically significant coefficient. Is that conclusion sound?

The problem: people with more innate ability tend **both** to pursue more schooling (learning comes easier, they're encouraged to continue) **and** to earn higher wages (they work more productively, independent of credentials). But `ability` is almost never measured directly in survey data — it sits in the **unobserved** part, i.e. inside the model's error term $e$. Because `ability` is correlated with `schooling` and is also part of $e$, `schooling` ends up correlated with $e$. Consequence: the OLS coefficient on `schooling` no longer measures only "the effect of schooling on wages" — it also "mixes in" part of the effect of innate ability (since higher ability comes bundled with more schooling). We can no longer separate the true effect of education from the effect of ability "riding along" with education.

This is the essence of **endogeneity**: the explanatory variable is no longer "clean" — it carries information correlated with exactly the part the model assigns to the random error.

### Formal definition

Structural equation / data generating process (DGP):

$$y=X\beta+e$$

OLS estimates $\hat\beta_{OLS}=(X'X)^{-1}X'y$, which implies $X'X\hat\beta_{OLS}=X'y=X'(X\beta+e)=X'X\beta+X'e$, i.e.:

$$X'X\hat\beta_{OLS} = X'X\beta + X'e$$

OLS **assumes** $X'e=0$ — this is exactly assumption A3 (exogeneity) of [[concepts/linear-regression-model]]: the error carries no systematic information related to $X$.

$$\textbf{Endogeneity occurs when } X'e\neq0$$

— any regressor correlated with the error. Direct consequence of the identity above:

- If $X'e=0$ → $\hat\beta_{OLS}=\beta$.
- If $X'e\neq0$ → $\hat\beta_{OLS}\neq\beta$.

**Precise terminology — the point slides-16 corrects from slides-5**: when $X'e\neq0$, the precise way to describe it is that $\hat\beta_{OLS}$ becomes an **inconsistent** estimator — i.e. no matter how much more data you have, the estimate still does *not* converge to the true value $\beta$. Slides-5 in places calls this "biased"; slides-16 consistently corrects it to "inconsistent." The two concepts differ in nature: bias is a finite-sample discrepancy (which can vanish as $N\to\infty$ under some other violations); under endogeneity, the problem **does not vanish** no matter how large the sample grows — which is why "inconsistent" is the term that correctly describes the nature of the problem.

### Consequences for causal interpretation

With $y=X\beta+e$:

- If $e$ is **not** correlated with $X$: the causal effect is exactly $\dfrac{\partial y}{\partial X}=\beta$ — the regression coefficient measures precisely what we want.
- If $e$ **is** correlated with $X$: because $e$ also changes with $X$, the full effect becomes $\dfrac{\partial y}{\partial X}=\beta+\dfrac{\partial e}{\partial X}$ — meaning $\beta$ **no longer isolates** the true effect of $X$ on $y$; it is mixed with a part coming from $e$.

In other words: a high $R^2$ or a strongly significant t-statistic cannot rescue a coefficient corrupted by endogeneity. This is exactly why section 9 of [[concepts/linear-regression-model]] stresses that "a high $R^2$ is not the goal of econometrics" — the goal is to correctly estimate $\beta$, and endogeneity is the direct enemy of that goal.

## Three sources of endogeneity — one concrete example per type

### Omission of important regressors

Suppose the true DGP is $y=\beta_0+\beta_1x_1+\beta_2x_2+e$, but we omit $x_2$ (no data available, or it simply wasn't considered), and only run:

$$y=\beta_0+\beta_1x_1+\mu, \qquad \mu=\beta_2x_2+e$$

Then $E(\mu x_1)\neq0$ **if** $Cov(x_1,x_2)\neq0$ — the new error $\mu$ "contains" the omitted $x_2$, and if $x_2$ is correlated with $x_1$ which remains in the model, then $\mu$ is also correlated with $x_1$ → endogeneity.

**Slide example**: ice cream sales and drowning accidents are strongly positively correlated in seasonal data — but ice cream does not "cause" drowning. The omitted variable is **summer temperature**: hot weather both makes people buy more ice cream and makes people swim more (and hence increases drowning risk). Omitting temperature from the model causes the ice-cream variable to "absorb" part of temperature's influence.

**This is exactly the education–wage case from section 1.1**: the true DGP includes `ability`, we omit it, `ability` is correlated with `schooling` → `schooling` becomes an endogenous variable.

### Reverse causality / simultaneity

Suppose we want to regress $y=\beta X+e$, but in reality $y$ also feeds back and affects $X$ — a feedback equation:

$$X=\gamma y+v$$

Substituting $y=\beta X+e$ into the feedback equation:

$$X=\gamma(\beta X+e)+v \;\;\Rightarrow\;\; X=\frac{\gamma e}{1-\gamma\beta}+\frac{v}{1-\gamma\beta}$$

$X$ is now a function of $e$ itself → $X$ is correlated with $e$ → endogeneity.

**Slide example**: police and crime. More police officers can reduce crime (the "forward" causal direction we want to measure) — but at the same time, areas with high crime are also typically assigned more police (the "reverse" direction — authorities respond to crime conditions). A simple regression of `crime` on `number of police` mixes both directions of effect, so the estimated coefficient no longer measures the true "net effect of police on crime."

### Measurement error

Consider the regression $y=\beta x+e$, but we do not observe the true $x$, only a noisy version of it:

$$x^*=x+v \quad (v = \text{measurement error})$$

The equation we actually run becomes $y=\beta x^*+e=\beta(x+v)+e$, i.e.:

$$y=\beta x+\omega, \qquad \omega=\beta v+e$$

Both the new error $\omega$ **and** the explanatory variable $x$ contain $v$ → they are correlated with each other → endogeneity. (This is "classical measurement error in the independent variable" — different from measurement error in the dependent variable $y$, which typically does not cause endogeneity, only inflates the error variance.)

## Running example: the wage equation in HCMC

$$\ln wage = f(schooling, X) + e$$

`schooling` is suspected to be endogenous through exactly the mechanism of section 2.1: **ability** (unobserved) both affects the decision to pursue further education and directly affects labor productivity and hence wages → `ability` sits inside $e$ → `schooling` is correlated with $e$.

**Data**: a survey of workers in Ho Chi Minh City.


| Variable | Meaning | Role |
|---|---|---|
| `wage` | Wage ($/hour) | Dependent variable |
| `age` | Age (years) | Control |
| `schooling` | Number of years of education | **Suspected endogenous variable** |
| `tenure` | Number of months at the current job | Control |
| `gender` | 1 = male, 0 = female | Control |
| `origin` | 1 = migrant, 0 = HCMC native | Control |
| `science` | 1 = science track (base = technology) | Control |
| `social` | 1 = social-science track (base = technology) | Control |
| `fatheredu` | Father's number of years of education | **Instrument** |
| `motheredu` | Mother's number of years of education | **Instrument** |


> **Small source note**: `slides-5-iu.pdf` describes both `fatheredu` **and** `motheredu` as "schooling years of the **father**" — clearly a copy-paste error (the `motheredu` variable cannot be the father's education). `slides-16-iu.pdf` correctly fixes it to "schooling years of the **mother**." Nothing further needs to be done here — just noting this as a concrete example of slides-16 refining slides-5, consistent with what the ingest log already records.

Running OLS directly of $\ln wage$ on `schooling` and the controls produces a coefficient — but the slide immediately stresses: **"This OLS estimate is biased if schooling is endogenous."** This is exactly the motivation for moving to instrumental variable regression.

## Instrumental Variables — what does a "good instrument" need?

### Intuition: two conditions

Consider the model:

$$y=\alpha+\beta_1X_1+\beta_2X_2+e$$

with $X_2$ the suspected endogenous variable ($E(X_2'e)\neq0$). The idea of IV is to find an "auxiliary" variable $Z$ (called $IV$/$W$ in the slide's notation) that acts as a "clean source of variation" for $X_2$ — whatever variation in $X_2$ comes from $Z$ is kept for estimation, whatever comes from the "dirty" part (correlated with $e$) is discarded.

To do this, $Z$ must satisfy **both** conditions simultaneously — missing either one makes the instrument "broken":

1. **Relevance**: $Z$ must actually be correlated with $X_2$. Intuition: if $Z$ is nearly unrelated to $X_2$, using it to "substitute" for $X_2$'s variation is no different from using random noise — it doesn't help (see section 6.1 for the consequences of weak instruments).
2. **Exogeneity / Exclusion**: $Z$ must not be correlated with $e$, and more importantly — intuitively — $Z$ is only allowed to affect $y$ **through** $X_2$, with no other direct path onto $y$.

The slide further clarifies the relationship between "exogeneity" and "exclusion": mathematically, exogeneity ($Z$ uncorrelated with $e$) already implies exclusion. The slide separates out "exclusion" for emphasis because, in research practice, the easiest thing to violate is an unanticipated **direct path** from the instrument to $y$ — separating it out prompts the reader to ask specifically: "does $Z$ have any other channel onto $y$, besides the one through $X_2$?"

**Applied to the wage example**: `fatheredu` and `motheredu` are proposed as instruments for `schooling`.

- **Relevance**: parents' education is typically strongly correlated with their child's education (family conditions, expectations, resources invested in education) — directly testable via the first-stage F (see section 6.1).
- **Exclusion**: assumes parents' education affects the child's wage **only** through how many years the child studies — no other direct path (highly educated parents don't directly "pay" their child's wage), and no correlation with other unobserved factors in the wage function (such as ability, social networks...). This is an **assumption**, not a condition directly testable with data (see section 6.2).

### The identification problem: $h$ versus $k$

Let $k$ = number of endogenous variables, $h$ = number of instruments (excluded instruments):


| Comparison | Name | Intuitive meaning |
|---|---|---|
| $h<k$ | **Unidentified** (not allowed) | Not enough "clean sources of variation" to separate out all endogenous variables — the problem is unsolvable |
| $h=k$ | **Just-identified / exactly-identified** | Exactly enough instruments for each endogenous variable — a unique solution, but **cannot be tested** for whether the instruments are actually valid (see section 6.2) |
| $h>k$ | **Over-identified** | More instruments than strictly needed — this "surplus" enables **testing overidentifying restrictions** |


In the wage example: 1 endogenous variable (`schooling`, $k=1$), 2 instruments (`fatheredu`, `motheredu`, $h=2$) → **over-identified** ($h>k$) → overidentifying restrictions can be tested via Sargan/Hansen J.

## 2-Stage Least Squares (2SLS)

### The manual 2-step procedure — and why its SE cannot be trusted

Before the packaged 2SLS formula existed, the original idea was very intuitive — done manually in 2 steps:

- **Stage 1**: regress the endogenous variable $X_2$ on $X_1$ (the exogenous variables already in the model, called **included instruments**) and $IV$ (the instrument, called **excluded instruments**):
then compute the fitted values: $\hat X_2=\hat\gamma_0+\hat\gamma_1X_1+\hat\gamma_2 IV$. This stage is also exactly where we **test relevance** — whether the coefficient $\gamma_2$ on $IV$ is different from 0 (see section 6.1).
- **Stage 2**: regress $y$ on $X_1$ and $\hat X_2$ (instead of the true $X_2$):
Because $\hat X_2$ is only the part of $X_2$'s variation "explained" by $X_1$ and $IV$ — with $IV$ satisfying exogeneity — $\hat X_2$ is **no longer correlated with $e$**, which resolves the endogeneity problem.

> **Important warning**: if done manually as two separate OLS steps as above, **the standard error at stage 2 is computed incorrectly (inconsistent)** — because stage 2 "forgets" that $\hat X_2$ is only an estimate (carrying its own uncertainty from stage 1), not a true observed value. This is exactly why a packaged **2SLS estimator** (section 5.2) is needed instead of manually running two consecutive OLS regressions.

### 2SLS estimator in closed form

Let $Z=[X_1,\ IV]$ — the full instrument set. The 2SLS estimator formula:

$$b_{2SLS} = \big[(X'Z)(Z'Z)^{-1}(Z'X)\big]^{-1}(X'Z)(Z'Z)^{-1}Z'y$$

**A special case worth remembering**: if $Z=X$ (no excluded instruments, no endogenous variables) — 2SLS **collapses exactly to OLS**:

$$b_{2SLS}=(X'X)^{-1}X'y = b_{OLS}$$

This shows 2SLS is not a tool "entirely different" from OLS — it is OLS generalized to handle the case with endogenous variables; when there are no endogenous variables, the two formulas coincide.

### Projection interpretation — why 2SLS is exactly "OLS with $X_2$ cleaned up"

Slides-16 presents an additional equivalent formulation that bridges the intuition of the 2-step procedure (section 5.1) with the closed-form formula (section 5.2). Let $\hat X = Z(Z'Z)^{-1}Z'X = P_Z X$ (the projection of $X$ onto the space spanned by $Z$):

$$b_{2SLS}=(\hat X'X)^{-1}\hat X'y$$

Substituting $y=X\beta+e$:

$$b_{2SLS} = \beta + (\hat X'X)^{-1}\hat X'e$$

From this, two conditions needed for 2SLS to be "viable" become clear:

- **$b_{2SLS}$ is only defined** if $\hat X'X\neq0$ (equivalent to $Z'X\neq0$) — this is exactly the **relevance** condition.
- **$b_{2SLS}$ is only consistent** if $\hat X'e=0$ (equivalent to $Z'e=0$) — this is exactly the **exogeneity** condition.

Because $X=[X_1,X_2]$ and $Z=[X_1,IV]$, the projection $P_Z$ splits into $P_ZX=[P_ZX_1,\ P_ZX_2]$. Since $X_1$ is already inside $Z$, projecting $X_1$ onto a space that already contains it leaves it **unchanged**: $P_ZX_1=X_1$. Only $P_ZX_2=\hat X_2$ changes. In other words: **2SLS is precisely "keep $X_1$ as is, replace $X_2$ with the predicted value $\hat X_2$ from stage 1"** — exactly matching the intuition of the 2-step procedure in section 5.1, except the closed-form formula computes the SE correctly from the start.

## Three groups of diagnostic tests after IV regression

After running 2SLS, there are three diagnostic questions to answer, in strict logical order — each question is only meaningful **after** the previous question has been answered "pass":

1. **Is the instrument related to the endogenous variable at all, and is it related strongly enough?** (weak instruments)
2. **If there is more than 1 instrument for 1 endogenous variable — are the "surplus" instruments consistent with each other?** (overidentifying restrictions — applies only when $h>k$)
3. **Is the suspected variable actually endogenous?** (endogeneity — Wu-Hausman)

### Testing for weak instruments

**Why are weak instruments a problem — intuition before formulas**: recall section 5.3 — 2SLS replaces $X_2$ with $\hat X_2$, the predicted value from stage 1. If the instrument is nearly uncorrelated with $X_2$ (weak), then $\hat X_2$ carries **almost no real information** about $X_2$ — it behaves more like a random noise variable than a "clean" version of $X_2$. In that case, at stage 2, we are regressing $y$ on a nearly-noise variable → the estimate becomes **extremely sensitive to random sampling variation** (very large variance), and worse, this "projection noise" can push the 2SLS estimate systematically away from the true value — to the point that **2SLS bias under weak instruments can be even worse than the OLS bias from the endogeneity we were trying to fix** ("the cure can be worse than the disease" — the slide's own phrasing). This is why the slide stresses: weak instruments are **not merely an efficiency problem** — they can completely defeat the original purpose of using IV.

Slides-16 organizes the testing of instrument "strength" into three tiers of questions, from weakest to strongest:

1. **Is there any relevance at all?** (Kleibergen-Paap rk LM test — test for underidentification)
2. **Is the relevance strong enough?** (F-statistic / Cragg-Donald F / Kleibergen-Paap rk F, compared against Stock-Yogo critical values)
3. **If still unsure it's strong enough, is there a reliable way to do inference regardless?** (Anderson-Rubin, Stock-Wright)

**Tier 1 — Test for underidentification (relevance test)**:

$H_0$: the instrument is not relevant — more precisely, $E(Z'X_2)=0$ (single endogenous variable case); with multiple endogenous variables, $H_0: \text{rank}(Z'X_2)<k_2$. Interpretation: the instruments' coefficients in stage 1 are jointly zero.

- Rejecting $H_0$ → initial evidence the instrument **is relevant** (but **says nothing yet about whether it is strong enough**).
- Failing to reject $H_0$ → the model is **unidentified**, a different instrument is needed — every subsequent diagnostic test is **untrustworthy** in this case.

Numerical example (a simple example used in slides-5, a joint F-test on the instrument coefficients at stage 1): F-statistic (excluded instruments) $=10.07$, very small p-value → reject $H_0$ → evidence the instruments are jointly relevant. Slides-16 replaces this with a more general/standard tool — the **Kleibergen-Paap (KP) rk LM test**, which has the advantage of being **robust to heteroskedasticity** (whereas Cragg-Donald LM is not).

**Tier 2 — Test for weak instruments (strength test, graduate level)**:

Rejecting underidentification **does not guarantee** the instrument is strong enough — these are two different tests. One needs to compare:

- **[[people/cragg-donald|Cragg-Donald]] (CD) F-statistic** — assumes homoskedasticity. In the case of 1 endogenous variable + homoskedasticity, the CD F numerically coincides with the F-statistic of the excluded instruments at stage 1.
- **Kleibergen-Paap (KP) rk Wald F** — robust to heteroskedasticity, but **cannot be directly compared** to the Stock-Yogo table (the SY table is built under the homoskedasticity assumption); in practice, people still compare KP-F to SY or to the rule-of-thumb threshold of 10 "informally."

**Common rule of thumb**: CD F-statistic $>10$. But for greater reliability, one should compute the correct statistic and compare it against **[[people/stock-yogo|Stock-Yogo]] (SY) critical values** — there are two different criteria for looking up the table, yielding two different thresholds:

- **Relative bias** ($b$): bounds $\text{bias}(\hat\beta_{2SLS}) \le b\times\text{bias}(\hat\beta_{OLS})$ — intuitive, independent of $\alpha$; but "$10\%$ of a huge bias" can still be large in absolute terms. Approximation: relative bias $\approx 1/\text{F-statistic}$ — this is exactly the origin of the "F>10" rule ($1/10=10\%$).
- **Size distortion** ($r$): ensures the actual test size does not exceed $r$ even when a nominal $\alpha=5\%$ is chosen — directly protects hypothesis testing, with a higher (more conservative) threshold.

Numerical example (1 endogenous variable, $K_2=2$ instruments, observed F-statistic $=10.07$):

- **Relative bias $b=0.1$**: SY critical value $<9.08$ (the table has no column for $K_2=2$, but it must be lower than the $K_2=3$ threshold of $9.08$) → $10.07>$ threshold → **reject weak instruments** — the instrument is strong enough to ensure 2SLS bias does not exceed 10% of OLS bias.
- **Size distortion**: this is where **the two slide versions use different values of $r$ for the same example**, producing two different thresholds — see the note box right below.

> **Source discrepancy note**: with the **same** F-statistic $=10.07$, the same 1 endogenous variable + 2 instruments, the two slide versions choose **different values of $r$** to illustrate the size distortion criterion:
> `slides-5-iu.pdf`: $r=15\%$ → SY critical value $=11.59$. Since $10.07<11.59$ → weak instruments **cannot be rejected** at $r=15\%$ (the instrument is "weak" by this criterion).
> `slides-16-iu.pdf`: $r=10\%$ → SY critical value $=19.93$. Since $10.07<19.93$ → weak instruments **cannot be rejected** at $r=10\%$ (same conclusion, but a completely different numerical threshold).
>Both versions agree on one further point: at $r=20\%$, the SY threshold $=8.75$, so $F=10.07>8.75$ → **not weak** at the $r=20\%$ level. This is not really an "error" — just two illustrative examples using different input values of $r$ — but it can easily confuse a student who directly compares the $11.59$ and $19.93$ thresholds without noticing that $r$ changed between the two versions. Noted here rather than picking one number and discarding the other.

**Bias or size — which criterion to choose?**


| Criterion | Protects | Characteristics | When to prefer |
|---|---|---|---|
| Relative bias $b$ | Point estimate (the estimated coefficient value) | Intuitive, independent of $\alpha$; but less conservative — "10% of a huge bias" can still be large | When prioritizing accuracy of the estimated **number** |
| Size distortion $r$ | Hypothesis testing (whether the t-test/p-value can be trusted) | Directly protects hypothesis testing, higher (more conservative) threshold | When prioritizing reliable **statistical inference** (hypothesis testing) |


An important point slides-16 adds: "**a good estimate does not guarantee a good test, and a good test does not guarantee a good estimate**" — meeting the relative bias criterion only controls the deviation of the estimated number, it does not guarantee the t-test/p-value is trustworthy; meeting the size distortion criterion is the reverse. In practice, instruments often fall into a **borderline** zone — not weak enough to discard entirely, not strong enough to fully trust standard inference (the ordinary t-test) — which is exactly the motivation for the next section.

**Tier 3 — Robust inference under weak instruments (only in the extended slides-16 version)**:

When the instrument is in the borderline zone, instead of continuing to trust the standard t-test (which fails when the instrument is weak), use tests that **remain valid even when the instrument is weak** (as long as it is not underidentified and the instrument is truly exogenous):

- **Anderson-Rubin (AR) test**: under $H_0:\beta_2=\beta_0$, compute the residual $u(\beta_0)=y-X_1\beta_1-X_2\beta_0$. If $H_0$ is true, $u(\beta_0)$ behaves exactly like the true error, i.e. $Z'u(\beta_0)\approx0$. AR regresses $u(\beta_0)$ on $Z$ — if $Z$ still explains this residual significantly, reject $H_0$ (there is an AR-F version jointly testing the significance of the excluded instruments, and an AR chi-square Wald-type version).
- **Stock-Wright (SW) LM test**: based on the moment condition $Z'u(\beta_0)$, rejects $H_0$ if this value deviates significantly from 0.

Example (testing the coefficient of `schooling` $=0$): all AR/SW variants give p-value $<5\%$ → reject $H_0$ → the result **remains valid even though the instrument is weak** (but not underidentified) — as long as the instrument is truly exogenous.

**Important limitation to remember**: AR/SW **can only test** hypotheses about the endogenous variable's coefficient (they do not improve the quality of the point estimate itself — 2SLS can still be unstable/biased when the instrument is weak), and **are only valid if the instrument is truly exogenous** — they do not "rescue" the case of an invalid instrument, only the "weak" problem.

### Testing overidentifying restrictions (only when $h>k$)

The exogeneity condition of the instrument, rewritten in testable form: $E(Z'e)=E\big(Z'(y-X\hat\beta)\big)=0$ — also called the **orthogonality** condition.

- If the model is **just-identified** ($h=k$): $\hat\beta$ is always chosen such that $Z'e=0$ **holds by the structure of the problem** (since the number of equations exactly equals the number of unknowns) → **there is nothing to test** — instrument validity in this case **cannot be tested with data**, it can only be argued through research design.
- If **over-identified** ($h>k$): additional instruments mean additional restrictions on $E(Z'e)=0$ — there are $h-k$ "surplus" restrictions beyond what identification requires, and this surplus is exactly the part that **is testable**.

$H_0$: all instruments are **valid** (valid = satisfies both exogeneity and exclusion — as discussed in section 4.1, mathematically exogeneity implies exclusion, but they are separated out to emphasize the risk of a direct path from IV to $y$).

**[[people/sargan|Sargan]] test** (assumes homoskedasticity):

$$J=nR^2 \text{ (from regressing the IV residual } e \text{ on the full instrument set } Z\text{)}, \qquad J\sim\chi^2_{h-k}$$

Limitation: not robust to heteroskedasticity or autocorrelation.

**[[people/hansen|Hansen's J]] test** (more general, allows heteroskedasticity):

$$J=n\cdot g(\hat\beta)'W^{-1}g(\hat\beta), \qquad g(\hat\beta)=\frac{1}{n}Z'e, \qquad J\sim\chi^2_{h-k}$$

Under homoskedasticity, Sargan and Hansen J **coincide theoretically**.

**Numerical example** (instruments `fatheredu`, `motheredu` for `schooling`, $h=2>k=1$):

- Sargan statistic $=0.36$, p-value $=0.551$ (computed with vcov = "iid") → **fail to reject** $H_0$ → no evidence against the joint validity of the instruments.
- Hansen's J test: p-value $=0.541$ (computed with vcov = "robust") → also **fails to reject** $H_0$, same conclusion.

> **Source note**: although theory says Sargan and Hansen J "coincide" under homoskedasticity, slides-16's numerical example produces two **slightly different** p-values ($0.551$ vs $0.541$) — not a serious contradiction, most likely reflecting that the real data is not perfectly homoskedastic (Sargan uses vcov "iid", Hansen uses vcov "robust", so with data that has a bit of heteroskedasticity, the two numbers are close but not **exactly** identical). Noted here because this is a point where learners easily mistake it for requiring **the exact same number**.

**Most important interpretation — a common exam trap**: failing to reject Sargan/Hansen **does NOT prove** the instruments are valid — it only means "no evidence found against joint validity." Validity must always be **argued through research design**: in this example, one must argue that parents' education has no direct effect on the child's wage, and is not correlated with any other unobserved factor in the wage function — the only path to affect wages is through the child's own `schooling`.

**Additional warning**: the more instruments (proliferation), the higher the chance at least one is invalid. Overidentifying restrictions should only be tested **after** confirming the instrument is not weak — a weak instrument distorts both the size and the power of the Sargan/Hansen test.

### Testing endogeneity: the Wu-Hausman test

**Intuition**: if the suspected variable $X_2$ is actually **not** endogenous, and the instrument is strong enough, then both OLS and 2SLS are consistent estimators — they will **converge asymptotically to the same value**. But if $X_2$ **is truly** endogenous, OLS is biased/inconsistent while 2SLS remains consistent → the two estimates will **diverge systematically**, not merely differ due to random sampling noise. The Wu-Hausman test is precisely a systematic comparison of these two estimates.

$$H_0: X_2 \text{ exogenous} \;(\hat\beta_{OLS}=\hat\beta_{2SLS}, \text{both consistent}), \qquad H_a: X_2 \text{ endogenous}$$

$$\text{Statistic: } (\hat\beta_{2SLS}-\hat\beta_{OLS})'\big[V_{2SLS}-V_{OLS}\big]^{-1}(\hat\beta_{2SLS}-\hat\beta_{OLS}) \sim \chi^2_k$$

with $k$ = number of suspected endogenous variables.

- Large p-value → fail to reject $H_0$ → no evidence of endogeneity → OLS remains consistent (and **more efficient** than 2SLS under homoskedasticity — so OLS should be preferred if there is no evidence of endogeneity).
- Small p-value → reject $H_0$ → $X_2$ is endogenous → OLS is biased, use 2SLS.

**Numerical example — and two source points to note**:

- `slides-5-iu.pdf`: Wu-Hausman statistic $=3.63$. At $\alpha=10\%$: p-value $=0.057<0.1$ → reject $H_0$ → evidence `schooling` is endogenous. At $\alpha=5\%$: the same p-value $=0.057>0.05$ → fail to reject $H_0$ → no evidence of endogeneity.
- `slides-16-iu.pdf`: Wu-Hausman statistic recomputed $=3.8$ (using `ivreg2r::ivreg2()` with robust VCV). At $\alpha=10\%$: p-value $=0.0512<0.1$ → reject $H_0$. At $\alpha=5\%$: p-value $=0.057>0.05$ → fail to reject $H_0$.

Both versions arrive at the same interpretive conclusion: **`schooling` is "endogenous at the 10% level but not at the 5% level"** — a textbook example of how a test's conclusion depends on the pre-chosen significance level $\alpha$, and how the statistic's value depends on the type of VCV used (slides-16 itself notes explicitly: "Wu-Hausman test depends on VCV").

> **Source discrepancy note — important, not previously recorded in earlier versions of this page**: the difference between statistic $3.63$ (slides-5) and $3.8$ (slides-16) is a reasonable "methodological nuance" — due to a different VCV choice, exactly as log.md already records, **not an error**. But within `slides-16-iu.pdf` itself, there is an **internal inconsistency**: the same statistic $3.8$ is reported with **two different p-values** on two adjacent bullet points — $p=0.0512$ when compared against $\alpha=10\%$, but $p=0.057$ when compared against $\alpha=5\%$. Logically, **a single statistic has exactly one p-value** — only the $\alpha$ threshold being compared against should change, the p-value must stay the same. The number $0.057$ matches exactly the p-value from slides-5 (corresponding to statistic $3.63$, not $3.8$) — most likely this is a spot where **slides-16 updated the statistic value but forgot to update the p-value on the second bullet**, leaving it over from the slides-5 version. Noted here per the wiki's own principle, without arbitrarily picking one of the two numbers to "fix" to match.

## Alternative estimators when 2SLS is not good enough (graduate level)

Anderson-Rubin/Stock-Wright (section 6.1) give valid inference under weak instruments, but **do not improve the point estimate itself** — 2SLS can still be unstable/biased. The next question: is there an estimator **better** than 2SLS when instruments are weak or numerous?

### The κ-class estimator and LIML

Both 2SLS and OLS are special cases of a more general family of estimators — the **κ-class estimator**:

$$b(\kappa)=\big[X'(I-\kappa M_Z)X\big]^{-1}X'(I-\kappa M_Z)y, \qquad M_Z=I-Z(Z'Z)^{-1}Z'$$

- $\kappa=0$ → exactly OLS.
- $\kappa=1$ → exactly 2SLS.

**LIML (Limited Information Maximum Likelihood)** chooses $\kappa$ **optimally** via maximum likelihood — specifically the minimum eigenvalue of a ratio matrix $B^{-1}A$, constructed from the residuals after projecting onto $Z$ (for matrix $A$) and after projecting onto $X$ (for matrix $B$).

> **Technical source note**: the exact formulas for matrices $A$, $B$ in the original slide were corrupted during `pdftotext` extraction (some image-embedded matrix notation was lost/garbled in both slide-5 and slide-16) — the core conceptual content (LIML solves an eigenvalue problem to choose the optimal $\kappa$, bridging OLS and 2SLS) remains clear and consistent across both sources, so it is presented in full here; the details of matrices $A,B$ are not reproduced, to avoid inferring beyond what can be read with confidence from the source.

**Intuition**: the "full model" (an estimate ignoring the endogeneity problem) is exactly OLS ($\kappa=0$); the "projected model" (after projecting the regressor onto the instrument) is exactly 2SLS ($\kappa=1$). LIML combines both, choosing the optimal $\kappa$ somewhere in between according to likelihood.

**Why is LIML less sensitive to weak instruments than 2SLS?**

- 2SLS is the κ-class with $\kappa=1$ — it **completely replaces** $X_2$ with $\hat X_2=P_ZX_2$. If the instrument is weak, $\hat X_2$ is a very noisy "proxy" for the true $X_2$, and this projection noise pushes 2SLS away from the true parameter — as analyzed intuitively in section 6.1, "the cure can be worse than the disease."
- LIML chooses $\kappa$ optimally based on the data: with a **strong** instrument, $\kappa\approx1$ → LIML $\approx$ 2SLS. With a **weak** instrument, $\kappa$ drops significantly below 1 → LIML optimally "pulls" the estimate back closer to OLS, reducing weak-IV bias.
- Trade-off: LIML **sacrifices some efficiency** in exchange for robustness against weak instruments.
- **Important note**: LIML is less sensitive to weak-IV bias, but **is not a guarantee of consistency** — if the instrument is truly invalid (not merely weak), LIML cannot rescue it either.

### Fuller-adjusted LIML

Remaining problem: although LIML has less bias than 2SLS under weak instruments, it can still have **large variance and notable small-sample problems**. Fuller (1977) proposes a simple adjustment to reduce bias further while preserving good variance properties.

Instead of using $\kappa$ chosen directly by LIML, Fuller proposes:

$$\kappa_F = \kappa - \frac{a}{n-k} \qquad \text{(formula in } \texttt{slides-5-iu.pdf}\text{)}$$

with $n$ = sample size, $k$ = number of regressors (endo + exo), $a$ = a positive constant, typically chosen as $a=1$ or $a=4$.

> **Source discrepancy note — the Fuller adjustment formula differs between the two versions**: `slides-16-iu.pdf` (the extended/canonical version) gives a formula with a **different denominator**:
> with $l$ = total number of instruments (included + excluded), $k$ still the number of regressors (endo + exo), $a$ still chosen as $1$ or $4$. These are two **algebraically different** formulas (denominator $n-k$ versus $n-l+k-1$), not merely equivalent rewritings — it is unclear whether this is a typo in one of the two versions, or slides-16 deliberately refines the formula to be more general (the $n-l+k-1$ form appears in some reference literature on the Fuller estimator that accounts for the total instrument count). Since slides-16 is the canonical/extended version, its formula is used as the default for computation, but this discrepancy is noted rather than silently picking one version and dropping the other.

**Fuller estimator**: $\hat\beta_F=b(\kappa_F)$.

**Properties** (per the slide, applying to both formulas):


| Property | Remark |
|---|---|
| Bias | Substantially reduced compared to the weak-IV bias of both LIML and 2SLS |
| Variance | Similar to LIML, usually higher than 2SLS |
| Consistency | Consistent if the instrument is valid and relevant |
| Efficiency | Not asymptotically efficient in the absolute sense, but in practice often **outperforms** thanks to better small-sample properties |


Choosing $a$: $a=1$ gives lower variance but slightly higher bias; $a=4$ reduces bias more strongly and is usually considered the safer practical choice. Econometricians typically recommend Fuller specifically in cases where weak IV is a genuine concern.

### GMM (Generalized Method of Moments)

**General framework**: GMM starts from the moment condition $E[m(\theta,d_i)]=0$. Sample moment: $g(\theta)=\frac{1}{n}\sum_i m(\theta,d_i)$. Estimate $\hat\theta=\arg\min_\theta J(\theta)$ with criterion function:

$$J(\theta)=n\cdot g(\theta)'Wg(\theta)$$

$W$ is the weighting matrix: $W=I$ → simple GMM; $W=S^{-1}$ (with $S=E[m(\theta,d_i)m(\theta,d_i)']$) → **efficient GMM**.

**OLS/GLS/2SLS are all special cases of GMM**:

- Ordinary linear regression: $m(\beta,d_i)=y_i-\beta X_i=e_i$ → $J(\beta)=e'We$ is exactly the RSS (residual sum of squares) when $W=I$. $W=I$ → coincides with **OLS**; $W=S^{-1}$ → coincides with **GLS**.
- IV: $m(\theta,d_i)=Z_i(y_i-\beta X_i)=Z_ie_i$ → $g(\beta)=\frac1n\sum Z_ie_i$. $W=(Z'Z)^{-1}$ → coincides with **2SLS**; $W=S^{-1}$ → **efficient IV-GMM**, with $S=E[Z_ie_ie_i'Z_i]=E[e_i^2Z_iZ_i]$, sample estimate $\hat S=\frac1n Z'\,\text{diag}(e^2)\,Z$.

**Role of the error structure**:

- Under **homoskedasticity** ($E(e_i^2|Z_i)=\sigma^2$): $S=\sigma^2Z_iZ_i'$, $\hat S=\sigma^2Z'Z$, $W=S^{-1}=(Z'Z)^{-1}$ → **efficient GMM collapses exactly to 2SLS**.
- Under **heteroskedasticity** ($E(e_i^2|Z_i)=\sigma_i^2$): $\hat S=Z'\Sigma Z$ with $\Sigma=\text{diag}(e^2)$ → **2SLS is no longer efficient**. GMM is more efficient because it assigns **lower weight** to observations with larger error variance (the same GLS principle: trust "noisier" observations less).

**Three GMM variants, differing in how $W$ is chosen/updated**:

1. **Two-step GMM**: Step 1 — choose $W_0=(Z'Z)^{-1}$ (as in 2SLS), estimate $\beta_{2SLS}$, compute $e$ to estimate $S$ and $W=S^{-1}$. Step 2 — re-estimate with the newly computed $W$: $\beta_{GMM,2s}=[X'ZWZ'X]^{-1}X'ZWZ'y$. Under homoskedasticity (or ignoring hetero), $\beta_{GMM,2s}=\beta_{2SLS}$ exactly; under heteroskedasticity, it's more efficient thanks to down-weighting high-variance observations, but the SE at the initial estimation step (if hetero is ignored) is biased.
2. **Iterative GMM**: instead of stopping after 2 steps, repeat the cycle of updating $W$ → re-estimating → updating $W$... until convergence. Improves stability and efficiency compared to two-step.
3. **Continuously Updated Estimator (CUE)**: estimates $\beta$ and $W(\beta)$ simultaneously in **one single** optimization problem, instead of alternating as in the two variants above: $\hat\theta=\arg\min_\theta g(\theta)'\hat S(\beta)^{-1}g(\theta)$. In large samples, CUE achieves efficiency on par with optimal GMM; in small samples, it can sometimes **outperform** two-step.

### Estimator comparison table


| Estimator | Asymptotics | Finite sample | Robustness | Practical takeaway |
|---|---|---|---|---|
| **2SLS** | Consistent if instrument valid; efficient under homoskedasticity + just-identified | Sensitive to weak IV | Not robust to hetero unless corrected | Workhorse — easy to use, closed form, but easily "breaks" when IV is weak |
| **LIML** | Asymptotically equivalent to 2SLS under strong IV | Less biased than 2SLS when IV is weak | Same robustness limits as 2SLS | Better small-sample properties than 2SLS; more stable with many IVs |
| **Fuller** | Same asymptotic limit as LIML | Reduces bias further compared to LIML | Same framework as LIML (linear IV) | Often the best choice when IV is weak or numerous |
| **Efficient GMM** | Most asymptotically efficient | Inherits weak-IV bias similar to 2SLS | Robust to hetero, handles many moment conditions | Preferred when IV is strong + heteroskedasticity present; unstable when IV is numerous/weak |


## Exam traps — extended

1. Calling the consequence of endogeneity on OLS "biased" in a generic way — the precise term is **inconsistent** (the terminology slides-16 corrects from slides-5); bias is a finite-sample problem, inconsistency is a problem that does not vanish no matter $N\to\infty$.
2. Rejecting the underidentification (relevance) test and then concluding right away "the instrument is strong enough" — these are **two different tests**: relevance (tier 1) and the strength/weak-instrument test (tier 2).
3. Rejecting underidentification/weak-instrument and then treating 2SLS as "certainly giving correct inference" — Anderson-Rubin/Stock-Wright are only strictly necessary in the borderline zone, but the general principle is: the closer the instrument is to the weak boundary, the more the standard t-test should be doubted.
4. Confusing the 2 criteria for choosing a Stock-Yogo threshold (**relative bias** vs **size distortion**) — an instrument can meet one criterion but not the other; "a good estimate does not guarantee a good test, and vice versa."
5. Failing to reject Sargan/Hansen J and then treating it as "proof the instrument is valid" — it only means "no evidence found against it"; validity **always** has to be argued through research design, never by the test statistic alone.
6. Testing overidentifying restrictions when the model is **just-identified** ($h=k$) — structurally $Z'e=0$ always holds, "there is nothing to test"; just-identified must **not** be read as "the instrument is automatically valid" — it only means validity cannot be tested with data in this case.
7. Forgetting that the Wu-Hausman conclusion (and statistic value) depends on the chosen significance level $\alpha$ **and** the type of VCV used — the same dataset can yield different conclusions depending on the pre-chosen $\alpha$ (e.g. endogenous at 10% but not at 5%).
8. Treating a statistically significant Anderson-Rubin/Stock-Wright result as evidence the "instrument is strong" or that it "improves the point estimate" — they only provide **valid inference** under weak instruments, they do not improve the 2SLS estimate itself, and they are only valid if the instrument is truly exogenous.
9. Mistaking exogeneity and exclusion for two independent conditions that must each be proven separately — mathematically exogeneity already implies exclusion; they are separated only to emphasize the practical risk (a direct path from the instrument to $y$ that the researcher overlooked).
10. Treating LIML/Fuller as "always better" than 2SLS — it is actually a trade-off: reduced bias in exchange for increased variance; only worth considering when weak/many instruments are a genuine concern, not the default choice for every IV problem.
11. Treating (efficient) GMM as a "universal upgrade" over 2SLS in every situation — GMM is only more efficient when heteroskedasticity is present; it **inherits the weak-IV bias problem intact**, same as 2SLS, and can be even more unstable when instruments are numerous/weak.
12. Confusing "included instruments" ($X_1$ — the exogenous variables already in the model) with "excluded instruments" ($IV$ — the newly added instrument variables) — $Z=[X_1, IV]$ is the **full** instrument set, not $IV$ alone.

## Connections to the rest of the course

This is the toolkit for resolving the violation of **A3 (exogeneity)** of [[concepts/linear-regression-model]] — completing the trio of most-commonly-violated assumptions and their fixes: A2 (near-violation) → [[concepts/multicollinearity]], A4 → [[concepts/heteroskedasticity]], A3 → endogeneity/IV on this very page.

- The **GMM** framework here reappears, extended further, in [[concepts/dynamic-panel-data-models]] (Topic 14 — Arellano-Bond/Difference GMM and Arellano-Bover-Blundell-Bond/System GMM are both concrete applications of the GMM framework to dynamic panel data).
- The entire diagnostic toolkit here (weak-instrument test, Sargan/Hansen, Wu-Hausman) is **reused almost intact**, with only an added transformation step to remove the fixed effect ($\alpha_i$) before applying 2SLS/LIML/Fuller/GMM, in [[concepts/iv-regression-panel-data]] (Topic 13 — IV regression for panel data, using an FD or FE transformation before feeding into 2SLS).
- The **omitted variable** issue (section 2.1) is the direct thread connecting to [[concepts/econometrics-overview]] (the identification problem, introduced back in Topic 0) — endogeneity is exactly the technical formalization of the question "is correlation causation?" that the entire course revolves around.
- The **Wu-Hausman** test here shares the same comparison logic — "two estimators, one consistent-under-all-conditions and one consistent-only-under-$H_0$" — with the **Hausman test** in [[concepts/fixed-random-effects-model]] (Topic 6/12, comparing Fixed Effects vs Random Effects) — same namesake (Hausman), same underlying idea, different application context. See [[people/hausman]].
