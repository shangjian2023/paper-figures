# -*- coding: utf-8 -*-
"""案例105 (seg 103) - Nature 填充型等高线 small multiples。
参考 frames/seg_103.jpg: 上排 4 小面板 + 下 1 大面板; 各面板单色系
填充等高线 (Blues/Purples/Reds/Greens), 右上括号样本计数,
x = -log10(P value), y = Length (amino acids)。"""
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

set_style()
r = rng(103)


def cloud(mu, cov, n, extra=None):
    pts = r.multivariate_normal(mu, cov, n)
    if extra is not None:
        pts = np.vstack([pts, r.multivariate_normal(extra[0], extra[1], extra[2])])
    return pts


G1 = cloud((2.18, 185), [[0.022, 0.45], [0.45, 1500]], 380, ((3.0, 255), [[0.06, 0.6], [0.6, 800]], 16))
G2 = cloud((2.42, 160), [[0.070, 0.60], [0.60, 1100]], 270, ((3.6, 140), [[0.25, 1.2], [1.2, 1000]], 14))
G3 = cloud((2.75, 150), [[0.500, 1.80], [1.8, 1800]], 98)
G4 = cloud((2.28, 182), [[0.008, 0.09], [0.09, 640]], 134)

PANELS = [('All IDRs with signi-\nficant periodicity', '(396)', 'Blues', G1),
          ('PLDs', '(89/271)', 'Purples', G2),
          ('Aromatic-rich\nPLDs', '(47/98)', 'Reds', G3),
          ('TFs', '(134/1,542)', 'Greens', G4)]

XLO, XHI, YLO, YHI = 1.75, 5.25, 95, 310
gx = np.linspace(XLO, XHI, 130)
gy = np.linspace(YLO, YHI, 150)
XX, YY = np.meshgrid(gx, gy)

COMB = np.vstack([G1, G2, G3, G4])            # 汇总组, 供下方大面板


def draw_contour(ax, pts, cmap, cnt, cnt_fs=7.5):
    Z = gaussian_kde(pts.T)(np.vstack([XX.ravel(), YY.ravel()])).reshape(XX.shape)
    Z /= Z.max()
    ax.set_facecolor(plt.get_cmap(cmap)(0.045))
    ax.contourf(XX, YY, Z, levels=np.linspace(0.04, 1.0, 10), cmap=cmap)
    ax.set_xlim(XLO, XHI)
    ax.set_ylim(YLO, YHI)
    ax.set_xticks([2, 3, 4, 5])
    ax.set_yticks([100, 150, 200, 250, 300])
    for sp in ax.spines.values():
        sp.set_visible(True)
    ax.text(0.94, 0.905, cnt, transform=ax.transAxes, ha='right', va='center',
            fontsize=cnt_fs)


fig = plt.figure(figsize=cm2in(18, 15))
gs = fig.add_gridspec(2, 4, height_ratios=[1.0, 1.30], hspace=0.30,
                      wspace=0.28, left=0.085, right=0.985, top=0.905,
                      bottom=0.075)

ax_top = []
for i, (title, cnt, cmap, pts) in enumerate(PANELS):
    ax = fig.add_subplot(gs[0, i])
    ax_top.append(ax)
    draw_contour(ax, pts, cmap, cnt)
    ax.set_title(title, fontsize=7.5, pad=4)
    ax.tick_params(labelsize=7)
    if i == 0:
        ax.set_ylabel('Length (amino acids)', fontsize=8)
    else:
        ax.set_yticklabels([])

# 下方大面板: 跨全宽 (colspan=4), 与左上面板同数据同 Blues 配色的放大版
ax = fig.add_subplot(gs[1, :])
draw_contour(ax, G1, 'Blues', '(396)', cnt_fs=11)
ax.tick_params(labelsize=10)
ax.set_xlabel(r'$-\log_{10}$(P value)', fontsize=8)
ax.set_ylabel('Length (amino acids)', fontsize=8)

save(fig, 'case_seg103.png')
