# -*- coding: utf-8 -*-
"""迭代5-阶段2+3:
2) PNG 边缘裁切检测: 四边 2px 带内非白像素占比(贴边=可能被裁/出界)。
3) 颜色审计: 扫描配方中 matplotlib 默认色环引用(C0-C9/tab:*)、单字母色、
   seaborn 默认 palette —— 这些是"颜色不统一/不对"的候选。
"""
import os
import re
import glob
import json
import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
GALLERY = os.path.join(ROOT, 'gallery')
RECIPES = os.path.join(ROOT, 'scripts', 'recipes')

# ---- 2) 边缘检测
suspects = []
for f in sorted(glob.glob(os.path.join(GALLERY, 'case_seg*.png'))):
    seg = int(os.path.basename(f)[8:11])
    im = np.asarray(Image.open(f).convert('RGB').resize(
        (min(1600, Image.open(f).width), min(1600, Image.open(f).height))))
    h, w, _ = im.shape
    band = 2
    edges = {
        'top': im[:band, :, :], 'bottom': im[-band:, :, :],
        'left': im[:, :band, :], 'right': im[:, -band:, :],
    }
    hits = []
    for name, e in edges.items():
        nonwhite = (np.abs(e.astype(int) - 255).max(axis=2) > 18).mean()
        if nonwhite > 0.30:  # 边缘带 30% 以上非白 → 内容贴边(疑似裁切)
            hits.append('%s=%.0f%%' % (name, nonwhite * 100))
    if hits:
        suspects.append((seg, hits))
print('== 边缘贴边(疑似裁切/出界) ==')
for seg, hits in suspects:
    print('seg%03d: %s' % (seg, ', '.join(hits)))
print('suspects:', len(suspects), '/146')

# ---- 3) 颜色审计
DEFAULT_C = re.compile(r"\bC[0-9]\b(?!\w)|'tab:(?:blue|orange|green|red|purple|brown|pink|gray|olive|cyan)'|\"tab:(?:blue|orange|green|red|purple|brown|pink|gray|olive|cyan)\"")
LETTER_C = re.compile(r"color=['\"]([brgkcmyw])['\"]")
SNS_PAL = re.compile(r"sns\.(?:color_palette\(\)|set_palette\(\)|set_theme\(|set\()")
report = {}
for f in sorted(glob.glob(os.path.join(RECIPES, 'case_seg*.py'))):
    seg = int(os.path.basename(f)[8:11])
    src = open(f, encoding='utf-8').read()
    hits = []
    m = DEFAULT_C.findall(src)
    if m:
        hits.append('默认色环 x%d (%s)' % (len(m), sorted(set(m))[:4]))
    m2 = LETTER_C.findall(src)
    if m2:
        hits.append("单字母色 x%d (%s)" % (len(m2), sorted(set(m2))))
    if SNS_PAL.search(src):
        hits.append('seaborn 默认调色')
    if hits:
        report[seg] = hits
print('== 颜色扫描 ==')
for seg, hits in sorted(report.items()):
    print('seg%03d: %s' % (seg, '; '.join(hits)))
print('color-flagged:', len(report), '/146')

json.dump({'edge_suspects': {str(s): h for s, h in suspects},
           'color_flagged': {str(k): v for k, v in report.items()}},
          open(os.path.join(ROOT, 'scripts', 'iter5_stage23.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('STAGE23 DONE')
