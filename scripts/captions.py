# -*- coding: utf-8 -*-
"""文档插图图题(captions)生成器: 图名以文本形式附在图下方, 不嵌入图片内。

用法:
  python scripts/captions.py --segs 5 69 121 --out figures/captions.md
  python scripts/captions.py --segs 5 --names "我的三组比较" --prefix 图
  python scripts/captions.py --files figures/a.png figures/b.png --names "A题" "B题"

输出 markdown: 每行 "**图N**  图题（segNNN 或文件名）"，--with-plain 时附 "> 讲解：…" 行。
图题取自场景档案 caption 字段; --names 可覆盖; 交付时把对应行粘贴到文档里图片下方。
"""
import json
import os
import glob
import argparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
ROUTING = os.path.join(ROOT, 'reference', 'routing')


def load_profiles():
    out = {}
    for p in glob.glob(os.path.join(ROUTING, 'seg*.json')):
        try:
            r = json.load(open(p, encoding='utf-8'))
            out[int(r['seg'])] = r
        except Exception:
            continue
    return out


def load_catalog():
    p = os.path.join(ROOT, 'catalog.json')
    try:
        return {c['seg']: c for c in json.load(open(p, encoding='utf-8'))['cases']}
    except Exception:
        return {}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    ap.add_argument('--segs', nargs='*', type=int, default=[], help='图库案例号(取档案 caption)')
    ap.add_argument('--files', nargs='*', default=[], help='自定义成品 PNG 路径(配 --names)')
    ap.add_argument('--names', nargs='*', default=[], help='覆盖/自定义图题(与 --segs/--files 一一对应)')
    ap.add_argument('--prefix', default='图', help='编号前缀(默认 图)')
    ap.add_argument('--with-plain', action='store_true', help='图题后附直白解释(讲给非绘图者听)')
    ap.add_argument('--out', default=None, help='写到文件(默认打印到 stdout)')
    args = ap.parse_args()

    prof = load_profiles()
    cat = load_catalog()
    rows = []
    for i, seg in enumerate(args.segs):
        name = (args.names[i] if i < len(args.names) else '') or prof.get(seg, {}).get('caption', '') \
            or cat.get(seg, {}).get('type_zh', 'seg%03d' % seg)
        plain = prof.get(seg, {}).get('plain', '') if args.with_plain else ''
        rows.append((name, 'seg%03d' % seg, plain))
    for i, f in enumerate(args.files):
        j = len(args.segs) + i   # --names 与 --segs/--files 顺序一一对应, files 接在 segs 之后
        name = args.names[j] if j < len(args.names) else os.path.splitext(os.path.basename(f))[0]
        rows.append((name, os.path.basename(f), ''))
    if not rows:
        ap.error('给 --segs 或 --files')

    lines = ['# 插图图题（贴在文档中对应图片下方；名称不嵌入图片内）', '']
    for k, (name, ref, plain) in enumerate(rows, 1):
        ln = '**%s%d**  %s（%s）' % (args.prefix, k, name, ref)
        if plain:
            ln += '\n> 讲解：%s' % plain
        lines.append(ln)
        lines.append('')
    text = '\n'.join(lines)
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        open(args.out, 'w', encoding='utf-8').write(text)
        print('captions written:', args.out)
    else:
        print(text)


if __name__ == '__main__':
    main()
