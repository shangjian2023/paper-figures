# -*- coding: utf-8 -*-
"""高级感(wow)分级: 给 catalog.json 每个案例写 wow 字段(1-3), 供精确响应
"要一张高级/惊艳/顶刊范的图"。

分级标准(全部经视觉验收, 无 0 分):
  3 = 镇场级: 结构复杂或形式特殊(环形/3D/双编码复合), 单独拿出就撑住一页
  2 = 有设计感: 明显高于基线(边际分布/双编码/镜像/复合面板)
  1 = 常规扎实: 朴素可靠, 数据说话型

映射是人工按 146 张成品逐张定的, 改分请直接改 WOW3/WOW2 再重跑本脚本。
新案例入库(new_case.py)后也重跑一次: 未列出的 seg 默认 1。
用法: python scripts/wow_score.py [--root DIR]
"""
import json
import os
import argparse
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))

# wow=3 镇场级(32 张)
WOW3 = [
    # 环形/发育树
    12, 13, 14, 15, 48,
    # 山脊/流向/网络
    16, 27, 32, 35, 45, 46, 89, 91,
    # 极坐标
    92, 93, 100, 101,
    # 空间/3D
    51, 52, 53, 59, 117, 143,
    # 双编码复合/特殊形态
    56, 74, 127, 128, 129, 133, 134, 135, 139,
]

# wow=2 有设计感(73 张)
WOW2 = [
    2, 3, 5, 11, 17, 20, 21, 22, 23, 25, 28, 33, 34, 38, 39, 40,
    43, 44, 47, 49, 50, 54, 55, 57, 58, 62, 66, 67, 68, 69, 70, 71,
    75, 76, 80, 81, 82, 83, 84, 85, 88, 90, 94, 95, 96, 97, 98, 99,
    102, 103, 107, 110, 111, 112, 113, 114, 115, 116, 118, 119, 120, 123,
    124, 125, 126, 136, 137, 140, 141, 142, 144, 145, 146,
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=ROOT)
    args = ap.parse_args()
    p = os.path.join(args.root, 'catalog.json')
    if not os.path.exists(p):
        p = os.path.join(args.root, 'reference', 'catalog.json')
    cat = json.load(open(p, encoding='utf-8'))
    for c in cat['cases']:
        c['wow'] = 3 if c['seg'] in WOW3 else (2 if c['seg'] in WOW2 else 1)
    json.dump(cat, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    cnt = Counter(c['wow'] for c in cat['cases'])
    print('wow written to %s' % p)
    print('distribution:', dict(sorted(cnt.items())))
    print('wow=3:', ' '.join('%03d' % c['seg'] for c in cat['cases'] if c['wow'] == 3))


if __name__ == '__main__':
    main()
