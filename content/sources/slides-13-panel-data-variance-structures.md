---
title: "Lecture 6: Panel Data Models with Covariance Structure"
type: source
raw_file: "raw/SLIDES/slides-13-iu.pdf"
pages: 61
topic: 12
lecture: 6
status: current
ingested: 2026-07-29
concepts: ["[[concepts/fixed-random-effects-model]]"]
---

## Vai trò - <span class="en">Role</span>

Slide Topic 12 (file numbered 13 — xem `CLAUDE.md` §3 cho lý do lệch số). Bản mở rộng của Topic 6 (`slides-6-iu.pdf`), tựa cuối slide ghi rõ "PANEL DATA MODELS WITH COVARIANCE STRUCTURE" — xác nhận đây đúng là nội dung "Panel data models with variance structures" trong Course Outline. Rất nhiều nội dung lý thuyết (giả định A3a/A3b, A4a/b/c, GLS/FGLS, các loại SE) trích xuất đầy đủ qua text; các trang ví dụ R output (POLS/FE/RE với từng loại SE) là ảnh, chỉ có phần diễn giải bằng lời (sidebar note) mới trích xuất được — đã đủ để nắm ý nghĩa của từng loại SE mà không cần xem số liệu cụ thể.
<br><span class="en">Topic 12 slide deck (numbered file 13 — see `CLAUDE.md` §3 for the numbering mismatch). An extended version of Topic 6 (`slides-6-iu.pdf`); its closing title slide reads "PANEL DATA MODELS WITH COVARIANCE STRUCTURE" — confirming this is indeed the Course Outline's "Panel data models with variance structures." Most of the theoretical content (assumptions A3a/A3b, A4a/b/c, GLS/FGLS, the SE types) extracted fully via text; the R-output example pages (POLS/FE/RE with each SE type) are images, only the sidebar-note prose extracted — enough to grasp the meaning of each SE type without needing the specific numbers.</span>

## Ví dụ dữ liệu - <span class="en">Example data</span>

Dữ liệu 300 doanh nghiệp, 5 năm: `output` (giá trị sản lượng), `capital`, `training` (giờ đào tạo/lao động), `labor`, `export`, `credit`, `tech` (3 mức: lowtech/mediumtech/hightech). Cùng bộ dữ liệu này được tái sử dụng ở Topic 13 (`slides-14-iu.pdf`) và Topic 14 (`slides-15-iu.pdf`) — cho thấy chủ đích thiết kế: cùng một bối cảnh thực nghiệm, tăng dần độ phức tạp qua 3 bài giảng panel liên tiếp (FE/RE cơ bản → IV cho panel → dynamic panel).
<br><span class="en">Data on 300 firms, 5 years: `output` (output value), `capital`, `training` (training hours/worker), `labor`, `export`, `credit`, `tech` (3 levels: lowtech/mediumtech/hightech). The same dataset is reused in Topic 13 (`slides-14-iu.pdf`) and Topic 14 (`slides-15-iu.pdf`) — a deliberate design choice: the same empirical setting, with complexity increasing across three consecutive panel-data lectures (basic FE/RE → panel IV → dynamic panel).</span>

Toàn bộ nội dung đã hợp nhất vào `[[concepts/fixed-random-effects-model]]` (cùng với Topic 6).
<br><span class="en">All content has been merged into `[[concepts/fixed-random-effects-model]]` (together with Topic 6).</span>
