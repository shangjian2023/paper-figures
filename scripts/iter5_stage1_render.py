# -*- coding: utf-8 -*-
"""迭代5-阶段1: 渲染质量审计。
A) 重跑全部配方, 捕获 stderr 警告并分类:
   findfont 回退 / Glyph missing(字形缺失->豆腐) / tight_layout / 其他
B) 字体落地探针: set_style() 后 findfont('Arial') 实际解析到哪个文件
C) 负号/unicode_minus 与数学字体设置扫描
输出: scripts/iter5_stage1.json + 控制台报告
"""
import os
import re
import glob
import json
import subprocess
import sys
import warnings

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RECIPES = os.path.join(ROOT, 'scripts', 'recipes')
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

scripts = sorted(glob.glob(os.path.join(RECIPES, 'case_seg*.py')))

# ---- B) 字体落地探针
from matplotlib import font_manager
import matplotlib
from paper_style import set_style
set_style()
resolved = font_manager.findfont('Arial', fallback_to_default=False) if any(
    f.name == 'Arial' for f in font_manager.fontManager.ttflist) else font_manager.findfont('Arial')
print('probe: findfont(Arial) ->', resolved)
print('probe: rcParams family ->', matplotlib.rcParams['font.sans-serif'][:3])
print('probe: unicode_minus ->', matplotlib.rcParams['axes.unicode_minus'])

# ---- A) 重跑收集警告
CAT = {
    'font_fallback': re.compile(r'findfont: (Font family|font).*(not found|falling back)', re.I),
    'glyph_missing': re.compile(r'Glyph \S+ missing from (the )?font', re.I),
    'tight_layout': re.compile(r'This figure includes Axes that are not compatible with tight_layout', re.I),
    'bbox_clip': re.compile(r'( clipped|outside the (figure|axes)|not in (the )?axes)', re.I),
    'deprecation': re.compile(r'DeprecationWarning|MatplotlibDeprecationWarning', re.I),
}
issues = {}
for f in scripts:
    seg = int(os.path.basename(f)[8:11])
    p = subprocess.run([sys.executable, f], capture_output=True, text=True, timeout=300,
                       env={**os.environ, 'PYTHONWARNINGS': 'always'})
    err = p.stderr or ''
    tags = []
    for name, pat in CAT.items():
        hits = pat.findall(err)
        if hits:
            tags.append((name, len(hits), hits[0].strip()[:110]))
    if p.returncode != 0:
        tags.append(('CRASH', 1, (err.strip().splitlines() or ['?'])[-1][:150]))
    if tags:
        issues[seg] = tags

n_font = sum(1 for v in issues.values() if any(t[0] == 'font_fallback' for t in v))
n_glyph = sum(1 for v in issues.values() if any(t[0] == 'glyph_missing' for t in v))
print('== 渲染警告 ==')
print('scripts with issues: %d/%d | font_fallback=%d glyph_missing=%d' % (
    len(issues), len(scripts), n_font, n_glyph))
for seg, tags in sorted(issues.items()):
    print('seg%03d: %s' % (seg, ' | '.join('%s x%d: %s' % t for t in tags)))

# ---- C) 脚本内字体/负号覆盖扫描
susp = {}
for f in scripts:
    seg = int(os.path.basename(f)[8:11])
    src = open(f, encoding='utf-8').read()
    flags = []
    if re.search(r'unicode_minus\s*=\s*True', src):
        flags.append('unicode_minus=True(负号风险)')
    if re.search(r"font[^,\)]*=['\"](SimHei|Microsoft YaHei|SimSun|KaiTi|FangSong)", src):
        m = re.search(r"font[^,\)]*=['\"]([^'\"]+)", src)
        flags.append('中文字体: %s' % m.group(1))
    if re.search(r'fontfamily|font_properties|FontProperties\(', src):
        flags.append('自定义字体覆盖')
    if 'usetex' in src:
        flags.append('usetex(需LaTeX)')
    if flags:
        susp[seg] = flags
print('== 字体覆盖扫描 ==')
for seg, fl in sorted(susp.items()):
    print('seg%03d: %s' % (seg, '; '.join(fl)))

json.dump({'probe_font': str(resolved),
           'issues': {str(k): [[t[0], t[1], t[2]] for t in v] for k, v in issues.items()},
           'font_overrides': {str(k): v for k, v in susp.items()}},
          open(os.path.join(ROOT, 'scripts', 'iter5_stage1.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('STAGE1 DONE')
