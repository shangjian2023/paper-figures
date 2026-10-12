# -*- coding: utf-8 -*-
"""paper-figures 环境与安装自检。

检查: Python 版本 / 依赖包 / 字体 / assets / gallery 与 recipes 数量 / 各 agent 安装状态。
用法: python scripts/doctor.py [--skill-dir PATH]   (默认自动探测本技能所在目录)
"""
import os
import sys
import importlib
import argparse

HERE = os.path.dirname(os.path.abspath(__file__))


def find_skill_dir():
    cands = [
        os.path.abspath(os.path.join(HERE, '..')),                       # 源目录(项目根)
        os.path.join(os.path.expanduser('~'), '.agents', 'skills', 'paper-figures'),
        os.path.join(os.path.expanduser('~'), '.zcode', 'skills', 'paper-figures'),
        os.path.join(os.environ.get('CLAUDE_CONFIG_DIR') or os.path.join(os.path.expanduser('~'), '.claude'), 'skills', 'paper-figures'),
        os.path.join(os.environ.get('CODEX_HOME') or os.path.join(os.path.expanduser('~'), '.codex'), 'skills', 'paper-figures'),
        os.path.join(os.environ.get('XDG_CONFIG_HOME') or os.path.join(os.path.expanduser('~'), '.config'), 'opencode', 'skills', 'paper-figures'),
    ]
    for p in cands:
        if os.path.exists(os.path.join(p, 'SKILL.md')):
            return p
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--skill-dir', default=None)
    args = ap.parse_args()
    skill = args.skill_dir or find_skill_dir()

    ok = True
    print('== paper-figures doctor ==')
    v = sys.version_info
    print('python      : %d.%d.%d %s' % (v.major, v.minor, v.micro, 'OK' if v >= (3, 9) else 'TOO OLD(<3.9)'))
    ok &= v >= (3, 9)

    missing = []
    for mod in ['matplotlib', 'numpy', 'PIL', 'scipy', 'networkx',
                'jieba', 'rank_bm25']:
        try:
            m = importlib.import_module(mod)
            print('dep         : %-11s %s' % (mod, getattr(m, '__version__', '?')))
        except Exception:
            missing.append(mod)
            print('dep         : %-11s MISSING' % mod)
    ok &= not missing
    if missing:
        print('              -> pip install %s' % ' '.join(['matplotlib', 'numpy', 'pillow', 'scipy', 'networkx', 'jieba', 'rank_bm25']))

    # 字体
    fonts = [r'C:\Windows\Fonts\arial.ttf', '/System/Library/Fonts/Supplemental/Arial.ttf',
             '/usr/share/fonts/truetype/msttcorefonts/Arial.ttf',
             '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    found = next((f for f in fonts if os.path.exists(f)), None)
    print('latin font  : %s' % (found or 'FALLBACK(DejaVu via matplotlib)'))

    if skill:
        print('skill dir   : %s' % skill)
        def count(p, pred=lambda x: True):
            base = os.path.join(skill, p)
            return len([f for f in os.listdir(base) if pred(f)]) if os.path.isdir(base) else 0
        n_png = count('gallery', lambda f: f.startswith('case_seg') and f.endswith('.png'))
        n_rec = count(os.path.join('scripts', 'recipes'), lambda f: f.startswith('case_seg') and f.endswith('.py'))
        n_cards = count(os.path.join('gallery', 'cards'), lambda f: f.endswith('.md') and not f.startswith('_'))
        n_ref = count('reference')
        geo = all(os.path.exists(os.path.join(skill, 'assets', 'map_data', f))
                  for f in ('world.geo.json', 'china.geo.json'))
        has_schema = os.path.exists(os.path.join(skill, 'reference', 'data-schemas.json'))
        print('gallery     : %d/146 成品图 %s' % (n_png, 'OK' if n_png == 146 else '(lite 模式属正常)'))
        print('recipes     : %d/146 配方 %s' % (n_rec, 'OK' if n_rec == 146 else 'INCOMPLETE'))
        print('cards       : %d/146 卡片 %s' % (n_cards, 'OK' if n_cards == 146 else 'INCOMPLETE'))
        print('reference   : %d 个文件 %s' % (n_ref, 'OK' if n_ref >= 3 else 'INCOMPLETE'))
        n_route = count(os.path.join('reference', 'routing'), lambda f: f.startswith('seg') and f.endswith('.json'))
        print('routing     : %d/146 场景档案 %s' % (n_route, 'OK' if n_route == 146 else '(补齐: 见 stages/2 路由流程)'))
        print('map assets  : %s' % ('OK' if geo else 'MISSING'))
        print('data schema : %s' % ('OK' if has_schema else 'MISSING (python scripts/build_schemas.py)'))
        ok &= n_rec == 146 and n_cards == 146 and geo and has_schema
        smoke = os.path.join(skill, 'scripts', 'test_helpers.py')
        print('smoke test  : python "%s"' % smoke if os.path.exists(smoke) else 'smoke test  : MISSING')
    else:
        print('skill dir   : NOT FOUND (不在源目录, 也未装到任何 agent 路径)')
        ok = False

    # agent 安装状态
    print('agents      :')
    H = os.path.expanduser('~')
    cfg = os.environ.get('XDG_CONFIG_HOME') or os.path.join(H, '.config')
    for name, p in [
        ('agents(canonical)', os.path.join(H, '.agents', 'skills', 'paper-figures')),
        ('zcode', os.path.join(H, '.zcode', 'skills', 'paper-figures')),
        ('claude', os.path.join(os.environ.get('CLAUDE_CONFIG_DIR') or os.path.join(H, '.claude'), 'skills', 'paper-figures')),
        ('codex', os.path.join(os.environ.get('CODEX_HOME') or os.path.join(H, '.codex'), 'skills', 'paper-figures')),
        ('opencode', os.path.join(cfg, 'opencode', 'skills', 'paper-figures')),
    ]:
        if os.path.exists(p):
            kind = 'link' if os.path.islink(p) else 'dir'
            print('  %-18s INSTALLED (%s)' % (name, kind))
        else:
            print('  %-18s -' % name)

    print('RESULT: %s' % ('HEALTHY' if ok else 'NEEDS ATTENTION'))
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
