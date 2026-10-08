# -*- coding: utf-8 -*-
"""案例97 - Nature 环状折线图: 4 组线带圆点标记沿 29 个代表性指标环形排布,
径向 -1.5~+1.5, 中心白圆分区注释, 右上图例。
参考: frames/seg_095.jpg。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import set_style, save, cm2in

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle

set_style()

cats = [
    ('Mental\nquality\nof life',
     ['SF8_mentalcomp*', 'SF8_mentalhlt*', 'SF8_roleemot*'], 0.9),
    ('Tinnitus\ncharacteristics',
     ['TINSKAL_freq', 'TINSKAL_loudness', 'TLQ_botheread', 'TLQ_hissing'],
     -0.1),
    ('Physical\nquality\nof life',
     ['SF8_overallhlt*', 'SF8_physcomp*', 'SF8_rolephys*'], 0.8),
    ('Experiences\nof pain',
     ['SES_affectivepain', 'SSKAL_painfreq*', 'SSKAL_painsev*'], 0.6),
    ('Somatic\nexpressions',
     ['BI_abdsymptoms', 'BI_fatigue', 'BI_overallcompl'], 0.7),
    ('Affective\nsymptoms',
     ['ADSL_depression', 'BSF_anxidepr*', 'BSF_fatigue'], 0.7),
    ('Tinnitus-\nrelated\ndistress',
     ['ISR_depression*', 'ISR_anxiety*', 'ISR_totalpsych*',
      'PHOK_panicsyn*'], 0.8),
    ('Internal\nresources',
     ['TQ_distress*', 'TQ_intrusiveness', 'TQ_cogdistress'], -0.2),
    ('Perceived\nstress',
     ['ACSA_qol*', 'PSQ_stress', 'SWOP_optimism*'], 0.4),
]
metrics, cat_mid = [], []
for cname, names, _ in cats:
    metrics += names
    cat_mid.append((cname, len(metrics) - len(names) / 2 - 0.5, len(names)))
N = len(metrics)

groups = [
    ('PT 1: avoidant\ngroup (n=697)', '#3182BD',
     [0.05, -0.25, 0.15, -0.05, 0.05, -0.15, -0.45, -0.35, -0.25]),
    ('PT 2: psychosomatic\ngroup (n=173)', '#D95F02',
     [1.05, 0.25, 0.95, 0.85, 0.95, 1.05, 1.15, 0.35, 0.75]),
    ('PT 3: somatic\ngroup (n=185)', '#E8B33A',
     [0.25, 0.15, 0.35, 0.95, 1.05, 0.55, 0.35, 0.05, 0.35]),
    ('PT 4: distress\ngroup (n=171)', '#D77FB4',
     [0.45, 0.05, 0.35, 0.55, 0.55, 0.75, 0.85, -0.05, 0.25]),
]

rng = np.random.default_rng(95)
prof = np.concatenate([np.full(len(n), off) for _, n, off in
                       [(c, nm, o) for c, nm, o in cats]])
Z = np.clip(rng.normal(0, 0.16, (4, N)) + prof, -1.45, 1.45)

R0, RORG = -1.75, -5.0
SPAN = 2.00 - RORG


def frac(r):                      # 数据 r -> 屏幕半径占比
    return (r - RORG) / SPAN


step = 360.0 / N
th = np.radians(np.arange(N) * step)

fig = plt.figure(figsize=cm2in(17.0, 17.5))
ax = fig.add_subplot(projection='polar')
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_ylim(-2.70, 2.00)
ax.set_rorigin(RORG)
ax.set_yticks([-1.5, -1.0, -0.5, 0, 0.5, 1.0, 1.5])
ax.set_yticklabels(['−1.5', '−1.0', '−0.5', '0', '+0.5',
                    '+1.0', '+1.5'], fontsize=6)
# 径向刻度移到数据低洼处的柱间空隙(耳鸣特征区, 约56度), 避开折线数据点
k_gap = 4
ax.set_rlabel_position((k_gap + 0.5) * step)
ax.set_xticks([])
ax.set_thetamin(0)
ax.set_thetamax(360)
ax.spines['polar'].set_visible(False)
ax.patch.set_visible(False)
ax.grid(True, axis='y', color='#C8C8C8', lw=0.5, ls=(0, (3, 3)))
ax.grid(False, axis='x')
ax.tick_params(pad=5)

# 中心白圆 + 分区刻痕 + 类目文字
disk_r = frac(-1.75) * 0.5
ax.add_patch(Circle((0.5, 0.5), disk_r, transform=ax.transAxes, fc='white',
                    ec='black', lw=1.1, zorder=10, clip_on=False))
k = 0
for cname, _, cnt in cat_mid:
    tb = np.radians(k * step)
    ax.plot([tb, tb], [-1.75, -1.58], color='black', lw=0.8, zorder=11)
    tmid = np.radians((k + cnt / 2) * step)
    ax.text(tmid, -2.45, cname, ha='center', va='center', fontsize=4.4,
            color='#3A3A3A', linespacing=1.1, zorder=11)
    k += cnt

# 4 组环形折线
for j, (lab, color, _) in enumerate(groups):
    ax.plot(th, Z[j], '-', color=color, lw=1.1, zorder=6)
    ax.plot(th, Z[j], 'o', color=color, ms=2.6, zorder=7)

# 外圈指标标签: 统一半径, 切向旋转, 隔一根错位防重叠
for i in range(N):
    tdeg = np.degrees(th[i])
    rot = -tdeg if tdeg <= 90 or tdeg > 270 else 180 - tdeg
    rr = 1.66 if i % 2 == 0 else 1.84
    ax.text(th[i], rr, metrics[i], rotation=rot,
            rotation_mode='anchor', ha='center', va='center', fontsize=4.1,
            color='#6E6E6E', zorder=12)

# 右上图例
handles = [Line2D([], [], color=c, marker='o', ms=4, lw=1.2) for _, c, _ in
           groups]
fig.legend(handles, [g[0] for g in groups], loc='upper right',
           bbox_to_anchor=(0.995, 0.99), frameon=False, fontsize=6.3,
           labelspacing=1.1, handlelength=1.4, borderaxespad=0)

save(fig, 'case_seg095.png')
