# -*- coding: utf-8 -*-
"""案例80 - Nature 时间序列图(二): cAMP 诱发荧光响应, 3 小鼠 + 均值。
参考: frames/seg_078.jpg — 上排 3 小面板(Mouse 1-3), 灰 ACSF / 橙红 SHU9119
均值线 + SEM 阴影带, 0 处黑虚线, ↑cAMP 注记; 下方 1 大面板, 面板标题。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt

set_style()

C_ACSF = '#8F8F8F'
C_SHU = '#DE5B3A'
t = np.linspace(-20, 120, 281)


def trace(r, peak, plateau, tau=26.0, t0=0.0, noise=0.006, ntrials=5):
    """t0 处快速上升, 峰值后衰减到平台; 返回 mean 与 sem。"""
    rise = 1 / (1 + np.exp(-(t - t0 - 1.5) / 1.1))
    decay = plateau + (peak - plateau) * np.exp(-np.clip(t, 0, None) / tau)
    shape = rise * decay
    trials = np.clip(shape[None, :]
                     + r.normal(0, noise, (ntrials, t.size)), 0, None)
    trials[:, t < 0] *= np.linspace(0, 1, (t < 0).sum()) * 0  # 基线为 0
    return trials.mean(0), trials.std(0, ddof=1) / np.sqrt(ntrials)


params = {  # (ACSF peak, ACSF plat, SHU peak, SHU plat)
    1: (0.135, 0.098, 0.082, 0.048),
    2: (0.125, 0.135, 0.075, 0.085),
    3: (0.100, 0.095, 0.033, 0.030),
}

fig = plt.figure(figsize=cm2in(17.0, 15.0))
gs = fig.add_gridspec(2, 3, height_ratios=[1.0, 1.15], hspace=0.5,
                      wspace=0.30)

for m in (1, 2, 3):
    ax = fig.add_subplot(gs[0, m - 1])
    r = rng(780 + m)
    pk, pl, sk, sl = params[m]
    a_m, a_s = trace(r, pk, pl)
    s_m, s_s = trace(r, sk, sl, tau=30.0)
    ax.fill_between(t, a_m - a_s, a_m + a_s, color=C_ACSF, alpha=0.30, lw=0)
    ax.plot(t, a_m, color=C_ACSF, lw=1.2)
    ax.fill_between(t, s_m - s_s, s_m + s_s, color=C_SHU, alpha=0.30, lw=0)
    ax.plot(t, s_m, color=C_SHU, lw=1.2)
    ax.axhline(0, color='black', ls='--', lw=1.0)
    ax.text(-17, -0.033, '\u2191cAMP', fontsize=8, va='bottom')
    if m == 1:
        ax.text(118, 0.140, 'ACSF', color='0.55', fontsize=9, ha='right')
        ax.text(118, 0.068, 'SHU9119', color=C_SHU, fontsize=9, ha='right')
    ax.set_xlim(-22, 124)
    ax.set_ylim(-0.05, 0.155)
    ax.set_xticks([0, 40, 80, 120])
    ax.set_yticks([0, 0.05, 0.10, 0.15])
    ax.tick_params(labelsize=7)
    ax.set_title('Hits: Mouse %d' % m, fontsize=9, pad=4)
    if m == 1:
        ax.set_ylabel('$-\\Delta$F/F$_0$', fontsize=8)
        ax.set_xlabel('Time (s)', fontsize=8)
    else:
        ax.set_xlabel('Time (s)', fontsize=8)

# ---- 下方大面板: Mouse 1 均值放大 ----
ax = fig.add_subplot(gs[1, :])
r = rng(781)
a_m, a_s = trace(r, *params[1][:2])
s_m, s_s = trace(r, params[1][2], params[1][3], tau=30.0)
ax.fill_between(t, a_m - a_s, a_m + a_s, color=C_ACSF, alpha=0.30, lw=0)
ax.plot(t, a_m, color=C_ACSF, lw=1.4)
ax.fill_between(t, s_m - s_s, s_m + s_s, color=C_SHU, alpha=0.30, lw=0)
ax.plot(t, s_m, color=C_SHU, lw=1.4)
ax.axhline(0, color='black', ls='--', lw=1.1)
ax.text(-17, -0.036, '\u2191cAMP', fontsize=10, va='bottom')
ax.text(118, 0.132, 'ACSF', color='0.55', fontsize=12, ha='right')
ax.text(118, 0.050, 'SHU9119', color=C_SHU, fontsize=12, ha='right')
ax.set_title('Hits: Mouse 1', fontsize=11, pad=5)
ax.set_xlim(-22, 124)
ax.set_ylim(-0.055, 0.155)
ax.set_xticks([0, 40, 80, 120])
ax.set_yticks([0, 0.05, 0.10, 0.15])
ax.set_ylabel('$-\\Delta$F/F$_0$')
ax.set_xlabel('Time (s)')

save(fig, 'case_seg078.png')
