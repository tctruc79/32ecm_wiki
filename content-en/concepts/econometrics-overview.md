---
title: "Econometrics: Tổng quan, Causality và Identification"
type: concept
status: mature
tags: [foundations, causality, identification, research-design]
sources: ["[[sources/intro-to-econometrics]]", "[[sources/2026-course-outline]]"]
related: ["[[concepts/linear-regression-model]]", "[[concepts/binary-response-models]]", "[[concepts/fixed-random-effects-model]]", "[[concepts/endogeneity-iv-regression]]"]
updated: 2026-08-29
---

> **How to read this page**: this is the **foundational philosophy** page for the entire course — there is no specific estimation formula here, only the foundational thinking that every later technique (OLS, IV, panel data, logit/probit...) serves.
> If [[concepts/linear-regression-model]] answers the question "how do we estimate, how reliable is it", this page answers the question that comes *before* that: "why do we need to estimate at all, and why does estimating a number not mean we have correctly understood the causal relationship".
> Read this page first, then read [[concepts/linear-regression-model]] to understand the technical mechanics.

## 1. Why do we need Econometrics? — the starting point is an economic question

Economics puts forward many theories about the behavior of individuals, firms, and markets.
But a theory, however reasonable it sounds, remains only a **hypothesis** until there is evidence from real data.
The slide opens the course with 4 empirical questions to illustrate this:

- Does education increase wages?
- Does foreign direct investment (FDI) reduce inequality?
- Do higher electricity prices cause households to reduce electricity consumption?
- What is the impact of carbon taxes on emissions?

What all 4 questions have in common: they are all **causal** questions, not merely descriptive ones.
**Econometrics** is defined (per the slide) as:

> Econometrics is the discipline that uses statistical methods and data to quantify economic relationships and evaluate economic theories.

Specifically, econometrics allows economists to do 4 things:

1. **Estimate the magnitude** of economic relationships (e.g., by how many % wages rise for one more year of schooling, not just "does it rise or not").
2. **Test economic theories** using real data, instead of relying on pure theoretical reasoning alone.
3. **Evaluate the impact of policies and interventions** — e.g., raising electricity prices, imposing carbon taxes.
4. **Make well-founded forecasts** about future economic outcomes.

## 2. Three components that define Econometrics

The definition of econometrics always comes with three components, all three of which must be present — missing one, what remains is no longer econometrics in the sense the course means it:

|Component |Role |Illustration: the education → wage example |
|---|---|---|
|**Economic theory** |Puts forward a **hypothesis** about how the variables relate to each other, and **why** |Human capital theory (e.g. Mincer 1974, already mentioned in [[concepts/linear-regression-model]]) holds that education increases labor productivity, thereby increasing wages |
|**Mathematical model** |**Formalizes** that hypothesis into a specific, estimable equation | $wage = \beta_0 + \beta_1 \cdot education + u$ |
|**Statistical methods** |**Estimates and tests** that equation using real data — producing a specific number and the reliability of that number |Uses OLS (see [[concepts/linear-regression-model]]) on a real data sample to estimate $\hat\beta_1$, then tests whether this coefficient is statistically significant |

**A point beginners often misunderstand**: econometrics is **not** "taking a dataset and running a regression to see what comes out".
If step (1) is missing — no economic theory as a foundation — the choice of which variables to include in the model becomes arbitrary, and the resulting estimate can be completely meaningless economically even if the statistics look "clean".
The correct sequence is always: have an economic question → have a theory that explains it → only then formalize it into a model → only then estimate.

## 3. Econometrics vs. Statistics — same tools, different questions

Econometrics and statistics share many mathematical/statistical tools, so they are easily mistaken for "the same thing".
The difference lies in the **objective**, not in the formulas:

|  | Statistics | Econometrics |
|---|---|---|
|Focus |Describing patterns in data |Economic mechanisms |
|Objective | Prediction, statistical inference | Causal inference |
|Scope |Broadly applicable, across many fields |Evaluating economic theory & policy |

The slide illustrates this difference using exactly one situation, framed under two different question angles (household electricity consumption):

- **Statistical question**: "Can we predict household electricity consumption from income and household size?" — concerned only with **whether it can be predicted**, not with the mechanism.
- **Econometric question**: "Does a higher electricity price cause households to reduce electricity consumption?" — requires a **causal** answer, meaning "the price increase" must actually be the *cause*, not merely a good predictor.

A good predictive model (statistics) can perfectly well use variables that have no causal relationship with the outcome whatsoever (e.g., using a "month of the year" variable to predict electricity consumption — a good predictor but not a cause).
In contrast, an econometric question demands much greater rigor.
This is the most important reason: **many statistical methods are borrowed by econometrics from statistics, but adapted to solve the identification problem** (see section 7) — this is the real boundary between the two disciplines, not the mathematical tools.

## 4. What is Statistical Association?

**Association** (statistical linkage) means that when one variable changes, the other also changes in a systematic way — the two variables "move together" in the data.
Association is measured using familiar tools: **correlation**, **regression coefficients**, **conditional averages**.

The slide gives three purely-association examples (not yet saying anything about causation):

- Households with higher income tend to consume more electricity.
- Cities with more cars tend to have higher air pollution.
- Ice cream sales rise when the number of drowning accidents rises.

For each example, the question the slide immediately poses is: **"If two variables have an association, does that mean one causes the other?"** — and the answer running through the whole course is **not necessarily**.

Another example the slide uses to clarify the boundary between **association** and **causality** as two separate concepts:

- **Association** (pure observation): "Taller workers tend to earn higher wages" — just an observed pattern, saying nothing yet about the mechanism.
- **Causality** (a true causal relationship): "An increase in electricity price causes households to reduce electricity consumption" — this is a statement about **mechanism**, far stronger than an observed pattern.

The central question econometrics exists to answer, exactly as the slide poses it: ***"Does X merely move together with Y, or does X actually cause Y?"***

## 5. Association ≠ Causality: Three sources of confusion

Three reasons why an observed association **does not** prove causality:

### 5.1 Confounding variables

A third factor affects **both** of the observed variables, causing them to "move together" even though neither variable causes the other.

> *Example*: Bigger fires have more firefighters **and** more damage.
> Does this mean firefighters cause fire damage? **No.**
> It is the size of the fire (the confounding variable) that causes **both**: more damage, and the need to dispatch more firefighters to the scene.

### 5.2 Reverse causality

The variable we think is the "outcome" (Y) is in fact the one that causes an effect back on the variable we think is the "cause" (X).

> *Example*: Areas with higher crime tend to have more police.
> Does this mean police cause crime? **No.**
> The authorities dispatch more police **to** places that already have high crime — the direction of causality runs opposite to the initial intuition.

### 5.3 Coincidence

Two variables move together entirely by chance, with no real mechanism linking them.

> *Classic example*: The number of pirates in the world has been steadily declining while global temperature has been steadily rising.
> Does this mean fewer pirates causes global warming? **No.**
> These two variables move together purely by coincidence, not because one causes the other.

### 5.4 Why this matters for policy — a table illustrating policy mistakes

Confusing association with causation is not merely an academic error — it leads directly to **policy mistakes** if decision-makers act on correlation numbers without checking the causal mechanism behind them.

|Observation (association) |Wrong conclusion if mistaken for causal |Possible resulting policy mistake |Why it's wrong |
|---|---|---|---|
|Ice cream sales rise at the same time as drowning accidents rise |"Eating ice cream increases drowning risk" |Restrict/heavily tax ice cream sales to reduce drowning accidents |Both very likely rise because of the same third cause: hot weather leads people to both buy more ice cream and swim/go to the beach more (raising drowning risk) — ice cream does not cause drowning |
|Bigger fires have more firefighters and more damage |"Dispatching more firefighters increases damage" |Cut the firefighting force to reduce fire damage |The size of the fire (the confounder) causes both; cutting firefighters would actually make damage **worse** |
|High-crime areas have more police |"Police increase crime" |Withdraw police from the area to reduce crime |The direction of causality is reversed: police are dispatched *because* crime is high, they are not the cause of crime |

> **Note on the source**: the original slide only lists the "ice cream sales – drowning accidents" pair as an example of statistical association (section 4), and **does not** explain the specific mechanism behind it.
> The interpretation "hot weather is the confounder" in the first row of the table above is inferred by applying the exact same confounding logic this slide uses to explain the firefighter example (a third factor causing both observed variables) — it is not verbatim from the slide.
> This is noted explicitly here so as not to conflate original slide content with an inference applying similar logic.

## 6. Ceteris paribus — "other factors held constant"

Even after avoiding the three traps in section 5, the real economic question a researcher cares about is usually not "do X and Y move together" but rather: **holding all other relevant factors constant, how much does Y change when X changes by 1 unit?**
This is called the **ceteris paribus** effect ("everything else held constant" — Latin).

*The slide's example*: How does wage change when education increases, **holding fixed** ability, family, and other factors?
To control for these factors, we include them in the same regression equation:

$$wage = \beta_0 + \beta_1 \cdot education + \beta_2 \cdot ability + \cdots + u$$

In observational data, many factors simultaneously affect the economic outcome.
If these factors are not controlled for, the observed relationship may reflect **many effects mixed together**, not just the effect of the variable we care about.

**The practical problem**: in practice, we rarely observe **all** the relevant factors such as ability — this is exactly the point that connects directly to section 7.

## 7. Omitted Variable Bias (OVB)

To correctly estimate the ceteris paribus effect, one needs to control for **every** relevant factor affecting the outcome.
But in reality, some relevant variables are **unobservable or have no available data**.
When an important factor is omitted from the regression model, the estimated coefficient can become **biased**.

Back to the education–wage example with the simple equation (controlling for nothing yet):

$$wage = \beta_0 + \beta_1 \cdot education + u$$

This equation ignores confounding factors such as **ability, family, social networks**.
Because these factors affect **both** education level and labor-market outcomes (wages), and because they are unobserved, they sit entirely inside the error term $u$ — making `education` **correlated with the error term**.
Result: the estimated coefficient $\hat\beta_1$ no longer measures purely "the true effect of education", but **mixes together** two things:

- the true effect of education on wage, **and**
- the effect of ability on wage (wrongly "attributed" to education because the two variables are correlated with each other).

**Explanation for beginners of what "bias" means**: bias here is not "random error" (if we resample repeatedly, random error averages out to 0).
Bias is a **systematic deviation** — no matter how many data samples you draw, the estimate keeps deviating in a consistent direction from the true value, because the very *way the model was built* (missing an important variable) was wrong from the start.
Increasing the sample size **does not** fix omitted variable bias — this is entirely different from the problem of "imprecise estimates due to a small sample".

The natural question that arises from this, and which is also the central question for the rest of the course: **if important factors are unobservable, how can we identify the true effect of education on wages?**
This is precisely **why the course exists** — almost every subsequent topic (multicollinearity, heteroskedasticity, and especially [[concepts/endogeneity-iv-regression]]) revolves around detecting and handling different variants of this problem.

## 8. The Identification Problem — the heart of Econometrics

> A parameter is called **identified** when the data and the model allow us to **isolate** the causal effect of a variable on the outcome.

### 8.1 Intuition: what is "clean variation"?

Economists care about the ceteris paribus effect of a variable on an outcome.
But in observational data, the variable we care about is usually affected by **many other factors at the same time** — meaning its observed variation reflects **many mixed sources of influence**, not just the causal mechanism we want to study.
**Identification** means finding the portion of variation in the explanatory variable that is **not** driven by confounding factors — only with this "clean" variation can we truly isolate the causal effect.

### 8.2 A full example: electricity price and electricity consumption

The slide uses the same "statistical vs. econometric question" example from section 3 to concretely illustrate the identification problem:

- We want to estimate the effect of electricity price on household electricity consumption.
- Observed: areas with higher electricity prices tend to have lower electricity consumption.
- But this pattern could be driven by many other factors: **income, climate, housing characteristics, energy efficiency**.
- Because these factors vary differently across regions, the observed relationship **may not reflect** the true effect of the price.
- **To identify the causal effect**, we need variation in the electricity price that is **not** related to these confounding factors.
- *Example of "clean" variation*: a government policy that raises the electricity price **uniformly** across many regions. In this case, the variation in price is not driven by the specific characteristics of individual households — this type of variation helps isolate the ceteris paribus effect of price on consumption.

### 8.3 Why economics is harder than natural science in this respect

In natural sciences, causal relationships are usually studied using **controlled experiments**: the researcher actively changes one variable while holding other factors constant.

> *The slide's example*: to study the effect of a drug, the researcher **randomly assigns** patients into a treatment group and a control group.
> Because the assignment is random, other factors are automatically balanced between the two groups — thereby isolating the true causal effect of the drug.

In economics and other social sciences, **controlled experiments are often difficult or impossible to carry out**.
Economic outcomes are affected by many factors that are not easy to control directly:

- we cannot randomly assign **years of schooling** to each individual;
- we cannot randomly vary the **tax system** applied to each individual;
- policies usually affect **many groups** simultaneously, making it hard to isolate individuals.

Therefore, economists usually have to rely on **observational data** (data that is observed, not generated by a controlled experiment) and indirect **identification strategies** to replicate, as closely as possible, the "clean variation" condition that a randomized experiment naturally provides.
This is precisely why the entire rest of the course exists: IV regression ([[concepts/endogeneity-iv-regression]]), panel data FE/RE ([[concepts/fixed-random-effects-model]]), dynamic panel GMM... are all different "identification strategies", suited to different data contexts, but sharing one goal: finding variation that is not driven by confounding.

## 9. The empirical research process

Empirical economic research usually follows a 6-step sequence:

1. **Research question** — a clearly defined economic question. *Example*: does a higher electricity price reduce household electricity consumption?
2. **Economic theory** — the theoretical framework explaining why that relationship might exist. *Example*: consumers reduce consumption when the price rises (basic demand theory).
3. **Empirical model** — the formal representation of the theoretical relationship. *Example*: $Consumption = f(Price, Income, Household\ Characteristics)$.
4. **Data** — collecting observed data for the relevant variables.
5. **Econometric analysis** — the statistical methods used to estimate the relationship and test hypotheses.
6. **Interpretation and policy implications** — interpreting the results and drawing out policy implications.

### Three foundational questions at every step

The slide emphasizes: behind the 6 technical steps above, there are **three foundational questions** that truly determine the quality of an empirical study — illustrated again using the same electricity-price example:

1. **What is the economic question?** — the relationship of interest needs to be clearly defined. *Example*: does a higher electricity price reduce household electricity consumption? This step identifies: the outcome variable, the main variable of interest, and the behavioral/policy question being asked.
2. **What is the economic mechanism?** — the economic theory explaining **why** this relationship might exist. *Example*: a higher price raises the cost of consumption, which may lead households to reduce electricity use. Theory helps identify: which variables matter, and how they relate to each other.
3. **Can the causal effect be identified in the data?** — the observed relationship may be confounded by other factors; the core challenge is isolating the portion of variation in the explanatory variable that is **not** driven by confounding influences. This is precisely the **central task of econometrics**, not question (1) or (2).

> Note related to the Course Outline: `VNP2026-CO.pdf` describes Topic 0 (Introduction) as covering exactly the content areas matching this slide — "the use of econometrics", "some alternative statistical techniques", "econometric analysis in the research process" — confirming that this page correctly covers the foundational philosophy taught in the course's first session.
> Other logistical details of the CO (grading scale, 15/16 topics, software...) are not directly relevant to causal inference, so they are not repeated here — see `sources/2026-course-outline.md`.

## 10. Summary exam traps

1. **Interpreting association as causation** just because two variables "move together" in the data — always ask whether confounding, reverse causality, or coincidence could explain this pattern, before concluding causality.
2. **Assuming that running a regression automatically produces a causal effect** — a regression coefficient only describes a relationship *within the data*; without a credible identification strategy, the estimated coefficient **does not represent** the causal effect, no matter how strong its statistical significance.
3. **Focusing on estimation (computing the coefficient) while forgetting identification (finding "clean" variation)** — the central challenge of econometrics is not *computing* a number $\hat\beta$, but finding a source of variation in the explanatory variable that is not driven by confounding. Computing a coefficient is easy; identifying the causal effect is the hard part.
4. **Confusing "no confounder is clearly observed" with "no confounder exists"** — omitted variable bias occurs precisely because confounding factors (like ability) are usually **unobservable**, not because they don't exist.
5. **Treating the ceteris paribus effect (controlling for observed variables) as the causal effect** — controlling for the variables *present in the data* does not guarantee every confounder has been controlled for; omitted variable bias can still remain from factors that are not yet, or cannot be, observed.
6. **Confusing statistics and econometrics** — a good predictive model (statistics) does not mean a causal relationship has been found (econometrics); two different objectives that share tools but cannot be equated.
7. **Over-extrapolating from a coincidence or confounding example into a policy proposal** (see the table in section 5.4) — the classic policy mistake is acting as if association were causation, leading to intervening on exactly the wrong variable (e.g. restricting ice cream sales to reduce drowning).

## 11. Connection to the rest of the course

This page is the anchor for the entire wiki.
The course introduction slide describes **3 main parts**, each a different set of tools for solving the identification problem in different data contexts:

- **Part 1 — The Linear Regression Model and its problems**: OLS, multicollinearity, heteroskedasticity, endogeneity. See [[concepts/linear-regression-model]] (OLS, 5 assumptions), [[concepts/functional-forms]], [[concepts/multicollinearity]], [[concepts/heteroskedasticity]], [[concepts/endogeneity-iv-regression]].
- **Part 2 — Models for Limited Dependent Variables**: logit/probit, multinomial logit, Poisson/negative binomial regression, ordinal response model, censored/truncated regressions. See [[concepts/binary-response-models]] (LPM/Logit/Probit), [[concepts/multinomial-logit-model]], [[concepts/ordinal-response-models]], [[concepts/count-data-models]], [[concepts/censored-regression-tobit]].
- **Part 3 — Panel data models**: FE/RE, IV regression for panel data (2SLS, LIML, GMM), dynamic panel data model. See [[concepts/fixed-random-effects-model]] (FE/RE), [[concepts/iv-regression-panel-data]], [[concepts/dynamic-panel-data-models]] — using the time dimension to control for unobserved, time-invariant confounders (a different identification strategy, one that does not require an external instrumental variable).

All 15 topics of the course have been ingested (see `index.md` for the full listing) — this page serves as the overall map connecting everything: every technical tool on the other `concepts/` pages is a specific answer to the single philosophical question this page poses — **how to identify the causal effect when a true controlled experiment cannot be run**.
