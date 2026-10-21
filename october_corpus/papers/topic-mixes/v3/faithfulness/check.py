#!/usr/bin/env python3
"""Replay the bounded F007 diagnostics and our six generic Lean declarations."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

P = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def run(command, cwd=None, env=None):
    result = subprocess.run(list(map(str, command)), cwd=cwd, env=env,
                            capture_output=True, text=True, timeout=180)
    return result.returncode, result.stdout + result.stderr


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--render', action='store_true')
    ap.add_argument('--source', type=Path)
    ap.add_argument('--packages', type=Path,
                    default=Path('/Users/sasha/bogachev/formal/.lake/packages'))
    ap.add_argument('--lean', default='/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean')
    ap.add_argument('--xelatex', default='/opt/homebrew/bin/xelatex')
    a = ap.parse_args()
    need(not a.out.exists(), 'Use a fresh output directory')
    a.out.mkdir(parents=True)
    a.out = a.out.resolve()
    source = json.loads((P / 'source_contract.json').read_text())['source']
    if a.source:
        data = a.source.read_bytes()
        need(len(data) == source['bytes'] and hashlib.sha256(data).hexdigest() == source['sha256'],
             'Different source edition')
    if (P / 'manifest.json').exists():
        for row in json.loads((P / 'manifest.json').read_text())['exports']:
            data = (P / row['path']).read_bytes()
            need(len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'],
                 'Changed frozen export: ' + row['path'])
    rc, text = run([sys.executable, '-B', '-O', P / 'check_small_maps.py'])
    (a.out / 'small_maps.json').write_text(text)
    need(rc == 0 and json.loads(text)['corrected_torus_contains_example_after_layer_exchange'],
         'Exact small-map diagnostic failed')
    companion = [sys.executable, '-B', '-O', P / 'companion/check.py', '--out', a.out / 'companion']
    if a.render:
        companion.append('--render')
    rc, text = run(companion)
    (a.out / 'companion.log').write_text(text)
    need(rc == 0, 'Bounded companion replay failed')
    pins = json.loads((P / 'dependency_manifest.json').read_text())
    libraries = []
    for row in pins['packages']:
        package = a.packages / row['name']
        rc, text = run(['git', '-C', package, 'rev-parse', 'HEAD'])
        need(rc == 0 and text.strip() == row['rev'], 'Different package: ' + row['name'])
        rc, text = run(['git', '-C', package, 'diff', '--quiet', 'HEAD', '--'])
        need(rc == 0, 'Modified package: ' + row['name'])
        library = package / '.lake/build/lib/lean'
        if library.is_dir():
            libraries.append(str(library))
    rc, text = run([a.lean, '--version'])
    need(rc == 0 and 'version 4.32.2,' in text, 'Different Lean version')
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(libraries))
    env.pop('LEAN_SRC_PATH', None)
    raw = (P / 'RelationFibers.lean').read_text()
    clean = re.sub(r'/\-.*?\-/|--[^\n]*', '', raw, flags=re.S)
    need(not re.search(r'\b(sorry|admit|axiom|native_decide)\b', clean), 'Formal placeholder')
    rc, text = run([a.lean, '--root=' + str(P), '-o', a.out / 'RelationFibers.olean',
                    P / 'RelationFibers.lean'], env=env)
    (a.out / 'RelationFibers.log').write_text(text)
    need(rc == 0 and 'warning:' not in text, 'Lean verification failed')
    declarations = re.findall(
        r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",
        text, re.S)
    expected = json.loads((P / 'formal_scope.json').read_text())['declarations']
    need([name.split('.')[-1] for name, _ in declarations] == expected, 'Declaration inventory')
    for _, axioms in declarations:
        need(set(re.findall(r'[A-Za-z][\w.]*', axioms)) <= {'propext', 'Classical.choice', 'Quot.sound'},
             'Unexpected axiom')
    rendered = []
    if a.render:
        from pypdf import PdfReader
        rd = a.out / 'render'
        rd.mkdir()
        for name, pages in [('relations_and_flags', 4), ('faithfulness_application', 5)]:
            shutil.copyfile(P / (name + '.tex'), rd / (name + '.tex'))
            for i in range(2):
                rc, text = run([a.xelatex, '-interaction=nonstopmode', '-halt-on-error', name + '.tex'], rd)
                (a.out / (name + str(i) + '.log')).write_text(text)
                need(rc == 0, 'Render failed: ' + name)
            need(not re.search('Overfull|Missing character|LaTeX Warning|Font Warning', text),
                 'Render diagnostic: ' + name)
            old = [p.extract_text() for p in PdfReader(P / (name + '.pdf')).pages]
            new = [p.extract_text() for p in PdfReader(rd / (name + '.pdf')).pages]
            need(old == new and len(new) == pages, 'Changed page text: ' + name)
            rendered.append({'paper': name, 'pages': pages, 'exact_page_text': True})
    report = {'status': 'PASS_BOUNDED_AUTHOR_REPLAY', 'partial_Lean_declarations': len(declarations),
              'full_source_formalization': False, 'new_required_programs': 0,
              'new_optional_diagnostics': 2, 'source_edition_checked': bool(a.source),
              'renders': rendered, 'whole_source_credit': 0, 'new_question_credit': 0,
              'compression_factor': None, 'software_inclusive_factor': None}
    (a.out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
