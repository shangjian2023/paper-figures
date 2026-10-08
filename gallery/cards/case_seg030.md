---
title: Cell 箱线图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 4年龄类×2组×dN/dS值
input: long (reference/data-schemas.json #030)
journal: Cell
recipe: scripts/recipes/case_seg030.py
preview: ../case_seg030.png
---

**一句话**：分面箱线图（Cell 风格）

**部件亮点**
- 结构布局：4个独立分面箱线
- 编码方式：灰 vs 彩色箱线;面板底色对应年龄渐变;含须线;顶部P值横线;彩色标题条;X标签斜排

**复现**：配方 `scripts/recipes/case_seg030.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
