# -*- coding: utf-8 -*-
"""审核阶段A: 1) 重跑全部配方验证可重复性  2) PNG 完整性与空白/低方差检测。"""
import os
import sys
import glob
import json
import subprocess
import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
GALLERY = os.path.join(ROOT, 'gallery')
RECIPES = os.path.join(ROOT, 'scripts', 'recipes')

catalog = json.load(open(os.path.join(ROOT, 'catalog.json'), encoding='utf-8'))
segs = sorted(c['seg'] for c in catalog['cases'])

# ---- 1) 重跑全部脚本
fails = []
for s in segs:
    script = os.path.join(RECIPES, 'case_seg%03d.py' % s)
    if not os.path.exists(script):
        fails.append((s, 'NO SCRIPT'))
        continue
    p = subprocess.run([sys.executable, script], capture_output=True, text=True, timeout=300)
    if p.returncode != 0:
        fails.append((s, p.stderr.strip().splitlines()[-1] if p.stderr else 'unknown'))
print('RERUN: %d/%d ok' % (len(segs) - len([f for f in fails]), len(segs)))
for s, e in fails:
    print('  FAIL seg%03d: %s' % (s, e))

# ---- 2) PNG 完整性 + 空白检测
blank, broken, tiny = [], [], []
for s in segs:
    png = os.path.join(GALLERY, 'case_seg%03d.png' % s)
    if not os.path.exists(png):
        blank.append((s, 'MISSING'))
        continue
    if os.path.getsize(png) < 8000:
        tiny.append((s, os.path.getsize(png)))
        continue
    try:
        im = Image.open(png).convert('RGB')
        a = np.asarray(im.resize((128, 128)))
        var = float(a.std())
        if var < 6.0:
            blank.append((s, 'std=%.1f' % var))
    except Exception as e:
        broken.append((s, str(e)))
print('PNG check: blank/suspect=%d broken=%d tiny=%d' % (len(blank), len(broken), len(tiny)))
for s, e in blank + broken + tiny:
    print('  BAD seg%03d: %s' % (s, e))
print('STAGE A DONE')
