# -*- coding: utf-8 -*-
"""案例94 - Nature 半圆形小提琴图: 180 度弧上 11 组径向小提琴 + 白色小箱线。
参考: frames/seg_092.jpg — 内孔留白, 外侧彩色类目标签 + 中位数标注, 径向轴 0-4。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import set_style, save, cm2in

import numpy as np
import matplotlib.pyplot as plt

set_style()

# (名称, 颜色, 中位数标注值)
groups = [
    ('SARS-CoV-2',            '#2D2E5F', 422.4),
    ('SARS-CoV-2 Delta',      '#3E6DB5', 290.9),
    ('SARS-CoV-2 Beta',       '#2E9E6B', 235.0),
    ('SARS-CoV-2 Mu',         '#45386B', 221.2),
    ('SARS-CoV-2\nOmicron BA.1', '#E8823A', 58.6),
    ('SARS-CoV-2\nOmicron BA.2', '#C4342B', 87.5),
    ('Bat CoV',               '#8B84C3', 311.8),
    ('Pangolin CoV GL',       '#29A8D8', 291.5),
    ('Bat CoV RaTG13',        '#E06A5A', 233.1),
    ('Pangolin',              '#1F9E89', 130.3),
    ('SARS',                  '#E8823A', 19.8),
]
G = len(groups)
RSCALE = 0.42          # 径向坐标 = RSCALE × log2(ID50 滴度)
RMAX, HOLE = 4.45, -1.15


def r_of(titer):
    """滴度 → 径向坐标, 使径向刻度直接读出 log2 滴度。"""
    return RSCALE * np.log2(titer)

fig = plt.figure(figsize=cm2in(15.5, 15.0))
ax = fig.add_subplot(projection='polar')
ax.set_theta_zero_location('W')
ax.set_theta_direction(-1)
ax.set_thetamin(0)
ax.set_thetamax(180)
ax.set_rorigin(HOLE)
ax.set_ylim(0, RMAX)
tk = np.array([0, 2, 4, 6, 8, 10])     # 径向刻度 = log2(ID50)
ax.set_yticks(tk * RSCALE)
ax.set_yticklabels([''] * len(tk))   # 数字改画在半盘下缘之外, 防遮挡
ax.set_rlabel_position(0)
ax.set_xticks([])
ax.set_thetamin(0)
ax.set_thetamax(180)
ax.spines['polar'].set_visible(True)
ax.spines['polar'].set_linewidth(0.9)
ax.grid(True, axis='y', color='#D9D9D9', lw=0.5)
ax.grid(False, axis='x')
ax.tick_params(pad=-22)

rng = np.random.default_rng(92)
step = 180.0 / G
rs = np.linspace(0.30, 4.42, 160)

for i, (name, color, med) in enumerate(groups):
    tc = np.radians((i + 0.5) * step)              # 组中心角
    half = np.radians(step * 0.36)                 # 最大半宽
    rp = float(np.clip(r_of(med), 1.2, 3.72))
    sig = rng.uniform(0.38, 0.55)
    kde = (np.exp(-0.5 * ((rs - rp) / sig) ** 2)
           + 0.38 * np.exp(-0.5 * ((rs - rp * 0.45) / (sig * 1.4)) ** 2))
    kde = kde / kde.max()
    th = np.concatenate([tc - half * kde, (tc + half * kde)[::-1]])
    ax.fill(th, np.concatenate([rs, rs[::-1]]), color=color, alpha=0.9,
            lw=0.4, edgecolor=color, zorder=3)
    # 白色小箱线
    q1, q3 = rp - 0.62 * sig, rp + 0.52 * sig
    med_r = rp - 0.08 * sig
    bw = half * 0.22
    bx = [tc - bw, tc + bw, tc + bw, tc - bw, tc - bw]
    by = [q1, q1, q3, q3, q1]
    ax.fill(bx, by, color='white', ec='#666666', lw=0.6, zorder=4)
    ax.plot([tc - bw, tc + bw], [med_r, med_r], color='#333333', lw=1.0,
            zorder=5)
    # 中位数标注(沿径向旋转): 统一外移到尾尖之外, 与类目标签分层(不同半径带);
    # 顶部大提琴尾尖顶到类目带时, 数值角度错开 8 度, 避开类目标签
    tdeg = (i + 0.5) * step
    rot = 90 - tdeg
    lr = rp + 3.1 * sig + 0.38
    t_v = tdeg
    if lr > 3.78:
        t_v = tdeg + 8.0
        lr = min(lr, 4.32)
    ax.text(np.radians(t_v), lr, '%.1f' % med, rotation=90 - t_v,
            rotation_mode='anchor', ha='center', va='center',
            fontsize=6.5, color='#222222', zorder=6)
    # 外侧类目标签
    name_r = 4.72 + (0.55 if i in (1, 3, 8) else 0.0)
    ax.text(np.radians(tdeg), name_r, name, rotation=rot,
            rotation_mode='anchor', ha='center', va='center',
            fontsize=7, color=color, fontweight='bold', zorder=6)

# 径向刻度数字与轴题画在半盘下缘之外(theta<0, 不裁剪), 避免被小提琴遮挡
for v in tk:
    ax.text(np.radians(-4), v * RSCALE, str(v), ha='center', va='center',
            fontsize=9, zorder=10, clip_on=False)
ax.text(np.radians(-12), 2.3, 'Log$_2$ ID$_{50}$ neutralization titer',
        ha='center', va='top', fontsize=8.5, zorder=10, clip_on=False)
# 外圈数字含义说明
fig.text(0.5, 0.028,
         'Outer labels: group median ID$_{50}$ neutralization titer',
         ha='center', va='bottom', fontsize=8.5)

save(fig, 'case_seg092.png')
