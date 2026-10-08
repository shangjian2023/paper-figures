# -*- coding: utf-8 -*-
"""案例36 - Nature FC-FC散点: 双log2FC四类着色 + 灰色NS空心点 + 基因引线标注。
参考: frames/seg_036.jpg — monocytes Dexa vs ctrl core signature。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt

set_style()

r = rng(36)
fig, ax = plt.subplots(figsize=cm2in(13.0, 12.0))

RED, PINK = '#C02020', '#F0A8A8'
BLUE, LBLUE = '#2166AC', '#A9C6E8'
GRAY = '#595959'

# ---------------- 数据云 ----------------
ns = r.multivariate_normal([0.18, -0.12], [[0.30, 0.05], [0.05, 0.16]], 380)
ax.scatter(ns[:, 0], ns[:, 1], s=22, facecolors='none', edgecolors=GRAY,
           linewidths=0.8, zorder=2, label='not significant')

up2 = r.multivariate_normal([0.50, 0.30], [[0.040, 0.008], [0.008, 0.017]], 55)
up1 = r.multivariate_normal([1.30, 0.30], [[0.80, 0.10], [0.10, 0.09]], 26)
up1 = np.vstack([up1, [[2.85, 0.08], [3.40, 0.06], [1.95, 0.55], [0.35, 0.55]]])
dn2 = r.multivariate_normal([-0.55, -0.35], [[0.075, 0.02], [0.02, 0.075]], 50)
dn1 = r.multivariate_normal([-1.05, -0.72], [[0.20, 0.05], [0.05, 0.16]], 22)
ax.scatter(up2[:, 0], up2[:, 1], s=42, color=RED, zorder=4, label='DE up (both)')
ax.scatter(up1[:, 0], up1[:, 1], s=38, color=PINK, zorder=3, label='DE up (one)')
ax.scatter(dn2[:, 0], dn2[:, 1], s=42, color=BLUE, zorder=4, label='DE down (both)')
ax.scatter(dn1[:, 0], dn1[:, 1], s=38, color=LBLUE, zorder=3, label='DE down (one)')

# ---------------- 参考线 ----------------
dd = np.array([-1.85, 2.30])
ax.plot(dd, dd, ls='--', lw=1.6, color='#C8C8C8', zorder=1)
ax.axhline(0, color='black', lw=1.1, zorder=1.5)
ax.axvline(0, color='black', lw=1.1, zorder=1.5)

# ---------------- 基因点 + 引线标注 ----------------
genes = [
    ('IL1R2',   (2.60, 1.75),  (2.42, 2.00)),
    ('TSC22D3', (0.62, 0.62),  (0.50, 1.10)),
    ('CD163',   (0.95, 0.45),  (1.40, 0.82)),
    ('DDIT4',   (0.32, 0.60),  (-0.44, 0.70)),
    ('ZFP36L2', (0.68, 0.42),  (0.88, 0.58)),
    ('SAP30',   (1.15, 0.40),  (1.66, 0.52)),
    ('JDP2',    (1.05, 0.28),  (1.52, 0.20)),
    ('PER1',    (0.92, 0.09),  (1.46, 0.01)),
    ('CD300E',  (-0.72, -0.48), (-1.60, -0.62)),
    ('CXCL8',   (-0.52, -0.85), (-0.82, -0.92)),
    ('CCL3L3',  (-1.05, -0.88), (-1.82, -1.04)),
    ('G0S2',    (-0.65, -1.02), (-0.36, -1.08)),
    ('CCL3',    (-0.88, -1.18), (-0.98, -1.40)),
    ('IL1B',    (-1.02, -1.32), (-1.48, -1.28)),
]
for g, (px, py), (tx, ty) in genes:
    col = RED if py > 0 else BLUE
    ax.scatter([px], [py], s=46, color=col, zorder=5)
    ax.annotate(r'$\it{%s}$' % g, xy=(px, py), xytext=(tx, ty), fontsize=9.5,
                ha='center', va='center', zorder=6,
                arrowprops=dict(arrowstyle='-', lw=0.8, color='black',
                                shrinkA=1, shrinkB=2))

# ---------------- 角落标签框 ----------------
ax.text(0.03, 2.14, 'Dexa core up', fontsize=9.5, ha='left', va='center',
        bbox=dict(facecolor='#F2B8B8', edgecolor='black', lw=0.8, pad=3.0))
ax.text(-1.76, -1.62, 'Dexa core down', fontsize=9.5, ha='left', va='center',
        bbox=dict(facecolor='#B8CCE4', edgecolor='black', lw=0.8, pad=3.0))

ax.set_xlim(-1.85, 3.85)
ax.set_ylim(-1.78, 2.35)
ax.set_xticks([-1, 0, 1, 2, 3])
ax.set_yticks([-1, 0, 1, 2])
ax.set_title('monocytes: Dexa vs. ctrl. core signature', fontsize=10.5, pad=8)
ax.legend(loc='lower right', frameon=True, edgecolor='black', framealpha=1.0,
          fontsize=8.5, borderaxespad=0.5, handletextpad=0.4, labelspacing=0.35)

# 双色轴标签: severe(红)/moderate(橙)
for frac, txt, col, rot in [(0.245, 'log2FC ', 'black', 0),
                            (0.372, 'moderate', '#E69138', 0),
                            (0.522, ' Dexa vs ctrl.', 'black', 0)]:
    ax.text(frac, -0.105, txt, transform=ax.transAxes, ha='left', va='top',
            fontsize=10, color=col, rotation=rot)
for frac, txt, col in [(0.275, 'log2FC ', 'black'),
                       (0.435, 'severe', '#CC2200'),
                       (0.620, 'Dexa vs ctrl.', 'black')]:
    ax.text(-0.105, frac, txt, transform=ax.transAxes, ha='center', va='center',
            fontsize=10, color=col, rotation=90)

save(fig, 'case_seg036.png')
