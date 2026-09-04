---
title: "Lecture 8: Dynamic Panel Data Models"
type: concept
status: mature
tags: [panel-data, dynamic-model, nickell-bias, gmm, arellano-bond, blundell-bond]
sources: ["[[sources/slides-15-dynamic-panel-data-models]]"]
related: ["[[concepts/fixed-random-effects-model]]", "[[concepts/iv-regression-panel-data]]", "[[concepts/endogeneity-iv-regression]]", "[[people/arellano-bond]]"]
lecture: 8
assignment: ["Assignment 7: Dynamic panel data models: Anderson-Hsiao estimator", "Assignment 8: Dynamic panel data models: Difference GMM", "Assignment 9: Dynamic panel data models: System GMM"]
updated: 2026-09-04
---

> **Cách đọc trang này**: đây là bài cuối của khóa học, và là điểm hội tụ của toàn bộ mạch panel data — nên đọc sau khi đã nắm [[concepts/fixed-random-effects-model]] (phép biến đổi within/FD) và [[concepts/iv-regression-panel-data]] (khung GMM/IV áp cho panel). Nếu chỉ có thời gian ôn hai điểm quan trọng nhất, hãy tập trung vào: (1) Nickell bias là hàm của $1/T$, **không phải** $1/N$ — điểm hay bị hiểu ngược nhất của cả topic; và (2) bộ kiểm định AR(1)/AR(2) có quy tắc **phản trực giác** — AR(1) *nên* bị bác bỏ, không bác bỏ mới là dấu hiệu có vấn đề; AR(2) *không nên* bị bác bỏ, bác bỏ mới là dấu hiệu instrument hỏng.
> <br><span class="en">**How to read this page**: this is the final lesson of the course, and the convergence point of the entire panel-data thread — so read it after mastering [[concepts/fixed-random-effects-model]] (the within/FD transformation) and [[concepts/iv-regression-panel-data]] (the GMM/IV framework applied to panel data). If you only have time to review the two most important points, focus on: (1) Nickell bias is a function of $1/T$, **not** $1/N$ — the single most commonly reversed point in the whole topic; and (2) the AR(1)/AR(2) test battery follows a **counter-intuitive** rule — AR(1) *should* be rejected, failing to reject it is the sign of a problem; AR(2) *should not* be rejected, rejecting it is the sign of a broken instrument.</span>

**Lecture 8** trong đề cương (CO Topic 14) — Assignment 7 (Anderson-Hsiao), Assignment 8 (Difference GMM), Assignment 9 (System GMM).
<br><span class="en">**Lecture 8** in the syllabus (CO Topic 14) — Assignment 7 (Anderson-Hsiao), Assignment 8 (Difference GMM), Assignment 9 (System GMM).</span>

Mô hình động đưa **biến trễ của chính $y$** vào vế phải — và biến trễ này luôn nội sinh, đòi hỏi một họ ước lượng riêng (Anderson-Hsiao → Difference GMM → System GMM).
<br><span class="en">A dynamic model brings **the lagged value of $y$ itself** into the right-hand side — and this lagged variable is always endogenous, requiring its own family of estimators (Anderson-Hsiao → Difference GMM → System GMM).</span>

## 1. Vì sao cần một mô hình động? — trực giác trước công thức - <span class="en">Why do we need a dynamic model? — intuition before formulas</span>

### 1.1 Trực giác: "quán tính" trong hành vi kinh tế - <span class="en">Intuition: "inertia" in economic behavior</span>

Nhiều hiện tượng kinh tế không "quên" quá khứ — giá trị hôm nay phụ thuộc mạnh vào giá trị hôm qua. Slide đưa ra hai ví dụ cụ thể:
<br><span class="en">Many economic phenomena do not "forget" the past — today's value depends strongly on yesterday's value. The slide gives two concrete examples:</span>

- **Employment persists over time** — việc làm có tính bền vững: một doanh nghiệp đang có nhiều lao động năm nay thường vẫn có nhiều lao động năm sau (chi phí sa thải/tuyển dụng lại, quán tính tổ chức).
<br><span class="en">**Employment persists over time** — a firm with high employment this year tends to still have high employment next year (firing/rehiring costs, organizational inertia).</span>
- **Investment decisions depend on installed capacity** — quyết định đầu tư hiện tại phụ thuộc vào năng lực sản xuất *đã lắp đặt sẵn* từ trước — doanh nghiệp không quyết định đầu tư "từ số 0" mỗi năm.
<br><span class="en">**Investment decisions depend on installed capacity** — current investment decisions depend on production capacity *already installed* beforehand — a firm does not decide on investment "from zero" every year.</span>

Hình thức hóa ý tưởng "quán tính" này bằng cách đưa $y_{i,t-1}$ vào chính vế phải của phương trình:
<br><span class="en">This "inertia" idea is formalized by bringing $y_{i,t-1}$ directly into the right-hand side of the equation:</span>

$$y_{it}=\alpha_i+\alpha y_{i,t-1}+\beta X_{it}+\varepsilon_{it}$$

Slide đưa ra ba lý do (giữ nguyên thuật ngữ gốc) để đặc tả mô hình theo dạng động:
<br><span class="en">The slide gives three reasons (original terms kept) for specifying a model in dynamic form:</span>

1. **Capture state dependence** — nhiều quá trình kinh tế phụ thuộc giá trị quá khứ của chính nó (hai ví dụ employment/investment ở trên).
<br><span class="en">**Capture state dependence** — many economic processes depend on their own past values (the employment/investment examples above).</span>
2. **Avoid omitted variables** — biến trễ đóng vai trò **proxy** cho các ảnh hưởng quá khứ không quan sát được (không cần biết chính xác *điều gì* trong quá khứ ảnh hưởng đến hiện tại, chỉ cần biết rằng toàn bộ ảnh hưởng đó đã "kết tinh" vào giá trị $y_{i,t-1}$).
<br><span class="en">**Avoid omitted variables** — the lagged variable acts as a **proxy** for unobserved past influences (no need to know exactly *what* in the past affects the present, only that all of that influence has "crystallized" into the value $y_{i,t-1}$).</span>
3. **Align with dynamic economic theory** — phù hợp với lý thuyết kinh tế học vốn dĩ mô tả hành vi qua thời gian (mô hình điều chỉnh từng phần, mô hình kỳ vọng thích nghi…).
<br><span class="en">**Align with dynamic economic theory** — consistent with economic theory, which inherently describes behavior over time (partial adjustment models, adaptive expectations models…).</span>

### 1.2 Cái giá phải trả: nội sinh tất yếu - <span class="en">The price to pay: inevitable endogeneity</span>

Đưa $y_{i,t-1}$ vào vế phải không "miễn phí" — nó luôn tạo ra **endogeneity**, vì hai lý do liên kết với nhau:
<br><span class="en">Bringing $y_{i,t-1}$ into the right-hand side is not "free" — it always creates **endogeneity**, for two linked reasons:</span>

- $y_{i,t-1}$ được sinh ra từ chính quá trình động ở kỳ trước, nên nó **chứa $\varepsilon_{i,t-1}$** bên trong.
<br><span class="en">$y_{i,t-1}$ is generated by the same dynamic process in the previous period, so it **contains $\varepsilon_{i,t-1}$** within it.</span>
- Nếu sai số có **tự tương quan AR(1)** (tức $\varepsilon_{it}$ tương quan với $\varepsilon_{i,t-1}$), thì $y_{i,t-1}$ — vì chứa $\varepsilon_{i,t-1}$ — sẽ tương quan với $\varepsilon_{it}$. Đây chính là **endogeneity**.
<br><span class="en">If the error has **AR(1) serial correlation** (i.e. $\varepsilon_{it}$ correlated with $\varepsilon_{i,t-1}$), then $y_{i,t-1}$ — because it contains $\varepsilon_{i,t-1}$ — will be correlated with $\varepsilon_{it}$. This is precisely **endogeneity**.</span>

**Nguyên tắc chọn mô hình (nhấn mạnh riêng trong slide)**: mô hình được đặc tả là động **dựa trên bản chất của quá trình kinh tế đang nghiên cứu**, việc chọn ước lượng theo sau đặc tả đó — **không được làm ngược lại** (không đặc tả mô hình động chỉ để có cớ dùng System GMM). Các ước lượng trình bày ở trang này **chỉ giải quyết** endogeneity của riêng biến trễ $y_{i,t-1}$; nếu các regressor khác trong mô hình cũng nội sinh, vẫn cần instrument riêng cho chúng (internal — lag của chính biến đó — hoặc external).
<br><span class="en">**Model-selection principle (specifically emphasized in the slide)**: a model is specified as dynamic **based on the nature of the economic process being studied**, and the choice of estimator follows from that specification — **never the other way around** (never specify a dynamic model just for an excuse to use System GMM). The estimators presented on this page **only address** the endogeneity of the lagged variable $y_{i,t-1}$ itself; if other regressors in the model are also endogenous, they still need their own instruments (internal — a lag of that same variable — or external).</span>

### 1.3 Mô hình tổng quát với biến nội sinh khác, và ví dụ xuyên suốt: 300 doanh nghiệp, 10 năm - <span class="en">General model with other endogenous variables, and the running example: 300 firms, 10 years</span>

Dạng tổng quát nhất mà slide dùng xuyên suốt các mục sau, có thêm một vector biến nội sinh khác $Y_{it}$ (ngoài $y_{i,t-1}$):
<br><span class="en">The most general form, used by the slide throughout the following sections, adds another vector of endogenous variables $Y_{it}$ (besides $y_{i,t-1}$):</span>

$$y_{it}=\alpha_i+\alpha y_{i,t-1}+\gamma Y_{it}+\beta X_{it}+\varepsilon_{it}$$

- $Y_{it}$: vector biến **nội sinh** (correlated với $\varepsilon_{it}$), khác với $y_{i,t-1}$.
<br><span class="en">$Y_{it}$: vector of **endogenous** variables (correlated with $\varepsilon_{it}$), distinct from $y_{i,t-1}$.</span>
- $X_{it}$: vector biến **ngoại sinh** (strictly exogenous).
<br><span class="en">$X_{it}$: vector of **exogenous** variables (strictly exogenous).</span>
- $\alpha_i$: hiệu ứng cá nhân không quan sát được (individual effects).
<br><span class="en">$\alpha_i$: unobserved individual effect (individual effects).</span>
- $\varepsilon_{it}$: sai số đặc trưng (idiosyncratic error).
<br><span class="en">$\varepsilon_{it}$: idiosyncratic error.</span>

Cả $y_{i,t-1}$ lẫn $Y_{it}$ đều cần instrument: **internal instruments** (lag ở mức hoặc sai phân của chính $y$ và $Y$) hoặc **external instruments** ($IV$ từ nguồn dữ liệu khác). Đây là cấu trúc tổng quát nhất — một số thành phần có thể được bỏ qua tùy bài toán cụ thể.
<br><span class="en">Both $y_{i,t-1}$ and $Y_{it}$ need instruments: **internal instruments** (level or difference lags of $y$ and $Y$ themselves) or **external instruments** ($IV$ from another data source). This is the most general structure — some components may be dropped depending on the specific problem.</span>

**Bộ dữ liệu minh họa** dùng xuyên suốt slide Topic 14 (300 doanh nghiệp, quan sát 10 năm — dài hơn 5 năm ở Topic 12–13, vì mô hình động và GMM cần đủ độ dài chuỗi thời gian để có đủ lag làm instrument):
<br><span class="en">**Illustrative dataset** used throughout the Topic 14 slides (300 firms, observed over 10 years — longer than the 5 years in Topic 12–13, because dynamic models and GMM need enough time-series length to have sufficient lags to use as instruments):</span>

| Biến - <span class="en">Variable</span> | Ý nghĩa - <span class="en">Meaning</span> | Đơn vị - <span class="en">Unit</span> | Vai trò trong mô hình - <span class="en">Role in the model</span> |
|---|---|---|---|
| `output` | Giá trị sản lượng — **biến phụ thuộc**, dùng dạng log<br><span class="en">Output value — the **dependent variable**, in log form</span> | triệu VND<br><span class="en">million VND</span> | $y_{it}$ |
| `lag(output)` | Sản lượng kỳ trước<br><span class="en">Previous-period output</span> | log(triệu VND)<br><span class="en">log(million VND)</span> | $y_{i,t-1}$ — **luôn nội sinh**<br><span class="en">$y_{i,t-1}$ — **always endogenous**</span> |
| `capital` | Giá trị vốn vật chất, dùng dạng log<br><span class="en">Physical capital value, in log form</span> | triệu VND<br><span class="en">million VND</span> | $X_{it}$ (exogenous) |
| `labor` | Số lượng lao động, dùng dạng log<br><span class="en">Number of workers, in log form</span> | người<br><span class="en">persons</span> | $X_{it}$ (exogenous) |
| `training` | Số giờ đào tạo bình quân mỗi lao động<br><span class="en">Average training hours per worker</span> | giờ/người<br><span class="en">hours/person</span> | $Y_{it}$ — **endogenous** |
| `export` | Doanh nghiệp có xuất khẩu hay không<br><span class="en">Whether the firm exports</span> | dummy (1/0) | $X_{it}$ (exogenous) |
| `credit` | Doanh nghiệp có tiếp cận tín dụng hay không<br><span class="en">Whether the firm has access to credit</span> | dummy (1/0) | $X_{it}$ (exogenous) |
| `tech` | Trình độ công nghệ: `lowtech` (nền), `mediumtech`, `hightech`<br><span class="en">Technology level: `lowtech` (base), `mediumtech`, `hightech`</span> | categorical | $X_{it}$ (exogenous, 2 dummy) |
| `subeligible` | Doanh nghiệp đủ điều kiện nhận trợ cấp đào tạo lao động<br><span class="en">Whether the firm is eligible for labor-training subsidies</span> | dummy (1/0) | **external IV** cho `training`<br><span class="en">**external IV** for `training`</span> |
| `localbudget` | Ngân sách chính quyền địa phương dành cho đào tạo lao động<br><span class="en">Local government budget allocated to labor training</span> | triệu VND<br><span class="en">million VND</span> | **external IV** cho `training`<br><span class="en">**external IV** for `training`</span> |

Trong hầu hết ví dụ số ở trang này, mô hình cụ thể được ước lượng là:
<br><span class="en">In most numerical examples on this page, the specific model estimated is:</span>

$$\log(output_{it}) = \alpha_i + \alpha\,\log(output_{i,t-1}) + \gamma\, training_{it} + \beta_1\log(capital_{it}) + \beta_2\log(labor_{it}) + \cdots + \varepsilon_{it}$$

## 2. FE và FD đơn thuần đều thất bại: Nickell bias - <span class="en">FE and FD alone both fail: Nickell bias</span>

### 2.1 Trực giác: vì sao within-transformation "vỡ" trong mô hình động - <span class="en">Intuition: why the within-transformation "breaks" in a dynamic model</span>

Trực giác cốt lõi (đây là điểm hay bị bỏ qua nhất khi mới học): FE **hoạt động tốt** trong mô hình tĩnh nhờ within-transform khử được $\alpha_i$ *mà không đụng vào cấu trúc của $X_{it}$ và $\varepsilon_{it}$* — biến độc lập và sai số ở các kỳ khác nhau, sau khi trừ đi trung bình nhóm, vẫn giữ nguyên quan hệ (không) tương quan ban đầu. Nhưng khi biến độc lập chính là **biến trễ của $y$**, trung bình nhóm $\bar y_{i,-1}=\frac1{T-1}\sum_t y_{i,t-1}$ lại **chứa chính những giá trị $y$ được sinh ra từ các cú sốc $\varepsilon$ ở những kỳ khác** — tức là within-transform vô tình "trộn" thông tin của sai số vào cả biến giải thích lẫn phần dư đã biến đổi.
<br><span class="en">The core intuition (the point most often overlooked when first learning this): FE **works well** in a static model because the within-transform eliminates $\alpha_i$ *without disturbing the structure of $X_{it}$ and $\varepsilon_{it}$* — the independent variable and the error at different periods, after subtracting the group mean, retain their original (non-)correlation relationship. But when the independent variable is precisely **the lag of $y$**, the group mean $\bar y_{i,-1}=\frac1{T-1}\sum_t y_{i,t-1}$ itself **contains the very $y$ values generated by the $\varepsilon$ shocks of other periods** — meaning the within-transform inadvertently "mixes" error information into both the transformed regressor and the transformed residual.</span>

Áp dụng within transform lên mô hình động cơ bản $y_{it}=\alpha y_{i,t-1}+\beta X_{it}+\alpha_i+\varepsilon_{it}$:
<br><span class="en">Applying the within transform to the basic dynamic model $y_{it}=\alpha y_{i,t-1}+\beta X_{it}+\alpha_i+\varepsilon_{it}$:</span>

$$y_{it}-\bar y_i=\alpha\left(y_{i,t-1}-\bar y_{i,-1}\right)+\beta\left(X_{it}-\bar X_i\right)+\left(\varepsilon_{it}-\bar\varepsilon_i\right)$$

Biến giải thích đã biến đổi $y_{i,t-1}-\bar y_{i,-1}$ vẫn tương quan với sai số đã biến đổi $\varepsilon_{it}-\bar\varepsilon_i$. Cơ chế cụ thể: $\bar\varepsilon_i=\frac1T\sum_t\varepsilon_{it}$ chứa cả $\varepsilon_{i,t-1}$ bên trong (một trong các số hạng được lấy trung bình) — và $\varepsilon_{i,t-1}$ chính là thành phần tạo nên $y_{i,t-1}$ qua cấu trúc đệ quy của mô hình động. Do đó $y_{i,t-1}$ (và cả $\bar y_{i,-1}$, vì trung bình cũng chứa các giá trị $y$ liên quan) tương quan với $\bar\varepsilon_i$ — **kể cả khi bản thân $\varepsilon_{it}$ không hề có tự tương quan qua các kỳ**. Đây không phải là một sai lầm về đặc tả, mà là **hệ quả cơ học tất yếu** của việc lấy trung bình nhóm khi biến độc lập là biến trễ của chính biến phụ thuộc.
<br><span class="en">The transformed regressor $y_{i,t-1}-\bar y_{i,-1}$ remains correlated with the transformed error $\varepsilon_{it}-\bar\varepsilon_i$. The specific mechanism: $\bar\varepsilon_i=\frac1T\sum_t\varepsilon_{it}$ contains $\varepsilon_{i,t-1}$ within it (one of the terms being averaged) — and $\varepsilon_{i,t-1}$ is precisely the component that generates $y_{i,t-1}$ through the recursive structure of the dynamic model. Hence $y_{i,t-1}$ (and also $\bar y_{i,-1}$, since the average also contains related $y$ values) is correlated with $\bar\varepsilon_i$ — **even when $\varepsilon_{it}$ itself has no serial correlation whatsoever across periods**. This is not a specification error, but an **inevitable mechanical consequence** of taking the group mean when the regressor is a lag of the dependent variable itself.</span>

### 2.2 FD cũng thất bại — cùng một câu chuyện, khác phép biến đổi - <span class="en">FD also fails — the same story, a different transformation</span>

Áp dụng first-difference (FD) thay vì within transform:
<br><span class="en">Applying first-difference (FD) instead of the within transform:</span>

$$\Delta y_{it}=\alpha\Delta y_{i,t-1}+\beta\Delta X_{it}+\Delta\varepsilon_{it}$$

Biến đã sai phân $\Delta y_{i,t-1}=y_{i,t-1}-y_{i,t-2}$ vẫn tương quan với sai số đã sai phân $\Delta\varepsilon_{it}=\varepsilon_{it}-\varepsilon_{i,t-1}$ — vì $y_{i,t-1}$ (thành phần của $\Delta y_{i,t-1}$) là hàm số của $\varepsilon_{i,t-1}$ (thành phần của $\Delta\varepsilon_{it}$, với dấu âm). Cả FE lẫn FD đều mắc **cùng một loại bias**, chỉ khác phép biến đổi tạo ra nó.
<br><span class="en">The differenced regressor $\Delta y_{i,t-1}=y_{i,t-1}-y_{i,t-2}$ remains correlated with the differenced error $\Delta\varepsilon_{it}=\varepsilon_{it}-\varepsilon_{i,t-1}$ — because $y_{i,t-1}$ (a component of $\Delta y_{i,t-1}$) is a function of $\varepsilon_{i,t-1}$ (a component of $\Delta\varepsilon_{it}$, with a negative sign). Both FE and FD suffer from **the same type of bias**, differing only in which transformation produces it.</span>

### 2.3 Bằng chứng thực nghiệm: FE và FD cho hai con số rất khác nhau - <span class="en">Empirical evidence: FE and FD give two very different numbers</span>

Chạy trực tiếp FE và FD "ngây thơ" (không xử lý nội sinh) trên bộ dữ liệu minh họa, hồi quy $\log(output)$ theo $\log(output)$ trễ 1 kỳ, $\log(capital)$, $\log(labor)$, `training`, `export`, `credit`, `mediumtech`, `hightech`:
<br><span class="en">Running FE and FD directly and "naively" (without addressing endogeneity) on the illustrative dataset, regressing $\log(output)$ on 1-period-lagged $\log(output)$, $\log(capital)$, $\log(labor)$, `training`, `export`, `credit`, `mediumtech`, `hightech`:</span>

**FE** (`plm(..., model = "within")`, Balanced Panel $n=300$, $T=9$, $N=2700$):

| Biến - <span class="en">Variable</span> | Hệ số - <span class="en">Coefficient</span> | SE | t |
|---|---|---|---|
| $y_{i,t-1}$ (lag output) | **0.742** | 0.00919 | 80.77 |
| $\log(capital)$ | 0.234 | 0.00703 | 33.29 |
| $\log(labor)$ | 0.017 | 0.01073 | 1.60 (n.s.) |
| `training` | 0.048 | 0.00155 | 30.97 |
| `credit` | 0.039 | 0.01294 | 3.02 |
| `hightech` | 0.164 | 0.01786 | 9.17 |

**FD** (`plm(..., model = "fd")`, cùng dữ liệu, $N$ sử dụng $=2400$):
<br><span class="en">**FD** (`plm(..., model = "fd")`, same data, $N$ used $=2400$):</span>

| Biến - <span class="en">Variable</span> | Hệ số - <span class="en">Coefficient</span> | SE | t |
|---|---|---|---|
| $y_{i,t-1}$ (lag output) | **0.332** | 0.01751 | 18.95 |
| $\log(capital)$ | 0.190 | 0.00664 | 28.64 |
| $\log(labor)$ | 0.017 | 0.00933 | 1.82 |
| `training` | 0.038 | 0.00142 | 26.92 |
| `credit` | 0.032 | 0.01130 | 2.84 |
| `hightech` | 0.121 | 0.01601 | 7.57 |

Đây là minh chứng thực nghiệm sống động nhất cho Nickell bias: **cùng một dữ liệu, cùng một tham số thật cần ước lượng**, nhưng FE cho $\hat\alpha=0.742$ trong khi FD cho $\hat\alpha=0.332$ — chênh lệch hơn gấp đôi. Vì cả hai đều là ước lượng chệch (theo hai cơ chế/phép biến đổi khác nhau), chúng không có lý do gì để trùng khớp — và khoảng cách lớn giữa hai con số chính là dấu hiệu cho thấy có một vấn đề hệ thống (không phải nhiễu ngẫu nhiên) đang chi phối cả hai.
<br><span class="en">This is the most vivid empirical demonstration of Nickell bias: **the same data, the same true parameter to be estimated**, yet FE gives $\hat\alpha=0.742$ while FD gives $\hat\alpha=0.332$ — a difference of more than double. Since both are biased estimates (through two different mechanisms/transformations), there is no reason for them to coincide — and the large gap between the two numbers is itself the sign that a systematic problem (not random noise) is driving both.</span>

### 2.4 Nickell bias là hàm của $1/T$ — không phải $1/N$ (điểm hay hiểu nhầm nhất) - <span class="en">Nickell bias is a function of $1/T$ — not $1/N$ (the most commonly misunderstood point)</span>

Nickell (1981, *Econometrica*) chứng minh bias trong FE (và cấu trúc tương tự trong FD) là hàm của $\dfrac1T$:
<br><span class="en">Nickell (1981, *Econometrica*) proves that the bias in FE (and the analogous structure in FD) is a function of $\dfrac1T$:</span>

- Khi $T\to\infty$, bias $\to0$ — FE trở nên **consistent** khi panel đủ dài (long panel).
<br><span class="en">As $T\to\infty$, bias $\to0$ — FE becomes **consistent** when the panel is long enough (long panel).</span>
- Với $T$ nhỏ (panel ngắn — phổ biến trong dữ liệu vi mô, ví dụ 5–10 năm), bias **đáng kể**.
<br><span class="en">With small $T$ (short panel — common in micro data, e.g. 5–10 years), the bias is **substantial**.</span>
- **Bias không biến mất dù $N$ lớn** — công thức bias không có $N$ trong đó.
<br><span class="en">**The bias does not vanish even with large $N$** — the bias formula does not contain $N$.</span>

**Đây là điểm hay bị hiểu ngược nhất của cả topic**: nhiều người trực giác nghĩ "cứ có nhiều quan sát (nhiều doanh nghiệp/cá nhân, $N$ lớn) là ước lượng sẽ đáng tin hơn" — điều này đúng với hầu hết các bài toán ước lượng khác (kể cả OLS thường, xem [[concepts/linear-regression-model]]), nhưng **sai với Nickell bias**. Tăng $N$ từ 300 lên 3.000 hay 30.000 doanh nghiệp không giúp gì cho bias này — chỉ có tăng $T$ (quan sát thêm nhiều năm hơn cho *cùng* các doanh nghiệp đó) mới làm bias nhỏ lại. Trong thực tế, $T$ thường bị giới hạn bởi cửa sổ thu thập dữ liệu sẵn có — nên Nickell bias thường là một vấn đề *không tránh được bằng cách thu thập thêm dữ liệu chéo*, mà đòi hỏi phải **đổi ước lượng** (Anderson-Hsiao → Difference GMM → System GMM, các mục dưới đây).
<br><span class="en">**This is the single most commonly reversed point in the whole topic**: many people intuitively think "having more observations (more firms/individuals, large $N$) makes the estimate more trustworthy" — this is true for most other estimation problems (including plain OLS, see [[concepts/linear-regression-model]]), but **false for Nickell bias**. Increasing $N$ from 300 to 3,000 or 30,000 firms does nothing to help this bias — only increasing $T$ (observing more years for the *same* firms) shrinks the bias. In practice, $T$ is usually constrained by the available data-collection window — so Nickell bias is usually a problem that *cannot be avoided by collecting more cross-sectional data*, and instead requires **changing the estimator** (Anderson-Hsiao → Difference GMM → System GMM, the sections below).</span>

> Nickell, S. (1981). Biases in dynamic models with fixed effects. *Econometrica*, 49(6), 1417–1426.

## 3. Anderson-Hsiao (AH) Estimator - <span class="en">Anderson-Hsiao (AH) Estimator</span>

### 3.1 Trực giác - <span class="en">Intuition</span>

**Bước 1 — sai phân bậc 1 để khử $\alpha_i$**: xuất phát từ $y_{it}=\alpha y_{i,t-1}+\beta X_{it}+\alpha_i+\varepsilon_{it}$, lấy sai phân:
<br><span class="en">**Step 1 — first-difference to eliminate $\alpha_i$**: starting from $y_{it}=\alpha y_{i,t-1}+\beta X_{it}+\alpha_i+\varepsilon_{it}$, take differences:</span>

$$\Delta y_{it}=\alpha\Delta y_{i,t-1}+\beta\Delta X_{it}+\Delta\varepsilon_{it}, \qquad \Delta y_{it}=y_{it}-y_{i,t-1}$$

**Bước 2 — nhận ra nội sinh vẫn còn đó**: $\Delta y_{i,t-1}=y_{i,t-1}-y_{i,t-2}$ vẫn tương quan với $\Delta\varepsilon_{it}=\varepsilon_{it}-\varepsilon_{i,t-1}$, vì $y_{i,t-1}$ tương quan với $\varepsilon_{i,t-1}$ (thành phần chung). OLS chạy trực tiếp trên phương trình đã sai phân **vẫn chệch** — sai phân chỉ giải quyết được $\alpha_i$, không giải quyết được nội sinh của biến trễ.
<br><span class="en">**Step 2 — realize the endogeneity is still there**: $\Delta y_{i,t-1}=y_{i,t-1}-y_{i,t-2}$ remains correlated with $\Delta\varepsilon_{it}=\varepsilon_{it}-\varepsilon_{i,t-1}$, because $y_{i,t-1}$ is correlated with $\varepsilon_{i,t-1}$ (the shared component). OLS run directly on the differenced equation **is still biased** — differencing only solves $\alpha_i$, not the endogeneity of the lagged variable.</span>

**Bước 3 — ý tưởng của Anderson & Hsiao**: thay vì OLS, dùng **instrumental variables (IV)** — tìm một biến tương quan mạnh với $\Delta y_{i,t-1}$ (relevance) nhưng không tương quan với $\Delta\varepsilon_{it}$ (exogeneity/validity). Điểm đặc biệt: instrument này **không cần lấy từ nguồn dữ liệu bên ngoài** — nó có sẵn ngay trong chính panel, chỉ cần lùi sâu thêm một kỳ nữa.
<br><span class="en">**Step 3 — Anderson & Hsiao's idea**: instead of OLS, use **instrumental variables (IV)** — find a variable strongly correlated with $\Delta y_{i,t-1}$ (relevance) but uncorrelated with $\Delta\varepsilon_{it}$ (exogeneity/validity). The special point: this instrument **need not come from an external data source** — it is already available within the panel itself, simply by going back one more period.</span>

### 3.2 Hai lựa chọn instrument — đánh đổi mạnh/hợp lệ - <span class="en">Two instrument choices — the strength/validity trade-off</span>

Anderson & Hsiao đề xuất **$y_{i,t-2}$** (ở mức, level) hoặc **$\Delta y_{i,t-2}$** (đã sai phân) làm instrument cho $\Delta y_{i,t-1}$ — cả hai đều là **internal instrument** (nội tại, lấy từ chính biến $y$), và cả hai đều **chỉ dùng một biến duy nhất** (khác biệt cốt lõi so với Difference GMM ở mục 4).
<br><span class="en">Anderson & Hsiao propose **$y_{i,t-2}$** (in level) or **$\Delta y_{i,t-2}$** (differenced) as an instrument for $\Delta y_{i,t-1}$ — both are **internal instruments** (internal, taken from $y$ itself), and both **use only a single variable** (the core difference from Difference GMM in section 4).</span>

| Instrument | Relevance | Exogeneity (Validity) |
|---|---|---|
| $y_{i,t-2}$ (level) | Tương quan **mạnh** với $\Delta y_{i,t-1}=y_{i,t-1}-y_{i,t-2}$ (chia sẻ trực tiếp thành phần $y_{i,t-2}$)<br><span class="en">**Strongly** correlated with $\Delta y_{i,t-1}=y_{i,t-1}-y_{i,t-2}$ (directly shares the component $y_{i,t-2}$)</span> | Cần **giả định không có tự tương quan ở mức (level)** — nếu có, $y_{i,t-2}$ tương quan với $\varepsilon_{i,t-1}$ → invalid<br><span class="en">Requires the **assumption of no serial correlation at level** — if present, $y_{i,t-2}$ is correlated with $\varepsilon_{i,t-1}$ → invalid</span> |
| $\Delta y_{i,t-2}=y_{i,t-2}-y_{i,t-3}$ (difference) | Cũng tương quan với $\Delta y_{i,t-1}$ (cả hai đều chứa $y_{i,t-2}$), nhưng **yếu hơn**<br><span class="en">Also correlated with $\Delta y_{i,t-1}$ (both contain $y_{i,t-2}$), but **weaker**</span> | Dưới giả định không tự tương quan ở mức, không tương quan với cả $\varepsilon_{it}$ lẫn $\varepsilon_{i,t-1}$ → **dễ hợp lệ hơn**<br><span class="en">Under the no-serial-correlation-at-level assumption, uncorrelated with both $\varepsilon_{it}$ and $\varepsilon_{i,t-1}$ → **more easily valid**</span> |

Đúc kết trực giác từ slide: instrument lag-level **thường mạnh nhưng dễ không hợp lệ** (nếu có tự tương quan); instrument lag-diff **thường yếu hơn nhưng dễ hợp lệ hơn**. Đây là một đánh đổi kinh điển giữa relevance và exogeneity trong chọn instrument.
<br><span class="en">The slide's intuition in a nutshell: the lag-level instrument is **usually strong but easily invalid** (if serial correlation is present); the lag-diff instrument is **usually weaker but more easily valid**. This is a classic trade-off between relevance and exogeneity in instrument choice.</span>

### 3.3 Ví dụ thực nghiệm — đối chiếu trực tiếp hai lựa chọn instrument - <span class="en">Empirical example — direct comparison of the two instrument choices</span>

Đây là minh họa giá trị nhất của cả mục AH: cùng một phương trình, chỉ đổi instrument, kết quả khác biệt rõ rệt (ước lượng bằng `fixest::feols` theo phương pháp TSLS trên dữ liệu đã sai phân):
<br><span class="en">This is the most valuable illustration in the whole AH section: the same equation, only the instrument changes, and the results differ markedly (estimated with `fixest::feols` using TSLS on the differenced data):</span>

| | Lag-level ($y_{i,t-2}$) | Lag-diff ($\Delta y_{i,t-2}$) |
|---|---|---|
| $\hat\alpha$ (hệ số lag output)<br><span class="en">$\hat\alpha$ (lag-output coefficient)</span> | 0.850 | 0.883 |
| SE | 0.122 | **0.712** |
| t | 6.98 | 1.24 (n.s., $p=0.215$) |
| First-stage F | **69.59** ($p<2.2\times10^{-16}$) | **2.11** ($p=0.146$) |
| Wu-Hausman | 25.77 ($p=4.1\times10^{-7}$) | 0.93 ($p=0.336$) |
| Đánh giá<br><span class="en">Assessment</span> | Instrument **mạnh**, nhưng khả năng **không hợp lệ** nếu có tự tương quan ở mức<br><span class="en">Instrument **strong**, but potentially **invalid** if serial correlation at level is present</span> | Instrument **yếu** (F « 10 — dưới ngưỡng kinh nghiệm được nêu ở mục 7), nhưng dễ hợp lệ hơn<br><span class="en">Instrument **weak** (F « 10 — below the rule-of-thumb threshold given in section 7), but more easily valid</span> |

Đây chính xác là hai chú thích của slide gốc: instrument lag-level "appear to be strong, but likely invalid (due to serial correlation)"; instrument lag-diff "appear to be weak, but likely valid." Quan sát số liệu càng làm rõ hệ quả: khi chuyển từ instrument mạnh sang instrument yếu, SE của $\hat\alpha$ tăng gần **6 lần** (từ 0.122 lên 0.712), và hệ số vốn có ý nghĩa thống kê mạnh (t=6.98) trở thành **không còn ý nghĩa thống kê** (t=1.24) — một minh họa sinh động cho vấn đề **weak instrument** đã học ở [[concepts/endogeneity-iv-regression]]: instrument yếu không chỉ làm ước lượng kém chính xác, mà còn có thể khiến một kiểm định giả thuyết đúng lẽ ra có ý nghĩa lại "biến mất" chỉ vì độ bất định quá lớn.
<br><span class="en">This is exactly the original slide's two annotations: the lag-level instrument "appear to be strong, but likely invalid (due to serial correlation)"; the lag-diff instrument "appear to be weak, but likely valid." The numbers make the consequence even clearer: switching from the strong instrument to the weak one, the SE of $\hat\alpha$ increases almost **6-fold** (from 0.122 to 0.712), and a coefficient that was strongly statistically significant (t=6.98) becomes **no longer statistically significant** (t=1.24) — a vivid illustration of the **weak instrument** problem already covered in [[concepts/endogeneity-iv-regression]]: a weak instrument not only makes the estimate less precise, it can also make a hypothesis test that should be significant "disappear" simply because of excessive uncertainty.</span>

### 3.4 Mở rộng cho biến nội sinh khác — ví dụ `training` - <span class="en">Extension to other endogenous variables — the `training` example</span>

Với mô hình đầy đủ có thêm biến nội sinh $Y_{it}$ (`training`), sau khi sai phân, cả $\Delta y_{i,t-1}$ lẫn $\Delta Y_{it}$ đều cần instrument. Có thể dùng $Y_{i,t-2}$ làm internal instrument cho $\Delta Y_{it}$ nếu thỏa hai điều kiện:
<br><span class="en">With the full model that adds an endogenous variable $Y_{it}$ (`training`), after differencing, both $\Delta y_{i,t-1}$ and $\Delta Y_{it}$ need instruments. $Y_{i,t-2}$ can be used as an internal instrument for $\Delta Y_{it}$ if two conditions hold:</span>

- **Sức mạnh (relevance)**: cần $Y_{it}$ đủ **persistent** — nếu $Y_{it}=\rho Y_{i,t-1}+v_{it}$ với $\rho$ đủ lớn, $Y_{i,t-2}$ dự đoán tốt $\Delta Y_{it}=Y_{it}-Y_{i,t-1}$.
<br><span class="en">**Strength (relevance)**: $Y_{it}$ needs to be sufficiently **persistent** — if $Y_{it}=\rho Y_{i,t-1}+v_{it}$ with $\rho$ large enough, $Y_{i,t-2}$ predicts $\Delta Y_{it}=Y_{it}-Y_{i,t-1}$ well.</span>
- **Tính hợp lệ (validity)**: cần $E[Y_{i,t-2}\cdot\Delta\varepsilon_{it}]=0$ — tương đương yêu cầu **không có tự tương quan ở mức** của $\varepsilon_{it}$.
<br><span class="en">**Validity**: requires $E[Y_{i,t-2}\cdot\Delta\varepsilon_{it}]=0$ — equivalent to requiring **no serial correlation at level** of $\varepsilon_{it}$.</span>

Nếu một trong hai điều kiện không thỏa, cần **external instrument** $\Delta IV_{it}$ (`subeligible`, `localbudget`, ở dạng sai phân để khớp với vế trái đã sai phân).
<br><span class="en">If either condition fails, an **external instrument** $\Delta IV_{it}$ is needed (`subeligible`, `localbudget`, in differenced form to match the differenced left-hand side).</span>

**Ví dụ thực nghiệm** — AH với cả hai biến nội sinh ($y_{i,t-1}$ instrumented bởi $y_{i,t-2}$, `training` instrumented bởi `training`$_{t-1}$):
<br><span class="en">**Empirical example** — AH with both endogenous variables ($y_{i,t-1}$ instrumented by $y_{i,t-2}$, `training` instrumented by `training`$_{t-1}$):</span>

| Biến - <span class="en">Variable</span> | Hệ số - <span class="en">Coefficient</span> | SE | t |
|---|---|---|---|
| $y_{i,t-1}$ | 0.850 | 0.127 | 6.71 |
| `training` | 0.050 | 0.008 | 6.64 |
| $\log(capital)$ | 0.254 | 0.016 | 15.75 |

First-stage F cho $y_{i,t-1}$: 430.14; first-stage F cho `training`: 1.112,77 — cả hai instrument đều **rất mạnh**. Wu-Hausman = 120.99 ($p<2.2\times10^{-16}$) — bằng chứng thống kê rất mạnh cho nội sinh, xác nhận việc dùng IV (thay vì FE/FD ngây thơ) là cần thiết.
<br><span class="en">First-stage F for $y_{i,t-1}$: 430.14; first-stage F for `training`: 1,112.77 — both instruments are **very strong**. Wu-Hausman = 120.99 ($p<2.2\times10^{-16}$) — very strong statistical evidence of endogeneity, confirming that using IV (instead of naive FE/FD) is necessary.</span>

### 3.5 Hạn chế của AH: just-identified - <span class="en">Limitation of AH: just-identified</span>

AH chỉ dùng **một lag duy nhất** làm instrument cho mỗi biến nội sinh → mô hình **just-identified** (số instrument = số biến nội sinh, vừa đủ để nhận diện, không dư). Hạn chế: không tận dụng hết thông tin sẵn có trong cấu trúc panel (còn nhiều lag sâu hơn — $y_{i,t-3}, y_{i,t-4}$… — cũng có thể là instrument hợp lệ nhưng bị bỏ qua), và không có overidentifying restrictions nào để kiểm định (vì không có "dư" instrument). Đây chính là động lực cho **Difference GMM** — xem [[people/arellano-bond]] cho mạch phát triển đầy đủ Anderson-Hsiao → Arellano-Bond → Arellano-Bover/Blundell-Bond.
<br><span class="en">AH uses only **a single lag** as the instrument for each endogenous variable → the model is **just-identified** (number of instruments = number of endogenous variables, just enough to identify, no surplus). Limitation: it does not exploit all the information available in the panel structure (deeper lags — $y_{i,t-3}, y_{i,t-4}$… — could also be valid instruments but are ignored), and there are no overidentifying restrictions to test (since there is no "surplus" instrument). This is precisely the motivation for **Difference GMM** — see [[people/arellano-bond]] for the full development thread Anderson-Hsiao → Arellano-Bond → Arellano-Bover/Blundell-Bond.</span>

## 4. Difference GMM: Arellano-Bond (AB) Estimator - <span class="en">Difference GMM: Arellano-Bond (AB) Estimator</span>

### 4.1 Trực giác: dùng nhiều lag cùng lúc thay vì chỉ một - <span class="en">Intuition: using many lags at once instead of just one</span>

Ý tưởng cải tiến rất tự nhiên: nếu $y_{i,t-2}$ là instrument hợp lệ cho $\Delta y_{i,t-1}$ (dưới giả định không tự tương quan ở mức), thì $y_{i,t-3}, y_{i,t-4},\dots$ **cũng hợp lệ với cùng lý do** — chúng đều được xác định trước thời điểm sai số $\Delta\varepsilon_{it}$ phát sinh. Anderson-Hsiao chỉ dùng một trong số đó, "bỏ phí" các điều kiện moment hợp lệ còn lại. Arellano & Bond (1991) đề xuất dùng **đồng thời tất cả** các lag hợp lệ này làm một bộ instrument, đưa bài toán về khung **GMM overidentified**.
<br><span class="en">The natural improvement: if $y_{i,t-2}$ is a valid instrument for $\Delta y_{i,t-1}$ (under the no-serial-correlation-at-level assumption), then $y_{i,t-3}, y_{i,t-4},\dots$ **are valid for the same reason** — they are all determined before the error $\Delta\varepsilon_{it}$ arises. Anderson-Hsiao uses only one of them, "wasting" the remaining valid moment conditions. Arellano & Bond (1991) propose using **all** of these valid lags **simultaneously** as a set of instruments, casting the problem into an **overidentified GMM** framework.</span>

Trực giác cho việc "nhiều instrument hơn = hiệu quả hơn": mỗi lag thêm vào là một **điều kiện moment** (moment condition) bổ sung — càng nhiều điều kiện dùng để "ràng buộc" nghiệm ước lượng, thông tin từ dữ liệu được khai thác càng triệt để, và (nếu tất cả instrument đều hợp lệ) phương sai của ước lượng càng nhỏ.
<br><span class="en">The intuition for "more instruments = more efficient": each additional lag is one more **moment condition** — the more conditions used to "constrain" the estimated solution, the more thoroughly the information in the data is exploited, and (if all instruments are valid) the smaller the variance of the estimate.</span>

Với phương trình sai phân $\Delta y_{it}=\alpha\Delta y_{i,t-1}+\beta\Delta X_{it}+\Delta\varepsilon_{it}$, dùng $y_{i,t-s}$ ($s\ge2$) làm instrument, điều kiện moment là:
<br><span class="en">For the differenced equation $\Delta y_{it}=\alpha\Delta y_{i,t-1}+\beta\Delta X_{it}+\Delta\varepsilon_{it}$, using $y_{i,t-s}$ ($s\ge2$) as instruments, the moment condition is:</span>

$$E[y_{i,t-s}\cdot\Delta\varepsilon_{it}]=0$$

Áp dụng khung GMM (giống [[concepts/endogeneity-iv-regression]]): sample moment $g(\theta)=\frac1N\sum_i Z_i'\Delta e_i(\theta)$ (với $Z_i$ là ma trận xếp toàn bộ các lag hợp lệ làm instrument cho từng $i$), tiêu chí $J(\theta)=g(\theta)'Wg(\theta)$. Ước lượng **hiệu quả (efficient)** khi $W=S^{-1}$, với $S=\frac1n Z'\,\text{diag}(e^2)\,Z$ (ma trận trọng số robust với heteroskedasticity).
<br><span class="en">Applying the GMM framework (same as [[concepts/endogeneity-iv-regression]]): sample moment $g(\theta)=\frac1N\sum_i Z_i'\Delta e_i(\theta)$ (where $Z_i$ is the matrix stacking all valid lags used as instruments for each $i$), criterion $J(\theta)=g(\theta)'Wg(\theta)$. The estimator is **efficient** when $W=S^{-1}$, with $S=\frac1n Z'\,\text{diag}(e^2)\,Z$ (a weighting matrix robust to heteroskedasticity).</span>

### 4.2 Sức mạnh instrument phụ thuộc độ bền vững (persistence) của $y$ - <span class="en">Instrument strength depends on the persistence of $y$</span>

Xét quá trình $y_{it}=\rho y_{i,t-1}$: nếu **persistent** (nghĩa là $\rho$ lớn), $y_{i,t-2}$ dự đoán tốt $y_{i,t-1}$, do đó dự đoán tốt $\Delta y_{i,t-1}$ — AB tận dụng thêm được **nhiều lag** ($y_{i,t-2}, y_{i,t-3},\dots$) để tăng sức mạnh tổng thể của bộ instrument, ngay cả khi từng lag riêng lẻ chỉ tương quan vừa phải.
<br><span class="en">Consider the process $y_{it}=\rho y_{i,t-1}$: if **persistent** (i.e. $\rho$ is large), $y_{i,t-2}$ predicts $y_{i,t-1}$ well, and hence predicts $\Delta y_{i,t-1}$ well — AB can additionally exploit **many lags** ($y_{i,t-2}, y_{i,t-3},\dots$) to increase the overall strength of the instrument set, even when each individual lag is only moderately correlated.</span>

Hai trường hợp cực đoan gây vấn đề:
<br><span class="en">Two extreme cases cause problems:</span>

- $\rho=0$: biến trễ hoàn toàn không liên quan — đưa vào mô hình vô nghĩa (không có gì để instrument).
<br><span class="en">$\rho=0$: the lagged variable is entirely irrelevant — including it in the model is meaningless (nothing to instrument).</span>
- $\rho\approx1$ (gần unit root/random walk): $\Delta y_{i,t-1}\approx0$ (biến thiên rất ít qua các kỳ) → **mọi lag đều trở thành instrument yếu cùng lúc** — không thể khắc phục bằng cách thêm lag, vì vấn đề nằm ở bản chất chuỗi gần như không đổi, không phải ở số lượng instrument. Đây chính là động lực trực tiếp dẫn đến **System GMM** (mục 6).
<br><span class="en">$\rho\approx1$ (near unit root/random walk): $\Delta y_{i,t-1}\approx0$ (varies very little across periods) → **every lag simultaneously becomes a weak instrument** — this cannot be fixed by adding more lags, because the problem lies in the near-constant nature of the series, not in the number of instruments. This is the direct motivation leading to **System GMM** (section 6).</span>

### 4.3 Tính hợp lệ (validity) — kết nối với AR(1)/AR(2) ở mức - <span class="en">Validity — the connection to AR(1)/AR(2) at level</span>

Điều kiện hợp lệ của $y_{i,t-2}$: cần $E[\Delta\varepsilon_{it}\cdot y_{i,t-2}]=0$. Vì $\Delta\varepsilon_{it}=\varepsilon_{it}-\varepsilon_{i,t-1}$, điều này đòi hỏi $y_{i,t-2}$ không tương quan với **cả** $\varepsilon_{it}$ **lẫn** $\varepsilon_{i,t-1}$:
<br><span class="en">The validity condition for $y_{i,t-2}$: requires $E[\Delta\varepsilon_{it}\cdot y_{i,t-2}]=0$. Since $\Delta\varepsilon_{it}=\varepsilon_{it}-\varepsilon_{i,t-1}$, this requires $y_{i,t-2}$ to be uncorrelated with **both** $\varepsilon_{it}$ **and** $\varepsilon_{i,t-1}$:</span>

- Nếu có **AR(1) ở mức** (level) trong $\varepsilon_{it}$: $y_{i,t-2}$ tương quan với $\varepsilon_{i,t-1}$ → instrument **không hợp lệ**.
<br><span class="en">If there is **AR(1) at level** in $\varepsilon_{it}$: $y_{i,t-2}$ is correlated with $\varepsilon_{i,t-1}$ → the instrument is **invalid**.</span>
- Nếu có **AR(2) ở mức**: $y_{i,t-2}$ tương quan cả với $\varepsilon_{it}$ → **càng không hợp lệ**.
<br><span class="en">If there is **AR(2) at level**: $y_{i,t-2}$ is also correlated with $\varepsilon_{it}$ → **even more invalid**.</span>

**Hệ quả kiểm định quan trọng nhất của cả topic** (giải thích đầy đủ ở mục 7.2): trong phần dư đã sai phân, ta **luôn kỳ vọng** thấy AR(1) một cách cơ học (vì $\Delta\varepsilon_{it}$ và $\Delta\varepsilon_{i,t-1}$ đều chứa chung $\varepsilon_{i,t-1}$) nhưng **không nên** thấy AR(2) — nếu thấy, đó là bằng chứng có tự tương quan thực sự ở mức, làm hỏng tính hợp lệ của instrument.
<br><span class="en">**The most important testing implication of the whole topic** (fully explained in section 7.2): in the differenced residuals, we **always expect** to see AR(1) mechanically (because $\Delta\varepsilon_{it}$ and $\Delta\varepsilon_{i,t-1}$ both share $\varepsilon_{i,t-1}$) but we **should not** see AR(2) — if we do, it is evidence of genuine serial correlation at level, which breaks the validity of the instrument.</span>

### 4.4 Ví dụ thực nghiệm: Arellano-Bond / Difference GMM - <span class="en">Empirical example: Arellano-Bond / Difference GMM</span>

Đặc tả trong R (`plm::pgmm`): chỉ `lag(output)` được coi là nội sinh, dùng **lag 2, 3 và 4 của output** làm instrument đồng thời (đúng ý tưởng "nhiều lag cùng lúc" ở mục 4.1); các regressor khác (kể cả `training`) tạm coi là ngoại sinh trong đặc tả này; two-step GMM, transformation = "d" (difference).
<br><span class="en">Specification in R (`plm::pgmm`): only `lag(output)` is treated as endogenous, using **lags 2, 3, and 4 of output** simultaneously as instruments (exactly the "many lags at once" idea from section 4.1); other regressors (including `training`) are temporarily treated as exogenous in this specification; two-step GMM, transformation = "d" (difference).</span>

| Biến - <span class="en">Variable</span> | Hệ số - <span class="en">Coefficient</span> | SE | z |
|---|---|---|---|
| $y_{i,t-1}$ (lag output) | **0.822** | **0.021** | 38.53 |
| $\log(capital)$ | 0.239 | 0.011 | 21.78 |
| $\log(labor)$ | −0.0005 | 0.017 | −0.03 (n.s.) |
| `training` | 0.052 | 0.002 | 22.04 |
| `credit` | 0.065 | 0.019 | 3.42 |
| `hightech` | 0.200 | 0.027 | 7.48 |

So với AH lag-level ($\hat\alpha=0.850$, SE $=0.122$), Difference GMM cho $\hat\alpha=0.822$ với SE $=0.021$ — **SE giảm khoảng 6 lần** nhờ dùng 3 instrument (lag 2–4) thay vì 1. Đây là minh chứng thực nghiệm trực tiếp cho lợi ích hiệu quả (efficiency gain) của việc dùng nhiều điều kiện moment cùng lúc thay vì chỉ một, đúng như trực giác nêu ở mục 4.1.
<br><span class="en">Compared to AH lag-level ($\hat\alpha=0.850$, SE $=0.122$), Difference GMM gives $\hat\alpha=0.822$ with SE $=0.021$ — **SE falls by roughly 6-fold** thanks to using 3 instruments (lags 2–4) instead of 1. This is direct empirical evidence for the efficiency gain from using many moment conditions at once instead of just one, exactly as the intuition in section 4.1 predicts.</span>

Bộ kiểm định chẩn đoán đi kèm (diễn giải đầy đủ ở mục 7.2):
<br><span class="en">The accompanying diagnostic tests (fully interpreted in section 7.2):</span>

- **Sargan**: $\chi^2(69)=51.792$, $p=0.939$ — không bác bỏ → phù hợp với overidentifying restrictions.
<br><span class="en">**Sargan**: $\chi^2(69)=51.792$, $p=0.939$ — not rejected → consistent with the overidentifying restrictions.</span>
- **AR(1)**: $z=-12.346$, $p\approx0$ → **bác bỏ mạnh** → đây là điều **được kỳ vọng**, dấu hiệu tốt.
<br><span class="en">**AR(1)**: $z=-12.346$, $p\approx0$ → **strongly rejected** → this is the **expected** outcome, a good sign.</span>
- **AR(2)**: $z=-0.777$, $p=0.437$ → **không bác bỏ** → cũng là điều được kỳ vọng, ủng hộ tính hợp lệ của bộ instrument (lag 2–4).
<br><span class="en">**AR(2)**: $z=-0.777$, $p=0.437$ → **not rejected** → also the expected outcome, supporting the validity of the instrument set (lags 2–4).</span>

### 4.5 Mở rộng: biến nội sinh khác (`training`) trong Difference GMM - <span class="en">Extension: other endogenous variables (`training`) in Difference GMM</span>

Khi `training` cũng được coi là nội sinh: $\Delta training_{it}$ cần instrument riêng. Hai lựa chọn tương tự mục 3.4:
<br><span class="en">When `training` is also treated as endogenous: $\Delta training_{it}$ needs its own instrument. Two choices similar to section 3.4:</span>

- **Internal**: lag 2 và 3 của `training` (ở mức) — nếu đủ mạnh (persistent) và hợp lệ (không tự tương quan ở mức).
<br><span class="en">**Internal**: lags 2 and 3 of `training` (in level) — if sufficiently strong (persistent) and valid (no serial correlation at level).</span>
- **External**: `subeligible` và `localbudget` — dùng khi lag nội tại không đủ mạnh/hợp lệ.
<br><span class="en">**External**: `subeligible` and `localbudget` — used when the internal lags are not strong/valid enough.</span>

Điều kiện strength/validity giống hệt lập luận ở mục 3.4 (chỉ thay $Y_{i,t-2}$ cho `training`): cần $Y_{it}=\rho Y_{i,t-1}+v_{it}$ đủ persistent để $Y_{i,t-2}$ dự đoán tốt $\Delta Y_{it}$, và cần $E[Y_{i,t-2}\cdot\Delta\varepsilon_{it}]=0$.
<br><span class="en">The strength/validity conditions are identical to the argument in section 3.4 (just substitute $Y_{i,t-2}$ for `training`): $Y_{it}=\rho Y_{i,t-1}+v_{it}$ must be persistent enough for $Y_{i,t-2}$ to predict $\Delta Y_{it}$ well, and $E[Y_{i,t-2}\cdot\Delta\varepsilon_{it}]=0$ must hold.</span>

## 5. Predetermined regressors - <span class="en">Predetermined regressors</span>

Một biến $P_{it}$ được gọi là **predetermined** nếu thỏa đồng thời hai điều kiện:
<br><span class="en">A variable $P_{it}$ is called **predetermined** if it satisfies both conditions simultaneously:</span>

$$E[P_{it}\cdot\varepsilon_{i,t+s}]=0,\ \forall s\ge0 \qquad\text{(không tương quan với sai số hiện tại/tương lai)}$$
$$E[P_{it}\cdot\varepsilon_{i,t-1}]\neq0 \text{ được phép} \qquad\text{(được phép tương quan với sai số quá khứ)}$$
<br><span class="en">$$E[P_{it}\cdot\varepsilon_{i,t+s}]=0,\ \forall s\ge0 \qquad\text{(uncorrelated with current/future errors)}$$
$$E[P_{it}\cdot\varepsilon_{i,t-1}]\neq0 \text{ allowed} \qquad\text{(allowed to be correlated with past errors)}$$</span>

**Ví dụ**: đầu tư phản ứng với cú sốc năng suất/lợi nhuận **trong quá khứ** — quyết định đầu tư hôm nay được lập ra dựa trên thông tin đã biết đến hôm qua, nên nó "biết" về $\varepsilon_{i,t-1}$ nhưng chưa thể "biết" trước $\varepsilon_{it}$ hay $\varepsilon_{i,t+1}$.
<br><span class="en">**Example**: investment reacts to productivity/profit shocks **in the past** — today's investment decision is made based on information already known up to yesterday, so it "knows" about $\varepsilon_{i,t-1}$ but cannot yet "know" $\varepsilon_{it}$ or $\varepsilon_{i,t+1}$ in advance.</span>

**Điểm tinh tế nhất cần nhớ**: biến predetermined **ngoại sinh ở mức (level)** nhưng **trở thành nội sinh sau khi sai phân**. Sau FD:
<br><span class="en">**The most subtle point to remember**: a predetermined variable is **exogenous at level** but **becomes endogenous after differencing**. After FD:</span>

$$\Delta P_{it}\cdot\Delta\varepsilon_{it} = (P_{it}-P_{i,t-1})(\varepsilon_{it}-\varepsilon_{i,t-1})$$

Khai triển kỳ vọng:
<br><span class="en">Expanding the expectation:</span>

$$E[\Delta P_{it}\Delta\varepsilon_{it}]=E[P_{it}\varepsilon_{it}]+E[P_{it}\varepsilon_{i,t-1}]+E[P_{i,t-1}\varepsilon_{it}]+E[P_{i,t-1}\varepsilon_{i,t-1}]$$

(dấu của từng số hạng phụ thuộc cách khai triển tích hai hiệu; điều quan trọng là **liệt kê đủ 4 số hạng chéo**). Áp định nghĩa predetermined cho từng số hạng:
<br><span class="en">(the sign of each term depends on how the product of the two differences is expanded; what matters is **listing all 4 cross terms**). Applying the predetermined definition to each term:</span>

- $E[P_{it}\varepsilon_{it}]=0$ (trường hợp $s=0$ trong định nghĩa, áp cho $P_{it}$).
<br><span class="en">$E[P_{it}\varepsilon_{it}]=0$ (the case $s=0$ in the definition, applied to $P_{it}$).</span>
- $E[P_{i,t-1}\varepsilon_{it}]=0$ ($P_{i,t-1}$ không tương quan với sai số *tương lai* $\varepsilon_{it}$).
<br><span class="en">$E[P_{i,t-1}\varepsilon_{it}]=0$ ($P_{i,t-1}$ is uncorrelated with the *future* error $\varepsilon_{it}$).</span>
- $E[P_{i,t-1}\varepsilon_{i,t-1}]=0$ (trường hợp $s=0$ áp cho $P_{i,t-1}$ tại chính kỳ $t-1$ của nó).
<br><span class="en">$E[P_{i,t-1}\varepsilon_{i,t-1}]=0$ (the case $s=0$ applied to $P_{i,t-1}$ at its own period $t-1$).</span>
- $E[P_{it}\varepsilon_{i,t-1}]\neq0$ — **đây chính là số hạng "sống sót"**, khác 0 theo đúng định nghĩa predetermined (được phép tương quan với sai số quá khứ).
<br><span class="en">$E[P_{it}\varepsilon_{i,t-1}]\neq0$ — **this is precisely the "surviving" term**, nonzero exactly as the predetermined definition allows (permitted to correlate with the past error).</span>

Kết luận (giữ nguyên như slide): $E[P_{it}\varepsilon_{i,t-1}]\neq0$, nên $\Delta P_{it}$ **nội sinh** trong phương trình đã sai phân, dù $P_{it}$ hoàn toàn "an toàn" ở mức level. Bài học thực hành: **ngay cả những biến quen được coi là "chắc chắn ngoại sinh"** (vì chúng phản ứng với quá khứ chứ không dự đoán trước tương lai) vẫn cần được xử lý như biến nội sinh một khi mô hình được sai phân để khử $\alpha_i$ — không thể mặc định giữ chúng ở vế phải mà không instrument.
<br><span class="en">Conclusion (kept as in the slide): $E[P_{it}\varepsilon_{i,t-1}]\neq0$, so $\Delta P_{it}$ is **endogenous** in the differenced equation, even though $P_{it}$ is entirely "safe" at level. Practical lesson: **even variables commonly regarded as "certainly exogenous"** (because they react to the past rather than anticipate the future) must still be treated as endogenous once the model is differenced to eliminate $\alpha_i$ — they cannot be left on the right-hand side by default without instrumenting.</span>

## 6. System GMM: Arellano-Bover / Blundell-Bond Estimator - <span class="en">System GMM: Arellano-Bover / Blundell-Bond Estimator</span>

### 6.1 Động lực trực quan - <span class="en">Intuitive motivation</span>

Đã thấy ở mục 4.2: khi $y$ có tính bền vững cao (highly persistent, $\rho$ gần 1), biến trễ **ở mức** trở thành instrument **yếu** cho biến **đã sai phân** (vì bản thân biến đã sai phân biến thiên rất ít). Ba hệ quả slide liệt kê rõ: **biased estimates** (ước lượng chệch), **weak identification** (nhận diện yếu), **poor performance in finite samples** (hoạt động kém ở mẫu hữu hạn).
<br><span class="en">Already seen in section 4.2: when $y$ is highly persistent ($\rho$ near 1), the lagged variable **at level** becomes a **weak** instrument for the **differenced** variable (because the differenced variable itself varies very little). The slide lists three consequences clearly: **biased estimates**, **weak identification**, **poor performance in finite samples**.</span>

### 6.2 Ý tưởng cốt lõi: "xếp chồng" phương trình sai phân và phương trình mức - <span class="en">Core idea: "stacking" the differenced equation and the level equation</span>

Giải pháp: bổ sung thêm **điều kiện moment ở mức (levels)** để tăng cường bộ instrument — kết hợp đồng thời **phương trình sai phân** (giống Arellano-Bond) và **phương trình mức** thành một "hệ thống" (system) duy nhất. Đóng góp: **Arellano & Bover (1995)** đề xuất ý tưởng hệ thống; **Blundell & Bond (1998)** hình thức hóa điều kiện moment đảm bảo tính vững.
<br><span class="en">Solution: add extra **moment conditions at level (levels)** to strengthen the instrument set — combining the **differenced equation** (like Arellano-Bond) and the **level equation** simultaneously into a single "system." Contribution: **Arellano & Bover (1995)** proposed the system idea; **Blundell & Bond (1998)** formalized the moment conditions ensuring consistency.</span>

Trực giác của "phép hoán đổi" thông minh này: phương trình sai phân cần instrument **ở mức** cho biến **đã sai phân** (như AB) — yếu khi $y$ rất persistent. Phương trình mức thì ngược lại, cần instrument cho biến **ở mức** $y_{i,t-1}$ (vốn tương quan với $\alpha_i$ chưa bị khử) — và ở đây, biến **đã sai phân** $\Delta y_{i,t-1}$ lại đóng vai trò instrument tốt, vì sai phân đã loại bỏ $\alpha_i$ nên không còn tương quan với $\alpha_i$ trong phương trình mức (với điều kiện tính dừng, xem mục 6.4–6.5). Hai phương trình "bù trừ" điểm yếu cho nhau.
<br><span class="en">The intuition behind this clever "swap": the differenced equation needs an instrument **at level** for the **differenced** variable (like AB) — weak when $y$ is highly persistent. The level equation, conversely, needs an instrument for the variable **at level** $y_{i,t-1}$ (which is correlated with $\alpha_i$, not yet eliminated) — and here the **differenced** variable $\Delta y_{i,t-1}$ serves as a good instrument, because differencing has already removed $\alpha_i$, so it is no longer correlated with $\alpha_i$ in the level equation (subject to the stationarity condition, see sections 6.4–6.5). The two equations "compensate" for each other's weaknesses.</span>

- **Phương trình sai phân**: $\Delta y_{it}=\alpha\Delta y_{i,t-1}+\beta\Delta X_{it}+\Delta\varepsilon_{it}$, moment: $E[y_{i,t-s}\cdot\Delta\varepsilon_{it}]=0$ (dùng $y_{i,t-s}$ làm instrument, giống hệt Difference GMM).
<br><span class="en">**Differenced equation**: $\Delta y_{it}=\alpha\Delta y_{i,t-1}+\beta\Delta X_{it}+\Delta\varepsilon_{it}$, moment: $E[y_{i,t-s}\cdot\Delta\varepsilon_{it}]=0$ (using $y_{i,t-s}$ as instrument, exactly like Difference GMM).</span>
- **Phương trình mức**: $y_{it}=\alpha y_{i,t-1}+\beta X_{it}+\alpha_i+\varepsilon_{it}$, moment: $E[\Delta y_{i,t-1}\cdot(\alpha_i+\varepsilon_{it})]=0$ (dùng **$\Delta y_{i,t-1}$** làm instrument cho $y_{i,t-1}$ ở phương trình mức).
<br><span class="en">**Level equation**: $y_{it}=\alpha y_{i,t-1}+\beta X_{it}+\alpha_i+\varepsilon_{it}$, moment: $E[\Delta y_{i,t-1}\cdot(\alpha_i+\varepsilon_{it})]=0$ (using **$\Delta y_{i,t-1}$** as instrument for $y_{i,t-1}$ in the level equation).</span>

### 6.3 Ước lượng: xếp chồng (stacking) hai vector moment - <span class="en">Estimation: stacking the two moment vectors</span>

Gọi $Z_i^D$ là ma trận instrument của phương trình sai phân (moment $E[Z_i^{D\prime}\cdot\Delta\varepsilon_i]=0$) và $Z_i^L$ là ma trận instrument của phương trình mức (moment $E[Z_i^{L\prime}\cdot(\alpha_i+\varepsilon_i)]=0$). Vector moment mẫu được xếp chồng:
<br><span class="en">Let $Z_i^D$ be the instrument matrix of the differenced equation (moment $E[Z_i^{D\prime}\cdot\Delta\varepsilon_i]=0$) and $Z_i^L$ be the instrument matrix of the level equation (moment $E[Z_i^{L\prime}\cdot(\alpha_i+\varepsilon_i)]=0$). The stacked sample moment vector:</span>

$$g(\theta)=\begin{bmatrix}g^D(\theta)\\g^L(\theta)\end{bmatrix}=\frac1N\sum_{i=1}^N\begin{bmatrix}Z_i^{D\prime}\cdot\Delta u_i(\theta)\\Z_i^{L\prime}\cdot u_i(\theta)\end{bmatrix}$$

với $\Delta u_i(\theta)$ là phần dư từ phương trình sai phân, $u_i(\theta)$ là phần dư (cộng hằng số) từ phương trình mức. Tiêu chí GMM:
<br><span class="en">where $\Delta u_i(\theta)$ is the residual from the differenced equation, $u_i(\theta)$ is the residual (plus constant) from the level equation. GMM criterion:</span>

$$J(\theta)=g(\theta)'W^{-1}g(\theta), \qquad W=\begin{bmatrix}W^D&0\\0&W^L\end{bmatrix}\ \text{(block-diagonal)}$$

với $W^D$ là VCV của phương trình sai phân, $W^L$ là VCV của phương trình mức. Ước lượng System GMM:
<br><span class="en">where $W^D$ is the VCV of the differenced equation, $W^L$ is the VCV of the level equation. The System GMM estimator:</span>

$$\theta_{GMM}=\arg\min_\theta \begin{bmatrix}g^D(\theta)'&g^L(\theta)'\end{bmatrix}\begin{bmatrix}W^D&0\\0&W^L\end{bmatrix}^{-1}\begin{bmatrix}g^D(\theta)\\g^L(\theta)\end{bmatrix}$$

### 6.4 Instrument cho phương trình mức: sức mạnh và tính hợp lệ - <span class="en">Instrument for the level equation: strength and validity</span>

**Sức mạnh (strength)**: $Cov(y_{i,t-1},\Delta y_{i,t-1})=Var(y_{i,t-1})-Cov(y_{i,t-1},y_{i,t-2})$ — mạnh khi quá trình **không phải unit-root** ($\rho\neq1$). Nếu $\rho=0$, quá trình không có tính động ($\alpha=0$, không có gì để bàn về instrument). Có thể dùng lag sâu hơn ($\Delta y_{i,t-2}$…) nhưng yếu dần; trong thực hành thường dừng ở $\Delta y_{i,t-1}$ — slide còn ghi chú thực tế: hàm `pgmm()` trong R **không hỗ trợ** lag sâu hơn cho phương trình mức.
<br><span class="en">**Strength**: $Cov(y_{i,t-1},\Delta y_{i,t-1})=Var(y_{i,t-1})-Cov(y_{i,t-1},y_{i,t-2})$ — strong when the process is **not unit-root** ($\rho\neq1$). If $\rho=0$, the process has no dynamics ($\alpha=0$, nothing to discuss regarding an instrument). Deeper lags ($\Delta y_{i,t-2}$…) can be used but grow progressively weaker; in practice one usually stops at $\Delta y_{i,t-1}$ — the slide also notes a practical fact: the `pgmm()` function in R **does not support** deeper lags for the level equation.</span>

**Tính hợp lệ (validity)**: cần **đồng thời** hai điều kiện:
<br><span class="en">**Validity**: requires **both** conditions simultaneously:</span>

$$E[\Delta y_{i,t-1}\cdot\varepsilon_{it}]=0 \qquad\text{và}\qquad E[\Delta y_{i,t-1}\cdot\alpha_i]=0$$

Điều kiện thứ nhất giống hệt điều kiện "không tự tương quan ở mức" đã gặp ở AB. Điều kiện thứ hai **mới**, và đòi hỏi **tính dừng (stationarity)** của $y_{it}$: $E[y_{it}\mid\alpha_i]$ không đổi theo $t$.
<br><span class="en">The first condition is identical to the "no serial correlation at level" condition already encountered in AB. The second condition is **new**, and requires **stationarity** of $y_{it}$: $E[y_{it}\mid\alpha_i]$ is constant over $t$.</span>

### 6.5 Điều kiện tính dừng, giải thích đầy đủ qua đại số AR(1) - <span class="en">The stationarity condition, fully explained through AR(1) algebra</span>

Xét quá trình $y_{it}=\alpha_i+\rho y_{i,t-1}+v_{it}$, với $E[v_{it}]=0$. Thế lặp lại đến tận $y_{i0}$:
<br><span class="en">Consider the process $y_{it}=\alpha_i+\rho y_{i,t-1}+v_{it}$, with $E[v_{it}]=0$. Substituting repeatedly back to $y_{i0}$:</span>

$$y_{it}=\alpha_i\left(1+\rho+\rho^2+\cdots+\rho^t\right)+y_{i0}\rho^t+\sum_{k=0}^{t-1}\rho^k v_{i,t-k}$$

> **Lưu ý về nguồn**: số mũ trên cùng của chuỗi hình học $(1+\rho+\cdots+\rho^t)$ bị mờ khi trích xuất từ slide gốc (chồng chữ do OCR) — có thể là $\rho^t$ hoặc $\rho^{t-1}$ tùy góc đọc. Giữ nguyên cách viết đã dùng trong bản wiki trước (khớp với bản trích xuất gốc có sẵn) thay vì tự ý sửa lại theo đại số "chuẩn" (thường $t$ số hạng từ $\rho^0$ đến $\rho^{t-1}$ đi kèm điều kiện đầu $\rho^t y_{i0}$ tách riêng) — bản chất kết luận về ba trường hợp $\rho$ dưới đây không đổi dù chọn cách viết nào.
> <br><span class="en">**Note on the source**: the top exponent of the geometric series $(1+\rho+\cdots+\rho^t)$ is blurred in the extraction from the original slide (text overlap from OCR) — it could be $\rho^t$ or $\rho^{t-1}$ depending on the reading angle. The notation used in the previous wiki version is kept as-is (matching the available original extraction) rather than being unilaterally "corrected" to "standard" algebra (usually $t$ terms from $\rho^0$ to $\rho^{t-1}$ with the initial condition $\rho^t y_{i0}$ kept separate) — the substance of the conclusions about the three cases of $\rho$ below is unchanged regardless of which notation is chosen.</span>

Ba thành phần của biểu thức: $\alpha_i(1+\rho+\rho^2+\cdots)$ là **cân bằng dài hạn** (long-run equilibrium); $y_{i0}\rho^t$ là **điều kiện ban đầu** (initial condition); $\sum_{k=0}^{t-1}\rho^k v_{i,t-k}$ là **cú sốc tích lũy** (accumulated shock).
<br><span class="en">Three components of the expression: $\alpha_i(1+\rho+\rho^2+\cdots)$ is the **long-run equilibrium**; $y_{i0}\rho^t$ is the **initial condition**; $\sum_{k=0}^{t-1}\rho^k v_{i,t-k}$ is the **accumulated shock**.</span>

- **Nếu $\rho=1$**: cân bằng dài hạn **phân kỳ** — không có steady state ($y_{it}$ là random walk, drift không giới hạn theo $t$) → $E[y_{it}\mid\alpha_i]$ **không** hằng số theo $t$ → **không dừng** → instrument $\Delta y_{i,t-1}$ **không hợp lệ**. Đây là một điểm đáng chú ý: System GMM ra đời để giải quyết trường hợp $y$ *rất* persistent (mục 6.1), nhưng chính tại cực điểm $\rho=1$ (unit root), điều kiện định danh riêng của System GMM (tính dừng) lại đổ vỡ — "điểm ngọt" (sweet spot) của System GMM là $\rho$ **gần** 1 nhưng **nhỏ hơn** 1 thực sự, không phải $\rho=1$.
<br><span class="en">**If $\rho=1$**: the long-run equilibrium **diverges** — there is no steady state ($y_{it}$ is a random walk, with unbounded drift over $t$) → $E[y_{it}\mid\alpha_i]$ is **not** constant over $t$ → **non-stationary** → the instrument $\Delta y_{i,t-1}$ is **invalid**. This is a notable point: System GMM was created to address the case of *highly* persistent $y$ (section 6.1), but precisely at the extreme $\rho=1$ (unit root), System GMM's own identification condition (stationarity) breaks down — the "sweet spot" of System GMM is $\rho$ **close to** 1 but **strictly less than** 1, not $\rho=1$.</span>
- **Nếu $\rho=0$**: mức dài hạn $=\alpha_i$, nhưng quá trình **không có tính động** — không có lý do gì để đặc tả mô hình động ngay từ đầu.
<br><span class="en">**If $\rho=0$**: the long-run level $=\alpha_i$, but the process **has no dynamics** — there is no reason to specify a dynamic model in the first place.</span>
- **Nếu $\rho<1$** (trường hợp lý tưởng cho System GMM): mức cân bằng dài hạn **ổn định theo thời gian**:
<br><span class="en">**If $\rho<1$** (the ideal case for System GMM): the long-run equilibrium level is **stable over time**:</span>
$$\mu_i=\frac{\alpha_i}{1-\rho}$$
tính dừng được thỏa mãn, instrument $\Delta y_{i,t-1}$ hợp lệ.
<br><span class="en">stationarity is satisfied, and the instrument $\Delta y_{i,t-1}$ is valid.</span>

### 6.6 Mở rộng: System GMM với biến nội sinh khác (`training`) - <span class="en">Extension: System GMM with other endogenous variables (`training`)</span>

Logic song song hoàn toàn với biến trễ của $y$: nếu `training` cũng persistent và không có tự tương quan ở mức, dùng **`training`$_{t-2}$ (và sâu hơn)** làm instrument cho $\Delta training_{it}$ trong phương trình sai phân, và **$\Delta training_{i,t-1}$** làm instrument cho `training`$_{it}$ trong phương trình mức. Nếu lag nội tại không đủ mạnh/hợp lệ, dùng external instrument (`subeligible`, `localbudget`) cho cả hai phương trình.
<br><span class="en">The logic runs entirely parallel to the lag of $y$: if `training` is also persistent and has no serial correlation at level, use **`training`$_{t-2}$ (and deeper)** as an instrument for $\Delta training_{it}$ in the differenced equation, and **$\Delta training_{i,t-1}$** as an instrument for `training`$_{it}$ in the level equation. If the internal lags are not strong/valid enough, use external instruments (`subeligible`, `localbudget`) for both equations.</span>

### 6.7 Ví dụ thực nghiệm — và áp dụng ngay 3 dấu hiệu gián tiếp kiểm tra tính dừng - <span class="en">Empirical example — and applying the 3 indirect signs for checking stationarity right away</span>

Đặc tả System GMM trong R (`plm::pgmm`, `transformation = "ld"` — level+difference): lag 2–4 của output làm instrument cho phương trình sai phân, $\Delta output_{t-1}$ làm instrument cho phương trình mức.
<br><span class="en">System GMM specification in R (`plm::pgmm`, `transformation = "ld"` — level+difference): lags 2–4 of output as instruments for the differenced equation, $\Delta output_{t-1}$ as instrument for the level equation.</span>

| Biến - <span class="en">Variable</span> | Hệ số - <span class="en">Coefficient</span> | SE | z |
|---|---|---|---|
| $y_{i,t-1}$ (lag output) | **0.9999** | **0.006** | 165.36 |
| $\log(capital)$ | 0.236 | 0.013 | 18.05 |
| $\log(labor)$ | −0.016 | 0.021 | −0.76 (n.s.) |
| `training` | 0.049 | 0.003 | 16.94 |
| `credit` | 0.045 | 0.024 | 1.88 (biên, $p=0.061$) |
| `hightech` | 0.236 | 0.031 | 7.64 |

Sargan: $\chi^2(133)=146.83$, $p=0.195$ (không bác bỏ). AR(1): $z=-12.888$, $p\approx0$ (bác bỏ mạnh — kỳ vọng, tốt). AR(2): $z=-0.629$, $p=0.529$ (không bác bỏ — kỳ vọng, tốt).
<br><span class="en">Sargan: $\chi^2(133)=146.83$, $p=0.195$ (not rejected). AR(1): $z=-12.888$, $p\approx0$ (strongly rejected — expected, good). AR(2): $z=-0.629$, $p=0.529$ (not rejected — expected, good).</span>

So với Difference GMM ($\hat\alpha=0.822$, SE$=0.021$), System GMM cho SE nhỏ hơn nữa (0.006) — đúng như kỳ vọng lý thuyết ở mục 6.1 (thêm điều kiện moment ở mức giúp tăng hiệu quả khi $y$ persistent). Nhưng đây cũng chính là dịp để **áp dụng trực tiếp 3 dấu hiệu gián tiếp kiểm tra tính dừng** mà slide đề xuất (mục 7.5) vào chính bảng số này:
<br><span class="en">Compared to Difference GMM ($\hat\alpha=0.822$, SE$=0.021$), System GMM gives an even smaller SE (0.006) — exactly as the theoretical expectation in section 6.1 predicts (adding moment conditions at level increases efficiency when $y$ is persistent). But this is also the occasion to **directly apply the 3 indirect signs for checking stationarity** proposed by the slide (section 7.5) to this very table of results:</span>

1. **So sánh hệ số Difference GMM và System GMM**: $0.822$ so với $0.9999$ — chênh lệch khoảng $0.18$, **không thực sự "gần nhau"** — đây là một tín hiệu **cảnh báo**, chứ chưa hẳn xác nhận tính dừng.
<br><span class="en">**Compare the Difference GMM and System GMM coefficients**: $0.822$ versus $0.9999$ — a gap of about $0.18$, **not really "close"** — this is a **warning** signal, not confirmation of stationarity.</span>
2. **Kiểm tra $\hat\alpha$ không quá gần 0 hoặc 1**: $\hat\alpha_{SGMM}=0.9999$ — **cực kỳ gần 1** (gần như unit-root/random walk) — chính xác là loại giá trị mà slide dặn phải cảnh giác.
<br><span class="en">**Check that $\hat\alpha$ is not too close to 0 or 1**: $\hat\alpha_{SGMM}=0.9999$ — **extremely close to 1** (near unit-root/random walk) — exactly the kind of value the slide warns to be cautious about.</span>
3. **Vẽ đồ thị $y_{it}$ theo thời gian**: slide không cung cấp dữ liệu để vẽ trực tiếp tại đây, nhưng đây là bước thứ ba bắt buộc trong thực hành để xác nhận trực quan hành vi chuỗi.
<br><span class="en">**Plot $y_{it}$ over time**: the slide does not provide data to plot directly here, but this is the mandatory third step in practice to visually confirm the series' behavior.</span>

**Rút ra**: hai trong ba dấu hiệu gián tiếp, khi áp vào chính ví dụ này, đều gợi ý giả định tính dừng (điều kiện cho tính hợp lệ của instrument phương trình mức, mục 6.4–6.5) **đáng ngờ** — dù các kiểm định chính thức AR(1)/AR(2)/Sargan đều "đẹp" (pass) như thường lệ. Đây là quan sát rút ra bằng cách áp dụng đúng bộ tiêu chí mà slide đã nêu vào chính bảng kết quả mà slide cung cấp — không phải khẳng định mô hình "sai," mà là một lời nhắc thận trọng: **SE rất nhỏ + AR/Sargan pass không tự động đảm bảo tính dừng** — vì không có một kiểm định chính thức duy nhất cho tính dừng trong khung System GMM, ba dấu hiệu gián tiếp này luôn cần được đối chiếu cùng nhau, không dừng lại ở mỗi Sargan/AR "đẹp."
<br><span class="en">**Takeaway**: two of the three indirect signs, when applied to this very example, both suggest the stationarity assumption (the condition for the validity of the level-equation instrument, sections 6.4–6.5) is **questionable** — even though the formal AR(1)/AR(2)/Sargan tests all "look good" (pass) as usual. This is an observation derived by applying exactly the criteria the slide sets out to the very results table the slide provides — not a claim that the model is "wrong," but a cautionary reminder: **a very small SE + passing AR/Sargan tests does not automatically guarantee stationarity** — because there is no single formal test for stationarity within the System GMM framework, these three indirect signs must always be cross-checked together, not stopped at merely a "good-looking" Sargan/AR result.</span>

## 7. Bộ kiểm định chẩn đoán cho mô hình động - <span class="en">Diagnostic test battery for dynamic models</span>

### 7.1 Cho Anderson-Hsiao - <span class="en">For Anderson-Hsiao</span>

- **Instrument relevance/strength**: First-stage F (cho từng biến nội sinh riêng). Lưu ý: **first-stage F-statistic thay đổi theo cấu trúc VCV** dùng để tính — không có một con số F "chuẩn" duy nhất áp dụng mọi trường hợp. Có thể dùng ngưỡng kinh nghiệm không chính thức **$F=10$** (theo tiêu chí relative bias).
<br><span class="en">**Instrument relevance/strength**: First-stage F (for each endogenous variable separately). Note: the **first-stage F-statistic changes with the VCV structure** used to compute it — there is no single "standard" F number that applies to every case. An informal rule-of-thumb threshold of **$F=10$** may be used (based on the relative-bias criterion).</span>
- **Endogeneity**: Wu-Hausman test.
<br><span class="en">**Endogeneity**: Wu-Hausman test.</span>
- **Overidentifying restrictions**: Sargan test (chỉ đáng tin dưới giả định homoskedasticity).
<br><span class="en">**Overidentifying restrictions**: Sargan test (only trustworthy under the homoskedasticity assumption).</span>

### 7.2 AR(1)/AR(2) cho Difference GMM và System GMM — hai quy tắc phản trực giác, giải thích cặn kẽ - <span class="en">AR(1)/AR(2) for Difference GMM and System GMM — two counter-intuitive rules, explained thoroughly</span>

Đây là phần **quan trọng và dễ hiểu ngược nhất** của toàn bộ topic — cả hai kiểm định đều chạy trên **phần dư đã sai phân** $\Delta\hat\varepsilon_{it}$, không phải phần dư ở mức gốc.
<br><span class="en">This is the **most important and most commonly reversed** part of the whole topic — both tests run on the **differenced residuals** $\Delta\hat\varepsilon_{it}$, not the residuals at the original level.</span>

**Quy tắc 1 — AR(1) NÊN bị bác bỏ.** Xét hiệp phương sai giữa $\Delta\varepsilon_{it}=\varepsilon_{it}-\varepsilon_{i,t-1}$ và $\Delta\varepsilon_{i,t-1}=\varepsilon_{i,t-1}-\varepsilon_{i,t-2}$:
<br><span class="en">**Rule 1 — AR(1) SHOULD be rejected.** Consider the covariance between $\Delta\varepsilon_{it}=\varepsilon_{it}-\varepsilon_{i,t-1}$ and $\Delta\varepsilon_{i,t-1}=\varepsilon_{i,t-1}-\varepsilon_{i,t-2}$:</span>

$$Cov(\Delta\varepsilon_{it},\Delta\varepsilon_{i,t-1}) = Cov(\varepsilon_{it},\varepsilon_{i,t-1}) - Cov(\varepsilon_{it},\varepsilon_{i,t-2}) - Var(\varepsilon_{i,t-1}) + Cov(\varepsilon_{i,t-1},\varepsilon_{i,t-2})$$

Ngay cả trong trường hợp **lý tưởng nhất** — $\varepsilon_{it}$ ở mức gốc hoàn toàn không tự tương quan (mọi $Cov(\varepsilon_{it},\varepsilon_{is})=0$ với $t\neq s$) — ba số hạng đầu/cuối triệt tiêu, nhưng còn lại:
<br><span class="en">Even in the **most ideal case** — $\varepsilon_{it}$ at the original level has no serial correlation whatsoever (every $Cov(\varepsilon_{it},\varepsilon_{is})=0$ for $t\neq s$) — the first/last three terms cancel out, but what remains is:</span>

$$Cov(\Delta\varepsilon_{it},\Delta\varepsilon_{i,t-1}) = -Var(\varepsilon_{i,t-1}) \neq 0$$

Đây là điểm mấu chốt: dù sai số gốc hoàn toàn "sạch" (đúng giả định lý tưởng nhất), phép **sai phân tự nó tạo ra tự tương quan bậc 1 một cách cơ học** — vì $\Delta\varepsilon_{it}$ và $\Delta\varepsilon_{i,t-1}$ **dùng chung số hạng $\varepsilon_{i,t-1}$** (chỉ khác dấu ở hai phương trình). Đây là hệ quả toán học tất yếu của việc sai phân, không liên quan gì đến việc mô hình có sai đặc tả hay không.
<br><span class="en">This is the crux: even when the original error is entirely "clean" (the most ideal assumption holds), **differencing itself mechanically creates first-order serial correlation** — because $\Delta\varepsilon_{it}$ and $\Delta\varepsilon_{i,t-1}$ **share the term $\varepsilon_{i,t-1}$** (only with opposite signs in the two equations). This is an inevitable mathematical consequence of differencing, unrelated to whether the model is misspecified or not.</span>

→ **Quan sát AR(1) có ý nghĩa thống kê (bị bác bỏ) chính là điều được kỳ vọng** — dấu hiệu mô hình đang hoạt động đúng như lý thuyết dự đoán. → Ngược lại: **nếu AR(1) không bác bỏ được**, đây mới là điều **bất thường**, gợi ý sai đặc tả mô hình hoặc lỗi dữ liệu (đúng theo lời slide). Minh họa từ ví dụ AB ở mục 4.4: AR(1) $z=-12.346$, $p\approx0$ → bác bỏ mạnh → đúng như kỳ vọng.
<br><span class="en">→ **Observing statistically significant AR(1) (rejected) is precisely what is expected** — a sign that the model is behaving exactly as theory predicts. → Conversely: **if AR(1) fails to be rejected**, this is the truly **abnormal** outcome, suggesting model misspecification or a data error (exactly per the slide). Illustration from the AB example in section 4.4: AR(1) $z=-12.346$, $p\approx0$ → strongly rejected → exactly as expected.</span>

**Quy tắc 2 — AR(2) bị bác bỏ mới chỉ ra instrument không hợp lệ.** Xét $Cov(\Delta\varepsilon_{it},\Delta\varepsilon_{i,t-2})$ với $\Delta\varepsilon_{i,t-2}=\varepsilon_{i,t-2}-\varepsilon_{i,t-3}$: nếu $\varepsilon_{it}$ ở mức không tự tương quan, **không có chỉ số thời gian nào trùng nhau** giữa $\{t, t-1\}$ (của $\Delta\varepsilon_{it}$) và $\{t-2, t-3\}$ (của $\Delta\varepsilon_{i,t-2}$) — khác hẳn trường hợp AR(1) ở trên (nơi $\varepsilon_{i,t-1}$ xuất hiện ở cả hai vế). Vì vậy $Cov(\Delta\varepsilon_{it},\Delta\varepsilon_{i,t-2})=0$ **về mặt lý thuyết, không có sự trùng lặp cơ học nào**.
<br><span class="en">**Rule 2 — rejecting AR(2) is what indicates an invalid instrument.** Consider $Cov(\Delta\varepsilon_{it},\Delta\varepsilon_{i,t-2})$ with $\Delta\varepsilon_{i,t-2}=\varepsilon_{i,t-2}-\varepsilon_{i,t-3}$: if $\varepsilon_{it}$ at level has no serial correlation, **there is no overlapping time index** between $\{t, t-1\}$ (of $\Delta\varepsilon_{it}$) and $\{t-2, t-3\}$ (of $\Delta\varepsilon_{i,t-2}$) — quite unlike the AR(1) case above (where $\varepsilon_{i,t-1}$ appears on both sides). Hence $Cov(\Delta\varepsilon_{it},\Delta\varepsilon_{i,t-2})=0$ **theoretically, with no mechanical overlap whatsoever**.</span>

→ Nếu kiểm định thực nghiệm **phát hiện** tự tương quan bậc 2 có ý nghĩa thống kê trong phần dư đã sai phân, điều này **không thể** là hệ quả cơ học của phép sai phân — nó buộc phải phản ánh một tự tương quan **thực sự** tồn tại ở sai số **mức gốc** ($\varepsilon_{it}$ có AR(1) hoặc AR(2) thật). Và đây chính xác là điều kiện làm cho $y_{i,t-2}$ (và các lag sâu hơn) **không còn hợp lệ** làm instrument cho biến trễ phụ thuộc (vi phạm điều kiện validity nêu ở mục 4.3).
<br><span class="en">→ If the empirical test **detects** statistically significant second-order serial correlation in the differenced residuals, this **cannot** be a mechanical consequence of differencing — it must reflect **genuine** serial correlation existing at the **original level** error ($\varepsilon_{it}$ has real AR(1) or AR(2)). And this is exactly the condition that makes $y_{i,t-2}$ (and deeper lags) **no longer valid** as instruments for the lagged dependent variable (violating the validity condition stated in section 4.3).</span>

→ **Bác bỏ AR(2) = bằng chứng chống lại tính hợp lệ của bộ instrument** (cho biến trễ phụ thuộc) — cần xem lại đặc tả mô hình hoặc giảm bớt số lag dùng làm instrument. Minh họa: AR(2) trong ví dụ AB ở mục 4.4 là $z=-0.777$, $p=0.437$ → **không bác bỏ** → tốt, ủng hộ tính hợp lệ.
<br><span class="en">→ **Rejecting AR(2) = evidence against the validity of the instrument set** (for the lagged dependent variable) — the model specification should be revisited, or the number of lags used as instruments reduced. Illustration: AR(2) in the AB example in section 4.4 is $z=-0.777$, $p=0.437$ → **not rejected** → good, supporting validity.</span>

**Bảng tóm tắt (bẫy thi kinh điển vì đi ngược trực giác thông thường "bác bỏ = xấu")**:
<br><span class="en">**Summary table (a classic exam trap because it runs against the usual intuition "reject = bad")**:</span>

| Kiểm định - <span class="en">Test</span> | Kỳ vọng khi mô hình đúng - <span class="en">Expectation when the model is correct</span> | Nếu ngược lại xảy ra - <span class="en">If the opposite happens</span> |
|---|---|---|
| AR(1) trên $\Delta\hat\varepsilon$ | **Nên bác bỏ** — hệ quả cơ học tất yếu của first-difference, không phải dấu hiệu xấu<br><span class="en">**Should be rejected** — an inevitable mechanical consequence of first-difference, not a bad sign</span> | Không bác bỏ được → bất thường, gợi ý sai đặc tả hoặc lỗi dữ liệu<br><span class="en">Fails to be rejected → abnormal, suggests misspecification or a data error</span> |
| AR(2) trên $\Delta\hat\varepsilon$ | **Không nên bác bỏ** — không có trùng lặp cơ học giữa $\Delta\varepsilon_{it}$ và $\Delta\varepsilon_{i,t-2}$<br><span class="en">**Should not be rejected** — no mechanical overlap between $\Delta\varepsilon_{it}$ and $\Delta\varepsilon_{i,t-2}$</span> | Bác bỏ được → instrument (cho biến trễ phụ thuộc) không hợp lệ<br><span class="en">Rejected → the instrument (for the lagged dependent variable) is invalid</span> |

### 7.3 [[people/sargan|Sargan]] test - <span class="en">[[people/sargan|Sargan]] test</span>

Kiểm định overidentifying restrictions — áp dụng cho cả Difference GMM lẫn System GMM, chỉ đáng tin dưới giả định **homoskedasticity** (giống hoàn toàn logic Sargan ở [[concepts/endogeneity-iv-regression]]). Không bác bỏ Sargan chỉ có nghĩa "chưa có bằng chứng chống lại" tính hợp lệ của bộ instrument, không phải "đã chứng minh" instrument hợp lệ — cùng nguyên tắc diễn giải kiểm định giả thuyết đã nêu ở [[concepts/linear-regression-model]] (mục t-test/F-test: "không bác bỏ ≠ đã chứng minh").
<br><span class="en">A test of overidentifying restrictions — applies to both Difference GMM and System GMM, only trustworthy under the **homoskedasticity** assumption (exactly the same Sargan logic as in [[concepts/endogeneity-iv-regression]]). Not rejecting Sargan only means "no evidence against" the validity of the instrument set, not that the instruments have been "proven" valid — the same hypothesis-testing interpretation principle stated in [[concepts/linear-regression-model]] (the t-test/F-test section: "not rejected ≠ proven").</span>

### 7.4 Kiểm tra external instruments - <span class="en">Checking external instruments</span>

Để kiểm tra sức mạnh/liên quan (relevance) của **external** instrument (`subeligible`, `localbudget`) trong Difference GMM hay System GMM: dùng chính **AH estimator** làm công cụ kiểm tra (chạy IV riêng cho biến nội sinh đó với external instrument, xem first-stage F).
<br><span class="en">To check the strength/relevance of an **external** instrument (`subeligible`, `localbudget`) in Difference GMM or System GMM: use the **AH estimator** itself as the checking tool (run a separate IV for that endogenous variable with the external instrument, and check the first-stage F).</span>

### 7.5 Ba dấu hiệu gián tiếp kiểm tra tính dừng (riêng cho System GMM) - <span class="en">Three indirect signs for checking stationarity (specific to System GMM)</span>

Không có kiểm định chính thức duy nhất cho tính dừng trong khung System GMM — dùng 3 dấu hiệu gián tiếp kết hợp (áp dụng minh họa đầy đủ ở mục 6.7):
<br><span class="en">There is no single formal test for stationarity within the System GMM framework — use 3 indirect signs combined (fully illustrated in application in section 6.7):</span>

1. Nếu Difference GMM và System GMM cho hệ số **gần nhau**, tính dừng khả dĩ đúng.
<br><span class="en">If Difference GMM and System GMM give **close** coefficients, stationarity is plausibly valid.</span>
2. Kiểm tra $\hat\alpha$ **không quá gần 0 hoặc 1**.
<br><span class="en">Check that $\hat\alpha$ is **not too close to 0 or 1**.</span>
3. Vẽ đồ thị $y_{it}$ theo thời gian, quan sát trực quan hành vi chuỗi.
<br><span class="en">Plot $y_{it}$ over time, and visually observe the series' behavior.</span>

## 8. Bẫy thi - <span class="en">Exam traps</span>

1. Đặc tả mô hình động **để có cớ** dùng System GMM — slide nhấn mạnh rõ đây là **sai quy trình**: đặc tả động phải xuất phát từ bản chất kinh tế, ước lượng chọn theo sau.
<br><span class="en">Specifying a dynamic model **as an excuse** to use System GMM — the slide clearly emphasizes this is the **wrong procedure**: a dynamic specification must originate from the economic nature of the process, with the estimator chosen after.</span>
2. Nghĩ rằng tăng $N$ (số đơn vị) có thể khắc phục Nickell bias — **sai**, bias là hàm của $1/T$, không liên quan đến $N$ (mục 2.4).
<br><span class="en">Thinking that increasing $N$ (number of units) can fix Nickell bias — **wrong**, the bias is a function of $1/T$, unrelated to $N$ (section 2.4).</span>
3. Diễn giải "không bác bỏ AR(1)" là tín hiệu tốt — **ngược lại hoàn toàn**: bác bỏ AR(1) mới là kỳ vọng đúng (hệ quả cơ học của sai phân); không bác bỏ mới là dấu hiệu bất thường (mục 7.2).
<br><span class="en">Interpreting "AR(1) not rejected" as a good sign — **exactly the opposite**: rejecting AR(1) is the correct expectation (a mechanical consequence of differencing); failing to reject is the abnormal sign (section 7.2).</span>
4. Diễn giải "bác bỏ AR(2)" như một kết quả bình thường/vô hại — **sai**: bác bỏ AR(2) là bằng chứng chống lại tính hợp lệ của instrument, cần xem lại đặc tả (mục 7.2).
<br><span class="en">Interpreting "AR(2) rejected" as a normal/harmless outcome — **wrong**: rejecting AR(2) is evidence against the validity of the instrument, requiring a review of the specification (section 7.2).</span>
5. Dùng Difference GMM khi $y$ có tính bền vững rất cao ($\rho\approx1$) mà không cân nhắc System GMM — Difference GMM hoạt động kém chính trong trường hợp này (mục 4.2, 6.1).
<br><span class="en">Using Difference GMM when $y$ is highly persistent ($\rho\approx1$) without considering System GMM — Difference GMM performs poorly precisely in this case (sections 4.2, 6.1).</span>
6. Quên rằng các ước lượng ở đây (AH/AB/System GMM) chỉ xử lý nội sinh của **biến trễ phụ thuộc**, không tự động xử lý nội sinh của các regressor khác (`training` vẫn cần instrument riêng).
<br><span class="en">Forgetting that the estimators here (AH/AB/System GMM) only address the endogeneity of the **lagged dependent variable**, not automatically the endogeneity of other regressors (`training` still needs its own instrument).</span>
7. Coi $\hat\alpha$ System GMM càng gần 1 kèm SE càng nhỏ là "càng đáng tin" — thực ra $\hat\alpha$ gần 1 lại chính là một trong 3 dấu hiệu **cảnh báo** khả năng vi phạm tính dừng (mục 6.7), không phải bằng chứng ủng hộ.
<br><span class="en">Treating a System GMM $\hat\alpha$ closer to 1 with a smaller SE as "more trustworthy" — in fact $\hat\alpha$ close to 1 is precisely one of the 3 **warning** signs of a possible stationarity violation (section 6.7), not supporting evidence.</span>
8. Coi biến **predetermined** là an toàn tuyệt đối (hoàn toàn ngoại sinh) trong mọi phép biến đổi — predetermined chỉ ngoại sinh **ở mức**; sau khi first-difference nó **trở thành nội sinh** và vẫn cần instrument (mục 5).
<br><span class="en">Treating a **predetermined** variable as absolutely safe (fully exogenous) under every transformation — predetermined is only exogenous **at level**; after first-difference it **becomes endogenous** and still needs an instrument (section 5).</span>
9. Áp ngưỡng $F=10$ một cách máy móc cho first-stage F mà quên rằng con số F-statistic thay đổi theo cấu trúc VCV sử dụng — không có một ngưỡng "đúng tuyệt đối" cho mọi trường hợp (mục 7.1).
<br><span class="en">Mechanically applying the $F=10$ threshold to first-stage F while forgetting that the F-statistic number changes with the VCV structure used — there is no single "absolutely correct" threshold for every case (section 7.1).</span>
10. Coi Sargan "không bác bỏ" là bằng chứng chắc chắn instrument hợp lệ trong mọi trường hợp — Sargan chỉ đáng tin dưới homoskedasticity, và giống mọi kiểm định giả thuyết khác, không bác bỏ chỉ là "chưa có bằng chứng chống lại", không phải "đã chứng minh hợp lệ" (mục 7.3).
<br><span class="en">Treating "Sargan not rejected" as definitive proof that the instrument is valid in every case — Sargan is only trustworthy under homoskedasticity, and like every other hypothesis test, not rejecting only means "no evidence against," not "proven valid" (section 7.3).</span>

## 9. Kết nối với phần còn lại của khóa học - <span class="en">Connections to the rest of the course</span>

Đây là điểm hội tụ của toàn bộ mạch panel data trong khóa học: dùng lại khung GMM đầy đủ từ [[concepts/endogeneity-iv-regression]] (Topic 5), phép biến đổi within/FD từ [[concepts/fixed-random-effects-model]] (Topic 6/12) và [[concepts/iv-regression-panel-data]] (Topic 13), rồi giải quyết thêm lớp vấn đề riêng của biến trễ (Nickell bias). Mạch phát triển ước lượng — Anderson-Hsiao (just-identified, 1 instrument) → Arellano-Bond/Difference GMM (overidentified, nhiều lag) → Arellano-Bover/Blundell-Bond/System GMM (thêm phương trình mức) — được tổng hợp riêng ở [[people/arellano-bond]].
<br><span class="en">This is the convergence point of the entire panel-data thread in the course: it reuses the full GMM framework from [[concepts/endogeneity-iv-regression]] (Topic 5), the within/FD transformation from [[concepts/fixed-random-effects-model]] (Topic 6/12) and [[concepts/iv-regression-panel-data]] (Topic 13), then addresses the additional layer of problems specific to the lagged variable (Nickell bias). The estimator development thread — Anderson-Hsiao (just-identified, 1 instrument) → Arellano-Bond/Difference GMM (overidentified, many lags) → Arellano-Bover/Blundell-Bond/System GMM (adds the level equation) — is synthesized separately at [[people/arellano-bond]].</span>

Đây cũng là bài học cuối cùng của khóa — điểm neo ngược lại [[concepts/econometrics-overview]]: mỗi ước lượng trong toàn khóa học (OLS → IV → FE/RE → IV-panel → Dynamic GMM) là một "chiến lược nhận diện" (identification strategy) khác nhau cho cùng một bài toán gốc — **identification problem**: làm sao tách được hiệu ứng nhân quả thật sự ra khỏi mọi nguồn nội sinh đang che khuất nó.
<br><span class="en">This is also the final lesson of the course — an anchor point back to [[concepts/econometrics-overview]]: every estimator across the whole course (OLS → IV → FE/RE → IV-panel → Dynamic GMM) is a different "identification strategy" for the same underlying problem — the **identification problem**: how to separate the true causal effect from every source of endogeneity obscuring it.</span>
