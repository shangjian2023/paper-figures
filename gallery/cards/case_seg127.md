---
title: PNAS 三元图(4)
kind: 数据图
purpose: [构成占比, 相关关系]
data: OTU三维丰度+富集归属
input: long (reference/data-schemas.json #127)
journal: PNAS
recipe: scripts/recipes/case_seg127.py
preview: ../case_seg127.png
---

**一句话**：三元气泡图（PNAS 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：气泡面积=丰度;颜色=富集生境(红/橙/绿),未富集灰;顶点标Nodule/Root/Rhizosphere计数

**复现**：配方 `scripts/recipes/case_seg127.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
