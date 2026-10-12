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
    """保存到 gallery/(或指定 dirs, 自动创建)并关闭 figure。

    环境变量 PF_AUDIT=1 时(如经 scripts/polish.py 调起)保存前先跑 audit(fig),
    结果以 'AUDIT:' 行打印, 供 polish 解析判 PASS/FAIL。"""
    out_dir = dirs or GALLERY
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, name)
    fig.savefig(out, dpi=dpi, bbox_inches='tight', facecolor='white')
    if os.environ.get('PF_AUDIT') == '1':
        issues = audit(fig)
        print('AUDIT: %s' % ('clean' if not issues else '%d issue(s)' % len(issues)))
        for msg in issues:
            print('AUDIT: ' + msg)
    _plt.close(fig)
    print('saved:', out)
    return out


def audit(fig, iou=0.35, tol=2.0, cap=8):
    """成品视觉自检(机器能查的部分): 文字两两重叠 / 导出必截断的文字 / 字号过小。

    返回 issue 描述列表(空 = 通过)。交给 polish 门禁用; 日常手动调用:
        from paper_style import audit; print(audit(fig))
    刻意叠放(镜像轴同位刻度等)若误报, 复核后说明即可, 不要为消 warning 改坏图。"""
    fig.canvas.draw()
    ren = fig.canvas.get_renderer()
    texts = []
    for ax in fig.axes:
        items = list(ax.texts) + [ax.title, ax.xaxis.label, ax.yaxis.label]
        if getattr(ax, 'axison', True):   # 轴关了(axison=False)的刻度标签不会被画, 不算
            items += ax.get_xticklabels() + ax.get_yticklabels()
        lg = ax.get_legend()
        if lg is not None:
            items += lg.get_texts()
        for t in items:
            if t is None or not str(t.get_text()).strip() or not t.get_visible():
                continue
            try:
                bb = t.get_window_extent(renderer=ren)
            except Exception:
                continue
            if bb.width > 0 and bb.height > 0:
                texts.append((t, bb))
    # 完全同位同文(镜像/双子轴共享标签)视为同一处, 消误报
    uniq = []
    for t, bb in texts:
        if not any(t.get_text() == t2.get_text() and abs(bb.x0 - b2.x0) < 1
                   and abs(bb.y0 - b2.y0) < 1 for t2, b2 in uniq):
            uniq.append((t, bb))
    issues = []
    # 1) 文字两两重叠(占较小者面积 >iou)
    n = len(uniq)
    for i in range(n):
        for j in range(i + 1, n):
            a, b = uniq[i][1], uniq[j][1]
            ix = min(a.x1, b.x1) - max(a.x0, b.x0)
            iy = min(a.y1, b.y1) - max(a.y0, b.y0)
            if ix <= 0 or iy <= 0:
                continue
            smaller = min(a.width * a.height, b.width * b.height)
            frac = (ix * iy) / smaller if smaller > 0 else 0
            if frac > iou:
                issues.append('text overlap: %r x %r (%.0f%%)'
                              % (str(uniq[i][0].get_text())[:28], str(uniq[j][0].get_text())[:28], frac * 100))
    # 2) 导出必截断: 只查 in_layout=False 的文字——matplotlib 的 tight bbox 本身就
    #    把它们排除在外, 落在 tight bbox 之外就一定被裁。其余文字 tight bbox 会自动
    #    扩进来, 不会截。
    tb = fig.get_tightbbox(ren)
    dpi = fig.dpi
    tx0, ty0 = tb.x0 * dpi - tol, tb.y0 * dpi - tol
    tx1, ty1 = tb.x1 * dpi + tol, tb.y1 * dpi + tol
    for t, bb in uniq:
        if not t.get_in_layout():
            if bb.x0 < tx0 or bb.y0 < ty0 or bb.x1 > tx1 or bb.y1 > ty1:
                issues.append('text clipped on export: %r' % str(t.get_text())[:28])
    # 3) 字号事故(≥3pt 的小字可能是刻意设计, 不报; 全库验收过的最小 3.8pt)
    for t, bb in uniq:
        fs = t.get_fontsize()
        if fs and fs < 3.0:
            issues.append('tiny font %.1fpt: %r' % (fs, str(t.get_text())[:24]))
    # 4) 遮挡: 文字压散点/曲线(无白描边或底衬保护时) / 图例盖住数据
    issues += _audit_occlusion(fig, ren, uniq)
    dedup = []
    for s in issues:
        if s not in dedup:
            dedup.append(s)
    return dedup[:cap]


def _protected_text(t):
    """文字带白描边或半透明以上底衬时, 压在数据上仍可读, 视为受保护。"""
    import matplotlib.patheffects as _pe
    for e in (t.get_path_effects() or []):
        if isinstance(e, _pe.withStroke):
            return True
    bp = t.get_bbox_patch()
    if bp is not None:
        fc = bp.get_facecolor()
        if len(fc) >= 4 and fc[3] > 0.5:
            return True
    return False


def _ax_data_points(ax, ren, per_artist_cap=600):
    """轴上散点/曲线的采样点(显示坐标)。柱形等 patch 不算——数值标在柱上是常规画法。"""
    pts = []
    td = getattr(ax, 'transData', None)
    if td is None:
        return pts
    try:
        for coll in ax.collections:
            off = coll.get_offsets()
            if off is not None and len(off):
                pts.append(td.transform(off[:per_artist_cap]))
        for ln in ax.lines:
            xy = ln.get_xydata()
            if xy is not None and len(xy):
                step = max(1, len(xy) // per_artist_cap)
                pts.append(td.transform(xy[::step]))
    except Exception:
        pass
    return [p for p in pts if len(p)]


def _inside_count(pts2d, bb):
    if not len(pts2d):
        return 0
    m = (pts2d[:, 0] >= bb.x0) & (pts2d[:, 0] <= bb.x1) & \
        (pts2d[:, 1] >= bb.y0) & (pts2d[:, 1] <= bb.y1)
    return int(m.sum())


def _audit_occlusion(fig, ren, uniq, min_hits=3, cap=6):
    """文字压数据: 文本框内落进 >=min_hits 个散点/曲线采样点且文字无保护 → issue。
    图例盖数据: 图例框内落进 >=min_hits 个数据点 → issue(图例内文字由此覆盖, 不重复报)。"""
    out = []
    shown = 0
    for ax in fig.axes:
        pts_list = _ax_data_points(ax, ren)
        if not pts_list:
            continue
        lg = ax.get_legend()
        lg_texts = set(lg.get_texts()) if lg is not None else set()
        if lg is not None:
            try:
                lb = lg.get_window_extent(renderer=ren)
                n = sum(_inside_count(p, lb) for p in pts_list)
                if n >= min_hits:
                    out.append('legend covers data: %d pts under legend' % n)
                    shown += 1
            except Exception:
                pass
        for t, bb in uniq:
            if shown >= cap:
                break
            if t in lg_texts or not _owned_by(ax, t):
                continue
            if _protected_text(t):
                continue
            n = sum(_inside_count(p, bb) for p in pts_list)
            if n >= min_hits:
                out.append('text over data (no stroke/bbox): %r (%d pts)' % (str(t.get_text())[:24], n))
                shown += 1
        if shown >= cap:
            break
    return out


def _owned_by(ax, t):
    """文字确实属于该轴(tick/title/label/text), 避免 Twin 轴重复计数。"""
    if t in ax.texts:
        return True
    if t is ax.title or t is ax.xaxis.label or t is ax.yaxis.label:
        return True
    if getattr(ax, 'axison', True) and (t in ax.get_xticklabels() or t in ax.get_yticklabels()):
        return True
    lg = ax.get_legend()
    if lg is not None and t in lg.get_texts():
        return True
    return False


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
