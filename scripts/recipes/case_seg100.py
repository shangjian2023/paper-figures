# -*- coding: utf-8 -*-
"""案例102 - ES&T 环状条形图: 38 个代表城市 CPUG 值环形柱, 正值蓝/负值红黄渐变,
中心竖直色条, 右侧径向刻度, 标签切向旋转置于外圈。
参考: frames/seg_100.jpg。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import set_style, save, cm2in

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

set_style()

cities = ['Dezhou', 'Gongqing', 'Jiaxing', 'Wenzhou', 'Huzhou', 'Shengzhou',
          'Zhengzhou', 'Karamay', 'Liaoyang', 'Anshan', 'Suqian', 'Yinchuan',
          'Yancheng', 'Nantong', 'Xiamen', 'Kunming', 'Suzhou', 'Rizhao',
          'Hangzhou', 'Shaoxing', 'Nanning', 'Fuyang', 'Luoyang', 'Ningbo',
          'Fuzhou', 'Shangqiu', 'Chengdu', 'Jining', 'Baoji', 'Lianyungang',
          'Handan', 'Shantou', 'Qinhuangdao', 'Quanzhou', 'Zhangzhou',
          'Nanyang', 'Nanjing', 'Jiaxian']
N = len(cities)

rng = np.random.default_rng(100)
v = rng.normal(0.15, 0.95, N).clip(-1.95, 1.95)
v[np.argmax(v)] = 1.98                      # Dezhou 最强
v[np.argmin(v)] = -1.85                     # Jiaxian 最弱
order = np.argsort(-v)                      # 降序, 自东逆时针排布
cities = [cities[i] for i in order]
v = v[order]

step = 360.0 / (N + 1)          # 东侧留 1 个空档放径向轴
theta_deg = (90 - (np.arange(N) + 1.5) * step) % 360
th = np.radians(theta_deg)

norm = Normalize(-2, 2)
cmap = plt.get_cmap('RdYlBu')

fig = plt.figure(figsize=cm2in(16.5, 17.0))
ax = fig.add_subplot(projection='polar')
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_ylim(-2.2, 2.35)
ax.set_rorigin(-2.75)
ax.set_yticks([-2, -1, 0, 1, 2])
ax.set_yticklabels(['\u22122', '\u22121', '0', '1', '2'], fontsize=7)
ax.set_rlabel_position(90)
ax.set_xticks([])
ax.set_thetamin(0)
ax.set_thetamax(360)
ax.spines['polar'].set_visible(False)
ax.patch.set_visible(False)
ax.set_frame_on(False)
ax.grid(False)
ax.tick_params(pad=-6)

w = np.radians(step * 0.80)
for i in range(N):
    if v[i] >= 0:
        ax.bar(th[i], v[i], width=w, bottom=0, color=cmap(norm(v[i])),
               ec='none', zorder=3)
        tip = v[i]
    else:
        ax.bar(th[i], -v[i], width=w, bottom=v[i],
               color=cmap(norm(v[i])), ec='none', zorder=3)
        tip = 0.0
    tdeg = theta_deg[i]
    rot = -tdeg if tdeg <= 90 or tdeg > 270 else 180 - tdeg
    # 标签统一放外圈固定半径, 切向旋转, 隔一根错位防重叠; 外圈 ylim 留白保证不出画布
    rr = 2.06 if i % 2 == 0 else 2.19
    ax.text(th[i], rr, cities[i], rotation=rot,
            rotation_mode='anchor', ha='center', va='center', fontsize=4.6,
            color='#333333', zorder=5)

# 基线虚线圈(0 值)
tbase = np.linspace(0, 2 * np.pi, 721)
ax.plot(tbase, np.zeros_like(tbase), color='#999999', lw=0.7,
        ls=(0, (4, 3)), zorder=2)

# 中心竖直色条
cax = fig.add_axes([0.4925, 0.40, 0.010, 0.20])
sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
sm.set_array([])
cb = fig.colorbar(sm, cax=cax)
cb.set_ticks([-2, -1, 0, 1, 2])
cb.ax.tick_params(labelsize=6, length=2, pad=1)
cb.outline.set_visible(False)
cax.text(-1.6, 0.5, 'CPUG (K)', transform=cax.transAxes, rotation=90,
         ha='center', va='center', fontsize=8)

save(fig, 'case_seg100.png')
