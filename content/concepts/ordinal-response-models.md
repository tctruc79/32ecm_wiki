---
title: "Lecture 11: Ordinal Response Models (Ordered Logit/Probit)"
type: concept
status: mature
tags: [ordinal-response, ordered-probit, ordered-logit, brant-test, limited-dependent-variable]
sources: ["[[sources/slides-9-ordinal-response-models]]"]
related: ["[[concepts/binary-response-models]]", "[[concepts/multinomial-logit-model]]"]
lecture: 11
assignment: []
updated: 2026-09-04
---

> **Cách đọc trang này**: đây là Topic 9, tiếp nối trực tiếp [[concepts/binary-response-models]] (biến phụ thuộc nhị phân, Topic 7) và song song với [[concepts/multinomial-logit-model]] (biến phụ thuộc phân loại không thứ tự, Topic 8). Nếu chưa quen với ý tưởng "biến phụ thuộc rời rạc, ước lượng bằng Maximum Likelihood thay vì OLS", nên đọc [[concepts/binary-response-models]] trước — trang đó xây khung log-likelihood, LR test, marginal effects mà trang này tái sử dụng gần như nguyên vẹn, chỉ thêm một lớp phức tạp: **thứ tự** giữa các phạm trù.
> <br><span class="en">**How to read this page**: this is Topic 9, a direct continuation of [[concepts/binary-response-models]] (binary dependent variable, Topic 7) and a parallel to [[concepts/multinomial-logit-model]] (unordered categorical dependent variable, Topic 8). If you're not yet familiar with the idea "discrete dependent variable, estimated by Maximum Likelihood instead of OLS," read [[concepts/binary-response-models]] first — that page builds the log-likelihood framework, LR test, and marginal effects that this page reuses almost unchanged, adding only one extra layer of complexity: **order** among the categories.</span>

**Lecture 11** trong đề cương (CO Topic 9) — chưa có assignment riêng.
<br><span class="en">**Lecture 11** in the syllabus (CO Topic 9) — no dedicated assignment yet.</span>

## 1. Bài toán ordinal response là gì? - <span class="en">What is the ordinal response problem?</span>

### 1.1 Biến phụ thuộc "có thứ tự" nghĩa là gì - <span class="en">What an "ordered" dependent variable means</span>

Rất nhiều biến kết quả trong khảo sát kinh tế/xã hội là **rời rạc** (discrete, chỉ nhận một số hữu hạn giá trị) **và có thứ tự tự nhiên** (ordered), nhưng **không có đơn vị đo** (no measurement unit) — nghĩa là khoảng cách giữa các mức không có ý nghĩa số học rõ ràng.
<br><span class="en">Many outcome variables in economic/social surveys are **discrete** (taking only a finite number of values) **and naturally ordered**, but have **no measurement unit** — meaning the distance between levels has no clear numerical meaning.</span>
Hai ví dụ slide dùng để mở đầu:
<br><span class="en">Two examples the slides use to open with:</span>

- **Self-reported health status** theo thang Likert: kém / trung bình / tốt / rất tốt.
  <br><span class="en">**Self-reported health status** on a Likert scale: poor / average / good / very good.</span>
- **Mức độ đồng ý với một phát biểu**: hoàn toàn không đồng ý / không đồng ý / trung lập / đồng ý / hoàn toàn đồng ý.
  <br><span class="en">**Level of agreement with a statement**: strongly disagree / disagree / neutral / agree / strongly agree.</span>

Ví dụ xuyên suốt của slide (dùng lại ở mọi phần sau của trang này): **tần suất ăn ngoài hàng tuần** (`eatout`), ban đầu slide minh họa với 3 mức đơn giản (0 = không lần nào; 1 = 1–2 lần/tuần; 2 = từ 3 lần trở lên), sau đó bộ dữ liệu thực hành mở rộng thành 5 mức chi tiết hơn (xem mục 7).
<br><span class="en">The running example of the slides (reused throughout every later section of this page): **weekly eating-out frequency** (`eatout`), first illustrated by the slides with 3 simple levels (0 = no times; 1 = 1–2 times/week; 2 = 3 or more times), later expanded by the practice dataset into 5 more detailed levels (see section 7).</span>
Điểm chung của mọi ví dụ này: ta biết "nhiều hơn" hay "ít hơn", nhưng **không biết khoảng cách giữa 'kém' và 'trung bình' có bằng khoảng cách giữa 'trung bình' và 'tốt' hay không** — đây chính là đặc điểm định nghĩa nên "ordinal".
<br><span class="en">What all these examples share: we know "more" or "less," but **we don't know whether the distance between 'poor' and 'average' equals the distance between 'average' and 'good'** — this is precisely the defining feature of "ordinal."</span>

### 1.2 Vì sao không dùng OLS, và vì sao MNL "phí" thông tin - <span class="en">Why not OLS, and why MNL "wastes" information</span>

Slide đặt câu hỏi trực tiếp: nếu biến này là biến phụ thuộc, ta ước lượng bằng gì?
<br><span class="en">The slide asks directly: if this variable is the dependent variable, what do we estimate it with?</span>

| Cách tiếp cận - <span class="en">Approach</span> | Dùng được không? - <span class="en">Usable?</span> | Vì sao - <span class="en">Why</span> |
|---|---|---|
| **OLS** ([[concepts/linear-regression-model]]) | ❌ Không - <span class="en">No</span> | Biến không có đơn vị đo (no measurement unit) — chạy OLS trực tiếp lên mã số 0/1/2/3/4 ngầm giả định khoảng cách giữa mọi cặp mức **bằng nhau** (khoảng cách "0→1" = khoảng cách "3→4"), một giả định gần như không bao giờ đúng với dữ liệu Likert hay tần suất tự báo cáo. Hệ số OLS trong trường hợp này không có cách diễn giải hợp lý về mặt kinh tế lượng. <br><span class="en">The variable has no measurement unit — running OLS directly on the codes 0/1/2/3/4 implicitly assumes the distance between every pair of levels is **equal** (distance "0→1" = distance "3→4"), an assumption that is almost never true for Likert or self-reported frequency data. The OLS coefficient in this case has no sound econometric interpretation.</span> |
| **MNL** ([[concepts/multinomial-logit-model]]) | ⚠️ Áp dụng được, nhưng không nên - <span class="en">Technically usable, but not advisable</span> | MNL coi mỗi phạm trù là một lựa chọn độc lập, không giả định thứ tự gì cả — nên **dùng được về mặt kỹ thuật**, nhưng (a) phức tạp không cần thiết (ước lượng riêng một bộ hệ số cho từng phạm trù so với phạm trù nền — với 5 phạm trù là 4 bộ hệ số riêng biệt) và (b) **bỏ phí thông tin thứ tự** vốn có sẵn trong dữ liệu — ta biết "3–5 lần/tháng" nằm giữa "1–2 lần" và "6–10 lần" nhưng MNL không tận dụng thông tin đó. <br><span class="en">MNL treats each category as an independent choice, assuming no ordering at all — so it is **technically usable**, but (a) it is unnecessarily complex (estimating a separate coefficient set for each category relative to the base category — with 5 categories that's 4 separate coefficient sets) and (b) it **wastes the ordering information** already present in the data — we know "3–5 times/month" lies between "1–2 times" and "6–10 times," but MNL does not exploit that information.</span> |
| **Ordered Probit / Ordered Logit** | ✅ Đúng công cụ - <span class="en">The right tool</span> | Thiết kế riêng cho biến rời rạc có thứ tự: tiết kiệm tham số hơn MNL (chỉ một bộ hệ số $\beta$ dùng chung — xem mục 9) và không áp đặt giả định "khoảng cách bằng nhau" như OLS. <br><span class="en">Purpose-built for discrete ordered variables: more parameter-efficient than MNL (only one shared coefficient set $\beta$ — see section 9) and does not impose the "equal distance" assumption the way OLS does.</span> |

**Trực giác cần nhớ**: đây là bài toán nằm **giữa** binary response (chỉ 2 phạm trù, không có "thứ tự" để nói vì chỉ có một ranh giới) và MNL (nhiều phạm trù nhưng không thứ tự).
<br><span class="en">**Intuition to remember**: this problem sits **between** binary response (only 2 categories, no "order" to speak of since there is only one boundary) and MNL (many categories but no order).</span>
Ordinal response là "nhiều phạm trù **và** có thứ tự" — điều đó cho phép dùng chung **một chỉ số liên tục duy nhất** để mô tả toàn bộ hiện tượng, thay vì nhiều bộ hệ số như MNL. Đó chính là ý tưởng "latent variable" ở mục 2.
<br><span class="en">Ordinal response is "many categories **and** ordered" — that allows a **single continuous index** to describe the entire phenomenon, instead of the multiple coefficient sets MNL requires. That is exactly the "latent variable" idea in section 2.</span>

## 2. Latent variable framework — ý tưởng cốt lõi (và khó nhất) - <span class="en">Latent variable framework — the core (and hardest) idea</span>

Đây là khái niệm nền tảng của toàn bộ mô hình, và cũng là điểm dễ gây rối nhất với người mới học. Trực giác:
<br><span class="en">This is the foundational concept of the whole model, and also the point most likely to confuse newcomers. Intuition:</span>

> Đằng sau con số rời rạc $y$ mà ta *quan sát được* (0, 1, 2, 3, 4…), có một biến **liên tục, không quan sát được** $y^*$ — gọi là **latent variable** (biến tiềm ẩn) hay **index variable** (biến chỉ số) — đo mức độ/cường độ "thật" của hiện tượng đang nghiên cứu. Khi khảo sát buộc người trả lời chọn một trong số hữu hạn các mức, con số liên tục đó bị "cắt" thành các khoảng rời rạc.
> <br><span class="en">Behind the discrete number $y$ that we *observe* (0, 1, 2, 3, 4…), there is a **continuous, unobserved** variable $y^*$ — called the **latent variable** or **index variable** — measuring the "true" degree/intensity of the phenomenon under study. When a survey forces the respondent to pick one of a finite set of levels, that continuous number gets "cut" into discrete intervals.</span>

Ví dụ cụ thể với `eatout`: mỗi cá nhân có một "khuynh hướng ăn ngoài" (propensity to eat out) — chịu ảnh hưởng của thu nhập, tuổi tác, tình trạng hôn nhân, sở thích cá nhân — và khuynh hướng này về bản chất là một đại lượng **liên tục** (không ai thực sự "nhảy" đột ngột từ mức 0 sang mức 5 lần/tháng; khuynh hướng tăng dần một cách trơn tru theo các yếu tố quyết định). Nhưng khi đi khảo sát, ta chỉ hỏi được "bạn ăn ngoài bao nhiêu lần/tháng, chọn một trong 5 khoảng" — câu trả lời $y$ chỉ cho biết khuynh hướng liên tục đó **rơi vào khoảng nào**, không cho biết giá trị chính xác của nó.
<br><span class="en">A concrete example with `eatout`: each individual has a "propensity to eat out" — influenced by income, age, marital status, personal preference — and this propensity is by nature a **continuous** quantity (no one truly "jumps" abruptly from level 0 to level 5 times/month; the propensity rises smoothly with its determinants). But when surveyed, we can only ask "how many times a month do you eat out, choose one of 5 bins" — the answer $y$ only tells us which interval that continuous propensity **falls into**, not its exact value.</span>
Một ví dụ khác dễ hình dung hơn: "mức độ hài lòng" của một khách hàng thực chất là một **cảm nhận liên tục** trong đầu người đó (có thể rất hài lòng, hơi hài lòng, hài lòng vừa phải…) — nhưng bảng khảo sát chỉ cho phép chọn "kém / trung bình / tốt / rất tốt", nên câu trả lời quan sát được chỉ là **bản rời rạc hóa** của cảm nhận liên tục đó.
<br><span class="en">Another, easier-to-picture example: a customer's "satisfaction level" is really a **continuous feeling** in that person's mind (could be very satisfied, mildly satisfied, moderately satisfied…) — but the survey form only allows "poor / average / good / very good," so the observed answer is just a **discretized version** of that continuous feeling.</span>

Hình thức hóa: $y^*$ được mô hình như một hàm tuyến tính của $X$ cộng sai số, giống hệt cấu trúc của PRE ở [[concepts/linear-regression-model]]:
<br><span class="en">Formally: $y^*$ is modeled as a linear function of $X$ plus an error term, exactly the same structure as the PRE in [[concepts/linear-regression-model]]:</span>

$$y^*=\beta X+\varepsilon = \beta_1 x_1 + \cdots + \beta_k x_k + \varepsilon$$

$y^*$ càng cao thì cường độ/khuynh hướng của hiện tượng càng cao — giống $y$ quan sát được về mặt *thứ tự*, nhưng khác nhau về *bản chất*: $y^*$ liên tục và không có giới hạn trên/dưới, còn $y$ chỉ nhận một số hữu hạn giá trị nguyên.
<br><span class="en">The higher $y^*$, the higher the intensity/propensity of the phenomenon — matching observed $y$ in terms of *ordering*, but different in *nature*: $y^*$ is continuous and unbounded above/below, while $y$ takes only a finite number of integer values.</span>

**Hình dung trên trục số**: đặt $y^*$ lên một trục số liên tục, các **cutpoints** (mục 3) chia trục này thành các đoạn — mỗi đoạn ứng với một mức của $y$ quan sát được:
<br><span class="en">**Picturing it on a number line**: place $y^*$ on a continuous number line; the **cutpoints** (section 3) divide this line into segments — each segment corresponds to one level of observed $y$:</span>

```
 y* : ───────────●────────────●────────────●────────────●───────────→
                 u1           u2           u3           u4
        y=0      │     y=1    │     y=2    │     y=3    │     y=4
       (No)      │  (1-2/th)  │  (3-5/th)  │ (5-10/th)  │  (11+/th)
```

Bất kỳ cá nhân nào có $y^*$ rơi vào đoạn giữa $u_2$ và $u_3$ sẽ được quan sát là $y=2$, bất kể giá trị chính xác của $y^*$ trong đoạn đó là bao nhiêu — đây chính là lý do gọi $y^*$ là "latent" (tiềm ẩn/ẩn giấu): nó tồn tại về mặt lý thuyết, chi phối hành vi quan sát được, nhưng bản thân giá trị của nó thì **không bao giờ đo được trực tiếp**, y hệt cách $\beta$ (population) không bao giờ quan sát được trực tiếp trong LRM — chỉ khác ở đây thứ "không quan sát được" là chính biến số, không phải hệ số.
<br><span class="en">Any individual whose $y^*$ falls between $u_2$ and $u_3$ will be observed as $y=2$, regardless of the exact value of $y^*$ within that segment — this is precisely why $y^*$ is called "latent": it exists theoretically, governs the observed behavior, but its own value is **never directly measurable**, exactly the way the (population) $\beta$ is never directly observed in the LRM — the only difference here is that the "unobservable" thing is the variable itself, not the coefficient.</span>

## 3. Cutpoints (threshold parameters) — điểm cắt - <span class="en">Cutpoints (threshold parameters)</span>

Với $J$ phạm trù (VD $J=3$: $y\in\{0,1,2\}$ như slide minh họa ban đầu), cần $J-1$ **cutpoints** $u_1<u_2<\cdots<u_{J-1}$ để chia trục $y^*$ thành $J$ đoạn. Quy tắc liên hệ $y^*$ với $y$ quan sát được (minh họa 3 phạm trù):
<br><span class="en">With $J$ categories (e.g. $J=3$: $y\in\{0,1,2\}$ as the slide first illustrates), $J-1$ **cutpoints** $u_1<u_2<\cdots<u_{J-1}$ are needed to divide the $y^*$ axis into $J$ segments. The rule linking $y^*$ to the observed $y$ (illustrated with 3 categories):</span>

$$y=0 \text{ nếu } y^*\le u_1, \qquad y=1 \text{ nếu } u_1<y^*\le u_2, \qquad y=2 \text{ nếu } y^*> u_2$$
<br><span class="en">(read: $y=0$ if $y^*\le u_1$; $y=1$ if $u_1<y^*\le u_2$; $y=2$ if $y^*> u_2$)</span>

**Ý nghĩa của cutpoints**: chúng là các **tham số ngưỡng** (threshold parameters) — không phải là "hệ số chặn" (intercept) theo nghĩa thông thường của OLS, dù trong output phần mềm (R) chúng được liệt kê dưới tên **"Intercepts"**. Mô hình ước lượng **đồng thời** $\beta$ **và** các cutpoints $u_j$ bằng Maximum Likelihood (mục 5) — cả hai đều là tham số chưa biết, không ai được cho trước.
<br><span class="en">**What cutpoints mean**: they are **threshold parameters** — not an "intercept" in the usual OLS sense, even though R's software output lists them under the name **"Intercepts."** The model estimates $\beta$ **and** the cutpoints $u_j$ **simultaneously** by Maximum Likelihood (section 5) — both are unknown parameters, neither is given in advance.</span>

**Một chi tiết cấu trúc quan trọng, dễ bị bỏ qua**: phương trình $y^*=\beta X+\varepsilon$ **không có hệ số chặn $\beta_0$ riêng** như PRE của LRM. Lý do: với chỉ một cutpoint (trường hợp binary, $J=2$), việc có cả một cutpoint tự do *và* một intercept tự do sẽ **không xác định được** (identification) — hai tham số "cạnh tranh" vai trò dịch chuyển trục số theo cùng một hướng. Ordinal model giải quyết bằng cách bỏ hẳn $\beta_0$ ra khỏi $X\beta$, để các cutpoints $u_j$ đảm nhiệm vai trò "định vị" đó.
<br><span class="en">**An important structural detail, easy to overlook**: the equation $y^*=\beta X+\varepsilon$ **has no separate intercept $\beta_0$** the way the LRM's PRE does. Reason: with only one cutpoint (the binary case, $J=2$), having both a free cutpoint *and* a free intercept would make the model **unidentified** (identification) — the two parameters "compete" for the role of shifting the number line in the same direction. The ordinal model resolves this by dropping $\beta_0$ entirely from $X\beta$, letting the cutpoints $u_j$ take over that "positioning" role.</span>
Điều này thấy rõ ngay trong code ước lượng ở ví dụ thực hành (mục 7): công thức mô hình `eatout ~ age + whours + income + homeown + gender + inrelationship + married` không có số hạng intercept, và R báo cáo riêng "No coefficients" cho intercept ở mô hình rỗng — chỉ có mục "Intercepts:" (chính là các cutpoints) được ước lượng.
<br><span class="en">This is clearly visible in the estimation code in the practical example (section 7): the model formula `eatout ~ age + whours + income + homeown + gender + inrelationship + married` has no intercept term, and R separately reports "No coefficients" for the intercept in the null model — only the "Intercepts:" section (i.e., the cutpoints) gets estimated.</span>

**Minh họa cutpoints "trần trụi"**: mô hình null (chỉ có cutpoints, không có biến $X$ nào — `eatout ~ 1`) trong ví dụ thực hành mục 7.3 là cách trực quan nhất để thấy cutpoints hoạt động độc lập với $\beta$ — vì $X\beta=0$, các cutpoints ước lượng được ở mô hình null chính là ngưỡng phân định phân phối biên (marginal/unconditional) của $y$, không điều chỉnh gì theo đặc điểm cá nhân.
<br><span class="en">**Cutpoints "in the raw"**: the null model (only cutpoints, no $X$ variables — `eatout ~ 1`) in the practical example section 7.3 is the clearest way to see cutpoints working independently of $\beta$ — since $X\beta=0$, the cutpoints estimated in the null model are exactly the thresholds delimiting the marginal/unconditional distribution of $y$, with no adjustment for individual characteristics.</span>

## 4. Xác suất mỗi phạm trù — suy ra công thức - <span class="en">Probability of each category — deriving the formula</span>

### 4.1 Trường hợp minh họa: 3 phạm trù, giả định $\varepsilon$ chuẩn (Ordered Probit) - <span class="en">Illustrative case: 3 categories, normal $\varepsilon$ assumption (Ordered Probit)</span>

**$Pr(y=0)$**: dùng quy tắc ở mục 3,
<br><span class="en">**$Pr(y=0)$**: using the rule from section 3,</span>

$$Pr(y=0)=Pr(y^*\le u_1)=Pr(\beta X+\varepsilon\le u_1)=Pr(\varepsilon\le u_1-\beta X)=\Phi(u_1-\beta X)$$

với $\Phi(\cdot)$ là hàm phân phối tích lũy (CDF) của phân phối chuẩn hóa (standard normal).
<br><span class="en">where $\Phi(\cdot)$ is the cumulative distribution function (CDF) of the standard normal distribution.</span>

**$Pr(y=2)$** (phạm trù cao nhất), suy luận tương tự:
<br><span class="en">**$Pr(y=2)$** (the highest category), by the same reasoning:</span>

$$Pr(y=2)=Pr(y^*> u_2)=Pr(\varepsilon> u_2-\beta X)=Pr(\varepsilon\le \beta X-u_2)=\Phi(\beta X-u_2)$$

(bước cuối dùng tính đối xứng của phân phối chuẩn quanh 0).
<br><span class="en">(the last step uses the symmetry of the normal distribution around 0).</span>

**$Pr(y=1)$** (phạm trù giữa) — là hiệu của hai xác suất tích lũy:
<br><span class="en">**$Pr(y=1)$** (the middle category) — is the difference of two cumulative probabilities:</span>

$$Pr(y=1)=Pr(u_1<y^*\le u_2)=Pr(y^*\le u_2)-Pr(y^*\le u_1)=\Phi(u_2-\beta X)-\Phi(u_1-\beta X)$$

**Tổng luôn bằng 1**: $\Phi(\beta X-u_2)=1-\Phi(u_2-\beta X)$ (đối xứng), nên $Pr(y=0)+Pr(y=1)+Pr(y=2)=\Phi(u_1-\beta X)+[\Phi(u_2-\beta X)-\Phi(u_1-\beta X)]+[1-\Phi(u_2-\beta X)]=1$ — một cách tự kiểm tra công thức khi tính tay.
<br><span class="en">**The sum always equals 1**: $\Phi(\beta X-u_2)=1-\Phi(u_2-\beta X)$ (symmetry), so $Pr(y=0)+Pr(y=1)+Pr(y=2)=\Phi(u_1-\beta X)+[\Phi(u_2-\beta X)-\Phi(u_1-\beta X)]+[1-\Phi(u_2-\beta X)]=1$ — a useful self-check of the formulas when computing by hand.</span>

### 4.2 Tổng quát hóa cho $J$ phạm trù - <span class="en">Generalizing to $J$ categories</span>

Slide minh họa lý thuyết bằng 3 phạm trù, nhưng ví dụ thực hành ở mục 7 dùng **5 phạm trù** (`eatout` = No / 1–2 / 3–5 / 5–10 / 11+ lần/tháng) — nên cần nối hai phần này lại. Với $J$ phạm trù $y\in\{0,1,\dots,J-1\}$ và $J-1$ cutpoints $u_1<\cdots<u_{J-1}$, cùng logic ở mục 4.1 tổng quát hóa thành:
<br><span class="en">The slide illustrates the theory with 3 categories, but the practical example in section 7 uses **5 categories** (`eatout` = No / 1–2 / 3–5 / 5–10 / 11+ times/month) — so the two need to be connected. With $J$ categories $y\in\{0,1,\dots,J-1\}$ and $J-1$ cutpoints $u_1<\cdots<u_{J-1}$, the same logic from section 4.1 generalizes to:</span>

$$Pr(y=0)=\Phi(u_1-\beta X), \qquad Pr(y=J-1)=1-\Phi(u_{J-1}-\beta X)$$
$$Pr(y=j)=\Phi(u_{j+1}-\beta X)-\Phi(u_j-\beta X) \quad \text{với } j=1,\dots,J-2 \text{ (các phạm trù ở giữa)}$$
<br><span class="en">(the second line: $Pr(y=j)=\Phi(u_{j+1}-\beta X)-\Phi(u_j-\beta X)$ for $j=1,\dots,J-2$, i.e. the categories in between)</span>

Với `eatout` ($J=5$, cutpoints $u_1,u_2,u_3,u_4$):
<br><span class="en">For `eatout` ($J=5$, cutpoints $u_1,u_2,u_3,u_4$):</span>

$$Pr(No)=\Phi(u_1-X\beta),\quad Pr(1\text{–}2)=\Phi(u_2-X\beta)-\Phi(u_1-X\beta),\quad\dots,\quad Pr(11+)=1-\Phi(u_4-X\beta)$$

Đúng 5 công thức xác suất, mỗi công thức ứng với một hàng trong bảng "Intercepts" mà R báo cáo (mục 7).
<br><span class="en">Exactly 5 probability formulas, each corresponding to one row in the "Intercepts" table R reports (section 7).</span>

## 5. Log-likelihood function - <span class="en">Log-likelihood function</span>

$$LL=\sum_i \sum_k Y_{ik}\ln Pr(y_i=k), \qquad Y_{ik}=\begin{cases}1 & \text{nếu } y_i=k\\0 & \text{nếu ngược lại}\end{cases}$$
<br><span class="en">(where $Y_{ik}=1$ if $y_i=k$, and $0$ otherwise)</span>

Cấu trúc **giống hệt** log-likelihood của Logit/Probit nhị phân ([[concepts/binary-response-models]]) và của MNL ([[concepts/multinomial-logit-model]]) — chỉ khác cách tính $Pr(y_i=k)$ (ở đây là hiệu của hai CDF liên tiếp, thay vì công thức softmax của MNL hay công thức nhị phân đơn giản). Đây là "sợi chỉ chung" xuyên suốt toàn bộ Part 2 của khóa học mà mục Kết nối (mục 12) sẽ nhắc lại: mọi mô hình discrete-choice trong khóa học đều ước lượng bằng Maximum Likelihood trên cùng một khung log-likelihood tổng quát này, chỉ thay công thức $Pr(y_i=k)$.
<br><span class="en">The structure is **exactly the same** as the log-likelihood of binary Logit/Probit ([[concepts/binary-response-models]]) and of MNL ([[concepts/multinomial-logit-model]]) — the only difference is how $Pr(y_i=k)$ is computed (here, the difference of two consecutive CDFs, instead of MNL's softmax formula or the simple binary formula). This is the "common thread" running through the entire Part 2 of the course, which the Connections section (section 12) will revisit: every discrete-choice model in the course is estimated by Maximum Likelihood on this same general log-likelihood framework, only swapping the formula for $Pr(y_i=k)$.</span>

## 6. Ordered Logit vs. Ordered Probit - <span class="en">Ordered Logit vs. Ordered Probit</span>

Cùng logic phân biệt Logit/Probit nhị phân ([[concepts/binary-response-models]]): sự khác biệt nằm ở **giả định phân phối của sai số $\varepsilon$** trong phương trình $y^*=\beta X+\varepsilon$.
<br><span class="en">The same logic that distinguishes binary Logit/Probit ([[concepts/binary-response-models]]) applies: the difference lies in the **assumed distribution of the error $\varepsilon$** in the equation $y^*=\beta X+\varepsilon$.</span>

| | Phân phối $\varepsilon$ - <span class="en">Distribution of $\varepsilon$</span> | Hàm liên kết - <span class="en">Link function</span> | VD $Pr(y=0)$ - <span class="en">e.g. $Pr(y=0)$</span> |
|---|---|---|---|
| **Ordered Probit** | Chuẩn (normal) - <span class="en">Normal</span> | $\Phi(\cdot)$ | $\Phi(u_1-\beta X)$ |
| **Ordered Logit** | Logistic - <span class="en">Logistic</span> | $\Lambda(x)=\dfrac{1}{1+e^{-x}}$ | $\Lambda(u_1-\beta X)$ |

**Khác biệt so với trường hợp binary**: ở mô hình nhị phân, **Logit** thường được ưu tiên hơn (marginal effect có dạng đóng, dễ tính hơn Probit). Ở mô hình **ordinal**, slide ghi rõ chiều ngược lại: **"Probit is more popular"** (Probit phổ biến hơn) trong thực hành. Slide không giải thích lý do cụ thể — ghi nhận đây là một phát biểu thực hành (convention), không phải một định lý.
<br><span class="en">**Difference from the binary case**: in the binary model, **Logit** is usually preferred (the marginal effect has a closed form, easier to compute than Probit). In the **ordinal** model, the slide explicitly notes the opposite direction: **"Probit is more popular"** in practice. The slide does not explain the specific reason — note that this is a practical statement (convention), not a theorem.</span>

## 7. Ví dụ đầy đủ: Tần suất ăn ngoài (`eatout`) - <span class="en">Full example: eating-out frequency (`eatout`)</span>

### 7.1 Dữ liệu - <span class="en">Data</span>

| Biến - <span class="en">Variable</span> | Ý nghĩa - <span class="en">Meaning</span> |
|---|---|
| `eatout` (depvar) | Tần suất ăn ngoài/tháng — ordinal, 5 mức: 0 = "No"; 1 = "1–2 times/month"; 2 = "3–5 times/month"; 3 = "6–10 times/month"; 4 = "11 times/month or more" <br><span class="en">Eating-out frequency/month — ordinal, 5 levels: 0 = "No"; 1 = "1–2 times/month"; 2 = "3–5 times/month"; 3 = "6–10 times/month"; 4 = "11 times/month or more"</span> |
| `age` | Tuổi (năm) <br><span class="en">Age (years)</span> |
| `whours` | Số giờ làm việc/tuần <br><span class="en">Weekly working hours</span> |
| `income` | Thu nhập hàng tháng (triệu VND/tháng) <br><span class="en">Monthly income (million VND/month)</span> |
| `homeown` | 1 nếu là chủ nhà, 0 nếu ngược lại <br><span class="en">1 if homeowner, 0 otherwise</span> |
| `gender` | 1 nếu là nam, 0 nếu ngược lại <br><span class="en">1 if male, 0 otherwise</span> |
| `marriage` | biến gốc dạng chữ: "single" / "inrelationship" / "married" → sinh ra 2 dummy `inrelationship`, `married` (nhóm nền/base là "single") <br><span class="en">original text-valued variable: "single" / "inrelationship" / "married" → generates 2 dummies `inrelationship`, `married` (base group is "single")</span> |

**Phân phối `eatout`** (`barplot(table(data$eatout))`): No ≈ 280 quan sát (đông nhất), 1–2/tháng ≈ 160, 3–5/tháng ≈ 235, 5–10/tháng ≈ 220, 11+/tháng ≈ 50 (ít nhất) — phân phối lệch, tập trung nhiều ở "No" và các mức trung bình, thưa dần ở mức cao nhất.
<br><span class="en">**Distribution of `eatout`** (`barplot(table(data$eatout))`): No ≈ 280 observations (largest), 1–2/month ≈ 160, 3–5/month ≈ 235, 5–10/month ≈ 220, 11+/month ≈ 50 (smallest) — a skewed distribution, concentrated heavily on "No" and the middle levels, thinning out at the highest level.</span>

### 7.2 Mô hình null (chỉ cutpoints, không biến X) — `polr(eatout ~ 1, method="probit")` - <span class="en">Null model (cutpoints only, no X variables)</span>

| Cutpoint | Value | Std. Error | t value |
|---|---|---|---|
| No \| 1-2/month | −0.5425 | 0.0431 | −12.59 |
| 1-2/month \| 3-5/month | −0.0918 | 0.0409 | −2.25 |
| 3-5/month \| 5-10/month | 0.5611 | 0.0432 | 12.98 |
| 5-10/month \| 11 or more | 1.6162 | 0.0675 | 23.94 |

Residual Deviance: 2834.382; AIC: 2842.382. Đây chính là minh họa "cutpoints trần trụi" nhắc ở mục 3 — không có biến giải thích nào, các ngưỡng này chỉ phản ánh phân phối biên của `eatout` trong mẫu.
<br><span class="en">Residual Deviance: 2834.382; AIC: 2842.382. This is exactly the "cutpoints in the raw" illustration mentioned in section 3 — with no explanatory variables at all, these thresholds simply reflect the marginal distribution of `eatout` in the sample.</span>

### 7.3 Mô hình đầy đủ (Ordered Probit) — `polr(eatout ~ age + whours + income + homeown + gender + inrelationship + married, method="probit")` - <span class="en">Full model (Ordered Probit)</span>

**Hệ số $\beta$** (tác động lên $y^*$, chưa phải lên $Pr(y=k)$ — xem mục 8):
<br><span class="en">**Coefficients $\beta$** (the effect on $y^*$, not yet on $Pr(y=k)$ — see section 8):</span>

| Biến | Value | Std. Error | t value | p-value |
|---|---|---|---|---|
| `age` | −0.2900 | 0.0123 | −23.53 | 0.000 |
| `whours` | 0.0045 | 0.0025 | 1.81 | 0.071 |
| `income` | −0.0009 | 0.0049 | −0.19 | 0.849 |
| `homeown` | −2.8831 | 0.1307 | −22.06 | 0.000 |
| `gender` | −0.0760 | 0.0832 | −0.91 | 0.361 |
| `inrelationship` | 2.9727 | 0.1373 | 21.65 | 0.000 |
| `married` | 0.2040 | 0.1045 | 1.95 | 0.051 |

**Cutpoints (Intercepts):**
<br><span class="en">**Cutpoints (Intercepts):**</span>

| Cutpoint | Value | Std. Error | t value |
|---|---|---|---|
| No \| 1-2/month | −9.4303 | 0.4167 | −22.63 |
| 1-2/month \| 3-5/month | −8.2827 | 0.3945 | −21.00 |
| 3-5/month \| 5-10/month | −6.5769 | 0.3602 | −18.26 |
| 5-10/month \| 11 or more | −3.7760 | 0.3215 | −11.74 |

Residual Deviance: 1446.688; AIC: 1468.688 (giảm mạnh so với mô hình null → thêm biến giải thích cải thiện độ khớp đáng kể).
<br><span class="en">Residual Deviance: 1446.688; AIC: 1468.688 (a sharp drop compared to the null model → adding explanatory variables substantially improves fit).</span>

**Vì sao cutpoints ở mô hình full "trông rất khác" mô hình null** (từ khoảng −0.5→1.6 nhảy sang khoảng −9.4→−3.8)? Đây **không phải mâu thuẫn** mà là hệ quả trực tiếp của việc thêm $X\beta$ vào công thức: ở mô hình null, $X\beta=0$ nên cutpoints trực tiếp là ngưỡng của phân phối biên; ở mô hình full, các biến như `age` (tính bằng năm, không chuẩn hóa) hay `whours` đóng góp một lượng lớn vào $X\beta$, nên cutpoints phải dịch chuyển tương ứng để giữ xác suất dự đoán hợp lý. Cutpoints và $\beta$ luôn phải đọc **cùng nhau**, không tách rời.
<br><span class="en">**Why do the full model's cutpoints "look very different" from the null model's** (jumping from roughly −0.5→1.6 to roughly −9.4→−3.8)? This is **not a contradiction** but a direct consequence of adding $X\beta$ to the formula: in the null model, $X\beta=0$ so the cutpoints are directly the thresholds of the marginal distribution; in the full model, variables like `age` (measured in years, not standardized) or `whours` contribute a large amount to $X\beta$, so the cutpoints must shift accordingly to keep the predicted probabilities sensible. Cutpoints and $\beta$ must always be read **together**, never separately.</span>

**p-value** (đuôi hai phía, tính từ $t$ qua phân phối chuẩn — `pnorm`): với $\alpha=5\%$, các biến có ý nghĩa thống kê là `age`, `homeown`, `inrelationship` (p<0.001); `married` cận biên (p=0.051, không có ý nghĩa ở đúng 5% nhưng có ý nghĩa ở 10% — cùng bài học "ngưỡng $\alpha$ quyết định kết luận" như ở [[concepts/linear-regression-model]] mục 7.4); `whours`, `income`, `gender` không có ý nghĩa thống kê.
<br><span class="en">**p-value** (two-tailed, computed from $t$ via the normal distribution — `pnorm`): at $\alpha=5\%$, the statistically significant variables are `age`, `homeown`, `inrelationship` (p<0.001); `married` is borderline (p=0.051, not significant at exactly 5% but significant at 10% — the same "the $\alpha$ threshold determines the conclusion" lesson as in [[concepts/linear-regression-model]] section 7.4); `whours`, `income`, `gender` are not statistically significant.</span>

### 7.4 LR test cho overall significance — tương đương F-test tổng thể ở OLS - <span class="en">LR test for overall significance — the OLS overall F-test equivalent</span>

So sánh mô hình null (7.2) và full (7.3) bằng likelihood-ratio test (`anova(OIM, oprobit)`):
<br><span class="en">Comparing the null model (7.2) and the full model (7.3) with a likelihood-ratio test (`anova(OIM, oprobit)`):</span>

$$LR = 2(LL_{full}-LL_{null}) \sim \chi^2_{q}$$

| Model | Resid. df | Resid. Dev |
|---|---|---|
| Null | 939 | 2834.382 |
| Full | 932 | 1446.688 |

$q=939-932=7$ (đúng bằng số biến thêm vào), LR stat = 1387.694, $p\approx0$ (< 2.2e-16) → **bác bỏ mạnh** $H_0$: toàn bộ 7 hệ số góc = 0. Đây là **phiên bản Maximum-Likelihood của F-test tổng thể** ở [[concepts/linear-regression-model]] mục 8.5 — cùng logic "so sánh restricted vs. unrestricted", chỉ thay $RSS$ bằng deviance/log-likelihood. **Cùng bài học diễn giải áp dụng**: LR test có ý nghĩa chỉ nói "không phải tất cả hệ số đều bằng 0" — không nói mô hình đã đặc tả đúng, không kiểm tra được biến bị bỏ sót.
<br><span class="en">$q=939-932=7$ (exactly the number of added variables), LR stat = 1387.694, $p\approx0$ (< 2.2e-16) → **strongly reject** $H_0$: all 7 slope coefficients = 0. This is the **Maximum-Likelihood version of the overall F-test** in [[concepts/linear-regression-model]] section 8.5 — the same "compare restricted vs. unrestricted" logic, only $RSS$ is replaced by deviance/log-likelihood. **The same interpretation lesson applies**: a significant LR test only says "not all coefficients are zero" — it does not say the model is correctly specified, and it cannot detect omitted variables.</span>

### 7.5 Xác suất dự đoán (fitted values) - <span class="en">Predicted probabilities (fitted values)</span>

Với quan sát đầu tiên trong mẫu, mô hình cho ra 5 xác suất (cộng lại đúng bằng 1):
<br><span class="en">For the first observation in the sample, the model produces 5 probabilities (summing exactly to 1):</span>

$Pr(No)\approx0.0000115$, $Pr(1\text{–}2)\approx0.0010$, $Pr(3\text{–}5)\approx0.0829$, $Pr(5\text{–}10)\approx0.8385$, $Pr(11+)\approx0.0776$ — cá nhân này gần như chắc chắn thuộc nhóm "5–10 lần/tháng" (xác suất 83.85%).
<br><span class="en">$Pr(No)\approx0.0000115$, $Pr(1\text{–}2)\approx0.0010$, $Pr(3\text{–}5)\approx0.0829$, $Pr(5\text{–}10)\approx0.8385$, $Pr(11+)\approx0.0776$ — this individual almost certainly belongs to the "5–10 times/month" group (83.85% probability).</span>

**Đồ thị $Pr(y=4)$ (ăn ngoài ≥11 lần/tháng) theo tuổi**: slide vẽ `Pr(11+)` dự đoán theo `age` và cho thấy quan hệ **giảm dần rõ rệt** — xác suất gần 1.0 ở tuổi ~18, giảm mạnh qua tuổi 20 (~0.85), tiếp tục giảm và gần như bằng 0 từ khoảng tuổi 30 trở đi. Đây là minh họa trực quan cho dấu **âm** của $\beta_{age}=-0.29$: tuổi càng cao, khuynh hướng ăn ngoài tần suất cao càng giảm.
<br><span class="en">**Plot of $Pr(y=4)$ (eating out ≥11 times/month) against age**: the slide plots predicted `Pr(11+)` against `age` and shows a clearly **decreasing** relationship — probability near 1.0 at age ~18, dropping sharply past age 20 (~0.85), continuing to fall and reaching near 0 from around age 30 onward. This is a visual illustration of the **negative** sign of $\beta_{age}=-0.29$: the older a person is, the lower their propensity toward high-frequency eating out.</span>

### 7.6 Dự báo (prediction) và ma trận nhầm lẫn - <span class="en">Prediction and the confusion matrix</span>

`predict(oprobit)` gán mỗi quan sát vào phạm trù có xác suất dự đoán cao nhất. Ma trận đối chiếu thực tế (hàng) và dự đoán (cột):
<br><span class="en">`predict(oprobit)` assigns each observation to the category with the highest predicted probability. The matrix cross-tabulating actual (rows) against predicted (columns):</span>

| Thực tế \ Dự đoán - <span class="en">Actual \ Predicted</span> | No | 1-2/mo | 3-5/mo | 5-10/mo | 11+ |
|---|---|---|---|---|---|
| **No** | 236 | 29 | 10 | 2 | 0 |
| **1-2/month** | 53 | 52 | 51 | 4 | 0 |
| **3-5/month** | 15 | 29 | 154 | 37 | 0 |
| **5-10/month** | 1 | 3 | 51 | 155 | 11 |
| **11 or more** | 0 | 0 | 0 | 21 | 29 |

Tỷ lệ dự đoán đúng tổng thể (`sum(diag(tab))/sum(tab)`): **0.6638** (66.4%). Nhưng con số tổng thể này **che giấu chênh lệch lớn giữa các phạm trù**: nhóm "No" (236/277≈85%) và "5-10/month" (155/221≈70%) được dự đoán khá tốt, trong khi nhóm "1-2/month" chỉ đúng 52/160≈32.5% — mô hình thường xuyên nhầm nhóm này với "No" (53 trường hợp) hoặc "3-5/month" (51 trường hợp) — hai nhóm lân cận trên trục $y^*$. Đây là lý do **không nên chỉ báo cáo tỷ lệ đúng tổng thể** mà cần trình bày cả ma trận nhầm lẫn đầy đủ.
<br><span class="en">Overall correct-prediction rate (`sum(diag(tab))/sum(tab)`): **0.6638** (66.4%). But this overall figure **hides large differences across categories**: the "No" group (236/277≈85%) and "5-10/month" (155/221≈70%) are predicted fairly well, while the "1-2/month" group is only correct 52/160≈32.5% of the time — the model frequently confuses this group with "No" (53 cases) or "3-5/month" (51 cases) — its two neighbors on the $y^*$ axis. This is why **the overall accuracy rate alone should not be the only thing reported** — the full confusion matrix should be presented too.</span>

### 7.7 Dự đoán cho một cá nhân cụ thể - <span class="en">Prediction for a specific individual</span>

Slide minh họa dự đoán cho hai hồ sơ giả định, giống hệt nhau ngoại trừ tình trạng quan hệ:
<br><span class="en">The slide illustrates prediction for two hypothetical profiles, identical except for relationship status:</span>

- `person1`: age=23, whours=60, income=30, homeown=0, gender=0, `inrelationship=0`, married=0 → dự đoán: **"5-10/month"**.
  <br><span class="en">`person1`: age=23, whours=60, income=30, homeown=0, gender=0, `inrelationship=0`, married=0 → predicted: **"5-10/month"**.</span>
- `person2`: giống hệt person1 nhưng `inrelationship=1` → dự đoán: **"11 or more"**.
  <br><span class="en">`person2`: identical to person1 but `inrelationship=1` → predicted: **"11 or more"**.</span>

Chỉ thay đổi **một** biến dummy (`inrelationship`: 0→1) đã đủ đẩy phạm trù dự đoán lên hẳn một bậc — nhất quán với hệ số $\beta_{inrelationship}=2.97$ rất lớn và có ý nghĩa mạnh (mục 7.3): có người yêu/bạn đời làm tăng đáng kể khuynh hướng ăn ngoài $y^*$, đủ để vượt qua cutpoint $u_4=-3.776$ và rơi vào nhóm cao nhất.
<br><span class="en">Changing just **one** dummy variable (`inrelationship`: 0→1) is enough to push the predicted category up a full level — consistent with the large, strongly significant coefficient $\beta_{inrelationship}=2.97$ (section 7.3): having a partner substantially raises the eating-out propensity $y^*$, enough to cross the cutpoint $u_4=-3.776$ and fall into the highest group.</span>

### 7.8 Pseudo R² (hiếm khi dùng) - <span class="en">Pseudo R² (rarely used)</span>

`PseudoR2(oprobit, which=c("CoxSnell","Nagelkerke","McFadden"))`: CoxSnell = 0.770, Nagelkerke = 0.811, McFadden = 0.490. Slide ghi chú rõ tiêu đề trang này: **"(RARELY USED)"** — các pseudo-R² này không có thang đo và cách diễn giải tương đương $R^2$ tuyến tính ở [[concepts/linear-regression-model]] mục 9, và không nên dùng làm tiêu chí chính để đánh giá độ phù hợp mô hình.
<br><span class="en">`PseudoR2(oprobit, which=c("CoxSnell","Nagelkerke","McFadden"))`: CoxSnell = 0.770, Nagelkerke = 0.811, McFadden = 0.490. The slide explicitly notes this page's title: **"(RARELY USED)"** — these pseudo-R² measures do not have the same scale or interpretation as the linear $R^2$ in [[concepts/linear-regression-model]] section 9, and should not be used as the primary criterion for evaluating model fit.</span>

### 7.9 Kiểm định ý nghĩa đồng thời của một nhóm hệ số - <span class="en">Testing the joint significance of a group of coefficients</span>

Câu hỏi: `inrelationship` và `married` có ý nghĩa **đồng thời** hay không? (`lmtest::lrtest(oprobit, c("inrelationship","married"))`) — so sánh mô hình đầy đủ với mô hình bỏ hai biến này:
<br><span class="en">Question: are `inrelationship` and `married` **jointly** significant? (`lmtest::lrtest(oprobit, c("inrelationship","married"))`) — comparing the full model with a model that drops these two variables:</span>

| Model | #Df | LogLik |
|---|---|---|
| Full (có `inrelationship`, `married`) | 11 | −723.34 |
| Restricted (bỏ hai biến) | 9 | −1095.00 |

Chisq = 743.32, df=2, $p<2.2\times10^{-16}$ → bác bỏ mạnh $H_0$: cả hai hệ số cùng bằng 0. Đây là phiên bản ML của **F-test cho một nhóm hệ số** ở [[concepts/linear-regression-model]] mục 8 (VD kiểm định `chighland`/`ccoastal` đồng thời) — cùng logic "ép hệ số về 0 (restricted) rồi so với mô hình đầy đủ (unrestricted)", chỉ thay thống kê $F$ dựa trên $RSS$ bằng thống kê $\chi^2$ dựa trên log-likelihood.
<br><span class="en">Chisq = 743.32, df=2, $p<2.2\times10^{-16}$ → strongly reject $H_0$: both coefficients are jointly zero. This is the ML version of the **F-test for a group of coefficients** in [[concepts/linear-regression-model]] section 8 (e.g. jointly testing `chighland`/`ccoastal`) — the same "force the coefficients to 0 (restricted) then compare against the full model (unrestricted)" logic, only the $F$ statistic based on $RSS$ is replaced by a $\chi^2$ statistic based on log-likelihood.</span>

## 8. Diễn giải hệ số và marginal effects - <span class="en">Interpreting coefficients and marginal effects</span>

### 8.1 Vì sao không thể đọc trực tiếp $\beta$ - <span class="en">Why $\beta$ cannot be read directly</span>

**Hệ số ước lượng $\beta$ là marginal effect lên biến tiềm ẩn $y^*$, không phải lên bất kỳ xác suất $Pr(y=k)$ nào.** Nhà nghiên cứu hầu như không bao giờ quan tâm trực tiếp đến $\beta$ (vì $y^*$ không quan sát được, không có đơn vị đo cụ thể) — điều thực sự cần biết là: khi $X$ tăng, **xác suất rơi vào từng phạm trù cụ thể** thay đổi bao nhiêu.
<br><span class="en">**The estimated coefficient $\beta$ is the marginal effect on the latent variable $y^*$, not on any probability $Pr(y=k)$.** Researchers almost never care directly about $\beta$ (since $y^*$ is unobserved, with no concrete measurement unit) — what actually matters is: as $X$ increases, how much does **the probability of falling into each specific category** change.</span>

### 8.2 Công thức marginal effect - <span class="en">Marginal effect formula</span>

Với $Pr(y=0)=\Phi(u_1-X\beta)$:
<br><span class="en">With $Pr(y=0)=\Phi(u_1-X\beta)$:</span>

$$\frac{\partial Pr(y=0)}{\partial X_k}=-\beta_k\,\phi(u_1-X\beta)$$

($\phi$ là hàm mật độ xác suất — pdf — của phân phối chuẩn). Mỗi phạm trù $k$ có công thức marginal effect **riêng** (đạo hàm của hiệu hai $\Phi$ đối với phạm trù giữa), và vì $\phi(\cdot)>0$ luôn dương, **dấu của marginal effect lên $Pr(y=0)$ ngược dấu với $\beta_k$** — đây là điểm mấu chốt để hiểu vì sao dấu marginal effect có thể "lật" giữa các phạm trù.
<br><span class="en">($\phi$ is the probability density function — pdf — of the normal distribution). Each category $k$ has its **own** marginal-effect formula (the derivative of the difference of two $\Phi$'s for middle categories), and since $\phi(\cdot)>0$ is always positive, **the sign of the marginal effect on $Pr(y=0)$ is opposite to the sign of $\beta_k$** — this is the key point for understanding why the sign of the marginal effect can "flip" across categories.</span>

### 8.3 Ví dụ số — bảng marginal effects đầy đủ (`ocME`, `library(erer)`) - <span class="en">Numerical example — full marginal-effects table</span>

| Biến - <span class="en">Variable</span> | ME trên Pr(No) - <span class="en">ME on Pr(No)</span> | ME trên Pr(1-2) - <span class="en">ME on Pr(1-2)</span> | ME trên Pr(3-5) - <span class="en">ME on Pr(3-5)</span> | ME trên Pr(5-10) - <span class="en">ME on Pr(5-10)</span> | ME trên Pr(11+) - <span class="en">ME on Pr(11+)</span> |
|---|---|---|---|---|---|
| `age` | +0.044 | +0.069 | −0.072 | −0.040 | 0.000 |
| `whours` | −0.001 | −0.001 | +0.001 | +0.001 | 0.000 |
| `income` | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| `homeown` | +0.689 | +0.152 | −0.528 | −0.312 | −0.001 |
| `gender` | +0.011 | +0.018 | −0.019 | −0.011 | 0.000 |
| `inrelationship` | −0.369 | −0.408 | +0.108 | +0.659 | +0.009 |
| `married` | −0.029 | −0.049 | +0.048 | +0.030 | 0.000 |

**Ba quan sát quan trọng, minh họa trực tiếp bằng số:**
<br><span class="en">**Three important observations, illustrated directly with the numbers:**</span>

1. **Tổng marginal effect trên một hàng luôn xấp xỉ 0** (VD `age`: $0.044+0.069-0.072-0.040+0.000\approx0.001\approx0$, sai lệch nhỏ do làm tròn 3 chữ số thập phân). Đây là hệ quả logic tất yếu: tổng xác suất luôn bằng 1, nên khi $X$ thay đổi, xác suất chỉ **dịch chuyển/phân bố lại** (redistribute) giữa các phạm trù, không thể "tạo ra" xác suất mới — tổng đạo hàm phải bằng 0.
   <br><span class="en">**The sum of marginal effects across one row always approximates 0** (e.g. `age`: $0.044+0.069-0.072-0.040+0.000\approx0.001\approx0$, the small deviation from rounding to 3 decimal places). This is a necessary logical consequence: total probability always equals 1, so when $X$ changes, probability can only **shift/redistribute** among categories, never "create" new probability — the sum of the derivatives must equal 0.</span>

2. **Dấu marginal effect ở hai đầu (phạm trù thấp nhất/cao nhất) thường ngược nhau, và ngược với dấu ở giữa cũng có thể xảy ra**. VD `age` có $\beta_{age}=-0.29$ (âm — tuổi cao hơn → $y^*$ thấp hơn, tức khuynh hướng ăn ngoài giảm), nhưng marginal effect trên $Pr(No)$ lại **dương** (+0.044: tuổi cao hơn → xác suất "không ăn ngoài" tăng — hợp lý, đúng chiều) trong khi marginal effect trên $Pr(3\text{-}5)$ và $Pr(5\text{-}10)$ lại **âm** (tuổi cao hơn → xác suất rơi vào các mức trung-cao giảm). Đây chính xác là ví dụ số cho quy tắc trực giác: $\beta$ âm không có nghĩa "làm giảm mọi xác suất" — nó có nghĩa **"đẩy phân phối xác suất về phía các phạm trù thấp hơn"**, nên xác suất ở đầu thấp tăng còn xác suất ở đầu cao giảm.
   <br><span class="en">**The sign of the marginal effect at the two ends (lowest/highest category) is usually opposite, and the sign at the middle can also differ**. For example `age` has $\beta_{age}=-0.29$ (negative — higher age → lower $y^*$, i.e. lower eating-out propensity), but the marginal effect on $Pr(No)$ is **positive** (+0.044: higher age → higher probability of "not eating out" — sensible, correct direction), while the marginal effect on $Pr(3\text{-}5)$ and $Pr(5\text{-}10)$ is **negative** (higher age → lower probability of falling into the mid-high levels). This is exactly the numerical example of the intuitive rule: a negative $\beta$ does not mean "decreases every probability" — it means **"pushes the probability distribution toward the lower categories,"** so probability at the low end rises while probability at the high end falls.</span>

3. **`homeown`** ($\beta=-2.88$, âm mạnh): marginal effect trên $Pr(No)$ là **+0.689** — cực lớn, chủ nhà có xác suất "không ăn ngoài" cao hơn hẳn 68.9 điểm phần trăm so với người không sở hữu nhà (giữ các yếu tố khác không đổi), trong khi marginal effect trên $Pr(3\text{-}5)$ là −0.528 và $Pr(5\text{-}10)$ là −0.312 — tất cả nhất quán với dấu âm của $\beta$: chủ nhà có khuynh hướng ăn ngoài thấp hơn, nên xác suất dồn về phía các mức thấp.
   <br><span class="en">**`homeown`** ($\beta=-2.88$, strongly negative): the marginal effect on $Pr(No)$ is **+0.689** — extremely large; homeowners have a "not eating out" probability that is 68.9 percentage points higher than non-homeowners (holding other factors constant), while the marginal effect on $Pr(3\text{-}5)$ is −0.528 and on $Pr(5\text{-}10)$ is −0.312 — all consistent with the negative sign of $\beta$: homeowners have a lower eating-out propensity, so probability piles up toward the lower levels.</span>

### 8.4 Suy luận thống kê trên marginal effects (không chỉ trên $\beta$) - <span class="en">Statistical inference on marginal effects (not just on $\beta$)</span>

Mỗi marginal effect cũng có SE, t-value, p-value riêng — có thể kiểm định ý nghĩa thống kê **trực tiếp trên marginal effect**, không chỉ trên $\beta$. Ví dụ marginal effect trên $Pr(No)$ (`$ME.0`): `age` = 0.044 (SE=0.004, t=10.62, p<0.001); `homeown` = 0.689 (SE=0.032, t=21.28, p<0.001); `inrelationship` = −0.369 (SE=0.027, t=−13.70, p<0.001) — cả ba đều có ý nghĩa thống kê rất mạnh, khớp với ý nghĩa của $\beta$ tương ứng. Nhưng lưu ý: **ý nghĩa thống kê của $\beta$ không tự động đảm bảo ý nghĩa thống kê của marginal effect ở mọi phạm trù** — vì công thức marginal effect còn phụ thuộc vào $\phi(\cdot)$ (khác nhau ở từng phạm trù, từng giá trị $X$), nên về nguyên tắc SE của marginal effect và của $\beta$ không nhất thiết dẫn đến cùng kết luận kiểm định — dù trong ví dụ cụ thể này chúng khớp nhau.
<br><span class="en">Each marginal effect also has its own SE, t-value, p-value — statistical significance can be tested **directly on the marginal effect**, not only on $\beta$. For example, the marginal effect on $Pr(No)$ (`$ME.0`): `age` = 0.044 (SE=0.004, t=10.62, p<0.001); `homeown` = 0.689 (SE=0.032, t=21.28, p<0.001); `inrelationship` = −0.369 (SE=0.027, t=−13.70, p<0.001) — all three are very strongly significant, matching the significance of their corresponding $\beta$. But note: **statistical significance of $\beta$ does not automatically guarantee statistical significance of the marginal effect in every category** — because the marginal-effect formula also depends on $\phi(\cdot)$ (which differs across categories and $X$ values), so in principle the SE of the marginal effect and of $\beta$ need not lead to the same test conclusion — even though in this specific example they do match.</span>

## 9. Ordered Logit — ví dụ số và so sánh với Ordered Probit - <span class="en">Ordered Logit — numerical example and comparison with Ordered Probit</span>

Chạy lại đúng phương trình ở mục 7.3 với `method="logistic"` thay vì `"probit"`:
<br><span class="en">Re-running the exact same equation from section 7.3 with `method="logistic"` instead of `"probit"`:</span>

| Biến - <span class="en">Variable</span> | $\beta$ (Logit) | $\beta$ (Probit, mục 7.3) - <span class="en">$\beta$ (Probit, section 7.3)</span> | Tỷ lệ Logit/Probit - <span class="en">Logit/Probit ratio</span> |
|---|---|---|---|
| `age` | −0.5248 | −0.2900 | 1.81 |
| `whours` | 0.0076 | 0.0045 | 1.71 |
| `income` | −0.0016 | −0.0009 | 1.72 |
| `homeown` | −5.2108 | −2.8831 | 1.81 |
| `gender` | −0.1287 | −0.0760 | 1.69 |
| `inrelationship` | 5.3464 | 2.9727 | 1.80 |
| `married` | 0.3489 | 0.2040 | 1.71 |

**Cutpoints (Logit)**: $0|1=-17.10$, $1|2=-15.04$, $2|3=-11.95$, $3|4=-6.88$ (tất cả tăng dần, có ý nghĩa thống kê mạnh).
<br><span class="en">**Cutpoints (Logit)**: $0|1=-17.10$, $1|2=-15.04$, $2|3=-11.95$, $3|4=-6.88$ (all increasing, strongly statistically significant).</span>

> **Quan sát thêm** (tính toán từ hai bảng hệ số trên, không phải một phát biểu trực tiếp của slide): tỷ lệ hệ số Logit/Probit dao động khá đều quanh **1.7–1.8** cho mọi biến. Đây khớp với một quy tắc kinh nghiệm quen thuộc trong kinh tế lượng — phân phối logistic có phương sai $\pi^2/3\approx3.29$ trong khi phân phối chuẩn hóa có phương sai 1, nên hệ số logit thường lớn hơn hệ số probit tương ứng khoảng $\sqrt{\pi^2/3}\approx1.81$ lần. Không nên dùng con số này để so sánh **độ lớn tác động** giữa hai mô hình một cách trực tiếp (như đã lưu ý ở [[concepts/binary-response-models]]) — chỉ hữu ích như một cách kiểm tra nhanh xem hai mô hình có cho ra kết quả "nhất quán" hay không (cùng dấu, tỷ lệ hệ số gần hằng số).
> <br><span class="en">**Additional observation** (computed from the two coefficient tables above, not a direct statement from the slide): the Logit/Probit coefficient ratio hovers fairly evenly around **1.7–1.8** for every variable. This matches a familiar rule of thumb in econometrics — the logistic distribution has variance $\pi^2/3\approx3.29$ while the standard normal has variance 1, so logit coefficients are typically about $\sqrt{\pi^2/3}\approx1.81$ times larger than their probit counterparts. This number should not be used to directly compare the **magnitude of effects** between the two models (as already noted in [[concepts/binary-response-models]]) — it is only useful as a quick check of whether the two models give "consistent" results (same signs, roughly constant coefficient ratio).</span>

Dấu và mức ý nghĩa thống kê của mọi hệ số **giống hệt** giữa hai mô hình (cùng biến có ý nghĩa, cùng biến không có ý nghĩa) — một dấu hiệu tốt cho thấy kết luận không nhạy cảm với lựa chọn Logit hay Probit ở ví dụ này.
<br><span class="en">The sign and statistical significance level of every coefficient are **identical** between the two models (the same variables significant, the same variables not) — a good sign that the conclusions are not sensitive to the choice of Logit or Probit in this example.</span>

## 10. Parallel regression assumption (proportional odds assumption) và Brant test - <span class="en">Parallel regression assumption (proportional odds assumption) and the Brant test</span>

### 10.1 Giả định này là gì, hiểu trực quan - <span class="en">What this assumption is, an intuitive understanding</span>

Ordered Logit/Probit giả định **cùng một bộ hệ số $\beta$ cho mọi ngưỡng phân loại (cutpoint)** — gọi là **parallel regression assumption** (đôi khi còn gọi **proportional odds assumption**, đặc biệt trong ngữ cảnh ordered logit). Nhắc lại công thức mục 4: mỗi $Pr(y=j)$ dùng **cùng** $\beta X$ (chỉ khác cutpoint $u_j$ trừ đi). Nói cách khác, mô hình giả định rằng tác động của mỗi biến $X_k$ lên "khuynh hướng dịch chuyển lên một mức" là **như nhau, bất kể đang ở ranh giới nào** — ranh giới giữa "No" và "1-2/tháng" chịu tác động của `age` giống hệt về độ lớn như ranh giới giữa "5-10" và "11+".
<br><span class="en">Ordered Logit/Probit assumes **the same coefficient set $\beta$ for every category threshold (cutpoint)** — called the **parallel regression assumption** (sometimes also called the **proportional odds assumption**, especially in the ordered logit context). Recall the formula from section 4: each $Pr(y=j)$ uses **the same** $\beta X$ (only the cutpoint $u_j$ subtracted differs). In other words, the model assumes the effect of each variable $X_k$ on "the propensity to move up one level" is **the same, regardless of which boundary is being crossed** — the boundary between "No" and "1-2/month" is affected by `age` in exactly the same magnitude as the boundary between "5-10" and "11+".</span>

**Tên gọi "parallel"** xuất phát từ cách hình dung sau: nếu vẽ mỗi ranh giới $j$ như một "đường hồi quy" riêng theo $X$ (dạng $u_j - X\beta$), $J-1$ đường này chỉ khác nhau ở **hệ số chặn** (cutpoint $u_j$) nhưng có **cùng độ dốc** $\beta$ với mọi $X$ — tức chúng **song song** với nhau. Nếu giả định này sai — tức mỗi ranh giới thực ra chịu tác động khác nhau của $X$ — buộc dùng chung một $\beta$ sẽ làm ước lượng bị **chệch (biased)**, vì mô hình đang ép một cấu trúc không đúng với dữ liệu thực.
<br><span class="en">**The name "parallel"** comes from the following picture: if each boundary $j$ is drawn as its own "regression line" against $X$ (of the form $u_j - X\beta$), these $J-1$ lines differ only in their **intercept** (cutpoint $u_j$) but share the **same slope** $\beta$ for every $X$ — i.e. they are **parallel** to one another. If this assumption is false — i.e. each boundary is actually affected differently by $X$ — forcing a shared $\beta$ will make the estimates **biased**, because the model is imposing a structure that does not match the real data.</span>

### 10.2 Brant test - <span class="en">Brant test</span>

- $H_0$ (giả thuyết gốc) của Brant test: **parallel regression assumption được thỏa mãn** (tức $\beta$ thực sự giống nhau ở mọi ngưỡng).
  <br><span class="en">$H_0$ (null hypothesis) of the Brant test: **the parallel regression assumption holds** (i.e. $\beta$ is truly the same across every threshold).</span>
- Nếu **bác bỏ** $H_0$ → giả định bị vi phạm → nên cân nhắc mô hình khác — slide gợi ý **MNL** (không ràng buộc hệ số giống nhau giữa các ngưỡng — đổi lại, mất thông tin thứ tự — xem [[concepts/multinomial-logit-model]]). *(Slide không đề cập generalized ordered logit hay các mô hình khác — chỉ nêu MNL là lựa chọn thay thế; không mở rộng thêm vì không có trong nguồn.)*
  <br><span class="en">If $H_0$ is **rejected** → the assumption is violated → an alternative model should be considered — the slide suggests **MNL** (does not constrain the coefficients to be the same across thresholds — in exchange, it loses the ordering information — see [[concepts/multinomial-logit-model]]). *(The slide does not mention generalized ordered logit or other models — it only names MNL as the alternative; not expanded further since it's not in the source.)*</span>

**Ví dụ số** (`brant::brant(ologit)`, chạy trên mô hình Ordered Logit ở mục 9):
<br><span class="en">**Numerical example** (`brant::brant(ologit)`, run on the Ordered Logit model from section 9):</span>

| Test for | $\chi^2$ | df | p |
|---|---|---|---|
| Omnibus | 17.24 | 21 | 0.7 |
| age | 2.94 | 3 | 0.4 |
| whours | 5.98 | 3 | 0.1 |
| income | 1.28 | 3 | 0.7 |
| homeown | 1.18 | 3 | 0.7 |
| gender | 2.20 | 3 | 0.5 |
| inrelationship | 0.52 | 3 | 0.9 |
| married | 0.38 | 3 | 0.9 |

Mọi p-value (kể cả Omnibus, kiểm định tổng quát cho toàn bộ hệ số cùng lúc) đều **lớn hơn 0.05** → **không bác bỏ** $H_0$ → kết luận của slide: **"parallel regression assumption holds for all coefficients"** (giả định song song được thỏa mãn cho mọi hệ số) — ước lượng Ordered Logit ở ví dụ `eatout` này đáng tin cậy, không cần chuyển sang MNL.
<br><span class="en">Every p-value (including Omnibus, the overall test for all coefficients jointly) is **greater than 0.05** → **fail to reject** $H_0$ → the slide's conclusion: **"parallel regression assumption holds for all coefficients"** — the Ordered Logit estimates in this `eatout` example are reliable, no need to switch to MNL.</span>

## 11. Bẫy thi tổng hợp - <span class="en">Exam traps</span>

1. Diễn giải trực tiếp $\beta$ như tác động lên $Pr(y=k)$ — sai, $\beta$ là tác động lên **biến tiềm ẩn $y^*$**, phải tính marginal effect riêng cho từng xác suất (mục 8.2).
   <br><span class="en">Interpreting $\beta$ directly as the effect on $Pr(y=k)$ — wrong; $\beta$ is the effect on the **latent variable $y^*$**, the marginal effect must be computed separately for each probability (section 8.2).</span>
2. Kỳ vọng dấu marginal effect **giống nhau ở mọi phạm trù** cho cùng một biến — sai; ví dụ số `age` ở mục 8.3 cho thấy marginal effect có thể **dương** ở phạm trù thấp nhất và **âm** ở phạm trù giữa/cao, dù $\beta$ chỉ có một dấu duy nhất.
   <br><span class="en">Expecting the marginal effect's sign to be **the same across every category** for a given variable — wrong; the numerical example for `age` in section 8.3 shows the marginal effect can be **positive** at the lowest category and **negative** at the middle/higher categories, even though $\beta$ has only one sign.</span>
3. Quên rằng tổng marginal effect của một biến trên **tất cả** các phạm trù luôn xấp xỉ 0 (xác suất chỉ dịch chuyển giữa các mức, không "sinh thêm") — nếu tính tay mà tổng lệch xa 0, khả năng cao đã tính sai công thức.
   <br><span class="en">Forgetting that a variable's marginal effects summed across **all** categories always approximate 0 (probability only shifts between levels, it isn't "created") — if a hand calculation's total is far from 0, the formula was likely applied incorrectly.</span>
4. Coi "Intercepts" trong output R (`polr`) là hệ số chặn kiểu OLS — sai, đó là **cutpoints/threshold parameters**; và giá trị của chúng **không cố định** — nó thay đổi mạnh tùy mô hình có bao nhiêu biến $X$ và thang đo của $X$ ra sao (so sánh cutpoints mô hình null vs. full ở mục 7.2 và 7.3, dù cùng một biến phụ thuộc).
   <br><span class="en">Treating "Intercepts" in R's output (`polr`) as OLS-style intercepts — wrong, they are **cutpoints/threshold parameters**; and their values are **not fixed** — they shift substantially depending on how many $X$ variables the model has and their scale (compare the null-model vs. full-model cutpoints in sections 7.2 and 7.3, despite sharing the same dependent variable).</span>
5. Bỏ qua Brant test khi báo cáo Ordered Logit/Probit — nếu không kiểm định, không biết parallel regression assumption có giữ hay không; nếu vi phạm mà vẫn dùng ordered model, hệ số ước lượng bị chệch (biased).
   <br><span class="en">Skipping the Brant test when reporting Ordered Logit/Probit — without testing it, there's no way to know whether the parallel regression assumption holds; if it's violated and an ordered model is still used, the estimated coefficients are biased.</span>
6. Hiểu sai chiều $H_0$ của Brant test: $H_0$ = **giả định được thỏa mãn** (holds), không phải "giả định bị vi phạm". Bác bỏ $H_0$ mới là dấu hiệu **vi phạm**; không bác bỏ nghĩa là giả định ổn (như ví dụ số mục 10.2, mọi p>0.05 → giả định giữ).
   <br><span class="en">Getting the direction of the Brant test's $H_0$ backwards: $H_0$ = **the assumption holds**, not "the assumption is violated". Rejecting $H_0$ is the sign of a **violation**; failing to reject means the assumption is fine (as in the numerical example in section 10.2, where every p>0.05 → the assumption holds).</span>
7. Nhầm lẫn Ordinal response (có thứ tự, dùng Ordered Logit/Probit) với Multinomial response (không thứ tự, dùng MNL) — xem [[concepts/multinomial-logit-model]]; hoặc dùng OLS trực tiếp lên mã số của biến ordinal, ngầm giả định khoảng cách giữa các mức bằng nhau (mục 1.2).
   <br><span class="en">Confusing an Ordinal response (ordered, uses Ordered Logit/Probit) with a Multinomial response (unordered, uses MNL) — see [[concepts/multinomial-logit-model]]; or running OLS directly on the ordinal variable's numeric codes, implicitly assuming the distance between levels is equal (section 1.2).</span>
8. Dùng Pseudo R² (McFadden/CoxSnell/Nagelkerke) như tiêu chí đánh giá độ phù hợp chính của mô hình — slide ghi rõ các chỉ số này **"rarely used"**, không có thang đo/diễn giải tương đương $R^2$ tuyến tính.
   <br><span class="en">Using Pseudo R² (McFadden/CoxSnell/Nagelkerke) as the main fit criterion for the model — the slide explicitly notes these measures are **"rarely used"**, and have no scale/interpretation equivalent to linear $R^2$.</span>
9. Chỉ báo cáo tỷ lệ dự đoán đúng tổng thể (VD 66.4% ở mục 7.6) mà không kiểm tra ma trận nhầm lẫn đầy đủ theo từng phạm trù — một mô hình có thể "trông tốt" ở mức tổng thể nhưng dự đoán rất kém ở một phạm trù cụ thể (VD "1-2/month" chỉ đúng ~32.5% trong ví dụ này).
   <br><span class="en">Reporting only the overall correct-prediction rate (e.g. 66.4% in section 7.6) without checking the full confusion matrix broken down by category — a model can "look good" overall while predicting a specific category very poorly (e.g. "1-2/month" is only correct ~32.5% of the time in this example).</span>
10. So sánh trực tiếp độ lớn hệ số Ordered Logit với Ordered Probit như thể chúng cùng thang đo — hai mô hình khác thang đo sai số (logistic vs. chuẩn); chỉ nên so sánh dấu, mức ý nghĩa, hoặc xác suất dự đoán, không so sánh độ lớn hệ số trực tiếp (dù tỷ lệ ~1.8 lần ở mục 9 là một quy tắc kinh nghiệm hữu ích để kiểm tra tính nhất quán).
    <br><span class="en">Directly comparing Ordered Logit and Ordered Probit coefficient magnitudes as if they shared the same scale — the two models have different error-term scales (logistic vs. normal); only compare sign, significance level, or predicted probabilities, not raw coefficient magnitude directly (though the ~1.8× ratio in section 9 is a useful rule of thumb for checking consistency).</span>

## 12. Kết nối với phần còn lại của khóa học - <span class="en">Connections to the rest of the course</span>

Ordinal response models đứng giữa hai mô hình discrete-choice khác trong Part 2 của khóa học, cùng chia sẻ khung log-likelihood/Maximum Likelihood:
<br><span class="en">Ordinal response models sit between two other discrete-choice models in Part 2 of the course, all sharing the log-likelihood/Maximum Likelihood framework:</span>

- **[[concepts/binary-response-models]]** (Topic 7): trường hợp đặc biệt $J=2$ — chỉ cần 1 cutpoint, và về mặt thực hành cutpoint đó thường được cố định (thường bằng 0) để ước lượng một intercept $\beta_0$ thông thường thay vào — đây là lý do binary Logit/Probit "trông" có intercept như OLS trong khi ordinal model thì không (mục 3). Khung LR test, Wald test, phân biệt Logit/Probit theo giả định phân phối sai số đều được ordinal model kế thừa nguyên vẹn.
  <br><span class="en">**[[concepts/binary-response-models]]** (Topic 7): the special case $J=2$ — only 1 cutpoint is needed, and in practice that cutpoint is usually fixed (typically at 0) so an ordinary intercept $\beta_0$ can be estimated instead — this is why binary Logit/Probit "look like" they have an OLS-style intercept while the ordinal model doesn't (section 3). The LR test framework, the Wald test, and the Logit/Probit distinction by error-distribution assumption are all inherited unchanged by the ordinal model.</span>
- **[[concepts/multinomial-logit-model]]** (Topic 8): áp dụng khi các phạm trù **không có thứ tự** — là lựa chọn thay thế khi Brant test bác bỏ parallel regression assumption (mục 10.2). MNL ước lượng riêng một bộ hệ số cho mỗi phạm trù so với phạm trù nền, "tốn" tham số hơn nhưng không bị ràng buộc "song song" như ordinal model.
  <br><span class="en">**[[concepts/multinomial-logit-model]]** (Topic 8): applies when the categories are **unordered** — it is the fallback when the Brant test rejects the parallel regression assumption (section 10.2). MNL estimates a separate coefficient set for each category relative to the base category, "spending" more parameters but without the "parallel" constraint the ordinal model imposes.</span>
- Khung log-likelihood $LL=\sum_i\sum_k Y_{ik}\ln Pr(y_i=k)$ (mục 5) là **mẫu số chung** của cả ba mô hình (binary, ordinal, MNL) — điểm khác biệt duy nhất giữa chúng là công thức tính $Pr(y_i=k)$.
  <br><span class="en">The log-likelihood framework $LL=\sum_i\sum_k Y_{ik}\ln Pr(y_i=k)$ (section 5) is the **common denominator** of all three models (binary, ordinal, MNL) — the only difference between them is the formula used to compute $Pr(y_i=k)$.</span>

Câu hỏi triết lý "tại sao cần Maximum Likelihood thay vì OLS khi biến phụ thuộc rời rạc" được đặt nền tảng ở [[concepts/binary-response-models]] — nên đọc trang đó trước nếu cần ôn lại từ đầu trước khi đi vào các biến thể phức tạp hơn (ordinal, MNL, và các mô hình đếm ở Topic 10).
<br><span class="en">The foundational question "why is Maximum Likelihood needed instead of OLS when the dependent variable is discrete" is laid out in [[concepts/binary-response-models]] — worth reading that page first if you need to review from scratch before moving on to the more complex variants (ordinal, MNL, and the count models in Topic 10).</span>

## 11. Tài liệu tham khảo ứng dụng thực tế - <span class="en">Real-world application references</span>

Ba bài báo gần đây minh họa ordered logit/probit models trong nghiên cứu kinh tế thực tế (đề cương Lecture 11):
<br><span class="en">Three recent papers illustrating ordered logit/probit models in real-world economic research (Lecture 11 syllabus):</span>

- Kolog, J. D., Asem, F. E., & Mensah-Bonsu, A. (2023). The state of food security and its determinants in Ghana: an ordered probit analysis of the household hunger scale and household food insecurity access scale. *Scientific African*, 19, e01579. https://doi.org/10.1016/j.sciaf.2023.e01579
- Chen, F., Yu, D., & Sun, Z. (2023). Investigating the associations of consumer financial knowledge and financial behaviors of credit card use. *Heliyon*, 9(1), E12713. https://doi.org/10.1016/j.heliyon.2022.e12713
- Ramachandran, R., Sudhir, S., & Unnithan, A. B. (2021). Exploring the relationship between emotionality and product star ratings in online reviews. *IIMB Management Review*, 33(4), 299-308. https://doi.org/10.1016/j.iimb.2021.12.002
