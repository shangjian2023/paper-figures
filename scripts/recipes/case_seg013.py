# -*- coding: utf-8 -*-
"""案例13 - Nature 环形系统发育树圈图(二)。
参考: frames/seg_013.jpg — 黑色环形树 + 4环境扇形底色 + 外侧红蓝柱状环 + presence灰白热图环 + 放射刻度0-0.6。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'helpers'))
from paper_style import *
set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from newick import random_newick, parse_newick

SEED, N = 13, 150

# ---------------------------------------------------------------- 树 + 每叶数据
tree = parse_newick(random_newick(N, seed=SEED))

def leaves_of(nd):
    if not nd['children']:
        return [nd['name']]
    out = []
    for c in nd['children']:
        out += leaves_of(c)
    return out

order = leaves_of(tree)
r13 = rng(SEED)
abu = r13.beta(1.4, 3.2, N) * 0.6                       # 丰度 0-0.6
presence = r13.random(N) < 0.38
bar_col = ['#C0392B' if a > 0.30 else '#2C5F8A' for a in abu]

# 4 环境 = 4 个 90° 扇区(沿叶序)
ENVS = ['Marine', 'Terrestrial', 'Freshwater', 'Ice-Snow']
SEC_COL = ['#E7EFF7', '#EFF4E2', '#F9E7E2', '#ECEAF3']

# ---------------------------------------------------------------- 黑色环形树
R0, R1 = 0.07, 0.55
ang = {nm: 2 * np.pi * (j + 0.5) / N for j, nm in enumerate(order)}
nleaf = {}

def cnt(nd):
    nleaf[id(nd)] = 1 if not nd['children'] else sum(cnt(c) for c in nd['children'])
    return nleaf[id(nd)]
cnt(tree)

def maxd(nd):
    return 0 if not nd['children'] else 1 + max(maxd(c) for c in nd['children'])
TOT = max(maxd(tree), 1)

def rd(d):
    return R0 + (R1 - R0) * d / TOT

def P(th, r):
    return (r * np.cos(th), r * np.sin(th))

SPAN = {id(tree): (0.0, 2 * np.pi, 0)}

fig = plt.figure(figsize=cm2in(17.5, 10.6))
gs = fig.add_gridspec(1, 2, width_ratios=[1.18, 1], wspace=-0.05)
ax = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

# 环境扇形底色
for q in range(4):
    ax.add_patch(Wedge((0, 0), 0.72, q * 90, (q + 1) * 90, width=0.72 - 0.05,
                       facecolor=SEC_COL[q], edgecolor='none', zorder=1))

def walk(nd):
    a0, a1, d = SPAN[id(nd)]
    if nd['children']:
        k = nleaf[id(nd)]; pos = a0
        for ch in nd['children']:
            w = nleaf[id(ch)] / k * (a1 - a0)
            SPAN[id(ch)] = (pos, pos + w, d + 1); pos += w
        mid = 0.5 * (a0 + a1)
        (x0, y0), (x1, y1) = P(mid, rd(d)), P(mid, rd(d + 1))
        ax.plot([x0, x1], [y0, y1], color='black', lw=0.45, zorder=2)
        ax.add_patch(Wedge((0, 0), rd(d + 1), np.degrees(a0), np.degrees(a1),
                           width=max(rd(d + 1) - rd(d), 1e-4), facecolor='none',
                           edgecolor='black', lw=0.45, zorder=2))
        for ch in nd['children']:
            walk(ch)
    else:
        a = ang[nd['name']]
        (x0, y0), (x1, y1) = P(a, rd(d)), P(a, R1)
        ax.plot([x0, x1], [y0, y1], color='black', lw=0.45, zorder=2)

walk(tree)

# ---------------------------------------------------------------- presence 热图环
hw = np.pi / N * 0.96
for j, nm in enumerate(order):
    a = np.degrees(ang[nm])
    ax.add_patch(Wedge((0, 0), 0.72, a - np.degrees(hw), a + np.degrees(hw),
                       width=0.10, facecolor='#3F3F3F' if presence[j] else '#F1F1F1',
                       edgecolor='white', lw=0.2, zorder=2))

# ---------------------------------------------------------------- 外侧红蓝柱状环 + 刻度
RB, SC = 0.745, 0.17 / 0.6
for g in np.arange(4):
    rr = RB + 0.6 * SC * g / 3
    ax.add_patch(Wedge((0, 0), rr + 0.004, 0, 360, width=0.008,
                       facecolor='none', edgecolor='#CCCCCC', lw=0.4, zorder=1))
for j, nm in enumerate(order):
    a = np.degrees(ang[nm])
    L = abu[j] * SC
    ax.add_patch(Wedge((0, 0), RB + L, a - np.degrees(hw) * 0.7,
                       a + np.degrees(hw) * 0.7, width=L,
                       facecolor=bar_col[j], edgecolor='none', zorder=3))
# 径向刻度轴整体放到左下象限(205°): 轴线沿半径方向, 刻度标签交错排在轴两侧
# (同侧相邻间距加倍), 不再相互叠压
AXD = 205
ra = np.radians(AXD)
ux, uy = np.cos(ra), np.sin(ra)
px, py = np.cos(ra + np.pi / 2), np.sin(ra + np.pi / 2)
ax.plot([RB * ux, (RB + 0.6 * SC) * ux], [RB * uy, (RB + 0.6 * SC) * uy],
        lw=0.5, color='#888888', zorder=6)
for i, v in enumerate([0, 0.2, 0.4, 0.6]):
    rr = RB + v * SC
    side = 1 if i % 2 == 0 else -1          # 奇偶交错 -> 相邻标签分居轴两侧
    ax.plot([rr * ux, rr * ux + 0.010 * side * px],
            [rr * uy, rr * uy + 0.010 * side * py],
            lw=0.5, color='#888888', zorder=6)
    ax.text(rr * ux + 0.036 * side * px, rr * uy + 0.036 * side * py, ('%g' % v),
            fontsize=5.5, rotation=AXD - 270, rotation_mode='anchor',
            ha='center', va='center', zorder=7,
            bbox=dict(fc='white', ec='none', pad=0.15))

# 环境放射标签(扇区中线外侧)
for q, nm in enumerate(ENVS):
    deg = q * 90 + 45
    a = np.radians(deg)
    rot = deg - 90 if not (90 < deg % 360 <= 270) else deg + 90
    ax.text(0.945 * np.cos(a), 0.945 * np.sin(a), nm, rotation=rot, fontsize=6,
            ha='center', va='center', color='#444444')

ax.set_xlim(-0.98, 0.98); ax.set_ylim(-0.98, 0.98)
ax.set_aspect('equal'); ax.axis('off')

# ---------------------------------------------------------------- 图例
ax2.set_xlim(0, 1); ax2.set_ylim(0, 1); ax2.axis('off')

def block(y0, title, labels, colors, marker='sq', fs=6.5, dy=0.030):
    ax2.text(0.02, y0, title, fontsize=8, va='top')
    y = y0 - 0.050
    for lab, col in zip(labels, colors):
        if marker == 'sq':
            ax2.add_patch(plt.Rectangle((0.03, y - 0.019), 0.030, 0.025,
                                        facecolor=col, edgecolor='#999999', lw=0.4))
        else:
            ax2.plot([0.045], [y - 0.006], 'o', ms=4.5, color=col)
        ax2.text(0.075, y - 0.006, lab, fontsize=fs, va='center')
        y -= dy
    return y

y = block(0.97, 'Presence (grey ring)', ['No', 'Yes'], ['#F1F1F1', '#3F3F3F'])
# 红/蓝柱状环图例: 按脚本数据语义 (abu>0.30 红 / 否则蓝), 并注明 0-0.6 径向刻度归属
y = block(y - 0.045, 'Relative abundance (bar ring)',
          ['High (> 0.3)', 'Low (≤ 0.3)'], ['#C0392B', '#2C5F8A'])
ax2.text(0.03, y - 0.012, 'bar length = relative abundance, radial scale 0 – 0.6',
         fontsize=5.5, va='top', color='#555555')
PHY = [('Acidobacteriota', '#B49B72'), ('Actinobacteriota', '#E8967A'),
       ('Bacteroidota', '#C00000'), ('Chloroflexi', '#B5E3C8'),
       ('Cyanobacteria', '#17A877'), ('Firmicutes', '#8B5E3C'),
       ('Others', '#BFBFBF'), ('Patescibacteria', '#8C8C8C'),
       ('Planctomycetota', '#4FC3D9'), ('Proteobacteria', '#2E4D7B'),
       ('Verrucomicrobiota', '#7B86C9')]
y = block(y - 0.045, 'Phylum', [p for p, _ in PHY], [c for _, c in PHY])

save(fig, 'case_seg013.png')
