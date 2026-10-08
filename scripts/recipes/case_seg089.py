# -*- coding: utf-8 -*-
"""案例91(seg089) - Nature 多维变量相关性热图 (Mantel 组合):
右上三角 Pearson 矩阵(青正/橙负 + 星号) + 左侧 4 群落节点贝塞尔连边
(线色=Mantel p 三档, 线宽=r 三档) + 右侧 3 组图例。
参考: frames/seg_089.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.patches import Rectangle, PathPatch, FancyBboxPatch
from matplotlib.path import Path
from matplotlib.cm import ScalarMappable

vars_ = ['NH$_4^+$-N', 'NO$_3^-$-N', 'NO$_2^-$-N', 'TN', 'TP', 'pH',
         'SO$_4^{2-}$', 'Temp', 'Salinity', 'Moisture', 'TOC']
n = len(vars_)
comms = ['Prokaryotic\nhost\ncommunity\ncomposition',
         'Microbial\ncommunity\ncomposition\n(mOTUs)',
         'Viral\n(host)\ncommunity\ncomposition',
         'Viral\ncommunity\ncomposition\n(vOTUs)']

r = rng(89)
R = r.uniform(-0.15, 0.15, (n, n))
P = r.uniform(0.3, 0.9, (n, n))
hot = [0, 3, 5, 6, 7, 8, 10]          # 高相关变量簇
for a in range(len(hot)):
    for b in range(a + 1, len(hot)):
        i, j = hot[a], hot[b]
        R[i, j] = r.uniform(0.30, 0.72)
        P[i, j] = r.choice([0.0001, 0.0005, 0.0009])
for i in range(n):                    # 少量中等显著
    for j in range(i + 1, n):
        if P[i, j] > 0.9 and r.random() < 0.30:
            P[i, j] = r.uniform(0.01, 0.05)
            R[i, j] = r.uniform(0.1, 0.3)
        elif P[i, j] > 0.9 and r.random() < 0.25:
            P[i, j] = r.uniform(0.05, 0.3)
            R[i, j] = r.uniform(-0.3, 0.05)

mr = r.uniform(0.02, 0.35, (4, n))
mp = r.uniform(0.0002, 0.35, (4, n))
mp[0, :4] = r.uniform(0.002, 0.04, 4)
mp[1, 3:] = r.uniform(0.0003, 0.02, n - 3)
mp[3, 5:] = r.uniform(0.0005, 0.01, n - 5)

cmap_pr = LinearSegmentedColormap.from_list(
    'pr', ['#e6550d', '#fdae6b', '#f7f7f7', '#7bccc4', '#2b8cbe'], N=256)
norm_pr = Normalize(-1, 1)

def p_col(p):
    return '#c9c9c9' if p >= 0.05 else ('#b3cc33' if p >= 0.001 else '#35a2be')

def r_lw(rv):
    return 0.7 if rv < 0.1 else (1.4 if rv < 0.2 else 2.2)

fig = plt.figure(figsize=cm2in(21.0, 14.0))
ax = fig.add_axes([0.015, 0.02, 0.975, 0.96])
ax.set_xlim(-11.5, n + 10.0)
ax.set_ylim(n + 3.5, -6.5)
ax.axis('off')

# ---- 右上三角 Pearson 格
for i in range(n):
    for j in range(i + 1, n):
        rv, pv = R[i, j], P[i, j]
        if pv >= 0.05 and abs(rv) < 0.12:
            continue                   # 弱且不显著 -> 留白成阶梯
        ax.add_patch(Rectangle((j, i), 1, 1, facecolor=cmap_pr(norm_pr(rv)),
                               edgecolor='#b0b0b0', linewidth=0.45, zorder=2))
        if pv < 0.05:
            st = '***' if pv < 0.001 else ('**' if pv < 0.01 else '*')
            ax.text(j + 0.5, i + 0.47, st, ha='center', va='center',
                    fontsize=5.8, color='#1a1a1a', zorder=4)

for j in range(n):                     # 顶部 45° 变量名
    ax.text(j + 0.55, -0.35, vars_[j], rotation=45, ha='left', va='bottom',
            fontsize=7.5)
for i in range(n):                     # 右侧变量名
    ax.text(n + 0.35, i + 0.5, vars_[i], ha='left', va='center', fontsize=7.5)

# ---- 群落节点 + 贝塞尔 Mantel 连边
node_xy = [(k + 0.5, k + 0.5) for k in range(n)]
comm_xy = [(-7.0, 1.0), (-4.6, 3.2), (-2.2, 5.4), (0.4, 7.6)]
for k in range(4):
    for i in range(n):
        x0, y0 = comm_xy[k]
        x1, y1 = node_xy[i]
        mx, my = (x0 + x1) / 2.0, (y0 + y1) / 2.0
        d = np.hypot(x1 - x0, y1 - y0)
        cx, cy = mx - (y1 - y0) / d * d * 0.16, my + (x1 - x0) / d * d * 0.16
        pth = Path([(x0, y0), (cx, cy), (x1, y1)],
                   [Path.MOVETO, Path.CURVE3, Path.CURVE3])
        ax.add_patch(PathPatch(pth, facecolor='none', edgecolor=p_col(mp[k, i]),
                               linewidth=r_lw(mr[k, i]), alpha=0.85, zorder=1))
for k in range(4):
    ax.scatter(*comm_xy[k], s=34, c='#7b68d8', edgecolor='#4a3aa8',
               linewidths=0.7, zorder=5)
    ax.text(comm_xy[k][0] - 0.45, comm_xy[k][1], comms[k], ha='right',
            va='center', fontsize=7, linespacing=1.25)
for (x, y) in node_xy:
    ax.scatter(x, y, s=13, c='#7b68d8', edgecolor='#4a3aa8', linewidths=0.6,
               zorder=5)

# ---- 右侧图例
lx = n + 3.4
ax.text(lx, 0.1, "Mantel's $p$", fontsize=8, ha='left', va='center')
seg = [('#c9c9c9', '$p \\geq 0.05$'), ('#b3cc33', '$0.001 \\leq p < 0.05$'),
       ('#35a2be', '$p < 0.001$')]
for k, (cc, tt) in enumerate(seg):
    y = 0.75 + k * 0.62
    ax.plot([lx, lx + 1.1], [y, y], color=cc, lw=1.4)
    ax.text(lx + 1.3, y, tt, fontsize=7.5, ha='left', va='center')
ax.text(lx, 2.9, "Mantel's $r$", fontsize=8, ha='left', va='center')
for k, (lw_, tt) in enumerate([(0.7, '$r < 0.1$'), (1.4, '$0.1 \\leq r < 0.2$'),
                               (2.2, '$r \\geq 0.2$')]):
    y = 3.55 + k * 0.62
    ax.plot([lx, lx + 1.1], [y, y], color='#555555', lw=lw_)
    ax.text(lx + 1.3, y, tt, fontsize=7.5, ha='left', va='center')
ax.text(lx, 5.6, "Pearson's $r$", fontsize=8, ha='left', va='center')
p0 = ax.transData.transform((lx + 0.15, 9.6))
p1 = ax.transData.transform((lx + 0.15 + 0.85, 6.05))
inv = fig.transFigure.inverted()
f0, f1 = inv.transform(p0), inv.transform(p1)
cax = fig.add_axes([f0[0], min(f0[1], f1[1]), f1[0] - f0[0],
                    abs(f1[1] - f0[1])])
cb = fig.colorbar(ScalarMappable(norm=norm_pr, cmap=cmap_pr), cax=cax,
                  ticks=[1, 0.5, 0, -0.5, -1])
cb.ax.tick_params(labelsize=6.5, length=2)
cb.outline.set_linewidth(0.6)

save(fig, 'case_seg089.png')
