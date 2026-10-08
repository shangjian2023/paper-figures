# -*- coding: utf-8 -*-
"""UpSet 图助手 — 交集条形 + 点阵 + 集合大小条。"""
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations


def upset_plot(sets, ax=None, color='#3B6E8F', dot_color='black',
               max_inter=15, fs=7):
    """sets: dict{集合名: set(元素)}。绘制 UpSet 图(交集降序前 max_inter 个)。
    返回 ax(共用 x 轴的三个区域画在同一 ax 中, 用自定义坐标)。"""
    if ax is None:
        fig, ax = plt.subplots(figsize=(7.2, 4.0))
    names = list(sets.keys())
    n = len(names)
    elems = sorted(set().union(*sets.values()))
    idx = {e: i for i, e in enumerate(elems)}
    # 所有可能交集(1..n 个集合的并型组合, 取"仅在组合内出现"的严格交集)
    inter = []
    for r in range(1, n + 1):
        for comb in combinations(range(n), r):
            s = set(sets[names[comb[0]]])
            for c in comb[1:]:
                s &= set(sets[names[c]])
            for other in range(n):
                if other not in comb:
                    s -= set(sets[names[other]])
            if s:
                inter.append((comb, len(s)))
    inter.sort(key=lambda t: -t[1])
    inter = inter[:max_inter]
    xs = np.arange(len(inter))
    # --- 顶部交集条形
    top_h = [c for _, c in inter]
    ax.bar(xs, top_h, width=0.6, color=color, zorder=3)
    for x, h in zip(xs, top_h):
        ax.text(x, h, str(h), ha='center', va='bottom', fontsize=fs - 1)
    ymax = max(top_h) * 1.18
    # --- 中部点阵
    y_of = {nm: n - 1 - i for i, nm in enumerate(names)}
    for x, (comb, _) in zip(xs, inter):
        ys = [y_of[names[c]] for c in comb]
        if len(ys) > 1:
            ax.plot([x, x], [min(ys), max(ys)], color=dot_color, lw=0.8, zorder=2)
        ax.scatter([x] * len(ys), ys, s=22, color=dot_color, zorder=3)
    # --- 左侧集合大小
    for nm in names:
        ax.barh(y_of[nm], len(sets[nm]), height=0.55, color='#BBBBBB', zorder=1)
        ax.text(len(sets[nm]), y_of[nm], ' ' + str(len(sets[nm])), va='center', fontsize=fs - 1)
    # --- 坐标伪装
    ax.set_xlim(-1.2, len(inter) + max(len(sets[nm]) for nm in names) * 0.25)
    ax.set_ylim(-0.7, n - 0.3 + ymax / (n) * 0)
    ax.set_yticks([y_of[nm] for nm in names])
    ax.set_yticklabels(names, fontsize=fs)
    ax.set_xticks([])
    for sp in ['top', 'right', 'bottom']:
        ax.spines[sp].set_visible(False)
    # 顶部条形与点阵共用 y 会被拉伸 —— 改为真双轴方案:
    return ax


def upset_plot_pro(sets, figsize=(7.2, 4.2), color='#3B6E8F', max_inter=15, fs=7,
                   shade=None):
    """三区 UpSet: 顶部交集条 / 中部点阵 / 左侧 set size 条。shade: {行:颜色} 行底纹。
    返回 (fig, ax_top, ax_mid)。"""
    from itertools import combinations as _c
    names = list(sets.keys())
    n = len(names)
    inter = []
    for r in range(1, n + 1):
        for comb in _c(range(n), r):
            s = set(sets[names[comb[0]]])
            for c in comb[1:]:
                s &= set(sets[names[c]])
            for other in range(n):
                if other not in comb:
                    s -= set(sets[names[other]])
            if s:
                inter.append((comb, len(s)))
    inter.sort(key=lambda t: -t[1])
    inter = inter[:max_inter]
    fig = plt.figure(figsize=figsize)
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 14], height_ratios=[2.2, 1.6],
                          wspace=0.03, hspace=0.04)
    ax_top = fig.add_subplot(gs[0, 1])
    ax_mid = fig.add_subplot(gs[1, 1], sharex=ax_top)
    ax_left = fig.add_subplot(gs[1, 0], sharey=ax_mid)
    xs = np.arange(len(inter))
    ax_top.bar(xs, [c for _, c in inter], width=0.62, color=color)
    for x, (_, c) in zip(xs, inter):
        ax_top.text(x, c, str(c), ha='center', va='bottom', fontsize=fs - 1)
    ax_top.set_ylim(0, max(c for _, c in inter) * 1.2)
    ax_top.set_xticks([])
    ax_top.set_ylabel('Intersection size', fontsize=fs)
    y_of = {nm: n - 1 - i for i, nm in enumerate(names)}
    if shade:
        for nm, col in shade.items():
            ax_mid.axhspan(y_of[nm] - 0.5, y_of[nm] + 0.5, color=col, alpha=0.25, lw=0)
    for x, (comb, _) in zip(xs, inter):
        ys = [y_of[names[c]] for c in comb]
        if len(ys) > 1:
            ax_mid.plot([x, x], [min(ys), max(ys)], color='k', lw=0.9, zorder=2)
        ax_mid.scatter([x] * len(ys), ys, s=24, color='k', zorder=3)
    ax_mid.set_ylim(-0.6, n - 0.4)
    ax_mid.set_yticks([y_of[nm] for nm in names])
    ax_mid.set_yticklabels([])
    ax_mid.set_xticks([])
    ax_mid.tick_params(left=False)
    sizes = [len(sets[nm]) for nm in names]
    ax_left.barh([y_of[nm] for nm in names], sizes, height=0.58, color='#9E9E9E')
    for nm in names:
        ax_left.text(len(sets[nm]) + max(sizes) * 0.03, y_of[nm], str(len(sets[nm])),
                     va='center', fontsize=fs - 1)
    ax_left.set_xlim(0, max(sizes) * 1.28)
    ax_left.set_yticks([y_of[nm] for nm in names])
    ax_left.set_yticklabels(names, fontsize=fs)
    ax_left.set_xticks([])
    for a in (ax_top, ax_mid, ax_left):
        for sp in ['top', 'right']:
            a.spines[sp].set_visible(False)
    ax_mid.spines['left'].set_visible(False)
    ax_left.spines['left'].set_visible(True)
    return fig, ax_top, ax_mid
