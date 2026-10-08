# -*- coding: utf-8 -*-
"""案例132 - Nature 配对相关矩阵(R版): 7×7, 对角=变量名, 上三角=r值着色方块
(jet, 0.1~0.8)+数值, 下三角=散点+2D KDE 等高线, 右侧竖色标。
参考: frames/seg_130.jpg。"""
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
# 上三角 r 值 (同参考图)
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
vmin, vmax = 0.1, 0.8
norm = plt.Normalize(vmin, vmax)

# 各变量取值范围
lo = np.zeros(n)
hi = np.array([5.0, 5.0, 5.0, 40.0, 4.0, 5.0, 3.0])

def make_pair(i, j):
    """相关为 R[i,j] 的双变量样本, 边际按各变量量程缩放"""
    rho = R[i, j]
    z = np.random.default_rng(1300 + 10 * i + j).normal(0, 1, (2, 600))
    zx, zy = z[0], rho * z[0] + np.sqrt(1 - rho ** 2) * z[1]
    x = 0.5 * (lo[j] + hi[j]) + zx * (hi[j] - lo[j]) / 3.6
    y = 0.5 * (lo[i] + hi[i]) + zy * (hi[i] - lo[i]) / 3.6
    return (np.clip(x, lo[j], hi[j]), np.clip(y, lo[i], hi[i]))

L, B, W = 0.135, 0.075, 0.70
fig_h = 15.6
H = W * (16.0 / fig_h)              # 保证格子等比
fig = plt.figure(figsize=cm2in(16.0, fig_h))
cw, ch = W / n, H / n
shrink = 0.87                        # 面板留缝, 刻度文字不重叠

sq = fig.add_axes([L, B, W, H])
sq.set_xlim(0, n); sq.set_ylim(n, 0)
sq.axis('off')

# 上三角: r 值方块 + 数值; 对角: 变量名
for i in range(n):
    for j in range(n):
        if j > i:
            sq.add_patch(plt.Rectangle((j, i), 1, 1, facecolor=cmap(norm(R[i, j])),
                                       edgecolor='none'))
            sq.text(j + 0.5, i + 0.5, f'{R[i, j]:.2f}', ha='center', va='center',
                    fontsize=9.5)
        elif i == j:
            sq.text(j + 0.5, i + 0.45, labels[i], ha='center', va='center',
                    fontsize=10.5)

# 下三角: 散点 + 2D KDE; 刻度只在最左列/最底行
for i in range(1, n):
    for j in range(i):
        x0 = L + j * cw + cw * (1 - shrink) / 2
        y0 = B + (n - 1 - i) * ch + ch * (1 - shrink) / 2
        ax = fig.add_axes([x0, y0, cw * shrink, ch * shrink])
        x, y = make_pair(i, j)
        ax.scatter(x, y, s=1.2, c='0.55', alpha=0.35, linewidths=0)
        kde = gaussian_kde(np.vstack([x, y]))
        gx, gy = np.mgrid[lo[j]:hi[j]:60j, lo[i]:hi[i]:60j]
        zz = kde(np.vstack([gx.ravel(), gy.ravel()])).reshape(gx.shape)
        ax.contourf(gx, gy, zz, levels=8, cmap='jet')
        ax.set_xlim(lo[j], hi[j]); ax.set_ylim(lo[i], hi[i])
        for s in ax.spines.values():
            s.set_linewidth(0.8)
        ax.set_xticks([]); ax.set_yticks([])
        ax.tick_params(length=2, pad=1.0, labelsize=5.5)
        if i == n - 1:
            ax.set_xticks([0, hi[j] * (0.5 if hi[j] > 8 else 1.0)])
            ax.set_xticklabels(['0', f'{hi[j] if hi[j] <= 8 else 20:g}'])
        if j == 0:
            ax.set_yticks([0, hi[i]])
            ax.set_yticklabels(['0', f'{hi[i]:g}'])

# 右侧竖色标
cax = fig.add_axes([0.88, 0.30, 0.028, 0.42])
fig.colorbar(plt.cm.ScalarMappable(norm, cmap), cax=cax,
             ticks=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
cax.tick_params(labelsize=7)
cax.set_ylabel('Spearman correlation', fontsize=8.5)

save(fig, 'case_seg130.png')
