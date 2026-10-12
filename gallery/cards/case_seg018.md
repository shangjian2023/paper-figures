---
title: Nature 分组+分面山脊图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 4细胞因子×9亚群×荧光强度
input: long (reference/data-schemas.json #018)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg018.py
preview: ../case_seg018.png
---

**一句话**：分组分面山脊图（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：流式胞内染色：4-6 个细胞因子各占一列分面，6-10 个亚群在未刺激(−)/刺激(+)下各一条荧光强度分布

**有什么用**：七种免疫细胞在刺激前后各画一条密度小山，按四种因子分列；未刺激的小山靠左、刺激后右移，一眼看出哪类细胞被激活后分泌哪种因子。

**部件亮点**
- 结构布局：单面板
- 编码方式：4列细胞因子分面×9行亚群;行左+/−标记,色按ILC3至LT-ILC1(绿蓝灰青红紫粉);右侧彩色图例;对数X轴

**复现**：配方 `scripts/recipes/case_seg018.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
