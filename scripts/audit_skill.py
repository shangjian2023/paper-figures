# -*- coding: utf-8 -*-
"""skill 终审: selection/SKILL 引用合法性、路径泄漏、参考图完整性、catalog 完整性。"""
import json
import re
import os
import glob
from PIL import Image

SKILL = r'C:\Users\共产主义接班人\.zcode\skills\paper-figures'
os.chdir(SKILL)

catalog = json.load(open('reference/catalog.json', encoding='utf-8'))
segs = set(c['seg'] for c in catalog['cases'])

txt = open('reference/selection.md', encoding='utf-8').read()
refs = set(int(n) for n in re.findall(r'\b(\d{3})\b', txt))
bad = [n for n in refs if n not in segs]
print('selection.md 引用 seg 数:', len(refs), '非法引用:', bad)

txt2 = open('SKILL.md', encoding='utf-8').read()
refs2 = set(int(n) for n in re.findall(r'seg(\d{3})', txt2))
print('SKILL.md 引用 seg:', sorted(refs2), '非法:', [n for n in refs2 if n not in segs])

leak = []
# 泄漏口径: 代码文件(script)与数据文件里的项目绝对路径会让 skill 失去可移植性;
# SKILL.md / stages / reference 文档中"注明源库位置"属于有意文档, 不算泄漏。
for f in glob.glob('scripts/**/*.py', recursive=True):
    s = open(f, encoding='utf-8', errors='ignore').read()
    if ('绘图绘表skills' in s) or ('D:\\绘图' in s) or ('D:/绘图' in s) or ('edge默认下载' in s):
        leak.append(f)
for f in glob.glob('reference/*.json'):
    s = open(f, encoding='utf-8', errors='ignore').read()
    if ('D:\\绘图' in s) or ('D:/绘图' in s) or ('edge默认下载' in s):
        leak.append(f)
print('路径泄漏文件:', leak)

bad_png = []
for f in glob.glob('gallery/*.png'):
    try:
        Image.open(f).verify()
    except Exception as e:
        bad_png.append((f, str(e)))
print('参考图损坏:', bad_png)

assert len(catalog['cases']) == 146 and len(segs) == 146
assert sum(len(v) for v in catalog['batches'].values()) == 146
families = set(c['family'] for c in catalog['cases'])
print('catalog 146 完整, families:', sorted(families))
ok = not bad and not refs2 - segs and not leak and not bad_png
print('FINAL AUDIT', 'PASS' if ok else 'FAIL')
