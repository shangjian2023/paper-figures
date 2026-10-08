# -*- coding: utf-8 -*-
"""案例95 - Nature 扇形箱线图: 180 度弧上 11 组 径向箱线 + 抖动散点。
参考: frames/seg_093.jpg — 浅灰同心网格, 中心留白孔, 顶部弧形彩色类目标签+中位数标注。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import set_style, save, cm2in

import numpy as np
import matplotlib.pyplot as plt

set_style()

groups = [
    ('SARS-CoV-2',                '#2D2E5F', 422.4),
    ('SARS-CoV-2 Delta',          '#3E6DB5', 290.9),
    ('SARS-CoV-2 Beta',           '#2E9E6B', 235.0),
    ('SARS-CoV-2 Mu',             '#45386B', 221.2),
    ('SARS-CoV-2\nOmicron BA.1',  '#E8823A', 58.6),
    ('SARS-CoV-2\nOmicron BA.2',  '#C4342B', 87.5),
    ('Bat CoV',                   '#8B84C3', 311.8),
    ('Pangolin CoV GL',           '#29A8D8', 291.5),
    ('Bat CoV RaTG13',            '#E06A5A', 233.1),
    ('Pangolin',                  '#1F9E89', 130.3),
    ('SARS',                      '#E8823A', 19.8),
]
G = len(groups)
RSCALE = 0.42          # 径向坐标 = RSCALE × log2(ID50 滴度)
RMAX = 4.45


def r_of(titer):
    """滴度 → 径向坐标, 使径向刻度直接读出 log2 滴度。"""
    return RSCALE * np.log2(titer)

fig = plt.figure(figsize=cm2in(15.5, 15.0))
ax = fig.add_subplot(projection='polar')
ax.set_theta_zero_location('W')
ax.set_theta_direction(-1)
ax.set_thetamin(0)
ax.set_thetamax(180)
ax.set_rorigin(-1.15)
ax.set_ylim(0, RMAX)
tk = np.array([0, 2, 4, 6, 8, 10])     # 径向刻度 = log2(ID50)
ax.set_yticks(tk * RSCALE)
ax.set_yticklabels([''] * len(tk))   # 数字改画在半盘下缘之外, 防遮挡
ax.set_rlabel_position(0)
ax.set_xticks([])
ax.set_thetamin(0)
ax.set_thetamax(180)
ax.spines['polar'].set_linewidth(0.9)
ax.grid(True, axis='y', color='#DDDDDD', lw=0.5)
ax.grid(False, axis='x')
ax.tick_params(pad=-26)

rng = np.random.default_rng(93)
step = 180.0 / G

for i, (name, color, med) in enumerate(groups):
    tdeg = (i + 0.5) * step
    tc = np.radians(tdeg)
    half = np.radians(step * 0.40)
    rp = float(np.clip(r_of(med), 1.2, 3.72))
    sig = rng.uniform(0.34, 0.52)
    n = rng.integers(28, 46)
    rr = rng.normal(rp, sig, n)
    rr = rr[(rr > 0.30) & (rr < 4.05)]   # 上界留出中位数标注带
    tj = tc + rng.uniform(-0.72, 0.72, len(rr)) * half
    ax.plot(tj, rr, 'o', color=color, ms=2.6, alpha=0.9, zorder=3)
    # 径向箱线(白底灰边)
    q1, q3 = np.percentile(rr, [25, 75])
    med_r = np.median(rr)
    lo, hi = np.percentile(rr, [5, 95])
    bw = half * 0.26
    ax.plot([tc, tc], [lo, hi], color='#888888', lw=0.8, zorder=4)
    bx = [tc - bw, tc + bw, tc + bw, tc - bw, tc - bw]
    by = [q1, q1, q3, q3, q1]
    ax.fill(bx, by, color='white', ec='#777777', lw=0.7, zorder=5)
    ax.plot([tc - bw, tc + bw], [med_r, med_r], color='#333333', lw=1.1,
            zorder=6)
    # 中位数标注 + 外侧类目标签
    rot = 90 - tdeg
    lr = min(4.32, hi + 0.30)
    ax.text(np.radians(tdeg), lr, '%.1f' % med, rotation=rot,
            rotation_mode='anchor', ha='center', va='center',
            fontsize=6.5, color='#222222', zorder=6)
    name_r = 4.72 + (0.55 if i in (1, 3, 8) else 0.0)
    ax.text(tc, name_r, name, rotation=rot, rotation_mode='anchor',
            ha='center', va='center', fontsize=7, color=color,
            fontweight='bold', zorder=6)

# 径向刻度数字与轴题画在半盘下缘之外(theta<0, 不裁剪), 避免被散点遮挡
# (与案例092 同源同语义)
for v in tk:
    ax.text(np.radians(-4), v * RSCALE, str(v), ha='center', va='center',
            fontsize=9, zorder=10, clip_on=False)
ax.text(np.radians(-12), 2.3, 'Log$_2$ ID$_{50}$ neutralization titer',
        ha='center', va='top', fontsize=8.5, zorder=10, clip_on=False)
# 外圈数字含义说明
fig.text(0.5, 0.028,
         'Outer labels: group median ID$_{50}$ neutralization titer',
         ha='center', va='bottom', fontsize=8.5)

save(fig, 'case_seg093.png')
