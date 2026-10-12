---
title: Nature 云雨图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 4物种×每基因组BGC数
input: long (reference/data-schemas.json #005)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg005.py
preview: ../case_seg005.png
---

**一句话**：云雨图（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：比较 3-6 组连续变量的完整分布，每组有几十到几百个原始观测

**有什么用**：每组数据撒成一片点、旁边画出分布轮廓、中间再立一个简易箱线：哪组数值偏高、哪组波动大、哪组形状不寻常，一眼全看到。数据多、又想看全貌时用它。

**部件亮点**
- 结构布局：单面板
- 编码方式：每组:左抖动散点+中央半小提琴+白底窄箱线;绿/红/橙/灰4色;右上图例框;Y轴0-30;仅左下轴线

**复现**：配方 `scripts/recipes/case_seg005.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
