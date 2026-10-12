---
title: Nature 时间序列图(一)
kind: 数据图
purpose: [趋势变化]
data: 两组×16时间点GIR均值±SEM
input: long (reference/data-schemas.json #077)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg077.py
preview: ../case_seg077.png
---

**一句话**：时间序列折线图（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：两组（处理 vs 对照）随时间的连续指标变化，每个时间点有均值±SEM，每组 n=5-6

**有什么用**：两组动物在各时间点的平均响应画成两条折线，点旁小须表示波动范围，一眼看出处理组一路更高、最后各自稳定在什么水平。

**部件亮点**
- 结构布局：单面板
- 编码方式：黑圆Vehicle/金黄圆chABC+误差棒;浅紫竖带Basal与Clamp两阶段;逐点*/**,Clamp上***横括

**复现**：配方 `scripts/recipes/case_seg077.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
