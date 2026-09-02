---
title: "Stock & Yogo"
type: person
role: "Econometricians — bảng ngưỡng tới hạn (critical values) cho kiểm định weak instruments"
tags: [stock-yogo, weak-instruments, iv-regression]
---

James H. Stock & Motohiro Yogo (2005, *"Testing for Weak Instruments in Linear IV Regression"*, trong *Identification and Inference for Econometric Models*) cung cấp bảng **ngưỡng tới hạn (critical values)** để đánh giá thống kê [[people/cragg-donald|Cragg-Donald (CD) F]] — trả lời câu hỏi "CD-F bao nhiêu thì đủ để coi là instrument không yếu?".
<br><span class="en">James H. Stock & Motohiro Yogo (2005, *"Testing for Weak Instruments in Linear IV Regression"*, in *Identification and Inference for Econometric Models*) provide a table of **critical values** for evaluating the [[people/cragg-donald|Cragg-Donald (CD) F]] statistic — answering the question "how large does CD-F need to be to call the instruments not weak?".</span>

Ngưỡng Stock-Yogo được xây dựng theo **hai tiêu chí khác nhau**, hay bị nhầm lẫn với nhau:
<br><span class="en">The Stock-Yogo thresholds are built on **two different criteria**, which are commonly confused with each other:</span>

- **Maximum relative bias**: ngưỡng sao cho độ chệch của 2SLS so với OLS không vượt quá một tỷ lệ cho phép (VD 10%).
  <br><span class="en">**Maximum relative bias**: a threshold such that 2SLS's bias relative to OLS does not exceed an allowed proportion (e.g. 10%).</span>
- **Maximum size distortion**: ngưỡng sao cho một kiểm định Wald danh nghĩa mức 5% không bị méo mó vượt quá một mức cho phép (VD kiểm định thực chất có size 10% hoặc 15% thay vì 5%).
  <br><span class="en">**Maximum size distortion**: a threshold such that a nominal 5% Wald test's actual size distortion does not exceed an allowed level (e.g. the test's true size is 10% or 15% instead of 5%).</span>

Một instrument có thể đạt tiêu chí này nhưng không đạt tiêu chí kia — cần nói rõ đang dùng tiêu chí nào khi báo cáo kết quả, không chỉ nói chung chung "vượt ngưỡng Stock-Yogo". Bảng chỉ được thiết kế cho CD-F (giả định homoskedastic); không dùng chính thức được cho Kleibergen-Paap F (robust heteroskedasticity), dù trong thực hành người ta vẫn so sánh không chính thức.
<br><span class="en">An instrument can meet one criterion but not the other — state clearly which criterion is being used when reporting results, not just a generic "exceeds the Stock-Yogo threshold." The table was designed only for CD-F (homoskedastic assumption); it is not formally valid for the Kleibergen-Paap F (robust to heteroskedasticity), though in practice people still compare them informally.</span>

## Xuất hiện trong

- [[concepts/endogeneity-iv-regression]]
- [[concepts/iv-regression-panel-data]]
