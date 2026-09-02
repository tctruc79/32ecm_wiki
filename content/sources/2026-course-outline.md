---
title: "Course Outline — Applied Econometrics (2026)"
type: source
raw_file: "raw/SLIDES/VNP2026-CO.pdf"
pages: 12
topic: null
status: current
ingested: 2026-07-29
concepts: ["[[concepts/econometrics-overview]]"]
---

## Vai trò của tài liệu này - <span class="en">Role of this document</span>

Đề cương môn **Applied Econometrics for Master Programme in Economics (2026)**, giảng viên **[[people/truong-dang-thuy|Trương Đăng Thụy]]** (UEH University — VNP). Đây là tài liệu "meta" định nghĩa toàn bộ cấu trúc khóa học — dùng để dựng bản đồ chủ đề cho cả wiki (xem bảng ở `index.md` và `CLAUDE.md` §3).
<br><span class="en">The syllabus for **Applied Econometrics for Master Programme in Economics (2026)**, taught by **[[people/truong-dang-thuy|Trương Đăng Thụy]]** (UEH University — VNP). This is a "meta" document defining the whole course structure — used to build the topic map for the whole wiki (see the table in `index.md` and `CLAUDE.md` §3).</span>

## Course description

Môn học dạy cách nhà kinh tế dùng mô hình kinh tế lượng để phân tích dữ liệu, kiểm định giả thuyết kinh tế và đề xuất hàm ý chính sách. Trọng tâm: ước lượng mô hình + diễn giải kết quả, không chỉ chạy lệnh.
<br><span class="en">This course teaches how economists use econometric models to analyze data, test economic hypotheses, and derive policy implications. Focus: model estimation + result interpretation, not just running commands.</span>

## Prerequisites

- Nắm được các mô hình kinh tế lượng cơ bản và functional forms
  <br><span class="en">Familiarity with basic econometric models and functional forms</span>
- Vi tích phân (differential calculus)
  <br><span class="en">Differential calculus</span>
- Đại số ma trận (matrix operations)
  <br><span class="en">Matrix algebra (matrix operations)</span>
- Máy tính cài sẵn R, RStudio, Rtools, Stata
  <br><span class="en">A computer with R, RStudio, Rtools, Stata installed</span>

## Materials chính - <span class="en">Main materials</span>

1. Gujarati D. (2014) *Econometrics by Example*, Palgrave Macmillan — **giáo trình chính**, được trích dẫn "Reading" cho từng topic.
   <br><span class="en">Gujarati D. (2014) *Econometrics by Example*, Palgrave Macmillan — **main textbook**, cited as the "Reading" for each topic.</span>
2. Gujarati D. & Porter D. (2008) *Basic Econometrics*, 5th ed.
3. Long J.S. & Freese J. (2014) *Regression Models for Categorical Dependent Variables Using Stata*, 3rd ed.
4. Wooldridge J. (2020) *Introductory Econometrics*, 7th ed.
5. Baltagi B.H. (2013) *Econometric Analysis of Panel Data*.
6. Loạt bài báo panel động: Anderson & Hsiao (1981, 1982), Arellano & Bond (1991), Arellano & Bover (1995), Blundell & Bond (1998), Roodman (2009), Windmeijer (2005) — nền tảng lý thuyết cho Topic 14 (Dynamic panel data models).
   <br><span class="en">The dynamic-panel paper series: Anderson & Hsiao (1981, 1982), Arellano & Bond (1991), Arellano & Bover (1995), Blundell & Bond (1998), Roodman (2009), Windmeijer (2005) — the theoretical foundation for Topic 14 (Dynamic panel data models).</span>

## Software

- **R/RStudio**: dùng cho hầu hết môn học.
  <br><span class="en">**R/RStudio**: used for most of the course.</span>
- **Stata** (bản 15+): chỉ dùng riêng cho phần panel data models.
  <br><span class="en">**Stata** (v15+): used specifically only for the panel data models section.</span>

## Course evaluation (50/25/25 split — xem lưu ý về mâu thuẫn số liệu ở CLAUDE.md §7) - <span class="en">Course evaluation (50/25/25 split — see the note on the data mismatch in CLAUDE.md §7)</span>

- Practice assignments: 25% (làm trên nền tảng học trực tuyến econometrics.site)
  <br><span class="en">Practice assignments: 25% (done on the econometrics.site online learning platform)</span>
- In-class assignments: 50% — CO ghi "10 assignments × 5%"; slide Introduction lại ghi "5 assignments × 10%". Cả hai đều cộng ra 50%, chỉ khác cách chia nhỏ — không phải mâu thuẫn về tổng điểm.
  <br><span class="en">In-class assignments: 50% — the CO states "10 assignments × 5%"; the Introduction slide states "5 assignments × 10%". Both add up to 50%, they only differ in how it's broken down — not a contradiction in the total.</span>
- Individual project: 25% — bắt buộc dùng **panel data**, báo cáo ~10 trang, chấm theo: chất lượng câu hỏi nghiên cứu, xử lý dữ liệu, đặc tả mô hình, kỹ thuật ước lượng, diễn giải kết quả.
  <br><span class="en">Individual project: 25% — must use **panel data**, ~10-page report, graded on: quality of the research question, data handling, model specification, estimation technique, and result interpretation.</span>

## Topics (15 topic, đánh số 0–14) - <span class="en">Topics (15 topics, numbered 0–14)</span>

CO ghi "16 topics" ở câu mở đầu Section VII nhưng chỉ định nghĩa 15 topic (0 đến 14) — coi đây là một điểm không khớp trong nguồn gốc, **không** tự suy ra topic thứ 16.
<br><span class="en">The CO states "16 topics" in Section VII's opening line but only defines 15 topics (0 through 14) — treated as a source-level inconsistency, **not** guessed into a 16th topic.</span>

Bảng đầy đủ (chủ đề, nội dung, file slide, reading) đã được chuyển vào `index.md` (mục "Course map") vì đó là bảng điều hướng dùng chung cho toàn bộ wiki — tránh duplicate ở đây.
<br><span class="en">The full table (topic, content, slide file, reading) has been moved to `index.md` (the "Course map" section) since that is the shared navigation table for the whole wiki — avoiding duplication here.</span>

Điểm cần nhớ khi ingest các slide sau này: **tên file slide không khớp số thứ tự Topic trong CO** (VD: Topic 12 nằm trong `slides-13-iu.pdf`, không phải `slides-12`). Xem chi tiết đầy đủ ở `CLAUDE.md` §3.
<br><span class="en">Important for ingesting later slides: **slide filenames don't match the Topic numbers in the CO** (e.g., Topic 12 lives in `slides-13-iu.pdf`, not `slides-12`). Full detail in `CLAUDE.md` §3.</span>

## Schedule

22 buổi học/thực hành (mỗi buổi ~2 giờ + Q&A), phòng H-204. 4 buổi là Tutorial (R/RStudio thực hành), phần Panel data models chiếm 6 buổi cuối (buổi 18–22 gồm cả 2 buổi cho IV-panel và 2 buổi cho Dynamic panel).
<br><span class="en">22 lecture/practice sessions (~2 hours + Q&A each), room H-204. 4 sessions are Tutorials (R/RStudio practice); the Panel data models section takes up the final 6 sessions (sessions 18–22, including 2 sessions for panel IV and 2 for Dynamic panel).</span>
