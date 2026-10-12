---
title: Nature 圆形雷达图
kind: 数据图
purpose: [多指标综合]
data: 5聚类×22指标均值
input: long (reference/data-schemas.json #058)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg058.py
preview: ../case_seg058.png
---

**一句话**：多雷达+放大面板（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：5-8 个聚类/亚组各用 15-25 个相同指标（如临床代谢 panel：血压血糖血脂肝肾功能）画均值画像，一排小雷达每类一格+顶部色条标题

**有什么用**：五类人群各占一格小雷达，二十多项体检指标一次画完，偏离明显的指标用彩色标出，下方再放大一类细看，各类代谢模式一张图扫完。

**部件亮点**
- 结构布局：上排5小雷达+下方放大
- 编码方式：每雷达22指标放射轴,细线多边形+浅填充+顶点点;显著偏离指标标红/橙;顶部色条标题(绿/蓝/橙/红/紫)

**复现**：配方 `scripts/recipes/case_seg058.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
