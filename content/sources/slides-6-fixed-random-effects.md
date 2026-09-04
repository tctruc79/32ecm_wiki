---
title: "Lecture 6: Panel Data Models — Fixed and Random Effects (basic)"
type: source
raw_file: "raw/SLIDES/slides-6-iu.pdf"
pages: 38
topic: 6
lecture: 6
status: current
ingested: 2026-07-29
concepts: ["[[concepts/fixed-random-effects-model]]"]
---

## Vai trò - <span class="en">Role</span>

Slide Topic 6 — mở đầu phần Panel Data Models, mở rộng [[concepts/linear-regression-model]] sang dữ liệu có cả chiều đơn vị (unit) lẫn chiều thời gian. Bản mở rộng/chi tiết hơn của panel data nói chung là `slides-13-iu.pdf` (Topic 12 — xem `[[sources/slides-13-panel-data-variance-structures]]`).
<br><span class="en">Topic 6 slide deck — opens the Panel Data Models section, extending [[concepts/linear-regression-model]] to data with both a unit and a time dimension. A more extended/detailed panel-data deck is `slides-13-iu.pdf` (Topic 12 — see `[[sources/slides-13-panel-data-variance-structures]]`).</span>

## Ví dụ dữ liệu - <span class="en">Example data</span>

Dữ liệu cấp tỉnh Việt Nam 2007–2011 (58 tỉnh × 5 năm): `rgdp` (GDP thực), `labfo` (lực lượng lao động), `rinvest` (đầu tư), `pci` (chỉ số năng lực cạnh tranh cấp tỉnh). Mô hình: $\ln(rgdp)_{it}=\alpha+\beta X_{it}+u$ với $X$ gồm $\ln(labfo)$, $\ln(rinvest)$, `pci`.
<br><span class="en">Vietnamese province-level data, 2007–2011 (58 provinces × 5 years): `rgdp` (real GDP), `labfo` (labor force), `rinvest` (investment), `pci` (provincial competitiveness index). Model: $\ln(rgdp)_{it}=\alpha+\beta X_{it}+u$ with $X$ comprising $\ln(labfo)$, $\ln(rinvest)$, `pci`.</span>

## Lưu ý về nội dung thiếu - <span class="en">Note on missing content</span>

Slide đầu tiên liệt kê outline 6 mục, mục cuối là **"Between group estimator"** — nhưng nội dung thực tế của deck (38 trang) **dừng lại ở "Notes on Hausman test"**, không có phần between-group estimator nào được trình bày. Đây là một trường hợp tương tự "16 vs 15 topics" ở Course Outline — outline hứa nhiều hơn nội dung thực tế truyền tải. Ghi nhận, không suy đoán nội dung.
<br><span class="en">The first slide lists a 6-item outline whose last item is **"Between group estimator"** — but the deck's actual content (38 pages) **stops at "Notes on Hausman test"**, with no between-group estimator section ever presented. This mirrors the "16 vs. 15 topics" case in the Course Outline — the outline promises more than the actual content delivers. Noted, not guessed at.</span>

Nhiều trang là output R/Stata dạng ảnh (SUMMARY STATISTICS, POOLED OLS IN R, FE/RE với robust/clustered SE) không trích xuất được qua text nhưng đã xác nhận trực quan phần "Hausman test in R" và "Random vs Fixed Effects" (trang 33–38) để đảm bảo không bỏ sót nội dung công thức.
<br><span class="en">Many pages are R/Stata output images (SUMMARY STATISTICS, POOLED OLS IN R, FE/RE with robust/clustered SE) not extractable via text, but the "Hausman test in R" and "Random vs Fixed Effects" pages (pp. 33–38) were visually verified to make sure no formula content was missed.</span>

Toàn bộ nội dung khái niệm đã tổng hợp vào `[[concepts/fixed-random-effects-model]]`.
<br><span class="en">All conceptual content has been synthesized into `[[concepts/fixed-random-effects-model]]`.</span>
