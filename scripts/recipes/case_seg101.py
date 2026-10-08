# -*- coding: utf-8 -*-
"""案例103 - Nature 环状条形图(双系列): 青绿 MTase 面板 + 深红 Safety 面板各占半环,
径向条长=抑制值, 顶部径向刻度, 内弧彩字面板名, 标签旋转。
参考: frames/seg_101.jpg。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import set_style, save, cm2in

import numpy as np
import matplotlib.pyplot as plt

set_style()

MIN = chr(0x2212)

mtase = ['PRMT5 (C449S)', 'PRMT5/MEP50', 'PRMT6', 'PRMT50', 'DOT1L',
         'PRMT7', 'DNMT1', 'MLL3 Complex', 'PRMT8', 'G9a', 'MLL2 Complex',
         'SUV39H2', 'SMYD3', 'SET7/9', 'SUV420H1 TV2', 'PRDM9',
         'EZH2 Complex', 'SMYD2', 'PRMT4', 'SETD2', 'NSD3', 'GLP',
         'DNMT3a', 'PRMT1', 'DNMT3b', 'NSD2 (E1099K)', 'SUV39H1',
         'DNMT3b/3L', 'EZH1 Complex', 'SET8', 'ASH1L', 'MLL1 Complex',
         'NSD2 (T1150A)', 'SET1b Complex', 'NSD3', 'MLL4 Complex', 'NSD1']
safety = ['AIR', '5-HT3', 'KV channel', 'GR', 'A2A', 'CB2 (h)', 'V1a',
          'beta 1 (h)', 'D1', 'ETA', 'DAT', 'NMDA', 'delta (DOP)',
          '5-HT transporter', 'kappa (KOP)', 'beta 2 (h)', 'Ca2+ channel',
          'MAO\u2013A', 'CB1 (h)', 'H2', 'D2S', 'N neuronal alpha',
          'alpha 1A', 'M3 (h)', 'CCK1 (h)', 'hERG', 'alpha 2A',
          'BZD (central)', 'Na+ channel (site 2)', 'mu (MOP) (h)',
          '5-HT1B (h)', 'NET', '5-HT1D', '5-HT2C', '5-HT2A', '5-HT2B',
          'M1', 'M2 (h)', 'H1', '5-H T2']

rng = np.random.default_rng(101)
v_mt = rng.uniform(2, 24, len(mtase))
v_mt[0:4] = rng.uniform(-14, -3, 4)          # 顶部几个负值
v_mt[-1] = 30
v_sf = rng.uniform(3, 22, len(safety))
v_sf[0] = -16                                 # AIR 负值
for k in (-1, -2, -3, -4, -5):
    v_sf[k] = rng.uniform(30, 42)             # 底部强抑制
v_sf[-6] = 28

NT, NS = len(mtase), len(safety)
GAP = 2                                       # 顶部空档放刻度轴
step = 180.0 / (max(NT, NS) + GAP)

fig = plt.figure(figsize=cm2in(16.0, 17.0))
ax = fig.add_subplot(projection='polar')
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_ylim(-22, 46)
ax.set_rorigin(-30)
ax.set_yticks([])

ax.set_xticks([])
ax.set_thetamin(0)
ax.set_thetamax(360)
ax.spines['polar'].set_visible(False)
ax.patch.set_visible(False)
ax.grid(False)
ax.tick_params(pad=-8)

TEAL, RED = '#4C9FAd'.replace('9F', '9F'), '#B22B3A'
TEAL = '#4C9FAD'


def bar(theta_deg, val, color):
    t = np.radians(theta_deg)
    w = np.radians(step * 0.72)
    if val >= 0:
        ax.bar(t, val, width=w, bottom=0, color=color, ec='none', zorder=3)
    else:
        ax.bar(t, -val, width=w, bottom=val, color=color, ec='none',
               zorder=3)


def tangential_label(theta_deg, r, txt):
    t = np.radians(theta_deg)
    tdeg = theta_deg % 360
    rot = -tdeg if tdeg <= 90 or tdeg > 270 else 180 - tdeg
    ax.text(t, r, txt, rotation=rot, rotation_mode='anchor',
            ha='center', va='center', fontsize=4.0, color='#222222',
            zorder=5)


def radial_label(theta_deg, r0, txt):
    ax.text(np.radians(theta_deg), r0, txt, rotation=90 - theta_deg,
            rotation_mode='anchor', ha='left', va='center', fontsize=4.0,
            color='#222222', zorder=5)


# 负值柱标签沿半径书写并逐根错开半径, 消除顶部两系列交界处的叠压;
# 正值柱标签切向居中, 贪心防重叠: 与近邻角度/径向带同时相交时自动外推
recent = []                                   # (中心角, 角半宽, 中心r, 径向半带宽)


def adiff(a, b):
    d = abs(a - b) % 360.0
    return min(d, 360.0 - d)


def register_radial(theta_deg, r0, txt):
    hl = 0.55 * len(txt)
    recent.append((theta_deg % 360.0, 2.0, r0 + hl / 2.0, hl / 2.0 + 0.3))


def tangential_label(theta_deg, r0, txt):
    tdeg = theta_deg % 360.0
    half_len = 0.55 * len(txt)
    r = float(r0)
    ah = 0.0
    for _ in range(40):
        ah = np.degrees(np.arctan2(half_len, max(r, 0.5)))
        hit = False
        for pa, pah, pr, prad in recent[-10:]:
            if adiff(tdeg, pa) < ah + pah and abs(r - pr) < prad + 1.0:
                r = pr + prad + 1.0
                hit = True
        if not hit:
            break
    recent.append((tdeg, ah, r, 1.0))
    t = np.radians(theta_deg)
    rot = -tdeg if tdeg <= 90 or tdeg > 270 else 180 - tdeg
    ax.text(t, r, txt, rotation=rot, rotation_mode='anchor',
            ha='center', va='center', fontsize=4.0, color='#222222',
            zorder=5)


ni = 0
neg_r = [3.0, 10.0, 17.0, 24.0]               # 顶部 4 根负值柱标签的错开半径
for i, (name, val) in enumerate(zip(mtase, v_mt)):
    tdeg = -(i + 1 + GAP) * step              # 左半环(逆时针)
    bar(tdeg, val, TEAL)
    if val < 0:
        register_radial(tdeg, neg_r[ni], name)
        radial_label(tdeg % 360, neg_r[ni], name)
        ni += 1
    else:
        tangential_label(tdeg, val + 1.2, name)
for i, (name, val) in enumerate(zip(safety, v_sf)):
    tdeg = (i + 1 + GAP) * step               # 右半环(顺时针)
    bar(tdeg, val, RED)
    if val < 0:
        register_radial(tdeg, val - 2.0, name)
        radial_label(tdeg, val - 2.0, name)   # AIR: 从负柱尖端内侧向外读
    else:
        tangential_label(tdeg, val + 1.2, name)

# 顶部径向刻度小线 + 数字(数字统一放到刻度线左侧空档, 避开柱体)
for rr, lab in [(-20, MIN + '20'), (0, '0'), (20, '20'), (40, '40')]:
    ax.plot([0, 0], [rr - 1.2, rr + 1.2], color='#333333', lw=0.8,
            zorder=4)
    ax.text(np.radians(-2.5), rr, lab, ha='right', va='center', fontsize=8,
            color='#111111', zorder=5)

# 径向轴标题: 顶部空档 (GAP 扇区无柱体), 置于刻度轴正上方
ax.text(0, 49.5, 'Inhibition (%)', ha='center', va='bottom', fontsize=9.5,
        color='#111111', zorder=5)

# 内弧面板名(逐字沿弧)


def arc_text(text, a0_deg, a1_deg, r, color, fontsize=7.5):
    angs = np.radians(np.linspace(a0_deg, a1_deg, len(text)))
    for ch, a in zip(text, angs):
        ax.text(a, r, ch, rotation=-np.degrees(a), rotation_mode='anchor',
                ha='center', va='center', fontsize=fontsize, color=color,
                zorder=5, fontweight='bold')


arc_text('Rxn Biology MTase panel', 196, 336, -13, TEAL)
arc_text('Eurofins Safety Screen', 24, 156, -13, RED)

save(fig, 'case_seg101.png')
