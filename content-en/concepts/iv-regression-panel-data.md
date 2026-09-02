---
title: "Instrumental Variable (IV) Regression for Panel Data"
type: concept
status: mature
tags: [panel-data, instrumental-variables, 2sls, gmm, endogeneity]
sources: ["[[sources/slides-14-iv-regression-panel-data]]"]
related: ["[[concepts/endogeneity-iv-regression]]", "[[concepts/fixed-random-effects-model]]", "[[concepts/dynamic-panel-data-models]]"]
updated: 2026-08-29
---

> **How to read this page**: this is a **bridge** page — not a starting point.
> If you haven't mastered 2SLS, LIML/Fuller, GMM, and the four groups of diagnostic tests (underidentification, weak instrument, overidentification, Wu-Hausman) at the cross-section level, read [[concepts/endogeneity-iv-regression]] first — that page is the foundation, and this page **does not re-teach** what 2SLS is.
> If you haven't mastered FE/RE and the A3a/A3b assumption set (split from the original A3), read [[concepts/fixed-random-effects-model]] first — this page reuses that exact framework.
> This page focuses only on the **extension specific to panel data**: how to remove $\alpha_i$ (individual effects) *before* applying the already-learned IV toolkit, and the adjustments needed for the diagnostic tests when moving from cross-section to panel.

## Why is IV still needed even with FE?

This is the first question that needs a clear answer before diving into formulas — otherwise it's easy to mistakenly assume "once FE is used, endogeneity is gone."

Recall from [[concepts/fixed-random-effects-model]]: the original exogeneity assumption A3 from [[concepts/linear-regression-model]] gets **split into two** when moving to panel data:

- **A3a**: $E(X_{it}\varepsilon_{it})=0$ — the explanatory variable is uncorrelated with the **time-specific** error (idiosyncratic error) $\varepsilon_{it}$.
- **A3b**: $E(X_{it}\alpha_i)=0$ — the explanatory variable is uncorrelated with the **time-invariant individual effect** (individual effect) $\alpha_i$.

**The FE model solves A3b but does not solve A3a.** Intuition: the within-transformation (or first-difference) only removes the **time-invariant** part of the error ($\alpha_i$) — because that part is identical across every $t$ for the same unit $i$, subtracting the mean (or subtracting the previous period) makes it vanish. But if $X_{it}$ is correlated with $\varepsilon_{it}$ — the error part that **changes at each specific point in time**, not a constant unique to each unit — then this transformation is **powerless**: $\varepsilon_{it}$ still remains fully in the equation after $\alpha_i$ has been removed.

**Concrete example (used throughout this page, taken from the slide)**: firm $i$ decides to increase labor training hours (`training`) in year $t$ because management *anticipates* that production demand for that year will rise (reverse causality/simultaneity — see also the three sources of endogeneity in [[concepts/endogeneity-iv-regression]]). This decision changes from year to year for each specific firm, not a fixed characteristic of that firm — so it belongs in $\varepsilon_{it}$, not in $\alpha_i$. FE (even after removing every fixed difference across firms — industry scale, geographic location, baseline management capability…) **cannot remove** this type of correlation. This is exactly why IV is needed **even after FE has already been used**.

## Model setup

$$y_{it}=\gamma Y_{it}+\beta X_{it}+\alpha_i+\varepsilon_{it}, \qquad W_{it}=[Y_{it}, X_{it}],\; \delta=[\gamma,\beta]$$

- $Y_{it}$: vector of **endogenous** variables (correlated with $\varepsilon_{it}$ — violates A3a).
- $X_{it}$: vector of **exogenous** variables.
- $\alpha_i$: individual effects (unobserved).
- $\varepsilon_{it}$: time-specific (idiosyncratic) error.

Compactly: $y_{it}=\delta W_{it}+\alpha_i+\varepsilon_{it}$. The instrument $IV_{it}$ must satisfy the two familiar conditions — **relevance** and **exogeneity** (see [[concepts/endogeneity-iv-regression]]).

**Note on scope**: this is a **static model** — there is no lagged $y$ on the right-hand side. The case with a lagged term (dynamic panel, where $y_{i,t-1}$ itself becomes the endogenous variable) belongs to [[concepts/dynamic-panel-data-models]], which uses different logic (internal instruments).

**Models/estimators available per the slide**:
- **RE-IV** (Generalized 2SLS) — the slide states verbatim "**not covered**". This is a gap **explicitly confirmed** by the slide itself (unlike gaps that must be inferred from the absence of content) — the Course Outline lists "2SLS RE estimator"/"G2GLS estimator" for Topic 13, but the actual slide does not teach it. Recorded verbatim.
- **FD-IV** (First-Difference) — 2SLS, plus the LIML/Fuller/GMM variants.
- **FE-IV** (Fixed Effects) — 2SLS, plus the LIML/Fuller/GMM variants.

### Running data example

Dataset: 300 firms × 5 years (balanced panel, $N=1500$).

| Biến / Variable | Ý nghĩa / Meaning | Vai trò / Role |
|---|---|---|
| `output` | Giá trị sản lượng (mil. VND) / Output value (mil. VND) | Biến phụ thuộc, dùng $\ln$ / Dependent variable, uses $\ln$ |
| `capital` | Giá trị vốn vật chất (mil. VND) / Physical capital value (mil. VND) | Ngoại sinh, dùng $\ln$ / Exogenous, uses $\ln$ |
| `training` | Giờ đào tạo/lao động (giờ/người) / Training hours per worker (hours/person) | **Nội sinh nghi ngờ** / **Suspected endogenous** |
| `labor` | Số lao động (người) / Number of workers (persons) | Ngoại sinh, dùng $\ln$ / Exogenous, uses $\ln$ |
| `export` | Dummy, 1 = có xuất khẩu / Dummy, 1 = exports | Ngoại sinh / Exogenous |
| `credit` | Dummy, 1 = có tiếp cận tín dụng / Dummy, 1 = has credit access | Ngoại sinh / Exogenous |
| `tech` | Trình độ công nghệ tương đối: `lowtech` (nền), `mediumtech`, `hightech` / Relative technology level: `lowtech` (base), `mediumtech`, `hightech` | Ngoại sinh (categorical → 2 dummy) / Exogenous (categorical → 2 dummies) |
| `subeligible` | Dummy, 1 = doanh nghiệp đủ điều kiện nhận trợ cấp đào tạo / Dummy, 1 = firm eligible for training subsidy | **Instrument (excluded)** |
| `localbudget` | Ngân sách chính quyền địa phương cho đào tạo (mil. VND) / Local government training budget (mil. VND) | **Instrument (excluded)** |

Specific model: $\ln(output)_{it} = \alpha_i + \gamma\,training_{it} + \beta_1\ln(capital)_{it} + \beta_2\ln(labor)_{it} + \cdots + \varepsilon_{it}$.

**Benchmark — basic FE, treating `training` as exogenous** (not yet addressing suspected endogeneity, used for comparison against the IV results in later sections):

| Biến / Variable | Estimate | SE | t | p |
|---|---|---|---|---|
| `log(capital)` | 0.25465 | 0.01063 | 23.96 | <0.001 *** |
| `log(labor)` | 0.02106 | 0.01522 | 1.38 | 0.167 |
| **`training`** | **0.04185** | 0.00211 | 19.87 | <0.001 *** |
| `export` | 0.01613 | 0.02045 | 0.79 | 0.430 |
| `credit` | 0.07176 | 0.01900 | 3.78 | <0.001 *** |
| `mediumtech` | 0.00925 | 0.02096 | 0.44 | 0.659 |
| `hightech` | 0.21237 | 0.02554 | 8.32 | <0.001 *** |

Remember the number **0.04185** for `training` — this is the "naïve" FE coefficient, which will be compared again in section 7.4 once the FE-IV result is available, to concretely illustrate the magnitude of bias caused by endogeneity.

## First-Difference IV (FD-IV) Estimator

### Intuition: differencing removes $\alpha_i$ first, then 2SLS

The mechanism is identical to the first-difference idea in ordinary panel data: $\alpha_i$ is a constant **specific to each unit** $i$, unchanging over $t$. If the equation is written at two consecutive time points for the same unit and then **subtracted from each other**, $\alpha_i$ appears identically on both sides and **cancels out on its own** — no need to know its value.

$$y_{it}=\delta W_{it}+\alpha_i+\varepsilon_{it}, \qquad y_{i,t-1}=\delta W_{i,t-1}+\alpha_i+\varepsilon_{i,t-1}$$

Subtracting side by side:

$$y_{it}-y_{i,t-1}=\delta(W_{it}-W_{i,t-1})+(\varepsilon_{it}-\varepsilon_{i,t-1}) \;\;\Rightarrow\;\; \Delta y_{it}=\delta\Delta W_{it}+\Delta\varepsilon_{it}$$

The differenced equation **no longer contains $\alpha_i$** — but $\Delta\varepsilon_{it}$ can still be correlated with $\Delta W_{it}$ if $Y_{it}$ is endogenous (this is why A3a is not automatically solved by differencing alone — unlike A3b). The next step: apply **2SLS exactly as in the cross-section case** ([[concepts/endogeneity-iv-regression]]), but on the differenced variables, with the instrument also differenced $\Delta IV_{it}$.

### Numeric example (FD-IV, conventional/IID SE)

```
FDIV: d(log(output)) ~ d(log(capital)) + d(log(labor)) + d(export) + d(credit)
      + d(mediumtech) + d(hightech) | 0 | d(training) ~ d(subeligible) + d(localbudget)
```

| Biến / Variable | Estimate | SE | t | p |
|---|---|---|---|---|
| Intercept | 0.033730 | 0.013872 | 2.43 | 0.015 * |
| **`fit_d(training)`** | **0.016833** | 0.005997 | 2.81 | 0.005 ** |
| `d(log(capital))` | 0.272336 | 0.011799 | 23.08 | <0.001 *** |
| `d(log(labor))` | 0.033934 | 0.016140 | 2.10 | 0.036 * |
| `d(export))` | 0.017373 | 0.021595 | 0.80 | 0.421 |
| `d(credit))` | 0.081324 | 0.020953 | 3.88 | <0.001 *** |
| `d(mediumtech))` | 0.055805 | 0.023798 | 2.34 | 0.019 * |
| `d(hightech))` | 0.251878 | 0.029615 | 8.51 | <0.001 *** |

$N=1200$ observations (down from 1500 because differencing loses the first year of each firm: $300\times(5-1)=1200$).

## Fixed Effects IV (FE-IV) Estimator

### Intuition: the within-transformation removes $\alpha_i$ first, then 2SLS

The mechanism runs parallel to ordinary FE ([[concepts/fixed-random-effects-model]]): subtract from each variable **its own unit's time average** ($\bar y_i$, $\bar W_i$…). Because $\alpha_i$ does not change over $t$, its time average **is exactly $\alpha_i$** — subtracting it makes it vanish, by the exact same mechanism as section 3.1, just a different operation (demeaning instead of differencing).

$$\tilde y_{it}=y_{it}-\bar y_i+\bar y, \qquad \tilde W_{it}=W_{it}-\bar W_i+\bar W, \qquad \tilde{IV}_{it}=IV_{it}-\overline{IV}_i+\overline{IV}$$

(adding back the overall sample mean $\bar y$, $\bar W$, $\overline{IV}$ is just a convention to keep the original scale — it does not affect the slope coefficients). The transformed equation:

$$\tilde y_{it}=\delta\tilde W_{it}+\varepsilon_{it}$$

No more $\alpha_i$ → apply 2SLS to $\tilde y_{it}$ and $\tilde W_{it}$, with instrument $\tilde{IV}_{it}$.

### Numeric example (FE-IV, conventional/IID SE)

```
FEIV1: log(output) ~ log(capital) + log(labor) + export + credit + mediumtech + hightech
       | id | training ~ subeligible + localbudget
```

$N=1500$, fixed-effects: `id` (300 groups).

| Biến / Variable | Estimate | SE | t | p |
|---|---|---|---|---|
| **`fit_training`** | **0.021190** | 0.005724 | 3.70 | <0.001 *** |
| `log(capital)` | 0.264823 | 0.011351 | 23.33 | <0.001 *** |
| `log(labor)` | 0.029598 | 0.015970 | 1.85 | 0.064 . |
| `export` | 0.030703 | 0.021588 | 1.42 | 0.155 |
| `credit` | 0.090846 | 0.020351 | 4.46 | <0.001 *** |
| `mediumtech` | 0.036322 | 0.022865 | 1.59 | 0.112 |
| `hightech` | 0.256436 | 0.028846 | 8.89 | <0.001 *** |

### Extension: Two-way FE-IV

The slide has a dedicated section "Two-way FE-IV Regression" — in substance, this is just adding **time fixed effects** $\gamma_t$ alongside $\alpha_i$ (like two-way FE in [[concepts/fixed-random-effects-model]]), declared in `fixest` with `| id + year |` instead of `| id |`:

```r
eqIVfixest2 = log(output) ~ log(capital) + log(labor) + export + credit + mediumtech + hightech
              | id + year | training ~ subeligible + localbudget
```

The slide only presents the code for all 5 types of SE (homoskedastic, individual hetero, clustered by `id`, two-way clustered `id+year`, Driscoll-Kraay) — **without an accompanying numeric results table** for this part, unlike the one-way FD-IV/FE-IV above which have full numeric tables. Recorded exactly as presented in the slide, without inferring numbers.

## FD-IV vs. FE-IV comparison — which to choose when

Both validly remove $\alpha_i$ and both use the same 5 types of SE (conventional/robust/clustered/two-way clustered/Driscoll-Kraay) with application conditions identical to [[concepts/fixed-random-effects-model]] (two-way clustered and DK need $T$ large enough to be reliable). But **the two estimators do not coincide numerically** unless $T=2$ — evidence right in the example above: the `training` coefficient is **0.0168** (FD-IV) versus **0.0212** (FE-IV), not the same despite the same data, same instruments.

> **Note on the source**: the slide **does not give an explicit decision rule** between FD-IV and FE-IV beyond presenting both as parallel options (differing only in SE robustness notes, which are identical across the two models). The "which to choose" reasoning below is **general panel-data econometrics background knowledge** (not excerpted from this slide) — included because it's useful for choosing an estimator in practice/thesis work, but it must be clearly distinguished as content not directly confirmed by the slide.

Classic criterion: the relative efficiency between FD and FE depends on the **serial correlation structure** of $\varepsilon_{it}$:

- If $\varepsilon_{it}$ **has no serial correlation** (close to white noise, like the ideal A4b assumption) → **FE (within) is more efficient**. Intuitive reason: differencing ($\Delta\varepsilon_{it}=\varepsilon_{it}-\varepsilon_{i,t-1}$) of an originally uncorrelated series **artificially creates** negative first-order (MA(1)) correlation — making FD less efficient than necessary.
- If $\varepsilon_{it}$ has **strong** serial correlation, **close to a random walk** (persistent shock, effect lasting many periods) → **FD is more efficient**. Intuitive reason: differencing a near-random-walk series produces residuals close to white noise (each shock appears only once in $\Delta\varepsilon_{it}=\varepsilon_{it}-\varepsilon_{i,t-1}$ then vanishes in the next period), whereas the within-transformation still retains the entire persistent component.
- In practice: run both, compare precision (SE) and coefficient stability across different SE specifications; if the two results diverge substantially, that is also a signal worth noting (though not a formal test) about model specification.

## Alternative estimators: LIML, Fuller, GMM

The framework is identical to [[concepts/endogeneity-iv-regression]] — both FD-IV and FE-IV can be estimated with four methods: 2SLS, LIML, Fuller-adjusted LIML, GMM (2-step/iterative/CUE), applied **after** differencing/demeaning to remove $\alpha_i$.

**κ-class estimator**: $b(\kappa)=\big[X'(I-\kappa M_Z)X\big]^{-1}X'(I-\kappa M_Z)y$, $M_Z=I-Z(Z'Z)^{-1}Z'$. $\kappa=0$ → OLS; $\kappa=1$ → 2SLS. LIML picks $\kappa$ as the minimum eigenvalue of $B^{-1}A$, with $A=Y'M_ZY$, $B=Y'M_XY$ — equivalent to the smallest root of $\det(A-\kappa B)=0$. Intuition: the κ-class "interpolates" between OLS and 2SLS; LIML picks the optimal point according to the likelihood function, which makes it **less biased than 2SLS when instruments are weak**.

**Fuller adjustment**: although LIML has less bias than 2SLS when instruments are weak, it can still have large variance and small-sample issues. Fuller (1977) proposed adjusting $\kappa$:

$$\kappa_F=\kappa-\frac{a}{n-l+k-1}$$

where $n$ = sample size, $k$ = number of regressors (endogenous + exogenous), $l$ = total number of instruments (included + excluded), $a$ = a positive constant usually chosen as 1 or 4. Result: $\hat\beta_F=b(\kappa_F)$.

**Panel-specific practical note** (unlike cross-section, explicitly stated in the slide): two-way clustered SE is **not reliable** when $T$ is small; Driscoll-Kraay SE is **not available** for LIML/Fuller estimation in common R packages — this is a practical constraint to remember when choosing an SE type, not simply picking "the most robust type is always best."

**On GMM in the static model**: under a static specification (no lagged terms), IV-GMM **does not meaningfully expand** the instrument set relative to 2SLS — both rely on the same excluded instruments, differing only in the weighting matrix $W$ (2SLS uses $W=(Z'Z)^{-1}$; efficient GMM uses $W=S^{-1}$). Under homoskedasticity, efficient GMM **collapses exactly to 2SLS**; under heteroskedasticity, GMM assigns lower weight to observations with larger error variance and is therefore more efficient — but **the empirical benefit in the static model is fairly limited** per the slide's note. (Comparison: GMM proves far more useful in **dynamic panel** — see [[concepts/dynamic-panel-data-models]] — where the internal instrument set expands substantially with the number of available lags.)

## Diagnostic tests for IV-panel

Reuses exactly the four groups of tests from [[concepts/endogeneity-iv-regression]], adjusted for panel. The slide notes: "*In R, diagnostic tests for IV regression with panel data is limited*" — the tools available in R are more limited than for pure cross-section.

### Underidentification test

$H_0: E(Z'Y)=0$ — the instrument carries no information to identify the endogenous variable. Use the **first-stage F test**. Important note: **the F value changes with the VCV structure** (conventional/robust/clustered/two-way clustered) — the VCV type must match the main model, without mixing them. Rejecting $H_0$ **does not mean** causal identification or a strong instrument — these are two different questions (see section 7.2).

**Numeric example** (FE-IV, two-way clustered SE by `id` and `year`):

$$F\text{-test (1st stage), training: stat} = 127.758, \quad p<2.2\times10^{-16}, \quad \text{on } 2 \text{ and } 1{,}491 \text{ degrees of freedom}$$

### Weak identification test: CD-F vs. KP-F

**Why are two statistic versions needed instead of one?** The same question "how much variation in $Y$ does the instrument explain" can be answered in two ways, depending on the error assumption at stage 1:

- **[[people/cragg-donald|Cragg-Donald]] Wald F (CD-F)**: assumes **homoskedasticity**.
- **Kleibergen-Paap rk Wald F (KP-F)**: **robust to heteroskedasticity** (and also clustering).

Intuition: exactly the same reason OLS needs both conventional SE and robust SE — if errors are hetero but a homo-assuming statistic is still used, the conclusion "instrument is strong enough" can be wrong. KP-F is the "patched" version for the more common real-world case (hetero, or panel with clustered errors).

**Special case to remember**: with **1 endogenous variable**, the first-stage F-statistic **exactly coincides with** CD-F. In the example above, `training` is the sole endogenous variable → $CD\text{-}F = 127.758$, far above both the rule-of-thumb threshold of 10 and any usual Stock-Yogo threshold → no evidence of a weak instrument.

**Decision rule**: compare CD-F against the **[[people/stock-yogo|Stock-Yogo]] (SY)** threshold or the rule-of-thumb value of 10 (details of the two SY criteria — relative bias vs. size distortion — see [[concepts/endogeneity-iv-regression]]).

> **The most important note in this section — a common exam trap**: **KP-F cannot be directly compared against the Stock-Yogo threshold**, because SY was built under the homoskedastic assumption while KP-F is not — applying a criterion to a statistic it's incompatible with is a technical error. The slide states clearly: in practice, people still **compare KP-F informally** with SY or with the threshold of 10, despite knowing this is not a theoretically rigorous comparison — it's merely a common practical convention, not a formally valid test.

**Note on the numeric example**: the slide's illustrative example (table in section 7.1) presents only **one** F value (using two-way clustered SE) and confirms in words that with 1 endogenous variable, this F is exactly CD-F — the slide **does not provide a separate KP-F number** to compare within this exact numeric example. Recorded exactly as the slide has it, without inferring an unprovided KP-F value.

### Overidentification test

The formula and logic are **identical** to the cross-section version in [[concepts/endogeneity-iv-regression]] — [[people/sargan|Sargan]] (assumes homoskedasticity) or [[people/hansen|Hansen's J]] (allows heteroskedasticity), same $\chi^2_{h-k}$ distribution, only performable when $h>k$ (over-identified) and **requires instruments already confirmed not weak beforehand** (section 7.2).

**Numeric example** (FE-IV, homoskedastic/IID): 2 instruments (`subeligible`, `localbudget`) for 1 endogenous variable (`training`) → degrees of freedom $=2-1=1$.

$$\text{Sargan: stat} = 1.6171, \quad p = 0.2035, \quad df=1$$

$p>0.05$ → **fail to reject** $H_0$ → no evidence against the joint validity of the two instruments.

**The point the slide emphasizes most, worth recording in spirit verbatim**: even though the Sargan result "supports" validity, the slide itself warns of two layers of limitation:
1. Sargan assumes homoskedastic — "*should be interpreted with caution given the presence of heteroskedasticity and serial correlation*" (in practice panel data almost always carries risk of both).
2. **More important than the test itself**: "*the credibility of the instruments ultimately relies on economic reasoning and the plausibility of the exclusion restriction, not the formal tests*" — the ultimate credibility of an instrument **never** comes from the test statistic itself, but from **economic reasoning** that the instrument affects $y$ **only through** the endogenous-variable channel, with no other direct path. Failing to reject Sargan/Hansen only means "no evidence found against it," absolutely not "the instrument has been proven valid."

### Test for endogeneity: Wu-Hausman

The logic and formula match [[concepts/endogeneity-iv-regression]]: if the suspected variable is actually exogenous and the instrument is strong, OLS/FE and 2SLS converge asymptotically to the same value; if endogenous, they diverge systematically.

$$H_0: X_2 \text{ exogenous}, \qquad \text{Statistic: } (\hat\beta_{2SLS}-\hat\beta_{OLS})'[V_{2SLS}-V_{OLS}]^{-1}(\hat\beta_{2SLS}-\hat\beta_{OLS}) \sim \chi^2_k$$

**Numeric example**: Wu-Hausman $=16.7$; at $\alpha=10\%$, $p\approx0.00<0.1$ → **strongly reject** $H_0$ → evidence that `training` is indeed endogenous.

**Visual comparison with section 2 and section 4.2** — a concrete numeric illustration well worth remembering for "feeling" endogeneity bias rather than just reading an abstract test statistic:

| Ước lượng / Estimate | Hệ số `training` / `training` coefficient |
|---|---|
| FE cơ bản (coi `training` ngoại sinh — mục 2) / Basic FE (treating `training` as exogenous — section 2) | **0.04185** |
| FE-IV (coi `training` nội sinh, IV = `subeligible`, `localbudget` — mục 4.2) / FE-IV (treating `training` as endogenous, IV = `subeligible`, `localbudget` — section 4.2) | **0.02119** |

The "naïve" FE coefficient is **nearly double** the corrected FE-IV coefficient — consistent with the economic story "firms increase training *because* they expect output to rise" (reverse causality): the "training increase alongside output increase" portion of the naïve FE coefficient is not entirely a causal effect of training on output, but partly reflects firms' self-selection correlated with growth expectations. FE-IV strips out and removes that bias, yielding a smaller coefficient — consistent with the Wu-Hausman conclusion that `training` is endogenous and OLS/FE is biased.

**Practical note prone to confusion**: the `fixest` package in R **does not use heteroskedastic VCV** to compute the Wu-Hausman statistic by default — a detail that can easily lead two users with two different packages to get two different Wu-Hausman numbers on the same data, even with the same model.

## Common exam traps

1. **Assuming that using FE already eliminates endogeneity.** FE only solves A3b (correlation with $\alpha_i$), not A3a (correlation with $\varepsilon_{it}$) — if the explanatory variable is endogenous with the time-specific error, IV is still needed even after using FE (see section 1).
2. Forgetting that both FD-IV and FE-IV must remove $\alpha_i$ **before** applying 2SLS — applying 2SLS directly to the original equation with $\alpha_i$ still intact gives wrong results (because $\alpha_i$ is unobserved and may be correlated with the endogenous variable, violating the instrument's own exogeneity condition).
3. **Confusing CD-F with KP-F when looking up the Stock-Yogo threshold** — SY was designed only for CD-F (homoskedastic assumption); comparing KP-F with SY is only an informal practical convention, not a theoretically rigorous comparison.
4. Treating rejection of the underidentification test as evidence the instrument is "strong" — these are two different tests (relevance vs. strength), exactly the same trap already noted in [[concepts/endogeneity-iv-regression]].
5. Assuming FD-IV and FE-IV always give **the same number** — they only coincide when $T=2$; with $T>2$ (as in the $T=5$ example here), the two `training` coefficients (0.0168 vs. 0.0212) are genuinely different.
6. Expecting GMM to always be substantially more efficient than 2SLS in a static model — the empirical benefit is fairly modest (unlike dynamic panel, where GMM proves much more useful).
7. Failing to reject Sargan/Hansen J and then treating it as "proof the instrument is valid" — and **more importantly**: forgetting that an instrument's ultimate credibility always rests on **economic reasoning** (a plausible exclusion restriction), not the test statistic itself — a point the slide itself emphasizes twice, not an inference by the wiki author.
8. Using two-way clustered SE or Driscoll-Kraay when $T$ is small — both are only reliable with $T$ large enough (same note as in [[concepts/fixed-random-effects-model]]); LIML/Fuller in particular have no DK SE available in common R packages.

## Connections

A direct bridge between [[concepts/endogeneity-iv-regression]] (Topic 5, cross-section data — supplies the entire 2SLS/LIML/Fuller/GMM machinery and the 4 groups of diagnostic tests) and [[concepts/fixed-random-effects-model]] (Topic 6/12, panel without endogeneity — supplies the A3a/A3b framework and the within/demean mechanism for removing $\alpha_i$). This page applies the IV toolkit exactly to a setting with $\alpha_i$, adding only the "remove $\alpha_i$ first" step (differencing or demeaning) compared to pure cross-section. It is a direct stepping stone to [[concepts/dynamic-panel-data-models]] (Topic 14), where the **lagged $y$** itself becomes the endogenous variable to be handled with similar IV logic, but with internal instruments instead of external instruments like `subeligible`/`localbudget` here.
