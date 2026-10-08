# -*- coding: utf-8 -*-
"""案例61 - Nature 多边形雷达图: 浅灰世界地图 + 10 个山脉位置嵌小雷达 + 引线标签。
参考: frames/seg_059.jpg — 每雷达 6 轴六边形填充, 顶点标数值, 山脉名引线。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import set_style, save, cm2in

import numpy as np
import matplotlib.pyplot as plt
from helpers.geo import world_map, mercator

set_style()

# (名称, 位置lon, 位置lat, 雷达中心lon, 雷达中心lat, 颜色, 6 个属性值, 名称文字放置)
mts = [
    ('Alaska Range',        -152, 63.0, -149, 71.5, '#7F7F7F',
     [8.5, 152, 30, 4.4, 50, 141], (-167, 60.0, 'left')),
    ('Southwest\nGreenland', -44, 63.5,  -45, 76.0, '#7B9DC9',
     [6.0, 121, 14, 4.2, 52, 41], (-56, 57.0, 'left')),
    ('Scandinavian\nMountains', 13, 62.0, 17, 71.0, '#B5D56A',
     [7.0, 108, 49, 2.3, 63, 31], (0, 55.8, 'left')),
    ('Pamir and Tien Shan',  72, 38.5,   80, 55.0, '#DE6E6A',
     [8.5, 250, 411, 1.6, 111, 53], (86, 49.5, 'left')),
    ('Ecuadorian Andes',    -78, -1.5,  -88,  1.0, '#C3A075',
     [5.2, 263, 33, 16.3, 78, 0.4], (-101, -18.0, 'left')),
    ('European Alps',        10, 46.5,    3, 51.5, '#E47FB4',
     [7.5, 152, 177, 2, 54, 4.8], (-16, 38.5, 'left')),
    ('Rwenzori\nMountains',  29.5, 0.3,   52, -6.0, '#888888',
     [5.1, 190, 88, 2.5, 55, 26], (2, -6.5, 'left')),
    ('Himalayas',            84, 28.5,   74, 36.0, '#B9BECB',
     [8.3, 111, 118, 1.2, 44, 4], (88, 20.5, 'left')),
    ('Chilean Andes',       -70, -35.0, -74, -20.0, '#45C1B4',
     [4.3, 105, 29, 3.8, 43, 7.7], (-97, -36.5, 'left')),
    ('Caucasus Mountains',   43, 42.5,   42, 27.0, '#9575CD',
     [7.8, 184, 260, 1.6, 44, 24], (56, 9.0, 'left')),
    ('Southern\nAlps',      170, -43.0, 173, -29.0, '#E9A25C',
     [7.8, 92, 51, 6.8, 37, 1.2], (148, -36.0, 'left')),
]

fig = plt.figure(figsize=cm2in(18.0, 14.0))
ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
world_map(ax, facecolor_fn=lambda p: '#E8E8E8')
ax.set_xlim(np.radians(-178), np.radians(192))
ax.set_ylim(mercator(0, -60)[1], mercator(0, 83)[1])

angs = np.radians([90, 30, -30, -90, -150, 150])      # 六轴, 顶点朝上


def draw_radar(cx, cy, vals, color, r=0.25, fs=4.5):
    v = np.asarray(vals, float)
    v = v / v.max()
    for t in angs:
        ax.plot([cx, cx + r * np.cos(t)], [cy, cy + r * np.sin(t)],
                color='#C4C4C4', lw=0.4, zorder=4)
    for f in (0.5, 1.0):
        ax.add_patch(plt.Circle((cx, cy), r * f, fc='none', ec='#C9C9C9',
                                lw=0.4, zorder=4))
    px, py = cx + r * v * np.cos(angs), cy + r * v * np.sin(angs)
    ax.fill(px, py, color=color, alpha=0.60, zorder=5,
            edgecolor=color, lw=1.1, joinstyle='round')
    for t, val in zip(angs, vals):                     # 顶点数值
        c, s = np.cos(t), np.sin(t)
        ha = 'left' if c > 0.4 else ('right' if c < -0.4 else 'center')
        va = 'bottom' if s > 0.4 else ('top' if s < -0.4 else 'center')
        lx, ly = cx + 1.28 * r * c, cy + 1.28 * r * s
        txt = ('%g' % val)
        ax.text(lx, ly, txt, ha=ha, va=va, fontsize=fs, color='#222222',
                zorder=7)


rng = np.random.default_rng(59)
for name, lon, lat, cx, cy, color, vals, (tx, ty, ha) in mts:
    # 山脉位置黑点(短链)
    k = 3
    jit = rng.uniform(-2.2, 2.2, (k, 2))
    ax.scatter(np.radians(lon) + jit[:, 0] * 0.02, mercator(lon, lat)[1]
               + jit[:, 1] * 0.012, s=5, color='black', zorder=6)
    if cx is not None:
        draw_radar(np.radians(cx), mercator(cx, cy)[1], vals, color)
        ax.plot([np.radians(cx), np.radians(lon)],
                [mercator(cx, cy)[1], mercator(lon, lat)[1]],
                color='#444444', lw=0.55, zorder=3)
    ax.text(np.radians(tx), mercator(tx, ty)[1], name, ha=ha, va='bottom',
            fontsize=7, color='#111111', linespacing=1.0, zorder=7)

# 径向轴说明: 六轴 = 6 个气候变量, 半径各自归一化, 顶点数字为原始值
ax.text(np.radians(-176), mercator(0, -59.0)[1],
        'Radar: 6 climatic variables, each normalized 0-1\n'
        '(vertex numbers = raw values)',
        ha='left', va='bottom', fontsize=6.5, color='#555555',
        linespacing=1.5, zorder=8)

save(fig, 'case_seg059.png')
