# -*- coding: utf-8 -*-
"""案例150 - 氨基酸位点突变能量热图。
57位点×20氨基酸主热图(绿-白-红 -2.0~2.94) + 顶部横向色标(数值刻度竖排)
+ 热图上叠加位点平均能量折线(黑虚线+红/蓝圆点, 右轴) + 零虚线。
参考: frames/seg_145.jpg。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

set_style()

AA = list('VYWTS PFMKLIHGEQCDNRA'.replace(' ', ''))   # y 轴自上而下
n_site = 57
r = rng(145)

# 位点标签: 氨基酸字母+编号
letters = list('ACDEFGHIKLMNPQRSTVWY')
nums = r.choice(np.arange(10, 285), n_site, replace=False)
sites = [f'{letters[i % 20]}{nums[i]}' for i in range(n_site)]

# 能量矩阵: 大面积浅色 + 少量纵向红色条纹
E = r.normal(0.05, 0.34, (20, n_site))
col_off = r.normal(0.0, 0.22, n_site).clip(-0.35, 0.35)
E += col_off[None, :]
for _ in range(14):                          # 零散强正/负点
    E[r.integers(0, 20), r.integers(0, n_site)] = r.uniform(1.6, 2.7) * r.choice([-1, 1])
E[15:20, 33:40] += r.uniform(1.0, 2.4, (5, 7))       # C/D/N/R/A 区红色条带
E[15:20, 34:39] += r.uniform(0.8, 1.8, (5, 5))
E[0:3, 47:51] += r.uniform(1.0, 2.2, (3, 4))         # V/Y/W 区红条
E[0, 8:12] += r.uniform(1.0, 2.0, 4)
E[5:8, 20:23] -= r.uniform(1.0, 2.0, (3, 3))         # 少量深绿
E[10:13, 50:54] -= r.uniform(1.0, 2.2, (3, 4))
E = E.clip(-2.0, 2.94)

cmap = LinearSegmentedColormap.from_list(
    'gwr', ['#004b12', '#1f9c46', '#8fd481', '#d7f0c2', '#f9fcf0',
            '#fbdcb4', '#ef9264', '#d2402e', '#a80f0f'])

fig = plt.figure(figsize=cm2in(18.5, 14.5))
ax = fig.add_axes([0.115, 0.115, 0.735, 0.565])
im = ax.imshow(E, aspect='auto', cmap=cmap, vmin=-2.0, vmax=2.94,
               interpolation='nearest')
ax.set_yticks(np.arange(20))
ax.set_yticklabels(AA, fontsize=6.5)
ax.set_xticks(np.arange(n_site))
ax.set_xticklabels(sites, rotation=90, fontsize=4.3)
ax.tick_params(length=2, pad=1.5)
for s in ax.spines.values():
    s.set_linewidth(0.9)
ax.set_ylabel('Mutation sites', fontsize=8.5)

# 叠加: 位点平均能量 (右轴)
ax2 = ax.twinx()
means = E.mean(axis=0)
ax2.plot(np.arange(n_site), means, '--', color='black', lw=0.8, zorder=4)
ax2.scatter(np.arange(n_site), means, c=['#e8194b' if m > 0 else '#2a3bef'
                                         for m in means], s=11, zorder=5)
ax2.axhline(0, ls='--', color='0.25', lw=0.7, zorder=3)
ax2.set_ylim(-0.62, 1.05)
ax2.set_yticks([-0.6, -0.3, 0, 0.3, 0.6, 0.9])
ax2.tick_params(labelsize=6.5, length=2)
ax2.set_ylabel('Average mutation energy\n(binding, Kcal/mol)', fontsize=8)
for s in ax2.spines.values():
    s.set_visible(False)

# ------------------------------------------------ 顶部横向色标 (数值竖排)
cax = fig.add_axes([0.115, 0.755, 0.735, 0.032])
cb = fig.colorbar(im, cax=cax, orientation='horizontal')
ticks = np.linspace(-2.0, 2.94, 13)
cb.set_ticks(ticks)
cax.xaxis.tick_top()
cax.set_xticklabels([f'{t:.2f}' for t in ticks], rotation=90, fontsize=6)
cax.tick_params(length=2, pad=1.5)
cax.set_title('Color scales of saturated mutation energy', fontsize=9, pad=21)

fig.text(0.012, 0.93, 'A', fontsize=13, fontweight='bold')

save(fig, 'case_seg145.png')
