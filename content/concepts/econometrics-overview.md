---
title: "Econometrics: Overview, Causality and Identification"
type: concept
status: mature
tags: [foundations, causality, identification, research-design]
sources: ["[[sources/intro-to-econometrics]]", "[[sources/2026-course-outline]]"]
related: ["[[concepts/linear-regression-model]]", "[[concepts/binary-response-models]]", "[[concepts/fixed-random-effects-model]]", "[[concepts/endogeneity-iv-regression]]"]
updated: 2026-08-29
---

> **Cách đọc trang này**: đây là trang **triết lý nền** của toàn bộ khóa học — không có một công thức ước lượng cụ thể nào ở đây, chỉ có tư duy nền tảng mà mọi kỹ thuật sau này (OLS, IV, panel data, logit/probit...) đều phục vụ.
> <br><span class="en">**How to read this page**: this is the **foundational philosophy** page for the entire course — there is no specific estimation formula here, only the foundational thinking that every later technique (OLS, IV, panel data, logit/probit...) serves.</span>
> Nếu [[concepts/linear-regression-model]] trả lời câu hỏi "ước lượng bằng cách nào, tin cậy đến đâu", thì trang này trả lời câu hỏi đứng *trước* đó: "vì sao cần ước lượng, và vì sao ước lượng một con số không đồng nghĩa với việc đã hiểu đúng quan hệ nhân quả".
> <br><span class="en">If [[concepts/linear-regression-model]] answers the question "how do we estimate, how reliable is it", this page answers the question that comes *before* that: "why do we need to estimate at all, and why does estimating a number not mean we have correctly understood the causal relationship".</span>
> Nên đọc trang này trước, rồi mới đọc [[concepts/linear-regression-model]] để hiểu cơ chế kỹ thuật.
> <br><span class="en">Read this page first, then read [[concepts/linear-regression-model]] to understand the technical mechanics.</span>

## 1. Vì sao cần Econometrics? — xuất phát điểm là câu hỏi kinh tế - <span class="en">1. Why do we need Econometrics? — the starting point is an economic question</span>

Kinh tế học đưa ra rất nhiều lý thuyết về hành vi của cá nhân, doanh nghiệp, thị trường.
<br><span class="en">Economics puts forward many theories about the behavior of individuals, firms, and markets.</span>
Nhưng một lý thuyết, dù nghe hợp lý đến đâu, vẫn chỉ là một **giả thuyết** cho đến khi có bằng chứng từ dữ liệu thực.
<br><span class="en">But a theory, however reasonable it sounds, remains only a **hypothesis** until there is evidence from real data.</span>
Khóa học mở đầu bằng 4 câu hỏi thực nghiệm để minh họa việc này:
<br><span class="en">The course opens with 4 empirical questions to illustrate this:</span>

- Giáo dục có làm tăng lương không? (*Does education increase wages?*)
  <br><span class="en">Does education increase wages?</span>
- Đầu tư trực tiếp nước ngoài (FDI) có làm giảm bất bình đẳng không? (*Does foreign direct investment reduce inequality?*)
  <br><span class="en">Does foreign direct investment (FDI) reduce inequality?</span>
- Giá điện tăng có khiến hộ gia đình giảm tiêu thụ điện không? (*Do higher electricity prices reduce consumption?*)
  <br><span class="en">Do higher electricity prices cause households to reduce electricity consumption?</span>
- Thuế carbon tác động thế nào đến lượng khí thải? (*What is the impact of carbon taxes on emissions?*)
  <br><span class="en">What is the impact of carbon taxes on emissions?</span>

Điểm chung của cả 4 câu hỏi: chúng đều là câu hỏi **nhân quả** (causal), không phải câu hỏi mô tả đơn thuần.
<br><span class="en">What all 4 questions have in common: they are all **causal** questions, not merely descriptive ones.</span>
**Econometrics** được định nghĩa là:
<br><span class="en">**Econometrics** is defined as:</span>

> *"Econometrics is the discipline that uses statistical methods and data to quantify economic relationships and evaluate economic theories."*
> (Econometrics là ngành dùng phương pháp thống kê và dữ liệu để **định lượng** các quan hệ kinh tế và **kiểm định** các lý thuyết kinh tế.)
> <br><span class="en">Econometrics is the discipline that uses statistical methods and data to quantify economic relationships and evaluate economic theories.</span>

Cụ thể, econometrics cho phép nhà kinh tế học làm 4 việc:
<br><span class="en">Specifically, econometrics allows economists to do 4 things:</span>

1. **Ước lượng độ lớn** của các quan hệ kinh tế (VD: đi học thêm 1 năm làm lương tăng bao nhiêu %, không chỉ "có tăng hay không").
   <br><span class="en">**Estimate the magnitude** of economic relationships (e.g., by how many % wages rise for one more year of schooling, not just "does it rise or not").</span>
2. **Kiểm định lý thuyết kinh tế** bằng dữ liệu thực tế, thay vì chỉ suy luận lý thuyết suông.
   <br><span class="en">**Test economic theories** using real data, instead of relying on pure theoretical reasoning alone.</span>
3. **Đánh giá tác động của chính sách và can thiệp** (policy/interventions) — VD: tăng giá điện, áp thuế carbon.
   <br><span class="en">**Evaluate the impact of policies and interventions** — e.g., raising electricity prices, imposing carbon taxes.</span>
4. **Đưa ra dự báo** có cơ sở về các kết quả kinh tế trong tương lai.
   <br><span class="en">**Make well-founded forecasts** about future economic outcomes.</span>

## 2. Ba thành phần định nghĩa Econometrics - <span class="en">2. Three components that define Econometrics</span>

Định nghĩa econometrics luôn đi kèm ba thành phần bắt buộc phải có đủ cả ba — thiếu một, cái còn lại không còn là econometrics theo đúng nghĩa của khóa học:
<br><span class="en">The definition of econometrics always comes with three components, all three of which must be present — missing one, what remains is no longer econometrics in the sense the course means it:</span>

| Thành phần<br><span class="en">Component</span> | Vai trò<br><span class="en">Role</span> | Minh họa: ví dụ giáo dục → lương<br><span class="en">Illustration: the education → wage example</span> |
|---|---|---|
| **Economic theory** (lý thuyết kinh tế)<br><span class="en">**Economic theory**</span> | Đưa ra **giả thuyết** về việc các biến liên hệ với nhau như thế nào, và **tại sao**<br><span class="en">Puts forward a **hypothesis** about how the variables relate to each other, and **why**</span> | Lý thuyết vốn con người (human capital theory — VD Mincer 1974, đã nhắc ở [[concepts/linear-regression-model]]) cho rằng giáo dục làm tăng năng suất lao động, do đó làm tăng lương<br><span class="en">Human capital theory (e.g. Mincer 1974, already mentioned in [[concepts/linear-regression-model]]) holds that education increases labor productivity, thereby increasing wages</span> |
| **Mathematical model** (mô hình toán học)<br><span class="en">**Mathematical model**</span> | **Hình thức hóa** giả thuyết đó thành một phương trình cụ thể, có thể ước lượng được<br><span class="en">**Formalizes** that hypothesis into a specific, estimable equation</span> | $wage = \beta_0 + \beta_1 \cdot education + u$ |
| **Statistical methods** (phương pháp thống kê)<br><span class="en">**Statistical methods**</span> | **Ước lượng và kiểm định** phương trình đó bằng dữ liệu thực — cho ra con số cụ thể và độ tin cậy của con số đó<br><span class="en">**Estimates and tests** that equation using real data — producing a specific number and the reliability of that number</span> | Dùng OLS (xem [[concepts/linear-regression-model]]) trên một mẫu dữ liệu thật để ước lượng $\hat\beta_1$, rồi kiểm định xem hệ số này có ý nghĩa thống kê hay không<br><span class="en">Uses OLS (see [[concepts/linear-regression-model]]) on a real data sample to estimate $\hat\beta_1$, then tests whether this coefficient is statistically significant</span> |

**Điểm hay bị hiểu lầm của người mới học**: econometrics **không phải** là "lấy một tập dữ liệu rồi chạy hồi quy xem ra gì".
<br><span class="en">**A point beginners often misunderstand**: econometrics is **not** "taking a dataset and running a regression to see what comes out".</span>
Nếu thiếu bước (1) — không có economic theory làm nền — việc chọn biến nào đưa vào mô hình sẽ tùy tiện, và con số ước lượng ra có thể hoàn toàn vô nghĩa về mặt kinh tế dù thống kê "đẹp".
<br><span class="en">If step (1) is missing — no economic theory as a foundation — the choice of which variables to include in the model becomes arbitrary, and the resulting estimate can be completely meaningless economically even if the statistics look "clean".</span>
Trình tự đúng luôn là: có câu hỏi kinh tế → có lý thuyết giải thích → mới hình thức hóa thành mô hình → mới ước lượng.
<br><span class="en">The correct sequence is always: have an economic question → have a theory that explains it → only then formalize it into a model → only then estimate.</span>

## 3. Econometrics vs. Statistics — cùng công cụ, khác câu hỏi - <span class="en">3. Econometrics vs. Statistics — same tools, different questions</span>

Econometrics và statistics dùng chung rất nhiều công cụ toán/thống kê, nên dễ nhầm là "cùng một thứ".
<br><span class="en">Econometrics and statistics share many mathematical/statistical tools, so they are easily mistaken for "the same thing".</span>
Khác biệt nằm ở **mục tiêu**, không phải ở công thức:
<br><span class="en">The difference lies in the **objective**, not in the formulas:</span>

|  | Statistics | Econometrics |
|---|---|---|
| Trọng tâm<br><span class="en">Focus</span> | Mô tả pattern trong dữ liệu<br><span class="en">Describing patterns in data</span> | Cơ chế kinh tế (economic mechanisms)<br><span class="en">Economic mechanisms</span> |
| Mục tiêu<br><span class="en">Objective</span> | Prediction, statistical inference | Causal inference |
| Phạm vi<br><span class="en">Scope</span> | Áp dụng rộng, nhiều ngành<br><span class="en">Broadly applicable, across many fields</span> | Đánh giá lý thuyết & chính sách kinh tế<br><span class="en">Evaluating economic theory & policy</span> |

Khác biệt này được minh họa bằng đúng một tình huống, đặt dưới hai góc nhìn câu hỏi khác nhau (tiêu thụ điện của hộ gia đình):
<br><span class="en">This difference is illustrated using exactly one situation, framed under two different question angles (household electricity consumption):</span>

- **Statistical question**: "Can we predict household electricity consumption from income and household size?" — chỉ quan tâm **dự báo được hay không**, không quan tâm cơ chế.
  <br><span class="en">**Statistical question**: "Can we predict household electricity consumption from income and household size?" — concerned only with **whether it can be predicted**, not with the mechanism.</span>
- **Econometric question**: "Does a higher electricity price cause households to reduce electricity consumption?" — đòi hỏi phải trả lời được **causal**, tức "giá tăng" phải thực sự là *nguyên nhân*, không chỉ là một yếu tố dự báo tốt.
  <br><span class="en">**Econometric question**: "Does a higher electricity price cause households to reduce electricity consumption?" — requires a **causal** answer, meaning "the price increase" must actually be the *cause*, not merely a good predictor.</span>

Một mô hình dự báo tốt (statistics) hoàn toàn có thể dùng những biến không hề có quan hệ nhân quả với outcome (VD: dùng biến "tháng trong năm" để dự báo tiêu thụ điện — dự báo tốt nhưng không phải nguyên nhân).
<br><span class="en">A good predictive model (statistics) can perfectly well use variables that have no causal relationship with the outcome whatsoever (e.g., using a "month of the year" variable to predict electricity consumption — a good predictor but not a cause).</span>
Ngược lại, một câu hỏi econometric đòi hỏi khắt khe hơn nhiều.
<br><span class="en">In contrast, an econometric question demands much greater rigor.</span>
Đây chính là lý do quan trọng nhất: **nhiều phương pháp thống kê được econometrics vay mượn từ statistics, nhưng được điều chỉnh để giải quyết identification problem** (xem mục 7) — đây mới là ranh giới thực sự giữa hai ngành, không phải công cụ toán học.
<br><span class="en">This is the most important reason: **many statistical methods are borrowed by econometrics from statistics, but adapted to solve the identification problem** (see section 7) — this is the real boundary between the two disciplines, not the mathematical tools.</span>

## 4. Statistical Association là gì? - <span class="en">4. What is Statistical Association?</span>

**Association** (liên kết thống kê) nghĩa là khi một biến thay đổi, biến kia cũng thay đổi theo một cách có hệ thống — hai biến "đi cùng nhau" trong dữ liệu.
<br><span class="en">**Association** (statistical linkage) means that when one variable changes, the other also changes in a systematic way — the two variables "move together" in the data.</span>
Association được đo bằng các công cụ quen thuộc: **correlation** (hệ số tương quan), **regression coefficients** (hệ số hồi quy), **conditional averages** (trung bình có điều kiện).
<br><span class="en">Association is measured using familiar tools: **correlation**, **regression coefficients**, **conditional averages**.</span>

Ba ví dụ thuần túy association (chưa nói gì đến nguyên nhân):
<br><span class="en">Three purely-association examples (not yet saying anything about causation):</span>

- Hộ gia đình thu nhập cao hơn có xu hướng tiêu thụ điện nhiều hơn.
  <br><span class="en">Households with higher income tend to consume more electricity.</span>
- Thành phố có nhiều xe hơi hơn có xu hướng ô nhiễm không khí cao hơn.
  <br><span class="en">Cities with more cars tend to have higher air pollution.</span>
- Doanh số bán kem tăng khi số vụ tai nạn đuối nước tăng.
  <br><span class="en">Ice cream sales rise when the number of drowning accidents rises.</span>

Với mỗi ví dụ, câu hỏi đặt ra ngay sau đó là: **"Nếu hai biến có association, điều đó có nghĩa là biến này gây ra biến kia không?"** — và câu trả lời xuyên suốt khóa học là **không nhất thiết**.
<br><span class="en">For each example, the question immediately posed is: **"If two variables have an association, does that mean one causes the other?"** — and the answer running through the whole course is **not necessarily**.</span>

Một ví dụ khác làm rõ ranh giới giữa **association** và **causality** như hai khái niệm tách biệt:
<br><span class="en">Another example that clarifies the boundary between **association** and **causality** as two separate concepts:</span>

- **Association** (quan sát thuần túy): "Taller workers tend to earn higher wages" (người lao động cao hơn có xu hướng lương cao hơn) — chỉ là một pattern quan sát được, chưa nói gì về cơ chế.
  <br><span class="en">**Association** (pure observation): "Taller workers tend to earn higher wages" — just an observed pattern, saying nothing yet about the mechanism.</span>
- **Causality** (quan hệ nhân quả thật): "An increase in electricity price causes households to reduce electricity consumption" (giá điện tăng **khiến** hộ gia đình giảm tiêu thụ) — đây là phát biểu về **cơ chế**, mạnh hơn hẳn một pattern quan sát.
  <br><span class="en">**Causality** (a true causal relationship): "An increase in electricity price causes households to reduce electricity consumption" — this is a statement about **mechanism**, far stronger than an observed pattern.</span>

Câu hỏi trung tâm mà econometrics tồn tại để trả lời: ***"Does X merely move together with Y, or does X actually cause Y?"*** (X chỉ đi cùng Y, hay X thực sự gây ra Y?)
<br><span class="en">The central question econometrics exists to answer: ***"Does X merely move together with Y, or does X actually cause Y?"***</span>

## 5. Association ≠ Causality: Ba nguyên nhân gây nhầm lẫn - <span class="en">5. Association ≠ Causality: Three sources of confusion</span>

Ba lý do khiến một association quan sát được **không** chứng minh được causality:
<br><span class="en">Three reasons why an observed association **does not** prove causality:</span>

### 5.1 Confounding variables (biến gây nhiễu) - <span class="en">5.1 Confounding variables</span>

Một yếu tố thứ ba tác động lên **cả hai** biến đang quan sát, khiến chúng "đi cùng nhau" dù không biến nào gây ra biến kia.
<br><span class="en">A third factor affects **both** of the observed variables, causing them to "move together" even though neither variable causes the other.</span>

> *Ví dụ*: Đám cháy lớn có nhiều lính cứu hỏa **và** nhiều thiệt hại hơn.
> <br><span class="en">*Example*: Bigger fires have more firefighters **and** more damage.</span>
> Điều này có nghĩa là lính cứu hỏa gây ra thiệt hại do cháy? **Không.**
> <br><span class="en">Does this mean firefighters cause fire damage? **No.**</span>
> Chính đám cháy lớn (biến gây nhiễu) gây ra **cả hai**: vừa gây thiệt hại nhiều hơn, vừa khiến phải điều nhiều lính cứu hỏa hơn đến hiện trường.
> <br><span class="en">It is the size of the fire (the confounding variable) that causes **both**: more damage, and the need to dispatch more firefighters to the scene.</span>

### 5.2 Reverse causality (nhân quả ngược) - <span class="en">5.2 Reverse causality</span>

Biến mà ta tưởng là "kết quả" (Y) thực ra mới là nguyên nhân tác động ngược lại lên biến ta tưởng là "nguyên nhân" (X).
<br><span class="en">The variable we think is the "outcome" (Y) is in fact the one that causes an effect back on the variable we think is the "cause" (X).</span>

> *Ví dụ*: Khu vực có tội phạm cao hơn có xu hướng có nhiều cảnh sát hơn.
> <br><span class="en">*Example*: Areas with higher crime tend to have more police.</span>
> Điều này có nghĩa là cảnh sát gây ra tội phạm? **Không.**
> <br><span class="en">Does this mean police cause crime? **No.**</span>
> Chính quyền điều thêm cảnh sát **đến** những nơi vốn đã có tội phạm cao — chiều nhân quả đi ngược lại so với trực giác ban đầu.
> <br><span class="en">The authorities dispatch more police **to** places that already have high crime — the direction of causality runs opposite to the initial intuition.</span>

### 5.3 Coincidence (trùng hợp ngẫu nhiên) - <span class="en">5.3 Coincidence</span>

Hai biến di chuyển cùng nhau hoàn toàn ngẫu nhiên, không có cơ chế thật nào liên kết chúng.
<br><span class="en">Two variables move together entirely by chance, with no real mechanism linking them.</span>

> *Ví dụ kinh điển*: Số lượng cướp biển trên thế giới giảm dần trong khi nhiệt độ toàn cầu tăng dần.
> <br><span class="en">*Classic example*: The number of pirates in the world has been steadily declining while global temperature has been steadily rising.</span>
> Điều này có nghĩa là ít cướp biển hơn gây ra nóng lên toàn cầu? **Không.**
> <br><span class="en">Does this mean fewer pirates causes global warming? **No.**</span>
> Hai biến này di chuyển cùng nhau hoàn toàn do trùng hợp, không phải vì biến này gây ra biến kia.
> <br><span class="en">These two variables move together purely by coincidence, not because one causes the other.</span>

### 5.4 Vì sao điều này quan trọng cho chính sách — bảng minh họa sai lầm chính sách - <span class="en">5.4 Why this matters for policy — a table illustrating policy mistakes</span>

Nhầm association với causation không chỉ là lỗi học thuật — nó dẫn thẳng đến **sai lầm chính sách** nếu người ra quyết định hành động dựa trên con số tương quan mà không kiểm tra cơ chế nhân quả đằng sau.
<br><span class="en">Confusing association with causation is not merely an academic error — it leads directly to **policy mistakes** if decision-makers act on correlation numbers without checking the causal mechanism behind them.</span>

| Quan sát (association)<br><span class="en">Observation (association)</span> | Kết luận sai nếu nhầm là causal<br><span class="en">Wrong conclusion if mistaken for causal</span> | Chính sách sai lầm có thể xảy ra<br><span class="en">Possible resulting policy mistake</span> | Vì sao sai<br><span class="en">Why it's wrong</span> |
|---|---|---|---|
| Doanh số kem tăng cùng lúc với số vụ tai nạn đuối nước tăng<br><span class="en">Ice cream sales rise at the same time as drowning accidents rise</span> | "Ăn kem làm tăng nguy cơ đuối nước"<br><span class="en">"Eating ice cream increases drowning risk"</span> | Hạn chế/đánh thuế nặng việc bán kem để giảm tai nạn đuối nước<br><span class="en">Restrict/heavily tax ice cream sales to reduce drowning accidents</span> | Rất có thể cả hai đều tăng vì cùng một nguyên nhân thứ ba: mùa nóng khiến người dân vừa mua kem nhiều hơn, vừa đi bơi/tắm biển nhiều hơn (tăng rủi ro đuối nước) — không phải kem gây đuối nước<br><span class="en">Both very likely rise because of the same third cause: hot weather leads people to both buy more ice cream and swim/go to the beach more (raising drowning risk) — ice cream does not cause drowning</span> |
| Đám cháy lớn có nhiều lính cứu hỏa và nhiều thiệt hại<br><span class="en">Bigger fires have more firefighters and more damage</span> | "Điều thêm lính cứu hỏa làm tăng thiệt hại"<br><span class="en">"Dispatching more firefighters increases damage"</span> | Cắt giảm lực lượng cứu hỏa để giảm thiệt hại do cháy<br><span class="en">Cut the firefighting force to reduce fire damage</span> | Đám cháy lớn (confounder) gây ra cả hai; cắt lính cứu hỏa thực chất sẽ làm thiệt hại **tệ hơn**<br><span class="en">The size of the fire (the confounder) causes both; cutting firefighters would actually make damage **worse**</span> |
| Khu vực tội phạm cao có nhiều cảnh sát<br><span class="en">High-crime areas have more police</span> | "Cảnh sát làm tăng tội phạm"<br><span class="en">"Police increase crime"</span> | Rút cảnh sát khỏi khu vực để giảm tội phạm<br><span class="en">Withdraw police from the area to reduce crime</span> | Chiều nhân quả ngược lại: cảnh sát được điều đến *vì* tội phạm cao, không phải nguyên nhân của tội phạm<br><span class="en">The direction of causality is reversed: police are dispatched *because* crime is high, they are not the cause of crime</span> |
> Ghi chú rõ ở đây để không lẫn giữa nội dung gốc và suy luận áp dụng logic tương tự.
> <br><span class="en">This is noted explicitly here so as not to conflate the original content with an inference applying similar logic.</span>

## 6. Ceteris paribus — "các yếu tố khác giữ nguyên" - <span class="en">6. Ceteris paribus — "other factors held constant"</span>

Ngay cả khi tránh được ba bẫy ở mục 5, câu hỏi kinh tế thật sự nhà nghiên cứu quan tâm thường không phải "X và Y có đi cùng nhau không" mà là: **giữ mọi yếu tố liên quan khác không đổi, Y thay đổi bao nhiêu khi X thay đổi 1 đơn vị?**
<br><span class="en">Even after avoiding the three traps in section 5, the real economic question a researcher cares about is usually not "do X and Y move together" but rather: **holding all other relevant factors constant, how much does Y change when X changes by 1 unit?**</span>
Đây gọi là hiệu ứng **ceteris paribus** ("mọi thứ khác không đổi" — tiếng Latin).
<br><span class="en">This is called the **ceteris paribus** effect ("everything else held constant" — Latin).</span>

*Ví dụ minh họa*: Lương thay đổi thế nào khi giáo dục tăng, **giữ nguyên** ability (năng lực), gia đình, và các yếu tố khác?
<br><span class="en">*Illustrative example*: How does wage change when education increases, **holding fixed** ability, family, and other factors?</span>
Để kiểm soát các yếu tố này, ta đưa chúng vào cùng phương trình hồi quy:
<br><span class="en">To control for these factors, we include them in the same regression equation:</span>

$$wage = \beta_0 + \beta_1 \cdot education + \beta_2 \cdot ability + \cdots + u$$

Trong dữ liệu quan sát được (observational data), rất nhiều yếu tố cùng ảnh hưởng đến outcome kinh tế.
<br><span class="en">In observational data, many factors simultaneously affect the economic outcome.</span>
Nếu không kiểm soát các yếu tố này, quan hệ quan sát được có thể phản ánh **nhiều ảnh hưởng trộn lẫn với nhau**, không chỉ riêng ảnh hưởng của biến ta đang quan tâm.
<br><span class="en">If these factors are not controlled for, the observed relationship may reflect **many effects mixed together**, not just the effect of the variable we care about.</span>

**Vấn đề thực tế**: trong thực hành, ta hiếm khi quan sát được **tất cả** các yếu tố liên quan như ability — đây chính là điểm nối trực tiếp sang mục 7.
<br><span class="en">**The practical problem**: in practice, we rarely observe **all** the relevant factors such as ability — this is exactly the point that connects directly to section 7.</span>

## 7. Omitted Variable Bias (OVB) — thiên lệch do bỏ sót biến - <span class="en">7. Omitted Variable Bias (OVB)</span>

Để ước lượng đúng hiệu ứng ceteris paribus, cần kiểm soát **mọi** yếu tố liên quan ảnh hưởng đến outcome.
<br><span class="en">To correctly estimate the ceteris paribus effect, one needs to control for **every** relevant factor affecting the outcome.</span>
Nhưng trong thực tế, một số biến liên quan là **không quan sát được hoặc không có sẵn dữ liệu**.
<br><span class="en">But in reality, some relevant variables are **unobservable or have no available data**.</span>
Khi một yếu tố quan trọng bị bỏ sót khỏi mô hình hồi quy, hệ số ước lượng được có thể bị **thiên lệch** (biased).
<br><span class="en">When an important factor is omitted from the regression model, the estimated coefficient can become **biased**.</span>

Quay lại ví dụ giáo dục–lương với phương trình đơn giản (chưa kiểm soát gì):
<br><span class="en">Back to the education–wage example with the simple equation (controlling for nothing yet):</span>

$$wage = \beta_0 + \beta_1 \cdot education + u$$

Phương trình này bỏ qua các yếu tố gây nhiễu (confounding factors) như **ability, gia đình, mạng lưới xã hội**.
<br><span class="en">This equation ignores confounding factors such as **ability, family, social networks**.</span>
Vì các yếu tố này ảnh hưởng đến **cả** trình độ học vấn lẫn kết quả trên thị trường lao động (lương), và vì chúng không được quan sát, chúng nằm gọn trong sai số $u$ — khiến `education` trở nên **tương quan với sai số**.
<br><span class="en">Because these factors affect **both** education level and labor-market outcomes (wages), and because they are unobserved, they sit entirely inside the error term $u$ — making `education` **correlated with the error term**.</span>
Kết quả: hệ số ước lượng $\hat\beta_1$ không còn đo riêng "hiệu ứng thật của giáo dục", mà **trộn lẫn** hai thứ:
<br><span class="en">Result: the estimated coefficient $\hat\beta_1$ no longer measures purely "the true effect of education", but **mixes together** two things:</span>

- hiệu ứng thật của education lên wage, **và**
  <br><span class="en">the true effect of education on wage, **and**</span>
- hiệu ứng của ability lên wage (bị "gán nhầm" cho education vì hai biến này tương quan với nhau).
  <br><span class="en">the effect of ability on wage (wrongly "attributed" to education because the two variables are correlated with each other).</span>

**Giải thích cho người mới học "bias" nghĩa là gì**: bias ở đây không phải là "sai số ngẫu nhiên" (nếu lấy mẫu lại nhiều lần, sai số ngẫu nhiên sẽ trung bình về 0).
<br><span class="en">**Explanation for beginners of what "bias" means**: bias here is not "random error" (if we resample repeatedly, random error averages out to 0).</span>
Bias là một **độ lệch có hệ thống** — dù có lấy bao nhiêu mẫu dữ liệu đi nữa, ước lượng vẫn liên tục lệch theo một hướng nhất định so với giá trị thật, vì bản thân *cách xây dựng* mô hình (thiếu biến quan trọng) đã sai ngay từ đầu.
<br><span class="en">Bias is a **systematic deviation** — no matter how many data samples you draw, the estimate keeps deviating in a consistent direction from the true value, because the very *way the model was built* (missing an important variable) was wrong from the start.</span>
Tăng cỡ mẫu **không** sửa được omitted variable bias — đây khác hẳn với vấn đề "ước lượng kém chính xác vì mẫu nhỏ".
<br><span class="en">Increasing the sample size **does not** fix omitted variable bias — this is entirely different from the problem of "imprecise estimates due to a small sample".</span>

Câu hỏi tự nhiên nảy sinh từ đây, và cũng là câu hỏi trung tâm của toàn bộ phần còn lại của khóa học: **nếu các yếu tố quan trọng không quan sát được, làm sao nhận diện (identify) được hiệu ứng thật của giáo dục lên lương?**
<br><span class="en">The natural question that arises from this, and which is also the central question for the rest of the course: **if important factors are unobservable, how can we identify the true effect of education on wages?**</span>
Đây chính xác là **lý do khóa học tồn tại** — gần như mọi topic sau (multicollinearity, heteroskedasticity, và đặc biệt là [[concepts/endogeneity-iv-regression]]) đều xoay quanh việc phát hiện và xử lý các biến thể khác nhau của vấn đề này.
<br><span class="en">This is precisely **why the course exists** — almost every subsequent topic (multicollinearity, heteroskedasticity, and especially [[concepts/endogeneity-iv-regression]]) revolves around detecting and handling different variants of this problem.</span>

## 8. Identification Problem — trái tim của Econometrics - <span class="en">8. The Identification Problem — the heart of Econometrics</span>

> Một tham số được gọi là **identified** khi dữ liệu và mô hình cho phép ta **cô lập** (isolate) được hiệu ứng nhân quả của một biến lên outcome.
> <br><span class="en">A parameter is called **identified** when the data and the model allow us to **isolate** the causal effect of a variable on the outcome.</span>

### 8.1 Trực giác: "biến thiên sạch" là gì? - <span class="en">8.1 Intuition: what is "clean variation"?</span>

Nhà kinh tế học quan tâm đến hiệu ứng ceteris paribus của một biến lên một outcome.
<br><span class="en">Economists care about the ceteris paribus effect of a variable on an outcome.</span>
Nhưng trong dữ liệu quan sát được, biến ta quan tâm thường bị ảnh hưởng bởi **rất nhiều yếu tố khác cùng lúc** — nghĩa là phần biến thiên (variation) quan sát được của nó phản ánh **nhiều nguồn ảnh hưởng trộn lẫn**, không chỉ riêng cơ chế nhân quả ta muốn nghiên cứu.
<br><span class="en">But in observational data, the variable we care about is usually affected by **many other factors at the same time** — meaning its observed variation reflects **many mixed sources of influence**, not just the causal mechanism we want to study.</span>
**Identification** nghĩa là tìm ra được phần biến thiên trong biến giải thích **không** bị chi phối bởi các yếu tố gây nhiễu — chỉ khi có phần biến thiên "sạch" này, ta mới thực sự cô lập được hiệu ứng nhân quả.
<br><span class="en">**Identification** means finding the portion of variation in the explanatory variable that is **not** driven by confounding factors — only with this "clean" variation can we truly isolate the causal effect.</span>

### 8.2 Ví dụ đầy đủ: giá điện và tiêu thụ điện - <span class="en">8.2 A full example: electricity price and electricity consumption</span>

Ví dụ "statistical vs. econometric question" ở mục 3 minh họa cụ thể identification problem:
<br><span class="en">The "statistical vs. econometric question" example from section 3 concretely illustrates the identification problem:</span>

- Ta muốn ước lượng hiệu ứng của giá điện lên tiêu thụ điện của hộ gia đình.
  <br><span class="en">We want to estimate the effect of electricity price on household electricity consumption.</span>
- Quan sát được: khu vực có giá điện cao hơn thường có tiêu thụ điện thấp hơn.
  <br><span class="en">Observed: areas with higher electricity prices tend to have lower electricity consumption.</span>
- Nhưng pattern này có thể bị chi phối bởi nhiều yếu tố khác: **thu nhập (income), khí hậu (climate), đặc điểm nhà ở (housing characteristics), hiệu suất sử dụng năng lượng (energy efficiency)**.
  <br><span class="en">But this pattern could be driven by many other factors: **income, climate, housing characteristics, energy efficiency**.</span>
- Vì các yếu tố này thay đổi khác nhau giữa các khu vực, quan hệ quan sát được **có thể không phản ánh** hiệu ứng thật của giá điện.
  <br><span class="en">Because these factors vary differently across regions, the observed relationship **may not reflect** the true effect of the price.</span>
- **Để identify được hiệu ứng nhân quả**, cần có sự thay đổi trong giá điện mà **không** liên quan đến các yếu tố gây nhiễu này.
  <br><span class="en">**To identify the causal effect**, we need variation in the electricity price that is **not** related to these confounding factors.</span>
- *Ví dụ về biến thiên "sạch"*: một chính sách của chính phủ làm tăng giá điện **đồng loạt** trên nhiều khu vực. Trong trường hợp này, phần biến thiên của giá không bị chi phối bởi đặc điểm riêng của từng hộ gia đình — loại biến thiên này giúp cô lập được hiệu ứng ceteris paribus của giá lên tiêu thụ điện.
  <br><span class="en">*Example of "clean" variation*: a government policy that raises the electricity price **uniformly** across many regions. In this case, the variation in price is not driven by the specific characteristics of individual households — this type of variation helps isolate the ceteris paribus effect of price on consumption.</span>

### 8.3 Vì sao kinh tế học khó hơn khoa học tự nhiên ở điểm này - <span class="en">8.3 Why economics is harder than natural science in this respect</span>

Trong khoa học tự nhiên, quan hệ nhân quả thường được nghiên cứu bằng **controlled experiments** (thí nghiệm có kiểm soát): nhà nghiên cứu chủ động thay đổi một biến trong khi giữ các yếu tố khác không đổi.
<br><span class="en">In natural sciences, causal relationships are usually studied using **controlled experiments**: the researcher actively changes one variable while holding other factors constant.</span>

> *Ví dụ minh họa*: để nghiên cứu hiệu ứng của một loại thuốc, nhà nghiên cứu **phân bổ ngẫu nhiên** (randomly assign) bệnh nhân vào nhóm điều trị (treatment group) và nhóm đối chứng (control group).
> <br><span class="en">*Illustrative example*: to study the effect of a drug, the researcher **randomly assigns** patients into a treatment group and a control group.</span>
> Vì việc phân bổ là ngẫu nhiên, các yếu tố khác được cân bằng tự động giữa hai nhóm — nhờ đó cô lập được hiệu ứng nhân quả thật của thuốc.
> <br><span class="en">Because the assignment is random, other factors are automatically balanced between the two groups — thereby isolating the true causal effect of the drug.</span>

Trong kinh tế học và các ngành khoa học xã hội khác, **controlled experiments thường khó hoặc không thể thực hiện được**.
<br><span class="en">In economics and other social sciences, **controlled experiments are often difficult or impossible to carry out**.</span>
Kết quả kinh tế bị ảnh hưởng bởi rất nhiều yếu tố không dễ kiểm soát trực tiếp:
<br><span class="en">Economic outcomes are affected by many factors that are not easy to control directly:</span>

- không thể phân bổ ngẫu nhiên **số năm đi học** cho từng cá nhân;
  <br><span class="en">we cannot randomly assign **years of schooling** to each individual;</span>
- không thể thay đổi ngẫu nhiên **hệ thống thuế** áp dụng cho từng cá nhân;
  <br><span class="en">we cannot randomly vary the **tax system** applied to each individual;</span>
- chính sách thường tác động đồng thời lên **nhiều nhóm** cùng lúc, khó tách riêng từng cá nhân.
  <br><span class="en">policies usually affect **many groups** simultaneously, making it hard to isolate individuals.</span>

Vì vậy, nhà kinh tế học thường phải dựa vào **observational data** (dữ liệu quan sát được, không phải dữ liệu từ thí nghiệm có kiểm soát) và các **chiến lược nhận diện gián tiếp** (identification strategies) để mô phỏng lại, càng gần càng tốt, điều kiện "biến thiên sạch" mà một thí nghiệm ngẫu nhiên hóa mang lại tự nhiên.
<br><span class="en">Therefore, economists usually have to rely on **observational data** (data that is observed, not generated by a controlled experiment) and indirect **identification strategies** to replicate, as closely as possible, the "clean variation" condition that a randomized experiment naturally provides.</span>
Đây chính là lý do toàn bộ phần sau của khóa học tồn tại: IV regression ([[concepts/endogeneity-iv-regression]]), panel data FE/RE ([[concepts/fixed-random-effects-model]]), dynamic panel GMM... đều là các "chiến lược nhận diện" khác nhau, phù hợp với các bối cảnh dữ liệu khác nhau, nhưng chung một mục tiêu: tìm ra biến thiên không bị chi phối bởi confounding.
<br><span class="en">This is precisely why the entire rest of the course exists: IV regression ([[concepts/endogeneity-iv-regression]]), panel data FE/RE ([[concepts/fixed-random-effects-model]]), dynamic panel GMM... are all different "identification strategies", suited to different data contexts, but sharing one goal: finding variation that is not driven by confounding.</span>

## 9. Quy trình nghiên cứu thực nghiệm (Empirical research process) - <span class="en">9. The empirical research process</span>

Nghiên cứu kinh tế thực nghiệm thường đi theo một trình tự 6 bước:
<br><span class="en">Empirical economic research usually follows a 6-step sequence:</span>

1. **Research question** — một câu hỏi kinh tế được định nghĩa rõ ràng. *Ví dụ*: giá điện tăng có làm giảm tiêu thụ điện của hộ gia đình không?
   <br><span class="en">**Research question** — a clearly defined economic question. *Example*: does a higher electricity price reduce household electricity consumption?</span>
2. **Economic theory** — khung lý thuyết giải thích tại sao quan hệ đó có thể tồn tại. *Ví dụ*: người tiêu dùng giảm tiêu thụ khi giá tăng (lý thuyết cầu cơ bản).
   <br><span class="en">**Economic theory** — the theoretical framework explaining why that relationship might exist. *Example*: consumers reduce consumption when the price rises (basic demand theory).</span>
3. **Empirical model** — biểu diễn hình thức của quan hệ lý thuyết. *Ví dụ*: $Consumption = f(Price, Income, Household\ Characteristics)$.
   <br><span class="en">**Empirical model** — the formal representation of the theoretical relationship. *Example*: $Consumption = f(Price, Income, Household\ Characteristics)$.</span>
4. **Data** — thu thập dữ liệu quan sát được cho các biến liên quan.
   <br><span class="en">**Data** — collecting observed data for the relevant variables.</span>
5. **Econometric analysis** — phương pháp thống kê dùng để ước lượng quan hệ và kiểm định giả thuyết.
   <br><span class="en">**Econometric analysis** — the statistical methods used to estimate the relationship and test hypotheses.</span>
6. **Interpretation and policy implications** — diễn giải kết quả và rút ra hàm ý chính sách.
   <br><span class="en">**Interpretation and policy implications** — interpreting the results and drawing out policy implications.</span>

### Ba câu hỏi nền tảng ở mỗi bước - <span class="en">Three foundational questions at every step</span>

Đằng sau 6 bước kỹ thuật trên, có **ba câu hỏi nền tảng** thực sự quyết định chất lượng của một nghiên cứu thực nghiệm — minh họa lại bằng đúng ví dụ giá điện:
<br><span class="en">Behind the 6 technical steps above, there are **three foundational questions** that truly determine the quality of an empirical study — illustrated again using the same electricity-price example:</span>

1. **Câu hỏi kinh tế là gì?** (*What is the economic question?*) — cần định nghĩa rõ quan hệ đang quan tâm. *Ví dụ*: giá điện tăng có làm giảm tiêu thụ điện của hộ gia đình không? Bước này xác định: biến outcome, biến quan tâm chính, và câu hỏi hành vi/chính sách đang được đặt ra.
   <br><span class="en">**What is the economic question?** — the relationship of interest needs to be clearly defined. *Example*: does a higher electricity price reduce household electricity consumption? This step identifies: the outcome variable, the main variable of interest, and the behavioral/policy question being asked.</span>
2. **Cơ chế kinh tế là gì?** (*What is the economic mechanism?*) — lý thuyết kinh tế giải thích **vì sao** quan hệ này có thể tồn tại. *Ví dụ*: giá cao hơn làm tăng chi phí của việc tiêu thụ, có thể khiến hộ gia đình giảm sử dụng điện. Lý thuyết giúp xác định: biến nào quan trọng, chúng liên hệ với nhau ra sao.
   <br><span class="en">**What is the economic mechanism?** — the economic theory explaining **why** this relationship might exist. *Example*: a higher price raises the cost of consumption, which may lead households to reduce electricity use. Theory helps identify: which variables matter, and how they relate to each other.</span>
3. **Hiệu ứng nhân quả có identify được trong dữ liệu không?** (*Can the causal effect be identified in the data?*) — quan hệ quan sát được có thể bị confound bởi các yếu tố khác; thách thức cốt lõi là cô lập được phần biến thiên trong biến giải thích **không** bị chi phối bởi các ảnh hưởng gây nhiễu. Đây chính là **nhiệm vụ trung tâm của econometrics**, không phải câu hỏi (1) hay (2).
   <br><span class="en">**Can the causal effect be identified in the data?** — the observed relationship may be confounded by other factors; the core challenge is isolating the portion of variation in the explanatory variable that is **not** driven by confounding influences. This is precisely the **central task of econometrics**, not question (1) or (2).</span>

## 10. Bẫy thi tổng hợp (exam traps) - <span class="en">10. Summary exam traps</span>

1. **Diễn giải association như causation** chỉ vì hai biến "đi cùng nhau" trong dữ liệu — luôn phải hỏi: có confounding, reverse causality, hay coincidence nào có thể giải thích pattern này không, trước khi kết luận nhân quả.
   <br><span class="en">**Interpreting association as causation** just because two variables "move together" in the data — always ask whether confounding, reverse causality, or coincidence could explain this pattern, before concluding causality.</span>
2. **Mặc định rằng chạy regression tự động cho ra hiệu ứng nhân quả** — hệ số hồi quy chỉ mô tả quan hệ *trong dữ liệu*; nếu không có một identification strategy đáng tin cậy, hệ số ước lượng **không đại diện** cho causal effect, dù có ý nghĩa thống kê mạnh đến đâu.
   <br><span class="en">**Assuming that running a regression automatically produces a causal effect** — a regression coefficient only describes a relationship *within the data*; without a credible identification strategy, the estimated coefficient **does not represent** the causal effect, no matter how strong its statistical significance.</span>
3. **Tập trung vào estimation (tính hệ số) mà quên mất identification (tìm biến thiên "sạch")** — thách thức trung tâm của econometrics không phải là *tính toán* ra một con số $\hat\beta$, mà là tìm được nguồn biến thiên trong biến giải thích không bị chi phối bởi confounding. Tính hệ số dễ; identify được hiệu ứng nhân quả mới khó.
   <br><span class="en">**Focusing on estimation (computing the coefficient) while forgetting identification (finding "clean" variation)** — the central challenge of econometrics is not *computing* a number $\hat\beta$, but finding a source of variation in the explanatory variable that is not driven by confounding. Computing a coefficient is easy; identifying the causal effect is the hard part.</span>
4. **Nhầm "không quan sát thấy confounder rõ ràng" với "không có confounder"** — omitted variable bias xảy ra chính xác vì các yếu tố gây nhiễu (như ability) thường **không quan sát được**, không phải vì chúng không tồn tại.
   <br><span class="en">**Confusing "no confounder is clearly observed" with "no confounder exists"** — omitted variable bias occurs precisely because confounding factors (like ability) are usually **unobservable**, not because they don't exist.</span>
5. **Coi ceteris paribus effect (đã kiểm soát các biến quan sát được) là causal effect** — kiểm soát được các biến *có trong dữ liệu* không đảm bảo đã kiểm soát hết mọi confounder; vẫn có thể còn omitted variable bias từ các yếu tố chưa/không quan sát được.
   <br><span class="en">**Treating the ceteris paribus effect (controlling for observed variables) as the causal effect** — controlling for the variables *present in the data* does not guarantee every confounder has been controlled for; omitted variable bias can still remain from factors that are not yet, or cannot be, observed.</span>
6. **Nhầm lẫn statistics và econometrics** — một mô hình dự báo tốt (statistics) không đồng nghĩa với việc đã tìm ra quan hệ nhân quả (econometrics); hai mục tiêu khác nhau, dùng chung công cụ nhưng không thể đánh đồng.
   <br><span class="en">**Confusing statistics and econometrics** — a good predictive model (statistics) does not mean a causal relationship has been found (econometrics); two different objectives that share tools but cannot be equated.</span>
7. **Suy diễn quá đà từ một ví dụ coincidence hoặc confounding sang đề xuất chính sách** (xem bảng mục 5.4) — sai lầm chính sách kinh điển là hành động như thể association là causation, dẫn đến can thiệp vào đúng biến sai (VD hạn chế bán kem để giảm đuối nước).
   <br><span class="en">**Over-extrapolating from a coincidence or confounding example into a policy proposal** (see the table in section 5.4) — the classic policy mistake is acting as if association were causation, leading to intervening on exactly the wrong variable (e.g. restricting ice cream sales to reduce drowning).</span>

## 11. Kết nối với phần còn lại của khóa học - <span class="en">11. Connection to the rest of the course</span>

Trang này là điểm neo (anchor) cho toàn bộ wiki.
<br><span class="en">This page is the anchor for the entire wiki.</span>
Khóa học có 3 phần chính (**3 main parts**), mỗi phần là một tập hợp công cụ khác nhau để giải quyết identification problem trong các bối cảnh dữ liệu khác nhau:
<br><span class="en">The course has **3 main parts**, each a different set of tools for solving the identification problem in different data contexts:</span>

- **Phần 1 — Linear Regression Model và các vấn đề của nó**: OLS, multicollinearity, heteroskedasticity, endogeneity. Xem [[concepts/linear-regression-model]] (OLS, 5 giả định), [[concepts/functional-forms]], [[concepts/multicollinearity]], [[concepts/heteroskedasticity]], [[concepts/endogeneity-iv-regression]].
  <br><span class="en">**Part 1 — The Linear Regression Model and its problems**: OLS, multicollinearity, heteroskedasticity, endogeneity. See [[concepts/linear-regression-model]] (OLS, 5 assumptions), [[concepts/functional-forms]], [[concepts/multicollinearity]], [[concepts/heteroskedasticity]], [[concepts/endogeneity-iv-regression]].</span>
- **Phần 2 — Models for Limited Dependent Variables**: logit/probit, multinomial logit, Poisson/negative binomial regression, ordinal response model, censored/truncated regressions. Xem [[concepts/binary-response-models]] (LPM/Logit/Probit), [[concepts/multinomial-logit-model]], [[concepts/ordinal-response-models]], [[concepts/count-data-models]], [[concepts/censored-regression-tobit]].
  <br><span class="en">**Part 2 — Models for Limited Dependent Variables**: logit/probit, multinomial logit, Poisson/negative binomial regression, ordinal response model, censored/truncated regressions. See [[concepts/binary-response-models]] (LPM/Logit/Probit), [[concepts/multinomial-logit-model]], [[concepts/ordinal-response-models]], [[concepts/count-data-models]], [[concepts/censored-regression-tobit]].</span>
- **Phần 3 — Panel data models**: FE/RE, IV regression cho panel data (2SLS, LIML, GMM), dynamic panel data model. Xem [[concepts/fixed-random-effects-model]] (FE/RE), [[concepts/iv-regression-panel-data]], [[concepts/dynamic-panel-data-models]] — dùng chiều thời gian để kiểm soát các confounder không quan sát được và bất biến theo thời gian (một chiến lược identification khác, không cần biến công cụ bên ngoài).
  <br><span class="en">**Part 3 — Panel data models**: FE/RE, IV regression for panel data (2SLS, LIML, GMM), dynamic panel data model. See [[concepts/fixed-random-effects-model]] (FE/RE), [[concepts/iv-regression-panel-data]], [[concepts/dynamic-panel-data-models]] — using the time dimension to control for unobserved, time-invariant confounders (a different identification strategy, one that does not require an external instrumental variable).</span>

Toàn bộ 15 topic của khóa học đã được ingest (xem `index.md` để tra cứu đầy đủ) — trang này đóng vai trò bản đồ tổng thể kết nối tất cả: mỗi công cụ kỹ thuật ở các trang `concepts/` khác đều là một câu trả lời cụ thể cho câu hỏi triết lý duy nhất đặt ra ở trang này — **làm sao identify được hiệu ứng nhân quả khi không thể chạy một controlled experiment thật sự**.
<br><span class="en">All 15 topics of the course have been ingested (see `index.md` for the full listing) — this page serves as the overall map connecting everything: every technical tool on the other `concepts/` pages is a specific answer to the single philosophical question this page poses — **how to identify the causal effect when a true controlled experiment cannot be run**.</span>
