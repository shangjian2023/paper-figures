# -*- coding: utf-8 -*-
"""案例35 - Nature 通路富集 circos & 网络图 (双面板)。
参考: frames/seg_035.jpg — i: circos 弧连线(3 细胞类型弧, 灰细线+紫共享带);
j: 富集网络(饼图节点, 点径=P值, 灰边, 通路标签)。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *
set_style()

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib.patches import Arc, Wedge, FancyArrowPatch, Circle
import networkx as nx

r = rng(35)

fig = plt.figure(figsize=cm2in(18.0, 9.6))
axc = fig.add_axes([0.02, 0.16, 0.36, 0.72])          # circos
axn = fig.add_axes([0.40, 0.02, 0.58, 0.92])          # network

# ============================================================ i: circos
axc.set_aspect('equal')
axc.axis('off')
axc.set_xlim(-1.75, 1.75)
axc.set_ylim(-1.9, 1.75)

# 三段弧: Islets(蓝) a_cells(红) b_cells(绿), 各占约 1/3
segs = [(-80, 40, '#2166AC', 'Islets'),        # (起角, 终角, 色)
        (48, 168, '#C0392B', 'alpha cells'),
        (176, 288, '#2E8B57', 'beta cells')]
gene_angles = []
for a0, a1, col, name in segs:
    axc.add_patch(Arc((0, 0), 2.0, 2.0, angle=0, theta1=a0, theta2=a1,
                      color=col, lw=7))
    # 沿弧的基因刻度
    n_g = int(abs(a1 - a0) // 2.4)
    ts = np.linspace(np.radians(a0), np.radians(a1), n_g)
    gene_angles.append(ts)
    for t in ts:
        axc.plot([np.cos(t), np.cos(t) * 1.035], [np.sin(t), np.sin(t) * 1.035],
                 color='k', lw=0.5, alpha=0.8)
# 弧名标签
for a0, a1, col, name in segs:
    tm = np.radians((a0 + a1) / 2)
    axc.text(1.22 * np.cos(tm), 1.22 * np.sin(tm), name, color=col,
             fontsize=8, ha='center', va='center', fontweight='bold')
axc.add_patch(Arc((0, 0), 2.06, 2.06, theta1=0, theta2=360, color='k', lw=0.8))

# 灰细线: 每个基因连到近中心(独特基因)
for ts in gene_angles:
    for t in ts:
        rr = r.uniform(0.10, 0.22)
        axc.plot([np.cos(t), rr * np.cos(t + r.uniform(-0.25, 0.25))],
                 [np.sin(t), rr * np.sin(t + r.uniform(-0.25, 0.25))],
                 color='#B9B9B9', lw=0.35, alpha=0.65, zorder=1)

# 紫色共享带: 弧间宽贝塞尔曲线
pairs = [(8, 15), (18, 25), (28, 35), (38, 45), (48, 52), (58, 62),
         (5, 30), (15, 40), (25, 50), (35, 20), (45, 55), (2, 28)]
t1 = gene_angles[0]
t2 = gene_angles[1]
t3 = gene_angles[2]
for k, (i1, i2) in enumerate(pairs):
    ta = t1[i1 % len(t1)]
    tb = t2[i2 % len(t2)] if k % 2 == 0 else t3[i2 % len(t3)]
    p0 = np.array([np.cos(ta), np.sin(ta)]) * 0.99
    p1 = np.array([np.cos(tb), np.sin(tb)]) * 0.99
    ctrl = (p0 + p1) * 0.5 * r.uniform(0.06, 0.22)
    axc.plot([p0[0], ctrl[0], p1[0]], [p0[1], ctrl[1], p1[1]],
             color='#7B4EA3', lw=2.8, alpha=0.55, solid_capstyle='round', zorder=3)

# 图例文字
axc.text(-1.78, -1.30, 'Genes arranged\nalong arc', fontsize=7, va='top')
axc.add_patch(plt.Rectangle((-1.78, -1.68), 0.085, 0.065, fc='k', ec='none'))
axc.text(-1.655, -1.648, 'Unique to list', fontsize=7, va='center')
axc.add_patch(plt.Rectangle((-1.78, -1.83), 0.085, 0.065, fc='#7B4EA3', ec='none'))
axc.text(-1.655, -1.798, 'Shared between lists', fontsize=7, va='center')
axc.text(-1.78, -1.95, 'Inner curves\n  Genes shared between lists\n  Unique genes '
         'belong to same\n  ontology term', fontsize=6.5, va='top')

# ============================================================ j: 富集网络
G = nx.Graph()
cluster_names = ['Cell cycle', 'DNA replication', 'Apoptosis', 'mTOR signaling',
                 'Hypoxia', 'EMT', 'Inflammatory response',
                 'Interferon gamma response', 'G2M checkpoint', 'Coagulation',
                 'Complement', 'Oxidative phosphorylation']
node_meta = {}
nid = 0
for ci, cname in enumerate(cluster_names):
    size = int(r.integers(3, 8))
    for m in range(size):
        G.add_node(nid)
        frac = r.dirichlet([1.2, 1.2, 1.2])
        p = 10 ** r.uniform(-15, -2)
        node_meta[nid] = {'cluster': ci, 'frac': frac, 'p': p}
        nid += 1
    # 簇内链
    for m in range(size - 1):
        G.add_edge(nid - size + m, nid - size + m + 1)
    if size > 3:
        G.add_edge(nid - size, nid - size + 2)
# 少量簇间桥
for _ in range(10):
    a = int(r.integers(0, nid))
    b = int(r.integers(0, nid))
    if a != b and node_meta[a]['cluster'] != node_meta[b]['cluster']:
        G.add_edge(a, b)

pos0 = nx.spring_layout(G, seed=35, iterations=200, k=0.5)

# 簇质心手工布置(避免重叠), 簇内用 spring 偏移
targets = {0: (0.16, 0.52), 1: (0.36, 0.66), 2: (0.55, 0.26), 3: (0.45, 0.44),
           4: (0.08, 0.74), 5: (0.28, 0.88), 6: (0.10, 0.16),
           7: (0.44, 0.12), 8: (0.42, 0.78), 9: (0.68, 0.66),
           10: (0.86, 0.44), 11: (0.80, 0.10)}
xs = np.array([p[0] for p in pos0.values()])
ys = np.array([p[1] for p in pos0.values()])
span = max(xs.max() - xs.min(), ys.max() - ys.min())
pos = {}
for k in pos0:
    ci = node_meta[k]['cluster']
    tx, ty = targets[ci]
    off = ((pos0[k][0] - xs.mean()) / span, (pos0[k][1] - ys.mean()) / span)
    pos[k] = (tx + off[0] * 0.22, ty + off[1] * 0.22)

for u, v in G.edges():
    (x1, y1), (x2, y2) = pos[u], pos[v]
    axn.plot([x1, x2], [y1, y2], color='#C8C8C8', lw=0.6, alpha=0.5, zorder=1)

def node_radius(p):
    return 0.005 + 0.013 * (15 - np.log10(p)) / 13.0

for k in G.nodes():
    x, y = pos[k]
    fr = node_meta[k]['frac']
    rad = node_radius(node_meta[k]['p'])
    cols = ['#C0392B', '#2E8B57', '#2166AC']      # alpha / beta / islets
    start = 90.0
    for f, c in zip(fr, cols):
        end = start - 360 * f
        axn.add_patch(Wedge((x, y), rad, end, start, fc=c, ec='white',
                            lw=0.3, zorder=3))
        start = end

# 通路标签放在各簇质心旁
for ci, cname in enumerate(cluster_names):
    mem = [pos[k] for k in node_meta if node_meta[k]['cluster'] == ci]
    cx = np.mean([m[0] for m in mem])
    cy = np.mean([m[1] for m in mem])
    axn.text(cx, cy + 0.055, cname, fontsize=7.2, ha='center', va='bottom',
             color='#1A1A1A', style='normal')

# P 值图例(右上, 用 scatter 尺寸表示)
def rad_to_s(rad):
    return (rad * 2 * 72 / (axn.get_window_extent().width /
                            (axn.bbox.x1 - axn.bbox.x0))) ** 2

p_leg = [1e-2, 1e-8, 1e-15]
s_leg = [(node_radius(p) * 300) ** 2 for p in p_leg]
axn.scatter([0.85, 0.90, 0.95], [1.0, 1.0, 1.0], s=s_leg,
            transform=axn.transAxes, clip_on=False,
            facecolor='#9DB8D9', edgecolor='#4A6A8A', lw=0.5, zorder=5)
axn.text(0.90, 1.05, '$P$ value:', fontsize=7, ha='center',
         transform=axn.transAxes, clip_on=False)
for i, p in enumerate(p_leg):
    axn.text(0.85 + i * 0.05, 0.968, '$10^{%d}$' % (-2 if i == 0 else (-8 if i == 1 else -15)),
             fontsize=5.5, ha='center', transform=axn.transAxes, clip_on=False)
# 成分图例
lx = 0.80
for i, (c, t) in enumerate([('#C0392B', 'alpha cells'), ('#2E8B57', 'beta cells'),
                            ('#2166AC', 'Islets')]):
    axn.scatter([lx], [0.925 - i * 0.026], s=14, transform=axn.transAxes,
                clip_on=False, color=c, zorder=5)
    axn.text(lx + 0.013, 0.925 - i * 0.026, t, fontsize=5.5, va='center',
             transform=axn.transAxes, clip_on=False)
axn.text(lx - 0.01, 0.952, 'Per cent of genes from:', fontsize=6,
         transform=axn.transAxes, clip_on=False)

axn.set_xlim(-0.08, 1.08)
axn.set_ylim(-0.06, 1.06)
axn.axis('off')
axc.text(0.0, 1.03, 'i', transform=axc.transAxes, fontsize=11, fontweight='bold')
axn.text(-0.02, 1.0, 'j', transform=axn.transAxes, fontsize=11, fontweight='bold')

save(fig, 'case_seg035.png')
