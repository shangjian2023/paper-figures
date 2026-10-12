# -*- coding: utf-8 -*-
"""完美度门禁: 实跑图脚本并做机器能查的成品检查, 交付前的最后一道程序化关口。

用法:
  python scripts/polish.py figures/my_fig.py        # 实跑脚本(自动 PF_AUDIT=1) + 查产物
  python scripts/polish.py --png figures/my_fig.png # 只查现成 PNG 元数据

检查项:
  1. audit(fig) 文字两两重叠 / 文字出画布 / 字号过小(来自 save() 的 AUDIT 行)
  2. PNG 元数据: dpi≈300、可解码、尺寸、体积
判读: POLISH FAIL 必须处理; AUDIT 报的"刻意叠放"复核后可说明放行,
但程序不替你判断——修不掉就如实告诉用户。

退出码: 0=PASS  1=FAIL(有 issue 或脚本/产物异常)
"""
import os
import re
import sys
import argparse
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def check_png(path):
    """返回 (issues, infos)。dpi 容差 270-330(写出 300 时 PIL 读回 ~299.9994)。"""
    issues, infos = [], []
    if not os.path.exists(path):
        return ['png missing: %s' % path], infos
    size = os.path.getsize(path)
    if size < 20 * 1024:
        issues.append('png suspiciously small (%.0fKB): %s' % (size / 1024, path))
    try:
        from PIL import Image
        im = Image.open(path)
        im.verify()
        im = Image.open(path)  # verify 后需重开
        w, h = im.size
        dpi = im.info.get('dpi', (0, 0))[0]
    except Exception as e:
        return ['png undecodable: %s (%s)' % (path, e)], infos
    infos.append('%s  %dx%dpx  %.0fdpi  %.0fKB' % (os.path.basename(path), w, h, dpi, size / 1024))
    if not (270 <= dpi <= 330):
        issues.append('dpi=%.0f (expect ~300): %s' % (dpi, path))
    if w < 600 or h < 400:
        issues.append('canvas %dx%d too small for publication: %s' % (w, h, path))
    return issues, infos


def run_script(script):
    """实跑图脚本(PF_AUDIT=1), 返回 (audit_lines, saved_pngs, error 或 None)。"""
    script = os.path.abspath(script)
    env = dict(os.environ, PF_AUDIT='1', PYTHONIOENCODING='utf-8')
    p = subprocess.run([sys.executable, script], capture_output=True, text=True,
                       cwd=os.path.dirname(script), env=env, timeout=600)
    out = (p.stdout or '') + '\n' + (p.stderr or '')
    audit_lines = [ln.split('AUDIT:', 1)[1].strip() for ln in out.splitlines()
                   if 'AUDIT:' in ln]
    script_dir = os.path.dirname(script)
    saved = [s if os.path.isabs(s) else os.path.abspath(os.path.join(script_dir, s))
             for s in re.findall(r'^saved:\s*(.+\.png)\s*$', out, re.M)]
    error = None
    if p.returncode != 0:
        error = out.strip().splitlines()[-8:]
    return audit_lines, saved, error


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    ap.add_argument('script', nargs='?', help='要实跑的图脚本')
    ap.add_argument('--png', action='append', default=[], help='额外检查的 PNG(可多次)')
    args = ap.parse_args()
    if not args.script and not args.png:
        ap.error('给图脚本路径, 或 --png 指定现成 PNG')

    issues, infos = [], []
    audit_lines = []
    if args.script:
        audit_lines, saved, error = run_script(args.script)
        for s in saved:
            i2, f2 = check_png(s)
            issues += i2
            infos += f2
        if not saved:
            issues.append('script produced no PNG (saved: 未捕获; 用 --png 手动指定产物)')
        if error:
            issues.append('script exited non-zero:\n    ' + '\n    '.join(error))
    for p in args.png:
        i2, f2 = check_png(p)
        issues += i2
        infos += f2

    # 摘要行('clean' / 'N issue(s)')不算 issue, 只有明细行算
    audit_issues = [a for a in audit_lines
                    if a != 'clean' and not re.match(r'^\d+ issue', a)]
    print('--- polish report ---')
    for f in infos:
        print('  png   :', f)
    print('  audit : %s' % ('clean' if not audit_issues else '%d issue(s)' % len(audit_issues)))
    for a in audit_issues:
        print('    -', a)
    for s in issues:
        print('  ISSUE :', s)
    fail = issues or audit_issues
    print('POLISH %s' % ('FAIL (%d issue(s))' % (len(issues) + len(audit_issues)) if fail else 'PASS'))
    sys.exit(1 if fail else 0)


if __name__ == '__main__':
    main()
