---
title: "Lecture 5: Endogeneity and Instrumental Variable (IV) Regression"
type: concept
status: mature
tags: [endogeneity, instrumental-variables, 2sls, gmm, liml, hausman-test]
sources: ["[[sources/slides-5-endogeneity-iv-regression]]", "[[sources/slides-16-endogeneity-iv-regression-extended]]"]
related: ["[[concepts/linear-regression-model]]", "[[concepts/econometrics-overview]]", "[[people/hausman]]"]
lecture: 5
assignment: ["Assignment 4: Endogeneity and Instrumental Variable Regression"]
updated: 2026-09-04
---

> **Cách đọc trang này**: đây là trang giải quyết vi phạm giả định **A3 (exogeneity)** của [[concepts/linear-regression-model]] — có lẽ là chủ đề quan trọng nhất môn học vì nó chạm trực tiếp vào câu hỏi "khi nào một hệ số hồi quy thực sự đo được quan hệ nhân quả". Trang hợp nhất `slides-5-iu.pdf` (bản gốc, 63 trang) và `slides-16-iu.pdf` (bản mở rộng, 70 trang, dùng làm cấu trúc chính/canonical). Khác biệt chính giữa hai bản: slides-16 sửa thuật ngữ "biased" → "inconsistent" cho chính xác hơn, và thêm hẳn một mục mới — **robust inference dưới weak instruments** (Anderson-Rubin, Stock-Wright) — không có trong slides-5. Các khác biệt số liệu cụ thể giữa hai bản được ghi chú tại đúng chỗ xuất hiện trong bài, không âm thầm sửa.
> <br><span class="en">**How to read this page**: this page resolves the violation of assumption **A3 (exogeneity)** of [[concepts/linear-regression-model]] — arguably the single most important topic in the course, because it goes straight at the question "when does a regression coefficient actually measure a causal relationship?" The page merges `slides-5-iu.pdf` (original version, 63 slides) and `slides-16-iu.pdf` (extended version, 70 slides, used as the canonical structure). Main difference between the two versions: slides-16 corrects the terminology "biased" → "inconsistent" for greater precision, and adds an entirely new section — **robust inference under weak instruments** (Anderson-Rubin, Stock-Wright) — absent from slides-5. Specific numerical discrepancies between the two versions are noted exactly where they occur in the text, never silently reconciled.</span>

**Lecture 5** trong đề cương (CO Topic 5) — Assignment 4: Endogeneity and Instrumental Variable Regression.
<br><span class="en">**Lecture 5** in the syllabus (CO Topic 5) — Assignment 4: Endogeneity and Instrumental Variable Regression.</span>

## 1. Endogeneity là gì? — trực quan trước khi vào công thức - <span class="en">What is endogeneity? — intuition before formulas</span>

### 1.1 Câu chuyện minh họa: giáo dục, năng lực và lương - <span class="en">Illustrative story: education, ability, and wages</span>

Giả sử bạn muốn trả lời câu hỏi kinh điển của kinh tế học lao động: "đi học thêm 1 năm thì lương tăng bao nhiêu?" Bạn hồi quy $\ln(wage)$ lên `schooling` (số năm đi học) và một số biến kiểm soát khác. OLS cho ra một hệ số dương, có ý nghĩa thống kê. Kết luận có ổn không?
<br><span class="en">Suppose you want to answer the classic labor-economics question: "how much does wage increase for one extra year of schooling?" You regress $\ln(wage)$ on `schooling` (number of years of education) and a few other control variables. OLS produces a positive, statistically significant coefficient. Is that conclusion sound?</span>

Vấn đề: người có nhiều năng lực/khả năng bẩm sinh hơn (ability) thường **vừa** có xu hướng học lên cao hơn (dễ học, được khuyến khích học tiếp) **vừa** kiếm được lương cao hơn (làm việc hiệu quả hơn, không cần thông qua bằng cấp). Nhưng `ability` hầu như không bao giờ được đo lường trực tiếp trong dữ liệu khảo sát — nó nằm trong phần **không quan sát được**, tức nằm trong sai số $e$ của mô hình. Vì `ability` vừa tương quan với `schooling` vừa là một phần của $e$, nên `schooling` tương quan với $e$. Hệ quả: hệ số OLS của `schooling` không chỉ đo "tác động của việc đi học lên lương" — nó còn "trộn" luôn một phần tác động của năng lực bẩm sinh (vì năng lực cao đi kèm với học nhiều hơn). Ta không còn tách được đâu là hiệu ứng thật của giáo dục, đâu là hiệu ứng của năng lực "đi ké" theo giáo dục.
<br><span class="en">The problem: people with more innate ability tend **both** to pursue more schooling (learning comes easier, they're encouraged to continue) **and** to earn higher wages (they work more productively, independent of credentials). But `ability` is almost never measured directly in survey data — it sits in the **unobserved** part, i.e. inside the model's error term $e$. Because `ability` is correlated with `schooling` and is also part of $e$, `schooling` ends up correlated with $e$. Consequence: the OLS coefficient on `schooling` no longer measures only "the effect of schooling on wages" — it also "mixes in" part of the effect of innate ability (since higher ability comes bundled with more schooling). We can no longer separate the true effect of education from the effect of ability "riding along" with education.</span>

Đây chính là bản chất của **endogeneity**: biến giải thích không còn "sạch" — nó mang theo thông tin tương quan với đúng cái phần mà mô hình gán cho sai số ngẫu nhiên.
<br><span class="en">This is the essence of **endogeneity**: the explanatory variable is no longer "clean" — it carries information correlated with exactly the part the model assigns to the random error.</span>

### 1.2 Định nghĩa hình thức - <span class="en">Formal definition</span>

Phương trình cấu trúc (structural equation / data generating process — DGP):
<br><span class="en">Structural equation / data generating process (DGP):</span>

$$y=X\beta+e$$

OLS ước lượng $\hat\beta_{OLS}=(X'X)^{-1}X'y$, suy ra $X'X\hat\beta_{OLS}=X'y=X'(X\beta+e)=X'X\beta+X'e$, tức:
<br><span class="en">OLS estimates $\hat\beta_{OLS}=(X'X)^{-1}X'y$, which implies $X'X\hat\beta_{OLS}=X'y=X'(X\beta+e)=X'X\beta+X'e$, i.e.:</span>

$$X'X\hat\beta_{OLS} = X'X\beta + X'e$$

OLS **giả định** $X'e=0$ — đây chính xác là nội dung giả định A3 (exogeneity) của [[concepts/linear-regression-model]]: sai số không mang thông tin hệ thống nào liên quan đến $X$.
<br><span class="en">OLS **assumes** $X'e=0$ — this is exactly assumption A3 (exogeneity) of [[concepts/linear-regression-model]]: the error carries no systematic information related to $X$.</span>

$$\textbf{Endogeneity xảy ra khi } X'e\neq0$$
<br><span class="en">$$\textbf{Endogeneity occurs when } X'e\neq0$$</span>

— bất kỳ regressor nào tương quan với sai số. Hệ quả trực tiếp từ đúng đẳng thức ở trên:
<br><span class="en">— any regressor correlated with the error. Direct consequence of the identity above:</span>

- Nếu $X'e=0$ → $\hat\beta_{OLS}=\beta$.
<br><span class="en">If $X'e=0$ → $\hat\beta_{OLS}=\beta$.</span>
- Nếu $X'e\neq0$ → $\hat\beta_{OLS}\neq\beta$.
<br><span class="en">If $X'e\neq0$ → $\hat\beta_{OLS}\neq\beta$.</span>

**Thuật ngữ chính xác — điểm slides-16 sửa lại so với slides-5**: khi $X'e\neq0$, cách gọi chính xác là $\hat\beta_{OLS}$ trở thành ước lượng **inconsistent** (không vững) — tức càng có nhiều dữ liệu, ước lượng vẫn *không* hội tụ về giá trị thật $\beta$. Bản slides-5 ở một số chỗ gọi đây là "biased" (chệch); slides-16 sửa nhất quán thành "inconsistent". Về bản chất hai khái niệm khác nhau: bias là sai lệch ở mẫu hữu hạn (có thể biến mất khi $N\to\infty$ với một số vi phạm khác); còn dưới endogeneity, vấn đề **không biến mất** dù có tăng cỡ mẫu bao nhiêu — đây là lý do "inconsistent" mới là mô tả đúng bản chất vấn đề.
<br><span class="en">**Precise terminology — the point slides-16 corrects from slides-5**: when $X'e\neq0$, the precise way to describe it is that $\hat\beta_{OLS}$ becomes an **inconsistent** estimator — i.e. no matter how much more data you have, the estimate still does *not* converge to the true value $\beta$. Slides-5 in places calls this "biased"; slides-16 consistently corrects it to "inconsistent." The two concepts differ in nature: bias is a finite-sample discrepancy (which can vanish as $N\to\infty$ under some other violations); under endogeneity, the problem **does not vanish** no matter how large the sample grows — which is why "inconsistent" is the term that correctly describes the nature of the problem.</span>

### 1.3 Hệ quả cho diễn giải nhân quả - <span class="en">Consequences for causal interpretation</span>

Với $y=X\beta+e$:
<br><span class="en">With $y=X\beta+e$:</span>

- Nếu $e$ **không** tương quan với $X$: hiệu ứng nhân quả (causal effect) chính là $\dfrac{\partial y}{\partial X}=\beta$ — hệ số hồi quy đo đúng cái ta muốn.
<br><span class="en">If $e$ is **not** correlated with $X$: the causal effect is exactly $\dfrac{\partial y}{\partial X}=\beta$ — the regression coefficient measures precisely what we want.</span>
- Nếu $e$ **tương quan** với $X$: vì $e$ cũng thay đổi theo $X$, hiệu ứng đầy đủ trở thành $\dfrac{\partial y}{\partial X}=\beta+\dfrac{\partial e}{\partial X}$ — tức $\beta$ **không còn cô lập được** tác động thật sự của $X$ lên $y$ nữa; nó bị trộn lẫn với một phần đến từ $e$.
<br><span class="en">If $e$ **is** correlated with $X$: because $e$ also changes with $X$, the full effect becomes $\dfrac{\partial y}{\partial X}=\beta+\dfrac{\partial e}{\partial X}$ — meaning $\beta$ **no longer isolates** the true effect of $X$ on $y$; it is mixed with a part coming from $e$.</span>

Nói cách khác: $R^2$ cao, t-statistic có ý nghĩa thống kê mạnh — không cứu được một hệ số bị endogeneity làm hỏng. Đây chính là lý do mục 9 của [[concepts/linear-regression-model]] nhấn mạnh "$R^2$ cao không phải mục tiêu của econometrics" — mục tiêu là ước lượng đúng $\beta$, và endogeneity là kẻ thù trực tiếp của mục tiêu đó.
<br><span class="en">In other words: a high $R^2$ or a strongly significant t-statistic cannot rescue a coefficient corrupted by endogeneity. This is exactly why section 9 of [[concepts/linear-regression-model]] stresses that "a high $R^2$ is not the goal of econometrics" — the goal is to correctly estimate $\beta$, and endogeneity is the direct enemy of that goal.</span>

## 2. Ba nguồn gốc của endogeneity — mỗi loại một ví dụ cụ thể - <span class="en">Three sources of endogeneity — one concrete example per type</span>

### 2.1 Omission of important regressors (bỏ sót biến quan trọng) - <span class="en">Omission of important regressors</span>

Giả sử DGP thật là $y=\beta_0+\beta_1x_1+\beta_2x_2+e$, nhưng ta bỏ sót $x_2$ (vì không có dữ liệu, hoặc không nghĩ tới), chỉ hồi quy:
<br><span class="en">Suppose the true DGP is $y=\beta_0+\beta_1x_1+\beta_2x_2+e$, but we omit $x_2$ (no data available, or it simply wasn't considered), and only run:</span>

$$y=\beta_0+\beta_1x_1+\mu, \qquad \mu=\beta_2x_2+e$$

Khi đó $E(\mu x_1)\neq0$ **nếu** $Cov(x_1,x_2)\neq0$ — sai số mới $\mu$ "chứa" $x_2$ bị bỏ sót, và nếu $x_2$ tương quan với $x_1$ đang có mặt trong mô hình, thì $\mu$ cũng tương quan với $x_1$ → endogeneity.
<br><span class="en">Then $E(\mu x_1)\neq0$ **if** $Cov(x_1,x_2)\neq0$ — the new error $\mu$ "contains" the omitted $x_2$, and if $x_2$ is correlated with $x_1$ which remains in the model, then $\mu$ is also correlated with $x_1$ → endogeneity.</span>

**Ví dụ của slide**: doanh số kem (ice cream sales) và số vụ đuối nước (drowning accidents) tương quan dương rất mạnh trong dữ liệu theo mùa — nhưng không phải kem "gây ra" đuối nước. Biến bị bỏ sót là **nhiệt độ mùa hè**: trời nóng vừa làm người ta mua kem nhiều hơn, vừa làm người ta đi bơi nhiều hơn (và do đó tăng rủi ro đuối nước). Bỏ sót nhiệt độ khỏi mô hình khiến biến kem "hấp thụ" luôn một phần ảnh hưởng của nhiệt độ.
<br><span class="en">**Slide example**: ice cream sales and drowning accidents are strongly positively correlated in seasonal data — but ice cream does not "cause" drowning. The omitted variable is **summer temperature**: hot weather both makes people buy more ice cream and makes people swim more (and hence increases drowning risk). Omitting temperature from the model causes the ice-cream variable to "absorb" part of temperature's influence.</span>

**Chính là trường hợp giáo dục–lương ở mục 1.1**: DGP thật có `ability`, ta bỏ sót nó, `ability` tương quan với `schooling` → `schooling` trở thành biến nội sinh.
<br><span class="en">**This is exactly the education–wage case from section 1.1**: the true DGP includes `ability`, we omit it, `ability` is correlated with `schooling` → `schooling` becomes an endogenous variable.</span>

### 2.2 Reverse causality / simultaneity (nhân quả ngược / đồng thời) - <span class="en">Reverse causality / simultaneity</span>

Giả sử ta muốn hồi quy $y=\beta X+e$, nhưng thực ra $y$ cũng tác động ngược lại $X$ — một phương trình phản hồi (feedback equation):
<br><span class="en">Suppose we want to regress $y=\beta X+e$, but in reality $y$ also feeds back and affects $X$ — a feedback equation:</span>

$$X=\gamma y+v$$

Thế $y=\beta X+e$ vào phương trình feedback:
<br><span class="en">Substituting $y=\beta X+e$ into the feedback equation:</span>

$$X=\gamma(\beta X+e)+v \;\;\Rightarrow\;\; X=\frac{\gamma e}{1-\gamma\beta}+\frac{v}{1-\gamma\beta}$$

$X$ giờ đây là một hàm số của chính $e$ → $X$ tương quan với $e$ → endogeneity.
<br><span class="en">$X$ is now a function of $e$ itself → $X$ is correlated with $e$ → endogeneity.</span>

**Ví dụ của slide**: cảnh sát (police) và tội phạm (crime). Có nhiều cảnh sát hơn có thể làm giảm tội phạm (hướng nhân quả "thuận" ta muốn đo) — nhưng đồng thời, nơi tội phạm cao cũng thường được bố trí nhiều cảnh sát hơn (hướng nhân quả "ngược" — chính quyền phản ứng lại tình trạng tội phạm). Hồi quy đơn giản `crime` lên `số cảnh sát` sẽ trộn lẫn cả hai chiều tác động, khiến hệ số ước lượng không còn đo được đúng "tác động thuần của cảnh sát lên tội phạm".
<br><span class="en">**Slide example**: police and crime. More police officers can reduce crime (the "forward" causal direction we want to measure) — but at the same time, areas with high crime are also typically assigned more police (the "reverse" direction — authorities respond to crime conditions). A simple regression of `crime` on `number of police` mixes both directions of effect, so the estimated coefficient no longer measures the true "net effect of police on crime."</span>

### 2.3 Measurement error (sai số đo lường) - <span class="en">Measurement error</span>

Xét hồi quy $y=\beta x+e$, nhưng ta không quan sát được $x$ thật, mà chỉ quan sát một phiên bản có nhiễu:
<br><span class="en">Consider the regression $y=\beta x+e$, but we do not observe the true $x$, only a noisy version of it:</span>

$$x^*=x+v \quad (v = \text{sai số đo lường})$$
<br><span class="en">$$x^*=x+v \quad (v = \text{measurement error})$$</span>

Phương trình ta thực sự hồi quy trở thành $y=\beta x^*+e=\beta(x+v)+e$, tức:
<br><span class="en">The equation we actually run becomes $y=\beta x^*+e=\beta(x+v)+e$, i.e.:</span>

$$y=\beta x+\omega, \qquad \omega=\beta v+e$$

Cả sai số mới $\omega$ **lẫn** biến giải thích $x$ đều chứa $v$ → chúng tương quan với nhau → endogeneity. (Đây là dạng "classical measurement error trong biến độc lập" — khác với sai số đo lường ở biến phụ thuộc $y$, vốn thường không gây endogeneity mà chỉ làm tăng phương sai sai số.)
<br><span class="en">Both the new error $\omega$ **and** the explanatory variable $x$ contain $v$ → they are correlated with each other → endogeneity. (This is "classical measurement error in the independent variable" — different from measurement error in the dependent variable $y$, which typically does not cause endogeneity, only inflates the error variance.)</span>

## 3. Ví dụ xuyên suốt: phương trình lương ở TP.HCM - <span class="en">Running example: the wage equation in HCMC</span>

$$\ln wage = f(schooling, X) + e$$

`schooling` bị nghi ngờ là biến nội sinh chính xác theo cơ chế mục 2.1: **ability/năng lực** (không quan sát được) vừa ảnh hưởng đến quyết định học lên, vừa ảnh hưởng trực tiếp đến năng suất lao động và do đó đến lương → `ability` nằm trong $e$ → `schooling` tương quan với $e$.
<br><span class="en">`schooling` is suspected to be endogenous through exactly the mechanism of section 2.1: **ability** (unobserved) both affects the decision to pursue further education and directly affects labor productivity and hence wages → `ability` sits inside $e$ → `schooling` is correlated with $e$.</span>

**Dữ liệu**: khảo sát người lao động tại TP.HCM.
<br><span class="en">**Data**: a survey of workers in Ho Chi Minh City.</span>

| Biến | Ý nghĩa | Vai trò |
|---|---|---|
| `wage` | Lương ($/giờ) | Biến phụ thuộc |
| `age` | Tuổi (năm) | Kiểm soát |
| `schooling` | Số năm đi học | **Biến nội sinh nghi ngờ** |
| `tenure` | Số tháng làm việc tại nơi hiện tại | Kiểm soát |
| `gender` | 1 = nam, 0 = nữ | Kiểm soát |
| `origin` | 1 = di cư, 0 = người TP.HCM | Kiểm soát |
| `science` | 1 = khối tự nhiên (nền = công nghệ) | Kiểm soát |
| `social` | 1 = khối xã hội (nền = công nghệ) | Kiểm soát |
| `fatheredu` | Số năm đi học của cha | **Instrument** |
| `motheredu` | Số năm đi học của mẹ | **Instrument** |

<span class="en">

| Variable | Meaning | Role |
|---|---|---|
| `wage` | Wage ($/hour) | Dependent variable |
| `age` | Age (years) | Control |
| `schooling` | Number of years of education | **Suspected endogenous variable** |
| `tenure` | Number of months at the current job | Control |
| `gender` | 1 = male, 0 = female | Control |
| `origin` | 1 = migrant, 0 = HCMC native | Control |
| `science` | 1 = science track (base = technology) | Control |
| `social` | 1 = social-science track (base = technology) | Control |
| `fatheredu` | Father's number of years of education | **Instrument** |
| `motheredu` | Mother's number of years of education | **Instrument** |

</span>

> **Ghi chú nhỏ về nguồn**: bản `slides-5-iu.pdf` ghi mô tả cả `fatheredu` **và** `motheredu` đều là "schooling years of the **father**" — rõ ràng là lỗi copy-paste (biến `motheredu` không thể là học vấn của cha). Bản `slides-16-iu.pdf` đã sửa đúng thành "schooling years of the **mother**". Không có gì cần làm thêm — chỉ ghi nhận đây là một ví dụ cụ thể cho thấy slides-16 tinh chỉnh lại slides-5, đúng như log ingest đã ghi.
> <br><span class="en">**Small source note**: `slides-5-iu.pdf` describes both `fatheredu` **and** `motheredu` as "schooling years of the **father**" — clearly a copy-paste error (the `motheredu` variable cannot be the father's education). `slides-16-iu.pdf` correctly fixes it to "schooling years of the **mother**." Nothing further needs to be done here — just noting this as a concrete example of slides-16 refining slides-5, consistent with what the ingest log already records.</span>

Hồi quy OLS trực tiếp $\ln wage$ lên `schooling` và các biến kiểm soát cho ra một hệ số — nhưng slide nhấn mạnh ngay: **"This OLS estimate is biased if schooling is endogenous"**. Đây chính là động lực để chuyển sang instrumental variable regression.
<br><span class="en">Running OLS directly of $\ln wage$ on `schooling` and the controls produces a coefficient — but the slide immediately stresses: **"This OLS estimate is biased if schooling is endogenous."** This is exactly the motivation for moving to instrumental variable regression.</span>

## 4. Instrumental Variables — "instrument tốt" cần gì? - <span class="en">Instrumental Variables — what does a "good instrument" need?</span>

### 4.1 Trực giác: hai điều kiện - <span class="en">Intuition: two conditions</span>

Xét mô hình:
<br><span class="en">Consider the model:</span>

$$y=\alpha+\beta_1X_1+\beta_2X_2+e$$

với $X_2$ là biến nội sinh nghi ngờ ($E(X_2'e)\neq0$). Ý tưởng của IV là tìm một biến "phụ" $Z$ (hay $IV$/$W$ theo cách slide đặt tên) đóng vai trò "nguồn biến động sạch" cho $X_2$ — biến động nào của $X_2$ đến từ $Z$ thì được giữ lại để ước lượng, biến động nào đến từ phần "bẩn" (tương quan với $e$) thì bị loại bỏ.
<br><span class="en">with $X_2$ the suspected endogenous variable ($E(X_2'e)\neq0$). The idea of IV is to find an "auxiliary" variable $Z$ (called $IV$/$W$ in the slide's notation) that acts as a "clean source of variation" for $X_2$ — whatever variation in $X_2$ comes from $Z$ is kept for estimation, whatever comes from the "dirty" part (correlated with $e$) is discarded.</span>

Để làm được việc đó, $Z$ phải thỏa **đồng thời** hai điều kiện — thiếu một trong hai là instrument "hỏng":
<br><span class="en">To do this, $Z$ must satisfy **both** conditions simultaneously — missing either one makes the instrument "broken":</span>

1. **Relevance (tính liên quan)**: $Z$ phải thực sự tương quan với $X_2$. Trực giác: nếu $Z$ gần như không liên quan gì đến $X_2$, dùng nó để "thay thế" cho biến động của $X_2$ chẳng khác nào dùng nhiễu ngẫu nhiên — không giúp ích gì (xem thêm mục 6.1 về hậu quả của instrument yếu).
<br><span class="en">**Relevance**: $Z$ must actually be correlated with $X_2$. Intuition: if $Z$ is nearly unrelated to $X_2$, using it to "substitute" for $X_2$'s variation is no different from using random noise — it doesn't help (see section 6.1 for the consequences of weak instruments).</span>
2. **Exogeneity / Exclusion (tính ngoại sinh / bị loại trừ)**: $Z$ không được tương quan với $e$, và quan trọng hơn — về mặt trực giác — $Z$ chỉ được phép ảnh hưởng đến $y$ **thông qua** $X_2$, không có đường tác động trực tiếp nào khác lên $y$.
<br><span class="en">**Exogeneity / Exclusion**: $Z$ must not be correlated with $e$, and more importantly — intuitively — $Z$ is only allowed to affect $y$ **through** $X_2$, with no other direct path onto $y$.</span>

Slide làm rõ thêm mối quan hệ giữa hai khái niệm "exogeneity" và "exclusion": về mặt toán học, exogeneity ($Z$ không tương quan $e$) tự nó đã bao hàm exclusion. Sở dĩ slide tách riêng "exclusion" ra để nhấn mạnh, là vì trong thực hành nghiên cứu, cái dễ vi phạm nhất chính là có một **đường tác động trực tiếp** từ instrument đến $y$ mà nhà nghiên cứu không lường trước — tách riêng ra giúp người đọc tự hỏi cụ thể: "liệu $Z$ có kênh nào khác tác động lên $y$, ngoài kênh đi qua $X_2$ hay không?"
<br><span class="en">The slide further clarifies the relationship between "exogeneity" and "exclusion": mathematically, exogeneity ($Z$ uncorrelated with $e$) already implies exclusion. The slide separates out "exclusion" for emphasis because, in research practice, the easiest thing to violate is an unanticipated **direct path** from the instrument to $y$ — separating it out prompts the reader to ask specifically: "does $Z$ have any other channel onto $y$, besides the one through $X_2$?"</span>

**Áp dụng vào ví dụ lương**: `fatheredu`, `motheredu` được đề xuất làm instrument cho `schooling`.
<br><span class="en">**Applied to the wage example**: `fatheredu` and `motheredu` are proposed as instruments for `schooling`.</span>

- **Relevance**: học vấn của cha mẹ thường tương quan mạnh với học vấn của con (điều kiện gia đình, kỳ vọng, nguồn lực đầu tư cho giáo dục) — có thể kiểm định trực tiếp bằng first-stage F (xem mục 6.1).
<br><span class="en">**Relevance**: parents' education is typically strongly correlated with their child's education (family conditions, expectations, resources invested in education) — directly testable via the first-stage F (see section 6.1).</span>
- **Exclusion**: giả định học vấn cha mẹ **chỉ** ảnh hưởng đến lương của người con **thông qua** việc con học được bao nhiêu năm — không có đường tác động trực tiếp nào khác (cha mẹ học cao không trực tiếp "trả lương" cho con), và không tương quan với các yếu tố không quan sát được khác trong hàm lương (như ability, mạng lưới quan hệ...). Đây là một **giả định**, không phải điều kiện kiểm định được trực tiếp bằng dữ liệu (xem mục 6.2).
<br><span class="en">**Exclusion**: assumes parents' education affects the child's wage **only** through how many years the child studies — no other direct path (highly educated parents don't directly "pay" their child's wage), and no correlation with other unobserved factors in the wage function (such as ability, social networks...). This is an **assumption**, not a condition directly testable with data (see section 6.2).</span>

### 4.2 Bài toán identification: $h$ so với $k$ - <span class="en">The identification problem: $h$ versus $k$</span>

Gọi $k$ = số biến nội sinh, $h$ = số instrument (excluded instruments):
<br><span class="en">Let $k$ = number of endogenous variables, $h$ = number of instruments (excluded instruments):</span>

| So sánh | Tên gọi | Ý nghĩa trực quan |
|---|---|---|
| $h<k$ | **Unidentified** (không được phép) | Không đủ "nguồn biến động sạch" để tách hết các biến nội sinh — bài toán không giải được |
| $h=k$ | **Just-identified / exactly-identified** | Vừa đủ instrument cho mỗi biến nội sinh — nghiệm duy nhất, nhưng **không thể kiểm định được** liệu instrument có thực sự valid hay không (xem mục 6.2) |
| $h>k$ | **Over-identified** | Nhiều instrument hơn cần thiết — phần "dư" này cho phép **kiểm định overidentifying restrictions** |

<span class="en">

| Comparison | Name | Intuitive meaning |
|---|---|---|
| $h<k$ | **Unidentified** (not allowed) | Not enough "clean sources of variation" to separate out all endogenous variables — the problem is unsolvable |
| $h=k$ | **Just-identified / exactly-identified** | Exactly enough instruments for each endogenous variable — a unique solution, but **cannot be tested** for whether the instruments are actually valid (see section 6.2) |
| $h>k$ | **Over-identified** | More instruments than strictly needed — this "surplus" enables **testing overidentifying restrictions** |

</span>

Trong ví dụ lương: 1 biến nội sinh (`schooling`, $k=1$), 2 instrument (`fatheredu`, `motheredu`, $h=2$) → **over-identified** ($h>k$) → có thể kiểm định overidentifying restrictions bằng Sargan/Hansen J.
<br><span class="en">In the wage example: 1 endogenous variable (`schooling`, $k=1$), 2 instruments (`fatheredu`, `motheredu`, $h=2$) → **over-identified** ($h>k$) → overidentifying restrictions can be tested via Sargan/Hansen J.</span>

## 5. 2-Stage Least Squares (2SLS) - <span class="en">2-Stage Least Squares (2SLS)</span>

### 5.1 Thủ tục 2 bước thủ công — và vì sao SE của nó không đáng tin - <span class="en">The manual 2-step procedure — and why its SE cannot be trusted</span>

Trước khi có công thức 2SLS đóng gói sẵn, ý tưởng gốc rất trực quan — làm thủ công theo 2 bước:
<br><span class="en">Before the packaged 2SLS formula existed, the original idea was very intuitive — done manually in 2 steps:</span>

- **Stage 1**: hồi quy biến nội sinh $X_2$ lên $X_1$ (biến ngoại sinh sẵn có trong mô hình, gọi là **included instruments**) và $IV$ (instrument, gọi là **excluded instruments**):
<br><span class="en">**Stage 1**: regress the endogenous variable $X_2$ on $X_1$ (the exogenous variables already in the model, called **included instruments**) and $IV$ (the instrument, called **excluded instruments**):</span>
$$X_2=\gamma_0+\gamma_1X_1+\gamma_2 IV+v$$
rồi tính giá trị dự đoán (fitted values): $\hat X_2=\hat\gamma_0+\hat\gamma_1X_1+\hat\gamma_2 IV$. Stage này cũng chính là nơi ta **kiểm định relevance** — hệ số $\gamma_2$ của $IV$ có khác 0 hay không (xem mục 6.1).
<br><span class="en">then compute the fitted values: $\hat X_2=\hat\gamma_0+\hat\gamma_1X_1+\hat\gamma_2 IV$. This stage is also exactly where we **test relevance** — whether the coefficient $\gamma_2$ on $IV$ is different from 0 (see section 6.1).</span>
- **Stage 2**: hồi quy $y$ lên $X_1$ và $\hat X_2$ (thay vì $X_2$ thật):
<br><span class="en">**Stage 2**: regress $y$ on $X_1$ and $\hat X_2$ (instead of the true $X_2$):</span>
$$y=\alpha+\beta_1X_1+\beta_2\hat X_2+e$$
Vì $\hat X_2$ chỉ là phần biến động của $X_2$ "giải thích được" bởi $X_1$ và $IV$ — với $IV$ thỏa exogeneity — nên $\hat X_2$ **không còn tương quan với $e$** nữa, giải quyết được vấn đề endogeneity.
<br><span class="en">Because $\hat X_2$ is only the part of $X_2$'s variation "explained" by $X_1$ and $IV$ — with $IV$ satisfying exogeneity — $\hat X_2$ is **no longer correlated with $e$**, which resolves the endogeneity problem.</span>

> **Cảnh báo quan trọng**: nếu làm thủ công đúng 2 bước OLS riêng biệt như trên, **standard error ở stage 2 bị tính sai (inconsistent)** — lý do là stage 2 "quên" rằng $\hat X_2$ chỉ là ước lượng (có độ bất định riêng từ stage 1), không phải giá trị quan sát thật. Đây chính xác là lý do cần một **2SLS estimator** đóng gói sẵn (mục 5.2) thay vì tự chạy 2 hồi quy OLS liên tiếp bằng tay.
> <br><span class="en">**Important warning**: if done manually as two separate OLS steps as above, **the standard error at stage 2 is computed incorrectly (inconsistent)** — because stage 2 "forgets" that $\hat X_2$ is only an estimate (carrying its own uncertainty from stage 1), not a true observed value. This is exactly why a packaged **2SLS estimator** (section 5.2) is needed instead of manually running two consecutive OLS regressions.</span>

### 5.2 2SLS estimator dạng đóng - <span class="en">2SLS estimator in closed form</span>

Đặt $Z=[X_1,\ IV]$ — bộ công cụ đầy đủ (full instrument set). Công thức 2SLS estimator:
<br><span class="en">Let $Z=[X_1,\ IV]$ — the full instrument set. The 2SLS estimator formula:</span>

$$b_{2SLS} = \big[(X'Z)(Z'Z)^{-1}(Z'X)\big]^{-1}(X'Z)(Z'Z)^{-1}Z'y$$

**Trường hợp đặc biệt đáng nhớ**: nếu $Z=X$ (không có excluded instrument nào, không có biến nội sinh nào) — 2SLS **thu gọn về đúng OLS**:
<br><span class="en">**A special case worth remembering**: if $Z=X$ (no excluded instruments, no endogenous variables) — 2SLS **collapses exactly to OLS**:</span>

$$b_{2SLS}=(X'X)^{-1}X'y = b_{OLS}$$

Điều này cho thấy 2SLS không phải một công cụ "khác hẳn" OLS — nó là OLS được tổng quát hóa để xử lý trường hợp có biến nội sinh; khi không có biến nội sinh, hai công thức trùng nhau.
<br><span class="en">This shows 2SLS is not a tool "entirely different" from OLS — it is OLS generalized to handle the case with endogenous variables; when there are no endogenous variables, the two formulas coincide.</span>

### 5.3 Diễn giải hình chiếu (projection) — vì sao 2SLS chính là "OLS với $X_2$ đã lọc sạch" - <span class="en">Projection interpretation — why 2SLS is exactly "OLS with $X_2$ cleaned up"</span>

Slides-16 trình bày thêm một cách viết tương đương, giúp nối trực giác của thủ tục 2 bước (mục 5.1) với công thức đóng (mục 5.2). Đặt $\hat X = Z(Z'Z)^{-1}Z'X = P_Z X$ (phép chiếu $X$ lên không gian sinh bởi $Z$):
<br><span class="en">Slides-16 presents an additional equivalent formulation that bridges the intuition of the 2-step procedure (section 5.1) with the closed-form formula (section 5.2). Let $\hat X = Z(Z'Z)^{-1}Z'X = P_Z X$ (the projection of $X$ onto the space spanned by $Z$):</span>

$$b_{2SLS}=(\hat X'X)^{-1}\hat X'y$$

Thay $y=X\beta+e$ vào:
<br><span class="en">Substituting $y=X\beta+e$:</span>

$$b_{2SLS} = \beta + (\hat X'X)^{-1}\hat X'e$$

Từ đây thấy rõ hai điều kiện cần cho 2SLS "sống được":
<br><span class="en">From this, two conditions needed for 2SLS to be "viable" become clear:</span>

- **$b_{2SLS}$ chỉ xác định được** nếu $\hat X'X\neq0$ (tương đương $Z'X\neq0$) — đây chính là điều kiện **relevance**.
<br><span class="en">**$b_{2SLS}$ is only defined** if $\hat X'X\neq0$ (equivalent to $Z'X\neq0$) — this is exactly the **relevance** condition.</span>
- **$b_{2SLS}$ chỉ consistent** nếu $\hat X'e=0$ (tương đương $Z'e=0$) — đây chính là điều kiện **exogeneity**.
<br><span class="en">**$b_{2SLS}$ is only consistent** if $\hat X'e=0$ (equivalent to $Z'e=0$) — this is exactly the **exogeneity** condition.</span>

Vì $X=[X_1,X_2]$ và $Z=[X_1,IV]$, phép chiếu $P_Z$ tách ra thành $P_ZX=[P_ZX_1,\ P_ZX_2]$. Do $X_1$ đã nằm sẵn trong $Z$, chiếu $X_1$ lên không gian chứa chính nó thì **không đổi**: $P_ZX_1=X_1$. Chỉ có $P_ZX_2=\hat X_2$ là thay đổi. Nói cách khác: **2SLS chính xác là "giữ nguyên $X_1$, thay $X_2$ bằng giá trị dự đoán $\hat X_2$ từ stage 1"** — đúng như trực giác thủ tục 2 bước ở mục 5.1, chỉ khác là công thức đóng tính đúng SE ngay từ đầu.
<br><span class="en">Because $X=[X_1,X_2]$ and $Z=[X_1,IV]$, the projection $P_Z$ splits into $P_ZX=[P_ZX_1,\ P_ZX_2]$. Since $X_1$ is already inside $Z$, projecting $X_1$ onto a space that already contains it leaves it **unchanged**: $P_ZX_1=X_1$. Only $P_ZX_2=\hat X_2$ changes. In other words: **2SLS is precisely "keep $X_1$ as is, replace $X_2$ with the predicted value $\hat X_2$ from stage 1"** — exactly matching the intuition of the 2-step procedure in section 5.1, except the closed-form formula computes the SE correctly from the start.</span>

## 6. Ba nhóm kiểm định chẩn đoán sau IV regression - <span class="en">Three groups of diagnostic tests after IV regression</span>

Sau khi chạy 2SLS, có ba câu hỏi chẩn đoán cần trả lời, theo đúng thứ tự logic — mỗi câu hỏi chỉ có ý nghĩa **sau khi** câu hỏi trước đã được trả lời "đạt":
<br><span class="en">After running 2SLS, there are three diagnostic questions to answer, in strict logical order — each question is only meaningful **after** the previous question has been answered "pass":</span>

1. **Instrument có liên quan gì đến biến nội sinh không, và liên quan đủ mạnh không?** (weak instruments)
<br><span class="en">**Is the instrument related to the endogenous variable at all, and is it related strongly enough?** (weak instruments)</span>
2. **Nếu có nhiều hơn 1 instrument cho 1 biến nội sinh — các instrument "dư" có nhất quán với nhau không?** (overidentifying restrictions — chỉ áp dụng khi $h>k$)
<br><span class="en">**If there is more than 1 instrument for 1 endogenous variable — are the "surplus" instruments consistent with each other?** (overidentifying restrictions — applies only when $h>k$)</span>
3. **Biến nghi ngờ có thực sự nội sinh hay không?** (endogeneity — Wu-Hausman)
<br><span class="en">**Is the suspected variable actually endogenous?** (endogeneity — Wu-Hausman)</span>

### 6.1 Kiểm định instrument yếu (weak instruments) - <span class="en">Testing for weak instruments</span>

**Tại sao instrument yếu lại là vấn đề — trực giác trước khi vào công thức**: nhớ lại mục 5.3 — 2SLS thay $X_2$ bằng $\hat X_2$, giá trị dự đoán từ stage 1. Nếu instrument gần như không tương quan gì với $X_2$ (weak), thì $\hat X_2$ gần như **không mang thông tin thật** về $X_2$ — nó gần giống một biến nhiễu ngẫu nhiên hơn là một phiên bản "sạch" của $X_2$. Khi đó, ở stage 2, ta đang hồi quy $y$ lên một biến gần như nhiễu → ước lượng trở nên **rất nhạy với biến động ngẫu nhiên của mẫu** (phương sai rất lớn), và tệ hơn, phần "nhiễu hình chiếu" (projection noise) này có thể đẩy ước lượng 2SLS lệch xa giá trị thật theo một hướng có hệ thống — đến mức **bias của 2SLS dưới instrument yếu có thể còn tệ hơn bias của OLS dưới endogeneity mà ta đang cố sửa** ("liều thuốc còn tệ hơn bệnh" — cách nói của slide). Đây là lý do slide nhấn mạnh: instrument yếu **không phải chỉ là vấn đề về hiệu quả (efficiency)** — nó có thể phá hỏng hoàn toàn mục tiêu ban đầu của việc dùng IV.
<br><span class="en">**Why are weak instruments a problem — intuition before formulas**: recall section 5.3 — 2SLS replaces $X_2$ with $\hat X_2$, the predicted value from stage 1. If the instrument is nearly uncorrelated with $X_2$ (weak), then $\hat X_2$ carries **almost no real information** about $X_2$ — it behaves more like a random noise variable than a "clean" version of $X_2$. In that case, at stage 2, we are regressing $y$ on a nearly-noise variable → the estimate becomes **extremely sensitive to random sampling variation** (very large variance), and worse, this "projection noise" can push the 2SLS estimate systematically away from the true value — to the point that **2SLS bias under weak instruments can be even worse than the OLS bias from the endogeneity we were trying to fix** ("the cure can be worse than the disease" — the slide's own phrasing). This is why the slide stresses: weak instruments are **not merely an efficiency problem** — they can completely defeat the original purpose of using IV.</span>

Slides-16 tổ chức việc kiểm định "sức mạnh" của instrument thành ba tầng câu hỏi, từ yếu đến mạnh:
<br><span class="en">Slides-16 organizes the testing of instrument "strength" into three tiers of questions, from weakest to strongest:</span>

1. **Có liên quan gì không?** (Kleibergen-Paap rk LM test — test for underidentification)
<br><span class="en">**Is there any relevance at all?** (Kleibergen-Paap rk LM test — test for underidentification)</span>
2. **Liên quan đủ mạnh không?** (F-statistic / Cragg-Donald F / Kleibergen-Paap rk F, so với Stock-Yogo critical values)
<br><span class="en">**Is the relevance strong enough?** (F-statistic / Cragg-Donald F / Kleibergen-Paap rk F, compared against Stock-Yogo critical values)</span>
3. **Nếu vẫn không chắc đủ mạnh, còn cách nào suy luận đáng tin cậy không?** (Anderson-Rubin, Stock-Wright)
<br><span class="en">**If still unsure it's strong enough, is there a reliable way to do inference regardless?** (Anderson-Rubin, Stock-Wright)</span>

**Tầng 1 — Test for underidentification (kiểm định relevance)**:
<br><span class="en">**Tier 1 — Test for underidentification (relevance test)**:</span>

$H_0$: instrument không liên quan — chính xác hơn, $E(Z'X_2)=0$ (trường hợp 1 biến nội sinh); với nhiều biến nội sinh, $H_0: \text{rank}(Z'X_2)<k_2$. Diễn giải: hệ số của các instrument trong stage 1 đồng thời bằng 0.
<br><span class="en">$H_0$: the instrument is not relevant — more precisely, $E(Z'X_2)=0$ (single endogenous variable case); with multiple endogenous variables, $H_0: \text{rank}(Z'X_2)<k_2$. Interpretation: the instruments' coefficients in stage 1 are jointly zero.</span>

- Bác bỏ $H_0$ → bằng chứng ban đầu instrument **có liên quan** (nhưng **chưa nói gì về việc đủ mạnh hay không**).
<br><span class="en">Rejecting $H_0$ → initial evidence the instrument **is relevant** (but **says nothing yet about whether it is strong enough**).</span>
- Không bác bỏ $H_0$ → mô hình **unidentified**, cần tìm instrument khác — mọi kiểm định chẩn đoán tiếp theo đều **không đáng tin** trong trường hợp này.
<br><span class="en">Failing to reject $H_0$ → the model is **unidentified**, a different instrument is needed — every subsequent diagnostic test is **untrustworthy** in this case.</span>

Ví dụ số (ví dụ đơn giản dùng ở slides-5, một F-test đồng thời cho hệ số instrument ở stage 1): F-statistic (excluded instruments) $=10.07$, p-value rất nhỏ → bác bỏ $H_0$ → có bằng chứng các instrument liên quan đồng thời. Slides-16 thay bằng công cụ tổng quát/chuẩn hơn — **Kleibergen-Paap (KP) rk LM test**, có ưu điểm **robust với heteroskedasticity** (trong khi Cragg-Donald LM thì không).
<br><span class="en">Numerical example (a simple example used in slides-5, a joint F-test on the instrument coefficients at stage 1): F-statistic (excluded instruments) $=10.07$, very small p-value → reject $H_0$ → evidence the instruments are jointly relevant. Slides-16 replaces this with a more general/standard tool — the **Kleibergen-Paap (KP) rk LM test**, which has the advantage of being **robust to heteroskedasticity** (whereas Cragg-Donald LM is not).</span>

**Tầng 2 — Test for weak instruments (kiểm định độ mạnh, graduate level)**:
<br><span class="en">**Tier 2 — Test for weak instruments (strength test, graduate level)**:</span>

Bác bỏ được underidentification **không đảm bảo** instrument đủ mạnh — đây là hai kiểm định khác nhau. Cần so sánh:
<br><span class="en">Rejecting underidentification **does not guarantee** the instrument is strong enough — these are two different tests. One needs to compare:</span>

- **[[people/cragg-donald|Cragg-Donald]] (CD) F-statistic** — giả định homoskedasticity. Trường hợp 1 biến nội sinh + homoskedastic, CD F trùng số với F-statistic của excluded instruments ở stage 1.
<br><span class="en">**[[people/cragg-donald|Cragg-Donald]] (CD) F-statistic** — assumes homoskedasticity. In the case of 1 endogenous variable + homoskedasticity, the CD F numerically coincides with the F-statistic of the excluded instruments at stage 1.</span>
- **Kleibergen-Paap (KP) rk Wald F** — robust với heteroskedasticity, nhưng **không so sánh trực tiếp được** với bảng Stock-Yogo (bảng SY xây dựng dưới giả định homoskedastic); trong thực hành, người ta vẫn so sánh KP-F với SY hoặc với ngưỡng kinh nghiệm 10 một cách "không chính thức".
<br><span class="en">**Kleibergen-Paap (KP) rk Wald F** — robust to heteroskedasticity, but **cannot be directly compared** to the Stock-Yogo table (the SY table is built under the homoskedasticity assumption); in practice, people still compare KP-F to SY or to the rule-of-thumb threshold of 10 "informally."</span>

**Quy tắc kinh nghiệm phổ biến**: CD F-statistic $>10$. Nhưng để đáng tin cậy hơn, cần tính đúng thống kê rồi so với **[[people/stock-yogo|Stock-Yogo]] (SY) critical values** — có hai tiêu chí khác nhau để tra bảng, cho ra hai ngưỡng khác nhau:
<br><span class="en">**Common rule of thumb**: CD F-statistic $>10$. But for greater reliability, one should compute the correct statistic and compare it against **[[people/stock-yogo|Stock-Yogo]] (SY) critical values** — there are two different criteria for looking up the table, yielding two different thresholds:</span>

- **Relative bias** ($b$): giới hạn $\text{bias}(\hat\beta_{2SLS}) \le b\times\text{bias}(\hat\beta_{OLS})$ — trực giác, không phụ thuộc $\alpha$; nhưng "$10\%$ của một bias rất lớn" vẫn có thể lớn về giá trị tuyệt đối. Xấp xỉ: relative bias $\approx 1/\text{F-statistic}$ — đây chính là nguồn gốc quy tắc "F>10" ($1/10=10\%$).
<br><span class="en">**Relative bias** ($b$): bounds $\text{bias}(\hat\beta_{2SLS}) \le b\times\text{bias}(\hat\beta_{OLS})$ — intuitive, independent of $\alpha$; but "$10\%$ of a huge bias" can still be large in absolute terms. Approximation: relative bias $\approx 1/\text{F-statistic}$ — this is exactly the origin of the "F>10" rule ($1/10=10\%$).</span>
- **Size distortion** ($r$): đảm bảo kích thước kiểm định thực tế (test size thực) không vượt quá $r$ dù chọn $\alpha=5\%$ danh nghĩa — bảo vệ trực tiếp cho hypothesis testing, ngưỡng cao hơn (bảo thủ hơn).
<br><span class="en">**Size distortion** ($r$): ensures the actual test size does not exceed $r$ even when a nominal $\alpha=5\%$ is chosen — directly protects hypothesis testing, with a higher (more conservative) threshold.</span>

Ví dụ số (1 biến nội sinh, $K_2=2$ instrument, F-statistic quan sát $=10.07$):
<br><span class="en">Numerical example (1 endogenous variable, $K_2=2$ instruments, observed F-statistic $=10.07$):</span>

- **Relative bias $b=0.1$**: SY critical value $<9.08$ (bảng không có cột $K_2=2$, nhưng phải thấp hơn ngưỡng của $K_2=3$ là $9.08$) → $10.07>$ ngưỡng → **bác bỏ weak instruments** — instrument đủ mạnh để đảm bảo bias của 2SLS không vượt quá 10% bias của OLS.
<br><span class="en">**Relative bias $b=0.1$**: SY critical value $<9.08$ (the table has no column for $K_2=2$, but it must be lower than the $K_2=3$ threshold of $9.08$) → $10.07>$ threshold → **reject weak instruments** — the instrument is strong enough to ensure 2SLS bias does not exceed 10% of OLS bias.</span>
- **Size distortion**: đây là chỗ **hai bản slide dùng $r$ khác nhau cho cùng một ví dụ**, cho ra hai ngưỡng khác nhau — xem hộp ghi chú ngay dưới đây.
<br><span class="en">**Size distortion**: this is where **the two slide versions use different values of $r$ for the same example**, producing two different thresholds — see the note box right below.</span>

> **Ghi chú mâu thuẫn nguồn**: với **cùng** F-statistic $=10.07$, cùng 1 biến nội sinh + 2 instrument, hai bản slide chọn **giá trị $r$ khác nhau** để minh họa tiêu chí size distortion:
> <br><span class="en">**Source discrepancy note**: with the **same** F-statistic $=10.07$, the same 1 endogenous variable + 2 instruments, the two slide versions choose **different values of $r$** to illustrate the size distortion criterion:</span>
> - `slides-5-iu.pdf`: $r=15\%$ → SY critical value $=11.59$. Vì $10.07<11.59$ → **không bác bỏ** được weak instruments ở $r=15\%$ (instrument "yếu" theo tiêu chí này).
> <br><span class="en">`slides-5-iu.pdf`: $r=15\%$ → SY critical value $=11.59$. Since $10.07<11.59$ → weak instruments **cannot be rejected** at $r=15\%$ (the instrument is "weak" by this criterion).</span>
> - `slides-16-iu.pdf`: $r=10\%$ → SY critical value $=19.93$. Vì $10.07<19.93$ → **không bác bỏ** được weak instruments ở $r=10\%$ (kết luận tương tự, nhưng ngưỡng số khác hẳn).
> <br><span class="en">`slides-16-iu.pdf`: $r=10\%$ → SY critical value $=19.93$. Since $10.07<19.93$ → weak instruments **cannot be rejected** at $r=10\%$ (same conclusion, but a completely different numerical threshold).</span>
>
> Cả hai bản đều thống nhất thêm một điểm: ở $r=20\%$, ngưỡng SY $=8.75$, nên $F=10.07>8.75$ → **không yếu** ở mức $r=20\%$. Đây không hẳn là "lỗi" — chỉ là hai ví dụ minh họa dùng tham số $r$ đầu vào khác nhau — nhưng dễ gây nhầm lẫn nếu học viên so sánh trực tiếp ngưỡng $11.59$ và $19.93$ mà không để ý $r$ đã thay đổi giữa hai bản. Ghi chú lại ở đây thay vì chọn một con số rồi bỏ con số kia.
> <br><span class="en">Both versions agree on one further point: at $r=20\%$, the SY threshold $=8.75$, so $F=10.07>8.75$ → **not weak** at the $r=20\%$ level. This is not really an "error" — just two illustrative examples using different input values of $r$ — but it can easily confuse a student who directly compares the $11.59$ and $19.93$ thresholds without noticing that $r$ changed between the two versions. Noted here rather than picking one number and discarding the other.</span>

**Bias hay size — chọn tiêu chí nào?**
<br><span class="en">**Bias or size — which criterion to choose?**</span>

| Tiêu chí | Bảo vệ cho | Đặc điểm | Khi nào ưu tiên |
|---|---|---|---|
| Relative bias $b$ | Point estimate (giá trị hệ số ước lượng) | Trực giác, không phụ thuộc $\alpha$; nhưng kém bảo thủ hơn — "10% của bias khổng lồ" vẫn có thể lớn | Khi ưu tiên độ chính xác của **con số** ước lượng |
| Size distortion $r$ | Hypothesis testing (t-test, p-value có đáng tin không) | Bảo vệ trực tiếp việc kiểm định giả thuyết, ngưỡng cao hơn (bảo thủ hơn) | Khi ưu tiên **suy luận thống kê** (kiểm định giả thuyết) đáng tin cậy |

<span class="en">

| Criterion | Protects | Characteristics | When to prefer |
|---|---|---|---|
| Relative bias $b$ | Point estimate (the estimated coefficient value) | Intuitive, independent of $\alpha$; but less conservative — "10% of a huge bias" can still be large | When prioritizing accuracy of the estimated **number** |
| Size distortion $r$ | Hypothesis testing (whether the t-test/p-value can be trusted) | Directly protects hypothesis testing, higher (more conservative) threshold | When prioritizing reliable **statistical inference** (hypothesis testing) |

</span>

Điểm quan trọng slides-16 nhấn thêm: "**một ước lượng tốt không đảm bảo một kiểm định tốt, và một kiểm định tốt không đảm bảo một ước lượng tốt**" — đạt tiêu chí relative bias chỉ kiểm soát được độ lệch của con số ước lượng, không đảm bảo t-test/p-value đáng tin; đạt tiêu chí size distortion thì ngược lại. Trong thực hành, instrument thường rơi vào vùng **biên** — không đủ yếu để loại bỏ hoàn toàn, không đủ mạnh để tin tuyệt đối vào suy luận chuẩn (t-test thông thường) — đây chính là động lực cho mục tiếp theo.
<br><span class="en">An important point slides-16 adds: "**a good estimate does not guarantee a good test, and a good test does not guarantee a good estimate**" — meeting the relative bias criterion only controls the deviation of the estimated number, it does not guarantee the t-test/p-value is trustworthy; meeting the size distortion criterion is the reverse. In practice, instruments often fall into a **borderline** zone — not weak enough to discard entirely, not strong enough to fully trust standard inference (the ordinary t-test) — which is exactly the motivation for the next section.</span>

**Tầng 3 — Robust inference dưới weak instruments (chỉ có ở bản mở rộng slides-16)**:
<br><span class="en">**Tier 3 — Robust inference under weak instruments (only in the extended slides-16 version)**:</span>

Khi instrument ở vùng biên, thay vì tiếp tục tin vào t-test chuẩn (vốn thất bại khi instrument yếu), dùng các kiểm định **vẫn hợp lệ ngay cả khi instrument yếu** (miễn là không underidentified và instrument thực sự exogenous):
<br><span class="en">When the instrument is in the borderline zone, instead of continuing to trust the standard t-test (which fails when the instrument is weak), use tests that **remain valid even when the instrument is weak** (as long as it is not underidentified and the instrument is truly exogenous):</span>

- **Anderson-Rubin (AR) test**: dưới $H_0:\beta_2=\beta_0$, tính phần dư $u(\beta_0)=y-X_1\beta_1-X_2\beta_0$. Nếu $H_0$ đúng, $u(\beta_0)$ hành xử giống hệt sai số thật, tức $Z'u(\beta_0)\approx0$. AR hồi quy $u(\beta_0)$ lên $Z$ — nếu $Z$ vẫn giải thích được phần dư này một cách có ý nghĩa, bác bỏ $H_0$ (có bản AR-F kiểm định đồng thời ý nghĩa của excluded instruments, và bản AR chi-square dạng Wald).
<br><span class="en">**Anderson-Rubin (AR) test**: under $H_0:\beta_2=\beta_0$, compute the residual $u(\beta_0)=y-X_1\beta_1-X_2\beta_0$. If $H_0$ is true, $u(\beta_0)$ behaves exactly like the true error, i.e. $Z'u(\beta_0)\approx0$. AR regresses $u(\beta_0)$ on $Z$ — if $Z$ still explains this residual significantly, reject $H_0$ (there is an AR-F version jointly testing the significance of the excluded instruments, and an AR chi-square Wald-type version).</span>
- **Stock-Wright (SW) LM test**: dựa trên điều kiện moment $Z'u(\beta_0)$, bác bỏ $H_0$ nếu giá trị này lệch xa 0 một cách có ý nghĩa.
<br><span class="en">**Stock-Wright (SW) LM test**: based on the moment condition $Z'u(\beta_0)$, rejects $H_0$ if this value deviates significantly from 0.</span>

Ví dụ (kiểm định hệ số của `schooling` $=0$): tất cả các phiên bản AR/SW đều cho p-value $<5\%$ → bác bỏ $H_0$ → kết quả **vẫn hợp lệ dù instrument yếu** (nhưng không underidentified) — miễn là instrument thực sự exogenous.
<br><span class="en">Example (testing the coefficient of `schooling` $=0$): all AR/SW variants give p-value $<5\%$ → reject $H_0$ → the result **remains valid even though the instrument is weak** (but not underidentified) — as long as the instrument is truly exogenous.</span>

**Giới hạn quan trọng cần nhớ**: AR/SW **chỉ kiểm định được** giả thuyết về hệ số của biến nội sinh (không cải thiện chất lượng của chính điểm ước lượng — 2SLS vẫn có thể bất ổn/chệch khi instrument yếu), và **chỉ hợp lệ nếu instrument thực sự exogenous** — chúng không "cứu" được trường hợp instrument không hợp lệ (invalid), chỉ cứu được vấn đề "yếu" (weak).
<br><span class="en">**Important limitation to remember**: AR/SW **can only test** hypotheses about the endogenous variable's coefficient (they do not improve the quality of the point estimate itself — 2SLS can still be unstable/biased when the instrument is weak), and **are only valid if the instrument is truly exogenous** — they do not "rescue" the case of an invalid instrument, only the "weak" problem.</span>

### 6.2 Kiểm định overidentifying restrictions (chỉ khi $h>k$) - <span class="en">Testing overidentifying restrictions (only when $h>k$)</span>

Điều kiện exogeneity của instrument, viết lại dưới dạng có thể kiểm định: $E(Z'e)=E\big(Z'(y-X\hat\beta)\big)=0$ — còn gọi là điều kiện **orthogonality**.
<br><span class="en">The exogeneity condition of the instrument, rewritten in testable form: $E(Z'e)=E\big(Z'(y-X\hat\beta)\big)=0$ — also called the **orthogonality** condition.</span>

- Nếu mô hình **just-identified** ($h=k$): $\hat\beta$ luôn được chọn sao cho $Z'e=0$ **đúng theo cấu trúc của bài toán** (do số phương trình bằng đúng số ẩn) → **không có gì để kiểm định** — validity của instrument trong trường hợp này **không thể kiểm định bằng dữ liệu**, chỉ có thể lập luận bằng thiết kế nghiên cứu.
<br><span class="en">If the model is **just-identified** ($h=k$): $\hat\beta$ is always chosen such that $Z'e=0$ **holds by the structure of the problem** (since the number of equations exactly equals the number of unknowns) → **there is nothing to test** — instrument validity in this case **cannot be tested with data**, it can only be argued through research design.</span>
- Nếu **over-identified** ($h>k$): thêm instrument tức thêm ràng buộc lên $E(Z'e)=0$ — có $h-k$ ràng buộc "dư" so với mức cần cho identification, và đây chính là phần **kiểm định được**.
<br><span class="en">If **over-identified** ($h>k$): additional instruments mean additional restrictions on $E(Z'e)=0$ — there are $h-k$ "surplus" restrictions beyond what identification requires, and this surplus is exactly the part that **is testable**.</span>

$H_0$: tất cả instrument đều **valid** (valid = thỏa cả exogeneity lẫn exclusion — như đã bàn ở mục 4.1, về mặt toán học exogeneity bao hàm exclusion, nhưng tách riêng để nhấn mạnh rủi ro của một đường tác động trực tiếp từ IV đến $y$).
<br><span class="en">$H_0$: all instruments are **valid** (valid = satisfies both exogeneity and exclusion — as discussed in section 4.1, mathematically exogeneity implies exclusion, but they are separated out to emphasize the risk of a direct path from IV to $y$).</span>

**[[people/sargan|Sargan]] test** (giả định homoskedasticity):
<br><span class="en">**[[people/sargan|Sargan]] test** (assumes homoskedasticity):</span>

$$J=nR^2 \text{ (từ hồi quy phần dư IV } e \text{ lên toàn bộ instrument set } Z\text{)}, \qquad J\sim\chi^2_{h-k}$$
<br><span class="en">$$J=nR^2 \text{ (from regressing the IV residual } e \text{ on the full instrument set } Z\text{)}, \qquad J\sim\chi^2_{h-k}$$</span>

Hạn chế: không robust với heteroskedasticity hoặc autocorrelation.
<br><span class="en">Limitation: not robust to heteroskedasticity or autocorrelation.</span>

**[[people/hansen|Hansen's J]] test** (tổng quát hơn, cho phép heteroskedasticity):
<br><span class="en">**[[people/hansen|Hansen's J]] test** (more general, allows heteroskedasticity):</span>

$$J=n\cdot g(\hat\beta)'W^{-1}g(\hat\beta), \qquad g(\hat\beta)=\frac{1}{n}Z'e, \qquad J\sim\chi^2_{h-k}$$

Dưới homoskedasticity, Sargan và Hansen J **trùng nhau về mặt lý thuyết**.
<br><span class="en">Under homoskedasticity, Sargan and Hansen J **coincide theoretically**.</span>

**Ví dụ số** (instrument `fatheredu`, `motheredu` cho `schooling`, $h=2>k=1$):
<br><span class="en">**Numerical example** (instruments `fatheredu`, `motheredu` for `schooling`, $h=2>k=1$):</span>

- Sargan statistic $=0.36$, p-value $=0.551$ (tính với vcov = "iid") → **không bác bỏ** $H_0$ → không có bằng chứng chống lại tính hợp lệ đồng thời của các instrument.
<br><span class="en">Sargan statistic $=0.36$, p-value $=0.551$ (computed with vcov = "iid") → **fail to reject** $H_0$ → no evidence against the joint validity of the instruments.</span>
- Hansen's J test: p-value $=0.541$ (tính với vcov = "robust") → cũng **không bác bỏ** $H_0$, kết luận tương tự.
<br><span class="en">Hansen's J test: p-value $=0.541$ (computed with vcov = "robust") → also **fails to reject** $H_0$, same conclusion.</span>

> **Ghi chú về nguồn**: dù lý thuyết nói Sargan và Hansen J "coincide" (trùng nhau) dưới homoskedasticity, ví dụ số của slides-16 cho ra hai p-value **hơi khác nhau** ($0.551$ vs $0.541$) — không phải mâu thuẫn nghiêm trọng, nhiều khả năng phản ánh việc dữ liệu thực tế không hoàn toàn homoskedastic tuyệt đối (Sargan dùng vcov "iid", Hansen dùng vcov "robust", nên với dữ liệu có chút heteroskedasticity, hai con số gần nhau nhưng không **hoàn toàn** trùng khớp). Ghi chú lại vì đây là điểm dễ khiến người học tưởng nhầm là phải ra **cùng một số tuyệt đối**.
> <br><span class="en">**Source note**: although theory says Sargan and Hansen J "coincide" under homoskedasticity, slides-16's numerical example produces two **slightly different** p-values ($0.551$ vs $0.541$) — not a serious contradiction, most likely reflecting that the real data is not perfectly homoskedastic (Sargan uses vcov "iid", Hansen uses vcov "robust", so with data that has a bit of heteroskedasticity, the two numbers are close but not **exactly** identical). Noted here because this is a point where learners easily mistake it for requiring **the exact same number**.</span>

**Diễn giải quan trọng nhất — bẫy thi hay gặp**: **không bác bỏ Sargan/Hansen KHÔNG chứng minh được** instrument hợp lệ — nó chỉ có nghĩa là "không tìm thấy bằng chứng chống lại tính hợp lệ đồng thời". Validity luôn phải được **biện luận bằng thiết kế nghiên cứu**: trong ví dụ này, phải lập luận rằng học vấn cha mẹ không có tác động trực tiếp nào lên lương của người con, và không tương quan với bất kỳ yếu tố không quan sát được nào khác trong hàm lương — con đường duy nhất để tác động đến lương là thông qua `schooling` của chính người con.
<br><span class="en">**Most important interpretation — a common exam trap**: failing to reject Sargan/Hansen **does NOT prove** the instruments are valid — it only means "no evidence found against joint validity." Validity must always be **argued through research design**: in this example, one must argue that parents' education has no direct effect on the child's wage, and is not correlated with any other unobserved factor in the wage function — the only path to affect wages is through the child's own `schooling`.</span>

**Cảnh báo bổ sung**: càng nhiều instrument (proliferation), khả năng ít nhất một cái không hợp lệ càng cao. Chỉ nên kiểm định overidentifying restrictions **sau khi** đã xác nhận instrument không yếu — instrument yếu làm méo cả kích thước (size) lẫn sức mạnh (power) của kiểm định Sargan/Hansen.
<br><span class="en">**Additional warning**: the more instruments (proliferation), the higher the chance at least one is invalid. Overidentifying restrictions should only be tested **after** confirming the instrument is not weak — a weak instrument distorts both the size and the power of the Sargan/Hansen test.</span>

### 6.3 Kiểm định endogeneity: Wu-Hausman test - <span class="en">Testing endogeneity: the Wu-Hausman test</span>

**Ý tưởng trực quan**: nếu biến nghi ngờ $X_2$ thực ra **không** nội sinh, và instrument đủ mạnh, thì OLS và 2SLS đều là ước lượng consistent — chúng sẽ **hội tụ tiệm cận về cùng một giá trị**. Nhưng nếu $X_2$ **thực sự** nội sinh, OLS bị chệch/inconsistent trong khi 2SLS vẫn consistent → hai ước lượng sẽ **phân kỳ có hệ thống**, không chỉ khác nhau do nhiễu ngẫu nhiên của mẫu. Wu-Hausman test chính là phép so sánh có hệ thống hai ước lượng này.
<br><span class="en">**Intuition**: if the suspected variable $X_2$ is actually **not** endogenous, and the instrument is strong enough, then both OLS and 2SLS are consistent estimators — they will **converge asymptotically to the same value**. But if $X_2$ **is truly** endogenous, OLS is biased/inconsistent while 2SLS remains consistent → the two estimates will **diverge systematically**, not merely differ due to random sampling noise. The Wu-Hausman test is precisely a systematic comparison of these two estimates.</span>

$$H_0: X_2 \text{ exogenous} \;(\hat\beta_{OLS}=\hat\beta_{2SLS}, \text{cả hai đều consistent}), \qquad H_a: X_2 \text{ endogenous}$$
<br><span class="en">$$H_0: X_2 \text{ exogenous} \;(\hat\beta_{OLS}=\hat\beta_{2SLS}, \text{both consistent}), \qquad H_a: X_2 \text{ endogenous}$$</span>

$$\text{Statistic: } (\hat\beta_{2SLS}-\hat\beta_{OLS})'\big[V_{2SLS}-V_{OLS}\big]^{-1}(\hat\beta_{2SLS}-\hat\beta_{OLS}) \sim \chi^2_k$$

với $k$ = số biến nghi ngờ nội sinh.
<br><span class="en">with $k$ = number of suspected endogenous variables.</span>

- p-value lớn → không bác bỏ $H_0$ → không có bằng chứng endogeneity → OLS vẫn consistent (và **hiệu quả hơn** 2SLS dưới homoskedasticity — nên ưu tiên dùng OLS nếu không có bằng chứng nội sinh).
<br><span class="en">Large p-value → fail to reject $H_0$ → no evidence of endogeneity → OLS remains consistent (and **more efficient** than 2SLS under homoskedasticity — so OLS should be preferred if there is no evidence of endogeneity).</span>
- p-value nhỏ → bác bỏ $H_0$ → $X_2$ nội sinh → OLS chệch, dùng 2SLS.
<br><span class="en">Small p-value → reject $H_0$ → $X_2$ is endogenous → OLS is biased, use 2SLS.</span>

**Ví dụ số — và hai điểm cần lưu ý về nguồn**:
<br><span class="en">**Numerical example — and two source points to note**:</span>

- `slides-5-iu.pdf`: Wu-Hausman statistic $=3.63$. Ở $\alpha=10\%$: p-value $=0.057<0.1$ → bác bỏ $H_0$ → có bằng chứng `schooling` nội sinh. Ở $\alpha=5\%$: cùng p-value $=0.057>0.05$ → không bác bỏ $H_0$ → không có bằng chứng nội sinh.
<br><span class="en">`slides-5-iu.pdf`: Wu-Hausman statistic $=3.63$. At $\alpha=10\%$: p-value $=0.057<0.1$ → reject $H_0$ → evidence `schooling` is endogenous. At $\alpha=5\%$: the same p-value $=0.057>0.05$ → fail to reject $H_0$ → no evidence of endogeneity.</span>
- `slides-16-iu.pdf`: Wu-Hausman statistic tính lại $=3.8$ (dùng `ivreg2r::ivreg2()` với robust VCV). Ở $\alpha=10\%$: p-value $=0.0512<0.1$ → bác bỏ $H_0$. Ở $\alpha=5\%$: p-value $=0.057>0.05$ → không bác bỏ $H_0$.
<br><span class="en">`slides-16-iu.pdf`: Wu-Hausman statistic recomputed $=3.8$ (using `ivreg2r::ivreg2()` with robust VCV). At $\alpha=10\%$: p-value $=0.0512<0.1$ → reject $H_0$. At $\alpha=5\%$: p-value $=0.057>0.05$ → fail to reject $H_0$.</span>

Cả hai bản đều đi đến cùng một kết luận diễn giải: **`schooling` "nội sinh ở mức 10% nhưng không ở mức 5%"** — một ví dụ điển hình cho việc kết luận kiểm định phụ thuộc vào mức ý nghĩa $\alpha$ đã chọn trước, và giá trị statistic phụ thuộc vào loại VCV được dùng (bản thân slides-16 ghi chú rõ: "Wu-Hausman test depends on VCV").
<br><span class="en">Both versions arrive at the same interpretive conclusion: **`schooling` is "endogenous at the 10% level but not at the 5% level"** — a textbook example of how a test's conclusion depends on the pre-chosen significance level $\alpha$, and how the statistic's value depends on the type of VCV used (slides-16 itself notes explicitly: "Wu-Hausman test depends on VCV").</span>

> **Ghi chú mâu thuẫn nguồn — quan trọng, chưa được ghi trong bản trước của trang này**: khác biệt statistic $3.63$ (slides-5) so với $3.8$ (slides-16) là một "methodological nuance" hợp lý — do khác lựa chọn VCV, đúng như log.md đã ghi nhận, **không phải lỗi**. Nhưng bên trong chính `slides-16-iu.pdf`, có một điểm **bất nhất nội tại**: cùng một statistic $3.8$ được báo cáo với **hai p-value khác nhau** ở hai gạch đầu dòng liền kề — $p=0.0512$ khi so với $\alpha=10\%$, nhưng $p=0.057$ khi so với $\alpha=5\%$. Về mặt logic, **một statistic chỉ có đúng một p-value** — chỉ có ngưỡng $\alpha$ đem ra so sánh mới thay đổi, p-value phải giữ nguyên. Con số $0.057$ trùng khớp chính xác với p-value của bản slides-5 (ứng với statistic $3.63$, không phải $3.8$) — nhiều khả năng đây là một chỗ **slides-16 cập nhật giá trị statistic nhưng quên cập nhật p-value ở gạch đầu dòng thứ hai**, còn sót lại từ bản slides-5. Ghi chú lại đây theo đúng nguyên tắc của wiki, không tự ý chọn một trong hai con số để "sửa" cho khớp.
> <br><span class="en">**Source discrepancy note — important, not previously recorded in earlier versions of this page**: the difference between statistic $3.63$ (slides-5) and $3.8$ (slides-16) is a reasonable "methodological nuance" — due to a different VCV choice, exactly as log.md already records, **not an error**. But within `slides-16-iu.pdf` itself, there is an **internal inconsistency**: the same statistic $3.8$ is reported with **two different p-values** on two adjacent bullet points — $p=0.0512$ when compared against $\alpha=10\%$, but $p=0.057$ when compared against $\alpha=5\%$. Logically, **a single statistic has exactly one p-value** — only the $\alpha$ threshold being compared against should change, the p-value must stay the same. The number $0.057$ matches exactly the p-value from slides-5 (corresponding to statistic $3.63$, not $3.8$) — most likely this is a spot where **slides-16 updated the statistic value but forgot to update the p-value on the second bullet**, leaving it over from the slides-5 version. Noted here per the wiki's own principle, without arbitrarily picking one of the two numbers to "fix" to match.</span>

## 7. Các ước lượng thay thế khi 2SLS không đủ tốt (graduate level) - <span class="en">Alternative estimators when 2SLS is not good enough (graduate level)</span>

Anderson-Rubin/Stock-Wright (mục 6.1) cho suy luận hợp lệ dưới instrument yếu, nhưng **không cải thiện bản thân điểm ước lượng** — 2SLS vẫn có thể bất ổn/chệch. Câu hỏi tiếp theo: có ước lượng nào **tốt hơn** 2SLS khi instrument yếu hoặc nhiều instrument không?
<br><span class="en">Anderson-Rubin/Stock-Wright (section 6.1) give valid inference under weak instruments, but **do not improve the point estimate itself** — 2SLS can still be unstable/biased. The next question: is there an estimator **better** than 2SLS when instruments are weak or numerous?</span>

### 7.1 κ-class estimator và LIML - <span class="en">The κ-class estimator and LIML</span>

Cả 2SLS lẫn OLS đều là trường hợp riêng của một họ ước lượng tổng quát hơn — **κ-class estimator**:
<br><span class="en">Both 2SLS and OLS are special cases of a more general family of estimators — the **κ-class estimator**:</span>

$$b(\kappa)=\big[X'(I-\kappa M_Z)X\big]^{-1}X'(I-\kappa M_Z)y, \qquad M_Z=I-Z(Z'Z)^{-1}Z'$$

- $\kappa=0$ → chính là OLS.
<br><span class="en">$\kappa=0$ → exactly OLS.</span>
- $\kappa=1$ → chính là 2SLS.
<br><span class="en">$\kappa=1$ → exactly 2SLS.</span>

**LIML (Limited Information Maximum Likelihood)** chọn $\kappa$ **tối ưu** theo phương pháp hợp lý cực đại (maximum likelihood) — cụ thể là giá trị riêng nhỏ nhất (minimum eigenvalue) của một ma trận tỷ lệ $B^{-1}A$, xây dựng từ phần dư sau khi chiếu lên $Z$ (cho ma trận $A$) và sau khi chiếu lên $X$ (cho ma trận $B$).
<br><span class="en">**LIML (Limited Information Maximum Likelihood)** chooses $\kappa$ **optimally** via maximum likelihood — specifically the minimum eigenvalue of a ratio matrix $B^{-1}A$, constructed from the residuals after projecting onto $Z$ (for matrix $A$) and after projecting onto $X$ (for matrix $B$).</span>

> **Ghi chú kỹ thuật về nguồn**: công thức chính xác của ma trận $A$, $B$ trong slide gốc bị lỗi hiển thị khi trích xuất bằng `pdftotext` (một số ký hiệu ma trận nhúng dạng hình ảnh bị mất/lẫn lộn ở cả hai bản slide-5 và slide-16) — phần cốt lõi về mặt khái niệm (LIML giải một bài toán trị riêng để chọn $\kappa$ tối ưu, nối liền OLS và 2SLS) vẫn rõ ràng và nhất quán giữa hai nguồn, nên được trình bày đầy đủ ở đây; chi tiết ma trận $A,B$ không trình bày lại để tránh suy diễn ngoài những gì đọc được chắc chắn từ nguồn.
> <br><span class="en">**Technical source note**: the exact formulas for matrices $A$, $B$ in the original slide were corrupted during `pdftotext` extraction (some image-embedded matrix notation was lost/garbled in both slide-5 and slide-16) — the core conceptual content (LIML solves an eigenvalue problem to choose the optimal $\kappa$, bridging OLS and 2SLS) remains clear and consistent across both sources, so it is presented in full here; the details of matrices $A,B$ are not reproduced, to avoid inferring beyond what can be read with confidence from the source.</span>

**Trực giác**: "full model" (ước lượng bỏ qua vấn đề endogeneity) chính là OLS ($\kappa=0$); "projected model" (sau khi chiếu regressor lên instrument) chính là 2SLS ($\kappa=1$). LIML kết hợp cả hai, chọn điểm $\kappa$ tối ưu ở giữa theo likelihood.
<br><span class="en">**Intuition**: the "full model" (an estimate ignoring the endogeneity problem) is exactly OLS ($\kappa=0$); the "projected model" (after projecting the regressor onto the instrument) is exactly 2SLS ($\kappa=1$). LIML combines both, choosing the optimal $\kappa$ somewhere in between according to likelihood.</span>

**Vì sao LIML ít nhạy với weak instrument hơn 2SLS?**
<br><span class="en">**Why is LIML less sensitive to weak instruments than 2SLS?**</span>

- 2SLS là κ-class với $\kappa=1$ — nó **thay hoàn toàn** $X_2$ bằng $\hat X_2=P_ZX_2$. Nếu instrument yếu, $\hat X_2$ là một "đại diện" (proxy) rất nhiễu cho $X_2$ thật, và nhiễu hình chiếu này đẩy 2SLS lệch khỏi tham số thật — như đã phân tích trực quan ở mục 6.1, "liều thuốc có thể tệ hơn bệnh".
<br><span class="en">2SLS is the κ-class with $\kappa=1$ — it **completely replaces** $X_2$ with $\hat X_2=P_ZX_2$. If the instrument is weak, $\hat X_2$ is a very noisy "proxy" for the true $X_2$, and this projection noise pushes 2SLS away from the true parameter — as analyzed intuitively in section 6.1, "the cure can be worse than the disease."</span>
- LIML chọn $\kappa$ tối ưu theo dữ liệu: với instrument **mạnh**, $\kappa\approx1$ → LIML $\approx$ 2SLS. Với instrument **yếu**, $\kappa$ thấp hơn 1 một cách đáng kể → LIML "kéo" ước lượng trở lại gần OLS hơn theo cách tối ưu, giảm bớt weak-IV bias.
<br><span class="en">LIML chooses $\kappa$ optimally based on the data: with a **strong** instrument, $\kappa\approx1$ → LIML $\approx$ 2SLS. With a **weak** instrument, $\kappa$ drops significantly below 1 → LIML optimally "pulls" the estimate back closer to OLS, reducing weak-IV bias.</span>
- Đánh đổi: LIML **hy sinh một phần hiệu quả (efficiency)** để đổi lấy tính ổn định (robustness) trước instrument yếu.
<br><span class="en">Trade-off: LIML **sacrifices some efficiency** in exchange for robustness against weak instruments.</span>
- **Lưu ý quan trọng**: LIML ít nhạy với weak-IV bias hơn, nhưng **không phải là bảo chứng cho tính consistent** — nếu instrument thực sự không valid (không chỉ yếu), LIML cũng không cứu được.
<br><span class="en">**Important note**: LIML is less sensitive to weak-IV bias, but **is not a guarantee of consistency** — if the instrument is truly invalid (not merely weak), LIML cannot rescue it either.</span>

### 7.2 Fuller-adjusted LIML - <span class="en">Fuller-adjusted LIML</span>

Vấn đề còn lại: LIML tuy ít bias hơn 2SLS dưới weak instrument, nhưng vẫn có thể có **phương sai lớn và vấn đề mẫu nhỏ (small-sample problems)** đáng kể. Fuller (1977) đề xuất một hiệu chỉnh đơn giản để giảm bias hơn nữa mà vẫn giữ tính chất phương sai tốt.
<br><span class="en">Remaining problem: although LIML has less bias than 2SLS under weak instruments, it can still have **large variance and notable small-sample problems**. Fuller (1977) proposes a simple adjustment to reduce bias further while preserving good variance properties.</span>

Thay vì dùng $\kappa$ do LIML chọn trực tiếp, Fuller đề xuất:
<br><span class="en">Instead of using $\kappa$ chosen directly by LIML, Fuller proposes:</span>

$$\kappa_F = \kappa - \frac{a}{n-k} \qquad \text{(công thức trong } \texttt{slides-5-iu.pdf}\text{)}$$
<br><span class="en">$$\kappa_F = \kappa - \frac{a}{n-k} \qquad \text{(formula in } \texttt{slides-5-iu.pdf}\text{)}$$</span>

với $n$ = cỡ mẫu, $k$ = số regressor (endo + exo), $a$ = hằng số dương, thường chọn $a=1$ hoặc $a=4$.
<br><span class="en">with $n$ = sample size, $k$ = number of regressors (endo + exo), $a$ = a positive constant, typically chosen as $a=1$ or $a=4$.</span>

> **Ghi chú mâu thuẫn nguồn — công thức hiệu chỉnh Fuller khác nhau giữa hai bản**: `slides-16-iu.pdf` (bản mở rộng/canonical) đưa ra một công thức **mẫu số khác**:
> <br><span class="en">**Source discrepancy note — the Fuller adjustment formula differs between the two versions**: `slides-16-iu.pdf` (the extended/canonical version) gives a formula with a **different denominator**:</span>
> $$\kappa_F = \kappa - \frac{a}{n-l+k-1}$$
> với $l$ = tổng số instrument (included + excluded), $k$ vẫn là số regressor (endo + exo), $a$ vẫn chọn $1$ hoặc $4$. Đây là hai công thức **khác nhau về mặt đại số** (mẫu số $n-k$ so với $n-l+k-1$), không chỉ là cách viết lại tương đương — không rõ đây là một sai sót đánh máy ở một trong hai bản, hay slides-16 cố ý tinh chỉnh công thức cho tổng quát hơn (cách viết $n-l+k-1$ xuất hiện trong một số tài liệu tham khảo về Fuller estimator có tính đến tổng số instrument). Vì slides-16 là bản canonical/mở rộng, dùng công thức của slides-16 làm mặc định khi cần tính toán, nhưng ghi chú lại sự khác biệt này thay vì chọn một bản rồi im lặng bỏ qua bản kia.
> <br><span class="en">with $l$ = total number of instruments (included + excluded), $k$ still the number of regressors (endo + exo), $a$ still chosen as $1$ or $4$. These are two **algebraically different** formulas (denominator $n-k$ versus $n-l+k-1$), not merely equivalent rewritings — it is unclear whether this is a typo in one of the two versions, or slides-16 deliberately refines the formula to be more general (the $n-l+k-1$ form appears in some reference literature on the Fuller estimator that accounts for the total instrument count). Since slides-16 is the canonical/extended version, its formula is used as the default for computation, but this discrepancy is noted rather than silently picking one version and dropping the other.</span>

**Ước lượng Fuller**: $\hat\beta_F=b(\kappa_F)$.
<br><span class="en">**Fuller estimator**: $\hat\beta_F=b(\kappa_F)$.</span>

**Tính chất** (theo slide, áp dụng cho cả hai công thức):
<br><span class="en">**Properties** (per the slide, applying to both formulas):</span>

| Thuộc tính | Nhận xét |
|---|---|
| Bias | Giảm mạnh so với weak-IV bias của cả LIML và 2SLS |
| Variance | Tương tự LIML, thường cao hơn 2SLS |
| Consistency | Consistent nếu instrument valid và relevant |
| Efficiency | Không hiệu quả tiệm cận tuyệt đối, nhưng trong thực hành thường **vượt trội** nhờ tính chất mẫu nhỏ tốt hơn |

<span class="en">

| Property | Remark |
|---|---|
| Bias | Substantially reduced compared to the weak-IV bias of both LIML and 2SLS |
| Variance | Similar to LIML, usually higher than 2SLS |
| Consistency | Consistent if the instrument is valid and relevant |
| Efficiency | Not asymptotically efficient in the absolute sense, but in practice often **outperforms** thanks to better small-sample properties |

</span>

Chọn $a$: $a=1$ cho phương sai thấp hơn nhưng bias cao hơn một chút; $a=4$ giảm bias mạnh hơn, thường được coi là lựa chọn an toàn trong thực hành. Các nhà kinh tế lượng thường khuyến nghị Fuller đúng trong những trường hợp weak IV là mối lo ngại thực sự.
<br><span class="en">Choosing $a$: $a=1$ gives lower variance but slightly higher bias; $a=4$ reduces bias more strongly and is usually considered the safer practical choice. Econometricians typically recommend Fuller specifically in cases where weak IV is a genuine concern.</span>

### 7.3 GMM (Generalized Method of Moments) - <span class="en">GMM (Generalized Method of Moments)</span>

**Khung tổng quát**: GMM xuất phát từ điều kiện moment $E[m(\theta,d_i)]=0$. Sample moment: $g(\theta)=\frac{1}{n}\sum_i m(\theta,d_i)$. Ước lượng $\hat\theta=\arg\min_\theta J(\theta)$ với hàm tiêu chí (criterion function):
<br><span class="en">**General framework**: GMM starts from the moment condition $E[m(\theta,d_i)]=0$. Sample moment: $g(\theta)=\frac{1}{n}\sum_i m(\theta,d_i)$. Estimate $\hat\theta=\arg\min_\theta J(\theta)$ with criterion function:</span>

$$J(\theta)=n\cdot g(\theta)'Wg(\theta)$$

$W$ là ma trận trọng số (weighting matrix): $W=I$ → GMM đơn giản; $W=S^{-1}$ (với $S=E[m(\theta,d_i)m(\theta,d_i)']$) → **efficient GMM**.
<br><span class="en">$W$ is the weighting matrix: $W=I$ → simple GMM; $W=S^{-1}$ (with $S=E[m(\theta,d_i)m(\theta,d_i)']$) → **efficient GMM**.</span>

**OLS/GLS/2SLS đều là trường hợp đặc biệt của GMM**:
<br><span class="en">**OLS/GLS/2SLS are all special cases of GMM**:</span>

- Hồi quy tuyến tính thường: $m(\beta,d_i)=y_i-\beta X_i=e_i$ → $J(\beta)=e'We$ chính là RSS (tổng bình phương phần dư) khi $W=I$. $W=I$ → trùng **OLS**; $W=S^{-1}$ → trùng **GLS**.
<br><span class="en">Ordinary linear regression: $m(\beta,d_i)=y_i-\beta X_i=e_i$ → $J(\beta)=e'We$ is exactly the RSS (residual sum of squares) when $W=I$. $W=I$ → coincides with **OLS**; $W=S^{-1}$ → coincides with **GLS**.</span>
- IV: $m(\theta,d_i)=Z_i(y_i-\beta X_i)=Z_ie_i$ → $g(\beta)=\frac1n\sum Z_ie_i$. $W=(Z'Z)^{-1}$ → trùng **2SLS**; $W=S^{-1}$ → **efficient IV-GMM**, với $S=E[Z_ie_ie_i'Z_i]=E[e_i^2Z_iZ_i]$, ước lượng mẫu $\hat S=\frac1n Z'\,\text{diag}(e^2)\,Z$.
<br><span class="en">IV: $m(\theta,d_i)=Z_i(y_i-\beta X_i)=Z_ie_i$ → $g(\beta)=\frac1n\sum Z_ie_i$. $W=(Z'Z)^{-1}$ → coincides with **2SLS**; $W=S^{-1}$ → **efficient IV-GMM**, with $S=E[Z_ie_ie_i'Z_i]=E[e_i^2Z_iZ_i]$, sample estimate $\hat S=\frac1n Z'\,\text{diag}(e^2)\,Z$.</span>

**Vai trò của cấu trúc sai số**:
<br><span class="en">**Role of the error structure**:</span>

- Dưới **homoskedasticity** ($E(e_i^2|Z_i)=\sigma^2$): $S=\sigma^2Z_iZ_i'$, $\hat S=\sigma^2Z'Z$, $W=S^{-1}=(Z'Z)^{-1}$ → **efficient GMM thu gọn về đúng 2SLS**.
<br><span class="en">Under **homoskedasticity** ($E(e_i^2|Z_i)=\sigma^2$): $S=\sigma^2Z_iZ_i'$, $\hat S=\sigma^2Z'Z$, $W=S^{-1}=(Z'Z)^{-1}$ → **efficient GMM collapses exactly to 2SLS**.</span>
- Dưới **heteroskedasticity** ($E(e_i^2|Z_i)=\sigma_i^2$): $\hat S=Z'\Sigma Z$ với $\Sigma=\text{diag}(e^2)$ → **2SLS không còn hiệu quả**. GMM hiệu quả hơn vì gán **trọng số thấp hơn** cho những quan sát có phương sai sai số lớn (đúng nguyên tắc GLS: tin ít hơn vào quan sát "ồn" hơn).
<br><span class="en">Under **heteroskedasticity** ($E(e_i^2|Z_i)=\sigma_i^2$): $\hat S=Z'\Sigma Z$ with $\Sigma=\text{diag}(e^2)$ → **2SLS is no longer efficient**. GMM is more efficient because it assigns **lower weight** to observations with larger error variance (the same GLS principle: trust "noisier" observations less).</span>

**Ba biến thể GMM, khác nhau ở cách chọn/cập nhật $W$**:
<br><span class="en">**Three GMM variants, differing in how $W$ is chosen/updated**:</span>

1. **Two-step GMM**: Bước 1 — chọn $W_0=(Z'Z)^{-1}$ (như 2SLS), ước lượng $\beta_{2SLS}$, tính $e$ để ước lượng $S$ và $W=S^{-1}$. Bước 2 — ước lượng lại với $W$ vừa tính: $\beta_{GMM,2s}=[X'ZWZ'X]^{-1}X'ZWZ'y$. Dưới homoskedasticity (hoặc bỏ qua hetero), $\beta_{GMM,2s}=\beta_{2SLS}$ y hệt; dưới heteroskedasticity, hiệu quả hơn nhờ down-weight quan sát phương sai lớn, nhưng SE ở bước ước lượng ban đầu (nếu bỏ qua hetero) bị chệch.
<br><span class="en">**Two-step GMM**: Step 1 — choose $W_0=(Z'Z)^{-1}$ (as in 2SLS), estimate $\beta_{2SLS}$, compute $e$ to estimate $S$ and $W=S^{-1}$. Step 2 — re-estimate with the newly computed $W$: $\beta_{GMM,2s}=[X'ZWZ'X]^{-1}X'ZWZ'y$. Under homoskedasticity (or ignoring hetero), $\beta_{GMM,2s}=\beta_{2SLS}$ exactly; under heteroskedasticity, it's more efficient thanks to down-weighting high-variance observations, but the SE at the initial estimation step (if hetero is ignored) is biased.</span>
2. **Iterative GMM**: thay vì dừng sau 2 bước, lặp lại chu trình cập nhật $W$ → ước lượng lại → cập nhật $W$... cho đến khi hội tụ. Cải thiện tính ổn định và hiệu quả so với two-step.
<br><span class="en">**Iterative GMM**: instead of stopping after 2 steps, repeat the cycle of updating $W$ → re-estimating → updating $W$... until convergence. Improves stability and efficiency compared to two-step.</span>
3. **Continuously Updated Estimator (CUE)**: ước lượng đồng thời $\beta$ và $W(\beta)$ trong **một** bài toán tối ưu duy nhất, thay vì luân phiên như hai biến thể trên: $\hat\theta=\arg\min_\theta g(\theta)'\hat S(\beta)^{-1}g(\theta)$. Ở mẫu lớn, CUE đạt hiệu quả ngang GMM tối ưu; ở mẫu nhỏ, đôi khi **vượt trội** hơn two-step.
<br><span class="en">**Continuously Updated Estimator (CUE)**: estimates $\beta$ and $W(\beta)$ simultaneously in **one single** optimization problem, instead of alternating as in the two variants above: $\hat\theta=\arg\min_\theta g(\theta)'\hat S(\beta)^{-1}g(\theta)$. In large samples, CUE achieves efficiency on par with optimal GMM; in small samples, it can sometimes **outperform** two-step.</span>

### 7.4 Bảng so sánh các ước lượng - <span class="en">Estimator comparison table</span>

| Ước lượng | Tiệm cận (asymptotics) | Mẫu hữu hạn (finite sample) | Robustness | Kết luận thực hành |
|---|---|---|---|---|
| **2SLS** | Consistent nếu instrument valid; hiệu quả dưới homoskedasticity + just-identified | Nhạy với weak IV | Không robust hetero trừ khi hiệu chỉnh | Workhorse — dễ dùng, dạng đóng, nhưng dễ "vỡ" khi IV yếu |
| **LIML** | Tiệm cận tương đương 2SLS dưới IV mạnh | Ít chệch hơn 2SLS khi IV yếu | Giới hạn robustness giống 2SLS | Tính chất mẫu nhỏ tốt hơn 2SLS; ổn định hơn khi có nhiều IV |
| **Fuller** | Cùng giới hạn tiệm cận với LIML | Giảm bias hơn nữa so với LIML | Cùng khung với LIML (linear IV) | Thường là lựa chọn tốt nhất khi IV yếu hoặc nhiều |
| **Efficient GMM** | Hiệu quả tiệm cận nhất | Kế thừa weak-IV bias giống 2SLS | Robust hetero, xử lý được nhiều moment condition | Ưu tiên khi IV mạnh + có heteroskedasticity; bất ổn khi IV nhiều/yếu |

<span class="en">

| Estimator | Asymptotics | Finite sample | Robustness | Practical takeaway |
|---|---|---|---|---|
| **2SLS** | Consistent if instrument valid; efficient under homoskedasticity + just-identified | Sensitive to weak IV | Not robust to hetero unless corrected | Workhorse — easy to use, closed form, but easily "breaks" when IV is weak |
| **LIML** | Asymptotically equivalent to 2SLS under strong IV | Less biased than 2SLS when IV is weak | Same robustness limits as 2SLS | Better small-sample properties than 2SLS; more stable with many IVs |
| **Fuller** | Same asymptotic limit as LIML | Reduces bias further compared to LIML | Same framework as LIML (linear IV) | Often the best choice when IV is weak or numerous |
| **Efficient GMM** | Most asymptotically efficient | Inherits weak-IV bias similar to 2SLS | Robust to hetero, handles many moment conditions | Preferred when IV is strong + heteroskedasticity present; unstable when IV is numerous/weak |

</span>

## 8. Bẫy thi (exam traps) — mở rộng - <span class="en">Exam traps — extended</span>

1. Gọi hệ quả của endogeneity lên OLS là "biased" một cách chung chung — chính xác hơn là **inconsistent** (thuật ngữ slides-16 sửa lại so với slides-5); bias là vấn đề mẫu hữu hạn, inconsistency là vấn đề không biến mất dù $N\to\infty$.
<br><span class="en">Calling the consequence of endogeneity on OLS "biased" in a generic way — the precise term is **inconsistent** (the terminology slides-16 corrects from slides-5); bias is a finite-sample problem, inconsistency is a problem that does not vanish no matter $N\to\infty$.</span>
2. Bác bỏ được test underidentification (relevance) rồi kết luận luôn "instrument đủ mạnh" — đây là **hai kiểm định khác nhau**: relevance (tầng 1) và strength/weak-instrument test (tầng 2).
<br><span class="en">Rejecting the underidentification (relevance) test and then concluding right away "the instrument is strong enough" — these are **two different tests**: relevance (tier 1) and the strength/weak-instrument test (tier 2).</span>
3. Bác bỏ underidentification/weak-instrument rồi coi 2SLS "chắc chắn cho suy luận đúng" — Anderson-Rubin/Stock-Wright chỉ cần thiết cho vùng biên, nhưng nguyên tắc chung là instrument càng gần biên yếu, càng nên nghi ngờ t-test chuẩn.
<br><span class="en">Rejecting underidentification/weak-instrument and then treating 2SLS as "certainly giving correct inference" — Anderson-Rubin/Stock-Wright are only strictly necessary in the borderline zone, but the general principle is: the closer the instrument is to the weak boundary, the more the standard t-test should be doubted.</span>
4. Nhầm 2 tiêu chí chọn ngưỡng Stock-Yogo (**relative bias** vs **size distortion**) — instrument có thể đạt tiêu chí này nhưng không đạt tiêu chí kia; "một ước lượng tốt không đảm bảo một kiểm định tốt, và ngược lại".
<br><span class="en">Confusing the 2 criteria for choosing a Stock-Yogo threshold (**relative bias** vs **size distortion**) — an instrument can meet one criterion but not the other; "a good estimate does not guarantee a good test, and vice versa."</span>
5. Không bác bỏ Sargan/Hansen J rồi coi là "đã chứng minh instrument hợp lệ" — chỉ là "không tìm thấy bằng chứng chống lại", validity **luôn** phải biện luận bằng thiết kế nghiên cứu, không bao giờ chỉ bằng con số kiểm định.
<br><span class="en">Failing to reject Sargan/Hansen J and then treating it as "proof the instrument is valid" — it only means "no evidence found against it"; validity **always** has to be argued through research design, never by the test statistic alone.</span>
6. Kiểm định overidentifying restrictions khi mô hình **just-identified** ($h=k$) — về mặt cấu trúc $Z'e=0$ luôn đúng, "không có gì để kiểm định"; **không được** hiểu just-identified là "instrument tự động valid" — chỉ là validity không kiểm định được bằng dữ liệu trong trường hợp này.
<br><span class="en">Testing overidentifying restrictions when the model is **just-identified** ($h=k$) — structurally $Z'e=0$ always holds, "there is nothing to test"; just-identified must **not** be read as "the instrument is automatically valid" — it only means validity cannot be tested with data in this case.</span>
7. Quên rằng kết luận Wu-Hausman (và giá trị thống kê) phụ thuộc vào mức ý nghĩa $\alpha$ **và** loại VCV sử dụng — cùng một bộ dữ liệu có thể cho kết luận khác nhau tùy $\alpha$ chọn trước (ví dụ: nội sinh ở 10% nhưng không ở 5%).
<br><span class="en">Forgetting that the Wu-Hausman conclusion (and statistic value) depends on the chosen significance level $\alpha$ **and** the type of VCV used — the same dataset can yield different conclusions depending on the pre-chosen $\alpha$ (e.g. endogenous at 10% but not at 5%).</span>
8. Coi Anderson-Rubin/Stock-Wright có ý nghĩa thống kê là bằng chứng "instrument mạnh" hoặc "cải thiện điểm ước lượng" — chúng chỉ cho **suy luận hợp lệ** dưới instrument yếu, không cải thiện bản thân 2SLS estimate, và chỉ hợp lệ nếu instrument thực sự exogenous.
<br><span class="en">Treating a statistically significant Anderson-Rubin/Stock-Wright result as evidence the "instrument is strong" or that it "improves the point estimate" — they only provide **valid inference** under weak instruments, they do not improve the 2SLS estimate itself, and they are only valid if the instrument is truly exogenous.</span>
9. Nhầm exogeneity và exclusion là hai điều kiện độc lập cần chứng minh riêng biệt — về mặt toán học exogeneity đã bao hàm exclusion; tách riêng chỉ để nhấn mạnh rủi ro thực tế (đường tác động trực tiếp từ instrument đến $y$ mà nhà nghiên cứu bỏ sót).
<br><span class="en">Mistaking exogeneity and exclusion for two independent conditions that must each be proven separately — mathematically exogeneity already implies exclusion; they are separated only to emphasize the practical risk (a direct path from the instrument to $y$ that the researcher overlooked).</span>
10. Coi LIML/Fuller "luôn luôn tốt hơn" 2SLS — thực chất là đánh đổi: giảm bias đổi lấy tăng variance; chỉ đáng cân nhắc khi thực sự lo ngại weak/many instruments, không phải lựa chọn mặc định cho mọi bài toán IV.
<br><span class="en">Treating LIML/Fuller as "always better" than 2SLS — it is actually a trade-off: reduced bias in exchange for increased variance; only worth considering when weak/many instruments are a genuine concern, not the default choice for every IV problem.</span>
11. Coi (efficient) GMM là "nâng cấp toàn diện" của 2SLS trong mọi tình huống — GMM chỉ hiệu quả hơn khi có heteroskedasticity; nó **kế thừa nguyên vẹn** vấn đề weak-IV bias giống 2SLS, và có thể bất ổn hơn khi instrument nhiều/yếu.
<br><span class="en">Treating (efficient) GMM as a "universal upgrade" over 2SLS in every situation — GMM is only more efficient when heteroskedasticity is present; it **inherits the weak-IV bias problem intact**, same as 2SLS, and can be even more unstable when instruments are numerous/weak.</span>
12. Nhầm lẫn "included instruments" ($X_1$ — biến ngoại sinh sẵn có trong mô hình) với "excluded instruments" ($IV$ — biến công cụ mới thêm vào) — $Z=[X_1, IV]$ là bộ công cụ **đầy đủ**, không phải chỉ riêng $IV$.
<br><span class="en">Confusing "included instruments" ($X_1$ — the exogenous variables already in the model) with "excluded instruments" ($IV$ — the newly added instrument variables) — $Z=[X_1, IV]$ is the **full** instrument set, not $IV$ alone.</span>

## 9. Kết nối với phần còn lại của khóa học - <span class="en">Connections to the rest of the course</span>

Đây là công cụ giải quyết vi phạm **A3 (exogeneity)** của [[concepts/linear-regression-model]] — hoàn thiện bộ ba giả định hay bị vi phạm nhất và cách vá: A2 (gần vi phạm) → [[concepts/multicollinearity]], A4 → [[concepts/heteroskedasticity]], A3 → endogeneity/IV ở chính trang này.
<br><span class="en">This is the toolkit for resolving the violation of **A3 (exogeneity)** of [[concepts/linear-regression-model]] — completing the trio of most-commonly-violated assumptions and their fixes: A2 (near-violation) → [[concepts/multicollinearity]], A4 → [[concepts/heteroskedasticity]], A3 → endogeneity/IV on this very page.</span>

- Khung **GMM** ở đây tái xuất hiện, mở rộng hơn nữa, ở [[concepts/dynamic-panel-data-models]] (Topic 14 — Arellano-Bond/Difference GMM và Arellano-Bover-Blundell-Bond/System GMM đều là ứng dụng cụ thể của khung GMM cho dữ liệu panel động).
<br><span class="en">The **GMM** framework here reappears, extended further, in [[concepts/dynamic-panel-data-models]] (Topic 14 — Arellano-Bond/Difference GMM and Arellano-Bover-Blundell-Bond/System GMM are both concrete applications of the GMM framework to dynamic panel data).</span>
- Toàn bộ bộ công cụ chẩn đoán ở đây (weak-instrument test, Sargan/Hansen, Wu-Hausman) được **tái sử dụng gần như nguyên vẹn**, chỉ thêm bước biến đổi loại bỏ hiệu ứng cố định ($\alpha_i$) trước khi áp dụng 2SLS/LIML/Fuller/GMM, ở [[concepts/iv-regression-panel-data]] (Topic 13 — IV regression cho panel data, dùng phép biến đổi FD hoặc FE trước khi đưa vào 2SLS).
<br><span class="en">The entire diagnostic toolkit here (weak-instrument test, Sargan/Hansen, Wu-Hausman) is **reused almost intact**, with only an added transformation step to remove the fixed effect ($\alpha_i$) before applying 2SLS/LIML/Fuller/GMM, in [[concepts/iv-regression-panel-data]] (Topic 13 — IV regression for panel data, using an FD or FE transformation before feeding into 2SLS).</span>
- Vấn đề **omitted variable** (mục 2.1) chính là sợi chỉ nối trực tiếp với [[concepts/econometrics-overview]] (identification problem, được giới thiệu từ Topic 0) — endogeneity chính là hình thức kỹ thuật hóa của câu hỏi "correlation có phải causation không" mà toàn khóa học xoay quanh.
<br><span class="en">The **omitted variable** issue (section 2.1) is the direct thread connecting to [[concepts/econometrics-overview]] (the identification problem, introduced back in Topic 0) — endogeneity is exactly the technical formalization of the question "is correlation causation?" that the entire course revolves around.</span>
- Kiểm định **Wu-Hausman** ở đây dùng chung logic so sánh "hai ước lượng, một consistent-dưới-mọi-điều-kiện và một chỉ-consistent-dưới-$H_0$" với kiểm định **Hausman test** ở [[concepts/fixed-random-effects-model]] (Topic 6/12, so sánh Fixed Effects vs Random Effects) — cùng tên người (Hausman), cùng ý tưởng nền tảng, khác bối cảnh áp dụng. Xem [[people/hausman]].
<br><span class="en">The **Wu-Hausman** test here shares the same comparison logic — "two estimators, one consistent-under-all-conditions and one consistent-only-under-$H_0$" — with the **Hausman test** in [[concepts/fixed-random-effects-model]] (Topic 6/12, comparing Fixed Effects vs Random Effects) — same namesake (Hausman), same underlying idea, different application context. See [[people/hausman]].</span>

## 15. Tài liệu tham khảo ứng dụng thực tế - <span class="en">Real-world application references</span>

Ba bài báo gần đây minh họa endogeneity và IV regression trong nghiên cứu kinh tế thực tế (đề cương Lecture 5):
<br><span class="en">Three recent papers illustrating endogeneity and IV regression in real-world economic research (Lecture 5 syllabus):</span>

- Gonzales, J. T. (2023). Implications of AI innovation on economic growth: A panel data study. *Journal of Economic Structures*, 12(1), 13. https://doi.org/10.1186/s40008-023-00307-w
- Acerenza, S., Gandelman, N., & Misail, D. (2025). Neighborhood impacts on human capital accumulation of adolescents and young adults in Montevideo. *Regional Science and Urban Economics*, 111, 104085. https://doi.org/10.1016/j.regsciurbeco.2025.104085
- Chen, Y., & Lyu, Y. (2025). Grandchild care and grandparents' labor supply. *Economic Modelling*, 143, 106936. https://doi.org/10.1016/j.econmod.2024.106936
