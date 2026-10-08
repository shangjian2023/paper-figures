# -*- coding: utf-8 -*-
"""案例60 - Nature 圆形雷达图: 上排 5 个 22 轴小雷达 + 下方 MC5 放大面板。
参考: frames/seg_058.jpg — 彩色标题条(绿/蓝/橙/红/紫), 细线多边形+浅填充+顶点点,
显著偏离指标的轴标签着色。手算笛卡尔雷达(22 辐条, 顶部辐条无标签)。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import set_style, save, cm2in

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

set_style()

# 22 条辐条, 每 16.36 度一条; 顶部(90°)那条无标签(与参考图一致)
label_at = {106.36: 'eGFR', 73.64: 'HDL-C', 57.27: 'ApoA-1', 40.91: 'LDL-C',
            24.55: 'TC', 8.18: 'ApoB', -8.18: 'GGT', -24.55: 'ALT',
            -40.91: 'AST', -57.27: 'BMI', -73.64: 'WC', -90.0: 'Fins',
            -106.36: 'Pins', -122.73: 'TG', -139.09: 'UA',
            -155.45: 'HOMA-IR', -171.82: 'HbA1c', 171.82: 'FPG',
            155.45: 'PPG', 139.09: 'DBP', 122.73: 'SBP'}
spokes = []
for k in range(22):
    a = 90 + k * (360 / 22)
    key = np.round(((a + 180) % 360) - 180, 2)      # 归一到 (-180,180]
    spokes.append((np.radians(a), label_at.get(key)))
ang = np.array([s[0] for s in spokes])
labels = [s[1] for s in spokes]

r = np.random.default_rng(58)
base = r.uniform(0.10, 0.28, 22)


def vals(peaks):
    v = base.copy()
    for name, h in peaks.items():
        v[labels.index(name)] = h
    return v


clusters = [
    ('MC1', '#96C894', vals({})),
    ('MC2', '#85AECE', vals({'ApoA-1': 0.62})),
    ('MC3', '#F0AC78', vals({'LDL-C': 0.55, 'TC': 0.60, 'ApoB': 0.65})),
    ('MC4', '#D98484', vals({'HOMA-IR': 0.50, 'UA': 0.44, 'GGT': 0.48,
                             'ALT': 0.46, 'TG': 0.40, 'Pins': 0.38,
                             'Fins': 0.36, 'BMI': 0.35, 'WC': 0.32})),
    ('MC5', '#AC92CE', vals({'FPG': 0.90, 'PPG': 0.95, 'HbA1c': 0.74,
                             'SBP': 0.55, 'DBP': 0.38})),
]
hot = {'MC1': {}, 'MC2': {'ApoA-1': '#3B7DD8'},
       'MC3': {'LDL-C': '#E8823A', 'TC': '#E8823A', 'ApoB': '#E8823A'},
       'MC4': {k: '#C0392B' for k in ['HOMA-IR', 'UA', 'GGT', 'ALT', 'TG',
                                      'Pins', 'Fins', 'BMI', 'WC']},
       'MC5': {k: '#5E35A3' for k in ['FPG', 'PPG', 'HbA1c', 'SBP']}}

fig = plt.figure(figsize=cm2in(18.0, 16.0))


def draw_radar(rect, v, color, hotmap, lab_fs, lw, ms, lab_r=1.22, nudge=None,
               tick_fs=3.5):
    ax = fig.add_axes(rect)
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.45, 1.45)
    ax.set_aspect('equal')
    ax.axis('off')
    xs, ys = v * np.cos(ang), v * np.sin(ang)
    for t in ang:                                   # 辐条
        ax.plot([0, np.cos(t)], [0, np.sin(t)], color='#C9C9C9', lw=0.45,
                zorder=1)
    for rv in (0.25, 0.50, 0.75):                   # 标度参考环(每 0.25)
        ax.add_patch(plt.Circle((0, 0), rv, fc='none', ec='#DEDEDE', lw=0.35,
                                zorder=1))
    ax.add_patch(plt.Circle((0, 0), 1.0, fc='none', ec='#C9C9C9', lw=0.45,
                            zorder=1))
    for rv, tx in ((0.25, '0.25'), (0.5, '0.50'), (0.75, '0.75'),
                   (1.0, '1.0')):                   # 径向刻度: 顶部无标签辐条
        ax.text(0.045, rv, tx, fontsize=tick_fs, color='#8A8A8A',
                ha='left', va='center', zorder=5)
    ax.fill(xs, ys, color=color, alpha=0.30, zorder=2)
    ax.plot(np.append(xs, xs[0]), np.append(ys, ys[0]), color=color, lw=lw,
            zorder=3)
    ax.plot(xs, ys, 'o', color=color, ms=ms, zorder=4)
    for t, lab in zip(ang, labels):                 # 轴标签
        if lab is None:
            continue
        c, s = np.cos(t), np.sin(t)
        ha = 'left' if c > 0.35 else ('right' if c < -0.35 else 'center')
        va = 'bottom' if s > 0.35 else ('top' if s < -0.35 else 'center')
        col = hotmap.get(lab, '#4D4D4D')
        w = 'bold' if lab in hotmap else 'normal'
        # 逐标签微调: 角度偏移/半径偏移/水平对齐覆盖(错开底部拥挤的 TG/Pins/Fins/WC)
        d_deg, dr, ha_ovr = (nudge or {}).get(lab, (0.0, 0.0, None))
        tt = t + np.radians(d_deg)
        if ha_ovr:
            ha = ha_ovr
        c, s = np.cos(tt), np.sin(tt)
        ax.text((lab_r + dr) * c, (lab_r + dr) * s, lab, ha=ha, va=va,
                fontsize=lab_fs, color=col, fontweight=w)


# ---- 上排 5 个小雷达 --------------------------------------------------
# 底部拥挤区错峰: TG 外移+角度偏移, Pins 右对齐, WC 左对齐, UA 内移
LAB_NUDGE = {'Pins': (0.0, 0.0, 'right'), 'WC': (0.0, 0.05, 'left'),
             'UA': (0.0, -0.07, None), 'TG': (-8.0, 0.05, None)}
# 格高压缩到贴合雷达: 雷达方形区(宽 0.142×18cm) + 上下标签余量, 垂直居中
RAD_W = 0.142                          # fig 宽比例 -> 2.56 cm
RAD_H = RAD_W * 18.0 / 16.0            # 换算 fig 高比例, 保持正方形
PANEL_CY, PANEL_H = 0.785, RAD_H + 2 * 0.040
for i, (name, color, v) in enumerate(clusters):
    x0 = 0.015 + i * 0.196
    cx = x0 + 0.0945                   # 格中心
    draw_radar([cx - RAD_W / 2, PANEL_CY - RAD_H / 2, RAD_W, RAD_H],
               v, color, hot[name], 4.6, 0.9, 1.8, lab_r=1.24,
               nudge=LAB_NUDGE, tick_fs=3.5)
    # 彩色标题条 + 面板黑框(高度随雷达收紧, 雷达居中)
    fig.patches.append(Rectangle((x0 - 0.004, PANEL_CY + PANEL_H / 2), 0.197,
                                 0.045, transform=fig.transFigure, fc=color,
                                 ec='black', lw=0.8, zorder=3))
    fig.text(x0 + 0.0945, PANEL_CY + PANEL_H / 2 + 0.0225, name, ha='center',
             va='center', fontsize=10, fontweight='bold')
    fig.patches.append(Rectangle((x0 - 0.004, PANEL_CY - PANEL_H / 2), 0.197,
                                 PANEL_H, transform=fig.transFigure, fc='none',
                                 ec='black', lw=0.8, zorder=3))

# 标度说明(归一化)
fig.text(0.012, 0.984, 'Radar axes: values normalized to 0\u20131; '
         'grey rings every 0.25', fontsize=6.2, color='0.30',
         ha='left', va='top')

# ---- 下方 MC5 放大面板 ------------------------------------------------
ZOOM_H = 0.535                          # 方形边 8.56 cm
draw_radar([0.50 - ZOOM_H * 18 / 16 / 2, 0.040, ZOOM_H * 18 / 16, ZOOM_H],
           clusters[4][2], '#5E35A3', hot['MC5'], 11, 1.6, 4.5, lab_r=1.18,
           nudge=LAB_NUDGE, tick_fs=7)
fig.patches.append(Rectangle((0.245, 0.575), 0.51, 0.058,
                             transform=fig.transFigure, fc='#AC92CE',
                             ec='black', lw=1.0, zorder=3))
fig.text(0.50, 0.604, 'MC5', ha='center', va='center', fontsize=15,
         fontweight='bold')
fig.patches.append(Rectangle((0.245, 0.040), 0.51, 0.535,
                             transform=fig.transFigure, fc='none',
                             ec='black', lw=1.0, zorder=3))

save(fig, 'case_seg058.png')
