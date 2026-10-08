# -*- coding: utf-8 -*-
"""案例2 - Lancet PCoA图: 主散点(3组+置信椭圆) + 上/右边际箱线 + PERMANOVA 注释框。
参考: frames/seg_002.jpg — 橙HC/蓝T1D/红T2D, 十字形布局。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

set_style()

C_HC, C_T1D, C_T2D = '#E8862D', '#2077B4', '#B03A2E'
groups = ['HC', 'Adult-onset T1D', 'T2D']
gcolors = [C_HC, C_T1D, C_T2D]

r = rng(2)
# 每组 ~50 样本, 组间中心/协方差不同(贴近参考图分布)
centers = [(-0.05, -0.12), (0.06, 0.02), (0.01, 0.04)]
covs = [
    [[0.052, 0.012], [0.012, 0.020]],
    [[0.030, -0.006], [-0.006, 0.017]],
    [[0.013, 0.007], [0.007, 0.020]],
]
pts = [r.multivariate_normal(c, cv, 50) for c, cv in zip(centers, covs)]

fig = plt.figure(figsize=cm2in(15.5, 14.5))
gs = fig.add_gridspec(2, 2, width_ratios=[3.1, 1.0], height_ratios=[1.0, 3.1],
                      hspace=0.06, wspace=0.06)
ax_top = fig.add_subplot(gs[0, 0])
ax_txt = fig.add_subplot(gs[0, 1])
ax_main = fig.add_subplot(gs[1, 0], sharex=ax_top)
ax_right = fig.add_subplot(gs[1, 1], sharey=ax_main)

plt.setp(ax_top.get_xticklabels(), visible=False)
plt.setp(ax_right.get_yticklabels(), visible=False)

# ---------------- 主图 ----------------
for i, p in enumerate(pts):
    ax_main.scatter(p[:, 0], p[:, 1], s=34, color=gcolors[i], zorder=3,
                    label=groups[i], edgecolors='none')
    # 2σ 置信椭圆
    mu = p.mean(0)
    cov = np.cov(p.T)
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    vals, vecs = vals[order], vecs[:, order]
    ang = np.degrees(np.arctan2(vecs[1, 0], vecs[0, 0]))
    ax_main.add_patch(Ellipse(mu, 2 * 2 * np.sqrt(vals[0]), 2 * 2 * np.sqrt(vals[1]),
                              angle=ang, facecolor='none', edgecolor=gcolors[i],
                              lw=1.2, zorder=2))
ax_main.axhline(0, color='#BBBBBB', lw=0.8, ls='--', zorder=1)
ax_main.axvline(0, color='#BBBBBB', lw=0.8, ls='--', zorder=1)

ax_main.set_xlim(-0.66, 0.76)
ax_main.set_ylim(-0.53, 0.385)   # 顶部加 ~6% headroom, 防最高散点被上缘截断(右边际 sharey 同步)
ax_main.set_xticks([-0.4, 0.0, 0.4])
ax_main.set_yticks([-0.4, -0.2, 0.0, 0.2])
ax_main.set_xlabel('PCoA1 ( 25.44 %)', fontsize=10)
ax_main.set_ylabel('PCoA2 ( 11.79 %)', fontsize=10)
ax_main.text(0.97, 0.965, 'Bacteria', transform=ax_main.transAxes,
             ha='right', va='top', fontsize=10)
ax_main.legend(loc='lower right', frameon=False, fontsize=8.5,
               handletextpad=0.25, borderaxespad=0.1, labelspacing=0.32)

# ---------------- 上边际箱线(横向, 红/蓝/橙 自上而下) ----------------
for i, (p, pos) in enumerate(zip(pts[::-1], [2, 1, 0])):
    x = p[:, 0]
    bp = ax_top.boxplot(x, orientation='horizontal', positions=[pos], widths=0.55,
                        patch_artist=True, showfliers=False,
                        medianprops=dict(color='black', lw=1.1),
                        whiskerprops=dict(color='black', lw=0.9),
                        capprops=dict(color='black', lw=0.9))
    bp['boxes'][0].set_facecolor(gcolors[::-1][i])
    bp['boxes'][0].set_edgecolor('black')
    bp['boxes'][0].set_linewidth(0.9)
    jit = rng(20 + pos).uniform(-0.16, 0.16, len(x))
    ax_top.scatter(x, pos + jit, s=7, color='black', zorder=3)
ax_top.set_ylim(-0.55, 2.55)
ax_top.set_yticks([])
despine(ax_top, left=True)

# ---------------- 右边际箱线(纵向, 橙/蓝/红) ----------------
for i, p in enumerate(pts):
    y = p[:, 1]
    bp = ax_right.boxplot(y, positions=[i], widths=0.55, patch_artist=True,
                          showfliers=False,
                          medianprops=dict(color='black', lw=1.1),
                          whiskerprops=dict(color='black', lw=0.9),
                          capprops=dict(color='black', lw=0.9))
    bp['boxes'][0].set_facecolor(gcolors[i])
    bp['boxes'][0].set_edgecolor('black')
    bp['boxes'][0].set_linewidth(0.9)
    jit = rng(30 + i).uniform(-0.16, 0.16, len(y))
    ax_right.scatter(i + jit, y, s=7, color='black', zorder=3)
ax_right.set_xlim(-0.55, 2.55)
ax_right.set_xticks([])
despine(ax_right, bottom=True)

# ---------------- PERMANOVA 注释框 ----------------
ax_txt.axis('off')
ax_txt.text(0.5, 0.55, 'PERMANOVA', ha='center', va='center', fontsize=9.5)
ax_txt.text(0.5, 0.36, '$P$ = 0.0029', ha='center', va='center', fontsize=9)
for s in ax_txt.spines.values():
    s.set_visible(True)

save(fig, 'case_seg002.png')
