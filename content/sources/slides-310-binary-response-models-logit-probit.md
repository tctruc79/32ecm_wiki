---
title: "Lecture 9: Binary Response Models: Logit and Probit (e-wallet example)"
type: source
raw_file: "raw/SLIDES/slides-310-iu.pdf"
pages: 39
topic: 7
lecture: 9
status: current
ingested: 2026-07-29
concepts: ["[[concepts/binary-response-models]]"]
---

## Vai trò - <span class="en">Role</span>

Bản song song của `slides-7-iu.pdf` (xem `[[sources/slides-7-binary-response-models]]`) — cùng cấu trúc lý thuyết (LPM → Logit → Probit → LR/Wald test → marginal effects → Logistic regression với odds ratio) nhưng dùng ví dụ dữ liệu khác. Không có nội dung lý thuyết mới so với slides-7 (đã so sánh cấu trúc mục lục của cả hai deck).
<br><span class="en">A parallel deck to `slides-7-iu.pdf` (see `[[sources/slides-7-binary-response-models]]`) — the same theoretical structure (LPM → Logit → Probit → LR/Wald test → marginal effects → logistic regression with odds ratio) but different example data. No new theoretical content compared to slides-7 (the table-of-contents structure of both decks was compared).</span>

## Ví dụ dữ liệu - <span class="en">Example data</span>

Quyết định sử dụng ví điện tử (`ewallet`, 1 = có dùng): `income` (thu nhập khả dụng hàng tháng, triệu VND), `age`, `schooling`, `male`, `risklover` (tự nhận là người thích rủi ro), `freq` (tần suất mua online: monthly/weekly/daily → sinh biến dummy `weekly`, `daily`).
<br><span class="en">The decision to use an e-wallet (`ewallet`, 1 = uses it): `income` (monthly disposable income, million VND), `age`, `schooling`, `male`, `risklover` (self-identified risk lover), `freq` (online purchase frequency: monthly/weekly/daily → generates dummy variables `weekly`, `daily`).</span>

Toàn bộ nội dung lý thuyết đã hợp nhất vào `[[concepts/binary-response-models]]` cùng với slides-7.
<br><span class="en">All theoretical content has been merged into `[[concepts/binary-response-models]]` together with slides-7.</span>
