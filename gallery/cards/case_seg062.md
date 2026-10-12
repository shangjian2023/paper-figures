---
title: Nature 拟合气泡图
kind: 数据图
purpose: [排序降维]
data: 每点:两观测值,站点,深度
input: long (reference/data-schemas.json #062)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg062.py
preview: ../case_seg062.png
---

**一句话**：拟合气泡图 2×2（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：两种测量方法/两套数据产品对同一批对象各测一次，想用 1:1 虚线验证一致性（点贴线=吻合）

**有什么用**：两套观测对同一批样本各测一次、两两对画：点越贴对角虚线说明两套数据越吻合，点的大小是水深、颜色是观测站，下排拟合线专看有没有系统性偏差。

**部件亮点**
- 结构布局：2×2面板a-d,底部共用图例
- 编码方式：气泡大小=深度3档,色=8站点;a/b虚线1:1线,c/d黑拟合线+灰置信带

**复现**：配方 `scripts/recipes/case_seg062.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
