---
title: "Sargan (J. D.)"
type: person
role: "Econometrician — the original overidentifying-restrictions test for IV/GMM under homoskedasticity"
tags: [sargan-test, overidentification, iv-regression]
---

Denis Sargan (1958, *"The Estimation of Economic Relationships using Instrumental Variables"*, Econometrica) đề xuất kiểm định overidentifying restrictions đầu tiên cho mô hình IV: khi số instrument $h$ nhiều hơn số biến nội sinh $k$ (overidentified), Sargan test kiểm tra xem phần dư IV có tương quan với toàn bộ tập instrument $Z$ hay không — $J=nR^2$ từ hồi quy phần dư lên $Z$, phân phối $\chi^2_{h-k}$.
<br><span class="en">Denis Sargan (1958, *"The Estimation of Economic Relationships using Instrumental Variables"*, Econometrica) proposed the first overidentifying-restrictions test for IV models: when the number of instruments $h$ exceeds the number of endogenous regressors $k$ (overidentified), the Sargan test checks whether the IV residuals are correlated with the full instrument set $Z$ — $J=nR^2$ from regressing the residuals on $Z$, distributed $\chi^2_{h-k}$.</span>

Giả định nền: **homoskedasticity**. Khi giả định này không giữ, [[people/hansen|Hansen's J test]] là bản tổng quát hóa (dùng trọng số GMM efficient thay vì $nR^2$), trùng với Sargan khi thực sự homoskedastic.
<br><span class="en">Underlying assumption: **homoskedasticity**. When this assumption fails, [[people/hansen|Hansen's J test]] is the generalization (using the efficient GMM weight matrix instead of $nR^2$), coinciding with Sargan when the data is truly homoskedastic.</span>

**Lưu ý diễn giải chung cho cả hai kiểm định**: không bác bỏ $H_0$ chỉ có nghĩa "không tìm thấy bằng chứng chống lại tính hợp lệ của instrument", **không phải** "đã chứng minh instrument hợp lệ" — validity luôn phải được biện luận bằng thiết kế nghiên cứu (exclusion restriction), kiểm định chỉ hỗ trợ chứ không thay thế lập luận này.
<br><span class="en">**Interpretation note common to both tests**: failing to reject $H_0$ only means "no evidence found against instrument validity", **not** "instrument validity has been proven" — validity must always be argued through the research design (the exclusion restriction); the test only supports, never replaces, that argument.</span>

## Xuất hiện trong - <span class="en">Appears in</span>

- [[concepts/endogeneity-iv-regression]]
- [[concepts/iv-regression-panel-data]]
- [[concepts/dynamic-panel-data-models]]
