---
title: Nature 网络气泡图
kind: 数据图
purpose: [网络与流向]
data: 类别→条目两层,各数值
input: edges (reference/data-schemas.json #056)
journal: Nature
recipe: scripts/recipes/case_seg056.py
preview: ../case_seg056.png
---

**一句话**：放射状网络气泡图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：中心类别大圆点+彩色文字,细曲线连外圈小气泡,气泡径∝数值;10类配色;节点名放射旋转

**复现**：配方 `scripts/recipes/case_seg056.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
