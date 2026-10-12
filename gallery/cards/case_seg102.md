---
title: Nature 渐变型等高线图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 基因(x,y)坐标+KDE网格+高亮名单
input: long (reference/data-schemas.json #102)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg102.py
preview: ../case_seg102.png
---

**一句话**：渐变等高线密度图（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：几千个点（基因/样本）构成二维散点云，想用灰度 KDE 渐变等高线交代总体密度轮廓、浅灰散点保底展示原始观测

**有什么用**：几千个基因按两个评分排成点云，深浅底色勾出扎堆的密度轮廓，黑虚线是参考对角线，少数重点基因用绿红两色挑出并写上名字，落在线内线外一眼分明。

**部件亮点**
- 结构布局：单面板
- 编码方式：灰度填充+细线等高线,浅灰背景散点,黑/蓝/红虚斜线参考,绿红重点基因点带引线标注,右侧灰度色条0-3

**复现**：配方 `scripts/recipes/case_seg102.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
