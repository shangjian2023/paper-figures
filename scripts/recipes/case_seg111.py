# -*- coding: utf-8 -*-
"""案例111 - Nature 火山图+富集图(一) 2x2: 上=基础state(红上/蓝下),
下=IFN刺激state。火山 x=-log10FDR(断轴 >=300), y=log2FC;
网络 蓝节点/橙红节点+灰边+浅色椭圆功能群。参考: frames/seg_111.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import networkx as nx
from matplotlib.patches import Ellipse, Rectangle

set_style()
r = rng(111)

PATHWAYS = ['DNA repair and chromatin\norganization', 'Cell cycle',
            'Cytoskeleton\norganization', 'Cell junctions/\nadhesion',
            'Morphogenesis', 'Protein dephosphorylation',
            'Blood vessel development', 'Wnt signalling',
            'Regulation of protein\nphosphorylation',
            'Growth factor signalling',
            'GTPase signalling\n(Ras / Rap1)', 'Nuclear transport',
            'Antigen presentation', 'Type I IFN response',
            'Response to cytokine /\nvirus / bacterium',
            'NFkB-signalling', 'Apoptosis', 'ER stress',
            'Protein catabolism\nand autophagy',
            'Peptide biosynthetic\nprocesses', 'Hypoxia',
            '(Golgi) vesicle\ntransport']


def title_bar(ax, txt='Endothelial cells'):
    ax.add_patch(Rectangle((0, 1.005), 1, 0.13, transform=ax.transAxes,
                           clip_on=False, facecolor='#e5aebc',
                           edgecolor='0.3', lw=0.6))
    ax.text(0.5, 1.07, txt, transform=ax.transAxes, ha='center', va='center',
            fontsize=8.5)


def volcano(ax, seed, right_lab, left_lab):
    rr = rng(seed)
    n = 1900
    l10 = rr.exponential(0.28, n) * 60 + rr.uniform(0, 8, n)
    l10 = np.clip(l10, 0, 285)
    fc = 0.9 * l10 / 60 + rr.normal(0, 0.22, n)
    fc = np.clip(fc, -1.15, 4.6)
    dn = rr.random(n) < 0.35
    fc[dn] = np.clip(-0.25 - rr.exponential(0.3, dn.sum()) - 0.02 * l10[dn],
                     -1.15, -0.02)
    col = np.where(fc > 0.25, '#c0392b',
                   np.where(fc < -0.05, '#2e6db4', '#9a9a9a'))
    ax.scatter(l10, fc, s=7, c=col, alpha=0.8, lw=0, zorder=2)
    # x>=300 处一列高分点
    hi = rr.uniform(1.9, 4.5, 26)
    ax.scatter(np.full(26, 310) + rr.uniform(-6, 6, 26), hi, s=7,
               c='#c0392b', alpha=0.85, lw=0, zorder=2)
    for g, x, y, side in right_lab + left_lab:
        ax.text(x, y, italic_gene(g), fontsize=6.8, va='center',
                ha='left' if side > 0 else 'right', color='#1a1a1a', zorder=5)
        if side > 0:
            ax.plot([x - 0.28, x - 0.06], [y, y], lw=0.5, color='0.3')
        else:
            ax.plot([x + 0.06, x + 0.28], [y, y], lw=0.5, color='0.3')
    ax.set_xlim(-14, 355)
    ax.set_ylim(-1.25, 4.7)
    ax.set_xticks([0, 100, 200, 315])
    ax.set_xticklabels(['0', '100', '200', '$\\geq$300'])
    ax.set_yticks([-1, 0, 1, 2, 3, 4])
    ax.tick_params(labelsize=7)


def network(ax, node_colors, ell_color, seed, names, ncl=12, cb_cmap=None):
    rr = rng(seed)
    G = nx.Graph()
    cluster_of = {}
    centers = []
    cols, rows = 4, 3
    ci = 0
    for row_ in range(rows):
        for col_ in range(cols):
            if ci >= ncl:
                break
            # 4x3 簇心网格, 行距加大(0.95)给组标签留出无节点的空带
            centers.append((0.12 + col_ * 0.56 + rr.uniform(-0.03, 0.03),
                            1.66 - row_ * 0.95 + rr.uniform(-0.03, 0.03)))
            ci += 1
    # 按功能群预分配角度/半径(内盘+外环)再局部抖动: 节点散开不成团
    RX, RY = 0.15, 0.16                    # 外环半径(x/y 数据单位, 纸面等向)
    pos = {}
    for c, (cx, cy) in enumerate(centers):
        n = int(rr.integers(6, 12))
        n_in = max(2, n // 3)
        ang0 = rr.uniform(0, 2 * np.pi)
        for i in range(n):
            if i < n_in:
                rad_x = 0.045 * rr.uniform(0.2, 1.0)
                rad_y = 0.060 * rr.uniform(0.2, 1.0)
                ang = ang0 + 2 * np.pi * i / n_in + rr.uniform(-0.35, 0.35)
            else:
                rad_x = RX * rr.uniform(0.75, 1.15)
                rad_y = RY * rr.uniform(0.75, 1.15)
                ang = ang0 + 2 * np.pi * (i - n_in) / (n - n_in) \
                    + rr.uniform(-0.22, 0.22)
            nid = f'c{c}_{i}'
            G.add_node(nid)
            cluster_of[nid] = c
            pos[nid] = (cx + rad_x * np.cos(ang), cy + rad_y * np.sin(ang))
        for i in range(n):
            for j in range(i + 1, n):
                if rr.random() < 0.55:
                    G.add_edge(f'c{c}_{i}', f'c{c}_{j}')
    for a in range(ncl):
        for b in range(a + 1, ncl):
            if np.hypot(centers[a][0] - centers[b][0],
                        centers[a][1] - centers[b][1]) < 0.70 and \
                    rr.random() < 0.4:
                na = [x for x in G if cluster_of[x] == a]
                nb = [x for x in G if cluster_of[x] == b]
                G.add_edge(rr.choice(na), rr.choice(nb))
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='0.6', width=1.2,
                           alpha=0.4)
    nodes = list(G.nodes())
    sz = rr.uniform(14, 78, len(nodes))
    ax.scatter([pos[n_][0] for n_ in nodes], [pos[n_][1] for n_ in nodes],
               c=[node_colors[cluster_of[n_]] for n_ in nodes], s=sz,
               zorder=3)
    groups = [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9], [10], [11]]
    for name, gi in zip(names, groups):
        pts = np.array([pos[n_] for n_ in nodes if cluster_of[n_] in gi])
        cx, cy = pts.mean(0)
        w = np.ptp(pts[:, 0]) + 0.34
        h = np.ptp(pts[:, 1]) + 0.22
        ax.add_patch(Ellipse((cx, cy), w, h, facecolor=ell_color,
                             alpha=0.14, edgecolor=ell_color, lw=0.8,
                             zorder=1))
        # 标签全部放进无节点的空带: 行0/行1组与簇10 放椭圆上缘(上方是行间空带),
        # 行2组放下缘; 簇11 再降一排并左移, 避开簇10标签与 ES 色条
        lx = cx - (0.45 if 11 in gi else 0.0)
        if min(gi) < 8 or 10 in gi:
            ax.text(lx, cy + h / 2 + 0.04, name, fontsize=6.0, ha='center',
                    va='bottom', color='0.25', zorder=4)
        else:
            ly = cy - h / 2 - 0.045
            if 11 in gi:
                ly -= 0.16
            ax.text(lx, ly, name, fontsize=6.0, ha='center', va='top',
                    color='0.25', zorder=4)
    ax.set_xlim(-0.30, 2.45)
    ax.set_ylim(-0.90, 2.33)
    ax.axis('off')
    # 右侧图例: 数量圈 + ES 渐变 (cmap 与该面板节点色一致)
    lg = ax.inset_axes([0.895, 0.52, 0.10, 0.36])
    lg.axis('off')
    lg.set_xlim(0, 1)
    lg.set_ylim(0, 1)
    ys = [0.85, 0.62, 0.38, 0.12]
    for y_, s_ in zip(ys, [20, 45, 85, 130]):
        lg.scatter([0.20], [y_], s=s_, facecolor='none', edgecolor='0.3',
                   lw=0.8, clip_on=False)
    for y_, t in zip(ys, ['50', '100', '200', '300']):
        lg.text(0.55, y_, t, fontsize=5.5, va='center')
    lg.text(0.5, 1.08, 'number of genes', fontsize=5.5, ha='center')
    cg = ax.inset_axes([0.905, 0.05, 0.075, 0.28])
    grad = np.linspace(0, 1, 128).reshape(-1, 1)
    cg.imshow(grad, aspect='auto', cmap=cb_cmap if cb_cmap is not None
              else PLL_CMAP, extent=[0, 1, 0, 1])
    cg.set_xticks([])
    cg.set_yticks([0.05, 0.95])
    cg.set_yticklabels(['1.3e-03', '1.3e-05'], fontsize=5)
    cg.tick_params(length=2, pad=1)
    cg.set_title('ES p-val', fontsize=5.5, pad=1.5)


PLL_CMAP = mcolors.LinearSegmentedColormap.from_list(
    'pll', ['#e8e2f2', '#b9a8d8', '#7b5fa8', '#3a2a6b'])
fig = plt.figure(figsize=cm2in(17.5, 16.5))
gs = fig.add_gridspec(2, 2, left=0.075, right=0.97, top=0.925, bottom=0.065,
                      wspace=0.28, hspace=0.62)

axv1 = fig.add_subplot(gs[0, 0])
title_bar(axv1)
volcano(axv1, 1111,
        [('ISG15', 300, 4.42, 1), ('MX1', 296, 4.14, 1), ('IFIT1', 302, 3.86, 1),
         ('IFI27', 294, 3.58, 1), ('OAS1', 298, 3.30, 1), ('DDX58', 304, 3.02, 1)],
        [('TFF1', 42, 0.30, -1), ('CDH5', 100, 0.10, -1),
         ('PDGFB', 150, -0.08, -1), ('CDH2', 55, -0.38, -1),
         ('EDN1', 110, -0.56, -1), ('CLDN5', 160, -0.72, -1),
         ('APLN', 85, -0.88, -1), ('SOX18', 140, -1.02, -1)])
axv1.set_xlabel('-log$_{10}$FDR', fontsize=8.5)
axv1.set_ylabel('log$_2$-FC', fontsize=8.5)

axn1 = fig.add_subplot(gs[0, 1])
title_bar(axn1)
r = rng(1111)
ncol1 = [mcolors.to_hex(PLL_CMAP(r.uniform(0.35, 1.0))) for _ in range(14)]
network(axn1, ncol1, '#8fa8d8', 1112, PATHWAYS[:7] + PATHWAYS[11:12])

RED_CMAP = mcolors.LinearSegmentedColormap.from_list(
    'rr', ['#f2ddd8', '#e8a090', '#d84a35', '#a81a10'])
axv2 = fig.add_subplot(gs[1, 0])
title_bar(axv2)
volcano(axv2, 1113,
        [('ISG15', 300, 4.42, 1), ('MX1', 294, 4.14, 1), ('IFIT1', 302, 3.86, 1),
         ('IFI27', 296, 3.58, 1), ('OAS1', 298, 3.30, 1), ('DDX58', 304, 3.02, 1),
         ('HLA-B', 205, 1.80, 1), ('TAP1', 235, 1.55, 1),
         ('STAT1', 255, 1.30, 1), ('ISG20', 185, 1.10, 1)],
        [('HMOX1', 250, 2.55, -1), ('NFKBIA', 115, 0.78, -1),
         ('IRF2', 160, 1.02, -1), ('IRF9', 200, 0.95, -1),
         ('ICAM1', 55, 0.42, -1), ('STAT2', 180, 0.68, -1),
         ('CXCL11', 125, 0.25, -1)])
axv2.set_xlabel('-log$_{10}$FDR', fontsize=8.5)
axv2.set_ylabel('log$_2$ FC', fontsize=8.5)

axn2 = fig.add_subplot(gs[1, 1])
title_bar(axn2)
r = rng(1113)
ncol2 = [mcolors.to_hex(RED_CMAP(r.uniform(0.3, 1.0))) for _ in range(14)]
network(axn2, ncol2, '#f0b8a0', 1114,
        ['Antigen presentation', 'Type I IFN response',
         'Response to cytokine /\nvirus / bacterium', 'NFkB-signalling',
         'Apoptosis', 'Protein catabolism\nand autophagy', 'ER stress'],
        cb_cmap=RED_CMAP)

save(fig, 'case_seg111.png')
