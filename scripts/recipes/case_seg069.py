# -*- coding: utf-8 -*-
"""案例69 - Nature 差异云雨图(一): 两组, 外侧半小提琴 + 中间箱线 + 内侧点阵雨。
参考: frames/seg_069.jpg — Epilepsy(紫) vs Control(黄), p < 2.22e-16。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

set_style()

r = rng(69)
d_epi = r.normal(-10, 24, 380).clip(-72, 58)
d_ctl = r.normal(16, 21, 380).clip(-68, 58)

fig, ax = plt.subplots(figsize=cm2in(11.5, 13.0))


def half_violin(ax, x0, vals, color, width=0.30, side=1):
    k = gaussian_kde(vals)
    grid = np.linspace(vals.min(), vals.max(), 160)
    w = width * k(grid) / k(grid).max()
    ax.fill(np.concatenate([[x0], x0 + side * w, [x0]]),
            np.concatenate([[grid[0]], grid, [grid[-1]]]),
            facecolor=color, edgecolor=color, lw=0.5, zorder=2)


# Epilepsy (x=0): 散点在左, 箱线居中, 半小提琴朝右
jit = r.uniform(-0.24, 0.06, len(d_epi))
ax.scatter(-0.42 + jit, d_epi, s=6, color='#6A4FC0', alpha=0.85,
           linewidths=0, zorder=3)
ax.boxplot(d_epi, positions=[-0.06], widths=0.13, patch_artist=True,
           whis=(0, 100),
           boxprops=dict(facecolor='#C8B8E8', edgecolor='black', lw=0.9),
           medianprops=dict(color='black', lw=1.2),
           whiskerprops=dict(color='black', lw=0.7),
           capprops=dict(color='black', lw=0.7),
           showfliers=False, zorder=4, manage_ticks=False)
half_violin(ax, 0.05, d_epi, '#6A4FC0', width=0.30, side=1)

# Control (x=1): 散点在左, 箱线居中, 半小提琴朝右
jit = r.uniform(-0.24, 0.06, len(d_ctl))
ax.scatter(0.58 + jit, d_ctl, s=6, color='#E8C020', alpha=0.85,
           linewidths=0, zorder=3)
ax.boxplot(d_ctl, positions=[0.94], widths=0.13, patch_artist=True,
           whis=(0, 100),
           boxprops=dict(facecolor='#F5E6A8', edgecolor='black', lw=0.9),
           medianprops=dict(color='black', lw=1.2),
           whiskerprops=dict(color='black', lw=0.7),
           capprops=dict(color='black', lw=0.7),
           showfliers=False, zorder=4, manage_ticks=False)
half_violin(ax, 1.05, d_ctl, '#F5C518', width=0.30, side=1)

ax.set_xlim(-0.85, 1.55)
ax.set_ylim(-80, 72)
ax.set_xticks([0, 1])
ax.set_xticklabels(['Epilepsy', 'Control'], fontsize=9)
ax.set_yticks([-40, 0, 40])
ax.set_ylabel('Network overlap (%)', fontsize=9.5)
ax.tick_params(length=3)
despine(ax)

sig_bracket(ax, -0.06, 0.94, 62, r'p < 2.22e-16', h=2.5, fontsize=10)

save(fig, 'case_seg069.png')
