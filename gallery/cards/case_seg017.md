---
title: Nature 分面山脊图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 12标记×9亚群×单细胞表达
input: long (reference/data-schemas.json #017)
journal: Nature
recipe: scripts/recipes/case_seg017.py
preview: ../case_seg017.png
---

**一句话**：分面山脊图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：6列标记分面×8行亚群山脊,色按c1-c8(紫蓝绿黄);每格竖线=中位数;底部2个放大分面;X=Expression

**复现**：配方 `scripts/recipes/case_seg017.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
