# -*- coding: utf-8 -*-
"""helpers 冒烟测试: 每个特殊图型助手各生成一张验证图。"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import matplotlib.pyplot as plt
from paper_style import set_style, save, rng, pal

set_style()
os.makedirs(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'gallery', '_smoke'), exist_ok=True)
SMOKE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'gallery', '_smoke')

# ---- ternary
from helpers.ternary import Ternary
fig, ax = plt.subplots(figsize=(4.2, 4.0))
t = Ternary(ax, vertex_labels=('ISC/TA', 'Non-canon', 'Diff.int.'))
t.setup()
t.edge_arrows(['ISC/TA', 'Diff', 'Non-canon'])
r = rng(1)
p = r.dirichlet([2, 2, 2], 300)
t.scatter(p[:, 0], p[:, 1], p[:, 2], s=3, alpha=0.4, color='gray')
t.density(p[:, 0], p[:, 1], p[:, 2], cmap='Purples')
save(fig, 'smoke_ternary.png', dirs=SMOKE)

# ---- chord
from helpers.chord import chord_diagram
fig, ax = plt.subplots(figsize=(5.2, 5.2))
M = np.array([[0, 12, 3, 1], [12, 0, 8, 2], [3, 8, 0, 5], [1, 2, 5, 0]])
chord_diagram(['CN', 'US', 'EU', 'AU'], M, colors=pal('cell', 4), ax=ax)
save(fig, 'smoke_chord.png', dirs=SMOKE)

# ---- sankey
from helpers.sankey import sankey
fig, ax = plt.subplots(figsize=(6.4, 3.6))
layers = [{'ZT0': 40, 'ZT6': 30, 'ZT12': 20, 'ZT18': 10},
          {'GeneA': 35, 'GeneB': 25, 'GeneC': 40},
          {'target1': 45, 'target2': 55}]
links = [(0, 'ZT0', 1, 'GeneA', 25, '#4E79A7'), (0, 'ZT0', 1, 'GeneB', 15, '#F28E2B'),
         (0, 'ZT6', 1, 'GeneA', 10, '#4E79A7'), (0, 'ZT6', 1, 'GeneC', 20, '#59A14F'),
         (0, 'ZT12', 1, 'GeneB', 10, '#F28E2B'), (0, 'ZT12', 1, 'GeneC', 10, '#59A14F'),
         (0, 'ZT18', 1, 'GeneC', 10, '#59A14F'),
         (1, 'GeneA', 2, 'target1', 20, '#4E79A7'), (1, 'GeneA', 2, 'target2', 15, '#B07AA1'),
         (1, 'GeneB', 2, 'target2', 25, '#F28E2B'), (1, 'GeneC', 2, 'target1', 25, '#59A14F'),
         (1, 'GeneC', 2, 'target2', 15, '#59A14F')]
sankey(layers, links, ax=ax, node_colors={'ZT0': '#E15759', 'ZT6': '#4E79A7'})
save(fig, 'smoke_sankey.png', dirs=SMOKE)

# ---- upset
from helpers.upset import upset_plot_pro
r = rng(2)
sets = {'D1_Apo': set(r.choice(2000, 500, replace=False)),
        'D2_Apo': set(r.choice(2000, 400, replace=False)),
        'D1_Sym': set(r.choice(2000, 350, replace=False)),
        'D2_Sym': set(r.choice(2000, 300, replace=False))}
fig, axt, axm = upset_plot_pro(sets)
save(fig, 'smoke_upset.png', dirs=SMOKE)

# ---- geo
from helpers.geo import world_map, china_map, china_names
fig, ax = plt.subplots(figsize=(6.8, 3.6))
world_map(ax, facecolor_fn=lambda p: '#8FB8D8' if p.get('name') in ('China', 'United States of America') else '#E8E8E8')
save(fig, 'smoke_world.png', dirs=SMOKE)
fig, ax = plt.subplots(figsize=(4.8, 4.2))
china_map(ax, facecolor_fn=lambda p: '#DE8F6E' if p.get('name') == '四川省' else '#F0F0F0', edgecolor='gray', lw=0.3)
save(fig, 'smoke_china.png', dirs=SMOKE)

# ---- newick
from helpers.newick import random_newick, parse_newick, draw_circular_tree
tree = parse_newick(random_newick(40, seed=3))
phyla = ['Firmicutes', 'Bacteroidetes', 'Proteobacteria', 'Actinobacteria']
fig = plt.figure(figsize=(5.4, 5.4))
ax = fig.add_subplot(111, polar=False)
cols = pal('tab20', 40)
draw_circular_tree(ax, tree, color_fn=lambda nm, leaf, d: cols[hash(nm) % 40], tip_labels=False)
save(fig, 'smoke_tree.png', dirs=SMOKE)

print('ALL SMOKE OK')
