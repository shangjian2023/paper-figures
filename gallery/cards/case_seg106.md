---
title: Cell 热图(一)
kind: 数据图
purpose: [相关关系]
data: 状态×因子active/repressed%+显著性
input: matrix (reference/data-schemas.json #106)
journal: Cell
wow: 1
recipe: scripts/recipes/case_seg106.py
preview: ../case_seg106.png
---

**一句话**：多面板热图（Cell 风格）

**高级感**：★ 常规扎实

**适用场景**：同一批 行(细胞状态/样本)×列(转录因子/因子组合) 有两个互补测量：%active 和 %repressed，上下两排热图各用独立色标（激活橙黑、抑制蓝绿）

**有什么用**：颜色越亮代表调控作用越强：上排看每个因子对每类细胞的激活程度，下排看抑制程度，带白点的格子是统计上可靠的。下方还有一块放大图细看单因子效果。

**部件亮点**
- 结构布局：2行×3列+下方放大面板
- 编码方式：激活橙黑渐变、抑制蓝绿渐变,白点=显著,底部因子分类色条,右侧两色标

**复现**：配方 `scripts/recipes/case_seg106.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
