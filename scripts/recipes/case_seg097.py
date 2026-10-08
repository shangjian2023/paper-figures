# -*- coding: utf-8 -*-
"""案例99 - Nature 相关性矩阵点图(二): WGD-low / WGD-high 双面板。
参考: frames/seg_097.jpg — 签名×6 CNV事件, 圆大小=-log10P, 色=Spearman rho,
圆内*号, 行按模块分框, 右侧 -log10P 尺寸图例 + rho 色标。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

set_style()

modules = [
    ['ISG', u'IFN\u03b3 (B)', 'Inflam.', 'CIN'],
    ['STING1'],
    [u'IFN\u03b3 (H)', u'IFN\u03b1', 'Protein Secretion', 'Inflam. Resp.',
     u'TNF\u03b1 via NFKB', 'Apoptosis', 'Complement'],
    ['Interferon MHC II (1)', 'Interferon MHC II (2)'],
    [u'MHC\u2013I', u'MHC\u2013II'],
]
events = ['Chrom. Gain', 'Chrom. Loss', 'Arm Gain', 'Arm Loss',
          'Segment Gain', 'Segment Loss']
nE = len(events)
# 行坐标: 模块间留 0.8 间隔, 模块间加空行便于画框
ypos, ylab, blocks = [], [], []
y = 0.0
for mod in modules:
    y += 1.0
    start = y
    for name in mod:
        ypos.append(y)
        ylab.append(name)
        y += 1.0
    blocks.append((start, y - 1.0))
    y += 0.8
nR = len(ypos)
ypos = np.array(ypos)

r = rng(97)
def make_data(mean, strong, seed_shift):
    rr = rng(97 + seed_shift)
    rho = rr.normal(mean, 0.28, (nR, nE)).clip(-0.62, 0.62)
    for _ in range(strong):
        rho[rr.integers(0, nR), rr.integers(2, nE)] = rr.uniform(0.42, 0.6) * rr.choice([-1, 1])
    nlogp = rr.exponential(0.85, (nR, nE)).clip(0.05, 3.3)
    return rho, nlogp

rho_L, p_L = make_data(0.18, 16, 1)     # WGD-low: 偏正相关
rho_H, p_H = make_data(-0.15, 6, 2)     # WGD-high: 偏负相关

norm = TwoSlopeNorm(vmin=-0.55, vcenter=0.0, vmax=0.55)
cmap = plt.get_cmap('RdBu_r')
def psize(nlp):
    return 12 + nlp * 52

fig = plt.figure(figsize=cm2in(17.5, 17.0))
axes = []
for k, (ttl, rho, nlp) in enumerate([('WGD-low', rho_L, p_L),
                                     ('WGD-high', rho_H, p_H)]):
    ax = fig.add_axes([0.215 + k * 0.325, 0.13, 0.27, 0.74])
    axes.append(ax)
    ax.set_xlim(-0.5, nE - 0.5)
    ax.set_ylim(ypos.max() + 0.7, ypos.min() - 0.7)
    ax.set_xticks(np.arange(nE))
    ax.set_yticks(ypos)
    ax.set_xticklabels(events, rotation=35, ha='right', fontsize=7.5)
    if k == 0:
        ax.set_yticklabels(ylab, fontsize=7.5)
    else:
        ax.set_yticklabels([])
    ax.set_title(ttl, fontsize=9.5, pad=4)
    ax.tick_params(length=2, color='0.7')
    for s in ax.spines.values():
        s.set_color('0.4')
    # 浅灰网格
    for gx in range(nE):
        ax.axvline(gx, color='0.88', lw=0.6, zorder=0)
    for gy in ypos:
        ax.axhline(gy, color='0.88', lw=0.6, zorder=0)
    # 模块分框
    for (y0, y1) in blocks:
        ax.add_patch(plt.Rectangle((-0.5, y0 - 0.5), nE, y1 - y0 + 1.0,
                                   fill=False, edgecolor='black', lw=0.9, zorder=2))
    # 点
    for i in range(nR):
        for j in range(nE):
            ax.scatter(j, ypos[i], s=psize(nlp[i, j]),
                       facecolor=cmap(norm(rho[i, j])), edgecolor='black',
                       linewidth=0.5, zorder=3)
            if nlp[i, j] > 1.3:
                ax.text(j, ypos[i], '*', ha='center', va='center',
                        fontsize=7.5, fontweight='bold', zorder=4)

# ------------------------------------------------ 右侧图例
lx = fig.add_axes([0.845, 0.60, 0.14, 0.22])
lx.set_xlim(0, 1); lx.set_ylim(0, 1)
lx.set_xticks([]); lx.set_yticks([])
for s in lx.spines.values():
    s.set_visible(False)
lx.text(0.42, 1.02, u'$-\\log_{10}\\,\\mathrm{P}$', fontsize=9, ha='center')
for k, v in enumerate([1, 2, 3]):
    yy = 0.72 - k * 0.30
    lx.scatter(0.42, yy, s=psize(v) * 1.15, facecolor='black', clip_on=False)
    lx.text(0.72, yy, str(v), fontsize=8, va='center')

cax = fig.add_axes([0.875, 0.22, 0.05, 0.26])
sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
cb = fig.colorbar(sm, cax=cax, ticks=[-0.5, 0.0, 0.5])
cax.tick_params(labelsize=7.5)
cax.set_title(u"Spearman's \u03c1", fontsize=9, loc='center', pad=8)

save(fig, 'case_seg097.png')
