---
title: "Lecture 7: Instrumental Variable Regression for Panel Data"
type: source
raw_file: "raw/SLIDES/slides-14-iu.pdf"
pages: 56
topic: 13
lecture: 7
status: current
ingested: 2026-07-29
concepts: ["[[concepts/iv-regression-panel-data]]"]
---

## Vai trò - <span class="en">Role</span>

Slide Topic 13 (file numbered 14). Áp dụng khung IV/2SLS/LIML/Fuller/GMM đã học ở Topic 5 ([[concepts/endogeneity-iv-regression]]) vào bối cảnh panel data — xử lý biến nội sinh **kèm theo** individual fixed effects. Lý thuyết trích xuất đầy đủ qua text; các trang minh họa bằng R output (mỗi loại SE cho FD-IV, FE-IV, LIML, Fuller) đều có ghi chú diễn giải bằng lời captured qua text.
<br><span class="en">Topic 13 slide deck (file numbered 14). Applies the IV/2SLS/LIML/Fuller/GMM framework from Topic 5 ([[concepts/endogeneity-iv-regression]]) to a panel-data setting — handling an endogenous regressor **together with** individual fixed effects. The theory extracted fully via text; the R-output illustration pages (each SE type for FD-IV, FE-IV, LIML, Fuller) all have prose annotations captured via text.</span>

## Ví dụ dữ liệu - <span class="en">Example data</span>

Cùng bộ dữ liệu 300 doanh nghiệp × 5 năm với Topic 12: `output`, `capital`, `labor`, và biến `training` (giờ đào tạo/lao động) được coi là **nội sinh**, dùng instrument `subeligible` (đủ điều kiện nhận trợ cấp đào tạo) và `localbudget` (ngân sách chính quyền địa phương cho đào tạo).
<br><span class="en">The same 300-firm × 5-year dataset as Topic 12: `output`, `capital`, `labor`, with `training` (training hours/worker) treated as **endogenous**, using instruments `subeligible` (eligible for a training subsidy) and `localbudget` (local government training budget).</span>

## Lưu ý về nội dung không được dạy - <span class="en">Note on content not taught</span>

CO liệt kê "**2SLS RE estimator**" và "**G2GLS estimator**" là các mục của Topic 13 — nhưng slide **nói rõ ràng**: "RE (Random Effects) IV regression (Generalized 2SLS, **not covered**)". Đây là gap được chính slide xác nhận minh bạch (khác các gap trước phải tự suy luận từ việc thiếu nội dung) — ghi nhận nguyên văn, không suy diễn thêm.
<br><span class="en">The CO lists "**2SLS RE estimator**" and "**G2GLS estimator**" as items under Topic 13 — but the slide **states explicitly**: "RE (Random Effects) IV regression (Generalized 2SLS, **not covered**)." This is a gap explicitly confirmed by the slide itself (unlike earlier gaps that had to be inferred from absence) — noted verbatim, no further inference.</span>

Toàn bộ nội dung đã tổng hợp vào `[[concepts/iv-regression-panel-data]]`.
<br><span class="en">All content has been synthesized into `[[concepts/iv-regression-panel-data]]`.</span>
