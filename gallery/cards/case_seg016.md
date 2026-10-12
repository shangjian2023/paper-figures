---
title: Nature 分组山脊图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 2组×6时间点×RMSD分布
input: long (reference/data-schemas.json #016)
journal: Nature
wow: 3
recipe: scripts/recipes/case_seg016.py
preview: ../case_seg016.png
---

**一句话**：分组山脊图（Nature 风格）

**高级感**：★★★ 镇场级（用户要"高级/惊艳"时优先摆）

**适用场景**：同一指标在 5-8 个时间点各有一条分布，想展示分布峰随时间整体右移（如 MD 轨迹 0→24 ns 的 RMSD 演化）

**有什么用**：把六个时间点各画成一条“小山”上下排开，颜色越深时间越晚；山包一路向右挪，一眼看出数值随时间整体变大，适合展示分布的渐变推移。

**部件亮点**
- 结构布局：单面板
- 编码方式：6条分布水平堆叠,绿系与紫系两版,0ns→24ns峰右移;仅顶部填充+底部细基线;X=Core RMSD

**复现**：配方 `scripts/recipes/case_seg016.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
