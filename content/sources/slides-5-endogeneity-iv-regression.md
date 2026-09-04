---
title: "Lecture 5: Endogeneity and Instrumental Variable Regression (basic)"
type: source
raw_file: "raw/SLIDES/slides-5-iu.pdf"
pages: 63
topic: 5
lecture: 5
status: superseded
ingested: 2026-07-29
concepts: ["[[concepts/endogeneity-iv-regression]]"]
---

## Vai trò - <span class="en">Role</span>

Slide Topic 5 (bản đầu) — vi phạm A3 (exogeneity) của [[concepts/linear-regression-model]]. Có bản mở rộng/tinh chỉnh hơn là `slides-16-iu.pdf` (xem `[[sources/slides-16-endogeneity-iv-regression-extended]]`) — đánh dấu `status: superseded` nhưng vẫn giữ lại vì là nguồn gốc thực tế đã ingest, theo CLAUDE.md §3.
<br><span class="en">Topic 5 slide deck (original version) — a violation of A3 (exogeneity) of [[concepts/linear-regression-model]]. A more refined/extended version exists, `slides-16-iu.pdf` (see `[[sources/slides-16-endogeneity-iv-regression-extended]]`) — marked `status: superseded` but kept because it is a real ingested source, per CLAUDE.md §3.</span>

## Ví dụ dữ liệu xuyên suốt - <span class="en">Running example dataset</span>

Khảo sát người lao động tại TP.HCM: `wage` (biến phụ thuộc), `schooling` (biến nội sinh — endogenous), `fatheredu`/`motheredu` (biến công cụ — instruments), cùng các biến kiểm soát `age`, `tenure`, `gender`, `origin`, `science`/`social`.
<br><span class="en">A survey of workers in Ho Chi Minh City: `wage` (dependent variable), `schooling` (endogenous variable), `fatheredu`/`motheredu` (instruments), plus control variables `age`, `tenure`, `gender`, `origin`, `science`/`social`.</span>

Nội dung kỹ thuật đầy đủ (định nghĩa endogeneity, 2SLS, LIML/Fuller, GMM, các kiểm định chẩn đoán) đã tổng hợp vào `[[concepts/endogeneity-iv-regression]]`.
<br><span class="en">The full technical content (the definition of endogeneity, 2SLS, LIML/Fuller, GMM, the diagnostic tests) has been synthesized into `[[concepts/endogeneity-iv-regression]]`.</span>
