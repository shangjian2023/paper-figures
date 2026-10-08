# -*- coding: utf-8 -*-
"""在终端 agent 会话里向用户呈图: 打开系统看图器 + 打印路径。

用法:
  python scripts/show.py <png> [<png> ...] [--print-only]

- 默认: 打开 OS 默认看图器(Windows os.startfile / macOS open / Linux xdg-open),
  并打印每个文件的绝对路径供用户手动打开。
- --print-only: 不弹窗, 只打印路径(无人值守/无 GUI 场景)。
"""
import os
import sys
import subprocess
import argparse


def open_file(path):
    try:
        if sys.platform == 'win32':
            os.startfile(path)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', path])
        else:
            subprocess.Popen(['xdg-open', path])
        return True
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('images', nargs='+')
    ap.add_argument('--print-only', action='store_true')
    args = ap.parse_args()

    opened = 0
    for p in args.images:
        ap_abs = os.path.abspath(p)
        ok = False
        if not args.print_only:
            ok = open_file(ap_abs)
        tag = 'opened' if ok else 'path  '
        print('[%s] %s' % (tag, ap_abs))
        opened += ok
    if not args.print_only and not opened:
        print('(无法自动打开看图器——请手动打开上面的路径)')


if __name__ == '__main__':
    main()
