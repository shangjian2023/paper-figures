# -*- coding: utf-8 -*-
"""案例24 - Nature 折线图与柱形图: 左右双面板。
参考: frames/seg_024.jpg — 左: Control(黑圆)/Acox1-LKO(红方) 体重曲线 ±SEM,
点上方竖排 P 值; 右: Fat/Lean 双柱 + 散点, 0.0154 显著线, 图例左上。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

set_style()

r = rng(24)
weeks = np.arange(0, 12)
ctl = np.array([22.6, 26.4, 29.6, 32.6, 37.2, 40.2, 41.6, 41.9, 41.6,
                42.0, 42.7, 43.6])
lko = np.array([22.4, 24.8, 26.3, 29.0, 32.1, 34.1, 35.6, 36.4, 36.3,
                36.5, 36.8, 38.6])
pvals = [None, None, None, None, '0.0385', '0.0412', '0.0396', '0.0289',
         '0.0389', '0.0329', '0.0296', '0.060']
sem_c = np.linspace(0.55, 1.6, 12)
sem_l = np.linspace(0.45, 1.1, 12)

fig, axes = plt.subplots(1, 2, figsize=cm2in(16.5, 8.8),
                         gridspec_kw={'width_ratios': [1.35, 1]})
ax, ax2 = axes

# ---- 左面板: 体重折线 ----
ax.errorbar(weeks, ctl, yerr=sem_c, color='black', fmt='-o', ms=4.5,
            elinewidth=1.0, capsize=2.5, zorder=3)
ax.errorbar(weeks, lko, yerr=sem_l, color='#D92B2B', fmt='-s', ms=4.5,
            mfc='#D92B2B', elinewidth=1.0, capsize=2.5, zorder=3)
for i, p in enumerate(pvals):
    if p:
        ax.text(weeks[i], max(ctl[i], lko[i]) + 2.6, p, rotation=90,
                ha='center', va='bottom', fontsize=6.3)
ax.set_xlim(-0.4, 11.6)
ax.set_ylim(12, 53)
ax.set_xticks(range(0, 12, 2))
ax.set_yticks([10, 15, 20, 25, 30, 35, 40, 45, 50])
ax.set_xlabel('Weeks (HFD)')
ax.set_ylabel('Body weight (g)')
ax.legend([Line2D([], [], color='black', marker='o', ms=4.5, lw=1.2),
           Line2D([], [], color='#D92B2B', marker='s', ms=4.5, lw=1.2)],
          ['Control', 'Acox1-LKO'], loc='upper left', frameon=False,
          bbox_to_anchor=(0.02, 1.0), fontsize=8)

# ---- 右面板: Fat/Lean 柱 + 散点 ----
fat_c = r.normal(19.5, 2.6, 9).clip(13, 24)
fat_l = r.normal(15.0, 2.4, 9).clip(8, 20)
lean_c = r.normal(22.0, 0.9, 9).clip(19.5, 26)
lean_l = r.normal(21.2, 1.0, 9).clip(18, 24)
groups = [(fat_c, fat_l, 0), (lean_c, lean_l, 1)]
for dc, dl, x in groups:
    ax2.bar(x - 0.17, dc.mean(), width=0.3, facecolor='white',
            edgecolor='black', lw=1.2, zorder=2)
    ax2.bar(x + 0.17, dl.mean(), width=0.3, facecolor='white',
            edgecolor='#D92B2B', lw=1.2, zorder=2)
    ax2.errorbar([x - 0.17], [dc.mean()],
                 yerr=[dc.std(ddof=1) / np.sqrt(len(dc))], fmt='none',
                 ecolor='black', elinewidth=1.0, capsize=3, zorder=3)
    ax2.errorbar([x + 0.17], [dl.mean()],
                 yerr=[dl.std(ddof=1) / np.sqrt(len(dl))], fmt='none',
                 ecolor='#D92B2B', elinewidth=1.0, capsize=3, zorder=3)
    ax2.scatter(x - 0.17 + r.uniform(-0.05, 0.05, len(dc)), dc, s=12,
                color='black', zorder=4, lw=0)
    ax2.scatter(x + 0.17 + r.uniform(-0.05, 0.05, len(dl)), dl, s=12,
                color='#D92B2B', marker='s', zorder=4, lw=0)
# 0.0154 显著线 (Fat mass)
ax2.plot([-0.34, 0.34], [25.2, 25.2], color='black', lw=1.0)
ax2.text(0, 25.7, '0.0154', ha='center', va='bottom', fontsize=7)
ax2.set_xlim(-0.6, 1.6)
ax2.set_ylim(0, 31.5)
ax2.set_yticks([0, 10, 20, 30])
ax2.set_xticks([0, 1])
ax2.set_xticklabels(['Fat mass', 'Lean mass'])
ax2.set_ylabel('Body composition (g)')
ax2.legend([Line2D([], [], color='black', marker='o', ms=4, lw=0),
            Line2D([], [], color='#D92B2B', marker='s', ms=4, lw=0)],
           ['Control', 'Acox1-LKO'], loc='upper left', frameon=False,
           bbox_to_anchor=(0.02, 1.0), fontsize=8)

fig.subplots_adjust(wspace=0.34)
save(fig, 'case_seg024.png')
