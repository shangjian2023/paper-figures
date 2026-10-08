# -*- coding: utf-8 -*-
"""案例130 (seg128) - Nature 三元气泡图(属水平): 顶点 NPK(上)/Control(左下)/NPKM(右下)。
参考: frames/seg_128.jpg — 细灰三角网格 + 黑色数字 20-100(沿边旋转), 气泡=丰度,
色=属(红 Klebsiella 大泡 + 黑箭头注释, 蓝 Enterobacteriaceae 等), 灰=低丰度/不显著;
下方 'Genus' 三列图例。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *
set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from helpers.ternary import Ternary

H = Ternary.H
A, B, C = np.array([0.5, H]), np.array([0.0, 0.0]), np.array([1.0, 0.0])


def txy(fa, fb, fc):
    s = np.asarray(fa) + np.asarray(fb) + np.asarray(fc)
    fa, fb, fc = np.asarray(fa) / s, np.asarray(fb) / s, np.asarray(fc) / s
    return 0.5 * fa + fc, fa * H


r = rng(128)
fig, ax = plt.subplots(figsize=cm2in(15, 16))
fig.subplots_adjust(left=0.02, right=0.98, top=0.97, bottom=0.22)
ax.set_xlim(-0.36, 1.36)
ax.set_ylim(-0.34, H + 0.14)
ax.set_aspect('equal')
ax.axis('off')

# 细灰网格 + 黑边框
for v in range(10, 100, 10):
    t = v / 100
    ax.plot([B[0] + t * (A[0] - B[0]), C[0] + t * (A[0] - C[0])],
            [B[1] + t * (A[1] - B[1]), C[1] + t * (A[1] - C[1])],
            color='#E0E0E0', lw=0.5, zorder=0.5)
    ax.plot([B[0] + (1 - t) * (A[0] - B[0]), B[0] + (1 - t) * (C[0] - B[0])],
            [B[1] + (1 - t) * (A[1] - B[1]), B[1] + (1 - t) * (C[1] - B[1])],
            color='#E0E0E0', lw=0.5, zorder=0.5)
    ax.plot([(1 - t) * B[0] + t * C[0], (1 - t) * A[0] + t * C[0]],
            [(1 - t) * B[1] + t * C[1], (1 - t) * A[1] + t * C[1]],
            color='#E0E0E0', lw=0.5, zorder=0.5)
for p, q in [(A, B), (B, C), (C, A)]:
    ax.plot([p[0], q[0]], [p[1], q[1]], 'k-', lw=1.0, zorder=3)

# 顶点标签
ax.text(0.5, H + 0.03, 'NPK', ha='center', va='bottom', fontsize=12)
ax.text(-0.24, -0.02, 'Control', ha='right', va='center', fontsize=12)
ax.text(1.24, -0.02, 'NPKM', ha='left', va='center', fontsize=12)

# 黑色数字 20-100 沿边旋转
for v in (20, 40, 60, 80):
    t = v / 100
    ax.text((1 - t) / 2 - 0.035, (1 - t) * H, str(v), rotation=55,
            ha='center', va='center', rotation_mode='anchor', fontsize=9)
    ax.text(1 - t / 2 + 0.035, t * H, str(v), rotation=-55,
            ha='center', va='center', rotation_mode='anchor', fontsize=9)
    ax.text(t, -0.055, str(v), ha='center', va='center', fontsize=9)
ax.text(0.545, H - 0.02, '100', fontsize=9, ha='left', va='center')
ax.text(-0.045, -0.03, '100', fontsize=9, ha='right', va='center', rotation=55,
        rotation_mode='anchor')
ax.text(1.045, -0.03, '100', fontsize=9, ha='left', va='center', rotation=-55,
        rotation_mode='anchor')

# ---------------- 气泡(面积=丰度, 颜色=属)
def bub(comp, size, color, alpha=0.92):
    fa, fb, fc = comp
    ax.scatter(*txy(fa, fb, fc), s=size, color=color, alpha=alpha,
               edgecolor='white', linewidth=0.6, zorder=4)

# 低丰度(深灰) 与 不显著(浅灰) 背景
n0 = 95
fa0 = np.abs(r.normal(0.14, 0.13, n0)) + 0.01
fb0 = r.uniform(0.04, 1.0, n0)
s0 = r.uniform(6, 120, n0)
col0 = np.where(r.uniform(0, 1, n0) < 0.45, '#9E9E9E', '#D9D9D9')
for i in range(n0):
    if fa0[i] + fb0[i] > 0.98:
        continue
    bub((fa0[i], fb0[i], 1 - fa0[i] - fb0[i]), s0[i], col0[i], alpha=0.85)

genus_pts = [
    ('Klebsiella', '#C23B3B', [(0.32, 0.58, 0.10, 2200), (0.20, 0.70, 0.10, 90),
                               (0.42, 0.30, 0.28, 60)]),
    ('Pseudomonas', '#4DAF4C', [(0.68, 0.14, 0.18, 210), (0.75, 0.12, 0.13, 130),
                                (0.55, 0.24, 0.21, 70)]),
    ('Enterobacteriaceae_unclassified', '#3B7DD8', [(0.55, 0.25, 0.20, 1500),
                                                    (0.66, 0.13, 0.21, 100)]),
    ('Rosenbergiella', '#F0B37A', [(0.63, 0.22, 0.15, 240)]),
    ('Oxalobacteraceae_unclassified', '#8E5BA6', [(0.76, 0.13, 0.11, 130),
                                                  (0.08, 0.82, 0.10, 60)]),
    ('Erwinia', '#D07AB8', [(0.72, 0.15, 0.13, 120)]),
    ('Lactococcus', '#5BC8F5', [(0.86, 0.05, 0.09, 90)]),
    ('Sphingobacterium', '#5C6BC0', [(0.92, 0.04, 0.04, 140), (0.06, 0.86, 0.08, 70)]),
]
for _, col, pts in genus_pts:
    for fa, fb, fc, s in pts:
        bub((fa, fb, fc), s, col)

# 黑箭头注释 Klebsiella 大泡 (箭头 + 短标注, 不再悬空)
xb, yb = txy(0.32, 0.58, 0.10)
ax.annotate('', xy=(xb + 0.035, yb + 0.012), xytext=(xb - 0.115, yb + 0.115),
            arrowprops=dict(arrowstyle='-|>', color='black', lw=1.3,
                            shrinkA=0, shrinkB=2), zorder=6)
ax.text(xb - 0.115, yb + 0.13, 'Klebsiella dominant\nunder NPK', fontsize=8,
        ha='center', va='bottom', zorder=6)

# ---------------- 下方 Genus 图例(3 列)
handles, labels = [], []
for name, col, _ in genus_pts:
    handles.append(Line2D([], [], marker='o', ls='', color=col, ms=8))
    labels.append(name)
for name, col in [('Not significant', '#D9D9D9'), ('Low abundance', '#9E9E9E')]:
    handles.append(Line2D([], [], marker='o', ls='', color=col, ms=8))
    labels.append(name)
leg = fig.legend(handles, labels, title='Genus', loc='lower left',
                 bbox_to_anchor=(0.02, 0.0), ncol=3, frameon=False, fontsize=9,
                 title_fontsize=10, columnspacing=1.6, labelspacing=0.9,
                 handletextpad=0.3)
# 气泡大小编码说明 (置于图例正上方)
ax.annotate('Bubble area $\\propto$ mean abundance', xy=(0.0, 1.06), xycoords=leg,
            ha='left', va='bottom', fontsize=8.5, fontstyle='italic',
            annotation_clip=False)

save(fig, 'case_seg128.png')
