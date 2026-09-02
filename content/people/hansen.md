---
title: "Hansen (L. P.)"
type: person
role: "Econometrician — GMM framework và kiểm định overidentifying restrictions tổng quát (Hansen's J test)"
tags: [hansen-j-test, gmm, overidentification, iv-regression]
---

Lars Peter Hansen (1982, *"Large Sample Properties of Generalized Method of Moments Estimators"*, Econometrica) xây dựng khung **Generalized Method of Moments (GMM)** — một họ ước lượng tổng quát hóa cả OLS lẫn 2SLS/IV thành trường hợp riêng, dựa trên việc chọn trọng số tối ưu cho các điều kiện moment. Đóng góp này mang lại giải Nobel Kinh tế học 2013.
<br><span class="en">Lars Peter Hansen (1982, *"Large Sample Properties of Generalized Method of Moments Estimators"*, Econometrica) built the **Generalized Method of Moments (GMM)** framework — a family of estimators that generalizes both OLS and 2SLS/IV as special cases, based on choosing an optimal weight for the moment conditions. This contribution earned the 2013 Nobel Prize in Economics.</span>

**Hansen's J test** là kiểm định overidentifying restrictions xây dựng trên khung GMM đó: $J=n\cdot g(\hat\beta)'W^{-1}g(\hat\beta)$, phân phối $\chi^2_{h-k}$ — về bản chất là bản tổng quát hóa của [[people/sargan|Sargan test]], cho phép **heteroskedasticity** (Sargan chỉ đúng dưới homoskedasticity). Khi dữ liệu thực sự homoskedastic, hai kiểm định trùng nhau.
<br><span class="en">**Hansen's J test** is the overidentifying-restrictions test built on that GMM framework: $J=n\cdot g(\hat\beta)'W^{-1}g(\hat\beta)$, distributed $\chi^2_{h-k}$ — essentially a generalization of the [[people/sargan|Sargan test]] that allows for **heteroskedasticity** (Sargan is only valid under homoskedasticity). When the data is truly homoskedastic, the two tests coincide.</span>

**Lưu ý diễn giải chung cho cả hai kiểm định**: không bác bỏ $H_0$ chỉ có nghĩa "không tìm thấy bằng chứng chống lại tính hợp lệ của instrument", **không phải** "đã chứng minh instrument hợp lệ" — validity luôn phải được biện luận bằng thiết kế nghiên cứu (exclusion restriction), kiểm định chỉ hỗ trợ chứ không thay thế lập luận này.
<br><span class="en">**Interpretation note common to both tests**: failing to reject $H_0$ only means "no evidence found against instrument validity", **not** "instrument validity has been proven" — validity must always be argued through the research design (the exclusion restriction); the test only supports, never replaces, that argument.</span>

## Xuất hiện trong

- [[concepts/endogeneity-iv-regression]]
- [[concepts/iv-regression-panel-data]]
