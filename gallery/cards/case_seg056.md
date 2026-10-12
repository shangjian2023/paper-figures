---
title: Nature 网络气泡图
kind: 数据图
purpose: [网络与流向]
data: 类别→条目两层,各数值
input: long (reference/data-schemas.json #056)
journal: Nature
wow: 3
recipe: scripts/recipes/case_seg056.py
preview: ../case_seg056.png
---

**一句话**：放射状网络气泡图（Nature 风格）

**高级感**：★★★ 镇场级（用户要"高级/惊艳"时优先摆）

**适用场景**：类别→条目两级网络：中心 8-10 个彩色大类大圆点（带彩色文字），放射细线连到外圈小气泡，气泡大小∝条目数值

**有什么用**：中心大圆点是大类，细线向外散开连着一圈小气泡，气泡越大数值越大，像一圈星系，哪类条目多、哪个条目值最大一眼可见。

**部件亮点**
- 结构布局：单面板
- 编码方式：中心类别大圆点+彩色文字,细曲线连外圈小气泡,气泡径∝数值;10类配色;节点名放射旋转

**复现**：配方 `scripts/recipes/case_seg056.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
