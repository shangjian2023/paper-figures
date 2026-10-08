---
title: Nature 气泡图
kind: 数据图
purpose: [相关关系]
data: motif×layer比例矩阵
input: long (reference/data-schemas.json #105)
journal: Nature
recipe: scripts/recipes/case_seg105.py
preview: ../case_seg105.png
---

**一句话**：气泡图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：x=18皮层柱,y=18抑制基序;气泡4档=Frac Syn,颜色随皮层彩虹渐变,灰竖线分层,右侧大小图例

**复现**：配方 `scripts/recipes/case_seg105.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
