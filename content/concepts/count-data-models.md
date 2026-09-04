---
title: "Lecture 12: Count Data Models (Poisson, Negative Binomial, ZINB)"
type: concept
status: mature
tags: [count-data, poisson, negative-binomial, zero-inflated, limited-dependent-variable]
sources: ["[[sources/slides-10-count-data-models]]"]
related: ["[[concepts/binary-response-models]]", "[[concepts/linear-regression-model]]"]
lecture: 12
assignment: []
updated: 2026-09-04
---

> **Cách đọc trang này**: Topic 10 tiếp tục mạch **Models for Limited Dependent Variables** mở đầu từ [[concepts/binary-response-models]] (Topic 7) — cùng khung Maximum Likelihood, cùng logic "dùng hàm liên kết (link function) phi tuyến vì bản chất biến phụ thuộc không cho phép mô hình tuyến tính trực tiếp".
> <br><span class="en">**How to read this page**: Topic 10 continues the **Models for Limited Dependent Variables** thread opened in [[concepts/binary-response-models]] (Topic 7) — same Maximum Likelihood framework, same logic of "using a nonlinear link function because the nature of the dependent variable rules out a direct linear model".</span>
> Khác biệt duy nhất: ở Topic 7, biến phụ thuộc là nhị phân (0/1) — "có xảy ra hay không"; ở Topic 10, biến phụ thuộc là **số đếm** (0, 1, 2, 3, …) — "xảy ra bao nhiêu lần".
> <br><span class="en">The one difference: in Topic 7 the dependent variable is binary (0/1) — "did it happen or not"; in Topic 10 the dependent variable is a **count** (0, 1, 2, 3, …) — "how many times did it happen".</span>

**Lecture 12** trong đề cương (CO Topic 10) — chưa có assignment riêng.
<br><span class="en">**Lecture 12** in the syllabus (CO Topic 10) — no dedicated assignment yet.</span>
> Ví dụ dữ liệu xuyên suốt trang này chính là **cùng bộ khảo sát vaccine COVID-19** dùng ở Topic 7 (377 người trả lời tại TP.HCM), chỉ đổi biến phụ thuộc từ `dself` (nhị phân — cá nhân có quyết định tiêm hay không) sang `dhh` (đếm — số liều vaccine mua cho các thành viên trong hộ gia đình).
> <br><span class="en">The example data running through this page is the **same COVID-19 vaccine survey** used in Topic 7 (377 respondents in Ho Chi Minh City), only swapping the dependent variable from `dself` (binary — whether the individual decided to get vaccinated) to `dhh` (count — the number of vaccine doses purchased for the members of the household).</span>
> Đây là minh họa trực tiếp cho nguyên tắc chọn mô hình: **chọn theo bản chất của biến phụ thuộc, không phải theo thói quen hay theo dữ liệu có sẵn**.
> <br><span class="en">This is a direct illustration of the model-choice principle: **choose according to the nature of the dependent variable, not out of habit or whatever data happens to be available**.</span>

## 1. Vì sao cần một họ mô hình riêng cho "count data"? - <span class="en">Why do we need a separate family of models for "count data"?</span>

### 1.1 Count data là gì? - <span class="en">What is count data?</span>

**Count data** (dữ liệu đếm) là biến phụ thuộc đo **số lần một sự kiện xảy ra** trong một khoảng thời gian/đơn vị quan sát cho trước — luôn là **số nguyên không âm**:
<br><span class="en">**Count data** is a dependent variable that measures **the number of times an event occurs** within a given time period/unit of observation — always a **non-negative integer**:</span>

$$y = 0, 1, 2, \dots, K$$

Slide gốc liệt kê các ví dụ kinh điển trong kinh tế lượng ứng dụng:
<br><span class="en">The original slide lists the classic examples in applied econometrics:</span>

- Số lời chào mua lại (takeover bids) mà một doanh nghiệp mục tiêu nhận được.
<br><span class="en">The number of takeover bids a target firm receives.</span>
- Số lần trả góp tín dụng bị trễ hạn (number of unpaid credit installment).
<br><span class="en">The number of unpaid credit installments.</span>
- Số vụ tai nạn (number of accidents).
<br><span class="en">The number of accidents.</span>
- Số khoản vay thế chấp được trả trước hạn (number of prepaid mortgage loans).
<br><span class="en">The number of prepaid mortgage loans.</span>

Trong ví dụ xuyên suốt trang này (mục 4): `dhh` — số liều vaccine COVID-19 mà một hộ gia đình quyết định mua cho các thành viên trong nhà. Điểm chung của mọi ví dụ: đây là **số lượng biến cố xảy ra trong một khoảng thời gian nhất định**, không phải một đại lượng liên tục đo lường được ở bất kỳ độ chính xác nào.
<br><span class="en">In the example running through this page (section 4): `dhh` — the number of COVID-19 vaccine doses a household decides to purchase for its members. What all these examples share: this is **the number of events occurring within a given time period**, not a continuous quantity that can be measured to any degree of precision.</span>

### 1.2 Tại sao OLS không phù hợp? - <span class="en">Why is OLS not appropriate?</span>

OLS ([[concepts/linear-regression-model]]) ngầm giả định $y$ là biến liên tục, có thể nhận bất kỳ giá trị thực nào, với sai số phân phối chuẩn và phương sai không đổi (A4, A5). Cả ba giả định ngầm này đều bị count data "phá vỡ":
<br><span class="en">OLS ([[concepts/linear-regression-model]]) implicitly assumes that $y$ is continuous, able to take any real value, with normally distributed errors and constant variance (A4, A5). All three implicit assumptions are "broken" by count data:</span>

1. **Dự đoán có thể âm hoặc không phải số nguyên**: $\hat y_i = Xb$ trong OLS là một hàm tuyến tính không giới hạn — không có cơ chế nào ngăn nó cho ra kết quả như $\hat y = -2.7$. Với biến đếm, "số vaccine mua = −2.7" không có ý nghĩa gì trong thực tế.
<br><span class="en">**Predictions can be negative or non-integer**: $\hat y_i = Xb$ in OLS is an unbounded linear function — nothing stops it from producing a result like $\hat y = -2.7$. For a count variable, "number of vaccines purchased = −2.7" is meaningless in practice.</span>
2. **Phân phối chuẩn không khớp với số nguyên nhỏ**: khi phần lớn quan sát tập trung ở các giá trị nhỏ (0, 1, 2, 3…) và có nhiều quan sát bằng 0, hình dạng phân phối thực tế lệch phải (right-skewed) và rời rạc — khác hẳn đường cong chuông đối xứng, liên tục mà OLS/A5 giả định.
<br><span class="en">**The normal distribution does not match small integers**: when most observations cluster at small values (0, 1, 2, 3…) with many observations at zero, the actual distribution's shape is right-skewed and discrete — quite unlike the symmetric, continuous bell curve that OLS/A5 assumes.</span>
3. **Phương sai tăng theo trung bình theo một cấu trúc đặc thù**: với hầu hết dữ liệu đếm, quan sát nào có kỳ vọng đếm cao thường cũng dao động nhiều hơn quanh kỳ vọng đó. Đây không phải heteroskedasticity ngẫu nhiên như ở [[concepts/heteroskedasticity]], mà là một **quy luật cấu trúc** gắn liền với chính bản chất số đếm — và chính quy luật này định nghĩa nên phân phối Poisson ở mục 2.
<br><span class="en">**Variance increases with the mean following a specific structure**: for most count data, an observation with a higher expected count also tends to fluctuate more around that expectation. This is not random heteroskedasticity as in [[concepts/heteroskedasticity]], but a **structural regularity** tied directly to the nature of counts — and this very regularity is what defines the Poisson distribution in section 2.</span>

## 2. Phân phối Poisson — nền tảng - <span class="en">The Poisson distribution — foundation</span>

### 2.1 Trực giác - <span class="en">Intuition</span>

**Phân phối Poisson** mô tả xác suất một sự kiện xảy ra đúng $k$ lần trong một khoảng thời gian cho trước, khi biết **tần suất trung bình** của sự kiện đó là $\lambda$:
<br><span class="en">The **Poisson distribution** describes the probability that an event occurs exactly $k$ times within a given time period, given that the event's **mean rate** is $\lambda$:</span>

$$Pr(y=k)=\frac{e^{-\lambda}\lambda^k}{k!}, \qquad \lambda\ge0$$

Toàn bộ phân phối Poisson chỉ có **một tham số duy nhất** $\lambda$ — và tham số này đóng vai trò kép, vừa là **trung bình** (mean) vừa là **phương sai** (variance):
<br><span class="en">The entire Poisson distribution has only **one single parameter** $\lambda$ — and this parameter plays a dual role, serving as both the **mean** and the **variance**:</span>

$$E[Y]=Var[Y]=\lambda$$

### 2.2 Equidispersion — tính chất "mean = variance" - <span class="en">Equidispersion — the "mean = variance" property</span>

Đây là **đặc điểm quan trọng nhất, đặc trưng nhất của Poisson**, gọi là **equidispersion**. Trực giác: nếu $\lambda$ nhỏ (sự kiện hiếm, VD trung bình xảy ra 1 lần), Poisson đồng thời dự đoán rằng độ dao động xung quanh con số đó cũng nhỏ. Nếu $\lambda$ lớn (sự kiện phổ biến, VD trung bình 100 lần), Poisson dự đoán độ dao động cũng lớn tương ứng — **phương sai luôn tăng đúng cùng một nhịp với trung bình, không nhanh hơn, không chậm hơn**. Đây chính là lý do phân phối Poisson giải quyết được vấn đề #3 ở mục 1.2 (phương sai gắn với trung bình một cách có cấu trúc) — nhưng cũng chính là **điểm yếu cốt lõi** của nó, sẽ được khai thác ở mục 6.
<br><span class="en">This is the **single most important, most defining feature of Poisson**, called **equidispersion**. Intuition: if $\lambda$ is small (a rare event, e.g. occurring once on average), Poisson simultaneously predicts that the fluctuation around that number is also small. If $\lambda$ is large (a common event, e.g. 100 times on average), Poisson predicts a correspondingly large fluctuation — **variance always grows at exactly the same pace as the mean, no faster, no slower**. This is precisely why the Poisson distribution solves problem #3 from section 1.2 (variance tied to the mean in a structured way) — but it is also its **core weakness**, which will be exploited in section 6.</span>

**Tại sao equidispersion thường bị vi phạm trong thực tế?** Vì đây là một giả định rất chặt: nó đòi hỏi *mọi* cá nhân/đơn vị có cùng giá trị $X$ phải có **cùng một** $\lambda$ y hệt nhau — không có sai khác nào khác ngoài những gì $X$ giải thích được. Trong thực tế luôn tồn tại **dị biệt không quan sát được** (unobserved heterogeneity) giữa các cá nhân: hai hộ gia đình giống hệt nhau về mọi biến $X$ đưa vào mô hình (thu nhập, quy mô hộ, tuổi…) vẫn có thể có xu hướng mua vaccine khác nhau vì những lý do không đo lường được (niềm tin vào y tế, mức độ e ngại rủi ro, thông tin riêng từng hộ…). Dị biệt này làm phương sai *thực tế* của $y$ lớn hơn những gì Poisson dự đoán tại cùng một $\lambda$ — đây chính là cơ chế kinh tế học đứng sau **overdispersion** (mục 6).
<br><span class="en">**Why is equidispersion often violated in practice?** Because it is a very tight assumption: it requires *every* individual/unit with the same value of $X$ to have **exactly the same** $\lambda$ — with no discrepancy other than what $X$ explains. In reality there is always **unobserved heterogeneity** between individuals: two households identical on every $X$ variable in the model (income, household size, age…) can still have different tendencies to purchase vaccines for reasons that are not measured (trust in healthcare, degree of risk aversion, household-specific information…). This heterogeneity makes the *actual* variance of $y$ larger than what Poisson predicts at the same $\lambda$ — this is exactly the economic mechanism behind **overdispersion** (section 6).</span>

## 3. Mô hình hóa: The Poisson Model - <span class="en">Modeling: the Poisson Model</span>

Để đưa các biến giải thích $X$ vào, ta mô hình hóa $\lambda$ như một hàm của $X$:
<br><span class="en">To bring in explanatory variables $X$, we model $\lambda$ as a function of $X$:</span>

$$E(y_i|X)=\lambda=e^{X_i\beta}$$

Dùng dạng mũ $e^{X_i\beta}$ (thay vì $X_i\beta$ trực tiếp) để đảm bảo $\lambda>0$ với **mọi** giá trị của $X_i\beta$ (kể cả âm) — cùng logic dùng hàm liên kết phi tuyến để giữ đại lượng dự đoán trong miền hợp lệ, như Logit/Probit giữ xác suất trong $[0,1]$ (xem [[concepts/binary-response-models]]).
<br><span class="en">The exponential form $e^{X_i\beta}$ (rather than $X_i\beta$ directly) is used to guarantee $\lambda>0$ for **every** value of $X_i\beta$ (including negative ones) — the same logic of using a nonlinear link function to keep the predicted quantity within its valid domain, just as Logit/Probit keep probability within $[0,1]$ (see [[concepts/binary-response-models]]).</span>

$$Pr(y=k)=\frac{e^{-\lambda}\lambda^k}{k!}=\frac{e^{-e^{X_i\beta}}\big(e^{X_i\beta}\big)^k}{k!}$$

**Log-likelihood function**:
<br><span class="en">**Log-likelihood function**:</span>

$$\log L=\sum_{i=1}^N\Big[-e^{X_i\beta}+y_iX_i\beta-\log(y_i!)\Big]$$

**Ước lượng**: Maximum Likelihood (ML) — không có nghiệm dạng đóng như OLS ($b=(X'X)^{-1}X'y$), phải tối ưu hóa số (numerical optimization), giống hệt Logit/Probit.
<br><span class="en">**Estimation**: Maximum Likelihood (ML) — there is no closed-form solution like OLS ($b=(X'X)^{-1}X'y$); it requires numerical optimization, exactly like Logit/Probit.</span>

### 3.1 Marginal effect - <span class="en">Marginal effect</span>

$$\frac{\partial E(y_i|X)}{\partial X_i}=e^{X_i\beta}\cdot\beta=\lambda\cdot\beta$$

Giống hệt logic của Logit/Probit: marginal effect **không phải là hằng số** $\beta$ — nó tỷ lệ thuận với chính giá trị kỳ vọng $\lambda$ tại điểm đang xét. Hai hệ quả quan trọng:
<br><span class="en">Exactly the same logic as Logit/Probit: the marginal effect **is not the constant** $\beta$ — it is proportional to the expected value $\lambda$ itself at the point being considered. Two important consequences:</span>

- Ảnh hưởng biên của $X$ lên $y$ **lớn hơn** ở những quan sát vốn đã có $\lambda$ cao, và **nhỏ hơn** ở những quan sát có $\lambda$ thấp — cùng một $\beta$ nhưng tạo ra tác động tuyệt đối khác nhau tùy hồ sơ quan sát.
<br><span class="en">The marginal effect of $X$ on $y$ is **larger** for observations that already have a high $\lambda$, and **smaller** for observations with a low $\lambda$ — the same $\beta$ produces different absolute impacts depending on the observation's profile.</span>
- Phải chọn báo cáo marginal effect tại một điểm cụ thể — **marginal effects at the mean (MEM)** hoặc **average marginal effects (AME)** — xem ví dụ số ở mục 9.2.
<br><span class="en">One must choose to report the marginal effect at a specific point — **marginal effects at the mean (MEM)** or **average marginal effects (AME)** — see the numerical example in section 9.2.</span>

## 4. Bộ dữ liệu minh họa: Nhu cầu vaccine COVID-19 (household count) - <span class="en">Illustrative dataset: COVID-19 vaccine demand (household count)</span>

**Bối cảnh**: nhu cầu đối với một loại vaccine COVID-19 giả định. Dữ liệu: 377 người trả lời tại TP.HCM (data file `EMP4.dta`) — **đúng bộ dữ liệu đã dùng ở Topic 7** ([[concepts/binary-response-models]]), chỉ đổi biến phụ thuộc.
<br><span class="en">**Context**: demand for a hypothetical COVID-19 vaccine. Data: 377 respondents in Ho Chi Minh City (data file `EMP4.dta`) — **exactly the dataset used in Topic 7** ([[concepts/binary-response-models]]), only the dependent variable changes.</span>

| Biến - <span class="en">Variable</span> | Ý nghĩa - <span class="en">Meaning</span> |
|---|---|
| `dhh` | **Biến phụ thuộc (count)**: số liều vaccine COVID-19 mua cho các thành viên trong hộ gia đình<br><span class="en">**Dependent variable (count)**: number of COVID-19 vaccine doses purchased for household members</span> |
| `efficacy80` | 1 = hiệu quả vaccine 80%, 0 = 50%<br><span class="en">1 = vaccine efficacy 80%, 0 = 50%</span> |
| `duration3` | 1 = thời gian hiệu lực 3 năm, 0 = 1 năm<br><span class="en">1 = duration of effect 3 years, 0 = 1 year</span> |
| `priceUS` | Giá vaccine (USD/2 liều)<br><span class="en">Vaccine price (USD/2 doses)</span> |
| `pbenefit` | 1 = người trả lời được cung cấp thông tin về ngoại tác (externality) của việc tiêm chủng<br><span class="en">1 = respondent was given information about the externality of vaccination</span> |
| `hhincomeUS` | Tổng thu nhập hộ gia đình hàng tháng (USD/tháng)<br><span class="en">Total monthly household income (USD/month)</span> |
| `hhsize` | Quy mô hộ gia đình (số thành viên)<br><span class="en">Household size (number of members)</span> |
| `age` | Tuổi người trả lời (năm)<br><span class="en">Respondent's age (years)</span> |
| `male` | Giới tính, 1 = nam, 0 = nữ<br><span class="en">Gender, 1 = male, 0 = female</span> |
| `risk` (ordinal) | Nhận thức về rủi ro nhiễm COVID-19: "Very unlikely", "Unlikely", "Neither", "Likely", "Very likely" — chuyển thành 4 dummy (`unlikely`, `neither`, `likely`, `verylikely`), nhóm nền (base) là "Very unlikely"<br><span class="en">Perceived risk of COVID-19 infection: "Very unlikely", "Unlikely", "Neither", "Likely", "Very likely" — converted into 4 dummies (`unlikely`, `neither`, `likely`, `verylikely`), with base group "Very unlikely"</span> |

Ví dụ ở đây dùng lại **chính xác** bộ khảo sát vaccine của [[concepts/binary-response-models]] — chỉ đổi biến phụ thuộc từ `dself` (nhị phân, quyết định cá nhân có tiêm hay không) sang `dhh` (đếm, số liều mua cho cả hộ): cùng một khảo sát, hai câu hỏi nghiên cứu khác nhau đòi hỏi hai họ mô hình khác nhau.
<br><span class="en">The example here reuses **exactly** the same vaccine survey as [[concepts/binary-response-models]] — only swapping the dependent variable from `dself` (binary, individual decision to get vaccinated or not) to `dhh` (count, number of doses purchased for the whole household): the same survey, two different research questions requiring two different model families.</span>

### 4.1 Thống kê mô tả — và một tín hiệu "cảnh báo sớm" - <span class="en">Descriptive statistics — and an "early warning" signal</span>

| Biến - <span class="en">Variable</span> | Mean | SD | Min | Max |
|---|---|---|---|---|
| `dhh` | 4.13 | 2.80 | 0 | 24 |
| `hhsize` | 4.69 | 2.51 | 1 | 25 |
| `age` | 43.32 | 14.00 | 18 | 86 |
| `priceUS` | 18.38 | 13.72 | 4.33 | 43.29 |
| `hhincomeUS` | 949.91 | 790.36 | 108.23 | 3787.88 |
| `pbenefit`, `efficacy80`, `duration3` | ≈0.49–0.50 | ≈0.50 | 0 | 1 |
| `male` | 0.32 | 0.47 | 0 | 1 |

Phân phối chi tiết của `dhh` (n=377): 0→73, 1→1, 2→15, 3→35, 4→74, 5→82, 6→47, 7→16, 8→14, 9→10, 10→4, 11→4, 12→1, 24→1 (một quan sát ngoại lai rõ rệt ở 24). Histogram trong slide cho thấy hình dạng **lệch phải điển hình của count data**: khối lượng quan sát tập trung ở 0–9, đuôi phải dài và mỏng.
<br><span class="en">Detailed distribution of `dhh` (n=377): 0→73, 1→1, 2→15, 3→35, 4→74, 5→82, 6→47, 7→16, 8→14, 9→10, 10→4, 11→4, 12→1, 24→1 (one clear outlier at 24). The histogram in the slide shows the shape **typical right-skew of count data**: the bulk of observations concentrate at 0–9, with a long, thin right tail.</span>

Phân bố `risk` (n=377): Very unlikely 87, Unlikely 109, Neither 129, Likely 42, Very likely 10.
<br><span class="en">Distribution of `risk` (n=377): Very unlikely 87, Unlikely 109, Neither 129, Likely 42, Very likely 10.</span>

**Tín hiệu cảnh báo sớm, tính được ngay từ đây, trước khi chạy bất kỳ mô hình nào**: $SD(dhh)=2.80 \Rightarrow Var(dhh)=2.80^2=7.84$, trong khi $Mean(dhh)=4.13$. Tỷ lệ
<br><span class="en">**An early warning signal, computable right here, before running any model**: $SD(dhh)=2.80 \Rightarrow Var(dhh)=2.80^2=7.84$, while $Mean(dhh)=4.13$. The ratio</span>

$$\frac{Var(dhh)}{Mean(dhh)}=\frac{7.84}{4.13}\approx1.90$$

Nếu Poisson đúng (equidispersion), tỷ lệ này phải xấp xỉ 1. Con số ≈1.90 — phương sai thô gần **gấp đôi** trung bình thô — là dấu hiệu định tính sớm cho thấy khả năng cao dữ liệu này bị **overdispersion**, trước khi cần đến kiểm định chính thức (mục 6.2). Đây là một phép tính minh họa tự suy ra từ thống kê mô tả của slide, không phải một con số slide tính sẵn — nhưng là bước kiểm tra trực giác nên làm theo thói quen trước khi ước lượng Poisson.
<br><span class="en">If Poisson holds (equidispersion), this ratio should be approximately 1. The figure ≈1.90 — raw variance nearly **double** the raw mean — is an early qualitative sign that this data is likely subject to **overdispersion**, before any formal test is needed (section 6.2). This is an illustrative calculation derived from the slide's descriptive statistics, not a figure the slide computes directly — but it is a sanity check worth doing as a habit before estimating a Poisson model.</span>

## 5. Ước lượng Poisson model trên dữ liệu vaccine - <span class="en">Estimating the Poisson model on the vaccine data</span>

```r
poisson = glm(dhh ~ efficacy80+duration3+priceUS+pbenefit+hhincomeUS
              +hhsize+age+male+unlikely+neither+likely+verylikely,
              data=data, family="poisson")
```

| Biến - <span class="en">Variable</span> | $\hat\beta$ | SE | p-value |
|---|---|---|---|
| (Intercept) | 1.401 | 0.1264 | <2e-16 *** |
| `efficacy80` | 0.04788 | 0.05161 | 0.354 |
| `duration3` | −0.03719 | 0.05146 | 0.470 |
| `priceUS` | −0.007833 | 0.001980 | 7.61e-05 *** |
| `pbenefit` | 0.08713 | 0.05117 | 0.089 . |
| `hhincomeUS` | 0.0001133 | 0.00003055 | 0.000207 *** |
| `hhsize` | 0.06796 | 0.007993 | <2e-16 *** |
| `age` | −0.009329 | 0.001905 | 9.75e-07 *** |
| `male` | −0.08896 | 0.05581 | 0.111 |
| `unlikely` | 0.06480 | 0.07301 | 0.375 |
| `neither` | 0.1073 | 0.07072 | 0.129 |
| `likely` | 0.05306 | 0.09525 | 0.578 |
| `verylikely` | 0.4176 | 0.1404 | 0.00293 ** |

Null deviance 906.53 (df=376); Residual deviance 742.67 (df=364); AIC 1813.1.
<br><span class="en">Null deviance 906.53 (df=376); Residual deviance 742.67 (df=364); AIC 1813.1.</span>

**Overall significance** ($H_0$: mọi hệ số góc = 0), qua kiểm định dựa trên deviance: `1-pchisq(poisson$null.deviance-poisson$deviance, poisson$df.null-poisson$df.residual)` = **0** (làm tròn xuống dưới độ chính xác máy tính, tức p-value cực nhỏ) → bác bỏ mạnh $H_0$, các biến giải thích cùng nhau có ý nghĩa thống kê.
<br><span class="en">**Overall significance** ($H_0$: all slope coefficients = 0), via a deviance-based test: `1-pchisq(poisson$null.deviance-poisson$deviance, poisson$df.null-poisson$df.residual)` = **0** (rounded below computer precision, i.e. an extremely small p-value) → strongly reject $H_0$, the explanatory variables are jointly statistically significant.</span>

**Test for joint significance** của nhóm 4 dummy `risk` (Wald test, `Terms=10:13`): $X^2=9.6$, $df=4$, $p=0.048$ → bác bỏ $H_0$ ở mức 5% (nhưng rất sát ngưỡng — đây sẽ là điểm mấu chốt của mục 8.2).
<br><span class="en">**Test for joint significance** of the group of 4 `risk` dummies (Wald test, `Terms=10:13`): $X^2=9.6$, $df=4$, $p=0.048$ → reject $H_0$ at the 5% level (but very close to the threshold — this will be the crux of section 8.2).</span>

## 6. Overdispersion & Underdispersion — trực quan - <span class="en">Overdispersion & Underdispersion — intuition</span>

### 6.1 Khi Poisson "sai" - <span class="en">When Poisson is "wrong"</span>

Vì Poisson buộc $Var(y)=E(y)$, có hai kiểu vi phạm có thể xảy ra:
<br><span class="en">Because Poisson forces $Var(y)=E(y)$, two kinds of violation can occur:</span>

- **Overdispersion**: phương sai tăng **nhanh hơn** trung bình ($Var>Mean$) — **phổ biến hơn nhiều** trong thực tế. Cơ chế điển hình: dị biệt không quan sát được giữa các cá nhân (mục 2.2) — một số hộ gia đình có xu hướng "mua nhiều vaccine" nói chung (vì lý do không đo được), số khác có xu hướng "mua ít" nói chung; sự phân tầng ẩn này làm biến thiên thực tế của $y$ lớn hơn Poisson dự đoán. Một cơ chế khác cũng hay gặp: **excess zeros** (quá nhiều quan sát bằng 0 so với dự đoán) — sẽ bàn kỹ ở mục 10.
<br><span class="en">**Overdispersion**: variance grows **faster** than the mean ($Var>Mean$) — **much more common** in practice. The typical mechanism: unobserved heterogeneity between individuals (section 2.2) — some households tend to "buy a lot of vaccine" in general (for unmeasured reasons), others tend to "buy little" in general; this hidden stratification makes the actual variation of $y$ larger than Poisson predicts. Another common mechanism: **excess zeros** (far more zero observations than predicted) — discussed in detail in section 10.</span>
- **Underdispersion**: phương sai tăng **chậm hơn** trung bình ($Var<Mean$) — ít gặp hơn hẳn. Thường xảy ra khi có một cơ chế *điều tiết* tự nhiên làm số đếm ổn định quanh trung bình hơn mức ngẫu nhiên thuần túy — ví dụ số chuyến xe buýt khởi hành mỗi giờ theo đúng lịch trình cố định sẽ dao động ít hơn nhiều so với một quá trình Poisson thuần túy, vì lịch trình "kìm" biến thiên lại.
<br><span class="en">**Underdispersion**: variance grows **slower** than the mean ($Var<Mean$) — noticeably less common. It usually occurs when there is a natural *regulating* mechanism that keeps counts more stable around the mean than pure randomness would — e.g. the number of buses departing per hour on a fixed schedule fluctuates much less than a pure Poisson process would, because the schedule "holds back" the variation.</span>

### 6.2 Kiểm định chính thức - <span class="en">Formal test</span>

```r
AER::dispersiontest(poisson)
```

Kết quả: $z=3.3973$, $p=0.0003403$, $H_a$: "true dispersion is greater than 1", ước lượng dispersion $=1.366071$.
<br><span class="en">Result: $z=3.3973$, $p=0.0003403$, $H_a$: "true dispersion is greater than 1", estimated dispersion $=1.366071$.</span>

→ Bác bỏ mạnh $H_0$ (equidispersion) ở mức ý nghĩa rất cao, xác nhận **overdispersion** — nhất quán với tín hiệu định tính đã thấy ở mục 4.1 (tỷ lệ $Var/Mean$ thô ≈1.90; con số 1.366 ở đây là ước lượng dispersion *dựa trên mô hình đã fit* — hai con số liên quan về mặt khái niệm nhưng không phải cùng một phép tính, nên không kỳ vọng chúng trùng khớp).
<br><span class="en">→ Strongly reject $H_0$ (equidispersion) at a very high significance level, confirming **overdispersion** — consistent with the qualitative signal already seen in section 4.1 (raw $Var/Mean$ ratio ≈1.90; the 1.366 figure here is a dispersion estimate *based on the fitted model* — the two numbers are conceptually related but not the same calculation, so they are not expected to match exactly).</span>

**Hệ quả trực tiếp**: khi có overdispersion mà vẫn dùng Poisson, Standard Error của Poisson bị **đánh giá thấp** (underestimate) — vì công thức SE của Poisson ngầm giả định $Var=Mean$ đúng. SE nhỏ hơn thực tế → t/z-statistic lớn hơn thực tế → p-value nhỏ hơn thực tế → **dễ kết luận nhầm là có ý nghĩa thống kê trong khi thực ra không có**. Mục 8.2 minh họa hệ quả này bằng con số cụ thể.
<br><span class="en">**Direct consequence**: when overdispersion is present but Poisson is still used, the Poisson Standard Error is **underestimated** — because the Poisson SE formula implicitly assumes $Var=Mean$ holds. A smaller-than-true SE → a larger-than-true t/z-statistic → a smaller-than-true p-value → **an easy false conclusion of statistical significance when in fact there is none**. Section 8.2 illustrates this consequence with concrete numbers.</span>

## 7. Negative Binomial (NB) Model — nới lỏng equidispersion - <span class="en">Negative Binomial (NB) Model — relaxing equidispersion</span>

### 7.1 Trực giác: NB "nới lỏng" giả định của Poisson bằng cách nào? - <span class="en">Intuition: how does NB "relax" the Poisson assumption?</span>

Poisson buộc mọi quan sát cùng $X$ phải có đúng một $\lambda$, không chừa chỗ cho dị biệt cá nhân không quan sát được. **Negative Binomial (NB)** giải quyết đúng vấn đề đó: nó thêm một **tham số phân tán** (dispersion parameter) $\alpha \ge 0$, cho phép phương sai tăng **nhanh hơn** trung bình một lượng tỷ lệ với $\alpha$ — về bản chất, $\alpha$ đo lường mức độ dị biệt không quan sát được còn sót lại sau khi đã kiểm soát các biến $X$ trong mô hình. $\alpha$ càng lớn, dị biệt càng nhiều, overdispersion càng nặng.
<br><span class="en">Poisson forces every observation with the same $X$ to have exactly one $\lambda$, leaving no room for unobserved individual heterogeneity. **Negative Binomial (NB)** solves precisely that problem: it adds a **dispersion parameter** $\alpha \ge 0$, allowing variance to grow **faster** than the mean by an amount proportional to $\alpha$ — in essence, $\alpha$ measures the amount of unobserved heterogeneity remaining after controlling for the $X$ variables in the model. The larger $\alpha$ is, the more heterogeneity there is, and the more severe the overdispersion.</span>

### 7.2 Công thức - <span class="en">Formula</span>

$$Pr(y=k)=\frac{\Gamma(k+\theta)}{\Gamma(k+1)\Gamma(\theta)}p^\theta(1-p)^k, \qquad \theta=\frac{1}{\alpha},\; p=\frac{1}{1+\alpha\mu}$$

trong đó $\Gamma(\cdot)$ là hàm Gamma: với $y$ nguyên không âm, $\Gamma(y)=(y-1)!$; tổng quát hơn, $\Gamma(y)=\int_0^{+\infty}x^{y-1}e^{-x}dx$.
<br><span class="en">where $\Gamma(\cdot)$ is the Gamma function: for a non-negative integer $y$, $\Gamma(y)=(y-1)!$; more generally, $\Gamma(y)=\int_0^{+\infty}x^{y-1}e^{-x}dx$.</span>

Trung bình **không đổi** so với Poisson: $E(y_i|X)=\lambda=e^{X_i\beta}$. Nhưng **phương sai**:
<br><span class="en">The mean is **unchanged** relative to Poisson: $E(y_i|X)=\lambda=e^{X_i\beta}$. But the **variance**:</span>

$$Var(y_i|X)=\lambda+\alpha\lambda^2$$

### 7.3 Vì sao NB "nesting" Poisson tại $\alpha=0$ - <span class="en">Why NB "nests" Poisson at $\alpha=0$</span>

Nhìn vào công thức phương sai: nếu $\alpha=0$, thì $Var(y_i|X)=\lambda$ — **đúng bằng** giả định equidispersion của Poisson. Nói cách khác, **Poisson là một trường hợp đặc biệt của NB, khi $\alpha=0$** — đây gọi là quan hệ **nesting** (Poisson "lồng bên trong" NB như một ràng buộc). Hệ quả thực dụng quan trọng nhất: **kiểm định "NB hay Poisson" chính là kiểm định thống kê $H_0:\alpha=0$** — nếu bác bỏ được $H_0$, có bằng chứng NB phù hợp hơn Poisson (mục 8.3).
<br><span class="en">Looking at the variance formula: if $\alpha=0$, then $Var(y_i|X)=\lambda$ — **exactly equal to** the Poisson equidispersion assumption. In other words, **Poisson is a special case of NB, when $\alpha=0$** — this is called a **nesting** relationship (Poisson is "nested inside" NB as a restriction). The most practically important consequence: **testing "NB or Poisson" is exactly the statistical test $H_0:\alpha=0$** — if $H_0$ can be rejected, there is evidence NB fits better than Poisson (section 8.3).</span>

## 8. Ước lượng NB trên dữ liệu vaccine + so sánh với Poisson - <span class="en">Estimating NB on the vaccine data + comparison with Poisson</span>

```r
negbin = glm.nb(dhh ~ efficacy80+duration3+priceUS+pbenefit+hhincomeUS
                +hhsize+age+male+unlikely+neither+likely+verylikely,
                data=data)
```

(`init.theta = 6.680685757`, `link = log`)

| Biến - <span class="en">Variable</span> | $\hat\beta$ (NB) | SE (NB) | p-value | So sánh SE với Poisson - <span class="en">SE compared to Poisson</span> |
|---|---|---|---|---|
| (Intercept) | 1.361 | 0.1634 | <2e-16 *** | — |
| `efficacy80` | 0.05406 | 0.06618 | 0.414 | — |
| `duration3` | −0.03044 | 0.06606 | 0.645 | — |
| `priceUS` | −0.007658 | 0.002482 | 0.00204 ** | SE gấp **1.25×** Poisson<br><span class="en">SE is **1.25×** Poisson</span> |
| `pbenefit` | 0.08533 | 0.06558 | 0.193 | — |
| `hhincomeUS` | 0.0001039 | 0.00004166 | 0.01264 * | SE gấp **1.36×** Poisson<br><span class="en">SE is **1.36×** Poisson</span> |
| `hhsize` | 0.07759 | 0.01199 | 9.83e-11 *** | SE gấp **1.50×** Poisson<br><span class="en">SE is **1.50×** Poisson</span> |
| `age` | −0.009695 | 0.002433 | 6.73e-05 *** | SE gấp **1.28×** Poisson<br><span class="en">SE is **1.28×** Poisson</span> |
| `male` | −0.0860 | 0.07123 | 0.227 | — |
| `unlikely` | 0.05616 | 0.09340 | 0.548 | SE gấp **1.28×** Poisson<br><span class="en">SE is **1.28×** Poisson</span> |
| `neither` | 0.1206 | 0.09002 | 0.180 | SE gấp **1.27×** Poisson<br><span class="en">SE is **1.27×** Poisson</span> |
| `likely` | 0.1003 | 0.1209 | 0.407 | SE gấp **1.27×** Poisson<br><span class="en">SE is **1.27×** Poisson</span> |
| `verylikely` | 0.4376 | 0.1931 | 0.02348 * | SE gấp **1.38×** Poisson<br><span class="en">SE is **1.38×** Poisson</span> |

**Điểm mấu chốt nhìn từ bảng trên**: chuyển từ Poisson sang NB, hệ số $\hat\beta$ hầu như không đổi nhiều — nhưng **SE tăng đều đặn 25–50%** trên mọi biến. Đây chính là hệ quả trực tiếp và định lượng của overdispersion đã nói ở mục 6.2: SE của Poisson bị đánh giá thấp một cách hệ thống.
<br><span class="en">**The key point from the table above**: moving from Poisson to NB, the coefficients $\hat\beta$ barely change — but **SE consistently increases by 25–50%** across every variable. This is the direct, quantitative consequence of the overdispersion discussed in section 6.2: Poisson's SE is systematically underestimated.</span>

### 8.1 Overall significance (NB) - <span class="en">Overall significance (NB)</span>

`1-pchisq(negbin$null.deviance-negbin$deviance, negbin$df.null-negbin$df.residual)` = $7.771561\times10^{-16}$ → bác bỏ mạnh $H_0$ (mọi hệ số góc = 0).
<br><span class="en">`1-pchisq(negbin$null.deviance-negbin$deviance, negbin$df.null-negbin$df.residual)` = $7.771561\times10^{-16}$ → strongly reject $H_0$ (all slope coefficients = 0).</span>

### 8.2 Test for joint significance — kết luận đảo ngược hoàn toàn so với Poisson - <span class="en">Test for joint significance — a conclusion completely reversed from Poisson</span>

Đây là minh họa quan trọng nhất của toàn bộ trang này. Kiểm định lại đúng câu hỏi đã hỏi ở Poisson (mục 5) — nhóm 4 dummy `risk` có cùng ảnh hưởng hay không — nhưng lần này dùng NB:
<br><span class="en">This is the single most important illustration on this entire page. It re-tests exactly the same question asked under Poisson (section 5) — whether the group of 4 `risk` dummies is jointly significant — but this time using NB:</span>

- **LR test** (`lmtest::lrtest(negbin, c("unlikely","neither","likely","verylikely"))`): Model đầy đủ (df=14, logLik=−877.77) so với model bỏ 4 dummy risk (df=10, logLik=−880.71): $\chi^2=5.8759$, $df=4$, $p=0.2086$.
<br><span class="en">**LR test** (`lmtest::lrtest(negbin, c("unlikely","neither","likely","verylikely"))`): the full model (df=14, logLik=−877.77) versus the model dropping the 4 risk dummies (df=10, logLik=−880.71): $\chi^2=5.8759$, $df=4$, $p=0.2086$.</span>
- **Wald test** (`aod::wald.test(..., Terms=10:13)`): $X^2=6.0$, $df=4$, $p=0.2$.
<br><span class="en">**Wald test** (`aod::wald.test(..., Terms=10:13)`): $X^2=6.0$, $df=4$, $p=0.2$.</span>

| Mô hình - <span class="en">Model</span> | Thống kê - <span class="en">Statistic</span> | df | p-value | Kết luận ở $\alpha=5\%$ - <span class="en">Conclusion at $\alpha=5\%$</span> |
|---|---|---|---|---|
| Poisson (Wald) | $X^2=9.6$ | 4 | **0.048** | **Bác bỏ $H_0$** (risk có ý nghĩa)<br><span class="en">**Reject $H_0$** (risk is significant)</span> |
| NB (LR) | $\chi^2=5.8759$ | 4 | **0.2086** | **Không bác bỏ $H_0$** (risk không còn ý nghĩa)<br><span class="en">**Fail to reject $H_0$** (risk is no longer significant)</span> |
| NB (Wald) | $X^2=6.0$ | 4 | **0.2** | **Không bác bỏ $H_0$**<br><span class="en">**Fail to reject $H_0$**</span> |

**Cùng một câu hỏi nghiên cứu, cùng một bộ dữ liệu — hai mô hình cho ra hai kết luận trái ngược nhau ở mức ý nghĩa 5%.** Đây chính xác là hệ quả đã cảnh báo ở mục 6.2: SE của Poisson bị đánh giá thấp do bỏ qua overdispersion, khiến kiểm định Poisson "nhìn thấy" ý nghĩa thống kê không thực sự tồn tại một khi SE được điều chỉnh đúng qua NB.
<br><span class="en">**The same research question, the same dataset — two models produce two opposite conclusions at the 5% significance level.** This is exactly the consequence warned about in section 6.2: Poisson's SE is underestimated because it ignores overdispersion, causing the Poisson test to "see" statistical significance that does not actually exist once the SE is correctly adjusted via NB.</span>

### 8.3 Kiểm định chính thức NB so với Poisson - <span class="en">Formal test of NB versus Poisson</span>

$$H_0: \alpha=0 \text{ (Poisson đủ)} \quad\text{vs.}\quad H_a: \alpha>0 \text{ (cần NB)}$$
<br><span class="en">$$H_0: \alpha=0 \text{ (Poisson is sufficient)} \quad\text{vs.}\quad H_a: \alpha>0 \text{ (NB is needed)}$$</span>

```r
lrtest(poisson, negbin)
```

Model 1 (Poisson, df=13, logLik=−893.57) so với Model 2 (NB, df=14, logLik=−877.77): $\chi^2=31.605$, $df=1$, $p=1.889\times10^{-8}$ *** → bác bỏ mạnh $H_0:\alpha=0$ → **NB phù hợp hơn Poisson một cách có ý nghĩa thống kê rất cao**, xác nhận lại kết luận từ `dispersiontest` (mục 6.2) và từ chính bảng so sánh SE ở mục 8.
<br><span class="en">Model 1 (Poisson, df=13, logLik=−893.57) versus Model 2 (NB, df=14, logLik=−877.77): $\chi^2=31.605$, $df=1$, $p=1.889\times10^{-8}$ *** → strongly reject $H_0:\alpha=0$ → **NB fits better than Poisson with very high statistical significance**, reconfirming the conclusion from `dispersiontest` (section 6.2) and from the SE comparison table in section 8.</span>

## 9. Diễn giải hệ số: từ thang log sang Incidence Rate Ratio (IRR) - <span class="en">Interpreting coefficients: from the log scale to the Incidence Rate Ratio (IRR)</span>

### 9.1 Vì sao không thể đọc trực tiếp $\hat\beta$ - <span class="en">Why $\hat\beta$ cannot be read directly</span>

Vì mô hình dùng hàm liên kết log ($\log\lambda = X\beta$, tương đương $\lambda=e^{X\beta}$), hệ số $\hat\beta_j$ đo **thay đổi trong log của số đếm kỳ vọng**, không phải thay đổi trực tiếp của bản thân số đếm — hoàn toàn tương tự việc hệ số Logit đo log-odds chứ không đo trực tiếp xác suất (xem [[concepts/binary-response-models]]). Để diễn giải bằng đơn vị dễ hiểu, cần lũy thừa hệ số để có **Incidence Rate Ratio (IRR)**:
<br><span class="en">Because the model uses a log link ($\log\lambda = X\beta$, equivalent to $\lambda=e^{X\beta}$), the coefficient $\hat\beta_j$ measures **the change in the log of the expected count**, not a direct change in the count itself — entirely analogous to how a Logit coefficient measures log-odds rather than probability directly (see [[concepts/binary-response-models]]). To interpret it in an easily understandable unit, the coefficient must be exponentiated to get the **Incidence Rate Ratio (IRR)**:</span>

$$IRR_j = e^{\hat\beta_j}$$

**Quy tắc đọc IRR**:
<br><span class="en">**Rule for reading IRR**:</span>

- $IRR_j > 1$: tăng $X_j$ thêm 1 đơn vị làm số đếm kỳ vọng $\lambda$ tăng $(IRR_j-1)\times100\%$, giữ các biến khác không đổi.
<br><span class="en">$IRR_j > 1$: increasing $X_j$ by 1 unit raises the expected count $\lambda$ by $(IRR_j-1)\times100\%$, holding other variables fixed.</span>
- $IRR_j < 1$: tăng $X_j$ thêm 1 đơn vị làm $\lambda$ giảm $(1-IRR_j)\times100\%$.
<br><span class="en">$IRR_j < 1$: increasing $X_j$ by 1 unit lowers $\lambda$ by $(1-IRR_j)\times100\%$.</span>
- $IRR_j = 1$ ($\hat\beta_j=0$): $X_j$ không có ảnh hưởng.
<br><span class="en">$IRR_j = 1$ ($\hat\beta_j=0$): $X_j$ has no effect.</span>

### 9.2 Ví dụ số — IRR từ mô hình NB - <span class="en">Numerical example — IRR from the NB model</span>

| Biến - <span class="en">Variable</span> | $\hat\beta$ (NB) | $IRR=e^{\hat\beta}$ | Diễn giải - <span class="en">Interpretation</span> |
|---|---|---|---|
| `priceUS` | −0.007658 | 0.9924 | Giá vaccine tăng 1 USD → số vaccine kỳ vọng mua **giảm 0.76%**, giữ các biến khác không đổi<br><span class="en">Vaccine price increases by 1 USD → expected number of vaccines purchased **falls by 0.76%**, holding other variables fixed</span> |
| `hhincomeUS` | 0.0001039 | 1.00010 | Thu nhập hộ tăng 1 USD → số vaccine kỳ vọng mua **tăng 0.010%** (≈1.04% nếu thu nhập tăng 100 USD)<br><span class="en">Household income increases by 1 USD → expected number of vaccines purchased **rises by 0.010%** (≈1.04% if income rises by 100 USD)</span> |
| `hhsize` | 0.07759 | 1.0807 | Hộ có thêm 1 thành viên → số vaccine kỳ vọng mua **tăng 8.07%**<br><span class="en">Household gains 1 additional member → expected number of vaccines purchased **rises by 8.07%**</span> |
| `age` | −0.009695 | 0.9904 | Tuổi tăng 1 năm → số vaccine kỳ vọng mua **giảm 0.96%**<br><span class="en">Age increases by 1 year → expected number of vaccines purchased **falls by 0.96%**</span> |
| `verylikely` (so với base "very unlikely")<br><span class="en">`verylikely` (relative to base "very unlikely")</span> | 0.4376 | 1.5490 | Người cho rằng rủi ro nhiễm là "rất có khả năng" mua vaccine kỳ vọng **cao hơn 54.9%** so với người cho rằng "rất không có khả năng" (base), giữ các biến khác không đổi<br><span class="en">A person who perceives the risk of infection as "very likely" has an expected vaccine purchase **54.9% higher** than someone who perceives it as "very unlikely" (base), holding other variables fixed</span> |

Vì `risk` không được slide gán nhãn causal/non-causal một cách tường minh như bộ dữ liệu Forest/Storm ở [[concepts/linear-regression-model]], nên diễn giải trên chỉ dùng ngôn ngữ liên kết ("có liên quan đến", "cao hơn") — **không khẳng định nhân quả** khi nguồn không xác nhận rõ cơ chế nhân quả.
<br><span class="en">Because `risk` is not explicitly labeled causal/non-causal by the slide the way the Forest/Storm dataset is in [[concepts/linear-regression-model]], the interpretation above uses only associational language ("associated with", "higher than") — **no causal claim is made** when the source does not clearly confirm a causal mechanism.</span>

### 9.3 Marginal effects trên thang số đếm (bổ sung IRR, không thay thế) - <span class="en">Marginal effects on the count scale (supplementing IRR, not replacing it)</span>

IRR cho biết **thay đổi tương đối (%)**; muốn biết thay đổi **tuyệt đối** trên chính đơn vị đếm (số vaccine), cần marginal effect như ở mục 3.1, tính bằng `negbinmfx()` — và giống Logit/Probit, phải chọn MEM hay AME:
<br><span class="en">IRR tells us the **relative change (%)**; to know the **absolute** change in the count unit itself (number of vaccines), we need the marginal effect as in section 3.1, computed via `negbinmfx()` — and just as with Logit/Probit, one must choose MEM or AME:</span>

| Biến - <span class="en">Variable</span> | MEM: dF/dx (tại giá trị trung bình) - <span class="en">MEM: dF/dx (at the mean value)</span> | AME: dF/dx (trung bình các hiệu ứng biên) - <span class="en">AME: dF/dx (average of marginal effects)</span> |
|---|---|---|
| `priceUS` | −0.0301 (p=0.00326 **) | −0.0318 (p=0.00506 **) |
| `hhincomeUS` | 0.000409 (p=0.01294 *) | 0.000431 (p=0.01562 *) |
| `hhsize` | 0.3054 (p=6.49e-06 ***) | 0.3220 (p=1.21e-06 ***) |
| `age` | −0.0382 (p=6.57e-06 ***) | −0.0402 (p=1.71e-05 ***) |
| `verylikely` | 2.1355 (p=0.007715 **, thay đổi rời rạc 0→1)<br><span class="en">2.1355 (p=0.007715 **, discrete change 0→1)</span> | 2.2458 (p=0.00782 **) |

Đọc ví dụ `hhsize`: tại quan sát trung bình (MEM), thêm 1 thành viên hộ gia đình làm số vaccine mua kỳ vọng **tăng khoảng 0.305 liều**, giữ các biến khác ở giá trị trung bình mẫu — một con số tuyệt đối, bổ sung cho con số tương đối 8.07% ở mục 9.2 (hai con số này nhất quán về mặt khái niệm: 0.305 chính là gần đúng $\lambda \times (\text{IRR}-1)$ tại $\lambda$ trung bình mẫu ≈4.13, vì $4.13\times0.0807\approx0.333$, xấp xỉ nhưng không trùng khít tuyệt đối do MEM/AME tính theo cách khác công thức đạo hàm giải tích đơn giản).
<br><span class="en">Reading the `hhsize` example: at the average observation (MEM), adding 1 household member makes the expected number of vaccines purchased **rise by about 0.305 doses**, holding other variables at their sample mean — an absolute figure that supplements the relative figure of 8.07% in section 9.2 (the two numbers are conceptually consistent: 0.305 is approximately $\lambda \times (\text{IRR}-1)$ at the sample mean $\lambda$ ≈4.13, since $4.13\times0.0807\approx0.333$ — close but not an exact match because MEM/AME are computed differently from the simple analytic derivative formula).</span>

### 9.4 Một điểm dễ nhầm: `predict(..., type="link")` không phải là số đếm kỳ vọng - <span class="en">An easy point of confusion: `predict(..., type="link")` is not the expected count</span>

Slide minh họa tính "partial effect tại một điểm dữ liệu cụ thể" bằng cách tăng `hhincomeUS` từ 700 lên 701 (giữ các biến khác cố định) và lấy hiệu của hai dự đoán:
<br><span class="en">The slide illustrates computing a "partial effect at a specific data point" by increasing `hhincomeUS` from 700 to 701 (holding other variables fixed) and taking the difference between the two predictions:</span>

```r
nbpred1 = predict(negbin, newdata=point1, type="link")
nbpred2 = predict(negbin, newdata=point2, type="link")
nbpred2 - nbpred1
# = 0.0001038968
```

Con số $0.0001038968$ này **đúng bằng** $\hat\beta_{hhincomeUS}=0.0001039$ (làm tròn) — điều này là hiển nhiên về mặt đại số: `type="link"` trả về $X\beta$ (thang log của $\lambda$), và vì mô hình tuyến tính theo $X$ trên thang log, chênh lệch $X\beta$ khi $X_j$ tăng đúng 1 đơn vị luôn **chính xác bằng** $\hat\beta_j$ — không cần chạy `predict()` để biết trước con số này. Tương tự, ví dụ đổi `risk` từ "likely" sang "very likely" cho hiệu số $\approx0.3374$, xấp xỉ đúng $\hat\beta_{verylikely}-\hat\beta_{likely}=0.4376-0.1003=0.3373$.
<br><span class="en">This figure $0.0001038968$ is **exactly equal to** $\hat\beta_{hhincomeUS}=0.0001039$ (rounded) — this is algebraically obvious: `type="link"` returns $X\beta$ (the log scale of $\lambda$), and because the model is linear in $X$ on the log scale, the difference in $X\beta$ when $X_j$ increases by exactly 1 unit is always **exactly equal to** $\hat\beta_j$ — there is no need to run `predict()` to know this number in advance. Similarly, the example of changing `risk` from "likely" to "very likely" gives a difference $\approx0.3374$, closely matching $\hat\beta_{verylikely}-\hat\beta_{likely}=0.4376-0.1003=0.3373$.</span>

## 10. Zero-Inflated Negative Binomial (ZINB) — bài toán "excess zeros" - <span class="en">Zero-Inflated Negative Binomial (ZINB) — the "excess zeros" problem</span>

### 10.1 Trực giác: khi nào có "quá nhiều số 0"? - <span class="en">Intuition: when are there "too many zeros"?</span>

Ngay từ thống kê mô tả (mục 4.1): 73/377 ≈ **19.4%** hộ gia đình mua **0** vaccine. Nếu Poisson với $\lambda=4.13$ (trung bình mẫu) đúng, xác suất quan sát được $y=0$ chỉ là:
<br><span class="en">Right from the descriptive statistics (section 4.1): 73/377 ≈ **19.4%** of households purchase **0** vaccines. If Poisson with $\lambda=4.13$ (sample mean) held, the probability of observing $y=0$ would only be:</span>

$$Pr(y=0)=\frac{e^{-4.13}(4.13)^0}{0!}=e^{-4.13}\approx0.0161 \;(\approx1.6\%)$$

Tỷ lệ số 0 **thực tế quan sát được (≈19.4%) lớn hơn rất nhiều** so với tỷ lệ Poisson dự đoán (≈1.6%) tại cùng mức trung bình — đây là một minh họa trực quan cho bài toán **excess zeros** (quá nhiều quan sát bằng 0 so với những gì phân phối đếm chuẩn dự đoán). *(Đây là phép tính minh họa tự suy ra từ số liệu mô tả trong slide — bản thân slide không trình bày trực tiếp phép so sánh này, nhưng dùng đúng công thức Poisson mà slide đã cho ở mục 2 và trung bình mẫu ở mục 4.1.)*
<br><span class="en">The **actually observed** zero rate (≈19.4%) is **far larger** than the Poisson-predicted rate (≈1.6%) at the same mean — this is a direct illustration of the **excess zeros** problem (far more zero observations than a standard count distribution predicts). *(This is an illustrative calculation derived from the slide's descriptive data — the slide itself does not present this comparison directly, but it uses exactly the Poisson formula given by the slide in section 2 and the sample mean from section 4.1.)*</span>

**Diễn giải kinh tế học của excess zeros**: có thể tồn tại **hai nhóm tiềm ẩn (latent groups)** trong dân số, mà biến $X$ quan sát được không phân biệt được hoàn toàn:
<br><span class="en">**Economic interpretation of excess zeros**: there may exist **two latent groups** in the population that the observed $X$ variables cannot fully distinguish:</span>

1. **Nhóm "không bao giờ" (always-zero / structural zero)**: những hộ về bản chất sẽ *luôn* mua 0 vaccine — ví dụ đã hoàn toàn không tin vào vaccine, hoặc đã có đủ vaccine từ nguồn khác. Với nhóm này, $y=0$ không phải vì "may mắn không cần mua" mà vì họ **không bao giờ nằm trong thị trường** này.
<br><span class="en">The "never" group (always-zero / structural zero): households that will *always* purchase 0 vaccines by nature — e.g. they completely distrust vaccines, or already have enough vaccine from another source. For this group, $y=0$ is not because they "happened not to need to buy" but because they **are never in this market** at all.</span>
2. **Nhóm "có khả năng mua" (count process / at-risk group)**: những hộ *có thể* mua vaccine (số lượng tuân theo một quá trình đếm, VD NB), nhưng vẫn có thể tình cờ mua đúng 0 liều trong lần khảo sát này (VD do giá cao, thu nhập thấp thời điểm đó…) mà không phải vì họ "không bao giờ mua".
<br><span class="en">The "potential buyer" group (count process / at-risk group): households that *could* purchase vaccine (the quantity follows a count process, e.g. NB), but may happen to purchase exactly 0 doses at this particular survey moment (e.g. because of a high price, low income at that time…) without it meaning they "never buy".</span>

Slide gốc gọi đây là trường hợp có **"too many zeros, or two separate processes"**.
<br><span class="en">The original slide calls this a case of **"too many zeros, or two separate processes"**.</span>

### 10.2 Cấu trúc hai phần (two-part structure) - <span class="en">Two-part structure</span>

$$\lambda_i^{zinf} = \pi_i\times\{y_i=0\} + (1-\pi_i)\times\lambda_i$$

trong đó:
<br><span class="en">where:</span>

- $\pi_i$: xác suất $y_i$ là "số 0 cấu trúc" (structural zero), mô hình hóa bằng **logit**: $\pi_i=\dfrac{1}{1+e^{-\gamma Z}}$.
<br><span class="en">$\pi_i$: the probability that $y_i$ is a "structural zero", modeled using **logit**: $\pi_i=\dfrac{1}{1+e^{-\gamma Z}}$.</span>
- $\lambda_i=e^{\beta X}$: kỳ vọng đến từ **quá trình đếm** (count process — mô hình NB).
<br><span class="en">$\lambda_i=e^{\beta X}$: the expectation coming from the **count process** (count process — the NB model).</span>

**Điểm mấu chốt**: trong ZINB, xác suất quan sát $y=0$ đến từ **hai nguồn** cộng lại:
<br><span class="en">**Key point**: in ZINB, the probability of observing $y=0$ comes from **two sources** added together:</span>

1. Nhóm "luôn luôn 0" — xác suất $\pi_i$.
<br><span class="en">The "always zero" group — probability $\pi_i$.</span>
2. Nhóm thuộc quá trình đếm nhưng tình cờ ra kết quả 0 — xác suất $(1-\pi_i)\times Pr_{NB}(y=0)$.
<br><span class="en">The group belonging to the count process but happening to yield a 0 outcome — probability $(1-\pi_i)\times Pr_{NB}(y=0)$.</span>

Mô hình ước lượng đồng thời ba bộ tham số: $\beta$ (phương trình đếm), $\gamma$ (phương trình zero-inflation), và $\alpha$ (hay $\theta=1/\alpha$, tham số phân tán của phần NB).
<br><span class="en">The model simultaneously estimates three sets of parameters: $\beta$ (the count equation), $\gamma$ (the zero-inflation equation), and $\alpha$ (or $\theta=1/\alpha$, the dispersion parameter of the NB part).</span>

**ZINB có hai phương trình đồng thời**:
<br><span class="en">**ZINB has two simultaneous equations**:</span>

$$\pi_i = \frac{1}{1+e^{-\gamma Z}} \qquad \lambda_i = e^{\beta X}$$

## 11. Ước lượng ZINB trên dữ liệu vaccine - <span class="en">Estimating ZINB on the vaccine data</span>

```r
library(pscl)
zinb = zeroinfl(dhh ~ efficacy80+duration3+priceUS+pbenefit+hhincomeUS+hhsize+age+male
                 | hhsize+age+male, data=data, dist="negbin")
```

**Count model coefficients (NB với log link)**:
<br><span class="en">**Count model coefficients (NB with log link)**:</span>

| Biến - <span class="en">Variable</span> | $\hat\beta$ | SE | p-value |
|---|---|---|---|
| (Intercept) | 1.234 | 0.1112 | <2e-16 *** |
| `efficacy80` | 0.03932 | 0.05282 | 0.4566 |
| `duration3` | 0.02925 | 0.05294 | 0.5806 |
| `priceUS` | −0.0007768 | 0.002039 | 0.7033 |
| `pbenefit` | 0.01382 | 0.05219 | 0.7911 |
| `hhincomeUS` | 0.00003168 | 0.00003750 | 0.3982 |
| `hhsize` | 0.09846 | 0.01958 | 4.94e-07 *** |
| `age` | −0.003792 | 0.002083 | 0.0687 . |
| `male` | 0.002423 | 0.06371 | 0.9697 |

**Zero-inflation model coefficients (binomial, logit link)**:
<br><span class="en">**Zero-inflation model coefficients (binomial, logit link)**:</span>

| Biến - <span class="en">Variable</span> | $\hat\gamma$ | SE | p-value |
|---|---|---|---|
| (Intercept) | −3.39078 | 0.57675 | 4.13e-09 *** |
| `hhsize` | 0.04892 | 0.05009 | 0.32881 |
| `age` | 0.03318 | 0.01034 | 0.00134 ** |
| `male` | 0.45359 | 0.28784 | 0.11507 |

$\theta = 8{,}841{,}154.89$ (log-likelihood = −747.4, df=14).
<br><span class="en">$\theta = 8{,}841{,}154.89$ (log-likelihood = −747.4, df=14).</span>

### 11.1 Diễn giải phần zero-inflation - <span class="en">Interpreting the zero-inflation part</span>

Vì $\pi_i$ dùng hàm liên kết logit, hệ số $\hat\gamma_j$ có ý nghĩa **hệt như hệ số Logit** ([[concepts/binary-response-models]]): chỉ cho biết **chiều** ảnh hưởng lên log-odds của việc thuộc nhóm "luôn luôn 0", **không cho biết trực tiếp độ lớn** — muốn có độ lớn phải tính marginal effect hoặc odds ratio $e^{\hat\gamma}$, tương tự IRR nhưng áp cho xác suất thay vì số đếm.
<br><span class="en">Because $\pi_i$ uses a logit link, the coefficient $\hat\gamma_j$ has the same meaning **exactly as a Logit coefficient** ([[concepts/binary-response-models]]): it only tells us the **direction** of the effect on the log-odds of belonging to the "always zero" group, **not directly the magnitude** — to get the magnitude one must compute a marginal effect or the odds ratio $e^{\hat\gamma}$, analogous to IRR but applied to a probability rather than a count.</span>

Trong kết quả trên, chỉ có `age` có ý nghĩa thống kê ($\hat\gamma=0.03318$, $p=0.00134$): tuổi càng cao, log-odds thuộc nhóm "không bao giờ mua vaccine cho hộ" càng cao — tức người trả lời lớn tuổi hơn có xu hướng thuộc nhóm "structural zero" nhiều hơn, giữ `hhsize` và `male` không đổi. `hhsize` và `male` không có ý nghĩa thống kê ở phần zero-inflation này.
<br><span class="en">In the results above, only `age` is statistically significant ($\hat\gamma=0.03318$, $p=0.00134$): the higher the age, the higher the log-odds of belonging to the "never buys vaccine for the household" group — i.e. older respondents tend more toward the "structural zero" group, holding `hhsize` and `male` fixed. `hhsize` and `male` are not statistically significant in this zero-inflation part.</span>

### 11.2 Một quan sát thú vị: $\theta$ cực lớn nghĩa là gì? - <span class="en">An interesting observation: what does an extremely large $\theta$ mean?</span>

So sánh hai giá trị $\theta$ (và $\alpha=1/\theta$) giữa NB thường (mục 8) và ZINB:
<br><span class="en">Comparing the two $\theta$ values (and $\alpha=1/\theta$) between the plain NB (section 8) and ZINB:</span>

| Mô hình - <span class="en">Model</span> | $\theta$ | $\alpha=1/\theta$ |
|---|---|---|
| NB (mục 8, không tách zero-inflation)<br><span class="en">NB (section 8, without separating zero-inflation)</span> | 6.6807 | 0.1497 |
| ZINB — phần đếm<br><span class="en">ZINB — count part</span> | 8,841,154.89 | ≈0.0000001 (≈0) |

$\alpha\approx0$ trong ZINB tương đương gần như **Poisson thuần túy** ở phần đếm (nhắc lại mục 7.3: $\alpha=0\Leftrightarrow$ NB thu gọn về Poisson). Diễn giải trực quan: khi mô hình NB thường (mục 8) phải "gánh" toàn bộ overdispersion — bao gồm cả phần overdispersion sinh ra bởi excess zeros — vào một tham số $\alpha$ duy nhất, $\alpha$ ước lượng được khá lớn (0.1497). Nhưng khi tách riêng phần "luôn luôn 0" ra thành một phương trình logit độc lập (ZINB), phần overdispersion còn lại trong quá trình đếm gần như biến mất ($\alpha\to0$). Điều này gợi ý: phần lớn overdispersion phát hiện được ở mục 6–8 trong ví dụ này **có thể chủ yếu đến từ excess zeros**, chứ không phải từ dị biệt cá nhân lan tỏa đều trên mọi mức đếm. Đây là một quan sát tự suy ra từ hai bảng số của slide (không phải kết luận slide tự phát biểu trực tiếp), nên trình bày như một cách đọc số liệu, không phải một khẳng định của giảng viên.
<br><span class="en">$\alpha\approx0$ in ZINB is nearly equivalent to **pure Poisson** in the count part (recall section 7.3: $\alpha=0\Leftrightarrow$ NB collapses to Poisson). Intuitive interpretation: when the plain NB model (section 8) has to "carry" all the overdispersion — including the portion generated by excess zeros — into a single parameter $\alpha$, the estimated $\alpha$ turns out fairly large (0.1497). But once the "always zero" part is separated out into its own logit equation (ZINB), the remaining overdispersion in the count process nearly vanishes ($\alpha\to0$). This suggests that most of the overdispersion detected in sections 6–8 in this example **may come mainly from excess zeros**, rather than from individual heterogeneity spread evenly across all count levels. This is an observation derived from the slide's two numerical tables (not a conclusion the slide states directly), so it is presented as one way of reading the data, not a claim made by the instructor.</span>

> Lưu ý: slide không trình bày kiểm định hình thức nào (VD Vuong test) để so sánh trực tiếp NB và ZINB có thực sự khác biệt có ý nghĩa thống kê hay không — quan sát ở mục 11.2 chỉ mang tính minh họa định tính, không thay thế cho một kiểm định chính thức.
> <br><span class="en">Note: the slide does not present any formal test (e.g. a Vuong test) to directly compare whether NB and ZINB actually differ with statistical significance — the observation in section 11.2 is only a qualitative illustration, not a substitute for a formal test.</span>

## 12. Bẫy thi tổng hợp (exam traps) - <span class="en">Comprehensive exam traps</span>

1. **Dùng Poisson mà không kiểm tra overdispersion trước.** Nếu có overdispersion, SE của Poisson bị đánh giá thấp (underestimate) một cách hệ thống, dẫn đến kết luận sai về ý nghĩa thống kê — ví dụ số cụ thể ở mục 8.2: cùng kiểm định joint significance của nhóm `risk`, Poisson cho $p=0.048$ (bác bỏ $H_0$) trong khi NB cho $p\approx0.2$ (không bác bỏ) — **kết luận đảo ngược hoàn toàn** chỉ vì chuyển từ Poisson sang NB.
<br><span class="en">**Using Poisson without first checking for overdispersion.** If overdispersion is present, Poisson's SE is systematically underestimated, leading to wrong conclusions about statistical significance — the concrete numerical example in section 8.2: the same joint significance test of the `risk` group, Poisson gives $p=0.048$ (reject $H_0$) while NB gives $p\approx0.2$ (fail to reject) — **a completely reversed conclusion** simply from switching from Poisson to NB.</span>
2. **Diễn giải trực tiếp $\hat\beta$ như đơn vị thay đổi của $y$** — sai, vì mô hình dùng hàm liên kết log; phải lũy thừa để có IRR ($e^{\hat\beta}$) mới diễn giải được bằng % thay đổi của số đếm kỳ vọng (mục 9.1–9.2).
<br><span class="en">**Interpreting $\hat\beta$ directly as the unit change of $y$** — wrong, because the model uses a log link; the coefficient must be exponentiated to get IRR ($e^{\hat\beta}$) before it can be interpreted as a % change in the expected count (sections 9.1–9.2).</span>
3. **Nhầm ZINB với NB thông thường** khi dữ liệu chỉ đơn giản có nhiều số 0 do bản chất phân phối đếm (VD $\lambda$ nhỏ tự nhiên sinh nhiều số 0), chứ không có bằng chứng về một "quá trình cấu trúc" riêng biệt (structural zero process) sinh ra zero.
<br><span class="en">**Confusing ZINB with plain NB** when the data simply has many zeros due to the nature of the count distribution (e.g. a small $\lambda$ naturally generates many zeros), without evidence of a separate "structural" process (structural zero process) generating the zeros.</span>
4. **Quên rằng marginal effect của count models (giống Logit/Probit) không hằng số** — luôn phụ thuộc vào giá trị $X$ đang xét (vì tỷ lệ với $\lambda$) — phải nói rõ đang báo cáo MEM hay AME.
<br><span class="en">**Forgetting that the marginal effect of count models (like Logit/Probit) is not constant** — it always depends on the $X$ value being considered (because it is proportional to $\lambda$) — one must state clearly whether MEM or AME is being reported.</span>
5. **Nhầm lẫn `predict(..., type="link")` với `predict(..., type="response")`.** `type="link"` trả về $X\beta$ (log của số đếm kỳ vọng), chênh lệch giữa hai điểm dự đoán trên thang này chỉ đơn giản bằng chênh lệch hệ số × chênh lệch $X$ — **không phải** là tác động thực tế lên số đếm kỳ vọng $\lambda$ (mục 9.4).
<br><span class="en">**Confusing `predict(..., type="link")` with `predict(..., type="response")`.** `type="link"` returns $X\beta$ (the log of the expected count); the difference between two predictions on this scale is simply the coefficient difference × the $X$ difference — **not** the actual impact on the expected count $\lambda$ (section 9.4).</span>
6. **Diễn giải hệ số $\hat\gamma$ ở phần zero-inflation (logit) giống hệ số $\hat\beta$ ở phần đếm (log-count).** Hai phần có ý nghĩa hoàn toàn khác nhau: $\hat\gamma$ nói về log-odds của việc thuộc nhóm "luôn luôn 0"; $\hat\beta$ nói về log của số đếm kỳ vọng trong nhóm "có khả năng đếm được". Không được gộp chung diễn giải (mục 11.1).
<br><span class="en">**Interpreting the coefficient $\hat\gamma$ in the zero-inflation part (logit) the same way as the coefficient $\hat\beta$ in the count part (log-count).** The two parts have entirely different meanings: $\hat\gamma$ speaks to the log-odds of belonging to the "always zero" group; $\hat\beta$ speaks to the log of the expected count within the "at-risk" group. They must not be interpreted interchangeably (section 11.1).</span>
7. **So sánh trực tiếp log-likelihood/AIC giữa hai mô hình dùng tập biến độc lập khác nhau** — như trong ví dụ slide, ZINB bỏ biến `risk` khỏi phần đếm so với NB thường (mục 11) — so sánh như vậy không "apples-to-apples", vì chênh lệch fit có thể đến từ khác biệt tập biến, không hẳn từ cấu trúc mô hình.
<br><span class="en">**Directly comparing log-likelihood/AIC between two models that use different sets of independent variables** — as in the slide's example, ZINB drops the `risk` variable from the count part relative to the plain NB (section 11) — such a comparison is not "apples-to-apples", because the fit difference could come from the different variable sets, not necessarily from the model structure.</span>
8. **Coi "NB fit tốt hơn Poisson có ý nghĩa thống kê" (mục 8.3) là bằng chứng dứt khoát cho một cơ chế kinh tế cụ thể** (VD "chắc chắn do dị biệt cá nhân") — kiểm định $H_0:\alpha=0$ chỉ nói overdispersion tồn tại về mặt thống kê, không tự động xác định **nguyên nhân** overdispersion (dị biệt cá nhân thuần túy hay excess zeros hay cả hai) — muốn phân biệt, cần thử thêm ZINB như ở mục 10–11.
<br><span class="en">**Treating "NB fits significantly better than Poisson" (section 8.3) as conclusive evidence for a specific economic mechanism** (e.g. "definitely due to individual heterogeneity") — the test $H_0:\alpha=0$ only tells us overdispersion exists statistically, it does not automatically identify the **cause** of the overdispersion (pure individual heterogeneity, excess zeros, or both) — distinguishing between them requires trying ZINB as in sections 10–11.</span>

## 13. Kết nối với phần còn lại của khóa học - <span class="en">Connections with the rest of the course</span>

Count data models dùng chung khung Maximum Likelihood với toàn bộ **Part 2: Models for Limited Dependent Variables**, mở đầu ở [[concepts/binary-response-models]] (Topic 7):
<br><span class="en">Count data models share the same Maximum Likelihood framework with the whole of **Part 2: Models for Limited Dependent Variables**, opened at [[concepts/binary-response-models]] (Topic 7):</span>

- **Cùng logic hàm liên kết phi tuyến** để giữ đại lượng dự đoán trong miền hợp lệ: Logit/Probit giữ xác suất trong $[0,1]$; Poisson/NB giữ $\lambda$ dương.
<br><span class="en">**The same nonlinear link-function logic** to keep the predicted quantity within its valid domain: Logit/Probit keep probability within $[0,1]$; Poisson/NB keep $\lambda$ positive.</span>
- **Cùng cấu trúc diễn giải hệ số hai bước**: hệ số thô chỉ cho *chiều*, phải biến đổi (odds ratio ở Logit, IRR ở Poisson/NB) mới có *độ lớn* diễn giải được trực tiếp.
<br><span class="en">**The same two-step coefficient-interpretation structure**: the raw coefficient only gives the *direction*; it must be transformed (odds ratio in Logit, IRR in Poisson/NB) before the *magnitude* becomes directly interpretable.</span>
- **Cùng vấn đề marginal effect không hằng số**, cùng lựa chọn MEM vs AME.
<br><span class="en">**The same issue of a non-constant marginal effect**, and the same choice between MEM vs AME.</span>
- **Cùng bộ dữ liệu khảo sát vaccine COVID-19**, chỉ đổi biến phụ thuộc (`dself` nhị phân ở Topic 7 → `dhh` đếm ở Topic 10) — minh họa nguyên tắc chọn mô hình theo bản chất biến phụ thuộc.
<br><span class="en">**The same COVID-19 vaccine survey dataset**, only the dependent variable changes (`dself` binary in Topic 7 → `dhh` count in Topic 10) — illustrating the principle of choosing a model according to the nature of the dependent variable.</span>

Khái niệm **nesting** (NB lồng Poisson tại $\alpha=0$, mục 7.3) và kiểm định LR dựa trên so sánh log-likelihood giữa mô hình đầy đủ/rút gọn (mục 8.3, 8.1) tái sử dụng đúng logic Likelihood Ratio test đã xây dựng ở [[concepts/binary-response-models]] — chỉ khác đối tượng kiểm định (một tham số phân tán $\alpha$ thay vì một tập hệ số $\beta$).
<br><span class="en">The concept of **nesting** (NB nests Poisson at $\alpha=0$, section 7.3) and the LR test based on comparing log-likelihood between the full/restricted model (sections 8.3, 8.1) reuse exactly the Likelihood Ratio test logic already built in [[concepts/binary-response-models]] — only the object being tested differs (a dispersion parameter $\alpha$ instead of a set of coefficients $\beta$).</span>

## 11. Tài liệu tham khảo ứng dụng thực tế - <span class="en">Real-world application references</span>

Ba bài báo gần đây minh họa count data models (Poisson, Negative Binomial) trong nghiên cứu kinh tế thực tế (đề cương Lecture 12):
<br><span class="en">Three recent papers illustrating count data models (Poisson, Negative Binomial) in real-world economic research (Lecture 12 syllabus):</span>

- Meredith, N. R., Macy, A., & Meredith, A. (2022). Income elasticity of demand for tanning bed usage: evidence from survey data. *Journal of Applied Economics*, 25(1), 1156-1181. https://doi.org/10.1080/15140326.2022.2110640
- Hynes, S., O'Reilly, P., & Corless, R. (2015). An on-site versus a household survey approach to modelling the demand for recreational angling: Do welfare estimates differ? *Ecosystem Services*, 16, 136-145. https://doi.org/10.1016/j.ecoser.2015.10.013
- Xu, M., Ye, Q., Wang, X., & Wang, M. (2017). Assessing influence of online reputation on sales using a zero-inflated negative binomial model. *Procedia Computer Science*, 122, 1108-1113. https://doi.org/10.1016/j.procs.2017.11.480
