# -*- coding: utf-8 -*-
"""案例121 - cell 带显著性的小提琴图(一): 7 组 × 2 成对小提琴,
顶部彩色组标签矩形 + < 2.2e-16 括号, 白点=中位数, 图例右下。
参考: frames/seg_121.jpg — Active(粉) vs Repressive(深蓝)。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib.patches import Patch

set_style()

groups = [('Exc', '#22A022', 'white'), ('Inh', '#90D060', 'black'),
          ('Ast', '#C02020', 'white'), ('Oli', '#E89040', 'black'),
          ('OPC', '#8B4513', 'white'), ('Mic/\nImmune', '#B0A0D0', 'black'),
          ('Vasc', '#E8A0C0', 'black')]
C_ACT, C_REP = '#E8B4D0', '#1F4E9C'
r = rng(121)

fig, ax = plt.subplots(figsize=cm2in(16.5, 10.0))
for gi, (name, rc, tc) in enumerate(groups):
    xc = gi * 1.0
    for off, mu, sd, c in [(-0.18, 0.575, 0.048, C_ACT),
                           (0.18, 0.615, 0.022, C_REP)]:
        vals = r.normal(mu, sd, 400)
        k = gaussian_kde(vals)
        grid = np.linspace(max(vals.min(), 0.43), min(vals.max(), 0.665), 120)
        w = 0.15 * k(grid) / k(grid).max()
        ax.fill(np.concatenate([xc + off - w, (xc + off + w)[::-1]]),
                np.concatenate([grid, grid[::-1]]),
                facecolor=c, edgecolor='none', zorder=2)
        md = np.median(vals)
        ax.scatter([xc + off], [md], s=26, c='white', edgecolors='black',
                   linewidths=0.6, zorder=4)
        q1, q3 = np.percentile(vals, [25, 75])
        ax.plot([xc + off, xc + off], [q1, q3], c='white', lw=1.0, zorder=3)
    # 顶部组标签矩形
    ax.add_patch(plt.Rectangle((xc - 0.34, 0.745), 0.68, 0.055, facecolor=rc,
                               edgecolor='none', clip_on=False, zorder=5))
    ax.text(xc, 0.7725, name, ha='center', va='center', color=tc,
            fontsize=9, fontweight='bold', clip_on=False, zorder=6)
    # P 值 + 小括号
    it = r'$\it{P}$'
    ax.text(xc, 0.728, f'< 2.2e-16'.replace('<', '< ', 1), ha='center',
            va='bottom', fontsize=7.5, clip_on=False)
    bx = 0.26
    ax.plot([xc - bx, xc - bx, xc + bx, xc + bx],
            [0.712, 0.706, 0.706, 0.712], c='black', lw=0.8, clip_on=False)

# 图例右下
handles = [Patch(facecolor=C_ACT, edgecolor='none'),
           Patch(facecolor=C_REP, edgecolor='none')]
ax.legend(handles, ['Active', 'Repressive'], loc='lower right',
          bbox_to_anchor=(0.98, 0.06), title='Epigenomic\ncompartment',
          frameon=False, fontsize=9, title_fontsize=9, handlelength=1.1,
          handleheight=1.1, labelspacing=0.5, borderaxespad=0)

ax.set_xlim(-0.6, 6.6)
ax.set_ylim(0.42, 0.675)
ax.set_xticks(np.arange(7))
ax.set_xticklabels([''] * 7)
ax.tick_params(axis='x', length=4)
ax.set_yticks([0.4, 0.5, 0.6, 0.7])
ax.set_ylabel('A/T content', fontsize=10)
ax.tick_params(labelsize=9)
despine(ax)

save(fig, 'case_seg121.png')
