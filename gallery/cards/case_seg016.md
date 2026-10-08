---
title: Nature 分组山脊图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 2组×6时间点×RMSD分布
input: long (reference/data-schemas.json #016)
journal: Nature
recipe: scripts/recipes/case_seg016.py
preview: ../case_seg016.png
---

**一句话**：分组山脊图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：6条分布水平堆叠,绿系与紫系两版,0ns→24ns峰右移;仅顶部填充+底部细基线;X=Core RMSD

**复现**：配方 `scripts/recipes/case_seg016.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
