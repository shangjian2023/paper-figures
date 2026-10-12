---
title: Nature 扇形&箱线图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 分组连续数据长表
input: long (reference/data-schemas.json #093)
journal: Nature
wow: 3
recipe: scripts/recipes/case_seg093.py
preview: ../case_seg093.png
---

**一句话**：扇形极坐标箱线图（Nature 风格）

**高级感**：★★★ 镇场级（用户要"高级/惊艳"时优先摆）

**适用场景**：有约 8-14 组连续数据，既想看每组箱线的中位数/四分位，又想保留全部原始散点

**有什么用**：多组数据换成箱线加散点绕成扇形：白框标出每组的中段和中间值，彩色小点是逐一画出的原始观测，各组高低波动和个别离群点都看得见。

**部件亮点**
- 结构布局：单面板
- 编码方式：约12组沿扇形排列,箱线+抖动散点,浅灰同心网格,顶部弧形类目标签,中心留白孔

**复现**：配方 `scripts/recipes/case_seg093.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
