---
title: Microbiome Upset图(一)
kind: 数据图
purpose: [网络与流向]
data: 8集合元素交集计数
input: sets (reference/data-schemas.json #114)
journal: Microbiome
wow: 2
recipe: scripts/recipes/case_seg114.py
preview: ../case_seg114.png
---

**一句话**：UpSet图（Microbiome 风格）

**高级感**：★★ 有设计感

**适用场景**：4-8 个集合（各时间点/处理组的 DEG、物种或通路列表）之间的交集与特有元素数量要一张图讲清，Venn 图已画不下

**有什么用**：几组基因清单之间谁和谁共享、共享多少，用一排柱子直接标数：柱子越高交集越大，下方的圆点标明这个交集由哪几组构成。清单超过三四个、韦恩图画不下时就用它。

**部件亮点**
- 结构布局：单面板
- 编码方式：顶部交集条形+数值,左侧setSize条形,8集合点阵连线;彩色版紫/橙条;用 helpers.upset.upset_plot_pro

**复现**：配方 `scripts/recipes/case_seg114.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
