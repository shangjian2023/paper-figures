---
title: Nature 分组+分面山脊图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 4细胞因子×9亚群×荧光强度
input: long (reference/data-schemas.json #018)
journal: Nature
recipe: scripts/recipes/case_seg018.py
preview: ../case_seg018.png
---

**一句话**：分组分面山脊图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：4列细胞因子分面×9行亚群;行左+/−标记,色按ILC3至LT-ILC1(绿蓝灰青红紫粉);右侧彩色图例;对数X轴

**复现**：配方 `scripts/recipes/case_seg018.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
