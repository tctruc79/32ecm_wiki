---
title: "Multinomial Logit Model"
type: source
raw_file: "raw/SLIDES/slides-8-iu.pdf"
pages: 42
topic: 8
status: current
ingested: 2026-07-29
concepts: ["[[concepts/multinomial-logit-model]]"]
---

## Vai trò - <span class="en">Role</span>

Slide Topic 8 — mở rộng [[concepts/binary-response-models]] sang biến phụ thuộc có **nhiều hơn 2 lựa chọn không thứ tự (nominal)**. Phần lý thuyết (định nghĩa, log-odds so với base category, công thức xác suất, log-likelihood) trích xuất đầy đủ qua text; phần ví dụ minh họa (trang ~15–42) là output R dạng ảnh, đã xác nhận trực quan riêng công thức **McFadden R²** (trang 37, dùng nhiều — xem concept page).
<br><span class="en">Topic 8 slide deck — extends [[concepts/binary-response-models]] to a dependent variable with **more than 2 unordered (nominal) choices**. The theory (definitions, log-odds vs. the base category, probability formula, log-likelihood) extracted fully via text; the illustrative example (pp. ~15–42) is R output as images — the **McFadden R²** formula (p. 37, heavily used — see the concept page) was separately visually verified.</span>

## Ví dụ dữ liệu - <span class="en">Example data</span>

VHLSS 2012 — lựa chọn nơi khám chữa bệnh (5 phạm trù: trạm y tế xã, bệnh viện công, bệnh viện tư, thầy lang, tự điều trị), giải thích bởi `insurance`, `income`, `female`, `age`, `edu`, `urban`.
<br><span class="en">VHLSS 2012 — choice of healthcare provider (5 categories: commune health station, public hospital, private hospital, traditional healer, self-treatment), explained by `insurance`, `income`, `female`, `age`, `edu`, `urban`.</span>

Toàn bộ nội dung đã tổng hợp vào `[[concepts/multinomial-logit-model]]`.
<br><span class="en">All content has been synthesized into `[[concepts/multinomial-logit-model]]`.</span>
