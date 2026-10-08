# paper-figures — AGENTS.md 指针片段

给读取 AGENTS.md 的终端 agent（Codex / DeepSeek Harness(DSH) / 其他）用的接入片段。
把下面整段追加到你的 AGENTS.md（全局 `~/.agents/AGENTS.md`、`~/.codex/AGENTS.md`，
或项目 `./AGENTS.md`），把 `<SKILL_DIR>` 换成实际安装位置
（默认 `~/.agents/skills/paper-figures`，用 `python install.py --list` 查询）。

```markdown
## 论文绘图技能（paper-figures）

需要为论文/组会画图、选图型、美化图表、按例图复刻时，读取并遵循 <SKILL_DIR>/SKILL.md
的四阶段流程（鉴赏/共鸣/演绎/品评，细则在其 stages/ 目录）：

- 选图：先读 <SKILL_DIR>/reference/gallery-index.md 头部用途词统计，grep 定位候选，
  `python <SKILL_DIR>/scripts/make_contact_sheet.py sheet --out /tmp/sheet.png <候选> --open`
  摆样板册给用户挑，同时在对话里给 A/B/C 文字菜单。
- 画图：从 <SKILL_DIR>/scripts/recipes/ 对应 case_segNNN.py 改数据段，头部保持
  `from paper_style import *; set_style()`；交付 PNG+PDF+脚本三件套到 figures/。
- 交付前：`python <SKILL_DIR>/scripts/make_contact_sheet.py compare --out /tmp/cmp.png <seg> --open`
  并排品评，无文字重叠/截断/数值错误才交付。
- 环境问题：`python <SKILL_DIR>/scripts/doctor.py` 自检。
```

说明：
- Codex 若已把本技能装进 `$CODEX_HOME/skills/`（install.py 默认会做），无需此片段即可被发现；
  片段用于老版本 Codex 或希望强制常驻提示的场景。
- DeepSeek Harness(DSH)：社区 skill 目录尚未标准化（生态用 dshub.cc + dsh-skill-manager
  从 GitHub 装 skill）。DSH 用户可用 `python install.py --agents custom:<DSH的skills目录>`
  实体安装，再把本片段加进其 AGENTS.md。
