---
title: Nature 点线图
kind: 数据图
purpose: [趋势变化]
data: 16温度×频率扫描数值
input: long (reference/data-schemas.json #132)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg132.py
preview: ../case_seg132.png
---

**一句话**：点线图(普通vs顶刊对比)（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：十几条到几十条曲线共享同一 x 轴（频率扫描、温度系列 52K-100K），想按参数彩虹着色分层

**有什么用**：同一族曲线画两遍做对比：上面是随手画的普通版，下面是打磨过的出版版——横轴改对数、曲线按温度彩虹排色、点线更讲究；照着下面那张改进自己的多曲线图。

**部件亮点**
- 结构布局：上下两面板对比
- 编码方式：上:线性x多彩曲线;下:log x,16条温度曲线52K-100K彩虹着色,空心/实心点+平滑线,右列图例

**复现**：配方 `scripts/recipes/case_seg132.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
