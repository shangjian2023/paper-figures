---
title: Nature 配对散点图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 三联体序号+两条件成对值
input: long (reference/data-schemas.json #054)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg054.py
preview: ../case_seg054.png
---

**一句话**：配对散点+边缘密度（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：同一批对象（三元组/被试/配对样本）在两种条件下各有一个值，几十到几百对，想逐对连线展示两条件的此消彼长

**有什么用**：同一批对象在两种条件下的数值逐对连线：蓝点随排序越走越高、灰点越走越低，两种条件此消彼长，右侧密度曲线补看各自分布。

**部件亮点**
- 结构布局：单面板
- 编码方式：深蓝实心=given、灰空心=no coordination;配对点竖灰线;平滑曲线+置信带;x=按ΔZ排序序号;右侧分布弧线

**复现**：配方 `scripts/recipes/case_seg054.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
