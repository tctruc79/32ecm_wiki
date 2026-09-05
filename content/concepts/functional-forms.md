---
title: "Lecture 2: Functional Forms"
type: concept
status: mature
tags: [functional-forms, elasticity, interaction, linear-regression]
sources: ["[[sources/slides-2-functional-forms]]"]
related: ["[[concepts/linear-regression-model]]"]
lecture: 2
assignment: ["Assignment 1: Linear Regression Model with functional forms"]
updated: 2026-09-04
---

> **Cách đọc trang này**: trang này mở rộng trực tiếp giả định **A1 (Linearity)** của [[concepts/linear-regression-model]] — "linear regression model" nghĩa là mô hình tuyến tính theo **tham số** $\beta$, **không nhất thiết** tuyến tính theo **biến** $X$ hay $Y$. Nếu chưa đọc mục 4 (Năm giả định OLS) của trang linear regression, nên đọc trước — mọi kỹ thuật dưới đây (log-log, log-lin, lin-log, quadratic, interaction term) chỉ là những cách biến đổi (transform) $X$ và/hoặc $Y$ trước khi đưa vào hồi quy, để mô hình *vẫn* tuyến tính theo $\beta$ (nên OLS vẫn dùng được y nguyên công thức $b=(X'X)^{-1}X'y$) trong khi biểu diễn được các quan hệ kinh tế phi tuyến trong thực tế.<br><span class="en">**How to read this page**: this page directly extends assumption **A1 (Linearity)** from [[concepts/linear-regression-model]] — "linear regression model" means a model that is linear in the **parameters** $\beta$, **not necessarily** linear in the **variables** $X$ or $Y$. If you haven't read section 4 (the five OLS assumptions) of the linear regression page yet, read it first — every technique below (log-log, log-lin, lin-log, quadratic, interaction term) is simply a way of transforming $X$ and/or $Y$ before running the regression, so that the model *remains* linear in $\beta$ (so OLS still applies exactly as-is via the formula $b=(X'X)^{-1}X'y$) while still being able to represent nonlinear economic relationships found in reality.</span>

**Lecture 2** trong đề cương (CO Topic 2) — Assignment 1: Linear Regression Model with functional forms.
<br><span class="en">**Lecture 2** in the syllabus (CO Topic 2) — Assignment 1: Linear Regression Model with functional forms.</span>

## 1. Vì sao cần vượt ra khỏi dạng linear? - <span class="en">Why go beyond the linear form?</span>

Ở dạng linear thuần túy $Y=\beta_0+\beta_1X+\varepsilon$, hệ số $\beta_1$ ngầm định một giả thiết kinh tế khá mạnh: **mỗi đơn vị $X$ tăng thêm luôn tạo ra đúng $\beta_1$ đơn vị thay đổi ở $Y$, bất kể đang xuất phát từ mức $X$ nào**. Ví dụ, nếu $\beta_{schooling}=2.26$ (nghìn VND/giờ) trong một mô hình linear, thì đi từ 12 lên 13 năm học tăng lương đúng 2.26 nghìn VND/giờ, và đi từ 17 lên 18 năm học cũng tăng đúng 2.26 — mức tăng **tuyệt đối** như nhau, bất kể mức lương gốc cao hay thấp.
<br><span class="en">In the pure linear form $Y=\beta_0+\beta_1X+\varepsilon$, the coefficient $\beta_1$ implicitly imposes a fairly strong economic assumption: **each additional unit of $X$ always produces exactly $\beta_1$ units of change in $Y$, regardless of the starting level of $X$**. For example, if $\beta_{schooling}=2.26$ (thousand VND/hour) in a linear model, then going from 12 to 13 years of schooling raises the wage by exactly 2.26 thousand VND/hour, and going from 17 to 18 years of schooling also raises it by exactly 2.26 — the same **absolute** increase, regardless of whether the base wage is high or low.</span>

Nhiều quan hệ kinh tế không vận hành như vậy trong thực tế:
<br><span class="en">Many economic relationships do not behave this way in reality:</span>

- **Lợi tức giáo dục (return to education) thường được nói bằng phần trăm, không phải bằng đơn vị tiền tệ tuyệt đối.** "Thêm 1 năm học làm lương tăng x%" là cách diễn đạt tự nhiên hơn "thêm 1 năm học làm lương tăng x nghìn đồng", vì % tự động điều chỉnh theo quy mô lương gốc — người có lương cao, cùng một % tăng đó tương ứng với nhiều tiền hơn về số tuyệt đối, điều này khớp với trực giác kinh tế.
<br><span class="en">**Return to education is usually expressed in percentage terms, not in absolute monetary units.** "An extra year of schooling raises wages by x%" is a more natural way to express this than "an extra year of schooling raises wages by x thousand VND," because % automatically scales with the base wage level — for someone with a high wage, the same % increase corresponds to more money in absolute terms, which matches economic intuition.</span>
- **Lương theo tuổi tác thường không đơn điệu (non-monotonic).** Lương có xu hướng tăng khi còn trẻ (tích lũy kinh nghiệm, kỹ năng) nhưng có thể chững lại hoặc giảm dần ở tuổi cao hơn. Một đường thẳng không thể biểu diễn hình dạng "tăng rồi giảm" này — cần dạng **quadratic**.
<br><span class="en">**Wages as a function of age are usually non-monotonic.** Wages tend to rise while workers are young (accumulating experience, skills) but may plateau or decline at older ages. A straight line cannot represent this "rise then fall" shape — this requires the **quadratic** form.</span>
- **Hiệu ứng của một biến có thể phụ thuộc vào giá trị của một biến khác.** Ví dụ lợi tức giáo dục có thể khác nhau giữa lao động nam và nữ. Một mô hình linear cộng gộp (additive) mặc định mọi biến tác động **độc lập** với nhau lên $Y$ — không cho phép hai biến "tương tác" (interact). Muốn kiểm định điều này, cần **interaction term**.
<br><span class="en">**The effect of one variable may depend on the value of another variable.** For example, the return to education may differ between male and female workers. An additive linear model by default assumes every variable affects $Y$ **independently** of the others — it does not allow two variables to "interact." Testing for this requires an **interaction term**.</span>

**Điểm mấu chốt cần giữ trong đầu xuyên suốt trang này**: dù đồ thị $Y$ theo $X$ trông "cong" hay "phi tuyến" đến đâu, tất cả các dạng hàm dưới đây đều **vẫn tuyến tính theo $\beta$** — đây chính là "mẹo" cho phép công cụ OLS (vốn chỉ giải được bài toán tuyến tính) biểu diễn được các quan hệ kinh tế phi tuyến: ta không thay đổi công cụ ước lượng, ta chỉ **biến đổi biến số** ($\ln X$, $X^2$, $X_1\times X_2$...) trước khi đưa vào hồi quy.
<br><span class="en">**The key point to keep in mind throughout this page**: no matter how "curved" or "nonlinear" the plot of $Y$ against $X$ looks, all the functional forms below **remain linear in $\beta$** — this is exactly the "trick" that lets the OLS tool (which can only solve linear problems) represent nonlinear economic relationships: we do not change the estimation tool, we only **transform the variables** ($\ln X$, $X^2$, $X_1\times X_2$...) before running the regression.</span>

## 2. Bộ dữ liệu ví dụ xuyên suốt: lương của lao động trẻ có kỹ năng tại Việt Nam - <span class="en">Running example dataset: wages of young, skilled workers in Vietnam</span>

Bài này dùng một bộ dữ liệu thực tế xuyên suốt để minh họa mọi dạng hàm — cần nắm để hiểu các ví dụ số ở mục 3, 6, 7 bên dưới.
<br><span class="en">This lecture uses one real dataset throughout to illustrate every functional form — understanding it is necessary to follow the numerical examples in sections 3, 6, and 7 below.</span>

**Mô tả nguồn dữ liệu**: dữ liệu thu thập từ khoảng 900–1000 lao động trẻ, có kỹ năng (young and skilled workers), tại các tỉnh thành Việt Nam.
<br><span class="en">**Data source description**: data collected from roughly 900–1000 young, skilled workers, across provinces/cities in Vietnam.</span>

| Biến<br><span class="en">Variable</span> | Ý nghĩa<br><span class="en">Meaning</span> | Đơn vị/thang đo<br><span class="en">Unit/scale</span> |
|---|---|---|
| `wage` | Lương — **biến phụ thuộc**<br><span class="en">Wage — **dependent variable**</span> | nghìn VND/giờ<br><span class="en">thousand VND/hour</span> |
| `age` | Tuổi<br><span class="en">Age</span> | năm<br><span class="en">years</span> |
| `schooling` | Số năm đi học<br><span class="en">Years of schooling</span> | năm<br><span class="en">years</span> |
| `tenure` | Thời gian làm việc cho chủ sử dụng lao động hiện tại<br><span class="en">Time worked for the current employer</span> | tháng<br><span class="en">months</span> |
| `gender` | Giới tính<br><span class="en">Gender</span> | dummy (0 = nữ, 1 = nam)<br><span class="en">dummy (0 = female, 1 = male)</span> |
| `origin` | Xuất thân<br><span class="en">Origin/background</span> | dummy (0 = lớn lên tại TP.HCM, 1 = nhập cư/di dân)<br><span class="en">dummy (0 = grew up in HCMC, 1 = migrant)</span> |
| `spec` | Chuyên ngành đào tạo: `technology` (nền/base), `science` (khoa học tự nhiên), `social` (khoa học xã hội)<br><span class="en">Field of study: `technology` (base), `science` (natural science), `social` (social science)</span> | categorical |
| `science` | Dummy sinh từ `spec`<br><span class="en">Dummy derived from `spec`</span> | dummy (1 = chuyên ngành khoa học tự nhiên)<br><span class="en">dummy (1 = natural science major)</span> |
| `social` | Dummy sinh từ `spec`<br><span class="en">Dummy derived from `spec`</span> | dummy (1 = chuyên ngành khoa học xã hội)<br><span class="en">dummy (1 = social science major)</span> |

**Thống kê mô tả** (n = 998, trích `psych::describe(data, fast = TRUE)`):
<br><span class="en">**Descriptive statistics** (n = 998, from `psych::describe(data, fast = TRUE)`):</span>

| Biến<br><span class="en">Variable</span> | n | mean | sd | median | min | max | range |
|---|---|---|---|---|---|---|---|
| `wage` | 998 | 75.02 | 41.81 | 65 | 10 | 302 | 292 |
| `age` | 998 | 23.94 | 4.96 | 24 | 10 | 43 | 33 |
| `schooling` | 998 | 14.03 | 1.58 | 14 | 12 | 18 | 6 |
| `tenure` | 998 | 25.02 | 12.75 | 24 | 1 | 83 | 82 |
| `gender` | 998 | 0.61 | 0.49 | 1 | 0 | 1 | 1 |
| `origin` | 998 | 0.40 | 0.49 | 0 | 0 | 1 | 1 |
| `science` | 998 | 0.31 | 0.46 | 0 | 0 | 1 | 1 |
| `social` | 998 | 0.55 | 0.50 | 1 | 0 | 1 | 1 |

Đọc nhanh bảng này trước khi đi vào hệ số hồi quy: lương trung bình 75.02 nghìn VND/giờ nhưng dao động rất mạnh (10–302, range 292 — gợi ý phân phối lệch phải, một lý do thực nghiệm khiến `ln(wage)` hay được dùng làm biến phụ thuộc thay vì `wage` thô); 61% người lao động trong mẫu là nam; 40% là dân nhập cư; 31% chuyên ngành khoa học tự nhiên, 55% khoa học xã hội (còn lại — nhóm nền `technology` — chiếm khoảng 14%).
<br><span class="en">A quick read of this table before moving to the regression coefficients: mean wage is 75.02 thousand VND/hour but varies widely (10–302, range 292 — suggesting a right-skewed distribution, one empirical reason `ln(wage)` is often used as the dependent variable instead of raw `wage`); 61% of workers in the sample are male; 40% are migrants; 31% majored in natural science, 55% in social science (the remainder — the `technology` base group — accounts for about 14%).</span>

Trên bộ dữ liệu này, sáu mô hình hồi quy khác nhau được ước lượng (bốn dạng hàm cơ bản ở mục 3, cộng quadratic ở mục 6, cộng interaction ở mục 7) trên cùng một tập biến kiểm soát — cho phép so sánh trực tiếp cách các dạng hàm "đọc" cùng một dữ liệu khác nhau như thế nào.
<br><span class="en">On this dataset, six different regression models are estimated (the four basic functional forms in section 3, plus quadratic in section 6, plus interaction in section 7) on the same set of control variables — allowing a direct comparison of how differently each functional form "reads" the same data.</span>

## 3. Bốn dạng hàm cơ bản - <span class="en">Four basic functional forms</span>

### 3.1 Linear — đường cơ sở - <span class="en">Linear — the baseline</span>

**Khi nào dùng**: khi lý thuyết dự đoán một đơn vị $X$ tăng thêm tạo ra một lượng thay đổi **tuyệt đối, cố định** ở $Y$, không phụ thuộc mức $X$ hay $Y$ đang ở đâu. Đây là dạng đơn giản nhất, không cần biến đổi gì cả — nhưng cũng là dạng "cứng nhắc" nhất về giả thiết kinh tế.
<br><span class="en">**When to use it**: when theory predicts that one additional unit of $X$ produces a **fixed, absolute** amount of change in $Y$, independent of the current level of $X$ or $Y$. This is the simplest form, requiring no transformation at all — but also the most "rigid" in terms of its economic assumption.</span>

$$Y=\beta_0+\beta_1X+\varepsilon$$

- **Biến liên tục (continuous regressor)**: $X$ tăng 1 đơn vị → $Y$ đổi $\beta_1$ đơn vị (đúng chính xác, không có khái niệm "xấp xỉ" ở đây vì quan hệ vốn đã tuyến tính).
<br><span class="en">**Continuous regressor**: $X$ increases by 1 unit → $Y$ changes by $\beta_1$ units (exact, there is no notion of "approximation" here since the relationship is already linear).</span>
- **Biến dummy (dummy regressor)**: $\beta_1$ là chênh lệch $Y$ trung bình giữa hai nhóm của $X$ (giống hệt cách diễn giải dummy đã học ở [[concepts/linear-regression-model]]).
<br><span class="en">**Dummy regressor**: $\beta_1$ is the difference in mean $Y$ between the two groups defined by $X$ (identical to the dummy-variable interpretation already covered in [[concepts/linear-regression-model]]).</span>

**Ví dụ số (hồi quy trên bộ dữ liệu lương)**:
<br><span class="en">**Numerical example (regression on the wage dataset)**:</span>

```
wage ~ age + schooling + tenure + gender + origin + science + social
```

| Biến<br><span class="en">Variable</span> | Estimate | Std. Error | t value | Pr(>|t|) |
|---|---|---|---|---|
| (Intercept) | 63.22655 | 13.91486 | 4.544 | 6.21e-06 *** |
| `age` | 0.09858 | 0.26065 | 0.378 | 0.70536 |
| `schooling` | 2.25944 | 0.82103 | 2.752 | 0.00603 ** |
| `tenure` | −0.66558 | 0.10136 | −6.566 | 8.32e-11 *** |
| `gender` | 0.46931 | 2.65664 | 0.177 | 0.85981 |
| `origin` | −7.54529 | 2.64807 | −2.849 | 0.00447 ** |
| `science` | −2.55645 | 4.22214 | −0.605 | 0.54499 |
| `social` | −3.79893 | 3.94543 | −0.963 | 0.33585 |

Residual SE = 40.74 (df = 990); $R^2$ = 0.05744; $R^2_{adj}$ = 0.05077; F = 8.618 trên (7, 990); p = 2.731e-10.
<br><span class="en">Residual SE = 40.74 (df = 990); $R^2$ = 0.05744; $R^2_{adj}$ = 0.05077; F = 8.618 on (7, 990); p = 2.731e-10.</span>

**Diễn giải mẫu**: "thêm 1 năm học làm tăng lương trung bình 2.259 nghìn VND/giờ, giữ các biến khác không đổi" (có ý nghĩa thống kê ở mức 1%). Đây chính là con số dùng để đối chiếu ở các mục 3.2–3.4: cùng biến `schooling`, cùng dữ liệu, nhưng cách "đọc" hệ số sẽ khác hẳn khi đổi dạng hàm.
<br><span class="en">**Sample interpretation**: "an extra year of schooling raises the average wage by 2.259 thousand VND/hour, holding other variables constant" (statistically significant at the 1% level). This is exactly the number used for comparison in sections 3.2–3.4: same variable `schooling`, same data, but the way the coefficient is "read" changes completely as the functional form changes.</span>

### 3.2 Log-log (còn gọi là Log-linear, Cobb-Douglas) - <span class="en">Log-log (also called Log-linear, Cobb-Douglas)</span>

**Khi nào dùng**: khi lý thuyết dự đoán quan hệ **co giãn không đổi (constant elasticity)** — % thay đổi của $Y$ tỷ lệ cố định với % thay đổi của $X$, bất kể đang ở mức $X$ nào. Đây là dạng hàm quen thuộc trong lý thuyết sản xuất (hàm Cobb-Douglas $Q=AK^{\alpha}L^{\beta}$ chính là log-log khi lấy log hai vế) và trong các nghiên cứu về lợi tức giáo dục, cầu hàng hóa (price elasticity)...
<br><span class="en">**When to use it**: when theory predicts a **constant elasticity** relationship — the % change in $Y$ is a fixed proportion of the % change in $X$, regardless of the level of $X$. This is a familiar functional form in production theory (the Cobb-Douglas function $Q=AK^{\alpha}L^{\beta}$ is exactly log-log once both sides are logged) and in studies of return to education, demand for goods (price elasticity)...</span>

$$\ln Y=\beta_0+\beta_1\ln X+\varepsilon$$

Với $X$ là biến liên tục, $\beta_1$ chính là **elasticity tức thời (instantaneous elasticity)** của $Y$ theo $X$ — số đo kinh điển trong kinh tế học vi mô.
<br><span class="en">With $X$ a continuous variable, $\beta_1$ is exactly the **instantaneous elasticity** of $Y$ with respect to $X$ — a classic measure in microeconomics.</span>

- **Diễn giải xấp xỉ (approximate)**: $X$ tăng 1% → $Y$ đổi $\beta_1$ phần trăm.
<br><span class="en">**Approximate interpretation**: $X$ increases by 1% → $Y$ changes by $\beta_1$ percent.</span>
- **Diễn giải chính xác (exact)**: $X$ tăng 1% → $Y$ đổi $b=(1.01^{\beta_1}-1)\times100$ phần trăm.
<br><span class="en">**Exact interpretation**: $X$ increases by 1% → $Y$ changes by $b=(1.01^{\beta_1}-1)\times100$ percent.</span>

**Ví dụ số (hồi quy trên bộ dữ liệu lương)**:
<br><span class="en">**Numerical example (regression on the wage dataset)**:</span>

```
log(wage) ~ log(age) + log(schooling) + log(tenure) + gender + origin + science + social
```

| Biến<br><span class="en">Variable</span> | Estimate | Std. Error | t value | Pr(>|t|) |
|---|---|---|---|---|
| (Intercept) | 3.70523 | 0.46038 | 8.048 | 2.39e-15 *** |
| `log(age)` | 0.03129 | 0.07559 | 0.414 | 0.67896 |
| `log(schooling)` | 0.36100 | 0.14695 | 2.457 | 0.01419 * |
| `log(tenure)` | −0.17078 | 0.02462 | −6.936 | 7.25e-12 *** |
| `gender` | 0.02054 | 0.03311 | 0.620 | 0.53521 |
| `origin` | −0.10287 | 0.03300 | −3.117 | 0.00188 ** |
| `science` | −0.02639 | 0.05259 | −0.502 | 0.61586 |
| `social` | −0.02822 | 0.04914 | −0.574 | 0.56595 |

Residual SE = 0.5076 (df = 990); $R^2$ = 0.06106; $R^2_{adj}$ = 0.05442; F = 9.197 trên (7, 990); p = 4.704e-11.
<br><span class="en">Residual SE = 0.5076 (df = 990); $R^2$ = 0.06106; $R^2_{adj}$ = 0.05442; F = 9.197 on (7, 990); p = 4.704e-11.</span>

$\beta_{\ln schooling}=0.361$ (có ý nghĩa ở mức 5%):
<br><span class="en">$\beta_{\ln schooling}=0.361$ (significant at the 5% level):</span>

- **Xấp xỉ**: tăng 1% năm học → lương tăng xấp xỉ **0.361%**.
<br><span class="en">**Approximate**: a 1% increase in years of schooling → wage increases by approximately **0.361%**.</span>
- **Chính xác**: $b=(1.01^{0.361}-1)\times100=0.360\%$ — rất gần với con số xấp xỉ (đúng như quy tắc: $\beta_1$ càng nhỏ, xấp xỉ và chính xác càng gần nhau).
<br><span class="en">**Exact**: $b=(1.01^{0.361}-1)\times100=0.360\%$ — very close to the approximate figure (as expected from the rule: the smaller $\beta_1$ is, the closer the approximate and exact values are).</span>

### 3.3 Log-lin (semi-log, semi-elasticity) - <span class="en">Log-lin (semi-log, semi-elasticity)</span>

**Khi nào dùng**: khi $X$ vẫn đo bằng đơn vị tự nhiên (năm học, tuổi, một biến dummy...) nhưng $Y$ co giãn theo **phần trăm** — đây là dạng hàm phổ biến nhất trong các nghiên cứu về tiền lương (Mincer wage equation gốc chính là log-lin theo `schooling`), vì "return to education" theo truyền thống được đo bằng %/năm học, không phải bằng đơn vị tiền tệ/năm học.
<br><span class="en">**When to use it**: when $X$ is still measured in its natural units (years of schooling, age, a dummy variable...) but $Y$ responds in **percentage** terms — this is the most common functional form in wage studies (the original Mincer wage equation is exactly log-lin in `schooling`), because "return to education" is traditionally measured in %/year of schooling, not in monetary units/year of schooling.</span>

$$\ln Y=\beta_0+\beta_1X+\varepsilon$$

Hệ số $\beta_1$ ở đây là **semi-elasticity** — co giãn "nửa vời": $Y$ đo theo %, còn $X$ vẫn đo theo đơn vị tự nhiên.
<br><span class="en">The coefficient $\beta_1$ here is a **semi-elasticity** — a "half" elasticity: $Y$ is measured in %, while $X$ is still measured in its natural units.</span>

**3.3.a — Biến liên tục (VD `schooling`)**
<br><span class="en">**3.3.a — Continuous variable (e.g. `schooling`)**</span>

- **Xấp xỉ**: $X$ tăng 1 đơn vị → $Y$ đổi $\beta_1\times100$ phần trăm.
<br><span class="en">**Approximate**: $X$ increases by 1 unit → $Y$ changes by $\beta_1\times100$ percent.</span>
- **Chính xác**: $X$ tăng 1 đơn vị → $Y$ đổi $b=(e^{\beta_1}-1)\times100$ phần trăm.
<br><span class="en">**Exact**: $X$ increases by 1 unit → $Y$ changes by $b=(e^{\beta_1}-1)\times100$ percent.</span>

**Ví dụ số (hồi quy trên bộ dữ liệu lương)**:
<br><span class="en">**Numerical example (regression on the wage dataset)**:</span>

```
log(wage) ~ age + schooling + tenure + gender + origin + science + social
```

| Biến<br><span class="en">Variable</span> | Estimate | Std. Error | t value | Pr(>|t|) |
|---|---|---|---|---|
| (Intercept) | 4.060887 | 0.172488 | 23.543 | < 2e-16 *** |
| `age` | 0.001358 | 0.003231 | 0.420 | 0.67441 |
| `schooling` | 0.026674 | 0.010178 | 2.621 | 0.00890 ** |
| `tenure` | −0.009561 | 0.001257 | −7.609 | 6.42e-14 *** |
| `gender` | 0.020419 | 0.032932 | 0.620 | 0.53537 |
| `origin` | −0.102151 | 0.032825 | −3.112 | 0.00191 ** |
| `science` | −0.019312 | 0.052338 | −0.369 | 0.71222 |
| `social` | −0.022739 | 0.048907 | −0.465 | 0.64208 |

Residual SE = 0.505 (df = 990); $R^2$ = 0.07053; $R^2_{adj}$ = 0.06396; F = 10.73 trên (7, 990); p = 4.413e-13.
<br><span class="en">Residual SE = 0.505 (df = 990); $R^2$ = 0.07053; $R^2_{adj}$ = 0.06396; F = 10.73 on (7, 990); p = 4.413e-13.</span>

$\beta_{schooling}=0.02667$ (có ý nghĩa ở mức 1%):
<br><span class="en">$\beta_{schooling}=0.02667$ (significant at the 1% level):</span>

- **Xấp xỉ**: thêm 1 năm học → lương tăng xấp xỉ $0.02667\times100=$ **2.667%**.
<br><span class="en">**Approximate**: an extra year of schooling → wage increases by approximately $0.02667\times100=$ **2.667%**.</span>
- **Chính xác**: $b=(e^{0.02667}-1)\times100=2.703\%\approx$ **2.700%** — rất gần con số xấp xỉ.
<br><span class="en">**Exact**: $b=(e^{0.02667}-1)\times100=2.703\%\approx$ **2.700%** — very close to the approximate figure.</span>

**3.3.b — Biến dummy (VD `gender`)**
<br><span class="en">**3.3.b — Dummy variable (e.g. `gender`)**</span>

- **Xấp xỉ**: chênh lệch % giữa nhóm $X=1$ và nhóm nền $X=0$ là $\beta_1\times100$ phần trăm.
<br><span class="en">**Approximate**: the % difference between group $X=1$ and the base group $X=0$ is $\beta_1\times100$ percent.</span>
- **Chính xác**: chênh lệch giữa hai nhóm là $b=(e^{\beta_1}-1)\times100$ phần trăm.
<br><span class="en">**Exact**: the difference between the two groups is $b=(e^{\beta_1}-1)\times100$ percent.</span>

Ví dụ minh họa (riêng ngoài bảng hồi quy đầy đủ ở trên): $\beta_{gender}=0.02$ →
<br><span class="en">Illustrative example (separate from the full regression table above): $\beta_{gender}=0.02$ →</span>

- **Xấp xỉ**: lương nam cao hơn nữ khoảng **2.00%**.
<br><span class="en">**Approximate**: male wages are about **2.00%** higher than female wages.</span>
- **Chính xác**: $b=(e^{0.02}-1)\times100=2.02\%$.
<br><span class="en">**Exact**: $b=(e^{0.02}-1)\times100=2.02\%$.</span>

(Ví dụ dummy này **nhất quán nội bộ** — không có mâu thuẫn số liệu như ở mục 3.2/3.3.a, dùng để đối chiếu.)
<br><span class="en">(This dummy example is **internally consistent** — no numerical contradiction like the ones in sections 3.2/3.3.a — and is used here as a clean reference point.)</span>

### 3.4 Lin-log - <span class="en">Lin-log</span>

**Khi nào dùng**: trường hợp ngược lại 3.3 — $Y$ vẫn đo bằng đơn vị tự nhiên (VD nghìn VND/giờ), nhưng $X$ co giãn theo phần trăm. Ít phổ biến hơn log-lin trong nghiên cứu tiền lương, nhưng hữu ích khi $X$ có phạm vi giá trị rất rộng (order-of-magnitude khác nhau) trong khi $Y$ thì không — lấy log $X$ giúp "nén" phạm vi đó lại.
<br><span class="en">**When to use it**: the reverse case of 3.3 — $Y$ is still measured in its natural units (e.g. thousand VND/hour), but $X$ responds in percentage terms. Less common than log-lin in wage studies, but useful when $X$ spans a very wide range of values (differing orders of magnitude) while $Y$ does not — taking the log of $X$ helps "compress" that range.</span>

$$Y=\beta_0+\beta_1\ln X+\varepsilon$$

- **Xấp xỉ**: $X$ tăng 1% → $Y$ đổi $\beta_1\div100$ đơn vị.
<br><span class="en">**Approximate**: $X$ increases by 1% → $Y$ changes by $\beta_1\div100$ units.</span>
- **Chính xác**: $X$ tăng 1% → $Y$ đổi $b=\beta_1\times\ln(1.01)$ đơn vị.
<br><span class="en">**Exact**: $X$ increases by 1% → $Y$ changes by $b=\beta_1\times\ln(1.01)$ units.</span>

**Ví dụ số (hồi quy trên bộ dữ liệu lương)**:
<br><span class="en">**Numerical example (regression on the wage dataset)**:</span>

```
wage ~ log(age) + log(schooling) + log(tenure) + gender + origin + science + social
```

| Biến<br><span class="en">Variable</span> | Estimate | Std. Error | t value | Pr(>|t|) |
|---|---|---|---|---|
| (Intercept) | 29.9728 | 37.0611 | 0.809 | 0.41886 |
| `log(age)` | 2.1460 | 6.0849 | 0.353 | 0.72441 |
| `log(schooling)` | 30.9070 | 11.8295 | 2.613 | 0.00912 ** |
| `log(tenure)` | −12.1797 | 1.9820 | −6.145 | 1.16e-09 *** |
| `gender` | 0.4929 | 2.6653 | 0.185 | 0.85333 |
| `origin` | −7.5937 | 2.6566 | −2.858 | 0.00435 ** |
| `science` | −3.0487 | 4.2336 | −0.720 | 0.47162 |
| `social` | −4.1834 | 3.9561 | −1.057 | 0.29057 |

Residual SE = 40.86 (df = 990); $R^2$ = 0.05185; $R^2_{adj}$ = 0.04515; F = 7.734 trên (7, 990); p = 3.978e-9.
<br><span class="en">Residual SE = 40.86 (df = 990); $R^2$ = 0.05185; $R^2_{adj}$ = 0.04515; F = 7.734 on (7, 990); p = 3.978e-9.</span>

$\beta_{\ln schooling}=30.907$ (có ý nghĩa ở mức 1%):
<br><span class="en">$\beta_{\ln schooling}=30.907$ (significant at the 1% level):</span>

- **Xấp xỉ**: tăng 1% năm học → lương tăng xấp xỉ $30.907\div100=$ **0.309 nghìn VND/giờ**.
<br><span class="en">**Approximate**: a 1% increase in years of schooling → wage increases by approximately $30.907\div100=$ **0.309 thousand VND/hour**.</span>
- **Chính xác**: $b=30.907\times\ln(1.01)=30.907\times0.009950=$ **0.307 nghìn VND/giờ**.
<br><span class="en">**Exact**: $b=30.907\times\ln(1.01)=30.907\times0.009950=$ **0.307 thousand VND/hour**.</span>

Đây là ví dụ **nhất quán nội bộ** (không có mâu thuẫn số liệu như mục 3.2/3.3.a) — dùng làm điểm đối chiếu "sạch" để hiểu công thức đúng hoạt động ra sao.
<br><span class="en">This is an **internally consistent** example (no numerical contradiction like sections 3.2/3.3.a) — used as a "clean" reference point for understanding how the correct formula works.</span>

## 4. Bảng tổng hợp — cheat sheet diễn giải hệ số - <span class="en">Summary table — coefficient interpretation cheat sheet</span>

| Dạng hàm<br><span class="en">Functional form</span> | Phương trình<br><span class="en">Equation</span> | X tăng theo<br><span class="en">X increases by</span> | Diễn giải xấp xỉ của $\beta_1$<br><span class="en">Approximate interpretation of $\beta_1$</span> | Công thức chính xác<br><span class="en">Exact formula</span> |
|---|---|---|---|---|
| **Linear** | $Y=\beta_0+\beta_1X+\varepsilon$ | 1 đơn vị<br><span class="en">1 unit</span> | $Y$ đổi $\beta_1$ **đơn vị**<br><span class="en">$Y$ changes by $\beta_1$ **units**</span> | (đã chính xác, không cần công thức riêng)<br><span class="en">(already exact, no separate formula needed)</span> |
| **Log-log** | $\ln Y=\beta_0+\beta_1\ln X+\varepsilon$ | 1% | $Y$ đổi $\beta_1$ **phần trăm** (= elasticity)<br><span class="en">$Y$ changes by $\beta_1$ **percent** (= elasticity)</span> | $b=(1.01^{\beta_1}-1)\times100$ |
| **Log-lin** | $\ln Y=\beta_0+\beta_1X+\varepsilon$ | 1 đơn vị<br><span class="en">1 unit</span> | $Y$ đổi $\beta_1\times100$ **phần trăm**<br><span class="en">$Y$ changes by $\beta_1\times100$ **percent**</span> | $b=(e^{\beta_1}-1)\times100$ |
| **Lin-log** | $Y=\beta_0+\beta_1\ln X+\varepsilon$ | 1% | $Y$ đổi $\beta_1\div100$ **đơn vị**<br><span class="en">$Y$ changes by $\beta_1\div100$ **units**</span> | $b=\beta_1\times\ln(1.01)$ |

**Cách nhớ nhanh** (mẹo ghi nhớ tự đặt): nhìn vào **vị trí của "log"** trong tên gọi — "log" đứng trước $Y$ hay $X$ (hay cả hai) quyết định đơn vị đo của **thay đổi**, không phải của **biến**:
<br><span class="en">**Quick mnemonic** (a self-devised memory aid): look at **where "log" sits** in the name — whether "log" appears before $Y$ or $X$ (or both) determines the unit of measurement of the **change**, not of the **variable**:</span>
- Có `log` ở $X$ (log-log, lin-log) → nói về $X$ **tăng 1%**.
<br><span class="en">- `log` present on $X$ (log-log, lin-log) → refers to $X$ **increasing by 1%**.</span>
- Không có `log` ở $X$ (linear, log-lin) → nói về $X$ **tăng 1 đơn vị**.
<br><span class="en">- No `log` on $X$ (linear, log-lin) → refers to $X$ **increasing by 1 unit**.</span>
- Có `log` ở $Y$ (log-log, log-lin) → $Y$ **đổi theo phần trăm**.
<br><span class="en">- `log` present on $Y$ (log-log, log-lin) → $Y$ **changes in percentage terms**.</span>
- Không có `log` ở $Y$ (linear, lin-log) → $Y$ **đổi theo đơn vị đo gốc**.
<br><span class="en">- No `log` on $Y$ (linear, lin-log) → $Y$ **changes in its original unit of measurement**.</span>

> **Quy tắc chung về xấp xỉ vs. chính xác**: hai cách tính **gần nhau khi $\beta_1$ nhỏ** (nói lỏng: $|\beta_1|<0.1$ thường lệch không đáng kể); khi $\beta_1$ lớn, hai cách tính có thể lệch đáng kể — đây là bẫy thi kinh điển (dùng công thức xấp xỉ khi đề bài yêu cầu "exact effect", hoặc ngược lại). Bốn ví dụ số ở mục 3 phía trên đều có $\beta_1$ tương đối nhỏ nên xấp xỉ và chính xác luôn gần nhau — **không được suy ra từ đó rằng hai cách tính luôn cho kết quả gần nhau**; với $\beta_1$ lớn (VD trên 0.5), độ lệch có thể trở nên rõ rệt.
> <br><span class="en">**General rule on approximate vs. exact**: the two calculation methods are **close when $\beta_1$ is small** (loosely: $|\beta_1|<0.1$ usually gives a negligible difference); when $\beta_1$ is large, the two methods can diverge substantially — this is a classic exam trap (using the approximate formula when the question asks for the "exact effect," or vice versa). The four numerical examples in section 3 above all have relatively small $\beta_1$, so the approximate and exact values are always close — **do not conclude from this that the two methods always give close results**; with a large $\beta_1$ (e.g. above 0.5), the discrepancy can become substantial.</span>

## 5. Suy ra công thức "exact" — từng bước (tự học) - <span class="en">Deriving the "exact" formula — step by step (self-study)</span>

Phần này thuộc diện tự học (self-study) — chứng minh vì sao công thức "exact" ở mục 3, 4 lại đúng, thay vì chỉ ghi nhớ máy móc.
<br><span class="en">This part is self-study material — proving why the "exact" formula in sections 3 and 4 is correct, rather than just memorizing it mechanically.</span>

### 5.1 Log-log → công thức exact elasticity - <span class="en">Log-log → the exact elasticity formula</span>

Xuất phát từ $\ln y=\beta_0+\beta_1\ln X$. Khi $X$ tăng 1% (tức $X$ mới là $1.01X$), giá trị hàm trở thành:
<br><span class="en">Start from $\ln y=\beta_0+\beta_1\ln X$. When $X$ increases by 1% (i.e. the new $X$ is $1.01X$), the function value becomes:</span>

$$\ln y' = \beta_0+\beta_1\ln(1.01X)$$

Lấy hiệu hai phương trình để cô lập phần thay đổi:
<br><span class="en">Take the difference between the two equations to isolate the change:</span>

$$\ln y' - \ln y = \beta_1\ln(1.01X)-\beta_1\ln X = \beta_1\ln(1.01)$$

(vì $\ln(1.01X)-\ln X=\ln\!\left(\frac{1.01X}{X}\right)=\ln(1.01)$, theo tính chất logarit). Vậy $\ln\!\left(\frac{y'}{y}\right)=\beta_1\ln(1.01)$. Dùng đồng nhất thức $e^{a\ln b}=b^a$ (lấy mũ hai vế với cơ số $e$):
<br><span class="en">(since $\ln(1.01X)-\ln X=\ln\!\left(\frac{1.01X}{X}\right)=\ln(1.01)$, by the properties of logarithms). So $\ln\!\left(\frac{y'}{y}\right)=\beta_1\ln(1.01)$. Using the identity $e^{a\ln b}=b^a$ (exponentiating both sides with base $e$):</span>

$$\frac{y'}{y}=1.01^{\beta_1}$$

Trừ 1 hai vế rồi nhân 100 để chuyển từ tỉ lệ sang phần trăm:
<br><span class="en">Subtract 1 from both sides then multiply by 100 to convert from a ratio to a percentage:</span>

$$\frac{y'-y}{y}\times100=(1.01^{\beta_1}-1)\times100$$

Đây chính là công thức "exact" ở mục 3.2/4.
<br><span class="en">This is exactly the "exact" formula in sections 3.2/4.</span>

### 5.2 Log-lin → công thức exact semi-elasticity - <span class="en">Log-lin → the exact semi-elasticity formula</span>

Xuất phát từ $\ln y=\beta_0+\beta_1X$. Khi $X$ tăng 1 đơn vị:
<br><span class="en">Start from $\ln y=\beta_0+\beta_1X$. When $X$ increases by 1 unit:</span>

$$\ln y_0=\beta_0+\beta_1X \qquad \ln y_1=\beta_0+\beta_1(X+1)$$

Lấy hiệu: $\ln y_1-\ln y_0=\beta_1$. Vậy $\dfrac{y_1}{y_0}=e^{\beta_1}$, và:
<br><span class="en">Taking the difference: $\ln y_1-\ln y_0=\beta_1$. So $\dfrac{y_1}{y_0}=e^{\beta_1}$, and:</span>

$$\frac{y_1-y_0}{y_0}\times100=(e^{\beta_1}-1)\times100$$

Đây chính là công thức "exact" ở mục 3.3/4.
<br><span class="en">This is exactly the "exact" formula in sections 3.3/4.</span>

### 5.3 Lin-log → công thức exact - <span class="en">Lin-log → the exact formula</span>

Xuất phát từ $y=\beta_0+\beta_1\ln X$. Khi $X$ tăng 1%:
<br><span class="en">Start from $y=\beta_0+\beta_1\ln X$. When $X$ increases by 1%:</span>

$$y_0=\beta_0+\beta_1\ln X \qquad y_1=\beta_0+\beta_1\ln(1.01X)$$

Lấy hiệu trực tiếp (không cần logarit hóa lần nữa vì $y$ đã ở dạng tuyến tính):
<br><span class="en">Take the difference directly (no need to take logs again since $y$ is already linear):</span>

$$y_1-y_0=\beta_1\big[\ln(1.01X)-\ln X\big]=\beta_1\ln(1.01)$$

Đây chính là công thức "exact" ở mục 3.4/4. Vì $\ln(1.01)\approx0.01$, công thức xấp xỉ $\beta_1/100$ chỉ là cách "làm tròn" $\ln(1.01)$ thành $0.01$ — và cần lưu ý rõ: **xấp xỉ này có thể lệch đáng kể so với con số chính xác nếu $\beta_1$ đủ lớn**.
<br><span class="en">This is exactly the "exact" formula in sections 3.4/4. Since $\ln(1.01)\approx0.01$, the approximate formula $\beta_1/100$ is simply a way of "rounding" $\ln(1.01)$ to $0.01$ — and it's worth noting explicitly: **this approximation can deviate substantially from the exact figure if $\beta_1$ is large enough**.</span>

## 6. Quadratic functional form - <span class="en">Quadratic functional form</span>

**Khi nào dùng**: khi lý thuyết dự đoán quan hệ **không đơn điệu** — tăng đến một điểm rồi giảm (hoặc ngược lại: giảm rồi tăng), thay vì tăng/giảm đều một chiều suốt toàn miền giá trị của $X$. Ví dụ kinh điển: lương tăng theo tuổi (tích lũy kinh nghiệm) nhưng đến một độ tuổi nào đó thì bắt đầu giảm dần.
<br><span class="en">**When to use it**: when theory predicts a **non-monotonic** relationship — rising up to a point then falling (or the reverse: falling then rising), instead of moving steadily in one direction across the entire range of $X$. Classic example: wages rise with age (accumulating experience) but start declining after a certain age.</span>

$$\ln y = \beta_0 + \beta_1 \cdot age + \beta_2 \cdot age^2 + \cdots$$

**Trực giác về dấu của $\beta_2$**: $\beta_2<0$ → parabol úp xuống → có điểm **cực đại (maximum)** — khớp với câu chuyện "tăng rồi giảm". $\beta_2>0$ → parabol ngửa lên → có điểm **cực tiểu (minimum)** — khớp với câu chuyện "giảm rồi tăng" (ít gặp hơn trong ví dụ lương-tuổi, nhưng phổ biến trong các quan hệ chi phí).
<br><span class="en">**Intuition about the sign of $\beta_2$**: $\beta_2<0$ → downward-opening parabola → has a **maximum** point — matching the "rise then fall" story. $\beta_2>0$ → upward-opening parabola → has a **minimum** point — matching the "fall then rise" story (less common in the wage-age example, but common in cost relationships).</span>

**Tính điểm cực trị (extremum)**: lấy đạo hàm riêng theo `age`, cho bằng 0:
<br><span class="en">**Finding the extremum**: take the partial derivative with respect to `age` and set it to zero:</span>

$$\frac{\partial \ln wage}{\partial age} = \beta_1 + 2\beta_2\cdot age = 0 \;\Rightarrow\; age^* = -\frac{\beta_1}{2\beta_2}$$

**Ví dụ số (hồi quy trên bộ dữ liệu lương)**:
<br><span class="en">**Numerical example (regression on the wage dataset)**:</span>

```
log(wage) ~ age + I(age^2) + schooling + tenure + gender + origin + science + social
```

| Biến<br><span class="en">Variable</span> | Estimate | Std. Error | t value | Pr(>|t|) |
|---|---|---|---|---|
| (Intercept) | 3.9590078 | 0.3024932 | 13.088 | < 2e-16 *** |
| `age` | 0.0103682 | 0.0222095 | 0.467 | 0.64072 |
| `I(age^2)` | −0.0001830 | 0.0004462 | −0.410 | 0.68184 |
| `schooling` | 0.0263959 | 0.0102044 | 2.587 | 0.00983 ** |
| `tenure` | −0.0095798 | 0.0012579 | −7.616 | 6.12e-14 *** |
| `gender` | 0.0197287 | 0.0329885 | 0.598 | 0.54995 |
| `origin` | −0.1022937 | 0.0328411 | −3.115 | 0.00189 ** |
| `science` | −0.0186382 | 0.0523853 | −0.356 | 0.72207 |
| `social` | −0.0223893 | 0.0489354 | −0.458 | 0.64739 |

Residual SE = 0.5052 (df = 989); $R^2$ = 0.07069; $R^2_{adj}$ = 0.06317; F = 9.404 trên (8, 989); p = 1.406e-12.
<br><span class="en">Residual SE = 0.5052 (df = 989); $R^2$ = 0.07069; $R^2_{adj}$ = 0.06317; F = 9.404 on (8, 989); p = 1.406e-12.</span>

Với $\beta_1=0.0103682$ và $\beta_2=-0.0001830$ ($\beta_2<0$ → đây là điểm **cực đại**):
<br><span class="en">With $\beta_1=0.0103682$ and $\beta_2=-0.0001830$ ($\beta_2<0$ → this is a **maximum** point):</span>

$$age^*=-\frac{0.0103682}{2\times(-0.0001830)}=28.3$$

**Trước 28.3 tuổi**, $\ln wage$ tăng theo tuổi; **sau 28.3 tuổi**, giảm dần theo tuổi (theo mô hình này).
<br><span class="en">**Before age 28.3**, $\ln wage$ increases with age; **after age 28.3**, it declines with age (according to this model).</span>

### 6.1 Kiểm định ý nghĩa: t-test không đủ, cần F-test đồng thời - <span class="en">Testing significance: a t-test is not enough, a joint F-test is needed</span>

Kiểm định $\beta_2$ riêng lẻ (câu hỏi "số hạng bậc hai có đóng góp thêm thông tin ngoài số hạng bậc một hay không?") dùng **t-test** bình thường. Nhưng câu hỏi rộng hơn — "biến `age` (nói chung, cả bậc 1 lẫn bậc 2) có ảnh hưởng gì đến lương hay không?" — **không thể** trả lời chỉ bằng t-test của $\beta_1$ hoặc của $\beta_2$ riêng lẻ, vì hai hệ số cùng mô tả một biến; phải dùng **F-test đồng thời**:
<br><span class="en">Testing $\beta_2$ alone (the question "does the quadratic term contribute additional information beyond the linear term?") uses an ordinary **t-test**. But the broader question — "does the variable `age` (overall, both the linear and quadratic terms) have any effect on wages at all?" — **cannot** be answered using only the t-test of $\beta_1$ or of $\beta_2$ alone, because the two coefficients jointly describe one variable; a **joint F-test** must be used:</span>

$$H_0: \beta_1=\beta_2=0$$

**Kết quả F-test thực tế** (`car::linearHypothesis`, so sánh mô hình có và không có `age`, `I(age^2)`):
<br><span class="en">**Actual F-test result** (`car::linearHypothesis`, comparing the model with and without `age`, `I(age^2)`):</span>

```
Model 1: restricted model (without age, age^2)
Model 2: log(wage) ~ age + I(age^2) + schooling + tenure + gender + origin + science + social

  Res.Df   RSS Df Sum of Sq      F Pr(>F)
1    991 252.52
2    989 252.44  2  0.087956 0.1723 0.8418
```

F = 0.1723, p = 0.8418 → **không bác bỏ** $H_0$. Nói cách khác: trong đúng bộ dữ liệu này, **`age` (kể cả khi cho phép quan hệ bậc hai) không có ảnh hưởng có ý nghĩa thống kê đến lương**, dù đã tính được một điểm cực trị "đẹp" ở tuổi 28.3.
<br><span class="en">F = 0.1723, p = 0.8418 → **fail to reject** $H_0$. In other words: in this exact dataset, **`age` (even allowing for a quadratic relationship) has no statistically significant effect on wages**, despite having computed a "nice-looking" extremum at age 28.3.</span>

> **Điểm quan trọng nhất của mục 6 — dễ bị bỏ sót khi ôn thi**: việc tính ra được một điểm cực trị $age^*=28.3$ **không tự động có nghĩa quan hệ đó có ý nghĩa thống kê**. Công thức $age^*=-\beta_1/2\beta_2$ luôn cho ra một con số miễn $\beta_2\neq0$ — kể cả khi cả $\beta_1$ và $\beta_2$ đều hoàn toàn không có ý nghĩa thống kê (như chính ví dụ này: $p_{\beta_1}=0.64$, $p_{\beta_2}=0.68$, và F-test đồng thời $p=0.84$). Trước khi diễn giải điểm cực trị theo nghĩa kinh tế ("lương đạt đỉnh ở tuổi 28.3"), phải kiểm tra F-test đồng thời có ý nghĩa hay không — nếu không, con số $age^*$ chỉ là một artefact toán học của mẫu dữ liệu cụ thể này, không phải một phát hiện kinh tế đáng tin cậy.
> <br><span class="en">**The most important point in section 6 — easy to miss when reviewing for exams**: computing an extremum $age^*=28.3$ **does not automatically mean that relationship is statistically significant**. The formula $age^*=-\beta_1/2\beta_2$ always produces a number as long as $\beta_2\neq0$ — even when both $\beta_1$ and $\beta_2$ are completely non-significant (as in this very example: $p_{\beta_1}=0.64$, $p_{\beta_2}=0.68$, and the joint F-test $p=0.84$). Before interpreting the extremum in economic terms ("wages peak at age 28.3"), you must check whether the joint F-test is significant — if it is not, the $age^*$ figure is merely a mathematical artefact of this particular sample, not a reliable economic finding.</span>

## 7. Interaction terms - <span class="en">Interaction terms</span>

**Khi nào dùng**: khi câu hỏi nghiên cứu là "hiệu ứng của biến A lên $Y$ có khác nhau giữa các nhóm/giá trị của biến B hay không?" — tức nghi ngờ rằng **độ dốc** (không chỉ mức chặn) của quan hệ A→Y phụ thuộc vào B. Ví dụ minh họa: liệu **lợi tức giáo dục (return to education)** có khác nhau giữa lao động nam và nữ hay không.
<br><span class="en">**When to use it**: when the research question is "does the effect of variable A on $Y$ differ across groups/values of variable B?" — i.e. suspecting that the **slope** (not just the intercept) of the A→Y relationship depends on B. Illustrative example: whether **return to education** differs between male and female workers.</span>

$$\ln wage = \beta_1\cdot schooling + \beta_2\cdot schooling\times gender$$

Định nghĩa "return to education" là đạo hàm riêng của $\ln wage$ theo `schooling`:
<br><span class="en">Define "return to education" as the partial derivative of $\ln wage$ with respect to `schooling`:</span>

$$\frac{\partial \ln wage}{\partial schooling} = \beta_1+\beta_2\cdot gender$$

- Lao động **nữ** ($gender=0$): return to education $=\beta_1$.
<br><span class="en">- **Female** workers ($gender=0$): return to education $=\beta_1$.</span>
- Lao động **nam** ($gender=1$): return to education $=\beta_1+\beta_2$.
<br><span class="en">- **Male** workers ($gender=1$): return to education $=\beta_1+\beta_2$.</span>
- **Chênh lệch nam − nữ** $=\beta_2$ — chính là hệ số của số hạng tương tác $schooling\times gender$.
<br><span class="en">- **Male − female difference** $=\beta_2$ — exactly the coefficient of the interaction term $schooling\times gender$.</span>

**Diễn giải dấu của $\beta_2$**: $\beta_2>0$ → nam có lợi tức giáo dục cao hơn nữ; $\beta_2<0$ → nam có lợi tức giáo dục thấp hơn nữ; $\beta_2=0$ → không khác biệt giữa hai giới.
<br><span class="en">**Interpreting the sign of $\beta_2$**: $\beta_2>0$ → men have a higher return to education than women; $\beta_2<0$ → men have a lower return to education than women; $\beta_2=0$ → no difference between the two genders.</span>

### 7.1 Ví dụ số thực tế (hồi quy trên bộ dữ liệu lương) - <span class="en">Real numerical example (regression on the wage dataset)</span>

Mô hình thực tế được ước lượng đầy đủ hơn công thức rút gọn ở trên — có thêm các biến kiểm soát, và cú pháp R `schooling*gender` tự động thêm cả hai hệu ứng chính (`schooling`, `gender`) lẫn số hạng tương tác `schooling:gender`:
<br><span class="en">The actual estimated model is more complete than the simplified formula above — it adds control variables, and the R syntax `schooling*gender` automatically adds both main effects (`schooling`, `gender`) as well as the interaction term `schooling:gender`:</span>

```
log(wage) ~ age + schooling*gender + tenure + origin + science + social
```

| Biến<br><span class="en">Variable</span> | Estimate | Std. Error | t value | Pr(>|t|) |
|---|---|---|---|---|
| (Intercept) | 3.730489 | 0.250296 | 14.904 | < 2e-16 *** |
| `age` | 0.001279 | 0.003227 | 0.396 | 0.69192 |
| `schooling` | 0.050169 | 0.016433 | 3.053 | 0.00233 ** |
| `gender` | 0.553769 | 0.294931 | 1.878 | 0.06073 . |
| `tenure` | −0.009512 | 0.001255 | −7.578 | 8.07e-14 *** |
| `origin` | −0.101775 | 0.032788 | −3.104 | 0.00196 ** |
| `science` | −0.018045 | 0.052281 | −0.345 | 0.73005 |
| `social` | −0.023645 | 0.048853 | −0.484 | 0.62849 |
| `schooling:gender` | −0.037944 | 0.020852 | −1.820 | 0.06910 . |

Residual SE = 0.5044 (df = 989); $R^2$ = 0.07363; $R^2_{adj}$ = 0.06614; F = 9.827 trên (8, 989); p = 3.298e-13.
<br><span class="en">Residual SE = 0.5044 (df = 989); $R^2$ = 0.07363; $R^2_{adj}$ = 0.06614; F = 9.827 on (8, 989); p = 3.298e-13.</span>

**Diễn giải**:
<br><span class="en">**Interpretation**:</span>

- Return to education của lao động **nữ** ($\beta_1$): $0.050169$ → thêm 1 năm học, lương nữ tăng xấp xỉ **5.02%**, có ý nghĩa ở mức 1%.
<br><span class="en">- Return to education for **female** workers ($\beta_1$): $0.050169$ → an extra year of schooling raises female wages by approximately **5.02%**, significant at the 1% level.</span>
- Return to education của lao động **nam** ($\beta_1+\beta_2$): $0.050169+(-0.037944)=0.012225$ → thêm 1 năm học, lương nam chỉ tăng xấp xỉ **1.22%**.
<br><span class="en">- Return to education for **male** workers ($\beta_1+\beta_2$): $0.050169+(-0.037944)=0.012225$ → an extra year of schooling raises male wages by only approximately **1.22%**.</span>
- **Chênh lệch nam − nữ** ($\beta_2=-0.037944$): lợi tức giáo dục của nam **thấp hơn** nữ khoảng 3.79 điểm phần trăm trong mẫu này. Hệ số này có $p=0.069$ — **có ý nghĩa ở mức 10%, nhưng KHÔNG có ý nghĩa ở mức 5%** (dấu `.` trong bảng R, không phải `*`). Đây là điểm cần cẩn trọng khi báo cáo: nếu bài tập/luận văn quy định $\alpha=5\%$, kết luận đúng phải là "**chưa có đủ bằng chứng** ở mức ý nghĩa 5% cho thấy lợi tức giáo dục khác nhau giữa nam và nữ", dù dấu và độ lớn của $\beta_2$ ("nam thấp hơn nữ ~3.8 điểm phần trăm") vẫn đáng để báo cáo mô tả.
<br><span class="en">- **Male − female difference** ($\beta_2=-0.037944$): the return to education for men is **lower** than for women by about 3.79 percentage points in this sample. This coefficient has $p=0.069$ — **significant at the 10% level, but NOT significant at the 5% level** (the `.` symbol in the R table, not `*`). This is a point to be careful about when reporting: if the assignment/thesis specifies $\alpha=5\%$, the correct conclusion should be "**there is not enough evidence** at the 5% significance level that the return to education differs between men and women," even though the sign and magnitude of $\beta_2$ ("men lower than women by ~3.8 percentage points") is still worth reporting descriptively.</span>

> **Ghi chú phương pháp (một điểm cần lưu ý khi tự chạy mô hình interaction)**: công thức rút gọn ở đầu mục 7 ($\ln wage=\beta_1\cdot schooling+\beta_2\cdot schooling\times gender$) chỉ có hai số hạng, dùng để minh họa nhanh cách lấy đạo hàm riêng — nhưng mô hình R thực tế chạy ra bảng số ở trên **có đầy đủ hiệu ứng chính** của cả `schooling` lẫn `gender` (vì cú pháp `schooling*gender` trong R tự mở rộng thành `schooling + gender + schooling:gender`), cộng thêm các biến kiểm soát khác. Đây là một quy tắc chung quan trọng trong econometrics: **khi đưa một interaction term vào mô hình, luôn phải giữ lại cả hai biến gốc (main effects) trong mô hình**, nếu không hệ số của số hạng tương tác sẽ bị chệch (biased) vì gánh luôn cả phần hiệu ứng chính bị bỏ sót của biến kia.
> <br><span class="en">**Methodological note (a point to keep in mind when running your own interaction models)**: the simplified formula at the start of section 7 ($\ln wage=\beta_1\cdot schooling+\beta_2\cdot schooling\times gender$) has only two terms, used to quickly illustrate how to take the partial derivative — but the actual R model that produced the table above **includes the full main effects** of both `schooling` and `gender` (because the R syntax `schooling*gender` automatically expands to `schooling + gender + schooling:gender`), plus the other control variables. This is an important general rule in econometrics: **when adding an interaction term to a model, both original variables (main effects) must always be kept in the model**, otherwise the interaction term's coefficient will be biased because it ends up absorbing the omitted main effect of the other variable.</span>

## 8. So sánh $R^2$ giữa các dạng hàm — và vì sao không nên dùng để "chọn form tốt nhất" - <span class="en">Comparing $R^2$ across functional forms — and why it should not be used to "pick the best form"</span>

Gộp lại độ khớp (fit) của sáu mô hình chạy trên cùng bộ dữ liệu ở các mục 3, 6, 7:
<br><span class="en">Combining the fit of the six models run on the same dataset in sections 3, 6, and 7:</span>

| Dạng hàm<br><span class="en">Functional form</span> | $Y$ | $R^2$ | $R^2_{adj}$ | F | df | p-value |
|---|---|---|---|---|---|---|
| Linear | `wage` | 0.05744 | 0.05077 | 8.618 | (7, 990) | 2.731e-10 |
| Log-log | `log(wage)` | 0.06106 | 0.05442 | 9.197 | (7, 990) | 4.704e-11 |
| Log-lin | `log(wage)` | 0.07053 | 0.06396 | 10.730 | (7, 990) | 4.413e-13 |
| Lin-log | `wage` | 0.05185 | 0.04515 | 7.734 | (7, 990) | 3.978e-9 |
| Quadratic | `log(wage)` | 0.07069 | 0.06317 | 9.404 | (8, 989) | 1.406e-12 |
| Interaction | `log(wage)` | 0.07363 | 0.06614 | 9.827 | (8, 989) | 3.298e-13 |

> **Lưu ý quan trọng**: bảng trên **không nên** được dùng để kết luận "log-lin hay interaction là form tốt nhất" theo kiểu so $R^2$ trực tiếp: các mô hình có biến phụ thuộc `wage` (linear, lin-log) và các mô hình có biến phụ thuộc `log(wage)` (log-log, log-lin, quadratic, interaction) tính $TSS$ (và do đó $R^2=1-RSS/TSS$) trên **hai thang đo khác nhau** — $R^2$ giữa hai nhóm này **không so sánh trực tiếp được**. Việc chọn dạng hàm phải dựa trên **lý thuyết kinh tế** (dạng quan hệ nào hợp lý về mặt kinh tế) và **kiểm định thống kê phù hợp** (t-test/F-test cho từng hệ số, kiểm định đặc tả nếu có), không phải chỉ nhìn $R^2$ cao hơn.
> <br><span class="en">**Important note**: the table above **should not** be used to conclude that "log-lin or interaction is the best form" by directly comparing $R^2$: the models with dependent variable `wage` (linear, lin-log) and the models with dependent variable `log(wage)` (log-log, log-lin, quadratic, interaction) compute $TSS$ (and hence $R^2=1-RSS/TSS$) on **two different scales** — $R^2$ across these two groups **cannot be compared directly**. Choosing a functional form must be based on **economic theory** (which relationship form is economically sensible) and **appropriate statistical tests** (t-test/F-test for each coefficient, specification tests where applicable), not simply looking at which one has a higher $R^2$.</span>

## 9. Bẫy thi tổng hợp (exam traps) - <span class="en">Comprehensive exam traps</span>

1. **Nhầm công thức xấp xỉ và công thức chính xác giữa các dạng hàm** — đặc biệt khi đề bài yêu cầu rõ "exact effect"/"instantaneous elasticity" mà lại dùng công thức xấp xỉ, hoặc ngược lại. Lệch càng lớn khi $|\beta_1|$ càng lớn (xem mục 4).
<br><span class="en">**Confusing the approximate formula with the exact formula across functional forms** — especially when the question explicitly asks for "exact effect"/"instantaneous elasticity" but the approximate formula is used, or vice versa. The discrepancy grows as $|\beta_1|$ grows (see section 4).</span>
2. **Nhầm chiều diễn giải log-lin với log-log**: log-lin → hệ số $\times100$ = %Δ$y$ khi $X$ đổi **1 đơn vị**; log-log → hệ số (không nhân gì thêm) = %Δ$y$ khi $X$ đổi **1%**. Nhầm hai chiều này là lỗi hay gặp nhất của mục này.
<br><span class="en">**Confusing the interpretation direction of log-lin with log-log**: log-lin → coefficient $\times100$ = %Δ$y$ when $X$ changes by **1 unit**; log-log → coefficient (no further multiplication) = %Δ$y$ when $X$ changes by **1%**. Mixing up these two directions is the most common error in this section.</span>
3. **Quên nhân 100 khi chuyển từ tỉ lệ (proportion) sang phần trăm (percent)** — cả trong công thức exact ($e^{\beta_1}-1$ hay $1.01^{\beta_1}-1$ đều ra một tỉ lệ, phải nhân 100 mới ra %) lẫn khi đọc kết quả R (hệ số hồi quy $\ln y$ trên $X$ vốn đã ở dạng tỉ lệ nhỏ, VD $0.02667$, không phải đã ở dạng phần trăm $2.667$).
<br><span class="en">**Forgetting to multiply by 100 when converting from a proportion to a percent** — both in the exact formula ($e^{\beta_1}-1$ or $1.01^{\beta_1}-1$ both yield a proportion, which must be multiplied by 100 to get %) and when reading R output (the regression coefficient of $\ln y$ on $X$ is already a small proportion, e.g. $0.02667$, not already in percentage form as $2.667$).</span>
4. **Với quadratic, chỉ dùng t-test cho $\beta_2$ mà quên rằng câu hỏi "biến $X$ có ảnh hưởng gì không" (không phải chỉ "số hạng bậc hai có cần thiết không") cần F-test đồng thời cả $\beta_1$ và $\beta_2$** — xem mục 6.1.
<br><span class="en">**For quadratic forms, using only a t-test for $\beta_2$ while forgetting that the question "does variable $X$ have any effect at all" (not just "is the quadratic term needed") requires a joint F-test of both $\beta_1$ and $\beta_2$** — see section 6.1.</span>
5. **Diễn giải điểm cực trị (extremum) của quadratic như một phát hiện kinh tế chắc chắn, dù F-test đồng thời không có ý nghĩa thống kê** — công thức $age^*=-\beta_1/2\beta_2$ luôn cho ra một con số toán học, không tự động đảm bảo quan hệ đó có ý nghĩa thống kê (xem ví dụ thực tế ở mục 6: $age^*=28.3$ nhưng F-test $p=0.84$).
<br><span class="en">**Interpreting the extremum of a quadratic as a certain economic finding, even when the joint F-test is not statistically significant** — the formula $age^*=-\beta_1/2\beta_2$ always produces a mathematical number, which does not automatically guarantee that relationship is statistically significant (see the real example in section 6: $age^*=28.3$ but the F-test $p=0.84$).</span>
6. **Đưa interaction term vào mô hình mà bỏ sót một hoặc cả hai hiệu ứng chính (main effects)** — làm hệ số tương tác bị chệch, vì nó phải "gánh" luôn phần hiệu ứng chính bị bỏ sót (xem mục 7.1).
<br><span class="en">**Adding an interaction term to a model while omitting one or both main effects** — this biases the interaction coefficient, because it ends up "absorbing" the omitted main effect (see section 7.1).</span>
7. **Diễn giải hệ số của interaction term có ý nghĩa ở mức $\alpha$ này thành kết luận chắc chắn ở mức $\alpha$ khác chặt hơn** — ví dụ $\beta_2$ (interaction schooling×gender) có $p=0.069$: đúng ở mức 10% nhưng **sai** nếu báo cáo là "có ý nghĩa thống kê" khi bài yêu cầu $\alpha=5\%$.
<br><span class="en">**Interpreting an interaction term coefficient that is significant at one $\alpha$ level as a firm conclusion at a stricter $\alpha$ level** — for example $\beta_2$ (interaction schooling×gender) has $p=0.069$: correct at the 10% level but **incorrect** if reported as "statistically significant" when the question specifies $\alpha=5\%$.</span>
8. **So sánh $R^2$ giữa các mô hình có biến phụ thuộc khác thang đo** (VD `wage` so với `log(wage)`) để kết luận "form nào tốt hơn" — không hợp lệ về mặt kỹ thuật vì $TSS$ tính trên hai thang đo khác nhau (xem mục 8).
<br><span class="en">**Comparing $R^2$ between models with dependent variables on different scales** (e.g. `wage` versus `log(wage)`) to conclude "which form is better" — technically invalid because $TSS$ is computed on two different scales (see section 8).</span>
9. **Chọn sai dạng hàm rồi diễn giải hệ số theo "công thức mặc định" của dạng hàm khác** — VD chạy log-lin (`log(y) ~ X`) nhưng diễn giải hệ số theo kiểu lin-log (chia 100 thay vì nhân 100), một lỗi thường gặp khi làm bài nhanh mà không nhìn kỹ vế nào có `log`.
<br><span class="en">**Choosing the wrong functional form and then interpreting the coefficient using the "default formula" of a different form** — e.g. running log-lin (`log(y) ~ X`) but interpreting the coefficient the lin-log way (dividing by 100 instead of multiplying by 100), a common error when working quickly without carefully checking which side has `log`.</span>

## 10. Kết nối với phần còn lại của khóa học - <span class="en">Connections to the rest of the course</span>

Trang này là phần mở rộng trực tiếp của giả định **A1 (Linearity — linear in parameters)** trong [[concepts/linear-regression-model]] — toàn bộ nội dung ở đây (log-log, log-lin, lin-log, quadratic, interaction) không phải là một lớp mô hình khác, mà vẫn là OLS thông thường, chỉ khác ở bước biến đổi biến trước khi hồi quy. Vì vậy mọi giả định A2–A5, mọi công cụ suy luận (t-test, F-test, VCV/SE) đã học ở [[concepts/linear-regression-model]] áp dụng y nguyên cho các mô hình ở trang này — chỉ có **cách diễn giải hệ số** là thay đổi theo dạng hàm.
<br><span class="en">This page is a direct extension of assumption **A1 (Linearity — linear in parameters)** in [[concepts/linear-regression-model]] — everything covered here (log-log, log-lin, lin-log, quadratic, interaction) is not a different class of model, but still ordinary OLS, differing only in the variable-transformation step before running the regression. Therefore every assumption A2–A5, and every inference tool (t-test, F-test, VCV/SE) already covered in [[concepts/linear-regression-model]] applies unchanged to the models on this page — only the **way the coefficients are interpreted** changes with the functional form.</span>

Hai điểm nối tiếp đáng chú ý cho các topic sau của khóa học:
<br><span class="en">Two noteworthy connections to later topics in the course:</span>

- **Interaction term làm tăng nguy cơ multicollinearity** giữa số hạng tương tác và các biến gốc cấu thành nó (VD `schooling` và `schooling:gender` thường tương quan khá cao) — đây là lý do các số hạng tương tác hay có standard error lớn hơn kỳ vọng, liên quan trực tiếp đến chủ đề [[concepts/linear-regression-model]] mục A2 và được bàn sâu hơn ở phần multicollinearity của khóa học.
<br><span class="en">- **Interaction terms increase the risk of multicollinearity** between the interaction term and the original variables that compose it (e.g. `schooling` and `schooling:gender` are often fairly highly correlated) — this is why interaction terms tend to have larger-than-expected standard errors, directly related to the topic covered in [[concepts/linear-regression-model]] section A2, and discussed further in the multicollinearity part of the course.</span>
- **Việc chọn sai functional form** (VD dùng linear khi quan hệ thật là log-log) là một dạng **model misspecification** — không vi phạm trực tiếp A1 (mô hình vẫn tuyến tính theo $\beta$ dù chọn form nào), nhưng có thể khiến hệ số ước lượng mất đi ý nghĩa kinh tế đúng đắn dù về mặt thống kê vẫn "chạy được" bình thường. Đây là lý do khóa học luôn nhấn mạnh: chọn dạng hàm phải xuất phát từ **lý thuyết kinh tế** về bản chất quan hệ giữa các biến, không phải chọn dạng nào cho $R^2$ cao nhất (xem mục 8) hay dạng nào "chạy ra p-value đẹp".
<br><span class="en">- **Choosing the wrong functional form** (e.g. using linear when the true relationship is log-log) is a form of **model misspecification** — it does not directly violate A1 (the model remains linear in $\beta$ regardless of which form is chosen), but it can cause the estimated coefficients to lose their correct economic meaning even though the model still "runs" fine statistically. This is why the course always emphasizes: the choice of functional form must come from **economic theory** about the underlying nature of the relationship between variables, not from picking whichever form gives the highest $R^2$ (see section 8) or whichever form "produces a nice-looking p-value."</span>

## 11. Tài liệu tham khảo ứng dụng thực tế - <span class="en">Real-world application references</span>

Ba bài báo gần đây minh họa cách các functional form (log-log, log-lin, quadratic, interaction) được dùng trong nghiên cứu kinh tế thực tế (đề cương Lecture 2):
<br><span class="en">Three recent papers illustrating how functional forms (log-log, log-lin, quadratic, interaction) are used in real-world economic research (Lecture 2 syllabus):</span>

- Yang, F., & Zhan, J. (2025). Economic impact of cooperative management behavior on citrus production performance. *Finance Research Letters*, 107042. https://doi.org/10.1016/j.frl.2025.107042
- Xia, H., Li, C., Zhou, D., Zhang, Y., & Xu, J. (2020). Peasant households' land use decision-making analysis using social network analysis: A case of Tantou Village, China. *Journal of Rural Studies*, 80, 452-468. https://doi.org/10.1016/j.jrurstud.2020.07.004
- Gonzales, J. T. (2023). Implications of AI innovation on economic growth: A panel data study. *Journal of Economic Structures*, 12(1), 13. https://doi.org/10.1186/s40008-023-00307-w
