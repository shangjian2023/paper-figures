---
title: Nature 柱形图
kind: 数据图
purpose: [组间比较]
data: 分组(3组)×细胞计数,Cont约13个、处理组8-15个重复
input: long (reference/data-schemas.json #001)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg001.py
preview: ../case_seg001.png
---

**一句话**：柱形图+抖动散点（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：比较 3 组左右单因素实验的细胞计数/测量值，突出处理组显著低于对照组

**有什么用**：用柱子代表每组的平均值，柱上叠出每个样本的真实数据点，再用星号标出哪两组差异明显、哪里其实没差别。想比较几种处理的效果、每组样本又不多时，最先想到它。

**部件亮点**
- 结构布局：单面板
- 编码方式：3组柱:Cont黑描边白底、处理组绿描边;均值±SEM误差棒+柱内外散点;***与ns横线支架;y轴# INL PCNA+ cells/300um 0-400;基因名斜体

**复现**：配方 `scripts/recipes/case_seg001.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
