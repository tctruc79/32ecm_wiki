---
title: "Lecture 10: Multinomial Logit Model (MNL)"
type: concept
status: mature
tags: [multinomial-logit, discrete-choice, limited-dependent-variable]
sources: ["[[sources/slides-8-multinomial-logit-model]]"]
related: ["[[concepts/binary-response-models]]", "[[concepts/ordinal-response-models]]"]
lecture: 10
assignment: []
updated: 2026-09-04
---

> **Cách đọc trang này**: MNL là mắt xích thứ hai trong chuỗi "limited dependent variable models" của khóa học — sau [[concepts/binary-response-models]] (Topic 7, biến phụ thuộc 0/1) và trước [[concepts/ordinal-response-models]] (Topic 9, biến phụ thuộc có thứ tự). Điều quan trọng nhất cần nắm **trước khi** đọc công thức là: MNL giải quyết trường hợp biến phụ thuộc là **một lựa chọn trong nhiều lựa chọn KHÔNG có thứ tự tự nhiên** — khác hẳn cả biến nhị phân lẫn biến có thứ tự. Toàn bộ trang này dùng lại đúng một case study xuyên suốt (chọn nơi khám chữa bệnh, dữ liệu VHLSS 2012) — cần nắm case study này để hiểu các ví dụ số ở các mục sau.
> <br><span class="en">**How to read this page**: MNL is the second link in the course's "limited dependent variable models" chain — after [[concepts/binary-response-models]] (Topic 7, 0/1 dependent variable) and before [[concepts/ordinal-response-models]] (Topic 9, ordered dependent variable). The most important thing to grasp **before** reading the formulas: MNL handles the case where the dependent variable is **one choice among several choices with NO natural order** — fundamentally different from both a binary variable and an ordinal one. This entire page reuses exactly one running case study (choice of healthcare provider, VHLSS 2012 data) — understanding this case study is necessary for following the numeric examples in the sections below.</span>

**Lecture 10** trong đề cương (CO Topic 8) — chưa có assignment riêng.
<br><span class="en">**Lecture 10** in the syllabus (CO Topic 8) — no dedicated assignment yet.</span>

## 1. Định vị bài toán: ba họ mô hình cho biến phụ thuộc rời rạc - <span class="en">Positioning the problem: three model families for discrete dependent variables</span>

Trước khi đi vào công thức, cần trả lời câu hỏi: biến phụ thuộc rời rạc (categorical) có mấy "dạng", và MNL xử lý dạng nào?
<br><span class="en">Before diving into the formulas, we need to answer: how many "kinds" of discrete (categorical) dependent variable are there, and which one does MNL handle?</span>

| Đặc điểm biến phụ thuộc $Y$ | Số phạm trù | Có thứ tự? | Mô hình tương ứng | Trang wiki |
|---|---|---|---|---|
| Nhị phân (binary) | 2 (VD: có/không, sống/chết) | Không áp dụng | Logit/Probit nhị phân | [[concepts/binary-response-models]] |
| **Đa phạm trù, không thứ tự (nominal)** | $J>2$ (VD: chọn hãng xe, chọn nghề, chọn bệnh viện) | **Không** — các phạm trù ngang hàng, không có phạm trù nào "cao/thấp hơn" phạm trù khác | **Multinomial Logit (MNL)** ← trang này | — |
| Đa phạm trù, có thứ tự (ordinal) | $J>2$ (VD: hài lòng thấp/trung bình/cao, xếp hạng tín dụng) | **Có** — các phạm trù có trật tự tự nhiên | Ordered Logit/Probit | [[concepts/ordinal-response-models]] |

<span class="en">

| $Y$ characteristic | Number of categories | Ordered? | Corresponding model | Wiki page |
|---|---|---|---|---|
| Binary | 2 (e.g., yes/no, alive/dead) | Not applicable | Binary Logit/Probit | [[concepts/binary-response-models]] |
| **Multi-category, unordered (nominal)** | $J>2$ (e.g., choice of car brand, occupation, hospital) | **No** — categories are on par, none is "higher/lower" than another | **Multinomial Logit (MNL)** ← this page | — |
| Multi-category, ordered (ordinal) | $J>2$ (e.g., low/medium/high satisfaction, credit rating) | **Yes** — categories have a natural order | Ordered Logit/Probit | [[concepts/ordinal-response-models]] |

</span>

Ví dụ minh họa từ slide gốc cho thấy rõ tính chất "không thứ tự" của MNL:
<br><span class="en">Illustrative examples from the original slide clearly show MNL's "unordered" property:</span>

- Hiệu ứng dài hạn của phơi nhiễm phóng xạ: 1 = chết vì ung thư, 2 = chết vì nguyên nhân khác, 3 = còn sống — ba phạm trù này **không** xếp được theo một trục "tăng dần/giảm dần" có ý nghĩa.
<br><span class="en">Long-term effects of radiation exposure: 1 = death by cancer, 2 = death by other cause, 3 = still alive — these three categories **cannot** be arranged along a meaningful "increasing/decreasing" axis.</span>
- Chọn nơi khám chữa bệnh: bệnh viện công, bệnh viện/phòng khám tư, thầy lang truyền thống, tự điều trị — không có phạm trù nào "hơn" phạm trù kia theo một thang đo chung, chỉ đơn thuần là các lựa chọn khác nhau.
<br><span class="en">Choice of healthcare provider: public hospital, private hospital/clinic, traditional healer, self-treatment — no category is "better" than another on a common scale, they are simply different choices.</span>
- Các ví dụ khác nêu trong slide: chọn hãng xe (Toyota, Honda, Suzuki, Mazda, KIA…), chọn ngành học, chọn nghề nghiệp.
<br><span class="en">Other examples given in the slide: choice of car brand (Toyota, Honda, Suzuki, Mazda, KIA…), choice of field of study, choice of occupation.</span>

**Vì sao không dùng OLS?** Muốn dùng OLS, $Y$ phải là một đại lượng có ý nghĩa số học — khoảng cách giữa hai giá trị phải mang thông tin (VD: chênh lệch giữa 3 và 1 năm học đúng bằng chênh lệch giữa 6 và 4 năm học). Nếu mã hóa "chọn bệnh viện công = 1, chọn bệnh viện tư = 2, chọn thầy lang = 3" rồi chạy OLS, mô hình sẽ ngầm giả định "thầy lang" cách "bệnh viện tư" đúng bằng khoảng cách "bệnh viện tư" cách "bệnh viện công" — một giả định vô nghĩa vì con số 1/2/3 chỉ là **nhãn** (label), không phải thang đo.
<br><span class="en">**Why not use OLS?** For OLS to be valid, $Y$ must be a quantity with arithmetic meaning — the distance between two values must carry information (e.g., the gap between 3 and 1 years of schooling must equal the gap between 6 and 4 years of schooling). If we code "chose public hospital = 1, chose private hospital = 2, chose traditional healer = 3" and run OLS, the model implicitly assumes "traditional healer" is exactly as far from "private hospital" as "private hospital" is from "public hospital" — a meaningless assumption, since the numbers 1/2/3 are merely **labels**, not a scale.</span>

**Vì sao không dùng Logit/Probit nhị phân?** Logit/Probit nhị phân ([[concepts/binary-response-models]]) chỉ xử lý được đúng 2 phạm trù. Khi $J>2$, cần một mô hình mở rộng được xác suất sang nhiều hơn 2 outcome mà vẫn đảm bảo mọi xác suất không âm và tổng bằng 1 — đó chính là động cơ ra đời của MNL.
<br><span class="en">**Why not use binary Logit/Probit?** Binary Logit/Probit ([[concepts/binary-response-models]]) can only handle exactly 2 categories. When $J>2$, we need a model that extends the probability structure to more than 2 outcomes while still guaranteeing every probability is non-negative and they sum to 1 — that is precisely the motivation behind MNL.</span>

## 2. Case study xuyên suốt: chọn nơi khám chữa bệnh (VHLSS 2012) - <span class="en">Running case study: choice of healthcare provider (VHLSS 2012)</span>

Đây là bộ dữ liệu thầy Thụy dùng cho toàn bộ slide Topic 8 — cần nắm để hiểu mọi ví dụ số ở các mục sau. Nguồn: **Vietnam Household Living Standards Survey (VHLSS) 2012**, file `mnl.xlsx`.
<br><span class="en">This is the dataset Prof. Thụy uses throughout the Topic 8 slides — understanding it is necessary for following every numeric example in the sections below. Source: **Vietnam Household Living Standards Survey (VHLSS) 2012**, file `mnl.xlsx`.</span>

**Biến phụ thuộc** `choice` — nơi khám chữa bệnh, 5 phạm trù không thứ tự:
<br><span class="en">**Dependent variable** `choice` — healthcare provider, 5 unordered categories:</span>

| Mã gốc | Phạm trù | Tần suất trong mẫu |
|---|---|---|
| 1 | Commune health center (trạm y tế xã) | 434 |
| 2 | Public hospital (bệnh viện công) | 2,320 |
| 3 | Private hospital (bệnh viện/phòng khám tư) | 522 |
| 4 | Lang y (thầy lang, y học cổ truyền dân gian) | 34 |
| 5 | Individual health care provider (cơ sở y tế cá nhân/tự do) | 165 |

<span class="en">

| Original code | Category | Sample frequency |
|---|---|---|
| 1 | Commune health center | 434 |
| 2 | Public hospital | 2,320 |
| 3 | Private hospital | 522 |
| 4 | Lang y (traditional folk healer) | 34 |
| 5 | Individual health care provider | 165 |

</span>

Tổng $N = 3{,}475$ quan sát. **Public hospital chiếm ưu thế áp đảo** — 2,320/3,475 ≈ 66.8% mẫu — một chi tiết quan trọng cần nhớ vì nó giải thích nhiều hiện tượng ở các mục dự đoán và McFadden $R^2$ bên dưới.
<br><span class="en">Total $N = 3{,}475$ observations. **Public hospital dominates overwhelmingly** — 2,320/3,475 ≈ 66.8% of the sample — an important detail to remember since it explains several phenomena in the prediction and McFadden $R^2$ sections below.</span>

> **Ghi chú về đơn vị phân tích**: bảng xem trước dữ liệu trong slide gốc có các cột `id`, `case`, `choice`, `income`, `female`… Cùng một `id` có thể xuất hiện ở nhiều dòng `case` khác nhau với `choice` khác nhau (VD `id=1` có `case=1` chọn Public hospital và `case=2` chọn Lang y) — cho thấy đơn vị phân tích thực chất là **mỗi lượt lựa chọn** (mỗi lần cần khám chữa bệnh), không phải cố định một lựa chọn duy nhất mỗi cá nhân. Một số dòng khác (`id=3`, `case=1,2,3`) bị để trống ở cột `choice` trong ảnh chụp slide gốc — không rõ đây là dữ liệu thiếu thật hay chỉ do ảnh preview bị cắt, ghi chú lại chứ không suy diễn thêm.
> <br><span class="en">**Note on the unit of analysis**: the data-preview table in the original slide has columns `id`, `case`, `choice`, `income`, `female`… The same `id` can appear across several different `case` rows with different `choice` values (e.g. `id=1` has `case=1` choosing Public hospital and `case=2` choosing Lang y) — showing that the unit of analysis is actually **each choice occasion** (each time healthcare is needed), not one fixed choice per individual. Some other rows (`id=3`, `case=1,2,3`) have a blank `choice` column in the original slide screenshot — it's unclear whether this is genuinely missing data or just a cropped preview image; noted here without further speculation.</span>

**Biến độc lập** (giữ nguyên tên biến từ slide):
<br><span class="en">**Independent variables** (variable names kept as in the slide):</span>

| Biến | Ý nghĩa | Đơn vị/mã hóa |
|---|---|---|
| `insurance` | Có bảo hiểm y tế hay không | dummy (1 = có, 0 = không) |
| `income` | Thu nhập hộ gia đình | triệu VND/năm |
| `female` | Giới tính | dummy (1 = nữ, 0 = nam) |
| `age` | Tuổi | năm |
| `edu` | Trình độ học vấn | categorical: 0 = dưới tiểu học, 1 = tiểu học, 2 = trung học cơ sở, 3 = trung học phổ thông, 4 = cao đẳng/đại học trở lên |
| `urban` | Sống ở khu vực đô thị hay không | dummy (1 = đô thị, 0 = nông thôn) |

<span class="en">

| Variable | Meaning | Unit/coding |
|---|---|---|
| `insurance` | Has health insurance or not | dummy (1 = yes, 0 = no) |
| `income` | Household income | million VND/year |
| `female` | Gender | dummy (1 = female, 0 = male) |
| `age` | Age | years |
| `edu` | Education level | categorical: 0 = below primary, 1 = primary, 2 = lower secondary, 3 = upper secondary, 4 = college/university or above |
| `urban` | Lives in an urban area or not | dummy (1 = urban, 0 = rural) |

</span>

`edu` được đưa vào mô hình dưới dạng `factor(edu)`, sinh ra 4 biến dummy (`edu1`–`edu4`, so với nền `edu0` = dưới tiểu học) — đúng logic biến phân loại (categorical) đã gặp ở [[concepts/linear-regression-model]] mục 5.
<br><span class="en">`edu` is entered into the model as `factor(edu)`, generating 4 dummy variables (`edu1`–`edu4`, relative to the base `edu0` = below primary) — following exactly the categorical-variable logic already seen in [[concepts/linear-regression-model]] section 5.</span>

## 3. Base category (nhóm nền) — vì sao cần, và chọn ai - <span class="en">Base category — why it's needed, and which one to choose</span>

### 3.1 Trực giác: vì sao không thể có $J$ phương trình độc lập - <span class="en">Intuition: why there cannot be $J$ independent equations</span>

Với $J$ phạm trù, ta có $J$ xác suất $p_{i1},\dots,p_{iJ}$, nhưng chúng phải thỏa ràng buộc $\sum_{j=1}^J p_{ij}=1$. Ràng buộc này có nghĩa: nếu biết $J-1$ xác suất, xác suất còn lại **tự động xác định được** ($p_{iJ}=1-\sum_{j<J}p_{ij}$) — nó không phải một bậc tự do độc lập. Vì vậy mô hình chỉ có thể ước lượng **tối đa $(J-1)$ bộ hệ số độc lập**, không phải $J$ bộ.
<br><span class="en">With $J$ categories, we have $J$ probabilities $p_{i1},\dots,p_{iJ}$, but they must satisfy the constraint $\sum_{j=1}^J p_{ij}=1$. This constraint means: if $J-1$ probabilities are known, the remaining one is **automatically determined** ($p_{iJ}=1-\sum_{j<J}p_{ij}$) — it is not an independent degree of freedom. So the model can only estimate **at most $(J-1)$ independent sets of coefficients**, not $J$ sets.</span>

Đây chính xác là **logic "nhóm nền" (base category)** đã gặp ở biến phân loại (categorical) trong OLS ([[concepts/linear-regression-model]] mục 5, ví dụ `cterrain` với `lowland` làm nền) — cùng một lý do toán học (tránh dư thừa/collinear hoàn hảo, tương ứng giả định A2 — full rank). Khác biệt: ở OLS, base category chỉ ảnh hưởng đến **một** phương trình hồi quy; ở MNL, base category chi phối **cả một hệ $(J-1)$ phương trình log-odds** cùng lúc.
<br><span class="en">This is exactly the **"base category" logic** already seen for categorical variables in OLS ([[concepts/linear-regression-model]] section 5, the `cterrain` example with `lowland` as the base) — the same mathematical reason (avoiding perfect redundancy/collinearity, corresponding to assumption A2 — full rank). The difference: in OLS, the base category only affects **one** regression equation; in MNL, the base category governs **an entire system of $(J-1)$ log-odds equations** simultaneously.</span>

### 3.2 Case study: chọn Public hospital làm base - <span class="en">Case study: choosing Public hospital as the base</span>

Slide gốc dùng lệnh R sau để đưa `Public hospital` (mã gốc = 2) lên làm nhóm nền:
<br><span class="en">The original slide uses the following R command to make `Public hospital` (original code = 2) the base group:</span>

```r
Z$choice = relevel(as.factor(Z$choice), ref = 2)
levels(Z$choice) = c("Public hospital", "Commune health center",
                      "Private hospital", "Lang y", "Ind. health care")
```

Việc chọn Public hospital (nhóm đông nhất, 66.8% mẫu) làm nền là lựa chọn thực dụng thường gặp — nó cho một điểm tham chiếu "phổ biến/mặc định" dễ diễn giải, và mọi so sánh trở thành "so với việc chọn bệnh viện công".
<br><span class="en">Choosing Public hospital (the largest group, 66.8% of the sample) as the base is a common, practical choice — it gives an easy-to-interpret "popular/default" reference point, and every comparison becomes "relative to choosing the public hospital".</span>

> **Điểm dễ gây nhầm lẫn giữa lý thuyết và code R**: công thức tổng quát ở mục 4 dưới đây đặt category **$J$ (phạm trù cuối cùng theo đánh số $1,\dots,J$)** làm base, với quy ước $h_{iJ}=0$. Nhưng trong R, hàm `nnet::multinom` (dùng để ước lượng MNL) lại lấy **level đầu tiên** của biến factor làm base. Đó là lý do đoạn code trên phải dùng `relevel()` rồi sắp lại `levels()` để đưa "Public hospital" lên vị trí đầu — không phải mâu thuẫn giữa lý thuyết và thực hành, chỉ là hai quy ước đánh số khác nhau (base = cuối trong công thức toán, base = đầu trong cách R tổ chức factor). Cần để ý khi đối chiếu công thức với output R.
> <br><span class="en">**A point that easily confuses theory and R code**: the general formula in section 4 below places category **$J$ (the last category under the numbering $1,\dots,J$)** as the base, with the convention $h_{iJ}=0$. But in R, the `nnet::multinom` function (used to estimate MNL) instead takes the **first level** of the factor variable as the base. That's why the code above must use `relevel()` and then reorder `levels()` to move "Public hospital" to the first position — this is not a contradiction between theory and practice, just two different numbering conventions (base = last in the math formula, base = first in how R organizes a factor). Worth noting when comparing the formula against R output.</span>

**Điểm quan trọng cần nhớ**: đổi base category **không** làm thay đổi xác suất dự đoán (fitted probabilities) hay độ khớp của mô hình — nó chỉ đổi cách các hệ số được *hiển thị/diễn giải* (điểm tham chiếu khác). Đây thuần túy là một chuẩn hóa (normalization), không phải một giả định mô hình.
<br><span class="en">**Key point to remember**: changing the base category does **not** change the fitted probabilities or the model's fit — it only changes how the coefficients are *displayed/interpreted* (a different reference point). This is purely a normalization, not a model assumption.</span>

## 4. Thiết lập: log-odds so với base category - <span class="en">Setup: log-odds relative to the base category</span>

Biến phụ thuộc $Y_i = 1,2,\dots,J$ với xác suất tương ứng $p_{i1},\dots,p_{iJ}$. Chọn category $J$ làm base, định nghĩa **logit** (log-odds ratio) so với base cho từng phạm trù còn lại:
<br><span class="en">Dependent variable $Y_i = 1,2,\dots,J$ with corresponding probabilities $p_{i1},\dots,p_{iJ}$. Choosing category $J$ as the base, define the **logit** (log-odds ratio) relative to the base for each remaining category:</span>

$$h_{ij} = \ln\frac{p_{ij}}{p_{iJ}} = \beta_j X_i \quad (j=1,\dots,J-1), \qquad h_{iJ} = \ln\frac{p_{iJ}}{p_{iJ}} = 0$$

Với $J$ lựa chọn, có **$(J-1)$ bộ hệ số $\beta$** cần ước lượng — mỗi bộ $\beta_j$ mô tả log-odds của việc chọn $j$ so với base, là một hàm tuyến tính riêng của $X$. Trong case study ($J=5$), có $(5-1)=4$ bộ hệ số: Commune health center vs. Public hospital, Private hospital vs. Public hospital, Lang y vs. Public hospital, Ind. health care vs. Public hospital.
<br><span class="en">With $J$ choices, there are **$(J-1)$ sets of $\beta$ coefficients** to estimate — each set $\beta_j$ describes the log-odds of choosing $j$ relative to the base, as its own separate linear function of $X$. In the case study ($J=5$), there are $(5-1)=4$ sets of coefficients: Commune health center vs. Public hospital, Private hospital vs. Public hospital, Lang y vs. Public hospital, Ind. health care vs. Public hospital.</span>

## 5. Suy ra công thức xác suất (softmax) - <span class="en">Deriving the probability formula (softmax)</span>

Đây là phần "derivation" — đi từng bước từ định nghĩa logit ở mục 4 ra công thức xác suất cuối cùng.
<br><span class="en">This is the "derivation" part — going step by step from the logit definition in section 4 to the final probability formula.</span>

**Bước 1 — mũ hóa hai vế** của $\ln(p_j/p_J) = \beta_j X$:
<br><span class="en">**Step 1 — exponentiate both sides** of $\ln(p_j/p_J) = \beta_j X$:</span>

$$p_{ij} = p_{iJ}\cdot e^{X_i\beta_j}$$

**Bước 2 — dùng ràng buộc tổng xác suất bằng 1**: vì $\sum_{j=1}^J p_{ij}=1$, ta có
<br><span class="en">**Step 2 — use the constraint that probabilities sum to 1**: since $\sum_{j=1}^J p_{ij}=1$, we have</span>

$$p_{iJ} = 1 - \sum_{j=1}^{J-1} p_{ij}$$

**Bước 3 — thay biểu thức ở Bước 1 vào Bước 2**:
<br><span class="en">**Step 3 — substitute the expression from Step 1 into Step 2**:</span>

$$p_{iJ} = 1 - \sum_{j=1}^{J-1} p_{iJ}\cdot e^{X_i\beta_j}$$

Giải phương trình này theo $p_{iJ}$ (đưa mọi số hạng chứa $p_{iJ}$ về một vế):
<br><span class="en">Solving this equation for $p_{iJ}$ (moving every term containing $p_{iJ}$ to one side):</span>

$$p_{iJ} = \frac{1}{1+\sum_{j=1}^{J-1} e^{X_i\beta_j}}$$

**Bước 4 — quay lại Bước 1** để tính các $p_{ij}$ còn lại:
<br><span class="en">**Step 4 — go back to Step 1** to compute the remaining $p_{ij}$:</span>

$$p_{ij} = \frac{e^{X_i\beta_j}}{1+\sum_{k=1}^{J-1} e^{X_i\beta_k}} \quad (j=1,\dots,J-1)$$

**Dạng gộp (softmax)** — nếu quy ước $\beta_J = 0$ cho category nền (khớp với $h_{iJ}=0$ ở mục 4), cả $p_{iJ}$ và $p_{ij}$ ở trên có thể viết chung một công thức:
<br><span class="en">**Combined form (softmax)** — if we adopt the convention $\beta_J = 0$ for the base category (consistent with $h_{iJ}=0$ in section 4), both $p_{iJ}$ and $p_{ij}$ above can be written as a single unified formula:</span>

$$p_{ij} = \frac{e^{X_i\beta_j}}{\sum_{k=1}^{J} e^{X_i\beta_k}}$$

Đây là dạng **softmax** quen thuộc (cũng chính là hàm kích hoạt đầu ra trong mạng neural cho bài toán phân loại đa lớp — cùng một cấu trúc toán học). Tính chất quan trọng của công thức này: **mọi $p_{ij} \in (0,1)$ và $\sum_j p_{ij}=1$ tự động được đảm bảo**, dù $X\beta_j$ có thể nhận bất kỳ giá trị thực nào — đây chính là lý do MNL "sửa" được vấn đề mà OLS mắc phải (không đảm bảo xác suất dự đoán nằm trong $[0,1]$).
<br><span class="en">This is the familiar **softmax** form (also exactly the output activation function used in neural networks for multi-class classification — the same mathematical structure). The important property of this formula: **every $p_{ij} \in (0,1)$ and $\sum_j p_{ij}=1$ is automatically guaranteed**, regardless of what real values $X\beta_j$ takes — this is precisely why MNL "fixes" the problem that plagues OLS (not guaranteeing predicted probabilities fall within $[0,1]$).</span>

## 6. Ước lượng: Maximum Likelihood - <span class="en">Estimation: Maximum Likelihood</span>

Khác với OLS — nơi có nghiệm dạng đóng (closed-form) $b=(X'X)^{-1}X'y$ (xem [[concepts/linear-regression-model]] mục 2.2) — công thức xác suất softmax ở mục 5 là **phi tuyến** theo $\beta$, nên không có nghiệm đóng. MNL được ước lượng bằng **Maximum Likelihood (ML)**, tối đa hóa hàm log-likelihood:
<br><span class="en">Unlike OLS — which has a closed-form solution $b=(X'X)^{-1}X'y$ (see [[concepts/linear-regression-model]] section 2.2) — the softmax probability formula in section 5 is **nonlinear** in $\beta$, so no closed-form solution exists. MNL is estimated by **Maximum Likelihood (ML)**, maximizing the log-likelihood function:</span>

$$\log L = \sum_{i=1}^N\sum_{j=1}^J y_{ij}\ln p_{ij}, \qquad y_{ij}=\begin{cases}1 & \text{nếu } j \text{ được chọn bởi quan sát } i\\0&\text{ngược lại}\end{cases}$$
<span class="en">(where $y_{ij}=1$ if $j$ is chosen by observation $i$, and $0$ otherwise)</span>

Việc tối ưu hóa này thực hiện bằng thuật toán số lặp (numerical iterative optimization — R dùng thuật toán Newton-type), không phải một phép tính ma trận trực tiếp như OLS.
<br><span class="en">This optimization is carried out via numerical iterative optimization (R uses a Newton-type algorithm), not a direct matrix computation as in OLS.</span>

### 6.1 Case study: mô hình null và mô hình đầy đủ - <span class="en">Case study: the null model and the full model</span>

**Mô hình null (chỉ có intercept)** — `choice ~ 1` — ước lượng log-odds trung bình của mỗi category so với base, không có biến giải thích nào:
<br><span class="en">**Null model (intercept only)** — `choice ~ 1` — estimates the average log-odds of each category relative to the base, with no explanatory variables:</span>

| Category (so với Public hospital) | Hệ số (intercept) | SE |
|---|---|---|
| Commune health center | −1.676278 | 0.05230 |
| Private hospital | −1.491655 | 0.04844 |
| Lang y | −4.222962 | 0.17275 |
| Ind. health care | −2.643377 | 0.08057 |

<span class="en">

| Category (relative to Public hospital) | Coefficient (intercept) | SE |
|---|---|---|
| Commune health center | −1.676278 | 0.05230 |
| Private hospital | −1.491655 | 0.04844 |
| Lang y | −4.222962 | 0.17275 |
| Ind. health care | −2.643377 | 0.08057 |

</span>

Residual Deviance = 6979.762, và vì $LL=-\text{Deviance}/2$ (ghi chú của chính slide gốc), $LL_{null} = -3489.881$.
<br><span class="en">Residual Deviance = 6979.762, and since $LL=-\text{Deviance}/2$ (as noted in the original slide itself), $LL_{null} = -3489.881$.</span>

> **Insight kiểm chứng được bằng tay**: với mô hình chỉ có intercept, hệ số ước lượng chính là **log-odds thô tính trực tiếp từ bảng tần suất** — $\hat\beta_{0j} = \ln(n_j/n_{base})$. Kiểm tra: $\ln(434/2320) = -1.676$, $\ln(522/2320)=-1.492$, $\ln(34/2320)=-4.223$, $\ln(165/2320)=-2.643$ — khớp chính xác với bảng trên. Đây là cách trực quan nhất để hiểu "log-odds" nghĩa là gì: nó chỉ là logarit của tỷ lệ tần suất giữa hai nhóm.
> <br><span class="en">**An insight you can verify by hand**: with an intercept-only model, the estimated coefficient is exactly the **raw log-odds computed directly from the frequency table** — $\hat\beta_{0j} = \ln(n_j/n_{base})$. Check: $\ln(434/2320) = -1.676$, $\ln(522/2320)=-1.492$, $\ln(34/2320)=-4.223$, $\ln(165/2320)=-2.643$ — matches the table above exactly. This is the most intuitive way to understand what "log-odds" means: it is simply the logarithm of the frequency ratio between two groups.</span>

**Mô hình đầy đủ** — `choice ~ insurance + income + female + age + factor(edu) + urban` — Residual Deviance = 6420.637, AIC = 6500.637, $LL_{full} = -3210.319$.
<br><span class="en">**Full model** — `choice ~ insurance + income + female + age + factor(edu) + urban` — Residual Deviance = 6420.637, AIC = 6500.637, $LL_{full} = -3210.319$.</span>

## 7. Diễn giải hệ số — phần dễ nhầm nhất của MNL - <span class="en">Interpreting coefficients — the most error-prone part of MNL</span>

### 7.1 Nguyên tắc - <span class="en">Principle</span>

Hệ số $\beta_j$ đo **thay đổi trong log-odds của việc chọn $j$ so với base category** khi $X$ tăng 1 đơn vị, giữ các biến khác không đổi — **không phải** thay đổi trực tiếp trong xác suất $P(Y=j)$. Đây là khác biệt căn bản so với hệ số OLS ([[concepts/linear-regression-model]] mục 5, nơi $b_j$ đo trực tiếp thay đổi của $y$).
<br><span class="en">The coefficient $\beta_j$ measures the **change in the log-odds of choosing $j$ relative to the base category** when $X$ increases by 1 unit, holding other variables constant — **not** a direct change in the probability $P(Y=j)$. This is a fundamental difference from OLS coefficients ([[concepts/linear-regression-model]] section 5, where $b_j$ directly measures the change in $y$).</span>

**Diễn giải bằng relative risk ratio (RRR)**: lấy $e^{\beta_j}$ cho một con số dễ đọc hơn — tỷ lệ odds chọn $j$ (so với base) thay đổi bao nhiêu lần khi $X$ tăng 1 đơn vị.
<br><span class="en">**Interpreting via the relative risk ratio (RRR)**: taking $e^{\beta_j}$ gives an easier-to-read number — by what multiple the odds of choosing $j$ (relative to the base) change when $X$ increases by 1 unit.</span>

### 7.2 Bảng hệ số case study (hai phương trình được slide trình bày riêng) - <span class="en">Case study coefficient tables (two equations presented separately in the slide)</span>

**Phương trình cho Commune health center (so với Public hospital):**
<br><span class="en">**Equation for Commune health center (relative to Public hospital):**</span>

| Biến | Coef | SE | z | p-value |
|---|---|---|---|---|
| (Intercept) | −0.26287 | 0.22855 | −1.150 | 0.250 |
| insurance | 0.01678 | 0.11720 | 0.143 | 0.886 |
| income | −0.00535 | 0.00128 | −4.171 | 0.00003 |
| female | 0.14753 | 0.10900 | 1.353 | 0.176 |
| age | −0.01318 | 0.00326 | −4.043 | 0.00005 |
| edu1 | −0.26877 | 0.14169 | −1.897 | 0.058 |
| edu2 | −0.39115 | 0.14641 | −2.672 | 0.008 |
| edu3 | −0.73012 | 0.19925 | −3.664 | 0.00025 |
| edu4 | −0.89003 | 0.34122 | −2.608 | 0.009 |
| urban | −0.97947 | 0.16298 | −6.010 | <0.0001 |

<span class="en">

| Variable | Coef | SE | z | p-value |
|---|---|---|---|---|
| (Intercept) | −0.26287 | 0.22855 | −1.150 | 0.250 |
| insurance | 0.01678 | 0.11720 | 0.143 | 0.886 |
| income | −0.00535 | 0.00128 | −4.171 | 0.00003 |
| female | 0.14753 | 0.10900 | 1.353 | 0.176 |
| age | −0.01318 | 0.00326 | −4.043 | 0.00005 |
| edu1 | −0.26877 | 0.14169 | −1.897 | 0.058 |
| edu2 | −0.39115 | 0.14641 | −2.672 | 0.008 |
| edu3 | −0.73012 | 0.19925 | −3.664 | 0.00025 |
| edu4 | −0.89003 | 0.34122 | −2.608 | 0.009 |
| urban | −0.97947 | 0.16298 | −6.010 | <0.0001 |

</span>

**Phương trình cho Private hospital (so với Public hospital):**
<br><span class="en">**Equation for Private hospital (relative to Public hospital):**</span>

| Biến | Coef | SE | z | p-value |
|---|---|---|---|---|
| (Intercept) | −0.33844 | 0.21710 | −1.559 | 0.119 |
| insurance | −1.20794 | 0.10718 | −11.270 | <0.0001 |
| income | 0.00210 | 0.00049 | 4.323 | 0.00002 |
| female | 0.16487 | 0.10213 | 1.614 | 0.106 |
| age | −0.01633 | 0.00332 | −4.926 | <0.0001 |
| edu1 | 0.14632 | 0.14578 | 1.004 | 0.316 |
| edu2 | −0.05282 | 0.14829 | −0.356 | 0.722 |
| edu3 | −0.38454 | 0.18512 | −2.077 | 0.038 |
| edu4 | 0.14029 | 0.22334 | 0.628 | 0.530 |
| urban | 0.08494 | 0.11546 | 0.736 | 0.462 |

<span class="en">

| Variable | Coef | SE | z | p-value |
|---|---|---|---|---|
| (Intercept) | −0.33844 | 0.21710 | −1.559 | 0.119 |
| insurance | −1.20794 | 0.10718 | −11.270 | <0.0001 |
| income | 0.00210 | 0.00049 | 4.323 | 0.00002 |
| female | 0.16487 | 0.10213 | 1.614 | 0.106 |
| age | −0.01633 | 0.00332 | −4.926 | <0.0001 |
| edu1 | 0.14632 | 0.14578 | 1.004 | 0.316 |
| edu2 | −0.05282 | 0.14829 | −0.356 | 0.722 |
| edu3 | −0.38454 | 0.18512 | −2.077 | 0.038 |
| edu4 | 0.14029 | 0.22334 | 0.628 | 0.530 |
| urban | 0.08494 | 0.11546 | 0.736 | 0.462 |

</span>

**Ví dụ diễn giải bằng lời (RRR)**:
<br><span class="en">**Example verbal interpretations (RRR)**:</span>

- ✅ "$e^{-1.20794}\approx 0.299$ — có bảo hiểm y tế làm giảm odds chọn bệnh viện tư (so với bệnh viện công) còn khoảng 30% so với người không có bảo hiểm, tức giảm khoảng 70% odds tương đối, giữ các yếu tố khác không đổi." (Đây là phát biểu về **log-odds/odds tương đối** — hợp lệ.)
<br><span class="en">✅ "$e^{-1.20794}\approx 0.299$ — having health insurance reduces the odds of choosing a private hospital (relative to a public hospital) to about 30% of the odds for someone without insurance, i.e., about a 70% relative-odds decrease, holding other factors constant." (This is a statement about **log-odds/relative odds** — valid.)</span>
- ❌ "Có bảo hiểm y tế làm giảm 70% **xác suất** chọn bệnh viện tư." — sai; con số 70% chỉ áp dụng cho tỷ lệ odds so với base, **không** áp dụng trực tiếp cho xác suất $P(\text{Private hospital})$ (xem mục 7.3 để thấy vì sao hai thứ này khác nhau về bản chất).
<br><span class="en">❌ "Having health insurance reduces the **probability** of choosing a private hospital by 70%." — wrong; the 70% figure only applies to the odds ratio relative to the base, it does **not** apply directly to the probability $P(\text{Private hospital})$ (see section 7.3 for why these two are fundamentally different).</span>
- ✅ "$e^{-0.97947}\approx 0.375$ — sống ở đô thị làm odds chọn trạm y tế xã (so với bệnh viện công) chỉ còn khoảng 37.5% so với sống ở nông thôn (giảm khoảng 62.5% odds tương đối)."
<br><span class="en">✅ "$e^{-0.97947}\approx 0.375$ — living in an urban area lowers the odds of choosing a commune health center (relative to a public hospital) to only about 37.5% of those of living in a rural area (about a 62.5% relative-odds decrease)."</span>

**Hệ số `insurance` qua cả 4 category** — một câu chuyện kinh tế nhất quán, minh họa cách đọc toàn bộ hệ phương trình cùng lúc:
<br><span class="en">**The `insurance` coefficient across all 4 categories** — a consistent economic story, illustrating how to read the entire system of equations at once:</span>

| Category (so với Public hospital) | Coef `insurance` | p-value |
|---|---|---|
| Commune health center | +0.0168 | 0.886 (không có ý nghĩa thống kê) |
| Private hospital | −1.2079 | <0.0001 |
| Lang y | −1.4630 | 0.0001 |
| Ind. health care | −1.8264 | <0.0001 |

<span class="en">

| Category (relative to Public hospital) | Coef `insurance` | p-value |
|---|---|---|
| Commune health center | +0.0168 | 0.886 (not statistically significant) |
| Private hospital | −1.2079 | <0.0001 |
| Lang y | −1.4630 | 0.0001 |
| Ind. health care | −1.8264 | <0.0001 |

</span>

Có bảo hiểm y tế gắn với odds thấp hơn **có ý nghĩa thống kê** cho cả 3 lựa chọn ngoài công (tư nhân, thầy lang, tự điều trị) so với bệnh viện công, trong khi so với trạm y tế xã thì không có khác biệt đáng kể — hợp lý về mặt kinh tế nếu bảo hiểm y tế công chủ yếu chi trả tốt tại các cơ sở công (bệnh viện công và có thể một phần trạm y tế xã).
<br><span class="en">Having health insurance is associated with **statistically significantly** lower odds for all 3 non-public options (private, traditional healer, self-treatment) relative to public hospital, while relative to the commune health center there is no significant difference — economically sensible if public health insurance mainly reimburses well at public facilities (public hospitals and possibly, to some extent, commune health centers).</span>

### 7.3 Bẫy tinh vi nhất: hệ số dương KHÔNG có nghĩa "xác suất chọn tăng" - <span class="en">The subtlest trap: a positive coefficient does NOT mean "choice probability increases"</span>

Đây là điểm nhầm lẫn phổ biến và tinh vi nhất khi mới học MNL — cần một ví dụ số cụ thể để thấy rõ.
<br><span class="en">This is the most common and subtle point of confusion when first learning MNL — a concrete numeric example is needed to see it clearly.</span>

**Nghịch lý xuất phát điểm**: category `Public hospital` (nền) có "hệ số $\beta$" bằng 0 **theo định nghĩa** (vì $h_{iJ}=0$, không có gì để so sánh nó với chính nó). Nếu suy diễn ngây thơ "hệ số 0 → biến $X$ không ảnh hưởng gì đến việc chọn category này", ta sẽ kết luận sai rằng `insurance` không ảnh hưởng đến xác suất chọn Public hospital. Thực tế, khi tính **marginal effect** thực sự (bằng gói `margins` trong R) — tức $\partial p_j/\partial x$, không phải $\partial h_j/\partial x$:
<br><span class="en">**The starting paradox**: the `Public hospital` (base) category has its "$\beta$ coefficient" equal to 0 **by definition** (since $h_{iJ}=0$ — there is nothing to compare it against itself). If we naively infer "coefficient 0 → variable $X$ has no effect on choosing this category", we'd wrongly conclude that `insurance` has no effect on the probability of choosing Public hospital. In reality, when we compute the true **marginal effect** (using the `margins` package in R) — i.e., $\partial p_j/\partial x$, not $\partial h_j/\partial x$:</span>

| Category | Average Marginal Effect của `insurance` lên $P(\text{category})$ |
|---|---|
| **Public hospital (base, hệ số = 0)** | **+0.17** ← lớn nhất trong tất cả! |
| Commune health center (hệ số +0.0168, *không* có ý nghĩa thống kê) | +0.03 |
| Private hospital (hệ số −1.2079, có ý nghĩa mạnh) | −0.12 |

<span class="en">

| Category | Average Marginal Effect of `insurance` on $P(\text{category})$ |
|---|---|
| **Public hospital (base, coefficient = 0)** | **+0.17** ← largest of all! |
| Commune health center (coefficient +0.0168, *not* statistically significant) | +0.03 |
| Private hospital (coefficient −1.2079, strongly significant) | −0.12 |

</span>

Có bảo hiểm y tế làm **tăng xác suất chọn Public hospital nhiều nhất** (+17 điểm phần trăm trung bình) — dù hệ số log-odds của chính category này "bằng 0 theo định nghĩa" vì nó là base. Ngược lại, `Commune health center` có hệ số log-odds gần như bằng 0 và không có ý nghĩa thống kê (p = 0.886) so với base, nhưng xác suất thực tế vẫn tăng nhẹ (+0.03) khi có bảo hiểm.
<br><span class="en">Having health insurance **increases the probability of choosing Public hospital the most** (+17 percentage points on average) — even though the log-odds coefficient of this very category is "0 by definition" because it is the base. Conversely, `Commune health center` has a log-odds coefficient close to zero and not statistically significant (p = 0.886) relative to the base, yet its actual probability still rises slightly (+0.03) with insurance.</span>

**Vì sao xảy ra nghịch lý này?** Có thể suy trực tiếp từ chính công thức softmax ở mục 5. Lấy đạo hàm $p_{ij}$ theo một biến $x$ bất kỳ trong $X$:
<br><span class="en">**Why does this paradox occur?** It can be derived directly from the softmax formula in section 5. Taking the derivative of $p_{ij}$ with respect to any variable $x$ in $X$:</span>

$$\frac{\partial p_{ij}}{\partial x} = p_{ij}\left(\beta_{jx} - \sum_{k=1}^{J} p_{ik}\,\beta_{kx}\right) = p_{ij}\left(\beta_{jx} - \bar\beta_x\right)$$

trong đó $\bar\beta_x = \sum_k p_{ik}\beta_{kx}$ là **trung bình có trọng số xác suất** của hệ số $\beta_{kx}$ trên **toàn bộ** $J$ category (kể cả base, với $\beta_{base,x}=0$). Marginal effect của $x$ lên $p_{ij}$ phụ thuộc vào **hiệu số** giữa $\beta_{jx}$ riêng của category $j$ và $\bar\beta_x$ — trung bình của **tất cả** category — chứ không phải giá trị tuyệt đối của $\beta_{jx}$ một mình. Với biến `insurance`: 3/4 category ngoài base có hệ số âm mạnh (−1.208, −1.463, −1.826) và chỉ 1 gần 0 (+0.017), nên $\bar\beta_{insurance} < 0$ rất rõ. Với category base (nơi $\beta_{base}=0$): $\partial p_{base}/\partial x = p_{base}(0-\bar\beta_x) = -p_{base}\bar\beta_x > 0$ — dương, đúng như số liệu quan sát được (+0.17)!
<br><span class="en">where $\bar\beta_x = \sum_k p_{ik}\beta_{kx}$ is the **probability-weighted average** of the coefficient $\beta_{kx}$ across **all** $J$ categories (including the base, with $\beta_{base,x}=0$). The marginal effect of $x$ on $p_{ij}$ depends on the **difference** between category $j$'s own $\beta_{jx}$ and $\bar\beta_x$ — the average across **all** categories — not on the absolute value of $\beta_{jx}$ alone. For the `insurance` variable: 3 of the 4 non-base categories have strongly negative coefficients (−1.208, −1.463, −1.826) and only 1 is near zero (+0.017), so $\bar\beta_{insurance} < 0$ quite clearly. For the base category (where $\beta_{base}=0$): $\partial p_{base}/\partial x = p_{base}(0-\bar\beta_x) = -p_{base}\bar\beta_x > 0$ — positive, exactly matching the observed figure (+0.17)!</span>

**Bài học cốt lõi**: marginal effect trên $P(Y=j)$ phụ thuộc vào **toàn bộ** hệ $(J-1)$ bộ hệ số, không chỉ riêng $\beta_j$. Vì vậy **không thể** suy trực tiếp dấu hay độ lớn của marginal effect chỉ từ dấu của một hệ số log-odds đơn lẻ — bắt buộc phải tính marginal effects riêng (như R làm bằng gói `margins`), tương tự cách [[concepts/binary-response-models]] phân biệt hệ số logit thô với marginal effects (MEM/AME).
<br><span class="en">**The core lesson**: the marginal effect on $P(Y=j)$ depends on the **entire** system of $(J-1)$ coefficient sets, not just $\beta_j$ alone. Therefore the sign or magnitude of a marginal effect **cannot** be inferred directly from the sign of a single log-odds coefficient — marginal effects must be computed separately (as R does with the `margins` package), similar to how [[concepts/binary-response-models]] distinguishes raw logit coefficients from marginal effects (MEM/AME).</span>

## 8. Kiểm định sau MNL — song song với t-test/F-test của OLS - <span class="en">Post-estimation tests for MNL — paralleling OLS's t-test/F-test</span>

### 8.1 z-test cho từng hệ số - <span class="en">z-test for each coefficient</span>

Vì MNL ước lượng bằng ML (không phải OLS với giả định A1–A5), thống kê kiểm định cho từng hệ số dùng phân phối **chuẩn tiệm cận (asymptotic normal)** — ký hiệu $z$ — chứ không phải phân phối Student-$t$ hữu hạn mẫu như OLS:
<br><span class="en">Since MNL is estimated by ML (not OLS with assumptions A1–A5), the test statistic for each coefficient uses the **asymptotic normal distribution** — denoted $z$ — rather than the finite-sample Student-$t$ distribution used in OLS:</span>

$$z = \frac{b_j}{SE(b_j)} \sim N(0,1) \text{ (xấp xỉ, khi } N \text{ đủ lớn)}$$
<span class="en">(approximate, when $N$ is sufficiently large)</span>

Cách đọc $p$-value và quy tắc bác bỏ $H_0$ giống hệt t-test ở [[concepts/linear-regression-model]] mục 7 — chỉ khác phân phối tham chiếu.
<br><span class="en">Reading the $p$-value and the rule for rejecting $H_0$ are exactly the same as the t-test in [[concepts/linear-regression-model]] section 7 — only the reference distribution differs.</span>

### 8.2 LR test cho ý nghĩa tổng thể (thay cho F-test) - <span class="en">LR test for overall significance (replacing the F-test)</span>

Muốn kiểm định "toàn bộ biến giải thích có ý nghĩa cùng lúc hay không" (giống F-test tổng thể ở [[concepts/linear-regression-model]] mục 8.5), MNL dùng **Likelihood Ratio (LR) test**, so sánh mô hình unrestricted (đầy đủ) với restricted (null):
<br><span class="en">To test "whether all explanatory variables are jointly significant" (like the overall F-test in [[concepts/linear-regression-model]] section 8.5), MNL uses the **Likelihood Ratio (LR) test**, comparing the unrestricted (full) model against the restricted (null) model:</span>

$$LR = -2(LL_{restricted}-LL_{unrestricted}) = \text{Deviance}_{restricted}-\text{Deviance}_{unrestricted} \sim \chi^2_q$$

với $q$ = số ràng buộc (số hệ số bị ép về 0). Đây là **cấu trúc logic giống hệt F-test** (so sánh unrestricted vs. restricted) — chỉ khác thống kê kiểm định (chi-square thay vì F) vì đây là mô hình MLE, không có "residual variance" để chuẩn hóa như OLS.
<br><span class="en">where $q$ = the number of restrictions (the number of coefficients forced to 0). This is **exactly the same logical structure as the F-test** (comparing unrestricted vs. restricted) — only the test statistic differs (chi-square instead of F) because this is an MLE model, with no "residual variance" to normalize against as in OLS.</span>

**Case study** — so sánh mô hình null (chỉ intercept, 4 tham số) với mô hình đầy đủ (40 tham số):
<br><span class="en">**Case study** — comparing the null model (intercept only, 4 parameters) with the full model (40 parameters):</span>

$$LR = 6979.762 - 6420.637 = 559.125 \sim \chi^2_{36}, \quad p \approx 0$$

Bác bỏ mạnh $H_0$ (mọi hệ số góc = 0) → có bằng chứng rằng **ít nhất một** trong các biến giải thích ảnh hưởng đến lựa chọn nơi khám chữa bệnh — đúng logic diễn giải F-test tổng thể (chỉ "ít nhất một", không phải "mọi biến").
<br><span class="en">Strongly rejects $H_0$ (all slope coefficients = 0) → there is evidence that **at least one** of the explanatory variables affects the choice of healthcare provider — following exactly the same interpretation logic as the overall F-test (only "at least one", not "every variable").</span>

### 8.3 LR test cho một nhóm biến con (giống F-test cho subset) - <span class="en">LR test for a subset of variables (like an F-test for a subset)</span>

Case study kiểm định thêm: bỏ nhóm biến `{female, age, factor(edu), urban}` ra khỏi mô hình có làm giảm độ khớp có ý nghĩa hay không? (28 ràng buộc: 1+1+4+1 hệ số × 4 phương trình)
<br><span class="en">An additional case-study test: does dropping the variable group `{female, age, factor(edu), urban}` from the model significantly reduce fit? (28 restrictions: 1+1+4+1 coefficients × 4 equations)</span>

$$LR = 6576.424 - 6420.637 = 155.787 \sim \chi^2_{28}, \quad p < 2.2\times10^{-16}$$

Bác bỏ mạnh $H_0$ → nhóm biến nhân khẩu học/địa lý này đóng góp có ý nghĩa thống kê vào mô hình, ngay cả sau khi đã kiểm soát `insurance` và `income`.
<br><span class="en">Strongly rejects $H_0$ → this group of demographic/geographic variables makes a statistically significant contribution to the model, even after controlling for `insurance` and `income`.</span>

## 9. Dự đoán và đánh giá độ khớp qua dự đoán - <span class="en">Prediction and assessing fit through prediction</span>

Xác suất dự đoán (fitted values) cho quan sát đầu tiên trong mẫu: $P(\text{Public})=0.702$, $P(\text{Commune})=0.172$, $P(\text{Private})=0.100$, $P(\text{Lang y})=0.004$, $P(\text{Ind.})=0.022$ — cộng đúng bằng 1, đúng như ràng buộc softmax đảm bảo ở mục 5.
<br><span class="en">Predicted probabilities (fitted values) for the first observation in the sample: $P(\text{Public})=0.702$, $P(\text{Commune})=0.172$, $P(\text{Private})=0.100$, $P(\text{Lang y})=0.004$, $P(\text{Ind.})=0.022$ — summing exactly to 1, as guaranteed by the softmax constraint in section 5.</span>

Quy tắc dự đoán category thường dùng: chọn category có xác suất fitted **cao nhất** (argmax). Vì `Public hospital` chiếm ưu thế áp đảo trong mẫu (66.8%), mô hình dự đoán "Public hospital" cho **cả 5 quan sát đầu tiên** trong case study.
<br><span class="en">The commonly used prediction rule: pick the category with the **highest** fitted probability (argmax). Because `Public hospital` dominates the sample (66.8%), the model predicts "Public hospital" for **all of the first 5 observations** in the case study.</span>

**Kiểm định goodness-of-prediction** (so khớp phân phối dự đoán với phân phối thực tế, Pearson chi-square): $X^2=40.476$, $df=8$, $p=2.6\times10^{-6}$ — có bằng chứng phân phối dự đoán khác phân phối thực tế một cách có ý nghĩa thống kê (R cũng cảnh báo "Chi-squared approximation may be incorrect", nhiều khả năng do một số ô có tần suất kỳ vọng quá nhỏ — category `Lang y` chỉ có 34/3475 quan sát).
<br><span class="en">**Goodness-of-prediction test** (comparing the predicted distribution against the actual distribution, Pearson chi-square): $X^2=40.476$, $df=8$, $p=2.6\times10^{-6}$ — there is statistically significant evidence that the predicted distribution differs from the actual one (R also warns "Chi-squared approximation may be incorrect", most likely because some cells have too small an expected frequency — category `Lang y` has only 34/3475 observations).</span>

> **Bẫy liên quan**: một mô hình MNL có thể "trông đúng" phần lớn thời gian chỉ vì luôn dự đoán category phổ biến nhất — điều đó **không** chứng minh mô hình khớp tốt cho các category thiểu số (Lang y, Ind. health care). Cần nhìn cả kiểm định goodness-of-prediction, không chỉ tỷ lệ dự đoán đúng thô.
> <br><span class="en">**A related trap**: an MNL model can "look correct" most of the time simply by always predicting the most popular category — that **does not** prove the model fits the minority categories well (Lang y, Ind. health care). One must also look at the goodness-of-prediction test, not just the raw proportion of correct predictions.</span>

## 10. McFadden R² (pseudo-R²) - <span class="en">McFadden R² (pseudo-R²)</span>

### 10.1 Công thức và ví dụ số - <span class="en">Formula and numeric example</span>

$$R^2_{McFadden} = 1-\frac{LL_{full}}{LL_{null}} = \frac{LL_{null}-LL_{full}}{LL_{null}}$$

**Case study** (dùng đúng $LL$ đã tính ở mục 6.1): $LL_{null}=-3489.881$, $LL_{full}=-3210.319$
<br><span class="en">**Case study** (using exactly the $LL$ values computed in section 6.1): $LL_{null}=-3489.881$, $LL_{full}=-3210.319$</span>

$$R^2_{McFadden} = \frac{-3489.881-(-3210.319)}{-3489.881} = \frac{-279.562}{-3489.881} \approx 0.0801$$

(Khớp chính xác với kết quả tính trực tiếp trong R từ slide gốc: `0.08010663`.)
<br><span class="en">(Matches exactly the result computed directly in R in the original slide: `0.08010663`.)</span>

### 10.2 Khác gì với $R^2$ của OLS - <span class="en">How it differs from OLS $R^2$</span>

$R^2$ của OLS ([[concepts/linear-regression-model]] mục 9) đo **tỷ lệ biến thiên (variance) của $y$ được giải thích** — một phép phân rã tổng bình phương (TSS = ESS + RSS) có ý nghĩa hình học rõ ràng vì $y$ là biến liên tục. MNL không có khái niệm "biến thiên" tương tự cho một biến phụ thuộc **categorical** — không có TSS/RSS nào để phân rã. Thay vào đó, McFadden $R^2$ đo **mức độ cải thiện log-likelihood** của mô hình đầy đủ so với mô hình chỉ có intercept (null model) — một đại lượng thuộc không gian xác suất/likelihood, không phải không gian phương sai.
<br><span class="en">OLS $R^2$ ([[concepts/linear-regression-model]] section 9) measures **the proportion of variance in $y$ explained** — a sum-of-squares decomposition (TSS = ESS + RSS) with a clear geometric meaning because $y$ is continuous. MNL has no analogous notion of "variance" for a **categorical** dependent variable — there is no TSS/RSS to decompose. Instead, McFadden $R^2$ measures **the degree of log-likelihood improvement** of the full model relative to the intercept-only model (null model) — a quantity living in probability/likelihood space, not variance space.</span>

Hệ quả quan trọng: **giá trị McFadden $R^2$ không thể so sánh trực tiếp về thang đo với $R^2$ OLS**. Một mô hình MNL với $R^2_{McFadden}\approx 0.08$ — như case study này — hoàn toàn có thể là một mô hình "tốt" theo tiêu chuẩn riêng của các mô hình ML, dù con số này trông rất thấp nếu so với kỳ vọng "$R^2$ tốt phải trên 0.6–0.7" quen thuộc từ OLS.
<br><span class="en">An important consequence: **the McFadden $R^2$ value cannot be directly compared on the same scale as OLS $R^2$**. An MNL model with $R^2_{McFadden}\approx 0.08$ — as in this case study — can perfectly well be a "good" model by the standards specific to ML models, even though this number looks very low compared to the familiar OLS expectation that "a good $R^2$ should be above 0.6–0.7".</span>

### 10.3 Ngưỡng đánh giá thường dùng - <span class="en">Commonly used evaluation thresholds</span>

Theo hướng dẫn kinh điển của McFadden (được trích dẫn rộng rãi trong các giáo trình discrete choice, không phải trực tiếp từ slide này), $R^2_{McFadden}$ trong khoảng **0.2–0.4** đã được coi là mức khớp **rất tốt** — thấp hơn nhiều so với ngưỡng "tốt" quen thuộc của $R^2$ OLS.
<br><span class="en">According to McFadden's classic guideline (widely cited in discrete-choice textbooks, not directly from this slide), $R^2_{McFadden}$ in the range **0.2–0.4** is already considered a **very good** fit — much lower than the familiar "good" threshold for OLS $R^2$.</span>

**Điểm quan trọng nhất từ case study**: mô hình MNL ở đây có $R^2_{McFadden}\approx 0.08$ — thấp hơn cả ngưỡng 0.2 — trong khi LR test tổng thể (mục 8.2) bác bỏ $H_0$ cực mạnh ($p\approx 0$). Đây là minh chứng sống động cho bài học đã nêu ở [[concepts/linear-regression-model]] mục 9: **"có ý nghĩa thống kê" (statistical significance) và "độ khớp tốt về mặt độ lớn" (fit magnitude) là hai chuyện hoàn toàn khác nhau** — một tập biến giải thích có thể ảnh hưởng thật (LR test rất có ý nghĩa) nhưng vẫn chỉ giải thích được một phần nhỏ trong toàn bộ log-likelihood cần cải thiện (vì hành vi lựa chọn nơi khám chữa bệnh còn phụ thuộc nhiều yếu tố không quan sát được — bệnh cụ thể, khoảng cách địa lý thực tế, chất lượng dịch vụ cảm nhận…).
<br><span class="en">**The most important point from the case study**: the MNL model here has $R^2_{McFadden}\approx 0.08$ — below even the 0.2 threshold — while the overall LR test (section 8.2) rejects $H_0$ extremely strongly ($p\approx 0$). This is a vivid illustration of the lesson already stated in [[concepts/linear-regression-model]] section 9: **"statistical significance" and "fit magnitude" are two completely different things** — a set of explanatory variables can have a genuine effect (LR test highly significant) yet still explain only a small fraction of the total log-likelihood that could be improved (because the behavior of choosing a healthcare provider also depends on many unobserved factors — the specific illness, actual geographic distance, perceived service quality…).</span>

## 11. Bẫy thi - <span class="en">Exam traps</span>

1. Diễn giải hệ số $\beta_j$ dương như "xác suất chọn $j$ tăng" — sai; $\beta_j$ chỉ đo thay đổi **log-odds so với base category**, không phải thay đổi trực tiếp $P(Y=j)$ (xem ví dụ số ở mục 7.3 — hệ số gần 0 vẫn có thể đi kèm marginal effect khác 0 rõ rệt, và ngược lại).
<br><span class="en">1. Interpreting a positive coefficient $\beta_j$ as "the probability of choosing $j$ increases" — wrong; $\beta_j$ only measures the change in **log-odds relative to the base category**, not a direct change in $P(Y=j)$ (see the numeric example in section 7.3 — a coefficient near 0 can still come with a clearly nonzero marginal effect, and vice versa).</span>
2. Nghĩ rằng base category "không bị ảnh hưởng gì" bởi $X$ vì hệ số của nó "bằng 0 theo định nghĩa" — sai; marginal effect trên $P(\text{base category})$ thường **khác 0**, và trong case study còn là marginal effect **lớn nhất** trong tất cả (insurance → +0.17 trên $P(\text{Public hospital})$).
<br><span class="en">2. Thinking the base category is "unaffected" by $X$ because its coefficient is "0 by definition" — wrong; the marginal effect on $P(\text{base category})$ is usually **nonzero**, and in the case study it is even the **largest** marginal effect of all (insurance → +0.17 on $P(\text{Public hospital})$).</span>
3. Đổi base category rồi coi hệ số "đổi dấu/đổi độ lớn" là dấu hiệu mô hình "không ổn định" — sai; đổi base chỉ đổi điểm tham chiếu diễn giải, xác suất dự đoán (fitted probabilities) không đổi.
<br><span class="en">3. Changing the base category and treating the coefficients "changing sign/magnitude" as a sign the model is "unstable" — wrong; changing the base only changes the interpretation reference point, the fitted probabilities do not change.</span>
4. Kỳ vọng McFadden $R^2$ đạt mức cao như $R^2$ OLS (0.6–0.9) — sai chuẩn so sánh; McFadden $R^2$ trong khoảng 0.2–0.4 đã được coi là khớp tốt, và ngay cả mô hình có LR test rất có ý nghĩa vẫn có thể có McFadden $R^2$ thấp (case study: 0.08).
<br><span class="en">4. Expecting McFadden $R^2$ to reach the high levels typical of OLS $R^2$ (0.6–0.9) — wrong comparison standard; McFadden $R^2$ in the range 0.2–0.4 is already considered a good fit, and even a model with a highly significant LR test can still have a low McFadden $R^2$ (case study: 0.08).</span>
5. Coi LR test tổng thể có ý nghĩa thống kê là "mọi hệ số trong mô hình đều có ý nghĩa riêng lẻ" — sai, giống hệt bẫy F-test ở [[concepts/linear-regression-model]] mục 8.4: LR test chỉ khẳng định "ít nhất một" hệ số khác 0, muốn biết từng hệ số phải quay lại z-test.
<br><span class="en">5. Treating a statistically significant overall LR test as meaning "every coefficient in the model is individually significant" — wrong, exactly the same trap as the F-test in [[concepts/linear-regression-model]] section 8.4: the LR test only confirms "at least one" coefficient is nonzero; to know about each individual coefficient you must go back to the z-test.</span>
6. Nhầm MNL (nominal, không thứ tự) với Ordinal response model (có thứ tự) — hai mô hình khác nhau về bản chất bài toán lẫn cách ước lượng; xem [[concepts/ordinal-response-models]].
<br><span class="en">6. Confusing MNL (nominal, unordered) with the Ordinal response model (ordered) — the two models differ fundamentally both in the nature of the problem and in estimation; see [[concepts/ordinal-response-models]].</span>
7. Dùng phân phối Student-$t$ để tính $p$-value cho hệ số MNL — sai; MNL ước lượng bằng ML nên dùng phân phối chuẩn tiệm cận ($z$-test), không phải $t$-test hữu hạn mẫu của OLS.
<br><span class="en">7. Using the Student-$t$ distribution to compute the $p$-value for an MNL coefficient — wrong; MNL is estimated by ML, so it uses the asymptotic normal distribution ($z$-test), not OLS's finite-sample $t$-test.</span>
8. Coi việc mô hình dự đoán đúng phần lớn quan sát (nhờ luôn chọn category phổ biến nhất) là bằng chứng mô hình khớp tốt cho mọi category — bỏ qua khả năng mô hình gần như không bao giờ dự đoán đúng cho các category thiểu số; cần đối chiếu với kiểm định goodness-of-prediction (mục 9).
<br><span class="en">8. Treating a model that correctly predicts most observations (by always picking the most popular category) as evidence it fits every category well — ignoring the possibility that the model almost never predicts the minority categories correctly; this needs to be checked against the goodness-of-prediction test (section 9).</span>
9. Diễn giải hệ số không có ý nghĩa thống kê (p lớn, VD `insurance` cho Commune health center, p=0.886) là "chắc chắn bằng 0/không có ảnh hưởng gì" — chỉ là "không đủ bằng chứng bác bỏ $H_0:\beta=0$", không phải "đã chứng minh $\beta=0$" (cùng nguyên tắc ở [[concepts/linear-regression-model]] mục 7.5).
<br><span class="en">9. Interpreting a statistically non-significant coefficient (large p, e.g. `insurance` for Commune health center, p=0.886) as "definitely zero/no effect at all" — it only means "insufficient evidence to reject $H_0:\beta=0$", not "$\beta=0$ has been proven" (the same principle as in [[concepts/linear-regression-model]] section 7.5).</span>

## 12. Kết nối với phần còn lại của khóa học - <span class="en">Connections to the rest of the course</span>

- MNL là **mở rộng trực tiếp** của [[concepts/binary-response-models]]: khi $J=2$, công thức softmax ở mục 5 thu gọn đúng về hàm logistic quen thuộc của Logit nhị phân (base category chính là outcome $=0$).
<br><span class="en">MNL is a **direct extension** of [[concepts/binary-response-models]]: when $J=2$, the softmax formula in section 5 collapses exactly into the familiar logistic function of binary Logit (the base category is precisely the outcome $=0$).</span>
- Phân biệt rõ với [[concepts/ordinal-response-models]] (Topic 9) — khi các phạm trù **có** thứ tự tự nhiên, dùng Ordered Logit/Probit với cơ chế cutpoints thay vì base category kiểu MNL; dùng nhầm MNL cho dữ liệu có thứ tự (hoặc ngược lại) là lãng phí thông tin về trật tự hoặc áp đặt sai một trật tự không tồn tại.
<br><span class="en">Clearly distinguished from [[concepts/ordinal-response-models]] (Topic 9) — when categories **do** have a natural order, use Ordered Logit/Probit with a cutpoints mechanism instead of MNL-style base categories; wrongly using MNL for ordered data (or vice versa) either wastes ordering information or imposes an order that doesn't exist.</span>
- Logic **LR test (unrestricted vs. restricted)** ở mục 8 song song hoàn toàn với **F-test** của OLS ([[concepts/linear-regression-model]] mục 8) — cùng một tư duy so sánh mô hình, khác thống kê kiểm định vì khác nền tảng ước lượng (ML vs. OLS).
<br><span class="en">The **LR test (unrestricted vs. restricted)** logic in section 8 parallels OLS's **F-test** entirely ([[concepts/linear-regression-model]] section 8) — the same model-comparison mindset, differing only in the test statistic because of the different estimation foundation (ML vs. OLS).</span>
- **McFadden $R^2$** là một dạng "pseudo-$R^2$" dùng chung cho mọi mô hình ước lượng bằng Maximum Likelihood — sẽ gặp lại đúng logic này (và đúng bài học "significance ≠ fit magnitude") ở [[concepts/ordinal-response-models]] và các mô hình đếm (count data models) học sau trong khóa.
<br><span class="en">**McFadden $R^2$** is a form of "pseudo-$R^2$" shared by every model estimated via Maximum Likelihood — this exact same logic (and the exact same "significance ≠ fit magnitude" lesson) will reappear in [[concepts/ordinal-response-models]] and the count data models covered later in the course.</span>
- Việc **base category** buộc mọi hệ số phải diễn giải tương đối là cùng một nguyên lý với biến phân loại (categorical) trong OLS ([[concepts/linear-regression-model]] mục 5) — chỉ khác ở chỗ MNL áp dụng nguyên lý đó cho *toàn bộ hệ* $(J-1)$ phương trình đồng thời, thay vì một phương trình duy nhất.
<br><span class="en">The way a **base category** forces every coefficient to be interpreted relatively is the same principle as categorical variables in OLS ([[concepts/linear-regression-model]] section 5) — the only difference is that MNL applies that principle to an *entire system* of $(J-1)$ equations simultaneously, instead of a single equation.</span>

## 11. Tài liệu tham khảo ứng dụng thực tế - <span class="en">Real-world application references</span>

Ba bài báo gần đây minh họa multinomial logit model trong nghiên cứu kinh tế thực tế (đề cương Lecture 10):
<br><span class="en">Three recent papers illustrating the multinomial logit model in real-world economic research (Lecture 10 syllabus):</span>

- Alem, Y., Beyene, A. D., Köhlin, G., & Mekonnen, A. (2016). Modeling household cooking fuel choice: A panel multinomial logit approach. *Energy Economics*, 59, 129-137. https://doi.org/10.1016/j.eneco.2016.06.025
- Mostofi, H. (2022). The frequency use and the modal shift to ICT-based mobility services. *Resources, Environment and Sustainability*, 9. https://doi.org/10.1016/j.resenv.2022.100076
- Fikire, A. H. (2021). Determinants of urban housing choice in Debre Berhan Town, North Shewa zone, Amhara Region, Ethiopia. *Cogent Economics & Finance*, 9(1). https://doi.org/10.1080/23322039.2021.1885196
