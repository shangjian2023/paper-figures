# Appraisal 品评（交付前检查）

目标：成品交到用户手里之前，先对照样例看一遍。代码跑通不等于图画对了，只有看图才知道。

## 自己先看

打开成品 PNG，同时打开选中案例的参考图，查三件事：

1. **部件清单到位了吗**：对照 Rendition 写下的清单逐条核对（布局/配色/标注各取自谁）。
2. **有没有硬伤**：文字重叠、标签截断、图例压数据、字号过小、中文方框、负号异常。
3. **数值画对了吗**：抽查几个点——最大最小类别、数量级、分组是否与数据一致。
   好看但画错的图比难看的图危害更大。

发现问题就改，改完重渲染再看；最多自修 3 轮，仍解决不了就如实告诉用户试过什么，不带硬伤交付。

## 并排对照给用户

```bash
# 对照"你刚画的成品"与选中案例(--got 传用户成品; 缺省对照图库验收图):
python scripts/make_contact_sheet.py compare --out /tmp/compare.png <seg> --got figures/my_fig.png --open
# 任意两图并排(如样例 A vs 成品):
python scripts/make_contact_sheet.py ab --out /tmp/ab.png <样例.png> figures/my_fig.png --open
```

`--open` 会在用户屏幕打开对照图；同时给用户**对话内文字总结**：从哪张图取了什么、
哪里做不到位、有什么要注意（无 GUI 会话则给对照图路径让用户自己打开）。
用户提意见 → 回 Rendition 修改或回 Resonance 换方向。

## 用户满意之后

1. **问一句：要不要收进图库？** 同意则按 `1-appreciation.md` 的入库标准走
   `new_case.py` → catalog 登记 → 重建索引。真实研究数据不进图库（图库会随技能分发），
   换模拟数据重画一份再收。
2. **在 `taste.md` 追加一行**（格式见 2-resonance.md）。
