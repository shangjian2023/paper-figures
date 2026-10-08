# -*- coding: utf-8 -*-
"""案例34 - Nature 火山图&富集网络图 2x2: 两张火山(上调紫/红, 下调黑)
+ 两张网络图(networkx spring_layout, 节点按ES着色, 灰边, 椭圆功能群)。
参考: frames/seg_034.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patheffects as pe
import networkx as nx
from matplotlib.patches import Ellipse

set_style()
r = rng(34)


# ================================================================ 火山图
def volcano(ax, up_cmap, seed, right_labels, left_labels):
    rr = rng(seed)
    n = 1500
    fc = rr.normal(0, 0.9, n).clip(-4.1, 4.1)
    pv = 0.4 + 3.4 * np.abs(fc) + rr.normal(0, 2.4, n)
    pv = np.clip(pv, 0, 28)
    grey = pv < 2.2
    ax.scatter(fc[grey], pv[grey], s=10, color='0.78', edgecolor='none',
               alpha=0.85, zorder=2)
    up = (pv >= 2.2) & (fc > 0.55)
    dn = (pv >= 2.2) & (fc < -0.55)
    cmap = mcolors.LinearSegmentedColormap.from_list('m', up_cmap)
    vmax = np.abs(fc[up]).max() if up.any() else 1
    ax.scatter(fc[up], pv[up], s=13, c=fc[up], cmap=cmap,
               vmin=0.5, vmax=max(vmax, 2.5), zorder=3)
    ax.scatter(fc[dn], pv[dn], s=12, color='#1a1a1a', zorder=3)
    ax.axhline(2.2, color='0.55', lw=0.8)
    for v in (-0.55, 0.55):
        ax.axvline(v, color='0.75', lw=0.8)
    # 基因名必须压在散点之上且带白描边: 密集黑/红点云中黑字会被同色点淹没
    stroke = [pe.withStroke(linewidth=2, foreground='white')]
    for g, x, y, side in right_labels:
        ax.annotate(italic_gene(g), (x, y), xytext=(x + 0.35 * side, y),
                    fontsize=7.5, va='center', zorder=7, path_effects=stroke,
                    arrowprops=dict(arrowstyle='-', lw=0.5, color='0.3'))
    for g, x, y, side in left_labels:
        ax.text(x, y, italic_gene(g), fontsize=7.5, va='center', ha='right',
                zorder=7, path_effects=stroke)
        ax.plot([x + 0.10, x + 0.55], [y, y], lw=0.5, color='0.3',
                zorder=6)
    ax.set_xlim(-4.2, 4.2)
    ax.set_ylim(0, 30)
    ax.set_xticks([-4, -2, 0, 2, 4])
    ax.set_yticks([0, 10, 20, 30])
    ax.set_xlabel('Log2 Difference', fontsize=9)
    ax.set_ylabel('-Log10 (p-value)', fontsize=9)
    ax.tick_params(labelsize=7.5)


# ================================================================ 网络图
def network(ax, hi_color, seed, ncl=15):
    rr = rng(seed)
    G = nx.Graph()
    cluster_of = {}
    centers = []
    cols, rows = 5, 3
    ci = 0
    for row in range(rows):
        for col in range(cols):
            if ci >= ncl:
                break
            centers.append((0.10 + col * 0.52 + rr.uniform(-0.07, 0.07),
                            0.10 + row * 0.74 + rr.uniform(-0.06, 0.06)))
            ci += 1
    all_pos = {}
    for c, (cx, cy) in enumerate(centers):
        n = int(rr.integers(5, 12))
        sub = nx.Graph()
        for i in range(n):
            nid = f'c{c}_{i}'
            sub.add_node(nid)
            G.add_node(nid, es=float(np.clip(rr.normal(0, 0.62), -1, 1)),
                       size=rr.uniform(35, 115))
            cluster_of[nid] = c
        for i in range(n):
            for j in range(i + 1, n):
                if rr.random() < 0.55:
                    sub.add_edge(f'c{c}_{i}', f'c{c}_{j}')
        lp = nx.spring_layout(sub, seed=seed * 13 + c, iterations=90,
                              scale=0.17, center=(cx, cy))
        all_pos.update(lp)
    # 相邻簇间灰桥连
    for a in range(ncl):
        for b in range(a + 1, ncl):
            d = np.hypot(centers[a][0] - centers[b][0],
                         centers[a][1] - centers[b][1])
            if d < 0.60 and rr.random() < 0.55:
                na = [x for x in G if cluster_of[x] == a]
                nb = [x for x in G if cluster_of[x] == b]
                G.add_edge(rr.choice(na), rr.choice(nb))
    pos = all_pos
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='0.62', width=1.6,
                           alpha=0.35)
    nodes = list(G.nodes())
    cmap = mcolors.LinearSegmentedColormap.from_list(
        'b2h', ['#141414', '#a8a8a8', '#efeaef', hi_color])
    es = [G.nodes[n_]['es'] for n_ in nodes]
    sz = [G.nodes[n_]['size'] for n_ in nodes]
    ax.scatter([pos[n_][0] for n_ in nodes], [pos[n_][1] for n_ in nodes],
               c=es, cmap=cmap, vmin=-1, vmax=1, s=sz, zorder=3)
    # 椭圆功能群圈注; 通路名防重叠: 上/中排组的名字放进两排节点云之间的走廊带,
    # 顶排组放椭圆上方; Sumoylation 名字缩短
    groups = [[0, 1], [2, 3], [5, 6], [7, 8, 9], [10, 11], [12, 13], [4], [14]]
    names = ['Mitochondrial\ntranslation', 'Vesicle mediated\ntransport',
             'Cell cycle', 'Sumoylation /\nubiquitinylation',
             'Signaling by Rho\nGTPases', 'Nucleotide excision\nrepair',
             'mTOR signaling', 'mRNA splicing']
    row_y = [0.10, 0.84, 1.58]
    for gi, name in zip(groups, names):
        pts = np.array([pos[n_] for n_ in G if cluster_of[n_] in gi])
        cx, cy = pts.mean(0)
        w = np.ptp(pts[:, 0]) + 0.50
        h = np.ptp(pts[:, 1]) + 0.38
        ax.add_patch(Ellipse((cx, cy), w, h, facecolor=hi_color,
                             alpha=0.10, edgecolor='none', zorder=1))
        grow = gi[0] // 5
        if grow < 2:
            ly = (row_y[grow] + row_y[grow + 1]) / 2
            ax.text(cx, ly, name, fontsize=5.8, ha='center', va='center',
                    color='0.35', style='italic', zorder=4)
        else:
            ax.text(cx, cy + h / 2 + 0.06, name, fontsize=5.8, ha='center',
                    va='bottom', color='0.35', style='italic', zorder=4)
    ax.set_xlim(-0.30, 2.45)
    ax.set_ylim(-0.30, 2.05)
    ax.axis('off')
    return cmap


def es_colorbar(ax, cmap, left_txt, right_txt, title=None):
    cax = ax.inset_axes([0.34, -0.155, 0.36, 0.07])
    grad = np.linspace(0, 1, 256).reshape(1, -1)
    cax.imshow(grad, aspect='auto', cmap=cmap, extent=[-1, 1, 0, 1])
    cax.set_yticks([])
    cax.set_xticks([-1, 0, 1])
    cax.tick_params(labelsize=6.5, length=2)
    for s_ in ('top', 'right', 'left'):
        cax.spines[s_].set_visible(False)
    if title:
        cax.set_title(title, fontsize=7, pad=2)
    # 两侧说明文字外移并与 '-1'/'1' 刻度标签拉开横向间距
    ax.text(0.295, -0.185, left_txt, fontsize=7.5, ha='right', va='top',
            transform=ax.transAxes)
    ax.text(0.745, -0.185, right_txt, fontsize=7.5, ha='left', va='top',
            transform=ax.transAxes)


fig = plt.figure(figsize=cm2in(17.5, 17))
gs = fig.add_gridspec(2, 2, left=0.08, right=0.97, top=0.965, bottom=0.09,
                      wspace=0.30, hspace=0.55)
axv1 = fig.add_subplot(gs[0, 0])
axn1 = fig.add_subplot(gs[0, 1])
axv2 = fig.add_subplot(gs[1, 0])
axn2 = fig.add_subplot(gs[1, 1])

volcano(axv1, ['#b57fc6', '#6b2d8e', '#4a1a6b'], 341,
        [('ATP1B1', 2.1, 27, 1), ('SYN1', 1.35, 25.1, 1),
         ('TUBB4A', 1.55, 19.5, 1), ('GLS', 1.8, 14, 1),
         ('VSNL1', 2.5, 11.5, 1)],
        [('TIMELESS', -1.55, 14, -1), ('ATAD2', -1.75, 11.2, -1),
         ('PCBP4', -1.5, 9.4, -1), ('PKB', -1.2, 7.6, -1),
         ('CRAPB2', -1.75, 4.6, -1)])
c1 = network(axn1, '#7d3f9e', 342)
es_colorbar(axn1, c1, 'Lower abundant in pSHHs', 'Higher abundant pSHHs')

volcano(axv2, ['#e86a6a', '#c22030', '#8e1020'], 343,
        [('FLNA', 0.75, 27, 1), ('ALDH1A31', 1.6, 24, 1),
         ('PDLIM3', 1.85, 20, 1), ('GAB1', 1.8, 14.5, 1),
         ('MICAL1', 1.95, 12.5, 1)],
        [('ASS1', -1.35, 21, -1), ('IGSF21', -1.15, 17.5, -1),
         ('TIGAR', -0.95, 13.9, -1), ('CA4', -0.9, 12.0, -1),
         ('CADPS', -0.85, 10.1, -1)])
c2 = network(axn2, '#c22030', 343)
es_colorbar(axn2, c2, 'Lower abundant in pSHHt', 'Higher abundant pSHHt',
            title='ES')

save(fig, 'case_seg034.png')
