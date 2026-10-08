# paper-figures — 期刊级科研绘图 skill（146 顶刊案例配方库）

> 本仓库即 skill 源：`python install.py --all --commands` 可安装到各终端 agent（详见下文）。

来源：`D:\edge默认下载\47b602a7f4c1687294ad243b193f977e.mp4`（33.5s，146 个镜头段，覆盖原视频案例 1-151，缺编号 43/54/55/136/138/141；seg49/50 为案例 50 两个变体；seg139/140 为"普通版 vs 顶刊版"对比帧）。

## 目录

```
catalog.json            146 案例目录（seg/标题/期刊/family/features/data + 12 个批次）
frames/                 视频逐段代表帧 seg_001..146.jpg（复现时的参考原图）
scripts/
  paper_style.py        全局期刊风格（set_style/pal/sig_bracket/save 等）
  helpers/              ternary/chord/sankey/upset/newick/geo 六个特殊图型助手
  recipes/              case_segNNN.py ×146，每个可独立运行出图
  audit_stage_a.py      全量重跑 + PNG 完整性审计
  audit_skill.py        skill 产物终审
gallery/                146 张成品 PNG（300 dpi，全部经视觉验收）
assets/map_data/        world.geo.json / china.geo.json
```

## 运行

```bash
cd scripts/recipes && python case_seg001.py   # 输出 gallery/case_seg001.png
python ../audit_stage_a.py                    # 全量重跑验证
```

## 多 agent 安装（按 vercel-labs/skills 框架）

项目根 = skill 完整源。安装器把组装产物装到 canonical 并为各 agent 建链接：

```bash
python install.py --list            # 查看各 agent 状态
python install.py --all --commands  # canonical + 全部已装 agent + slash commands
python install.py --agents zcode    # 只装/更新指定 agent
python install.py --lite            # 不带 gallery 成品图(~2MB)
python scripts/doctor.py            # 任一副本内自检
```

- **canonical**：`~/.agents/skills/paper-figures`（实体，vercel-labs/skills 的通用位置）
- **链接**：zcode / claude / codex / opencode / gemini / qwen / cursor / copilot / droid / iflow / kimi / dsh 的
  global skills 目录（Windows junction 免管理员；POSIX 相对 symlink；失败回退复制）
- 本机已实测 13 个 agent 全部安装；DSH 目录为 `~/.dsh/skills`（探测命中）
- slash commands：`/fig` `/fig-add` `/fig-check` 分发到 zcode/claude/codex/opencode 的
  commands（codex 为 prompts）目录；DSH 等其他 agent 用 `integrations/AGENTS-snippet.md`
- 改动源后：`python install.py --all` 一键同步全平台（幂等，只写变化文件）

## 已安装的 skill

本库已分发为各终端 agent skill：canonical `~/.agents/skills/paper-figures`，13 个 agent（zcode/claude/codex/opencode/gemini/qwen/cursor/copilot/droid/iflow/kimi/dsh/warp）junction 链接；`python install.py --list` 查看。
（SKILL.md + reference/{catalog.json, selection.md, style_guide.md} + scripts/ + gallery 缩略参考图 + assets/map_data）。

**同步规则**：改了 `scripts/paper_style.py`、`scripts/helpers/`、`scripts/recipes/` 或 `catalog.json` 后，需同步拷贝到 skill 目录对应位置；`gallery/` 在 skill 内是缩略版（≤1400px），可重跑缩小脚本再生成。

## 质量记录

- **迭代1（2026-10-06/07）**：阶段A 146/146 重跑通过；阶段B 视觉验收 32 fail 全部修复复验；阶段C 一致性对齐；ternary.py 顶点映射 bug 根治。
- **迭代2（2026-10-07）**：静态扫描+运行时测量（146/146，总 232s，中位 1.2s）；selection.md 语义复核修正 7 处错配；**146 对"原帧 vs 成品"保真度全量对比**（faithful 127 / drift 18 / wrong 1），19 项全部修复并复验通过（含 seg143 重建为真 3D 双层悬空地图、seg027 重建双环和弦图、seg114/115 补灰色总览双面板、seg137 补人体器官气泡内嵌）；catalog 新增 preview/runtime_s/helpers/lines 字段；新增 gallery/index.md 与 skill 内 gallery-index.md；seg132 图内文字改英文。
- **迭代3（2026-10-07）**：参考 [plot-is-all-you-need](https://github.com/liouhai/plot-is-all-you-need) 重构为**四阶段看图选图闭环**——stages/{1-appreciation, 2-resonance, 3-rendition, 4-appraisal}；新增 146 张鉴赏卡片（gallery/cards/，purpose 十一词表）与 gen_cards.py；新增工具链 build_index.py（用途词索引）/ make_contact_sheet.py（样板册 sheet + 品评 compare/ab）/ new_case.py（加图脚手架）；SKILL.md 重构为路由表+入口式；taste.md 品味记录。项目与 skill 两侧工具链全部实跑通过。
- **迭代4（2026-10-07）多 agent TUI 适配**：按 **vercel-labs/skills（skills.sh）框架**重写分发——canonical=~/.agents/skills/paper-figures 实体，13 个 agent（zcode/claude/codex/opencode/gemini/qwen/cursor/copilot/droid/iflow/kimi/dsh/warp）junction 链接；`python install.py --all --commands` 一键同步；slash commands /fig /fig-add /fig-check；show.py/doctor.py；SKILL.md 增"终端(TUI) 运行约定"。详见 install.py 文档头。
- **迭代5（2026-10-07）质量深审**：①渲染警告审计——3 处 vert 废弃参数 + 7 处无效转义/set_bad 弃用全部清零，**146/146 零渲染警告**；字体探针确认 Arial 实际生效、全库零字形缺失；②PNG 边缘裁切检测 0/146；③颜色审计——146 配方零默认色环依赖（初扫误报已澄清）；④全量视觉终检（错位/不全/颜色/字体/一致性四判据）137→146 全 pass，修复 9+1 项（含 seg090/113 复发根治、seg028 像素级穿字二次修复、seg019 拼写、seg032 表头残缺观感、seg052 缺图例、seg074 色标刻度堆叠等）。过程教训：批量正则改色误伤字符串/键语境，已从 canonical 备份恢复——**批量改动必须先备份、逐处核语境**。
- **迭代6（2026-10-07）使用质量与顶刊质感**：①**确定性审计**——146 配方连跑两遍比 PNG hash，揪出 seg086 的 `hash(lab)` 每进程随机化（改 crc32），146/146 逐字节可复现；②**端到端流程演练**（子 agent 首次接触技能走完整用户请求）→ 9 个断点全修复：compare 加 `--got` 参数+无 frames 降级、new_case 脚手架注入技能绝对路径、resonance 路径名统一、style_guide 明确显著性标注分工、新增 `helpers/stats.py`（vs_control：Welch t + Bonferroni，有 statsmodels 自动升 Dunnett）、seg042 星号偏移改 ylim 相对量、样板册标签自动缩字号、taste 空表引导、save() 自动建目录；③**美学终检**（判据升级：数据可信度/信息完备/信息层级/排版系统）——fail 11 项全修复复验（数据自相矛盾 seg007/090/122/146、占位符轴名 seg043、单位失真 seg049、缺玫瑰图 seg059、径向轴不可解读 seg092/093、缺主体图例 seg013）+ polish 高价值 16 项（图例缺失×5、轴名缺失×5、拼写与写法×6，其中 3 项经像素级复核为低清误报）。评审员不了解参考帧导致的误判（如 seg114/115 双面板、seg132 教学对比为保真设计）未采纳。剩余 polish（留白/重复面板/装饰类约 20 项）记录为 known-polish，不阻塞交付。
- **迭代7（2026-10-07）数据输入层**：补齐此前缺失的"用户数据 → 图"契约与工具——①**输入 Schema 全覆盖**：`reference/data-schemas.json` 为 146 案例逐一声明输入契约（format: long 106 / matrix / edges / xy / newick / sets；必需列/类型/约束）；②**data_io.py**：load（csv/tsv/xlsx/json+编码探测）/ validate（缺列/类型/缺失率校验）/ 六个适配器（as_groups/as_matrix/as_xy/as_edges/as_ternary/as_sets）+ 自检；③**端到端演练**：long 表→seg001 柱形+散点、matrix 表→seg019 三色注释热图均真实出图，缺列 CSV 正确 FAIL；④卡片 frontmatter 增 `input:` 字段；SKILL.md 增"数据输入约定"节、stages/3-rendition 数据接入走 data_io 三步链；doctor 增 schema 检查。
- **迭代8（2026-10-07）数据层精度 + known-polish 清账**：①**Schema 精度**——14 个形态错位案例逐一精修（seg039/048/55/56/66/67/68/73/76/83/86/89/105/124 等，matrix 21→24），schema 支持 **aliases**（语义列名为主、槽位名 fa/fb/fc 为别名，validate 自动识别）；**recipe_vars 注入**（62/146 配方的强语义数据变量名+行号写入 schema，适配器输出有明确落点）；②**数据输入端到端补齐**——edges→桑基、sets→UpSet、ternary→三元、xy→UMAP 四适配器真图验证 ALL OK（全部 8 种 format 至少验证一次），演练中暴露并修复 sankey 胶水对接/三元语义列名两处问题；③**known-polish 清账 15 项**（信息完备/布局类）全修复复验 pass：seg030 量程统一、seg031/079 留白压缩、seg048/057/058/127/128 图例与刻度补全、seg051/117 图例重排与配色区分、seg110/111 标签出界、seg123/135 轴名图例；④新增 `run_all_checks.py` 一键回归（5 条审计线：重跑/警告/边缘/确定性/终审，--quick 支持），终态 **ALL CHECKS PASSED**。
