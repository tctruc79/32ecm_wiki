---
title: "Anderson-Hsiao / Arellano-Bond / Arellano-Bover-Blundell-Bond"
type: person
role: "Dòng ước lượng GMM cho dynamic panel data"
tags: [dynamic-panel, gmm, arellano-bond, blundell-bond]
---

Chuỗi đóng góp liên tiếp giải quyết **Nickell bias** trong mô hình panel động (xem [[concepts/dynamic-panel-data-models]]):
<br><span class="en">A sequence of successive contributions solving the **Nickell bias** problem in dynamic panel models (see [[concepts/dynamic-panel-data-models]]):</span>

- **Anderson & Hsiao (1981, 1982)** — first-difference + instrument nội tại đơn lẻ ($y_{i,t-2}$ hoặc $\Delta y_{i,t-2}$), just-identified.
  <br><span class="en">**Anderson & Hsiao (1981, 1982)** — first-difference + a single internal instrument ($y_{i,t-2}$ or $\Delta y_{i,t-2}$), just-identified.</span>
- **Arellano & Bond (1991)** — mở rộng thành **Difference GMM**, dùng nhiều lag làm instrument cùng lúc, tăng hiệu quả.
  <br><span class="en">**Arellano & Bond (1991)** — extends this into **Difference GMM**, using multiple lags as instruments simultaneously, increasing efficiency.</span>
- **Arellano & Bover (1995)** — đề xuất ý tưởng kết hợp phương trình sai phân và phương trình mức thành một hệ thống.
  <br><span class="en">**Arellano & Bover (1995)** — proposes stacking the differenced equation and the levels equation into one system.</span>
- **Blundell & Bond (1998)** — hình thức hóa điều kiện moment cho **System GMM**, đảm bảo tính vững (đặc biệt khi $y$ có tính bền vững cao).
  <br><span class="en">**Blundell & Bond (1998)** — formalizes the moment conditions for **System GMM**, ensuring consistency (especially when $y$ is highly persistent).</span>

Đều được trích dẫn trong Course Outline như tài liệu đọc chính cho Topic 14, cùng với Roodman (2009, hướng dẫn `xtabond2`) và Windmeijer (2005, hiệu chỉnh phương sai two-step GMM).
<br><span class="en">All are cited in the Course Outline as the main readings for Topic 14, along with Roodman (2009, an `xtabond2` guide) and Windmeijer (2005, a two-step GMM variance correction).</span>

## Xuất hiện trong

- [[concepts/dynamic-panel-data-models]]
