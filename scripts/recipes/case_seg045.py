# -*- coding: utf-8 -*-
"""案例46 (seg45) - Nature 动态交互桑基图(一): 三层桑基 时间点→基因→目标基因。
参考: frames/seg_045.jpg — 左列4时间点节点(橙/浅蓝/红/绿), 中层4基因节点(黄/紫/绿/橙),
右列20个目标基因末端小块, 流带宽∝值, 带色随目标/源基因, 半透明。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *
set_style()

import numpy as np
import matplotlib.pyplot as plt
from helpers.sankey import sankey

# ---------------- 数据(和相等, 保证节点与流带对齐)
L0 = {'Exe_at_ZT1': 40, 'Exe_at_ZT13': 8, 'Exe_at_ZT17': 14, 'Exe_at_ZT21': 32}
L1 = {'Adh1': 22, 'Eno2': 30, 'G6pc': 18, 'Pck1': 24}
C0 = {'Exe_at_ZT1': '#E8A33D', 'Exe_at_ZT13': '#9BD1F2', 'Exe_at_ZT17': '#D9534F',
      'Exe_at_ZT21': '#3AA76D'}
C1 = {'Adh1': '#E8D44D', 'Eno2': '#8E3A80', 'G6pc': '#35C48D', 'Pck1': '#E8794A'}

targets = ['Wnt5b', 'Ccnd2', 'Sox9', 'Col1a1', 'Col1a2', 'Col2a1', 'Col6a1', 'Col6a2',
           'Col6a3', 'Col11a2', 'Acan', 'Bglap', 'Col10a1', 'Wnt4', 'Dkk2', 'Mapk3',
           'Comp', 'Wnt11', 'Mapk11', 'Gli1', 'Sost']
L2 = dict(zip(targets,
      [5, 4, 4, 5, 4, 5, 5, 4, 5, 4, 5, 7, 4, 4, 7, 5, 5, 4, 3, 4, 3]))
C2 = {g: pal('tab20')[i % 20] for i, g in enumerate(targets)}

# 时间点→基因 (值和 = 各基因节点值)
f01 = [('Exe_at_ZT1', 'Adh1', 10), ('Exe_at_ZT1', 'Eno2', 12), ('Exe_at_ZT1', 'G6pc', 9),
       ('Exe_at_ZT1', 'Pck1', 9), ('Exe_at_ZT13', 'Adh1', 2), ('Exe_at_ZT13', 'Eno2', 2),
       ('Exe_at_ZT13', 'G6pc', 2), ('Exe_at_ZT13', 'Pck1', 2), ('Exe_at_ZT17', 'Adh1', 4),
       ('Exe_at_ZT17', 'Eno2', 5), ('Exe_at_ZT17', 'G6pc', 3), ('Exe_at_ZT17', 'Pck1', 2),
       ('Exe_at_ZT21', 'Adh1', 6), ('Exe_at_ZT21', 'Eno2', 11), ('Exe_at_ZT21', 'G6pc', 4),
       ('Exe_at_ZT21', 'Pck1', 11)]
# 基因→目标基因 (和 = 各基因节点值)
f12 = [('Adh1', 'Wnt5b', 5), ('Adh1', 'Ccnd2', 4), ('Adh1', 'Sox9', 4),
       ('Adh1', 'Col1a1', 5), ('Adh1', 'Col1a2', 4),
       ('Eno2', 'Col2a1', 5), ('Eno2', 'Col6a1', 5), ('Eno2', 'Col6a2', 4),
       ('Eno2', 'Col6a3', 5), ('Eno2', 'Col11a2', 4), ('Eno2', 'Acan', 4), ('Eno2', 'Bglap', 3),
       ('G6pc', 'Col10a1', 4), ('G6pc', 'Wnt4', 4), ('G6pc', 'Dkk2', 5), ('G6pc', 'Mapk3', 5),
       ('Pck1', 'Comp', 5), ('Pck1', 'Wnt11', 5), ('Pck1', 'Mapk11', 4),
       ('Pck1', 'Gli1', 4), ('Pck1', 'Sost', 6)]

# 流带颜色: L0→L1 随目标基因, L1→L2 随源基因 (参考图观感)
links = [(0, s, 1, d, v, C1[d]) for s, d, v in f01] + \
        [(1, s, 2, d, v, C1[s]) for s, d, v in f12]
node_colors = {}
node_colors.update(C0); node_colors.update(C1); node_colors.update(C2)

# ---------------- 绘制
fig, ax = plt.subplots(figsize=cm2in(13.5, 14.5))
fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)
gap, node_w = 0.02, 0.022
sankey([L0, L1, L2], links, node_colors=node_colors, node_w=node_w, gap=gap,
       alpha=0.45, ax=ax, label_side='off')

# 节点描边加深
from matplotlib.patches import Rectangle
for p in ax.patches:
    if isinstance(p, Rectangle):
        p.set_edgecolor('#444444'); p.set_linewidth(0.4)

# ---------------- 标签(全部放节点右侧, 右列基因名放色块左侧)
def npos(layer, gap):
    pos, y = {}, 1.0
    tot = sum(layer.values())
    avail = 1.0 - gap * (len(layer) - 1)
    for name, v in layer.items():
        h = v / tot * avail
        pos[name] = (y - h, y)
        y -= h + gap
    return pos

xs = np.linspace(0, 1, 3)
P0, P1, P2 = (npos(L, gap) for L in (L0, L1, L2))
for name, (y0, y1) in P0.items():
    ax.text(xs[0] + node_w + 0.012, (y0 + y1) / 2, name, ha='left', va='center',
            fontsize=8.5, color='#222')
for name, (y0, y1) in P1.items():
    ax.text(xs[1] + node_w + 0.012, (y0 + y1) / 2, name, ha='left', va='center',
            fontsize=8.5, color='#222')
for name, (y0, y1) in P2.items():
    ax.text(xs[2] - 0.012, (y0 + y1) / 2, name, ha='right', va='center',
            fontsize=6.8, color='#333')

ax.set_xlim(-0.02, 1.10)
save(fig, 'case_seg045.png')
