---
title: "Cragg & Donald"
type: person
role: "Econometricians — the Cragg-Donald F statistic for testing weak instruments under homoskedasticity"
tags: [cragg-donald, weak-instruments, iv-regression]
---

John G. Cragg & Stephen G. Donald (1993, *"Testing Identifiability and Specification in Instrumental Variable Models"*, Econometric Theory) phát triển **Cragg-Donald (CD) F-statistic** — thống kê tổng quát hóa first-stage F sang trường hợp nhiều biến nội sinh cùng lúc (dùng eigenvalue nhỏ nhất của một ma trận liên quan đến các phương trình first-stage), dùng để kiểm định **weak identification**: bác bỏ được underidentification không có nghĩa instrument đã đủ mạnh — cần so sánh CD F-statistic với ngưỡng tới hạn.
<br><span class="en">John G. Cragg & Stephen G. Donald (1993, *"Testing Identifiability and Specification in Instrumental Variable Models"*, Econometric Theory) developed the **Cragg-Donald (CD) F-statistic** — a statistic generalizing the first-stage F to the case of multiple endogenous regressors at once (using the smallest eigenvalue of a matrix related to the first-stage equations), used to test **weak identification**: rejecting underidentification doesn't mean the instruments are strong enough — the CD F-statistic must be compared to a critical value.</span>

Với đúng 1 biến nội sinh, CD-F trùng với first-stage F thông thường. Giả định nền: **homoskedasticity**. Ngưỡng tới hạn để đánh giá CD-F do [[people/stock-yogo|Stock & Yogo]] cung cấp; quy tắc kinh nghiệm phổ biến trong thực hành: CD F-statistic > 10.
<br><span class="en">With exactly 1 endogenous regressor, CD-F coincides with the usual first-stage F. Underlying assumption: **homoskedasticity**. The critical values for evaluating CD-F are provided by [[people/stock-yogo|Stock & Yogo]]; a common rule of thumb in practice: CD F-statistic > 10.</span>

Khi giả định homoskedasticity không giữ, bản thay thế robust là **Kleibergen-Paap rk Wald F (KP-F)** — nhưng KP-F **không** so sánh trực tiếp được với ngưỡng Stock-Yogo (vốn được thiết kế riêng cho CD-F, giả định homoskedastic).
<br><span class="en">When the homoskedasticity assumption fails, the robust alternative is the **Kleibergen-Paap rk Wald F (KP-F)** — but KP-F **cannot** be directly compared to the Stock-Yogo critical values (which were designed specifically for CD-F, under homoskedasticity).</span>

## Xuất hiện trong - <span class="en">Appears in</span>

- [[concepts/endogeneity-iv-regression]]
- [[concepts/iv-regression-panel-data]]
