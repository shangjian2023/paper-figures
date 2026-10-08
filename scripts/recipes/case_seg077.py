# -*- coding: utf-8 -*-
"""案例79 - Nature 时间序列图(一): GIR 高胰岛素-正糖钳。
参考: frames/seg_077.jpg — 黑圆 Vehicle(n=6) / 金黄圆 chABC(n=5) 两线 + 误差棒,
浅紫 axvspan Basal(-15~0) 与 Clamp(90~120) 带标签, 逐点 */**, Clamp *** 横括。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt

set_style()

r = rng(77)
t_basal = np.array([-15.0, -7.5, 0.0])
t_post = np.arange(5, 121, 5, dtype=float)
t = np.concatenate([t_basal, t_post])

veh = np.concatenate([np.zeros(3), [
    17.2, 18.6, 19.2, 19.6, 20.6, 21.6, 22.1, 22.4, 22.7, 22.9, 23.0,
    23.1, 23.2, 23.2, 23.3, 23.3, 23.3, 23.4, 23.4, 23.4, 23.4, 23.4,
    23.5, 23.5]])
chabc = np.concatenate([np.zeros(3), [
    18.6, 21.2, 22.6, 24.2, 25.8, 27.0, 27.9, 28.6, 29.3, 30.0, 30.7,
    31.6, 32.6, 33.6, 34.1, 34.3, 34.4, 34.5, 34.5, 34.6, 34.6, 34.7,
    34.7, 34.7]])
sem_v = r.uniform(0.6, 1.1, t.size)
sem_c = r.uniform(0.8, 1.5, t.size)
sem_v[:3] = sem_c[:3] = 0.0

fig, ax = plt.subplots(figsize=cm2in(13.5, 12.0))

# 阶段底色
ax.axvspan(-15, 0, color='#C9C9EE', alpha=0.55, zorder=0)
ax.axvspan(90, 120, color='#C9C9EE', alpha=0.55, zorder=0)
ax.text(-7.5, 41.0, 'Basal', ha='center', va='bottom', fontsize=12)
ax.text(105, 41.0, 'Clamp', ha='center', va='bottom', fontsize=12)

ax.errorbar(t, chabc, yerr=sem_c, color='#F2C230', fmt='-o', ms=6,
            mfc='#F2C230', mec='black', mew=0.8, elinewidth=1.0,
            capsize=2.5, zorder=3)
ax.errorbar(t, veh, yerr=sem_v, color='black', fmt='-o', ms=6,
            elinewidth=1.0, capsize=2.5, zorder=4)

# 显著点上方 */**
ax.text(65, chabc[13] + sem_c[13] + 0.9, '*', ha='center', va='bottom',
        fontsize=11)
ax.text(75, chabc[15] + sem_c[15] + 0.9, '**', ha='center', va='bottom',
        fontsize=11)
# Clamp 区间 *** 横括
sig_bracket(ax, 90, 120, 38.3, '***', h=0.9, lw=1.0, fontsize=10)

ax.set_xlim(-19, 124)
ax.set_ylim(0, 44.5)
ax.set_xticks([-15, -5, 0, 20, 40, 60, 80, 100, 120])
ax.set_yticks([0, 5, 10, 15, 20, 25, 30, 35, 40])
ax.set_xlabel('Time (min)')
ax.set_ylabel('GIR (mg kg$^{-1}$ min$^{-1}$)')

ax.plot([], [], 'o', color='black', label='Vehicle ($n$ = 6)')
ax.plot([], [], 'o', color='#F2C230', mec='black', mew=0.8,
        label='chABC ($n$ = 5)')
ax.legend(loc='center left', bbox_to_anchor=(0.42, 0.40), frameon=False,
          fontsize=9, handletextpad=0.4)

save(fig, 'case_seg077.png')
