---
title: "Lecture 8: Dynamic Models for Panel Data"
type: source
raw_file: "raw/SLIDES/slides-15-iu.pdf"
pages: 64
topic: 14
lecture: 8
status: current
ingested: 2026-07-29
concepts: ["[[concepts/dynamic-panel-data-models]]"]
---

## Vai trò - <span class="en">Role</span>

Slide Topic 14 (cuối khóa học) — mở rộng panel data sang mô hình động (biến trễ của $y$ ở vế phải). Đây là bài giảng lý thuyết nặng nhất trong toàn bộ khóa (64 trang, gần như thuần công thức + diễn giải, rất ít trang thuần ảnh) — trích xuất gần như trọn vẹn qua text.
<br><span class="en">Topic 14 slide deck (end of the course) — extends panel data to dynamic models (a lagged $y$ on the right-hand side). The theoretically densest lecture in the whole course (64 pages, almost pure formulas + prose, very few pure-image pages) — extracted almost entirely via text.</span>

## Ví dụ dữ liệu - <span class="en">Example data</span>

Cùng bối cảnh 300 doanh nghiệp như Topic 12–13, nhưng mở rộng thời gian quan sát lên **10 năm** (so với 5 năm ở Topic 12–13) — cần thiết vì mô hình động và GMM cần đủ độ dài chuỗi thời gian để có đủ lag làm instrument. `training` tiếp tục đóng vai trò biến nội sinh, `subeligible`/`localbudget` là external instrument.
<br><span class="en">The same 300-firm setting as Topic 12–13, but with the observation window extended to **10 years** (vs. 5 years in Topic 12–13) — necessary because dynamic models and GMM need a long enough time series to have enough lags to use as instruments. `training` continues to play the endogenous-variable role, `subeligible`/`localbudget` are external instruments.</span>

## Reading liên quan (từ Course Outline) - <span class="en">Related readings (from the Course Outline)</span>

Anderson & Hsiao (1981, 1982); Arellano & Bond (1991); Arellano & Bover (1995); Blundell & Bond (1998); tài liệu Stata cho `xtabond`, `xtdpdsys`, `xtdpd`.
<br><span class="en">Anderson & Hsiao (1981, 1982); Arellano & Bond (1991); Arellano & Bover (1995); Blundell & Bond (1998); Stata documentation for `xtabond`, `xtdpdsys`, `xtdpd`.</span>

Toàn bộ nội dung đã tổng hợp vào `[[concepts/dynamic-panel-data-models]]`.
<br><span class="en">All content has been synthesized into `[[concepts/dynamic-panel-data-models]]`.</span>
