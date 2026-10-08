# -*- coding: utf-8 -*-
"""案例47 (seg46) - Nature 动态交互桑基图(二): 四层桑基 年份段→谱系→国家→省。
参考: frames/seg_046.jpg — 层1年份段彩块, 层2谱系, 层3国家(中国橙/美国紫), 层4省;
标签'名 (百分比)', 小流量浅灰, 大流随目标着色。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *
set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from helpers.sankey import sankey

# ---------------- 数据(百分比, 与参考图一致)
L0 = {'1994-1999': 1.19, '2000-2005': 19.61, '2006-2010': 33.36,
      '2011-2016': 36.92, '2017-2022': 8.93}
L1 = {'Sublineage 8.7': 63.13, 'Paraphyletic cluster\nin Lineage 8': 36.87}
small_c = ['Russia', 'Philippines', 'Laos', 'Cambodia', 'India', 'Switzerland',
           'Thailand', 'Vietnam']
L2 = {n: v for n, v in zip(small_c, [0.03, 0.03, 0.08, 0.16, 0.78, 0.03, 2.37, 3.29])}
L2['China'] = 56.36
L2['USA'] = 36.25
for n, v in [('Mexico', 0.24), ('Canada', 0.26), ('South Korea', 0.08), ('Japan', 0.03)]:
    L2[n] = v

prov_pct = [('Anhui', 3.11), ('Beijing', 2.82), ('Chongqing', 0.96), ('Fujian', 5.26),
            ('Gansu', 1.29), ('Guangdong', 28.79), ('Guangxi', 8.71), ('Guizhou', 0.48),
            ('Hainan', 0.10), ('Hebei', 2.01), ('Heilongjiang', 3.16), ('Henan', 7.03),
            ('Hongkong', 0.24), ('Hubei', 7.56), ('Hunan', 1.67), ('Inner Mongolia', 3.19),
            ('Jiangsu', 3.73), ('Jiangxi', 4.93), ('Jilin', 0.67), ('Liaoning', 0.29),
            ('Ningxia', 0.24), ('Qinghai', 0.05), ('Shaanxi', 0.48), ('Shandong', 4.55),
            ('Shanghai', 0.29), ('Shanxi', 0.10), ('Sichuan', 4.31), ('Tianjin', 0.29),
            ('Xinjiang', 3.11), ('Yunnan', 2.58), ('Zhejiang', 5.07)]
scale = 56.36 / sum(p for _, p in prov_pct)
L3 = {n: p * scale for n, p in prov_pct}

COL_SUB, COL_PARA = '#8E3A80', '#40E0D0'
C0 = {'1994-1999': '#222222', '2000-2005': '#7EC8E3', '2006-2010': '#D93B3B',
      '2011-2016': '#2FA055', '2017-2022': '#F0E442'}
C1 = {'Sublineage 8.7': COL_SUB, 'Paraphyletic cluster\nin Lineage 8': COL_PARA}
C2 = {n: '#333333' for n in L2}
C2['China'] = '#E8823A'; C2['USA'] = '#7D2A6E'
C3 = {n: pal('tab20')[i % 20] for i, (n, _) in enumerate(prov_pct)}

# 年→谱系 (值和精确匹配节点)
f01 = [('1994-1999', 'Sublineage 8.7', 0.70), ('1994-1999', 'Paraphyletic cluster\nin Lineage 8', 0.49),
       ('2000-2005', 'Sublineage 8.7', 13.60), ('2000-2005', 'Paraphyletic cluster\nin Lineage 8', 6.01),
       ('2006-2010', 'Sublineage 8.7', 21.40), ('2006-2010', 'Paraphyletic cluster\nin Lineage 8', 11.96),
       ('2011-2016', 'Sublineage 8.7', 19.90), ('2011-2016', 'Paraphyletic cluster\nin Lineage 8', 17.02),
       ('2017-2022', 'Sublineage 8.7', 7.53), ('2017-2022', 'Paraphyletic cluster\nin Lineage 8', 1.40)]
# 谱系→国家: Sublineage 63.13 与 Para 36.87 各自精确分解到国家, 和=国家节点值
sub_split = {'China': 33.50, 'USA': 24.50, 'Thailand': 1.60, 'Vietnam': 2.40,
             'India': 0.50, 'Cambodia': 0.10, 'Laos': 0.05, 'Russia': 0.02,
             'Philippines': 0.02, 'Switzerland': 0.02, 'South Korea': 0.05,
             'Japan': 0.02, 'Mexico': 0.15, 'Canada': 0.20}
para_split = {'China': 22.86, 'USA': 11.75, 'Thailand': 0.77, 'Vietnam': 0.89,
              'India': 0.28, 'Cambodia': 0.06, 'Laos': 0.03, 'Russia': 0.01,
              'Philippines': 0.01, 'Switzerland': 0.01, 'South Korea': 0.03,
              'Japan': 0.01, 'Mexico': 0.09, 'Canada': 0.06}
f12 = []
for src, split in (('Sublineage 8.7', sub_split),
                   ('Paraphyletic cluster\nin Lineage 8', para_split)):
    for dst, val in split.items():
        col = '#EFA57E' if dst == 'China' else ('#B088BC' if dst == 'USA' else '#D9D9D9')
        f12.append((1, src, 2, dst, val, col))
# 国家→省 (仅中国, 浅橙大带)
f23 = [(2, 'China', 3, n, v, '#F5C6A5') for n, v in L3.items()]

links = [(0, s, 1, d, v, '#B07CC6' if d == 'Sublineage 8.7' else '#5BC8B8') for s, d, v in
         [(s, d, v) for s, d, v in f01]] + f12 + f23
node_colors = {}
node_colors.update(C0); node_colors.update(C1); node_colors.update(C2); node_colors.update(C3)

# ---------------- 绘制
fig, ax = plt.subplots(figsize=cm2in(17, 16))
fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
gap, node_w = 0.02, 0.022
sankey([L0, L1, L2, L3], links, node_colors=node_colors, node_w=node_w, gap=gap,
       alpha=0.5, ax=ax, label_side='off')

for p in ax.patches:
    if isinstance(p, Rectangle):
        p.set_edgecolor('#444444'); p.set_linewidth(0.4)

# ---------------- 带百分比的标签 + 小节点标签防重叠铺开
def npos(layer, gap):
    pos, y = {}, 1.0
    tot = sum(layer.values())
    avail = 1.0 - gap * (len(layer) - 1)
    for name, v in layer.items():
        h = v / tot * avail
        pos[name] = (y - h, y)
        y -= h + gap
    return pos

pct = {n: f'{v:.2f}%' for n, v in L0.items()}
pct.update({'Sublineage 8.7': '63.13%', 'Paraphyletic cluster\nin Lineage 8': '36.87%'})
pct.update({n: f'{v:.2f}%' for n, v in L2.items()})
pct.update({n: f'{p:.2f}%' for n, p in prov_pct})

xs = np.linspace(0, 1, 4)
P = [npos(L, gap) for L in (L0, L1, L2, L3)]

def spread_centers(names, pos, min_dy):
    """自上而下强制标签最小间距, 返回 {name: label_y}。"""
    order = sorted(names, key=lambda n: -sum(pos[n]))
    out, prev = {}, None
    for n in order:
        yc = sum(pos[n]) / 2
        if prev is not None and yc > prev - min_dy:
            yc = prev - min_dy
        out[n] = yc
        prev = yc
    return out

# 层0/层1: 标签在节点右侧
for name, (y0, y1) in P[0].items():
    ax.text(xs[0] + node_w + 0.012, (y0 + y1) / 2, f'{name} ({pct[name]})',
            ha='left', va='center', fontsize=8, color='#222')
for name, (y0, y1) in P[1].items():
    ax.text(xs[1] + node_w + 0.012, (y0 + y1) / 2, f'{name} ({pct[name]})',
            ha='left', va='center', fontsize=8, color='#222')
# 层2/层3: 标签在节点左侧, 微小节点补色片
for li, min_dy, fs in ((2, 0.020, 6.8), (3, 0.0165, 6.5)):
    lay = (L2 if li == 2 else L3)
    lab_y = spread_centers(list(lay), P[li], min_dy)
    x0 = xs[li]
    for name in lay:
        y0, y1 = P[li][name]
        h = y1 - y0
        yl = lab_y[name]
        ax.text(x0 - 0.014, yl, f'{name} ({pct[name]})', ha='right', va='center',
                fontsize=fs, color='#222')
        if h < 0.006:
            ax.plot([x0 - 0.012, x0], [yl, yl], color=node_colors[name], lw=1.6,
                    solid_capstyle='butt', zorder=2)

ax.set_xlim(-0.02, 1.10)
save(fig, 'case_seg046.png')
