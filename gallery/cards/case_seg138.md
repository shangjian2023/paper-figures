---
title: 配对散点箱线图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 配对长表:患者×4组值
input: long (reference/data-schemas.json #138)
journal: 未标注
recipe: scripts/recipes/case_seg138.py
preview: ../case_seg138.png
---

**一句话**：配对散点箱线图

**部件亮点**
- 结构布局：左右两个同构面板
- 编码方式：4组箱线+抖动散点;灰色虚线连接配对个体;组间显著性横线+精确p值;x标签45°;左蓝绿系右紫红橙系

**复现**：配方 `scripts/recipes/case_seg138.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
