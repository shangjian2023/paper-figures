# -*- coding: utf-8 -*-
"""路由评测器: 对 reference/routing/_eval.jsonl 的意图集跑 route.rank, 算排序质量指标。

用法:
  python scripts/route_eval.py                # 全量指标
  python scripts/route_eval.py --verbose      # 逐例列出未命中
  python scripts/route_eval.py --tag 气质      # 只跑某 tag

指标:
  hit@5      前5名里出现任一期望 seg 的比例
  MRR@9      第一个期望 seg 排名的倒数均值(前9内)
  famcov@9   top9 的 family 覆盖数均值(多样性)
 垄断率@9    top9 内任一 family 占 >=4 的比例(应恒为 0)
  novelty    全部评测 top9 里不同 seg 的总数(多样性, 越大越不重复)
可覆盖命中率 只统计"至少一个期望 seg 已有档案"的案例——档案生产期内指标不被覆盖率稀释。
"""
import json
import os
import sys
import argparse
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
EVAL = os.path.join(ROOT, 'reference', 'routing', '_eval.jsonl')


def load_cases():
    cases = []
    for ln in open(EVAL, encoding='utf-8'):
        ln = ln.strip()
        if ln and not ln.startswith('#'):
            cases.append(json.loads(ln))
    return cases


def evaluate(verbose=False, tag=None):
    import route
    cat, profiles, purposes = route.load_all()
    cases = [c for c in load_cases() if not tag or c.get('tag') == tag]
    hit5 = mrr = famcov = mono = 0.0
    coverable = hit5_c = mrr_c = 0.0
    seen = Counter()
    rows = []
    for c in cases:
        top, meta = route.rank(c['intent'], n=9, min_wow=c.get('min_wow', 0), use_log=False)
        segs = [t['seg'] for t in top]
        fams = [t['family'] for t in top]
        famcov += len(set(fams))
        mono += 1 if max(Counter(fams).values()) >= 4 else 0
        seen.update(segs)
        exp = set(c['expect'])
        rank1 = next((i + 1 for i, s in enumerate(segs) if s in exp), 0)
        h5 = 1 if 0 < rank1 <= 5 else 0
        hit5 += h5
        mrr += 1.0 / rank1 if rank1 else 0.0
        cov = any(e in profiles for e in exp)
        if cov:
            coverable += 1
            hit5_c += h5
            mrr_c += 1.0 / rank1 if rank1 else 0.0
        rows.append((c['intent'], rank1, exp, cov))
    n = len(cases)
    res = {'cases': n,
           'hit@5': round(hit5 / n, 3),
           'MRR@9': round(mrr / n, 3),
           'famcov@9': round(famcov / n, 2),
           'monopoly@9': round(mono / n, 3),
           'novelty(总不同seg)': len(seen),
           '可覆盖命中率': round(hit5_c / coverable, 3) if coverable else 0,
           '可覆盖MRR': round(mrr_c / coverable, 3) if coverable else 0}
    if verbose:
        print('未命中明细:')
        for intent, rank1, exp, cov in rows:
            if not rank1 or rank1 > 5:
                mark = '(不可覆盖)' if not cov else ''
                print('  rank%-3s %s  expect=%s %s' % (rank1 or '-', intent[:30], exp, mark))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('--tag', default=None)
    args = ap.parse_args()
    res = evaluate(verbose=args.verbose, tag=args.tag)
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
