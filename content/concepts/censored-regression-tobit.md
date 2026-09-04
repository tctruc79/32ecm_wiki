---
title: "Lecture 13: Censored Regression: The Tobit Model"
type: concept
status: mature
tags: [tobit, censored-data, truncated-data, limited-dependent-variable]
sources: ["[[sources/slides-11-censored-regression-tobit]]"]
related: ["[[concepts/linear-regression-model]]", "[[concepts/binary-response-models]]"]
lecture: 13
assignment: []
updated: 2026-09-04
---

> **Cách đọc trang này**: đây là bài cuối của Part 2 — Models for Limited Dependent Variables, sau y nhị phân ([[concepts/binary-response-models]]), y đa lựa chọn không thứ tự ([[concepts/multinomial-logit-model]]), y có thứ tự ([[concepts/ordinal-response-models]]) và y đếm ([[concepts/count-data-models]]). Ở đây $y$ quay lại là **liên tục** như [[concepts/linear-regression-model]] — nhưng bị "cắt" ở một ngưỡng. **Phần khó nhất, và theo log ôn tập là "bẫy thi giá trị cao nhất" của topic này, là phân biệt BA loại giá trị dự đoán/marginal effect sau Tobit** (mục 7) — nếu chỉ có thời gian đọc một mục trước khi thi, hãy đọc mục 7. Mục 2 (censored vs. truncated) là nền tảng bắt buộc phải nắm trước, vì nó quyết định mô hình nào được phép dùng.
> <br><span class="en">**How to read this page**: this is the final lesson of Part 2 — Models for Limited Dependent Variables, after binary $y$ ([[concepts/binary-response-models]]), unordered multi-choice $y$ ([[concepts/multinomial-logit-model]]), ordered $y$ ([[concepts/ordinal-response-models]]) and count $y$ ([[concepts/count-data-models]]). Here $y$ goes back to being **continuous** as in [[concepts/linear-regression-model]] — but is "cut" at a threshold. **The hardest part, and per the review log the "highest-value exam trap" of this topic, is distinguishing the THREE types of predicted value/marginal effect after Tobit** (section 7) — if there is only time to read one section before the exam, read section 7. Section 2 (censored vs. truncated) is the mandatory foundation to master first, since it determines which model is allowed to be used.</span>

**Lecture 13** trong đề cương (CO Topic 11) — chưa có assignment riêng. Đây cũng là lecture cuối cùng của khóa.
<br><span class="en">**Lecture 13** in the syllabus (CO Topic 11) — no dedicated assignment yet. This is also the final lecture of the course.</span>

## 1. Vì sao cần một mô hình riêng? — khi $y$ bị "cắt" ở một ngưỡng - <span class="en">Why a dedicated model is needed — when $y$ is "cut" at a threshold</span>

[[concepts/linear-regression-model|OLS]] giả định $y$ là biến liên tục, dao động tự do không giới hạn. Nhưng rất nhiều biến kinh tế có một **điểm chặn tự nhiên** — một ngưỡng mà dưới (hoặc trên) đó, giá trị thật sự không còn được ghi nhận đúng như nó là, mà bị "gán" về một hằng số cố định. Slide gốc liệt kê bốn ví dụ kinh điển:
<br><span class="en">[[concepts/linear-regression-model|OLS]] assumes $y$ is a continuous variable, fluctuating freely without limit. But many economic variables have a **natural bound** — a threshold below (or above) which the true value is no longer recorded as it actually is, but instead "assigned" to a fixed constant. The original slide lists four classic examples:</span>

- **Cổ tức (dividend)**: bằng 0 cho đến khi lợi nhuận công ty đạt một ngưỡng nhất định — dưới ngưỡng đó, công ty không chia cổ tức, dù "khả năng chia cổ tức tiềm ẩn" của công ty có thể âm hay dương khác nhau.
<br><span class="en">**Dividend**: equal to 0 until the company's profit reaches a certain threshold — below that threshold, the company pays no dividend, even though the company's latent "dividend-paying capacity" could differ, positive or negative.</span>
- **Giá cả bị kiểm soát bởi chính phủ (price control)**: giá thị trường "thật" có thể muốn vượt lên trên hoặc xuống dưới mức trần/sàn do nhà nước quy định, nhưng giá quan sát được bị giữ cứng ở mức trần/sàn đó.
<br><span class="en">**Government-controlled price (price control)**: the "true" market price might want to rise above or fall below the ceiling/floor set by the government, but the observed price is held rigidly at that ceiling/floor.</span>
- **Giờ làm việc (working hours)**: bằng 0 với người thất nghiệp — nhưng "mong muốn làm việc" tiềm ẩn của họ vẫn có thể khác nhau giữa người này với người khác, dù quan sát được đều là 0.
<br><span class="en">**Working hours**: equal to 0 for the unemployed — but their latent "desire to work" can still differ from one person to another, even though what is observed is 0 for all of them.</span>
- **Khoản vay (loan)**: bằng 0 nếu đơn xin vay bị từ chối.
<br><span class="en">**Loan**: equal to 0 if the loan application is rejected.</span>

Điểm chung: có một biến "mong muốn" hoặc "khả năng" tiềm ẩn (không quan sát được trực tiếp) — nhưng dữ liệu chỉ ghi nhận được nó khi nó vượt qua một ngưỡng; dưới ngưỡng, mọi thứ đều bị "dán nhãn" giống nhau (thường là 0), bất kể tiềm ẩn bên dưới khác nhau bao nhiêu.
<br><span class="en">The common thread: there is a latent "desire" or "capacity" variable (not directly observable) — but the data only records it once it crosses a threshold; below the threshold, everything is "labeled" the same way (usually 0), regardless of how different the underlying latent value actually is.</span>

**Case study xuyên suốt của slide** (dùng lại ở mục 5 trở đi): **số dư nợ thẻ tín dụng (credit card balance)**. Nhiều khách hàng trả hết dư nợ mỗi tháng hoặc không dùng thẻ để vay → balance quan sát được đúng bằng 0, dù "khuynh hướng vay nợ" tiềm ẩn của họ (phụ thuộc lãi suất, tuổi, giới tính, học vấn) có thể rất khác nhau.
<br><span class="en">**The slide's running case study** (reused from section 5 onward): **credit card balance**. Many customers pay off their balance every month or do not use the card to borrow → the observed balance is exactly 0, even though their latent "borrowing tendency" (depending on interest rate, age, gender, education) can be very different.</span>

## 2. Censored vs. Truncated — phân biệt hai khái niệm hay bị nhầm lẫn nhất - <span class="en">Censored vs. Truncated — distinguishing the two most commonly confused concepts</span>

Đây là bẫy thi cơ bản nhất của topic: hai khái niệm nghe giống nhau, dữ liệu nhìn thoáng qua cũng giống nhau (nhiều giá trị "biến mất" ở một phía), nhưng bản chất — và mô hình phù hợp — hoàn toàn khác nhau.
<br><span class="en">This is the most fundamental exam trap of the topic: the two concepts sound alike, and the data looks alike at a glance too (many values "disappearing" on one side), but the underlying nature — and the appropriate model — are completely different.</span>

### 2.1 Censored data — quan sát được TOÀN BỘ mẫu, giá trị bị "cắt" - <span class="en">Censored data — the ENTIRE sample is observed, values are "cut"</span>

> Định nghĩa của slide: "$y$ is censored if: we can observe all values of $y$, but only in a certain interval, values beyond the interval are recorded as a constant (ví dụ: 0)."
> <br><span class="en">The slide's definition: "$y$ is censored if: we can observe all values of $y$, but only in a certain interval, values beyond the interval are recorded as a constant (e.g.: 0)."</span>

Trực giác: ta **vẫn có mặt đầy đủ của mọi quan sát trong mẫu** — vẫn biết $X_i$ (lãi suất, tuổi, giới tính, học vấn...) của từng người, kể cả những người bị "cắt". Chỉ riêng **giá trị của $y$** đối với những quan sát vượt ra ngoài một khoảng bị thay bằng một hằng số cố định (thường là 0), che mất giá trị "thật" tiềm ẩn bên dưới.
<br><span class="en">Intuition: we **still have the full presence of every observation in the sample** — we still know $X_i$ (interest rate, age, gender, education...) for each person, including those who are "cut." Only the **value of $y$** for observations that fall outside a range is replaced by a fixed constant (usually 0), hiding the "true" latent value underneath.</span>

- $y \ge k$: **censored from below** (censor từ dưới) — mọi giá trị dưới $k$ đều bị gán thành $k$.
<br><span class="en">$y \ge k$: **censored from below** — every value below $k$ is assigned to $k$.</span>
- $y \le k$: **censored from above** (censor từ trên) — mọi giá trị trên $k$ đều bị gán thành $k$.
<br><span class="en">$y \le k$: **censored from above** — every value above $k$ is assigned to $k$.</span>

**Ví dụ cụ thể** (case study của slide — số dư nợ thẻ tín dụng, censored from below tại 0): trong mẫu 2895 khách hàng, ta biết đầy đủ lãi suất, tuổi, giới tính, học vấn của **tất cả** 2895 người — kể cả 1018 người có `balance = 0`. Ta không biết "mức dư nợ mà lẽ ra họ sẽ có nếu được phép âm" (ví dụ, một khách hàng cực kỳ thận trọng về tài chính có thể có "khuynh hướng vay" tiềm ẩn rất âm), nhưng ta biết chắc chắn họ *tồn tại trong mẫu* và biết đặc điểm của họ.
<br><span class="en">**Concrete example** (the slide's case study — credit card balance, censored from below at 0): in the sample of 2895 customers, we fully know the interest rate, age, gender, education of **all** 2895 people — including the 1018 people with `balance = 0`. We don't know "the balance they would have had if it were allowed to be negative" (e.g., an extremely financially cautious customer could have a very negative latent "borrowing tendency"), but we know for certain that they *exist in the sample* and we know their characteristics.</span>

**Ví dụ minh họa bổ sung** (không phải từ slide này, nhưng cùng logic, quen thuộc trong kinh tế lượng — ví dụ gốc của Tobin 1958 về chi tiêu hàng lâu bền/hàng xa xỉ): chi tiêu của một hộ gia đình cho hàng xa xỉ trong năm = 0 với những hộ không mua gì cả, nhưng hộ đó **vẫn có trong mẫu khảo sát**, ta vẫn biết thu nhập, quy mô hộ, v.v. của họ — chỉ riêng "mức sẵn lòng chi tiêu" tiềm ẩn (có thể âm, ví dụ hộ đang nợ nần muốn "chi tiêu âm") bị che bởi ngưỡng 0.
<br><span class="en">**Additional illustrative example** (not from this slide, but same logic, familiar in econometrics — Tobin's 1958 original example on durable/luxury goods spending): a household's annual spending on luxury goods = 0 for households that buy nothing at all, but that household **is still in the survey sample**, we still know its income, household size, etc. — only its latent "willingness to spend" (which could be negative, e.g. an indebted household wanting to "spend negatively") is hidden by the 0 threshold.</span>

### 2.2 Truncated data — toàn bộ QUAN SÁT ngoài khoảng biến mất khỏi mẫu - <span class="en">Truncated data — entire OBSERVATIONS outside the range vanish from the sample</span>

> Định nghĩa của slide: "$y$ is truncated if we can only observe it in the uncensored interval."
> <br><span class="en">The slide's definition: "$y$ is truncated if we can only observe it in the uncensored interval."</span>

Trực giác: khác hẳn censored — ở đây **không phải chỉ giá trị $y$ bị che**, mà **toàn bộ quan sát** (cả $y$ lẫn $X$) của những đơn vị nằm ngoài khoảng quan tâm **không hề xuất hiện trong dữ liệu**. Ta thậm chí không biết họ tồn tại, không có cách nào đếm được có bao nhiêu người bị loại, càng không biết đặc điểm $X$ của họ.
<br><span class="en">Intuition: completely unlike censored — here **it is not just the value of $y$ that is hidden**, but the **entire observation** (both $y$ and $X$) of units outside the range of interest **does not appear in the data at all**. We don't even know they exist, have no way to count how many were excluded, and certainly don't know their $X$ characteristics.</span>

**Ví dụ minh họa** (không phải từ slide này, nhưng cùng logic, phù hợp với gợi ý ôn tập): một khảo sát **chỉ phỏng vấn những hộ gia đình có thu nhập trên một ngưỡng nhất định** (ví dụ khảo sát dành riêng cho "hộ khá giả") — những hộ thu nhập thấp hơn ngưỡng không hề có mặt trong bộ dữ liệu, không phải vì thu nhập của họ bị ghi thành một con số cố định, mà vì họ **chưa từng được đưa vào mẫu**.
<br><span class="en">**Illustrative example** (not from this slide, but same logic, consistent with the review hint): a survey **that only interviews households with income above a certain threshold** (e.g. a survey dedicated to "well-off households") — households with income below the threshold are not present in the dataset at all, not because their income was recorded as a fixed number, but because they **were never included in the sample**.</span>

Slide minh họa sự khác biệt bằng 4 đồ thị phân tán liên tiếp, cùng một tập nền $(x,y)$ với $x \in \{1,...,5\}$, $y \in \{1,...,9\}$:
<br><span class="en">The slide illustrates the difference with 4 consecutive scatter plots, on the same underlying set $(x,y)$ with $x \in \{1,...,5\}$, $y \in \{1,...,9\}$:</span>

1. **"No censoring or truncation"** — toàn bộ điểm dữ liệu gốc, trải đều từ $y=1$ đến $y=9$.
<br><span class="en">**"No censoring or truncation"** — the full set of original data points, spread evenly from $y=1$ to $y=9$.</span>
2. **"Censored from above"** (tại $y=6$) — mọi điểm có $y>6$ trong dữ liệu gốc bị "dồn" xuống nằm đúng tại $y=6$ (nhiều điểm chồng lên nhau ở mức 6), nhưng số lượng điểm trên mỗi giá trị $x$ **không đổi** so với đồ thị gốc.
<br><span class="en">**"Censored from above"** (at $y=6$) — every point with $y>6$ in the original data is "piled" down to sit exactly at $y=6$ (many points overlapping at level 6), but the number of points per $x$ value **is unchanged** compared to the original plot.</span>
3. **"Censored from below"** (tại $y=5$) — tương tự nhưng dồn lên $y=5$ từ dưới.
<br><span class="en">**"Censored from below"** (at $y=5$) — similar but piled up to $y=5$ from below.</span>
4. **"Truncated"** — chỉ còn các điểm có $x \ge 3$ xuất hiện trên đồ thị; toàn bộ điểm có $x=1,2$ **biến mất hoàn toàn**, không dồn về đâu cả.
<br><span class="en">**"Truncated"** — only points with $x \ge 3$ remain visible on the plot; every point with $x=1,2$ **vanishes entirely**, without piling up anywhere.</span>

Quan sát trực quan quan trọng nhất từ 4 đồ thị này: với censored, **mật độ điểm theo $x$ không đổi** (chỉ có $y$ bị "ép phẳng" ở ngưỡng); với truncated, **cả mật độ điểm cũng giảm hẳn** ở phần bị cắt — vì toàn bộ quan sát đó không còn nữa, chứ không phải chỉ $y$ của chúng bị che.
<br><span class="en">The most important visual takeaway from these 4 plots: with censored, **point density by $x$ is unchanged** (only $y$ gets "flattened" at the threshold); with truncated, **point density itself also drops sharply** in the cut portion — because those observations no longer exist at all, not merely that their $y$ is hidden.</span>

### 2.3 Bảng so sánh - <span class="en">Comparison table</span>

| Tiêu chí / <span class="en">Criterion</span> | Censored | Truncated |
|---|---|---|
| Kích thước mẫu / <span class="en">Sample size</span> | Đầy đủ, không đổi / <span class="en">Full, unchanged</span> | Bị thu hẹp — mất hẳn các quan sát ngoài khoảng / <span class="en">Shrunk — observations outside the range are lost entirely</span> |
| Biến độc lập $X$ / <span class="en">Independent variable $X$</span> | Quan sát được cho **mọi** đơn vị, kể cả đơn vị bị cắt / <span class="en">Observed for **every** unit, including cut units</span> | Chỉ quan sát được cho các đơn vị còn nằm trong mẫu / <span class="en">Only observed for units that remain in the sample</span> |
| Giá trị $y$ ngoài khoảng / <span class="en">Value of $y$ outside the range</span> | Gán thành một hằng số cố định (thường 0) / <span class="en">Assigned to a fixed constant (usually 0)</span> | Không tồn tại trong dữ liệu — biến mất hoàn toàn, không phải "0" / <span class="en">Does not exist in the data — vanishes entirely, not a "0"</span> |
| Ta có biết ai bị loại không? / <span class="en">Do we know who was excluded?</span> | Có — biết chính xác đơn vị nào bị censor và đặc điểm $X$ của họ / <span class="en">Yes — we know exactly which units are censored and their $X$ characteristics</span> | Không — không biết họ tồn tại, không đếm được số lượng / <span class="en">No — we don't know they exist, cannot count how many</span> |
| Mô hình phù hợp / <span class="en">Appropriate model</span> | **Tobit** | Truncated regression model (một mô hình khác, không phải Tobit) / <span class="en">Truncated regression model (a different model, not Tobit)</span> |
| Chạy OLS trực tiếp trên $y$ quan sát được / <span class="en">Running OLS directly on observed $y$</span> | Chệch / <span class="en">Biased</span> | Chệch / <span class="en">Biased</span> |

### 2.4 Vì sao Tobit KHÔNG áp dụng được cho dữ liệu truncated - <span class="en">Why Tobit CANNOT be applied to truncated data</span>

> Nguyên văn slide: **"Tobit can not be applied for truncated data."**
> <br><span class="en">The slide's exact wording: **"Tobit can not be applied for truncated data."**</span>

Lý do trực giác: log-likelihood của Tobit (mục 6) được xây dựng bằng cách cộng hai phần — phần mật độ liên tục cho quan sát không bị censor, và phần **xác suất** $\Phi(-X\beta/\sigma)$ cho quan sát bị censor. Để tính được phần xác suất đó, Tobit **cần biết $X$ của chính những quan sát bị censor** — đúng là những gì censored data cung cấp. Với truncated data, những quan sát ngoài khoảng không hề có mặt trong tập dữ liệu, nên không có $X$ nào để đưa vào công thức đó — hàm likelihood của Tobit đơn giản là không áp dụng được. Trường hợp này cần một hàm likelihood khác, có điều kiện hóa theo đúng việc "chỉ quan sát $y$ trong khoảng uncensored" — đó là **truncated regression model**, và xa hơn nữa, khi việc "lọt vào mẫu" bản thân nó tương quan với $y$ theo cách hệ thống (không chỉ đơn thuần là một ngưỡng cắt cứng theo $y$), người ta dùng **Heckman selection model** để xử lý (xem ghi chú phạm vi ở mục 9).
<br><span class="en">The intuitive reason: Tobit's log-likelihood (section 6) is built by adding two parts — a continuous density part for uncensored observations, and a **probability** part $\Phi(-X\beta/\sigma)$ for censored observations. To compute that probability part, Tobit **needs to know $X$ for the very observations that are censored** — exactly what censored data provides. With truncated data, observations outside the range are not present in the dataset at all, so there is no $X$ to plug into that formula — Tobit's likelihood function simply does not apply. This case needs a different likelihood function, conditioned on exactly "$y$ is only observed within the uncensored interval" — that is the **truncated regression model**, and further still, when "making it into the sample" is itself systematically correlated with $y$ (not merely a hard cutoff threshold on $y$), the **Heckman selection model** is used to handle it (see the scope note in section 9).</span>

## 3. Vì sao không dùng OLS trực tiếp trên biến censored? - <span class="en">Why not use OLS directly on a censored variable?</span>

> Nguyên văn slide: **"OLS with censored/truncated dependent variables is biased."**
> <br><span class="en">The slide's exact wording: **"OLS with censored/truncated dependent variables is biased."**</span>

Trực giác cho trường hợp censored (áp dụng tương tự cho truncated): với ví dụ credit card balance, 1018/2895 ≈ 35.2% khách hàng có `balance = 0` — một khối lớn điểm dữ liệu dồn hẳn tại $y=0$. Có hai cách "sai" hay gặp khi cố xử lý bằng OLS thường:
<br><span class="en">The intuition for the censored case (applies similarly to truncated): in the credit card balance example, 1018/2895 ≈ 35.2% of customers have `balance = 0` — a large mass of data points piled exactly at $y=0$. There are two common "wrong" ways of trying to handle this with ordinary OLS:</span>

1. **Chạy OLS trên toàn mẫu, coi 0 là một giá trị $y$ "thật"** — OLS cố kẻ một đường thẳng đi xuyên qua cả khối điểm dồn ở 0 lẫn phần dữ liệu dương phía trên. Vì khối điểm ở 0 kéo đường hồi quy "phẳng" xuống, hệ số ước lượng bị kéo về gần 0 hơn giá trị thật — đây là dạng **attenuation bias** (chệch làm giảm độ lớn của hệ số).
<br><span class="en">**Run OLS on the whole sample, treating 0 as a "real" $y$ value** — OLS tries to draw a straight line through both the mass of points at 0 and the positive data above. Because the mass of points at 0 pulls the regression line "flat," the estimated coefficient is pulled closer to 0 than its true value — this is a form of **attenuation bias** (bias shrinking the magnitude of the coefficient).</span>
2. **Bỏ hẳn các quan sát có $y=0$, chỉ chạy OLS trên phần còn lại ($y>0$)** — nhìn tưởng hợp lý (vì "dữ liệu còn lại đều là giá trị thật, không bị cắt") nhưng cũng chệch: đây là một dạng **loại mẫu không ngẫu nhiên** (mẫu con $y>0$ không phải một mẫu con ngẫu nhiên của dân số — nó có xu hướng hệ thống gồm những người có đặc điểm "thuận lợi" hơn theo đúng mô hình), về bản chất tương đương với việc biến mẫu censored thành một dạng truncated ngay trong quá trình phân tích.
<br><span class="en">**Drop the observations with $y=0$ entirely, and run OLS only on the rest ($y>0$)** — this looks reasonable at first (because "the remaining data are all real, uncut values") but is also biased: this is a form of **non-random sample exclusion** (the $y>0$ subsample is not a random subsample of the population — it systematically tends to include people with "more favorable" characteristics per the model), which is essentially equivalent to turning a censored sample into a truncated one right in the middle of the analysis.</span>

Cả hai cách đều chệch, bất kể mức độ censor nhiều hay ít. Chỉ có ước lượng **maximum likelihood đầy đủ theo Tobit** — dùng toàn bộ thông tin, kể cả biết $X$ của các quan sát bị censor — mới cho ước lượng nhất quán (consistent).
<br><span class="en">Both approaches are biased, regardless of how much or how little censoring there is. Only full **maximum likelihood estimation per Tobit** — using all the information, including knowing $X$ for censored observations — yields a consistent estimator.</span>

## 4. Mô hình Tobit — cấu trúc latent variable - <span class="en">The Tobit model — latent variable structure</span>

$$y^*=X\beta+\varepsilon, \qquad y=\begin{cases}0 & \text{if } y^*\le0\\ y^* & \text{if } y^*>0\end{cases}$$

- $y^*$ gọi là **biến chỉ số / biến tiềm ẩn (index/latent variable)** — cùng cấu trúc toán học với $y^*$ trong [[concepts/ordinal-response-models]] (đều là "một biến liên tục ẩn, quan sát được thông qua các ngưỡng"). Khác biệt quan trọng: ở ordinal model, có **nhiều ngưỡng cắt** và các ngưỡng đó thường **được ước lượng** từ dữ liệu; ở Tobit "censoring tại 0", chỉ có **một ngưỡng duy nhất, cố định tại 0** (đã biết trước, không cần ước lượng).
<br><span class="en">$y^*$ is called the **index / latent variable** — the same mathematical structure as $y^*$ in [[concepts/ordinal-response-models]] (both are "a hidden continuous variable, observed through thresholds"). Important difference: in the ordinal model, there are **multiple cut thresholds** and those thresholds are usually **estimated** from the data; in Tobit "censoring at 0," there is only **a single threshold, fixed at 0**" (known in advance, not estimated).</span>
- $y$ là **biến quan sát được** — chính là số dư nợ thẻ tín dụng thật sự ghi nhận trong dữ liệu.
<br><span class="en">$y$ is the **observed variable** — the actual credit card balance recorded in the data.</span>
- $\varepsilon$ là sai số ngẫu nhiên, giả định $\varepsilon \sim N(0,\sigma^2)$, nên $y^*\sim N(X\beta,\sigma^2)$.
<br><span class="en">$\varepsilon$ is the random error, assumed $\varepsilon \sim N(0,\sigma^2)$, so $y^*\sim N(X\beta,\sigma^2)$.</span>

Với giả định phân phối chuẩn này, xác suất một quan sát bị censor (tức $y=0$) là:
<br><span class="en">Under this normality assumption, the probability that an observation is censored (i.e. $y=0$) is:</span>

$$Pr(y=0)=Pr(y^*\le0)=\Phi\left(-\frac{X\beta}{\sigma}\right)=1-\Phi\left(\frac{X\beta}{\sigma}\right)$$

trong đó $\Phi$ là hàm phân phối tích lũy (CDF) của phân phối chuẩn chuẩn hóa — cùng ký hiệu, cùng vai trò với $\Phi$ trong mô hình Probit ở [[concepts/binary-response-models]]. Đây không phải trùng hợp: về bản chất, "có bị censor hay không" tự nó là một quyết định nhị phân ẩn bên trong Tobit, chi phối bởi đúng cơ chế của Probit.
<br><span class="en">where $\Phi$ is the cumulative distribution function (CDF) of the standard normal distribution — the same notation, the same role as $\Phi$ in the Probit model in [[concepts/binary-response-models]]. This is not a coincidence: fundamentally, "censored or not" is itself a hidden binary decision inside Tobit, governed by exactly the Probit mechanism.</span>

**Trường hợp tổng quát** (censoring cả hai phía, tại $a$ và $b$, ví dụ giá bị kiểm soát cả trần lẫn sàn):
<br><span class="en">**General case** (censoring on both sides, at $a$ and $b$, e.g. a price controlled by both a ceiling and a floor):</span>

$$y=\begin{cases}a & \text{if } y^*\le a\\ y^*=X\beta+\varepsilon & \text{if } a<y^*<b\\ b & \text{if } y^*\ge b\end{cases}$$

Xác suất không bị censor (nằm trong khoảng mở) trở thành:
<br><span class="en">The probability of not being censored (falling within the open interval) becomes:</span>

$$Pr(a<y^*<b)=\Phi\left(\frac{b-X\beta}{\sigma}\right)-\Phi\left(\frac{a-X\beta}{\sigma}\right)$$

Mọi công thức predicted value/marginal effect ở mục 7 (viết cho trường hợp censoring tại 0) đều có bản tổng quát tương ứng bằng cách thay $\Phi(X\beta/\sigma)$ bằng biểu thức xác suất hai phía này.
<br><span class="en">Every predicted value/marginal effect formula in section 7 (written for the censoring-at-0 case) has a corresponding general version by replacing $\Phi(X\beta/\sigma)$ with this two-sided probability expression.</span>

## 5. Case study xuyên suốt: Credit card balance - <span class="en">Running case study: Credit card balance</span>

**Biến phụ thuộc** (censored from below tại 0): `balance` — số dư nợ thẻ tín dụng (USD).
<br><span class="en">**Dependent variable** (censored from below at 0): `balance` — credit card balance (USD).</span>
**Biến độc lập**: `interest` (lãi suất thẻ tín dụng, %), `age` (tuổi, năm), `male` (dummy, 1=nam), `edu` (số năm đi học).
<br><span class="en">**Independent variables**: `interest` (credit card interest rate, %), `age` (age, years), `male` (dummy, 1=male), `edu` (years of education).</span>

**Thống kê mô tả** ($N=2895$ quan sát, `psych::describe`):
<br><span class="en">**Descriptive statistics** ($N=2895$ observations, `psych::describe`):</span>

| Biến / <span class="en">Variable</span> | mean | sd | min | max |
|---|---|---|---|---|
| `balance` | 1917.27 | 9675.95 | 0 | 147917.53 |
| `interest` | 14.42 | 4.46 | 5 | 28.88 |
| `age` | 50.10 | 15.03 | 18 | 106 |
| `male` | 0.78 | 0.42 | 0 | 1 |
| `edu` | 14.39 | 2.56 | 6 | 23 |

Histogram của `balance` cho thấy đúng hình dạng đặc trưng của một biến censored tại 0: một cột rất cao dồn ở 0, sau đó đuôi phải kéo dài (right-skewed) với vài quan sát cực lớn (max ≈ 147918 USD). Chia theo giới tính: nữ (`male=0`, $n=646$) có `balance` trung bình 1049.82 USD; nam (`male=1`, $n=2249$) có `balance` trung bình 2166.44 USD — chênh lệch thô lớn, khớp hướng với hệ số dương của `male` trong hồi quy Tobit dưới đây.
<br><span class="en">The histogram of `balance` shows exactly the shape characteristic of a variable censored at 0: a very tall bar piled at 0, followed by a long right tail (right-skewed) with a few extremely large observations (max ≈ 147918 USD). Split by gender: female (`male=0`, $n=646$) has mean `balance` of 1049.82 USD; male (`male=1`, $n=2249$) has mean `balance` of 2166.44 USD — a large raw gap, matching the direction of the positive `male` coefficient in the Tobit regression below.</span>

**Kết quả hồi quy Tobit** (R, package `censReg`, `censReg(balance ~ interest + age + male + edu, left = 0, data = z)`):
<br><span class="en">**Tobit regression results** (R, package `censReg`, `censReg(balance ~ interest + age + male + edu, left = 0, data = z)`):</span>

```
Observations: Total 2895, Left-censored 1018, Uncensored 1877, Right-censored 0

Coefficients:
              Estimate   Std.error   t value    Pr(>|t|)
(Intercept)   31227.12    1877.00     16.640    < 2e-16 ***
interest       -321.25      54.01     -5.948    2.71e-09 ***
age            -349.21      17.39    -20.083    < 2e-16 ***
male           2531.38     587.30      4.310    1.63e-05 ***
edu            -941.30      94.73     -9.937    < 2e-16 ***
logSigma          9.368      0.016    572.704    < 2e-16 ***

Log-likelihood: -20732.56 on 6 Df
```

Vài điểm đọc bảng này cần lưu ý:
<br><span class="en">A few points worth noting when reading this table:</span>

- **1018/2895 ≈ 35.2%** quan sát bị censor (left-censored tại 0) — đây chính là "khối điểm dồn ở 0" nói ở mục 3. 1877 quan sát còn lại (64.8%) có `balance` dương, quan sát được chính xác.
<br><span class="en">**1018/2895 ≈ 35.2%** of observations are censored (left-censored at 0) — this is exactly the "mass of points piled at 0" mentioned in section 3. The remaining 1877 observations (64.8%) have positive `balance`, observed exactly.</span>
- Package ước lượng **`logSigma`** thay vì $\sigma$ trực tiếp (đúng như lưu ý ở mục 6) — $\sigma = \exp(9.367847) \approx 11705.88$ (R tự tính lại từ `logSigma` khi cần dùng cho các công thức dự đoán/ME ở mục 7).
<br><span class="en">The package estimates **`logSigma`** instead of $\sigma$ directly (exactly as noted in section 6) — $\sigma = \exp(9.367847) \approx 11705.88$ (R recomputes this from `logSigma` when needed for the prediction/ME formulas in section 7).</span>
- Dấu của các hệ số: `interest` và `age` âm (lãi suất cao hơn, tuổi cao hơn → khuynh hướng nợ tiềm ẩn thấp hơn), `male` dương, `edu` âm (học vấn cao hơn → khuynh hướng nợ tiềm ẩn thấp hơn). Đây là các hệ số $\beta$ trên **biến latent** $y^*$ — mục 7 sẽ cho thấy các con số này **không** phải là hiệu ứng lên `balance` quan sát được.
<br><span class="en">Signs of the coefficients: `interest` and `age` are negative (higher interest rate, higher age → lower latent borrowing tendency), `male` is positive, `edu` is negative (more education → lower latent borrowing tendency). These are $\beta$ coefficients on the **latent variable** $y^*$ — section 7 will show that these numbers are **not** the effect on observed `balance`.</span>
- Vì slide không thảo luận chiến lược nhận diện nhân quả (identification) cho bộ dữ liệu này (không có bàn về exogeneity của `interest`, `age`...), trang này diễn giải các hệ số theo ngôn ngữ **liên kết/mô tả của mô hình ước lượng** ("mô hình ước lượng cho thấy..."), không khẳng định ngôn ngữ nhân quả mạnh — theo đúng nguyên tắc thận trọng ở [[concepts/linear-regression-model]] mục 5.
<br><span class="en">Since the slide does not discuss an identification strategy for this dataset (no discussion of the exogeneity of `interest`, `age`...), this page interprets the coefficients in **associational/descriptive language of the estimated model** ("the estimated model shows..."), without asserting strong causal language — following the same caution principle as in [[concepts/linear-regression-model]] section 5.</span>

## 6. Log-likelihood của Tobit — ý tưởng trực quan - <span class="en">Tobit's log-likelihood — the intuitive idea</span>

**Ý tưởng cốt lõi**: log-likelihood của Tobit là **tổng của hai loại đóng góp khác nhau**, tùy quan sát có bị censor hay không:
<br><span class="en">**Core idea**: Tobit's log-likelihood is the **sum of two different types of contributions**, depending on whether an observation is censored or not:</span>

- Với **1877 khách hàng có `balance` dương** ($Y>0$, không censor): ta biết chính xác giá trị $Y_i$. Đóng góp vào likelihood giống hệt OLS/hồi quy tuyến tính thông thường — dùng **mật độ xác suất** (density) của phân phối chuẩn tại đúng điểm $Y_i$: "xác suất (mật độ) quan sát được chính xác giá trị này, nếu mô hình đúng."
<br><span class="en">For the **1877 customers with positive `balance`** ($Y>0$, uncensored): we know the exact value $Y_i$. The contribution to the likelihood is identical to ordinary OLS/linear regression — using the normal distribution's **probability density** at exactly the point $Y_i$: "the probability (density) of observing exactly this value, if the model is correct."</span>
- Với **1018 khách hàng có `balance = 0`** ($Y=0$, censor): ta **không biết** giá trị latent $y^*_i$ thật sự là bao nhiêu (có thể là −50, có thể là −50000 USD "mong muốn vay âm") — chỉ biết chắc $y^*_i \le 0$. Vì không biết điểm chính xác, không thể dùng mật độ tại một điểm; thay vào đó đóng góp vào likelihood là **xác suất của cả một miền**: $Pr(y^*_i\le0)=\Phi(-X_i\beta/\sigma)$.
<br><span class="en">For the **1018 customers with `balance = 0`** ($Y=0$, censored): we **do not know** what the latent value $y^*_i$ truly is (it could be −50, it could be −50000 USD of "negative desired borrowing") — we only know for certain that $y^*_i \le 0$. Since the exact point is unknown, density at a single point cannot be used; instead the contribution to the likelihood is the **probability of an entire region**: $Pr(y^*_i\le0)=\Phi(-X_i\beta/\sigma)$.</span>

Công thức đầy đủ (trường hợp censoring tại 0), viết dưới dạng tổng theo từng quan sát $i$, với $\mathbb{1}(\cdot)$ là hàm chỉ thị:
<br><span class="en">The full formula (censoring-at-0 case), written as a sum over each observation $i$, with $\mathbb{1}(\cdot)$ the indicator function:</span>

$$\log L(\beta,\sigma\mid X,Y)=\sum_i\left[-\mathbb{1}(Y_i>0)\left(\tfrac12\log(2\pi\sigma^2)+\tfrac{(Y_i-X_i\beta)^2}{2\sigma^2}\right)+\mathbb{1}(Y_i=0)\log\Phi\left(\tfrac{-X_i\beta}{\sigma}\right)\right]$$

Số hạng đầu (nhân với $\mathbb{1}(Y_i>0)$) chính là log của mật độ chuẩn — quen thuộc từ OLS. Số hạng sau (nhân với $\mathbb{1}(Y_i=0)$) là log-xác suất censor. Tối đa hóa tổng này theo $\beta,\sigma$ đồng thời "khớp đường hồi quy" với phần dữ liệu quan sát được đầy đủ, **và** "khớp xác suất censor" với đúng tần suất censor thực tế trong dữ liệu — đây là lý do MLE theo Tobit cho ước lượng nhất quán trong khi OLS (chỉ dùng số hạng đầu, coi mọi quan sát đều là $Y>0$) thì không.
<br><span class="en">The first term (multiplied by $\mathbb{1}(Y_i>0)$) is exactly the log of the normal density — familiar from OLS. The second term (multiplied by $\mathbb{1}(Y_i=0)$) is the log-probability of censoring. Maximizing this sum over $\beta,\sigma$ simultaneously "fits the regression line" to the fully observed part of the data, **and** "matches the censoring probability" to the actual censoring frequency in the data — this is why Tobit's MLE yields a consistent estimator while OLS (which only uses the first term, treating every observation as $Y>0$) does not.</span>

**Trường hợp tổng quát** (censoring hai phía tại $a,b$) mở rộng ý tưởng trên thành ba loại đóng góp: mật độ liên tục cho $a<Y<b$, xác suất $\Phi\left(\frac{a-X\beta}{\sigma}\right)$ cho $Y=a$, và xác suất $1-\Phi\left(\frac{b-X\beta}{\sigma}\right)$ cho $Y=b$.
<br><span class="en">**The general case** (censoring on both sides at $a,b$) extends this idea into three types of contributions: continuous density for $a<Y<b$, probability $\Phi\left(\frac{a-X\beta}{\sigma}\right)$ for $Y=a$, and probability $1-\Phi\left(\frac{b-X\beta}{\sigma}\right)$ for $Y=b$.</span>

**Ghi chú kỹ thuật**: nhiều phần mềm (kể cả `censReg` trong ví dụ trên) ước lượng $\log\sigma$ thay vì $\sigma$ trực tiếp trong quá trình tối ưu hóa số — vì $\sigma$ luôn phải dương, ước lượng $\log\sigma$ (có thể nhận mọi giá trị thực) rồi lấy $\exp(\cdot)$ ở bước cuối tự động đảm bảo ràng buộc này mà không cần thêm điều kiện ràng buộc phức tạp trong thuật toán tối ưu (ở đây, Newton-Raphson, 30 vòng lặp).
<br><span class="en">**Technical note**: many software packages (including `censReg` in the example above) estimate $\log\sigma$ instead of $\sigma$ directly during numerical optimization — since $\sigma$ must always be positive, estimating $\log\sigma$ (which can take any real value) and then taking $\exp(\cdot)$ at the final step automatically enforces this constraint without needing additional complex constraints in the optimization algorithm (here, Newton-Raphson, 30 iterations).</span>

## 7. Ba loại giá trị dự đoán và marginal effect sau Tobit — phần khó nhất - <span class="en">Three types of predicted value and marginal effect after Tobit — the hardest part</span>

Đây là phần **quan trọng nhất và dễ nhầm lẫn nhất** của topic. Lý do gốc rễ: một khi có censoring, "hiệu ứng của $X$ lên $y$" không còn là MỘT con số duy nhất như trong OLS thường ($\beta$) — mà tách thành **ba câu hỏi khác nhau**, mỗi câu hỏi có câu trả lời bằng số khác nhau, và đề thi thường cố tình hỏi rất cụ thể câu hỏi nào trong ba câu để kiểm tra người học có phân biệt được không.
<br><span class="en">This is the **most important and most confusable** part of the topic. The root reason: once there is censoring, "the effect of $X$ on $y$" is no longer a SINGLE number as in ordinary OLS ($\beta$) — it splits into **three different questions**, each with a different numeric answer, and exam questions often deliberately ask very specifically which of the three questions is meant, to test whether the learner can tell them apart.</span>

### 7.1 Latent prediction — $E(y^*\mid X)=X\beta$ - <span class="en">Latent prediction — $E(y^*\mid X)=X\beta$</span>

Đây là hiệu ứng lên **biến tiềm ẩn không quan sát được** $y^*$ — tức "khuynh hướng vay nợ" ẩn, có thể âm, không bị chặn bởi ngưỡng 0.
<br><span class="en">This is the effect on the **unobserved latent variable** $y^*$ — i.e. the hidden "borrowing tendency," which can be negative and is not bounded by the 0 threshold.</span>

$$E(y^*\mid X)=X\beta \qquad\Rightarrow\qquad \text{Marginal effect} = \beta \text{ (constant, exactly like ordinary OLS)}$$

**Dùng khi nào**: khi câu hỏi nghiên cứu về bản thân "khuynh hướng"/"chỉ số" tiềm ẩn — ví dụ mô hình hóa một khái niệm lý thuyết (creditworthiness, willingness to borrow) mà `balance` quan sát được chỉ là một biểu hiện bị cắt của nó. **Đây KHÔNG phải là hiệu ứng lên số dư nợ thẻ tín dụng thực tế mà một nhà phân tích/ngân hàng quan tâm** — chỉ là hiệu ứng lên một cấu trúc toán học trung gian. Đây chính là lý do $\beta$ thô từ output Tobit **không nên được diễn giải trực tiếp như một marginal effect thực tế** — bẫy thi phổ biến nhất của mục này (xem mục 9).
<br><span class="en">**When to use**: when the research question is about the latent "tendency"/"index" itself — e.g. modeling a theoretical concept (creditworthiness, willingness to borrow) for which observed `balance` is just a cut-off manifestation. **This is NOT the effect on the actual credit card balance that an analyst/bank cares about** — it is only the effect on an intermediate mathematical structure. This is exactly why the raw $\beta$ from Tobit output **should not be interpreted directly as a real marginal effect** — the most common exam trap of this section (see section 9).</span>

### 7.2 Unconditional expected value — $E(y\mid X)$, tính cả xác suất censor - <span class="en">Unconditional expected value — $E(y\mid X)$, accounting for the censoring probability</span>

$$E(y\mid X)=\Phi\left(\frac{X\beta}{\sigma}\right)\left(X\beta+\sigma\lambda\right), \qquad \lambda=\frac{\phi(X\beta/\sigma)}{\Phi(X\beta/\sigma)}$$

$\lambda$ ở đây là **tỷ số nghịch đảo Mill (inverse Mills ratio)** — dù slide không gọi tên trực tiếp, đây chính là cấu trúc toán học sẽ tái xuất hiện trong Heckman selection model (mục 9).
<br><span class="en">$\lambda$ here is the **inverse Mills ratio** — although the slide does not name it directly, this is exactly the mathematical structure that will reappear in the Heckman selection model (section 9).</span>

Marginal effect tương ứng:
<br><span class="en">The corresponding marginal effect:</span>

$$\frac{\partial E(y\mid X)}{\partial X} = \beta\,\Phi\left(\frac{X\beta}{\sigma}\right)$$

**Ý nghĩa trực giác**: đây là hiệu ứng lên **giá trị quan sát được trung bình của TOÀN BỘ mẫu** — bao gồm cả những người sẽ (theo mô hình) bị censor về 0. Về công thức, nó chính là $\beta$ (hiệu ứng latent) **nhân với xác suất không bị censor** $\Phi(X\beta/\sigma)$ — luôn nhỏ hơn $|\beta|$ về độ lớn (vì $0<\Phi(\cdot)<1$), vì một phần "hiệu ứng tiềm ẩn" bị "hấp thụ" bởi khối quan sát đang nằm ở 0 (họ không phản ứng gì cả, vẫn giữ nguyên $y=0$, dù $y^*$ của họ có thay đổi).
<br><span class="en">**Intuitive meaning**: this is the effect on the **average observed value of the ENTIRE sample** — including those who will (per the model) be censored to 0. In terms of the formula, it is exactly $\beta$ (the latent effect) **multiplied by the probability of not being censored** $\Phi(X\beta/\sigma)$ — always smaller than $|\beta|$ in magnitude (since $0<\Phi(\cdot)<1$), because part of the "latent effect" is "absorbed" by the mass of observations sitting at 0 (they don't respond at all, staying at $y=0$, even though their $y^*$ changed).</span>

**Dùng khi nào**: khi câu hỏi là về **tổng thể** — ví dụ "nếu lãi suất trung bình toàn thị trường tăng 1%, tổng dư nợ thẻ tín dụng trung bình trên mỗi khách hàng (tính cả những người không nợ) thay đổi bao nhiêu?" — phù hợp cho các câu hỏi ở cấp độ **dự báo tổng thể/chính sách vĩ mô**.
<br><span class="en">**When to use**: when the question is about the **aggregate** — e.g. "if the market-wide average interest rate rises 1%, how much does the average credit card balance per customer (including those with no debt) change?" — suited to questions at the level of **aggregate forecasting/macro-level policy**.</span>

### 7.3 Conditional expected value — $E(y\mid X, y>0)$, chỉ trên nhóm không bị censor - <span class="en">Conditional expected value — $E(y\mid X, y>0)$, only over the uncensored group</span>

$$E(y\mid X, y>0)=X\beta+\sigma\lambda$$

Marginal effect tương ứng:
<br><span class="en">The corresponding marginal effect:</span>

$$\frac{\partial E(y\mid y>0)}{\partial X}=\beta\left[1-\lambda\left(\lambda+\frac{X\beta}{\sigma}\right)\right]$$

**Ý nghĩa trực giác**: đây là hiệu ứng lên giá trị trung bình **CHỈ trong nhóm đã biết chắc không bị censor** — với case study, chỉ trong nhóm 1877 khách hàng đang thực sự có dư nợ dương. Nói cách khác: "trong số những người ĐÃ đang vay nợ qua thẻ tín dụng, nếu lãi suất của họ tăng 1%, mức dư nợ trung bình của riêng nhóm này thay đổi bao nhiêu?"
<br><span class="en">**Intuitive meaning**: this is the effect on the average value **ONLY within the group already known not to be censored** — for the case study, only within the group of 1877 customers who actually have a positive balance. In other words: "among those ALREADY borrowing through their credit card, if their interest rate rises 1%, how much does the average balance of this group alone change?"</span>

**Dùng khi nào**: khi câu hỏi nghiên cứu chỉ quan tâm đến **intensive margin** (mức độ, trong nhóm đã tham gia) chứ không phải extensive margin (có tham gia hay không) — ví dụ ngân hàng muốn biết "trong số khách hàng đang có dư nợ, ai sẽ trả nợ nhiều/ít hơn nếu lãi suất thay đổi", bỏ qua câu hỏi "ai sẽ bắt đầu/ngừng có dư nợ".
<br><span class="en">**When to use**: when the research question only cares about the **intensive margin** (the degree, within the group already participating) rather than the extensive margin (participating or not) — e.g. a bank wants to know "among customers currently carrying a balance, who will pay more/less if interest rates change," ignoring the question of "who will start/stop carrying a balance."</span>

### 7.4 (Bổ sung) Marginal effect trên xác suất không bị censor - <span class="en">(Supplement) Marginal effect on the probability of not being censored</span>

$$\frac{\partial Pr(y>0\mid X)}{\partial X}=\frac{\phi(X\beta/\sigma)}{\sigma}\,\beta$$

Đây không phải là hiệu ứng lên *giá trị* của $y$, mà lên **xác suất** $y$ dương — với case study: "hiệu ứng lên xác suất khách hàng có dư nợ (không phải trả hết mỗi tháng)". Về mặt cấu trúc, công thức này giống hệt marginal effect của Probit ([[concepts/binary-response-models]]) áp lên đúng biến chỉ thị ẩn "$y^*>0$ hay không".
<br><span class="en">This is not the effect on the *value* of $y$, but on the **probability** that $y$ is positive — for the case study: "the effect on the probability a customer carries a balance (rather than paying it off each month)." Structurally, this formula is identical to Probit's marginal effect ([[concepts/binary-response-models]]) applied exactly to the hidden indicator variable "$y^*>0$ or not."</span>

### 7.5 Ví dụ số minh họa — bốn loại hiệu ứng, cùng bốn biến, một bảng - <span class="en">Illustrative numerical example — four types of effects, same four variables, one table</span>

Slide tính sẵn các con số này (bằng R, tại giá trị trung bình mẫu $\bar X$) cho case study credit card balance — đây là ví dụ định lượng rõ nhất để thấy ba loại prediction/marginal effect **khác nhau đến mức nào trên cùng một biến**:
<br><span class="en">The slide precomputes these numbers (in R, at the sample mean $\bar X$) for the credit card balance case study — this is the clearest quantitative example to see just **how different the three types of prediction/marginal effect are for the same variable**:</span>

| Biến / <span class="en">Variable</span> | $\beta$ (latent, "thô" / <span class="en">"raw"</span>) | Unconditional ME — $\partial E(y\mid X)/\partial X$ | Conditional ME — $\partial E(y\mid y{>}0)/\partial X$ | ME trên / <span class="en">on</span> $Pr(y>0)$ |
|---|---|---|---|---|
| `interest` (%) | −321.25 | −133.70 | −102.74 | −0.0107 |
| `age` (năm / <span class="en">years</span>) | −349.21 | −145.33 | −111.68 | −0.0116 |
| `male` (dummy) | +2531.38 | +1053.51 | +809.53 | +0.0844 |
| `edu` (năm học / <span class="en">years of education</span>) | −941.30 | −391.75 | −301.03 | −0.0314 |

Đọc bảng này theo hàng `interest` (tất cả tại $\bar X$, tức tại khách hàng có đặc điểm trung bình mẫu):
<br><span class="en">Reading this table along the `interest` row (all evaluated at $\bar X$, i.e. at a customer with sample-average characteristics):</span>

- $\beta_{interest}=-321.25$: đây là hiệu ứng lên **biến latent** $y^*$ — không có đơn vị "USD dư nợ thực tế" trực tiếp, vì $y^*$ có thể âm.
<br><span class="en">$\beta_{interest}=-321.25$: this is the effect on the **latent variable** $y^*$ — it has no direct "actual USD balance" unit, since $y^*$ can be negative.</span>
- Unconditional ME $=-133.70$: nếu lãi suất tăng 1 điểm phần trăm, **dư nợ trung bình của TOÀN BỘ 2895 khách hàng** (kể cả 1018 người đang có `balance=0`) giảm khoảng 133.70 USD, theo mô hình ước lượng.
<br><span class="en">Unconditional ME $=-133.70$: if interest rises 1 percentage point, **the average balance of ALL 2895 customers** (including the 1018 people currently at `balance=0`) falls by about 133.70 USD, per the estimated model.</span>
- Conditional ME $=-102.74$: nếu lãi suất tăng 1 điểm phần trăm, **dư nợ trung bình CHỈ trong nhóm 1877 khách hàng đang có dư nợ dương** giảm khoảng 102.74 USD.
<br><span class="en">Conditional ME $=-102.74$: if interest rises 1 percentage point, **the average balance ONLY within the group of 1877 customers currently holding a positive balance** falls by about 102.74 USD.</span>
- ME trên $Pr(y>0)$ $=-0.0107$: nếu lãi suất tăng 1 điểm phần trăm, **xác suất một khách hàng có dư nợ dương** (thay vì `balance=0`) giảm khoảng 1.07 điểm phần trăm.
<br><span class="en">ME on $Pr(y>0)$ $=-0.0107$: if interest rises 1 percentage point, **the probability that a customer has a positive balance** (rather than `balance=0`) falls by about 1.07 percentage points.</span>

**Ba con số này (−321.25, −133.70, −102.74) đều mô tả "hiệu ứng của lãi suất" nhưng trả lời ba câu hỏi khác nhau — và không thể dùng thay thế cho nhau.** Đây chính xác là bẫy thi lớn nhất của topic.
<br><span class="en">**These three numbers (−321.25, −133.70, −102.74) all describe "the effect of interest" but answer three different questions — and cannot be used interchangeably.** This is exactly the biggest exam trap of the topic.</span>

**Một cách tự kiểm tra nhanh** (tương tự tinh thần "self-check" ở [[concepts/linear-regression-model]] mục 7.4): tỷ số $\text{Unconditional ME}/\beta$ phải **giống nhau cho mọi biến**, vì cả hai đều nhân chung một hệ số $\Phi(X\beta/\sigma)$ chỉ phụ thuộc $\bar X$ chung, không phụ thuộc biến nào riêng lẻ. Kiểm tra với bảng trên: $133.70/321.25\approx0.416$; $145.33/349.21\approx0.416$; $1053.51/2531.38\approx0.416$; $391.75/941.30\approx0.416$ — khớp cả bốn biến. Điều này cho biết: tại khách hàng có đặc điểm trung bình mẫu, xác suất mô hình dự đoán có dư nợ dương $\Phi(\bar X\beta/\sigma)\approx41.6\%$. Tương tự, tỷ số Conditional ME$/\beta\approx0.320$ cho cả bốn biến.
<br><span class="en">**A quick self-check** (in the same spirit as the "self-check" in [[concepts/linear-regression-model]] section 7.4): the ratio $\text{Unconditional ME}/\beta$ must be **the same for every variable**, since both share the common factor $\Phi(X\beta/\sigma)$, which depends only on the shared $\bar X$, not on any individual variable. Checking against the table above: $133.70/321.25\approx0.416$; $145.33/349.21\approx0.416$; $1053.51/2531.38\approx0.416$; $391.75/941.30\approx0.416$ — matches for all four variables. This tells us: at a customer with sample-average characteristics, the model-predicted probability of a positive balance is $\Phi(\bar X\beta/\sigma)\approx41.6\%$. Similarly, the ratio Conditional ME$/\beta\approx0.320$ for all four variables.</span>

**Một điểm tinh tế đáng lưu ý**: $41.6\%$ (xác suất dự đoán *tại* khách hàng trung bình $\bar X$) khác với $1877/2895\approx64.8\%$ (tỷ lệ *thực tế* không bị censor trong toàn mẫu). Đây không phải mâu thuẫn — vì $\Phi(\cdot)$ là hàm phi tuyến, "xác suất tính tại giá trị trung bình của $X$" nói chung khác "giá trị trung bình của xác suất tính cho từng cá nhân" (một dạng bất đẳng thức Jensen). Đây cũng chính là lý do slide tính **cả hai phiên bản** của mỗi marginal effect:
<br><span class="en">**A subtle point worth noting**: $41.6\%$ (the predicted probability *at* the average customer $\bar X$) differs from $1877/2895\approx64.8\%$ (the *actual* proportion uncensored in the whole sample). This is not a contradiction — because $\Phi(\cdot)$ is a nonlinear function, "the probability evaluated at the mean of $X$" generally differs from "the mean of the probability evaluated for each individual" (a form of Jensen's inequality). This is also exactly why the slide computes **both versions** of each marginal effect:</span>

- **"At mean"**: tính công thức ME một lần duy nhất, thay $X=\bar X$ (đặc điểm trung bình mẫu) vào.
<br><span class="en">**"At mean"**: compute the ME formula a single time, plugging in $X=\bar X$ (sample-average characteristics).</span>
- **"Average" (average marginal effect — AME)**: tính công thức ME riêng cho **từng quan sát** trong mẫu (dùng $X_i$ của chính họ), rồi lấy trung bình của $N=2895$ con số ME đó.
<br><span class="en">**"Average" (average marginal effect — AME)**: compute the ME formula separately for **each observation** in the sample (using its own $X_i$), then take the average of the $N=2895$ resulting ME numbers.</span>

Với case study này, hai phiên bản gần nhau nhưng không trùng khớp tuyệt đối — ví dụ Unconditional ME của `interest`: "at mean" $=-133.70$ USD, "average" $=-136.74$ USD; Conditional ME của `interest`: "at mean" $=-102.74$ USD, "average" $=-107.21$ USD. Khác biệt nhỏ trong ví dụ này, nhưng về nguyên tắc có thể lớn hơn nhiều nếu $X$ phân tán rộng — luôn nêu rõ đang dùng phiên bản nào khi báo cáo kết quả.
<br><span class="en">For this case study, the two versions are close but not exactly identical — e.g. Unconditional ME of `interest`: "at mean" $=-133.70$ USD, "average" $=-136.74$ USD; Conditional ME of `interest`: "at mean" $=-102.74$ USD, "average" $=-107.21$ USD. The difference is small in this example, but in principle it could be much larger if $X$ is widely dispersed — always state clearly which version is being used when reporting results.</span>

### 7.6 Ghi chú kỹ thuật: p-value của marginal effect - <span class="en">Technical note: p-value of the marginal effect</span>

Không có công thức closed-form đơn giản cho standard error/p-value của các ME ở trên (cần **delta method** — kỹ thuật nâng cao, ngoài phạm vi tính tay của khóa học). Slide đề xuất cách xấp xỉ: coi tỷ số $ME/SE(ME)$ theo phân phối chuẩn chuẩn hóa,
<br><span class="en">There is no simple closed-form formula for the standard error/p-value of the ME's above (it requires the **delta method** — an advanced technique, outside the scope of by-hand computation in this course). The slide suggests an approximation: treat the ratio $ME/SE(ME)$ as standard-normally distributed,</span>

$$z=\frac{ME}{SE(ME)}, \qquad p=2\left(1-\Phi(|z|)\right)$$

## 8. Kiểm định sau Tobit: Likelihood Ratio (LR) test - <span class="en">Testing after Tobit: the Likelihood Ratio (LR) test</span>

Vì Tobit ước lượng bằng MLE (không phải OLS), kiểm định **đồng thời nhiều hệ số** không dùng F-test như [[concepts/linear-regression-model]] mục 8, mà dùng **Likelihood Ratio (LR) test** — so sánh log-likelihood của mô hình đầy đủ (unrestricted) với mô hình bị ép loại bỏ các biến đang kiểm định (restricted), cùng tinh thần trực giác với F-test (nếu loại biến mà "độ khớp" giảm mạnh, tức log-likelihood giảm nhiều, thì các biến đó thực sự quan trọng).
<br><span class="en">Since Tobit is estimated by MLE (not OLS), testing **multiple coefficients jointly** does not use the F-test as in [[concepts/linear-regression-model]] section 8, but instead uses the **Likelihood Ratio (LR) test** — comparing the log-likelihood of the full (unrestricted) model against a model forced to exclude the variables being tested (restricted), in the same intuitive spirit as the F-test (if excluding variables causes "goodness of fit" to drop sharply, i.e. log-likelihood drops a lot, then those variables truly matter).</span>

**Ví dụ từ slide** (`lmtest::lrtest`, kiểm định đồng thời `age`, `male`, `edu`):
<br><span class="en">**Example from the slide** (`lmtest::lrtest`, jointly testing `age`, `male`, `edu`):</span>

```
Model 1: balance ~ interest + age + male + edu     (unrestricted, LogLik = -20733, Df = 6)
Model 2: balance ~ interest                          (restricted, LogLik = -20998, Df = 3)

Chisq = 530.58, Df = 3, Pr(>Chisq) < 2.2e-16
```

$H_0: \beta_{age}=\beta_{male}=\beta_{edu}=0$. Với $\chi^2=530.58$, $p<2.2\times10^{-16}$ → **bác bỏ mạnh** $H_0$ → có bằng chứng rằng ít nhất một trong ba biến (`age`, `male`, `edu`) thực sự đóng góp vào việc giải thích số dư nợ, ngoài `interest`.
<br><span class="en">$H_0: \beta_{age}=\beta_{male}=\beta_{edu}=0$. With $\chi^2=530.58$, $p<2.2\times10^{-16}$ → **strongly reject** $H_0$ → there is evidence that at least one of the three variables (`age`, `male`, `edu`) genuinely contributes to explaining the balance, beyond `interest`.</span>

> Ghi chú của slide: kiểm định LR cho overall significance (toàn bộ hệ số góc cùng lúc) cũng làm tương tự — chỉ cần đưa toàn bộ biến của mô hình vào `lmtest::lrtest`. Cùng lưu ý diễn giải như F-test overall ở [[concepts/linear-regression-model]] mục 8.5: LR test có ý nghĩa thống kê **không** chứng minh mô hình đặc tả đúng, không kiểm tra được các giả định của Tobit (đặc biệt là giả định phân phối chuẩn của $\varepsilon$, vốn quan trọng hơn nhiều so với OLS vì toàn bộ log-likelihood dựa trên giả định này).
> <br><span class="en">Note from the slide: the LR test for overall significance (all slope coefficients at once) works the same way — simply put every variable of the model into `lmtest::lrtest`. The same interpretation caveat as the overall F-test in [[concepts/linear-regression-model]] section 8.5 applies: a statistically significant LR test **does not** prove the model is correctly specified, and does not test Tobit's assumptions (especially the normality assumption on $\varepsilon$, which matters far more than in OLS since the entire log-likelihood rests on this assumption).</span>

## 9. Bẫy thi tổng hợp (exam traps) — mở rộng - <span class="en">Consolidated exam traps — expanded</span>

1. **Chạy OLS trực tiếp trên biến censored** (dù giữ nguyên các quan sát $y=0$ hay loại bỏ chúng) — luôn cho ước lượng chệch, bất kể tỷ lệ censor cao hay thấp (mục 3).
<br><span class="en">**Running OLS directly on a censored variable** (whether keeping the $y=0$ observations or dropping them) — always yields a biased estimate, regardless of whether the censoring rate is high or low (section 3).</span>
2. **Áp dụng Tobit cho dữ liệu truncated** (không phải censored) — Tobit không phù hợp, vì likelihood của nó cần biết $X$ của cả quan sát bị "cắt", điều không có sẵn với truncated data (mục 2.4).
<br><span class="en">**Applying Tobit to truncated data** (not censored) — Tobit is not appropriate, since its likelihood needs to know $X$ for the "cut" observations too, which is not available with truncated data (section 2.4).</span>
3. **Nhầm censored với truncated** khi đọc đề bài — kiểm tra kỹ: đề có nói "vẫn biết đặc điểm của người bị loại/bị gán 0" (censored) hay "hoàn toàn không có thông tin gì về người bị loại" (truncated)?
<br><span class="en">**Confusing censored with truncated** when reading the exam question — check carefully: does the question say "we still know the characteristics of those excluded/assigned 0" (censored) or "we have absolutely no information about those excluded" (truncated)?</span>
4. **Bẫy lớn nhất: chọn nhầm loại prediction/marginal effect cho đúng câu hỏi nghiên cứu.** Cụ thể:
<br><span class="en">**The biggest trap: choosing the wrong type of prediction/marginal effect for the actual research question.** Specifically:</span>
   - Dùng thẳng $\beta$ (latent ME) để trả lời "hiệu ứng lên số dư nợ thực tế" — sai, vì $\beta$ là hiệu ứng lên $y^*$ (biến ẩn có thể âm), không phải lên $y$ quan sát được. Trong ví dụ, $\beta_{interest}=-321.25$ trong khi hiệu ứng thực tế lên `balance` chỉ khoảng $-134$ đến $-103$ tùy loại.
   <br><span class="en">Using the raw $\beta$ (latent ME) to answer "the effect on the actual balance" — wrong, because $\beta$ is the effect on $y^*$ (the latent variable, which can be negative), not on the observed $y$. In the example, $\beta_{interest}=-321.25$ while the actual effect on `balance` is only about $-134$ to $-103$ depending on the type.</span>
   - Dùng **Unconditional ME** khi câu hỏi chỉ hỏi về nhóm **đã tham gia/đã vượt ngưỡng** (đáng lẽ phải dùng Conditional ME), hoặc ngược lại — dùng **Conditional ME** khi câu hỏi hỏi về **hiệu ứng tổng thể trên toàn bộ dân số/thị trường** (đáng lẽ phải dùng Unconditional ME). Từ khóa cần bắt trong đề: "trung bình toàn mẫu/dân số" → Unconditional; "trong số những người đã..." / "biết rằng $y>0$" → Conditional.
   <br><span class="en">Using **Unconditional ME** when the question only asks about the group **already participating/already past the threshold** (should have used Conditional ME instead), or the reverse — using **Conditional ME** when the question asks about the **aggregate effect over the entire population/market** (should have used Unconditional ME instead). Keywords to catch in the question: "average over the whole sample/population" → Unconditional; "among those who already..." / "given that $y>0$" → Conditional.</span>
   - Nhầm **ME trên giá trị $y$** với **ME trên xác suất $Pr(y>0)$** — hai đại lượng khác đơn vị hoàn toàn (USD/điểm phần trăm lãi suất, so với điểm phần trăm xác suất/điểm phần trăm lãi suất).
   <br><span class="en">Confusing **ME on the value of $y$** with **ME on the probability $Pr(y>0)$** — the two quantities have completely different units (USD per percentage point of interest, versus percentage points of probability per percentage point of interest).</span>
5. **Nhầm lẫn "at mean" và "average" (AME)** khi trích dẫn một con số marginal effect — hai con số này có thể khác nhau (mục 7.5); luôn nêu rõ phương pháp tính khi báo cáo.
<br><span class="en">**Confusing "at mean" and "average" (AME)** when citing a marginal effect number — the two numbers can differ (section 7.5); always state clearly which method was used when reporting.</span>
6. **Coi LR test có ý nghĩa thống kê là "mô hình đúng/phù hợp"** — cùng lỗi diễn giải như F-test overall ở [[concepts/linear-regression-model]] mục 8.5; LR test không kiểm tra đặc tả mô hình hay giả định phân phối chuẩn của Tobit.
<br><span class="en">**Treating a statistically significant LR test as "the model is correct/well-specified"** — the same interpretation error as the overall F-test in [[concepts/linear-regression-model]] section 8.5; the LR test does not test model specification or Tobit's normality assumption.</span>
7. **(Ghi chú phạm vi)** Course Outline có nhắc đến Heckman selection model cho trường hợp có yếu tố truncation/selection "nếu còn thời gian" (`if time allowed`) — nhưng **không được dạy** trong bản slide (`slides-11-iu.pdf`, 35 trang) đã dùng để viết trang này: không có bất kỳ đề cập nào đến "Heckman" hay "selection" trong toàn bộ nội dung slide (đã kiểm tra bằng full-text search). Trang concept này vì vậy chỉ dừng ở Tobit; nếu tài liệu bổ sung về Heckman xuất hiện sau này, cần ingest riêng và mở rộng mục 2.4/9 này.
<br><span class="en">**(Scope note)** The Course Outline mentions the Heckman selection model for cases with a truncation/selection element "if time allowed" — but it is **not taught** in the slide deck (`slides-11-iu.pdf`, 35 pages) used to write this page: there is no mention whatsoever of "Heckman" or "selection" anywhere in the slide content (verified via full-text search). This concept page therefore stops at Tobit; if supplementary material on Heckman appears later, it should be ingested separately and this page's section 2.4/9 expanded.</span>

## 10. Kết nối với phần còn lại của khóa học - <span class="en">Connections to the rest of the course</span>

- Cấu trúc **latent variable** $y^*=X\beta+\varepsilon$ với ngưỡng cắt giống hệt [[concepts/ordinal-response-models]] — khác biệt là Tobit chỉ có một ngưỡng cố định (tại 0, hoặc $a,b$ đã biết trước), trong khi ordinal model có nhiều ngưỡng và các ngưỡng đó thường được ước lượng.
<br><span class="en">The **latent variable** structure $y^*=X\beta+\varepsilon$ with a cut threshold is identical to [[concepts/ordinal-response-models]] — the difference is that Tobit has only one fixed threshold (at 0, or known $a,b$), while the ordinal model has multiple thresholds and those thresholds are usually estimated.</span>
- Việc phân biệt rõ **hệ số thô $\beta$ và marginal effect thực sự** (luôn cần nhân thêm một hàm mật độ/CDF, không phải hằng số) là chủ đề xuyên suốt của toàn bộ Part 2 — xuất hiện y hệt ở [[concepts/binary-response-models]] (Probit/Logit) và tái xuất hiện phức tạp hơn ở đây với BA loại ME thay vì một.
<br><span class="en">Clearly distinguishing the **raw coefficient $\beta$ from the true marginal effect** (which always requires multiplying by a density/CDF function, not a constant) is a theme running throughout all of Part 2 — it appears identically in [[concepts/binary-response-models]] (Probit/Logit) and reappears more complex here with THREE types of ME instead of one.</span>
- $\Phi(\cdot)$ và cấu trúc "xác suất censor" của Tobit dùng chung công cụ toán học (CDF chuẩn) với Probit trong [[concepts/binary-response-models]] — về bản chất, "bị censor hay không" là một quyết định nhị phân ẩn bên trong Tobit.
<br><span class="en">$\Phi(\cdot)$ and Tobit's "censoring probability" structure share the same mathematical tool (the normal CDF) with Probit in [[concepts/binary-response-models]] — fundamentally, "censored or not" is a hidden binary decision inside Tobit.</span>
- Đại lượng $\lambda$ (inverse Mills ratio) xuất hiện trong Unconditional/Conditional expected value (mục 7.2–7.3) là cùng cấu trúc toán học sẽ tái xuất hiện trong **Heckman selection model** — mô hình chuẩn để xử lý sample selection/truncation có yếu tố hệ thống, nhưng **không được dạy trong slide này** (xem ghi chú phạm vi ở mục 9).
<br><span class="en">The quantity $\lambda$ (inverse Mills ratio) appearing in the Unconditional/Conditional expected value (sections 7.2–7.3) is the same mathematical structure that will reappear in the **Heckman selection model** — the standard model for handling sample selection/truncation with a systematic element, but **not taught in this slide deck** (see the scope note in section 9).</span>
- Đây là bài cuối của **Part 2 (Models for Limited Dependent Variables)** — sau bài này, khóa học quay lại **Panel Data** ở Part 3, mở rộng khung OLS/panel đã học ở [[concepts/fixed-random-effects-model]] sang các cấu trúc phương sai phức tạp hơn.
<br><span class="en">This is the final lesson of **Part 2 (Models for Limited Dependent Variables)** — after this lesson, the course returns to **Panel Data** in Part 3, extending the OLS/panel framework learned in [[concepts/fixed-random-effects-model]] to more complex variance structures.</span>

## 10. Tài liệu tham khảo ứng dụng thực tế - <span class="en">Real-world application references</span>

Ba bài báo gần đây minh họa Tobit model trong nghiên cứu kinh tế thực tế (đề cương Lecture 13):
<br><span class="en">Three recent papers illustrating the Tobit model in real-world economic research (Lecture 13 syllabus):</span>

- Liu, H., Wahl, T. I., Seale, J. L., & Bai, J. (2015). Household composition, income, and food-away-from-home expenditure in urban China. *Food Policy*, 51, 97-103. https://doi.org/10.1016/j.foodpol.2014.12.011
- Basnet, H. C., & Donou-Adonsou, F. (2016). Internet, consumer spending, and credit card balance: Evidence from US consumers. *Review of Financial Economics*, 30, 11-22. https://doi.org/10.1016/j.rfe.2016.01.002
- Jiang, H., Livingston, M., Room, R., & Callinan, S. (2016). Price elasticity of on- and off-premises demand for alcoholic drinks: A Tobit analysis. *Drug and Alcohol Dependence*, 163, 222-228. https://doi.org/10.1016/j.drugalcdep.2016.04.026
