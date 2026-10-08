---
description: 用 paper-figures 图库为数据选图并画成出版级图表（摆样板册→选图→演绎→品评）
argument-hint: [数据文件或用途描述]
---

按 paper-figures 技能的流程处理：$ARGUMENTS

1. 读技能 SKILL.md 与 stages/2-resonance.md，弄清受众与数据形状（自己打开数据看，不拿数据问题问用户）。
2. 粗筛候选（selection.md 决策表 + grep gallery-index.md 用途词），用
   `python scripts/make_contact_sheet.py sheet --out <tmp>/sheet-1.png <候选...> --open`
   摆第一轮样板册（6-9 张、拉开差距、标「我的推荐」与「贴近你的口味」），
   并在对话里给出 A/B/C 文字菜单（每张一句话）。
3. 用户选定后按 stages/3-rendition.md 演绎（写部件清单，从配方改），figures/ 三件套交付。
4. 交付前按 stages/4-appraisal.md 品评：compare --open 并排对照 + 三查，无硬伤才交。
