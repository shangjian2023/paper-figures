---
title: Nature 散点饼图
kind: 数据图
purpose: [相关关系]
data: 医院×类型网格:物种构成计数
input: long (reference/data-schemas.json #047)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg047.py
preview: ../case_seg047.png
---

**一句话**：散点饼图（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：在'地点×类型'网格上同时回答三件事：哪里有观测、物种/类别构成如何、规模多大（饼径=计数）

**有什么用**：每家医院、每种质粒类型画一个小饼：饼越大菌株越多，颜色区分是哪种菌，哪里病例集中、都是什么菌，一张图看全。

**部件亮点**
- 结构布局：单面板
- 编码方式：x=医院(45°斜排),y=质粒Inc类型;每观测画一个饼图,饼分色=物种(绿/品红/橙/蓝/灰),饼径=菌株数;网格白底灰线

**复现**：配方 `scripts/recipes/case_seg047.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
