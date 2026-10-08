# -*- coding: utf-8 -*-
"""案例82 - Nature 时间序列图(四): 事件对齐 ΔF/F。
参考: frames/seg_080.jpg — 棕褐 4 weeks HPD 与紫 Fasted 两均值线 +
半透明置信带, 0 与 10 s 两条灰虚线夹事件窗(淡灰 axvspan), 图例右上。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt

set_style()

r = rng(80)
t = np.linspace(-20, 30, 401)
G = lambda x, mu, s: np.exp(-((x - mu) / s) ** 2)

# 棕褐 4 weeks HPD
hpd = (2.0 + 3.3 * G(t, -5, 3.4) - 0.9 * G(t, 4.5, 2.4)
       + 0.9 * G(t, 11.5, 3.0) - 0.7 * G(t, 16, 2.0) + 2.0 * G(t, 25, 3.4)
       + 0.20 * np.convolve(r.normal(0, 1, t.size), np.ones(5) / 5, 'same'))
# 紫 Fasted
fas = (1.0 + 1.5 * G(t, -12, 2.5) - 3.6 * G(t, 5, 3.0)
       + 1.3 * G(t, 14, 3.0) + 2.9 * G(t, 25, 2.4) - 0.6 * G(t, 19, 2.0)
       + 0.20 * np.convolve(r.normal(0, 1, t.size), np.ones(5) / 5, 'same'))

band_h = 0.55 + 0.45 * np.abs(np.sin(t / 2.5)) + 0.25 * G(t, -5, 4)
band_f = 0.60 + 0.50 * np.abs(np.sin(t / 3.0 + 1)) + 0.25 * G(t, 25, 4)

fig, ax = plt.subplots(figsize=cm2in(13.5, 11.0))

# 事件窗: 0 与 10 s 两条灰虚线 + 淡灰底
ax.axvspan(0, 10, color='0.55', alpha=0.08, lw=0, zorder=0)
for xv in (0, 10):
    ax.axvline(xv, color='0.35', ls='--', lw=1.2, zorder=1)

ax.fill_between(t, hpd - band_h, hpd + band_h, color='#C8A165', alpha=0.28,
                lw=0, zorder=1)
ax.plot(t, hpd, color='#B08D4F', lw=1.5, zorder=3)
ax.fill_between(t, fas - band_f, fas + band_f, color='#8A6FC8', alpha=0.28,
                lw=0, zorder=1)
ax.plot(t, fas, color='#5B2C8D', lw=1.5, zorder=3)

from matplotlib.lines import Line2D
ax.legend([Line2D([], [], color='#B08D4F', lw=2),
           Line2D([], [], color='#5B2C8D', lw=2)],
          ['4 weeks HPD', 'Fasted'], loc='upper right', frameon=False,
          fontsize=9.5, handlelength=1.4)

ax.set_xlim(-21, 31)
ax.set_ylim(-4, 8)
ax.set_xticks([-20, -10, 0, 10, 20, 30])
ax.set_yticks([-4, -2, 0, 2, 4, 6, 8])
ax.set_xlabel('Time (s)')
ax.set_ylabel(r'$\Delta F/F$ (%)')

save(fig, 'case_seg080.png')
