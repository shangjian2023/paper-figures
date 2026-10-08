# -*- coding: utf-8 -*-
"""案例133 - Nature 配对相关矩阵(Python版): 同 R 版布局, 但每个子图带刻度,
jet 色标 0.1~0.8, 上三角色块带黑色边框, 下三角彩色密度散点。
参考: frames/seg_131.jpg。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

set_style()

labels = [r'sp$^{4+}$', r'spd$^{3+}$', r'CoH$^{3+}$', 'PEG',
          r'Ca$^{2+}$', r'HP1$\alpha$', 'HP1$\\beta$\n+tSUV']
R = np.array([
    [0.00, 0.67, 0.69, 0.60, 0.45, 0.29, 0.25],
    [0.67, 0.00, 0.72, 0.60, 0.45, 0.31, 0.26],
    [0.69, 0.72, 0.00, 0.64, 0.45, 0.35, 0.31],
    [0.60, 0.60, 0.64, 0.00, 0.41, 0.29, 0.24],
    [0.45, 0.45, 0.45, 0.41, 0.00, 0.26, 0.22],
    [0.29, 0.31, 0.35, 0.29, 0.26, 0.00, 0.66],
    [0.25, 0.26, 0.31, 0.24, 0.22, 0.66, 0.00]])
n = 7
cmap = plt.get_cmap('jet')
norm = plt.Normalize(0.1, 0.8)

lo = np.zeros(n)
hi = np.array([5.0, 5.0, 5.0, 40.0, 4.0, 5.0, 3.0])

def make_pair(i, j):
    rho = R[i, j]
    z = np.random.default_rng(1310 + 10 * i + j).normal(0, 1, (2, 600))
    zx, zy = z[0], rho * z[0] + np.sqrt(1 - rho ** 2) * z[1]
    x = 0.5 * (lo[j] + hi[j]) + zx * (hi[j] - lo[j]) / 3.6
    y = 0.5 * (lo[i] + hi[i]) + zy * (hi[i] - lo[i]) / 3.6
    return (np.clip(x, lo[j], hi[j]), np.clip(y, lo[i], hi[i]))

L, B, W = 0.13, 0.075, 0.70
fig_h = 15.6
H = W * (16.0 / fig_h)
fig = plt.figure(figsize=cm2in(16.0, fig_h))
cw, ch = W / n, H / n
shrink = 0.86          # 缩小子图占格比例 -> 增大子图间距, 防底行刻度标签互碰

sq = fig.add_axes([L, B, W, H])
sq.set_xlim(0, n); sq.set_ylim(n, 0)
sq.axis('off')

# 上三角: 带黑框的 r 值方块 + 数值; 对角: 变量名
for i in range(n):
    for j in range(n):
        if j > i:
            sq.add_patch(plt.Rectangle((j, i), 1, 1, facecolor=cmap(norm(R[i, j])),
                                       edgecolor='black', linewidth=0.9))
            sq.text(j + 0.5, i + 0.5, f'{R[i, j]:.2f}', ha='center', va='center',
                    fontsize=9.5)
        elif i == j:
            sq.text(j + 0.5, i + 0.45, labels[i], ha='center', va='center',
                    fontsize=10.5)

# 下三角: 密度散点; 每个子图都有刻度, 数字仅最左列/最底行
for i in range(1, n):
    for j in range(i):
        x0 = L + j * cw + cw * (1 - shrink) / 2
        y0 = B + (n - 1 - i) * ch + ch * (1 - shrink) / 2
        ax = fig.add_axes([x0, y0, cw * shrink, ch * shrink])
        x, y = make_pair(i, j)
        kde = gaussian_kde(np.vstack([x, y]))
        gx, gy = np.mgrid[lo[j]:hi[j]:60j, lo[i]:hi[i]:60j]
        zz = kde(np.vstack([gx.ravel(), gy.ravel()])).reshape(gx.shape)
        ax.scatter(x, y, s=2.0, c='0.6', alpha=0.30, linewidths=0)
        ax.contourf(gx, gy, zz, levels=8, cmap='jet')
        ax.set_xlim(lo[j], hi[j]); ax.set_ylim(lo[i], hi[i])
        for s in ax.spines.values():
            s.set_linewidth(0.8)
        xt = np.linspace(lo[j], hi[j], 3)
        yt = np.linspace(lo[i], hi[i], 3)
        ax.set_xticks(xt); ax.set_yticks(yt)
        ax.set_xticklabels([]); ax.set_yticklabels([])
        ax.tick_params(length=2.4, width=0.7, direction='out', pad=1.2)
        if i == n - 1:
            xt = [lo[j], hi[j]]          # 底行仅留首末 2 个刻度, %g 整数/一位小数
            ax.set_xticks(xt)
            ax.set_xticklabels(['%g' % v for v in xt], fontsize=5.5)
            xl = ax.get_xticklabels()
            xl[0].set_ha('left'); xl[-1].set_ha('right')
        if j == 0:
            ax.set_yticklabels([f'{v:.1f}' for v in yt], fontsize=5.5)
            yl = ax.get_yticklabels()
            yl[0].set_va('bottom'); yl[-1].set_va('top')

# 右侧竖色标
cax = fig.add_axes([0.88, 0.30, 0.028, 0.42])
fig.colorbar(plt.cm.ScalarMappable(norm, cmap), cax=cax,
             ticks=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
cax.tick_params(labelsize=7)
cax.set_ylabel('Spearman correlation', fontsize=8.5)

save(fig, 'case_seg131.png')
