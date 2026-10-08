# -*- coding: utf-8 -*-
"""一键回归: 把历次迭代的全部检查串成一个入口。

python scripts/run_all_checks.py [--quick]     # quick: 跳过确定性抽样(最耗时项)

包含:
  1. audit_stage_a       全量重跑 + PNG 完整性
  2. 渲染警告审计        146/146 零警告(findfont/Glyph/Deprecation)
  3. 边缘裁切检测        0 贴边
  4. 确定性抽样(--quick 抽 12 张; 否则全量) 两遍 PNG hash 一致
  5. audit_skill         引用/泄漏/图片/catalog 终审
"""
import os
import sys
import json
import hashlib
import glob
import random
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
FAILS = []


def run(desc, cmd, expect=None):
    print('\n== %s ==' % desc)
    p = subprocess.run([sys.executable] + cmd, capture_output=True, text=True,
                       cwd=ROOT, timeout=900)
    out = (p.stdout or '') + (p.stderr or '')
    tail = '\n'.join(out.strip().splitlines()[-6:])
    print(tail)
    ok = p.returncode == 0 and (expect is None or expect in out)
    if not ok:
        FAILS.append(desc)
    return ok


# 1) 全量重跑 + PNG 完整性
run('全量重跑 + PNG 完整性', ['scripts/audit_stage_a.py'], expect='STAGE A DONE')

# 2) 渲染警告(重跑已发生, 直接复用 iter5 的分类审计)
run('渲染警告审计', ['scripts/iter5_stage1_render.py'], expect='font_fallback=0 glyph_missing=0')

# 3) 边缘裁切
run('边缘裁切检测', ['scripts/iter5_stage23_edges_colors.py'], expect='STAGE23 DONE')

# 4) 确定性抽样
if '--quick' in sys.argv:
    cat = json.load(open(os.path.join(ROOT, 'catalog.json'), encoding='utf-8'))
    segs = [c['seg'] for c in random.Random(0).sample(cat['cases'], 12)]
else:
    segs = [c['seg'] for c in json.load(open(os.path.join(ROOT, 'catalog.json'), encoding='utf-8'))['cases']]


def sha1(p):
    h = hashlib.sha1()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 16), b''):
            h.update(c)
    return h.hexdigest()


print('\n== 确定性抽样 (%d 张) ==' % len(segs))
bad = []
for s in segs:
    png = os.path.join(ROOT, 'gallery', 'case_seg%03d.png' % s)
    script = os.path.join(ROOT, 'scripts', 'recipes', 'case_seg%03d.py' % s)
    h1 = sha1(png)
    subprocess.run([sys.executable, script], capture_output=True, timeout=300)
    if sha1(png) != h1:
        bad.append(s)
print('non-deterministic: %d' % len(bad), bad[:10])
if bad:
    FAILS.append('确定性')

# 5) skill 终审
run('skill 终审', ['scripts/audit_skill.py'], expect='FINAL AUDIT PASS')

print('\n===== 回归总结 =====')
if FAILS:
    print('FAILED:', FAILS)
    sys.exit(1)
print('ALL CHECKS PASSED (146 案例, 5 条审计线)')
