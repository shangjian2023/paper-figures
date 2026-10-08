# -*- coding: utf-8 -*-
"""案例5 - Nature 云雨图: 4组 抖动散点(左) + 半小提琴(右) + 白底窄箱线。
参考: frames/seg_005.jpg — subtilis/cereus/megaterium/circulans, Y=0-30。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib.patches import Patch

set_style()


def half_violin(ax, x0, vals, color, width=0.34, side=1):
    """竖直半小提琴: 从 x0 向 side 方向展开 KDE 填充多边形。"""
    k = gaussian_kde(vals)
    grid = np.linspace(vals.min(), vals.max(), 140)
    w = width * k(grid) / k(grid).max()
    xs = np.concatenate([[x0], x0 + side * w, [x0]])
    ys = np.concatenate([[grid[0]], grid, [grid[-1]]])
    ax.fill(xs, ys, facecolor=color, edgecolor='black', lw=0.7, zorder=2)


def slim_box(ax, x0, vals, width=0.075):
    """白底窄箱线 + 通体须线, 叠在半小提琴中轴上。"""
    ax.boxplot(vals, positions=[x0], widths=width, whis=(0, 100),
               patch_artist=True,
               boxprops=dict(facecolor='white', edgecolor='black', lw=1.0),
               medianprops=dict(color='black', lw=1.2),
               whiskerprops=dict(color='black', lw=0.8),
               capprops=dict(color='black', lw=0.8),
               showfliers=False, zorder=3)


groups = ['subtilis', 'cereus', 'megaterium', 'circulans']
colors = ['#7FB04C', '#A83248', '#D29B2C', '#8C8C8C']
ns = [420, 430, 210, 200]
r = rng(5)
data = [r.normal(12.0, 5.2, ns[0]).clip(2, 30),
        r.normal(11.6, 5.4, ns[1]).clip(1, 28.5),
        r.normal(7.0, 2.8, ns[2]).clip(2, 17.5),
        r.normal(4.3, 1.8, ns[3]).clip(0.4, 9.5)]

fig, ax = plt.subplots(figsize=cm2in(13.5, 9.5))
for i, (g, d) in enumerate(zip(groups, data)):
    xc = i * 1.0
    # 左侧抖动散点
    jit = rng(50 + i).uniform(-0.24, 0.06, len(d))
    ax.scatter(xc - 0.30 + jit, d, s=5, color=colors[i], alpha=0.75,
               linewidths=0, zorder=2)
    # 右侧半小提琴 + 中轴窄箱线
    x0 = xc + 0.04
    half_violin(ax, x0, d, colors[i], width=0.32, side=1)
    slim_box(ax, x0, d)

ax.set_xticks(np.arange(len(groups)))
ax.set_xticklabels([r'$\bf{\it{%s}}$' % g for g in groups], fontsize=10)
ax.set_xlim(-0.75, 3.55)
ax.set_ylim(-0.8, 31)
ax.set_yticks([0, 5, 10, 15, 20, 25, 30])
ax.set_ylabel('No. of BGCs / genome', fontsize=10)
ax.tick_params(axis='y', labelsize=9)
despine(ax)

handles = [Patch(facecolor=c, edgecolor='black', lw=0.6) for c in colors]
ax.legend(handles, [r'$\bf{\it{%s}}$' % g for g in groups], loc='center left',
          bbox_to_anchor=(1.02, 0.45), frameon=False, fontsize=9,
          handlelength=1.1, handleheight=1.1, borderaxespad=0)

save(fig, 'case_seg005.png')
