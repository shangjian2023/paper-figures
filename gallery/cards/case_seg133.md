---
title: Cell 环形热图
kind: 数据图
purpose: [网络与流向]
data: 基因×5样本矩阵+通路分组;交集矩阵
input: matrix (reference/data-schemas.json #133)
journal: Cell
wow: 3
recipe: scripts/recipes/case_seg133.py
preview: ../case_seg133.png
---

**一句话**：环形热图+UpSet内嵌（Cell 风格）

**高级感**：★★★ 镇场级（用户要"高级/惊艳"时优先摆）

**适用场景**：基因×样本表达矩阵且基因按通路分成 6 组左右，想用外圈弧形热图+中心 UpSet 交集一图两用

**有什么用**：把约 50 个基因按 6 条通路排成一圈：外圈弧形小格显示每个基因在 5 个实验中表达是升是降，中心小图回答这几组通路之间共享哪些基因；想一张一图两用的环形主图时用它。

**部件亮点**
- 结构布局：单面板
- 编码方式：外圈6扇区弧形热图,蓝白红(-2~2)色标;基因名放射;扇区间留白+弧形通路名;中心UpSet交集柱+点阵

**复现**：配方 `scripts/recipes/case_seg133.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
