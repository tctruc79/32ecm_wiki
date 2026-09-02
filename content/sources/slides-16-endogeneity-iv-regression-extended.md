---
title: "Endogeneity and Instrumental Variable Regression (extended)"
type: source
raw_file: "raw/SLIDES/slides-16-iu.pdf"
pages: 70
topic: 5
status: current
ingested: 2026-07-29
concepts: ["[[concepts/endogeneity-iv-regression]]"]
---

## Vai trò - <span class="en">Role</span>

Bản mở rộng/tinh chỉnh của Topic 5, thay thế `slides-5-iu.pdf` (xem `[[sources/slides-5-endogeneity-iv-regression]]`) làm nguồn **canonical**. Cùng ví dụ dữ liệu (wage, schooling, fatheredu/motheredu) và cùng các công cụ kỹ thuật (2SLS, LIML/Fuller, GMM, Sargan/Hansen, Wu-Hausman), nhưng:
<br><span class="en">The refined/extended version of Topic 5, replacing `slides-5-iu.pdf` (see `[[sources/slides-5-endogeneity-iv-regression]]`) as the **canonical** source. Same example data (wage, schooling, fatheredu/motheredu) and the same technical tools (2SLS, LIML/Fuller, GMM, Sargan/Hansen, Wu-Hausman), but:</span>

- Sửa thuật ngữ chính xác hơn: OLS dưới endogeneity là **inconsistent** (bản slides-5 có chỗ ghi "biased", kém chính xác hơn).
  <br><span class="en">More precise terminology: OLS under endogeneity is **inconsistent** (the slides-5 version says "biased" in places, which is less precise).</span>
- Thêm hẳn mục mới **"Robust inference under weak instruments"**: Anderson-Rubin (AR) test và Stock-Wright (SW) LM test — các kiểm định hệ số vẫn hợp lệ ngay cả khi instrument yếu (miễn là không underidentified và instrument hợp lệ).
  <br><span class="en">Adds an entirely new section, **"Robust inference under weak instruments"**: the Anderson-Rubin (AR) test and Stock-Wright (SW) LM test — coefficient tests that stay valid even under weak instruments (as long as the model isn't underidentified and the instruments are valid).</span>
- Wu-Hausman statistic tính lại = 3.8 (so với 3.63 ở bản cũ) — chênh lệch do dùng `ivreg2r::ivreg2()` với robust VCV, ghi chú rõ trong slide rằng kết quả kiểm định phụ thuộc vào VCV được chọn.
  <br><span class="en">The recomputed Wu-Hausman statistic = 3.8 (vs. 3.63 in the older version) — the difference comes from using `ivreg2r::ivreg2()` with a robust VCV; the slide explicitly notes the test result depends on the VCV choice.</span>

Toàn bộ nội dung hợp nhất (bao gồm phần mới) đã tổng hợp vào `[[concepts/endogeneity-iv-regression]]`.
<br><span class="en">All merged content (including the new section) has been synthesized into `[[concepts/endogeneity-iv-regression]]`.</span>
