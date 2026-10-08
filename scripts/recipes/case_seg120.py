# -*- coding: utf-8 -*-
"""案例122 - 双色点阵相关矩阵: 57×57, 上三角 M1 绿-白-红, 下三角 M0 黄-白-紫,
点径=|r|, 对角灰色, 底部两个水平色标。
参考: frames/seg_120.jpg。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

set_style()

base = ['AR', 'ARV7', 'BROMO10', 'CCP', 'CD4_Act', 'CD8_Act', 'CHD1_loss',
        'Cholesterol', 'CTLA4', 'Decipher', 'EMT', 'ER_E', 'ER_L', 'EST_Purity',
        'EST_Sroma', 'FAM', 'Glycolysis', 'GR', 'HRdef', 'HRR', 'Hypoxia',
        'IFN', 'Imm190', 'Inflammation', 'KRAS', 'MDSC', 'Mtorc1', 'NE_Ala',
        'NE_Bat', 'NE_Bel', 'NE_Kun', 'NE_Tsai', 'PDL2', 'Persist', 'PerjM',
        'PI3K', 'PORTOS', 'PROSGen', 'PTEN_Liu', 'PTEN_Snr', 'RT_sens',
        'SPOP_mut', 'TLS', 'TP53_loss', 'TP53_Donh', 'Treg']
sfx = ['_HM', '_IPS', '_Liu', '_Carter', '_Ricketts', '_Weiner', '_Kuner',
       '_SnaR', '_Esch', '_Calib', '_pathway']
r = rng(120)
names = []
for k, b in enumerate(base):
    names.append(b + sfx[k % 11])
gene = ['BAX', 'BCL2', 'CDK4', 'CTNNB1', 'EGFR', 'ERBB2', 'FOS', 'JUN',
        'KRAS', 'MAPK1', 'MYC', 'NFKB1', 'PIK3CA', 'PTEN', 'RB1', 'SRC',
        'TP53', 'AKT1', 'BRAF', 'CASP3', 'CCND1', 'CDH1', 'EGR1', 'ESR1']
k = 0
while len(names) < 57:
    names.append(gene[k % len(gene)] + '_sig')
    k += 1
names = names[:57]
n = len(names)

# 两套相关矩阵 (对称), 带 8 个签名模块的块结构
mod = np.repeat(np.arange(8), np.ceil(n / 8).astype(int))[:n]
def make_corr():
    C = r.normal(0, 0.2, (n, n))
    sgn = r.choice([-1, 1], 8, p=[0.35, 0.65])
    for k in range(8):
        idx = mod == k
        C[np.ix_(idx, idx)] = r.normal(0.45 * sgn[k], 0.22, (idx.sum(), idx.sum()))
    C = (C + C.T) / 2.0
    np.fill_diagonal(C, 1.0)
    return C.clip(-0.96, 0.96)

M1 = make_corr()
M0 = make_corr()

cmap_m1 = LinearSegmentedColormap.from_list('m1', ['#3fd43f', '#f4fbf2', '#e63333'])
cmap_m0 = LinearSegmentedColormap.from_list('m0', ['#f2e13c', '#fdfdf6', '#6a1fa8'])

fig = plt.figure(figsize=cm2in(19.0, 19.0))
ax = fig.add_axes([0.20, 0.115, 0.74, 0.78])
ax.set_xlim(-0.5, n - 0.5)
ax.set_ylim(n - 0.5, -0.5)
ax.set_xticks(np.arange(n))
ax.set_yticks(np.arange(n))
ax.set_xticklabels(names, rotation=90, fontsize=4.0)
ax.set_yticklabels(names, fontsize=4.4)
ax.xaxis.tick_top()
ax.tick_params(length=1.2, pad=1.2)
for s in ax.spines.values():
    s.set_color('0.5')
# 浅灰网格
for g in range(n):
    ax.axhline(g + 0.5, color='0.90', lw=0.4, zorder=0)
    ax.axvline(g + 0.5, color='0.90', lw=0.4, zorder=0)

ii, jj = np.meshgrid(np.arange(n), np.arange(n), indexing='ij')
up = ii < jj
dn = ii > jj
diag = ii == jj
sz = lambda M: 2.0 + np.abs(M) * 26
ax.scatter(jj[up], ii[up], c=M1[up], s=sz(M1)[up], cmap=cmap_m1,
           vmin=-1, vmax=1, edgecolors='none', zorder=3)
ax.scatter(jj[dn], ii[dn], c=M0[dn], s=sz(M0)[dn], cmap=cmap_m0,
           vmin=-1, vmax=1, edgecolors='none', zorder=3)
ax.scatter(jj[diag], ii[diag], s=20, c='0.62', edgecolors='none', zorder=4)

# ------------------------------------------------ 底部双水平色标
cax1 = fig.add_axes([0.20, 0.045, 0.30, 0.018])
fig.colorbar(plt.cm.ScalarMappable(plt.Normalize(-1, 1), cmap_m1), cax=cax1,
             orientation='horizontal', ticks=[-1, -0.5, 0, 0.5, 1])
cax1.tick_params(labelsize=7)
cax1.set_title('M1', fontsize=8, fontweight='bold', pad=3)

cax2 = fig.add_axes([0.60, 0.045, 0.30, 0.018])
fig.colorbar(plt.cm.ScalarMappable(plt.Normalize(-1, 1), cmap_m0), cax=cax2,
             orientation='horizontal', ticks=[-1, -0.5, 0, 0.5, 1])
cax2.tick_params(labelsize=7)
cax2.set_title('M0', fontsize=8, fontweight='bold', pad=3)

save(fig, 'case_seg120.png')
