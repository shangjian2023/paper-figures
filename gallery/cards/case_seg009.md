---
title: Nature 双Y轴图
kind: 数据图
purpose: [组间比较]
data: 17菌株×2指标×3重复
input: long (reference/data-schemas.json #009)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg009.py
preview: ../case_seg009.png
---

**一句话**：双Y轴分组柱形图（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：10-20 个菌株/样本各测了两个单位不同的指标，想并排双柱对比

**有什么用**：每个菌株并排两根柱子：一根量'长得好不好'，另一根量'产出多少'，两边刻度各管各的；再画两条横线当达标线，哪株又壮又高产，一眼挑出来。

**部件亮点**
- 结构布局：单面板
- 编码方式：17样本并列双柱:左轴蓝OD600、右轴米色药物浓度;±SEM;红/蓝横向阈值线;p<0.05;顶部图例

**复现**：配方 `scripts/recipes/case_seg009.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
