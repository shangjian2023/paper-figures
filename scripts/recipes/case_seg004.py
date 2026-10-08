# -*- coding: utf-8 -*-
"""案例4 - Nature 折线图: 4 组折线 + 顶部 iAUC 内嵌条形。
参考: frames/seg_004.jpg — 蓝/红/青/黄空心圆 ±SEM, day20 黑虚线 + 右侧灰底,
顶部两个 iAUC 内嵌条形(带散点/***), 右侧显著性括号, 图例顶部横排。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

set_style()

colors = ['#4C88C6', '#E8646C', '#12A08B', '#F2CE4B']
labels = ['Non-\nSMK', 'SMK', 'Non-\nSMK +abx', 'SMK\n+abx']

days = np.array([0, 7, 14, 20, 26, 30, 35])
means = np.array([
    [0.0, 6.0, 14.0, 18.0, 25.0, 29.0, 31.0],    # Non-SMK
    [0.0, 2.5, 3.2, 3.6, 17.5, 27.0, 29.0],      # SMK
    [0.0, 8.5, 18.0, 22.5, 30.0, 35.0, 38.5],    # Non-SMK +abx
    [0.0, 1.5, 2.0, 1.6, 12.0, 17.0, 19.0],      # SMK +abx
])
r = rng(4)
sems = r.uniform(0.6, 1.5, means.shape)
sems[:, 0] = 0.0

fig, ax = plt.subplots(figsize=cm2in(14.5, 15.5))
ax.axvspan(20, 40, color='0.88', zorder=0)
ax.axvline(20, color='black', ls='--', lw=1.3, zorder=1)
for i in range(4):
    ax.errorbar(days, means[i], yerr=sems[i], color=colors[i], fmt='-o',
                ms=6.5, mfc='white', mew=1.6, elinewidth=1.1, capsize=3,
                zorder=3)

# ---- 右侧显著性竖括号 ----
def vbracket(x, y1, y2, text):
    ax.plot([x, x], [y1, y2], lw=1.0, color='black')
    ax.plot([x - 0.7, x], [y1, y1], lw=1.0, color='black')
    ax.plot([x - 0.7, x], [y2, y2], lw=1.0, color='black')
    ax.text(x + 0.7, (y1 + y2) / 2, text, rotation=90, va='center',
            ha='left', fontsize=8)

vbracket(36.9, 29.0, 31.6, '***')
vbracket(38.3, 19.2, 38.6, '****')

ax.set_xlim(-1.5, 41)
ax.set_ylim(0, 60)
ax.set_xticks([0, 10, 20, 30, 40])
ax.set_yticks([0, 20, 40, 60])
ax.set_xlabel('Day')
ax.set_ylabel('Weight change (%)')

# ---- 顶部两个 iAUC 内嵌条形轴 ----
def iauc_inset(bounds, vals, title, xticks):
    axi = ax.inset_axes(bounds)
    for s in axi.spines.values():
        s.set_visible(True)
        s.set_linewidth(0.8)
    ys = np.arange(4)[::-1].astype(float)
    axi.barh(ys, vals, height=0.52, color='white', edgecolor='0.2',
             lw=1.0, zorder=2)
    for k, v in enumerate(vals):
        rj = rng(400 + k)
        n = 20
        sx = v + rj.normal(0, max(abs(v) * 0.35, 18), n)
        sy = ys[k] + rj.uniform(-0.16, 0.16, n)
        axi.scatter(sx, sy, s=6, color=colors[k], alpha=0.9,
                    linewidths=0, zorder=3)
    axi.set_xlim(min(xticks[0], min(vals) * 1.4), max(xticks[-1], 820))
    axi.set_ylim(-0.6, 3.6)
    axi.set_xticks(xticks)
    axi.tick_params(labelsize=7, length=2.5)
    axi.set_yticks([])
    axi.set_title(title, fontsize=8.5, loc='left', pad=2)
    # 右侧组间括号 (行0-1, 行2-3)
    xl = axi.get_xlim()
    xb = xl[1] - (xl[1] - xl[0]) * 0.10
    dt = (xl[1] - xl[0]) * 0.035
    for y1, y2, txt in [(3, 2, '***'), (1, 0, '***')]:
        axi.plot([xb, xb], [y1, y2], lw=0.8, color='black')
        axi.plot([xb - dt, xb], [y1, y1], lw=0.8, color='black')
        axi.plot([xb - dt, xb], [y2, y2], lw=0.8, color='black')
        axi.text(xb + dt, (y1 + y2) / 2, txt, rotation=90, va='center',
                 fontsize=5.5)

iauc_inset([0.13, 0.735, 0.36, 0.245], [250, -110, 380, -60],
           'iAUC: Exposure', [-200, 300, 800])
iauc_inset([0.60, 0.735, 0.37, 0.245], [120, 260, 100, 130],
           'iAUC: Cessation', [0, 200, 400])

# ---- 图例顶部横排 ----
handles = [Patch(facecolor=c, edgecolor='none') for c in colors]
ax.legend(handles, labels, loc='lower left', bbox_to_anchor=(-0.02, 1.01),
          ncol=4, frameon=False, handlelength=1.5, handleheight=1.1,
          columnspacing=1.2, fontsize=8.5)

save(fig, 'case_seg004.png')
