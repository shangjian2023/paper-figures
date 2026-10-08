# -*- coding: utf-8 -*-
"""案例142 - 森林图(表格风): 左变量名列+HR(95%CI)列+中间log刻度HR图
(x 0.5-2.5, HR=1虚线, 方块+CI)+右P值列; 交替行底纹, 分组花括号(Mono/TAM/DC),
彩色编号圆点, 右侧 Monocyte/TAM/Proliferating/DC 图例。
参考: frames/seg_142.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter, NullFormatter

set_style()

# (类型, 名字/编号, 颜色, hr, lo, hi, p, 星)
ROWS = [
    ('plain', 'Age', None, 1.00, 0.97, 1.03, '0.545', ''),
    ('plain', 'Sex', None, 1.23, 0.82, 1.90, '0.314', ''),
    ('plain', 'Stage', None, 1.51, 1.22, 1.90, '0.0001', '***'),
    ('head', 'Cell signature', None, None, None, None, '', ''),
    ('num', 1, '#2e8b57', 1.03, 0.67, 1.60, '0.908', ''),
    ('num', 2, '#8bc34a', 1.04, 0.71, 1.50, '0.848', ''),
    ('num', 3, '#e57fa4', 0.96, 0.65, 1.40, '0.818', ''),
    ('num', 4, '#c2185b', 1.07, 0.71, 1.60, '0.743', ''),
    ('num', 5, '#7b3fa0', 0.72, 0.47, 1.10, '0.12', ''),
    ('num', 6, '#7986cb', 1.00, 0.64, 1.60, '0.998', ''),
    ('num', 7, '#1f77b4', 1.63, 1.15, 2.30, '0.006', '**'),
    ('num', 8, '#f2a03d', 1.21, 0.85, 1.70, '0.21', ''),
    ('num', 9, '#3ba8a8', 0.95, 0.63, 1.40, '0.796', ''),
    ('num', 10, '#8b2f2f', 0.90, 0.60, 1.30, '0.6', ''),
    ('num', 11, '#8d6e2f', 1.05, 0.67, 1.70, '0.837', ''),
]
Y0, DY = 13.6, -1.15          # 行距加大: 给右侧图例的半行组头留出真实间隙
YMIN, YMAX = -3.4, 14.7
SHADE = [Y0 + DY * i for i in range(0, len(ROWS), 2)]   # 交替行底纹
BAND = abs(DY) / 2            # 底纹半高: 相邻底纹恰好相接

fig = plt.figure(figsize=cm2in(17.5, 10.7))
# ---------------- 背景表格轴 (整宽): 底纹/花括号/文本列/图例
bg = fig.add_axes([0.0, 0.0, 1.0, 1.0])
bg.set_xlim(0, 1)
bg.set_ylim(YMIN, YMAX)
bg.axis('off')
# ---------------- 中部森林图轴
# 全高放置: 与 bg 共用同一 y->像素映射, 误差条行与表格文字行严格对齐
ax = fig.add_axes([0.315, 0.0, 0.335, 1.0])
ax.set_xscale('log')
ax.set_xlim(0.47, 2.72)
ax.set_ylim(YMIN, YMAX)
ax.set_yticks([])
ax.xaxis.set_major_locator(FixedLocator([0.5, 1, 1.5, 2, 2.5]))
ax.xaxis.set_major_formatter(FixedFormatter(['0.5', '1', '1.5', '2', '2.5']))
ax.xaxis.set_minor_formatter(NullFormatter())
ax.tick_params(labelsize=8.5, length=3)
for s in ('top', 'right', 'left'):
    ax.spines[s].set_visible(False)
ax.axvline(1.0, color='black', ls=(0, (1.5, 1.8)), lw=1.0, ymin=0.05,
           ymax=0.94)

# ---------------- 交替行底纹 + 分隔线 + 花括号
TAB_R = 0.758                 # 底纹/分隔线止于 P 值列后, 右侧图例区留白
for y_ in SHADE:
    bg.axhspan(y_ - BAND, y_ + BAND, xmin=0.03, xmax=TAB_R, color='#e9e9e9',
               lw=0)
bg.plot([0.03, TAB_R], [Y0 + DY * 2.5, Y0 + DY * 2.5], color='0.35', lw=0.8)
for lab, i0, i1 in [('Mono', 4, 5), ('TAM', 6, 10), ('DC', 12, 14)]:
    ytop = Y0 + DY * i0 + 0.44 * abs(DY)
    ybot = Y0 + DY * i1 - 0.44 * abs(DY)
    bg.plot([0.024, 0.024], [ybot, ytop], color='black', lw=0.9)
    bg.plot([0.024, 0.031], [ytop, ytop], color='black', lw=0.9)
    bg.plot([0.024, 0.031], [ybot, ybot], color='black', lw=0.9)
    bg.text(0.012, (ytop + ybot) / 2, lab, fontsize=8.5, ha='center',
            va='center', rotation=90)

# ---------------- 列标题
bg.text(0.033, 14.25, 'Variable', fontsize=9, fontweight='bold',
        style='italic')
bg.text(0.135, 14.25, 'HR (95% CI)', fontsize=9, fontweight='bold',
        style='italic')
bg.text(0.660, 14.25, 'P value', fontsize=9, fontweight='bold',
        style='italic')

# ---------------- 行内容
NUMROW = {}    # 编号 -> 行 y: 左侧圆点/HR/P 值与右侧图例共用同一 y 来源
for i, (typ, name, col, hr, lo, hi, p, stars) in enumerate(ROWS):
    y = Y0 + DY * i
    if typ == 'num':
        NUMROW[name] = y
    if typ == 'head':
        bg.text(0.033, y, name, fontsize=8.5, va='center')
        continue
    if typ == 'plain':
        bg.text(0.033, y, name, fontsize=8.5, va='center')
    else:
        bg.scatter([0.085], [y], s=110, color=col, clip_on=False, zorder=5)
        bg.text(0.085, y, str(name), fontsize=7, ha='center', va='center',
                color='white', fontweight='bold', zorder=6)
    bg.text(0.135, y, '%.2f (%.2f $-$ %.1f)' % (hr, lo, hi), fontsize=8.5,
            va='center')
    ax.plot([lo, hi], [y, y], color='black', lw=1.1, zorder=3)
    ax.plot([hr], [y], marker='s', ms=5.2, color='black', zorder=4)
    bg.text(0.660, y, p, fontsize=8.5, va='center', style='italic')
    if stars:
        bg.text(0.725, y, stars, fontsize=8.5, va='center',
                fontweight='bold')

# ---------------- 右侧图例 (编号圆点 y 严格取 NUMROW, 与其变量行逐行对齐)
LEG = [
    ('head', 'Monocyte:', None, None),
    ('item', 1, '#2e8b57', 'Classical monocyte'),
    ('item', 2, '#8bc34a', 'Nonclassical monocyte'),
    ('head', 'TAM:', None, None),
    ('item', 3, '#e57fa4', 'FOLR2$^+$ TAM'),
    ('item', 4, '#c2185b', 'IFN-TAM'),
    ('item', 5, '#7b3fa0', 'Inflam-TAM'),
    ('item', 6, '#7986cb', 'RTM-TAM'),
    ('item', 7, '#1f77b4', 'TREM2$^+$ TAM'),
    ('head', 'Proliferating:', None, None),
    ('item', 8, '#f2a03d', 'Cycling cell'),
    ('head', 'DC:', None, None),
    ('item', 9, '#3ba8a8', 'cDC1 (CLEC9A$^+$)'),
    ('item', 10, '#8b2f2f', 'cDC2 (CD1C$^+$)'),
    ('item', 11, '#8d6e2f', 'cDC3 (LAMP3$^+$)'),
]
# 组头 y: "Cell signature"空行 或 相邻两行半行处, 与任何圆点行错开
HEADROW = {'Monocyte:': NUMROW[1] - DY,
           'TAM:': (NUMROW[2] + NUMROW[3]) / 2,
           'Proliferating:': (NUMROW[7] + NUMROW[8]) / 2,
           'DC:': (NUMROW[8] + NUMROW[9]) / 2}
for typ, num, col, lab in LEG:
    if typ == 'head':
        bg.text(0.775, HEADROW[num], num, fontsize=8, va='center',
                fontweight='bold',
                bbox=dict(facecolor='white', edgecolor='none', pad=1.5))
        continue
    y = NUMROW[num]        # 自查: 第 k 个编号圆点 y == 第 k 变量行 y
    bg.scatter([0.785], [y], s=90, color=col, clip_on=False, zorder=5)
    bg.text(0.785, y, str(num), fontsize=6.5, ha='center', va='center',
            color='white', fontweight='bold', zorder=6)
    bg.text(0.802, y, lab, fontsize=8, va='center')

save(fig, 'case_seg142.png')
