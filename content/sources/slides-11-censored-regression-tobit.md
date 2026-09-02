---
title: "Censored Regression: The Tobit Model"
type: source
raw_file: "raw/SLIDES/slides-11-iu.pdf"
pages: 35
topic: 11
status: current
ingested: 2026-07-29
concepts: ["[[concepts/censored-regression-tobit]]"]
---

## Vai trò - <span class="en">Role</span>

Slide Topic 11 — biến phụ thuộc bị **censored** (giá trị thật tồn tại nhưng bị "kẹp" ở một ngưỡng khi ghi nhận). Toàn bộ công thức (mô hình, xác suất, marginal effects, log-likelihood) trích xuất đầy đủ qua text.
<br><span class="en">Topic 11 slide deck — the dependent variable is **censored** (the true value exists but gets "clamped" at a threshold when recorded). All formulas (the model, probability, marginal effects, log-likelihood) extracted fully via text.</span>

## Ví dụ dữ liệu - <span class="en">Example data</span>

Số dư nợ thẻ tín dụng (`balance`, USD — censored tại 0, vì người không dùng thẻ ghi nhận balance=0), giải thích bởi lãi suất (`interest`), `age`, `male`, `edu`.
<br><span class="en">Credit card balance (`balance`, US$ — censored at 0, since non-cardholders are recorded with balance=0), explained by the interest rate (`interest`), `age`, `male`, `edu`.</span>

## Lưu ý về nội dung thiếu so với Course Outline - <span class="en">Note on content missing relative to the Course Outline</span>

CO liệt kê "the Heckman selection model (if time allowed)" là một mục của Topic 11 — nhưng **không xuất hiện** trong 35 trang của deck này. Đây có thể do giới hạn thời gian giảng dạy thực tế đúng như CO đã dự phòng ("if time allowed"). Ghi nhận, không suy diễn nội dung Heckman model.
<br><span class="en">The CO lists "the Heckman selection model (if time allowed)" as an item under Topic 11 — but it **does not appear** anywhere in this deck's 35 pages. This may simply reflect the time constraint the CO itself hedged for ("if time allowed"). Noted, no attempt to reconstruct Heckman-model content.</span>

Toàn bộ nội dung đã tổng hợp vào `[[concepts/censored-regression-tobit]]`.
<br><span class="en">All content has been synthesized into `[[concepts/censored-regression-tobit]]`.</span>
