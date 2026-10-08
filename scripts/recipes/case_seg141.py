# -*- coding: utf-8 -*-
"""案例146 - UMAP (T 亚群): 淡彩半透明簇云 + 彩色底标签框(文字与底色对比), 无图例无网格。
参考: frames/seg_141.jpg — 轴 umap_1(-10~10), umap_2。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt

set_style()

# 名称, 簇云色, 标签框色, 文字色, 中心, (sx, sy, rho), 点数
spec = [
    ('Tumor cells',           '#8B84C8', '#1F2FA8', 'white',
     (3.9, 0.1), (2.8, 2.0, -0.3), 4400),
    ('Macrophages/Monocytes', '#79C06E', '#4CAF50', 'black',
     (-3.2, -0.9), (1.5, 1.1, 0.1), 2100),
    ('Low count/Necrotic',    '#C8D4C4', '#D9D9D9', 'black',
     (-2.9, 3.9), (0.5, 0.45, 0.1), 360),
    ('Neutrophils',           '#B5D433', '#B5D433', 'black',
     (-3.2, 1.4), (0.55, 0.5, 0.25), 540),
    ('Dendritic cells',       '#E86BD8', '#E326D0', 'black',
     (-5.9, 2.4), (0.8, 0.7, 0.1), 880),
    ('NK cells',              '#F5A54A', '#F28E2B', 'black',
     (-6.9, 4.4), (0.7, 0.55, -0.1), 700),
    ('T cells',               '#D96A75', '#B22234', 'white',
     (-8.3, 3.1), (1.0, 0.9, 0.2), 1250),
    ('B cells',               '#F2E23E', '#F2D02E', 'black',
     (-10.6, 0.8), (0.5, 0.5, 0.1), 460),
    ('Plasma cells',          '#54CBDE', '#4DC5D6', 'black',
     (-8.9, -0.8), (0.9, 0.8, 0.2), 980),
    ('Stromal cells',         '#5C93BC', '#3179A0', 'white',
     (-9.1, -2.5), (0.9, 0.7, 0.25), 920),
    ('Vasculature',           '#F2A8C4', '#F2A0C0', 'black',
     (-7.2, -5.9), (1.0, 0.8, 0.15), 980)]

r = rng(141)
fig, ax = plt.subplots(figsize=cm2in(15.0, 12.5))

for nm, pc, bc, tc, mu, cv, n in spec:
    sx, sy, rho = cv
    cov = [[sx * sx, rho * sx * sy], [rho * sx * sy, sy * sy]]
    xy = r.multivariate_normal(mu, cov, n).T
    ax.scatter(xy[0], xy[1], s=3.0, c=pc, alpha=0.28, linewidths=0, zorder=2)
    k = max(n // 18, 12)
    sel = r.choice(n, k, replace=False)
    ax.scatter(xy[0][sel], xy[1][sel], s=3.0, c=pc, alpha=0.75,
               linewidths=0, zorder=3)

for nm, pc, bc, tc, mu, cv, n in spec:
    if nm == 'Neutrophils':
        ax.annotate(nm, xy=(-3.4, 1.0), xytext=(-2.4, 0.3), fontsize=9,
                    ha='center', va='center', zorder=10,
                    arrowprops=dict(arrowstyle='-', lw=0.9, color='black',
                                    shrinkA=1, shrinkB=1),
                    bbox=dict(boxstyle='round,pad=0.28', fc=bc, ec='black', lw=0.8))
    else:
        ax.text(mu[0], mu[1], nm, fontsize=9, ha='center', va='center',
                color=tc, zorder=10,
                bbox=dict(boxstyle='round,pad=0.28', fc=bc, ec='black', lw=0.8))

ax.set_xlim(-12.8, 10.8)
ax.set_ylim(-8.5, 6.5)
ax.set_xticks([-10, -5, 0, 5, 10])
ax.set_yticks([-8, -4, 0, 4])
ax.set_xlabel('umap_1', fontsize=10)
ax.set_ylabel('umap_2', fontsize=10)
ax.tick_params(labelsize=8)

save(fig, 'case_seg141.png')
