---
title: Nature 环状折线图
kind: 数据图
purpose: [多指标综合, 趋势变化]
data: 指标×4组z-score长表
input: long (reference/data-schemas.json #095)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg095.py
preview: ../case_seg095.png
---

**一句话**：环状折线图（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：3-6 组对象 × 几十个有序指标（约 40-80）的 z 分数，想把各组折线叠在同一个环上比较组间轮廓

**有什么用**：四个患者亚组各用一条彩线绕同一个环，比较几十项指标上的整体轮廓：哪组在哪一段整体偏高、哪几组走势接近或交叉，一圈看完。

**部件亮点**
- 结构布局：单面板
- 编码方式：4组线(蓝/橙/黄/粉)带圆点标记沿60指标环形排布,径向±1.5刻度,中心圆分区注释

**复现**：配方 `scripts/recipes/case_seg095.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
