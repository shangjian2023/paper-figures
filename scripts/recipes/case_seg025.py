# -*- coding: utf-8 -*-
"""案例25 - Nature 堆叠云雨图: 上半 KDE 山脊 + 箱线 + 下挂灰色雨滴。
参考: frames/seg_025.jpg — 5 区域, X=kyr BP 反转 15→0。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

set_style()

regions = ['Western Europe', 'Central/Eastern Europe', 'Southern Europe',
           'Northern Europe', 'Central/Western Asia']
colors = ['#A9C6E0', '#CDBE96', '#20B888', '#D42A2E', '#1A1A1A']

r = rng(25)
# 每区域年代样本 (kyr BP), 范围与参考轴 0-15 对齐
d_WE = np.concatenate([r.normal(3.4, 1.7, 320).clip(0.3, 9),
                       r.normal(12.5, 1.2, 30).clip(10.5, 14.6)])
d_CE = np.concatenate([r.normal(4.0, 2.1, 330).clip(0.4, 10.5),
                       r.normal(11.5, 1.5, 40).clip(9, 14.8)])
d_SE = r.normal(4.5, 2.7, 380).clip(0.3, 14.9)
d_NE = np.concatenate([r.normal(2.0, 1.2, 330).clip(0.2, 5.5),
                       r.normal(6.5, 2.8, 60).clip(2, 14.5)])
d_AS = np.concatenate([r.normal(9.8, 0.9, 160).clip(7.5, 12.5),
                       r.normal(12.8, 0.7, 25).clip(11, 14.2)])
samples = [d_WE, d_CE, d_SE, d_NE, d_AS]

fig, ax = plt.subplots(figsize=cm2in(15.5, 11.0))
nreg = len(regions)
for i, (name, d) in enumerate(zip(regions, samples)):
    yc = nreg - 1 - i          # 第一行在最上
    ridge_y = yc + 0.34        # KDE 山脊基线
    box_y = yc                 # 箱线所在线
    k = gaussian_kde(d)
    xs = np.linspace(0.05, 15, 300)
    dens = k(xs)
    dens = dens / dens.max() * 0.30
    ax.fill(xs, ridge_y + dens, color=colors[i], lw=0, zorder=2)
    ax.plot(xs, ridge_y + dens, color=colors[i], lw=0.6, zorder=3)
    # 箱线 (横向, 扁平)
    ax.boxplot(d, positions=[box_y], widths=0.15, orientation='horizontal',
               whis=(0, 100), patch_artist=True,
               boxprops=dict(facecolor='white', edgecolor='black', lw=1.0),
               medianprops=dict(color='black', lw=2.4),
               whiskerprops=dict(color='black', lw=0.9),
               capprops=dict(color='black', lw=0.9),
               showfliers=False, zorder=4, manage_ticks=False)
    # 下挂雨滴: 灰色短竖线
    rng_i = rng(700 + i)
    xj = d + rng_i.normal(0, 0.05, len(d))
    h = rng_i.uniform(0.05, 0.17, len(d))
    for x, hh in zip(xj, h):
        ax.plot([x, x], [box_y - 0.09, box_y - 0.09 - hh], color='#9A9A9A',
                lw=0.4, alpha=0.65, zorder=1)
    # 区域名 (左上)
    ax.text(15.35, yc + 0.30, name, ha='left', va='center', fontsize=10.5)

ax.set_xlim(15.4, -0.4)        # 反转: 15 在左, 0 在右
ax.set_ylim(-0.85, nreg - 0.30)
ax.set_xticks(np.arange(15, -1, -1))
ax.set_yticks([])
ax.set_xlabel('kyr BP', fontsize=10)
ax.tick_params(axis='x', labelsize=9)
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

save(fig, 'case_seg025.png')
