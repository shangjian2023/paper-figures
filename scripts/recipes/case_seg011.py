# -*- coding: utf-8 -*-
"""案例11 - Nature 气泡热图: 26 基因 × 14 细胞类型。
点径=表达核比例, 绿色深浅=平均表达; 左侧分组灰条; 右侧色条+尺寸图例。
参考: frames/seg_011.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.patches import Rectangle

genes = ['CRISPLD2', 'COL4A4', 'FBLN5', 'C7', 'NEGR1',
         'PBX1', 'CLSTN2', 'RIMS1', 'KCNMA1', 'PRRX1',
         'JAZF1', 'FAT1', 'ITGA10', 'ENPP1', 'FN1', 'CADM1', 'PALLD',
         'TENM3', 'SLC44A5', 'FAP', 'FAM155A', 'AEBP1', 'THBS4',
         'FGF14', 'POSTN', 'COL22A1']
groups = [('Early', 0, 5), ('Intermediate', 5, 10), ('Late', 10, 26)]
cells = ['Activated fibroblast', 'Fibroblast', 'Cardiomyocyte', 'Endothelial',
         'Pericyte', 'Macrophage', 'VSMC', 'Lymphocyte', 'Endocardial',
         'Adipocyte', 'Neuronal', 'Lymphatic endothelial', 'Mast cell',
         'Epicardial']
ng, nc = len(genes), len(cells)

r = rng(11)
# 每基因平均表达水平与每细胞类型表达比例
avg = np.zeros((ng, nc))
pct = np.zeros((ng, nc))
for i in range(ng):
    base = r.uniform(0.8, 3.4)
    k = r.integers(2, 8)               # 表达的细胞类型数
    idx = r.choice(nc, size=k, replace=False)
    idx = np.concatenate([idx[:2], idx])   # 前两个细胞类型几乎总表达
    for j in idx:
        avg[i, j] = base * r.uniform(0.55, 1.15)
        pct[i, j] = r.uniform(0.12, 1.0)
    # 低表达背景点
    bg = r.choice(nc, size=r.integers(3, 7), replace=False)
    for j in bg:
        if pct[i, j] == 0:
            avg[i, j] = r.uniform(0.2, 0.7)
            pct[i, j] = r.uniform(0.02, 0.10)

norm = Normalize(vmin=0, vmax=3.6)
cmap = plt.get_cmap('Greens')

def dot_size(p):
    return 6 + 105 * p

fig = plt.figure(figsize=cm2in(15.5, 19.5))
gs = fig.add_gridspec(1, 2, width_ratios=[3.4, 1.0], wspace=0.02,
                      left=0.17, right=0.97, top=0.985, bottom=0.16)
gsr = gs[0, 1].subgridspec(2, 1, height_ratios=[1.0, 1.5], hspace=0.05)
ax = fig.add_subplot(gs[0, 0])
ax_c = fig.add_subplot(gsr[0])
ax_s = fig.add_subplot(gsr[1])

# ---- 气泡矩阵
for i in range(ng):
    for j in range(nc):
        p, a = pct[i, j], avg[i, j]
        if p < 0.11:                      # 背景小点: 浅灰绿空心
            ax.scatter(j, i, s=7, facecolor='#e2efe2', edgecolor='#9bbf9b',
                       linewidths=0.5, zorder=3)
        else:
            ax.scatter(j, i, s=dot_size(p), facecolor=cmap(norm(a)),
                       edgecolor='#3a7d44', linewidths=0.45, zorder=3)

ax.set_xlim(-7.0, nc - 0.3)
ax.set_ylim(ng - 0.4, -0.9)
ax.set_xticks(np.arange(nc))
ax.set_xticklabels(cells, rotation=90, fontsize=6.3)
ax.tick_params(axis='x', pad=1.5, length=2)
ax.set_yticks([])
for sp in ax.spines.values():
    sp.set_visible(True)
    sp.set_linewidth(0.8)

# ---- 基因名 + 分组灰条
for i, g in enumerate(genes):
    ax.text(-0.75, i, g, ha='right', va='center', fontsize=6.8)
for name, i0, i1 in groups:
    ax.add_patch(Rectangle((-6.6, i0 - 0.42), 1.5, (i1 - i0) - 0.16 + 0.42,
                           facecolor='#d4d4d4', edgecolor='none', zorder=1))
    ax.text(-5.85, (i0 + i1 - 1) / 2.0, name, rotation=90, ha='center',
            va='center', fontsize=7.5)

# ---- 右上: Avg expr 色条
ax_c.axis('off')
sm = ScalarMappable(norm=norm, cmap=cmap)
cb = fig.colorbar(sm, cax=ax_c.inset_axes([0.30, 0.02, 0.34, 0.80]),
                  ticks=[1, 2, 3])
cb.ax.tick_params(labelsize=7, length=2.5)
cb.outline.set_linewidth(0.7)
ax_c.text(0.30, 1.12, 'Avg\nexpr', transform=ax_c.transAxes,
          fontsize=8, ha='left', va='top', linespacing=1.1)

# ---- 右下: Pct nuclei 尺寸图例
ax_s.axis('off')
ax_s.set_xlim(0, 1)
ax_s.set_ylim(0, 1)
ax_s.text(0.16, 1.02, 'Pct nuclei\nexpr > 0', transform=ax_s.transAxes,
          fontsize=8, ha='left', va='top', linespacing=1.15)
levels = [0.2, 0.4, 0.6, 0.8, 1.0]
for k, p in enumerate(levels):
    y = 0.80 - k * 0.155
    ax_s.scatter(0.24, y, s=dot_size(p), facecolor='white',
                 edgecolor='#8a8a8a', linewidths=0.7)
    ax_s.text(0.40, y, '%d%%' % (p * 100), ha='left', va='center', fontsize=7.5)

save(fig, 'case_seg011.png')
