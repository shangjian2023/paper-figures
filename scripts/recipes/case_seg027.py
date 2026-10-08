# -*- coding: utf-8 -*-
"""案例27 - Nature 和弦图(双环): 内环 8 土壤因子节点弧(深灰系), 弦连接因子间关系,
带色=大洲(6 色); 外环每因子下挂 2-4 个作物x管理细分小扇区(彩类色, 3.8pt 径向小字);
右上 Outer/Inner circle 双段图例。参考: frames/seg_027.jpg。
实现: 复用 helpers.chord 的 _arc_patch/_ribbon 手画双环。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *
set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from helpers.chord import _arc_patch, _ribbon

r = rng(27)

soil = ['CEC', 'Clay', 'BD', 'pH', 'TN', 'SOC', 'Temp', 'Moist']
ns = len(soil)
crops = ['Rice', 'Wheat', 'Maize', 'Barley']
col_crop = ['#1F6FBF', '#6A3D9A', '#2E8B57', '#D9A421']
col_soil = ['#4A4A4A', '#6E6E6E', '#8A8A8A', '#565656',
            '#757575', '#3F3F3F', '#909090', '#686868']
continents = ['South America', 'Africa', 'Asia', 'Oceania',
              'North America', 'Europe']
col_cont = ['#7EC8E3', '#3A9E5F', '#E3C74F', '#B5DFA0', '#9A9A9A', '#8E2F3E']

# ---- 内环因子间流量(无向对; 每对指定一个大洲配色)
flows = []
for i in range(ns):
    for j in range(i + 1, ns):
        if r.random() < 0.60:
            flows.append([i, j, float(r.uniform(2, 9)), int(r.integers(0, 6))])
deg = np.zeros(ns)
for i, j, w, ci in flows:
    deg[i] += w
    deg[j] += w
for i in range(ns):                              # 兜底: 保证每个因子至少一条弦
    if deg[i] == 0:
        j = (i + 1) % ns
        flows.append([i, j, 5.0, int(r.integers(0, 6))])
        deg[i] += 5.0
        deg[j] += 5.0

# ---- 角度布局: 90° 起顺时针, 因子间留缺口, 因子弧 span 正比于流量
GAP = 3.0
avail = 360.0 - GAP * ns
spans = deg / deg.sum() * avail
arc, curs = {}, {}
a = 90.0
for i in range(ns):
    arc[i] = (a - spans[i], a)                   # (lo, hi) 顺时针
    curs[i] = a                                  # 弦分配游标(自 hi 向 lo)
    a -= spans[i] + GAP

fig, ax = plt.subplots(figsize=cm2in(14.5, 14.0))
ax.set_aspect('equal')
ax.axis('off')
C, R = (0.0, 0.0), 1.0

# ---- 弦(因子<->因子, 底层), 两端按流量比例切分各因子弧段
for i, j, w, ci in flows:
    s_i = spans[i] * w / deg[i]
    s_j = spans[j] * w / deg[j]
    a1, a2 = curs[i] - s_i, curs[i]
    b1, b2 = curs[j] - s_j, curs[j]
    curs[i] -= s_i
    curs[j] -= s_j
    ax.add_patch(_ribbon(C, R, np.radians(a1), np.radians(a2),
                         np.radians(b1), np.radians(b2),
                         col_cont[ci], alpha=0.38))

# ---- 内环因子弧(深灰系) + 内侧切向标签
for i in range(ns):
    lo, hi = arc[i]
    ax.add_patch(_arc_patch(C, R, np.radians(lo), np.radians(hi), 0.055, col_soil[i]))
    mid = (lo + hi) / 2.0
    rot = mid - 360 if mid > 180 else mid
    if abs(rot) > 90:
        rot += 180
    m = np.radians(mid)
    ax.text(0.90 * np.cos(m), 0.90 * np.sin(m), soil[i], ha='center', va='center',
            fontsize=7.5, color='#1A1A1A', rotation=rot, rotation_mode='anchor')

# ---- 外环: 每因子 2-4 个作物x管理细分小扇区(彩类色) + 3.8pt 径向小字
ferts = ['U', 'DPM', 'SBC', 'EEF', 'Manure', 'AN', 'Others', 'Mix']
mgrs = ['CT-Once', 'NT-Once', 'CT-More', 'NT-More']
R2 = 1.10
for i in range(ns):
    lo, hi = arc[i]
    k = int(max(2, min(4, spans[i] / 6.0)))      # 扇区数随 span 缩放, 保证最小宽度
    ws = r.uniform(0.5, 1.0, k)
    totw = ws.sum()
    edges = [hi]
    csum = 0.0
    for t in range(k):
        csum += ws[t]
        edges.append(hi - (hi - lo) * csum / totw)
    g = 0.5
    for t in range(k):
        s_hi, s_lo = edges[t] - g / 2, edges[t + 1] + g / 2
        ci = int(r.integers(0, 4))
        ax.add_patch(_arc_patch(C, R2, np.radians(s_lo), np.radians(s_hi),
                                0.045, col_crop[ci]))
        mid = (s_lo + s_hi) / 2.0
        i1 = int(r.integers(0, 8))
        i2 = (i1 + int(r.integers(1, 8))) % 8   # 两段肥料名不同, 仿参考组合
        lbl = '%s-%s-%s' % (ferts[i1], ferts[i2], mgrs[int(r.integers(0, 4))])
        tdeg = mid - 360 if mid > 180 else mid
        if -90 <= tdeg <= 90:                    # 径向文字: 右半向外读, 左半翻转
            rot, ha = tdeg, 'left'
        else:
            rot = tdeg - 180 if tdeg > 0 else tdeg + 180
            ha = 'right'
        m = np.radians(mid)
        ax.text((R2 + 0.03) * np.cos(m), (R2 + 0.03) * np.sin(m), lbl,
                ha=ha, va='center', fontsize=3.8, color='#333333',
                rotation=rot, rotation_mode='anchor')

# ---- 右上双段图例: Outer circle(作物) / Inner circle(大洲), 置于坐标区右侧圈外, 防压外环小字
h_out = [Patch(fc=c, ec='none', label=l) for l, c in zip(crops, col_crop)]
leg1 = ax.legend(handles=h_out, title='Outer circle', loc='upper left',
                 bbox_to_anchor=(1.01, 1.0), fontsize=6.5, title_fontsize=7.5,
                 frameon=False, handlelength=1.1, handleheight=0.9,
                 labelspacing=0.35, borderaxespad=0.0)
ax.add_artist(leg1)
h_in = [Patch(fc=c, ec='none', label=l) for l, c in zip(continents, col_cont)]
ax.legend(handles=h_in, title='Inner circle', loc='upper left',
          bbox_to_anchor=(1.01, 0.63), fontsize=6.5, title_fontsize=7.5,
          frameon=False, handlelength=1.1, handleheight=0.9,
          labelspacing=0.35, borderaxespad=0.0)

ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
save(fig, 'case_seg027.png')
