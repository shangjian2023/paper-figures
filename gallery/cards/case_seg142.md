---
title: 森林图
kind: 数据图
purpose: [差异展示, 排序]
data: 变量HR、CI上下限、p+分组映射
input: long (reference/data-schemas.json #142)
journal: 未标注
wow: 2
recipe: scripts/recipes/case_seg142.py
preview: ../case_seg142.png
---

**一句话**：森林图(表格风)

**高级感**：★★ 有设计感

**适用场景**：多因素 Cox/Logistic 回归结果：十几个变量的 HR、95%CI、p 值，想一图同时给出效应图和表格数字（左列变量名+HR(CI)、中间方块+CI、右列 P 值带星号）

**有什么用**：把回归分析里十几个因素列成一张表：左列名字和数值，中间方块加横线画出影响大小与可能范围，右列 p 值加星号；横线离开中间竖线越远，说明该因素越站得住。

**部件亮点**
- 结构布局：单面板
- 编码方式：左文本列+中HR图+右P值列,交替行底纹;x=HR log刻度0.5-2.5虚线HR=1;方块+CI;右侧P值带*/**;分组花括号;彩色编号圆点图例

**复现**：配方 `scripts/recipes/case_seg142.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
