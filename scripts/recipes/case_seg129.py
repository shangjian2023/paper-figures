# -*- coding: utf-8 -*-
"""案例131 (seg129) - Nature 三元核密度图。
参考: frames/seg_129.jpg — 黑细三角 + 紫白渐变 KDE 等高线叠加灰细散点,
虚线中线, 三支彩箭头(绿 ISC/TA 左向下 / 蓝 Diff. int. 右向上 / 红 Non-canonical 底向右),
顶点 0 / 1.0 标注, 右上 'Probability' 横向紫色色标。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *
set_style()

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import FancyArrowPatch
from scipy.stats import gaussian_kde
from helpers.ternary import Ternary

GREEN, TEAL, CRIMSON = '#1E7B34', '#1F7A8C', '#C0133B'
H = Ternary.H
A, B, C = np.array([0.5, H]), np.array([0.0, 0.0]), np.array([1.0, 0.0])


def txy(fa, fb, fc):
    s = np.asarray(fa) + np.asarray(fb) + np.asarray(fc)
    fa, fb, fc = np.asarray(fa) / s, np.asarray(fb) / s, np.asarray(fc) / s
    return 0.5 * fa + fc, fa * H


r = rng(129)
n = 420
comp = np.vstack([
    np.column_stack([r.normal(0.44, 0.075, 260), r.normal(0.32, 0.075, 260)]),
    np.column_stack([r.normal(0.06, 0.030, 100), r.normal(0.86, 0.045, 100)]),
    np.column_stack([r.normal(0.62, 0.10, 60), r.normal(0.19, 0.07, 60)]),
])
fa, fb = comp[:, 0], comp[:, 1]
fc = 1 - fa - fb
ok = (fa > 0.005) & (fb > 0.005) & (fc > 0.005)
fa, fb, fc = fa[ok], fb[ok], fc[ok]
x, y = txy(fa, fb, fc)

fig, ax = plt.subplots(figsize=cm2in(15, 14))
fig.subplots_adjust(left=0.02, right=0.98, top=0.97, bottom=0.03)
ax.set_xlim(-0.30, 1.30)
ax.set_ylim(-0.30, H + 0.24)
ax.set_aspect('equal')
ax.axis('off')

# 三元 KDE: 在直角坐标上做 gaussian_kde, 仅填充三角形内部
kde = gaussian_kde(np.vstack([x, y]))
xg, yg = np.meshgrid(np.linspace(-0.02, 1.02, 220), np.linspace(-0.02, H + 0.02, 220))
Z = kde(np.vstack([xg.ravel(), yg.ravel()])).reshape(xg.shape)
tri_out = (yg < 0) | (xg < yg / (2 * H)) | (xg > 1 - yg / (2 * H))
Zm = np.ma.masked_where(tri_out | (Z < 0.035 * Z.max()), Z)
ax.contourf(xg, yg, Zm, levels=12, cmap='Purples', zorder=1)
ax.contour(xg, yg, Zm, levels=6, colors='#7B6BA8', linewidths=0.4,
           alpha=0.5, zorder=1.5)

# 灰细散点
ax.scatter(x, y, s=2.6, color='#7A7A7A', alpha=0.55, linewidths=0, zorder=2)

# 虚线中线(1/3 与 2/3)
dash = (0, (5, 4))
for t in (1 / 3, 2 / 3):
    ax.plot([B[0] + t * (A[0] - B[0]), C[0] + t * (A[0] - C[0])],
            [B[1] + t * (A[1] - B[1]), C[1] + t * (A[1] - C[1])],
            color='#9A9A9A', ls=dash, lw=0.7, zorder=1.6)
    ax.plot([B[0] + (1 - t) * (A[0] - B[0]), B[0] + (1 - t) * (C[0] - B[0])],
            [B[1] + (1 - t) * (A[1] - B[1]), B[1] + (1 - t) * (C[1] - B[1])],
            color='#9A9A9A', ls=dash, lw=0.7, zorder=1.6)
    ax.plot([(1 - t) * B[0] + t * C[0], (1 - t) * A[0] + t * C[0]],
            [(1 - t) * B[1] + t * C[1], (1 - t) * A[1] + t * C[1]],
            color='#9A9A9A', ls=dash, lw=0.7, zorder=1.6)

# 黑边框 + 角端刻度短线与 0 / 1.0 标注
for p, q in [(A, B), (B, C), (C, A)]:
    ax.plot([p[0], q[0]], [p[1], q[1]], 'k-', lw=1.4, zorder=3)
for v, rot, dx, dy in [(A, -20, 0.03, 0.02), (B, 55, -0.04, -0.02),
                       (C, -55, 0.04, -0.02)]:
    ax.plot([v[0] - 0.035 * np.sin(np.radians(rot)), v[0] + 0.035 * np.sin(np.radians(rot))],
            [v[1] - 0.035 * np.cos(np.radians(rot)), v[1] + 0.035 * np.cos(np.radians(rot))],
            'k-', lw=1.2, zorder=3)
ax.text(0.44, H + 0.055, '0', fontsize=13, ha='center', va='bottom')
ax.text(0.60, H - 0.015, '1.0', fontsize=13, ha='left', va='center')
ax.text(-0.075, H * 0.16, '1.0', fontsize=13, ha='right', va='center')
ax.text(-0.045, -0.10, '0', fontsize=13, ha='right', va='center')
ax.text(1.075, -0.055, '0', fontsize=13, ha='left', va='center')
ax.text(1.02, -0.13, '1.0', fontsize=13, ha='left', va='center')

# 三支彩箭头 + 状态名
cen = np.array([0.5, H / 3])

def edge_arrow(p0, p1, color, label, gap=0.10):
    d = p1 - p0
    s, e = p0 + 0.08 * d, p0 + 0.52 * d
    ax.add_patch(FancyArrowPatch(s, e, arrowstyle='-|>', mutation_scale=14,
                                 color=color, lw=1.6, zorder=4))
    u = d / np.linalg.norm(d)
    ang = np.degrees(np.arctan2(u[1], u[0]))
    if ang > 90 or ang < -90:
        ang += 180
    nrm = np.array([-u[1], u[0]])
    if np.dot(nrm, (s + e) / 2 - cen) < 0:
        nrm = -nrm
    mid = (s + e) / 2 + nrm * gap
    ax.text(mid[0], mid[1], label, color=color, fontsize=12,
            rotation=ang, ha='center', va='center', rotation_mode='anchor')

edge_arrow(A, B, GREEN, 'ISC/TA')
edge_arrow(C, A, TEAL, 'Diff. int.')
ax.add_patch(FancyArrowPatch((0.30, -0.20), (0.70, -0.20), arrowstyle='-|>',
                             mutation_scale=14, color=CRIMSON, lw=1.6, zorder=4))
ax.text(0.50, -0.27, 'Non-canonical', color=CRIMSON, fontsize=13,
        ha='center', va='center')

# ---------------- 右上 Probability 横向色标
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
cax = fig.add_axes([0.73, 0.955, 0.17, 0.022])
cax.imshow(np.linspace(0, 1, 256).reshape(1, -1), aspect='auto',
           cmap='Purples', extent=[0, 1, 0, 1])
cax.set_xticks([]); cax.set_yticks([])
for sp in cax.spines.values():
    sp.set_visible(False)
fig.text(0.725, 0.985, 'Probability', fontsize=11, ha='left', va='bottom')
fig.text(0.725, 0.915, '0', fontsize=9, ha='left', va='top')
fig.text(0.90, 0.915, '1.0', fontsize=9, ha='right', va='top')

save(fig, 'case_seg129.png')
