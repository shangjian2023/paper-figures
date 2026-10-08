# -*- coding: utf-8 -*-
"""案例138 - 配对散点箱线图: 4 组箱线 + 抖动散点, 灰虚线连接配对个体,
组间精确 p 值横线; 左右两个同构面板换配色。
参考: frames/seg_138.jpg。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt

set_style()

labels = ['primary', 'met', 'met', 'met']
npats = 16
mus = [0.14, 0.09, 0.16, 0.26]
sds = [0.09, 0.06, 0.08, 0.10]
colorsets = [['#3A6B9C', '#1A5C2A', '#4CAF50', '#20B2AA'],
             ['#8B1A4A', '#E04A2A', '#E8A020', '#B22222']]

fig, axes = plt.subplots(1, 2, figsize=cm2in(17.0, 10.0),
                         gridspec_kw=dict(wspace=0.30, left=0.07, right=0.99,
                                          top=0.97, bottom=0.14))

for pi, ax in enumerate(axes):
    r = rng(138 + pi * 10)
    # 配对数据: 患者 × 4 组
    base = r.normal(0.15, 0.10, npats)          # 患者效应
    data = np.stack([np.clip(base * w + r.normal(m, s, npats), 0.005, None)
                     for (m, s), w in zip(zip(mus, sds),
                                          [1.0, 0.5, 1.1, 1.6])], axis=1)
    # 配对虚线 (在最底层)
    for j in range(npats):
        ax.plot(range(4), data[j, :], c='#B0B0B0', lw=0.8, ls=(0, (4, 3)),
                zorder=1)
    for gi in range(4):
        ax.boxplot(data[:, gi], positions=[gi], widths=0.5, patch_artist=True,
                   whis=(0, 100),
                   boxprops=dict(facecolor='#E8E8E8', edgecolor='#707070',
                                 lw=1.0),
                   medianprops=dict(color='#404040', lw=1.2),
                   whiskerprops=dict(color='#707070', lw=0.9),
                   capprops=dict(color='#707070', lw=0.9),
                   showfliers=False, zorder=2, manage_ticks=False)
        jit = r.uniform(-0.16, 0.16, npats)
        ax.scatter(np.full(npats, gi) + jit, data[:, gi], s=22,
                   c=colorsets[pi][gi], edgecolors='white', linewidths=0.3,
                   zorder=3)
    # 显著性横线 (精确 p 值)
    P = r'$\times 10^{-4}$'
    rows = [
        (0, 3, 0.955, f'1.5{P}'),
        (0, 2, 0.875, '0.443'),
        (2, 3, 0.875, '0.004'),
        (0, 1, 0.795, '0.033'),
        (1, 2, 0.795, f'5.7{P}'),
    ]
    for g0, g1, y, txt in rows:
        ax.plot([g0, g0, g1, g1], [y, y + 0.012, y + 0.012, y],
                c='black', lw=0.9)
        ax.text((g0 + g1) / 2, y + 0.02, txt, ha='center', va='bottom',
                fontsize=8)
    ax.set_xlim(-0.55, 3.55)
    ax.set_ylim(0, 1.02)
    ax.set_xticks(range(4))
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_ylabel('Mean mutation diversity\nper patient', fontsize=9)
    ax.tick_params(length=3)
    despine(ax)

save(fig, 'case_seg138.png')
