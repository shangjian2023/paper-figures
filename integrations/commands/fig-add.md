---
description: 把一张（或一批）新图收进 paper-figures 图库：脚手架→渲染自检→登记→重建索引
argument-hint: <图片路径或案例参考号> [标题]
---

按 paper-figures 技能 stages/1-appreciation.md 的入库流程处理：$ARGUMENTS

1. 收到例图先看懂其用途/数据形状/六部件；有参考号则从该配方出发。
2. `python scripts/new_case.py --from <参考seg> --name <kebab-name> --title "<标题>"` 建脚手架。
3. 编辑新配方渲染自检（无硬伤、seed 固定可重跑），`python scripts/polish.py <新配方>` 必须 PASS。
4. 在 catalog.json 登记条目（seg 顺延；wow 分级跑 `python scripts/wow_score.py` 补上），
   `python scripts/gen_cards.py && python scripts/build_index.py` 重建卡片与索引。
5. 提示用户：是否同步到已安装的 agent 副本（`python install.py --list` 查看）。
