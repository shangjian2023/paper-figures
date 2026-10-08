# -*- coding: utf-8 -*-
"""案例23 - Nature 三角相关聚类热图: ~90 基因下三角热图 + 顶部聚类树 + 模块灰底标签。
45° 旋转三角形, 基因名沿两斜边放射, 右下 rho 色条。
参考: frames/seg_023.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.patches import Rectangle
from matplotlib.transforms import Affine2D
from matplotlib.cm import ScalarMappable
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import squareform

n = 90
sizes = [16, 30, 44]                       # TF / ECM / 其他 模块
gA = ['Tacc2', 'Egr1', 'Fos', 'Fosb', 'Jun', 'Jund', 'Fosl2', 'Carm1',
      'Ddx5', 'Gadd45g', 'Klf4', 'Runx1', 'Irf2', 'Mafg', 'Nfatc1', 'Zfp36']
gB = ['Akr1c18', 'Col1a1', 'Fn1', 'Mmp2', 'Postn', 'Lum', 'Vim', 'Itga10',
      'Thbs4', 'Spp1', 'Tgfb1', 'Cdh2', 'Wnt9a', 'Fam13a', 'Atp6v0e2',
      'Rif1', 'Dnajc11', 'Tmem45b', 'Pigq', 'Tns3', 'Gpc4', 'Fam171a1',
      'Itgb1', 'Epha4', 'Ramp1', 'Sort1', 'Padi2', 'Gas6', 'Sez6l',
      'Slc30a7']
gC = ['Cnn2', 'Utrn', 'Srgap2', 'Abca8a', 'Efnb2', 'Lhfpl2', 'Adamts6',
      'Apod', 'Cldn10', 'Cldn7', 'Myof', 'Fermt2', 'Sbsn', 'Cgn', 'Espn',
      'Lorr', 'Casp12', 'Tgfbr1', 'Stat3', 'NfkB1', 'Mtor', 'Bcl2', 'Bax',
      'Cdkn1a', 'Cebpb', 'Egr2', 'Kdm5b', 'Lmnb1', 'Smad2', 'Yap1',
      'Zeb1', 'Xpo1', 'Wnt3a', 'Vegfa', 'Pparg', 'Esr1', 'Jak1', 'Mmp14',
      'Nfe2l2', 'Ptenc', 'Fam102a', 'Unc13b', 'Rimbp2', 'Tenm2']
genes = gA + gB + gC
assert len(genes) == n

r = rng(23)
R = r.uniform(-0.25, 0.30, (n, n))
bnd = np.cumsum([0] + sizes)
for k in range(3):                         # 模块内强正相关
    a, b = bnd[k], bnd[k + 1]
    R[np.ix_(range(a, b), range(a, b))] = r.uniform(0.55, 0.95, (b - a, b - a))
R[np.ix_(range(bnd[0], bnd[1]), range(bnd[1], bnd[2]))] = r.uniform(-0.1, 0.35, (sizes[0], sizes[1]))
R = (R + R.T) / 2
np.fill_diagonal(R, 1.0)

Z = linkage(squareform(1 - R, checks=False), method='average')
dd = dendrogram(Z, no_plot=True)
order = np.array([int(x) for x in dd['ivl']])
R = R[np.ix_(order, order)]
genes_ord = [genes[i] for i in order]
lab = fcluster(Z, 3, criterion='maxclust')[order]
# 模块在叶子顺序中的连续区段
segs, s0 = [], 0
for i in range(1, n + 1):
    if i == n or lab[i] != lab[s0]:
        segs.append((s0, i - 1)); s0 = i

cmap = LinearSegmentedColormap.from_list(
    'rho', ['#9ecae1', '#deebf7', '#f7f7f7', '#fcae91', '#fb6a4a',
            '#cb181d', '#67000d'], N=256)
norm = Normalize(-0.35, 1.0)

fig = plt.figure(figsize=cm2in(19.0, 14.0))
gs = fig.add_gridspec(2, 2, height_ratios=[0.42, 1.0], width_ratios=[3.3, 0.62],
                      hspace=0.02, wspace=0.02,
                      left=0.015, right=0.985, top=0.90, bottom=0.015)
ax_d = fig.add_subplot(gs[0, 0])
ax = fig.add_subplot(gs[1, 0])
ax_r = fig.add_subplot(gs[1, 1]); ax_r.axis('off')

# ---- 顶部聚类树 (叶子 u = 2k+1, 与旋转坐标一致)
hmax = max(max(seg) for seg in dd['dcoord'])
for xc, yc in zip(dd['icoord'], dd['dcoord']):
    ax_d.plot(np.array(xc) / 5.0, yc, color='#3a3a3a', lw=0.55, zorder=3)
ax_d.set_xlim(-3, 2 * n + 1)
ax_d.set_ylim(0, hmax * 1.28)
ax_d.axis('off')
# 模块灰底 + 标签
for k, (a, b) in enumerate(segs):
    u0, u1 = 2 * a, 2 * b + 2
    ax_d.add_patch(Rectangle((u0, 0), u1 - u0, hmax * 0.30,
                             facecolor='#e2e2e2', edgecolor='#9a9a9a',
                             linewidth=0.7, zorder=1))
names_mod = ['TF module', 'ECM + $\\it{Akr1c18}$ module', '']
for k, (a, b) in enumerate(segs):
    if names_mod[k]:
        ax_d.text((2 * a + 2 * b + 2) / 2.0, hmax * 1.16, names_mod[k],
                  ha='center', va='top', fontsize=7.5)
ax_d.text(2 * n / 2.0, -hmax * 0.06, '', ha='center')

# ---- 45° 旋转三角热图 (下三角, 单元菱形)
t = Affine2D().rotate_deg(-45).scale(np.sqrt(2), np.sqrt(2)) + ax.transData
for i in range(n):
    for j in range(i + 1):
        val = R[i, j]
        ax.add_patch(Rectangle((j, i), 1, 1, transform=t,
                               facecolor=cmap(norm(val)),
                               edgecolor='white', linewidth=0.15, zorder=2))
# 对角基因角色点: TF=橙, ECM=紫
setA, setB = set(gA), set(gB)
for k in range(n):
    if genes_ord[k] in setA:
        ax.scatter(2 * k + 1, 1.3, s=7, c='#d95f02', zorder=5)
    elif genes_ord[k] in setB:
        ax.scatter(2 * k + 1, 1.3, s=7, c='#7b52ab', zorder=5)

ax.set_xlim(-2, 2 * n + 2)
ax.set_ylim(n + 2, -6)
ax.axis('off')

# 基因名: 左斜边=行名, 右斜边=列名
for i in range(n):
    ax.text(i - 0.4, i + 1.6, genes_ord[i], rotation=45, rotation_mode='anchor',
            ha='right', va='center', fontsize=3.1, style='italic')
for j in range(n):
    ax.text(n + j + 2.4, n - j, genes_ord[j], rotation=-45, rotation_mode='anchor',
            ha='left', va='center', fontsize=3.1, style='italic')

# ---- 右侧: rho 色条 + 图例
sm = ScalarMappable(norm=norm, cmap=cmap)
cax = ax_r.inset_axes([0.30, 0.52, 0.30, 0.44], transform=ax_r.transAxes)
cb = fig.colorbar(sm, cax=cax, ticks=[1.0, 0.8, 0.6, 0.4, 0.2, 0, -0.2])
cb.ax.tick_params(labelsize=6, length=2)
cb.outline.set_linewidth(0.6)
ax_r.text(0.26, 1.00, 'Correlation $\\rho$', transform=ax_r.transAxes,
          ha='left', va='top', fontsize=7.5)
ax_r.scatter(0.34, 0.40, s=14, c='#d95f02', transform=ax_r.transAxes,
             clip_on=False)
ax_r.text(0.42, 0.40, 'Transcription factor', transform=ax_r.transAxes,
          ha='left', va='center', fontsize=7)
ax_r.scatter(0.34, 0.35, s=14, c='#7b52ab', transform=ax_r.transAxes,
             clip_on=False)
ax_r.text(0.42, 0.35, 'Extracellular matrix', transform=ax_r.transAxes,
          ha='left', va='center', fontsize=7)

fig.text(0.44, 0.965, 'Zona inaudita co-expression landscape in F$_2$ hybrids',
         ha='center', va='top', fontsize=8.5)

save(fig, 'case_seg023.png')
