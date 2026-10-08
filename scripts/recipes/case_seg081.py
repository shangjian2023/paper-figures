# -*- coding: utf-8 -*-
"""案例83 - Nature FC-FC 四象限散点: 紫(同向)/品红/蓝(反向)/灰(NS), ±0.5 虚线,
四角 Concordant/Discordant + HARE5 注记。
参考: frames/seg_081.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt

set_style()

r = rng(81)
n = 1750
t = r.normal(0, 2.7, n)
x = t + r.normal(0, 1.15, n)
y = t + r.normal(0, 1.15, n)

# 分类: 灰=NS(中心云); 紫=对角带同向; 品红=同向但偏离对角; 蓝=反向
d = y - x
cls = np.zeros(n, dtype=int)                          # 0=紫
con = ((x > 0.55) & (y > 0.55)) | ((x < -0.55) & (y < -0.55))
disc = ((x > 0.55) & (y < -0.55)) | ((x < -0.55) & (y > 0.55))
cls[disc] = 2                                         # 蓝
gray = (np.abs(x) < 1.9) & (np.abs(y) < 1.9)          # 中心 NS 灰云
cls[gray] = 3
band = con & (np.abs(d) < 1.1) & ~gray
edge = con & (np.abs(d) >= 1.1) & ~gray               # 品红在紫带边缘
half = r.random(n) < 0.45                             # 边缘点中 45% 保持紫
edge_purple = edge & half
edge_mag = edge & ~half
cls[edge_purple] = 0
cls[edge_mag] = 1

cmap = {0: '#A583C9', 1: '#A62A8F', 2: '#4478B8', 3: '#C9C9C9'}
fig, ax = plt.subplots(figsize=cm2in(12.2, 12.2))
for k in (3, 0, 1, 2):
    m = cls == k
    ax.scatter(x[m], y[m], s=13, c=cmap[k], alpha=0.7, linewidths=0, zorder=3)

# 阈值虚线: y=0 与 y=-0.5, x=0 与 x=0.5
ax.axhline(0, ls='--', lw=1.1, color='black', zorder=4)
ax.axhline(-0.5, ls='--', lw=1.1, color='black', zorder=4)
ax.axvline(0, ls='--', lw=1.1, color='black', zorder=4)
ax.axvline(0.5, ls='--', lw=1.1, color='black', zorder=4)

# 四角注释
ax.text(-9.8, 9.2, 'Discordant', fontsize=13, ha='left', va='center')
ax.text(9.8, 9.2, 'Concordant', fontsize=13, ha='right', va='center')
ax.text(-9.8, -9.2, 'Concordant', fontsize=13, ha='left', va='center')
ax.text(9.8, -9.2, 'Discordant', fontsize=13, ha='right', va='center')
ax.text(-9.8, 7.9, r'$\downarrow\ \it{HARE5}^{Hs/Hs}$' + '\n' +
        r'$\uparrow\ \it{HARE5}^{Mm/Mm}$', fontsize=9, ha='left', va='center',
        color='0.35', linespacing=1.5)
ax.text(9.8, -7.9, r'$\uparrow\ \it{HARE5}^{Hs/Hs}$' + '\n' +
        r'$\downarrow\ \it{HARE5}^{Mm/Mm}$', fontsize=9, ha='right', va='center',
        color='0.15', linespacing=1.5)

ax.set_xlim(-10.6, 10.6)
ax.set_ylim(-10.6, 10.6)
ax.set_xticks([-10, -5, 0, 5, 10])
ax.set_yticks([-10, -5, 0, 5, 10])
ax.set_xlabel(r'$\log_2$(Fold Change) $\it{HARE5}^{Hs/Hs}$', fontsize=10)
ax.set_ylabel(r'$\log_2$(Fold Change) $\it{HARE5}^{Mm/Mm}$', fontsize=10)
for sp in ('top', 'right'):
    ax.spines[sp].set_visible(True)
ax.tick_params(direction='out', length=4, width=1.1)
for sp in ax.spines.values():
    sp.set_linewidth(1.4)

save(fig, 'case_seg081.png')
