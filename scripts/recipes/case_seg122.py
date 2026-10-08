# -*- coding: utf-8 -*-
"""案例122 - Nature 带显著性的小提琴图(二): 上下两面板各 10 组 × 2 小提琴,
*** 星号括号, 底部 CD4/Treg/CD8 分组横线, 图例内嵌散点。
参考: frames/seg_122.jpg — EBV 阴性/阳性。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib.lines import Line2D

set_style()

labels = ['CD45RA+', 'Naive', 'CD45RO+', 'CM', 'CD45RA+', 'Naive',
          'CD45RO+', 'CD127+\nTEMRA', 'KLRG1+\nTIGIT+\nEM', 'TIGIT+\nEM']
# 每组两小提琴的中位数 (阴性, 阳性) 上/下面板
med_top = [(60, 45), (68, 45), (32, 48), (25, 40), (35, 28), (55, 20),
           (75, 88), (78, 82), (30, 50), (35, 42)]
med_bot = [(55, 42), (62, 40), (28, 45), (22, 38), (32, 26), (50, 18),
           (70, 82), (75, 30), (28, 45), (32, 40)]
CL1, CR1 = '#E8A020', '#4080C0'   # 上: EBV- 橙 / EBV+ 蓝
CL2, CR2 = '#C8C8C8', '#E06080'   # 下: 灰 / 粉

fig, axes = plt.subplots(2, 1, figsize=cm2in(17.0, 15.0),
                         gridspec_kw=dict(hspace=0.80, left=0.07, right=0.99,
                                          top=0.965, bottom=0.10))

r = rng(122)
for pi, ax in enumerate(axes):
    med = med_top if pi == 0 else med_bot
    CL, CR = (CL1, CR1) if pi == 0 else (CL2, CR2)
    for gi in range(10):
        xc = gi * 1.0
        for off, mu, c in [(-0.17, med[gi][0], CL), (0.17, med[gi][1], CR)]:
            sd = 0.30 * mu + 6
            v = r.normal(mu, sd, 130)
            v = np.where(v > 100, 200 - v, v)   # 在 100% 处反射, 百分比 ≤ 100
            vals = np.clip(v, 2, 100)
            k = gaussian_kde(vals)
            grid = np.linspace(vals.min(), vals.max(), 110)
            w = 0.155 * k(grid) / k(grid).max()
            ax.fill(np.concatenate([xc + off - w, (xc + off + w)[::-1]]),
                    np.concatenate([grid, grid[::-1]]),
                    facecolor=c, edgecolor='#555555', lw=0.6, alpha=0.9,
                    zorder=2)
            jit = r.uniform(-0.09, 0.09, 40)
            ax.scatter(xc + off + jit,
                       r.choice(vals, 40, replace=False), s=3,
                       c='#333333', alpha=0.45, linewidths=0, zorder=3)
        # *** 括号
        yb = (118 if pi == 0 else 96) + gi * 0
        yt = yb + 6
        ax.plot([xc - 0.22, xc - 0.22, xc + 0.22, xc + 0.22],
                [yb + 2, yt, yt, yb + 2], c='black', lw=0.9)
        ax.text(xc, yt + 1.5, '***', ha='center', va='bottom', fontsize=8)
    # 底部分组横线 (位于 x 刻度标签下方, 轴分数坐标)
    tr = ax.get_xaxis_transform()
    for (g0, g1, lab) in [(0, 3, 'CD4'), (4, 6, 'Treg'), (7, 9, 'CD8')]:
        ax.plot([g0 - 0.42, g1 + 0.42], [-0.26, -0.26], c='black', lw=1.1,
                transform=tr, clip_on=False)
        ax.text((g0 + g1) / 2, -0.295, lab, ha='center', va='top',
                fontsize=9.5, transform=tr, clip_on=False)
    ax.set_xlim(-0.65, 9.65)
    if pi == 0:
        ax.set_ylim(-36, 142)
        ax.set_yticks([0, 25, 50, 75, 100])
        handles = [Line2D([], [], marker='o', ls='', color=CL1, markersize=7),
                   Line2D([], [], marker='o', ls='', color=CR1, markersize=7)]
        ax.legend(handles, [r'EBV$_{\rm{Negative}}$ (n =34)',
                            r'EBV$_{\rm{Positive}}$ (n =27)'],
                  loc='upper right', bbox_to_anchor=(1.0, 1.14), frameon=False,
                  fontsize=8, ncol=2, columnspacing=1.2, handletextpad=0.3)
        ax.text(-0.55, 138, 'Baseline', fontsize=10)
    else:
        ax.set_ylim(-30, 118)
        ax.set_yticks([0, 25, 50, 75, 100])
        handles = [Line2D([], [], marker='o', ls='', color=CL2, markersize=7),
                   Line2D([], [], marker='o', ls='', color=CR2, markersize=7)]
        ax.legend(handles, [r'EBV$_{\rm{Negative}}$ (n = 34)',
                            r'EBV$_{\rm{Positive}}$ (n = 27)'],
                  loc='upper right', bbox_to_anchor=(0.72, 1.16),
                  frameon=False, fontsize=8, ncol=2, columnspacing=1.2,
                  handletextpad=0.3)
        ax.text(-0.55, 114, 'Baseline', fontsize=10)
    ax.set_xticks(np.arange(10))
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel('Percentage of cells', fontsize=9)
    ax.tick_params(length=3)
    despine(ax)

save(fig, 'case_seg122.png')
