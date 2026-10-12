---
title: Nature 相关性矩阵点图(二)
kind: 数据图
purpose: [相关关系]
data: 签名×CNV事件:rho,p值,两组
input: matrix (reference/data-schemas.json #097)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg097.py
preview: ../case_seg097.png
---

**一句话**：相关矩阵点图(双面板)（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：同一套行×列的相关分析要按两个条件/亚组并排各画一张（如 WGD-low vs WGD-high），对比相关模式的条件差异

**有什么用**：同一套相关分析按低、高两个条件并排各画一遍：圆越大越显著、红蓝分正负，两面板一对照，只在其中一侧出现的关联立刻现形。

**部件亮点**
- 结构布局：WGD-low/WGD-high双面板
- 编码方式：圆大小=-log10P,色=Spearman ρ红蓝,圆内*号,6列CNV事件,行按模块分框,右侧双图例

**复现**：配方 `scripts/recipes/case_seg097.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
