---
title: "Introduction to Econometrics"
type: source
raw_file: "raw/SLIDES/VNP2026-intro.pdf"
pages: 22
topic: 0
status: current
ingested: 2026-07-29
concepts: ["[[concepts/econometrics-overview]]"]
---

## Vai trò của tài liệu này - <span class="en">Role of this document</span>

Slide bài giảng đầu tiên (Topic 0 trong Course Outline) của **[[people/truong-dang-thuy|Trương Đăng Thụy]]**. Đặt nền móng khái niệm cho toàn bộ khóa học: econometrics là gì, tại sao correlation ≠ causality, và quy trình nghiên cứu thực nghiệm. Không có công thức ước lượng nào ở bài này — thuần khái niệm và ví dụ minh họa (giá điện, bão, giáo dục–lương, cứu hỏa, cướp biển).
<br><span class="en">The first lecture deck (Topic 0 in the Course Outline) by **[[people/truong-dang-thuy|Trương Đăng Thụy]]**. Lays the conceptual groundwork for the whole course: what econometrics is, why correlation ≠ causality, and the empirical research process. No estimation formulas in this deck — purely conceptual, with illustrative examples (electricity prices, storms, education–wages, firefighters, pirates).</span>

## Mạch nội dung (narrative) - <span class="en">Content flow (narrative)</span>

1. **Why econometrics?** — kinh tế học đề xuất lý thuyết về hành vi cá nhân/doanh nghiệp/thị trường; cần dữ liệu để kiểm định các lý thuyết đó.
   <br><span class="en">**Why econometrics?** — economics proposes theories about individual/firm/market behavior; data is needed to test those theories.</span>
2. **What is econometrics?** — kết hợp 3 yếu tố: economic theory (đưa ra giả thuyết) + mathematical models (biểu diễn hình thức) + statistical methods (ước lượng, kiểm định).
   <br><span class="en">**What is econometrics?** — combines 3 elements: economic theory (proposes hypotheses) + mathematical models (formalizes them) + statistical methods (estimation, testing).</span>
3. **Econometrics vs. Statistics** — thống kê tập trung mô tả/dự báo pattern trong dữ liệu; econometrics tập trung vào **cơ chế kinh tế** và **suy luận nhân quả (causal inference)**.
   <br><span class="en">**Econometrics vs. Statistics** — statistics focuses on describing/predicting patterns in data; econometrics focuses on **economic mechanisms** and **causal inference**.</span>
4. **Statistical association** — hai biến "đi cùng nhau" không có nghĩa biến này gây ra biến kia.
   <br><span class="en">**Statistical association** — two variables "moving together" does not mean one causes the other.</span>
5. **Association vs. Causality** — ba lý do khiến association gây hiểu lầm: *confounding variables*, *reverse causality*, *coincidence* (mỗi loại có ví dụ minh họa cụ thể).
   <br><span class="en">**Association vs. Causality** — three reasons association can mislead: *confounding variables*, *reverse causality*, *coincidence* (each with a concrete illustrative example).</span>
6. **Ví dụ kinh tế**: `wage = β0 + β1·education + u` — ability, gia đình, mạng lưới xã hội là confounder ẩn trong `u`, khiến `education` tương quan với sai số → `β̂1` ước lượng cả hiệu ứng education lẫn ability.
   <br><span class="en">**Economic example**: `wage = β0 + β1·education + u` — ability, family, and social networks are confounders hidden inside `u`, making `education` correlated with the error term → `β̂1` ends up estimating a mix of the education effect and the ability effect.</span>
7. **Ceteris paribus** — hiệu ứng của một biến khi các biến khác giữ nguyên; đây là điều mỗi hệ số hồi quy `bⱼ` cố gắng nắm bắt.
   <br><span class="en">**Ceteris paribus** — the effect of one variable holding the others constant; this is what every regression coefficient `bⱼ` tries to capture.</span>
8. **Omitted variable bias** — bỏ sót biến quan trọng (không quan sát được) làm hệ số ước lượng bị chệch.
   <br><span class="en">**Omitted variable bias** — leaving out an important (unobserved) variable biases the estimated coefficient.</span>
9. **Identification problem** — bài toán trung tâm của econometrics: tìm được phần biến thiên (variation) trong biến giải thích *không* bị chi phối bởi yếu tố gây nhiễu. Ví dụ: giá điện tăng đồng loạt do chính sách chính phủ (không phụ thuộc đặc điểm hộ gia đình) mới giúp nhận diện được hiệu ứng nhân quả của giá lên tiêu thụ điện.
   <br><span class="en">**Identification problem** — the central problem of econometrics: finding the part of the variation in a regressor that is *not* driven by confounding factors. Example: only an across-the-board electricity price hike from government policy (independent of household characteristics) lets us identify the causal effect of price on consumption.</span>
10. **Causal inference: kinh tế học vs. khoa học tự nhiên** — khoa học tự nhiên dùng controlled experiments (random assignment) để cô lập nhân quả; kinh tế học hiếm khi làm được (không thể random hóa số năm đi học hay hệ thống thuế) → phải dựa vào observational data và các phương pháp nhận diện gián tiếp.
    <br><span class="en">**Causal inference: economics vs. natural science** — natural science uses controlled experiments (random assignment) to isolate causality; economics can rarely do this (you cannot randomize years of schooling or a tax system) → it must rely on observational data and indirect identification strategies.</span>
11. **Empirical research process** — 6 bước: (1) research question → (2) economic theory → (3) empirical model → (4) data → (5) econometric analysis → (6) interpretation & policy implications.
    <br><span class="en">**Empirical research process** — 6 steps: (1) research question → (2) economic theory → (3) empirical model → (4) data → (5) econometric analysis → (6) interpretation & policy implications.</span>
12. **3 câu hỏi nền tảng** khi làm nghiên cứu thực nghiệm: What is the economic question? What is the economic mechanism? Can the causal effect be identified in the data?
    <br><span class="en">**3 foundational questions** for empirical research: What is the economic question? What is the economic mechanism? Can the causal effect be identified in the data?</span>
13. **Common mistakes**: coi association là causation; mặc định regression tự động cho ra hiệu ứng nhân quả; tập trung vào ước lượng (estimation) mà quên mất bài toán identification.
    <br><span class="en">**Common mistakes**: treating association as causation; assuming regression automatically produces a causal effect; focusing on estimation while forgetting the identification problem.</span>
14. **Preview khóa học** — 3 phần chính: (a) Linear Regression Model và các vấn đề của nó (OLS, multicollinearity, heteroskedasticity, endogeneity); (b) Models for Limited Dependent Variables (logit/probit, multinomial logit, Poisson/NB, ordinal, censored/truncated); (c) Panel data models (FE/RE, IV cho panel: 2SLS/LIML/GMM, dynamic panel).
    <br><span class="en">**Course preview** — 3 main parts: (a) the Linear Regression Model and its problems (OLS, multicollinearity, heteroskedasticity, endogeneity); (b) Models for Limited Dependent Variables (logit/probit, multinomial logit, Poisson/NB, ordinal, censored/truncated); (c) Panel data models (FE/RE, panel IV: 2SLS/LIML/GMM, dynamic panel).</span>
15. **Nền tảng học tập**: econometrics.site — luyện tập, làm assignment, nộp project.
    <br><span class="en">**Course platform**: econometrics.site — practice, assignments, project submission.</span>

## Ghi chú - <span class="en">Note</span>

Toàn bộ nội dung khái niệm của bài này đã được tổng hợp vào `[[concepts/econometrics-overview]]` — trang đó là nơi chứa synthesis đầy đủ (định nghĩa, ví dụ, bảng so sánh). Trang này chỉ giữ vai trò ghi nhận nguồn và mạch trình bày gốc của slide.
<br><span class="en">All the conceptual content of this deck has been synthesized into `[[concepts/econometrics-overview]]` — that page holds the full synthesis (definitions, examples, comparison tables). This page only records provenance and the original slide's narrative flow.</span>
