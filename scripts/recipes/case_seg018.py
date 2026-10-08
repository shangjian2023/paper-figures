# -*- coding: utf-8 -*-
"""案例18 - Nature 分组分面山脊图。
参考 frames/seg_018.jpg: 4 列细胞因子 (IFN-γ / IL2 / TNF-α / GM-CSF) ×
9 亚群 × −/+ 两行 = 18 行山脊 KDE; 浅色 = 未刺激 −, 深色 = 刺激 +;
对数 x 轴 (log10 后绘制); 右侧彩色亚群图例。"""
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

set_style()
r = rng(18)

GROUPS = [
    ('ILC3',       '#bfe3a8', '#2f8f2f'),
    ('ILC2',       '#a9d2ee', '#4a90c8'),
    ('cILC1',      '#cccccc', '#4d4d4d'),
    ('cNK',        '#b2eeee', '#18cccc'),
    ('CD49a-trNK', '#f2bcbc', '#c82525'),
    ('CD49a+trNK', '#c3bae6', '#3f1a80'),
    ('LT-ILC1',    '#f2c4e2', '#cc1f9a'),
]
CYTO = ['IFN-$\\gamma$', 'IL2', 'TNF-$\\alpha$', 'GM-CSF']
XT = [-3, -2, -1, 0, 1, 2, 3]
XTL = [r'$10^{-3}$', r'$10^{-2}$', r'$10^{-1}$', r'$10^{0}$',
       r'$10^{1}$', r'$10^{2}$', r'$10^{3}$']


def sample(gi, ci, stim):
    """log10 荧光强度样本: − 窄峰偏左, + 右移变宽且不规则。"""
    base = -0.8 + 0.35 * r.standard_normal()
    if stim:
        mu = base + 1.15 + 0.5 * np.sin(gi * 1.3 + ci * 0.8)
        mu = float(np.clip(mu, -0.3, 1.5))
        v = r.normal(mu, 0.55, 2600)
        v = np.concatenate([v, r.normal(mu - 1.4, 0.40, 420)])
        if r.random() < 0.5:
            v = np.concatenate([v, r.normal(mu + 1.1, 0.35, 300)])
    else:
        v = r.normal(base, 0.22, 2600)
    return v


fig = plt.figure(figsize=cm2in(17, 13))
gs = fig.add_gridspec(1, 4, wspace=0.12, left=0.075, right=0.795,
                      top=0.905, bottom=0.115)
x = np.linspace(-3.3, 3.3, 400)
nrow = 14          # 7 亚群 × (−, +)
offs = -np.arange(nrow).astype(float)

for ci in range(4):
    ax = fig.add_subplot(gs[0, ci])
    row = 0
    for gi, (name, cl, cd) in enumerate(GROUPS):
        for stim in (0, 1):
            k = gaussian_kde(sample(gi, ci, stim))(x)
            k /= k.max()
            c = cl if stim == 0 else cd
            ax.fill_between(x, offs[row], offs[row] + 0.80 * k, color=c, lw=0,
                            zorder=nrow - row)
            ax.plot(x, np.full_like(x, offs[row]), color='0.3', lw=0.5,
                    zorder=nrow - row)
            row += 1
    ax.set_xlim(-3.3, 3.3)
    ax.set_ylim(-nrow + 0.5, 1.0)
    ax.set_xticks(XT)
    ax.set_xticklabels(XTL, fontsize=5)
    ax.set_xlabel(CYTO[ci], fontsize=9)
    if ci == 0:
        ax.set_yticks(offs)
        ax.set_yticklabels(['$-$', '+'] * 7, fontsize=6.5)
    else:
        ax.set_yticks([])
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(True)
    ax.tick_params(length=1.5, pad=1)

for i, (name, cl, cd) in enumerate(GROUPS):
    fig.text(0.825, 0.78 - i * 0.105, name, color=cd, fontsize=8.5,
             fontweight='bold', va='center')

save(fig, 'case_seg018.png')
