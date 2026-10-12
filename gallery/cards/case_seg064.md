---
title: Nature 平滑曲线图(二)
kind: 数据图
purpose: [趋势变化]
data: 3组浓度-电导率各十余点
input: long (reference/data-schemas.json #064)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg064.py
preview: ../case_seg064.png
---

**一句话**：平滑曲线图（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：3 条左右'先升后降'的单峰曲线对比（如不同电解液的浓度-电导率）

**有什么用**：三条先升后降的曲线各带一圈同色光晕标出峰值区，哪种配方导电最好、最优浓度落在哪个浓度附近，一眼看清。

**部件亮点**
- 结构布局：单面板
- 编码方式：3条平滑曲线+空心圆标记(深蓝/绿/红);峰下彩色光晕椭圆;图例右上

**复现**：配方 `scripts/recipes/case_seg064.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
