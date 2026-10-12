# -*- coding: utf-8 -*-
"""全库遮挡审计基线: 146 张配方重跑 audit, 与 gallery/_audit_issues.txt 基线比较。

用途: 保证"无字体遮挡等问题"不回退——
  - 基线里已登记的存量问题(待增量修复)不算失败;
  - 出现基线外的新问题(新配方不干净/改坏了旧图)→ 退出码 1。

用法:
  python scripts/audit_gallery.py                  # 审计 + 与基线比较
  python scripts/audit_gallery.py --update-baseline  # 用当前结果重写基线(修复后收缩)
退出码: 0=无回退  1=有新问题
"""
import json
import os
import sys
import glob
import argparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
BASELINE = os.path.join(ROOT, 'gallery', '_audit_issues.txt')


def parse_baseline():
    cur = None
    base = {}
    if not os.path.exists(BASELINE):
        return base
    for ln in open(BASELINE, encoding='utf-8'):
        ln = ln.rstrip('\n')
        if not ln or ln.startswith('#'):
            continue
        if not ln.startswith(' '):
            cur = ln.strip()
            base.setdefault(cur, [])
        elif cur is not None:
            base[cur].append(ln.strip())
    return base


def write_baseline(issues):
    lines = ['# 图库遮挡审计基线 — 由 scripts/audit_gallery.py --update-baseline 生成',
             '# 用途: 存量问题登记(待增量修复)。全库重跑 audit 后, 基线外新问题 = 回退, 判 FAIL。',
             '# 修一张划一张: 改配方 -> polish 到 PASS -> 重渲染 -> compare 复核 -> 更新基线。',
             '']
    for seg in sorted(issues):
        if not issues[seg]:
            continue
        lines.append(seg)
        for it in issues[seg]:
            lines.append('    ' + it)
    lines.append('')
    open(BASELINE, 'w', encoding='utf-8').write('\n'.join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--update-baseline', action='store_true')
    args = ap.parse_args()

    from polish import run_script
    recipes = sorted(glob.glob(os.path.join(ROOT, 'scripts', 'recipes', 'case_seg*.py')))
    cur = {}
    for rp in recipes:
        seg = 'seg' + os.path.basename(rp)[8:11]
        audit_lines, saved, error = run_script(rp)
        iss = [a for a in audit_lines if a != 'clean' and not a.endswith('issue(s)')]
        if error:
            iss.append('SCRIPT ERROR: %s' % ' | '.join(error[-2:]))
        if iss:
            cur[seg] = iss
    total = sum(len(v) for v in cur.values())
    print('全库审计: %d/%d 张有问题, %d 条 issue' % (len(cur), len(recipes), total))

    if args.update_baseline:
        write_baseline(cur)
        print('BASELINE UPDATED (%d segs)' % len(cur))
        return

    base = parse_baseline()
    regressions = []
    for seg, iss in sorted(cur.items()):
        known = set(base.get(seg, []))
        new = [i for i in iss if i not in known]
        if base.get(seg) is None or new:
            regressions.append((seg, new))
    fixed = [seg for seg in base if seg not in cur]
    if fixed:
        print('较基线修复: %s' % ' '.join(sorted(fixed)))
    if regressions:
        print('回退 %d 处:' % len(regressions))
        for seg, new in regressions:
            for i in new:
                print('  %s: %s' % (seg, i))
        sys.exit(1)
    print('GALLERY AUDIT OK (相对基线无回退)')


if __name__ == '__main__':
    main()
