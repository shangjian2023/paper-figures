# -*- coding: utf-8 -*-
"""案例32 - Nature 山脊图 + 侧边条形图。
参考 frames/seg_032.jpg: 左 20 个属的水平山脊 KDE, 填色按 β1 正负红/紫渐变;
右侧对齐水平条形 (深红 = 正 MAG 数, 紫蓝 = 负 MAG 数),
x 轴 β1(MAG) 与 Number of MAGs。"""
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

set_style()
r = rng(32)

# (属名, [(峰位, sd, 相对权重), ...], n_pos, n_neg) 峰位符号决定红/紫
GEN = [
    ('Blautia A',            [(0.026, 0.008, 1.0), (0.052, 0.005, 0.25)], 10, 0),
    ('Agathobacter',         [(0.014, 0.006, 1.0)], 8, 0),
    ('Faecalibacterium',     [(0.011, 0.005, 1.0)], 7, 0),
    ('Prevotella',           [(0.008, 0.007, 1.0), (-0.030, 0.005, 0.22)], 6, 1),
    ('Roseburia',            [(0.012, 0.008, 1.0), (-0.026, 0.005, 0.25)], 6, 1),
    ('Lachnospira',          [(0.010, 0.008, 1.0)], 5, 0),
    ('Gemmiger',             [(0.002, 0.007, 1.0), (0.030, 0.006, 0.45)], 5, 0),
    ('Anaerobutyricum',      [(0.009, 0.005, 1.0), (0.028, 0.005, 0.40)], 4, 0),
    ('Dorea',                [(0.002, 0.005, 1.0), (-0.022, 0.005, 0.30)], 2, 0),
    ('Parolsenella',         [(-0.038, 0.010, 1.0), (0.020, 0.007, 0.25)], 1, 5),
    ('Agathobaculum',        [(-0.045, 0.012, 1.0), (0.024, 0.005, 0.18)], 1, 7),
    ('Bifidobacterium',      [(-0.032, 0.011, 1.0), (0.018, 0.005, 0.15)], 1, 13),
    ('Bilophila',            [(-0.038, 0.010, 1.0)], 0, 3),
    ('Escherichia',          [(-0.022, 0.008, 1.0)], 0, 3),
    ('Ligilactobacillus',    [(-0.014, 0.007, 1.0)], 0, 3),
    ('Megamonas',            [(-0.016, 0.008, 1.0)], 0, 4),
    ('Limosilactobacillus',  [(-0.026, 0.009, 1.0)], 0, 5),
    ('Parabacteroides',      [(-0.024, 0.010, 1.0)], 0, 8),
    ('Bacteroides',          [(-0.042, 0.012, 1.0)], 0, 20),
    ('Streptococcus',        [(-0.024, 0.010, 1.0)], 0, 12),
]


def grad_fill(ax, x, y, base, color, zorder):
    """基线→曲线的纵向渐变填充(阈值逐层叠加, 越高越深)。"""
    ymax = y.max()
    for kk in range(1, 9):
        thr = ymax * kk / 9.0
        ax.fill_between(x, base, base + y, where=(y > thr), color=color,
                        alpha=0.10 + 0.105 * kk, lw=0, zorder=zorder)


fig = plt.figure(figsize=cm2in(13, 17))
gs = fig.add_gridspec(1, 2, width_ratios=[2.7, 1.0], wspace=0.045,
                      left=0.265, right=0.965, top=0.962, bottom=0.062)
axL = fig.add_subplot(gs[0, 0])
axR = fig.add_subplot(gs[0, 1])

x = np.linspace(-0.070, 0.070, 500)
nrow = len(GEN)
offs = -np.arange(nrow).astype(float)
names = []
for row, (name, comps, npos, nneg) in enumerate(GEN):
    names.append(name)
    off = offs[row]
    z = nrow - row
    for pk, sd, w in comps:
        v = r.normal(pk, sd, 3500)
        k = gaussian_kde(v)(x)
        k /= k.max()
        h = 0.85 * w * k
        color = '#b05252' if pk > 0 else '#7a70c4'   # β1 正红 / 负紫
        grad_fill(axL, x, h, off, color, z)
        axL.plot(x, off + h, color=color, lw=0.7, zorder=z)
    axL.plot(x, np.full_like(x, off), color='#222222', lw=0.7, zorder=z)
    axR.barh(off, npos, height=0.78, color='#9e3d3d', ec='black', lw=0.6,
             zorder=3)
    axR.barh(off, -nneg, height=0.78, color='#7f76c8', ec='black', lw=0.6,
             zorder=3)

axL.set_xlim(-0.070, 0.070)
axL.set_ylim(-nrow + 0.8, 1.35)
axL.set_xticks([-0.03, 0, 0.03, 0.06])
axL.set_xlabel(r'$\beta_1$(MAG)', fontsize=9)
axL.set_yticks(offs)
axL.set_yticklabels(names, fontsize=7.5)
for lbl in axL.get_yticklabels():
    lbl.set_fontstyle('italic')
despine(axL, left=True)   # 保留左 spine: 表头横线与纵轴相接成"门"形, 而非残枝
axL.tick_params(labelsize=7)

# 属名表头 'Genus' + 上划线(覆盖标签列, 右端与纵轴顶相接)
trL = axL.transAxes
axL.text(-0.245, 1.018, 'Genus', transform=trL, ha='center', fontsize=9,
         clip_on=False)
axL.plot([-0.48, 0.0], [1.005, 1.005], transform=trL, clip_on=False,
         color='black', lw=0.8)

axR.set_xlim(-21, 12)
axR.set_ylim(-nrow + 0.8, 1.35)
axR.set_xticks([-20, -15, -10, -5, 0, 5, 10])
axR.set_xticklabels(['20', '15', '10', '5', '0', '5', '10'])
axR.set_xlabel('Number of MAGs', fontsize=9)
axR.set_yticks([])
axR.axvline(0, color='black', lw=0.8)
despine(axR)
axR.tick_params(labelsize=7)

save(fig, 'case_seg032.png')
