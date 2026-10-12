---
title: Clin.Transl.Med Upset图(二)
kind: 数据图
purpose: [网络与流向]
data: 8组DEG交集矩阵
input: sets (reference/data-schemas.json #115)
journal: Clin.Transl.Med
wow: 2
recipe: scripts/recipes/case_seg115.py
preview: ../case_seg115.png
---

**一句话**：UpSet图（Clin.Transl.Med 风格）

**高级感**：★★ 有设计感

**适用场景**：8 个左右的两两比较（如各癌期 vs 早期、转移 vs 未转移）各自得到一个 DEG 列表，想看这些比较之间共享与独有的基因数

**有什么用**：八组比较各有一份差异清单，这张图回答'谁和谁共享、共享多少'：上方柱子是每种共享组合的基因数并标了数字，左边小条是各清单自己的总数。适合放进补充材料做总览。

**部件亮点**
- 结构布局：单面板
- 编码方式：交集条形计数330~4,点阵圆点连线8组,左侧setSize条;蓝/红条+行背景渐变+空心点阵

**复现**：配方 `scripts/recipes/case_seg115.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
