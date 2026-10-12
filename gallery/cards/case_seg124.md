---
title: Cell 三元图(1)
kind: 数据图
purpose: [构成占比, 相关关系]
data: 每细胞三维归一化得分+分组
input: long (reference/data-schemas.json #124)
journal: Cell
wow: 2
recipe: scripts/recipes/case_seg124.py
preview: ../case_seg124.png
---

**一句话**：三元散点图（Cell 风格）

**高级感**：★★ 有设计感

**适用场景**：每个细胞/样本有三个互斥状态得分且和为 100%，想看它在三角形里的命运归属位置

**有什么用**：每个细胞按三种命运打分放进一个三角形，点越靠哪个角就越像哪种命运；大图看全体落点，下面三张小图看群体随时间往哪个角迁移。

**部件亮点**
- 结构布局：上1大+下排3小
- 编码方式：顶点EPI/PrE/TE标100;散点按归属橙/蓝/绿;彩色虚线网格20-80;三边彩箭头;用 helpers.ternary.Ternary

**复现**：配方 `scripts/recipes/case_seg124.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
