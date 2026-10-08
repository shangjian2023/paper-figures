# -*- coding: utf-8 -*-
"""案例68 - Cancer Cell 镜像小提琴图 (蝴蝶状): 左右镜像水平 KDE + 内嵌白箱线,
中间基因标签列, 红虚线阈值, 顶部 Score 轴 0-1.5。
参考: frames/seg_068.jpg — M1 Feature vs M2 Feature, 12 行。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

set_style()

genes = ['FTH1', 'NUPR1', 'MT1X', 'SELENOP', 'IL1B', 'RNASE1',
         'FOLR2', 'FN1', 'CCL3L1', 'ISG15', 'CXCL9', 'CCL2']
# 标签颜色: 黑 / 青(斜体) / 橙
black = ['FTH1', 'NUPR1', 'SELENOP', 'IL1B', 'CCL3L1', 'ISG15', 'CCL2']
cyan = ['MT1X', 'RNASE1', 'FN1']
orange = ['FOLR2', 'CXCL9']
vcolors = ['#BCE0CC', '#C4D6F0', '#B8E4E4', '#E8B4D4', '#CCC2E4', '#F0C4DC',
           '#D8C2C8', '#F8DCE8', '#A8C4E4', '#D8B48C', '#98D8B8', '#98CCBC']
# 基因平均分 (M1 侧 / M2 侧)
m1_mu = [0.55, 0.34, 0.30, 0.40, 0.30, 0.33, 0.34, 0.30, 0.34, 0.34, 0.30, 0.33]
m2_mu = [0.14, 0.36, 0.40, 0.28, 0.38, 0.38, 0.30, 0.36, 0.38, 0.38, 0.44, 0.38]

fig = plt.figure(figsize=cm2in(16.5, 14.5))
gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 0.62, 1.0], wspace=0.02,
                      left=0.02, right=0.98, top=0.88, bottom=0.08)
axL = fig.add_subplot(gs[0])
axC = fig.add_subplot(gs[1])
axR = fig.add_subplot(gs[2])

nrow = len(genes)
r = rng(68)


def hviolin(ax, yc, vals, color):
    """水平小提琴: x=数值, y=行中心 ± 密度厚度; 内嵌白色箱线。"""
    k = gaussian_kde(vals)
    grid = np.linspace(max(vals.min(), 0.005), min(vals.max(), 1.5), 130)
    w = 0.36 * k(grid) / k(grid).max()
    ax.fill(np.concatenate([grid, grid[::-1]]),
            np.concatenate([yc - w, (yc + w)[::-1]]),
            facecolor=color, edgecolor='#555555', lw=0.7, zorder=3)
    ax.plot([vals.min(), vals.max()], [yc, yc], c='#444444', lw=0.7, zorder=2)
    q1, md, q3 = np.percentile(vals, [25, 50, 75])
    ax.fill_betweenx([yc - 0.10, yc + 0.10], q1, q3, facecolor='white',
                     edgecolor='#888888', lw=0.5, zorder=4)
    ax.plot([md, md], [yc - 0.10, yc + 0.10], c='white', lw=1.6, zorder=5)


for side, ax, mus in [('L', axL, m1_mu), ('R', axR, m2_mu)]:
    for i, (g, mu) in enumerate(zip(genes, mus)):
        vals = r.lognormal(np.log(mu) - 0.30, 0.62, 260).clip(0.005, 1.5)
        hviolin(ax, i, vals, vcolors[i])
    ax.set_ylim(nrow - 0.5, -0.7)
    ax.set_xlim((1.62, -0.06) if side == 'L' else (-0.06, 1.62))
    ax.set_xticks([0, 0.5, 1.0, 1.5])
    ax.set_xticklabels(['0.0', '0.5', '1.0', '1.5'], fontsize=8)
    ax.xaxis.tick_top()
    ax.set_yticks([])
    ax.axvline(0.25, color='#D02020', ls=(0, (5, 3)), lw=1.1, zorder=6)
    for sp in ax.spines.values():
        sp.set_visible(True)
        sp.set_linewidth(0.8)
    ax.spines['bottom'].set_visible(False)

# 中间基因标签列
axC.set_xlim(0, 1)
axC.set_ylim(nrow - 0.5, -0.7)
axC.axis('off')
for i, g in enumerate(genes):
    c = '#18A8D8' if g in cyan else ('#E8641B' if g in orange else 'black')
    axC.text(0.5, i, r'MΦ-$\it{%s}$' % g, ha='center', va='center',
             fontsize=9.5, color=c)
axC.text(0.5, 1.05, 'Score', transform=axC.transAxes, ha='center',
         va='bottom', fontsize=11)

axL.text(0.5, -0.05, 'M1 Feature', transform=axL.transAxes, ha='center',
         va='top', fontsize=11, color='#E8402A')
axR.text(0.5, -0.05, 'M2 Feature', transform=axR.transAxes, ha='center',
         va='top', fontsize=11, color='#28A8E0')

save(fig, 'case_seg068.png')
