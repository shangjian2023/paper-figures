# -*- coding: utf-8 -*-
"""案例116 (seg114) - Microbiome UpSet 图(彩色顶刊版)。
参考: frames/seg_114.jpg — 顶部交集条形(紫=Apo特有, 橙=Sym特有, 灰=混合)+数值,
左侧 setSize 条形(Apo 红/深红系, Sym 蓝系), 8 集合点阵连线, 行底纹,
右上双色 Venn 插图(两半透明圆 + 交集数)。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *
set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Patch
from helpers.upset import upset_plot_pro

# ---------------- 合成集合: 每个元素只属于一个"组合", 精确复现目标交集计数
names = ['D1_Apo', 'D3_Apo', 'D5_Apo', 'D7_Apo',
         'D1_Sym', 'D3_Sym', 'D5_Sym', 'D7_Sym']
combos = [
    (('D1_Apo',), 343), (('D3_Apo',), 336), (('D5_Apo',), 334),
    (('D1_Apo', 'D3_Apo'), 220), (('D5_Sym',), 190), (('D1_Sym',), 171),
    (('D3_Apo', 'D5_Apo'), 154), (('D7_Apo',), 147),
    (('D1_Apo', 'D3_Apo', 'D5_Apo'), 134), (('D1_Sym', 'D3_Sym'), 132),
    (('D1_Apo', 'D5_Apo'), 127), (('D5_Apo', 'D7_Apo'), 105), (('D3_Sym',), 104),
    (('D1_Apo', 'D3_Apo', 'D5_Apo', 'D7_Apo'), 101), (('D5_Sym', 'D7_Sym'), 86),
]
sets = {n: set() for n in names}
k = 0
for comb, cnt in combos:
    for _ in range(cnt):
        eid = f'e{k}'; k += 1
        for n in comb:
            sets[n].add(eid)

fig, ax_top, ax_mid = upset_plot_pro(sets, figsize=cm2in(18, 18.5),
                                     color='#7D3C98', max_inter=15, fs=7)

# ---------------- 交集条形按 组合归属 着色: 紫=Apo 内, 橙=Sym 内, 灰=混合
apo = {'D1_Apo', 'D3_Apo', 'D5_Apo', 'D7_Apo'}
sym = {'D1_Sym', 'D3_Sym', 'D5_Sym', 'D7_Sym'}
bar_col = []
for comb, _ in combos:
    s = set(comb)
    if s <= apo:
        bar_col.append('#7D3C98')
    elif s <= sym:
        bar_col.append('#E58606')
    else:
        bar_col.append('#9E9E9E')
for p, c in zip(ax_top.patches, bar_col):
    p.set_facecolor(c)
for t, c in zip(ax_top.texts, bar_col):
    t.set_color(c)

# ---------------- 行底纹: Apo 行淡粉, Sym 行淡紫
y_of = {n: len(names) - 1 - i for i, n in enumerate(names)}
for n in names:
    ax_mid.axhspan(y_of[n] - 0.5, y_of[n] + 0.5,
                   color='#FDEDEC' if n.endswith('Apo') else '#E8DAEF',
                   alpha=0.8, lw=0, zorder=0)
ax_mid.set_zorder(ax_top.get_zorder() + 1)
ax_mid.patch.set_visible(False)

# ---------------- 左侧 setSize 条形: Apo 红系, Sym 蓝系
red_shades = ['#8E2419', '#B03A2E', '#CD6155', '#E6B0AA']
blue_shades = ['#1A5276', '#21618C', '#2E86C1', '#5DADE2']
gidx = {'1': 0, '3': 1, '5': 2, '7': 3}
ax_left = ax_mid.figure.axes[-1]
for t in list(ax_left.texts):                    # 移除与行名重叠的端部数字
    t.remove()
xmax = ax_left.get_xlim()[1]
for p, n in zip(ax_left.patches, names):
    shade = red_shades if n.endswith('Apo') else blue_shades
    p.set_facecolor(shade[gidx[n[1]]])
    inside = p.get_width() > 0.35 * xmax
    ax_left.text(p.get_width() / 2 if inside else p.get_width() + 0.02 * xmax,
                 p.get_y() + p.get_height() / 2, str(len(sets[n])),
                 ha='center' if inside else 'left', va='center',
                 fontsize=6, color='white' if inside else '#333')
ax_mid.tick_params(labelleft=False)
ax_left.set_xlabel('Set size', fontsize=7)

# ---------------- 上方补灰色朴素 UpSet 总览(与彩色版共享集合行顺序)
# 交集算法与 helpers/upset.upset_plot_pro 完全一致, 保证与下方彩色面板逐列对齐
from itertools import combinations as _c
n_set = len(names)
inter = []
for r_ in range(1, n_set + 1):
    for comb in _c(range(n_set), r_):
        s = set(sets[names[comb[0]]])
        for c_ in comb[1:]:
            s &= set(sets[names[c_]])
        for other in range(n_set):
            if other not in comb:
                s -= set(sets[names[other]])
        if s:
            inter.append((comb, len(s)))
inter.sort(key=lambda t: -t[1])
inter = inter[:15]

fig = ax_mid.figure
b0 = min(a.get_position().y0 for a in (ax_top, ax_mid, ax_left))
t0 = max(a.get_position().y1 for a in (ax_top, ax_mid, ax_left))
S = 0.44 / (t0 - b0)                      # 彩色版压缩到下半区 0.02..0.46
for a in (ax_top, ax_mid, ax_left):
    x0, y0, w_, h_ = a.get_position().bounds
    a.set_position([x0, 0.02 + (y0 - b0) * S, w_, h_ * S])
DY = 0.50                                 # 灰色总览面板放在上半区

def _clone_axes(a, dy):
    x0, y0, w_, h_ = a.get_position().bounds
    return fig.add_axes([x0, y0 + dy, w_, h_])

g_top = _clone_axes(ax_top, DY)
g_mid = _clone_axes(ax_mid, DY)
g_left = _clone_axes(ax_left, DY)
xs = np.arange(len(inter))
g_top.bar(xs, [c for _, c in inter], width=0.62, color='#7F7F7F', zorder=3)
for x, (_, c) in zip(xs, inter):
    g_top.text(x, c, str(c), ha='center', va='bottom', fontsize=6)
g_top.set_ylim(0, max(c for _, c in inter) * 1.2)
g_top.set_xlim(ax_top.get_xlim())
g_top.set_xticks([])
g_top.set_ylabel('Intersection size', fontsize=7)
y_of = {nm: n_set - 1 - i for i, nm in enumerate(names)}
for x, (comb, _) in zip(xs, inter):
    ys = [y_of[names[c_]] for c_ in comb]
    if len(ys) > 1:
        g_mid.plot([x, x], [min(ys), max(ys)], color='k', lw=0.9, zorder=2)
    g_mid.scatter([x] * len(ys), ys, s=24, color='k', zorder=3)
g_mid.set_ylim(ax_mid.get_ylim())
g_mid.set_xlim(ax_top.get_xlim())
g_mid.set_yticks(range(n_set))
g_mid.set_yticklabels([])
g_mid.set_xticks([])
g_mid.tick_params(left=False)
sizes = [len(sets[nm]) for nm in names]
g_left.barh([y_of[nm] for nm in names], sizes, height=0.58,
            color='#9E9E9E', zorder=3)
for nm in names:
    g_left.text(len(sets[nm]) + max(sizes) * 0.03, y_of[nm], str(len(sets[nm])),
                va='center', fontsize=6)
g_left.set_xlim(ax_left.get_xlim())
g_left.set_yticks([y_of[nm] for nm in names])
g_left.set_yticklabels(names, fontsize=7)
g_left.set_xticks([0, 300, 600, 900])
g_left.set_xticklabels(['0', '300', '600', '900'], fontsize=5, rotation=90)
g_left.tick_params(axis='x', pad=1)
g_left.set_xlabel('Set size', fontsize=7)
for a in (g_top, g_mid, g_left):
    for sp in ['top', 'right']:
        a.spines[sp].set_visible(False)
g_mid.spines['left'].set_visible(False)

# ---------------- 右上双色 Venn 插图(放两面板间隙, 彩色条右端上方)
axv = fig.add_axes([0.72, 0.315, 0.21, 0.145])
axv.axis('off')
axv.set_xlim(-1.15, 1.75); axv.set_ylim(-0.75, 1.65)
c1 = Circle((0, 0.62), 0.55, facecolor='#9E9E9E', alpha=0.55, edgecolor='#666', lw=1)
c2 = Circle((0, 0.06), 0.55, facecolor='#7D3C98', alpha=0.55, edgecolor='#4A235A', lw=1)
axv.add_patch(c1); axv.add_patch(c2)
axv.text(0, 0.80, '1984', ha='center', va='center', fontsize=8)
axv.text(0, 0.34, '412', ha='center', va='center', fontsize=8)
axv.text(0, -0.18, '1677', ha='center', va='center', fontsize=8)
axv.text(0.62, 1.05, 'Up-regulation in\nApo-symbiotic', ha='left', va='center', fontsize=7)
axv.text(0.62, -0.42, 'Up-regulation in\nSymbiotic', ha='left', va='center',
         fontsize=7, color='#4A235A')

save(fig, 'case_seg114.png')
