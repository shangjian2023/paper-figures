---
title: 泳道图(python)
kind: 数据图
purpose: [分布形态, 组间比较]
data: 患者事件时间线+器官计数+配对数据
input: long (reference/data-schemas.json #137)
journal: 未标注
recipe: scripts/recipes/case_seg137.py
preview: ../case_seg137.png
---

**一句话**：泳道图

**部件亮点**
- 结构布局：a主泳道+内嵌;b堆叠柱+饼;c配对箱线
- 编码方式：患者行×天数;左3列注释色条;菱形=手术、圆点=时间点、色条=治疗、三角/方块=复发、X=死亡;顶部5组图例

**复现**：配方 `scripts/recipes/case_seg137.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
