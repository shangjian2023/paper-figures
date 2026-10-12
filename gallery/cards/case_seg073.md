---
title: Nature 堆积柱形图(二)
kind: 数据图
purpose: [构成占比]
data: 18列×5亚群百分比±SEM
input: long (reference/data-schemas.json #073)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg073.py
preview: ../case_seg073.png
---

**一句话**：纵向分块堆积柱形图（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：展示构成随时间的演变：6-8 个时间点×每点几根柱（如 unedited/对照/编辑组），各亚群占比堆到100%

**有什么用**：半年随访里每三根柱一组，免疫细胞构成堆到 100%，蓝色髓系占大头，后期柱顶冒出品红色的新生亚群，构成随时间的演变一目了然。

**部件亮点**
- 结构布局：6时间块×3处理,点虚线分块
- 编码方式：堆叠%:红/橙/蓝(主体)/黄,后期顶部品红段;每段误差棒;块间点状竖虚线;x标签斜排

**复现**：配方 `scripts/recipes/case_seg073.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
