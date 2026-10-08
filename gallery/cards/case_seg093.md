---
title: Nature 扇形&箱线图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 分组连续数据长表
input: long (reference/data-schemas.json #093)
journal: Nature
recipe: scripts/recipes/case_seg093.py
preview: ../case_seg093.png
---

**一句话**：扇形极坐标箱线图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：约12组沿扇形排列,箱线+抖动散点,浅灰同心网格,顶部弧形类目标签,中心留白孔

**复现**：配方 `scripts/recipes/case_seg093.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
