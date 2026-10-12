# -*- coding: utf-8 -*-
"""重新生成 README 展示图: assets/readme/hero.png(图库拼贴横幅) + workflow.png(四阶段闭环, 本 skill 风格自绘)。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from paper_style import *

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from PIL import Image

READMEDIR = os.path.join(ROOT, 'assets', 'readme')
os.makedirs(READMEDIR, exist_ok=True)


# --------------------------------------------------------------- 1. 拼贴横幅
def make_hero():
    tiles = ['case_seg143.png', 'case_seg027.png', 'case_seg012.png',
             'case_seg005.png', 'case_seg045.png', 'case_seg016.png']
    cell_w, cell_h, pad = 800, 520, 14
    cols, rows = 3, 2
    W = cols * cell_w + (cols + 1) * pad
    H = rows * cell_h + (rows + 1) * pad
    canvas = Image.new('RGB', (W, H), 'white')
    for i, name in enumerate(tiles):
        img = Image.open(os.path.join(GALLERY, name))
        s = min((cell_w - 8) / img.width, (cell_h - 8) / img.height)
        img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
        r, c = divmod(i, cols)
        x = pad + c * (cell_w + pad) + (cell_w - img.width) // 2
        y = pad + r * (cell_h + pad) + (cell_h - img.height) // 2
        canvas.paste(img, (x, y))
    out = os.path.join(READMEDIR, 'hero.png')
    canvas.save(out)
    print('saved:', out, canvas.size)


# --------------------------------------------------------------- 2. 工作流元图
STAGES = [
    ('1', '鉴赏  Appreciation', '146 张成品 + 鉴赏卡片', '加图 · 删图 · 去重', '#3B6E8F'),
    ('2', '共鸣  Resonance', '样板册摆候选，用眼睛选', '布局 × 配色 自由组合', '#C98A2D'),
    ('3', '演绎  Rendition', '选中配方 × 你的数据', '校验 · 适配 · 实算显著性', '#5E8A5E'),
    ('4', '品评  Appraisal', '对照参考，并排品评', '满意即入库，循环往复', '#A25B5B'),
]


def _tint(hex_color, f=0.14):
    h = hex_color.lstrip('#')
    rgb = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    mix = tuple(round(c * f + 255 * (1 - f)) for c in rgb)
    return '#%02X%02X%02X' % mix


def make_workflow():
    set_style()
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'Arial']
    plt.rcParams['axes.unicode_minus'] = False

    fig, ax = plt.subplots(figsize=cm2in(26, 9.5))
    ax.set_xlim(0, 104)
    ax.set_ylim(0, 34)
    ax.axis('off')

    bw, bh, y0 = 22, 14, 12
    centers = [13, 39, 65, 91]
    for (num, title, l1, l2, color), cx in zip(STAGES, centers):
        x0, x1 = cx - bw / 2, cx + bw / 2
        ax.add_patch(FancyBboxPatch((x0, y0), bw, bh,
                                    boxstyle='round,pad=0,rounding_size=2.2',
                                    facecolor=_tint(color), edgecolor=color, lw=1.3))
        ax.add_patch(Circle((x0, y0 + bh), 2.1,
                            facecolor=color, edgecolor='white', lw=1.6, zorder=5))
        ax.text(x0, y0 + bh, num, ha='center', va='center',
                color='white', fontsize=9.5, weight='bold', zorder=6)
        ax.text(cx, y0 + bh - 3.6, title, ha='center', va='center',
                fontsize=10.5, weight='bold', color='#1A1A1A')
        ax.text(cx, y0 + 5.6, l1, ha='center', va='center', fontsize=8, color='#444444')
        ax.text(cx, y0 + 2.6, l2, ha='center', va='center', fontsize=8, color='#444444')

    for a, b in zip(centers[:-1], centers[1:]):
        ax.add_patch(FancyArrowPatch((a + bw / 2 + 0.6, y0 + bh / 2),
                                     (b - bw / 2 - 0.6, y0 + bh / 2),
                                     arrowstyle='-|>', mutation_scale=15,
                                     lw=1.4, color='#333333'))

    # 回路: 品评 → 共鸣
    ax.add_patch(FancyArrowPatch((centers[3], y0 - 0.7), (centers[1], y0 - 0.7),
                                 connectionstyle='arc3,rad=-0.24',
                                 arrowstyle='-|>', mutation_scale=15,
                                 lw=1.4, color='#333333'))
    ax.text((centers[1] + centers[3]) / 2, 1.7, '看到成品有了新想法 → 回到共鸣，再走一轮',
            ha='center', va='center', fontsize=8, color='#666666')

    # 用户入口
    ax.text(centers[1], 31.6, '用户入口：要画图 · 给了例图 · 说「你定」',
            ha='center', va='center', fontsize=8, color='#666666')
    ax.add_patch(FancyArrowPatch((centers[1], 30.3), (centers[1], y0 + bh + 0.8),
                                 arrowstyle='-|>', mutation_scale=13,
                                 lw=1.2, color='#999999', linestyle=(0, (4, 2))))

    save(fig, 'workflow.png', dirs=READMEDIR)


if __name__ == '__main__':
    make_hero()
    make_workflow()
