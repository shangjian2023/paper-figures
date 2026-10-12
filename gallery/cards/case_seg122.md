---
title: Nature 带显著性的小提琴图(二)
kind: 数据图
purpose: [分布形态, 组间比较]
data: 长表:10亚群×2状态×百分比
input: long (reference/data-schemas.json #122)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg122.py
preview: ../case_seg122.png
---

**一句话**：双面板小提琴+星号（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：约 10 个亚群或标志物 × 2 状态（如 EBV 阴性 vs 阳性）的占比比较，一排放不下分上下两个面板

**有什么用**：十个免疫亚群并排两把小提琴，比较 EBV 阴性与阳性者的细胞占比，每对上方标三星表示差异显著，底部横线把亚群归入大类；扫一眼就知道几乎所有亚群都有差异。

**部件亮点**
- 结构布局：上下两面板各10组×2小提琴
- 编码方式：***星号+括号;底部CD4/Treg/CD8分组横线;图例右上;内嵌散点

**复现**：配方 `scripts/recipes/case_seg122.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
