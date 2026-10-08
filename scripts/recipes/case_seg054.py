# -*- coding: utf-8 -*-
"""案例56(seg54) - Nature 配对散点: 配对竖灰线 + 双平滑曲线+置信带 + 右侧边缘密度弧。
参考: frames/seg_054.jpg — 深蓝=given coordination, 灰空心=no coordination。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

set_style()

r = rng(54)
n = 190
x = np.arange(n, dtype=float)

def f_given(t):
    return 3.85 * (1 - np.exp(-t / 70.0)) - 1.15

def f_none(t):
    return 0.78 - 1.85 * (1 - np.exp(-t / 75.0))

y1 = f_given(x) + r.normal(0, 0.27, n)
y2 = f_none(x) + r.normal(0, 0.30, n)
y1[0] -= 0.55                                   # 左端两个低离群
y1[1] -= 0.10
y2[1] += 0.25

fig = plt.figure(figsize=cm2in(13.5, 9.2))
gs = fig.add_gridspec(1, 2, width_ratios=[5.0, 0.62], wspace=0.045,
                      left=0.10, right=0.985, top=0.97, bottom=0.13)
ax = fig.add_subplot(gs[0])
axm = fig.add_subplot(gs[1], sharey=ax)

# ---------------- 配对竖线 ----------------
for i in range(n):
    ax.plot([i, i], [y1[i], y2[i]], color='#C4C4C4', lw=0.45, zorder=1)

# ---------------- 曲线 + 置信带 ----------------
tt = np.linspace(0, n - 1, 300)
band1 = 0.06 + 0.16 * np.exp(-tt / 55.0)
band2 = 0.05 + 0.12 * np.exp(-tt / 55.0)
ax.fill_between(tt, f_given(tt) - band1, f_given(tt) + band1,
                color='#7B93D9', alpha=0.45, lw=0, zorder=2)
ax.fill_between(tt, f_none(tt) - band2, f_none(tt) + band2,
                color='#BDBDBD', alpha=0.35, lw=0, zorder=2)
ax.plot(tt, f_given(tt), color='#1F3B8C', lw=2.0, zorder=4)
ax.plot(tt, f_none(tt), color='#8C8C8C', lw=1.6, zorder=4)

# ---------------- 散点 ----------------
ax.scatter(x, y2, s=13, facecolors='none', edgecolors='#8F8F8F',
           linewidths=0.8, zorder=3, label='BC given no AB coordination')
ax.scatter(x, y1, s=13, color='#1F3B8C', zorder=4,
           label='BC given AB coordination')

# ---------------- 右侧边缘密度 ----------------
grid = np.linspace(-2.4, 3.6, 300)
d1 = gaussian_kde(y1)(grid); d1 = d1 / d1.max()
d2 = gaussian_kde(y2)(grid); d2 = d2 / d2.max()
axm.fill_betweenx(grid, 0, d1, color='#7B93D9', alpha=0.50, lw=0)
axm.plot(d1, grid, color='#1F3B8C', lw=1.0)
axm.fill_betweenx(grid, 0, d2, color='#BDBDBD', alpha=0.45, lw=0)
axm.plot(d2, grid, color='#8C8C8C', lw=1.0)
axm.set_xlim(0, 1)
axm.axis('off')

# ---------------- 装饰 ----------------
ax.set_xlim(-5, n + 4)
ax.set_ylim(-2.35, 3.45)
ax.set_yticks([-2, -1, 0, 1, 2, 3])
ax.set_xticks([0, 50, 100, 150])
ax.set_xlabel(r'all triplets (sorted on increasing $\Delta$Z)', fontsize=10)
ax.set_ylabel('BC coordination', fontsize=10)

# 图例: 线段+点 组合句柄
from matplotlib.lines import Line2D
h1 = [Line2D([], [], color='#1F3B8C', lw=2.0, marker='o', ms=5.5),
      Line2D([], [], color='#8C8C8C', lw=1.6, marker='o', ms=5.5,
             mfc='none')]
ax.legend(h1, ['BC given AB coordination', 'BC given no AB coordination'],
          loc='upper left', frameon=False, fontsize=9, borderaxespad=0.2,
          handlelength=1.6, labelspacing=0.5)

# "stronger triplets" 箭头注释
ax.annotate('', xy=(0.72, 0.055), xytext=(0.60, 0.055),
            xycoords='axes fraction',
            arrowprops=dict(arrowstyle='-|>', color='black', lw=1.1))
ax.text(0.735, 0.055, 'stronger triplets', transform=ax.transAxes,
        ha='left', va='center', fontsize=9.5)

save(fig, 'case_seg054.png')
