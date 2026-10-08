---
description: paper-figures 环境自检（依赖/图库/配方/各 agent 安装状态）
---

运行 `python scripts/doctor.py` 并把结果汇总给用户：

- HEALTHY：报告图库/配方/卡片数量与已安装的 agent 列表。
- NEEDS ATTENTION：逐项列出缺失（依赖包给出 pip 安装命令；图库不全是 lite 安装则属正常；
  某 agent 缺装则提示 `python install.py --agents <name>`）。
