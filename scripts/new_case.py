# -*- coding: utf-8 -*-
"""新案例脚手架: 复制最接近的配方 → 登记卡片 → 提示手工登记 catalog。

用法:
  python scripts/new_case.py --from 001 --name my_violin --title "Nature 小提琴图变体"
步骤:
  1. 复制 scripts/recipes/case_seg<from>.py → scripts/recipes/case_<name>.py
  2. 在 gallery/cards/ 生成卡片草稿(卡头待填 purpose/data)
  3. 提示你手工把条目加进 catalog.json(含 seg 分配规则), 然后重跑 build_index.py
"""
import os
import sys
import json
import shutil
import argparse
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--from', dest='src', required=True, help='参考配方 seg 号(3 位或纯数字)')
    ap.add_argument('--name', required=True, help='新案例名(kebab-case, 如 my-violin)')
    ap.add_argument('--title', default='', help='一句话标题')
    args = ap.parse_args()

    src_seg = '%03d' % int(args.src)
    src = os.path.join(ROOT, 'scripts', 'recipes', 'case_seg%s.py' % src_seg)
    dst = os.path.join(ROOT, 'scripts', 'recipes', 'case_%s.py' % args.name)
    if not os.path.exists(src):
        print('source recipe not found:', src)
        sys.exit(1)
    if os.path.exists(dst):
        print('target exists:', dst)
        sys.exit(1)
    shutil.copy(src, dst)
    head = open(dst, encoding='utf-8').read()
    # 脚手架可能被复制到技能目录外使用: 注入技能 scripts 绝对路径, 保证 paper_style 可导入
    skill_scripts = os.path.abspath(os.path.join(HERE))
    old_head = "sys.path.insert(0, os.path.join(HERE, '..'))"
    new_head = ("HERE = os.path.dirname(os.path.abspath(__file__))  # 用户目录(产物)\n"
                "sys.path.insert(0, r'%s')  # 技能 scripts 目录(绝对路径, 移动脚本也不失效)" % skill_scripts)
    if old_head in head:
        head = head.replace(old_head, new_head)
    marker = '"""'
    if marker in head:
        i = head.index(marker)
        head = head[:i] + '"""%s — %s\n改自 case_seg%s.py (%s)。数据段待替换为真实数据。\n参考:' % (
            args.name, args.title or '（待补标题）', src_seg, date.today().isoformat()) + head[i + 3:]
        open(dst, 'w', encoding='utf-8').write(head)

    card = os.path.join(ROOT, 'gallery', 'cards', 'case_%s.md' % args.name)
    with open(card, 'w', encoding='utf-8') as f:
        f.write('---\ntitle: %s\nkind: 数据图\npurpose: [待填]\ndata: [待填: 数据形状]\n'
                'recipe: scripts/recipes/case_%s.py\npreview: [渲染后填写]\n---\n\n'
                '（草稿卡片：渲染通过后补 purpose/data/一句话点评，并把条目登记进 catalog.json）\n'
                % (args.title or args.name, args.name))
    print('scaffold created:')
    print('  recipe:', dst)
    print('  card  :', card)
    print('next steps:')
    print('  1) 编辑配方替换数据段并渲染自检')
    print('  2) 在 catalog.json 登记条目(新 seg 号或替换旧条目)')
    print('  3) python scripts/gen_cards.py && python scripts/build_index.py')


if __name__ == '__main__':
    main()
