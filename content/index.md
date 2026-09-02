---
title: "Econometrics Wiki — Index"
type: index
---

# Index — Econometrics Wiki (GS Trương Đăng Thụy)

Catalog of every page in this wiki. Read this first when answering a query — drill into the linked pages rather than searching raw sources. Updated on every ingest. See `CLAUDE.md` for conventions.

## Published

- **Quartz site (VI+EN)**: https://tctruc79.github.io/32ecm_wiki/
- **Mindmap Artifact (bilingual, 14 topics, self-test)**: https://claude.ai/code/artifact/ef2bb6aa-5e72-4d31-ba0a-eae635f1df2d — private by default; share from the artifact's page if needed. Not synced automatically — regenerate by hand when concepts/*.md changes materially (see `CLAUDE.md` §5.2).

## Course map (canonical topic numbering, per Course Outline)

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

Full mapping notes (why file numbers ≠ topic numbers) are in `CLAUDE.md` §3.

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

| Page | Summary | Status |
|---|---|---|
| [[concepts/econometrics-overview]] | Correlation vs. ceteris paribus vs. causality; identification problem; PRE vs SRE | mature |
| [[concepts/linear-regression-model]] | OLS, 5 giả định (A1-A5), diễn giải hệ số, t-test, F-test, R² | mature |
| [[concepts/functional-forms]] | Linear/log-log/log-lin/lin-log/quadratic/interaction, elasticity | mature |
| [[concepts/multicollinearity]] | VIF, phát hiện, giải pháp | mature |
| [[concepts/heteroskedasticity]] | BP/White test, robust SE, Wald F-test | mature |
| [[concepts/endogeneity-iv-regression]] | 2SLS, LIML/Fuller, GMM, weak-IV tests, Sargan/Hansen, Wu-Hausman | mature |
| [[concepts/fixed-random-effects-model]] | Pooled OLS, GLS/FGLS, FE/RE, A3a/A3b+A4a/b/c, Hausman test, 5 loại SE | mature |
| [[concepts/iv-regression-panel-data]] | FD-IV, FE-IV, LIML/Fuller/GMM cho panel, CD-F/KP-F | mature |
| [[concepts/dynamic-panel-data-models]] | Nickell bias, Anderson-Hsiao, Difference/System GMM, AR(1)/AR(2) test | mature |
| [[concepts/r-basics]] | Tham khảo lệnh R cơ bản (không phải nội dung econometrics) | mature |
| [[concepts/binary-response-models]] | LPM, Logit, Probit, LR/Wald test, marginal effects | mature |
| [[concepts/multinomial-logit-model]] | MNL, log-odds vs base category, McFadden R² | mature |
| [[concepts/ordinal-response-models]] | Latent variable, cutpoints, ordered logit/probit, Brant test | mature |
| [[concepts/count-data-models]] | Poisson, over/underdispersion, Negative Binomial, ZINB | mature |
| [[concepts/censored-regression-tobit]] | Censored vs truncated, Tobit, 3 loại prediction/ME | mature |

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
