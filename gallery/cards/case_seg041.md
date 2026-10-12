---
title: Nature 小提琴图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 3组×3情境Z-score+两两P值
input: long (reference/data-schemas.json #041)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg041.py
preview: ../case_seg041.png
---

**一句话**：小提琴+抖动+P值（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：比较 2-4 组的连续得分/指标分布（每组几十个观测），要同时展示分布轮廓、均值±SD 和原始数据点

**有什么用**：把几组每个人的得分都画成点，外面套上分布轮廓（小提琴形），中间十字标出平均水平和波动范围，顶部括号写明组间检验的 P 值。想说明哪组偏高、哪组波动大、差异是否显著时用它。

**部件亮点**
- 结构布局：三面板并排(5/10/20)
- 编码方式：3组小提琴(粉红/橙/浅蓝半透明)+抖动空心点+粗横线均值+竖线SD;虚灰线y=0;顶部括号P值;x标签45°

**复现**：配方 `scripts/recipes/case_seg041.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
