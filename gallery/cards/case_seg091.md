---
title: Cell 冲击图
kind: 数据图
purpose: [网络与流向]
data: 流向表source-target-count
input: edges (reference/data-schemas.json #091)
journal: Cell
wow: 3
recipe: scripts/recipes/case_seg091.py
preview: ../case_seg091.png
---

**一句话**：冲击图/桑基图（Cell 风格）

**高级感**：★★★ 镇场级（用户要"高级/惊艳"时优先摆）

**适用场景**：样本有明确的阶段归属：从第一级（如物种）经中间状态（如特异性分级）流向末端结果（如信号亮度），想展示每条路径的计数与占比

**有什么用**：样本从左往右流过三站：来自哪个物种、命中目标还是打偏、最后信号强不强，带子越宽样本越多，每一步分流到哪去了在图上一清二楚。

**部件亮点**
- 结构布局：单面板
- 编码方式：三列节点(Species→Specificity→Brightness),灰主流量+蓝高亮流,各流标n;用 helpers.sankey.sankey

**复现**：配方 `scripts/recipes/case_seg091.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
