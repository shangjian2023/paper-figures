---
title: Nature 云雨图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 5区域×样本年代值
input: long (reference/data-schemas.json #025)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg025.py
preview: ../case_seg025.png
---

**一句话**：堆叠云雨图（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：4-6 组各自几百上千个观测，按行纵向堆叠比较分布的位置和形态

**有什么用**：每个地区一层：上面是分布轮廓的“云”，中间是箱线图，下面挂着一条条像雨滴的原始数据；一眼看出哪组偏新、哪组偏老、散得开不开。

**部件亮点**
- 结构布局：5行纵向堆叠云雨
- 编码方式：上半填充KDE山脊,下半箱线图,下挂雨滴;X=kyr BP反转15→0;蓝/卡其/绿/红/黑;区域名左上

**复现**：配方 `scripts/recipes/case_seg025.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
