# -*- coding: utf-8 -*-
"""paper-figures 多 agent TUI 安装器 — 按 vercel-labs/skills (skills.sh) 框架适配。

布局规范(与 vercel-labs/skills src/agents.ts 对齐):
  canonical : ~/.agents/skills/paper-figures          实体(全平台通用位置, 大量 agent 原生读取)
  zcode     : ~/.zcode/skills/paper-figures          -> 链接 canonical
  claude    : $CLAUDE_CONFIG_DIR/skills/...          -> 链接 (默认 ~/.claude)
  codex     : $CODEX_HOME/skills/...                 -> 链接 (默认 ~/.codex)
  opencode  : $XDG_CONFIG_HOME/opencode/skills/...   -> 链接 (默认 ~/.config)
  gemini    : ~/.gemini/skills/...                   -> 链接
  qwen      : ~/.qwen/skills/...                     -> 链接
  cursor    : ~/.cursor/skills/...                   -> 链接
  copilot   : ~/.copilot/skills/...                  -> 链接
  droid     : ~/.factory/skills/...                  -> 链接
  dsh       : DeepSeek Harness 未被框架收录: 探测 $DSH_HOME/skills, ~/.dsh/skills,
             ~/.deepseek-harness/skills; 未找到则提示 custom:<路径>
  custom:<abs路径>  把 skill 实体安装到该目录(不链接)

链接策略(同 vercel-labs/installer.ts): Windows 用 junction(免管理员), POSIX 用相对
symlink; 失败回退完整复制。重复安装幂等: 已指向 canonical 的链接保持不动。

用法:
  python install.py --list                 # 列出各 agent 状态
  python install.py --agents zcode,claude  # 装指定 agent(默认含 canonical)
  python install.py --all                  # canonical + 全部已探测 agent
  python install.py --lite                 # canonical 不带 gallery 成品图(~2MB)
  python install.py --mode copy            # 全部用复制(不做链接)
  python install.py --commands             # 同时分发 slash commands/prompts
  python install.py --dry-run --all
"""
import argparse
import hashlib
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = 'paper-figures'
HOME = os.path.expanduser('~')

SCRIPTS_TOP = ['paper_style.py', 'test_helpers.py', 'gen_cards.py', 'build_index.py',
               'make_contact_sheet.py', 'new_case.py', 'show.py', 'doctor.py']
EXCLUDE_GALLERY = {'_smoke', '_sheet_demo.png', '_compare_demo.png'}


def xdg_config():
    return os.environ.get('XDG_CONFIG_HOME') or os.path.join(HOME, '.config')


def agent_table():
    """name -> (display, global_skills_dir, installed?) — 对齐 vercel-labs/skills。"""
    claude_home = os.environ.get('CLAUDE_CONFIG_DIR') or os.path.join(HOME, '.claude')
    codex_home = os.environ.get('CODEX_HOME') or os.path.join(HOME, '.codex')
    cfg = xdg_config()
    t = {
        'zcode': ('ZCode', os.path.join(HOME, '.zcode', 'skills'),
                  os.path.isdir(os.path.join(HOME, '.zcode'))),
        'claude': ('Claude Code', os.path.join(claude_home, 'skills'),
                   os.path.isdir(claude_home)),
        'codex': ('Codex', os.path.join(codex_home, 'skills'),
                  os.path.isdir(codex_home)),
        'opencode': ('OpenCode', os.path.join(cfg, 'opencode', 'skills'),
                     os.path.isdir(os.path.join(cfg, 'opencode'))),
        'gemini': ('Gemini CLI', os.path.join(HOME, '.gemini', 'skills'),
                   os.path.isdir(os.path.join(HOME, '.gemini'))),
        'qwen': ('Qwen Code', os.path.join(HOME, '.qwen', 'skills'),
                 os.path.isdir(os.path.join(HOME, '.qwen'))),
        'cursor': ('Cursor', os.path.join(HOME, '.cursor', 'skills'),
                   os.path.isdir(os.path.join(HOME, '.cursor'))),
        'copilot': ('GitHub Copilot', os.path.join(HOME, '.copilot', 'skills'),
                    os.path.isdir(os.path.join(HOME, '.copilot'))),
        'droid': ('Droid', os.path.join(HOME, '.factory', 'skills'),
                  os.path.isdir(os.path.join(HOME, '.factory'))),
        'iflow': ('iFlow CLI', os.path.join(HOME, '.iflow', 'skills'),
                  os.path.isdir(os.path.join(HOME, '.iflow'))),
        'kimi': ('Kimi Code CLI', os.path.join(HOME, '.kimi-code', 'skills'),
                 os.path.isdir(os.path.join(HOME, '.kimi-code')) or os.path.isdir(os.path.join(HOME, '.kimi'))),
        'warp': ('Warp', os.path.join(HOME, '.agents', 'skills'), False),  # universal, 免链接
    }
    dsh = None
    for cand in (os.environ.get('DSH_HOME'),
                 os.path.join(HOME, '.dsh', 'skills'),
                 os.path.join(HOME, '.deepseek-harness', 'skills'),
                 os.path.join(HOME, '.dsh')):
        if cand and os.path.isdir(cand):
            dsh = cand if os.path.basename(cand) == 'skills' else os.path.join(cand, 'skills')
            break
    t['dsh'] = ('DeepSeek Harness', dsh, bool(dsh))
    return t


# ---------- 组装 ----------
def sha1(p):
    h = hashlib.sha1()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 16), b''):
            h.update(chunk)
    return h.hexdigest()


def collect_manifest(lite=False):
    out = []

    def add(src, rel):
        out.append((os.path.join(HERE, src), rel))

    add('SKILL.md', 'SKILL.md')
    add('requirements.txt', 'requirements.txt')
    add('taste.md', 'taste.md')
    if os.path.exists(os.path.join(HERE, 'catalog.json')):
        add('catalog.json', os.path.join('reference', 'catalog.json'))
    ref_base = os.path.join(HERE, 'reference')
    if os.path.isdir(ref_base):
        for f in sorted(os.listdir(ref_base)):
            if f != 'catalog.json':
                add(os.path.join('reference', f), os.path.join('reference', f))
    for d in ('stages', 'integrations'):
        base = os.path.join(HERE, d)
        if os.path.isdir(base):
            for root, _, files in os.walk(base):
                for f in files:
                    p = os.path.join(root, f)
                    add(p, os.path.relpath(p, HERE))
    for f in SCRIPTS_TOP:
        p = os.path.join(HERE, 'scripts', f)
        if os.path.exists(p):
            add(p, os.path.join('scripts', f))
    for sub in ('helpers', 'recipes'):
        base = os.path.join(HERE, 'scripts', sub)
        for f in sorted(os.listdir(base)):
            if f.endswith('.py'):
                add(os.path.join(base, f), os.path.join('scripts', sub, f))
    for f in sorted(os.listdir(os.path.join(HERE, 'assets', 'map_data'))):
        add(os.path.join('assets', 'map_data', f), os.path.join('assets', 'map_data', f))
    gbase = os.path.join(HERE, 'gallery')
    for f in sorted(os.listdir(gbase)):
        p = os.path.join(gbase, f)
        if os.path.isfile(p) and f not in EXCLUDE_GALLERY:
            if f == 'index.md':
                add(p, os.path.join('reference', 'gallery-index.md'))
            elif f.endswith('.png') and not lite:
                add(p, os.path.join('gallery', f))
    cbase = os.path.join(gbase, 'cards')
    for f in sorted(os.listdir(cbase)):
        add(os.path.join(cbase, f), os.path.join('gallery', 'cards', f))
    return out


def materialize(src, dst):
    """内容相同跳过; 否则同盘硬链接, 失败复制。返回动作。"""
    if os.path.exists(dst) and sha1(src) == sha1(dst):
        return 'same'
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst):
        os.remove(dst)
    try:
        if os.path.splitdrive(src)[0].lower() == os.path.splitdrive(dst)[0].lower():
            os.link(src, dst)
            return 'hardlink'
    except OSError:
        pass
    shutil.copy2(src, dst)
    return 'copy'


def dir_size(path):
    total = 0
    for root, _, files in os.walk(path):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return total


# ---------- canonical ----------
def install_canonical(manifest, dry=False):
    dst_root = os.path.join(HOME, '.agents', 'skills', NAME)
    stats = {'hardlink': 0, 'copy': 0, 'same': 0}
    for src, rel in manifest:
        dst = os.path.join(dst_root, rel.replace('/', os.sep))
        if dry:
            stats['same' if (os.path.exists(dst) and sha1(src) == sha1(dst)) else 'copy'] += 1
            continue
        stats[materialize(src, dst)] += 1
    return dst_root, stats, (dir_size(dst_root) / 1e6 if not dry else 0)


# ---------- 链接(按框架: junction/symlink -> 回退复制) ----------
def same_realpath(a, b):
    try:
        ra = os.path.realpath(a)
        rb = os.path.realpath(b)
        return os.path.normcase(ra) == os.path.normcase(rb)
    except OSError:
        return False


def link_skill(canonical, link_path, dry=False):
    """把 canonical 目录以链接/复制形式出现在 link_path。返回动作字符串。"""
    if os.path.exists(link_path) and same_realpath(link_path, canonical):
        return 'linked(already)'
    if dry:
        return 'link'
    if os.path.islink(link_path) or os.path.isdir(link_path):
        # 旧实体/旧链接: 仅当确认是 paper-figures 才替换
        mark = os.path.join(link_path, 'SKILL.md')
        if not (os.path.exists(mark) and 'name: paper-figures' in open(mark, encoding='utf-8', errors='ignore').read()):
            return 'blocked(not-ours)'
        if os.path.islink(link_path):
            os.remove(link_path)
        else:
            shutil.rmtree(link_path)
    os.makedirs(os.path.dirname(link_path), exist_ok=True)
    if sys.platform == 'win32':
        try:
            import _winapi
            _winapi.CreateJunction(canonical, link_path)
            return 'junction'
        except Exception:
            pass
    else:
        try:
            rel = os.path.relpath(canonical, os.path.dirname(link_path))
            os.symlink(rel, link_path)
            return 'symlink'
        except OSError:
            pass
    shutil.copytree(canonical, link_path)
    return 'copy'


# ---------- slash commands 分发 ----------
CMD_DIRS = {
    'claude': lambda: os.path.join(os.environ.get('CLAUDE_CONFIG_DIR') or os.path.join(HOME, '.claude'), 'commands'),
    'zcode': lambda: os.path.join(HOME, '.zcode', 'commands'),
    'opencode': lambda: os.path.join(xdg_config(), 'opencode', 'command'),
    'codex': lambda: os.path.join(os.environ.get('CODEX_HOME') or os.path.join(HOME, '.codex'), 'prompts'),
}


def install_commands(key, dry=False):
    src_dir = os.path.join(HERE, 'integrations', 'commands')
    fn = CMD_DIRS.get(key)
    if not os.path.isdir(src_dir) or not fn:
        return 0
    cmd_dir = fn()
    n = 0
    for f in sorted(os.listdir(src_dir)):
        if f.endswith('.md'):
            n += 1
            if not dry:
                os.makedirs(cmd_dir, exist_ok=True)
                materialize(os.path.join(src_dir, f), os.path.join(cmd_dir, f))
    return n


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--agents', default='',
                    help='逗号分隔: zcode,claude,codex,opencode,gemini,qwen,cursor,copilot,droid,iflow,kimi,dsh,custom:<abs路径>')
    ap.add_argument('--all', action='store_true', help='canonical + 全部已安装 agent')
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--lite', action='store_true', help='canonical 不带 gallery 成品图')
    ap.add_argument('--mode', choices=['link', 'copy'], default='link')
    ap.add_argument('--commands', action='store_true', help='同时分发 slash commands/prompts')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    table = agent_table()
    canonical_default = os.path.join(HOME, '.agents', 'skills', NAME)

    if args.list:
        print('canonical : %s [%s]' % (canonical_default,
                                       'INSTALLED' if os.path.isdir(canonical_default) else 'not-installed'))
        print('agents    (global skills dir -> 状态):')
        for k, (disp, d, inst) in table.items():
            state = '-' if not d else ('INSTALLED' if os.path.isdir(os.path.join(d, NAME)) else 'agent-dir-found')
            print('  %-9s %-18s %s [%s]' % (k, disp, d or '(未探测到)', state))
        print('\n链接框架: vercel-labs/skills (skills.sh) — canonical 实体 + 各 agent junction/symlink')
        return

    keys = []
    if args.all:
        keys = [k for k, (_, d, _) in table.items() if d]
    elif args.agents:
        for raw in [x.strip() for x in args.agents.split(',') if x.strip()]:
            if raw.startswith('custom:'):
                table[raw] = ('Custom', os.path.abspath(raw.split(':', 1)[1]), True)
                keys.append(raw)
            elif raw in table:
                if raw == 'dsh' and not table['dsh'][1]:
                    print('dsh: 未探测到 skills 目录($DSH_HOME/skills, ~/.dsh/skills, ~/.deepseek-harness/skills)。'
                      '确认 DSH 的 skills 目录后用 --agents custom:<该目录>。')
                    continue
                keys.append(raw)
            else:
                print('unknown agent:', raw, '(见 --list)')
                sys.exit(1)
    else:
        ap.print_help()
        return

    manifest = collect_manifest(lite=args.lite)
    print('source: %s  (%d files%s)' % (HERE, len(manifest), ', LITE' if args.lite else ''))

    # 1) canonical 实体
    cdir, stats, mb = install_canonical(manifest, dry=args.dry_run)
    if args.dry_run:
        print('[dry] canonical -> %s  write=%d same=%d' % (
            cdir, stats['copy'], stats['same']))
    else:
        print('[ok ] canonical -> %s  hardlink=%d copy=%d same=%d  %.1f MB' % (
            cdir, stats['hardlink'], stats['copy'], stats['same'], mb))

    # 2) 各 agent 链接
    for k in keys:
        disp, base, _ = table[k]
        link_path = os.path.join(base, NAME)
        if args.mode == 'copy' or k.startswith('custom:'):
            if args.dry_run:
                print('[dry] %-9s -> %s  (copy mode)' % (k, link_path))
                continue
            # 实体复制: 对 custom 就地组装
            n_ok = 0
            for src, rel in manifest:
                if materialize(src, os.path.join(link_path, rel.replace('/', os.sep))) != 'same':
                    n_ok += 1
            print('[ok ] %-9s -> %s  copy-mode files=%d  %.1f MB' % (
                k, link_path, n_ok, dir_size(link_path) / 1e6))
        else:
            act = link_skill(cdir, link_path, dry=args.dry_run)
            print('[%s] %-9s -> %s  %s' % ('dry' if args.dry_run else 'ok ', k, link_path, act))
        if args.commands:
            n = install_commands(k, dry=args.dry_run)
            if n:
                print('      commands/prompts: %d 个 -> %s' % (n, CMD_DIRS.get(k, lambda: '?')()))


if __name__ == '__main__':
    main()
