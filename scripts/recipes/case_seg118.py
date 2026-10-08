# -*- coding: utf-8 -*-
"""案例118 - Sci. Adv 曼哈顿式气泡图: 3 层堆叠面板, x=目级分类位次,
气泡色=目、大小=丰度, 灰竖分隔线, 0/±1 虚线, 底部彩点+旋转类目标签。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

set_style()

ORDERS = ['Bacteroidales', 'Clostridiales', 'Lactobacillales', 'Burkholderiales',
          'Enterobacteriales', 'Pseudomonadales', 'Rhizobiales', 'Actinomycetales',
          'Bacillales', 'Campylobacterales', 'Desulfovibrionales', 'Sphingomonadales',
          'Flavobacteriales', 'Cytophagales', 'Mycoplasmatales', 'Spirochaetales',
          'Verrucomicrobiales', 'Rickettsiales', 'Corynebacteriales', 'Mycobacteriales']
COMP = [('Antibiotics vs Ctrl (gut)', 42), ('High-fat diet vs Ctrl (gut)', 47),
        ('Probiotics vs Ctrl (gut)', 39)]
r = rng(118)
cmap = plt.get_cmap('tab20')

fig, axes = plt.subplots(3, 1, figsize=cm2in(18, 14), sharex=True,
                         gridspec_kw={'height_ratios': [1, 1, 1], 'hspace': 0.28})
# 底部留出竖排类目标签带(标签画在坐标轴外, 不与 -1 行方块/刻度叠压)
fig.subplots_adjust(bottom=0.17, top=0.93)
# 类目索引与颜色(3 层共享同一排序与配色)
n_per = [r.integers(3, 7) for _ in ORDERS]
cats, colors, xtick_pos, xtick_lab = [], [], [], []
xi = 0
for oi, od in enumerate(ORDERS):
    for k in range(n_per[oi]):
        cats.append({'x': xi, 'order': od, 'color': cmap(oi % 20)})
        xtick_pos.append(xi)
        xtick_lab.append(od)
        xi += 1
    xi += 1  # 类目间隔
n_total = xi - 1
bounds = np.cumsum([0] + n_per + [0])
seps = []
acc = 0
for oi in range(len(ORDERS) - 1):
    acc += n_per[oi]
    seps.append(acc + 0.5 + oi * 1)  # 与下面 x 映射一致

for ai, ax in enumerate(axes):
    xi = 0
    for oi, od in enumerate(ORDERS):
        for k in range(n_per[oi]):
            lfc = r.normal(0.15 * (ai - 1) * (1 + (oi % 3 - 1)), 0.9)
            ab = r.uniform(3, 30) ** 2 / 30
            ax.scatter(xi, lfc, s=ab, color=cmap(oi % 20), alpha=0.85,
                       edgecolor='white', lw=0.4, zorder=3)
            xi += 1
        xi += 1
    # 类目分隔线
    xi = 0
    for oi in range(len(ORDERS) - 1):
        xi += n_per[oi]
        ax.axvline(xi + 0.5, color='#BBBBBB', lw=0.6, zorder=1)
        xi += 1
    ax.axhline(0, color='#888888', ls='--', lw=0.7, zorder=2)
    ax.axhline(1, color='#BBBBBB', ls='--', lw=0.6, zorder=2)
    ax.axhline(-1, color='#BBBBBB', ls='--', lw=0.6, zorder=2)
    ax.set_ylim(-4.6, 4.6)
    ax.set_ylabel('Log2FCs')
    ax.text(0.005, 0.96, COMP[ai][0], transform=ax.transAxes,
            fontsize=7, fontweight='bold', va='top')
    ax.spines['bottom'].set_visible(ai == 2)
    if ai < 2:
        ax.tick_params(labelbottom=False)

axes[2].set_xlim(-1, n_total + 1)
axes[2].set_xticks(xtick_pos)
axes[2].set_xticklabels([])
# 底部彩点(方块=类目色键, 置于轴线以下)+旋转类目名(每目取其首个 ASV 位置)
xi = 0
for oi, od in enumerate(ORDERS):
    axes[2].scatter(xi, -5.18, marker='s', s=14, color=cmap(oi % 20), clip_on=False)
    axes[2].text(xi + 0.1, -5.6, od, rotation=90, ha='left', va='top',
                 fontsize=4.8, color=cmap(oi % 20), clip_on=False)
    xi += n_per[oi] + 1
axes[2].set_ylim(-4.6, 4.6)

# ---- 面板1右上: 气泡大小图例 ----
leg_handles = [
    Line2D([], [], marker='o', ls='none', mfc='#7A7A7A', mec='#7A7A7A', ms=3,
           label='low abundance'),
    Line2D([], [], marker='o', ls='none', mfc='#7A7A7A', mec='#7A7A7A', ms=7.5,
           label='high abundance'),
]
axes[0].legend(handles=leg_handles, loc='upper right', bbox_to_anchor=(1.0, 1.02),
               ncol=2, frameon=False, fontsize=6, title='bubble size = abundance',
               title_fontsize=6, columnspacing=0.8, handletextpad=0.4,
               handlelength=1.0, borderaxespad=0.2)

save(fig, 'case_seg118.png')
