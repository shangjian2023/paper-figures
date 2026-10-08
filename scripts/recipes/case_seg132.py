# -*- coding: utf-8 -*-
"""案例134 - Nature 点线图: 普通版 vs 顶刊版 上下对比。
参考: frames/seg_132.jpg — 上面板 Plain(线性 x, 16 条杂色曲线密集重叠无图例);
下面板 Polished(log x, 16 条温度曲线 52K-100K 彩虹着色, 空心/实心点交替 +
平滑实线, 右侧外置图例), 面板间紫色过渡注记, y=Molar Volume。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

set_style()

temps = np.linspace(52, 100, 16)
cmap = plt.get_cmap('rainbow')
cols = [cmap(1.0 - i / (len(temps) - 1)) for i in range(len(temps))]


def volume(logf, i):
    """介电弛豫式摩尔体积色散曲线: 低温高->低下降, 高温低->平台上升。"""
    frac = i / (len(temps) - 1)
    fc = 10 ** (-0.55 + 3.1 * frac)         # 驰豫频率随温度大幅右移
    v_low = 0.062 - 0.058 * frac            # 低频端体积随温度降低
    v_high = 0.004 + 0.024 * frac           # 高频平台随温度升高
    m = 0.92
    y = v_high + (v_low - v_high) / (1 + (10 ** logf / fc) ** m)
    if frac < 0.35:                         # 低温低频上翘尖峰
        y = y + (0.35 - frac) * 0.030 * np.exp(-logf / 0.22)
    if 0.30 < frac < 0.78:                  # 中温宽包驼峰
        h = 0.006 * np.sin(np.pi * (frac - 0.30) / 0.48)
        y = y + h * np.exp(-((logf - np.log10(fc) - 1.1) / 0.9) ** 2)
    return y


flog = np.linspace(-1, 3, 200)
fpts = 10 ** np.linspace(-1, 3, 25)

fig = plt.figure(figsize=cm2in(16.0, 19.0))
gs = fig.add_gridspec(2, 1, height_ratios=[1, 1.1], hspace=0.42,
                      top=0.97, bottom=0.06)

# ---- 上面板: Plain 线性 x, 密集杂色 ----
ax1 = fig.add_subplot(gs[0])
for s in ax1.spines.values():
    s.set_visible(True)
for i in range(len(temps)):
    ax1.plot(10 ** flog, volume(flog, i) + 0.0012 * np.sin(i * 2.1),
             color=cols[i], lw=1.1, alpha=0.85)
ax1.set_xlim(-30, 1030)
ax1.set_ylim(-0.002, 0.065)
ax1.set_xticks([0, 250, 500, 750, 1000])
ax1.set_yticks([0, 0.02, 0.04, 0.06])
ax1.set_xlabel('Frequency (Hz)')
ax1.set_ylabel('Molar Volume (cm$^3$ mol$^{-1}$)')

# ---- 过渡注记 ----
fig.text(0.55, 0.485, 'Plain  ->  publication-grade polish', ha='center', va='center',
         color='#C333D1', fontsize=12, fontweight='bold', style='italic')

# ---- 下面板: Polished log x, 彩彩虹点线 + 外置图例 ----
ax2 = fig.add_subplot(gs[1])
for s in ax2.spines.values():
    s.set_visible(True)
handles = []
for i, T in enumerate(temps):
    xx = 10 ** flog
    yy = volume(flog, i)
    ax2.plot(xx, yy, '-', color=cols[i], lw=1.3, zorder=2)
    hollow = (i % 2 == 0)
    ax2.plot(fpts, volume(np.log10(fpts), i), 'o', ms=3.6,
             mfc='white' if hollow else cols[i], mec=cols[i],
             mew=0.9, ls='none', zorder=3)
    handles.append(Line2D([], [], marker='o', ms=4, color=cols[i],
                          mfc='white' if hollow else cols[i],
                          label='%dK' % round(T)))
ax2.legend(handles=handles, bbox_to_anchor=(1.015, 0.5), loc='center left',
           fontsize=6.5, handlelength=0.8, handletextpad=0.5,
           labelspacing=0.55, frameon=False)
ax2.set_xscale('log')
ax2.set_xlim(0.1, 1000)
ax2.set_ylim(0, 0.065)
ax2.set_xticks([1e-1, 1e0, 1e1, 1e2, 1e3])
ax2.set_yticks([0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06])
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Molar Volume (cm$^3$ mol$^{-1}$)')

save(fig, 'case_seg132.png')
