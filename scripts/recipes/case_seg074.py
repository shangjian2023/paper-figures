# -*- coding: utf-8 -*-
"""案例74 - Nature 空转&组合图: 哑铃 + 点阵热图 + KS 横条 三联面板。
参考: frames/seg_074.jpg — 左哑铃(WT黑/KO青), 中点阵(色=YlOrRd 表达,大小=占比), 右横条 KS 三色, 底部图例。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *
set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors as mcolors
from matplotlib.ticker import FormatStrFormatter

SEED = 74
r74 = rng(SEED)

CELLS = ['Enterocyte 2', 'Enterocyte 3', 'CD8 T Cell \u03b1\u03b1+', 'Goblet', 'MAIT',
         'Enterocyte 1', 'T Cell \u03b3\u03b4', 'NK Cell', 'T Cell', 'ILC',
         'CD8 T Cell \u03b1\u03b2+', 'B Cell', 'Eosinophil', 'Vascular Endothelial',
         'Fibroblast Apo*', 'cDC1', 'DC2', 'Monocyte', 'Macrophage', 'Tuft',
         'CD4 T Cell', 'Early Enterocyte', 'Complement Fibroblast',
         'Enteroendocrine', 'Megakaryocyte/Platelet', 'Fibroblast',
         'Fibroblast Pdgfrb+', 'Fibroblast Lymphatic', 'Fibroblast Pdgfra+',
         'Fibroblast NCam1+']
M = len(CELLS)
GENES = ['Tgfb1', 'Tgfb2', 'Tgfb3', 'Itgb6', 'Itgb8', 'Itgav', 'Ltbp3']
KO_COL, CYAN, ORNG, GREY = '#45A5B8', '#7FCDD6', '#E87D2B', '#CCCCCC'

# 哑铃数据: 相关性从上到下降序
base = np.linspace(0.36, -0.27, M) + r74.normal(0, 0.012, M)
wt = base.copy()
ko = base + r74.normal(0, 0.055, M)
order = np.argsort(-base)
CELLS_S = [CELLS[i] for i in order]
wt, ko = wt[order], ko[order]

# 点阵数据
frac = r74.beta(1.1, 3.0, (M, 7)) * 78 + 3
expr = np.clip(r74.gamma(2.2, 0.42, (M, 7)), 0.05, 2.2)
for rr, cc, v in [(7, 4, 2.4), (12, 0, 2.55), (15, 0, 2.3), (16, 0, 2.35),
                  (29, 6, 2.5), (20, 1, 2.25), (2, 2, 2.2), (25, 4, 2.3)]:
    expr[rr, cc] = v

# KS 数据
cat = r74.choice(3, M, p=[0.42, 0.44, 0.14])
ks = np.where(cat == 0, r74.uniform(3, 16, M),
              np.where(cat == 1, r74.uniform(9, 29, M), r74.uniform(0.8, 4, M)))
KS_COL = [CYAN, ORNG, GREY]

fig = plt.figure(figsize=cm2in(19, 13))
gs = fig.add_gridspec(1, 3, width_ratios=[1.35, 1.9, 1.0], wspace=0.07,
                      left=0.16, right=0.985, top=0.90, bottom=0.235)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1], sharey=ax1)
ax3 = fig.add_subplot(gs[2], sharey=ax1)
y = np.arange(M)[::-1]

# ---------------------------------------------------------------- 左: 哑铃
for j in range(M):
    ax1.plot([wt[j], ko[j]], [y[j], y[j]], color='#AAAAAA', lw=0.9, zorder=2)
ax1.scatter(wt, y, s=22, color='black', zorder=3)
ax1.scatter(ko, y, s=20, color=KO_COL, zorder=3)
ax1.set_yticks(y)
ax1.set_yticklabels(CELLS_S, fontsize=6.3)
ax1.set_xlim(-0.33, 0.44)
ax1.set_ylim(-0.8, M - 0.2)
ax1.set_xticks(np.arange(-0.3, 0.5, 0.1))
ax1.grid(axis='x', ls=':', color='#BBBBBB', lw=0.6)
ax1.tick_params(length=2)
ax1.set_xlabel('Correlation between expression and closeness\nto the cell',
               fontsize=7.5)
ax1.text(0.02, 1.028, 'Cell Type', transform=ax1.transAxes, fontsize=8,
         fontweight='bold', ha='left')
ax1.set_title('TGF\u03b2RII-dependent signature', fontsize=8.5, pad=16, x=0.75)

# ---------------------------------------------------------------- 中: 点阵
for j in range(M):
    for g in range(7):
        ax2.scatter(g, y[j], s=6 + 130 * frac[j, g] / 80.0,
                    c=[plt.get_cmap('YlOrRd')(min(expr[j, g] / 2.7, 1.0))],
                    edgecolors='#777777', linewidths=0.4, zorder=3)
ax2.set_xticks(range(7))
ax2.set_xticklabels([italic_gene(g) for g in GENES], fontsize=7, rotation=90)
ax2.tick_params(length=0, labelleft=False)
ax2.set_title('Gene Expression', fontsize=8.5, pad=20, x=0.5)
ax2.text(1.5, 1.012, 'TGF\u03b2', fontsize=7.5, ha='center',
         transform=ax2.get_xaxis_transform())
ax2.plot([-0.45, 3.45], [1.002, 1.002], lw=0.7, color='black',
         transform=ax2.get_xaxis_transform(), clip_on=False)
ax2.text(5.0, 1.012, 'present.', fontsize=7.5, ha='center',
         transform=ax2.get_xaxis_transform())
ax2.plot([3.55, 6.45], [1.002, 1.002], lw=0.7, color='black',
         transform=ax2.get_xaxis_transform(), clip_on=False)
despine(ax2, left=True, bottom=True)

# ---------------------------------------------------------------- 右: KS 横条
ax3.barh(y, ks, height=0.62, color=[KS_COL[c] for c in cat],
         edgecolor='#888888', lw=0.3)
ax3.set_xlim(0, 31)
ax3.set_xticks([0, 25])
ax3.tick_params(length=2, labelsize=6.5)
ax3.tick_params(labelleft=False)
ax3.set_xlabel('KS\nWT vs\nTGF\u03b2RII KO', fontsize=7)
ax3.set_title('proximity\ndifferences', fontsize=8, pad=4)
ax3.grid(axis='x', ls=':', color='#BBBBBB', lw=0.6)
despine(ax3)

# ---------------------------------------------------------------- 底部图例(4 组)
fig.text(0.03, 0.075, 'P14 CD8 T Cell', fontsize=7)
fig.text(0.045, 0.050, '\u25cf', fontsize=7, color='black')
fig.text(0.060, 0.049, 'WT', fontsize=6.5)
fig.text(0.045, 0.026, '\u25cf', fontsize=7, color=KO_COL)
fig.text(0.060, 0.025, 'TGF\u03b2RII KO', fontsize=6.5)

fig.text(0.245, 0.075, 'Mean expression\nin group', fontsize=7)
cax = fig.add_axes([0.25, 0.040, 0.10, 0.016])
cb = fig.colorbar(cm.ScalarMappable(norm=mcolors.Normalize(0, 2.5),
                                    cmap=plt.get_cmap('YlOrRd')), cax=cax,
                  orientation='horizontal')
cb.set_ticks([0, 1, 2])
cb.ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
cb.ax.tick_params(labelsize=6, length=2)
cb.outline.set_linewidth(0.5)

fig.text(0.455, 0.075, 'Fraction of cells\nin group (%)', fontsize=7)
for k_i, (v, lab) in enumerate([(10, '10'), (40, '40'), (70, '70')]):
    xx = 0.475 + k_i * 0.042
    fig.add_artist(plt.Circle((xx, 0.046), 0.003 + 0.0075 * v / 70.0,
                              transform=fig.transFigure, facecolor='#D9D9D9',
                              edgecolor='#888888', lw=0.5))
    fig.text(xx, 0.012, lab, fontsize=6, ha='center')

fig.text(0.66, 0.075, 'TGF\u03b2RII KO cells are', fontsize=7)
for k_i, (lab, col) in enumerate([('Further', CYAN), ('Closer', ORNG),
                                  ('Similar', GREY)]):
    yy = 0.050 - k_i * 0.024
    fig.add_artist(plt.Rectangle((0.665, yy - 0.004), 0.013, 0.013,
                                 transform=fig.transFigure, facecolor=col,
                                 edgecolor='#888888', lw=0.4))
    fig.text(0.683, yy + 0.002, lab, fontsize=6.5)

save(fig, 'case_seg074.png')
