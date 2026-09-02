---
title: "Binary Response Models (LPM, Logit, Probit)"
type: concept
status: mature
tags: [binary-response, logit, probit, limited-dependent-variable, marginal-effects]
sources: ["[[sources/slides-7-binary-response-models]]", "[[sources/slides-310-binary-response-models-logit-probit]]"]
related: ["[[concepts/linear-regression-model]]", "[[concepts/multinomial-logit-model]]", "[[concepts/ordinal-response-models]]"]
updated: 2026-08-29
---

> **Cách đọc trang này**: đây là trang mở đầu **Part 2: Models for Limited Dependent Variables** — phần còn lại của khóa học (Topic 8–11) đều là biến thể của khung ML/latent-variable dựng ở đây.
> <br><span class="en">**How to read this page**: this is the opening page of **Part 2: Models for Limited Dependent Variables** — the rest of the course (Topic 8–11) are all variants of the ML/latent-variable framework built here.</span>
> Nếu [[concepts/linear-regression-model]] là "luật chơi" khi $y$ liên tục, trang này là "luật chơi" khi $y$ chỉ có thể là 0 hoặc 1.
> <br><span class="en">If [[concepts/linear-regression-model]] is the "rulebook" for continuous $y$, this page is the "rulebook" for when $y$ can only be 0 or 1.</span>
> Hai bộ slide dạy cùng một lý thuyết bằng hai bộ dữ liệu khác nhau: `slides-7-iu.pdf` (48 trang, ví dụ quyết định tiêm vaccine COVID-19, có số liệu R thật ở trang 7–45) và `slides-310-iu.pdf` (39 trang, ví dụ dùng ví điện tử — e-wallet, chủ yếu văn bản/công thức, phần R-output là ảnh chưa trích xuất được số cụ thể).
> <br><span class="en">Two slide decks teach the same theory with two different datasets: `slides-7-iu.pdf` (48 pages, COVID-19 vaccine decision example, with real R output on pages 7–45) and `slides-310-iu.pdf` (39 pages, e-wallet example, mostly text/formulas, with the R-output section as images from which concrete numbers could not be extracted).</span>
> Toàn bộ ví dụ số trong trang này lấy từ bộ dữ liệu vaccine của `slides-7`; bộ e-wallet chỉ dùng để minh họa rằng lý thuyết áp dụng được cho bất kỳ outcome nhị phân nào.
> <br><span class="en">Every numerical example on this page is drawn from the `slides-7` vaccine dataset; the e-wallet dataset is used only to illustrate that the theory applies to any binary outcome.</span>

## 1. Vấn đề gốc: khi biến phụ thuộc chỉ có thể là 0 hoặc 1 - <span class="en">The original problem: when the dependent variable can only be 0 or 1</span>

Rất nhiều câu hỏi kinh tế không có outcome là một con số liên tục, mà là một **lựa chọn nhị phân** (binary choice) — có/không, xảy ra/không xảy ra.
<br><span class="en">Many economic questions do not have a continuous number as the outcome, but rather a **binary choice** — yes/no, occurs/does not occur.</span>
Slide liệt kê một loạt ví dụ:
<br><span class="en">The slide lists a series of examples:</span>

- Đơn xin vay có được duyệt hay không.
  <br><span class="en">Whether a loan application is approved or not.</span>
- Người vay có trả được nợ hay không.
  <br><span class="en">Whether a borrower can repay the debt or not.</span>
- Một người có sở hữu thẻ tín dụng hay không.
  <br><span class="en">Whether a person owns a credit card or not.</span>
- (Ví dụ xuyên suốt trang này) Một người có quyết định tiêm vaccine COVID-19 hay không (`dself`).
  <br><span class="en">(The running example throughout this page) Whether a person decides to get a COVID-19 vaccine or not (`dself`).</span>
- (Ví dụ của bộ slide song song) Một người có dùng ví điện tử hay không (`ewallet`).
  <br><span class="en">(The example from the parallel slide deck) Whether a person uses an e-wallet or not (`ewallet`).</span>

Gọi biến này là $y_i \in \{0,1\}$. Câu hỏi tự nhiên: **tại sao không hồi quy OLS trực tiếp** $y = \beta X + u$ như [[concepts/linear-regression-model]] đã làm?
<br><span class="en">Call this variable $y_i \in \{0,1\}$. The natural question: **why not just run OLS directly** on $y = \beta X + u$ the way [[concepts/linear-regression-model]] does?</span>

Vấn đề nằm ở chính bản chất của $y$. Về mặt lý thuyết xác suất, khi $y$ nhị phân, giá trị kỳ vọng của nó **chính là một xác suất**:
<br><span class="en">The problem lies in the very nature of $y$. In probability theory, when $y$ is binary, its expected value **is itself a probability**:</span>

$$E(y_i|X_i) = 1\cdot Pr(y_i=1|X_i) + 0\cdot Pr(y_i=0|X_i) = Pr(y_i=1|X_i)$$

Nói cách khác, hồi quy $y$ lên $X$ về bản chất là đang cố mô hình hóa $Pr(y=1|X)$ — và xác suất thì **luôn bị chặn trong khoảng [0,1]**. Nhưng vế phải của một phương trình hồi quy tuyến tính $X\beta$ thì **không bị chặn** — nó có thể chạy từ $-\infty$ đến $+\infty$ tùy giá trị $X$. Đây chính là mâu thuẫn nền tảng mà toàn bộ Part 2 của khóa học tồn tại để giải quyết: cần một hàm số biến đổi $X\beta$ (không giới hạn) thành một con số luôn nằm trong [0,1] (một xác suất hợp lệ).
<br><span class="en">In other words, regressing $y$ on $X$ is essentially an attempt to model $Pr(y=1|X)$ — and a probability is **always bounded within [0,1]**. But the right-hand side of a linear regression equation $X\beta$ is **unbounded** — it can range from $-\infty$ to $+\infty$ depending on the value of $X$. This is precisely the foundational contradiction that all of Part 2 of the course exists to resolve: we need a function that transforms $X\beta$ (unbounded) into a number that always lies in [0,1] (a valid probability).</span>

Slide hình thức hóa vấn đề bằng một hàm mật độ chung:
<br><span class="en">The slide formalizes the problem with a general density function:</span>

$$Pr(Y_i=1) = F(X_i\beta), \qquad Pr(Y_i=0) = 1-F(X_i\beta)$$

$F(\cdot)$ ở đây gọi là **hàm liên kết** (link function) — nhiệm vụ của nó chỉ đơn giản là "ép" $X\beta$ vào trong [0,1]. Khác biệt giữa LPM, Logit, và Probit **chỉ nằm ở việc chọn $F$ là hàm gì** — đây là ý tưởng cần nắm trước khi đi vào từng mô hình cụ thể.
<br><span class="en">$F(\cdot)$ here is called the **link function** — its job is simply to "squeeze" $X\beta$ into [0,1]. The difference between LPM, Logit, and Probit **lies purely in the choice of what function $F$ is** — this is the idea to grasp before diving into each specific model.</span>

## 2. Bộ dữ liệu minh họa - <span class="en">Illustrative datasets</span>

### 2.1 COVID-19 vaccine (slides-7, dùng cho mọi ví dụ số trong trang này) - <span class="en">COVID-19 vaccine (slides-7, used for every numerical example on this page)</span>

Khảo sát 377 người tại TP.HCM năm 2020 (dữ liệu công khai bởi EEPSEA), hỏi liệu họ có quyết định tiêm một loại vaccine COVID-19 giả định hay không.
<br><span class="en">A survey of 377 people in Ho Chi Minh City in 2020 (data made public by EEPSEA), asking whether they would decide to get a hypothetical COVID-19 vaccine.</span>

| Biến / Variable | Ý nghĩa / Meaning |
|---|---|
| `dself` (dep var) | 1 = quyết định tiêm cho bản thân / 1 = decides to get vaccinated for themselves |
| `efficacy80` | 1 = hiệu quả vaccine 80%, 0 = 50% / 1 = vaccine efficacy 80%, 0 = 50% |
| `duration3` | 1 = thời gian miễn dịch 3 năm, 0 = 1 năm / 1 = immunity duration 3 years, 0 = 1 year |
| `priceUS` (USD) | giá vaccine (2 liều) / vaccine price (2 doses) |
| `pbenefit` | 1 = được cung cấp thông tin về ngoại tác (externality) của việc tiêm vaccine / 1 = was given information about the externality of vaccination |
| `hhincomeUS` (USD/tháng) | tổng thu nhập hộ gia đình / total household income |
| `hhsize` | quy mô hộ gia đình / household size |
| `age` (năm) | tuổi người trả lời / respondent's age |
| `edu` (categorical 1–6) | trình độ học vấn / education level |
| `male` | 1 = nam / 1 = male |
| `risk` (ordinal 1–5) | mức độ cảm nhận rủi ro nhiễm COVID-19: "Very unlikely" → "Very likely" / perceived risk of COVID-19 infection: "Very unlikely" → "Very likely" |

### 2.2 E-wallet (slides-310, chỉ dùng minh họa khái niệm, không có số liệu R trích xuất được) - <span class="en">E-wallet (slides-310, used only to illustrate the concept, no extractable R output)</span>

| Biến / Variable | Ý nghĩa / Meaning |
|---|---|
| `ewallet` (dep var) | 1 = có dùng ví điện tử / 1 = uses an e-wallet |
| `income` (triệu VNĐ/tháng) | thu nhập khả dụng hàng tháng / monthly disposable income |
| `age`, `schooling` (năm) | tuổi, số năm đi học / age, years of schooling |
| `male` | 1 = nam / 1 = male |
| `risklover` | 1 = tự nhận là người ưa thích rủi ro / 1 = self-identifies as a risk lover |
| `freq` → `weekly`, `daily` (dummy) | tần suất mua sắm trực tuyến (nền: "monthly" — dưới hàng tuần) / frequency of online shopping (base: "monthly" — less than weekly) |

Hai bộ dữ liệu khác nhau hoàn toàn về bối cảnh, nhưng **cùng một cấu trúc bài toán**: một outcome 0/1 cần giải thích bằng một tập biến độc lập hỗn hợp (liên tục, dummy, categorical) — đúng dạng bài mà LPM/Logit/Probit được thiết kế để xử lý.
<br><span class="en">The two datasets differ completely in context, but share **the same problem structure**: a 0/1 outcome to be explained by a mixed set of independent variables (continuous, dummy, categorical) — exactly the type of problem LPM/Logit/Probit are designed to handle.</span>

## 3. Khung tổng quát: các lựa chọn cho $F(X\beta)$ - <span class="en">General framework: choices for $F(X\beta)$</span>

Slide liệt kê 5 lựa chọn hàm liên kết (3 lựa chọn đầu là trọng tâm khóa học):
<br><span class="en">The slide lists 5 choices of link function (the first 3 are the focus of the course):</span>

| Mô hình / Model | $F(X_i,\beta)$ |
|---|---|
| **Linear Probability Model (LPM)** | $X_i\beta$ |
| **Logit** | $\Lambda(X_i\beta) = \dfrac{1}{1+e^{-X_i\beta}}$ |
| **Probit** | $\Phi(X_i\beta) = \displaystyle\int_{-\infty}^{X_i\beta}\phi(t)\,dt = \int_{-\infty}^{X_i\beta}\frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{1}{2}\left(\frac{t-\mu}{\sigma}\right)^2}dt$ |
| Gumbel | $e^{-e^{-X_i\beta}}$ |
| Complementary log-log | $1-e^{-e^{X_i\beta}}$ |

"Và nhiều biến thể khác" — slide không đi sâu Gumbel/cloglog, chỉ liệt kê để cho thấy LPM/Logit/Probit là 3 trong nhiều lựa chọn khả dĩ, không phải toàn bộ vũ trụ các mô hình binary response.
<br><span class="en">"And many other variants" — the slide does not go into depth on Gumbel/cloglog, only listing them to show that LPM/Logit/Probit are 3 out of many possible choices, not the entire universe of binary response models.</span>

## 4. Linear Probability Model (LPM) - <span class="en">Linear Probability Model (LPM)</span>

### 4.1 Trực giác - <span class="en">Intuition</span>

Cách "dễ" nhất để chọn $F$: đặt $F(X\beta)=X\beta$ — tức là **không biến đổi gì cả**, cứ hồi quy OLS bình thường với $y$ (0/1) làm biến phụ thuộc:
<br><span class="en">The "easiest" way to choose $F$: set $F(X\beta)=X\beta$ — that is, **no transformation at all**, simply run an ordinary OLS regression with $y$ (0/1) as the dependent variable:</span>

$$Pr(y_i=1) = X_i\beta = \beta_0+\beta_1X_{1i}+\cdots$$

Vì $y_i=1$ trùng với $Pr(y_i=1)=1$, ta có thể dùng thẳng $y$ quan sát được làm biến phụ thuộc và chạy OLS như bình thường — về mặt cơ học, không có gì khác [[concepts/linear-regression-model]]. Nhưng **lưu ý quan trọng**: vế trái về bản chất là một xác suất, không phải bản thân $y$ — điều này quyết định cách đọc hệ số (mục 4.3) và cũng là gốc rễ của mọi vấn đề của LPM.
<br><span class="en">Since $y_i=1$ coincides with $Pr(y_i=1)=1$, we can use the observed $y$ directly as the dependent variable and run OLS as usual — mechanically, nothing differs from [[concepts/linear-regression-model]]. But **an important note**: the left-hand side is fundamentally a probability, not $y$ itself — this determines how the coefficients are read (section 4.3) and is also the root of every problem LPM has.</span>

### 4.2 Ví dụ trực quan bằng dữ liệu vaccine - <span class="en">A visual example using the vaccine data</span>

Giả sử ước lượng LPM cho `dself` theo `priceUS` (giữ các biến khác cố định ở mức tham chiếu). Vì LPM ép $Pr(dself=1)$ tuyến tính theo giá, đường hồi quy là **một đường thẳng**, không có điểm uốn, không có giới hạn tự nhiên.
<br><span class="en">Suppose we estimate an LPM for `dself` on `priceUS` (holding the other variables fixed at their reference levels). Because LPM forces $Pr(dself=1)$ to be linear in price, the regression line is **a straight line**, with no inflection point and no natural bound.</span>
Nếu hệ số của `priceUS` âm và đủ dốc (giá càng cao càng ít người muốn tiêm), thì với một mức giá đủ cao (ví dụ 300–500 USD, ngoài phạm vi dữ liệu quan sát nhưng vẫn là một giá trị $X$ hợp lệ để đưa vào công thức), đường thẳng này **hoàn toàn có thể đi xuống dưới 0** — nghĩa là mô hình "dự đoán" xác suất tiêm vaccine là *âm*, một điều vô nghĩa về mặt logic (xác suất âm không tồn tại).
<br><span class="en">If the coefficient on `priceUS` is negative and steep enough (the higher the price, the fewer people want to get vaccinated), then at a sufficiently high price (e.g. 300–500 USD, outside the observed data range but still a valid $X$ value to plug into the formula), this straight line **can perfectly well go below 0** — meaning the model "predicts" a *negative* probability of getting vaccinated, which is logically meaningless (negative probability does not exist).</span>
Tương tự, với giá rất thấp (âm, hoặc các biến kiểm soát ở mức cực đoan), dự đoán có thể vượt quá 1. Đây chính xác là nhược điểm #1 bên dưới, và nó không phải một tình huống "hiếm gặp lý thuyết" — nó xảy ra bất cứ khi nào $X$ đủ xa khỏi vùng trung tâm của dữ liệu mẫu.
<br><span class="en">Similarly, at a very low price (negative, or with control variables at extreme levels), the prediction can exceed 1. This is exactly disadvantage #1 below, and it is not a "theoretically rare" situation — it happens whenever $X$ is far enough from the central region of the sample data.</span>

### 4.3 Diễn giải hệ số - <span class="en">Interpreting the coefficients</span>

Vì vế trái là $Pr(y=1)$, hệ số $\beta_j$ trong LPM được đọc giống hệt LRM thường: $\beta_j$ là mức thay đổi của **xác suất** $y=1$ khi $X_j$ tăng 1 đơn vị, giữ các biến khác không đổi — và quan trọng nhất, **mức thay đổi này là hằng số**, không phụ thuộc giá trị ban đầu của $X_j$ hay của bất kỳ biến nào khác. Đây là điểm LPM khác biệt gốc rễ với Logit/Probit (xem mục 9).
<br><span class="en">Since the left-hand side is $Pr(y=1)$, the coefficient $\beta_j$ in LPM is read exactly like an ordinary LRM: $\beta_j$ is the change in the **probability** that $y=1$ when $X_j$ increases by 1 unit, holding the other variables constant — and most importantly, **this change is constant**, independent of the starting value of $X_j$ or of any other variable. This is the point where LPM differs fundamentally from Logit/Probit (see section 9).</span>

### 4.4 Bốn nhược điểm của LPM — và tại sao mỗi nhược điểm là vấn đề thực tế - <span class="en">The four drawbacks of LPM — and why each one is a real problem</span>

Slide liệt kê đúng 4 nhược điểm; dưới đây giải thích **tại sao** từng cái quan trọng, không chỉ liệt kê tên:
<br><span class="en">The slide lists exactly 4 drawbacks; below explains **why** each one matters, not just names them:</span>

1. **Giá trị dự đoán $Pr(y=1)$ có thể nằm ngoài [0,1].** Đây không phải lỗi thẩm mỹ — nó phá vỡ chính định nghĩa của một xác suất. Một nhà hoạch định chính sách nhìn thấy "xác suất tiêm vaccine là −8%" hoặc "112%" sẽ không thể diễn giải được kết quả, và không thể dùng con số đó cho bất kỳ tính toán xác suất tiếp theo nào (kỳ vọng, mô phỏng…).
   <br><span class="en">**The predicted value $Pr(y=1)$ can fall outside [0,1].** This is not a cosmetic flaw — it breaks the very definition of a probability. A policymaker seeing "the probability of getting vaccinated is −8%" or "112%" cannot interpret the result, and cannot use that number for any subsequent probability calculation (expectation, simulation…).</span>

2. **LPM giả định $Pr(y=1)$ tương quan tuyến tính với $X$ bất kể giá trị ban đầu của $X$.** Về mặt trực giác kinh tế, điều này thường phi lý: khi giá vaccine đã rất thấp (gần 0 USD), tăng thêm 1 USD hầu như không đổi quyết định của ai — hầu hết những người sẵn lòng tiêm đã "chốt" quyết định rồi. Ngược lại, khi giá đang ở vùng mà người ta còn đang "phân vân" (xác suất gần 50%), tăng 1 USD có thể lay chuyển quyết định của rất nhiều người. LPM buộc mức độ nhạy cảm này phải **giống hệt nhau ở mọi mức giá** — một giả định không tự nhiên. (Mục 9 sẽ định lượng chính xác sự khác biệt này bằng số liệu thật.)
   <br><span class="en">**LPM assumes $Pr(y=1)$ is linearly related to $X$ regardless of the starting value of $X$.** Economically, this is often implausible: when the vaccine price is already very low (near 0 USD), an additional 1 USD barely changes anyone's decision — most people willing to get vaccinated have already "locked in" their decision. Conversely, when the price is in the range where people are still "on the fence" (probability near 50%), a 1 USD increase can sway many people's decisions. LPM forces this sensitivity to be **identical at every price level** — an unnatural assumption. (Section 9 will quantify this difference precisely with real data.)</span>

3. **Sai số $\varepsilon$ có phương sai không đồng nhất (heteroskedastic) một cách "bẩm sinh".** Vì $y$ chỉ nhận 2 giá trị, phần dư $\varepsilon_i = y_i - X_i\beta$ cũng chỉ nhận 2 giá trị có thể: $1-X_i\beta$ (khi $y_i=1$) hoặc $-X_i\beta$ (khi $y_i=0$). Có thể chứng minh $Var(\varepsilon_i|X_i) = X_i\beta(1-X_i\beta)$ — phương sai này **luôn thay đổi theo $X_i$**, không phải hằng số, tức LPM luôn vi phạm giả định A4 (homoskedasticity) của [[concepts/linear-regression-model]]. Hệ quả trực tiếp: standard error tính theo công thức OLS thường sai, mọi t-test/F-test dựa trên các SE đó **không đáng tin cậy** — xem [[concepts/heteroskedasticity]] để hiểu cơ chế và cách vá (robust SE).
   <br><span class="en">**The error $\varepsilon$ has "inherently" heteroskedastic variance.** Because $y$ takes only 2 values, the residual $\varepsilon_i = y_i - X_i\beta$ also takes only 2 possible values: $1-X_i\beta$ (when $y_i=1$) or $-X_i\beta$ (when $y_i=0$). It can be shown that $Var(\varepsilon_i|X_i) = X_i\beta(1-X_i\beta)$ — this variance **always changes with $X_i$**, it is not constant, meaning LPM always violates assumption A4 (homoskedasticity) of [[concepts/linear-regression-model]]. Direct consequence: the standard errors computed from the usual OLS formula are typically wrong, and every t-test/F-test based on those SEs is **unreliable** — see [[concepts/heteroskedasticity]] for the mechanism and the fix (robust SE).</span>

4. **Vi phạm giả định $\varepsilon$ phân phối chuẩn (A5).** Vì phần dư chỉ có 2 giá trị rời rạc như trên, nó rõ ràng không thể tuân theo phân phối chuẩn liên tục. Ở mẫu nhỏ, điều này làm suy luận thống kê chính xác (exact inference — t-test, F-test dựa trên phân phối t/F) mất cơ sở lý thuyết.
   <br><span class="en">**Violates the assumption that $\varepsilon$ is normally distributed (A5).** Since the residual only takes the 2 discrete values above, it clearly cannot follow a continuous normal distribution. In small samples, this strips exact inference (t-test, F-test based on the t/F distribution) of its theoretical basis.</span>

**Điểm mấu chốt cần nhớ**: 4 nhược điểm này là lý do khóa học chuyển sang Logit/Probit — không phải vì LPM "sai" theo nghĩa toán học (OLS vẫn cho ra một $b$ hợp lệ), mà vì bản chất nhị phân của $y$ khiến các giả định nền tảng của OLS ([[concepts/linear-regression-model]] mục 4) bị vi phạm một cách **có hệ thống**, không phải ngẫu nhiên.
<br><span class="en">**Key point to remember**: these 4 drawbacks are why the course moves on to Logit/Probit — not because LPM is "wrong" in a mathematical sense (OLS still produces a valid $b$), but because the binary nature of $y$ causes the foundational assumptions of OLS ([[concepts/linear-regression-model]] section 4) to be violated **systematically**, not randomly.</span>

## 5. Mô hình Logit - <span class="en">The Logit model</span>

### 5.1 Trực giác: tại sao dùng hàm logistic - <span class="en">Intuition: why use the logistic function</span>

Vấn đề cốt lõi của LPM là dùng một đường thẳng để mô hình hóa một đại lượng bị chặn trong [0,1]. Giải pháp tự nhiên: dùng một hàm số có hình dạng **chữ S** (sigmoid) — phẳng gần 0 khi $X\beta$ rất nhỏ (rất âm), phẳng gần 1 khi $X\beta$ rất lớn (rất dương), và dốc nhất ở vùng giữa. Hàm **logistic** là một lựa chọn kinh điển cho hình dạng này:
<br><span class="en">The core problem with LPM is using a straight line to model a quantity bounded in [0,1]. The natural solution: use a function shaped like an **S** (sigmoid) — flat near 0 when $X\beta$ is very small (very negative), flat near 1 when $X\beta$ is very large (very positive), and steepest in the middle region. The **logistic** function is a classic choice for this shape:</span>

$$Pr(Y_i=1) = P_i = \frac{1}{1+e^{-\beta X_i}}$$

Vì $-\infty < X_i\beta < +\infty$ nhưng số mũ $e^{-\beta X_i}$ luôn dương, mẫu số $1+e^{-\beta X_i}$ luôn lớn hơn 1, nên $P_i$ **luôn nằm chặt trong khoảng (0,1)** — không bao giờ chạm 0 hay 1, và không bao giờ vượt ra ngoài, **bất kể $X\beta$ lớn/nhỏ đến đâu**. Đây chính là cách Logit khắc phục triệt để nhược điểm #1 của LPM: không phải bằng cách "cắt" giá trị dự đoán ở [0,1] một cách gượng ép, mà bằng cách chọn một hàm số mà toàn bộ miền giá trị của nó *tự động* nằm trong [0,1].
<br><span class="en">Since $-\infty < X_i\beta < +\infty$ but the exponent $e^{-\beta X_i}$ is always positive, the denominator $1+e^{-\beta X_i}$ is always greater than 1, so $P_i$ **always lies strictly within (0,1)** — never touching 0 or 1, and never going outside that range, **no matter how large or small $X\beta$ is**. This is precisely how Logit thoroughly fixes drawback #1 of LPM: not by forcibly "clipping" the predicted value to [0,1], but by choosing a function whose entire range *automatically* lies within [0,1].</span>

### 5.2 Derivation: từ odds ratio đến log-odds - <span class="en">Derivation: from odds ratio to log-odds</span>

Đây là phần kỹ thuật cần nắm để hiểu tại sao Logit "khác" LPM ở bản chất, không chỉ ở hình dạng đồ thị. Xuất phát từ $P_i = \dfrac{1}{1+e^{-\beta X_i}}$, ta có xác suất "không xảy ra":
<br><span class="en">This is the technical part needed to understand why Logit "differs" from LPM in substance, not just in graph shape. Starting from $P_i = \dfrac{1}{1+e^{-\beta X_i}}$, we have the "does not occur" probability:</span>

$$1-P_i = \frac{e^{-\beta X_i}}{1+e^{-\beta X_i}}$$

**Odds ratio** (tỷ lệ cược) là khái niệm quen thuộc trong cá cược: tỷ lệ giữa xác suất "xảy ra" và xác suất "không xảy ra". Ví dụ, odds = 3 nghĩa là "xảy ra" có khả năng gấp 3 lần "không xảy ra" ($P=0.75$, $1-P=0.25$, $0.75/0.25=3$). Với Logit:
<br><span class="en">**Odds ratio** is a concept familiar from betting: the ratio between the probability of "occurring" and the probability of "not occurring." For example, odds = 3 means "occurring" is 3 times as likely as "not occurring" ($P=0.75$, $1-P=0.25$, $0.75/0.25=3$). For Logit:</span>

$$\frac{P_i}{1-P_i} = \frac{1/(1+e^{-\beta X_i})}{e^{-\beta X_i}/(1+e^{-\beta X_i})} = \frac{1}{e^{-\beta X_i}} = e^{\beta X_i}$$

Lấy log hai vế, ta được **logit** (log-odds):
<br><span class="en">Taking the log of both sides gives the **logit** (log-odds):</span>

$$\ln\left(\frac{P_i}{1-P_i}\right) = \beta X_i$$

Đây là điểm khác biệt cốt lõi: **LPM giả định $P_i$ tuyến tính với $X_i$; Logit giả định log-odds (không phải $P_i$) tuyến tính với $X_i$**. Vì $\ln(P/(1-P))$ là một phép biến đổi phi tuyến của $P$, bản thân $P_i$ vẫn thay đổi phi tuyến theo $X_i$ dù logit của nó thay đổi tuyến tính — đây chính là nguồn gốc của "marginal effect không hằng số" ở mục 9.
<br><span class="en">This is the core distinction: **LPM assumes $P_i$ is linear in $X_i$; Logit assumes the log-odds (not $P_i$) is linear in $X_i$**. Since $\ln(P/(1-P))$ is a nonlinear transformation of $P$, $P_i$ itself still changes nonlinearly with $X_i$ even though its logit changes linearly — this is precisely the origin of the "non-constant marginal effect" in section 9.</span>

### 5.3 Tính chất của mô hình Logit - <span class="en">Properties of the Logit model</span>

- $P_i$ luôn nằm trong (0,1), trong khi logit $L_i=\ln(P_i/(1-P_i))$ chạy từ $-\infty$ đến $+\infty$.
  <br><span class="en">$P_i$ always lies within (0,1), while the logit $L_i=\ln(P_i/(1-P_i))$ ranges from $-\infty$ to $+\infty$.</span>
- $L_i$ là hàm tuyến tính của $X_i$, nhưng $P_i$ thì **không** — đây là hệ quả trực tiếp của biến đổi log-odds.
  <br><span class="en">$L_i$ is a linear function of $X_i$, but $P_i$ is **not** — this is a direct consequence of the log-odds transformation.</span>
- Diễn giải hệ số $\beta_j$: đó là mức thay đổi trong **log-odds ratio** khi $X_j$ tăng 1 đơn vị, giữ các biến khác không đổi; **dấu** của $\beta_j$ cho biết chiều thay đổi của $P_i$ (dương → $X_j$ tăng làm $P$ tăng; âm → ngược lại) — nhưng **bản thân $\beta_j$ không cho biết độ lớn** của tác động lên xác suất. Đây là khác biệt lớn nhất so với hệ số OLS trong LPM/LRM, và là nguồn gốc của một bẫy thi rất phổ biến (xem mục 12).
  <br><span class="en">Interpreting the coefficient $\beta_j$: it is the change in the **log-odds ratio** when $X_j$ increases by 1 unit, holding the other variables constant; the **sign** of $\beta_j$ tells the direction of change of $P_i$ (positive → an increase in $X_j$ increases $P$; negative → the opposite) — but **$\beta_j$ itself does not tell the magnitude** of the effect on the probability. This is the biggest difference from OLS coefficients in LPM/LRM, and is the source of a very common exam trap (see section 12).</span>
- Trong LPM, marginal effect của $X_j$ là hằng số. Trong Logit, marginal effect **thay đổi theo giá trị $X$** (chi tiết + số liệu thật ở mục 9).
  <br><span class="en">In LPM, the marginal effect of $X_j$ is constant. In Logit, the marginal effect **changes with the value of $X$** (details + real data in section 9).</span>

### 5.4 Ước lượng: Maximum Likelihood (ML) — ý tưởng trực quan - <span class="en">Estimation: Maximum Likelihood (ML) — the intuitive idea</span>

OLS không áp dụng trực tiếp được cho Logit vì bài toán không còn là "tối thiểu hóa tổng bình phương phần dư" theo nghĩa tuyến tính. Thay vào đó, Logit/Probit dùng **Maximum Likelihood (ML)**.
<br><span class="en">OLS cannot be applied directly to Logit because the problem is no longer "minimize the sum of squared residuals" in the linear sense. Instead, Logit/Probit use **Maximum Likelihood (ML)**.</span>

**Ý tưởng trực quan** (không cần chứng minh toán đầy đủ): với mỗi lựa chọn hệ số $\beta$, mô hình sẽ "dự đoán" một xác suất $P_i$ cho từng quan sát. Ta hỏi ngược lại: *nếu $\beta$ này là đúng, xác suất để quan sát được đúng chuỗi kết quả 0/1 mà ta thực sự thấy trong mẫu là bao nhiêu?* ML chọn $\beta$ sao cho xác suất "tái tạo" được đúng dữ liệu quan sát là **lớn nhất**. Nói cách khác: OLS hỏi "$\beta$ nào làm đường dự đoán gần dữ liệu nhất" (theo khoảng cách bình phương); ML hỏi "$\beta$ nào làm dữ liệu quan sát được trở nên *hợp lý nhất* (most likely)".
<br><span class="en">**Intuitive idea** (no need for a full mathematical proof): for each choice of coefficient $\beta$, the model "predicts" a probability $P_i$ for each observation. We ask the reverse question: *if this $\beta$ were true, what is the probability of observing exactly the sequence of 0/1 outcomes we actually see in the sample?* ML chooses $\beta$ so that the probability of "reproducing" the observed data is **maximized**. In other words: OLS asks "which $\beta$ makes the predicted line closest to the data" (by squared distance); ML asks "which $\beta$ makes the observed data *most likely*".</span>

Hàm log-likelihood cần tối đa hóa:
<br><span class="en">The log-likelihood function to be maximized:</span>

$$\log L = \sum_{i=1}^n\Big[Y_i\log P_i + (1-Y_i)\log(1-P_i)\Big], \qquad P_i=\frac{1}{1+e^{-\beta X_i}}$$

Với mỗi quan sát có $Y_i=1$, chỉ số hạng $\log P_i$ "đóng góp" vào tổng (số hạng còn lại nhân với $1-Y_i=0$ nên triệt tiêu); ngược lại với $Y_i=0$, chỉ $\log(1-P_i)$ đóng góp. Trực giác: nếu mô hình dự đoán $P_i$ cao cho một quan sát thực sự có $Y_i=1$ (dự đoán đúng, tự tin), $\log P_i$ gần 0 (đóng góp tốt); nếu mô hình dự đoán $P_i$ thấp cho một quan sát có $Y_i=1$ (dự đoán sai), $\log P_i$ rất âm (bị phạt nặng). Không có nghiệm dạng đóng (closed-form) như $b=(X'X)^{-1}X'y$ của OLS — $\beta$ được tìm bằng thuật toán số (numerical optimization, ví dụ Newton-Raphson), do phần mềm thống kê (R, Stata…) thực hiện.
<br><span class="en">For each observation with $Y_i=1$, only the term $\log P_i$ "contributes" to the sum (the other term is multiplied by $1-Y_i=0$ and vanishes); conversely for $Y_i=0$, only $\log(1-P_i)$ contributes. Intuition: if the model predicts a high $P_i$ for an observation that truly has $Y_i=1$ (correct, confident prediction), $\log P_i$ is close to 0 (a good contribution); if the model predicts a low $P_i$ for an observation with $Y_i=1$ (a wrong prediction), $\log P_i$ is very negative (heavily penalized). There is no closed-form solution like $b=(X'X)^{-1}X'y$ for OLS — $\beta$ is found by numerical optimization (e.g. Newton-Raphson), carried out by statistical software (R, Stata…).</span>

## 6. Mô hình Probit - <span class="en">The Probit model</span>

Probit dùng cùng khung $Pr(Y_i=1)=F(X_i\beta)$ nhưng thay hàm logistic bằng **hàm phân phối tích lũy (CDF) của phân phối chuẩn**:
<br><span class="en">Probit uses the same framework $Pr(Y_i=1)=F(X_i\beta)$ but replaces the logistic function with the **cumulative distribution function (CDF) of the normal distribution**:</span>

$$Pr(Y_i=1)=P_i=\Phi(\beta X_i)=\frac{1}{\sqrt{2\pi}}\int_{-\infty}^{\beta X_i}e^{-z^2/2}\,dz$$

Nói cách khác: Logit giả định sai số $u$ tuân theo **phân phối logistic**; Probit giả định $u$ tuân theo **phân phối chuẩn**. Cả hai đều có hình chữ S, đều tự động bị chặn trong (0,1) — khác biệt duy nhất là **hình dạng đuôi** của hai phân phối:
<br><span class="en">In other words: Logit assumes the error $u$ follows a **logistic distribution**; Probit assumes $u$ follows a **normal distribution**. Both have an S shape, both are automatically bounded in (0,1) — the only difference is the **shape of the tails** of the two distributions:</span>

- Phân phối logistic có đuôi **dày hơn** (fatter tails) một chút so với phân phối chuẩn.
  <br><span class="en">The logistic distribution has slightly **fatter tails** than the normal distribution.</span>
- Hệ quả: $P_i$ tiến về 0 và 1 **chậm hơn** trong Logit so với Probit — với cùng một mức thay đổi $X\beta$ ở vùng cực đoan (xa 0), Logit vẫn còn "để dành" một chút xác suất chưa hội tụ hẳn về biên, trong khi Probit hội tụ nhanh hơn.
  <br><span class="en">Consequence: $P_i$ converges to 0 and 1 **more slowly** in Logit than in Probit — for the same change in $X\beta$ in the extreme region (far from 0), Logit still "holds back" a bit of probability that has not fully converged to the boundary, while Probit converges faster.</span>

**Khi nào chọn cái nào?** Theo đúng slide: "không có lý do rõ ràng để chọn hẳn một trong hai" (no obvious reason of choosing between the two models) — với cùng một bộ dữ liệu, hai mô hình cho kết luận thực chất tương đương (cùng dấu, cùng mức ý nghĩa thống kê ở hầu hết biến — xem số liệu thật mục 8). Lý do thực dụng khiến **Logit thường được ưu tiên hơn**: marginal effect của Logit có dạng đóng, tính trực tiếp được bằng công thức đại số; marginal effect của Probit đòi hỏi tính đạo hàm của hàm phân phối chuẩn (không có công thức đóng đơn giản, phải tính số). Ngoài ra, Logit còn có thêm cách diễn giải bằng **odds ratio** (mục 10) — công cụ quen thuộc trong y tế/dịch tễ học — mà Probit không có tương đương trực tiếp.
<br><span class="en">**Which one to choose, and when?** Exactly as the slide states: "no obvious reason of choosing between the two models" — with the same dataset, the two models give substantively equivalent conclusions (same sign, same statistical significance level on most variables — see the real data in section 8). The practical reason **Logit is usually preferred**: Logit's marginal effect has a closed form, computable directly with an algebraic formula; Probit's marginal effect requires the derivative of the normal distribution function (no simple closed form, must be computed numerically). In addition, Logit also has the **odds ratio** interpretation (section 10) — a tool familiar in health/epidemiology — for which Probit has no direct equivalent.</span>

## 7. Ước lượng thực tế trên dữ liệu vaccine — Logit và Probit song song - <span class="en">Real estimation on the vaccine data — Logit and Probit side by side</span>

Đây là bảng kết quả ước lượng đầy đủ (`stargazer(logit, probit)`), $N=377$:
<br><span class="en">Here is the full estimation results table (`stargazer(logit, probit)`), $N=377$:</span>

| Biến / Variable | Logit $\hat\beta$ (SE) | Probit $\hat\beta$ (SE) |
|---|---|---|
| `efficacy80` | 0.1584 (0.2704) | 0.0821 (0.1542) |
| `duration3` | −0.2807 (0.2712) | −0.1603 (0.1544) |
| `priceUS` | −0.0318*** (0.0092) | −0.0184*** (0.0053) |
| `pbenefit` | 0.1423 (0.2689) | 0.0561 (0.1530) |
| `hhincomeUS` | 0.0005** (0.0002) | 0.0002* (0.0001) |
| `hhsize` | −0.0513 (0.0542) | −0.0225 (0.0317) |
| `age` | −0.0282*** (0.0101) | −0.0161*** (0.0057) |
| `male` | −0.3854 (0.2809) | −0.2281 (0.1614) |
| `riskNeither` | 0.0862 (0.5062) | 0.0229 (0.2788) |
| `riskUnlikely` | −0.6386 (0.4933) | −0.3494 (0.2764) |
| `riskVery likely` | 0.5589 (1.1846) | 0.2528 (0.6126) |
| `riskVery unlikely` | −0.9552* (0.4950) | −0.5516** (0.2798) |
| Constant | 3.5867*** (0.7870) | 2.1075*** (0.4356) |
| Log-likelihood | −175.1115 | −175.7007 |
| AIC | 376.2230 | 377.4013 |

(`risk` nền/base category là "Likely" — 4 dummy `riskNeither/riskUnlikely/riskVery likely/riskVery unlikely` đo chênh lệch so với nhóm này.)
<br><span class="en">(The `risk` base category is "Likely" — the 4 dummies `riskNeither/riskUnlikely/riskVery likely/riskVery unlikely` measure the difference relative to this group.)</span>

**Quan sát nổi bật, khớp giữa hai mô hình**: cùng dấu và cùng mức ý nghĩa thống kê ở gần như mọi biến — `priceUS` và `age` có ý nghĩa mạnh (p<0.01) ở cả hai, `hhincomeUS` có ý nghĩa yếu (p<0.1 probit, p<0.05 logit), `riskVery unlikely` có ý nghĩa ở cả hai. Đây minh họa đúng nhận định "không có lý do rõ ràng để chọn hẳn một trong hai" ở mục 6.
<br><span class="en">**Notable observation, consistent across both models**: same sign and same level of statistical significance on nearly every variable — `priceUS` and `age` are strongly significant (p<0.01) in both, `hhincomeUS` is weakly significant (p<0.1 probit, p<0.05 logit), `riskVery unlikely` is significant in both. This illustrates exactly the point made in section 6 that "there is no obvious reason to choose strictly one over the other."</span>

**Quy tắc kinh nghiệm về độ lớn hệ số**: hệ số Logit thường lớn hơn hệ số Probit tương ứng khoảng **1.6–1.8 lần** (do độ lệch chuẩn của phân phối logistic chuẩn hóa khác phân phối chuẩn chuẩn hóa — tỷ lệ lý thuyết xấp xỉ $\pi/\sqrt3\approx1.814$). Kiểm chứng bằng chính số liệu trên: $-0.0318/-0.0184\approx1.73$ (`priceUS`); $-0.0282/-0.0161\approx1.75$ (`age`) — khớp khá sát với quy tắc kinh nghiệm. **Đây là lý do hệ số Logit và Probit không được so sánh trực tiếp về độ lớn** — chỉ so sánh được dấu, ý nghĩa thống kê, hoặc quy đổi qua marginal effects/xác suất dự đoán (mục 9, 11).
<br><span class="en">**Rule of thumb for coefficient magnitude**: Logit coefficients are typically about **1.6–1.8 times** larger than their corresponding Probit coefficients (because the standardized logistic distribution's standard deviation differs from the standardized normal distribution's — the theoretical ratio is approximately $\pi/\sqrt3\approx1.814$). Verified with the data above: $-0.0318/-0.0184\approx1.73$ (`priceUS`); $-0.0282/-0.0161\approx1.75$ (`age`) — fairly close to the rule of thumb. **This is why Logit and Probit coefficients should not be compared directly in magnitude** — only their sign, statistical significance, or converted marginal effects/predicted probabilities can be compared (sections 9, 11).</span>

## 8. Kiểm định giả thuyết sau Logit/Probit: LR test và Wald test - <span class="en">Hypothesis testing after Logit/Probit: the LR test and Wald test</span>

### 8.1 Trực giác: hai cách kiểm định khác nhau - <span class="en">Intuition: two different ways of testing</span>

Cả hai kiểm định đều trả lời cùng một loại câu hỏi ("nhóm hệ số này có ý nghĩa thống kê không?") nhưng theo hai con đường khác nhau — tương tự tinh thần F-test của [[concepts/linear-regression-model]] mục 8, nhưng thay RSS bằng log-likelihood vì Logit/Probit ước lượng bằng ML chứ không phải OLS:
<br><span class="en">Both tests answer the same type of question ("is this group of coefficients statistically significant?") but by two different routes — in the same spirit as the F-test in [[concepts/linear-regression-model]] section 8, but replacing RSS with log-likelihood since Logit/Probit are estimated by ML, not OLS:</span>

- **Likelihood Ratio (LR) test**: ước lượng **hai lần** — một lần mô hình đầy đủ (full/unrestricted, log-likelihood $LL_F$), một lần mô hình bị ép ràng buộc $H_0$ (restricted, log-likelihood $LL_R$, thường là loại bỏ hẳn các biến đang kiểm định). So sánh mức độ "hợp lý hóa dữ liệu" giữa hai mô hình — nếu loại bỏ biến làm log-likelihood giảm nhiều, biến đó thực sự quan trọng.
  <br><span class="en">**Likelihood Ratio (LR) test**: estimate **twice** — once the full/unrestricted model (log-likelihood $LL_F$), once the model constrained by $H_0$ (restricted, log-likelihood $LL_R$, usually dropping the variables being tested entirely). Compare how well each model "rationalizes the data" — if removing a variable makes the log-likelihood drop a lot, that variable really matters.</span>
- **Wald test**: chỉ cần ước lượng **một lần** — mô hình đầy đủ. Dùng trực tiếp các hệ số ước lượng $\hat\beta$ và ma trận hiệp phương sai (VCV) của mô hình đầy đủ để suy ra liệu ràng buộc $H_0$ có "hợp lý" hay không, không cần ước lượng lại mô hình restricted — về tinh thần, giống một t-test/F-test mở rộng, dựa trên "khoảng cách" giữa ước lượng và giá trị giả định, tính theo đơn vị SE.
  <br><span class="en">**Wald test**: only needs to be estimated **once** — the full model. It directly uses the estimated coefficients $\hat\beta$ and the covariance matrix (VCV) of the full model to infer whether the $H_0$ constraint is "plausible," without re-estimating the restricted model — in spirit, it is like an extended t-test/F-test, based on the "distance" between the estimate and the hypothesized value, measured in units of SE.</span>

Hai kiểm định **tiệm cận tương đương** (asymptotically equivalent) khi cỡ mẫu đủ lớn, nhưng **không cho ra cùng một con số ở mẫu hữu hạn** — số liệu thật bên dưới minh họa rõ điều này.
<br><span class="en">The two tests are **asymptotically equivalent** when the sample size is large enough, but **do not give the same number in finite samples** — the real data below clearly illustrates this.</span>

Công thức LR test:
<br><span class="en">The LR test formula:</span>

$$LR = 2(LL_F - LL_R) \sim \chi^2_q$$

với $q$ = số hệ số bị kiểm định. Slide còn ghi chú kỹ thuật hữu ích: $\log L = -\text{deviance}/2$ — tức deviance (thường xuất hiện trực tiếp trong output R của `glm()`) chỉ là log-likelihood nhân với $-2$, nên `anova(model, test="Chisq")` (so deviance) và `lrtest()` (so log-likelihood) về bản chất tính cùng một con số.
<br><span class="en">where $q$ = the number of coefficients being tested. The slide also notes a useful technical point: $\log L = -\text{deviance}/2$ — i.e. deviance (which often appears directly in R's `glm()` output) is just the log-likelihood multiplied by $-2$, so `anova(model, test="Chisq")` (comparing deviance) and `lrtest()` (comparing log-likelihood) are essentially computing the same number.</span>

### 8.2 Số liệu thật — kiểm định overall significance (toàn bộ hệ số góc, trừ intercept) - <span class="en">Real data — testing overall significance (all slope coefficients, excluding the intercept)</span>

| | Logit | Probit |
|---|---|---|
| Null deviance (376 df) | 392.32 | 392.32 |
| Residual deviance (364 df) | 350.22 | 351.40 |
| $\Delta$Deviance, df=12 | 42.096 | 40.918 |
| p-value | 3.209e-05 | 5.057e-05 |

Cả hai bác bỏ mạnh $H_0:\beta_1=\cdots=\beta_{12}=0$ — có bằng chứng rằng các biến giải thích, xét đồng thời, không phải tất cả đều vô nghĩa (đọc đúng như mục 8.5 của [[concepts/linear-regression-model]] — F-test/LR-test overall chỉ nói "ít nhất một", không nói "tất cả").
<br><span class="en">Both strongly reject $H_0:\beta_1=\cdots=\beta_{12}=0$ — there is evidence that the explanatory variables, taken jointly, are not all irrelevant (read exactly as in section 8.5 of [[concepts/linear-regression-model]] — an overall F-test/LR-test only says "at least one," not "all").</span>

**Tự kiểm tra bằng công thức $\log L=-\text{deviance}/2$**: với Logit, $LL_{full}=-175.1115$ (từ bảng mục 7), suy ra $LL_{null}=-392.32/2=-196.16$; $2(LL_F-LL_R)=2(-175.1115-(-196.16))=42.097\approx42.096$ ✅ khớp (sai số nhỏ do làm tròn). Với Probit, $LL_{full}=-175.7007$, $2(-175.7007-(-196.16))=40.919\approx40.918$ ✅ cũng khớp — một cách nhanh để kiểm tra tính nhất quán nội bộ của bảng số khi làm bài tập tay.
<br><span class="en">**Self-check using $\log L=-\text{deviance}/2$**: for Logit, $LL_{full}=-175.1115$ (from the table in section 7), so $LL_{null}=-392.32/2=-196.16$; $2(LL_F-LL_R)=2(-175.1115-(-196.16))=42.097\approx42.096$ ✅ matches (small discrepancy due to rounding). For Probit, $LL_{full}=-175.7007$, $2(-175.7007-(-196.16))=40.919\approx40.918$ ✅ also matches — a quick way to check the internal consistency of a numbers table when working by hand.</span>

### 8.3 Số liệu thật — kiểm định riêng nhóm biến `risk` (4 dummy cùng lúc) - <span class="en">Real data — testing the `risk` variable group separately (4 dummies at once)</span>

$H_0: \beta_{riskNeither}=\beta_{riskUnlikely}=\beta_{riskVery\,likely}=\beta_{riskVery\,unlikely}=0$ (biến `risk` không ảnh hưởng gì, xét đồng thời cả 4 mức):
<br><span class="en">$H_0: \beta_{riskNeither}=\beta_{riskUnlikely}=\beta_{riskVery\,likely}=\beta_{riskVery\,unlikely}=0$ (the `risk` variable has no effect at all, considering all 4 levels jointly):</span>

| | LR test | Wald test |
|---|---|---|
| **Logit**: $LL_F=-175.11$ (13 tham số / parameters) vs $LL_R=-180.92$ (9 tham số / parameters) | $\chi^2=11.618$, df=4, p=0.02043 | $\chi^2=11.067$, df=4, p=0.02582 |
| **Probit**: $LL_F=-175.70$ (13 tham số / parameters) vs $LL_R=-181.01$ (9 tham số / parameters) | $\chi^2=10.626$, df=4, p=0.03111 | $\chi^2=10.452$, df=4, p=0.03346 |

Cả 4 kiểm định đều bác bỏ $H_0$ ở mức 5% — có bằng chứng rằng mức độ cảm nhận rủi ro COVID-19 ảnh hưởng đồng thời đến quyết định tiêm vaccine. **Điểm cần nhớ**: LR và Wald cho **kết luận giống nhau** (bác bỏ ở 5%) nhưng **giá trị thống kê không trùng khớp tuyệt đối** (11.618 ≠ 11.067; 10.626 ≠ 10.452) — đây là hệ quả bình thường của việc hai kiểm định chỉ tương đương *tiệm cận* (khi $n\to\infty$), không đồng nhất ở mẫu hữu hạn ($n=377$ ở đây).
<br><span class="en">All 4 tests reject $H_0$ at the 5% level — there is evidence that the perceived risk of COVID-19 infection jointly affects the vaccination decision. **Point to remember**: LR and Wald give the **same conclusion** (reject at 5%) but the **test statistics do not match exactly** (11.618 ≠ 11.067; 10.626 ≠ 10.452) — this is a normal consequence of the two tests being only *asymptotically* equivalent (as $n\to\infty$), not identical in finite samples ($n=377$ here).</span>

## 9. Marginal effects — phần khó nhất, vì sao không phải hằng số - <span class="en">Marginal effects — the hardest part, why it is not a constant</span>

### 9.1 Trực giác bằng hình dạng đường cong sigmoid - <span class="en">Intuition via the shape of the sigmoid curve</span>

Đây là khác biệt quan trọng nhất giữa LPM và Logit/Probit, và cũng là nguồn gốc của bẫy thi phổ biến nhất (mục 12). Trong LPM, đường hồi quy là **đường thẳng** — độ dốc (slope) không đổi ở mọi điểm, nên marginal effect $=\beta_j$, một hằng số duy nhất. Trong Logit/Probit, đường dự đoán $P_i$ theo $X_i$ có hình **chữ S** — và độ dốc của một đường cong chữ S **không đều nhau dọc theo đường cong**:
<br><span class="en">This is the most important difference between LPM and Logit/Probit, and also the source of the most common exam trap (section 12). In LPM, the regression line is **a straight line** — the slope is constant at every point, so the marginal effect $=\beta_j$, a single constant. In Logit/Probit, the predicted curve of $P_i$ against $X_i$ has an **S shape** — and the slope of an S-shaped curve **is not uniform along the curve**:</span>

- Ở hai đầu (khi $P_i$ đã gần 0 hoặc gần 1), đường cong gần như **phẳng** — vì hầu hết các cá nhân ở vùng này đã "chốt" quyết định (gần như chắc chắn có hoặc gần như chắc chắn không), nên thêm một đơn vị $X$ hầu như không đổi được quyết định của mấy ai. Marginal effect ở đây rất **nhỏ**.
  <br><span class="en">At the two ends (when $P_i$ is already near 0 or near 1), the curve is nearly **flat** — because most individuals in this region have already "locked in" their decision (nearly certainly yes or nearly certainly no), so one more unit of $X$ barely changes anyone's decision. The marginal effect here is very **small**.</span>
- Ở vùng giữa (khi $P_i$ gần 0.5 — nhóm "lưng chừng", đang phân vân), đường cong **dốc nhất** — một thay đổi nhỏ trong $X$ có thể lay chuyển quyết định của rất nhiều người đang ở ranh giới. Marginal effect ở đây **lớn nhất**.
  <br><span class="en">In the middle region (when $P_i$ is near 0.5 — the "fence-sitting" group, still undecided), the curve is **steepest** — a small change in $X$ can sway the decision of many people at the margin. The marginal effect here is **largest**.</span>

Đây chính là công thức hóa của nhược điểm #2 của LPM (mục 4.4): LPM giả định độ nhạy cảm giống nhau ở mọi mức $X$; Logit/Probit cho phép độ nhạy cảm **thay đổi tùy vị trí trên đường cong**, khớp với trực giác kinh tế tốt hơn nhiều.
<br><span class="en">This is precisely the formalization of LPM drawback #2 (section 4.4): LPM assumes the same sensitivity at every level of $X$; Logit/Probit allow the sensitivity to **change depending on position along the curve**, matching economic intuition much better.</span>

Công thức (đạo hàm của $P_i$ theo $X_i$, đối với Logit):
<br><span class="en">Formula (the derivative of $P_i$ with respect to $X_i$, for Logit):</span>

$$\frac{\partial P_i}{\partial X_i} = \frac{\partial}{\partial X_i}\left(\frac{1}{1+e^{-\beta X_i}}\right) = \beta_i\cdot\underbrace{\frac{1}{1+e^{-\beta X_i}}\Big(1-\frac{1}{1+e^{-\beta X_i}}\Big)}_{=P_i(1-P_i)} = \beta_i\cdot P_i(1-P_i)$$

Số hạng $P_i(1-P_i)$ là một "trọng số" hình chuông (bell-shaped), đạt cực đại $=0.25$ tại $P_i=0.5$ và tiến về 0 khi $P_i\to0$ hoặc $P_i\to1$ — đây chính là công thức hóa chặt chẽ của trực giác "dốc nhất ở giữa, phẳng ở hai đầu" vừa nêu. **Marginal effect trong Logit/Probit không phải một con số cố định — nó là một hàm số phụ thuộc vào giá trị cụ thể của $X$ (qua $P_i$)**.
<br><span class="en">The term $P_i(1-P_i)$ is a bell-shaped "weight," reaching a maximum $=0.25$ at $P_i=0.5$ and approaching 0 as $P_i\to0$ or $P_i\to1$ — this is precisely the rigorous formalization of the "steepest in the middle, flat at the ends" intuition just described. **The marginal effect in Logit/Probit is not a fixed number — it is a function that depends on the specific value of $X$ (through $P_i$)**.</span>

### 9.2 Minh họa bằng số tự tính từ hệ số Logit (dữ liệu vaccine) - <span class="en">Illustration with numbers computed by hand from the Logit coefficients (vaccine data)</span>

Dùng hệ số Logit ở mục 7 ($\beta_{priceUS}=-0.0318$; các biến khác cố định ở mức: `efficacy80=1, duration3=1, pbenefit=0, hhincomeUS=700, hhsize=4, age=30, male=1, risk="Very likely"` — đúng theo giá trị tham chiếu slide dùng để vẽ đồ thị dự đoán ở mục 10), tính tay bằng công thức trên để thấy rõ hình chữ S và marginal effect thay đổi ra sao theo giá vaccine:
<br><span class="en">Using the Logit coefficient from section 7 ($\beta_{priceUS}=-0.0318$; other variables fixed at: `efficacy80=1, duration3=1, pbenefit=0, hhincomeUS=700, hhsize=4, age=30, male=1, risk="Very likely"` — exactly the reference values the slide uses to plot the predicted-probability graph in section 10), computing by hand with the formula above to clearly see the S shape and how the marginal effect changes with vaccine price:</span>

| `priceUS` (USD) | $P_i$ dự đoán / predicted | Marginal effect ($\partial P/\partial X$, %-điểm mỗi $1 tăng thêm / pp per $1 increase) |
|---|---|---|
| 0 | ≈ 0.950 | ≈ −0.152 |
| 50 | ≈ 0.794 | ≈ −0.521 |
| 92 (≈ điểm $P=0.5$ / point where $P=0.5$) | = 0.500 | ≈ **−0.795 (dốc nhất / steepest)** |
| 100 | ≈ 0.440 | ≈ −0.783 |
| 150 | ≈ 0.138 | ≈ −0.378 |

*(Số liệu ở bảng này do tự tính từ hệ số đã làm tròn 4 chữ số thập phân trong bảng stargazer mục 7 — chỉ mang tính minh họa hình dạng đường cong, có thể lệch nhẹ so với số xuất trực tiếp từ R với hệ số đầy đủ chữ số.)*
<br><span class="en">*(The figures in this table were hand-computed from the coefficients rounded to 4 decimal places in the stargazer table of section 7 — intended only to illustrate the curve's shape, and may differ slightly from numbers output directly by R using full-precision coefficients.)*</span>

Thấy rõ: marginal effect không phải một con số, mà thay đổi từ khoảng −0.15 %-điểm (ở giá 0 USD, khi hầu hết đã sẵn sàng tiêm) lên đến gần −0.8 %-điểm (ở giá quanh 90 USD, vùng "lưng chừng"), rồi giảm lại còn khoảng −0.38 %-điểm (ở giá 150 USD, khi hầu hết đã từ chối). Đây là bằng chứng số học trực tiếp cho nhược điểm #2 của LPM.
<br><span class="en">Clearly: the marginal effect is not a single number, but changes from about −0.15 percentage points (at a price of 0 USD, when most are already willing to vaccinate) up to nearly −0.8 percentage points (at a price around 90 USD, the "fence-sitting" region), then falls back to about −0.38 percentage points (at a price of 150 USD, when most have already refused). This is direct numerical evidence for LPM drawback #2.</span>

### 9.3 MEM (Marginal Effect at the Mean) vs. AME (Average Marginal Effect) - <span class="en">MEM (Marginal Effect at the Mean) vs. AME (Average Marginal Effect)</span>

Vì marginal effect thay đổi theo $X$, một câu hỏi thực tế nảy sinh: khi báo cáo kết quả (ví dụ trong bảng hồi quy của luận văn), nên báo cáo **một con số** marginal effect nào cho mỗi biến? Có hai cách tiếp cận chuẩn:
<br><span class="en">Since the marginal effect changes with $X$, a practical question arises: when reporting results (e.g. in a thesis regression table), which **single number** for the marginal effect should be reported for each variable? There are two standard approaches:</span>

- **MEM — Marginal Effect at the Mean**: tính marginal effect tại **một điểm duy nhất** — điểm mà mọi biến $X$ được đặt bằng giá trị trung bình mẫu của chúng ($\bar X$). Trong R: `logitmfx(..., atmean=TRUE)`. Nhược điểm khái niệm: "quan sát trung bình" này thường **không tồn tại trong thực tế** — ví dụ nếu `male` trung bình mẫu là 0.55, "người trung bình" có 55% là nam, một cá thể không có thật. Với các biến dummy hoặc categorical, khái niệm "giá trị trung bình" trở nên mơ hồ về mặt diễn giải.
  <br><span class="en">**MEM — Marginal Effect at the Mean**: computes the marginal effect at **a single point** — the point where every $X$ variable is set to its sample mean ($\bar X$). In R: `logitmfx(..., atmean=TRUE)`. Conceptual drawback: this "average observation" often **does not exist in reality** — for example, if the sample mean of `male` is 0.55, the "average person" is 55% male, a nonexistent individual. For dummy or categorical variables, the notion of a "mean value" becomes ambiguous to interpret.</span>
- **AME — Average Marginal Effect**: tính marginal effect **tại từng quan sát** (dùng đúng giá trị $X_i$ thật của quan sát đó), sau đó lấy **trung bình cộng** của toàn bộ $N$ marginal effect cá nhân này. Trong R: `logitmfx(..., atmean=FALSE)`. Ưu điểm: phản ánh đúng sự không đồng nhất (heterogeneity) thật sự có trong mẫu, không dựa vào một "cá thể giả định" nào.
  <br><span class="en">**AME — Average Marginal Effect**: computes the marginal effect **at each observation** (using that observation's actual $X_i$ values), then takes the **arithmetic mean** of all $N$ individual marginal effects. In R: `logitmfx(..., atmean=FALSE)`. Advantage: correctly reflects the real heterogeneity present in the sample, without relying on any "hypothetical individual."</span>

**Tại sao AME thường được khuyến nghị hơn trong thực hành hiện đại?** Vì AME tôn trọng đúng phân phối thật của dữ liệu — nó là trung bình của N hiệu ứng biên thực tế, thay vì hiệu ứng biên tại một điểm nhân tạo có thể nằm ở vùng dữ liệu thưa hoặc không đại diện. Đây cũng là lựa chọn mặc định trong nhiều công cụ thống kê hiện đại (ví dụ lệnh `margins, dydx(*)` của Stata mặc định tính AME). MEM vẫn hữu ích khi câu hỏi nghiên cứu cụ thể là "hiệu ứng của X đối với một cá nhân có đặc điểm trung bình" — nhưng với hầu hết các báo cáo hồi quy tổng quát, AME là lựa chọn an toàn và được ưa chuộng hơn.
<br><span class="en">**Why is AME usually recommended over MEM in modern practice?** Because AME respects the actual distribution of the data — it is the average of N real marginal effects, rather than the marginal effect at an artificial point that may lie in a sparse or unrepresentative region of the data. This is also the default choice in many modern statistical tools (e.g. Stata's `margins, dydx(*)` computes AME by default). MEM is still useful when the specific research question is "the effect of X on an individual with average characteristics" — but for most general-purpose regression reporting, AME is the safer, more preferred choice.</span>

### 9.4 Số liệu thật — MEM và AME cho cùng một mô hình - <span class="en">Real data — MEM and AME for the same model</span>

**Logit — MEM (`atmean=TRUE`)**, chỉ liệt kê các biến có ý nghĩa thống kê:
<br><span class="en">**Logit — MEM (`atmean=TRUE`)**, listing only the statistically significant variables:</span>

| Biến / Variable | dF/dx | SE | p-value |
|---|---|---|---|
| `priceUS` | −4.7433e-03 | 1.3804e-03 | 0.0006 *** |
| `age` | −4.2117e-03 | 1.3341e-03 | 0.0016 ** |

**Logit — AME (`atmean=FALSE`)**:

| Biến / Variable | dF/dx | SE | p-value |
|---|---|---|---|
| `priceUS` | −4.7423e-03 | 1.5302e-03 | 0.00194 ** |
| `age` | −4.2108e-03 | 1.4774e-03 | 0.00437 ** |

**Probit — MEM**: `priceUS` dF/dx = −4.9899e-03 (SE 1.4710e-03, p=0.0007***); `age` dF/dx = −4.3804e-03 (SE 1.3546e-03, p=0.0012**).
**Probit — AME**: `priceUS` dF/dx = −4.8133e-03 (SE 1.3684e-03, p=0.0004***); `age` dF/dx = −4.2254e-03 (SE 1.2813e-03, p=0.0010***).

Các biến còn lại (`efficacy80`, `duration3`, `pbenefit`, `hhincomeUS`, `hhsize`, `male`, các mức của `risk`) không có ý nghĩa thống kê ở marginal effect trong cả hai cách tính, dù một vài biến (`hhincomeUS`) có ý nghĩa yếu ở hệ số thô (mục 7) — bản thân đây cũng là một điểm cần lưu ý: **ý nghĩa thống kê của hệ số thô và của marginal effect không nhất thiết trùng khớp hoàn toàn**.
<br><span class="en">The remaining variables (`efficacy80`, `duration3`, `pbenefit`, `hhincomeUS`, `hhsize`, `male`, the levels of `risk`) are not statistically significant for the marginal effect under either method, even though a few (`hhincomeUS`) are weakly significant in the raw coefficient (section 7) — this itself is a point worth noting: **the statistical significance of the raw coefficient and of the marginal effect do not necessarily match completely**.</span>

**Đọc con số cụ thể**: AME của `priceUS` (Logit) là −0.0047423 — nghĩa là, **trung bình trên toàn mẫu**, mỗi 1 USD tăng thêm trong giá vaccine làm giảm xác suất quyết định tiêm khoảng **0.474 điểm phần trăm**. So với bảng tự tính ở mục 9.2 (dao động từ −0.15 đến −0.80 %-điểm tùy mức giá), AME chính là một loại "trung bình có trọng số" của toàn bộ các marginal effect cá nhân dao động đó — một con số duy nhất tóm tắt một hiện tượng vốn dĩ không đồng nhất.
<br><span class="en">**Reading the specific number**: the AME of `priceUS` (Logit) is −0.0047423 — meaning, **on average across the whole sample**, each additional 1 USD in vaccine price reduces the probability of deciding to vaccinate by about **0.474 percentage points**. Compared to the hand-computed table in section 9.2 (ranging from −0.15 to −0.80 percentage points depending on the price level), the AME is essentially a "weighted average" of all those varying individual marginal effects — a single number summarizing an inherently heterogeneous phenomenon.</span>

**Nhận xét về sự khác biệt MEM vs AME ở ví dụ này**: hai con số dF/dx rất gần nhau về độ lớn (−4.7433e-03 vs −4.7423e-03 cho `priceUS`) — vì phân phối của các biến trong mẫu này không quá lệch/cực đoan, "quan sát trung bình" không quá khác biệt so với "trung bình của các quan sát". SE lại chênh nhau rõ hơn (1.3804e-03 MEM vs 1.5302e-03 AME cho `priceUS`) — minh họa rằng hai cách tính không chỉ khác về điểm ước lượng mà còn khác về độ bất định đi kèm.
<br><span class="en">**Remark on the MEM vs. AME difference in this example**: the two dF/dx numbers are very close in magnitude (−4.7433e-03 vs −4.7423e-03 for `priceUS`) — because the distribution of the variables in this sample is not too skewed/extreme, so the "average observation" is not too different from the "average of the observations." The SEs differ more noticeably (1.3804e-03 MEM vs 1.5302e-03 AME for `priceUS`) — illustrating that the two methods differ not only in the point estimate but also in the associated uncertainty.</span>

### 9.5 Marginal effect tại một điểm cụ thể — phương pháp sai phân rời rạc (discrete difference) - <span class="en">Marginal effect at a specific point — the discrete difference method</span>

Ngoài đạo hàm giải tích, còn một cách tính marginal effect **thực dụng** hơn — đặc biệt hữu ích khi muốn biết hiệu ứng tại một điểm dữ liệu cụ thể, hoặc khi biến độc lập không liên tục (dummy, categorical) và đạo hàm giải tích không áp dụng trực tiếp: dự đoán xác suất ở **hai điểm** chỉ khác nhau đúng 1 đơn vị của biến quan tâm, rồi lấy hiệu số.
<br><span class="en">Besides the analytical derivative, there is a more **practical** way of computing the marginal effect — especially useful when we want the effect at a specific data point, or when the independent variable is not continuous (dummy, categorical) and the analytical derivative does not apply directly: predict the probability at **two points** that differ by exactly 1 unit of the variable of interest, then take the difference.</span>

Ví dụ slide dùng cho biến `hhincomeUS`: cố định mọi biến khác (`priceUS=50, efficacy80=1, duration3=1, pbenefit=0, hhsize=4, age=30, male=1, risk="Very likely"`), chỉ thay đổi thu nhập hộ gia đình từ 700 lên 701 USD/tháng:
<br><span class="en">The example the slide uses for `hhincomeUS`: hold all other variables fixed (`priceUS=50, efficacy80=1, duration3=1, pbenefit=0, hhsize=4, age=30, male=1, risk="Very likely"`), and change only household income from 700 to 701 USD/month:</span>

- **Logit**: $Pr(dself=1\mid hhincomeUS=701) - Pr(dself=1\mid hhincomeUS=700) = 7.580978\times10^{-5}$
- **Probit**: hiệu số tương ứng $=6.806759\times10^{-5}$
  <br><span class="en">**Probit**: the corresponding difference $=6.806759\times10^{-5}$</span>

Nghĩa là, tại điểm dữ liệu này, tăng thu nhập hộ gia đình thêm 1 USD/tháng chỉ làm tăng xác suất quyết định tiêm vaccine khoảng **0.0076 điểm phần trăm** (Logit) — rất nhỏ, khớp với hệ số `hhincomeUS` vốn đã rất nhỏ (0.0005) và không có ý nghĩa thống kê ở marginal effect (mục 9.4). Phương pháp sai phân rời rạc này chính là cách R/Stata tính marginal effect cho các biến dummy (ví dụ `male`, `efficacy80`) — vì khái niệm "đạo hàm" không có ý nghĩa với một biến chỉ nhận giá trị 0 hoặc 1.
<br><span class="en">That is, at this data point, increasing household income by 1 USD/month only increases the probability of deciding to vaccinate by about **0.0076 percentage points** (Logit) — very small, consistent with the `hhincomeUS` coefficient already being tiny (0.0005) and not statistically significant at the marginal-effect level (section 9.4). This discrete-difference method is exactly how R/Stata compute the marginal effect for dummy variables (e.g. `male`, `efficacy80`) — since the concept of a "derivative" has no meaning for a variable that only takes the value 0 or 1.</span>

## 10. Predicted probability và độ chính xác dự đoán - <span class="en">Predicted probability and prediction accuracy</span>

### 10.1 Đường cong xác suất dự đoán - <span class="en">The predicted probability curve</span>

Cố định các biến khác ở mức tham chiếu (như mục 9.2), cho `priceUS` chạy từ 0 đến 150 USD và vẽ $\hat P_i$ dự đoán — đồ thị cho ra đúng hình chữ S kỳ vọng: bắt đầu gần 0.94–0.95 khi giá bằng 0, giảm dần và dốc nhất ở vùng giá giữa (khoảng 70–100 USD), rồi thoải dần về khoảng 0.13–0.14 khi giá chạm 150 USD — khớp hoàn toàn với bảng tự tính ở mục 9.2 và với hình dạng lý thuyết của sigmoid đã mô tả ở mục 9.1.
<br><span class="en">Holding the other variables at their reference levels (as in section 9.2), letting `priceUS` range from 0 to 150 USD and plotting the predicted $\hat P_i$ — the graph produces exactly the expected S shape: starting near 0.94–0.95 at price zero, decreasing and steepest in the middle price range (about 70–100 USD), then flattening out to about 0.13–0.14 as the price reaches 150 USD — fully consistent with the hand-computed table in section 9.2 and with the theoretical sigmoid shape described in section 9.1.</span>

### 10.2 Độ chính xác dự đoán (correct prediction rate) — ví dụ Probit - <span class="en">Prediction accuracy (correct prediction rate) — Probit example</span>

Dùng ngưỡng $\hat P_i>0.5$ để phân loại dự đoán "có tiêm"/"không tiêm", đối chiếu với thực tế:
<br><span class="en">Using the threshold $\hat P_i>0.5$ to classify the prediction as "vaccinate"/"not vaccinate," compared against the actual outcome:</span>

| | Thực tế: `dself=0` / Actual: `dself=0` | Thực tế: `dself=1` / Actual: `dself=1` |
|---|---|---|
| Dự đoán: không tiêm (FALSE) / Predicted: not vaccinate (FALSE) | 9 | 7 |
| Dự đoán: có tiêm (TRUE) / Predicted: vaccinate (TRUE) | 72 | 289 |

Tỷ lệ dự đoán đúng tổng thể: $\dfrac{9+289}{377} = 0.7904509$ (≈79.05%).
<br><span class="en">Overall correct prediction rate: $\dfrac{9+289}{377} = 0.7904509$ (≈79.05%).</span>

**Điểm cần lưu ý khi diễn giải con số này** (tự tính thêm từ chính bảng trên, không phải số slide nêu sẵn — nhưng là hệ quả số học trực tiếp): trong mẫu, tổng số người thực sự chọn "có tiêm" là $7+289=296/377\approx78.5\%$. Nghĩa là một mô hình "ngây thơ" chỉ đơn giản luôn dự đoán "có tiêm" cho mọi người (không cần biết gì về $X$) đã đạt độ chính xác khoảng 78.5% — gần bằng con số 79.05% mà mô hình Probit đạt được. Mô hình chỉ nhận diện đúng 9/81 (≈11%) trường hợp thực sự "không tiêm" — cho thấy **tỷ lệ dự đoán đúng tổng thể có thể gây hiểu lầm khi outcome mất cân bằng** (imbalanced) — một điểm cần cẩn trọng khi đánh giá mô hình binary response trong thực hành, không chỉ dừng ở một con số "% đúng" duy nhất.
<br><span class="en">**A point to note when interpreting this number** (computed additionally from the table above, not a number the slide states directly — but a direct arithmetic consequence): in the sample, the total number of people who actually chose "vaccinate" is $7+289=296/377\approx78.5\%$. This means a "naive" model that simply always predicts "vaccinate" for everyone (without knowing anything about $X$) would already achieve about 78.5% accuracy — close to the 79.05% the Probit model achieves. The model correctly identifies only 9/81 (≈11%) of the truly "not vaccinate" cases — showing that **the overall correct-prediction rate can be misleading when the outcome is imbalanced** — a point to be cautious about when evaluating binary response models in practice, rather than stopping at a single "% correct" number.</span>

## 11. Logit hay Probit? — so sánh trực tiếp bằng đồ thị dự đoán - <span class="en">Logit or Probit? — a direct comparison via the predicted-probability graph</span>

Vẽ chồng hai đường cong xác suất dự đoán (Logit và Probit) trên cùng một biến `priceUS`: hai đường **gần như trùng khít nhau** trên toàn bộ khoảng giá 0–150 USD, chỉ lệch rất nhẹ ở vùng giữa — đường Logit nằm hơi cao hơn Probit một chút ở vùng giá thấp/giữa, khớp với nhận định ở mục 6 rằng $P_i$ của Logit "tiến về 0 và 1 chậm hơn" Probit. Đây là bằng chứng trực quan cho thấy **kết luận thực chất (xác suất dự đoán) của hai mô hình gần như tương đương** dù hệ số thô của chúng chênh lệch nhau khoảng 1.6–1.8 lần (mục 7) — hai điều này không mâu thuẫn, vì hệ số thô của Logit/Probit tự thân không so sánh được, chỉ xác suất/marginal effect suy ra từ chúng mới so sánh được.
<br><span class="en">Overlaying the two predicted-probability curves (Logit and Probit) on the same `priceUS` variable: the two lines **nearly coincide** across the entire 0–150 USD price range, diverging only very slightly in the middle region — the Logit line sits a bit higher than Probit in the low/middle price region, consistent with the observation in section 6 that Logit's $P_i$ "converges to 0 and 1 more slowly" than Probit. This is visual evidence that **the substantive conclusion (predicted probability) of the two models is nearly equivalent** even though their raw coefficients differ by about 1.6–1.8 times (section 7) — the two facts are not contradictory, because Logit/Probit raw coefficients are not comparable on their own, only the probabilities/marginal effects derived from them are comparable.</span>

## 12. Logistic regression với Odds Ratio - <span class="en">Logistic regression with Odds Ratio</span>

Một cách trình bày kết quả Logit phổ biến khác — đặc biệt trong y tế/dịch tễ học — là báo cáo trực tiếp **odds ratio** thay vì hệ số thô. Vì đã có $\dfrac{P_i}{1-P_i}=e^{\beta X_i}$ (mục 5.2), odds ratio của từng biến chính là $e^{\hat\beta_j}$ — slide xác nhận bằng số liệu thật: `exp(coef(logit))` cho ra đúng cột "OddsRatio" trong bảng `logitor()`.
<br><span class="en">Another common way of presenting Logit results — especially in health/epidemiology — is to report the **odds ratio** directly instead of the raw coefficient. Since $\dfrac{P_i}{1-P_i}=e^{\beta X_i}$ (section 5.2) already holds, the odds ratio of each variable is exactly $e^{\hat\beta_j}$ — the slide confirms this with real data: `exp(coef(logit))` produces exactly the "OddsRatio" column in the `logitor()` table.</span>

| Biến / Variable | Odds Ratio | p-value | Diễn giải / Interpretation |
|---|---|---|---|
| `priceUS` | 0.9687 | 0.0005 *** | mỗi $1 tăng giá làm odds (tỷ lệ cược) quyết định tiêm **giảm khoảng 3.13%** ($(0.9687-1)\times100\%$), giữ các biến khác không đổi / each $1 increase in price **decreases** the odds of deciding to vaccinate by **about 3.13%** ($(0.9687-1)\times100\%$), holding other variables constant |
| `age` | 0.9722 | 0.0053 ** | mỗi năm tuổi tăng thêm làm odds quyết định tiêm giảm khoảng 2.78% / each additional year of age decreases the odds of deciding to vaccinate by about 2.78% |
| `hhincomeUS` | 1.00046 | 0.0428 * | mỗi $1 thu nhập hộ tăng thêm làm odds tăng khoảng 0.046% (rất nhỏ, dù có ý nghĩa thống kê yếu) / each additional $1 of household income increases the odds by about 0.046% (very small, though weakly statistically significant) |
| `riskVery unlikely` | 0.3847 | 0.0536 . | so với nhóm "Likely" (nền), nhóm cảm thấy rủi ro "rất khó xảy ra" có odds quyết định tiêm chỉ bằng khoảng 38.5% (ở mức ý nghĩa biên, p≈0.054) / relative to the "Likely" (base) group, the group who feel infection is "very unlikely" have odds of deciding to vaccinate only about 38.5% as large (at a marginal significance level, p≈0.054) |

**Quy tắc đọc odds ratio**: $OR>1$ → biến làm **tăng** odds (và do đó tăng $P$); $OR<1$ → làm **giảm** odds; $OR=1$ → không có tác động. Phần trăm thay đổi trong odds $=(OR-1)\times100\%$. Lưu ý: đây vẫn là phát biểu về **odds**, không phải phát biểu trực tiếp về xác suất $P$ hay về marginal effect — quy đổi ngược từ odds ratio sang xác suất vẫn cần công thức $P=OR/(1+OR)$ áp dụng đúng ngữ cảnh, không thể đọc thẳng odds ratio như một con số phần trăm thay đổi của $P$.
<br><span class="en">**Rule for reading an odds ratio**: $OR>1$ → the variable **increases** the odds (and hence increases $P$); $OR<1$ → **decreases** the odds; $OR=1$ → no effect. The percentage change in odds $=(OR-1)\times100\%$. Note: this is still a statement about **odds**, not a direct statement about the probability $P$ or the marginal effect — converting back from odds ratio to probability still requires applying the formula $P=OR/(1+OR)$ in the right context; the odds ratio cannot be read directly as a percentage-change number for $P$.</span>

## 13. So sánh tổng hợp: LPM vs Logit vs Probit - <span class="en">Summary comparison: LPM vs Logit vs Probit</span>

| Tiêu chí / Criterion | LPM | Logit | Probit |
|---|---|---|---|
| Hàm liên kết $F(X\beta)$ / Link function $F(X\beta)$ | $X\beta$ | $\dfrac{1}{1+e^{-X\beta}}$ | $\Phi(X\beta)$ (CDF chuẩn / normal CDF) |
| Dự đoán $Pr(y=1)$ có bị chặn [0,1] không / Is predicted $Pr(y=1)$ bounded in [0,1] | ❌ Không / No | ✅ Có / Yes | ✅ Có / Yes |
| Marginal effect | Hằng số ($=\beta_j$) / Constant ($=\beta_j$) | Thay đổi theo $X$ (qua $P(1-P)$) / Changes with $X$ (via $P(1-P)$) | Thay đổi theo $X$ (qua $\phi(X\beta)$) / Changes with $X$ (via $\phi(X\beta)$) |
| Ước lượng / Estimation | OLS | Maximum Likelihood | Maximum Likelihood |
| Heteroskedasticity | Có sẵn, luôn vi phạm A4 / Inherent, always violates A4 | Không phải vấn đề theo cùng cách (không dùng khung OLS) / Not an issue in the same way (does not use the OLS framework) | Tương tự Logit / Similar to Logit |
| Diễn giải hệ số thô / Interpreting the raw coefficient | Trực tiếp = thay đổi xác suất / Direct = change in probability | Chỉ cho **dấu** (chiều), không cho độ lớn — cần marginal effect hoặc odds ratio / Gives only the **sign** (direction), not the magnitude — need the marginal effect or odds ratio | Chỉ cho **dấu**, không cho độ lớn — cần marginal effect / Gives only the **sign**, not the magnitude — need the marginal effect |
| Ưu điểm / Advantage | Đơn giản, dễ diễn giải, dùng được công cụ OLS quen thuộc / Simple, easy to interpret, can use familiar OLS tools | Marginal effect có công thức đóng; có thêm cách diễn giải odds ratio / Marginal effect has a closed form; also has the odds-ratio interpretation | Nền tảng lý thuyết gắn với phân phối chuẩn — hay dùng khi mô hình hóa latent variable có $u\sim N(0,1)$ (ví dụ mở rộng sang Tobit, Heckman) / Theoretical foundation tied to the normal distribution — often used when modeling a latent variable with $u\sim N(0,1)$ (e.g. extensions to Tobit, Heckman) |
| Nhược điểm / Disadvantage | 4 nhược điểm ở mục 4.4 / The 4 drawbacks in section 4.4 | Đuôi dày hơn chuẩn — hội tụ về 0/1 chậm hơn / Fatter tails than normal — converges to 0/1 more slowly | Marginal effect phải tính số (không có công thức đóng đơn giản) / Marginal effect must be computed numerically (no simple closed form) |
| Khi nào dùng / When to use | Khi cần diễn giải cực nhanh, cực đơn giản, hoặc làm mô hình cơ sở (baseline) để so sánh; ít khi dùng làm mô hình chính thức trong nghiên cứu hiện đại / When an extremely fast, extremely simple interpretation is needed, or as a baseline model for comparison; rarely used as the formal model in modern research | Lựa chọn phổ biến nhất trong thực hành — đặc biệt khi cần odds ratio (y tế, tín dụng) / The most common choice in practice — especially when the odds ratio is needed (health, credit) | Khi lý thuyết/mô hình mở rộng yêu cầu giả định phân phối chuẩn (ví dụ liên kết với các mô hình censored/truncated ở Topic 11) / When the theory/extended model requires the normal-distribution assumption (e.g. linking to censored/truncated models in Topic 11) |

## 14. Bẫy thi - <span class="en">Exam traps</span>

1. **Diễn giải hệ số thô của Logit/Probit như thể nó là % thay đổi trực tiếp của xác suất** — đây là lỗi phổ biến nhất trong toàn bộ Topic 7. Hệ số thô ($\hat\beta_j$) chỉ cho biết **chiều** thay đổi của $P$ (dấu dương/âm), **không cho biết độ lớn**. Muốn biết độ lớn tác động lên xác suất, phải tính **marginal effect** (mục 9); muốn diễn giải qua odds, dùng $e^{\hat\beta_j}$ (mục 12) — và ngay cả khi đó, odds ratio vẫn là phát biểu về odds, không phải phát biểu trực tiếp về phần trăm thay đổi xác suất.
   <br><span class="en">**Interpreting a raw Logit/Probit coefficient as if it were a direct % change in probability** — the single most common mistake in all of Topic 7. The raw coefficient ($\hat\beta_j$) only tells you the **direction** of the change in $P$ (positive/negative sign), **not the magnitude**. To know the magnitude of the effect on probability, you must compute the **marginal effect** (section 9); to interpret via odds, use $e^{\hat\beta_j}$ (section 12) — and even then, an odds ratio is a statement about odds, not a direct statement about a percentage change in probability.</span>
2. **Coi marginal effect của Logit/Probit là một hằng số duy nhất, giống LPM** — sai. Marginal effect phụ thuộc giá trị của $X$ (qua $P_i(1-P_i)$ hoặc $\phi(X\beta)$) — khi báo cáo phải nói rõ đang dùng **MEM** hay **AME**, không được nói chung chung "marginal effect của biến X là...".
   <br><span class="en">**Treating the Logit/Probit marginal effect as a single constant, like the LPM** — wrong. The marginal effect depends on the value of $X$ (via $P_i(1-P_i)$ or $\phi(X\beta)$) — a report must state clearly whether it uses **MEM** or **AME**, never a generic "the marginal effect of variable X is...".</span>
3. **Nhầm MEM và AME là hai cách tính cho ra cùng một con số** — trong thực tế thường gần nhau (như ví dụ mục 9.4) nhưng **không đồng nhất về mặt toán học**, đặc biệt khi phân phối của $X$ trong mẫu lệch mạnh. Luôn nêu rõ đang dùng cách nào khi trình bày kết quả.
   <br><span class="en">**Assuming MEM and AME are two computation methods that give the same number** — in practice they are often close (as in the example in section 9.4) but **not mathematically identical**, especially when $X$'s sample distribution is strongly skewed. Always state clearly which one is being used when reporting results.</span>
4. **So sánh trực tiếp độ lớn hệ số thô giữa Logit và Probit** mà không quy đổi — hai mô hình có thang đo (variance chuẩn hóa) khác nhau; hệ số Logit thường lớn hơn Probit khoảng 1.6–1.8 lần một cách máy móc, không phản ánh hiệu ứng "mạnh hơn" thực sự — phải so sánh qua xác suất dự đoán hoặc marginal effect mới có ý nghĩa kinh tế.
   <br><span class="en">**Directly comparing the raw coefficient magnitudes between Logit and Probit** without rescaling — the two models have different scales (normalized variances); Logit coefficients are mechanically about 1.6–1.8 times larger than Probit's, which does not reflect a genuinely "stronger" effect — a meaningful economic comparison requires comparing predicted probabilities or marginal effects instead.</span>
5. **Kỳ vọng LR test và Wald test cho ra đúng cùng một giá trị thống kê** — hai kiểm định chỉ **tiệm cận tương đương**, không đồng nhất ở mẫu hữu hạn (xem số liệu thật mục 8.3: 11.618 vs 11.067).
   <br><span class="en">**Expecting the LR test and Wald test to give exactly the same statistic** — the two tests are only **asymptotically equivalent**, not identical in finite samples (see the real numbers in section 8.3: 11.618 vs. 11.067).</span>
6. **Dùng tỷ lệ dự đoán đúng (% correct prediction) làm thước đo duy nhất cho chất lượng mô hình** khi outcome mất cân bằng (imbalanced) — như ví dụ mục 10.2, một mô hình "ngây thơ" luôn dự đoán nhóm đa số đã đạt gần bằng độ chính xác của mô hình Probit thật; cần nhìn thêm vào khả năng nhận diện đúng nhóm thiểu số (ở đây chỉ 11%), không chỉ con số tổng.
   <br><span class="en">**Using the % correct prediction rate as the sole measure of model quality** when the outcome is imbalanced — as in the example in section 10.2, a "naive" model that always predicts the majority class already achieves accuracy close to that of the actual Probit model; you also need to look at the ability to correctly identify the minority class (only 11% here), not just the overall number.</span>
7. **Coi việc LPM "vẫn chạy được bằng OLS" nghĩa là LPM hợp lệ về mặt suy luận thống kê** — LPM luôn vi phạm A4 (heteroskedasticity, mục 4.4) một cách có hệ thống (không phải ngẫu nhiên như trong LRM thông thường), nên SE mặc định của OLS áp dụng cho LPM luôn cần nghi ngờ, dù mô hình vẫn "chạy" và cho ra hệ số.
   <br><span class="en">**Treating the fact that the LPM "still runs fine via OLS" as meaning the LPM is valid for statistical inference** — the LPM always violates A4 (heteroskedasticity, section 4.4) systematically (not randomly, as in an ordinary LRM), so OLS's default SE applied to an LPM should always be treated with suspicion, even though the model still "runs" and produces coefficients.</span>
8. **Quên rằng odds ratio > 1 hay < 1 mang ý nghĩa khác với hệ số thô dương/âm** — $OR=1$ (không phải $OR=0$) mới là điểm "không có tác động"; đọc nhầm $OR<1$ thành "tác động âm nhỏ" thay vì tính đúng phần trăm thay đổi $(OR-1)\times100\%$ là lỗi thường gặp khi mới làm quen với odds ratio.
   <br><span class="en">**Forgetting that an odds ratio > 1 or < 1 carries a different meaning than a positive/negative raw coefficient** — $OR=1$ (not $OR=0$) is the "no effect" point; misreading $OR<1$ as "a small negative effect" instead of correctly computing the percentage change $(OR-1)\times100\%$ is a common mistake for those new to odds ratios.</span>

## 15. Kết nối với phần còn lại của khóa học - <span class="en">Connections to the rest of the course</span>

Trang này là nền tảng cho toàn bộ **Part 2: Models for Limited Dependent Variables**:
<br><span class="en">This page is the foundation for all of **Part 2: Models for Limited Dependent Variables**:</span>

- Khung ML + latent-variable + LR/Wald test + marginal effects (MEM/AME) dựng ở đây được **tái sử dụng gần như nguyên vẹn** ở [[concepts/multinomial-logit-model]] (mở rộng sang nhiều lựa chọn không thứ tự — softmax thay cho logistic hai lựa chọn) và [[concepts/ordinal-response-models]] (mở rộng sang lựa chọn có thứ tự — latent variable với nhiều cutpoint).
  <br><span class="en">The ML + latent-variable + LR/Wald test + marginal effects (MEM/AME) framework built here is **reused almost unchanged** in [[concepts/multinomial-logit-model]] (extended to multiple unordered choices — softmax replacing two-choice logistic) and [[concepts/ordinal-response-models]] (extended to ordered choices — a latent variable with multiple cutpoints).</span>
- [[concepts/count-data-models]] và [[concepts/censored-regression-tobit]] cũng dùng chung triết lý ML thay OLS khi biến phụ thuộc không còn liên tục "sạch" theo nghĩa LRM cổ điển.
  <br><span class="en">[[concepts/count-data-models]] and [[concepts/censored-regression-tobit]] also share the same "use ML instead of OLS" philosophy once the dependent variable is no longer "cleanly" continuous in the classical LRM sense.</span>
- LPM ở mục 4 là điểm đối chiếu ngược trực tiếp với [[concepts/linear-regression-model]] — cùng một công cụ OLS, nhưng áp lên biến nhị phân bộc lộ rõ giới hạn của khung tuyến tính, đúng như phần "5 giả định A1–A5" đã cảnh báo trước ở trang đó.
  <br><span class="en">The LPM in section 4 is a direct point of comparison back to [[concepts/linear-regression-model]] — the same OLS tool, but applied to a binary variable clearly exposes the limits of the linear framework, exactly as the "5 assumptions A1–A5" section of that page warned in advance.</span>
- Vấn đề heteroskedasticity "bẩm sinh" của LPM (mục 4.4, nhược điểm #3) là một minh họa cụ thể, thực chứng cho toàn bộ nội dung lý thuyết ở [[concepts/heteroskedasticity]] — đáng đọc song song nếu cần hiểu sâu hơn tại sao robust SE lại cần thiết.
  <br><span class="en">The LPM's "built-in" heteroskedasticity problem (section 4.4, drawback #3) is a concrete, empirical illustration of the entire theoretical content in [[concepts/heteroskedasticity]] — worth reading alongside it for a deeper understanding of why robust SE is necessary.</span>
