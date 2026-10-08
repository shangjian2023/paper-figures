# -*- coding: utf-8 -*-
"""案例90(seg088) - Nature 二维变量相关性热图 (clustermap): 34 细胞类型 × 30 NMF 因子。
行列聚类树 + 紫正绿负色标(-0.5~0.5) + 行左侧 5 组分组色条。
参考: frames/seg_088.jpg"""
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

gcolors = {'E': '#F28E2B', 'Y': '#EDC948', 'M': '#8CD17D',
           'N': '#D37295', 'L': '#4E79A7'}
gname = {'E': 'Epithelium', 'Y': 'Mesenchyme', 'M': 'Myeloid',
         'N': 'Endothelium', 'L': 'Lymphoid'}
row_groups = list('EEEEEEMMEEEEEENNYYLYYYNNLLLLYYYMLL')
rows_nm = ['Basal cells', 'Differentiating ciliated cells',
           'SCGB3A2+ SCGB1A1+ cells', 'Ciliated cells', 'MUC5AC+ cells',
           'MUC5B+ cells', 'Macrophages', 'Proliferating macrophages',
           'AT1 cells', 'AT2 cells', 'SCGB3A2+ cells',
           'Proliferating epithelial cells', 'Transitional AT2 cells',
           'Endothelial cells', 'Lymphatic endothelial cells',
           'Smooth muscle cells', 'B cells', 'HAS1 high fibroblasts',
           'T cells', 'PLIN2+ fibroblasts', 'Proliferating T cells',
           'Mesothelial cells', 'pDCs', 'Mast cells', 'cDCs', 'Monocytes',
           'NK cells', 'Plasma cells', 'Fibroblasts', 'Myofibroblasts',
           'Peribronchial fibroblasts', 'Adventitial fibroblasts',
           'Ionocytes', 'KRT5-/KRT17+ cells']
nr, nc = 34, 30
cols_nm = ['F%d' % k for k in range(1, nc + 1)]

r = rng(88)
M = r.uniform(-0.28, 0.28, (nr, nc))
gkeys = ['E', 'M', 'Y', 'N', 'L']
for a, ga in enumerate(gkeys):            # 每组对应一段因子的正相关块
    ia = np.where(np.array(row_groups) == ga)[0]
    fa = slice(a * 5 + 2, a * 5 + 2 + 8)
    M[np.ix_(ia, np.arange(nc)[fa])] = r.uniform(0.30, 0.50, (len(ia), 8))
    fb = slice(((a + 2) % 5) * 5 + 1, ((a + 2) % 5) * 5 + 1 + 6)
    M[np.ix_(ia, np.arange(nc)[fb])] = r.uniform(-0.50, -0.28, (len(ia), 6))
strong = r.random((nr, nc)) < 0.045       # 少量强格
M[strong] = r.choice([-0.5, 0.5], strong.sum())
M = np.clip(M + r.normal(0, 0.05, (nr, nc)), -0.5, 0.5)

Zr = linkage(squareform(1 - np.corrcoef(M), checks=False), method='average')
Zc = linkage(squareform(1 - np.corrcoef(M.T), checks=False), method='average')
order_r = np.array([int(x) for x in dendrogram(Zr, no_plot=True)['ivl']])
order_c = np.array([int(x) for x in dendrogram(Zc, no_plot=True)['ivl']])
M = M[np.ix_(order_r, order_c)]
rows_o = [rows_nm[i] for i in order_r]
gcols_o = [row_groups[i] for i in order_r]
cols_o = [cols_nm[j] for j in order_c]

cmap = LinearSegmentedColormap.from_list(
    'pg', ['#453781', '#8073ac', '#f7f7f7', '#d8a1c8', '#a52c7f'], N=256)

fig = plt.figure(figsize=cm2in(19.0, 18.5))
gs = fig.add_gridspec(3, 4, height_ratios=[0.62, 5.2, 0.85],
                      width_ratios=[0.60, 0.14, 3.3, 1.35],
                      hspace=0.045, wspace=0.03,
                      left=0.015, right=0.985, top=0.955, bottom=0.015)
ax_dt = fig.add_subplot(gs[0, 2])
ax = fig.add_subplot(gs[1, 2])
ax_dl = fig.add_subplot(gs[1, 0])
ax_str = fig.add_subplot(gs[1, 1])
ax_lg = fig.add_subplot(gs[2, :]); ax_lg.axis('off')

ddt = dendrogram(Zc, no_plot=True)
hmax_c = max(max(s) for s in ddt['dcoord'])
for xc, yc in zip(ddt['icoord'], ddt['dcoord']):
    ax_dt.plot(np.array(xc) / 10.0, np.array(yc) / hmax_c, color='#3a3a3a',
               lw=0.6)
ddr = dendrogram(Zr, orientation='left', no_plot=True)
hmax_r = max(max(s) for s in ddr['dcoord'])
for xc, yc in zip(ddr['icoord'], ddr['dcoord']):
    ax_dl.plot(np.array(yc) / hmax_r, np.array(xc) / 10.0, color='#3a3a3a',
               lw=0.6)
ax_dt.set_xlim(-0.5, nc + 0.5); ax_dt.set_ylim(0, 1.05); ax_dt.axis('off')
ax_dl.set_xlim(1.05, -0.35); ax_dl.set_ylim(nr + 0.5, -0.5); ax_dl.axis('off')

# 热图 + 白色网格
ax.pcolormesh(np.arange(nc + 1), np.arange(nr + 1), M, cmap=cmap,
              norm=Normalize(-0.5, 0.5), edgecolors='white', linewidth=0.35)
ax.set_xlim(0, nc)
ax.set_ylim(nr, 0)
ax.set_xticks(np.arange(nc) + 0.5)
ax.set_xticklabels(cols_o, rotation=90, fontsize=6)
ax.set_yticks(np.arange(nr) + 0.5)
ax.set_yticklabels(rows_o, fontsize=6.2)
ax.tick_params(length=0, pad=2, labelleft=False, labelright=True)
for sp in ax.spines.values():
    sp.set_visible(True)
    sp.set_linewidth(0.8)

# 行分组色条
for i, g in enumerate(gcols_o):
    ax_str.add_patch(Rectangle((0, i), 1, 1, facecolor=gcolors[g],
                               edgecolor='white', linewidth=0.3))
ax_str.set_xlim(0, 1); ax_str.set_ylim(nr, 0); ax_str.axis('off')

fig.text(0.36, 0.975, 'NMF factors', ha='center', va='top', fontsize=8)

# ---- 底部图例
ax_lg.set_xlim(0, 1); ax_lg.set_ylim(0, 1)
ax_lg.text(0.03, 0.88, 'Group:', ha='left', va='center', fontsize=7.5)
for k, g in enumerate(['E', 'Y', 'M', 'N', 'L']):
    col, row = k % 3, k // 3
    x = 0.115 + col * 0.155
    y = 0.72 - row * 0.38
    ax_lg.add_patch(Rectangle((x, y - 0.09), 0.030, 0.18, facecolor=gcolors[g],
                              edgecolor='none'))
    ax_lg.text(x + 0.045, y, gname[g], ha='left', va='center', fontsize=7.5)
cax = ax_lg.inset_axes([0.62, 0.22, 0.24, 0.42], transform=ax_lg.transAxes)
cb = fig.colorbar(ScalarMappable(norm=Normalize(-0.5, 0.5), cmap=cmap),
                  cax=cax, orientation='horizontal', ticks=[-0.5, 0, 0.5])
cb.ax.tick_params(labelsize=6.5, length=2)
cb.outline.set_linewidth(0.6)
ax_lg.text(0.62, 0.88, 'Pearson cor.', ha='left', va='center', fontsize=7.5)

save(fig, 'case_seg088.png')
