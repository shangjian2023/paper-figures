---
title: PNAS 三元图(4)
kind: 数据图
purpose: [构成占比, 相关关系]
data: OTU三维丰度+富集归属
input: long (reference/data-schemas.json #127)
journal: PNAS
wow: 3
recipe: scripts/recipes/case_seg127.py
preview: ../case_seg127.png
---

**一句话**：三元气泡图（PNAS 风格）

**高级感**：★★★ 镇场级（用户要"高级/惊艳"时优先摆）

**适用场景**：OTU/物种/基因在三个生境（如根际-根-根瘤）中的丰度占比，想知道谁显著富集在哪个生境

**有什么用**：每个物种画成一个气泡放进三角形：越靠哪个角就越富集在哪个部位，气泡越大数量越多；富集物种上色、其余灰化，一眼看出谁扎堆在哪。

**部件亮点**
- 结构布局：单面板
- 编码方式：气泡面积=丰度;颜色=富集生境(红/橙/绿),未富集灰;顶点标Nodule/Root/Rhizosphere计数

**复现**：配方 `scripts/recipes/case_seg127.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
