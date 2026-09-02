---
title: "R Basics (tooling reference)"
type: concept
status: mature
tags: [r, tooling, reference]
sources: ["[[sources/slides-0-r-basics]]"]
related: ["[[concepts/linear-regression-model]]"]
updated: 2026-08-29
---

Trang tham khảo công cụ (không phải một Topic riêng của Course Outline) — dùng xuyên suốt các bài thực hành. Khác các trang concept khác, đây chỉ là bảng tra cứu, không có "bẫy thi" hay "kết nối lý thuyết" đáng kể.
<br><span class="en">A tooling reference page (not a separate Topic in the Course Outline) — used throughout the practice sessions. Unlike the other concept pages, this is just a lookup table, with no meaningful "exam traps" or "theoretical connections".</span>

## RStudio interface - <span class="en">RStudio interface</span>

3 vùng chính: **Source** (viết code), **Console** (chạy lệnh, command prompt), **Environment** (xem các object đang có trong session). Lưu code trong file `.R` (File → New file → R Script, rồi File → Save as). Chạy 1 dòng: đặt con trỏ vào dòng, `Ctrl+Enter`. Chạy nhiều dòng: bôi đen, `Ctrl+Enter`. Comment (loại một dòng khỏi khi chạy): đặt `#` ở đầu dòng.
<br><span class="en">3 main panes: **Source** (write code), **Console** (run commands, the command prompt), **Environment** (view the objects currently in the session). Save code in an `.R` file (File → New file → R Script, then File → Save as). Run one line: place the cursor on the line, `Ctrl+Enter`. Run multiple lines: select them, `Ctrl+Enter`. Comment (exclude a line from running): put `#` at the start of the line.</span>

## Data types và objects - <span class="en">Data types and objects</span>

Kiểu dữ liệu cơ bản: **Integer** (số nguyên), **Floating point number** (số thực dấu phẩy động), **String** (chuỗi ký tự).
<br><span class="en">Basic data types: **Integer**, **Floating point number**, **String**.</span>

Kiểu object hay dùng:
<br><span class="en">Commonly used object types:</span>
- **Vector** — một dãy giá trị một chiều, cùng kiểu dữ liệu.
  <br><span class="en">**Vector** — a one-dimensional sequence of values of the same data type.</span>
- **Dataframe** — bảng dữ liệu hai chiều (hàng = quan sát, cột = biến), mỗi cột có thể khác kiểu dữ liệu; đây là dạng object dùng để chứa dataset khi làm hồi quy.
  <br><span class="en">**Dataframe** — a two-dimensional data table (rows = observations, columns = variables), where each column can have a different data type; this is the object type used to hold a dataset when running a regression.</span>

## Hàm toán học cơ bản (base R) - <span class="en">Basic math functions (base R)</span>

| Lệnh - <span class="en">Command</span> | Ý nghĩa - <span class="en">Meaning</span> |
|---|---|
| `abs(a)` | giá trị tuyệt đối - <span class="en">absolute value</span> |
| `sqrt(a)` | căn bậc hai - <span class="en">square root</span> |
| `round(a, 3)` | làm tròn đến 3 chữ số thập phân - <span class="en">round to 3 decimal places</span> |
| `exp(a)` | hàm mũ cơ số e - <span class="en">the base-e exponential function</span> |
| `log(a)` | logarithm tự nhiên (cơ số e) - <span class="en">natural logarithm (base e)</span> |
| `log10(a)` | logarithm cơ số 10 - <span class="en">base-10 logarithm</span> |

## Hàm thống kê cơ bản - <span class="en">Basic statistical functions</span>

Áp dụng cho một biến (vector) `a`:
<br><span class="en">Applied to a variable (vector) `a`:</span>

| Lệnh - <span class="en">Command</span> | Ý nghĩa - <span class="en">Meaning</span> |
|---|---|
| `sum(a)` | tổng các phần tử - <span class="en">sum of the elements</span> |
| `min(a)` / `max(a)` | giá trị nhỏ nhất / lớn nhất - <span class="en">minimum / maximum value</span> |
| `mean(a)` | trung bình - <span class="en">mean</span> |
| `sd(a)` | độ lệch chuẩn - <span class="en">standard deviation</span> |
| `median(a)` | trung vị - <span class="en">median</span> |
| `summary(a)` | in bảng tóm tắt thống kê (min, Q1, median, mean, Q3, max) - <span class="en">prints a summary statistics table (min, Q1, median, mean, Q3, max)</span> |
| `sort(a)` | sắp xếp các phần tử tăng dần - <span class="en">sorts the elements in ascending order</span> |

Cho một giá trị cụ thể `a` — liên quan phân phối chuẩn:
<br><span class="en">For a specific value `a` — related to the normal distribution:</span>
- `dnorm(a)` — giá trị hàm mật độ xác suất (pdf) của phân phối chuẩn chuẩn hóa tại điểm a.
  <br><span class="en">`dnorm(a)` — the value of the probability density function (pdf) of the standard normal distribution at point a.</span>
- `pnorm(a)` — giá trị hàm phân phối tích lũy (cdf) của phân phối chuẩn chuẩn hóa tại điểm a.
  <br><span class="en">`pnorm(a)` — the value of the cumulative distribution function (cdf) of the standard normal distribution at point a.</span>
- `A = rnorm(10, mean=0, sd=1)` — tạo 10 số ngẫu nhiên theo phân phối chuẩn với mean 0 và SD 1.
  <br><span class="en">`A = rnorm(10, mean=0, sd=1)` — generates 10 random numbers from a normal distribution with mean 0 and SD 1.</span>

## Package ngoài base R - <span class="en">Packages outside base R</span>

Base R chỉ chứa chức năng cốt lõi; các package như `psych` (tóm tắt dữ liệu) cần cài đặt trước khi dùng:
<br><span class="en">Base R only contains core functionality; packages like `psych` (data summarization) need to be installed before use:</span>

- `install.packages("psych")` — cài package, **chỉ cần chạy 1 lần** trên một máy.
  <br><span class="en">`install.packages("psych")` — installs the package, **only needs to be run once** on a given machine.</span>
- `library(psych)` — nạp package vào session; cần gọi lại **mỗi lần mở R/RStudio mới**, trước khi dùng các hàm của package (VD `describe`).
  <br><span class="en">`library(psych)` — loads the package into the session; must be called again **every time a new R/RStudio session is opened**, before using the package's functions (e.g. `describe`).</span>

## Quy trình làm việc với dữ liệu - <span class="en">Workflow for working with data</span>

Thứ tự thao tác thường gặp khi làm việc với một dataset trong R:
<br><span class="en">The common sequence of steps when working with a dataset in R:</span>

1. Dọn môi trường làm việc (clear working environment) và đổi thư mục làm việc (working folder) nếu cần.
   <br><span class="en">Clear the working environment and change the working folder if needed.</span>
2. Import dữ liệu (từ file hoặc trực tiếp từ URL).
   <br><span class="en">Import the data (from a file or directly from a URL).</span>
3. Xem summary statistics.
   <br><span class="en">View summary statistics.</span>
4. Lập bảng tần suất một chiều (frequency table) và hai chiều (two-way table).
   <br><span class="en">Build a one-way frequency table and a two-way table.</span>
5. Vẽ biểu đồ: histogram, scatter plot.
   <br><span class="en">Draw charts: histogram, scatter plot.</span>
6. Chạy hồi quy (regression).
   <br><span class="en">Run the regression.</span>
7. Tạo biến mới trong dataframe (generate variables) nếu cần biến đổi/tạo biến phục vụ phân tích.
   <br><span class="en">Generate new variables in the dataframe if variable transformation/creation is needed for the analysis.</span>

## Kết nối - <span class="en">Connections</span>

Nền tảng thao tác cho toàn bộ các ví dụ thực nghiệm trong [[concepts/linear-regression-model]] và các concept khác — không mang nội dung lý thuyết econometrics riêng.
<br><span class="en">The operational foundation for all the empirical examples in [[concepts/linear-regression-model]] and the other concept pages — it carries no econometric theory content of its own.</span>
