# -*- coding: utf-8 -*-
"""路由档案质量校验: segNNN.json 的结构/字段/词表齐全性。

用法: python scripts/check_routing.py [--strict]
默认只对"已存在的档案"查结构(结构坏→退出码 1), 覆盖数只报告——生产期不阻塞回归;
--strict 要求 146 份齐全。"""
import json
import os
import sys
import glob
import argparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
ROUTING = os.path.join(ROOT, 'reference', 'routing')

REQUIRED = ['seg', 'use_when', 'triggers', 'anti_when', 'style', 'similar', 'audience']
AUDIENCES = {'期刊正文', '补充材料', '组会', '海报'}  # 权威四选项(终审裁决 2026-10-12; 全库现用值只有前两个, 后两个预留给海报/组会场景)


def _has(path, key):
    try:
        return key in json.load(open(path, encoding='utf-8'))
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--strict', action='store_true', help='要求 146 份齐全, 缺一份即失败')
    args = ap.parse_args()
    cat = json.load(open(os.path.join(ROOT, 'catalog.json'), encoding='utf-8'))['cases']
    all_segs = {c['seg'] for c in cat}
    files = {int(os.path.basename(p)[3:6]): p for p in glob.glob(os.path.join(ROUTING, 'seg*.json'))}
    problems = []
    missing = []
    for seg in sorted(all_segs):
        if seg not in files:
            missing.append(seg)
            continue
        try:
            r = json.load(open(files[seg], encoding='utf-8'))
        except Exception as e:
            problems.append('seg%03d: JSON 不可解析 (%s)' % (seg, e))
            continue
        for k in REQUIRED:
            if k not in r:
                problems.append('seg%03d: 缺字段 %s' % (seg, k))
        if not (3 <= len(r.get('use_when', [])) <= 6):
            problems.append('seg%03d: use_when %d 条(应 3-6)' % (seg, len(r.get('use_when', []))))
        if not (6 <= len(r.get('triggers', [])) <= 14):
            problems.append('seg%03d: triggers %d 个(应 6-14)' % (seg, len(r.get('triggers', []))))
        if not (1 <= len(r.get('anti_when', [])) <= 4):
            problems.append('seg%03d: anti_when %d 条(应 1-4)' % (seg, len(r.get('anti_when', []))))
        if r.get('audience') not in AUDIENCES:
            problems.append('seg%03d: audience 非法: %r' % (seg, r.get('audience')))
        if r.get('seg') != seg:
            problems.append('seg%03d: 文件内 seg=%r 不一致' % (seg, r.get('seg')))
        for s in r.get('similar', []):
            if int(s) not in all_segs:
                problems.append('seg%03d: similar 引用不存在的 seg%s' % (seg, s))
        # 交付讲解字段: plain(直白解释) / caption(文档图题) — 生产期允许暂缺, --strict 时必须齐
        plain = r.get('plain', '')
        if plain:
            if not (10 <= len(plain) <= 90):
                problems.append('seg%03d: plain %d 字(应 10-90)' % (seg, len(plain)))
        cap = r.get('caption', '')
        if cap and len(cap) > 25:
            problems.append('seg%03d: caption %d 字(应 <=25)' % (seg, len(cap)))
    print('routing 档案: %d/146%s' % (len(files), '' if not missing else ' (缺: %s%s)' % (
        ' '.join('%03d' % s for s in missing[:12]), '…' if len(missing) > 12 else '')))
    n_plain = sum(1 for p in files.values() if _has(p, 'plain'))
    n_cap = sum(1 for p in files.values() if _has(p, 'caption'))
    print('plain/caption: %d/%d' % (n_plain, n_cap))
    if args.strict:
        if missing:
            problems.append('strict: %d 份缺失' % len(missing))
        if n_plain < len(files) or n_cap < len(files):
            problems.append('strict: plain/caption 未全覆盖 (%d/%d 份 plain)' % (n_plain, len(files)))
    if problems:
        print('问题 %d 条:' % len(problems))
        for p in problems:
            print(' ', p)
        sys.exit(1)
    print('ROUTING CHECK OK')


if __name__ == '__main__':
    main()
