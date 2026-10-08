# -*- coding: utf-8 -*-
"""案例117(目录案例119) - Nat. Microbiol 中国地图(一): 省份生态区划底色 + 蜱属采样饼图。
参考: frames/seg_117.jpg — 淡彩省界+灰省名+经纬网+指北针+双图例+南海诸岛插图。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'helpers'))
from paper_style import *
set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle, Rectangle
from geo import china_map, mercator

SEED = 117
r117 = rng(SEED)

# ---------------------------------------------------------------- 生态区划(省 -> 区)
ZONES = [
    ('Boreal coniferous forest', '#D3DCCC', ['黑龙江省']),
    ('Temperate forest', '#D9E0CF', ['吉林省', '辽宁省']),
    ('Temperate forest grassland', '#DDE3D3', ['内蒙古自治区']),
    ('Temperate grassland', '#E5E8D8', ['河北省', '山西省', '陕西省']),
    ('Farmland', '#F3F0D8', ['山东省', '河南省', '江苏省', '安徽省', '北京市',
                             '天津市', '上海市', '宁夏回族自治区']),
    ('Desert', '#F6EACB', ['新疆维吾尔自治区']),
    ('Semi-desert', '#F3E5C4', ['甘肃省']),
    ('Plateau desert', '#F0E4C9', ['西藏自治区']),
    ('Alpine forest grassland', '#E3E5D6', ['青海省']),
    ('Alpine meadow', '#DAE3DB', ['四川省']),
    ('Subtropical shrubland', '#DEE6D6', ['云南省', '贵州省', '重庆市', '广西壮族自治区',
                                          '湖南省', '江西省', '福建省', '浙江省',
                                          '湖北省']),
    ('Tropical forest shrubland', '#D7E4D3', ['广东省', '海南省', '台湾省']),
]
ZCOL = {}
for nm, col, provs in ZONES:
    for p in provs:
        ZCOL[p] = col

def fill(props):
    return ZCOL.get(props.get('name'), '#EDEBDD')

fig = plt.figure(figsize=cm2in(19, 14.5))
ax = fig.add_subplot(111)
china_map(ax, facecolor_fn=fill, edgecolor='#FFFFFF', lw=0.5,
          extent=(76, 133, 17, 54))

# 经纬网 + 标注
for lon in [90, 100, 110, 120]:
    ax.plot([np.radians(lon)] * 2, [mercator(0, 17)[1], mercator(0, 54)[1]],
            color='#C8C8C8', lw=0.4, zorder=2)
    ax.text(np.radians(lon), mercator(0, 17.6)[1], u'%d\u00b0 E' % lon, fontsize=6,
            ha='center', va='bottom', color='#555555', zorder=8,
            bbox=dict(fc='white', ec='none', pad=0.5))
for lat in [30, 40, 50]:
    ax.plot([np.radians(76), np.radians(133)], [mercator(0, lat)[1]] * 2,
            color='#C8C8C8', lw=0.4, zorder=2)
    ax.text(np.radians(131.9), mercator(0, lat)[1] + 0.015, u'%d\u00b0 N' % lat,
            fontsize=6, ha='right', va='bottom', color='#555555', zorder=8,
            bbox=dict(fc='white', ec='none', pad=0.5))

# 省名(灰)
PROV = [('Heilongjiang', 127.8, 48.3), ('Jilin', 126.3, 43.3), ('Liaoning', 122.3, 40.8),
        ('Xinjiang', 84.5, 41.5), ('Xizang', 87.5, 31.2), ('Qinghai', 96.2, 35.4),
        ('Gansu', 100.2, 38.2), ('Inner Mongolia', 111.5, 44.5), ('Ningxia', 106.0, 37.2),
        ('Shaanxi', 109.3, 35.2), ('Shanxi', 112.3, 37.4), ('Hebei', 115.8, 38.9),
        ('Henan', 113.4, 33.6), ('Shandong', 118.4, 36.3), ('Jiangsu', 119.6, 33.2),
        ('Anhui', 117.0, 31.8), ('Sichuan', 102.4, 30.4), ('Yunnan', 101.2, 24.8),
        ('Guizhou', 106.8, 26.8), ('Hunan', 111.4, 27.4), ('Hubei', 112.4, 30.9),
        ('Jiangxi', 115.7, 27.4), ('Zhejiang', 120.2, 29.1), ('Guangxi', 108.4, 24.2),
        ('Guangdong', 113.4, 23.4), ('Fujian', 118.4, 26.1), ('Taiwan', 121.2, 23.8)]
for nm, lon, lat in PROV:
    ax.text(np.radians(lon), mercator(lon, lat)[1], nm, fontsize=5.6,
            ha='center', va='center', color='#9A9A9A', zorder=4)

# ---------------------------------------------------------------- 蜱属采样饼图
GENUS = [('Haemaphysalis', '#5FBFAE'), ('Rhipicephalus', '#6B7FA8'),
         ('Dermacentor', '#2B3A6B'), ('Ixodes', '#C4161C'),
         ('Hyalomma', '#5E35A3'), ('Amblyomma', '#3B6BD4'),
         ('Alveonasus', '#8B1A1A'), ('Argas', '#F2A0A0')]
W_REG = {'NE': [4, 2, 3, 2.5, 0.5, 1, 0.4, 0.3], 'N': [3, 2, 2, 1.5, 1, 1, 0.5, 0.3],
         'S': [4, 2.5, 0.8, 0.8, 0.3, 0.6, 0.3, 0.5], 'W': [1.2, 1.5, 1.5, 0.6, 3, 2.5, 1.5, 0.6]}
PICKS = [(124.5, 49.5, 'NE'), (127.5, 47.5, 'NE'), (130.5, 45.2, 'NE'), (126.5, 45.0, 'NE'),
         (123.0, 42.8, 'NE'), (119.8, 50.0, 'NE'), (125.0, 43.6, 'NE'), (129.0, 44.4, 'NE'),
         (116.5, 42.5, 'N'), (113.0, 44.0, 'N'), (108.0, 40.5, 'N'), (117.5, 40.0, 'N'),
         (112.0, 36.0, 'N'), (106.5, 35.0, 'N'), (114.5, 35.5, 'N'), (110.0, 34.0, 'N'),
         (118.0, 30.5, 'S'), (112.5, 29.0, 'S'), (107.0, 26.0, 'S'), (103.5, 26.0, 'S'),
         (110.5, 21.5, 'S'), (116.0, 25.5, 'S'), (108.5, 22.8, 'S'), (114.0, 27.5, 'S'),
         (87.0, 43.5, 'W'), (82.5, 41.0, 'W'), (88.0, 36.5, 'W'), (94.0, 36.0, 'W'),
         (101.5, 33.0, 'W'), (96.5, 30.0, 'W'), (118.5, 39.5, 'N'), (121.5, 38.8, 'N')]
# 先按原顺序取样(保持随机序列与饼的构成不变), 再做位置避让:
# 重叠饼对沿连线互相推开 + 弱弹簧拉回原址, 迭代至不相交;
# 位移大的饼画细引线指回真实采样点(密集区自动"引线展开/微移避让")
PIES = []
for lon, lat, reg in PICKS:
    n = int(r117.integers(1, 55))
    fr = r117.dirichlet(np.array(W_REG[reg]))
    x, y = mercator(lon, lat)
    PIES.append([x, y, np.radians(0.10 + 0.27 * np.sqrt(n)), fr, lon, lat])

GAP = 0.006
for _ in range(200):
    moved = False
    for i in range(len(PIES)):
        for j in range(i + 1, len(PIES)):
            xi, yi, ri = PIES[i][:3]
            xj, yj, rj = PIES[j][:3]
            d = np.hypot(xi - xj, yi - yj)
            if d < ri + rj + GAP:
                if d < 1e-9:
                    ux, uy = 1.0, 0.0
                else:
                    ux, uy = (xi - xj) / d, (yi - yj) / d
                push = (ri + rj + GAP - d) / 2 + 1e-4
                PIES[i][0] += ux * push
                PIES[i][1] += uy * push
                PIES[j][0] -= ux * push
                PIES[j][1] -= uy * push
                moved = True
    for p in PIES:                          # 弱弹簧: 限制漂移, 就近避让
        hx, hy = mercator(p[4], p[5])
        p[0] += (hx - p[0]) * 0.04
        p[1] += (hy - p[1]) * 0.04
    if not moved:
        break

for x, y, rad, fr, lon, lat in PIES:
    hx, hy = mercator(lon, lat)
    d = np.hypot(x - hx, y - hy)
    if d > max(rad, 0.010):                 # 明显移出原址: 细引线指回采样点
        ux, uy = (x - hx) / d, (y - hy) / d
        ax.plot([hx, x - rad * ux], [hy, y - rad * uy], lw=0.5,
                color='#666666', zorder=7)
        ax.plot([hx], [hy], marker='o', ms=1.6, color='#666666', zorder=7)
    start = 90.0
    for (_lab, col), f in zip(GENUS, fr):
        sweep = 360.0 * f
        ax.add_patch(Wedge((x, y), rad, start, start + sweep, width=rad,
                           facecolor=col, edgecolor='white', lw=0.3, zorder=6))
        start += sweep

# ---------------------------------------------------------------- 图例: Tick genus(左上)
ax.text(0.015, 0.985, 'Tick genus', transform=ax.transAxes, fontsize=8, va='top')
for k_i, (nm, col) in enumerate(GENUS):
    yy = 0.952 - k_i * 0.026
    ax.text(0.020, yy, '\u25a0', fontsize=6, color=col, transform=ax.transAxes,
            va='center')
    ax.text(0.035, yy, nm, transform=ax.transAxes, fontsize=6.2, va='center',
            style='italic')

# 图例: Number of tick samples(顶部中间, 双列同心圆)
ax.text(0.415, 0.99, 'Number of tick samples', transform=ax.transAxes, fontsize=8,
        va='top')
vals = [1, 5, 10, 20, 40, 60]
for k_i, v in enumerate(vals):
    col_i, row_i = k_i % 2, k_i // 2
    cx = 0.445 + col_i * 0.075
    cy = 0.925 - row_i * 0.048
    r = 0.011 + 0.020 * np.sqrt(v / 60.0)
    ax.add_patch(Circle((cx, cy), r, transform=ax.transAxes, facecolor='none',
                        edgecolor='#777777', lw=0.6, zorder=11))
    ax.text(cx + 0.022, cy, str(v), transform=ax.transAxes, fontsize=6.2,
            va='center', zorder=11)

# 图例: Ecological fauna(左下)
ax.text(0.015, 0.42, 'Ecological fauna', transform=ax.transAxes, fontsize=8, va='top')
for k_i, (nm, col, _p) in enumerate(ZONES):
    yy = 0.388 - k_i * 0.026
    ax.text(0.020, yy, '\u25a0', fontsize=6, color=col, transform=ax.transAxes,
            va='center')
    ax.text(0.035, yy, nm, transform=ax.transAxes, fontsize=6.2, va='center')

# ---------------------------------------------------------------- 指北针(右上)
nx, ny, nr = 0.945, 0.955, 0.030
ax.add_patch(Circle((nx, ny), nr, transform=ax.transAxes, facecolor='white',
                    edgecolor='#555555', lw=0.7, zorder=11))
ax.add_patch(plt.Polygon([[nx, ny + nr * 0.85], [nx - nr * 0.28, ny - nr * 0.3],
                          [nx, ny]], closed=True, transform=ax.transAxes,
                         facecolor='#B0B0B0', edgecolor='black', lw=0.4, zorder=12))
ax.add_patch(plt.Polygon([[nx, ny + nr * 0.85], [nx + nr * 0.28, ny - nr * 0.3],
                          [nx, ny]], closed=True, transform=ax.transAxes,
                         facecolor='#C4161C', edgecolor='black', lw=0.4, zorder=12))
ax.text(nx, ny - nr * 1.5, 'N', transform=ax.transAxes, fontsize=7,
        ha='center', va='top', zorder=12)

# ---------------------------------------------------------------- 南海诸岛插图
axi = fig.add_axes([0.815, 0.065, 0.125, 0.22])
china_map(axi, facecolor_fn=lambda p: '#FBFAF2', edgecolor='#AAAAAA', lw=0.4,
          extent=(104, 123, 2, 24))
axi.add_patch(Rectangle((0, 0), 1, 1, transform=axi.transAxes, facecolor='none',
                        edgecolor='#888888', lw=0.6, zorder=10))
axi.tick_params(labelleft=False, labelbottom=False)

save(fig, 'case_seg117.png')
