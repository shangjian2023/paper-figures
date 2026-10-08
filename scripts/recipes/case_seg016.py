# -*- coding: utf-8 -*-
"""案例16 - Nature 分组山脊图。
参考 frames/seg_016.jpg: 三块纵向堆叠 ridgeline (绿系/紫系/青蓝系), 每块 6 条
分布水平排列, 0 ns→24 ns 峰逐渐右移; 仅填充 + 细基线; 行标签 0-24 ns。"""
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import gaussian_kde

set_style()
r = rng(16)

BLOCKS = [
    dict(xlim=(2.2, 5.75), peaks=[2.75, 3.6, 4.05, 4.35, 4.85, 4.95],
         xt=np.arange(2.5, 5.6, 0.5), sd=0.17, xlabel='Core RMSD (A)',
         cmap=LinearSegmentedColormap.from_list('g', ['#a8d786', '#16283c'])),
    dict(xlim=(1.5, 14.8), peaks=[4.0, 6.7, 9.9, 11.1, 12.4, 12.9],
         xt=np.arange(2, 14.6, 2), sd=0.55, xlabel='A-Loop RMSD (A)',
         cmap=LinearSegmentedColormap.from_list('p', ['#e3a6c8', '#241036'])),
    dict(xlim=(-22.5, 17.5), peaks=[-3.0, 2.5, 6.0, 8.5, 10.2, 10.8],
         xt=np.arange(-20, 16, 5), sd=1.7, xlabel='Distance 1 Δ (A)',
         cmap=LinearSegmentedColormap.from_list('t', ['#b5e0da', '#0e2036'])),
]
TIMES = ['0', '8', '12', '16', '20', '24']

fig, axes = plt.subplots(3, 1, figsize=cm2in(12, 15))
fig.subplots_adjust(left=0.11, right=0.97, top=0.985, bottom=0.05, hspace=0.60)

for ax, B in zip(axes, BLOCKS):
    lo, hi = B['xlim']
    x = np.linspace(lo, hi, 500)
    nrow = len(B['peaks'])
    offs = -np.arange(nrow).astype(float)
    cols = [B['cmap'](0.05 + 0.90 * i / (nrow - 1)) for i in range(nrow)]
    for i, (pk, off, c) in enumerate(zip(B['peaks'], offs, cols)):
        zorder = nrow - i          # 从上往下画, zorder 递减 → 山脊遮挡效果
        v = r.normal(pk, B['sd'], 4000)
        if i in (1, 2, 4):         # 少量行带小肩峰, 模拟 MD 轨迹的不规则形状
            v = np.concatenate([v, r.normal(pk - 5 * B['sd'], B['sd'] * 1.5, 320)])
        k = gaussian_kde(v)(x)
        k /= k.max()
        ax.fill_between(x, off, off + 0.80 * k, color=c, lw=0, zorder=zorder)
        ax.plot(x, np.full_like(x, off), color='0.25', lw=0.8, zorder=zorder)
    ax.set_yticks(offs)
    ax.set_yticklabels([t + ' ns' for t in TIMES], fontsize=8, fontweight='bold')
    ax.set_xlim(lo, hi)
    ax.set_ylim(-nrow + 0.55, 1.12)
    ax.set_xticks(B['xt'])
    despine(ax)
    ax.set_xlabel(B['xlabel'], fontsize=9)
    ax.tick_params(labelsize=7)

save(fig, 'case_seg016.png')
