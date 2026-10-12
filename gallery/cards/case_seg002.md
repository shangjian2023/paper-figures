---
title: Lancet PCoA图
kind: 数据图
purpose: [分布形态, 组间比较, 排序降维]
data: 样本×PCo1/PCo2得分,3组各约50样本
input: xy (reference/data-schemas.json #002)
journal: Lancet
wow: 2
recipe: scripts/recipes/case_seg002.py
preview: ../case_seg002.png
---

**一句话**：PCoA排序图+边际箱线图（Lancet 风格）

**高级感**：★★ 有设计感

**适用场景**：有 2-4 组样本的 PCoA/PCA 降维得分，想展示组间分离并给每组画置信椭圆

**有什么用**：把每个样本按整体的相似程度排成点：越相似的靠得越近，各组再圈出范围椭圆，一眼看出不同人群是否各自抱团、能否分开。菌群、代谢物等'谁和谁像'的问题常用它。

**部件亮点**
- 结构布局：十字形:主散点+上/右侧箱线+右上注释框
- 编码方式：3组散点(橙HC/蓝T1D/红T2D)+置信椭圆;上/右边际箱线图;右上PERMANOVA P=0.0029框;轴标注PCo1 25.44%/PCo2 11.79%

**复现**：配方 `scripts/recipes/case_seg002.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
