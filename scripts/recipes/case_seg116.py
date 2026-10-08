# -*- coding: utf-8 -*-
"""案例116 - Sci. Adv 曼哈顿式气泡图: 3层堆叠, x=目级分类位次,
y=Log2(FCs), 气泡色=目(彩虹) 大小=丰度; 灰竖分隔线, 0/±1虚线,
底部彩点+旋转类目标签。参考: frames/seg_116.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D

set_style()

ORDERS = [
    ('Burkholderiales', '#c23b4a'), ('Chitinophagales', '#e0693c'),
    ('Prellales', '#e8873d'), ('PCC-6307', '#f0ab3c'),
    ('Chthoniobacterales', '#e3c94f'), ('Cytophagales', '#c9c94f'),
    ('Rhodobacterales', '#a3c44f'), ('Gemmatimonadales', '#78b848'),
    ('Planctomycetales', '#54a857'), ('Flavobacteriales', '#4f9e6e'),
    ('Rickettsiales', '#4fa08a'), ('Verrucomicrobiales', '#4a9aa8'),
    ('Sphingomonadales', '#4a8ab8'), ('Pedosphaerales', '#5578b8'),
    ('NS11-12g', '#5f68b0'), ('Rhizobiales', '#6b5aa8'),
    ('Acetobacteraceae', '#7b55a8'), ('UBA796', '#8b4fa0'),
    ('Nieskiales', '#9b4a98'), ('Actinomycetales', '#a84488'),
    ('Caulobacterales', '#b84078'), ('Steroidobacterales', '#c04468'),
    ('Nanopelagicales', '#b85c58'), ('Phycisphaerales', '#a87868'),
    ('Xanthomonadales', '#989088')]

TITLES = ['B_ AZM vs B', 'Co_ FL_ AZM vs Co_ FL', 'Co_ PS_ AZM vs Co_ PS']

r = rng(116)
axes_list = []
# 每目的 OTU 气泡: x 位置(块内), y=log2FC, 大小=丰度
data = []
x = 6.0
bounds = []
for name, col in ORDERS:
    n = int(r.integers(7, 20))
    xs, ys, ss, hollow = [], [], [], []
    for _ in range(n):
        xs.append(x + r.uniform(0, 6.4))
        yv = r.normal(0, 0.85)
        if r.random() < 0.14:
            yv = r.choice([-1, 1]) * r.uniform(1.2, 2.5)
        ys.append(np.clip(yv, -3.4, 3.4))
        ss.append(8 + r.exponential(45))
        # 空心 = 不显著(|log2FC| 未过 ±1 阈值); 实心 = 显著
        hollow.append(abs(yv) < 0.8 and r.random() < 0.6)
    data.append((name, col, xs, ys, ss, hollow))
    bounds.append(x + 3.2)
    x += 12.4
XMAX = x - 6.4

fig = plt.figure(figsize=cm2in(16.5, 18.5))
gs = GridSpec(4, 1, left=0.085, right=0.985, top=0.985, bottom=0.115,
              height_ratios=[1, 1, 1, 0.42], hspace=0.28)

for p in range(3):
    ax = fig.add_subplot(gs[p])
    axes_list.append(ax)
    for i, (name, col, xs, ys, ss, hollow) in enumerate(data):
        if p == 0:
            pass
        for x_, y_, s_, hol in zip(xs, ys, ss, hollow):
            rr2 = r.random()
            yy = y_ + r.normal(0, 0.35)
            if hol:
                ax.scatter([x_], [yy], s=s_, facecolor='none',
                           edgecolor=col, linewidth=1.0, alpha=0.8, zorder=3)
            else:
                ax.scatter([x_], [yy], s=s_, color=col, alpha=0.75, lw=0,
                           zorder=3)
    for bx in bounds[:-1]:
        ax.axvline(bx + 3.0, color='0.82', lw=0.7, zorder=1)
    for yv in (-1, 0, 1):
        ax.axhline(yv, color='0.65', ls=(0, (2, 2)), lw=0.8, zorder=2)
    ax.text(XMAX + 1.6, 1.12, '±1 log$_2$FC', fontsize=6, color='0.35',
            ha='right', va='bottom', zorder=4,
            path_effects=[pe.withStroke(linewidth=1.8, foreground='white')])
    ax.set_xlim(-2, XMAX + 2)
    ax.set_ylim(-4.2, 4.2)
    ax.set_yticks([-4, -2, 0, 2, 4])
    ax.set_ylabel('Log$_2$(FCs)', fontsize=9)
    ax.tick_params(labelsize=7.5)
    ax.set_xticks([])
    if p < 2:
        ax.tick_params(labelbottom=False)
    ax.text(0.995, 0.06, TITLES[p], transform=ax.transAxes, fontsize=9,
            ha='right', va='bottom')

# ---------------- 面板1顶部: 气泡大小 + 实心/空心 图例 ----------------
leg_handles = [
    Line2D([], [], marker='o', ls='none', mfc='0.45', mec='0.45', ms=3,
           label='size: low abundance'),
    Line2D([], [], marker='o', ls='none', mfc='0.45', mec='0.45', ms=9,
           label='size: high abundance'),
    Line2D([], [], marker='o', ls='none', mfc='#4a8ab8', mec='#4a8ab8', ms=6.5,
           label='filled: significant'),
    Line2D([], [], marker='o', ls='none', mfc='none', mec='#4a8ab8', mew=1.0,
           ms=6.5, label='hollow: not significant'),
]
axes_list[0].legend(handles=leg_handles, loc='upper left', bbox_to_anchor=(0.005, 1.0),
                    ncol=4, frameon=False, fontsize=6.3, columnspacing=0.9,
                    handletextpad=0.4, handlelength=1.0, borderaxespad=0.2)

# ---------------- 底部: 彩点 + 旋转类目标签 ----------------
axb = fig.add_subplot(gs[3])
axb.set_xlim(-2, XMAX + 2)
axb.set_ylim(-9.5, 1.2)
axb.axis('off')
for i, (name, col, xs, ys, ss, hollow) in enumerate(data):
    cx = float(np.mean(xs))
    axb.scatter([cx], [0], s=26, color=col, lw=0, zorder=3)
    axb.text(cx, -0.9, name, rotation=90, fontsize=6.8, ha='center',
             va='top', color='#333333')

save(fig, 'case_seg116.png')
