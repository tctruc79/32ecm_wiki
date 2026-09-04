---
title: "Lecture 1: Linear Regression Model"
type: concept
status: mature
tags: [linear-regression, ols, hypothesis-testing, foundations]
sources: ["[[sources/slides-1-linear-regression-model]]"]
related: ["[[concepts/econometrics-overview]]", "[[concepts/functional-forms]]", "[[concepts/multicollinearity]]", "[[concepts/heteroskedasticity]]", "[[concepts/endogeneity-iv-regression]]"]
lecture: 1
assignment: []
updated: 2026-09-04
---

> **Cách đọc trang này**: đây là trang nền của toàn bộ môn — mọi topic sau (Topic 2–14) đều là một biến thể hoặc một cách vá lỗi của mô hình ở đây. Nếu ôn thi/ôn luận văn mà chỉ có thời gian đọc kỹ một trang, hãy đọc trang này trước. Phần lý luận "tại sao cần ceteris paribus, correlation ≠ causation" được nói kỹ hơn ở [[concepts/econometrics-overview]] — trang này tập trung vào **cơ chế kỹ thuật**: OLS là gì, ước lượng ra sao, và làm sao biết được ước lượng đó có đáng tin không.
> <br><span class="en">**How to read this page**: this is the foundational page for the entire course — every later topic (Topic 2–14) is a variant of, or a patch for, the model presented here. If you only have time to carefully read one page while reviewing for the exam or thesis, read this one first. The reasoning behind "why we need ceteris paribus, correlation ≠ causation" is discussed in more depth in [[concepts/econometrics-overview]] — this page focuses on the **technical mechanics**: what OLS is, how it is estimated, and how to know whether that estimate is trustworthy.</span>

**Lecture 1** trong đề cương (CO Topic 1) — chưa có assignment riêng.
<br><span class="en">**Lecture 1** in the syllabus (CO Topic 1) — no dedicated assignment yet.</span>

## 1. Vì sao cần một "mô hình"? — PRE và SRE - <span class="en">Why do we need a "model"? — PRE and SRE</span>

Xuất phát điểm không phải là công thức, mà là một **câu hỏi kinh tế** cần trả lời bằng lý thuyết. Ví dụ thầy dùng để mở đầu: Mincer (1974) lý thuyết hóa rằng lương phụ thuộc dương vào giáo dục (và có thể cả kinh nghiệm làm việc). Econometrics không phải là "vẽ một đường thẳng xuyên qua các điểm dữ liệu một cách mù quáng" — nó là công cụ để **kiểm định và định lượng** một lý thuyết đã có sẵn.
<br><span class="en">The starting point is not a formula, but an **economic question** that needs to be answered through theory. The example the professor uses as an opener: Mincer (1974) theorized that wages depend positively on education (and possibly work experience too). Econometrics is not "blindly drawing a straight line through data points" — it is a tool to **test and quantify** an existing theory.</span>

Để kiểm định ý tưởng "giáo dục → lương", ta hình thức hóa nó thành một phương trình:
<br><span class="en">To test the idea "education → wages," we formalize it into an equation:</span>

$$y_i = \beta_0 + \beta_1 X_{1i} + \beta_2 X_{2i} + \cdots + \beta_k X_{ki} + \varepsilon_i$$

Đây gọi là **Population Regression Equation (PRE)** — phương trình ở cấp độ **dân số/tổng thể** (population), tức quan hệ lý thuyết "thật" mà ta muốn biết nhưng không bao giờ quan sát được trực tiếp, vì không ai có dữ liệu của *toàn bộ* dân số. Từng thành phần:
<br><span class="en">This is called the **Population Regression Equation (PRE)** — the equation at the **population** level, i.e. the "true" theoretical relationship we want to know but can never observe directly, since no one has data on the *entire* population. Each component:</span>

- $y_i$: biến phụ thuộc (outcome) của cá nhân/đơn vị $i$ — ví dụ lương.
<br><span class="en">$y_i$: the dependent variable (outcome) of individual/unit $i$ — for example, wages.</span>
- $X_{1i}, X_{2i}, \dots$: các biến độc lập, phải có **cơ sở lý thuyết** (không phải nhét đại vào cho có) — ví dụ số năm đi học, số năm kinh nghiệm.
<br><span class="en">$X_{1i}, X_{2i}, \dots$: the independent variables, which must have a **theoretical basis** (not just thrown in arbitrarily) — for example, years of schooling, years of experience.</span>
- $\beta_0$: hệ số chặn (intercept) — giá trị kỳ vọng của $y$ khi mọi $X=0$.
<br><span class="en">$\beta_0$: the intercept — the expected value of $y$ when all $X=0$.</span>
- $\beta_1, \beta_2, \dots$: hệ số góc (slope coefficients) — còn gọi là **marginal effects**, đo mức thay đổi của $y$ khi $X$ tương ứng tăng 1 đơn vị, giữ các biến khác không đổi.
<br><span class="en">$\beta_1, \beta_2, \dots$: the slope coefficients — also called **marginal effects**, measuring the change in $y$ when the corresponding $X$ increases by 1 unit, holding other variables constant.</span>
- $\varepsilon_i$: sai số (error term) — mọi ảnh hưởng lên $y_i$ mà mô hình **không quan sát được**.
<br><span class="en">$\varepsilon_i$: the error term — every influence on $y_i$ that the model **cannot observe**.</span>

Vì $\beta$ không bao giờ quan sát được trực tiếp, trong thực tế ta chỉ có một **mẫu** (sample) dữ liệu, và dùng nó để ước lượng. Phương trình tương ứng ở cấp độ mẫu:
<br><span class="en">Because $\beta$ can never be observed directly, in practice we only have a **sample** of data, and we use it to estimate. The corresponding equation at the sample level:</span>

$$y_i = b_0 + b_1 X_{1i} + \cdots + b_k X_{ki} + e_i, \qquad e_i = y_i - \hat y_i$$

gọi là **Sample Regression Equation (SRE)**. Khác biệt cốt lõi cần nhớ:
<br><span class="en">is called the **Sample Regression Equation (SRE)**. The core difference to keep in mind:</span>

| | Cấp độ<br><span class="en">Level</span> | Ký hiệu hệ số<br><span class="en">Coefficient notation</span> | Ký hiệu sai số/phần dư<br><span class="en">Error/residual notation</span> | Quan sát được?<br><span class="en">Observable?</span> |
|---|---|---|---|---|
| PRE | Population (dân số)<br><span class="en">Population</span> | $\beta$ (Hy Lạp)<br><span class="en">$\beta$ (Greek)</span> | $\varepsilon$ | Không — chỉ tồn tại trong lý thuyết<br><span class="en">No — exists only in theory</span> |
| SRE | Sample (mẫu)<br><span class="en">Sample</span> | $b$ (La-tinh, đôi khi viết $\hat\beta$)<br><span class="en">$b$ (Latin, sometimes written $\hat\beta$)</span> | $e$ (residual — phần dư)<br><span class="en">$e$ (residual)</span> | Có — tính được từ dữ liệu<br><span class="en">Yes — computable from data</span> |

$b$ chính là **best guess** (ước đoán tốt nhất) của $\beta$ chưa quan sát được, dựa trên mẫu dữ liệu đang có. Câu hỏi tiếp theo, tự nhiên: **ước lượng $b$ bằng cách nào?**
<br><span class="en">$b$ is precisely the **best guess** of the unobserved $\beta$, based on the sample data at hand. The next, natural question: **how do we estimate $b$?**</span>

## 2. OLS Estimator — trực giác trước, công thức sau - <span class="en">The OLS Estimator — intuition first, formula second</span>

### 2.1 Trực giác - <span class="en">Intuition</span>

Với mỗi cách chọn $b$, ta có thể tính được giá trị dự đoán $\hat y_i = bX_i$ cho từng quan sát, và so nó với giá trị thật $y_i$. Khoảng cách giữa hai giá trị này là **phần dư** (residual):
<br><span class="en">For any choice of $b$, we can compute the predicted value $\hat y_i = bX_i$ for each observation and compare it to the true value $y_i$. The distance between these two values is the **residual**:</span>

$$e_i = y_i - \hat y_i = y_i - bX_i$$

Hình dung trên đồ thị: đây chính là khoảng cách theo chiều dọc (vertical gap) giữa điểm dữ liệu thật và đường hồi quy. **OLS (Ordinary Least Squares)** chọn $b$ sao cho các khoảng cách này, tính chung toàn bộ mẫu, là **nhỏ nhất có thể**:
<br><span class="en">Picture it on a graph: this is exactly the vertical gap between the true data point and the regression line. **OLS (Ordinary Least Squares)** chooses $b$ so that these gaps, taken together across the whole sample, are **as small as possible**:</span>

$$\min_b \sum_{i=1}^N e_i^2 = \sum_{i=1}^N (y_i - bX_i)^2$$

Tại sao **bình phương** phần dư thay vì cộng trực tiếp hay lấy trị tuyệt đối? Hai lý do trực giác: (1) nếu cộng trực tiếp, phần dư dương và âm sẽ triệt tiêu lẫn nhau, một đường "tệ" (đi lệch nhiều nhưng lệch đều hai phía) có thể trông giống một đường "tốt"; (2) bình phương phạt nặng hơn những sai số lớn — một quan sát lệch xa bị phạt nặng hơn nhiều quan sát lệch gần, hợp lý với trực giác "muốn đường dự đoán bám sát dữ liệu nói chung".
<br><span class="en">Why **square** the residuals instead of summing them directly or taking absolute values? Two intuitive reasons: (1) if summed directly, positive and negative residuals would cancel each other out, so a "bad" line (deviating a lot but evenly on both sides) could look like a "good" line; (2) squaring penalizes large errors more heavily — one observation that deviates far is penalized much more than many observations that deviate slightly, which matches the intuition of "wanting the predicted line to track the data closely overall".</span>

### 2.2 Dạng đóng (graduate level) - <span class="en">Closed-form solution (graduate level)</span>

Viết lại bài toán tối thiểu hóa dưới dạng ma trận, với $e'e$ là tổng bình phương phần dư:
<br><span class="en">Rewrite the minimization problem in matrix form, with $e'e$ as the sum of squared residuals:</span>

$$e'e = (y-Xb)'(y-Xb) = y'y - 2bX'y + b'X'Xb$$

Lấy đạo hàm theo $b$, cho bằng 0 để tìm cực tiểu (điều kiện bậc nhất — first order condition):
<br><span class="en">Take the derivative with respect to $b$ and set it to 0 to find the minimum (the first order condition):</span>

$$\frac{\partial e'e}{\partial b} = -2X'y + 2X'Xb = 0 \;\;\Rightarrow\;\; X'Xb = X'y$$

Giải ra nghiệm dạng đóng (closed-form solution) — đây chính là **OLS estimator**:
<br><span class="en">Solving gives the closed-form solution — this is precisely the **OLS estimator**:</span>

$$b = (X'X)^{-1}X'y$$

Không cần nhớ cách chứng minh nếu không học sâu về ma trận — điều quan trọng cần nhớ là: OLS không phải một "thủ thuật" tùy ý, mà là **nghiệm duy nhất** của bài toán tối ưu hóa "cực tiểu tổng bình phương phần dư". Điều kiện để nghiệm này tồn tại (ma trận $X'X$ khả nghịch) chính là nội dung của giả định A2 ở phần dưới.
<br><span class="en">There's no need to memorize the derivation if you haven't studied matrix algebra in depth — what matters is remembering that OLS is not an arbitrary "trick," but the **unique solution** to the optimization problem of "minimizing the sum of squared residuals." The condition for this solution to exist (the matrix $X'X$ being invertible) is precisely the content of assumption A2 below.</span>

## 3. Ví dụ xuyên suốt: Forest coverage & Storm damages - <span class="en">Running example: Forest coverage & Storm damages</span>

Đây là bộ dữ liệu thầy Thụy dùng xuyên suốt slide Topic 1 để minh họa mọi khái niệm — cần nắm để hiểu các ví dụ số ở các phần sau.
<br><span class="en">This is the dataset Professor Thụy uses throughout the Topic 1 slides to illustrate every concept — it's important to understand it in order to follow the numerical examples in later sections.</span>

**Bối cảnh nghiên cứu**: thiệt hại do bão gây tổn thất lớn cho cộng đồng. Có hai nhóm đòn bẩy chính sách: bảo vệ tự nhiên (rừng) và chuẩn bị con người (kế hoạch ứng phó). Rừng được kỳ vọng làm giảm thiệt hại vì có tác dụng chắn gió/lũ; kế hoạch ứng phó (cảnh báo sớm, kế hoạch sơ tán) cũng được kỳ vọng làm giảm thiệt hại.
<br><span class="en">**Research context**: storm damage causes major losses for communities. There are two groups of policy levers: natural protection (forest) and human preparedness (response plans). Forests are expected to reduce damage because they block wind/flooding; response plans (early warning, evacuation plans) are also expected to reduce damage.</span>

> Lưu ý của slide gốc: các biến trong bộ dữ liệu này được xây dựng dựa trên các nghiên cứu kinh tế học thảm họa (disaster economics) nhưng đã đơn giản hóa — dữ liệu chỉ phục vụ mục đích học tập, có thể bỏ sót các biến giải thích quan trọng trong thực tế. Tên biến cũng đặt theo quy ước kỹ thuật riêng của khóa học, không phải cách đặt tên khuyến nghị cho công việc thực tế của bạn.
> <br><span class="en">Note from the original slide: the variables in this dataset were constructed based on disaster economics research but have been simplified — the data serves teaching purposes only and may omit explanatory variables that matter in practice. Variable names also follow the course's own technical convention, not a recommended naming scheme for your real-world work.</span>

**Đơn vị phân tích**: các cộng đồng (communities) từng hứng chịu ít nhất 1 cơn bão trong năm vừa qua.
<br><span class="en">**Unit of analysis**: communities that experienced at least 1 storm in the past year.</span>

| Biến<br><span class="en">Variable</span> | Ý nghĩa<br><span class="en">Meaning</span> | Đơn vị<br><span class="en">Unit</span> | Causal hay non-causal?<br><span class="en">Causal or non-causal?</span> |
|---|---|---|---|
| `pdamages` | Thiệt hại tài sản (không tính thiệt hại nhân mạng) — **biến phụ thuộc**<br><span class="en">Property damage (excluding loss of life) — **dependent variable**</span> | nghìn USD<br><span class="en">thousand USD</span> | — |
| `aforest` | Diện tích rừng che phủ<br><span class="en">Forest coverage area</span> | ha | **Causal** |
| `dplan` | Cộng đồng có kế hoạch ứng phó (cảnh báo sớm, sơ tán…) hay không<br><span class="en">Whether the community has a response plan (early warning, evacuation…)</span> | dummy (1/0) | **Causal** |
| `cgdp` | GDP bình quân đầu người<br><span class="en">GDP per capita</span> | nghìn USD/năm<br><span class="en">thousand USD/year</span> | Non-causal |
| `pdens` | Mật độ dân số<br><span class="en">Population density</span> | nghìn người/km²<br><span class="en">thousand people/km²</span> | Non-causal |
| `curban` | Cộng đồng đô thị hay không<br><span class="en">Whether the community is urban</span> | dummy (1/0) | Non-causal |
| `cterrain` | Địa hình: lowland (nền/base), highland, coastal → sinh ra 2 dummy `chighland`, `ccoastal`<br><span class="en">Terrain: lowland (base), highland, coastal → generates 2 dummies `chighland`, `ccoastal`</span> | categorical | Non-causal |

Phân biệt **causal vs. non-causal** ở đây không phải ngẫu nhiên — nó quyết định *ngôn ngữ* được phép dùng khi diễn giải hệ số (xem mục 5). `aforest` và `dplan` được coi là causal vì slide giả định có cơ chế nhân quả trực tiếp, hợp lý về mặt lý thuyết (rừng vật lý chắn gió/lũ; kế hoạch ứng phó vật lý làm giảm tổn thất); các biến còn lại chỉ là **kiểm soát** (controls) — đưa vào để "dọn nhiễu" chứ không phải đối tượng nghiên cứu.
<br><span class="en">Distinguishing **causal vs. non-causal** here is not arbitrary — it determines the *language* allowed when interpreting coefficients (see section 5). `aforest` and `dplan` are treated as causal because the slide assumes a direct causal mechanism that is theoretically plausible (forest physically blocks wind/flooding; a response plan physically reduces losses); the remaining variables are merely **controls** — included to "clean up noise" rather than being the object of study.</span>

**Thống kê mô tả đáng chú ý** (để cảm nhận thang đo trước khi đọc hệ số hồi quy):
<br><span class="en">**Notable descriptive statistics** (to get a feel for the scale before reading the regression coefficients):</span>

- `pdamages`: dao động 38–116 (nghìn USD) — một số cộng đồng thiệt hại nặng hơn hẳn cộng đồng khác.
<br><span class="en">`pdamages`: ranges 38–116 (thousand USD) — some communities suffer far more damage than others.</span>
- `aforest`: trung bình ≈ 1.51 ha, dao động 0–6.3 — có cộng đồng hoàn toàn không có rừng, có cộng đồng rừng che phủ đáng kể.
<br><span class="en">`aforest`: mean ≈ 1.51 ha, ranging 0–6.3 — some communities have no forest at all, others have substantial forest coverage.</span>
- `dplan`: chỉ 28% cộng đồng có kế hoạch ứng phó.
<br><span class="en">`dplan`: only 28% of communities have a response plan.</span>

**Kết quả hồi quy OLS đầy đủ** (đây là bảng số sẽ được dùng lại xuyên suốt các mục t-test, F-test bên dưới):
<br><span class="en">**Full OLS regression results** (this table of numbers will be reused throughout the t-test and F-test sections below):</span>

| Biến<br><span class="en">Variable</span> | Hệ số ước lượng ($b$)<br><span class="en">Estimated coefficient ($b$)</span> | Đúng kỳ vọng lý thuyết?<br><span class="en">Matches theoretical expectation?</span> |
|---|---|---|
| `aforest` (causal) | −5.363 | ✅ nhiều rừng hơn → ít thiệt hại hơn<br><span class="en">✅ more forest → less damage</span> |
| `dplan` (causal) | −1.99 | ✅ có kế hoạch ứng phó → ít thiệt hại hơn<br><span class="en">✅ having a response plan → less damage</span> |
| `cgdp` (non-causal) | +0.450 | ✅ GDP cao hơn → thiệt hại cao hơn (nhiều tài sản hơn để mất)<br><span class="en">✅ higher GDP → higher damage (more assets to lose)</span> |
| `pdens` (non-causal) | −2.62 | ❌ trái kỳ vọng ban đầu (mật độ cao hơn lại thiệt hại thấp hơn)<br><span class="en">❌ contrary to the initial expectation (higher density yet lower damage)</span> |
| `curban` (non-causal) | +0.426 | — |
| `chighland` (non-causal) | −0.194 | — |
| `ccoastal` (non-causal) | +2.24 | ✅ ven biển phơi nhiễm bão nhiều hơn<br><span class="en">✅ coastal areas are more exposed to storms</span> |

OLS chỉ cho ta **các con số này** — chưa nói được con số nào "đáng tin cậy về mặt thống kê". Đó là lý do cần giả định OLS (mục 4) và các kiểm định giả thuyết (mục 6–8).
<br><span class="en">OLS only gives us **these numbers** — it doesn't yet tell us which numbers are "statistically reliable." That is why we need the OLS assumptions (section 4) and hypothesis tests (sections 6–8).</span>

## 4. Năm giả định của OLS (A1–A5) — "luật chơi" - <span class="en">The five OLS assumptions (A1–A5) — the "rules of the game"</span>

OLS luôn cho ra một con số $b$, bất kể dữ liệu tốt hay xấu — vấn đề là con số đó có **đáng tin** hay không. Các giả định A1–A5 chính là "luật chơi" quyết định điều đó, theo ba khía cạnh:
<br><span class="en">OLS always produces a number $b$, regardless of whether the data is good or bad — the question is whether that number is **trustworthy**. Assumptions A1–A5 are exactly the "rules of the game" that determine this, along three dimensions:</span>

- **Consistency (tính vững)**: khi cỡ mẫu → ∞, ước lượng hội tụ về giá trị thật. Nói cách khác — càng nhiều dữ liệu, ước lượng càng gần với thực tế.
<br><span class="en">**Consistency**: as sample size → ∞, the estimate converges to the true value. In other words — the more data, the closer the estimate gets to reality.</span>
- **Efficiency (hiệu quả)**: trong nhóm các ước lượng không chệch (unbiased), ước lượng nào có phương sai nhỏ nhất là hiệu quả nhất — nó dùng dữ liệu theo cách "tốt nhất", cho ra ước lượng chụm nhất, chính xác nhất.
<br><span class="en">**Efficiency**: among unbiased estimators, the one with the smallest variance is the most efficient — it uses the data in the "best" way, producing the most precise, most accurate estimate.</span>
- **Inference (suy luận thống kê)**: cho phép làm t-test, F-test, và xây dựng khoảng tin cậy một cách đáng tin cậy.
<br><span class="en">**Inference**: allows t-tests, F-tests, and confidence intervals to be constructed reliably.</span>

| # | Giả định<br><span class="en">Assumption</span> | Nội dung<br><span class="en">Content</span> | Nếu vi phạm<br><span class="en">If violated</span> |
|---|---|---|---|
| A1 | **Linearity** | Mô hình tuyến tính theo **tham số** $\beta$ (biến $X$ có thể phi tuyến — quadratic, log-log — miễn $\beta$ vẫn xuất hiện tuyến tính)<br><span class="en">The model is linear in the **parameters** $\beta$ (the $X$ variables can be nonlinear — quadratic, log-log — as long as $\beta$ still enters linearly)</span> | Xem [[concepts/functional-forms]]<br><span class="en">See [[concepts/functional-forms]]</span> |
| A2 | **Full rank** | Các cột của ma trận $X$ độc lập tuyến tính (không có biến nào là tổ hợp tuyến tính hoàn hảo của các biến khác)<br><span class="en">The columns of matrix $X$ are linearly independent (no variable is a perfect linear combination of the others)</span> | Collinear hoàn hảo → $X'X$ không khả nghịch → $b$ không xác định được (công thức $b=(X'X)^{-1}X'y$ "vỡ"); collinear không hoàn hảo (gần collinear) → xem [[concepts/multicollinearity]]<br><span class="en">Perfect collinearity → $X'X$ is not invertible → $b$ cannot be determined (the formula $b=(X'X)^{-1}X'y$ "breaks"); imperfect collinearity (near-collinear) → see [[concepts/multicollinearity]]</span> |
| A3 | **Exogeneity** | $E(\varepsilon\|X)=0$ — sai số không mang thông tin hệ thống nào liên quan đến $X$, tương đương $X'E(\varepsilon)=0$<br><span class="en">$E(\varepsilon\|X)=0$ — the error term carries no systematic information related to $X$, equivalently $X'E(\varepsilon)=0$</span> | Vi phạm → **endogeneity**, xem [[concepts/endogeneity-iv-regression]]<br><span class="en">If violated → **endogeneity**, see [[concepts/endogeneity-iv-regression]]</span> |
| A4 | **Homoskedasticity** | $Var(\varepsilon\|X) = E(\varepsilon\varepsilon'\|X) = \sigma^2 I$ — phương sai sai số không đổi qua các quan sát<br><span class="en">$Var(\varepsilon\|X) = E(\varepsilon\varepsilon'\|X) = \sigma^2 I$ — the error variance is constant across observations</span> | Vi phạm → xem [[concepts/heteroskedasticity]]<br><span class="en">If violated → see [[concepts/heteroskedasticity]]</span> |
| A5 | **Normality** | $e \sim N(0,\sigma^2)$ | Cần cho suy luận chính xác (exact inference) ở mẫu nhỏ; mẫu lớn thì Central Limit Theorem giúp không cần A5<br><span class="en">Needed for exact inference in small samples; in large samples the Central Limit Theorem means A5 is not required</span> |

**Cách nhớ nhanh, theo "giá trị" mỗi giả định mang lại**: A1–A3 đảm bảo consistency; A4 thêm efficiency (và làm công thức phương sai/VCV đơn giản đi — xem mục 7); A5 cho phép suy luận chính xác ở mẫu nhỏ. Trong thực tế, **A3 và A4 là hai giả định hay bị vi phạm nhất** — đây chính xác là lý do khóa học tiếp tục dạy **robust standard errors** (vá A4) và **instrumental variable (IV) regression** (vá A3) ở các topic sau.
<br><span class="en">**A quick way to remember, by the "value" each assumption provides**: A1–A3 ensure consistency; A4 adds efficiency (and simplifies the variance/VCV formula — see section 7); A5 allows exact inference in small samples. In practice, **A3 and A4 are the two assumptions most often violated** — this is exactly why the course goes on to teach **robust standard errors** (patching A4) and **instrumental variable (IV) regression** (patching A3) in later topics.</span>

## 5. Diễn giải hệ số hồi quy - <span class="en">Interpreting regression coefficients</span>

Cách đọc một hệ số $b_j$ phụ thuộc vào **loại biến**:
<br><span class="en">How to read a coefficient $b_j$ depends on the **type of variable**:</span>

- **Biến liên tục** (continuous, ví dụ `aforest`, `cgdp`): $b_j$ là mức thay đổi của $y$ khi biến độc lập tăng thêm 1 đơn vị, giữ các biến khác không đổi.
<br><span class="en">**Continuous variable** (e.g. `aforest`, `cgdp`): $b_j$ is the change in $y$ when the independent variable increases by 1 unit, holding other variables constant.</span>
- **Biến dummy** (ví dụ `dplan`, `curban`): $b_j$ là **chênh lệch** giá trị $y$ trung bình giữa nhóm mang giá trị 1 và nhóm mang giá trị 0.
<br><span class="en">**Dummy variable** (e.g. `dplan`, `curban`): $b_j$ is the **difference** in average $y$ between the group valued 1 and the group valued 0.</span>
- **Biến phân loại** (categorical, ví dụ `cterrain`): mỗi dummy sinh ra (`chighland`, `ccoastal`) đo chênh lệch $y$ giữa nhóm đang xét và **nhóm nền** (base category — ở đây là `lowland`).
<br><span class="en">**Categorical variable** (e.g. `cterrain`): each generated dummy (`chighland`, `ccoastal`) measures the difference in $y$ between the group in question and the **base category** (here, `lowland`).</span>

Và một lớp quy tắc thứ hai, **độc lập** với loại biến ở trên — quy tắc về **ngôn ngữ diễn giải**:
<br><span class="en">And a second, **independent** set of rules from the variable type above — the rules about **interpretive language**:</span>

- Biến **causal** → được phép diễn giải bằng ngôn ngữ nhân quả ("làm giảm", "làm tăng", "gây ra").
<br><span class="en">**Causal** variables → may be interpreted using causal language ("decreases," "increases," "causes").</span>
- Biến **non-causal** → chỉ được diễn giải bằng ngôn ngữ liên kết ("có liên quan đến", "associated with") — **tuyệt đối không** dùng "cause"/"gây ra", dù hệ số có ý nghĩa thống kê mạnh đến đâu.
<br><span class="en">**Non-causal** variables → may only be interpreted using associative language ("is associated with") — **never** use "cause," no matter how statistically significant the coefficient is.</span>

**Ví dụ đúng/sai — đây là bẫy thi hay gặp nhất của thầy, xuất hiện lặp lại ở hầu hết các topic sau:**
<br><span class="en">**Correct/incorrect examples — this is the professor's most common exam trap, recurring throughout most of the later topics:**</span>

- ✅ (causal, `aforest`): "Dữ liệu cho thấy bằng chứng rằng tăng 1 ha rừng làm giảm thiệt hại 5.363 nghìn USD, trung bình."
<br><span class="en">✅ (causal, `aforest`): "The data show evidence that increasing forest by 1 ha decreases damage by 5.363 thousand USD, on average."</span>
- ✅ (causal, `dplan`): "Có bằng chứng rằng việc có kế hoạch ứng phó làm giảm thiệt hại do bão 1.99 nghìn USD, trung bình."
<br><span class="en">✅ (causal, `dplan`): "There is evidence that having a response plan decreases storm damage by 1.99 thousand USD, on average."</span>
- ✅ (non-causal, `cgdp`): "Có bằng chứng rằng cộng đồng có GDP đầu người cao hơn 1 nghìn USD có liên quan đến thiệt hại cao hơn 0.45 nghìn USD, trung bình."
<br><span class="en">✅ (non-causal, `cgdp`): "There is evidence that a community with GDP per capita 1 thousand USD higher is associated with damage that is 0.45 thousand USD higher, on average."</span>
- ✅ (non-causal, `curban`): "Có bằng chứng rằng cộng đồng đô thị trải qua thiệt hại do bão cao hơn trung bình 0.426 nghìn USD so với cộng đồng nông thôn."
<br><span class="en">✅ (non-causal, `curban`): "There is evidence that urban communities experience storm damage that is on average 0.426 thousand USD higher than rural communities."</span>
- ✅ (non-causal, `ccoastal`, chấp nhận được): "Cộng đồng ven biển có thiệt hại do bão cao hơn trung bình 2.24 nghìn USD so với cộng đồng lowland."
<br><span class="en">✅ (non-causal, `ccoastal`, acceptable): "Coastal communities have storm damage that is on average 2.24 thousand USD higher than lowland communities."</span>
- ❌ (proof claim): "Dữ liệu **chứng minh** (prove) rằng ven biển làm tăng thiệt hại đúng 2.24 nghìn USD." — sai vì không kiểm định nào "chứng minh" được điều gì tuyệt đối, chỉ có "bằng chứng" (evidence).
<br><span class="en">❌ (proof claim): "The data **prove** that being coastal increases damage by exactly 2.24 thousand USD." — wrong because no test can "prove" anything absolutely, only provide "evidence."</span>
- ❌ (causal claim cho biến non-causal): "Ven biển **làm tăng** (increases) thiệt hại." — sai vì `ccoastal` là biến non-causal, dù hệ số dương và có ý nghĩa thống kê, chỉ được nói "có liên quan đến" (associated with).
<br><span class="en">❌ (causal claim for a non-causal variable): "Being coastal **increases** damage." — wrong because `ccoastal` is a non-causal variable; even though the coefficient is positive and statistically significant, one may only say it "is associated with" damage.</span>

## 6. Độ bất định của ước lượng: VCV matrix và Standard Error - <span class="en">Uncertainty of the estimate: the VCV matrix and Standard Error</span>

Trước khi kiểm định giả thuyết, cần một câu hỏi trung gian: OLS cho ta một con số $b$ (point estimate — ước lượng điểm), nhưng nếu ta rút một mẫu dữ liệu **khác** (cùng dân số, khác quan sát), $b$ sẽ ra một con số **khác**. Vậy làm sao đo được mức độ "dao động" này?
<br><span class="en">Before hypothesis testing, we need an intermediate question: OLS gives us a number $b$ (a point estimate), but if we drew a **different** sample of data (same population, different observations), $b$ would come out **different**. So how do we measure this degree of "fluctuation"?</span>

### 6.1 Variance-covariance (VCV) matrix — graduate level - <span class="en">Variance-covariance (VCV) matrix — graduate level</span>

$$Var(b) = \sigma^2(X'X)^{-1} = \begin{pmatrix} Var(b_1) & \cdots & Cov(b_1,b_k) \\ \vdots & \ddots & \vdots \\ Cov(b_k,b_1) & \cdots & Var(b_k) \end{pmatrix}, \qquad \hat\sigma^2 = \frac{e'e}{n-k}$$

Đây là ma trận $k\times k$: phần tử trên đường chéo là phương sai của từng $b_j$; phần tử ngoài đường chéo là hiệp phương sai (covariance) giữa các cặp ước lượng. Công thức đơn giản $\sigma^2(X'X)^{-1}$ này **chỉ đúng dưới giả định A4 (homoskedasticity)** — đây là lý do A4 quan trọng: nó giúp công thức VCV/SE đơn giản đi rất nhiều; khi A4 bị vi phạm, phải dùng robust SE (xem [[concepts/heteroskedasticity]]).
<br><span class="en">This is a $k\times k$ matrix: the diagonal elements are the variances of each $b_j$; the off-diagonal elements are the covariances between pairs of estimates. This simple formula $\sigma^2(X'X)^{-1}$ **only holds under assumption A4 (homoskedasticity)** — this is why A4 matters: it simplifies the VCV/SE formula considerably; when A4 is violated, robust SE must be used instead (see [[concepts/heteroskedasticity]]).</span>

### 6.2 Standard Error (SE) — và vì sao nó khác Standard Deviation (SD) - <span class="en">Standard Error (SE) — and why it differs from Standard Deviation (SD)</span>

$$SE(b_j) = \sqrt{Var(b_j)}$$

Đây là điểm hay bị nhầm lẫn nhất của người mới học: **SD và SE đo hai thứ khác nhau**.
<br><span class="en">This is the point beginners confuse most often: **SD and SE measure two different things**.</span>

- **Standard Deviation (SD)**: đo độ phân tán của **dữ liệu quan sát được** ($y$, $X$) — ví dụ, SD của `pdamages` cho biết thiệt hại dao động nhiều hay ít *giữa các cộng đồng* trong mẫu.
<br><span class="en">**Standard Deviation (SD)**: measures the dispersion of the **observed data** ($y$, $X$) — for example, the SD of `pdamages` tells us how much or how little damage varies *across communities* in the sample.</span>
- **Standard Error (SE)**: đo độ phân tán của **ước lượng** $b$ *nếu lặp lại việc lấy mẫu nhiều lần* — SE của $b_{aforest}$ cho biết ước lượng hiệu ứng của rừng sẽ dao động bao nhiêu nếu ta rút một mẫu dữ liệu khác từ cùng dân số.
<br><span class="en">**Standard Error (SE)**: measures the dispersion of the **estimate** $b$ *if the sampling were repeated many times* — the SE of $b_{aforest}$ tells us how much the estimated forest effect would fluctuate if we drew a different sample of data from the same population.</span>

SE nhỏ → ước lượng chụm (precise); SE lớn → ước lượng "ồn" (noisy), kém tin cậy. SE chính là "thước đo độ bất định" dùng trong mọi kiểm định giả thuyết ở các mục tiếp theo.
<br><span class="en">A small SE → a precise estimate; a large SE → a "noisy," less reliable estimate. SE is exactly the "measure of uncertainty" used in every hypothesis test in the following sections.</span>

## 7. Kiểm định giả thuyết cho một hệ số: t-test - <span class="en">Hypothesis testing for a single coefficient: the t-test</span>

### 7.1 Vì sao dùng ngôn ngữ "bằng chứng" thay vì "chứng minh" - <span class="en">Why we use the language of "evidence" instead of "proof"</span>

Trong thống kê, ta **không bao giờ chứng minh được** một lý thuyết là đúng tuyệt đối — vì điều đó đòi hỏi sự chắc chắn tuyệt đối, còn dữ liệu mẫu luôn có nhiễu ngẫu nhiên. Thay vào đó, ta tìm **bằng chứng chống lại** giả thuyết ngược lại. Cụ thể, muốn biết "X có ảnh hưởng đến Y không?", ta kiểm định giả thuyết ngược lại — **không có ảnh hưởng** — gọi là **giả thuyết gốc / null hypothesis** $H_0$; đối lập là **giả thuyết thay thế / alternative hypothesis** $H_a$: X có ảnh hưởng. Nếu dữ liệu cho phép **bác bỏ** $H_0$, ta nói có bằng chứng ủng hộ $H_a$ — **không bao giờ** nói "đã chứng minh $H_a$ đúng".
<br><span class="en">In statistics, we can **never prove** a theory to be absolutely true — because that would require absolute certainty, while sample data always contains random noise. Instead, we look for **evidence against** the opposite hypothesis. Specifically, to find out "does X affect Y?", we test the opposite hypothesis — **no effect** — called the **null hypothesis** $H_0$; its opposite is the **alternative hypothesis** $H_a$: X has an effect. If the data allow us to **reject** $H_0$, we say there is evidence supporting $H_a$ — we **never** say "we have proven $H_a$ is true."</span>

Lý do sâu xa: mọi kiểm định thống kê đều dựa trên xác suất. Ngay cả khi bác bỏ $H_0$, vẫn luôn có một xác suất nhỏ ta đã sai — bác bỏ nhầm một $H_0$ thực ra đúng, gọi là **Type I error (sai lầm loại I)**.
<br><span class="en">The deeper reason: every statistical test is based on probability. Even when we reject $H_0$, there is always a small probability that we are wrong — mistakenly rejecting an $H_0$ that is actually true, called **Type I error**.</span>

> **Ẩn dụ của thầy** (đáng nhớ vì hay được nhắc lại xuyên suốt khóa học): bác bỏ $H_0$ giống như tìm thấy dấu vân tay tại hiện trường — bằng chứng mạnh cho thấy nghi phạm không vô tội, nhưng không phải "chứng minh tuyệt đối" tội. **Không bác bỏ** $H_0$ giống như không tìm thấy dấu vân tay — không có nghĩa nghi phạm vô tội, chỉ có nghĩa là chưa đủ bằng chứng để buộc tội.
> <br><span class="en">**The professor's metaphor** (worth remembering since it recurs throughout the course): rejecting $H_0$ is like finding a fingerprint at the crime scene — strong evidence the suspect is not innocent, but not "absolute proof" of guilt. **Failing to reject** $H_0$ is like finding no fingerprint — it does not mean the suspect is innocent, only that there isn't enough evidence to convict.</span>

### 7.2 Công thức và phân phối - <span class="en">Formula and distribution</span>

Kiểm định $H_0: \beta_j = c$ so với $H_a: \beta_j \neq c$ (dạng tổng quát nhất; trường hợp hay gặp nhất là $c=0$, tức "biến này không có ảnh hưởng gì"). Thống kê kiểm định (test statistic):
<br><span class="en">Testing $H_0: \beta_j = c$ against $H_a: \beta_j \neq c$ (the most general form; the most common case is $c=0$, i.e. "this variable has no effect at all"). The test statistic:</span>

$$t = \frac{b_j - c}{SE(b_j)} \sim t_{N-k}$$

t-statistic đo khoảng cách giữa ước lượng $b_j$ và giá trị giả định $c$, tính theo **đơn vị SE** — |t| càng lớn, $b_j$ càng "xa" $c$ một cách bất thường (khó xảy ra do ngẫu nhiên), càng là bằng chứng mạnh chống lại $H_0$. Dưới $H_0$ đúng và các giả định A1–A5 giữ, $t$ tuân theo phân phối Student's t với bậc tự do (degrees of freedom) $df=N-k$ ($N$ = số quan sát, $k$ = số hệ số ước lượng kể cả intercept).
<br><span class="en">The t-statistic measures the distance between the estimate $b_j$ and the hypothesized value $c$, expressed in **SE units** — the larger |t| is, the more unusually "far" $b_j$ is from $c$ (unlikely to occur by chance), and the stronger the evidence against $H_0$. Under $H_0$ being true and assumptions A1–A5 holding, $t$ follows a Student's t distribution with degrees of freedom $df=N-k$ ($N$ = number of observations, $k$ = number of estimated coefficients including the intercept).</span>

Vì $\beta_j$ (giá trị thật) không quan sát được, ta phải dùng ước lượng $b_j$ và SE của nó để tính thống kê kiểm định — đây là lý do cả t-test lẫn F-test luôn xây dựng trên $b$, chưa bao giờ trên $\beta$ trực tiếp.
<br><span class="en">Because $\beta_j$ (the true value) is unobservable, we must use the estimate $b_j$ and its SE to compute the test statistic — this is why both the t-test and the F-test are always built on $b$, never directly on $\beta$.</span>

### 7.3 Ba dạng kiểm định — và vì sao hướng của $H_a$ quan trọng - <span class="en">Three forms of the test — and why the direction of $H_a$ matters</span>

Cùng một t-statistic có thể dẫn đến **ba kết luận khác nhau**, tùy vào $H_a$ đặt ra câu hỏi gì. Minh họa bằng chính $b_{aforest}$ (t = −16.567, $df=945$):
<br><span class="en">The same t-statistic can lead to **three different conclusions**, depending on what question $H_a$ poses. Illustrated with $b_{aforest}$ itself (t = −16.567, $df=945$):</span>

**(a) Two-tailed test** — câu hỏi "X có ảnh hưởng gì không, không quan tâm chiều?" ($H_0: \beta=0$ vs. $H_a: \beta\neq0$). Bác bỏ nếu $|t|>t^*$.
<br><span class="en">**(a) Two-tailed test** — the question "does X have any effect at all, regardless of direction?" ($H_0: \beta=0$ vs. $H_a: \beta\neq0$). Reject if $|t|>t^*$.</span>
- Với $\alpha=5\%$, $df=945$: $t^*=1.96$.
<br><span class="en">With $\alpha=5\%$, $df=945$: $t^*=1.96$.</span>
- $|-16.567| > 1.96$ → **bác bỏ** $H_0$.
<br><span class="en">$|-16.567| > 1.96$ → **reject** $H_0$.</span>
- Kết luận: có bằng chứng rằng rừng che phủ ảnh hưởng đến thiệt hại do bão (không nói rõ chiều).
<br><span class="en">Conclusion: there is evidence that forest coverage affects storm damage (direction unspecified).</span>

**(b) Right-tailed test** — câu hỏi "X có làm **tăng** Y không?" ($H_0: \beta\le0$ vs. $H_a: \beta>0$). Bác bỏ nếu $t>t^*$.
<br><span class="en">**(b) Right-tailed test** — the question "does X **increase** Y?" ($H_0: \beta\le0$ vs. $H_a: \beta>0$). Reject if $t>t^*$.</span>
- Với $\alpha=5\%$, $df=945$ (một đuôi): $t^*=1.65$.
<br><span class="en">With $\alpha=5\%$, $df=945$ (one-tailed): $t^*=1.65$.</span>
- $t=-16.567$, **không** lớn hơn $1.65$ → **không bác bỏ** $H_0$.
<br><span class="en">$t=-16.567$, is **not** greater than $1.65$ → **fail to reject** $H_0$.</span>
- Kết luận: rừng che phủ **không** làm tăng thiệt hại — (hợp lý, vì hệ số âm, không phải dương).
<br><span class="en">Conclusion: forest coverage does **not** increase damage — (makes sense, since the coefficient is negative, not positive).</span>

**(c) Left-tailed test** — câu hỏi "X có làm **giảm** Y không?" ($H_0: \beta\ge0$ vs. $H_a: \beta<0$). Bác bỏ nếu $t<-t^*$.
<br><span class="en">**(c) Left-tailed test** — the question "does X **decrease** Y?" ($H_0: \beta\ge0$ vs. $H_a: \beta<0$). Reject if $t<-t^*$.</span>
- $t=-16.567 < -1.65$ → **bác bỏ** $H_0$.
<br><span class="en">$t=-16.567 < -1.65$ → **reject** $H_0$.</span>
- Kết luận: có bằng chứng rằng rừng che phủ làm **giảm** thiệt hại — khớp với kỳ vọng lý thuyết ban đầu.
<br><span class="en">Conclusion: there is evidence that forest coverage **decreases** damage — consistent with the original theoretical expectation.</span>

**Bài học quan trọng nhất từ ví dụ này**: *cùng một* t-statistic (−16.567) cho ra ba kết luận khác nhau tùy vào câu hỏi ($H_a$) đặt ra là gì. Chọn sai dạng kiểm định (VD dùng right-tailed cho một hiệu ứng thực chất âm) sẽ dẫn đến kết luận "không có bằng chứng" dù thực chất *có* bằng chứng — chỉ là bằng chứng cho chiều ngược lại câu hỏi đặt ra. Luôn đặt câu hỏi nghiên cứu **trước**, rồi mới chọn dạng kiểm định tương ứng — không chọn dạng kiểm định sau khi đã nhìn thấy dấu của hệ số (đó là p-hacking).
<br><span class="en">**The most important lesson from this example**: the *same* t-statistic (−16.567) yields three different conclusions depending on what question ($H_a$) is posed. Choosing the wrong test form (e.g. using right-tailed for an effect that is actually negative) leads to the conclusion "no evidence" even though there actually *is* evidence — just evidence for the opposite direction of the question posed. Always pose the research question **first**, then choose the corresponding test form — never choose the test form after having seen the sign of the coefficient (that is p-hacking).</span>

### 7.4 p-value - <span class="en">p-value</span>

**Định nghĩa**: p-value là xác suất quan sát được một thống kê kiểm định **cực đoan bằng hoặc hơn** giá trị đã quan sát, *với điều kiện* $H_0$ đúng. p-value càng nhỏ → càng khó xảy ra nếu $H_0$ đúng → càng là bằng chứng mạnh chống lại $H_0$. **Quy tắc quyết định**: bác bỏ $H_0$ khi p-value $<\alpha$.
<br><span class="en">**Definition**: the p-value is the probability of observing a test statistic **at least as extreme as** the one observed, *given that* $H_0$ is true. The smaller the p-value → the less likely it is to occur if $H_0$ is true → the stronger the evidence against $H_0$. **Decision rule**: reject $H_0$ when p-value $<\alpha$.</span>

**Ví dụ 1 — hai ngưỡng $\alpha$ cho ra hai kết luận khác nhau** ($b_{pdens}$, two-tailed, $H_0:\beta_{pdens}=0$): $t=-1.932$, p-value $=0.0537$.
<br><span class="en">**Example 1 — two $\alpha$ thresholds yield two different conclusions** ($b_{pdens}$, two-tailed, $H_0:\beta_{pdens}=0$): $t=-1.932$, p-value $=0.0537$.</span>

- Diễn giải trực tiếp của con số: nếu hiệu ứng thật của mật độ dân số bằng 0, xác suất quan sát được một t-statistic cực đoan như $-1.932$ (hoặc hơn) chỉ khoảng 5.4%.
<br><span class="en">Direct interpretation of the number: if the true effect of population density is 0, the probability of observing a t-statistic as extreme as $-1.932$ (or more) is only about 5.4%.</span>
- Ở $\alpha=5\%$: $0.0537 > 0.05$ → **không bác bỏ** $H_0$.
<br><span class="en">At $\alpha=5\%$: $0.0537 > 0.05$ → **fail to reject** $H_0$.</span>
- Ở $\alpha=10\%$: $0.0537 < 0.10$ → **bác bỏ** $H_0$.
<br><span class="en">At $\alpha=10\%$: $0.0537 < 0.10$ → **reject** $H_0$.</span>
- Bài học: kết luận "có ý nghĩa thống kê hay không" **phụ thuộc vào ngưỡng $\alpha$ chọn trước** — một kết quả có thể "đáng kể ở 10%" nhưng "không đáng kể ở 5%". Luôn nêu rõ $\alpha$ đang dùng.
<br><span class="en">Lesson: the conclusion of "statistically significant or not" **depends on the $\alpha$ threshold chosen in advance** — a result may be "significant at 10%" but "not significant at 5%." Always state clearly which $\alpha$ is being used.</span>

**Ví dụ 2 — p-value một đuôi, cùng một biến, hai hướng đối lập** ($b_{cgdp}$, $t_{obs}=2.113$, $df=945$):
<br><span class="en">**Example 2 — one-tailed p-values, same variable, two opposite directions** ($b_{cgdp}$, $t_{obs}=2.113$, $df=945$):</span>

- Right-tailed ($H_0:\beta_{cgdp}\le0$ vs. $H_a:\beta_{cgdp}>0$): p-value $=0.017 < 0.05$ → **bác bỏ** $H_0$ → có bằng chứng cộng đồng GDP đầu người cao hơn trải qua thiệt hại do bão cao hơn.
<br><span class="en">Right-tailed ($H_0:\beta_{cgdp}\le0$ vs. $H_a:\beta_{cgdp}>0$): p-value $=0.017 < 0.05$ → **reject** $H_0$ → there is evidence that communities with higher GDP per capita experience higher storm damage.</span>
- Left-tailed ($H_0:\beta_{cgdp}\ge0$ vs. $H_a:\beta_{cgdp}<0$, cùng $t_{obs}=2.113$): p-value $=0.9826 > 0.05$ → **không bác bỏ** $H_0$ → không đủ bằng chứng cho thấy GDP cao hơn đi cùng thiệt hại thấp hơn.
<br><span class="en">Left-tailed ($H_0:\beta_{cgdp}\ge0$ vs. $H_a:\beta_{cgdp}<0$, same $t_{obs}=2.113$): p-value $=0.9826 > 0.05$ → **fail to reject** $H_0$ → not enough evidence that higher GDP goes with lower damage.</span>
- Ghi chú kỹ thuật: hai p-value một đuôi ($0.017$ và $0.9826$) đối lập nhau trên cùng một $t_{obs}$ luôn cộng lại xấp xỉ 1 (ở đây $0.017+0.9826=0.9996\approx1$, sai lệch nhỏ do làm tròn) — một cách tự kiểm tra nhanh khi tính tay.
<br><span class="en">Technical note: the two opposite one-tailed p-values ($0.017$ and $0.9826$) for the same $t_{obs}$ always sum to approximately 1 (here $0.017+0.9826=0.9996\approx1$, the small discrepancy due to rounding) — a quick self-check when calculating by hand.</span>

### 7.5 Kiểm định với $c\neq0$ — kiểm định một tuyên bố cụ thể, không chỉ "có ảnh hưởng hay không" - <span class="en">Testing with $c\neq0$ — testing a specific claim, not just "is there an effect"</span>

Dạng tổng quát $H_0:\beta_j=c$ hữu ích khi câu hỏi nghiên cứu là một **tuyên bố định lượng cụ thể**, không chỉ "có ảnh hưởng hay không" — đây chính là dạng câu hỏi hay gặp khi viết luận văn ("liệu hiệu ứng có đúng bằng/lớn hơn/nhỏ hơn một ngưỡng cụ thể theo lý thuyết hoặc theo nghiên cứu trước hay không").
<br><span class="en">The general form $H_0:\beta_j=c$ is useful when the research question is a **specific quantitative claim**, not just "is there an effect" — this is precisely the kind of question that comes up when writing a thesis ("whether the effect is exactly equal to/greater than/less than a specific threshold according to theory or prior research").</span>

**Ví dụ**: "Liệu mỗi ha rừng có làm giảm thiệt hại đúng 5 nghìn USD hay không?" — tức $c=-5$ (không phải $c=0$).
<br><span class="en">**Example**: "Does each ha of forest reduce damage by exactly 5 thousand USD?" — i.e. $c=-5$ (not $c=0$).</span>

$$t_{obs} = \frac{b_{aforest}-c}{SE} = \frac{-5.363-(-5)}{0.32} \approx -1.12$$

- **Two-tailed** ($H_0:\beta=-5$ vs. $H_a:\beta\neq-5$): p-value $=0.26>0.05$ → không bác bỏ $H_0$ → dữ liệu **phù hợp** với giả thuyết "mỗi ha rừng giảm đúng 5 nghìn USD thiệt hại".
<br><span class="en">**Two-tailed** ($H_0:\beta=-5$ vs. $H_a:\beta\neq-5$): p-value $=0.26>0.05$ → fail to reject $H_0$ → the data are **consistent** with the hypothesis "each ha of forest reduces damage by exactly 5 thousand USD".</span>
- **Right-tailed** ($H_0:\beta\le-5$ vs. $H_a:\beta>-5$, tức kiểm định "giảm ít hơn 5 nghìn USD"): p-value $=0.868>0.05$ → không bác bỏ → dữ liệu phù hợp với "mỗi ha rừng giảm **ít nhất** 5 nghìn USD".
<br><span class="en">**Right-tailed** ($H_0:\beta\le-5$ vs. $H_a:\beta>-5$, i.e. testing "reduces by less than 5 thousand USD"): p-value $=0.868>0.05$ → fail to reject → the data are consistent with "each ha of forest reduces damage by **at least** 5 thousand USD".</span>
- **Left-tailed** ($H_0:\beta\ge-5$ vs. $H_a:\beta<-5$, tức kiểm định "giảm nhiều hơn 5 nghìn USD"): p-value $=0.131>0.05$ → không bác bỏ → dữ liệu phù hợp với "mỗi ha rừng giảm **nhiều nhất** 5 nghìn USD".
<br><span class="en">**Left-tailed** ($H_0:\beta\ge-5$ vs. $H_a:\beta<-5$, i.e. testing "reduces by more than 5 thousand USD"): p-value $=0.131>0.05$ → fail to reject → the data are consistent with "each ha of forest reduces damage by **at most** 5 thousand USD".</span>

**Bài học diễn giải quan trọng**: cả ba kết luận trên đều là "không bác bỏ $H_0$" — nhưng **không bác bỏ không có nghĩa đã chứng minh $H_0$ đúng**, chỉ có nghĩa dữ liệu **phù hợp/nhất quán** (consistent) với giả thuyết đó, trong khi vẫn có thể phù hợp với nhiều giả thuyết khác. Đây là lỗi diễn giải phổ biến nhất khi làm luận văn: biến "không bác bỏ" thành "đã xác nhận".
<br><span class="en">**Key interpretive lesson**: all three conclusions above are "fail to reject $H_0$" — but **failing to reject does not mean $H_0$ has been proven true**, it only means the data are **consistent** with that hypothesis, while still potentially being consistent with many other hypotheses. This is the most common interpretive error in thesis writing: turning "failed to reject" into "confirmed."</span>

## 8. Kiểm định đồng thời nhiều hệ số: F-test - <span class="en">Testing multiple coefficients jointly: the F-test</span>

### 8.1 Vì sao cần F-test - <span class="en">Why we need the F-test</span>

t-test chỉ xử lý **một hệ số tại một thời điểm**. Nhưng nhiều câu hỏi nghiên cứu đòi hỏi kiểm định **nhiều hệ số cùng lúc** — ví dụ: "địa hình (terrain) có ảnh hưởng gì đến thiệt hại do bão hay không?" — câu hỏi này liên quan đến **cả hai** dummy `chighland` và `ccoastal` cùng lúc, không phải riêng lẻ từng cái.
<br><span class="en">The t-test only handles **one coefficient at a time**. But many research questions require testing **several coefficients simultaneously** — for example: "does terrain affect storm damage at all?" — this question involves **both** dummies `chighland` and `ccoastal` at once, not each one separately.</span>

$$H_0: \beta_{chighland} = \beta_{ccoastal} = 0 \qquad H_a: \text{ít nhất một hệ số} \neq 0$$

### 8.2 Công thức - <span class="en">Formula</span>

So sánh hai mô hình: **unrestricted** (mô hình đầy đủ, có tất cả biến) và **restricted** (mô hình bị ép các hệ số đang kiểm định về giá trị giả định trong $H_0$ — thường là 0).
<br><span class="en">Compare two models: **unrestricted** (the full model, with all variables) and **restricted** (the model with the coefficients under test forced to the value hypothesized in $H_0$ — usually 0).</span>

$$F = \frac{(RSS_r - RSS_u)/q}{RSS_u/(N-k)} \sim F_{q,\,N-k}$$

- $RSS_r$: tổng bình phương phần dư (RSS) của mô hình **restricted**.
<br><span class="en">$RSS_r$: the residual sum of squares (RSS) of the **restricted** model.</span>
- $RSS_u$: RSS của mô hình **unrestricted**.
<br><span class="en">$RSS_u$: the RSS of the **unrestricted** model.</span>
- $q$: số hệ số đang bị kiểm định cùng lúc (ở ví dụ trên, $q=2$).
<br><span class="en">$q$: the number of coefficients being tested jointly (in the example above, $q=2$).</span>

**Trực giác**: nếu ép các hệ số về 0 mà RSS tăng lên **nhiều** ($RSS_r$ lớn hơn hẳn $RSS_u$), nghĩa là các biến đó thực sự đóng góp vào việc giải thích $y$ → bằng chứng chống lại $H_0$ → F lớn. Nếu ép về 0 mà RSS gần như không đổi, các biến đó "không làm gì nhiều" → F nhỏ, không bác bỏ được $H_0$.
<br><span class="en">**Intuition**: if forcing the coefficients to 0 makes RSS increase **a lot** ($RSS_r$ much larger than $RSS_u$), it means those variables really do contribute to explaining $y$ → evidence against $H_0$ → a large F. If forcing them to 0 leaves RSS nearly unchanged, those variables "aren't doing much" → a small F, $H_0$ cannot be rejected.</span>

### 8.3 Dạng tổng quát — không chỉ kiểm định "= 0" - <span class="en">General form — not just testing "= 0"</span>

F-test kiểm định được **bất kỳ ràng buộc tuyến tính nào** trên các hệ số, không chỉ ép về 0:
<br><span class="en">The F-test can test **any linear restriction** on the coefficients, not just forcing them to 0:</span>

$$H_0: R\beta = r$$

với $R$ là ma trận ràng buộc, $r$ là vector hằng số. Hai ví dụ minh họa (dạng câu hỏi hay gặp khi làm luận văn thực nghiệm):
<br><span class="en">where $R$ is the restriction matrix and $r$ is a constant vector. Two illustrative examples (question forms commonly seen in empirical thesis work):</span>

- **Constant returns to scale** (lợi suất không đổi theo quy mô, mô hình sản xuất): $H_0: \beta_K + \beta_L = 1$.
<br><span class="en">**Constant returns to scale** (a production-function model): $H_0: \beta_K + \beta_L = 1$.</span>
- **Equality of effects** (hai biến có hiệu ứng bằng nhau): $H_0: \beta_{aforest} = \beta_{dplan}$ — ví dụ kiểm định liệu 1 ha rừng và 1 đơn vị "có kế hoạch ứng phó" có tác dụng giảm thiệt hại như nhau hay không.
<br><span class="en">**Equality of effects** (two variables having equal effects): $H_0: \beta_{aforest} = \beta_{dplan}$ — for example, testing whether 1 ha of forest and 1 unit of "having a response plan" reduce damage by the same amount.</span>

### 8.4 Diễn giải kết quả F-test — bảng correct/acceptable/wrong - <span class="en">Interpreting F-test results — a correct/acceptable/wrong table</span>

Đây là phần giàu bẫy thi nhất của toàn bộ mục F-test, nên trình bày dạng bảng đối chiếu:
<br><span class="en">This is the part of the whole F-test section richest in exam traps, so it is presented as a comparison table:</span>

**Khi F-test có ý nghĩa thống kê (significant):**
<br><span class="en">**When the F-test is statistically significant:**</span>

| Cách nói<br><span class="en">Statement</span> | Đúng/Sai<br><span class="en">Correct/Wrong</span> | Vì sao<br><span class="en">Why</span> |
|---|---|---|
| "Có đủ bằng chứng cho thấy ít nhất một trong các hệ số đang kiểm định khác 0."<br><span class="en">"There is sufficient evidence that at least one of the coefficients under test is nonzero."</span> | ✅ Đúng<br><span class="en">✅ Correct</span> | Đây chính xác là những gì F-test kiểm định<br><span class="en">This is exactly what the F-test tests</span> |
| "Kết quả kiểm định chứng minh cả hai hệ số đều khác 0 về mặt thống kê."<br><span class="en">"The test result proves both coefficients are statistically nonzero."</span> | ❌ Sai<br><span class="en">❌ Wrong</span> | F-test chỉ nói "ít nhất một", không nói "cả hai" — muốn biết từng hệ số riêng lẻ phải quay lại t-test cho từng biến<br><span class="en">The F-test only says "at least one," not "both" — to know about each coefficient individually, one must go back to the t-test for each variable</span> |

**Khi F-test không có ý nghĩa thống kê (insignificant):**
<br><span class="en">**When the F-test is not statistically significant:**</span>

| Cách nói<br><span class="en">Statement</span> | Đúng/Sai<br><span class="en">Correct/Wrong</span> | Vì sao<br><span class="en">Why</span> |
|---|---|---|
| "Không có đủ bằng chứng đáng tin cậy cho thấy nhóm biến này có ảnh hưởng đồng thời."<br><span class="en">"There is not enough reliable evidence that this group of variables has a joint effect."</span> | ✅ Đúng<br><span class="en">✅ Correct</span> | Diễn giải chuẩn xác<br><span class="en">Accurate interpretation</span> |
| "Được chứng minh rằng cả hai hệ số đều khác 0 một cách riêng lẻ."<br><span class="en">"It has been proven that both coefficients are individually nonzero."</span> | ❌ Sai<br><span class="en">❌ Wrong</span> | Ngược hoàn toàn với kết quả — F-test không có ý nghĩa nghĩa là *không* có bằng chứng, chưa nói gì đến "chứng minh"<br><span class="en">Completely contrary to the result — an insignificant F-test means there is *no* evidence, let alone "proof"</span> |

### 8.5 Trường hợp đặc biệt: F-test cho overall significance - <span class="en">Special case: the F-test for overall significance</span>

Trường hợp đặc biệt khi $q=k$ (kiểm định **toàn bộ** hệ số góc cùng lúc, trừ intercept):
<br><span class="en">A special case when $q=k$ (testing **all** slope coefficients jointly, excluding the intercept):</span>

$$H_0: \beta_1=\beta_2=\cdots=\beta_k=0$$

F có ý nghĩa thống kê ở đây **chỉ** cho biết: các biến giải thích **không phải tất cả** đều vô nghĩa — nó **không** kiểm tra được (và do đó **không được** diễn giải là):
<br><span class="en">A statistically significant F here **only** tells us: the explanatory variables are **not all** meaningless — it **cannot** test (and therefore **must not** be interpreted as):</span>

- Mô hình có **đặc tả đúng** (correct specification) — functional form đúng, không thiếu biến quan trọng, tuyến tính theo tham số — hay không.
<br><span class="en">Whether the model has the **correct specification** — correct functional form, no important omitted variables, linear in parameters.</span>
- Các biến được chọn có phải là biến "đúng" cần đưa vào hay không — việc chọn biến phải dựa trên **lý thuyết**, không dựa vào F-test.
<br><span class="en">Whether the chosen variables are the "right" ones to include — variable selection must be based on **theory**, not on the F-test.</span>
- Các giả định OLS (A1–A5) có được thỏa mãn hay không — F-test không kiểm tra exogeneity, homoskedasticity...
<br><span class="en">Whether the OLS assumptions (A1–A5) are satisfied — the F-test does not check exogeneity, homoskedasticity...</span>
- Mô hình có **hữu ích cho dự báo hoặc chính sách** hay không — F-test không đo độ chính xác dự báo hay mức độ liên quan đến chính sách.
<br><span class="en">Whether the model is **useful for forecasting or policy** — the F-test does not measure forecast accuracy or policy relevance.</span>

Nói ngắn gọn: **"F-test có ý nghĩa" ≠ "mô hình phù hợp" (model is appropriate)** — đây là một trong những cụm từ hay bị lạm dụng nhất khi viết kết quả nghiên cứu, kể cả trong các bài báo đã xuất bản.
<br><span class="en">In short: **"the F-test is significant" ≠ "the model is appropriate"** — this is one of the most overused phrases when writing up research results, even in published papers.</span>

## 9. R² và Adjusted R² — đo độ khớp, không đo độ đúng đắn - <span class="en">R² and Adjusted R² — measuring fit, not correctness</span>

$$R^2 = 1 - \frac{RSS}{TSS}, \qquad TSS=\sum_{i=1}^N y_i^2 - \frac{\left(\sum_{i=1}^N y_i\right)^2}{N}, \qquad 0 \le R^2 \le 1$$

$R^2$ đo **tỷ lệ biến thiên của $y$ được giải thích bởi mô hình hồi quy**. Càng gần 1, mô hình giải thích được càng nhiều biến thiên trong dữ liệu; càng gần 0, giải thích được càng ít.
<br><span class="en">$R^2$ measures the **proportion of variation in $y$ explained by the regression model**. The closer to 1, the more variation in the data the model explains; the closer to 0, the less it explains.</span>

**Vấn đề**: $R^2$ **không bao giờ giảm** khi thêm biến vào mô hình — kể cả khi biến đó hoàn toàn vô nghĩa về mặt lý thuyết. Điều này khiến $R^2$ không công bằng khi so sánh hai mô hình có **số biến khác nhau** — mô hình nhiều biến hơn luôn có $R^2$ ≥ mô hình ít biến hơn, dù không thực sự "tốt hơn".
<br><span class="en">**The problem**: $R^2$ **never decreases** when a variable is added to the model — even when that variable is completely meaningless in theory. This makes $R^2$ unfair when comparing two models with **different numbers of variables** — a model with more variables always has $R^2$ ≥ a model with fewer variables, even though it isn't actually "better."</span>

**Giải pháp — Adjusted R²**, phạt thêm biến:
<br><span class="en">**Solution — Adjusted R²**, which penalizes added variables:</span>

$$R^2_{adj} = 1-(1-R^2)\frac{n-1}{n-k}$$

Khác với $R^2$ thường, $R^2_{adj}$ **có thể giảm** nếu biến mới thêm vào không đóng góp đủ để bù lại "hình phạt" mất thêm một bậc tự do. Vì vậy $R^2_{adj}$ là thước đo phù hợp hơn khi **so sánh các mô hình có số lượng biến khác nhau**.
<br><span class="en">Unlike ordinary $R^2$, $R^2_{adj}$ **can decrease** if a newly added variable doesn't contribute enough to offset the "penalty" of losing an additional degree of freedom. This makes $R^2_{adj}$ a more appropriate measure when **comparing models with different numbers of variables**.</span>

**Điểm quan trọng nhất cần nhớ**: cả $R^2$ và $R^2_{adj}$ chỉ đo **độ khớp (fit)** — mô hình "vẽ" gần dữ liệu quan sát đến đâu — **không hề đo độ đúng đắn (validity)** của các hệ số ước lượng. Một mô hình có thể có $R^2$ rất cao nhưng hệ số hoàn toàn bị chệch (biased) do vi phạm A3 (endogeneity); ngược lại một mô hình $R^2$ thấp vẫn có thể cho hệ số $\beta$ ước lượng chính xác nếu các giả định được thỏa mãn. **$R^2$ cao không phải mục tiêu của econometrics** — mục tiêu là ước lượng đúng hiệu ứng nhân quả/liên kết mà nghiên cứu đặt ra.
<br><span class="en">**The most important point to remember**: both $R^2$ and $R^2_{adj}$ only measure **fit** — how closely the model "traces" the observed data — they do **not** measure the **validity** of the estimated coefficients at all. A model can have a very high $R^2$ but coefficients that are completely biased due to a violation of A3 (endogeneity); conversely, a model with low $R^2$ can still yield accurately estimated $\beta$ coefficients if the assumptions are satisfied. **A high $R^2$ is not the goal of econometrics** — the goal is to correctly estimate the causal/associative effect that the research sets out to answer.</span>

## 10. Bẫy thi tổng hợp (exam traps) - <span class="en">Summary of exam traps</span>

1. Diễn giải hệ số của biến **non-causal** bằng ngôn ngữ nhân quả ("gây ra", "làm tăng/giảm") thay vì ngôn ngữ liên kết ("có liên quan đến").
<br><span class="en">Interpreting a **non-causal** variable's coefficient using causal language ("causes," "increases/decreases") instead of associative language ("is associated with").</span>
2. Dùng từ "chứng minh" (prove/proof) thay vì "có bằng chứng" (there is evidence) — áp dụng cho cả t-test lẫn F-test, không có ngoại lệ.
<br><span class="en">Using the word "prove/proof" instead of "there is evidence" — applies to both the t-test and F-test, no exceptions.</span>
3. Coi "không bác bỏ $H_0$" là "đã chứng minh $H_0$ đúng" — chỉ là "dữ liệu phù hợp với $H_0$", chưa loại trừ được các giả thuyết khác.
<br><span class="en">Treating "fail to reject $H_0$" as "$H_0$ has been proven true" — it only means "the data are consistent with $H_0$," without ruling out other hypotheses.</span>
4. Coi F-test tổng thể có ý nghĩa thống kê nghĩa là "mô hình đúng/phù hợp" (model is appropriate) — F-test không kiểm tra đặc tả mô hình, không kiểm tra giả định OLS, không đo độ hữu ích cho dự báo/chính sách.
<br><span class="en">Treating a statistically significant overall F-test as meaning "the model is correct/appropriate" — the F-test does not check model specification, does not check the OLS assumptions, and does not measure usefulness for forecasting/policy.</span>
5. So sánh $R^2$ (không phải $R^2_{adj}$) giữa hai mô hình có số biến khác nhau.
<br><span class="en">Comparing $R^2$ (rather than $R^2_{adj}$) between two models with different numbers of variables.</span>
6. Chọn hướng kiểm định (two-/right-/left-tailed) **sau khi** đã thấy dấu của hệ số ước lượng, thay vì đặt câu hỏi nghiên cứu trước rồi mới chọn dạng kiểm định — đây là một dạng p-hacking.
<br><span class="en">Choosing the test direction (two-/right-/left-tailed) **after** seeing the sign of the estimated coefficient, instead of posing the research question first and then choosing the test form — this is a form of p-hacking.</span>
7. Nhầm lẫn Standard Error (độ bất định của ước lượng $b$ qua các mẫu khác nhau) với Standard Deviation (độ phân tán của chính dữ liệu).
<br><span class="en">Confusing Standard Error (the uncertainty of the estimate $b$ across different samples) with Standard Deviation (the dispersion of the data itself).</span>
8. Diễn giải "F-test cho nhóm biến có ý nghĩa" thành "mọi hệ số trong nhóm đều có ý nghĩa riêng lẻ" — F-test chỉ đảm bảo "ít nhất một".
<br><span class="en">Interpreting "the F-test for a group of variables is significant" as "every coefficient in the group is individually significant" — the F-test only guarantees "at least one."</span>

## 11. Kết nối với phần còn lại của khóa học - <span class="en">Connections to the rest of the course</span>

Đây là mô hình nền — mọi vi phạm giả định A1–A4 đều mở ra một topic riêng của khóa học:
<br><span class="en">This is the foundational model — every violation of assumptions A1–A4 opens up its own topic in the course:</span>

- **A1 (Linearity)** được nới lỏng sang các dạng phi tuyến → [[concepts/functional-forms]].
<br><span class="en">**A1 (Linearity)** is relaxed toward nonlinear forms → [[concepts/functional-forms]].</span>
- **A2 (Full rank)** gần bị vi phạm (collinear không hoàn hảo) → [[concepts/multicollinearity]].
<br><span class="en">**A2 (Full rank)** is nearly violated (imperfect collinearity) → [[concepts/multicollinearity]].</span>
- **A3 (Exogeneity)** bị vi phạm → endogeneity → [[concepts/endogeneity-iv-regression]] (và mở rộng sang panel data ở [[concepts/iv-regression-panel-data]]).
<br><span class="en">**A3 (Exogeneity)** is violated → endogeneity → [[concepts/endogeneity-iv-regression]] (and extended to panel data in [[concepts/iv-regression-panel-data]]).</span>
- **A4 (Homoskedasticity)** bị vi phạm → [[concepts/heteroskedasticity]].
<br><span class="en">**A4 (Homoskedasticity)** is violated → [[concepts/heteroskedasticity]].</span>
- Toàn bộ khung PRE/SRE, OLS, t-test, F-test ở trang này còn được **mở rộng sang dữ liệu có chiều thời gian** ở [[concepts/fixed-random-effects-model]] (panel data) và **sang biến phụ thuộc không liên tục** ở [[concepts/binary-response-models]] và các trang liên quan.
<br><span class="en">The entire PRE/SRE, OLS, t-test, F-test framework on this page is also **extended to data with a time dimension** in [[concepts/fixed-random-effects-model]] (panel data) and **to non-continuous dependent variables** in [[concepts/binary-response-models]] and related pages.</span>

Câu hỏi triết lý nền tảng "vì sao cần identify được hiệu ứng nhân quả, không chỉ tính hệ số" được bàn kỹ ở [[concepts/econometrics-overview]] — nên đọc trang đó song song nếu cần ôn lại bức tranh tổng thể trước khi đi sâu vào từng kỹ thuật.
<br><span class="en">The foundational philosophical question "why do we need to identify the causal effect, not just compute a coefficient" is discussed in depth in [[concepts/econometrics-overview]] — worth reading alongside this page if you need to review the big picture before diving into individual techniques.</span>

## 12. Tài liệu tham khảo ứng dụng thực tế - <span class="en">Real-world application references</span>

Ba bài báo gần đây minh họa cách linear regression model được dùng trong nghiên cứu kinh tế thực tế (đề cương Lecture 1):
<br><span class="en">Three recent papers illustrating how the linear regression model is used in real-world economic research (Lecture 1 syllabus):</span>

- Peng, Y., Yang, J., Shen, J., & Gou, Q. (2025). Financial outreach, bank deposits, and economic growth. *Journal of Economic Behavior & Organization*, 171, 105036. https://doi.org/10.1016/j.jedc.2025.105036
- Su, Y., Huang, Q., Shu, Q., Wang, Y., & Qi, X. (2025). Mechanism of land trusteeship promoting farmers' collective action: A study based on social-ecological systems framework. *Journal of Rural Studies*, 116, 103622. https://doi.org/10.1016/j.jrurstud.2025.103622
- Yokying, P. (2025). Domestic and international migration, landownership, and rice farming in Cambodia. *Journal of Rural Studies*, 114, 103532. https://doi.org/10.1016/j.jrurstud.2024.103532
