# -*- coding: utf-8 -*-
"""案例129 (seg127) - PNAS 三元气泡图: 顶点 Nodule(上)/Root(左下)/Rhizosphere(右下)。
参考: frames/seg_127.jpg — 黑细三角 + 浅灰网格(无数字), 气泡面积=丰度,
颜色=富集生境: 红 Nodule / 橙 Rhizosphere / 绿 Root, 未富集灰;
右上 'Enriched OTUs' 方块图例, 顶点标计数。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *
set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, PathPatch
from matplotlib.path import Path as TPath
from helpers.ternary import Ternary

H = Ternary.H


def txy(fa, fb, fc):
    s = np.asarray(fa) + np.asarray(fb) + np.asarray(fc)
    fa, fb, fc = np.asarray(fa) / s, np.asarray(fb) / s, np.asarray(fc) / s
    return 0.5 * fa + fc, fa * H


r = rng(127)
fig, ax = plt.subplots(figsize=cm2in(14.5, 14))
ax.set_xlim(-0.22, 1.42)
ax.set_ylim(-0.18, H + 0.14)
ax.set_aspect('equal')
ax.axis('off')
A, B, C = np.array([0.5, H]), np.array([0.0, 0.0]), np.array([1.0, 0.0])

# 浅灰网格 + 黑色边框
for v in range(10, 100, 10):
    t = v / 100
    ax.plot([B[0] + t * (A[0] - B[0]), C[0] + t * (A[0] - C[0])],
            [B[1] + t * (A[1] - B[1]), C[1] + t * (A[1] - C[1])],
            color='#E3E3E3', lw=0.5, zorder=0.5)
    ax.plot([B[0] + (1 - t) * (A[0] - B[0]), B[0] + (1 - t) * (C[0] - B[0])],
            [B[1] + (1 - t) * (A[1] - B[1]), B[1] + (1 - t) * (C[1] - B[1])],
            color='#E3E3E3', lw=0.5, zorder=0.5)
    ax.plot([(1 - t) * B[0] + t * C[0], (1 - t) * A[0] + t * C[0]],
            [(1 - t) * B[1] + t * C[1], (1 - t) * A[1] + t * C[1]],
            color='#E3E3E3', lw=0.5, zorder=0.5)
for p, q in [(A, B), (B, C), (C, A)]:
    ax.plot([p[0], q[0]], [p[1], q[1]], 'k-', lw=1.1, zorder=3)

# 顶点标签(含计数)
ax.text(0.5, H + 0.035, 'Nodule  (12)', ha='center', va='bottom', fontsize=11)
ax.text(-0.03, -0.07, 'Root\n(40)', ha='right', va='top', fontsize=11)
ax.text(1.03, -0.07, 'Rhizosphere\n(13)', ha='left', va='top', fontsize=11)

# ---------------- 气泡: 面积=丰度 (全部限制在三角形内, 保证轮廓封闭)
tri_clip = PathPatch(TPath([(0.5, H), (0.0, 0.0), (1.0, 0.0), (0.5, H)]),
                     transform=ax.transData, fc='none', ec='none')
ax.add_patch(tri_clip)

PT2DATA = 0.00515                      # pt → 数据坐标半径 (校准原 scatter 尺寸)
GX, GY = 0.5, H / 3.0                  # 内心


def dist_in(x, y):
    """到三条边的最小距离(内切裕量): 左 AB / 右 AC / 底 BC。"""
    dL = H * x - 0.5 * y
    dR = H * (1 - x) - 0.5 * y
    return np.minimum(np.minimum(dL, dR), y)


def bubbles(fa, fb, fc, sizes, color, alpha=0.85):
    x, y = txy(fa, fb, fc)
    x = np.atleast_1d(np.asarray(x, float))
    y = np.atleast_1d(np.asarray(y, float))
    rad = PT2DATA * np.sqrt(np.atleast_1d(np.asarray(sizes, float)) / np.pi)
    # 越界气泡: 圆心沿指向内心方向内收至恰好内切 (凹性保证收后 d>=r)
    d0 = dist_in(x, y)
    den = H / 3.0 - d0
    t = np.where(den > 1e-9, (rad - d0) / np.maximum(den, 1e-9), 0.0)
    t = np.clip(t, 0.0, 1.0)
    x = x + t * (GX - x)
    y = y + t * (GY - y)
    rad = np.minimum(rad, dist_in(x, y))       # 保险截断
    for xi, yi, ri in zip(x, y, rad):
        c = Circle((xi, yi), ri, facecolor=color, alpha=alpha,
                   edgecolor='white', linewidth=0.5, zorder=4)
        c.set_clip_path(tri_clip)
        ax.add_patch(c)

# 未富集(灰): 底部偏置散布
n0 = 230
fa0 = np.abs(r.normal(0.10, 0.09, n0)) + 0.01
fb0 = r.uniform(0.05, 1.0, n0)
s0 = r.uniform(6, 130, n0)
bubbles(fa0, fb0, 1 - fa0 - fb0, s0, '#BDBDBD', alpha=0.8)

# Nodule 富集(红): 顶部垂直带, 含一个大气泡
fa1 = np.append(r.uniform(0.52, 0.90, 13), 0.62)
fb1 = np.append(r.uniform(0.10, 0.40, 13), 0.18)
s1 = np.append(r.uniform(15, 130, 13), 1500)
bubbles(fa1, fb1, 1 - fa1 - fb1, s1, '#C23B3B')

# Root 富集(绿): 左下簇
fa2 = r.uniform(0.04, 0.22, 26)
fb2 = r.uniform(0.30, 0.62, 26)
s2 = r.uniform(30, 420, 26)
bubbles(fa2, fb2, 1 - fa2 - fb2, s2, '#3AA76D')

# Rhizosphere 富集(橙): 右下少数
fa3 = r.uniform(0.03, 0.14, 9)
fc3 = r.uniform(0.55, 0.85, 9)
s3 = r.uniform(15, 110, 9)
bubbles(fa3, 1 - fa3 - fc3, fc3, s3, '#E8892B')

# 图例: Enriched OTUs + 未富集灰类目
handles = [Line2D([], [], marker='s', ls='', color=c, ms=9, label=l)
           for c, l in [('#C23B3B', 'Nodule'), ('#E8892B', 'Rhizosphere'),
                        ('#3AA76D', 'Root'), ('#BDBDBD', 'Not enriched')]]
leg = ax.legend(handles=handles, title='Enriched OTUs', loc='upper left',
                bbox_to_anchor=(0.80, 1.00), frameon=False, fontsize=10,
                title_fontsize=11, labelspacing=0.7, handletextpad=0.4)
ax.annotate('Bubble area $\\propto$ abundance', xy=(0.0, -0.10), xycoords=leg,
            ha='left', va='top', fontsize=8.5, fontstyle='italic',
            annotation_clip=False)

save(fig, 'case_seg127.png')
