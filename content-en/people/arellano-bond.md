---
title: "Anderson-Hsiao / Arellano-Bond / Arellano-Bover-Blundell-Bond"
type: person
role: "GMM estimator lineage for dynamic panel data"
tags: [dynamic-panel, gmm, arellano-bond, blundell-bond]
---

A sequence of successive contributions solving the **Nickell bias** problem in dynamic panel models (see [[concepts/dynamic-panel-data-models]]):

- **Anderson & Hsiao (1981, 1982)** — first-difference + a single internal instrument ($y_{i,t-2}$ or $\Delta y_{i,t-2}$), just-identified.
- **Arellano & Bond (1991)** — extends this into **Difference GMM**, using multiple lags as instruments simultaneously, increasing efficiency.
- **Arellano & Bover (1995)** — proposes stacking the differenced equation and the levels equation into one system.
- **Blundell & Bond (1998)** — formalizes the moment conditions for **System GMM**, ensuring consistency (especially when $y$ is highly persistent).

All are cited in the Course Outline as the main readings for Topic 14, along with Roodman (2009, an `xtabond2` guide) and Windmeijer (2005, a two-step GMM variance correction).

## Appears in

- [[concepts/dynamic-panel-data-models]]
