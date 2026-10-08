# -*- coding: utf-8 -*-
"""paper_style — 期刊级科研绘图全局风格 + 常用助手。

所有配方脚本统一:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    from paper_style import *
    set_style()
    ...画图...
    save(fig, 'case_segNNN.png')
"""
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.pyplot as _plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
GALLERY = os.path.join(ROOT, 'gallery')
os.makedirs(GALLERY, exist_ok=True)

# ---------------------------------------------------------------- 调色板
PALETTES = {
    # Nature 经典: 黑 + 绿
    'nature':    ['#000000', '#2E8B57', '#77B549', '#4DAF4C', '#1B9E77', '#8D8D8D'],
    'nature2':   ['#3B7DD8', '#E15759', '#59A14F', '#F28E2B', '#B07AA1', '#9C755F'],
    'science':   ['#C0392B', '#2C5F8A', '#E67E22', '#16A085', '#7D3C98', '#7F8C8D'],
    'cell':      ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F', '#EDC948',
                  '#B07AA1', '#FF9DA7', '#9C755F', '#BAB0AC'],
    'macaron':   ['#AED6F1', '#F5B7B1', '#D5F5E3', '#FCF3CF', '#E8DAEF', '#FDEBD0'],
    'rdbu':      ['#67001F', '#B2182B', '#D6604D', '#F4A582', '#FDDBC7', '#F7F7F7',
                  '#D1E5F0', '#92C5DE', '#4393C3', '#2166AC', '#053061'],
    'set3':      ['#8DD3C7', '#FFFFB3', '#BEBADA', '#FB8072', '#80B1D3', '#FDB462',
                  '#B3DE69', '#FCCDE5', '#BC80BD', '#CCEBC5'],
    'tab20':     ['#4E79A7', '#A0CBE8', '#F28E2B', '#FFBE7D', '#59A14F', '#8CD17D',
                  '#B6992D', '#F1CE63', '#499894', '#86BCB6', '#E15759', '#FF9D9A',
                  '#79706E', '#BAB0AC', '#D37295', '#FABFD2', '#B07AA1', '#D4A6C8',
                  '#9D7660', '#D7B5A6'],
    'muted':     ['#8C8C8C', '#3B6E8F', '#7FA6B8', '#C98A2D', '#5E8A5E', '#A25B5B'],
    'div_purple': ['#7B4EA3', '#AF7AC5', '#D7BDE2', '#F4ECF7', '#A9DFBF', '#58D68D', '#1E8449'],
    'warm_cool': ['#3465A8', '#6FA8DC', '#9FC5E8', '#C9DAF8', '#FCE5CD', '#F6B26B', '#E69138'],
}


def pal(name='nature', n=None):
    """取调色板; n 超出时循环。"""
    c = PALETTES[name]
    if n is None:
        return list(c)
    return [c[i % len(c)] for i in range(n)]


# ---------------------------------------------------------------- 全局样式
def set_style(scale=1.0):
    """期刊风格 rcParams。单栏宽 3.5in, 双栏 7.2in; 字号 7-9pt。"""
    matplotlib.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
        'font.size': 8 * scale,
        'axes.titlesize': 9 * scale,
        'axes.labelsize': 8 * scale,
        'xtick.labelsize': 7 * scale,
        'ytick.labelsize': 7 * scale,
        'legend.fontsize': 7 * scale,
        'axes.linewidth': 0.8,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.axisbelow': True,
        'xtick.direction': 'out',
        'ytick.direction': 'out',
        'xtick.major.width': 0.8,
        'ytick.major.width': 0.8,
        'xtick.major.size': 3,
        'ytick.major.size': 3,
        'lines.linewidth': 1.2,
        'lines.markersize': 4,
        'legend.frameon': False,
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
        'savefig.facecolor': 'white',
        'svg.fonttype': 'none',
        'axes.unicode_minus': False,
    })


def despine(ax, left=False, bottom=True):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    if not left:
        ax.spines['left'].set_visible(False)
    if not bottom:
        ax.spines['bottom'].set_visible(False)


def save(fig, name, dpi=300, dirs=None):
    """保存到 gallery/(或指定 dirs, 自动创建)并关闭 figure。"""
    out_dir = dirs or GALLERY
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, name)
    fig.savefig(out, dpi=dpi, bbox_inches='tight', facecolor='white')
    _plt.close(fig)
    print('saved:', out)
    return out


def rng(seed):
    return np.random.default_rng(seed)


# ---------------------------------------------------------------- 显著性标注
def sig_bracket(ax, x1, x2, y, text='*', h=None, lw=0.9, fontsize=8, color='black'):
    """在 (x1,x2) 两分类上方画显著性横线 + 星号/文字。y 为横线高度。"""
    if h is None:
        h = (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.02
    ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=lw, c=color)
    ax.text((x1 + x2) / 2, y + h * 1.1, text, ha='center', va='bottom',
            fontsize=fontsize, color=color)


def p_to_stars(p):
    if p < 0.001:
        return '***'
    if p < 0.01:
        return '**'
    if p < 0.05:
        return '*'
    return 'ns'


def italic_gene(name):
    """基因名斜体(用于 tick/注释)。"""
    return r'$\it{%s}$' % name


def jitter(x, y, s=0.08, seed=0, n=None):
    """分类轴上的横向抖动坐标。"""
    r = np.random.default_rng(seed)
    n = n if n is not None else len(np.atleast_1d(y))
    return x + r.uniform(-s, s, n)


def panel_label(ax, letter, dx=-0.12, dy=1.05, fontsize=10, weight='bold'):
    """面板编号 a/b/c。"""
    ax.text(dx, dy, letter, transform=ax.transAxes, fontsize=fontsize,
            fontweight=weight, va='bottom', ha='left')


def cm2in(w_cm, h_cm):
    return (w_cm / 2.54, h_cm / 2.54)
