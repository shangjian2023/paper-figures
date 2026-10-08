# -*- coding: utf-8 -*-
"""案例136 - 火山图(框式标签): 粉带黑边显著点/灰NS, 竖横虚线阈值,
关键基因深紫大点 + 白底黑边斜体标签框。参考: frames/seg_136.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import matplotlib.pyplot as plt

set_style()
r = rng(136)

fig, ax = plt.subplots(figsize=cm2in(12.8, 12.2))
fig.subplots_adjust(left=0.135, right=0.97, top=0.97, bottom=0.115)

# ---------------- NS 灰点 (中部矮云)
n0 = 700
x0 = r.normal(0, 0.55, n0)
y0 = r.exponential(1.6, n0)
k0 = y0 < 8
ax.scatter(x0[k0], y0[k0], s=11, color='#c8c8c8', alpha=0.9, lw=0, zorder=2)

# ---------------- 左上粉色点 (下调显著)
xl = np.clip(r.normal(-1.85, 0.55, 130), -2.9, -1.0)
yl = np.clip(4 + 5.5 * np.abs(xl) + r.normal(0, 4.5, 130), 2, 37)
kl = yl < 37
ax.scatter(xl[kl], yl[kl], s=52, facecolor='#eec2dc', edgecolor='#4a4a4a',
           linewidth=0.8, alpha=0.95, zorder=3)

# ---------------- 右侧弧形粉点云 (上调显著)
pts = []
while len(pts) < 300:
    xx = r.uniform(0.95, 3.05)
    base = 6 + 16 * (xx - 0.95) ** 1.35 + r.normal(0, 6.5)
    yy = r.uniform(0.3, max(0.5, min(base, 70)))
    if yy > 2:
        pts.append((xx, yy))
pts = np.array(pts)
ax.scatter(pts[:, 0], pts[:, 1], s=58, facecolor='#eec2dc',
           edgecolor='#4a4a4a', linewidth=0.8, alpha=0.95, zorder=3)

# ---------------- 靠近阈值的浅灰点
xg = r.normal(1.05, 0.18, 120)
yg = r.exponential(4, 120)
kg = yg < 16
ax.scatter(xg[kg], yg[kg], s=13, color='#c8c8c8', alpha=0.85, lw=0, zorder=2)

# ---------------- 阈值虚线
ax.axvline(-1.0, color='black', ls='--', lw=1.4, zorder=1)
ax.axvline(1.0, color='black', ls='--', lw=1.4, zorder=1)
ax.axhline(1.3, color='black', ls='--', lw=1.4, zorder=1)

# ---------------- 关键基因深紫大点 + 框式标签
KEY = [('lyve1b', 1.72, 50, 1.10, 56),
       ('osr2', 2.50, 52, 2.62, 58),
       ('mrc1a', 1.88, 41, 1.85, 34),
       ('cdh6', -1.38, 15, -1.30, 20),
       ('prox1a', -1.88, 10, -2.05, 5.5),
       ('tbx1', -1.12, 1.6, -0.98, 1.8)]
for g, x, y, tx, ty in KEY:
    ax.scatter([x], [y], s=290, color='#5b1a6e', edgecolor='none', zorder=5)
    ax.text(tx, ty, italic_gene(g), fontsize=12.5, ha='center', va='center',
            zorder=6,
            bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='black',
                      lw=1.1))

ax.set_xlim(-3.35, 3.25)
ax.set_ylim(-4, 70)
ax.set_xticks([-2, 0, 2])
ax.set_yticks([0, 20, 40, 60])
ax.tick_params(labelsize=10)
ax.set_xlabel('log$_2$[FC]', fontsize=12)
ax.set_ylabel('$-$log$_{10}$[P]', fontsize=12)
despine(ax)

save(fig, 'case_seg136.png')
