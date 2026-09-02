---
title: "Multicollinearity"
type: concept
status: mature
tags: [multicollinearity, vif, linear-regression, model-diagnostics]
sources: ["[[sources/slides-3-multicollinearity]]"]
related: ["[[concepts/linear-regression-model]]"]
updated: 2026-08-29
---

> **Cách đọc trang này**: multicollinearity là vấn đề "vá lỗi" đầu tiên trong chuỗi topic của khóa học — nó liên quan đến giả định **A2 (Full rank)** của [[concepts/linear-regression-model]], nhưng chỉ ở dạng "gần vi phạm", không phải vi phạm hoàn toàn. Nên đọc lại mục 4 (năm giả định OLS) và mục 6–7 (VCV matrix, Standard Error, t-test) của trang đó trước, vì toàn bộ hệ quả của multicollinearity ở trang này chỉ có ý nghĩa khi đã hiểu SE và t-statistic thực sự đo cái gì.
> <br><span class="en">**How to read this page**: multicollinearity is the first "bug-fix" issue in the course's topic sequence — it relates to assumption **A2 (Full rank)** of [[concepts/linear-regression-model]], but only in a "near-violation" form, not a full violation. You should reread section 4 (the five OLS assumptions) and sections 6–7 (VCV matrix, Standard Error, t-test) of that page first, because every consequence of multicollinearity on this page only makes sense once you understand what SE and the t-statistic actually measure.</span>

## 1. Trực giác: Multicollinearity là gì — và KHÔNG phải là gì - <span class="en">Intuition: what multicollinearity is — and is NOT</span>

Điểm dễ hiểu lầm nhất khi mới học: multicollinearity **không phải** là chuyện biến độc lập ($X$) tương quan với biến phụ thuộc ($y$) — đó là điều **mong muốn**, chính là lý do ta đưa $X$ vào mô hình ngay từ đầu. Multicollinearity là chuyện **hai (hoặc nhiều) biến độc lập tương quan mạnh với NHAU**.
<br><span class="en">The most common point of confusion for beginners: multicollinearity is **not** about an independent variable ($X$) correlating with the dependent variable ($y$) — that is actually **desirable**, indeed the very reason we include $X$ in the model in the first place. Multicollinearity is about **two (or more) independent variables being strongly correlated with EACH OTHER**.</span>

Ví dụ cụ thể — lấy ngay từ case study xuyên suốt trang này (mục 4 bên dưới): trong khảo sát 470 cặp vợ chồng tại TP.HCM năm 2020, tuổi vợ (`age_wife`) và tuổi chồng (`age_husband`) tương quan với nhau tới $r=0.921$ (mục 8.1) — điều này hợp lý về mặt xã hội học: người ta có xu hướng kết hôn với người cùng trang lứa. Cả hai biến đều có khả năng ảnh hưởng riêng lên chi tiêu hộ gia đình (`expense`), nhưng vì chúng gần như luôn "di chuyển cùng nhau" trong mẫu dữ liệu (hộ có vợ lớn tuổi thì hầu như chắc chắn cũng có chồng lớn tuổi), OLS gần như không có đủ **biến thiên độc lập** để tách bạch: chi tiêu tăng là do vợ già hơn, do chồng già hơn, hay do cả hai? Kết quả (xem số liệu thật ở mục 5): mô hình vẫn ước lượng được, nhưng ước lượng riêng cho từng biến tuổi rất "run rẩy", không đủ chắc chắn để bác bỏ giả thuyết hệ số bằng 0 — dù về lý thuyết tuổi tác hoàn toàn có thể ảnh hưởng đến chi tiêu.
<br><span class="en">A concrete example — taken directly from the case study running through this page (section 4 below): in a 2020 survey of 470 married couples in Ho Chi Minh City, wife's age (`age_wife`) and husband's age (`age_husband`) correlate at $r=0.921$ (section 8.1) — which makes sociological sense: people tend to marry someone of a similar age. Both variables could plausibly have their own effect on household expenditure (`expense`), but because they almost always "move together" in the sample (a household with an older wife almost certainly also has an older husband), OLS has almost no **independent variation** left to disentangle: did expenditure rise because the wife is older, because the husband is older, or both? The result (see the actual numbers in section 5): the model can still be estimated, but the separate estimates for each age variable are very "shaky," not confident enough to reject the hypothesis that the coefficient is zero — even though, in theory, age could well affect expenditure.</span>

**Ẩn dụ hình ảnh**: hình dung hai biến độc lập tương quan cao như hai vòng tròn Venn chồng lấn gần như hoàn toàn lên nhau. Phần "thông tin riêng, không trùng lặp" của từng biến (phần không chồng lấn) rất nhỏ — mà OLS chỉ có thể dùng đúng phần thông tin *riêng* đó để ước lượng hệ số *riêng* của từng biến. Phần chồng lấn (thông tin chung, nơi hai biến di chuyển giống nhau) không giúp phân biệt được hiệu ứng của biến nào — nó bị "lãng phí" theo nghĩa thống kê.
<br><span class="en">**Visual metaphor**: picture two highly correlated independent variables as two Venn diagram circles that overlap almost completely. Each variable's "unique, non-overlapping information" (the non-overlapping sliver) is very small — and OLS can only use that *unique* sliver of information to estimate each variable's *own* coefficient. The overlapping part (the shared information, where both variables move together) does not help distinguish which variable's effect is which — it is "wasted" in a statistical sense.</span>

## 2. Perfect collinearity vs. Imperfect collinearity (multicollinearity) - <span class="en">Perfect collinearity vs. Imperfect collinearity (multicollinearity)</span>

Mô hình hồi quy tuyến tính cổ điển (CLRM) giả định **A2 — Full rank**: không có quan hệ tuyến tính hoàn hảo giữa các regressor. Slide phân biệt rõ hai loại collinearity, và đây là điểm hay bị gộp lẫn khi ôn thi:
<br><span class="en">The Classical Linear Regression Model (CLRM) assumes **A2 — Full rank**: no perfect linear relationship among the regressors. The slide clearly distinguishes two types of collinearity, and this is a point that's often conflated during exam review:</span>

- **Perfect collinearity**: quan hệ tuyến tính **hoàn hảo** giữa 2+ biến (VD $X_2=2X_1$ đúng cho *mọi* quan sát). Đây là vi phạm A2 **hoàn toàn** — không phải "vấn đề cần cân nhắc" mà là **lỗi kỹ thuật khiến mô hình không chạy được**.
  <br><span class="en">**Perfect collinearity**: a **perfect** linear relationship between 2+ variables (e.g., $X_2=2X_1$ holding for *every* observation). This is a **complete** violation of A2 — not "an issue to weigh" but a **technical error that stops the model from running at all**.</span>
- **Imperfect collinearity (multicollinearity)**: các regressor tương quan cao nhưng **không hoàn hảo** — mô hình vẫn ước lượng được bình thường, chỉ là kém tin cậy hơn (SE lớn hơn). Đây là "gần vi phạm" A2, không phải vi phạm hoàn toàn.
  <br><span class="en">**Imperfect collinearity (multicollinearity)**: the regressors are highly correlated but **not perfectly** — the model still estimates normally, just less reliably (larger SE). This is a "near-violation" of A2, not a full violation.</span>

### Vì sao perfect collinearity làm OLS "vỡ" — chứng minh bằng đại số - <span class="en">Why perfect collinearity "breaks" OLS — an algebraic proof</span>

Với $y=\beta_0+\beta_1X_1+\beta_2X_2$ và $X_2=2X_1$ (quan hệ tuyến tính hoàn hảo), thay vào mô hình:
<br><span class="en">With $y=\beta_0+\beta_1X_1+\beta_2X_2$ and $X_2=2X_1$ (a perfect linear relationship), substituting into the model:</span>

$$y=\beta_0+\beta_1X_1+\beta_2(2X_1)=\beta_0+(\beta_1+2\beta_2)X_1=\beta_0+\gamma X_1, \qquad \gamma=\beta_1+2\beta_2$$

Mô hình gốc "thu gọn" thành một mô hình chỉ còn một biến $X_1$ với hệ số $\gamma$. Vấn đề: với **một** giá trị $\gamma$ ước lượng được, có **vô số** cặp $(\beta_1,\beta_2)$ thỏa mãn phương trình $\gamma=\beta_1+2\beta_2$. Slide minh họa bằng $\gamma=1$:
<br><span class="en">The original model "collapses" into a model with only one variable $X_1$ and coefficient $\gamma$. The problem: for **one** estimated value of $\gamma$, there are **infinitely many** pairs $(\beta_1,\beta_2)$ satisfying the equation $\gamma=\beta_1+2\beta_2$. The slide illustrates this with $\gamma=1$:</span>

- nếu $\beta_1=2$ thì $\beta_2=-0.5$;
  <br><span class="en">if $\beta_1=2$ then $\beta_2=-0.5$;</span>
- nếu $\beta_1=3$ thì $\beta_2=-1$;
  <br><span class="en">if $\beta_1=3$ then $\beta_2=-1$;</span>
- … (và còn vô số cặp khác).
  <br><span class="en">… (and infinitely many other pairs).</span>

Không có nghiệm duy nhất → $\beta_1,\beta_2$ **không xác định được riêng lẻ** (unidentifiable) → về mặt ma trận, $X'X$ trở thành **không khả nghịch** (uninvertible), khiến công thức OLS estimator $b=(X'X)^{-1}X'y$ (xem [[concepts/linear-regression-model]] mục 2.2) không tính được. Giải pháp bắt buộc: **phải bỏ bớt một trong hai biến collinear hoàn hảo** — không có lựa chọn "giữ cả hai và chấp nhận sai số".
<br><span class="en">There is no unique solution → $\beta_1,\beta_2$ are **individually unidentifiable** → in matrix terms, $X'X$ becomes **non-invertible** (uninvertible), so the OLS estimator formula $b=(X'X)^{-1}X'y$ (see [[concepts/linear-regression-model]] section 2.2) cannot be computed. The required fix: **one of the two perfectly collinear variables must be dropped** — there is no option to "keep both and accept some error".</span>

Khác hẳn với perfect collinearity, **imperfect collinearity (multicollinearity)** không làm $X'X$ mất khả nghịch — công thức OLS vẫn chạy ra được một con số $b$ bình thường. Vấn đề nằm ở **độ tin cậy** của con số đó, không nằm ở việc có tính được hay không. Phần còn lại của trang này nói về trường hợp này.
<br><span class="en">Quite unlike perfect collinearity, **imperfect collinearity (multicollinearity)** does not make $X'X$ non-invertible — the OLS formula still produces a normal value of $b$. The problem lies in the **reliability** of that value, not in whether it can be computed at all. The rest of this page is about this case.</span>

## 3. Nguồn gốc của multicollinearity - <span class="en">Sources of multicollinearity</span>

Slide liệt kê bốn cơ chế khiến các regressor trở nên tương quan cao trong thực tế:
<br><span class="en">The slide lists four mechanisms that make regressors highly correlated in practice:</span>

1. **Inherent relationships** (quan hệ nội tại): một số biến tự nhiên tương quan với nhau — VD giáo dục và thu nhập; các input lao động (labor) và vốn (capital) trong hàm sản xuất.
   <br><span class="en">**Inherent relationships**: some variables are naturally correlated with each other — e.g., education and income; the labor and capital inputs in a production function.</span>
2. **Repeated measures** (đo lường lặp): dùng nhiều biến để đo cùng một khái niệm, hoặc các khái niệm gần nhau — VD tài sản (assets) và thu nhập (income).
   <br><span class="en">**Repeated measures**: using multiple variables to measure the same concept, or closely related concepts — e.g., assets and income.</span>
3. **Sampling issue** (vấn đề chọn mẫu): cách thu thập dữ liệu từ một tổng thể mà ở đó một số biến vốn đã đồng biến tự nhiên có thể vô tình tạo ra multicollinearity trong mẫu.
   <br><span class="en">**Sampling issue**: the way data is collected from a population where some variables already naturally co-vary can inadvertently create multicollinearity in the sample.</span>
4. **Mathematical derivation** (suy ra từ phép tính): một biến được tạo ra trực tiếp từ biến khác — VD dùng cả một biến và bình phương của nó trong cùng mô hình. Đây là điểm nối trực tiếp với [[concepts/functional-forms]] dạng quadratic: khi đưa cả $X$ và $X^2$ vào cùng một mô hình để bắt hiệu ứng phi tuyến, hai biến này gần như chắc chắn tương quan cao.
   <br><span class="en">**Mathematical derivation**: a variable is created directly from another variable — e.g., using both a variable and its square in the same model. This connects directly to the quadratic form of [[concepts/functional-forms]]: when both $X$ and $X^2$ are included in the same model to capture a nonlinear effect, these two variables are almost certainly highly correlated.</span>

## 4. Ví dụ xuyên suốt: Household Expenditure Survey (Married Couples, TP.HCM, 2020) - <span class="en">Running example: Household Expenditure Survey (Married Couples, Ho Chi Minh City, 2020)</span>

Đây là bộ dữ liệu thầy Thụy dùng để minh họa toàn bộ quy trình phát hiện và xử lý multicollinearity — từ đây trở đi mọi con số trong trang đều lấy từ case study này.
<br><span class="en">This is the dataset Professor Thụy uses to illustrate the entire process of detecting and addressing multicollinearity — from here on, every number on this page is taken from this case study.</span>

**Đơn vị phân tích**: các hộ gia đình là cặp vợ chồng, khảo sát năm 2020 tại TP.HCM. Nguồn dữ liệu: `https://econometrics.site/public/mcl.csv`.
<br><span class="en">**Unit of analysis**: households that are married couples, surveyed in 2020 in Ho Chi Minh City. Data source: `https://econometrics.site/public/mcl.csv`.</span>

| Biến<br><span class="en">Variable</span> | Ý nghĩa<br><span class="en">Meaning</span> | Đơn vị<br><span class="en">Unit</span> |
|---|---|---|
| `expense` | Chi tiêu hộ gia đình — **biến phụ thuộc**<br><span class="en">Household expenditure — **dependent variable**</span> | triệu VNĐ/tháng<br><span class="en">million VND/month</span> |
| `income` | Thu nhập hộ gia đình hàng tháng<br><span class="en">Monthly household income</span> | triệu VNĐ/tháng<br><span class="en">million VND/month</span> |
| `age_wife` | Tuổi vợ (hoặc bạn đời nữ)<br><span class="en">Wife's age (or female partner)</span> | năm<br><span class="en">years</span> |
| `age_husband` | Tuổi chồng (hoặc bạn đời nam)<br><span class="en">Husband's age (or male partner)</span> | năm<br><span class="en">years</span> |
| `hhsize` | Quy mô hộ gia đình<br><span class="en">Household size</span> | số thành viên<br><span class="en">number of members</span> |
| `children` | % trẻ em trong hộ gia đình<br><span class="en">% of children in the household</span> | phần trăm<br><span class="en">percent</span> |

> Lưu ý của slide: dữ liệu đã loại bỏ các quan sát có giá trị NA và các hộ có `income = 0`, còn lại $n=470$ quan sát.
> <br><span class="en">Note from the slide: observations with NA values and households with `income = 0` were removed, leaving $n=470$ observations.</span>

**Thống kê mô tả** (sau khi làm sạch, $n=470$ cho mọi biến):
<br><span class="en">**Descriptive statistics** (after cleaning, $n=470$ for every variable):</span>

| Biến<br><span class="en">Variable</span> | mean | sd | median | min | max |
|---|---|---|---|---|---|
| `expense` | 12.02 | 11.16 | 10.0 | 1.0 | 180.00 |
| `income` | 17.03 | 17.00 | 12.5 | 0.4 | 180.00 |
| `age_wife` | 44.91 | 10.86 | 45.0 | 22.0 | 86.00 |
| `age_husband` | 48.36 | 10.73 | 49.0 | 26.0 | 84.81 |
| `hhsize` | 4.72 | 2.32 | 4.0 | 1.0 | 25.00 |
| `children` | 7.88 | 13.06 | 0.0 | 0.0 | 60.00 |

## 5. Kết quả hồi quy OLS đầy đủ — hệ quả nhìn thấy được ngay - <span class="en">Full OLS regression results — the consequence, visible right away</span>

Mô hình ước lượng: $\log(\text{expense}) = \beta_0+\beta_1\log(\text{income})+\beta_2\,\text{age\_wife}+\beta_3\,\text{age\_husband}+\beta_4\,\text{hhsize}+\beta_5\,\text{children}+\varepsilon$
<br><span class="en">Estimated model: $\log(\text{expense}) = \beta_0+\beta_1\log(\text{income})+\beta_2\,\text{age\_wife}+\beta_3\,\text{age\_husband}+\beta_4\,\text{hhsize}+\beta_5\,\text{children}+\varepsilon$</span>

| Biến<br><span class="en">Variable</span> | $b$ | SE | $t$ | $p$-value | Ý nghĩa (5%)<br><span class="en">Significance (5%)</span> |
|---|---|---|---|---|---|
| (Intercept) | 0.8105 | 0.1649 | 4.916 | 1.23e-06 | *** |
| `log(income)` | 0.4231 | 0.0297 | 14.240 | < 2e-16 | *** |
| `age_wife` | 0.0066 | 0.0054 | 1.236 | 0.2172 | không<br><span class="en">no</span> |
| `age_husband` | −0.0053 | 0.0054 | −0.980 | 0.3277 | không<br><span class="en">no</span> |
| `hhsize` | 0.0720 | 0.0097 | 7.400 | 6.46e-13 | *** |
| `children` | 0.0036 | 0.0018 | 2.007 | 0.0453 | * |

$n=470$; Residual SE $=0.4821$ trên $464$ bậc tự do; $R^2=0.3829$; $R^2_{adj}=0.3762$; $F=57.57$ trên $(5,464)$ df, $p<2.2\times10^{-16}$.
<br><span class="en">$n=470$; Residual SE $=0.4821$ on $464$ degrees of freedom; $R^2=0.3829$; $R^2_{adj}=0.3762$; $F=57.57$ on $(5,464)$ df, $p<2.2\times10^{-16}$.</span>

**Điều đáng chú ý nhất** (và là lý do trang này dùng đúng ví dụ này): cả `age_wife` lẫn `age_husband` đều **không có ý nghĩa thống kê** ở mức 5% ($p=0.217$ và $p=0.328$), dù về lý thuyết tuổi tác hộ gia đình hoàn toàn có thể ảnh hưởng đến chi tiêu. Đây chính xác là dấu hiệu kinh điển của multicollinearity: hai biến tương quan cao khiến t-statistic của **cả hai** đều nhỏ, dù (như sẽ thấy ở mục 8) chúng cùng nhau vẫn mang nhiều thông tin. $R^2=0.38$ ở mô hình này **không cao** — cần phân biệt rõ với $R^2$ của *auxiliary regression* ở mục 8.2, vốn mới là con số liên quan trực tiếp đến multicollinearity (bẫy thi #9 ở mục 10).
<br><span class="en">**The most noteworthy point** (and the reason this page uses exactly this example): both `age_wife` and `age_husband` are **not statistically significant** at the 5% level ($p=0.217$ and $p=0.328$), even though household age could in theory well affect expenditure. This is precisely the classic sign of multicollinearity: two highly correlated variables make **both** t-statistics small, even though (as will be seen in section 8) together they still carry a lot of information. $R^2=0.38$ in this model is **not high** — this must be clearly distinguished from the $R^2$ of the *auxiliary regression* in section 8.2, which is the number actually directly relevant to multicollinearity (exam trap #9 in section 10).</span>

## 6. Hệ quả của multicollinearity - <span class="en">Consequences of multicollinearity</span>

- $R^2$ **có thể** rất cao dù ít hệ số có ý nghĩa thống kê riêng lẻ (lưu ý: đây là hệ quả *có thể xảy ra*, không phải luôn xảy ra — trong case study ở mục 5, $R^2$ tổng thể chỉ ở mức trung bình 0.38, nhưng hai biến tuổi vẫn cùng mất ý nghĩa thống kê).
  <br><span class="en">$R^2$ **can** be very high even though few coefficients are individually statistically significant (note: this is a *possible* consequence, not one that always happens — in the case study in section 5, the overall $R^2$ is only a moderate 0.38, yet both age variables still lose statistical significance together).</span>
- Trong một số trường hợp, dấu kỳ vọng của hệ số ước lượng có thể sai (wrong expected sign).
  <br><span class="en">In some cases, the expected sign of an estimated coefficient can be wrong (wrong expected sign).</span>
- **OLS estimator vẫn consistent** — đây là điểm quan trọng nhất cần nhớ và hay bị hiểu sai (xem bẫy thi #3): multicollinearity **không** làm hệ số bị chệch (biased) hay mất tính vững, chỉ làm một hoặc nhiều hệ số có **SE lớn**, khiến t-statistic nhỏ và p-value lớn.
  <br><span class="en">**The OLS estimator remains consistent** — this is the single most important point to remember, and the one most often misunderstood (see exam trap #3): multicollinearity does **not** make coefficients biased or inconsistent, it only gives one or more coefficients a **large SE**, which makes the t-statistic small and the p-value large.</span>
- Vì t-statistic nhỏ, người phân tích dễ **kết luận nhầm** (misleadingly) rằng giá trị thật của các hệ số này không khác 0 — trong khi thực tế biến đó *có thể* thực sự có ảnh hưởng, chỉ là dữ liệu không đủ "biến thiên độc lập" để chứng minh điều đó với độ tin cậy thống kê.
  <br><span class="en">Because the t-statistic is small, an analyst can easily draw the **misleading** conclusion that the true value of these coefficients is no different from 0 — when in fact the variable *may* genuinely have an effect, it's just that the data lacks enough "independent variation" to prove it with statistical confidence.</span>

**Liên hệ ngược lại t-test** ([[concepts/linear-regression-model]] mục 7): nhớ lại $t=\dfrac{b_j-c}{SE(b_j)}$. Khi $SE(b_j)$ bị "phóng đại" do multicollinearity, mẫu số của $t$ tăng lên trong khi tử số ($b_j$) không đổi đáng kể → $|t|$ nhỏ đi → khó vượt ngưỡng bác bỏ $H_0$. Nói cách khác, multicollinearity làm giảm **power** của t-test — tăng nguy cơ **Type II error** (không bác bỏ $H_0$ dù $H_0$ sai, tức bỏ sót một hiệu ứng thực sự tồn tại). Đây là cơ chế thống kê cụ thể đằng sau hệ quả "kết luận nhầm" nói trên.
<br><span class="en">**Linking back to the t-test** ([[concepts/linear-regression-model]] section 7): recall $t=\dfrac{b_j-c}{SE(b_j)}$. When $SE(b_j)$ is "inflated" by multicollinearity, the denominator of $t$ increases while the numerator ($b_j$) doesn't change much → $|t|$ shrinks → it becomes harder to cross the threshold for rejecting $H_0$. In other words, multicollinearity reduces the **power** of the t-test — raising the risk of a **Type II error** (failing to reject $H_0$ even though $H_0$ is false, i.e., missing a genuinely existing effect). This is the specific statistical mechanism behind the "misleading conclusion" consequence mentioned above.</span>

## 7. Variance Inflation Factor (VIF) - <span class="en">Variance Inflation Factor (VIF)</span>

### 7.1 Công thức - <span class="en">Formula</span>

Với mô hình hai regressor $y_i=\beta_0+\beta_1X_1+\beta_2X_2+u$, phương sai của từng hệ số ước lượng:
<br><span class="en">With a two-regressor model $y_i=\beta_0+\beta_1X_1+\beta_2X_2+u$, the variance of each estimated coefficient:</span>

$$Var(\hat\beta_1)=\frac{\sigma^2}{(1-r_{12}^2)\sum(X_1-\bar X_1)^2}=\frac{\sigma^2}{\sum(X_1-\bar X_1)^2}\cdot VIF_1, \qquad Var(\hat\beta_2)=\frac{\sigma^2}{(1-r_{12}^2)\sum(X_2-\bar X_2)^2}=\frac{\sigma^2}{\sum(X_2-\bar X_2)^2}\cdot VIF_2$$

với $\sigma^2$ là phương sai của sai số $u_i$, và $r_{12}$ là hệ số tương quan giữa $X_1$ và $X_2$. Với hai regressor:
<br><span class="en">where $\sigma^2$ is the variance of the error $u_i$, and $r_{12}$ is the correlation coefficient between $X_1$ and $X_2$. With two regressors:</span>

$$VIF=\frac{1}{1-r_{12}^2}$$

VIF đo **mức độ phương sai của OLS estimator bị "phóng đại"** vì multicollinearity, so với trường hợp $X_1,X_2$ hoàn toàn không tương quan ($r_{12}=0$, khi đó $VIF=1$, không có sự phóng đại nào).
<br><span class="en">VIF measures **how much the variance of the OLS estimator is "inflated"** by multicollinearity, relative to the case where $X_1,X_2$ are completely uncorrelated ($r_{12}=0$, in which case $VIF=1$, no inflation at all).</span>

### 7.2 Trực giác: vì sao $r_{12}$ cao (VIF cao) → SE lớn - <span class="en">Intuition: why high $r_{12}$ (high VIF) → large SE</span>

Nhìn vào mẫu số $(1-r_{12}^2)$: khi $r_{12}\to1$ (hai biến gần như đồng biến hoàn hảo), mẫu số $\to0$, khiến $Var(\hat\beta_1)\to\infty$. Trực giác kinh tế đằng sau công thức: $\sum(X_1-\bar X_1)^2$ đo **tổng biến thiên** của $X_1$ có trong mẫu dữ liệu — nhưng khi $X_1$ và $X_2$ tương quan cao, phần lớn biến thiên đó bị "trùng lặp" với $X_2$; phần biến thiên **thực sự độc lập, riêng của $X_1$** (không trùng với $X_2$) rất nhỏ. OLS chỉ có thể dùng đúng phần biến thiên "riêng" đó để tách bạch hiệu ứng của $X_1$ khỏi hiệu ứng của $X_2$ — càng ít biến thiên riêng, ước lượng $\hat\beta_1$ càng dễ dao động mạnh nếu đổi sang một mẫu dữ liệu khác → SE lớn. Đây chính là cơ chế toán học của ẩn dụ "hai vòng tròn Venn chồng lấn" ở mục 1.
<br><span class="en">Look at the denominator $(1-r_{12}^2)$: as $r_{12}\to1$ (the two variables move together almost perfectly), the denominator $\to0$, so $Var(\hat\beta_1)\to\infty$. The economic intuition behind the formula: $\sum(X_1-\bar X_1)^2$ measures the **total variation** of $X_1$ present in the sample — but when $X_1$ and $X_2$ are highly correlated, most of that variation is "duplicated" with $X_2$; the portion of variation that is **truly independent, unique to $X_1$** (not shared with $X_2$) is very small. OLS can only use that "unique" variation to disentangle the effect of $X_1$ from the effect of $X_2$ — the less unique variation there is, the more wildly the estimate $\hat\beta_1$ tends to swing if you switched to a different sample → large SE. This is exactly the mathematical mechanism behind the "overlapping Venn diagram" metaphor in section 1.</span>

### 7.3 Ngưỡng thường dùng - <span class="en">Commonly used thresholds</span>

Quy tắc kinh nghiệm (rule of thumb) theo slide: **$VIF>5$** được coi là nghiêm trọng ở một chỗ trong slide ("Signs of Multicollinearity"), trong khi slide ghi "$VIF>5$ (hoặc 10)" ở chỗ khác — tức thừa nhận cả hai ngưỡng 5 và 10 đều được dùng phổ biến trong thực hành, không chốt một con số duy nhất. Xem thêm lưu ý về sự không nhất quán này ở bẫy thi #7 (mục 10).
<br><span class="en">Rule of thumb per the slide: **$VIF>5$** is treated as serious in one place in the slide ("Signs of Multicollinearity"), while the slide states "$VIF>5$ (or 10)" elsewhere — i.e., it acknowledges that both the 5 and 10 thresholds are commonly used in practice, without committing to a single number. See more on this inconsistency in exam trap #7 (section 10).</span>

## 8. Phát hiện (detection) - <span class="en">Detection</span>

Slide liệt kê ba nhóm công cụ phát hiện, với phân biệt quan trọng: chỉ VIF được coi là **xác nhận** (confirmation), hai công cụ còn lại chỉ là **dấu hiệu** (sign) — gợi ý nhưng không chắc chắn.
<br><span class="en">The slide lists three groups of detection tools, with an important distinction: only VIF is considered a **confirmation**, while the other two tools are merely a **sign** — suggestive but not certain.</span>

| Dấu hiệu<br><span class="en">Sign</span> | Diễn giải<br><span class="en">Interpretation</span> | Mức độ chắc chắn<br><span class="en">Level of certainty</span> |
|---|---|---|
| Dấu hệ số sai kỳ vọng nhưng $R^2$ cao<br><span class="en">Coefficient sign is wrong relative to expectation, but $R^2$ is high</span> | Gợi ý multicollinearity<br><span class="en">Suggests multicollinearity</span> | Dấu hiệu<br><span class="en">Sign</span> |
| $R^2$ cao nhưng ít t-ratio có ý nghĩa<br><span class="en">High $R^2$ but few significant t-ratios</span> | Gợi ý multicollinearity<br><span class="en">Suggests multicollinearity</span> | Dấu hiệu<br><span class="en">Sign</span> |
| Ma trận tương quan cặp cao (ngưỡng thường dùng $\pm0.8$)<br><span class="en">High pairwise correlation matrix values (commonly used threshold $\pm0.8$)</span> | Gợi ý multicollinearity<br><span class="en">Suggests multicollinearity</span> | **Chỉ là dấu hiệu, không phải xác nhận** — tương quan thấp cũng không đảm bảo không có multicollinearity (có thể multicollinear đa biến, không lộ ra ở tương quan cặp đơn lẻ)<br><span class="en">**Only a sign, not a confirmation** — low correlation also does not guarantee the absence of multicollinearity (it could be multivariate multicollinearity, which doesn't show up in any single pairwise correlation)</span> |
| Auxiliary regression: hồi quy mỗi regressor lên toàn bộ regressor còn lại<br><span class="en">Auxiliary regression: regressing each regressor on all other regressors</span> | $R^2$ của auxiliary regression cao (>0.8) hoặc F-test có ý nghĩa<br><span class="en">High $R^2$ of the auxiliary regression (>0.8) or a significant F-test</span> | Dấu hiệu — cùng logic: cao thì gợi ý, thấp không đảm bảo loại trừ<br><span class="en">Sign — same logic: high suggests it, low does not guarantee it's ruled out</span> |
| VIF > 5 (hoặc 10)<br><span class="en">VIF > 5 (or 10)</span> | Được slide coi là **xác nhận** (confirm) multicollinearity nghiêm trọng<br><span class="en">Treated by the slide as **confirming** serious multicollinearity</span> | Xác nhận<br><span class="en">Confirmation</span> |

Áp dụng cả ba công cụ vào case study ở mục 4–5:
<br><span class="en">Applying all three tools to the case study in sections 4–5:</span>

### 8.1 Correlation matrix - <span class="en">Correlation matrix</span>

Ma trận tương quan giữa $\log(\text{income})$, `age_wife`, `age_husband`, `hhsize`, `children`:
<br><span class="en">Correlation matrix among $\log(\text{income})$, `age_wife`, `age_husband`, `hhsize`, `children`:</span>

| | log(income) | age_wife | age_husband | hhsize | children |
|---|---|---|---|---|---|
| **log(income)** | 1.000 | −0.369 | −0.320 | −0.019 | −0.018 |
| **age_wife** | −0.369 | 1.000 | **0.921** | −0.039 | −0.220 |
| **age_husband** | −0.320 | **0.921** | 1.000 | −0.058 | −0.236 |
| **hhsize** | −0.019 | −0.039 | −0.058 | 1.000 | 0.156 |
| **children** | −0.018 | −0.220 | −0.236 | 0.156 | 1.000 |

Tương quan giữa `age_wife` và `age_husband` là $r=0.921$ — vượt xa ngưỡng $\pm0.8$ mà slide đề cập — đây là **dấu hiệu** multicollinearity rõ ràng nhất trong bảng. Các cặp còn lại đều có $|r|<0.4$, không đáng lo ngại.
<br><span class="en">The correlation between `age_wife` and `age_husband` is $r=0.921$ — far exceeding the $\pm0.8$ threshold mentioned by the slide — this is the clearest **sign** of multicollinearity in the table. All other pairs have $|r|<0.4$, which is not a concern.</span>

### 8.2 Auxiliary regression - <span class="en">Auxiliary regression</span>

Hồi quy `age_wife` lên toàn bộ regressor còn lại: $\text{age\_wife} = \beta_0+\beta_1\log(\text{income})+\beta_2\,\text{age\_husband}+\beta_3\,\text{hhsize}+\beta_4\,\text{children}+u$
<br><span class="en">Regressing `age_wife` on all other regressors: $\text{age\_wife} = \beta_0+\beta_1\log(\text{income})+\beta_2\,\text{age\_husband}+\beta_3\,\text{hhsize}+\beta_4\,\text{children}+u$</span>

| Biến<br><span class="en">Variable</span> | $b$ | SE | $t$ | $p$-value |
|---|---|---|---|---|
| (Intercept) | 3.8438 | 1.4107 | 2.725 | 0.00668 ** |
| `log(income)` | −1.1221 | 0.2509 | −4.472 | 9.76e-06 *** |
| `age_husband` | 0.9030 | 0.0195 | 46.203 | < 2e-16 *** |
| `hhsize` | 0.0639 | 0.0838 | 0.762 | 0.44622 |
| `children` | −0.0112 | 0.0154 | −0.731 | 0.46541 |

Residual SE $=4.158$ trên 465 df; $R^2=0.8548$; $R^2_{adj}=0.8536$; $F=684.4$ trên $(4,465)$ df, $p<2.2\times10^{-16}$.
<br><span class="en">Residual SE $=4.158$ on 465 df; $R^2=0.8548$; $R^2_{adj}=0.8536$; $F=684.4$ on $(4,465)$ df, $p<2.2\times10^{-16}$.</span>

$R^2=0.8548$ (>0.8, ngưỡng slide nêu) và F-test cực kỳ có ý nghĩa — cả hai đều xác nhận multicollinearity theo tiêu chí của slide. Đáng chú ý: riêng `age_husband` đã có $t=46.2$ trong auxiliary regression này — gần như một mình `age_husband` giải thích được phần lớn biến thiên của `age_wife`, đúng như trực giác ở mục 1.
<br><span class="en">$R^2=0.8548$ (>0.8, the threshold stated by the slide) and an extremely significant F-test — both confirm multicollinearity by the slide's criteria. Notably: `age_husband` alone has $t=46.2$ in this auxiliary regression — `age_husband` on its own explains most of the variation in `age_wife`, exactly matching the intuition in section 1.</span>

### 8.3 VIF - <span class="en">VIF</span>

Slide chỉ đưa ra công thức VIF cho trường hợp 2 regressor ($VIF=1/(1-r_{12}^2)$), nhưng bảng kết quả `car::vif()` ở mục 9.2 (5 regressor) cho thấy slide áp dụng công thức tổng quát hơn: $VIF_j=1/(1-R_j^2)$, với $R_j^2$ chính là $R^2$ của auxiliary regression cho biến $X_j$ — đây là cách hàm `car::vif()` trong R thực sự tính toán, và khớp với logic "auxiliary regression" mà slide đã trình bày ở mục 8.2.
<br><span class="en">The slide only gives the VIF formula for the 2-regressor case ($VIF=1/(1-r_{12}^2)$), but the `car::vif()` results table in section 9.2 (5 regressors) shows the slide applies the more general formula: $VIF_j=1/(1-R_j^2)$, where $R_j^2$ is precisely the $R^2$ of the auxiliary regression for variable $X_j$ — this is how the `car::vif()` function in R actually computes it, and matches the "auxiliary regression" logic the slide presented in section 8.2.</span>

> **Lưu ý về nguồn**: con số VIF cụ thể dưới đây **không được slide in ra trực tiếp** cho mô hình gốc (5 biến) — nó được suy ra ở đây bằng cách áp dụng công thức $VIF_j=1/(1-R_j^2)$ của chính slide vào $R^2=0.8548$ mà slide đã tính ở auxiliary regression mục 8.2. Ghi rõ để phân biệt với các con số VIF slide in trực tiếp (mục 9.2).
> <br><span class="en">**Note on the source**: the specific VIF number below is **not printed directly by the slide** for the original (5-variable) model — it is derived here by applying the slide's own formula $VIF_j=1/(1-R_j^2)$ to the $R^2=0.8548$ that the slide computed in the auxiliary regression in section 8.2. Noted explicitly to distinguish it from the VIF numbers the slide prints directly (section 9.2).</span>

$$VIF_{\text{age\_wife}}=\frac{1}{1-0.8548}=\frac{1}{0.1452}\approx 6.89$$

Với ngưỡng $VIF>5$, con số $\approx6.89$ xác nhận multicollinearity nghiêm trọng liên quan đến `age_wife` (và tương ứng, `age_husband`) — nhưng chưa vượt ngưỡng $10$ nếu dùng ngưỡng thay thế đó (xem bẫy thi #7).
<br><span class="en">With the $VIF>5$ threshold, the figure $\approx6.89$ confirms serious multicollinearity involving `age_wife` (and correspondingly, `age_husband`) — but it does not exceed the $10$ threshold if that alternative threshold is used (see exam trap #7).</span>

## 9. Giải pháp - <span class="en">Solutions</span>

### 9.1 Quy tắc chung: không phải lúc nào cũng cần xử lý - <span class="en">General rule: it doesn't always need to be fixed</span>

Slide nêu rõ **"General Rules of Thumb: DO NOT WORRY IF"**:
<br><span class="en">The slide clearly states **"General Rules of Thumb: DO NOT WORRY IF"**:</span>

- các hệ số vẫn có ý nghĩa thống kê (statistically significant), **và**
  <br><span class="en">the coefficients are still statistically significant, **and**</span>
- các hệ số vẫn đúng dấu kỳ vọng (correct expected signs).
  <br><span class="en">the coefficients still have the correct expected signs.</span>

Lý do: multicollinearity chỉ là vấn đề **thực tế** khi nó thực sự làm hỏng khả năng trả lời câu hỏi nghiên cứu (hệ số mất ý nghĩa hoặc sai dấu). Nếu hệ số vẫn có ý nghĩa và đúng dấu dù VIF cao, nghĩa là vẫn còn *đủ* biến thiên độc lập để ước lượng đáng tin cậy — "sửa" một vấn đề không thực sự gây hại (VD chỉ để hạ VIF cho đẹp) có thể tạo ra vấn đề mới (omitted variable bias, xem dưới) mà không mang lại lợi ích gì.
<br><span class="en">Reason: multicollinearity is only a **practical** problem when it actually undermines the ability to answer the research question (coefficients become insignificant or have the wrong sign). If the coefficients remain significant and correctly signed despite a high VIF, that means there is still *enough* independent variation for a reliable estimate — "fixing" a problem that isn't actually causing harm (e.g., just to make the VIF look nicer) can create a new problem (omitted variable bias, see below) without any real benefit.</span>

**Nếu cần xử lý**, slide đưa ra hai hướng, mỗi hướng kèm đánh đổi (trade-off) riêng:
<br><span class="en">**If a fix is needed**, the slide offers two directions, each with its own trade-off:</span>

### 9.2 Giải pháp 1 — Restructure mô hình (transform regressors) - <span class="en">Solution 1 — Restructure the model (transform regressors)</span>

**Ý tưởng**: tìm một cách đặc tả (specification) hoặc functional form thay thế, sao cho các regressor mới ít tương quan hơn nhưng vẫn giữ được nội dung kinh tế của mô hình gốc.
<br><span class="en">**Idea**: find an alternative specification or functional form such that the new regressors are less correlated while still preserving the economic content of the original model.</span>

**Ví dụ 1 (slide, hàm sản xuất)**: với $y=F(\text{labor},\text{land},\text{capital})$, nếu `labor` và `capital` tương quan cao qua các quan sát (VD trang trại lớn thì cả lao động lẫn vốn đều lớn), có thể chia cả hai vế cho `land`:
<br><span class="en">**Example 1 (slide, production function)**: with $y=F(\text{labor},\text{land},\text{capital})$, if `labor` and `capital` are highly correlated across observations (e.g., larger farms have both more labor and more capital), both sides can be divided by `land`:</span>

$$\frac{y}{\text{land}}=F\left(\frac{\text{labor}}{\text{land}},\ \text{land},\ \frac{\text{capital}}{\text{land}}\right)$$

Chuẩn hóa theo diện tích đất giúp giảm tương quan giữa các input, vì giờ đây các biến đo *cường độ sử dụng đầu vào trên một đơn vị đất*, không còn cùng bị chi phối bởi "quy mô trang trại" như trước.
<br><span class="en">Normalizing by land area reduces the correlation between the inputs, because the variables now measure *input intensity per unit of land*, no longer jointly driven by "farm size" as before.</span>

**Ví dụ 2 (case study, đã áp dụng thực tế)**: thay vì dùng cả `age_wife` và `age_husband` (tương quan $r=0.921$), slide tạo biến mới `age_diff = age_wife − age_husband` và thay `age_husband` bằng `age_diff` trong mô hình: $\log(\text{expense})=\beta_0+\beta_1\log(\text{income})+\beta_2\,\text{age\_wife}+\beta_3\,\text{age\_diff}+\beta_4\,\text{hhsize}+\beta_5\,\text{children}+\varepsilon$
<br><span class="en">**Example 2 (case study, actually applied)**: instead of using both `age_wife` and `age_husband` (correlation $r=0.921$), the slide creates a new variable `age_diff = age_wife − age_husband` and replaces `age_husband` with `age_diff` in the model: $\log(\text{expense})=\beta_0+\beta_1\log(\text{income})+\beta_2\,\text{age\_wife}+\beta_3\,\text{age\_diff}+\beta_4\,\text{hhsize}+\beta_5\,\text{children}+\varepsilon$</span>

| Biến<br><span class="en">Variable</span> | $b$ | SE | $t$ | $p$-value |
|---|---|---|---|---|
| (Intercept) | 0.8105 | 0.1649 | 4.916 | 1.23e-06 *** |
| `log(income)` | 0.4231 | 0.0297 | 14.240 | < 2e-16 *** |
| `age_wife` | 0.0014 | 0.0023 | 0.599 | 0.5492 |
| `age_diff` | 0.0053 | 0.0054 | 0.980 | 0.3277 |
| `hhsize` | 0.0720 | 0.0097 | 7.400 | 6.46e-13 *** |
| `children` | 0.0036 | 0.0018 | 2.007 | 0.0453 * |

Residual SE $=0.4821$; $R^2=0.3829$; $R^2_{adj}=0.3762$; $F=57.57$ — **giống hệt** mô hình gốc ở mục 5. Điều này không phải trùng hợp: `age_diff = age_wife − age_husband` là một tổ hợp tuyến tính của hai biến gốc, nên $\{\text{age\_wife},\ \text{age\_diff}\}$ trương (span) đúng cùng một không gian với $\{\text{age\_wife},\ \text{age\_husband}\}$ — mô hình dự báo *tổng thể* không đổi (cùng $\hat y$, cùng $R^2$, cùng $F$), chỉ có cách "chia" hiệu ứng cho từng hệ số riêng lẻ là thay đổi.
<br><span class="en">Residual SE $=0.4821$; $R^2=0.3829$; $R^2_{adj}=0.3762$; $F=57.57$ — **exactly identical** to the original model in section 5. This is no coincidence: `age_diff = age_wife − age_husband` is a linear combination of the two original variables, so $\{\text{age\_wife},\ \text{age\_diff}\}$ spans exactly the same space as $\{\text{age\_wife},\ \text{age\_husband}\}$ — the *overall* predictive model is unchanged (same $\hat y$, same $R^2$, same $F$), only the way the effect is "split" across the individual coefficients changes.</span>

Và `car::vif(model2)` cho kết quả:
<br><span class="en">And `car::vif(model2)` gives the result:</span>

| `log(income)` | `age_wife` | `age_diff` | `hhsize` | `children` |
|---|---|---|---|---|
| 1.175 | 1.288 | 1.068 | 1.027 | 1.094 |

Toàn bộ VIF giờ đều dưới 1.3 — multicollinearity gần như biến mất.
<br><span class="en">All VIF values are now below 1.3 — multicollinearity has almost disappeared.</span>

**Phân tích thêm (suy ra bằng đại số từ chính các hệ số slide đưa ra, không phải nguyên văn slide)**: vì $\text{age\_husband}=\text{age\_wife}-\text{age\_diff}$, thay vào mô hình gốc $\beta_2\,\text{age\_wife}+\beta_3\,\text{age\_husband}=\beta_2\,\text{age\_wife}+\beta_3(\text{age\_wife}-\text{age\_diff})=(\beta_2+\beta_3)\text{age\_wife}-\beta_3\,\text{age\_diff}$. Kiểm tra với số liệu thật: hệ số `age_wife` gốc $(0.0066)$ cộng hệ số `age_husband` gốc $(-0.0053)$ đúng bằng $0.0013\approx0.0014$ (hệ số `age_wife` mới, sai số làm tròn); và $-(-0.0053)=0.0053$ đúng bằng hệ số `age_diff` mới. Ý nghĩa kinh tế: hệ số `age_wife` **mới** không còn là "hiệu ứng của tuổi vợ, giữ tuổi chồng cố định" (điều gần như không thể ước lượng chính xác trong dữ liệu này, vì hai tuổi hiếm khi biến động độc lập) mà là **hiệu ứng khi cả hai vợ chồng cùng già đi 1 năm** (giữ khoảng cách tuổi cố định); còn hệ số `age_diff` là **hiệu ứng của việc nới rộng khoảng cách tuổi**, giữ tuổi vợ cố định. Đây là cách diễn giải lại phù hợp với chính biến thiên thực sự có trong dữ liệu — thay vì cố ước lượng một hiệu ứng mà dữ liệu gần như không có thông tin để trả lời.
<br><span class="en">**Further analysis (derived algebraically from the slide's own coefficients, not verbatim from the slide)**: since $\text{age\_husband}=\text{age\_wife}-\text{age\_diff}$, substituting into the original model $\beta_2\,\text{age\_wife}+\beta_3\,\text{age\_husband}=\beta_2\,\text{age\_wife}+\beta_3(\text{age\_wife}-\text{age\_diff})=(\beta_2+\beta_3)\text{age\_wife}-\beta_3\,\text{age\_diff}$. Checking against the actual numbers: the original `age_wife` coefficient $(0.0066)$ plus the original `age_husband` coefficient $(-0.0053)$ equals $0.0013\approx0.0014$ (the new `age_wife` coefficient, rounding error); and $-(-0.0053)=0.0053$ equals exactly the new `age_diff` coefficient. Economic meaning: the **new** `age_wife` coefficient is no longer "the effect of the wife's age, holding the husband's age fixed" (something almost impossible to estimate precisely in this data, since the two ages rarely vary independently), but rather **the effect of both spouses aging by 1 year together** (holding the age gap fixed); while the `age_diff` coefficient is **the effect of widening the age gap**, holding the wife's age fixed. This is a reinterpretation that fits the actual variation present in the data — rather than trying to estimate an effect the data has almost no information to answer.</span>

**Trade-off của giải pháp restructure**: giữ được toàn bộ thông tin gốc (không mất biến), nhưng (a) không phải lúc nào cũng tìm được một phép biến đổi vừa giảm tương quan vừa có ý nghĩa kinh tế rõ ràng để diễn giải (chia cho `land` hợp lý trong hàm sản xuất; lấy hiệu số tuổi hợp lý vì cùng đơn vị "năm" — nhưng không phải cặp biến collinear nào cũng có phép biến đổi tự nhiên tương tự); (b) hệ số sau khi biến đổi phải được diễn giải lại cẩn thận, không còn mang đúng nghĩa "giữ biến kia cố định" như hệ số gốc (xem bẫy thi #8).
<br><span class="en">**Trade-off of the restructure solution**: all of the original information is retained (no variable is lost), but (a) it isn't always possible to find a transformation that both reduces correlation and has a clear economic meaning for interpretation (dividing by `land` makes sense in a production function; taking the age difference makes sense since both are in the same "years" unit — but not every pair of collinear variables has a similarly natural transformation); (b) the transformed coefficients must be reinterpreted carefully, since they no longer carry the same "holding the other variable fixed" meaning as the original coefficients (see exam trap #8).</span>

### 9.3 Giải pháp 2 — Drop correlated regressors - <span class="en">Solution 2 — Drop correlated regressors</span>

Bỏ bớt (các) regressor tương quan cao khỏi mô hình.
<br><span class="en">Remove the highly correlated regressor(s) from the model.</span>

**Trade-off**: đơn giản, giải quyết multicollinearity ngay lập tức (giảm VIF), nhưng có rủi ro **omitted variable bias** — nếu biến bị bỏ thực sự thuộc về mô hình theo lý thuyết (tức có ảnh hưởng thật lên $y$ và tương quan với các biến còn lại), bỏ nó đi sẽ làm các hệ số còn lại bị **chệch** (biased), không chỉ mất hiệu quả (efficiency) như multicollinearity mà còn mất luôn tính đúng đắn (validity). Nói cách khác, đây là một đánh đổi giữa **bias và variance**: multicollinearity gây ra vấn đề về variance (SE lớn) — bỏ biến "chữa" variance bằng cách chấp nhận rủi ro bias, chỉ nên làm khi có lý do lý thuyết vững chắc để tin biến đó không thực sự cần thiết, không nên làm chỉ để "VIF đẹp hơn".
<br><span class="en">**Trade-off**: simple, solves multicollinearity immediately (reduces VIF), but carries the risk of **omitted variable bias** — if the dropped variable genuinely belongs in the model theoretically (i.e., truly affects $y$ and is correlated with the remaining variables), removing it will make the remaining coefficients **biased**, losing not just efficiency (as with multicollinearity) but also validity. In other words, this is a trade-off between **bias and variance**: multicollinearity causes a variance problem (large SE) — dropping a variable "cures" the variance by accepting the risk of bias, and should only be done when there is a solid theoretical reason to believe that variable isn't really needed, not just to make the "VIF look nicer".</span>

## 10. Bẫy thi (exam traps) - <span class="en">Exam traps</span>

1. **Nhầm perfect và imperfect (multicollinearity)**: nói "multicollinearity làm $X'X$ không khả nghịch" là **sai** — đó là hệ quả của **perfect** collinearity. Multicollinearity (imperfect) không làm $X'X$ mất khả nghịch, mô hình vẫn ước lượng được bình thường, chỉ SE bị phóng đại.
   <br><span class="en">**Confusing perfect and imperfect (multicollinearity)**: saying "multicollinearity makes $X'X$ non-invertible" is **wrong** — that is a consequence of **perfect** collinearity. Multicollinearity (imperfect) does not make $X'X$ non-invertible; the model still estimates normally, only the SE is inflated.</span>
2. **Nhầm đối tượng tương quan**: multicollinearity là tương quan giữa các biến **độc lập với nhau**, không phải giữa biến độc lập và biến phụ thuộc.
   <br><span class="en">**Confusing what's correlated with what**: multicollinearity is correlation **among the independent variables themselves**, not between an independent variable and the dependent variable.</span>
3. Nghĩ multicollinearity làm hệ số OLS bị chệch (biased)/mất consistency — sai. OLS vẫn unbiased/consistent dưới multicollinearity (miễn A1–A3 vẫn giữ); multicollinearity chỉ làm mất **efficiency** (SE lớn hơn). Dễ nhầm với omitted variable bias hoặc endogeneity — những vấn đề đó mới thực sự gây chệch.
   <br><span class="en">Thinking multicollinearity makes the OLS coefficients biased or inconsistent — wrong. OLS remains unbiased/consistent under multicollinearity (as long as A1–A3 still hold); multicollinearity only causes a loss of **efficiency** (larger SE). Easily confused with omitted variable bias or endogeneity — those are the problems that actually cause bias.</span>
4. Coi tương quan cặp cao/thấp là **bằng chứng dứt khoát** có/không có multicollinearity — slide chỉ coi đây là "dấu hiệu" (sign), không phải "xác nhận" (confirmation). Tương quan cặp thấp **không đảm bảo** không có multicollinearity (có thể multicollinear đa biến — 3+ biến cùng phụ thuộc lẫn nhau mà không cặp nào riêng lẻ lộ ra tương quan cao).
   <br><span class="en">Treating a high/low pairwise correlation as **conclusive evidence** of the presence/absence of multicollinearity — the slide only treats this as a "sign," not a "confirmation." A low pairwise correlation **does not guarantee** the absence of multicollinearity (it could be multivariate multicollinearity — 3+ variables jointly dependent on each other without any single pair individually showing a high correlation).</span>
5. "Xử lý" multicollinearity ngay cả khi hệ số vẫn significant và đúng dấu kỳ vọng — không cần thiết, đi ngược lại "General Rule of Thumb" của slide (mục 9.1).
   <br><span class="en">"Fixing" multicollinearity even when the coefficients are still significant and correctly signed — unnecessary, and goes against the slide's "General Rule of Thumb" (section 9.1).</span>
6. Bỏ biến để giảm multicollinearity mà **không cân nhắc omitted variable bias** — đây không phải một "sửa lỗi miễn phí" mà là một đánh đổi bias-variance thực sự.
   <br><span class="en">Dropping a variable to reduce multicollinearity **without weighing omitted variable bias** — this is not a "free fix" but a genuine bias-variance trade-off.</span>
7. Nhầm lẫn ngưỡng VIF: slide dùng cả "$VIF>5$" và "$VIF>5$ (hoặc 10)" ở hai chỗ khác nhau, không chốt một ngưỡng duy nhất — khi làm bài luôn nêu rõ đang dùng ngưỡng nào, vì cùng một VIF (VD $\approx6.89$ trong case study) có thể "nghiêm trọng" theo ngưỡng 5 nhưng "chưa nghiêm trọng" theo ngưỡng 10.
   <br><span class="en">Confusing the VIF threshold: the slide uses both "$VIF>5$" and "$VIF>5$ (or 10)" in two different places, without settling on a single threshold — when answering exam questions, always state clearly which threshold is being used, since the same VIF (e.g., $\approx6.89$ in the case study) can be "serious" under the threshold of 5 but "not yet serious" under the threshold of 10.</span>
8. Sau khi restructure mô hình (VD đổi `age_husband` → `age_diff`), quên diễn giải lại hệ số: hệ số `age_wife` **mới** không còn nghĩa là "hiệu ứng tuổi vợ, giữ tuổi chồng cố định" — vì dữ liệu gần như không có biến thiên độc lập để trả lời câu hỏi đó — mà là "hiệu ứng khi cả hai vợ chồng cùng già đi".
   <br><span class="en">After restructuring the model (e.g., replacing `age_husband` → `age_diff`), forgetting to reinterpret the coefficients: the **new** `age_wife` coefficient no longer means "the effect of the wife's age, holding the husband's age fixed" — since the data has almost no independent variation to answer that question — but rather "the effect of both spouses aging together".</span>
9. Nhầm $R^2$ của **mô hình chính** (đo độ khớp với $y$) với $R^2$ của **auxiliary regression** (đo mức một $X_j$ bị các $X$ còn lại giải thích). Trong case study, $R^2$ mô hình chính chỉ 0.38 (không cao) nhưng $R^2$ của auxiliary regression cho `age_wife` lên tới 0.85 — chỉ con số thứ hai mới liên quan trực tiếp đến việc xác nhận multicollinearity.
   <br><span class="en">Confusing the $R^2$ of the **main model** (measuring fit to $y$) with the $R^2$ of the **auxiliary regression** (measuring how much one $X_j$ is explained by the remaining $X$'s). In the case study, the main model's $R^2$ is only 0.38 (not high), but the auxiliary regression's $R^2$ for `age_wife` reaches 0.85 — only the second number is directly relevant to confirming multicollinearity.</span>
10. Dùng ngôn ngữ "chứng minh" (prove) khi nói về VIF/correlation matrix/auxiliary regression — đúng ra chỉ nên nói các công cụ này "xác nhận" hoặc "gợi ý" multicollinearity, nhất quán với nguyên tắc ngôn ngữ suy luận thống kê đã nêu ở [[concepts/linear-regression-model]] mục 7.1.
    <br><span class="en">Using the language of "proving" when talking about VIF/correlation matrix/auxiliary regression — these tools should properly only be said to "confirm" or "suggest" multicollinearity, consistent with the statistical-inference language convention stated in [[concepts/linear-regression-model]] section 7.1.</span>

## 11. Kết nối với phần còn lại của khóa học - <span class="en">Connections to the rest of the course</span>

- Multicollinearity là trường hợp "gần vi phạm" **A2 (Full rank)** của [[concepts/linear-regression-model]] — khác hẳn với perfect collinearity (vi phạm A2 hoàn toàn, khiến $b$ unidentifiable).
  <br><span class="en">Multicollinearity is a "near-violation" case of **A2 (Full rank)** of [[concepts/linear-regression-model]] — quite unlike perfect collinearity (a complete violation of A2, which makes $b$ unidentifiable).</span>
- Khác với [[concepts/heteroskedasticity]] (vi phạm **A4**): multicollinearity không làm mất consistency, chỉ làm mất efficiency (SE lớn hơn nhưng công thức VCV $\sigma^2(X'X)^{-1}$ về nguyên tắc vẫn đúng dạng); heteroskedasticity thì làm chính công thức VCV chuẩn đó **sai hoàn toàn**, đòi hỏi robust SE — hai cơ chế hoàn toàn khác nhau dù cả hai đều "chỉ ảnh hưởng SE, không gây bias" ở dạng cơ bản nhất.
  <br><span class="en">Unlike [[concepts/heteroskedasticity]] (a violation of **A4**): multicollinearity does not cause a loss of consistency, only a loss of efficiency (larger SE, but the VCV formula $\sigma^2(X'X)^{-1}$ is in principle still the correct form); heteroskedasticity, on the other hand, makes that standard VCV formula itself **entirely wrong**, requiring robust SE — two completely different mechanisms, even though both, in their most basic form, "only affect SE, without causing bias".</span>
- Khác với **A3 (Exogeneity)** bị vi phạm ([[concepts/endogeneity-iv-regression]]): multicollinearity không gây bias/inconsistency; endogeneity thì gây bias. Một hệ số "sai dấu kỳ vọng" có thể do multicollinearity **hoặc** do omitted-variable/endogeneity — cần dùng đúng bộ công cụ chẩn đoán tương ứng (VIF/correlation matrix cho multicollinearity; các kiểm định riêng cho endogeneity) trước khi kết luận nguyên nhân.
  <br><span class="en">Unlike a violation of **A3 (Exogeneity)** ([[concepts/endogeneity-iv-regression]]): multicollinearity does not cause bias/inconsistency; endogeneity does cause bias. A coefficient with the "wrong expected sign" could be due to multicollinearity **or** to an omitted variable/endogeneity — the correct corresponding diagnostic toolkit must be used (VIF/correlation matrix for multicollinearity; separate tests for endogeneity) before concluding the cause.</span>
- Nguồn gốc thứ tư của multicollinearity ("mathematical derivation" — một biến là hàm của biến khác, VD biến và bình phương của nó) liên hệ trực tiếp tới [[concepts/functional-forms]] dạng quadratic/polynomial.
  <br><span class="en">The fourth source of multicollinearity ("mathematical derivation" — one variable is a function of another, e.g., a variable and its square) connects directly to the quadratic/polynomial form in [[concepts/functional-forms]].</span>
- Cơ chế "SE lớn → t-statistic nhỏ → khó bác bỏ $H_0$" ở mục 6 là ứng dụng trực tiếp khung t-test đã học ở [[concepts/linear-regression-model]] mục 7 — case study ở trang này (`age_wife`, `age_husband` đều $|t|<2$) là một minh họa số cụ thể cho việc SE bị phóng đại làm giảm power của kiểm định, dẫn đến nguy cơ Type II error.
  <br><span class="en">The "large SE → small t-statistic → hard to reject $H_0$" mechanism in section 6 is a direct application of the t-test framework learned in [[concepts/linear-regression-model]] section 7 — the case study on this page (`age_wife`, `age_husband` both with $|t|<2$) is a concrete numerical illustration of how an inflated SE reduces the power of a test, leading to the risk of a Type II error.</span>
