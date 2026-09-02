---
title: "Binary Response Models (vaccine example)"
type: source
raw_file: "raw/SLIDES/slides-7-iu.pdf"
pages: 48
topic: 7
status: current
ingested: 2026-07-29
concepts: ["[[concepts/binary-response-models]]"]
---

## Vai trò - <span class="en">Role</span>

Slide Topic 7 — mở đầu Part 2 (Models for Limited Dependent Variables), khi biến phụ thuộc là nhị phân. Có bản song song `slides-310-iu.pdf` dùng ví dụ dữ liệu khác (xem `[[sources/slides-310-binary-response-models-logit-probit]]`) nhưng **cùng nội dung lý thuyết** — không phải bản cũ/mới như cặp Topic 5, mà là hai bộ ví dụ minh họa cho cùng một bài giảng.
<br><span class="en">Topic 7 slide deck — opens Part 2 (Models for Limited Dependent Variables), where the dependent variable is binary. A parallel deck, `slides-310-iu.pdf`, uses different example data (see `[[sources/slides-310-binary-response-models-logit-probit]]`) but **the same theoretical content** — not an old/new pair like Topic 5, but two illustrative datasets for the same lecture.</span>

## Ví dụ dữ liệu - <span class="en">Example data</span>

Khảo sát quyết định tiêm vaccine COVID-19 (giả định) của 377 người tại TP.HCM năm 2020 (nguồn: EEPSEA). Biến phụ thuộc `dself` (1 = quyết định tiêm); biến độc lập gồm `efficacy80`, `duration3`, `priceUS`, `pbenefit`, `hhincomeUS`, `hhsize`, `age`, `edu`, `male`, `risk`.
<br><span class="en">A survey of the (hypothetical) COVID-19 vaccination decision of 377 people in Ho Chi Minh City, 2020 (source: EEPSEA). Dependent variable `dself` (1 = decided to vaccinate); independent variables `efficacy80`, `duration3`, `priceUS`, `pbenefit`, `hhincomeUS`, `hhsize`, `age`, `edu`, `male`, `risk`.</span>

Đã xác nhận trực quan các trang kết quả R (LR test, Wald test, marginal effects) để lấy số liệu thực tế minh họa — các số này đã đưa vào `[[concepts/binary-response-models]]`.
<br><span class="en">The R-results pages (LR test, Wald test, marginal effects) were visually verified to pull real illustrative numbers — those numbers were carried into `[[concepts/binary-response-models]]`.</span>
