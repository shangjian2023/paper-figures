---
title: 氨基酸位点热图
kind: 数据图
purpose: [相关关系]
data: 57位点×20氨基酸能量矩阵+均值
input: matrix (reference/data-schemas.json #145)
journal: 未标注
recipe: scripts/recipes/case_seg145.py
preview: ../case_seg145.png
---

**一句话**：氨基酸突变能量热图

**部件亮点**
- 结构布局：单面板
- 编码方式：x=57位点,y=20氨基酸;绿-白-红能量色标(-2.0~2.94)顶部;黑虚折线+红/蓝圆点=位点平均能量(右轴);零虚线

**复现**：配方 `scripts/recipes/case_seg145.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
