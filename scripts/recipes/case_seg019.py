# -*- coding: utf-8 -*-
"""案例19 - Nature 注释热图: 43 胆汁酸 × 8 受体。
红=上调、蓝绿=下调、白=无变化, 显著格*号; 顶部 Fold Change 对数色条; 行按类别分组留白。
参考: frames/seg_019.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm
from matplotlib.cm import ScalarMappable

conv = ['CA', 'CDCA', 'DCA', 'UDCA', 'LCA', 'TCA', 'GCA']
aas = ['Ala', 'Arg', 'Glu', 'His', 'Ile', 'Leu', 'Lys', 'Met', 'Phe',
       'Ser', 'Trp', 'Tyr']
conj = ['CA', 'CDCA', 'DCA', 'UDCA']
bbaa = []
for k, a in enumerate(aas):           # 每氨基酸 3 种偶联物, 轮换跳过 -> 36 行
    sub = [c for ci, c in enumerate(conj) if ci != (k + 1) % 4]
    bbaa += [a + '-' + c for c in sub]
rows = conv + bbaa                    # 7 + 36 = 43
nrow_data = len(rows)
recs = ['FXR', 'VDR', 'CAR3', 'PXR', 'AHR', 'PPARA', 'PPARD', 'PPARG']
ncol = len(recs)

r = rng(19)
v = np.zeros((nrow_data, ncol))       # log2(FC), 0 = 无变化
sig = np.zeros((nrow_data, ncol), bool)
for i in range(nrow_data):
    for j in range(ncol):
        u = r.random()
        if u < 0.13:                  # 强上调
            v[i, j] = r.uniform(1.6, 7.3)
            sig[i, j] = True
        elif u < 0.30:                # 弱上调
            v[i, j] = r.uniform(0.3, 1.5)
            sig[i, j] = r.random() < 0.55
        elif u < 0.52:                # 下调
            v[i, j] = -r.uniform(0.2, 1.4)
            sig[i, j] = r.random() < 0.5
        else:
            v[i, j] = r.uniform(-0.1, 0.1)
v[1, 0] = 5.2; sig[1, 0] = True       # CDCA-FXR 深红
v[4, 0] = 4.6; v[4, 1] = 4.9          # LCA 深红
sig[4, 0] = sig[4, 1] = True

# 离散色带: 蓝绿 -> 白 -> 红 (log2 FC 轴, 0 居中偏左)
bounds = [-1.6, -0.9, -0.25, -0.05, 0.05, 0.55, 1.5, 3.4, 7.6]
colors = ['#35978f', '#7fcdbb', '#cfe8e3', '#ffffff',
          '#fcdbc8', '#ef8a62', '#c0392b', '#a63603']
cmap = LinearSegmentedColormap.from_list('fc', list(colors), N=len(colors))
norm = BoundaryNorm(bounds, cmap.N)

# 行矩阵: 43 数据行 + 1 空行(分组留白), 组间 1 行
nrow = nrow_data + 1
gap_at = len(conv)                    # 第 8 行为空
M = np.zeros((nrow, ncol))
S = np.zeros((nrow, ncol), bool)
ii = 0
for i in range(nrow):
    if i == gap_at:
        continue
    M[i] = v[ii]; S[i] = sig[ii]; ii += 1

fig = plt.figure(figsize=cm2in(13.5, 21.5))
gs = fig.add_gridspec(2, 1, height_ratios=[0.055, 1.0], hspace=0.10,
                      left=0.28, right=0.94, top=0.955, bottom=0.055)
ax_cb = fig.add_subplot(gs[0])
ax = fig.add_subplot(gs[1])

ax.pcolormesh(np.arange(ncol + 1), np.arange(nrow + 1), M,
              cmap=cmap, norm=norm, edgecolors='#8a8a8a', linewidth=0.35)
ax.set_ylim(nrow, 0)
ax.set_xlim(-4.6, ncol)

ax.set_xticks(np.arange(ncol) + 0.5)
ax.set_xticklabels(recs, rotation=45, ha='right', fontsize=8)
ax.set_yticks([])
ax.tick_params(length=2)
for sp in ax.spines.values():
    sp.set_visible(False)
ax.add_patch(plt.Rectangle((0, 0), ncol, nrow, facecolor='none',
                           edgecolor='black', linewidth=1.0, zorder=5))

# 行名(跳过空行) + 分组侧标签
labels = []
for i in range(nrow):
    if i == gap_at:
        labels.append('')
    else:
        labels.append(rows[labels.count('') and i - 1] if False else '')
ii = 0
for i in range(nrow):
    if i == gap_at:
        continue
    ax.text(-0.25, i + 0.5, rows[ii], ha='right', va='center', fontsize=6.2)
    ii += 1
ax.add_patch(plt.Rectangle((-4.35, -0.5), 1.35, len(conv) + 0.4,
                           facecolor='none', edgecolor='none'))
ax.text(-3.7, len(conv) / 2.0, 'Conventional\nBile Acids', rotation=90,
        ha='center', va='center', fontsize=7.5, linespacing=1.2)
ax.text(-3.7, gap_at + 1 + (nrow - gap_at - 1) / 2.0, 'BBAAs', rotation=90,
        ha='center', va='center', fontsize=7.5)

# 显著性星号
for i in range(nrow):
    if i == gap_at:
        continue
    for j in range(ncol):
        if S[i, j]:
            ax.text(j + 0.5, i + 0.5, '*', ha='center', va='center',
                    fontsize=7, color='#1a1a1a')

# 顶部 Fold Change 对数色条 (10^0 10^1; 离散分箱下 10^1/10^2 过近会粘连, 故稀疏化)
ax_cb.axis('off')
sm = ScalarMappable(cmap=cmap, norm=norm)
cb = fig.colorbar(sm, cax=ax_cb.inset_axes([0.42, 0.05, 0.50, 0.90],
                    transform=ax_cb.transAxes),
                  orientation='horizontal',
                  ticks=[0, np.log2(10)])
cb.ax.set_xticklabels([r'$10^0$', r'$10^1$'])
cb.ax.tick_params(labelsize=7.5, length=2.5, pad=2)
cb.outline.set_linewidth(0.7)
ax_cb.text(0.10, 0.5, 'Fold\nChange', transform=ax_cb.transAxes,
           ha='left', va='center', fontsize=8.5, linespacing=1.1)

save(fig, 'case_seg019.png')
