# -*- coding: utf-8 -*-
"""案例68 - Nature 限制性立方样条(RCS) 2×2 四面板。
参考: frames/seg_066.jpg — HR 实线 + 同色 CI 带(绿/黄/粉/橙), HR=1 黑虚线,
各面板左上 inset 小图(Mortality 灰线灰带), 面板内注 P-nonlinear / P-overall。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt

set_style()

panels = [
    dict(xlabel='Neutrophil count ($10^9$ cells/L)', xmax=18.5,
         color='#8FCB8F', hr=lambda x: 0.62 + 2.4 / (1 + np.exp(-(x - 11.5) / 2.2)),
         ylim=(0, 6), yticks=[0, 2, 4, 6], ixt=[0, 5, 10, 15],
         iyt=[0, 2, 4, 6],
         mort=lambda x: 0.9 + 3.1 / (1 + np.exp(-(x - 12) / 3.0)),
         pi=('0.0356', '8.99$\\times$10$^{-99}$'),
         pm=('0.5779', '2.36$\\times$10$^{-116}$')),
    dict(xlabel='Neutrophil%', xmax=87,
         color='#E8D24B', hr=lambda x: 0.75 + 0.5 * np.exp(-x / 28.0),
         ylim=(0, 4.6), yticks=[0, 1, 2, 3, 4], ixt=[0, 25, 50, 75],
         iyt=[0.0, 2.5, 5.0, 7.5],
         mort=lambda x: 0.15 + 1.15 * np.exp(-x / 22.0),
         pi=('0.0013', '1.01$\\times$10$^{-93}$'),
         pm=('0.1751', '1.56$\\times$10$^{-111}$')),
    dict(xlabel='CRP (mg/L)', xmax=83,
         color='#C99BCE', hr=lambda x: 0.7 + 3.3 / (1 + np.exp(-(x - 55) / 14)),
         ylim=(0, 10.5), yticks=[0.0, 2.5, 5.0, 7.5, 10.0],
         ixt=[0, 20, 40, 60, 80], iyt=[0, 5, 10, 15],
         mort=lambda x: 0.35 + 3.4 * (x / 80.0) ** 1.6,
         pi=('0.3045', '5.47$\\times$10$^{-95}$'),
         pm=('0.0691', '1.14$\\times$10$^{-111}$')),
    dict(xlabel='Monocyte%', xmax=87,
         color='#F0937A',
         hr=lambda x: 0.55 + 0.18 * np.exp(-((x - 5) / 4.0) ** 2)
                      + 2.8 / (1 + np.exp(-(x - 58) / 11)),
         ylim=(0, 26), yticks=[0, 5, 10, 15, 20, 25],
         ixt=[0, 25, 50, 75], iyt=[0, 10, 20, 30],
         mort=lambda x: 0.25 + 4.2 * (x / 85.0) ** 2.2,
         pi=('0.1873', '8.77$\\times$10$^{-91}$'),
         pm=('0.0075', '9.59$\\times$10$^{-112}$')),
]

fig, axes = plt.subplots(2, 2, figsize=cm2in(17.0, 15.5))

for ax, p in zip(axes.flat, panels):
    xg = np.linspace(0.15, p['xmax'], 240)
    hr = p['hr'](xg)
    t = (xg - xg.mean()) / (xg.max() - xg.min())
    half = hr * (0.20 + 1.35 * t ** 2)
    ax.fill_between(xg, np.maximum(hr - half, 0.02), hr + half,
                    color=p['color'], alpha=0.45, lw=0, zorder=1)
    ax.plot(xg, hr, color=p['color'], lw=1.6, zorder=2)
    ax.axhline(1, color='black', ls='--', lw=1.0, zorder=3)

    # 左上 inset: Mortality
    axi = ax.inset_axes([0.15, 0.50, 0.42, 0.46])
    axi.set_facecolor('white')
    for s in axi.spines.values():
        s.set_visible(True)
        s.set_linewidth(0.5)
    mi = p['mort'](xg)
    mhalf = mi * (0.18 + 1.5 * t ** 2)
    axi.fill_between(xg, np.maximum(mi - mhalf, 0), mi + mhalf,
                     color='#B9B9B9', alpha=0.45, lw=0)
    axi.plot(xg, mi, color='#8F8F8F', lw=1.0)
    axi.set_xticks(p['ixt'])
    axi.set_yticks(p['iyt'])
    axi.tick_params(labelsize=5.2, length=1.5, pad=1)
    axi.set_ylabel('Mortality', fontsize=5.5, labelpad=1)
    axi.text(0.04, 1.02, 'P$_{overall}$=' + p['pi'][1],
             transform=axi.transAxes, fontsize=5.6, va='bottom')
    axi.text(0.04, 1.16, 'P$_{non-linear}$=' + p['pi'][0],
             transform=axi.transAxes, fontsize=5.6, va='bottom')

    # 主面板 P 文本
    ax.text(0.17, 0.42, 'P$_{non-linear}$=' + p['pm'][0] + '\n'
            'P$_{overall}$=' + p['pm'][1],
            transform=ax.transAxes, fontsize=8, va='top')

    ax.set_xlim(0, p['xmax'])
    ax.set_ylim(*p['ylim'])
    ax.set_yticks(p['yticks'])
    ax.set_xlabel(p['xlabel'], fontsize=8.5)
    ax.set_ylabel('HR (95% CI) for incidence', fontsize=8)

fig.subplots_adjust(hspace=0.42, wspace=0.32)
save(fig, 'case_seg066.png')
