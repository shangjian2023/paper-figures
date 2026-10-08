---
title: Nature 云雨图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 5区域×样本年代值
input: long (reference/data-schemas.json #025)
journal: Nature
recipe: scripts/recipes/case_seg025.py
preview: ../case_seg025.png
---

**一句话**：堆叠云雨图（Nature 风格）

**部件亮点**
- 结构布局：5行纵向堆叠云雨
- 编码方式：上半填充KDE山脊,下半箱线图,下挂雨滴;X=kyr BP反转15→0;蓝/卡其/绿/红/黑;区域名左上

**复现**：配方 `scripts/recipes/case_seg025.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
