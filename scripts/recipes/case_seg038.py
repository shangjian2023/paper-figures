# -*- coding: utf-8 -*-
"""案例38 - Cognition 密度 + 箱线/蜂群组合图。
参考 frames/seg_038.jpg: 上 3 参数 × 4 条件矩阵, 每格上半 = 恢复分布 KDE
(灰/蓝/紫/橙) + 红方块真值, 下半 = 粉红箱线 + 蜂群; 下 1 宽面板 =
Empirical(紫 KDE) / Recovered(粉箱线蜂群) 对照。"""
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

set_style()
r = rng(38)

PINK = '#ef5f96'
PARAMS = [r'Inverse Choice' + '\n' + r'Stochasticity ($\beta$)',
          r'Exploration' + '\n' + r'Bonus ($\omega$)',
          r'Perseveration ($\tau$)']
CONDS = [('Baseline', '#cccccc'), ('Environment Size', '#bcd8ec'),
         ('Memory Demands', '#c9b3dd'), ('Interaction', '#f8d3ac')]
TRUE = [[8.0, 0.0, 0.0, 0.5],
        [2.5, 0.3, 5.5, 4.0],
        [2.7, 5.0, 0.2, 0.3]]
SPAN = [[(3.2, 12.5), (-4.5, 2.5), (-5.5, 2.8), (-2.8, 2.8)],
        [(-0.5, 6.8), (-4.5, 2.5), (2.0, 10.5), (1.2, 6.8)],
        [(-0.5, 7.8), (3.0, 10.5), (-5.5, 2.8), (-2.8, 2.8)]]
SD = [[1.5, 0.8, 0.9, 0.8], [1.0, 1.0, 1.3, 0.9], [1.2, 1.4, 0.8, 0.8]]

fig = plt.figure(figsize=cm2in(18, 17))
gs = fig.add_gridspec(4, 4, height_ratios=[1, 1, 1, 2.1], hspace=0.60,
                      wspace=0.50, left=0.13, right=0.97, top=0.94,
                      bottom=0.055)

for pi in range(3):
    for ci in range(4):
        ax = fig.add_subplot(gs[pi, ci])
        lo, hi = SPAN[pi][ci]
        data = r.normal(TRUE[pi][ci], SD[pi][ci], 70).clip(lo, hi)
        xs = np.linspace(lo, hi, 300)
        k = gaussian_kde(data)(xs)
        k /= k.max()
        # 上半: KDE + 红方块真值
        ax.fill_between(xs, 0, 1.55 * k, color=CONDS[ci][1], lw=0)
        ax.plot(xs, 1.55 * k, color='0.35', lw=0.8)
        ax.plot([TRUE[pi][ci]], [0], marker='s', ms=3.8, color='#d62728',
                clip_on=False, zorder=6)
        # 下半: 粉红箱线 + 蜂群抖动点
        ax.boxplot(data, orientation='horizontal', positions=[-1.15], widths=0.58,
                   patch_artist=True, showcaps=False, showfliers=False,
                   whiskerprops=dict(color=PINK, lw=0.9),
                   medianprops=dict(color='#d81b60', lw=1.5),
                   boxprops=dict(facecolor='none', edgecolor=PINK, lw=0.9))
        jit = r.uniform(-0.10, 0.10, len(data))
        ax.scatter(data, -1.15 + jit, s=3.5, color=PINK, lw=0, zorder=5)
        ax.set_xlim(lo, hi)
        ax.set_ylim(-1.8, 1.9)
        ax.set_yticks([])
        ax.set_xticks(np.round(np.linspace(lo, hi, 4), 1))
        ax.tick_params(labelsize=5.5)
        despine(ax)
        if pi == 0:
            ax.set_title(CONDS[ci][0], fontsize=8)
        if ci == 0:
            ax.set_ylabel(PARAMS[pi], fontsize=8)
        ax.text(-0.04, 0.74, 'Empirical', transform=ax.transAxes, rotation=90,
                fontsize=4.5, color='0.35', ha='center', va='center')
        ax.text(-0.04, 0.22, 'Recovered', transform=ax.transAxes, rotation=90,
                fontsize=4.5, color='0.35', ha='center', va='center')

# 底部宽面板: Empirical / Recovered 对照
gsub = gs[3, :].subgridspec(2, 1, height_ratios=[1.05, 1.0], hspace=0.06)
xs = np.linspace(-3.0, 3.0, 400)
data = r.normal(0.45, 0.95, 130).clip(-2.9, 2.9)
k = gaussian_kde(data)(xs)
k /= k.max()

axE = fig.add_subplot(gsub[0])
axE.fill_between(xs, 0, k, color='#c9aede', lw=0)
axE.plot(xs, k, color='0.3', lw=1.0)
axE.plot([0.5], [0], marker='s', ms=5, color='#d62728', clip_on=False, zorder=6)
axE.set_xlim(-3.0, 3.0)
axE.set_ylim(-0.02, 1.05)
axE.set_xticks([])
axE.set_yticks([])
for sp in axE.spines.values():
    sp.set_visible(True)
axE.text(-0.065, 0.62, 'Empirical', transform=axE.transAxes, rotation=90,
         ha='center', va='center', fontsize=11)

axB = fig.add_subplot(gsub[1])
axB.boxplot(data, orientation='horizontal', positions=[0], widths=0.55, patch_artist=True,
            showcaps=False, showfliers=False,
            whiskerprops=dict(color=PINK, lw=1.0),
            medianprops=dict(color='#d81b60', lw=2.0),
            boxprops=dict(facecolor='none', edgecolor=PINK, lw=1.0))
axB.scatter(data, r.uniform(-0.09, 0.09, len(data)), s=9, color=PINK, lw=0,
            zorder=5)
axB.set_xlim(-3.0, 3.0)
axB.set_ylim(-1.0, 1.0)
axB.set_yticks([])
axB.set_xticks([-2.5, 0.0, 2.5])
axB.tick_params(labelsize=8)
for sp in axB.spines.values():
    sp.set_visible(True)
axB.text(-0.065, 0.5, 'Recovered', transform=axB.transAxes, rotation=90,
         ha='center', va='center', fontsize=11)

save(fig, 'case_seg038.png')
