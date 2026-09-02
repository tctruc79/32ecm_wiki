---
title: "The Linear Regression Model"
type: source
raw_file: "raw/SLIDES/slides-1-iu.pdf"
pages: 51
topic: 1
status: current
ingested: 2026-07-29
concepts: ["[[concepts/linear-regression-model]]"]
---

## Vai trò - <span class="en">Role</span>

Slide Topic 1 — nền tảng ước lượng của toàn khóa học: PRE/SRE, OLS, 5 giả định, diễn giải hệ số, t-test, F-test, R². Toàn bộ công thức trích xuất được từ text layer của PDF (không cần đọc ảnh trực quan) — các trang thưa nội dung trong bản gốc chỉ là slide chuyển mục (section divider), không chứa công thức bị ẩn.
<br><span class="en">Topic 1 slide deck — the estimation foundation of the whole course: PRE/SRE, OLS, the 5 assumptions, coefficient interpretation, t-test, F-test, R². All formulas were extracted from the PDF's text layer (no need for visual page reads) — the sparse-looking pages in the original are section-divider slides, not hidden formulas.</span>

## Ví dụ dữ liệu xuyên suốt - <span class="en">Running example dataset</span>

Bộ dữ liệu **"Forest coverage and storm damages"**: biến phụ thuộc `pdamages` (thiệt hại tài sản, nghìn USD); biến độc lập gồm `aforest` [causal] (diện tích rừng, ha), `dplan` [causal] (có kế hoạch ứng phó không), và các biến non-causal `cgdp`, `pdens`, `curban`, `cterrain` (lowland/highland/coastal). Bộ dữ liệu được thầy nói rõ là **đơn giản hóa cho mục đích học tập**, có thể bỏ sót biến quan trọng — không dùng để suy luận thực tế.
<br><span class="en">The **"Forest coverage and storm damages"** dataset: dependent variable `pdamages` (asset losses, thousand US$); independent variables `aforest` [causal] (forest area, ha), `dplan` [causal] (has a resilience plan or not), and the non-causal variables `cgdp`, `pdens`, `curban`, `cterrain` (lowland/highland/coastal). The professor explicitly notes the dataset is **simplified for learning purposes** and may omit important regressors — not for real-world inference.</span>

Toàn bộ nội dung đã tổng hợp vào `[[concepts/linear-regression-model]]`.
<br><span class="en">All content has been synthesized into `[[concepts/linear-regression-model]]`.</span>
