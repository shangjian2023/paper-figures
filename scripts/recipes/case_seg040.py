# -*- coding: utf-8 -*-
"""案例40 - Cell 双三角聚类相关热图: 下三角(In-house 蓝白红) + 上三角(GSE 绿白紫),
四周 4 条 dendrogram, 左侧 JAK-STAT/HRD 注色, 右侧比例圆点, 关键簇红虚线框。
参考: frames/seg_040.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.patches import Rectangle
from matplotlib.cm import ScalarMappable
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import squareform

names = ['CD8+ Proliferative', 'CD4+ Proliferative', 'CD8+ IFN-responding',
         'CD4+ IFN-responding', 'CD4+ Effector Treg', 'CD8+ Progenitor Tex',
         'CD8+ Terminal Tex', 'CD4+ Effector Tph-like', 'CD4+ Resting Tph-like',
         'CD8+ Nuc-high', 'CD4+ Nuc-high', 'CD4+ HSP-high', 'CD4+ MAIT',
         'CD4+ Mito-high', 'CD4+ GZMK+', 'CD4+ IEG-high', 'CD4+ Tem',
         'CD8+ Tcm', 'CD4+ Tcm', 'CD8+ Tcm', 'CD8+ Trm', 'CD4+ Th17-like',
         'CD8+ Temra', 'CD4+ Resting Treg', 'CD4+ GZMH+', 'CD8+ IEG-high',
         'CD8+ Tem', 'CD4+ Tem']
n = len(names)

r = rng(40)
def make_R(seed):
    rr = np.random.default_rng(seed)
    M = rr.uniform(-0.4, 0.45, (n, n))
    for a, b, lo, hi in [(0, 9, 0.55, 0.95), (19, 28, 0.5, 0.9)]:
        M[np.ix_(range(a, b), range(a, b))] = rr.uniform(lo, hi, (b - a, b - a))
    M[np.ix_(range(0, 9), range(19, 28))] = rr.uniform(-0.8, -0.35, (9, 9))
    M = (M + M.T) / 2
    np.fill_diagonal(M, 1.0)
    return M
R1, R2 = make_R(1), make_R(2)
Rm = (R1 + R2) / 2

Z = linkage(squareform(1 - Rm, checks=False), method='average')
dd = dendrogram(Z, no_plot=True)
order = np.array([int(x) for x in dd['ivl']])
R1o, R2o = R1[np.ix_(order, order)], R2[np.ix_(order, order)]
names_o = [names[i] for i in order]
hmax = max(max(s) for s in dd['dcoord'])

cmap_gm = LinearSegmentedColormap.from_list(
    'gm', ['#3d9c40', '#a6dba3', '#f7f7f7', '#d29ecf', '#a3369c'], N=256)

fig = plt.figure(figsize=cm2in(20.5, 17.0))
gs = fig.add_gridspec(3, 4, height_ratios=[0.50, 3.5, 0.50],
                      width_ratios=[0.50, 3.5, 0.50, 1.55],
                      hspace=0.03, wspace=0.03,
                      left=0.005, right=0.99, top=0.96, bottom=0.01)
ax_dt = fig.add_subplot(gs[0, 1])
ax = fig.add_subplot(gs[1, 1])
ax_db = fig.add_subplot(gs[2, 1])
ax_dl = fig.add_subplot(gs[1, 0])
ax_dr = fig.add_subplot(gs[1, 2])
ax_lg = fig.add_subplot(gs[1, 3]); ax_lg.axis('off')

# ---- 4 条 dendrogram
for xc, yc in zip(dd['icoord'], dd['dcoord']):
    x = np.array(xc) / 10.0
    y = np.array(yc) / hmax * 0.92
    ax_dt.plot(x, y, color='#4a4a4a', lw=0.6)
    ax_db.plot(x, -y, color='#4a4a4a', lw=0.6)
    ax_dl.plot(y, x, color='#4a4a4a', lw=0.6)
    ax_dr.plot(y, x, color='#4a4a4a', lw=0.6)
for a in (ax_dt, ax_db, ax_dl, ax_dr):
    a.axis('off')
ax_dt.set_xlim(-0.4, n + 0.4); ax_dt.set_ylim(0, 1.0)
ax_db.set_xlim(-0.4, n + 0.4); ax_db.set_ylim(-1.0, 0)
ax_dl.set_xlim(1.0, -0.4); ax_dl.set_ylim(n + 0.4, -0.4)
ax_dr.set_xlim(-0.4, 1.0); ax_dr.set_ylim(n + 0.4, -0.4)

# ---- 双三角热图
lo = np.tril(np.ones((n, n)))            # 下三角含对角 -> In-house
up = np.triu(np.ones((n, n)), 1)         # 上三角 -> GSE
M1 = np.ma.masked_where(lo == 0, R1o)
M2 = np.ma.masked_where(up == 0, R2o)
ax.imshow(M1, cmap='RdBu_r', vmin=-1, vmax=1, interpolation='nearest')
ax.imshow(M2, cmap=cmap_gm, vmin=-1, vmax=1, interpolation='nearest')
ax.set_xlim(-3.1, n + 1.3)
ax.set_ylim(n - 0.5, -1.2)
ax.set_xticks([]); ax.set_yticks(np.arange(n) + 0.5)
ax.set_yticklabels(names_o, fontsize=5.2)
ax.tick_params(length=0, pad=2, labelleft=True, labelright=False)
for t, oi in zip(ax.get_yticklabels(), order):
    t.set_color('#c0392b' if oi < 9 else '#1a1a1a')
for i, oi in enumerate(order):
    c = '#c0392b' if oi < 9 else '#1a1a1a'
    ax.text(n + 0.75, i + 0.5, names[oi], ha='left', va='center',
            fontsize=5.2, color=c)

# 左侧注释方块: JAK-STAT 活性 + HRD FC
jak = r.uniform(-2.5, 2.5, n)
jak[order < 9] = r.uniform(1.2, 2.5, 9)
hrd = r.uniform(-1, 1, n)
hrd[order < 9] = r.uniform(-1, -0.2, 9)
for i in range(n):
    ax.scatter(-2.55, i + 0.5, marker='s', s=17,
               color=plt.get_cmap('RdBu_r')((jak[i] + 2.5) / 5.0))
    ax.scatter(-1.75, i + 0.5, marker='s', s=17,
               color=plt.get_cmap('PuOr')((hrd[i] + 1) / 2.0))
# 右侧比例圆点
prop = r.uniform(0.05, 1.0, n)
prop[order < 9] = r.uniform(0.5, 1.0, 9)
for i in range(n):
    ax.scatter(n + 0.15, i + 0.5, s=5 + 42 * prop[i],
               facecolor='#e8e8e8' if i % 3 else '#f3b8b8',
               edgecolor='#8a8a8a', linewidths=0.5)

# 关键簇红虚线框
for a, b in [(0, 9), (19, n)]:
    ax.add_patch(Rectangle((a - 0.5, a - 0.5), b - a, b - a, facecolor='none',
                           edgecolor='#c0392b', linestyle=(0, (4, 2)),
                           linewidth=0.9, zorder=6))

ax_dt.text(-2.5, 0.92, 'In-house', fontsize=8, fontweight='bold',
           ha='left', va='top')
ax_dt.text(-3.05, 0.50, '+RD', fontsize=4.8, ha='left', va='top')
ax_dt.text(-2.05, 0.50, 'JAK-STAT', fontsize=4.8, ha='left', va='top')
ax_db.set_ylim(-1.35, 0)
ax_db.text(n + 0.4, -1.28, 'GSE165897', fontsize=8, fontweight='bold',
           ha='right', va='bottom')

# ---- 右侧图例
ax_lg.set_xlim(0, 1); ax_lg.set_ylim(0, 1)
def hbar(y0, h, cmap_, vmin_, vmax_, ticks, title, fmt='%.0f'):
    ax_lg.text(0.02, y0 + h + 0.045, title, ha='left', va='bottom', fontsize=6.3,
               linespacing=1.15)
    cax = ax_lg.inset_axes([0.02, y0, 0.55, h], transform=ax_lg.transAxes)
    sm = ScalarMappable(norm=Normalize(vmin_, vmax_), cmap=cmap_)
    cb = fig.colorbar(sm, cax=cax, orientation='horizontal', ticks=ticks)
    cb.ax.set_xticklabels([fmt % t for t in ticks])
    cb.ax.tick_params(labelsize=5, length=1.5, pad=1)
    cb.outline.set_linewidth(0.5)

hbar(0.860, 0.045, 'PuOr', -1, 1, [-1, 0, 1],
     'HRD vs. HRP\nLog$_2$ FC')
ax_lg.text(0.62, 0.878, '\u00b7 P < 0.05', ha='left', va='center', fontsize=5.5)
ax_lg.text(0.02, 0.80, 'JAK-STAT\nPositive-cell proportion', ha='left',
           va='bottom', fontsize=6.3, linespacing=1.15)
for k, pc in enumerate([20, 40, 60, 80, 100]):
    ax_lg.scatter(0.065 + k * 0.115, 0.745, s=4 + 42 * pc / 100.0,
                  facecolor='#e0e0e0', edgecolor='#8a8a8a', linewidths=0.5)
ax_lg.text(0.02, 0.615, 'Mean pathway activity', ha='left', va='bottom',
           fontsize=6.3)
cax = ax_lg.inset_axes([0.02, 0.545, 0.55, 0.05], transform=ax_lg.transAxes)
cb = fig.colorbar(ScalarMappable(norm=Normalize(-2.5, 2.5), cmap='RdBu_r'),
                  cax=cax, orientation='horizontal', ticks=[-2.5, 0, 2.5])
cb.ax.tick_params(labelsize=5, length=1.5, pad=1)
cb.outline.set_linewidth(0.5)
ax_lg.text(0.02, 0.475, 'Proportion\ncorrelation (R$_s$)', ha='left',
           va='bottom', fontsize=6.3, linespacing=1.15)
cax = ax_lg.inset_axes([0.02, 0.405, 0.55, 0.05], transform=ax_lg.transAxes)
cb = fig.colorbar(ScalarMappable(norm=Normalize(-1, 1), cmap=cmap_gm),
                  cax=cax, orientation='horizontal', ticks=[-1, 0, 1])
cb.ax.tick_params(labelsize=5, length=1.5, pad=1)
cb.outline.set_linewidth(0.5)

save(fig, 'case_seg040.png')
