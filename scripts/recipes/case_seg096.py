# -*- coding: utf-8 -*-
"""案例98 - Nature 相关性矩阵点图(一)。
参考: frames/seg_096.jpg — 14行菌群×10列ARG, 圆面积=丰度3档, 填充红蓝=相关,
圆内*号=显著, 组间竖分隔线, 右侧双图例(色标+尺寸圆)。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.colors import TwoSlopeNorm

set_style()

rows = ['Bacteroidetes', 'Betaproteobacteria', 'Gammaproteobacteria',
        'Deltaproteobacteria', 'Alphaproteobacteria', 'Acidobacteria',
        'Chloroflexi', 'Actinobacteria', 'Nitrospirae', 'Chlorobi',
        'Planctomycetes', 'Verrucomicrobia', 'Gemmatimonadetes', 'Firmicutes']
cols = ['16S-ARG', 'Shotgun-ARG', '16S-Beta.lactam', 'Shotgun-Beta.lactam',
        '16S-Glycopeptide', 'Shotgun-Glycopeptide', '16S-Tetracycline',
        'Shotgun-Tetracycline', '16S-Aminoglycoside', 'Shotgun-Aminoglycoside']
nR, nC = len(rows), len(cols)

r = rng(96)
corr = r.normal(0, 0.22, (nR, nC)).clip(-0.85, 0.85)
# 让少数格子强相关, 模拟原图的高亮格子
for _ in range(14):
    corr[r.integers(0, nR), r.integers(0, nC)] = r.uniform(0.4, 0.78) * r.choice([-1, 1])
pval = r.uniform(0.0001, 1.0, (nR, nC))
sig = pval < 0.28
abund = r.choice([0, 1, 2], (nR, nC), p=[0.5, 0.33, 0.17])   # 3 档丰度
size3 = [95, 210, 360]           # 三档圆面积(pt^2)
sizes = np.take(size3, abund)

fig = plt.figure(figsize=cm2in(16.5, 15.5))
ax = fig.add_axes([0.21, 0.15, 0.55, 0.72])
ax.set_xlim(-0.5, nC - 0.5)
ax.set_ylim(nR - 0.5, -0.5)
ax.set_xticks(np.arange(nC))
ax.set_yticks(np.arange(nR))
ax.set_xticklabels(cols, rotation=32, ha='right', fontsize=7.5)
ax.set_yticklabels(rows, fontsize=8)
for s in ax.spines.values():
    s.set_visible(False)
ax.tick_params(length=0)

# 列组间竖分隔线 (每 2 列一组)
for gx in [1.5, 3.5, 5.5, 7.5]:
    ax.axvline(gx, color='0.35', lw=0.9, zorder=1)
ax.axhline(-0.5, color='0.2', lw=1.0, zorder=1)

norm = TwoSlopeNorm(vmin=-0.8, vcenter=0.0, vmax=0.8)
cmap = plt.get_cmap('RdBu')      # 正相关=蓝, 负相关=红 (同参考图)
for i in range(nR):
    for j in range(nC):
        c = cmap(norm(corr[i, j]))
        ax.scatter(j, i, s=sizes[i, j], facecolor=c, edgecolor='black',
                   linewidth=0.8, zorder=3)
        if sig[i, j]:
            ax.text(j, i, '*', ha='center', va='center', fontsize=9,
                    fontweight='bold', color='black', zorder=4)

# ------------------------------------------------ 右侧图例 1: Cor.with.ARG
cax = fig.add_axes([0.80, 0.60, 0.045, 0.22])
sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
fig.colorbar(sm, cax=cax, ticks=[-0.8, -0.4, 0.0, 0.4, 0.8])
cax.set_title('Cor.with.ARG', fontsize=8, loc='left', pad=6)
cax.tick_params(labelsize=7)

# ------------------------------------------------ 右侧图例 2: relative.abundance
lax = fig.add_axes([0.79, 0.26, 0.14, 0.20])
lax.set_xlim(0, 1)
lax.set_ylim(0, 1)
for s in lax.spines.values():
    s.set_visible(False)
lax.set_xticks([])
lax.set_yticks([])
lax.text(0.05, 0.98, 'relative.abundance', fontsize=8, va='top')
labels = ['(0.001,0.01]', '(0.01,0.1]', '(0.1,1]']
for k, (lab, s) in enumerate(zip(labels, size3)):
    yy = 0.62 - k * 0.30
    lax.scatter(0.22, yy, s=s, facecolor='white', edgecolor='black',
                linewidth=0.9, clip_on=False)
    lax.text(0.48, yy, lab, fontsize=7.5, va='center')

save(fig, 'case_seg096.png')
