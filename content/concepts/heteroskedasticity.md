---
title: "Lecture 4: Heteroskedasticity"
type: concept
status: mature
tags: [heteroskedasticity, robust-standard-errors, linear-regression, model-diagnostics]
sources: ["[[sources/slides-4-heteroskedasticity]]"]
related: ["[[concepts/linear-regression-model]]", "[[concepts/multicollinearity]]"]
lecture: 4
assignment: ["Assignment 3: Heteroskedasticity"]
updated: 2026-09-04
---

> **Cách đọc trang này**: đây là trang vá lỗi cho **giả định A4 (Homoskedasticity)** của OLS — nếu chưa nắm rõ A4 là gì và vì sao nó quan trọng, đọc mục 4 và mục 6 của [[concepts/linear-regression-model]] trước.
> <br><span class="en">**How to read this page**: this is the patch page for OLS's **A4 assumption (Homoskedasticity)** — if you're not yet clear on what A4 is and why it matters, read sections 4 and 6 of [[concepts/linear-regression-model]] first.</span>
> Điểm mấu chốt cần giữ trong đầu xuyên suốt trang này: heteroskedasticity **không** làm hệ số hồi quy sai đi — nó làm cho **thước đo độ bất định của hệ số đó** (SE, và do đó t-test, F-test, p-value, confidence interval) trở nên không đáng tin.
> <br><span class="en">The key point to keep in mind throughout this page: heteroskedasticity does **not** make the regression coefficient wrong — it makes **the measure of uncertainty around that coefficient** (SE, and hence the t-test, F-test, p-value, confidence interval) unreliable.</span>
> Đây là bài toán về **suy luận thống kê (inference)**, không phải bài toán về **độ chính xác của ước lượng (estimation)**.
> <br><span class="en">This is a problem of **statistical inference**, not a problem of **estimation accuracy**.</span>

**Lecture 4** trong đề cương (CO Topic 4) — Assignment 3: Heteroskedasticity.
<br><span class="en">**Lecture 4** in the syllabus (CO Topic 4) — Assignment 3: Heteroskedasticity.</span>

## 1. Trực giác trước — heteroskedasticity là gì - <span class="en">Intuition first — what is heteroskedasticity</span>

Hình dung một mô hình dự đoán **chi tiêu hộ gia đình** (`expense`) dựa vào **thu nhập** (`income`).
<br><span class="en">Imagine a model predicting **household expenditure** (`expense`) based on **income** (`income`).</span>
Với các hộ thu nhập thấp, lựa chọn chi tiêu của họ khá bị giới hạn — phần lớn thu nhập phải dành cho nhu cầu thiết yếu, nên chi tiêu thực tế của các hộ này thường **sát** với mức dự đoán từ mô hình, sai số nhỏ.
<br><span class="en">For low-income households, their spending choices are fairly constrained — most of their income must go toward essential needs, so these households' actual expenditure tends to sit **close** to the model's predicted level, with small errors.</span>
Ngược lại, với các hộ thu nhập cao, không gian lựa chọn rộng hơn nhiều: có hộ tiết kiệm phần lớn thu nhập, có hộ chi tiêu xa hoa vượt xa mức "trung bình" mà mô hình dự đoán — sai số dự đoán ở nhóm này **dao động rộng hơn hẳn**.
<br><span class="en">In contrast, for high-income households, the range of choices is much wider: some households save most of their income, others spend lavishly, far beyond the "average" level the model predicts — the prediction errors for this group **fluctuate much more widely**.</span>

Nói cách khác: **độ lớn của sai số dự đoán (phần dư) không đồng đều qua các quan sát** — nó có xu hướng "phình to" khi một biến nào đó (ở đây là thu nhập, hoặc giá trị dự đoán $\hat y$) tăng lên.
<br><span class="en">In other words: **the magnitude of the prediction error (residual) is not uniform across observations** — it tends to "balloon" as some variable (here, income, or the predicted value $\hat y$) increases.</span>
Đây chính là **heteroskedasticity** ("hetero" = khác nhau, "skedasticity" = độ phân tán).
<br><span class="en">This is exactly **heteroskedasticity** ("hetero" = different, "skedasticity" = dispersion).</span>
Ngược lại, nếu độ lớn sai số dự đoán đồng đều bất kể quan sát nào — không hộ nào có xu hướng bị dự đoán "lệch xa" nhiều hơn hộ khác một cách hệ thống — đó là **homoskedasticity**, giả định A4 của OLS (xem [[concepts/linear-regression-model]] mục 4).
<br><span class="en">Conversely, if the magnitude of the prediction error is uniform regardless of the observation — no household is systematically predicted "further off" than another — that is **homoskedasticity**, OLS's A4 assumption (see [[concepts/linear-regression-model]] section 4).</span>

Ví dụ số cụ thể minh họa đúng hiện tượng này nằm ở mục 4–5 bên dưới — dùng chính bộ dữ liệu chi tiêu hộ gia đình mà slide gốc dùng xuyên suốt.
<br><span class="en">A concrete numerical example illustrating exactly this phenomenon appears in sections 4–5 below — using the very same household expenditure dataset that the original slides use throughout.</span>

## 2. Định nghĩa hình thức - <span class="en">Formal definition</span>

Giả định **A4 (Homoskedasticity)** của CLRM (Classical Linear Regression Model) phát biểu rằng phương sai sai số là **hằng số**, không đổi qua các quan sát:
<br><span class="en">The **A4 (Homoskedasticity)** assumption of the CLRM (Classical Linear Regression Model) states that the error variance is **constant**, unchanging across observations:</span>

$$Var(\varepsilon_i) = \sigma^2 \quad \text{với mọi } i, \qquad \text{tương đương } Var(\varepsilon|X) = \sigma^2 I$$

trong đó $I$ là ma trận đơn vị $n\times n$ — nghĩa là không chỉ phương sai bằng nhau ở mọi quan sát, mà sai số ở quan sát này còn không tương quan với sai số ở quan sát khác (các phần tử ngoài đường chéo của ma trận VCV sai số bằng 0).
<br><span class="en">where $I$ is the $n\times n$ identity matrix — meaning not only that the variance is equal across all observations, but also that the error at one observation is uncorrelated with the error at another observation (the off-diagonal elements of the error VCV matrix are zero).</span>

**Heteroskedasticity** là khi giả định này **bị vi phạm**:
<br><span class="en">**Heteroskedasticity** is when this assumption is **violated**:</span>

$$Var(\varepsilon_i) \neq \sigma^2 \quad \text{(phương sai sai số thay đổi theo } i\text{)}, \qquad \text{tức } Var(\varepsilon|X) \neq \sigma^2 I$$

VCV và SE "chuẩn" mà OLS báo cáo mặc định (kể cả trong `summary(lm(...))` của R) được tính **dựa trên giả định A4 đúng** — đây là lý do vi phạm A4 làm những con số đó trở nên đáng ngờ (xem mục 6).
<br><span class="en">The "standard" VCV and SE that OLS reports by default (including in R's `summary(lm(...))`) are computed **assuming A4 holds** — this is why violating A4 makes those numbers suspect (see section 6).</span>

## 3. Nguồn gốc của heteroskedasticity - <span class="en">Sources of heteroskedasticity</span>

Slide liệt kê ba nguồn gốc phổ biến, không loại trừ lẫn nhau:
<br><span class="en">The slides list three common sources, not mutually exclusive:</span>

1. **Outlier trong dữ liệu**: một vài quan sát cực đoan có thể kéo phương sai sai số lên cao bất thường tại vùng dữ liệu chứa outlier đó.
<br><span class="en">**Outliers in the data**: a few extreme observations can pull the error variance up abnormally high in the region of the data containing that outlier.</span>
2. **Sai functional form (dạng hàm hồi quy sai)**: ví dụ mô hình thật sự là phi tuyến (log, quadratic…) nhưng lại được ước lượng như tuyến tính — phần "phi tuyến bị bỏ sót" này có thể biểu hiện ra dưới dạng phương sai sai số không đồng đều. (Xem thêm [[concepts/functional-forms]].)
<br><span class="en">**Wrong functional form**: for example the true model is nonlinear (log, quadratic…) but is estimated as linear — this "omitted nonlinearity" can manifest as non-uniform error variance. (See also [[concepts/functional-forms]].)</span>
3. **Trộn lẫn các nhóm quan sát khác nhau** — ví dụ trộn hộ thu nhập cao và hộ thu nhập thấp trong cùng một mẫu (đúng như ví dụ trực giác ở mục 1): mỗi nhóm có thể có "độ ồn" (noise) khác nhau về bản chất, và khi gộp chung, phương sai sai số tổng thể không còn đồng đều.
<br><span class="en">**Mixing different groups of observations** — for example mixing high-income and low-income households in the same sample (exactly as in the intuition example in section 1): each group may inherently have a different "noise" level, and once pooled together, the overall error variance is no longer uniform.</span>

## 4. Ví dụ xuyên suốt: khảo sát chi tiêu hộ gia đình TP.HCM 2020 - <span class="en">Running example: 2020 Ho Chi Minh City household expenditure survey</span>

Slide dùng bộ dữ liệu khảo sát các cặp vợ chồng tại TP.HCM năm 2020 (`https://econometrics.site/public/mcl.csv`) — **cùng bộ dữ liệu** dùng ở [[concepts/multicollinearity]], nhưng phục vụ hai mục đích chẩn đoán khác nhau (xem mục "Kết nối" cuối trang).
<br><span class="en">The slides use a dataset surveying married couples in Ho Chi Minh City in 2020 (`https://econometrics.site/public/mcl.csv`) — **the same dataset** used in [[concepts/multicollinearity]], but serving two different diagnostic purposes (see the "Connections" section at the end of the page).</span>

| Biến<br><span class="en">Variable</span> | Ý nghĩa<br><span class="en">Meaning</span> | Đơn vị<br><span class="en">Unit</span> |
|---|---|---|
| `expense` | Chi tiêu hộ gia đình — **biến phụ thuộc**<br><span class="en">Household expenditure — **dependent variable**</span> | triệu VNĐ/tháng<br><span class="en">million VND/month</span> |
| `income` | Thu nhập hộ gia đình<br><span class="en">Household income</span> | triệu VNĐ/tháng<br><span class="en">million VND/month</span> |
| `age_wife` | Tuổi vợ<br><span class="en">Wife's age</span> | năm<br><span class="en">years</span> |
| `age_husband` | Tuổi chồng<br><span class="en">Husband's age</span> | năm<br><span class="en">years</span> |
| `hhsize` | Quy mô hộ (số thành viên)<br><span class="en">Household size (number of members)</span> | người<br><span class="en">persons</span> |
| `children` | % trẻ em trong hộ<br><span class="en">% of children in household</span> | % |

Sau khi loại bỏ quan sát thiếu dữ liệu (NA) và các hộ có `income = 0`, mẫu còn lại $n=470$.
<br><span class="en">After removing observations with missing data (NA) and households with `income = 0`, the remaining sample is $n=470$.</span>

**Thống kê mô tả** (để cảm nhận thang đo trước khi đọc hệ số):
<br><span class="en">**Descriptive statistics** (to get a feel for scale before reading the coefficients):</span>

| Biến<br><span class="en">Variable</span> | n | mean | sd | median | min | max |
|---|---|---|---|---|---|---|
| `expense` | 470 | 12.02 | 11.16 | 10.0 | 1.0 | 180.00 |
| `income` | 470 | 17.03 | 17.00 | 12.5 | 0.4 | 180.00 |
| `age_wife` | 470 | 44.91 | 10.86 | 45.0 | 22.0 | 86.00 |
| `age_husband` | 470 | 48.36 | 10.73 | 49.0 | 26.0 | 84.81 |
| `hhsize` | 470 | 4.72 | 2.32 | 4.0 | 1.0 | 25.00 |
| `children` | 470 | 7.88 | 13.06 | 0.0 | 0.0 | 60.00 |

Chú ý ngay từ bảng mô tả: `expense` có độ lệch chuẩn (sd = 11.16) gần bằng trung bình (mean = 12.02), và max (180) cách rất xa median (10) — dấu hiệu sớm cho thấy phân phối chi tiêu bị lệch phải mạnh (right-skewed), điều này thường đi kèm với heteroskedasticity khi hồi quy tuyến tính.
<br><span class="en">Notice right away from the descriptive table: `expense` has a standard deviation (sd = 11.16) close to its mean (mean = 12.02), and the max (180) is very far from the median (10) — an early sign that the expenditure distribution is strongly right-skewed, which often comes together with heteroskedasticity in linear regression.</span>

**Kết quả hồi quy OLS đầy đủ** (`expense ~ income + age_wife + age_husband + hhsize + children`) — bảng số này được dùng lại xuyên suốt các mục BP test, robust SE, Wald F-test bên dưới:
<br><span class="en">**Full OLS regression results** (`expense ~ income + age_wife + age_husband + hhsize + children`) — this table of numbers is reused throughout the BP test, robust SE, and Wald F-test sections below:</span>

| Biến<br><span class="en">Variable</span> | Estimate | Std. Error (thường)<br><span class="en">Std. Error (usual)</span> | t value | Pr(>\|t\|) |
|---|---|---|---|---|
| (Intercept) | 0.13924 | 2.22451 | 0.063 | 0.950 |
| `income` | 0.42851 | 0.02368 | 18.094 | < 2e-16 *** |
| `age_wife` | 0.11018 | 0.09317 | 1.183 | 0.238 |
| `age_husband` | −0.08587 | 0.09351 | −0.918 | 0.359 |
| `hhsize` | 0.69243 | 0.16934 | 4.089 | 5.11e-05 *** |
| `children` | 0.06613 | 0.03092 | 2.139 | 0.033 * |

Residual SE = 8.394 trên 464 df; $R^2=0.4399$, Adjusted $R^2=0.4338$; F-statistic = 72.88 trên 5 và 464 df, p-value < 2.2e-16.
<br><span class="en">Residual SE = 8.394 on 464 df; $R^2=0.4399$, Adjusted $R^2=0.4338$; F-statistic = 72.88 on 5 and 464 df, p-value < 2.2e-16.</span>

Đọc nhanh: `income` và `hhsize` có ảnh hưởng rất rõ ràng lên chi tiêu (p rất nhỏ); `children` có ý nghĩa thống kê ở mức 5% (nhưng — xem mục 9 — điều này **sẽ thay đổi** khi dùng robust SE); `age_wife`, `age_husband` không có ý nghĩa thống kê.
<br><span class="en">Quick read: `income` and `hhsize` have a very clear effect on expenditure (very small p); `children` is statistically significant at the 5% level (but — see section 9 — this **will change** once robust SE is used); `age_wife` and `age_husband` are not statistically significant.</span>
Đây là bảng kết quả "thường" — nghĩa là dùng SE tính dưới giả định A4.
<br><span class="en">This is the "usual" results table — meaning it uses SE computed under the A4 assumption.</span>
Câu hỏi đặt ra: giả định A4 có thật sự đúng ở đây không?
<br><span class="en">The question that arises: does the A4 assumption actually hold here?</span>

## 5. Phát hiện bằng đồ thị (trực quan, trước khi kiểm định chính thức) - <span class="en">Graphical detection (visual, before formal testing)</span>

Slide minh họa hai đồ thị phần dư (residual) từ chính mô hình trên:
<br><span class="en">The slides illustrate two residual plots from the model above:</span>

- **Density plot của phần dư** (`plot(density(data$u))`): phân phối phần dư có đỉnh nhọn quanh 0 nhưng có **đuôi phải rất dài**, kéo dài tới hơn 100 (trong khi phần lớn khối lượng nằm trong khoảng [−20, 20]) — dấu hiệu phần dư không đối xứng, gợi ý cả vấn đề về normality (A5) lẫn khả năng có outlier/heteroskedasticity.
<br><span class="en">**Density plot of the residuals** (`plot(density(data$u))`): the residual distribution has a sharp peak around 0 but a **very long right tail**, extending past 100 (while most of the mass sits within [−20, 20]) — a sign that the residuals are asymmetric, suggesting both a normality issue (A5) and the possibility of outliers/heteroskedasticity.</span>
- **Residuals vs. Predicted values** (`plot(data$yh, data$u)`, trục x = "Predicted monthly expense", trục y = "Residuals"): đây là đồ thị chẩn đoán heteroskedasticity kinh điển nhất.
<br><span class="en">**Residuals vs. Predicted values** (`plot(data$yh, data$u)`, x-axis = "Predicted monthly expense", y-axis = "Residuals"): this is the classic heteroskedasticity diagnostic plot.</span>
  Khi giá trị dự đoán còn thấp (khoảng 0–20 triệu VNĐ), các điểm phần dư tụ rất sát quanh 0.
  <br><span class="en">When the predicted value is still low (around 0–20 million VND), the residual points cluster very tightly around 0.</span>
  Nhưng khi giá trị dự đoán tăng lên (40–80 triệu VNĐ), các điểm phần dư **tỏa rộng ra rất nhiều** — từ khoảng −40 đến gần +100.
  <br><span class="en">But as the predicted value increases (40–80 million VND), the residual points **spread out much more widely** — ranging from about −40 to nearly +100.</span>
  Hình dạng "loa kèn" (fan-out/cone shape) này — độ phân tán của phần dư tăng dần theo giá trị dự đoán — là chữ ký thị giác chuẩn của heteroskedasticity, và khớp chính xác với trực giác ở mục 1 (hộ dự đoán chi tiêu cao — tức hộ thu nhập cao — có sai số dự đoán dao động rộng hơn nhiều).
  <br><span class="en">This "megaphone" shape (fan-out/cone shape) — the spread of the residuals increasing with the predicted value — is the standard visual signature of heteroskedasticity, and matches exactly the intuition from section 1 (households with high predicted expenditure — i.e. high-income households — have prediction errors that fluctuate much more widely).</span>

Đồ thị chỉ cho **gợi ý bằng mắt**, không phải bằng chứng thống kê chính thức — cần các kiểm định chính thức ở mục 7–8 để kết luận chắc chắn.
<br><span class="en">The plots only give a **visual hint**, not formal statistical evidence — the formal tests in sections 7–8 are needed to reach a firm conclusion.</span>

## 6. Hậu quả của heteroskedasticity — điểm hay bị hiểu nhầm nhất - <span class="en">Consequences of heteroskedasticity — the most commonly misunderstood point</span>

Đây là phần **quan trọng nhất** của toàn bộ topic, vì nó là nguồn gốc của bẫy thi phổ biến nhất (xem mục 11, bẫy #1).
<br><span class="en">This is the **most important** part of the entire topic, because it is the source of the most common exam trap (see section 11, trap #1).</span>

**Điều heteroskedasticity KHÔNG làm**: hệ số ước lượng OLS $b=(X'X)^{-1}X'y$ **vẫn unbiased và consistent**.
<br><span class="en">**What heteroskedasticity does NOT do**: the OLS estimated coefficient $b=(X'X)^{-1}X'y$ **remains unbiased and consistent**.</span>
Lý do sâu xa: tính unbiased/consistent của OLS chỉ dựa vào các giả định A1–A3 (linearity, full rank, exogeneity) — xem [[concepts/linear-regression-model]] mục 4.
<br><span class="en">The underlying reason: OLS's unbiasedness/consistency rests only on assumptions A1–A3 (linearity, full rank, exogeneity) — see [[concepts/linear-regression-model]] section 4.</span>
A4 (homoskedasticity) **không** nằm trong danh sách điều kiện cần cho unbiasedness/consistency; nó chỉ liên quan đến **efficiency** và **công thức VCV/SE**.
<br><span class="en">A4 (homoskedasticity) is **not** among the conditions required for unbiasedness/consistency; it only pertains to **efficiency** and the **VCV/SE formula**.</span>
Vi phạm A4 không đụng gì đến A1–A3, nên $b$ vẫn là ước lượng đúng, chỉ là không còn "tốt nhất" theo nghĩa dưới đây.
<br><span class="en">Violating A4 does not touch A1–A3 at all, so $b$ remains a correct estimator, just no longer "best" in the sense below.</span>

**Điều heteroskedasticity THỰC SỰ làm**, theo hai mạch hậu quả:
<br><span class="en">**What heteroskedasticity ACTUALLY does**, through two lines of consequence:</span>

1. **Mất tính "Best" trong BLUE**: định lý Gauss-Markov nói OLS là **B**est **L**inear **U**nbiased **E**stimator — nhưng chữ "Best" (phương sai nhỏ nhất trong nhóm ước lượng tuyến tính không chệch) chỉ đúng **khi A4 giữ**.
<br><span class="en">**Losing "Best" in BLUE**: the Gauss-Markov theorem says OLS is the **B**est **L**inear **U**nbiased **E**stimator — but the word "Best" (smallest variance among unbiased linear estimators) only holds **when A4 holds**.</span>
   Khi heteroskedasticity xảy ra, OLS vẫn Linear và Unbiased, nhưng **không còn Best** — tồn tại một ước lượng khác (GLS/WLS có trọng số phù hợp) hiệu quả hơn OLS trong bối cảnh này.
   <br><span class="en">When heteroskedasticity occurs, OLS remains Linear and Unbiased, but **is no longer Best** — there exists another estimator (GLS/WLS with appropriate weights) that is more efficient than OLS in this setting.</span>
   Nói cách khác: OLS vẫn đúng "trung bình" nhưng không còn "chụm nhất có thể".
   <br><span class="en">In other words: OLS is still correct "on average" but is no longer "as tight as possible".</span>
2. **Công thức VCV/SE chuẩn bị sai**: VCV chuẩn được tính dưới giả định A4:
<br><span class="en">**The standard VCV/SE formula becomes wrong**: the standard VCV is computed under the A4 assumption:</span>
   $$VCV = (X'X)^{-1}\sigma^2$$
   và SE là căn bậc hai của các phần tử trên đường chéo VCV này.
   <br><span class="en">and SE is the square root of the diagonal elements of this VCV.</span>
   Công thức này **chỉ đúng khi $Var(\varepsilon)=\sigma^2$ là hằng số**.
   <br><span class="en">This formula **is only correct when $Var(\varepsilon)=\sigma^2$ is constant**.</span>
   Khi A4 bị vi phạm, công thức trên không còn phản ánh đúng độ bất định thật sự của $b$ — nói theo cách slide gốc dùng: "VCV và SE bị chệch" (biased).
   <br><span class="en">When A4 is violated, the formula above no longer correctly reflects the true uncertainty of $b$ — in the words the original slide uses: "VCV and SE are biased".</span>
   *Ghi chú diễn giải*: cách dùng từ "biased" ở đây của slide mang tính mô tả trực quan hơn là một phát biểu kỹ thuật chặt chẽ về phân phối lấy mẫu của SE; điều chính xác cần hiểu là **công thức SE thường không còn là một ước lượng đúng (invalid/không phù hợp) của độ bất định thật của $b$** khi A4 sai — SE tính ra có thể quá nhỏ hoặc quá lớn so với thực tế, không theo hướng cố định.
   <br><span class="en">*Interpretive note*: the slide's use of the word "biased" here is more of an intuitive description than a technically rigorous statement about the sampling distribution of SE; the precise thing to understand is that **the usual SE formula is no longer a valid (invalid/not appropriate) estimate of the true uncertainty of $b$** when A4 is wrong — the computed SE can be too small or too large relative to reality, with no fixed direction.</span>

**Hệ quả dây chuyền**: vì t-statistic $=\dfrac{b_j-c}{SE(b_j)}$ và F-statistic (qua Wald test, xem mục 10) đều xây dựng trực tiếp trên SE/VCV, khi SE sai thì **t-statistic sai, p-value sai, confidence interval sai** — toàn bộ suy luận thống kê (inference) trở nên không đáng tin, **dù bản thân hệ số $b$ vẫn đúng**.
<br><span class="en">**Chain-reaction consequence**: since the t-statistic $=\dfrac{b_j-c}{SE(b_j)}$ and the F-statistic (via the Wald test, see section 10) are both built directly on SE/VCV, when SE is wrong then **the t-statistic is wrong, the p-value is wrong, the confidence interval is wrong** — the entire chain of statistical inference becomes unreliable, **even though the coefficient $b$ itself is still correct**.</span>

> **Bẫy hiểu nhầm phổ biến nhất của cả topic**: nhiều người học nhầm rằng "heteroskedasticity làm hệ số hồi quy bị chệch (biased)".
> <br><span class="en">**The most common misunderstanding trap of the whole topic**: many learners mistakenly believe that "heteroskedasticity makes the regression coefficient biased".</span>
> Điều này **SAI**.
> <br><span class="en">This is **WRONG**.</span>
> Heteroskedasticity chỉ làm **SE/VCV** (và do đó suy luận thống kê) không đáng tin — hệ số $b$ tự nó không hề bị ảnh hưởng.
> <br><span class="en">Heteroskedasticity only makes **SE/VCV** (and hence statistical inference) unreliable — the coefficient $b$ itself is not affected at all.</span>
> Đây là lý do "giải pháp" cho heteroskedasticity (mục 9) chỉ cần sửa công thức SE, **không cần** ước lượng lại hệ số bằng phương pháp khác.
> <br><span class="en">This is why the "solution" for heteroskedasticity (section 9) only needs to fix the SE formula, **not** re-estimate the coefficients with a different method.</span>

## 7. Phát hiện chính thức: Breusch-Pagan (BP) test - <span class="en">Formal detection: the Breusch-Pagan (BP) test</span>

### 7.1 Trực giác - <span class="en">Intuition</span>

Nếu phương sai sai số thực sự đồng đều (homoskedastic), thì độ lớn của phần dư (đo bằng $e^2$, ước lượng cho phương sai sai số tại từng quan sát) **không nên** có mối liên hệ hệ thống nào với các biến giải thích $X$.
<br><span class="en">If the error variance is truly uniform (homoskedastic), then the magnitude of the residual (measured by $e^2$, an estimate of the error variance at each observation) **should not** have any systematic relationship with the explanatory variables $X$.</span>
Ngược lại, nếu $e^2$ **có** liên hệ rõ ràng với $X$ (ví dụ $e^2$ tăng khi $X$ tăng — đúng như đồ thị "loa kèn" ở mục 5), đó là bằng chứng của heteroskedasticity.
<br><span class="en">Conversely, if $e^2$ **does** have a clear relationship with $X$ (for example $e^2$ increases as $X$ increases — exactly as in the "megaphone" plot in section 5), that is evidence of heteroskedasticity.</span>
Ý tưởng của BP test: **hồi quy $e^2$ lên chính các biến giải thích ban đầu**, rồi kiểm định xem hồi quy phụ này có ý nghĩa thống kê hay không.
<br><span class="en">The idea of the BP test: **regress $e^2$ on the original explanatory variables themselves**, then test whether this auxiliary regression is statistically significant.</span>

### 7.2 Công thức - <span class="en">Formula</span>

Với phương trình hồi quy gốc $y=\beta_0+\beta_1X_1+\cdots+\beta_kX_k+e$, gọi $e^2$ là ước lượng cho phương sai sai số. Xét **hồi quy phụ (auxiliary regression)**:
<br><span class="en">Given the original regression equation $y=\beta_0+\beta_1X_1+\cdots+\beta_kX_k+e$, let $e^2$ be the estimate of the error variance. Consider the **auxiliary regression**:</span>

$$e^2 = \alpha_0+\alpha_1X_1+\cdots+\alpha_kX_k+u$$

Nếu homoskedastic, $e^2$ phải độc lập với các regressor — tức $\alpha_1=\cdots=\alpha_k=0$. Ta kiểm định:
<br><span class="en">If homoskedastic, $e^2$ must be independent of the regressors — that is, $\alpha_1=\cdots=\alpha_k=0$. We test:</span>

$$H_0: \alpha_1=\alpha_2=\cdots=\alpha_k=0 \qquad (\text{đây là một F-test trên hồi quy phụ})$$

- **Không bác bỏ $H_0$** → không có bằng chứng heteroskedasticity.
<br><span class="en">**Fail to reject $H_0$** → no evidence of heteroskedasticity.</span>
- **Bác bỏ $H_0$** → có bằng chứng heteroskedasticity.
<br><span class="en">**Reject $H_0$** → evidence of heteroskedasticity.</span>

### 7.3 Ví dụ số — case study chi tiêu hộ gia đình - <span class="en">Numerical example — household expenditure case study</span>

Áp dụng lên mô hình `expense ~ income + age_wife + age_husband + hhsize + children` ở mục 4, dùng hàm `lmtest::bptest(model)` trong R (phiên bản **studentized Breusch-Pagan test**):
<br><span class="en">Applying this to the `expense ~ income + age_wife + age_husband + hhsize + children` model from section 4, using the `lmtest::bptest(model)` function in R (the **studentized Breusch-Pagan test** version):</span>

$$BP = 167.46, \quad df=5, \quad \text{p-value} < 2.2\text{e-}16$$

p-value cực nhỏ → **bác bỏ mạnh** $H_0$ (homoskedastic) → có bằng chứng rất rõ ràng rằng mô hình chi tiêu hộ gia đình bị heteroskedasticity — đúng như gợi ý từ đồ thị "loa kèn" ở mục 5.
<br><span class="en">An extremely small p-value → **strongly reject** $H_0$ (homoskedastic) → very clear evidence that the household expenditure model has heteroskedasticity — exactly as suggested by the "megaphone" plot in section 5.</span>

> **Ghi chú về nguồn — điểm cần lưu ý khi đọc slide gốc**: slide trình bày BP test ở mục 7.2 là "**an F-test**" (kiểm định $H_0:\alpha_1=\cdots=\alpha_k=0$ trên hồi quy phụ), nhưng ví dụ minh họa trong R lại dùng `lmtest::bptest(model)`, và chính output của R tự ghi rõ đây là "**studentized Breusch-Pagan test**" với thống kê $BP=167.46$ theo phân phối **Chi-square** ($df=5$), **không phải** phân phối F.
> <br><span class="en">**Source note — a point to watch when reading the original slide**: the slide presents the BP test in section 7.2 as "**an F-test**" (testing $H_0:\alpha_1=\cdots=\alpha_k=0$ on the auxiliary regression), but the R example instead uses `lmtest::bptest(model)`, and R's own output explicitly labels it the "**studentized Breusch-Pagan test**" with statistic $BP=167.46$ following a **Chi-square** distribution ($df=5$), **not** an F distribution.</span>
> Slide sau đó có một khối code riêng, ghi chú "`# F-test version of the BP test`" — hồi quy thủ công $e^2$ lên các biến rồi dùng `car::linearHypothesis()` để lấy đúng phiên bản F — nhưng **không có kết quả số nào được hiển thị** cho khối code này trong slide (chỉ có code, không có output).
> <br><span class="en">The slide then has a separate code block, commented "`# F-test version of the BP test`" — manually regressing $e^2$ on the variables and then using `car::linearHypothesis()` to obtain the actual F version — but **no numerical result is shown** for this code block in the slide (only code, no output).</span>
> Vậy có hai phiên bản BP test cùng tồn tại trong slide (một chi-square qua `bptest()`, một F qua hồi quy phụ thủ công + `linearHypothesis()`) nhưng chỉ phiên bản chi-square có kết quả số minh họa — ghi chú lại đây thay vì tự suy diễn con số cho phiên bản F, theo đúng nguyên tắc của wiki này.
> <br><span class="en">So two versions of the BP test coexist in the slide (a chi-square version via `bptest()`, and an F version via the manual auxiliary regression + `linearHypothesis()`), but only the chi-square version has an illustrative numerical result — this is noted here rather than inventing a number for the F version, in keeping with this wiki's principles.</span>

## 8. White's test - <span class="en">White's test</span>

### 8.1 Trực giác và điểm khác biệt với BP test - <span class="en">Intuition and the difference from the BP test</span>

BP test chỉ hồi quy $e^2$ lên các biến $X$ **ở dạng tuyến tính gốc** — nghĩa là nó chỉ bắt được heteroskedasticity có dạng phụ thuộc tuyến tính đơn giản vào $X$.
<br><span class="en">The BP test only regresses $e^2$ on the $X$ variables **in their original linear form** — meaning it only catches heteroskedasticity that depends on $X$ in a simple linear way.</span>
Nhưng nếu mối quan hệ giữa phương sai sai số và $X$ phức tạp hơn (phi tuyến, hoặc phụ thuộc vào **tương tác** giữa các biến), BP test có thể bỏ sót.
<br><span class="en">But if the relationship between the error variance and $X$ is more complex (nonlinear, or dependent on **interactions** between variables), the BP test may miss it.</span>
**White's test** tổng quát hóa ý tưởng này bằng cách đưa thêm **bình phương** của từng biến giải thích và **tích chéo (cross-product)** giữa mọi cặp biến vào hồi quy phụ — nhờ vậy White's test **không cần giả định trước dạng cụ thể** của heteroskedasticity, linh hoạt hơn BP test.
<br><span class="en">**White's test** generalizes this idea by adding the **square** of each explanatory variable and the **cross-product** between every pair of variables into the auxiliary regression — thanks to this, White's test **does not need to assume a specific form** of heteroskedasticity in advance, making it more flexible than the BP test.</span>

### 8.2 Công thức - <span class="en">Formula</span>

1. Hồi quy $e^2$ lên: các regressor gốc $X_1,\dots,X_k$, bình phương của chúng $X_1^2,\dots,X_k^2$, và tích chéo từng cặp $X_iX_j$ ($i\neq j$).
<br><span class="en">Regress $e^2$ on: the original regressors $X_1,\dots,X_k$, their squares $X_1^2,\dots,X_k^2$, and the pairwise cross-products $X_iX_j$ ($i\neq j$).</span>
2. Lấy $R^2$ từ hồi quy phụ này, nhân với số quan sát $n$:
<br><span class="en">Take $R^2$ from this auxiliary regression, multiplied by the number of observations $n$:</span>
   $$nR^2 \sim \chi^2_{df}$$
   với $df$ = số hệ số ước lượng trong hồi quy phụ (bao gồm cả biến gốc, bình phương, và tích chéo).
   <br><span class="en">where $df$ = the number of estimated coefficients in the auxiliary regression (including the original variables, squares, and cross-products).</span>
3. Dưới $H_0$ (homoskedastic), thống kê $nR^2$ tuân theo phân phối Chi-square với $df$ tương ứng.
<br><span class="en">Under $H_0$ (homoskedastic), the statistic $nR^2$ follows a Chi-square distribution with the corresponding $df$.</span>

**Bác bỏ $H_0$** → có bằng chứng heteroskedasticity; **không bác bỏ** → không có bằng chứng.
<br><span class="en">**Reject $H_0$** → evidence of heteroskedasticity; **fail to reject** → no evidence.</span>

> **Ghi chú về nguồn**: slide chỉ trình bày White's test ở dạng lý thuyết/công thức (không có ví dụ số minh họa bằng dữ liệu chi tiêu hộ gia đình như đã làm với BP test) — không có bảng kết quả `nR²`, `df`, hay p-value cụ thể nào được đưa ra trong deck này cho White's test.
> <br><span class="en">**Source note**: the slide presents White's test only in theoretical/formula form (no numerical example using the household expenditure data as was done for the BP test) — no results table with `nR²`, `df`, or a specific p-value is given in this deck for White's test.</span>
> Vì vậy phần này chỉ trình bày được công thức và trực giác, không có case study số đi kèm — không tự bịa thêm con số.
> <br><span class="en">Therefore this section can only present the formula and intuition, with no accompanying numerical case study — no numbers are invented here.</span>

**Tóm tắt khác biệt BP vs. White**:
<br><span class="en">**Summary of the BP vs. White difference**:</span>

| | Breusch-Pagan (BP) | White's test |
|---|---|---|
| Hồi quy phụ trên<br><span class="en">Auxiliary regression on</span> | $X_1,\dots,X_k$ (tuyến tính gốc)<br><span class="en">$X_1,\dots,X_k$ (original linear form)</span> | $X_1,\dots,X_k$ + bình phương + tích chéo từng cặp<br><span class="en">$X_1,\dots,X_k$ + squares + pairwise cross-products</span> |
| Giả định về dạng heteroskedasticity<br><span class="en">Assumption about the form of heteroskedasticity</span> | Cần dạng tuyến tính đơn giản với $X$<br><span class="en">Requires a simple linear form in $X$</span> | Không cần giả định dạng cụ thể — tổng quát hơn<br><span class="en">No need to assume a specific form — more general</span> |
| Thống kê kiểm định<br><span class="en">Test statistic</span> | F-test (theo lý thuyết) hoặc Chi-square (bản studentized, `bptest()` trong R)<br><span class="en">F-test (in theory) or Chi-square (studentized version, `bptest()` in R)</span> | $nR^2 \sim \chi^2$ |
| Độ linh hoạt<br><span class="en">Flexibility</span> | Thấp hơn<br><span class="en">Lower</span> | **Cao hơn** — bắt được cả các dạng heteroskedasticity phi tuyến/tương tác mà BP bỏ sót<br><span class="en">**Higher** — catches nonlinear/interaction forms of heteroskedasticity that BP misses</span> |

## 9. Giải pháp: Robust Standard Errors (White/Huber-White) - <span class="en">Solution: Robust Standard Errors (White/Huber-White)</span>

### 9.1 Cơ chế trực giác - <span class="en">Intuitive mechanism</span>

Vấn đề gốc rễ ở mục 6 là công thức $VCV=(X'X)^{-1}\sigma^2$ giả định $\sigma^2$ là **một** hằng số chung cho mọi quan sát — đây chính xác là điều A4 khẳng định và heteroskedasticity phủ nhận.
<br><span class="en">The root problem from section 6 is that the formula $VCV=(X'X)^{-1}\sigma^2$ assumes $\sigma^2$ is **a single** constant common to every observation — this is exactly what A4 asserts and what heteroskedasticity denies.</span>
Ý tưởng của **robust standard errors** rất trực tiếp: **thay vì giả định** $Var(\varepsilon)=\sigma^2I$ là hằng số, ta **ước lượng trực tiếp** phương sai sai số tại *từng* quan sát bằng chính phần dư bình phương $\hat\varepsilon_i^2$ của quan sát đó — không cần biết trước heteroskedasticity có dạng cụ thể như thế nào (tăng theo income? theo hhsize? theo dạng gì?).
<br><span class="en">The idea behind **robust standard errors** is very direct: **instead of assuming** $Var(\varepsilon)=\sigma^2I$ is constant, we **directly estimate** the error variance at *each* observation using that observation's own squared residual $\hat\varepsilon_i^2$ — with no need to know in advance what specific form the heteroskedasticity takes (increasing with income? with hhsize? in what shape?).</span>
Đây là lý do robust SE là cách "chữa cháy" phổ biến nhất trong thực hành: nó **không đòi hỏi biết đúng dạng heteroskedasticity** — chỉ cần biết là *có thể có* heteroskedasticity, công thức vẫn tự động điều chỉnh đúng.
<br><span class="en">This is why robust SE is the most common "fix" used in practice: it **does not require knowing the correct form of heteroskedasticity** — one only needs to know that heteroskedasticity *might* be present, and the formula automatically adjusts correctly.</span>

### 9.2 Công thức - <span class="en">Formula</span>

VCV chuẩn (dưới A4): $VCV=(X'X)^{-1}\sigma^2$.
<br><span class="en">The standard VCV (under A4): $VCV=(X'X)^{-1}\sigma^2$.</span>
Nếu **không** giả định $Var(\varepsilon)=\sigma^2$ là hằng số, mà thay vào đó ước lượng trực tiếp ma trận $Var(\varepsilon)$ — một ma trận đường chéo với các phần tử $\hat\varepsilon_i^2$ (ước lượng từ chính phần dư của mô hình):
<br><span class="en">If we **do not** assume $Var(\varepsilon)=\sigma^2$ is constant, and instead directly estimate the matrix $Var(\varepsilon)$ — a diagonal matrix with elements $\hat\varepsilon_i^2$ (estimated from the model's own residuals):</span>

$$Var(\varepsilon) = \begin{pmatrix}\hat\varepsilon_1^2 & 0 & \cdots & 0\\ 0 & \hat\varepsilon_2^2 & \cdots & 0\\ \vdots & & \ddots & \vdots\\ 0 & 0 & \cdots & \hat\varepsilon_n^2\end{pmatrix}$$

thì VCV tổng quát trở thành:
<br><span class="en">then the general VCV becomes:</span>

$$VCV = (X'X)^{-1}X'\,Var(\varepsilon)\,X(X'X)^{-1}$$

Đây gọi là **White's heteroskedasticity-consistent (HC) VCV**.
<br><span class="en">This is called **White's heteroskedasticity-consistent (HC) VCV**.</span>
SE tính từ HC-VCV (căn bậc hai của các phần tử trên đường chéo HC-VCV) gọi là **robust standard errors** (còn gọi là White SE hoặc Huber-White SE) — dùng được **bất kể** có heteroskedasticity hay không (nếu thực sự homoskedastic, robust SE và SE thường sẽ cho kết quả gần giống nhau), nên trong thực hành thường được dùng **mặc định**, kể cả khi chưa chắc chắn có heteroskedasticity hay không.
<br><span class="en">SE computed from HC-VCV (the square root of the diagonal elements of HC-VCV) is called **robust standard errors** (also called White SE or Huber-White SE) — usable **regardless** of whether heteroskedasticity is present or not (if truly homoskedastic, robust SE and the usual SE will give nearly identical results), so in practice it is often used **by default**, even when one is not yet sure whether heteroskedasticity is present.</span>

### 9.3 Ví dụ số — so sánh SE thường vs. robust SE - <span class="en">Numerical example — comparing usual SE vs. robust SE</span>

Trong R, robust SE tính qua `coeftest(model, vcov = sandwich)` (packages `lmtest` + `sandwich`). Kết quả cho mô hình chi tiêu hộ gia đình:
<br><span class="en">In R, robust SE is computed via `coeftest(model, vcov = sandwich)` (packages `lmtest` + `sandwich`). Results for the household expenditure model:</span>

| Biến<br><span class="en">Variable</span> | Estimate | SE thường<br><span class="en">usual SE</span> | SE robust | Tỷ lệ robust/thường<br><span class="en">robust/usual ratio</span> | t (robust) | p (robust) |
|---|---|---|---|---|---|---|
| (Intercept) | 0.1392 | 2.2245 | 3.4777 | ×1.56 | 0.0400 | 0.968 |
| `income` | 0.4285 | 0.0237 | 0.1323 | **×5.59** | 3.2391 | 0.0013 ** |
| `age_wife` | 0.1102 | 0.0932 | 0.1067 | ×1.15 | 1.0325 | 0.302 |
| `age_husband` | −0.0859 | 0.0935 | 0.1083 | ×1.16 | −0.7928 | 0.428 |
| `hhsize` | 0.6924 | 0.1693 | 0.2091 | ×1.24 | 3.3110 | 0.0010 ** |
| `children` | 0.0661 | 0.0309 | 0.0446 | ×1.44 | 1.4814 | **0.139** |

Hai điểm cần đặc biệt chú ý:
<br><span class="en">Two points deserve special attention:</span>

1. **SE của `income` tăng gần 5.6 lần** (từ 0.0237 lên 0.1323) — mức thay đổi rất lớn, khớp với việc đồ thị residuals-vs-fitted ở mục 5 cho thấy phương sai sai số phình mạnh nhất ở vùng chi tiêu/thu nhập cao.
<br><span class="en">**The SE of `income` increases nearly 5.6-fold** (from 0.0237 to 0.1323) — a very large change, consistent with the residuals-vs-fitted plot in section 5 showing the error variance ballooning most strongly in the high expenditure/income region.</span>
   Dù vậy, `income` vẫn có ý nghĩa thống kê ở robust SE (p=0.0013), chỉ là t-statistic giảm mạnh từ 18.094 xuống 3.2391 — bằng chứng vẫn còn nhưng "yếu" hơn nhiều so với những gì SE thường (sai) từng cho thấy.
   <br><span class="en">Even so, `income` remains statistically significant under robust SE (p=0.0013), it's just that the t-statistic drops sharply from 18.094 to 3.2391 — the evidence is still there but much "weaker" than what the (wrong) usual SE had shown.</span>
2. **`children` đổi kết luận hoàn toàn**: với SE thường, `children` có ý nghĩa thống kê ở mức 5% (p=0.033, có dấu `*`); với robust SE, p-value tăng lên 0.139 — **không còn ý nghĩa thống kê** ở bất kỳ ngưỡng $\alpha$ thông thường nào.
<br><span class="en">**`children` completely flips the conclusion**: with the usual SE, `children` is statistically significant at the 5% level (p=0.033, marked `*`); with robust SE, the p-value rises to 0.139 — **no longer statistically significant** at any conventional $\alpha$ threshold.</span>
   Đây là ví dụ cụ thể, rõ ràng nhất cho thấy **robust SE có thể đảo ngược kết luận nghiên cứu** — nếu chỉ dùng SE thường (không kiểm tra heteroskedasticity), người nghiên cứu sẽ kết luận nhầm rằng % trẻ em trong hộ có ảnh hưởng đáng kể lên chi tiêu, trong khi thực ra không đủ bằng chứng cho điều đó.
   <br><span class="en">This is the clearest, most concrete example showing that **robust SE can reverse a research conclusion** — if one used only the usual SE (without checking for heteroskedasticity), the researcher would wrongly conclude that the % of children in the household has a significant effect on expenditure, when in fact there isn't sufficient evidence for that.</span>

## 10. Wald F-test dùng robust VCV - <span class="en">Wald F-test using robust VCV</span>

### 10.1 Vì sao cần Wald test riêng - <span class="en">Why a separate Wald test is needed</span>

F-statistic "thông thường" (tính từ $RSS_r, RSS_u$ — xem [[concepts/linear-regression-model]] mục 8) **vẫn giữ nguyên giá trị** dưới heteroskedasticity, vì công thức đó chỉ dựa vào RSS (tổng bình phương phần dư), không trực tiếp dùng SE/VCV.
<br><span class="en">The "ordinary" F-statistic (computed from $RSS_r, RSS_u$ — see [[concepts/linear-regression-model]] section 8) **keeps the same value** under heteroskedasticity, because that formula relies only on RSS (the residual sum of squares), not directly on SE/VCV.</span>
Tuy nhiên, trong thực hành, F-test thường được thực hiện thông qua **Wald test** (tương đương về mặt toán học với F-test khi VCV chuẩn đúng), và Wald test thì **dùng trực tiếp VCV** trong công thức — nên khi thay VCV chuẩn bằng HC-VCV (robust), kết quả Wald test **sẽ thay đổi**.
<br><span class="en">However, in practice, the F-test is often carried out via the **Wald test** (mathematically equivalent to the F-test when the standard VCV is correct), and the Wald test **uses VCV directly** in its formula — so when the standard VCV is replaced with the HC-VCV (robust), the Wald test result **will change**.</span>

### 10.2 Công thức - <span class="en">Formula</span>

$$H_0: R\beta=0, \qquad W = (Rb)'\big[R\cdot VCV\cdot R'\big]^{-1}(Rb) \sim \chi^2_q$$

với $R$ là ma trận ràng buộc (chỉ định các hệ số đang bị kiểm định), $q$ là số hệ số bị kiểm định cùng lúc. F-statistic suy ra từ Wald statistic:
<br><span class="en">where $R$ is the restriction matrix (specifying which coefficients are being tested), and $q$ is the number of coefficients tested jointly. The F-statistic is derived from the Wald statistic:</span>

$$F = \frac{W}{q}$$

Gọi cách làm này là **Wald F-test**.
<br><span class="en">This approach is called the **Wald F-test**.</span>
Vì $VCV$ trong công thức Wald có thể là VCV chuẩn hoặc HC-VCV (robust), **thống kê Wald F và p-value sẽ khác nhau** tùy loại VCV được dùng — đây là lý do luôn cần **chỉ định rõ đang dùng VCV nào** khi báo cáo kết quả kiểm định (đặc biệt quan trọng khi viết luận văn).
<br><span class="en">Because the $VCV$ in the Wald formula can be either the standard VCV or the HC-VCV (robust), **the Wald F statistic and p-value will differ** depending on which VCV is used — this is why it is always necessary to **clearly specify which VCV is being used** when reporting test results (especially important when writing a thesis).</span>

### 10.3 Ví dụ số — kiểm định đồng thời `hhsize` và `children` - <span class="en">Numerical example — jointly testing `hhsize` and `children`</span>

Kiểm định $H_0:\beta_{hhsize}=\beta_{children}=0$ trên mô hình chi tiêu hộ gia đình, dùng `car::linearHypothesis()`:
<br><span class="en">Testing $H_0:\beta_{hhsize}=\beta_{children}=0$ on the household expenditure model, using `car::linearHypothesis()`:</span>

**F-test thường (VCV chuẩn):**
<br><span class="en">**Usual F-test (standard VCV):**</span>

| | Res.Df | RSS | Df | Sum of Sq | F | Pr(>F) |
|---|---|---|---|---|---|---|
| Model 1 (restricted) | 466 | 34406 | | | | |
| Model 2 (unrestricted) | 464 | 32689 | 2 | 1716.6 | **12.183** | **6.97e-06 \*\*\*** |

**Wald F-test với robust VCV (`white.adjust = "hc1"`):**
<br><span class="en">**Wald F-test with robust VCV (`white.adjust = "hc1"`):**</span>

| | Res.Df | Df | F | Pr(>F) |
|---|---|---|---|---|
| Model 1 (restricted) | 466 | | | |
| Model 2 (unrestricted) | 464 | 2 | **11.274** | **1.655e-05 \*\*\*** |

Nhận xét: F-statistic đổi từ 12.183 xuống 11.274, p-value đổi từ 6.97e-06 lên 1.655e-05 — **hai con số khác nhau rõ ràng**, đúng như lý thuyết dự đoán.
<br><span class="en">Observation: the F-statistic changes from 12.183 to 11.274, the p-value changes from 6.97e-06 to 1.655e-05 — **two clearly different numbers**, exactly as theory predicts.</span>
Trong trường hợp cụ thể này, **kết luận cuối cùng không đổi** (cả hai đều bác bỏ $H_0$ ở bất kỳ ngưỡng $\alpha$ thông thường nào — cả hai đều có `***`) — nhưng đây chỉ là **trùng hợp của bộ dữ liệu này**, không phải quy luật chung.
<br><span class="en">In this particular case, **the final conclusion does not change** (both reject $H_0$ at any conventional $\alpha$ threshold — both carry `***`) — but this is only a **coincidence of this particular dataset**, not a general rule.</span>
Với `children` ở mục 9.3, ta đã thấy rõ ràng một trường hợp mà việc đổi VCV **có** đổi kết luận (từ có ý nghĩa sang không có ý nghĩa) — nên không thể giả định trước rằng "dùng robust VCV chắc cũng chỉ đổi con số, không đổi kết luận".
<br><span class="en">With `children` in section 9.3, we already saw a clear case where switching the VCV **did** change the conclusion (from significant to not significant) — so one cannot assume in advance that "using robust VCV probably just changes the numbers, not the conclusion".</span>

## 11. Bẫy thi (exam traps) - <span class="en">Exam traps</span>

1. **Kết luận hệ số OLS bị chệch (biased) do heteroskedasticity — SAI.**
<br><span class="en">**Concluding that the OLS coefficient is biased due to heteroskedasticity — WRONG.**</span>
   Đây là bẫy phổ biến nhất của cả topic (xem mục 6, hộp cảnh báo).
   <br><span class="en">This is the most common trap in the whole topic (see section 6, the warning box).</span>
   Heteroskedasticity chỉ làm SE/VCV/suy luận thống kê không đáng tin; hệ số $b$ vẫn **unbiased và consistent** vì tính chất này chỉ phụ thuộc A1–A3, không phụ thuộc A4.
   <br><span class="en">Heteroskedasticity only makes SE/VCV/statistical inference unreliable; the coefficient $b$ remains **unbiased and consistent** because this property depends only on A1–A3, not on A4.</span>
2. **Nhầm heteroskedasticity với mất "Best" (efficiency) thành mất "Unbiased"** — đây là hai khái niệm khác nhau trong BLUE.
<br><span class="en">**Confusing the loss of "Best" (efficiency) with the loss of "Unbiased"** due to heteroskedasticity — these are two different concepts within BLUE.</span>
   Heteroskedasticity làm OLS mất tính *Best* (không còn hiệu quả nhất), nhưng vẫn giữ *Linear* và *Unbiased*.
   <br><span class="en">Heteroskedasticity makes OLS lose the *Best* property (no longer the most efficient), but it still keeps *Linear* and *Unbiased*.</span>
3. **Tương quan cặp cao hoặc thấp trong ma trận tương quan không liên quan gì đến heteroskedasticity** — đó là chẩn đoán của [[concepts/multicollinearity]] (ảnh hưởng A2/full rank), một vấn đề hoàn toàn độc lập với heteroskedasticity (ảnh hưởng A4).
<br><span class="en">**High or low pairwise correlation in the correlation matrix has nothing to do with heteroskedasticity** — that is a diagnostic of [[concepts/multicollinearity]] (affecting A2/full rank), a problem entirely independent from heteroskedasticity (affecting A4).</span>
4. **Quên rằng F-statistic "thô" (dựa trên RSS) thường không đổi dưới heteroskedasticity, nhưng khi F-test được thực hiện qua Wald test (cách làm phổ biến trong thực hành), thống kê và p-value CÓ THỂ thay đổi** khi chuyển từ VCV chuẩn sang robust VCV — xem ví dụ số ở mục 10.3.
<br><span class="en">**Forgetting that the "raw" F-statistic (based on RSS) usually does not change under heteroskedasticity, but when the F-test is carried out via the Wald test (the common approach in practice), the statistic and p-value CAN change** when switching from the standard VCV to a robust VCV — see the numerical example in section 10.3.</span>
5. **Coi BP test và White's test là một** — BP test dùng hồi quy phụ tuyến tính đơn giản trên $X$ gốc, White's test tổng quát hơn (thêm bình phương và tích chéo), không cần giả định trước dạng cụ thể của heteroskedasticity.
<br><span class="en">**Treating the BP test and White's test as the same thing** — the BP test uses a simple linear auxiliary regression on the original $X$, while White's test is more general (adding squares and cross-products), not requiring a specific form of heteroskedasticity to be assumed in advance.</span>
6. **Bỏ qua việc kiểm tra loại VCV nào đang được dùng** khi đọc/báo cáo kết quả kiểm định t-test hay F-test — vì hai loại VCV (thường vs. robust) có thể cho ra kết luận khác nhau (ví dụ `children` ở mục 9.3: có ý nghĩa thống kê với SE thường, không có ý nghĩa với SE robust) — luôn phải nêu rõ đang dùng SE/VCV loại nào.
<br><span class="en">**Neglecting to check which type of VCV is being used** when reading/reporting t-test or F-test results — because the two types of VCV (usual vs. robust) can lead to different conclusions (for example `children` in section 9.3: statistically significant with the usual SE, not significant with robust SE) — one must always state clearly which type of SE/VCV is being used.</span>
7. **Cho rằng robust SE luôn lớn hơn SE thường** — về lý thuyết, robust SE có thể lớn hơn hoặc nhỏ hơn SE thường tùy vào dạng cụ thể của heteroskedasticity trong dữ liệu; không có quy luật "robust SE luôn tăng".
<br><span class="en">**Assuming robust SE is always larger than the usual SE** — in theory, robust SE can be larger or smaller than the usual SE depending on the specific form of heteroskedasticity in the data; there is no rule that "robust SE always increases".</span>
   (Trong ví dụ mục 9.3, mọi hệ số đều có robust SE lớn hơn SE thường, nhưng đây là đặc điểm của bộ dữ liệu này, không phải một định lý tổng quát.)
   <br><span class="en">(In the example in section 9.3, every coefficient has a robust SE larger than the usual SE, but this is a feature of this particular dataset, not a general theorem.)</span>
8. **Coi "dùng robust SE" là giải pháp thay thế cho việc chọn đúng functional form hay kiểm tra outlier** — robust SE chỉ sửa công thức SE, không sửa được mô hình nếu heteroskedasticity thực chất bắt nguồn từ sai functional form hoặc outlier (mục 3) — trong các trường hợp đó, nên cân nhắc sửa mô hình trước khi chỉ "vá" bằng robust SE.
<br><span class="en">**Treating "using robust SE" as a substitute for choosing the correct functional form or checking for outliers** — robust SE only fixes the SE formula, it cannot fix the model if the heteroskedasticity actually originates from a wrong functional form or outliers (section 3) — in those cases, one should consider fixing the model before merely "patching" it with robust SE.</span>

## 12. Kết nối với phần còn lại của khóa học - <span class="en">Connections to the rest of the course</span>

- Vi phạm **A4 (Homoskedasticity)** của [[concepts/linear-regression-model]] — xem mục 4 và mục 6 của trang đó để hiểu vị trí của A4 trong toàn bộ "luật chơi" A1–A5 của OLS.
<br><span class="en">A violation of **A4 (Homoskedasticity)** from [[concepts/linear-regression-model]] — see sections 4 and 6 of that page to understand where A4 sits within the full A1–A5 "rules of the game" for OLS.</span>
- **Cùng bộ dữ liệu minh họa** (khảo sát chi tiêu hộ TP.HCM 2020) với [[concepts/multicollinearity]], nhưng **hai vấn đề hoàn toàn độc lập**: multicollinearity ảnh hưởng A2 (full rank)/efficiency thông qua tương quan giữa các biến giải thích; heteroskedasticity ảnh hưởng A4/độ tin cậy của SE — một mô hình có thể vướng cả hai, một trong hai, hoặc không vướng vấn đề nào, độc lập với nhau.
<br><span class="en">**The same illustrative dataset** (2020 Ho Chi Minh City household expenditure survey) as [[concepts/multicollinearity]], but **two entirely independent issues**: multicollinearity affects A2 (full rank)/efficiency through correlation among the explanatory variables; heteroskedasticity affects A4/the reliability of SE — a model can suffer from both, either one, or neither, independently of each other.</span>
- [[concepts/fixed-random-effects-model]] (Topic 12, panel data) mở rộng khái niệm heteroskedasticity sang bối cảnh dữ liệu bảng (heteroskedasticity **giữa các panel/nhóm**, thường ký hiệu A4a/A4b/A4c trong slide panel data) — cùng logic gốc rễ (phương sai sai số không đồng đều) nhưng áp dụng theo chiều "giữa các đơn vị chéo" thay vì "giữa các quan sát" như ở trang này.
<br><span class="en">[[concepts/fixed-random-effects-model]] (Topic 12, panel data) extends the concept of heteroskedasticity to the panel data setting (heteroskedasticity **across panels/groups**, typically denoted A4a/A4b/A4c in the panel data slides) — the same root logic (non-uniform error variance) but applied along the "across cross-sectional units" dimension instead of "across observations" as on this page.</span>
- Kỹ thuật **robust standard errors** ở đây là nền tảng cho các kỹ thuật "cluster-robust SE" sẽ gặp lại ở panel data — cùng một triết lý: không cần biết đúng dạng của phương sai sai số, chỉ cần ước lượng trực tiếp nó từ dữ liệu.
<br><span class="en">The **robust standard errors** technique here is the foundation for "cluster-robust SE" techniques that will reappear in panel data — the same philosophy: no need to know the exact form of the error variance, just estimate it directly from the data.</span>

## 13. Tài liệu tham khảo ứng dụng thực tế - <span class="en">Real-world application references</span>

Ba bài báo gần đây minh họa vấn đề heteroskedasticity trong nghiên cứu kinh tế thực tế (đề cương Lecture 4):
<br><span class="en">Three recent papers illustrating heteroskedasticity in real-world economic research (Lecture 4 syllabus):</span>

- Li, W., & He, W. (2024). Revenue-increasing effect of rural e-commerce: A perspective of farmers' market integration and employment growth. *Economic Analysis and Policy*, 81, 482-493. https://doi.org/10.1016/j.eap.2023.12.015
- Zhou, Y., & Shi, X. (2025). How Does Digital Technology Adoption Affect Corporate Employment? Evidence from China. *Economic Modelling*, 107045. https://doi.org/10.1016/j.econmod.2025.107045
- Tang, Y., Sun, Y., & He, Z. (2025). Air pollution and firms' robot adoption: Evidence from China. *Economic Modelling*, 143, 106957. https://doi.org/10.1016/j.econmod.2024.106957
