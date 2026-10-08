# -*- coding: utf-8 -*-
"""案例78 (seg76) - New Phytol. 相关性网络 & 散点矩阵。
参考: frames/seg_076.jpg — 右上三角 6x6 散点矩阵(对角名称盒, 黑拟合线, 点色=4样地,
点形=叶型), 左下相关网络: 灰盒角点节点, 弧线连边 蓝 r>=0 / 红 r<0, 实线 P<0.05 / 虚线 NS;
左侧 Site/Leaf_type/Pearson's r/P value 图例。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *
set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch

r = rng(76)

# ---------------- 数据: 6 叶性状 x 90 观测, 4 样地 x 2 叶型
vars6 = ['Leaf N\nconcentration', 'Chl\nconcentration', 'SLA',
         'Stomatal\ndensity', 'Pore length', 'WUE$_i$']
nv = len(vars6)
sites = ['CB: Cold-temperate forest', 'DL: Warm-temperate forest',
         'DH: Subtropical forest', 'XSBN: Tropical forest']
site_col = ['#2E7D64', '#F08080', '#AFEEEE', '#C23B3B']
n = 90
site = r.integers(0, 4, n)
leaf = r.integers(0, 2, n)                      # 0 落叶 1 常绿
latent = r.normal(0, 1, n)
load = np.array([0.9, 0.8, 0.5, -0.6, -0.4, 0.7])      # 性状在经济谱上的载荷
X = latent[:, None] * load[None, :] + r.normal(0, 0.55, (n, nv))
X += r.normal(0, 0.3, (4, nv))[site]            # 样地效应
scales = np.array([12, 4, 150, 300, 12, 6])
X = X * scales + np.array([22, 6, 160, 380, 13, 8])
X = np.clip(X, scales * 0.06, None)              # 性状值保持为正

# 网络节点: 6 个对角盒角点 + 2 个自由节点(G_wmax, V_cmax)
# 边: (i, j, r, p)  节点编号 0..5 = 性状, 6 = G_wmax, 7 = V_cmax
edges = [(0, 6, 0.72, 0.001), (6, 7, 0.65, 0.002), (7, 3, 0.82, 0.001),
         (0, 5, 0.68, 0.002), (5, 4, 0.70, 0.001), (7, 5, -0.62, 0.004),
         (0, 3, -0.55, 0.008), (1, 2, 0.62, 0.001), (2, 4, 0.35, 0.12),
         (0, 1, 0.55, 0.003), (1, 5, 0.30, 0.16), (6, 3, 0.42, 0.06),
         (7, 4, 0.30, 0.10), (3, 4, 0.40, 0.05), (1, 4, -0.32, 0.10),
         (2, 5, 0.28, 0.22), (6, 5, 0.33, 0.09), (2, 3, -0.30, 0.15)]

# ---------------- 布局: 左窄列图例, 右侧 6x6 上三角矩阵
fig = plt.figure(figsize=cm2in(19.5, 15.5))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 2.05], wspace=0.02,
                      left=0.01, right=0.99, top=0.97, bottom=0.03)
gsL = gs[0, 0].subgridspec(1, 1)
ax_net = fig.add_subplot(gsL[0])
ax_net.axis('off')
gsR = gs[0, 1].subgridspec(nv, nv, wspace=0.05, hspace=0.05)

axs = {}
for i in range(nv):
    for j in range(i, nv):
        axs[(i, j)] = fig.add_subplot(gsR[i, j])

rng2 = np.random.default_rng(176)
for i in range(nv):
    for j in range(i, nv):
        ax = axs[(i, j)]
        if i == j:                               # 对角: 名称盒(四边框)
            ax.text(0.5, 0.5, vars6[i], transform=ax.transAxes, ha='center',
                    va='center', fontsize=8.5)
            for sp in ax.spines.values():
                sp.set_visible(True); sp.set_linewidth(1.1)
            ax.set_xticks([]); ax.set_yticks([])
            continue
        for s in range(4):
            m = (site == s)
            for lf, mk in ((0, 'o'), (1, '^')):
                mm = m & (leaf == lf)
                ax.scatter(X[mm, j], X[mm, i], s=14, marker=mk,
                           c=site_col[s], alpha=0.85, linewidths=0.3,
                           edgecolors='gray', zorder=3)
        kj = X[:, j]; ki = X[:, i]
        b, a = np.polyfit(kj, ki, 1)
        xs = np.linspace(kj.min(), kj.max(), 10)
        ax.plot(xs, a + b * xs, color='black', lw=1.3, zorder=4)
        ax.set_xticks([]); ax.set_yticks([])
        ax.tick_params(length=0)

# 外缘刻度: 顶行 x 刻度在上方, 最右列 y 刻度在右侧
for j in range(nv):
    ax = axs[(0, j)]
    if j > 0:
        lo, hi = X[:, j].min(), X[:, j].max()
        ax.set_xticks([lo + 0.15 * (hi - lo), hi - 0.15 * (hi - lo)])
        ax.set_xticklabels([f'{v:.0f}' for v in ax.get_xticks()], fontsize=6.5)
        ax.xaxis.set_ticks_position('top'); ax.tick_params(top=True, length=2)
for i in range(nv):
    ax = axs[(i, nv - 1)]
    if i < nv - 1:
        lo, hi = X[:, i].min(), X[:, i].max()
        ax.set_yticks([lo + 0.18 * (hi - lo), hi - 0.18 * (hi - lo)])
        ax.set_yticklabels([f'{v:.0f}' for v in ax.get_yticks()], fontsize=6.5)
        ax.yaxis.set_ticks_position('right'); ax.tick_params(right=True, length=2)

# ---------------- 相关网络(覆盖全图的透明 Axes, 用 figure 坐标)
axo = fig.add_axes([0, 0, 1, 1], zorder=10)
axo.axis('off')
axo.set_xlim(0, 1); axo.set_ylim(0, 1)

# 节点: 对角盒左下角(fig 坐标) + 自由节点
corner = {}
for i in range(nv):
    bb = axs[(i, i)].get_position()
    corner[i] = (bb.x0, bb.y0)
pts = dict(corner)
pts[6] = (0.115, 0.46)                          # G_wmax
pts[7] = (0.255, 0.335)                         # V_cmax

blue, red = '#3A5FCD', '#C23B3B'
for k, (i, j, rv, pv) in enumerate(edges):
    x0, y0 = pts[i]; x1, y1 = pts[j]
    dx, dy = x1 - x0, y1 - y0
    # 弧线统一向左下侧弓出, 避免横穿散点矩阵
    side = 1.0 if (dx + dy) > 0 else -1.0
    rad = side * (0.14 + 0.04 * (k % 3))
    col = blue if rv >= 0 else red
    ls = '-' if pv < 0.05 else (0, (4, 3))
    lw = 0.8 + 3.4 * abs(rv) * (1.0 if pv < 0.05 else 0.45)
    axo.add_patch(FancyArrowPatch((x0, y0), (x1, y1),
                                  connectionstyle=f'arc3,rad={rad}',
                                  arrowstyle='-', color=col, ls=ls, lw=lw,
                                  alpha=0.75, zorder=2))
for k in range(6):                               # 盒角点
    axo.scatter(*corner[k], s=26, c='#9E9E9E', edgecolor='#606060',
                linewidth=0.6, zorder=4)
for k in (6, 7):                                 # 自由节点 + 斜体名
    axo.scatter(*pts[k], s=30, c='#9E9E9E', edgecolor='#606060',
                linewidth=0.6, zorder=4)
axo.text(pts[6][0] - 0.015, pts[6][1] + 0.018, '$G_{\\mathrm{wmax}}$',
         fontsize=11, ha='right', va='bottom')
axo.text(pts[7][0] - 0.015, pts[7][1] - 0.012, '$V_{\\mathrm{cmax}}$',
         fontsize=11, ha='right', va='top')

# ---------------- 左侧图例
def leg_block(y, title, handles, labels, fs=7):
    axo.text(0.02, y + 0.055, title, fontsize=8, fontweight='bold',
             ha='left', va='top', transform=axo.transAxes)
    leg = axo.legend(handles, labels, loc='upper left', bbox_to_anchor=(0.02, y),
                     bbox_transform=axo.transAxes, frameon=False, fontsize=fs,
                     handlelength=1.2, borderaxespad=0)
    axo.add_artist(leg)   # 同轴多图例: 固定住, 防止下次 legend() 调用覆盖
    return leg

h1 = [Line2D([], [], marker='o', ls='', color=c, ms=6) for c in site_col]
leg_block(0.965, 'Site', h1, sites)
h2 = [Line2D([], [], marker=m, ls='', color='#555555', ms=6) for m in 'o^']
leg_block(0.72, 'Leaf_type', h2, ['Deciduous', 'Evergreen'])
h3 = [Line2D([], [], color=red, lw=2), Line2D([], [], color=blue, lw=2)]
leg_block(0.385, "Pearson's $r$", h3, ['< 0', '>= 0'])
h4 = [Line2D([], [], color='#555555', lw=1.4, ls='-'),
      Line2D([], [], color='#555555', lw=1.4, ls='--')]
leg_block(0.262, '$P$ value', h4, ['< 0.05', '>= 0.05'])

save(fig, 'case_seg076.png')
