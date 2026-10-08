# -*- coding: utf-8 -*-
"""样板册/并排对照生成器 (PIL)。

用法:
  # 样板册: 候选拼一张, 自动标 A/B/C, 可带标签
  python scripts/make_contact_sheet.py sheet --out sheet.png "1::我的推荐" "5" "69::贴近你的口味" ...
  # 按家族取样:
  python scripts/make_contact_sheet.py sheet --out sheet.png --family distribution --sample 6
  # 并排对照(品评): 参考帧 vs 成品
  python scripts/make_contact_sheet.py compare --out cmp.png 27
"""
import os
import sys
import argparse
import json
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
THUMB = 420
FONT_CANDS = ['C:/Windows/Fonts/msyh.ttc', 'C:/Windows/Fonts/simhei.ttf',
              'C:/Windows/Fonts/arial.ttf']


def load_font(size):
    for p in FONT_CANDS:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def thumb(seg):
    for base in [os.path.join(ROOT, 'gallery'),
                 os.path.join(ROOT, 'frames')]:
        for name in ('case_seg%03d.png' % seg, 'seg_%03d.jpg' % seg):
            p = os.path.join(base, name)
            if os.path.exists(p):
                im = Image.open(p).convert('RGB')
                im.thumbnail((THUMB, THUMB), Image.LANCZOS)
                return im
    return None


def sheet(items, out, cols=3):
    """items: [(seg, label 或 None)]"""
    font = load_font(22)
    cells = []
    for i, (seg, label) in enumerate(items):
        im = thumb(seg)
        if im is None:
            print('missing seg', seg)
            continue
        tag = chr(ord('A') + len(cells))
        canvas = Image.new('RGB', (THUMB + 8, THUMB + 46), 'white')
        canvas.paste(im, (4, 4))
        d = ImageDraw.Draw(canvas)
        label = '%s. seg%03d  %s' % (tag, seg, label or '')
        fs = 22
        while fs > 12 and d.textlength(label, font=load_font(fs)) > THUMB - 4:
            fs -= 1
        d.text((8, THUMB + 8), label, font=load_font(fs), fill='black')
        cells.append(canvas)
    if not cells:
        print('nothing to render')
        return
    rows = (len(cells) + cols - 1) // cols
    board = Image.new('RGB', (cols * (THUMB + 8), rows * (THUMB + 46)), 'white')
    for k, cell in enumerate(cells):
        board.paste(cell, ((k % cols) * (THUMB + 8), (k // cols) * (THUMB + 46)))
    board.save(out)
    print('sheet saved:', out, '(%d items)' % len(cells))


def compare(seg, out, got=None):
    """参考帧 vs 成品。got: 用户成品路径；缺省用图库验收图。
    frames/ 不随技能分发时自动降级为 ab 双图模式。"""
    ref = os.path.join(ROOT, 'frames', 'seg_%03d.jpg' % seg)
    right = got or os.path.join(ROOT, 'gallery', 'case_seg%03d.png' % seg)
    if not os.path.exists(ref):
        # 无参考帧：退化为参考验收图 vs 用户成品
        ref = os.path.join(ROOT, 'gallery', 'case_seg%03d.png' % seg)
        if got is None or not os.path.exists(ref):
            print('no reference available (frames/ 未分发且 gallery 缺图)；'
                  '用 ab 子命令手动指定两图')
            return
    a = Image.open(ref).convert('RGB')
    b = Image.open(right).convert('RGB')
    h = 900
    a.thumbnail((10000, h), Image.LANCZOS)
    b.thumbnail((10000, h), Image.LANCZOS)
    board = Image.new('RGB', (a.width + b.width + 24, h + 50), 'white')
    board.paste(a, (8, 42))
    board.paste(b, (a.width + 16, 42))
    d = ImageDraw.Draw(board)
    font = load_font(26)
    d.text((8, 6), ('reference (seg%03d)' % seg) if 'frames' in ref else 'gallery reference (seg%03d)' % seg,
            font=font, fill='black')
    d.text((a.width + 16, 6), 'rendered', font=font, fill='black')
    board.save(out)
    print('compare saved:', out)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    sh = sub.add_parser('sheet')
    sh.add_argument('--out', required=True)
    sh.add_argument('--family', default=None)
    sh.add_argument('--sample', type=int, default=0, help='按家族随机抽几张')
    sh.add_argument('--open', action='store_true', help='生成后用系统看图器打开(供 TUI 用户查看)')
    sh.add_argument('items', nargs='*', help='"seg::标签" 或 "seg"')
    cp = sub.add_parser('compare')
    cp.add_argument('--out', required=True)
    cp.add_argument('seg', type=int)
    cp.add_argument('--got', default=None, help='用户成品 PNG 路径；缺省时用图库验收图 gallery/case_segNNN.png')
    cp.add_argument('--open', action='store_true')
    ab = sub.add_parser('ab', help='任意两张图并排(如 成品 vs 用户例图)')
    ab.add_argument('--out', required=True)
    ab.add_argument('--open', action='store_true')
    ab.add_argument('imga')
    ab.add_argument('imgb')
    args = ap.parse_args()

    if args.cmd == 'compare':
        compare(args.seg, args.out, got=args.got)
        if args.open:
            from show import open_file
            open_file(os.path.abspath(args.out))
        return
    elif args.cmd == 'ab':
        a = Image.open(args.imga).convert('RGB')
        b = Image.open(args.imgb).convert('RGB')
        h = 900
        a.thumbnail((10000, h), Image.LANCZOS)
        b.thumbnail((10000, h), Image.LANCZOS)
        board = Image.new('RGB', (a.width + b.width + 24, h + 50), 'white')
        board.paste(a, (8, 42))
        board.paste(b, (a.width + 16, 42))
        d = ImageDraw.Draw(board)
        font = load_font(26)
        d.text((8, 6), os.path.basename(args.imga), font=font, fill='black')
        d.text((a.width + 16, 6), os.path.basename(args.imgb), font=font, fill='black')
        board.save(args.out)
        print('ab saved:', args.out)
        if args.open:
            from show import open_file
            open_file(os.path.abspath(args.out))
        return
    items = []
    for it in args.items:
        if '::' in it:
            s, lab = it.split('::', 1)
            items.append((int(s), lab))
        else:
            items.append((int(it), None))
    if args.family:
        cat = None
        for p in (os.path.join(ROOT, 'catalog.json'),
                  os.path.join(ROOT, 'reference', 'catalog.json')):
            if os.path.exists(p):
                cat = json.load(open(p, encoding='utf-8'))
                break
        segs = [c['seg'] for c in cat['cases'] if c['family'] == args.family]
        if args.sample:
            import random
            random.seed(0)
            segs = random.sample(segs, min(args.sample, len(segs)))
        items += [(s, args.family) for s in segs]
    sheet(items, args.out)
    if args.open:
        from show import open_file
        open_file(os.path.abspath(args.out))


if __name__ == '__main__':
    main()
