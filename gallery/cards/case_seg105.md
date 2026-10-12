---
title: Nature 气泡图
kind: 数据图
purpose: [相关关系]
data: motif×layer比例矩阵
input: matrix (reference/data-schemas.json #105)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg105.py
preview: ../case_seg105.png
---

**一句话**：气泡图（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：行=基序/基因/条目（约 18 行）、列=皮层/层级/条件（约 18 列）的矩阵值，用气泡大小编码比例并分 4 档（<5%、5-15%、15-30%、≥30%）

**有什么用**：哪里有气泡、泡有多大，就代表那个行条目在那个位置出现、占多大比例；空白处就是没有。整片气泡排成一条斜带，规律一眼可见。

**部件亮点**
- 结构布局：单面板
- 编码方式：x=18皮层柱,y=18抑制基序;气泡4档=Frac Syn,颜色随皮层彩虹渐变,灰竖线分层,右侧大小图例

**复现**：配方 `scripts/recipes/case_seg105.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
