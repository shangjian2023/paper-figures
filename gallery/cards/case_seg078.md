---
title: Nature 时间序列图(二)
kind: 数据图
purpose: [趋势变化]
data: 2条件×3只×时间均值+SEM
input: long (reference/data-schemas.json #078)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg078.py
preview: ../case_seg078.png
---

**一句话**：多面板时间序列（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：2 个条件（如给药前后、药物 vs 载体）× 3-5 只动物/重复的响应曲线，先分小面板看个体一致性，再放大典型个体细看

**有什么用**：三只动物各画一个小图，各自比较对照与给药两种条件下的响应，下面再把其中一只放大细看，一眼确认药物压低响应的效果在每只动物上都成立。

**部件亮点**
- 结构布局：上排3小面板+下方放大
- 编码方式：灰ACSF/橙红SHU9119均值线+阴影SEM带;0处黑虚线;↑cAMP箭头;面板标题Mouse 1-3

**复现**：配方 `scripts/recipes/case_seg078.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
