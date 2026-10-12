# Appreciation 鉴赏（图库维护）

目标：让图库里每张图都"被看懂"。卡片和索引是选图的依据，写法要守词表。

## 卡片词表（gallery/cards/case_segNNN.md）

卡片由 `python scripts/gen_cards.py` 从 catalog.json 生成，字段含义：

| 字段 | 含义 |
|---|---|
| `title` | 期刊 + 图型名（如 "Nature 柱形图"） |
| `purpose` | 用途词，只能从词表里取：组间比较 / 分布形态 / 相关关系 / 构成占比 / 趋势变化 / 网络与流向 / 空间分布 / 多指标综合 / 差异展示 / 排序降维 |
| `data` | 需要的数据形状（几组几列、重复数、数值范围） |
| `wow` | 高级感分级 1-3（3=镇场级；选图时 `--min-wow` 筛选用） |
| `recipe` | 配方脚本路径，可直接运行 |
| `preview` | 成品参考图 |

手工改卡片只允许改 `purpose`（在词表内）和正文点评；结构化字段以 catalog.json 为准，改 catalog 后重跑 `gen_cards.py`。

## 加一张图

```bash
python scripts/new_case.py --from 001 --name my-raincloud --title "Nature 云雨图变体"
# 1) 编辑 scripts/recipes/case_my-raincloud.py 换数据段, 渲染自检
# 2) catalog.json 登记条目（新 seg 号顺延 147+，或替换旧条目）
# 3) python scripts/gen_cards.py && python scripts/build_index.py
```

入库标准（对照 `stages/4-appraisal.md` 通过后再收）：
- 图表家族是图库里没有的，或同家族但有明显新的布局/编码；
- 配方零报错、seed 固定可重跑、经"自己先看"三查无硬伤；
- 卡片 purpose/data 填全。

## 删图 / 去重

- 删图：从 catalog.json 删条目 → `python scripts/build_index.py --prune` 清残留 PNG → 重跑 `gen_cards.py` 清卡片。
- 去重：同用途同布局的候选只留第一视觉印象最好的一张；变体有独立价值时（如案例 50 的两个风格变体）在 catalog `features` 里写明差异再保留。

## 已知待修清单

`gallery/_audit_issues.txt` 是全库 polish 校准的存量标签问题（文字重叠/文字压数据/图例盖数据等，
当年视觉验收的漏网之鱼）。修一张：改对应配方 → `python scripts/polish.py scripts/recipes/case_segNNN.py`
到 PASS → 重跑该配方出图 → 对照 `make_contact_sheet.py compare` 复核 →
`python scripts/audit_gallery.py --update-baseline` 把它从基线划掉。
加新图时新配方必须 polish 一次通过，别给清单添行；`run_all_checks` 里的全库遮挡审计
会把基线外的新问题判为回退。

## 索引与样板册

```bash
python scripts/build_index.py                    # 重建 gallery/index.md（用途词统计+高级感 TOP 在头部）
python scripts/make_contact_sheet.py sheet --out /tmp/x.png --family polar --sample 6
python scripts/make_contact_sheet.py sheet --out /tmp/wow.png --min-wow 3 --sample 9   # 高级感样板册
```

索引头部第一行列出所有用途词及张数，选图时先 `grep` 用途词再定位行，图库大时不要整份读入。
