# -*- coding: utf-8 -*-
"""案例109 - Cell 三角分割热图: 上三角%active(黑红橙黄), 下三角%repressed(黑蓝绿),
白色对角线, 白点=显著, 右侧双色标。
参考: frames/seg_107.jpg — TF×TF 大方阵, 轴标签旋转。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

set_style()

tfs = ['Cdx4', 'Foxa1', 'Ctcf', 'Cebpe', 'Nfix', 'Zbtb7a', 'Rxrg', 'Tcf12',
       'Meis2', 'Pbx1', 'Meis1', 'Runx1', 'Gli1b', 'Gfi1', 'Tfap2a', 'Ikzf1',
       'Tcf3', 'Nr2c2', 'Gata2', 'Myc', 'Creb1', 'Gata1', 'Irf7', 'Lyl1',
       'Myb', 'Cic', 'Yy1', 'Mecom', 'Spdef', 'Nfkb1', 'Fos', 'Sp1',
       'Stat5a', 'Klf1', 'Ddit3', 'Klf14', 'Nfyc', 'Fli1', 'Trp53', 'Elk1']
n = len(tfs)
r = rng(107)

# % active: 列>行 半区(x 反转后显示为上三角), 越靠下越亮
act = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        if j > i:
            depth = (j - i) / n                 # 离对角线深度
            base = 14 + 88 * (i / n) ** 1.1 * (1 - 0.35 * depth)
            act[i, j] = np.clip(base + r.normal(0, 15), 0, 100)
        else:
            act[i, j] = np.nan
act = act.clip(0, 100)

# % repressed: 列<行 半区(x 反转后显示为下三角), 大部分低值, 少量亮点
rep = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        if j < i:
            rep[i, j] = r.uniform(0, 1) ** 2.2 * 22
        else:
            rep[i, j] = np.nan
rep[27, 8] = 29; rep[27, 9] = 26           # Mecom 行的绿色高值
rep[20, 9] = 30; rep[2, 1] = 27; rep[12, 13] = 25

p_a = r.uniform(0, 1, (n, n)); p_a[0, :] = 0.1     # 左下显著性多
p_r = r.uniform(0, 1, (n, n))

cmap_act = LinearSegmentedColormap.from_list(
    'pact', ['#000000', '#2b0502', '#67000d', '#a81a06', '#d94d10',
             '#f07d1a', '#f9b13a', '#fee032'])
cmap_act = cmap_act.with_extremes(bad=(1, 1, 1, 0))  # 掩蔽区透明, 保留另一半三角
cmap_rep = LinearSegmentedColormap.from_list(
    'prep', ['#000000', '#0c2f6e', '#2166ac', '#4d94c8', '#8ec2dc',
             '#5cc06a', '#00e04d'])
cmap_rep = cmap_rep.with_extremes(bad=(1, 1, 1, 0))

fig = plt.figure(figsize=cm2in(17.0, 17.5))
ax = fig.add_axes([0.155, 0.045, 0.66, 0.86])
m_act = np.ma.masked_invalid(act)
m_rep = np.ma.masked_invalid(rep)
ax.imshow(m_act, cmap=cmap_act, vmin=0, vmax=100, interpolation='nearest')
ax.imshow(m_rep, cmap=cmap_rep, vmin=0, vmax=30, interpolation='nearest')
ax.set_xticks(np.arange(n))
ax.set_yticks(np.arange(n))
ax.set_xticklabels(tfs, rotation=90, fontsize=5.2)
ax.set_yticklabels(tfs, fontsize=5.2)
ax.xaxis.tick_top()
ax.invert_xaxis()                        # 对角白带右上->左下, %active 上三角 / %repressed 下三角
ax.tick_params(length=1.5, pad=1.5)
for s in ax.spines.values():
    s.set_color('0.3')

# 显著白点
yy, xx = np.where((p_a < 0.16) & ~np.isnan(act))
ax.scatter(xx, yy, s=2.5, c='white', zorder=3)
yy, xx = np.where((p_r < 0.13) & ~np.isnan(rep))
ax.scatter(xx, yy, s=2.5, c='white', zorder=3)

# ------------------------------------------------ 右侧双色标
cax1 = fig.add_axes([0.86, 0.62, 0.028, 0.26])
fig.colorbar(plt.cm.ScalarMappable(plt.Normalize(0, 100), cmap_act),
             cax=cax1, ticks=[0, 25, 50, 75, 100])
cax1.set_title('% active', fontsize=8, loc='left', pad=5)
cax1.tick_params(labelsize=7)

cax2 = fig.add_axes([0.86, 0.26, 0.028, 0.26])
fig.colorbar(plt.cm.ScalarMappable(plt.Normalize(0, 30), cmap_rep),
             cax=cax2, ticks=[0, 10, 20, 30])
cax2.set_title('% repressed', fontsize=8, loc='left', pad=5)
cax2.tick_params(labelsize=7)

save(fig, 'case_seg107.png')
