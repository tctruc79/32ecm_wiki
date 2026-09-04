---
title: "Econometrics Wiki — Index"
type: index
---

# Index — Econometrics Wiki (GS Trương Đăng Thụy)

Catalog of every page in this wiki. Read this first when answering a query — drill into the linked pages rather than searching raw sources. Updated on every ingest. See `CLAUDE.md` for conventions.

## Published

- **Quartz site (VI+EN)**: https://tctruc79.github.io/32ecm_wiki/ — sidebar now lists `concepts/` in **Lecture order** (see below), via the "Lecture N:" title prefix on each page (`CLAUDE.md` §3.1).
- **Mindmap Artifact (bilingual, Lecture-ordered, full-detail, self-test)**: https://claude.ai/code/artifact/ef2bb6aa-5e72-4d31-ba0a-eae635f1df2d — private by default; share from the artifact's page if needed. Tabs ordered Introduction → R basics → Lecture 1–13. Not synced automatically — regenerate by hand when `concepts/*.md` changes materially (see `CLAUDE.md` §5.3).

## Lectures (course order)

Canonical **Lecture 1–13** numbering, per the course syllabus — this is the primary reading/study order for this wiki. Distinct from the Course Outline's own "CO Topic" numbering (§ below), which is kept only as a secondary cross-reference for citations/slide filenames. See `CLAUDE.md` §3.1.

**Introduction** (not a numbered lecture) — [[concepts/econometrics-overview]]. Correlation vs. ceteris paribus vs. causality, the identification problem, PRE vs. SRE.

**R basics** (tooling, not a numbered lecture) — [[concepts/r-basics]]. Reference for the R commands used throughout the course.

### Lecture 1: Linear Regression Model

**Page:** [[concepts/linear-regression-model]] · CO Topic 1

**Summary:** This lesson introduces the basic concepts, estimation methods, and interpretation of results in linear regression models. It also covers hypothesis testing and how to interpret test results. The lecture further presents the assumptions underlying linear regression and the consequences of assumption violations.

**Key topics:** estimate linear regression model; interpret t-test results; interpret regression coefficients; interpret F-test results

**Practice assignment:** none numbered yet.

**References:**
- Peng, Y., Yang, J., Shen, J., & Gou, Q. (2025). Financial outreach, bank deposits, and economic growth. *Journal of Economic Behavior & Organization*, 171, 105036. https://doi.org/10.1016/j.jedc.2025.105036
- Su, Y., Huang, Q., Shu, Q., Wang, Y., & Qi, X. (2025). Mechanism of land trusteeship promoting farmers' collective action: A study based on social-ecological systems framework. *Journal of Rural Studies*, 116, 103622. https://doi.org/10.1016/j.jrurstud.2025.103622
- Yokying, P. (2025). Domestic and international migration, landownership, and rice farming in Cambodia. *Journal of Rural Studies*, 114, 103532. https://doi.org/10.1016/j.jrurstud.2024.103532

### Lecture 2: Functional forms

**Page:** [[concepts/functional-forms]] · CO Topic 2

**Summary:** Apply the linear regression model to estimate and interpret the results for common functional forms.

**Key topics:** Log-log functional form; Log-linear functional form; Linear-log functional form; Quadratic functional form; Functional form with interaction terms

**Practice assignment:** Assignment 1 — Linear Regression Model with functional forms.

**References:**
- Yang, F., & Zhan, J. (2025). Economic impact of cooperative management behavior on citrus production performance. *Finance Research Letters*, 107042. https://doi.org/10.1016/j.frl.2025.107042
- Xia, H., Li, C., Zhou, D., Zhang, Y., & Xu, J. (2020). Peasant households' land use decision-making analysis using social network analysis: A case of Tantou Village, China. *Journal of Rural Studies*, 80, 452-468. https://doi.org/10.1016/j.jrurstud.2020.07.004
- Gonzales, J. T. (2023). Implications of AI innovation on economic growth: A panel data study. *Journal of Economic Structures*, 12(1), 13. https://doi.org/10.1186/s40008-023-00307-w

### Lecture 3: Multicollinearity

**Page:** [[concepts/multicollinearity]] · CO Topic 3

**Summary:** Multicollinearity arises when explanatory variables in the dataset are correlated with each other, which inflates the variance of the regression coefficients. This topic explores the causes, consequences, and methods for detecting and addressing multicollinearity.

**Key topics:** Definition and causes; Indicators of multicollinearity; Variance Inflation Factor (VIF); Methods for addressing multicollinearity

**Practice assignment:** Assignment 2 — Multicollinearity.

**References:**
- Babina, T., Fedyk, A., He, A., & Hodson, J. (2024). Artificial intelligence, firm growth, and product innovation. *Journal of Financial Economics*, 151, 103745. https://doi.org/10.1016/j.jfineco.2023.103745
- Hoang, T. X., Pham, C. S., & Ulubaşoğlu, M. A. (2014). Non-farm activity, household expenditure, and poverty reduction in rural Vietnam: 2002-2008. *World Development*, 64, 554-568. https://doi.org/10.1016/j.worlddev.2014.06.027
- Xiaoxu, X., Qiangmin, X., & Weihao, S. (2024). Impact of urban compactness on carbon emission in Chinese cities: From moderating effects of industrial diversity and job-housing imbalances. *Land Use Policy*, 143, 107213. https://doi.org/10.1016/j.landusepol.2024.107213

### Lecture 4: Heteroskedasticity

**Page:** [[concepts/heteroskedasticity]] · CO Topic 4

**Summary:** Heteroskedasticity arises when the variance of the error terms is not constant across observations, leading to biased standard errors. This topic examines the causes, consequences, and methods for detecting and addressing heteroskedasticity.

**Key topics:** Definition and causes; Heteroskedasticity tests: BP/White test; Addressing heteroskedasticity: robust standard errors; Hypothesis testing with robust standard errors

**Practice assignment:** Assignment 3 — Heteroskedasticity.

**References:**
- Li, W., & He, W. (2024). Revenue-increasing effect of rural e-commerce: A perspective of farmers' market integration and employment growth. *Economic Analysis and Policy*, 81, 482-493. https://doi.org/10.1016/j.eap.2023.12.015
- Zhou, Y., & Shi, X. (2025). How Does Digital Technology Adoption Affect Corporate Employment? Evidence from China. *Economic Modelling*, 107045. https://doi.org/10.1016/j.econmod.2025.107045
- Tang, Y., Sun, Y., & He, Z. (2025). Air pollution and firms' robot adoption: Evidence from China. *Economic Modelling*, 143, 106957. https://doi.org/10.1016/j.econmod.2024.106957

### Lecture 5: Endogeneity and Instrumental Variable Regression

**Page:** [[concepts/endogeneity-iv-regression]] · CO Topic 5

**Summary:** Endogeneity is a common issue that leads to biased estimates in linear regression models. This topic introduces the causes of endogeneity, its consequences, and the methods used to address it.

**Key topics:** Instrumental variable regression: 2SLS, LIML, IV-GMM; Underidentification, Weak instruments; Robust inference under weak instruments; Overidentifying restrictions; Endogeneity test

**Practice assignment:** Assignment 4 — Endogeneity and Instrumental Variable Regression.

**References:**
- Gonzales, J. T. (2023). Implications of AI innovation on economic growth: A panel data study. *Journal of Economic Structures*, 12(1), 13. https://doi.org/10.1186/s40008-023-00307-w
- Acerenza, S., Gandelman, N., & Misail, D. (2025). Neighborhood impacts on human capital accumulation of adolescents and young adults in Montevideo. *Regional Science and Urban Economics*, 111, 104085. https://doi.org/10.1016/j.regsciurbeco.2025.104085
- Chen, Y., & Lyu, Y. (2025). Grandchild care and grandparents' labor supply. *Economic Modelling*, 143, 106936. https://doi.org/10.1016/j.econmod.2024.106936

### Lecture 6: Panel data models with variance structures

**Page:** [[concepts/fixed-random-effects-model]] · CO Topic 6 & 12

**Summary:** This lecture extends the basic panel data framework beyond FEM and REM by addressing critical issues related to the structure of the error term. In particular, it focuses on serial correlation and cross-sectional dependence, which, if ignored, may result in inefficient or inconsistent parameter estimates. Students will explore how these forms of heteroskedasticity and correlation arise in panel data, how to detect them, and which estimation techniques or model adjustments can correct for these violations.

**Key topics:** serial correlation; cross-sectional dependence; heterogeneity bias; panel-corrected SE; GLS estimators; FE and RE estimates with variance structures

**Practice assignment:** Assignment 5 — Panel data models with variance structures.

**References:**
- Yang, Z., Jia, P., Liu, W., & Yin, H. (2017). Car ownership and urban development in Chinese cities: A panel data analysis. *Journal of Transport Geography*, 58, 127-134. https://doi.org/10.1016/j.jtrangeo.2016.11.013
- González, E. S. M., & Soler-Vaya, F. (2024). Depopulation determinants of small rural municipalities in the Valencia Region (Spain). *Journal of Rural Studies*, 110, 103369. https://doi.org/10.1016/j.jrurstud.2024.103369
- de Haan, J., Pleninger, R., & Sturm, J. E. (2022). Does financial development reduce the poverty gap? *Social Indicators Research*, 161(1), 1-27. https://doi.org/10.1007/s11205-021-02705-8

### Lecture 7: Instrumental Variable Regression for Panel data

**Page:** [[concepts/iv-regression-panel-data]] · CO Topic 13

**Summary:** This lecture explores IV regression techniques for panel data, addressing the challenges of endogeneity that commonly arise in economic models. The lecture introduces IV-based estimation under different panel structures, including Fixed Effects (FE), Random Effects (RE), Between Estimator (BE), and First Differences (FD). Special attention is given to the role of covariance structures and efficiency considerations when using alternative IV estimators such as Two-Stage Least Squares (2SLS), Limited Information Maximum Likelihood (LIML), Generalized Method of Moments (GMM), and Continuously Updated Estimator (CUE). Diagnostic tests for instrument validity and specification are also covered.

**Key topics:** Panel data models with endogenous regressors; RE IV regression; FE-IV estimator, BE estimator, FD estimator; alternative estimation methods: 2SLS, LIML, GMM, CUE-GMM; test for weak instruments, endogeneity, and overidentifying restrictions

**Practice assignment:** Assignment 6 — Instrumental Variable Regression for Panel data.

**References:**
- Gonzales, J. T. (2023). Implications of AI innovation on economic growth: A panel data study. *Journal of Economic Structures*, 12(1), 13. https://doi.org/10.1186/s40008-023-00307-w
- Zheng, M., & Wong, C. Y. (2024). The impact of digital economy on renewable energy development in China. *Innovation and Green Development*, 3(1), 100094. https://doi.org/10.1016/j.igd.2024.100094
- Siddiki, J., & Bala-Keffi, L. R. (2024). Revisiting the relation between financial inclusion and economic growth: A global analysis using panel threshold regression. *Economic Modelling*, 135, 106707. https://doi.org/10.1016/j.econmod.2024.106707

### Lecture 8: Dynamic panel data models

**Page:** [[concepts/dynamic-panel-data-models]] · CO Topic 14

**Summary:** This lecture introduces dynamic panel data models, which incorporate lagged dependent variables as regressors to capture adjustment processes, persistence, and dynamic behavior in economic relationships. Traditional panel estimators such as Fixed Effects and Random Effects become biased and inconsistent in this context due to endogeneity of the lagged terms. The lecture presents estimation techniques specifically designed for dynamic panels, including the Arellano-Bond difference GMM and Arellano-Bover/Blundell-Bond system GMM estimators. Emphasis is placed on the underlying assumptions, instrument validity, and diagnostic testing to ensure robust inference in short time series and large cross-sectional datasets.

**Key topics:** difference GMM; system GMM; Arellano-Bond estimator; Arellano-Bover estimator; Blundell-Bond estimator

**Practice assignments:**
- Assignment 7 — Dynamic panel data models: Anderson-Hsiao estimator.
- Assignment 8 — Dynamic panel data models: Difference GMM.
- Assignment 9 — Dynamic panel data models: System GMM.

### Lecture 9: Binary Response Model: Logit/Probit

**Page:** [[concepts/binary-response-models]] · CO Topic 7

**Summary:** This topic introduces applications of models for binary dependent variables, along with hypothesis testing, forecasting steps, and post-estimation analysis.

**Key topics:** Linear Probability Model (LPM); Logit model; Probit model; Hypothesis testing: LR/Wald test; Probability prediction; Calculation and interpretation of marginal effects

**Practice assignment:** Assignment 10 — Binary Response Model: Logit/Probit.

**References:**
- Wagner, J., Bühner, C., Gölz, S., Trommsdorff, M., & Jürkenbeck, K. (2024). Factors influencing the willingness to use agrivoltaics: A quantitative study among German farmers. *Applied Energy*, 361, 122934. https://doi.org/10.1016/j.apenergy.2024.122934
- Alfano, V., De Simone, E., D'Uva, M., & Gaeta, G. L. (2022). Exploring motivations behind the introduction of tourist accommodation taxes: The case of the Marche region in Italy. *Land Use Policy*, 113, 105903. https://doi.org/10.1016/j.landusepol.2021.105903
- Mahn, D., Best, R., Wang, C., & Abiona, O. (2024). What drives solar energy adoption in developing countries? Evidence from household surveys across countries. *Energy Economics*, 138, 107815. https://doi.org/10.1016/j.eneco.2024.107815

### Lecture 10: Multinomial Logit Model (MNL)

**Page:** [[concepts/multinomial-logit-model]] · CO Topic 8

**Summary:** The Multinomial Logit (MNL) model is used for situations where the dependent variable represents discrete choices or classifications. The MNL model helps analyze the factors influencing the probability of choosing each alternative.

**Key topics:** Categorical dependent variable; Multinomial Logit model and estimation method; Hypothesis testing: LR/Wald test; Probability prediction; Calculation and interpretation of marginal effects

**Practice assignment:** none numbered yet.

**References:**
- Alem, Y., Beyene, A. D., Köhlin, G., & Mekonnen, A. (2016). Modeling household cooking fuel choice: A panel multinomial logit approach. *Energy Economics*, 59, 129-137. https://doi.org/10.1016/j.eneco.2016.06.025
- Mostofi, H. (2022). The frequency use and the modal shift to ICT-based mobility services. *Resources, Environment and Sustainability*, 9. https://doi.org/10.1016/j.resenv.2022.100076
- Fikire, A. H. (2021). Determinants of urban housing choice in Debre Berhan Town, North Shewa zone, Amhara Region, Ethiopia. *Cogent Economics & Finance*, 9(1). https://doi.org/10.1080/23322039.2021.1885196

### Lecture 11: Ordered Logit/Probit Models

**Page:** [[concepts/ordinal-response-models]] · CO Topic 9

**Summary:** The Ordered Logit/Probit models are designed for ordinal dependent variables, such as levels of agreement with a statement or categories like good, fair, or poor health status. These models help analyze how changes in explanatory variables affect the probabilities of each ordered outcome.

**Key topics:** Ordinal dependent variable; Ordered Logit/Probit model and estimation method; Hypothesis testing: LR/Wald test; Probability prediction; Calculation and interpretation of marginal effects

**Practice assignment:** none numbered yet.

**References:**
- Kolog, J. D., Asem, F. E., & Mensah-Bonsu, A. (2023). The state of food security and its determinants in Ghana: an ordered probit analysis of the household hunger scale and household food insecurity access scale. *Scientific African*, 19, e01579. https://doi.org/10.1016/j.sciaf.2023.e01579
- Chen, F., Yu, D., & Sun, Z. (2023). Investigating the associations of consumer financial knowledge and financial behaviors of credit card use. *Heliyon*, 9(1), E12713. https://doi.org/10.1016/j.heliyon.2022.e12713
- Ramachandran, R., Sudhir, S., & Unnithan, A. B. (2021). Exploring the relationship between emotionality and product star ratings in online reviews. *IIMB Management Review*, 33(4), 299-308. https://doi.org/10.1016/j.iimb.2021.12.002

### Lecture 12: Count data models: Poisson and Negative Binomial

**Page:** [[concepts/count-data-models]] · CO Topic 10

**Summary:** The Poisson and Negative Binomial models are used for dependent variables in the form of count data—non-negative integers. These models describe how changes in explanatory variables affect both the expected value of the dependent variable (the count) and the probability distribution of each possible count value.

**Key topics:** Count dependent variable; Poisson model and estimation method; Negative Binomial model and estimation method; Hypothesis testing: LR/Wald test; Probability prediction; Calculation and interpretation of marginal effects

**Practice assignment:** none numbered yet.

**References:**
- Meredith, N. R., Macy, A., & Meredith, A. (2022). Income elasticity of demand for tanning bed usage: evidence from survey data. *Journal of Applied Economics*, 25(1), 1156-1181. https://doi.org/10.1080/15140326.2022.2110640
- Hynes, S., O'Reilly, P., & Corless, R. (2015). An on-site versus a household survey approach to modelling the demand for recreational angling: Do welfare estimates differ? *Ecosystem Services*, 16, 136-145. https://doi.org/10.1016/j.ecoser.2015.10.013
- Xu, M., Ye, Q., Wang, X., & Wang, M. (2017). Assessing influence of online reputation on sales using a zero-inflated negative binomial model. *Procedia Computer Science*, 122, 1108-1113. https://doi.org/10.1016/j.procs.2017.11.480

### Lecture 13: Tobit model

**Page:** [[concepts/censored-regression-tobit]] · CO Topic 11

**Summary:** The Tobit model is designed for situations where the dependent variable is censored, and applying a linear regression model in such cases would yield biased results.

**Key topics:** Censored dependent variable; Tobit model and estimation method; Interpretation of regression coefficients; Hypothesis testing: LR/Wald test; Calculation and interpretation of marginal effects

**Practice assignment:** none numbered yet.

**References:**
- Liu, H., Wahl, T. I., Seale, J. L., & Bai, J. (2015). Household composition, income, and food-away-from-home expenditure in urban China. *Food Policy*, 51, 97-103. https://doi.org/10.1016/j.foodpol.2014.12.011
- Basnet, H. C., & Donou-Adonsou, F. (2016). Internet, consumer spending, and credit card balance: Evidence from US consumers. *Review of Financial Economics*, 30, 11-22. https://doi.org/10.1016/j.rfe.2016.01.002
- Jiang, H., Livingston, M., Room, R., & Callinan, S. (2016). Price elasticity of on- and off-premises demand for alcoholic drinks: A Tobit analysis. *Drug and Alcohol Dependence*, 163, 222-228. https://doi.org/10.1016/j.drugalcdep.2016.04.026

## Course map (CO Topic numbering — secondary cross-reference, see CLAUDE.md §3 vs §3.1)

| # | Topic | Slide file(s) | Concept page | Status |
|---|---|---|---|---|
| 0 | Introduction | VNP2026-intro.pdf | [[concepts/econometrics-overview]] | ✅ ingested |
| — | R basics (tooling) | slides-0-iu.pdf | [[concepts/r-basics]] | ✅ ingested |
| 1 | Linear regression model | slides-1-iu.pdf | [[concepts/linear-regression-model]] | ✅ ingested |
| 2 | Functional forms | slides-2-iu.pdf | [[concepts/functional-forms]] | ✅ ingested |
| 3 | Multicollinearity | slides-3-iu.pdf | [[concepts/multicollinearity]] | ✅ ingested |
| 4 | Heteroskedasticity | slides-4-iu.pdf | [[concepts/heteroskedasticity]] | ✅ ingested |
| 5 | Endogeneity and IV regression | slides-5-iu.pdf, slides-16-iu.pdf | [[concepts/endogeneity-iv-regression]] | ✅ ingested |
| 6 | Fixed and Random Effects Model | slides-6-iu.pdf | [[concepts/fixed-random-effects-model]] | ✅ ingested |
| 7 | Binary response models | slides-7-iu.pdf, slides-310-iu.pdf | [[concepts/binary-response-models]] | ✅ ingested |
| 8 | Multinomial logit model | slides-8-iu.pdf | [[concepts/multinomial-logit-model]] | ✅ ingested |
| 9 | Ordinal response models | slides-9-iu.pdf | [[concepts/ordinal-response-models]] | ✅ ingested |
| 10 | Count data models | slides-10-iu.pdf | [[concepts/count-data-models]] | ✅ ingested |
| 11 | Censored and truncated regressions | slides-11-iu.pdf | [[concepts/censored-regression-tobit]] | ✅ ingested |
| 12 | Panel data with variance structures | slides-13-iu.pdf | [[concepts/fixed-random-effects-model]] | ✅ ingested |
| 13 | IV regression for panel data | slides-14-iu.pdf | [[concepts/iv-regression-panel-data]] | ✅ ingested |
| 14 | Dynamic panel data models | slides-15-iu.pdf | [[concepts/dynamic-panel-data-models]] | ✅ ingested |

Full mapping notes (why file numbers ≠ topic numbers) are in `CLAUDE.md` §3. Lecture-order mapping (the numbering used above and on the live site) is in `CLAUDE.md` §3.1.

## Sources

| Page | Raw file | Topic | Status |
|---|---|---|---|
| [[sources/2026-course-outline]] | VNP2026-CO.pdf | (meta) | current |
| [[sources/intro-to-econometrics]] | VNP2026-intro.pdf | 0 | current |
| [[sources/slides-1-linear-regression-model]] | slides-1-iu.pdf | 1 | current |
| [[sources/slides-2-functional-forms]] | slides-2-iu.pdf | 2 | current |
| [[sources/slides-3-multicollinearity]] | slides-3-iu.pdf | 3 | current |
| [[sources/slides-4-heteroskedasticity]] | slides-4-iu.pdf | 4 | current |
| [[sources/slides-5-endogeneity-iv-regression]] | slides-5-iu.pdf | 5 | superseded |
| [[sources/slides-16-endogeneity-iv-regression-extended]] | slides-16-iu.pdf | 5 | current |
| [[sources/slides-6-fixed-random-effects]] | slides-6-iu.pdf | 6 | current |
| [[sources/slides-7-binary-response-models]] | slides-7-iu.pdf | 7 | current |
| [[sources/slides-310-binary-response-models-logit-probit]] | slides-310-iu.pdf | 7 | current |
| [[sources/slides-8-multinomial-logit-model]] | slides-8-iu.pdf | 8 | current |
| [[sources/slides-9-ordinal-response-models]] | slides-9-iu.pdf | 9 | current |
| [[sources/slides-10-count-data-models]] | slides-10-iu.pdf | 10 | current |
| [[sources/slides-11-censored-regression-tobit]] | slides-11-iu.pdf | 11 | current |
| [[sources/slides-13-panel-data-variance-structures]] | slides-13-iu.pdf | 12 | current |
| [[sources/slides-14-iv-regression-panel-data]] | slides-14-iu.pdf | 13 | current |
| [[sources/slides-15-dynamic-panel-data-models]] | slides-15-iu.pdf | 14 | current |
| [[sources/slides-0-r-basics]] | slides-0-iu.pdf | (tooling) | current |

## Concepts

| Lecture | Page | Summary | Status |
|---|---|---|---|
| — | [[concepts/econometrics-overview]] | Correlation vs. ceteris paribus vs. causality; identification problem; PRE vs SRE | mature |
| 1 | [[concepts/linear-regression-model]] | OLS, 5 giả định (A1-A5), diễn giải hệ số, t-test, F-test, R² | mature |
| 2 | [[concepts/functional-forms]] | Linear/log-log/log-lin/lin-log/quadratic/interaction, elasticity | mature |
| 3 | [[concepts/multicollinearity]] | VIF, phát hiện, giải pháp | mature |
| 4 | [[concepts/heteroskedasticity]] | BP/White test, robust SE, Wald F-test | mature |
| 5 | [[concepts/endogeneity-iv-regression]] | 2SLS, LIML/Fuller, GMM, weak-IV tests, Sargan/Hansen, Wu-Hausman | mature |
| 6 | [[concepts/fixed-random-effects-model]] | Pooled OLS, GLS/FGLS, FE/RE, A3a/A3b+A4a/b/c, Hausman test, 5 loại SE | mature |
| 7 | [[concepts/iv-regression-panel-data]] | FD-IV, FE-IV, LIML/Fuller/GMM cho panel, CD-F/KP-F | mature |
| 8 | [[concepts/dynamic-panel-data-models]] | Nickell bias, Anderson-Hsiao, Difference/System GMM, AR(1)/AR(2) test | mature |
| — | [[concepts/r-basics]] | Tham khảo lệnh R cơ bản (không phải nội dung econometrics) | mature |
| 9 | [[concepts/binary-response-models]] | LPM, Logit, Probit, LR/Wald test, marginal effects | mature |
| 10 | [[concepts/multinomial-logit-model]] | MNL, log-odds vs base category, McFadden R² | mature |
| 11 | [[concepts/ordinal-response-models]] | Latent variable, cutpoints, ordered logit/probit, Brant test | mature |
| 12 | [[concepts/count-data-models]] | Poisson, over/underdispersion, Negative Binomial, ZINB | mature |
| 13 | [[concepts/censored-regression-tobit]] | Censored vs truncated, Tobit, 3 loại prediction/ME | mature |

## People

| Page | Role |
|---|---|
| [[people/truong-dang-thuy]] | Instructor, UEH-VNP |
| [[people/hausman]] | Wu-Hausman test (endogeneity), Hausman test (FE vs RE) |
| [[people/arellano-bond]] | Anderson-Hsiao/Arellano-Bond/Arellano-Bover-Blundell-Bond — dynamic panel GMM |
| [[people/sargan]] | Sargan test — overidentifying restrictions (IV/GMM), homoskedastic |
| [[people/hansen]] | Hansen's J test — overidentifying restrictions, GMM framework, robust hetero |
| [[people/cragg-donald]] | Cragg-Donald F-statistic — weak-instrument test, homoskedastic |
| [[people/stock-yogo]] | Stock-Yogo critical values — ngưỡng đánh giá Cragg-Donald F |

## Synthesis

_(empty — populated as queries are answered and filed back)_
