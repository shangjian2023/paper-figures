# -*- coding: utf-8 -*-
"""案例117 (seg115) - Clin.Transl.Med UpSet 图(蓝红顶刊版)。
参考: frames/seg_115.jpg — 交集条形蓝(含 Malignant_vs_Benign)/红(不含), 数值同色,
点阵空心圆+连线, 行背景蓝→红渐变, 左侧 setSize 条形蓝/红系, 8 组比较。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *
set_style()

import numpy as np
import matplotlib.pyplot as plt
from helpers.upset import upset_plot_pro

names = ['Malignant_vs_Benign', 'StageII_vs_StageI', 'StageIII_vs_StageI',
         'StageIII_vs_StageII', 'StageIV_vs_StageI', 'StageIV_vs_StageII',
         'StageIV_vs_StageIII', 'N+_vs_N0']
FIRST = names[0]

combos = [
    ((FIRST,), 550),
    (('StageIV_vs_StageI',), 330), (('StageIV_vs_StageII',), 327),
    (('StageIV_vs_StageIII',), 316), ((FIRST, 'StageIV_vs_StageI'), 280),
    (('StageIII_vs_StageI',), 222), ((FIRST, 'StageIV_vs_StageII'), 196),
    (('StageIII_vs_StageII',), 142), ((FIRST, 'N+_vs_N0'), 122),
    (('StageIV_vs_StageI', 'StageIV_vs_StageII'), 120),
    (('StageIV_vs_StageII', 'StageIV_vs_StageIII'), 90),
    ((FIRST, 'StageII_vs_StageI'), 42), (('StageII_vs_StageI',), 38),
    ((FIRST, 'StageIV_vs_StageIII'), 35), (('N+_vs_N0',), 30),
    (('StageIV_vs_StageI', 'N+_vs_N0'), 26), ((FIRST, 'StageIII_vs_StageI'), 25),
    (('StageII_vs_StageI', 'StageIII_vs_StageI'), 23),
    (('StageIV_vs_StageI', 'StageIV_vs_StageII', 'StageIV_vs_StageIII'), 20),
    ((FIRST, 'N+_vs_N0', 'StageIV_vs_StageI'), 17),
    (('StageIII_vs_StageI', 'StageIII_vs_StageII'), 12),
    (('StageIV_vs_StageII', 'N+_vs_N0'), 10),
    (('StageIV_vs_StageI', 'StageIV_vs_StageIII'), 10),
    ((FIRST, 'StageII_vs_StageI', 'StageIII_vs_StageI', 'StageIII_vs_StageII'), 5),
    (('StageIV_vs_StageI', 'StageIV_vs_StageII', 'N+_vs_N0'), 4),
]
sets = {n: set() for n in names}
k = 0
for comb, cnt in combos:
    for _ in range(cnt):
        eid = f'e{k}'; k += 1
        for n in comb:
            sets[n].add(eid)

fig, ax_top, ax_mid = upset_plot_pro(sets, figsize=cm2in(18, 19),
                                     color='#3B7DD8', max_inter=25, fs=6.5)

# ---------------- 条形与数值: 蓝 = 含 Malignant_vs_Benign, 红 = 不含
bar_col = ['#3B7DD8' if FIRST in comb else '#B03A2E' for comb, _ in combos]
for p, c in zip(ax_top.patches, bar_col):
    p.set_facecolor(c)
for t, c in zip(ax_top.texts, bar_col):
    t.set_color(c)
    t.set_fontsize(6)

# ---------------- 行背景: 上 4 行蓝渐变, 下 4 行红渐变
y_of = {n: len(names) - 1 - i for i, n in enumerate(names)}
blue_a = [0.30, 0.20, 0.12, 0.06]                 # y=7..4
red_a = [0.06, 0.12, 0.20, 0.30]                  # y=3..0
for n in names[:4]:
    ax_mid.axhspan(y_of[n] - 0.5, y_of[n] + 0.5, color='#5DADE2',
                   alpha=blue_a[y_of[n] - 4], lw=0, zorder=0)
for n in names[4:]:
    ax_mid.axhspan(y_of[n] - 0.5, y_of[n] + 0.5, color='#E6B0AA',
                   alpha=red_a[y_of[n]], lw=0, zorder=0)
ax_mid.set_zorder(ax_top.get_zorder() + 1)
ax_mid.patch.set_visible(False)

# ---------------- 点阵改空心圆
for coll in ax_mid.collections:
    coll.set_facecolor('none')
    coll.set_edgecolor('black')
    coll.set_linewidth(0.9)

# ---------------- 左侧 setSize 条形: 蓝系(前4) / 红系(后4)
blue_shades = ['#1A5276', '#2E86C1', '#5DADE2', '#A9CCE3']
red_shades = ['#F5B7B1', '#E6B0AA', '#CD6155', '#922B21']
ax_left = ax_mid.figure.axes[-1]
for t in list(ax_left.texts):
    t.remove()
xmax = ax_left.get_xlim()[1]
for p, n in zip(ax_left.patches, names):
    shade = blue_shades if n in names[:4] else red_shades
    p.set_facecolor(shade[y_of[n] % 4 if n in names[:4] else y_of[n]])
    inside = p.get_width() > 0.35 * xmax
    ax_left.text(p.get_width() / 2 if inside else p.get_width() + 0.02 * xmax,
                 p.get_y() + p.get_height() / 2, str(len(sets[n])),
                 ha='center' if inside else 'left', va='center',
                 fontsize=6, color='white' if inside else '#333')
ax_mid.tick_params(labelleft=False)
ax_left.set_xlabel('size', fontsize=7)

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
inter = inter[:25]

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
    g_top.text(x, c, str(c), ha='center', va='bottom', fontsize=5.5)
g_top.set_ylim(0, max(c for _, c in inter) * 1.2)
g_top.set_xlim(ax_top.get_xlim())
g_top.set_xticks([])
g_top.set_ylabel('Intersection size', fontsize=7)
y_of = {nm: n_set - 1 - i for i, nm in enumerate(names)}
for x, (comb, _) in zip(xs, inter):
    ys = [y_of[names[c_]] for c_ in comb]
    if len(ys) > 1:
        g_mid.plot([x, x], [min(ys), max(ys)], color='k', lw=0.9, zorder=2)
    g_mid.scatter([x] * len(ys), ys, s=22, color='k', zorder=3)
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
                va='center', fontsize=5.5)
g_left.set_xlim(ax_left.get_xlim())
g_left.set_yticks([y_of[nm] for nm in names])
g_left.set_yticklabels(names, fontsize=6.5)
g_left.set_xticks([0, 500, 1000, 1500])
g_left.set_xticklabels(['0', '500', '1000', '1500'], fontsize=5, rotation=90)
g_left.tick_params(axis='x', pad=1)
g_left.set_xlabel('Set size', fontsize=7)
for a in (g_top, g_mid, g_left):
    for sp in ['top', 'right']:
        a.spines[sp].set_visible(False)
g_mid.spines['left'].set_visible(False)

save(fig, 'case_seg115.png')
