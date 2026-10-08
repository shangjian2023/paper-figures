# -*- coding: utf-8 -*-
"""案例93 (seg91) - Cell 冲击图: 三层 alluvial Species→Specificity→Brightness。
参考: frames/seg_091.jpg — 三列节点(灰 Mouse/蓝 Human; 绿 On-Target/橙 Mixed/紫 Off-Target/
白 No Signal; 7 个 Brightness 端块), 灰主流量 + 蓝高亮流, 流上标 n, 节点内标 n 与 %。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *
set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from helpers.sankey import sankey

GRAY, BLUE = '#B3B3B3', '#7B9FD4'

L0 = {'Mouse': 643, 'Human': 159}
L1 = {'On-Target': 313, 'Mixed': 78, 'Off-Target': 122, 'No Signal in cortex': 289}
L2 = {'High-G': 157, 'High-O': 55, 'High-P': 50,
      'Low-G': 156, 'Low-O': 23, 'Low-P': 72, 'NoSignal': 289}

C0 = {'Mouse': '#8C8C8C', 'Human': '#4C6FBF'}
C1 = {'On-Target': '#3A7D44', 'Mixed': '#E58606', 'Off-Target': '#7D3C98',
      'No Signal in cortex': 'white'}
C2 = {'High-G': '#3A7D44', 'High-O': '#E58606', 'High-P': '#7D3C98',
      'Low-G': '#A9DFBF', 'Low-O': '#F5CBA7', 'Low-P': '#D2B4DE', 'NoSignal': 'white'}
LBL2 = {'High-G': 'n = 157', 'High-O': 'n = 55', 'High-P': 'n = 50',
        'Low-G': 'n = 156', 'Low-O': 'n = 23', 'Low-P': 'n = 72',
        'NoSignal': 'No Signal\nin cortex\nn = 289\n36.1%'}

# Species → Specificity: 灰=Mouse, 蓝=Human (和=节点值)
f01 = [(0, 'Mouse', 1, 'On-Target', 239, GRAY),
       (0, 'Mouse', 1, 'Mixed', 64, GRAY),
       (0, 'Mouse', 1, 'Off-Target', 96, GRAY),
       (0, 'Mouse', 1, 'No Signal in cortex', 244, GRAY),
       (0, 'Human', 1, 'On-Target', 74, BLUE),
       (0, 'Human', 1, 'Mixed', 14, BLUE),
       (0, 'Human', 1, 'Off-Target', 26, BLUE),
       (0, 'Human', 1, 'No Signal in cortex', 45, BLUE)]
# Specificity → Brightness: 大多灰, 两条蓝高亮
f12 = [(1, 'On-Target', 2, 'High-G', 157, GRAY),
       (1, 'On-Target', 2, 'Low-G', 156, GRAY),
       (1, 'Mixed', 2, 'High-O', 55, BLUE),
       (1, 'Mixed', 2, 'Low-O', 23, GRAY),
       (1, 'Off-Target', 2, 'High-P', 50, GRAY),
       (1, 'Off-Target', 2, 'Low-P', 72, BLUE),
       (1, 'No Signal in cortex', 2, 'NoSignal', 289, GRAY)]

links = f01 + f12
node_colors = {}
node_colors.update(C0); node_colors.update(C1); node_colors.update(C2)

fig, ax = plt.subplots(figsize=cm2in(15, 16))
fig.subplots_adjust(left=0.01, right=0.99, top=0.97, bottom=0.01)
gap, node_w = 0.03, 0.05
sankey([L0, L1, L2], links, node_colors=node_colors, node_w=node_w, gap=gap,
       alpha=0.62, ax=ax, label_side='off')

for p in ax.patches:
    if isinstance(p, Rectangle):
        p.set_edgecolor('black'); p.set_linewidth(1.0)

# ---------------- 节点标签: 全部放节点外侧 + 白底 (左/中列放左, 右列放右)
BB = dict(boxstyle='round,pad=0.18', fc='white', ec='none', alpha=0.9)

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
xc = [xi + node_w / 2 for xi in xs]

# 左列(Species): 节点左侧
for name, v in L0.items():
    ym = sum(P0[name]) / 2
    ax.text(xs[0] - 0.012, ym, f'{name}\nn = {v}', ha='right', va='center',
            fontsize=8.5, color='black', bbox=BB, zorder=6)

# 中列(Specificity): 节点左侧
mid_lab = {'On-Target': 'On-Target\nn = 313\n38.9%', 'Mixed': 'Mixed\nn = 78\n9.7%',
           'Off-Target': 'Off-Target\nn = 122\n15.2%',
           'No Signal in cortex': 'No Signal\nin cortex\nn = 289\n36.1%'}
for name, txt in mid_lab.items():
    ym = sum(P1[name]) / 2
    ax.text(xs[1] - 0.012, ym, txt, ha='right', va='center', fontsize=8.5,
            color='black', bbox=BB, zorder=6)

# 右列(Brightness): 节点右侧
for name, txt in LBL2.items():
    ym = sum(P2[name]) / 2
    ax.text(xs[2] + node_w + 0.012, ym, txt, ha='left', va='center', fontsize=8,
            color='black', bbox=BB, zorder=6)

# ---------------- 流量 n 标签 → 两列间中点, 白底
def inflow_centers(layer, links_to, gap):
    """按 sankey() 的入流游标逻辑, 计算每条入流带的竖直中心。"""
    tot = sum(layer.values())
    avail = 1.0 - gap * (len(layer) - 1)
    tops, y = {}, 1.0
    for n_, v in layer.items():
        h = v / tot * avail
        tops[n_] = y
        y -= h + gap
    cur = dict(tops)                              # 从节点顶端往下扣
    out = {}
    for (_, _, _, dst, val, _) in links_to:
        h = val / tot * avail
        cur[dst] -= h
        out[(dst, val)] = cur[dst] + h / 2
    return out

centers = inflow_centers(L1, f01, gap)
xm01 = (xs[0] + node_w + xs[1]) / 2
for (dst, val), ym in centers.items():
    ax.text(xm01, ym, f'n = {val}', ha='center', va='center', fontsize=7.5,
            bbox=BB, zorder=6)

# ---------------- 列标题 + High/Low (右移, 与节点标签脱开)
ax.text(xc[0], 1.045, 'Species', ha='center', fontsize=11)
ax.text(xc[1], 1.045, 'Specificity', ha='center', fontsize=11)
ax.text(xc[2], 1.045, 'Brightness', ha='center', fontsize=11)
y_hi = (sum(P2['High-G']) / 2 + sum(P2['High-P']) / 2) / 2
y_lo = (sum(P2['Low-G']) / 2 + sum(P2['Low-P']) / 2) / 2
ax.text(1.20, y_hi, 'High', rotation=90, ha='center', va='center', fontsize=9)
ax.text(1.20, y_lo, 'Low', rotation=90, ha='center', va='center', fontsize=9)

ax.set_xlim(-0.17, 1.26)
ax.set_ylim(-0.12, 1.06)
save(fig, 'case_seg091.png')
