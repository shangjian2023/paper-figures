---
title: Nature 多边形雷达图
kind: 数据图
purpose: [多指标综合]
data: 两材料×5属性
input: long (reference/data-schemas.json #060)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg060.py
preview: ../case_seg060.png
---

**一句话**：五边形雷达对比（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：只有 2 个对象（两种材料/两个方案/处理 vs 对照）要对比，每个对象有 4-8 个不同量纲的性能属性

**有什么用**：两种材料各画一个五边形叠在一起，五个角是五项性能，谁的轮廓罩得大、差距集中在哪个角，一眼就能比出来。

**部件亮点**
- 结构布局：单面板
- 编码方式：5轴=折射率/热导/硬度/杨氏模量/电阻;粉红大五边形 vs 蓝色小五边形;顶点白字数值;底部双行图例

**复现**：配方 `scripts/recipes/case_seg060.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
