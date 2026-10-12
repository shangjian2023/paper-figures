---
title: Sci. Adv 曼哈顿图
kind: 数据图
purpose: [差异展示, 排序]
data: 目×3比较log2FC,丰度,类目
input: long (reference/data-schemas.json #116)
journal: Sci. Adv
wow: 2
recipe: scripts/recipes/case_seg116.py
preview: ../case_seg116.png
---

**一句话**：曼哈顿式气泡图（Sci. Adv 风格）

**高级感**：★★ 有设计感

**适用场景**：微生物组目级/科级数十至上百个分类单元在 2-4 个处理比较中的 log2FC，想按分类位次排成曼哈顿式全景，一眼看谁升谁降

**有什么用**：把上百种微生物按类别排成一条长队，每种是一个泡泡：位置越高越增多、越低越减少，泡越大原本越常见，实心代表变化可信。哪类菌对处理反应最强，一扫便知。

**部件亮点**
- 结构布局：3层堆叠面板
- 编码方式：y=Log2FCs,x=目级分类位次,气泡色=目(彩虹)大小=丰度,灰竖分隔线,0/±1虚线,底部彩点+旋转标签

**复现**：配方 `scripts/recipes/case_seg116.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
