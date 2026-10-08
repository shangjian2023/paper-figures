# -*- coding: utf-8 -*-
"""案例127 (seg125) - Nature 三元图(两组): CD4 TCM / TH1 / TH2 / TH17。
参考: frames/seg_125.jpg — 灰细三角网格 + 三向彩色 dash-dot 主网格, 三边彩箭头
(T_H2 state 藏青向下 / T_H1 state 深红向上 / T_H17 state 绿向右), 青色 Young 与
棕橙 Older 两团散点, 图例右上。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *
set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch
from helpers.ternary import Ternary

NAVY, DRED, GREEN = '#1F3A93', '#8B0000', '#1E7B34'
H = Ternary.H
A, B, C = np.array([0.5, H]), np.array([0.0, 0.0]), np.array([1.0, 0.0])


def txy(fa, fb, fc):
    s = np.asarray(fa) + np.asarray(fb) + np.asarray(fc)
    fa, fb, fc = np.asarray(fa) / s, np.asarray(fb) / s, np.asarray(fc) / s
    return 0.5 * fa + fc, fa * H


def draw_tern_th(ax, fs=9):
    ax.set_xlim(-0.30, 1.30)
    ax.set_ylim(-0.22, H + 0.16)
    ax.set_aspect('equal')
    ax.axis('off')

    def seg(p0, p1, color, ls, lw, z=1):
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=color, ls=ls, lw=lw, zorder=z)

    for v in range(10, 100, 10):
        t = v / 100
        seg(B + t * (A - B), C + t * (A - C), '#DCDCDC', '-', 0.5, 0.5)
        seg(B + (1 - t) * (A - B), B + (1 - t) * (C - B), '#DCDCDC', '-', 0.5, 0.5)
        seg((1 - t) * B + t * C, (1 - t) * A + t * C, '#DCDCDC', '-', 0.5, 0.5)
    dash = (0, (6, 3, 1, 3))
    for v in (20, 40, 60, 80):
        t = v / 100
        seg(B + t * (A - B), C + t * (A - C), DRED, dash, 0.9)
        seg(B + (1 - t) * (A - B), B + (1 - t) * (C - B), NAVY, dash, 0.9)
        seg((1 - t) * B + t * C, (1 - t) * A + t * C, GREEN, dash, 0.9)
    seg(A, B, NAVY, '-', 1.3, 3)
    seg(B, C, GREEN, '-', 1.3, 3)
    seg(C, A, DRED, '-', 1.3, 3)
    # 顶点与 100
    ax.text(0.5, H + 0.05, 'CD4 T$_{CM}$ cell', ha='center', va='bottom',
            fontsize=fs + 1.5, color='black')
    ax.text(0.555, H - 0.01, '100', color=DRED, fontsize=fs - 0.5, ha='left', va='center')
    ax.text(-0.045, 0.0, '100', color=NAVY, fontsize=fs - 0.5, ha='right', va='center')
    ax.text(1.045, 0.0, '100', color=GREEN, fontsize=fs - 0.5, ha='left', va='center')
    for v in (20, 40, 60, 80):
        t = v / 100
        ax.text((1 - t) / 2 - 0.035, (1 - t) * H + 0.01, str(v), color=NAVY,
                fontsize=fs - 1.5, rotation=60, ha='center', va='center',
                rotation_mode='anchor')
        ax.text(1 - t / 2 + 0.035, t * H + 0.01, str(v), color=DRED,
                fontsize=fs - 1.5, rotation=-60, ha='center', va='center',
                rotation_mode='anchor')
        ax.text(t, -0.05, str(v), color=GREEN, fontsize=fs - 1.5,
                ha='center', va='center')
    # 外侧三支箭头 + 状态名
    cen = np.array([0.5, H / 3])

    def edge_arrow(p0, p1, color, label, gap=0.10, frac0=0.10, frac1=0.55):
        d = p1 - p0
        s, e = p0 + frac0 * d, p0 + frac1 * d
        ax.add_patch(FancyArrowPatch(s, e, arrowstyle='-|>', mutation_scale=13,
                                     color=color, lw=1.4, zorder=4))
        u = d / np.linalg.norm(d)
        ang = np.degrees(np.arctan2(u[1], u[0]))
        if ang > 90 or ang < -90:
            ang += 180
        nrm = np.array([-u[1], u[0]])
        if np.dot(nrm, (s + e) / 2 - cen) < 0:
            nrm = -nrm
        mid = (s + e) / 2 + nrm * gap
        ax.text(mid[0], mid[1], label, color=color, fontsize=fs + 1,
                rotation=ang, ha='center', va='center', rotation_mode='anchor')

    edge_arrow(A, B, NAVY, '$T_{H}2$ state')
    edge_arrow(C, A, DRED, '$T_{H}1$ state')
    ax.add_patch(FancyArrowPatch((0.30, -0.13), (0.72, -0.13), arrowstyle='-|>',
                                 mutation_scale=13, color=GREEN, lw=1.4, zorder=4))
    ax.text(0.51, -0.185, '$T_{H}17$ state', color=GREEN, fontsize=fs + 1,
            ha='center', va='center')


def cluster(r, n, mean, sd):
    fa = r.normal(mean[0], sd[0], n * 3)
    fb = r.normal(mean[1], sd[1], n * 3)
    fc = 1 - fa - fb
    ok = (fa > 0.03) & (fb > 0.03) & (fc > 0.03)
    k = min(n, int(ok.sum()))
    return fa[ok][:k], fb[ok][:k], fc[ok][:k]


r = rng(125)
fig, ax = plt.subplots(figsize=cm2in(13.5, 13))
draw_tern_th(ax, fs=9)
fa, fb, fc = cluster(r, 110, (0.22, 0.42), (0.055, 0.075))
ax.scatter(*txy(fa, fb, fc), s=26, color='#1B9E86', alpha=0.9,
           edgecolor='white', linewidth=0.4, zorder=3, label='Young')
fa, fb, fc = cluster(r, 90, (0.20, 0.47), (0.055, 0.085))
ax.scatter(*txy(fa, fb, fc), s=26, color='#B8860B', alpha=0.9,
           edgecolor='white', linewidth=0.4, zorder=3, label='Older')
handles = [Line2D([], [], marker='o', ls='', color=c, ms=7, label=l)
           for c, l in [('#1B9E86', 'Young'), ('#B8860B', 'Older')]]
ax.legend(handles=handles, loc='upper left', bbox_to_anchor=(0.80, 1.02),
          frameon=False, fontsize=10, handletextpad=0.25)

save(fig, 'case_seg125.png')
