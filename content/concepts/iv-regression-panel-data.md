---
title: "Lecture 7: Instrumental Variable (IV) Regression for Panel Data"
type: concept
status: mature
tags: [panel-data, instrumental-variables, 2sls, gmm, endogeneity]
sources: ["[[sources/slides-14-iv-regression-panel-data]]"]
related: ["[[concepts/endogeneity-iv-regression]]", "[[concepts/fixed-random-effects-model]]", "[[concepts/dynamic-panel-data-models]]"]
lecture: 7
assignment: ["Assignment 6: Instrumental Variable Regression for Panel data"]
updated: 2026-09-04
---

> **Cách đọc trang này**: đây là trang **cầu nối** — không phải điểm khởi đầu.
> <br><span class="en">**How to read this page**: this is a **bridge** page — not a starting point.</span>
> Nếu chưa nắm 2SLS, LIML/Fuller, GMM, và bốn nhóm kiểm định chẩn đoán (underidentification, weak instrument, overidentification, Wu-Hausman) ở mức cross-section, hãy đọc [[concepts/endogeneity-iv-regression]] trước — trang đó là nền tảng, trang này **không giảng lại** khái niệm 2SLS là gì.
> <br><span class="en">If you haven't mastered 2SLS, LIML/Fuller, GMM, and the four groups of diagnostic tests (underidentification, weak instrument, overidentification, Wu-Hausman) at the cross-section level, read [[concepts/endogeneity-iv-regression]] first — that page is the foundation, and this page **does not re-teach** what 2SLS is.</span>
> Nếu chưa nắm FE/RE và bộ giả định A3a/A3b (tách từ A3 gốc), hãy đọc [[concepts/fixed-random-effects-model]] trước — trang này dùng lại đúng khung đó.
> <br><span class="en">If you haven't mastered FE/RE and the A3a/A3b assumption set (split from the original A3), read [[concepts/fixed-random-effects-model]] first — this page reuses that exact framework.</span>

**Lecture 7** trong đề cương (CO Topic 13) — Assignment 6: Instrumental Variable Regression for Panel data.
<br><span class="en">**Lecture 7** in the syllabus (CO Topic 13) — Assignment 6: Instrumental Variable Regression for Panel data.</span>
> Trang hiện tại chỉ tập trung vào **phần mở rộng riêng cho panel data**: làm sao loại bỏ $\alpha_i$ (individual effects) *trước khi* áp dụng bộ công cụ IV đã học, và những điều chỉnh cần thiết cho các kiểm định chẩn đoán khi chuyển từ cross-section sang panel.
> <br><span class="en">This page focuses only on the **extension specific to panel data**: how to remove $\alpha_i$ (individual effects) *before* applying the already-learned IV toolkit, and the adjustments needed for the diagnostic tests when moving from cross-section to panel.</span>

## 1. Vì sao vẫn cần IV, dù đã có FE? - <span class="en">Why is IV still needed even with FE?</span>

Đây là câu hỏi đầu tiên cần trả lời rõ trước khi vào công thức — nếu không, dễ nhầm rằng "đã dùng FE rồi thì hết endogeneity."
<br><span class="en">This is the first question that needs a clear answer before diving into formulas — otherwise it's easy to mistakenly assume "once FE is used, endogeneity is gone."</span>

Nhắc lại từ [[concepts/fixed-random-effects-model]]: giả định exogeneity A3 gốc của [[concepts/linear-regression-model]] được **tách làm hai** khi chuyển sang panel data:
<br><span class="en">Recall from [[concepts/fixed-random-effects-model]]: the original exogeneity assumption A3 from [[concepts/linear-regression-model]] gets **split into two** when moving to panel data:</span>

- **A3a**: $E(X_{it}\varepsilon_{it})=0$ — biến giải thích không tương quan với sai số **đặc thù theo thời gian** (idiosyncratic error) $\varepsilon_{it}$.
<br><span class="en">**A3a**: $E(X_{it}\varepsilon_{it})=0$ — the explanatory variable is uncorrelated with the **time-specific** error (idiosyncratic error) $\varepsilon_{it}$.</span>
- **A3b**: $E(X_{it}\alpha_i)=0$ — biến giải thích không tương quan với **hiệu ứng cá thể bất biến theo thời gian** (individual effect) $\alpha_i$.
<br><span class="en">**A3b**: $E(X_{it}\alpha_i)=0$ — the explanatory variable is uncorrelated with the **time-invariant individual effect** (individual effect) $\alpha_i$.</span>

**FE model giải quyết được A3b nhưng không giải quyết được A3a.** Trực giác: within-transformation (hay first-difference) chỉ khử được phần **không đổi theo thời gian** trong sai số ($\alpha_i$) — vì phần đó giống hệt nhau ở mọi $t$ của cùng một đơn vị $i$, trừ đi trung bình (hoặc trừ đi kỳ trước) sẽ làm nó biến mất. Nhưng nếu $X_{it}$ tương quan với $\varepsilon_{it}$ — phần sai số **thay đổi theo từng thời điểm cụ thể**, không phải một hằng số riêng của từng đơn vị — thì phép biến đổi này **bất lực**: $\varepsilon_{it}$ vẫn còn nguyên trong phương trình sau khi đã khử $\alpha_i$.
<br><span class="en">**The FE model solves A3b but does not solve A3a.** Intuition: the within-transformation (or first-difference) only removes the **time-invariant** part of the error ($\alpha_i$) — because that part is identical across every $t$ for the same unit $i$, subtracting the mean (or subtracting the previous period) makes it vanish. But if $X_{it}$ is correlated with $\varepsilon_{it}$ — the error part that **changes at each specific point in time**, not a constant unique to each unit — then this transformation is **powerless**: $\varepsilon_{it}$ still remains fully in the equation after $\alpha_i$ has been removed.</span>

**Ví dụ cụ thể (dùng xuyên suốt trang này)**: doanh nghiệp $i$ quyết định tăng giờ đào tạo lao động (`training`) trong năm $t$ vì ban lãnh đạo *dự đoán* nhu cầu sản xuất năm đó sẽ tăng (reverse causality/simultaneity — xem thêm ba nguồn gốc endogeneity ở [[concepts/endogeneity-iv-regression]]). Quyết định này thay đổi theo từng năm cụ thể của từng doanh nghiệp, không phải một đặc điểm cố định của doanh nghiệp đó — nên nó nằm trong $\varepsilon_{it}$, không nằm trong $\alpha_i$. FE (dù đã loại bỏ mọi khác biệt cố định giữa các doanh nghiệp — quy mô ngành, vị trí địa lý, năng lực quản lý gốc…) **không loại bỏ được** loại tương quan này. Đây chính xác là lý do cần IV **ngay cả sau khi đã dùng FE**.
<br><span class="en">**Concrete example (used throughout this page)**: firm $i$ decides to increase labor training hours (`training`) in year $t$ because management *anticipates* that production demand for that year will rise (reverse causality/simultaneity — see also the three sources of endogeneity in [[concepts/endogeneity-iv-regression]]). This decision changes from year to year for each specific firm, not a fixed characteristic of that firm — so it belongs in $\varepsilon_{it}$, not in $\alpha_i$. FE (even after removing every fixed difference across firms — industry scale, geographic location, baseline management capability…) **cannot remove** this type of correlation. This is exactly why IV is needed **even after FE has already been used**.</span>

## 2. Thiết lập mô hình - <span class="en">Model setup</span>

$$y_{it}=\gamma Y_{it}+\beta X_{it}+\alpha_i+\varepsilon_{it}, \qquad W_{it}=[Y_{it}, X_{it}],\; \delta=[\gamma,\beta]$$

- $Y_{it}$: vector biến **nội sinh** (tương quan với $\varepsilon_{it}$ — vi phạm A3a).
<br><span class="en">$Y_{it}$: vector of **endogenous** variables (correlated with $\varepsilon_{it}$ — violates A3a).</span>
- $X_{it}$: vector biến **ngoại sinh**.
<br><span class="en">$X_{it}$: vector of **exogenous** variables.</span>
- $\alpha_i$: individual effects (không quan sát được).
<br><span class="en">$\alpha_i$: individual effects (unobserved).</span>
- $\varepsilon_{it}$: sai số đặc thù theo thời gian.
<br><span class="en">$\varepsilon_{it}$: time-specific (idiosyncratic) error.</span>

Viết gọn: $y_{it}=\delta W_{it}+\alpha_i+\varepsilon_{it}$. Instrument $IV_{it}$ phải thỏa hai điều kiện quen thuộc — **relevance** và **exogeneity** (xem [[concepts/endogeneity-iv-regression]]).
<br><span class="en">Compactly: $y_{it}=\delta W_{it}+\alpha_i+\varepsilon_{it}$. The instrument $IV_{it}$ must satisfy the two familiar conditions — **relevance** and **exogeneity** (see [[concepts/endogeneity-iv-regression]]).</span>

**Lưu ý về phạm vi**: đây là **mô hình tĩnh (static)** — không có biến trễ của $y$ ở vế phải. Trường hợp có biến trễ (dynamic panel, nơi chính $y_{i,t-1}$ trở thành biến nội sinh) thuộc về [[concepts/dynamic-panel-data-models]], dùng logic khác (internal instruments).
<br><span class="en">**Note on scope**: this is a **static model** — there is no lagged $y$ on the right-hand side. The case with a lagged term (dynamic panel, where $y_{i,t-1}$ itself becomes the endogenous variable) belongs to [[concepts/dynamic-panel-data-models]], which uses different logic (internal instruments).</span>

**Các mô hình/ước lượng khả dụng**:
<br><span class="en">**Models/estimators available**:</span>
- **RE-IV** (Generalized 2SLS) — nội dung này **nằm ngoài phạm vi giảng dạy** của khóa học — Course Outline có liệt kê "2SLS RE estimator"/"G2GLS estimator" cho Topic 13, nhưng thực tế không được dạy. Ghi nhận khoảng trống này rõ ràng.
<br><span class="en">**RE-IV** (Generalized 2SLS) — this content is **outside the taught scope** of the course — the Course Outline lists "2SLS RE estimator"/"G2GLS estimator" for Topic 13, but it is not actually taught. This gap is noted explicitly.</span>
- **FD-IV** (First-Difference) — 2SLS, và các biến thể LIML/Fuller/GMM.
<br><span class="en">**FD-IV** (First-Difference) — 2SLS, plus the LIML/Fuller/GMM variants.</span>
- **FE-IV** (Fixed Effects) — 2SLS, và các biến thể LIML/Fuller/GMM.
<br><span class="en">**FE-IV** (Fixed Effects) — 2SLS, plus the LIML/Fuller/GMM variants.</span>

### Ví dụ dữ liệu xuyên suốt - <span class="en">Running data example</span>

Bộ dữ liệu: 300 doanh nghiệp × 5 năm (balanced panel, $N=1500$).
<br><span class="en">Dataset: 300 firms × 5 years (balanced panel, $N=1500$).</span>

| Biến<br><span class="en">Variable</span> | Ý nghĩa<br><span class="en">Meaning</span> | Vai trò<br><span class="en">Role</span> |
|---|---|---|
| `output` | Giá trị sản lượng (mil. VND)<br><span class="en">Output value (mil. VND)</span> | Biến phụ thuộc, dùng $\ln$<br><span class="en">Dependent variable, uses $\ln$</span> |
| `capital` | Giá trị vốn vật chất (mil. VND)<br><span class="en">Physical capital value (mil. VND)</span> | Ngoại sinh, dùng $\ln$<br><span class="en">Exogenous, uses $\ln$</span> |
| `training` | Giờ đào tạo/lao động (giờ/người)<br><span class="en">Training hours per worker (hours/person)</span> | **Nội sinh nghi ngờ**<br><span class="en">**Suspected endogenous**</span> |
| `labor` | Số lao động (người)<br><span class="en">Number of workers (persons)</span> | Ngoại sinh, dùng $\ln$<br><span class="en">Exogenous, uses $\ln$</span> |
| `export` | Dummy, 1 = có xuất khẩu<br><span class="en">Dummy, 1 = exports</span> | Ngoại sinh<br><span class="en">Exogenous</span> |
| `credit` | Dummy, 1 = có tiếp cận tín dụng<br><span class="en">Dummy, 1 = has credit access</span> | Ngoại sinh<br><span class="en">Exogenous</span> |
| `tech` | Trình độ công nghệ tương đối: `lowtech` (nền), `mediumtech`, `hightech`<br><span class="en">Relative technology level: `lowtech` (base), `mediumtech`, `hightech`</span> | Ngoại sinh (categorical → 2 dummy)<br><span class="en">Exogenous (categorical → 2 dummies)</span> |
| `subeligible` | Dummy, 1 = doanh nghiệp đủ điều kiện nhận trợ cấp đào tạo<br><span class="en">Dummy, 1 = firm eligible for training subsidy</span> | **Instrument (excluded)** |
| `localbudget` | Ngân sách chính quyền địa phương cho đào tạo (mil. VND)<br><span class="en">Local government training budget (mil. VND)</span> | **Instrument (excluded)** |

Mô hình cụ thể: $\ln(output)_{it} = \alpha_i + \gamma\,training_{it} + \beta_1\ln(capital)_{it} + \beta_2\ln(labor)_{it} + \cdots + \varepsilon_{it}$.
<br><span class="en">Specific model: $\ln(output)_{it} = \alpha_i + \gamma\,training_{it} + \beta_1\ln(capital)_{it} + \beta_2\ln(labor)_{it} + \cdots + \varepsilon_{it}$.</span>

**Mốc so sánh (benchmark) — FE cơ bản, coi `training` là ngoại sinh** (chưa xử lý nghi ngờ nội sinh, dùng để đối chiếu với kết quả IV ở các mục sau):
<br><span class="en">**Benchmark — basic FE, treating `training` as exogenous** (not yet addressing suspected endogeneity, used for comparison against the IV results in later sections):</span>

| Biến<br><span class="en">Variable</span> | Estimate | SE | t | p |
|---|---|---|---|---|
| `log(capital)` | 0.25465 | 0.01063 | 23.96 | <0.001 *** |
| `log(labor)` | 0.02106 | 0.01522 | 1.38 | 0.167 |
| **`training`** | **0.04185** | 0.00211 | 19.87 | <0.001 *** |
| `export` | 0.01613 | 0.02045 | 0.79 | 0.430 |
| `credit` | 0.07176 | 0.01900 | 3.78 | <0.001 *** |
| `mediumtech` | 0.00925 | 0.02096 | 0.44 | 0.659 |
| `hightech` | 0.21237 | 0.02554 | 8.32 | <0.001 *** |

Ghi nhớ con số **0.04185** cho `training` — đây là hệ số FE "ngây thơ" (naïve), sẽ được đối chiếu lại ở mục 7.4 sau khi có kết quả FE-IV, để minh họa cụ thể mức độ chệch do endogeneity gây ra.
<br><span class="en">Remember the number **0.04185** for `training` — this is the "naïve" FE coefficient, which will be compared again in section 7.4 once the FE-IV result is available, to concretely illustrate the magnitude of bias caused by endogeneity.</span>

## 3. First-Difference IV (FD-IV) Estimator - <span class="en">First-Difference IV (FD-IV) Estimator</span>

### 3.1 Trực giác: sai phân loại bỏ $\alpha_i$ trước, rồi mới 2SLS - <span class="en">Intuition: differencing removes $\alpha_i$ first, then 2SLS</span>

Cơ chế giống hệt ý tưởng first-difference trong panel data thường: $\alpha_i$ là một hằng số **riêng của từng đơn vị** $i$, không đổi theo $t$. Nếu viết phương trình ở hai thời điểm liên tiếp của cùng một đơn vị rồi **trừ cho nhau**, $\alpha_i$ xuất hiện y hệt ở cả hai vế và **tự triệt tiêu** — không cần biết giá trị của nó là bao nhiêu.
<br><span class="en">The mechanism is identical to the first-difference idea in ordinary panel data: $\alpha_i$ is a constant **specific to each unit** $i$, unchanging over $t$. If the equation is written at two consecutive time points for the same unit and then **subtracted from each other**, $\alpha_i$ appears identically on both sides and **cancels out on its own** — no need to know its value.</span>

$$y_{it}=\delta W_{it}+\alpha_i+\varepsilon_{it}, \qquad y_{i,t-1}=\delta W_{i,t-1}+\alpha_i+\varepsilon_{i,t-1}$$

Trừ vế theo vế:
<br><span class="en">Subtracting side by side:</span>

$$y_{it}-y_{i,t-1}=\delta(W_{it}-W_{i,t-1})+(\varepsilon_{it}-\varepsilon_{i,t-1}) \;\;\Rightarrow\;\; \Delta y_{it}=\delta\Delta W_{it}+\Delta\varepsilon_{it}$$

Phương trình sau sai phân **không còn $\alpha_i$** — nhưng $\Delta\varepsilon_{it}$ vẫn có thể tương quan với $\Delta W_{it}$ nếu $Y_{it}$ nội sinh (đây là lý do A3a không tự động được giải quyết chỉ bằng sai phân — khác với A3b). Bước tiếp theo: áp dụng **2SLS y hệt như ở cross-section** ([[concepts/endogeneity-iv-regression]]), nhưng trên biến đã sai phân, với instrument cũng đã sai phân $\Delta IV_{it}$.
<br><span class="en">The differenced equation **no longer contains $\alpha_i$** — but $\Delta\varepsilon_{it}$ can still be correlated with $\Delta W_{it}$ if $Y_{it}$ is endogenous (this is why A3a is not automatically solved by differencing alone — unlike A3b). The next step: apply **2SLS exactly as in the cross-section case** ([[concepts/endogeneity-iv-regression]]), but on the differenced variables, with the instrument also differenced $\Delta IV_{it}$.</span>

### 3.2 Ví dụ số (FD-IV, conventional/IID SE) - <span class="en">Numeric example (FD-IV, conventional/IID SE)</span>

```
FDIV: d(log(output)) ~ d(log(capital)) + d(log(labor)) + d(export) + d(credit)
      + d(mediumtech) + d(hightech) | 0 | d(training) ~ d(subeligible) + d(localbudget)
```

| Biến<br><span class="en">Variable</span> | Estimate | SE | t | p |
|---|---|---|---|---|
| Intercept | 0.033730 | 0.013872 | 2.43 | 0.015 * |
| **`fit_d(training)`** | **0.016833** | 0.005997 | 2.81 | 0.005 ** |
| `d(log(capital))` | 0.272336 | 0.011799 | 23.08 | <0.001 *** |
| `d(log(labor))` | 0.033934 | 0.016140 | 2.10 | 0.036 * |
| `d(export))` | 0.017373 | 0.021595 | 0.80 | 0.421 |
| `d(credit))` | 0.081324 | 0.020953 | 3.88 | <0.001 *** |
| `d(mediumtech))` | 0.055805 | 0.023798 | 2.34 | 0.019 * |
| `d(hightech))` | 0.251878 | 0.029615 | 8.51 | <0.001 *** |

$N=1200$ quan sát (giảm từ 1500 vì sai phân làm mất năm đầu tiên của mỗi doanh nghiệp: $300\times(5-1)=1200$).
<br><span class="en">$N=1200$ observations (down from 1500 because differencing loses the first year of each firm: $300\times(5-1)=1200$).</span>

## 4. Fixed Effects IV (FE-IV) Estimator - <span class="en">Fixed Effects IV (FE-IV) Estimator</span>

### 4.1 Trực giác: within-transformation loại bỏ $\alpha_i$ trước, rồi mới 2SLS - <span class="en">Intuition: the within-transformation removes $\alpha_i$ first, then 2SLS</span>

Cơ chế song song với FE thường ([[concepts/fixed-random-effects-model]]): trừ mỗi biến cho **trung bình theo thời gian của chính đơn vị đó** ($\bar y_i$, $\bar W_i$…). Vì $\alpha_i$ không đổi theo $t$, trung bình của nó theo thời gian **chính là $\alpha_i$** — trừ đi, nó biến mất y hệt cơ chế ở mục 3.1, chỉ khác phép toán (demean thay vì sai phân).
<br><span class="en">The mechanism runs parallel to ordinary FE ([[concepts/fixed-random-effects-model]]): subtract from each variable **its own unit's time average** ($\bar y_i$, $\bar W_i$…). Because $\alpha_i$ does not change over $t$, its time average **is exactly $\alpha_i$** — subtracting it makes it vanish, by the exact same mechanism as section 3.1, just a different operation (demeaning instead of differencing).</span>

$$\tilde y_{it}=y_{it}-\bar y_i+\bar y, \qquad \tilde W_{it}=W_{it}-\bar W_i+\bar W, \qquad \tilde{IV}_{it}=IV_{it}-\overline{IV}_i+\overline{IV}$$

(cộng lại trung bình toàn mẫu $\bar y$, $\bar W$, $\overline{IV}$ chỉ là quy ước giữ nguyên thang đo gốc — không ảnh hưởng đến hệ số góc). Phương trình sau biến đổi:
<br><span class="en">(adding back the overall sample mean $\bar y$, $\bar W$, $\overline{IV}$ is just a convention to keep the original scale — it does not affect the slope coefficients). The transformed equation:</span>

$$\tilde y_{it}=\delta\tilde W_{it}+\varepsilon_{it}$$

Không còn $\alpha_i$ → áp dụng 2SLS cho $\tilde y_{it}$ và $\tilde W_{it}$, với instrument $\tilde{IV}_{it}$.
<br><span class="en">No more $\alpha_i$ → apply 2SLS to $\tilde y_{it}$ and $\tilde W_{it}$, with instrument $\tilde{IV}_{it}$.</span>

### 4.2 Ví dụ số (FE-IV, conventional/IID SE) - <span class="en">Numeric example (FE-IV, conventional/IID SE)</span>

```
FEIV1: log(output) ~ log(capital) + log(labor) + export + credit + mediumtech + hightech
       | id | training ~ subeligible + localbudget
```

$N=1500$, fixed-effects: `id` (300 nhóm).
<br><span class="en">$N=1500$, fixed-effects: `id` (300 groups).</span>

| Biến<br><span class="en">Variable</span> | Estimate | SE | t | p |
|---|---|---|---|---|
| **`fit_training`** | **0.021190** | 0.005724 | 3.70 | <0.001 *** |
| `log(capital)` | 0.264823 | 0.011351 | 23.33 | <0.001 *** |
| `log(labor)` | 0.029598 | 0.015970 | 1.85 | 0.064 . |
| `export` | 0.030703 | 0.021588 | 1.42 | 0.155 |
| `credit` | 0.090846 | 0.020351 | 4.46 | <0.001 *** |
| `mediumtech` | 0.036322 | 0.022865 | 1.59 | 0.112 |
| `hightech` | 0.256436 | 0.028846 | 8.89 | <0.001 *** |

### 4.3 Mở rộng: Two-way FE-IV - <span class="en">Extension: Two-way FE-IV</span>

Có một cách tiếp cận riêng gọi là "Two-way FE-IV Regression" — về nội dung, đây chỉ là thêm **time fixed effects** $\gamma_t$ vào bên cạnh $\alpha_i$ (giống two-way FE ở [[concepts/fixed-random-effects-model]]), khai báo trong `fixest` bằng `| id + year |` thay vì `| id |`:
<br><span class="en">There is a dedicated approach called "Two-way FE-IV Regression" — in substance, this is just adding **time fixed effects** $\gamma_t$ alongside $\alpha_i$ (like two-way FE in [[concepts/fixed-random-effects-model]]), declared in `fixest` with `| id + year |` instead of `| id |`:</span>

```r
eqIVfixest2 = log(output) ~ log(capital) + log(labor) + export + credit + mediumtech + hightech
              | id + year | training ~ subeligible + localbudget
```

Chỉ có đoạn code cho cả 5 loại SE (homoskedastic, individual hetero, clustered by `id`, two-way clustered `id+year`, Driscoll-Kraay) — **không có bảng kết quả số** cho phần này, khác với FD-IV/FE-IV một chiều ở trên vốn có bảng số đầy đủ.
<br><span class="en">There is only code for all 5 types of SE (homoskedastic, individual hetero, clustered by `id`, two-way clustered `id+year`, Driscoll-Kraay) — **without an accompanying numeric results table** for this part, unlike the one-way FD-IV/FE-IV above which have full numeric tables.</span>

## 5. So sánh FD-IV vs. FE-IV — khi nào chọn cái nào - <span class="en">FD-IV vs. FE-IV comparison — which to choose when</span>

Cả hai đều loại bỏ $\alpha_i$ hợp lệ và đều dùng chung 5 loại SE (conventional/robust/clustered/two-way clustered/Driscoll-Kraay) với điều kiện áp dụng giống hệt [[concepts/fixed-random-effects-model]] (two-way clustered và DK cần $T$ đủ lớn mới đáng tin cậy). Nhưng **hai ước lượng không trùng nhau về mặt số học** trừ khi $T=2$ — bằng chứng ngay trong ví dụ trên: hệ số `training` là **0.0168** (FD-IV) so với **0.0212** (FE-IV), không giống nhau dù cùng dữ liệu, cùng instrument.
<br><span class="en">Both validly remove $\alpha_i$ and both use the same 5 types of SE (conventional/robust/clustered/two-way clustered/Driscoll-Kraay) with application conditions identical to [[concepts/fixed-random-effects-model]] (two-way clustered and DK need $T$ large enough to be reliable). But **the two estimators do not coincide numerically** unless $T=2$ — evidence right in the example above: the `training` coefficient is **0.0168** (FD-IV) versus **0.0212** (FE-IV), not the same despite the same data, same instruments.</span>

Tiêu chí kinh điển: hiệu quả tương đối giữa FD và FE phụ thuộc vào **cấu trúc tương quan chuỗi (serial correlation)** của $\varepsilon_{it}$:
<br><span class="en">Classic criterion: the relative efficiency between FD and FE depends on the **serial correlation structure** of $\varepsilon_{it}$:</span>

- Nếu $\varepsilon_{it}$ **không có tương quan chuỗi** (gần với white noise, giống giả định A4b lý tưởng) → **FE (within) hiệu quả hơn**. Lý do trực giác: sai phân ($\Delta\varepsilon_{it}=\varepsilon_{it}-\varepsilon_{i,t-1}$) của một chuỗi vốn không tương quan lại **tạo ra** tương quan âm bậc 1 (MA(1)) một cách nhân tạo — làm FD kém hiệu quả hơn cần thiết.
<br><span class="en">If $\varepsilon_{it}$ **has no serial correlation** (close to white noise, like the ideal A4b assumption) → **FE (within) is more efficient**. Intuitive reason: differencing ($\Delta\varepsilon_{it}=\varepsilon_{it}-\varepsilon_{i,t-1}$) of an originally uncorrelated series **artificially creates** negative first-order (MA(1)) correlation — making FD less efficient than necessary.</span>
- Nếu $\varepsilon_{it}$ có tương quan chuỗi **mạnh, gần giống random walk** (persistent shock, hiệu ứng kéo dài nhiều kỳ) → **FD hiệu quả hơn**. Lý do trực giác: sai phân của một chuỗi gần-random-walk cho ra phần dư gần với white noise (mỗi cú sốc chỉ xuất hiện một lần trong $\Delta\varepsilon_{it}=\varepsilon_{it}-\varepsilon_{i,t-1}$ rồi biến mất ở kỳ sau), trong khi within-transformation vẫn giữ nguyên toàn bộ tính persistent đó.
<br><span class="en">If $\varepsilon_{it}$ has **strong** serial correlation, **close to a random walk** (persistent shock, effect lasting many periods) → **FD is more efficient**. Intuitive reason: differencing a near-random-walk series produces residuals close to white noise (each shock appears only once in $\Delta\varepsilon_{it}=\varepsilon_{it}-\varepsilon_{i,t-1}$ then vanishes in the next period), whereas the within-transformation still retains the entire persistent component.</span>
- Trong thực hành: chạy cả hai, so sánh độ chính xác (SE) và tính ổn định của hệ số qua các đặc tả SE khác nhau; nếu hai kết quả lệch nhau đáng kể, đó cũng là một tín hiệu đáng lưu ý (dù không phải kiểm định chính thức) về đặc tả mô hình.
<br><span class="en">In practice: run both, compare precision (SE) and coefficient stability across different SE specifications; if the two results diverge substantially, that is also a signal worth noting (though not a formal test) about model specification.</span>

## 6. Ước lượng thay thế: LIML, Fuller, GMM - <span class="en">Alternative estimators: LIML, Fuller, GMM</span>

Khung giống hệt [[concepts/endogeneity-iv-regression]] — cả FD-IV lẫn FE-IV đều ước lượng được bằng bốn phương pháp: 2SLS, LIML, Fuller-adjusted LIML, GMM (2-step/iterative/CUE), áp dụng **sau khi** đã sai phân/demean để loại $\alpha_i$.
<br><span class="en">The framework is identical to [[concepts/endogeneity-iv-regression]] — both FD-IV and FE-IV can be estimated with four methods: 2SLS, LIML, Fuller-adjusted LIML, GMM (2-step/iterative/CUE), applied **after** differencing/demeaning to remove $\alpha_i$.</span>

**κ-class estimator**: $b(\kappa)=\big[X'(I-\kappa M_Z)X\big]^{-1}X'(I-\kappa M_Z)y$, $M_Z=I-Z(Z'Z)^{-1}Z'$. $\kappa=0$ → OLS; $\kappa=1$ → 2SLS. LIML chọn $\kappa$ là trị riêng nhỏ nhất (minimum eigenvalue) của $B^{-1}A$, với $A=Y'M_ZY$, $B=Y'M_XY$ — tương đương nghiệm nhỏ nhất của $\det(A-\kappa B)=0$. Trực giác: κ-class "nội suy" giữa OLS và 2SLS; LIML chọn điểm tối ưu theo hàm hợp lý (likelihood), giúp **ít bị chệch hơn 2SLS khi instrument yếu**.
<br><span class="en">**κ-class estimator**: $b(\kappa)=\big[X'(I-\kappa M_Z)X\big]^{-1}X'(I-\kappa M_Z)y$, $M_Z=I-Z(Z'Z)^{-1}Z'$. $\kappa=0$ → OLS; $\kappa=1$ → 2SLS. LIML picks $\kappa$ as the minimum eigenvalue of $B^{-1}A$, with $A=Y'M_ZY$, $B=Y'M_XY$ — equivalent to the smallest root of $\det(A-\kappa B)=0$. Intuition: the κ-class "interpolates" between OLS and 2SLS; LIML picks the optimal point according to the likelihood function, which makes it **less biased than 2SLS when instruments are weak**.</span>

**Fuller adjustment**: LIML tuy ít bias hơn 2SLS khi instrument yếu, nhưng vẫn có thể có phương sai lớn và vấn đề mẫu nhỏ. Fuller (1977) đề xuất điều chỉnh $\kappa$:
<br><span class="en">**Fuller adjustment**: although LIML has less bias than 2SLS when instruments are weak, it can still have large variance and small-sample issues. Fuller (1977) proposed adjusting $\kappa$:</span>

$$\kappa_F=\kappa-\frac{a}{n-l+k-1}$$

với $n$ = cỡ mẫu, $k$ = số regressor (nội sinh + ngoại sinh), $l$ = tổng số instrument (included + excluded), $a$ = hằng số dương thường chọn 1 hoặc 4. Kết quả: $\hat\beta_F=b(\kappa_F)$.
<br><span class="en">where $n$ = sample size, $k$ = number of regressors (endogenous + exogenous), $l$ = total number of instruments (included + excluded), $a$ = a positive constant usually chosen as 1 or 4. Result: $\hat\beta_F=b(\kappa_F)$.</span>

**Lưu ý thực hành riêng cho panel** (khác cross-section): two-way clustered SE **không đáng tin cậy** khi $T$ nhỏ; Driscoll-Kraay SE **không khả dụng** cho ước lượng LIML/Fuller trong các package R thông dụng — đây là một ràng buộc thực hành cần nhớ khi chọn loại SE, không chỉ chọn theo "loại robust nhất luôn tốt nhất".
<br><span class="en">**Panel-specific practical note** (unlike cross-section): two-way clustered SE is **not reliable** when $T$ is small; Driscoll-Kraay SE is **not available** for LIML/Fuller estimation in common R packages — this is a practical constraint to remember when choosing an SE type, not simply picking "the most robust type is always best."</span>

**Về GMM trong mô hình tĩnh**: với đặc tả tĩnh (static, không có biến trễ), IV-GMM **không mở rộng đáng kể** bộ instrument so với 2SLS — cả hai dựa trên cùng excluded instruments, chỉ khác nhau ở ma trận trọng số $W$ (2SLS dùng $W=(Z'Z)^{-1}$; GMM hiệu quả dùng $W=S^{-1}$). Dưới homoskedasticity, GMM hiệu quả **thu gọn về đúng 2SLS**; dưới heteroskedasticity, GMM gán trọng số thấp hơn cho quan sát có phương sai sai số lớn nên hiệu quả hơn — nhưng **lợi ích thực nghiệm trong mô hình tĩnh khá hạn chế**. (So sánh: GMM phát huy tác dụng rõ rệt hơn nhiều trong **dynamic panel** — xem [[concepts/dynamic-panel-data-models]] — nơi bộ instrument nội tại mở rộng đáng kể theo số lag khả dụng.)
<br><span class="en">**On GMM in the static model**: under a static specification (no lagged terms), IV-GMM **does not meaningfully expand** the instrument set relative to 2SLS — both rely on the same excluded instruments, differing only in the weighting matrix $W$ (2SLS uses $W=(Z'Z)^{-1}$; efficient GMM uses $W=S^{-1}$). Under homoskedasticity, efficient GMM **collapses exactly to 2SLS**; under heteroskedasticity, GMM assigns lower weight to observations with larger error variance and is therefore more efficient — but **the empirical benefit in the static model is fairly limited**. (Comparison: GMM proves far more useful in **dynamic panel** — see [[concepts/dynamic-panel-data-models]] — where the internal instrument set expands substantially with the number of available lags.)</span>

## 7. Kiểm định chẩn đoán cho IV-panel - <span class="en">Diagnostic tests for IV-panel</span>

Tái sử dụng đúng bốn nhóm kiểm định từ [[concepts/endogeneity-iv-regression]], điều chỉnh cho panel. Cần lưu ý: "*In R, diagnostic tests for IV regression with panel data is limited*" — công cụ sẵn có trong R hạn chế hơn so với cross-section thuần túy.
<br><span class="en">Reuses exactly the four groups of tests from [[concepts/endogeneity-iv-regression]], adjusted for panel. Worth noting: "*In R, diagnostic tests for IV regression with panel data is limited*" — the tools available in R are more limited than for pure cross-section.</span>

### 7.1 Underidentification test - <span class="en">Underidentification test</span>

$H_0: E(Z'Y)=0$ — instrument không mang thông tin nhận diện biến nội sinh. Dùng **first-stage F test**. Lưu ý quan trọng: **giá trị F thay đổi theo cấu trúc VCV** (conventional/robust/clustered/two-way clustered) — phải dùng đúng loại VCV tương ứng với mô hình chính, không trộn lẫn. Bác bỏ $H_0$ **không đồng nghĩa** với identification nhân quả hay instrument mạnh — đây là hai câu hỏi khác nhau (xem mục 7.2).
<br><span class="en">$H_0: E(Z'Y)=0$ — the instrument carries no information to identify the endogenous variable. Use the **first-stage F test**. Important note: **the F value changes with the VCV structure** (conventional/robust/clustered/two-way clustered) — the VCV type must match the main model, without mixing them. Rejecting $H_0$ **does not mean** causal identification or a strong instrument — these are two different questions (see section 7.2).</span>

**Ví dụ số** (FE-IV, two-way clustered SE theo `id` và `year`):
<br><span class="en">**Numeric example** (FE-IV, two-way clustered SE by `id` and `year`):</span>

$$F\text{-test (1st stage), training: stat} = 127.758, \quad p<2.2\times10^{-16}, \quad \text{trên } 2 \text{ và } 1{,}491 \text{ bậc tự do}$$
<br><span class="en">$$F\text{-test (1st stage), training: stat} = 127.758, \quad p<2.2\times10^{-16}, \quad \text{on } 2 \text{ and } 1{,}491 \text{ degrees of freedom}$$</span>

### 7.2 Weak identification test: CD-F vs. KP-F - <span class="en">Weak identification test: CD-F vs. KP-F</span>

**Vì sao cần hai phiên bản thống kê thay vì một?** Cùng câu hỏi "instrument giải thích được bao nhiêu biến thiên của $Y$" có thể trả lời theo hai cách, tùy giả định về sai số ở stage 1:
<br><span class="en">**Why are two statistic versions needed instead of one?** The same question "how much variation in $Y$ does the instrument explain" can be answered in two ways, depending on the error assumption at stage 1:</span>

- **[[people/cragg-donald|Cragg-Donald]] Wald F (CD-F)**: giả định **homoskedasticity**.
<br><span class="en">**[[people/cragg-donald|Cragg-Donald]] Wald F (CD-F)**: assumes **homoskedasticity**.</span>
- **Kleibergen-Paap rk Wald F (KP-F)**: **robust với heteroskedasticity** (và cả clustering).
<br><span class="en">**Kleibergen-Paap rk Wald F (KP-F)**: **robust to heteroskedasticity** (and also clustering).</span>

Trực giác: giống hệt lý do OLS cần cả conventional SE lẫn robust SE — nếu sai số hetero mà vẫn dùng thống kê giả định homo, kết luận "instrument đủ mạnh" có thể sai lệch. KP-F là phiên bản "vá" cho trường hợp thực tế phổ biến hơn (hetero, hoặc panel với clustered errors).
<br><span class="en">Intuition: exactly the same reason OLS needs both conventional SE and robust SE — if errors are hetero but a homo-assuming statistic is still used, the conclusion "instrument is strong enough" can be wrong. KP-F is the "patched" version for the more common real-world case (hetero, or panel with clustered errors).</span>

**Trường hợp đặc biệt cần nhớ**: với **1 biến nội sinh**, first-stage F-statistic **trùng đúng bằng** CD-F. Trong ví dụ trên, `training` là biến nội sinh duy nhất → $CD\text{-}F = 127.758$, vượt xa ngưỡng kinh nghiệm 10 lẫn mọi ngưỡng Stock-Yogo thông thường → không có bằng chứng instrument yếu.
<br><span class="en">**Special case to remember**: with **1 endogenous variable**, the first-stage F-statistic **exactly coincides with** CD-F. In the example above, `training` is the sole endogenous variable → $CD\text{-}F = 127.758$, far above both the rule-of-thumb threshold of 10 and any usual Stock-Yogo threshold → no evidence of a weak instrument.</span>

**Quy tắc quyết định**: so sánh CD-F với ngưỡng **[[people/stock-yogo|Stock-Yogo]] (SY)** hoặc mốc kinh nghiệm 10 (chi tiết hai tiêu chí SY — relative bias vs. size distortion — xem [[concepts/endogeneity-iv-regression]]).
<br><span class="en">**Decision rule**: compare CD-F against the **[[people/stock-yogo|Stock-Yogo]] (SY)** threshold or the rule-of-thumb value of 10 (details of the two SY criteria — relative bias vs. size distortion — see [[concepts/endogeneity-iv-regression]]).</span>

> **Lưu ý quan trọng nhất của mục này — bẫy thi hay gặp**: **KP-F không so sánh trực tiếp được với ngưỡng Stock-Yogo**, vì SY được xây dựng dưới giả định homoskedastic còn KP-F thì không — dùng sai một tiêu chí cho một thống kê không tương thích là lỗi kỹ thuật. Trong thực hành, người ta vẫn **so sánh không chính thức (informally)** KP-F với SY hoặc với ngưỡng 10, dù biết đây không phải phép so sánh chặt chẽ về mặt lý thuyết — chỉ là quy ước thực hành phổ biến, không phải một kiểm định chính danh.
> <br><span class="en">**The most important note in this section — a common exam trap**: **KP-F cannot be directly compared against the Stock-Yogo threshold**, because SY was built under the homoskedastic assumption while KP-F is not — applying a criterion to a statistic it's incompatible with is a technical error. In practice, people still **compare KP-F informally** with SY or with the threshold of 10, despite knowing this is not a theoretically rigorous comparison — it's merely a common practical convention, not a formally valid test.</span>

**Ghi chú về ví dụ số**: ví dụ minh họa (bảng ở mục 7.1) chỉ trình bày **một** giá trị F (dùng two-way clustered SE), với xác nhận rằng với 1 biến nội sinh, F này chính là CD-F — **không có một con số KP-F tách biệt** để đối chiếu trong đúng ví dụ số này.
<br><span class="en">**Note on the numeric example**: the illustrative example (table in section 7.1) presents only **one** F value (using two-way clustered SE), confirming that with 1 endogenous variable, this F is exactly CD-F — there is **no separate KP-F number** to compare within this exact numeric example.</span>

### 7.3 Overidentification test - <span class="en">Overidentification test</span>

Công thức và logic **giống hệt** bản cross-section ở [[concepts/endogeneity-iv-regression]] — [[people/sargan|Sargan]] (giả định homoskedasticity) hoặc [[people/hansen|Hansen's J]] (cho phép heteroskedasticity), cùng phân phối $\chi^2_{h-k}$, chỉ thực hiện được khi $h>k$ (over-identified) và **cần instrument đã xác nhận không yếu trước** (mục 7.2).
<br><span class="en">The formula and logic are **identical** to the cross-section version in [[concepts/endogeneity-iv-regression]] — [[people/sargan|Sargan]] (assumes homoskedasticity) or [[people/hansen|Hansen's J]] (allows heteroskedasticity), same $\chi^2_{h-k}$ distribution, only performable when $h>k$ (over-identified) and **requires instruments already confirmed not weak beforehand** (section 7.2).</span>

**Ví dụ số** (FE-IV, homoskedastic/IID): 2 instrument (`subeligible`, `localbudget`) cho 1 biến nội sinh (`training`) → bậc tự do $=2-1=1$.
<br><span class="en">**Numeric example** (FE-IV, homoskedastic/IID): 2 instruments (`subeligible`, `localbudget`) for 1 endogenous variable (`training`) → degrees of freedom $=2-1=1$.</span>

$$\text{Sargan: stat} = 1.6171, \quad p = 0.2035, \quad df=1$$

$p>0.05$ → **không bác bỏ** $H_0$ → không có bằng chứng chống lại tính hợp lệ đồng thời của hai instrument.
<br><span class="en">$p>0.05$ → **fail to reject** $H_0$ → no evidence against the joint validity of the two instruments.</span>

**Điểm cần nhấn mạnh nhất**: dù kết quả Sargan "ủng hộ" validity, vẫn có hai lớp giới hạn cần lưu ý:
<br><span class="en">**The point worth emphasizing most**: even though the Sargan result "supports" validity, there are two layers of limitation worth noting:</span>
1. Sargan giả định homoskedastic — "*should be interpreted with caution given the presence of heteroskedasticity and serial correlation*" (thực tế dữ liệu panel gần như luôn có nguy cơ cả hai).
<br><span class="en">Sargan assumes homoskedastic — "*should be interpreted with caution given the presence of heteroskedasticity and serial correlation*" (in practice panel data almost always carries risk of both).</span>
2. **Quan trọng hơn cả kiểm định**: "*the credibility of the instruments ultimately relies on economic reasoning and the plausibility of the exclusion restriction, not the formal tests*" — độ tin cậy cuối cùng của một instrument **không bao giờ** đến từ bản thân con số kiểm định, mà từ **lập luận kinh tế** rằng instrument chỉ tác động đến $y$ **qua duy nhất** kênh biến nội sinh, không có đường tác động trực tiếp nào khác. Không bác bỏ Sargan/Hansen chỉ có nghĩa "không tìm thấy bằng chứng chống lại", tuyệt đối không phải "đã chứng minh instrument hợp lệ".
<br><span class="en">**More important than the test itself**: "*the credibility of the instruments ultimately relies on economic reasoning and the plausibility of the exclusion restriction, not the formal tests*" — the ultimate credibility of an instrument **never** comes from the test statistic itself, but from **economic reasoning** that the instrument affects $y$ **only through** the endogenous-variable channel, with no other direct path. Failing to reject Sargan/Hansen only means "no evidence found against it," absolutely not "the instrument has been proven valid."</span>

### 7.4 Test for endogeneity: Wu-Hausman - <span class="en">Test for endogeneity: Wu-Hausman</span>

Logic và công thức giống [[concepts/endogeneity-iv-regression]]: nếu biến nghi ngờ thực sự ngoại sinh và instrument mạnh, OLS/FE và 2SLS hội tụ tiệm cận về cùng giá trị; nếu nội sinh, chúng phân kỳ có hệ thống.
<br><span class="en">The logic and formula match [[concepts/endogeneity-iv-regression]]: if the suspected variable is actually exogenous and the instrument is strong, OLS/FE and 2SLS converge asymptotically to the same value; if endogenous, they diverge systematically.</span>

$$H_0: X_2 \text{ exogenous}, \qquad \text{Statistic: } (\hat\beta_{2SLS}-\hat\beta_{OLS})'[V_{2SLS}-V_{OLS}]^{-1}(\hat\beta_{2SLS}-\hat\beta_{OLS}) \sim \chi^2_k$$

**Ví dụ số**: Wu-Hausman $=16.7$; ở $\alpha=10\%$, $p\approx0.00<0.1$ → **bác bỏ mạnh** $H_0$ → có bằng chứng `training` thực sự nội sinh.
<br><span class="en">**Numeric example**: Wu-Hausman $=16.7$; at $\alpha=10\%$, $p\approx0.00<0.1$ → **strongly reject** $H_0$ → evidence that `training` is indeed endogenous.</span>

**Đối chiếu trực quan với mục 2 và mục 4.2** — đây là minh họa số cụ thể, rất đáng nhớ cho việc "cảm nhận" endogeneity bias thay vì chỉ đọc con số kiểm định trừu tượng:
<br><span class="en">**Visual comparison with section 2 and section 4.2** — a concrete numeric illustration well worth remembering for "feeling" endogeneity bias rather than just reading an abstract test statistic:</span>

| Ước lượng<br><span class="en">Estimate</span> | Hệ số `training`<br><span class="en">`training` coefficient</span> |
|---|---|
| FE cơ bản (coi `training` ngoại sinh — mục 2)<br><span class="en">Basic FE (treating `training` as exogenous — section 2)</span> | **0.04185** |
| FE-IV (coi `training` nội sinh, IV = `subeligible`, `localbudget` — mục 4.2)<br><span class="en">FE-IV (treating `training` as endogenous, IV = `subeligible`, `localbudget` — section 4.2)</span> | **0.02119** |

Hệ số FE "ngây thơ" **gần gấp đôi** hệ số FE-IV đã hiệu chỉnh — nhất quán với câu chuyện kinh tế "doanh nghiệp tăng đào tạo *vì* kỳ vọng sản lượng tăng" (reverse causality): phần "tăng đào tạo đi kèm tăng sản lượng" trong hệ số FE ngây thơ không hoàn toàn là hiệu ứng nhân quả của đào tạo lên sản lượng, mà một phần là do lựa chọn tự thân của doanh nghiệp (self-selection) tương quan với kỳ vọng tăng trưởng. FE-IV bóc tách và loại bỏ phần chệch đó, cho hệ số nhỏ hơn — khớp với kết luận Wu-Hausman rằng `training` nội sinh và OLS/FE bị chệch.
<br><span class="en">The "naïve" FE coefficient is **nearly double** the corrected FE-IV coefficient — consistent with the economic story "firms increase training *because* they expect output to rise" (reverse causality): the "training increase alongside output increase" portion of the naïve FE coefficient is not entirely a causal effect of training on output, but partly reflects firms' self-selection correlated with growth expectations. FE-IV strips out and removes that bias, yielding a smaller coefficient — consistent with the Wu-Hausman conclusion that `training` is endogenous and OLS/FE is biased.</span>

**Lưu ý thực hành dễ gây nhầm lẫn**: gói `fixest` trong R **không dùng heteroskedastic VCV** để tính thống kê Wu-Hausman theo mặc định — một chi tiết dễ khiến hai người dùng hai package khác nhau ra hai con số Wu-Hausman khác nhau trên cùng dữ liệu, dù cùng mô hình.
<br><span class="en">**Practical note prone to confusion**: the `fixest` package in R **does not use heteroskedastic VCV** to compute the Wu-Hausman statistic by default — a detail that can easily lead two users with two different packages to get two different Wu-Hausman numbers on the same data, even with the same model.</span>

## 8. Bẫy thi - <span class="en">Common exam traps</span>

1. **Tưởng dùng FE là đã hết endogeneity.** FE chỉ giải quyết A3b (tương quan với $\alpha_i$), không giải quyết A3a (tương quan với $\varepsilon_{it}$) — nếu biến giải thích nội sinh với sai số đặc thù theo thời gian, vẫn cần IV dù đã dùng FE (xem mục 1).
<br><span class="en">**Assuming that using FE already eliminates endogeneity.** FE only solves A3b (correlation with $\alpha_i$), not A3a (correlation with $\varepsilon_{it}$) — if the explanatory variable is endogenous with the time-specific error, IV is still needed even after using FE (see section 1).</span>
2. Quên rằng FD-IV và FE-IV đều phải loại bỏ $\alpha_i$ **trước khi** áp dụng 2SLS — áp 2SLS trực tiếp lên phương trình gốc còn nguyên $\alpha_i$ cho kết quả sai (vì $\alpha_i$ không quan sát được và có thể tương quan với biến nội sinh, vi phạm chính điều kiện exogeneity của instrument).
<br><span class="en">Forgetting that both FD-IV and FE-IV must remove $\alpha_i$ **before** applying 2SLS — applying 2SLS directly to the original equation with $\alpha_i$ still intact gives wrong results (because $\alpha_i$ is unobserved and may be correlated with the endogenous variable, violating the instrument's own exogeneity condition).</span>
3. **Nhầm CD-F với KP-F khi tra ngưỡng Stock-Yogo** — SY chỉ được thiết kế cho CD-F (giả định homoskedastic); so KP-F với SY chỉ là quy ước thực hành không chính thức, không phải phép so sánh có nền tảng lý thuyết chặt.
<br><span class="en">**Confusing CD-F with KP-F when looking up the Stock-Yogo threshold** — SY was designed only for CD-F (homoskedastic assumption); comparing KP-F with SY is only an informal practical convention, not a theoretically rigorous comparison.</span>
4. Coi bác bỏ underidentification test là bằng chứng instrument "mạnh" — đây là hai kiểm định khác nhau (relevance vs. strength), y hệt bẫy đã nêu ở [[concepts/endogeneity-iv-regression]].
<br><span class="en">Treating rejection of the underidentification test as evidence the instrument is "strong" — these are two different tests (relevance vs. strength), exactly the same trap already noted in [[concepts/endogeneity-iv-regression]].</span>
5. Coi FD-IV và FE-IV luôn cho **cùng một con số** — chỉ trùng nhau khi $T=2$; với $T>2$ (như ví dụ $T=5$ ở đây), hai hệ số `training` (0.0168 vs. 0.0212) khác nhau thật sự.
<br><span class="en">Assuming FD-IV and FE-IV always give **the same number** — they only coincide when $T=2$; with $T>2$ (as in the $T=5$ example here), the two `training` coefficients (0.0168 vs. 0.0212) are genuinely different.</span>
6. Kỳ vọng GMM luôn hiệu quả hơn 2SLS đáng kể trong mô hình tĩnh — lợi ích thực nghiệm khá khiêm tốn (khác hẳn dynamic panel, nơi GMM phát huy tác dụng rõ rệt hơn).
<br><span class="en">Expecting GMM to always be substantially more efficient than 2SLS in a static model — the empirical benefit is fairly modest (unlike dynamic panel, where GMM proves much more useful).</span>
7. Không bác bỏ Sargan/Hansen J rồi coi là "đã chứng minh instrument hợp lệ" — và **quan trọng hơn**: quên rằng độ tin cậy cuối cùng của instrument luôn dựa vào **lập luận kinh tế** (exclusion restriction hợp lý), không phải bản thân con số kiểm định — đây là điểm cần nhấn mạnh, không chỉ là một chi tiết phụ.
<br><span class="en">Failing to reject Sargan/Hansen J and then treating it as "proof the instrument is valid" — and **more importantly**: forgetting that an instrument's ultimate credibility always rests on **economic reasoning** (a plausible exclusion restriction), not the test statistic itself — a point that deserves emphasis, not a minor detail.</span>
8. Dùng hai-way clustered SE hoặc Driscoll-Kraay khi $T$ nhỏ — cả hai chỉ đáng tin cậy với $T$ đủ lớn (giống lưu ý ở [[concepts/fixed-random-effects-model]]); riêng LIML/Fuller còn không có DK SE khả dụng trong các package R thông dụng.
<br><span class="en">Using two-way clustered SE or Driscoll-Kraay when $T$ is small — both are only reliable with $T$ large enough (same note as in [[concepts/fixed-random-effects-model]]); LIML/Fuller in particular have no DK SE available in common R packages.</span>

## 9. Kết nối - <span class="en">Connections</span>

Cầu nối trực tiếp giữa [[concepts/endogeneity-iv-regression]] (Topic 5, dữ liệu cross-section — cung cấp toàn bộ máy móc 2SLS/LIML/Fuller/GMM và 4 nhóm kiểm định chẩn đoán) và [[concepts/fixed-random-effects-model]] (Topic 6/12, panel không nội sinh — cung cấp khung A3a/A3b và cơ chế within/demean loại $\alpha_i$). Trang này áp đúng bộ công cụ IV vào bối cảnh có $\alpha_i$, chỉ thêm bước "loại $\alpha_i$ trước" (sai phân hoặc demean) so với cross-section thuần túy. Là bước đệm trực tiếp cho [[concepts/dynamic-panel-data-models]] (Topic 14), nơi chính **biến trễ của $y$** trở thành biến nội sinh cần xử lý bằng logic IV tương tự nhưng với instrument nội tại (internal instruments) thay vì instrument bên ngoài như `subeligible`/`localbudget` ở đây.
<br><span class="en">A direct bridge between [[concepts/endogeneity-iv-regression]] (Topic 5, cross-section data — supplies the entire 2SLS/LIML/Fuller/GMM machinery and the 4 groups of diagnostic tests) and [[concepts/fixed-random-effects-model]] (Topic 6/12, panel without endogeneity — supplies the A3a/A3b framework and the within/demean mechanism for removing $\alpha_i$). This page applies the IV toolkit exactly to a setting with $\alpha_i$, adding only the "remove $\alpha_i$ first" step (differencing or demeaning) compared to pure cross-section. It is a direct stepping stone to [[concepts/dynamic-panel-data-models]] (Topic 14), where the **lagged $y$** itself becomes the endogenous variable to be handled with similar IV logic, but with internal instruments instead of external instruments like `subeligible`/`localbudget` here.</span>

## 10. Tài liệu tham khảo ứng dụng thực tế - <span class="en">Real-world application references</span>

Ba bài báo gần đây minh họa IV regression cho panel data trong nghiên cứu kinh tế thực tế (đề cương Lecture 7):
<br><span class="en">Three recent papers illustrating IV regression for panel data in real-world economic research (Lecture 7 syllabus):</span>

- Gonzales, J. T. (2023). Implications of AI innovation on economic growth: A panel data study. *Journal of Economic Structures*, 12(1), 13. https://doi.org/10.1186/s40008-023-00307-w
- Zheng, M., & Wong, C. Y. (2024). The impact of digital economy on renewable energy development in China. *Innovation and Green Development*, 3(1), 100094. https://doi.org/10.1016/j.igd.2024.100094
- Siddiki, J., & Bala-Keffi, L. R. (2024). Revisiting the relation between financial inclusion and economic growth: A global analysis using panel threshold regression. *Economic Modelling*, 135, 106707. https://doi.org/10.1016/j.econmod.2024.106707
