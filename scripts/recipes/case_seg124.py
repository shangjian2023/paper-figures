# -*- coding: utf-8 -*-
"""案例126 (seg124) - Cell 三元图: 上 1 大 + 下排 3 小。
参考: frames/seg_124.jpg — 顶点 TE(上)/EPI(左下)/PrE(右下), 彩色虚线网格 20-80,
三边彩箭头(EPI.score.norm/TE.score.norm/PrE.score.norm), 散点按归属橙/绿/蓝着色;
下排 ESCs 0h(蓝)/iEFCs 60h(紫散)/36h post iEFCs(三簇)。
散点坐标用与 helpers.ternary.Ternary.setup() 框架一致的重心变换。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *
set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.lines import Line2D
from helpers.ternary import Ternary

NAVY, DRED, GREEN = '#1F3A93', '#8B1A1A', '#1E7B34'
H = Ternary.H
A, B, C = np.array([0.5, H]), np.array([0.0, 0.0]), np.array([1.0, 0.0])


def txy(fa, fb, fc):
    """与 setup() 框架一致的重心坐标: 顶点 A(上) B(左下) C(右下)。"""
    s = np.asarray(fa) + np.asarray(fb) + np.asarray(fc)
    fa, fb, fc = np.asarray(fa) / s, np.asarray(fb) / s, np.asarray(fc) / s
    return 0.5 * fa + fc, fa * H


def tscatter(ax, fa, fb, fc, **kw):
    x, y = txy(fa, fb, fc)
    return ax.scatter(x, y, **kw)


def draw_tern(ax, fs=8, minor=True, arrows=True):
    """彩色边框三元框架: 灰细网格 + 三向 dash-dot 主网格 + 旋转刻度 + 边箭头。"""
    ax.set_xlim(-0.16, 1.16)
    ax.set_ylim(-0.14, H + 0.14)
    ax.set_aspect('equal')
    ax.axis('off')

    def seg(p0, p1, color, ls, lw, z=1):
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=color, ls=ls, lw=lw, zorder=z)

    if minor:
        for v in range(10, 100, 10):
            t = v / 100
            seg(B + t * (A - B), C + t * (A - C), '#E0E0E0', '-', 0.4, 0.5)   # fA
            seg(B + (1 - t) * (A - B), B + (1 - t) * (C - B), '#E0E0E0', '-', 0.4, 0.5)  # fB
            seg((1 - t) * B + t * C, (1 - t) * A + t * C, '#E0E0E0', '-', 0.4, 0.5)      # fC
    dash = (0, (5, 2, 1, 2))
    for v in (20, 40, 60, 80):
        t = v / 100
        seg(B + t * (A - B), C + t * (A - C), DRED, dash, 0.9)                # fA 横线
        seg(B + (1 - t) * (A - B), B + (1 - t) * (C - B), NAVY, dash, 0.9)    # fB
        seg((1 - t) * B + t * C, (1 - t) * A + t * C, GREEN, dash, 0.9)       # fC
    # 边框: 左EPI藏青 / 底PrE绿 / 右TE深红
    seg(A, B, NAVY, '-', 1.3, 3)
    seg(B, C, GREEN, '-', 1.3, 3)
    seg(C, A, DRED, '-', 1.3, 3)
    # 顶点标签与 100
    ax.text(0.5, H + 0.045, 'TE', ha='center', va='bottom', fontsize=fs + 2,
            fontweight='bold', color='black')
    ax.text(-0.02, -0.06, 'EPI', ha='right', va='top', fontsize=fs + 2,
            fontweight='bold', color=NAVY)
    ax.text(1.02, -0.06, 'PrE', ha='left', va='top', fontsize=fs + 2,
            fontweight='bold', color=GREEN)
    ax.text(0.555, H - 0.01, '100', color=DRED, fontsize=fs - 1, ha='left', va='center')
    ax.text(-0.045, 0.0, '100', color=NAVY, fontsize=fs - 1, ha='right', va='center')
    ax.text(1.045, 0.0, '100', color=GREEN, fontsize=fs - 1, ha='left', va='center')
    # 旋转刻度数字
    for v in (20, 40, 60, 80):
        t = v / 100
        ax.text((1 - t) / 2 - 0.035, (1 - t) * H + 0.01, str(v), color=NAVY,
                fontsize=fs - 1.5, rotation=60, ha='center', va='center',
                rotation_mode='anchor')
        ax.text(1 - t / 2 + 0.035, t * H + 0.01, str(v), color=DRED,
                fontsize=fs - 1.5, rotation=-60, ha='center', va='center',
                rotation_mode='anchor')
        ax.text(t, -0.048, str(v), color=GREEN, fontsize=fs - 1.5,
                ha='center', va='center')
    if arrows:
        cen = np.array([0.5, H / 3])

        def edge_arrow(p0, p1, color, label):
            d = p1 - p0
            s, e = p0 + 0.12 * d, p0 + 0.42 * d
            ax.add_patch(FancyArrowPatch(s, e, arrowstyle='-|>', mutation_scale=11,
                                         color=color, lw=1.3, zorder=4))
            u = d / np.linalg.norm(d)
            ang = np.degrees(np.arctan2(u[1], u[0]))
            if ang > 90 or ang < -90:
                ang += 180
            nrm = np.array([-u[1], u[0]])
            if np.dot(nrm, (s + e) / 2 - cen) < 0:
                nrm = -nrm
            mid = (s + e) / 2 + nrm * 0.065
            ax.text(mid[0], mid[1], label, color=color, fontsize=fs - 0.5,
                    rotation=ang, ha='center', va='center', rotation_mode='anchor')

        edge_arrow(A, B, NAVY, 'EPI.score.norm')
        edge_arrow(C, A, DRED, 'TE.score.norm')
        edge_arrow(B, C, GREEN, 'PrE.score.norm')


def cluster(r, n, mean, sd):
    fa = r.normal(mean[0], sd[0], n * 3)
    fb = r.normal(mean[1], sd[1], n * 3)
    fc = 1 - fa - fb
    ok = (fa > 0.03) & (fb > 0.03) & (fc > 0.03)
    fa, fb, fc = fa[ok], fb[ok], fc[ok]
    k = min(n, len(fa))
    return fa[:k], fb[:k], fc[:k]


r = rng(124)
fig = plt.figure(figsize=cm2in(17, 18))
gs = fig.add_gridspec(2, 3, height_ratios=[2.05, 1], hspace=0.32, wspace=0.20,
                      left=0.03, right=0.97, top=0.96, bottom=0.03)
ax_big = fig.add_subplot(gs[0, :])

groups_big = [(cluster(r, 160, (0.55, 0.30), (0.10, 0.08)), '#E8823A'),
              (cluster(r, 140, (0.35, 0.22), (0.08, 0.10)), '#3A9D3A'),
              (cluster(r, 150, (0.78, 0.15), (0.07, 0.06)), '#2E6DA4')]
draw_tern(ax_big, fs=9)
for (fa, fb, fc), col in groups_big:
    tscatter(ax_big, fa, fb, fc, s=9, color=col, alpha=0.85, linewidths=0, zorder=3)

# ---------------- 主图图例: 三团颜色的 stage 语义, 放左下三角外空白 ----------------
leg_handles = [
    Line2D([], [], marker='o', ls='none', mfc='#2E6DA4', mec='#2E6DA4', ms=5,
           label='ESC-like'),
    Line2D([], [], marker='o', ls='none', mfc='#E8823A', mec='#E8823A', ms=5,
           label='EPI-like'),
    Line2D([], [], marker='o', ls='none', mfc='#3A9D3A', mec='#3A9D3A', ms=5,
           label='PrE-like'),
]
ax_big.legend(handles=leg_handles, loc='center left',
              bbox_to_anchor=(0.0, 0.30), frameon=False, fontsize=8,
              handlelength=1.0, handletextpad=0.4, borderaxespad=0,
              labelspacing=0.45, title='Stage', title_fontsize=8)

panels = [('ESCs\n0 h', [(cluster(r, 180, (0.88, 0.08), (0.045, 0.05)), '#2E6DA4')]),
          ('iEFCs\n60 h', [(cluster(r, 90, (0.45, 0.35), (0.15, 0.14)), '#BA55D3'),
                           (cluster(r, 90, (0.25, 0.45), (0.12, 0.12)), '#BA55D3')]),
          ('36 h post iEFCs', [(cluster(r, 70, (0.60, 0.28), (0.09, 0.08)), '#E8823A'),
                               (cluster(r, 60, (0.35, 0.18), (0.08, 0.10)), '#3A9D3A'),
                               (cluster(r, 60, (0.80, 0.12), (0.06, 0.05)), '#2E6DA4')])]
for k, (title, groups) in enumerate(panels):
    ax = fig.add_subplot(gs[1, k])
    draw_tern(ax, fs=6, arrows=False)
    for (fa, fb, fc), col in groups:
        tscatter(ax, fa, fb, fc, s=4, color=col, alpha=0.85, linewidths=0, zorder=3)
    ax.set_title(title, fontsize=9, pad=16)

save(fig, 'case_seg124.png')
