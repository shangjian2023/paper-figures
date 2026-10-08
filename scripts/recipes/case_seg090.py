# -*- coding: utf-8 -*-
"""案例92 - Cell 蝴蝶状&堆积柱形图: 镜像 100% 堆积条形 × 24 行。
参考: frames/seg_090.jpg — 灰 No Signal / 紫×2 Off-target / 橙×2 Mixed /
绿×2 On-target 七类; 中央彩色行名, 两端计数数字, 右侧图例。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

set_style()

# (行名, 行名颜色, 左计数, 右计数)
rows = [
    ('L2–3_IT',      '#59A14F', 29, 7),
    ('L4_IT',        '#4E79A7', 18, 11),
    ('L5_IT',        '#79706E', 13, 3),
    ('L5_ET',        '#4E79A7', 69, 7),
    ('L5–6_NP',      '#59A14F', 22, 21),
    ('L6_IT',        '#B6992D', 11, 0),
    ('L6_IT_Car3',   '#4E79A7', 47, 0),
    ('L6_CT',        '#4E79A7', 39, 0),
    ('L6b',          '#79706E', 38, 0),
    ('Lamp5',        '#E377C2', 30, 7),
    ('Lamp5_Lhx6',   '#FF9D9A', 22, 4),
    ('Pax6',         '#FABFD2', 14, 1),
    ('Sncg',         '#4E79A7', 35, 5),
    ('Vip',          '#4E79A7', 42, 7),
    ('Sst_Chrdi',    '#F1CE63', 42, 6),
    ('Sst',          '#E15759', 15, 19),
    ('Pvalb',        '#E15759', 21, 23),
    ('Pvalb_ChC',    '#D37295', 24, 5),
    ('Astro',        '#BAB0AC', 38, 11),
    ('Micro_PVM',    '#79706E', 17, 4),
    ('OPC',          '#9C755F', 3, 1),
    ('Oligo',        '#76B7B2', 16, 16),
    ('VLMC',         '#76B7B2', 10, 1),
    ('Endo',         '#76B7B2', 28, 0),
]
cats = ['No Signal', 'Off-target_Low', 'Off-target_High', 'Mixed_Low',
        'Mixed_High', 'On-target_Low', 'On-target_High']
cat_cols = ['#F2F2F0', '#C7A5DC', '#6A3D9A', '#FDD9A6', '#E67E22',
            '#8CD17D', '#38761D']

r = rng(90)
n = len(rows)


STYLE_BASE = {
    # 'none' 几乎全 No Signal / 'off' 富 Off-target_Low / 'mix' 混合 /
    # 'onL'、'onR' 富 On-target
    'none': np.array([96, 1, 0.5, 1, 0.5, 1, 0]),
    'off':  np.array([8, 78, 6, 2, 5, 1, 0]),
    'mix':  np.array([30, 14, 8, 10, 20, 10, 8]),
    'onL':  np.array([28, 10, 4, 6, 8, 18, 26]),
    'onR':  np.array([12, 6, 3, 4, 6, 30, 39]),
}


def allocate(n_exp, style):
    """把 n_exp 个实验整数分配到 7 类, 返回各类实验数 (和 = n_exp)。
    条形段宽 = 计数/n_exp×100, 保证堆叠构成与端部计数同源自洽:
    n=0 → 全 0 (不画条); n=1 → 主导类 1 个实验 = 100% 单段。"""
    if n_exp <= 0:
        return np.zeros(7, dtype=int)
    if n_exp == 1:
        k = np.zeros(7, dtype=int)
        k[int(np.argmax(STYLE_BASE[style]))] = 1
        return k
    p = STYLE_BASE[style] * r.normal(1, 0.22, 7)
    p = np.clip(p, 0, None)
    return r.multinomial(n_exp, p / p.sum())


# 每行风格: 左 onL / 右 (count=0 → none; VLMC → off; else onR)
left_style = ['onL'] * n
left_style[19] = 'mix'   # Micro_PVM
right_style = []
for nm, col, lc, rc in rows:
    if rc == 0:
        right_style.append('none')
    elif nm == 'VLMC':
        right_style.append('off')
    else:
        right_style.append('onR')

ys = np.arange(n)[::-1]
fig, (axL, axM, axR) = plt.subplots(
    1, 3, figsize=cm2in(21, 17), sharey=True,
    gridspec_kw={'width_ratios': [1.1, 0.55, 1.1], 'wspace': 0.0})

order = [0, 1, 2, 3, 4, 5, 6]  # 绘图次序: No Signal 最外 → On-target_High 贴 0
draw_order = [6, 5, 4, 3, 2, 1, 0]

for ax, style_list, sign in ((axL, left_style, -1), (axR, right_style, 1)):
    for y, (nm, col, lc, rc), st in zip(ys, rows, style_list):
        k = allocate(lc if sign < 0 else rc, st)
        if k.sum() == 0:          # 该侧计数为 0 → 不画条
            continue
        comp = k / k.sum() * 100.0
        left = 0.0
        for j in draw_order:
            if comp[j] > 0:
                ax.barh(y, sign * comp[j], left=sign * left, height=0.80,
                        color=cat_cols[j], lw=0, zorder=3)
            left += comp[j]
    ax.set_xlim(-104 if sign < 0 else -1, 1 if sign < 0 else 104)
    ax.set_ylim(-0.9, n - 0.1)
    despine(ax, left=True, bottom=False)
    ax.tick_params(left=True, labelleft=False, length=3)

axL.set_xticks([-100, -80, -60, -40, -20, 0])
axL.set_xticklabels(['100', '80', '60', '40', '20', '0'])
axR.set_xticks([0, 20, 40, 60, 80, 100])

# 端部计数数字(条形外端之外, 参考 Figure 布局)
for y, (nm, col, lc, rc) in zip(ys, rows):
    axL.text(-106, y, str(lc), ha='right', va='center', fontsize=8, clip_on=False)
    axR.text(106, y, str(rc), ha='left', va='center', fontsize=8, clip_on=False)

axM.set_xlim(0, 1)
axM.set_ylim(-0.9, n - 0.1)
axM.axis('off')
for y, (nm, col, lc, rc) in zip(ys, rows):
    axM.text(0.5, y, nm, ha='center', va='center', fontsize=7.5, color=col)

# x 轴标题放在两面板 '0' 刻度标签下方 ≥20pt 处(刻度标签底缘约 y=0.093)
fig.text(0.46, 0.040, 'Fraction of experiments (%)', ha='center', va='center',
         fontsize=9)

leg = axR.legend(handles=[Patch(fc=c, label=nm) for nm, c in zip(cats, cat_cols)],
                 loc='center left', bbox_to_anchor=(1.10, 0.45), frameon=False,
                 fontsize=8, handlelength=1.4, handleheight=1.2, labelspacing=0.7)

fig.subplots_adjust(left=0.055, right=0.87, top=0.975, bottom=0.125)
save(fig, 'case_seg090.png')
