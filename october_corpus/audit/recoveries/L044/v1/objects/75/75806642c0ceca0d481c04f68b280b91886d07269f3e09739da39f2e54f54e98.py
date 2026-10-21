#!/usr/bin/env python3
"""Operational bindings/scope/native replay; this is not a proof checker."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
from pypdf import PdfReader


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify(root, rows):
    for row in rows:
        data = (root / row['path']).read_bytes()
        require(len(data) == row['bytes'], 'size: ' + row['path'])
        require(digest(data) == row['sha256'], 'hash: ' + row['path'])
    return len(rows)


def scope_check(s):
    require(s['source_id'] == 'L044', 'source')
    require(s['pages'] == 3, 'native scope')
    require(s['parameters'] == {'n': '2t+6', 'rank_K': 't+1',
                               't': 'odd >=5'}, 'parameters')
    require(not s['whole_L044_recovered'], 'whole-source scope')
    for k in ('new_original_credit', 'new_question_credit',
              'new_formal_declarations'):
        require(s[k] == 0, k)
    require(s['new_factor'] is None, 'factor scope')
    for k in ('no_projected_IP', 'no_alternating_induction',
              'no_even_degree_rigidity'):
        require(s[k] is True, k)
    require(s['required_new_finite_programs'] == [], 'finite premise')
    require(s['operational_files'] == ['check.py'], 'operational role')
    require(s['roles']['current_distinct_acceptance'] is None,
            'author/reviewer separation')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--study-root', type=Path)
    ap.add_argument('--render', action='store_true')
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    here = Path(__file__).resolve().parent
    manifest = json.loads((here / 'manifest.json').read_text())
    exports = verify(here, manifest['exports'])
    dependencies = json.loads((here / 'dependencies.json').read_text())
    external = (verify(args.study_root, dependencies['bindings'])
                if args.study_root else None)
    scope = json.loads((here / 'scope.json').read_text())
    scope_check(scope)
    controls = []
    for key, value in [('whole_L044_recovered', True),
                       ('new_original_credit', 1),
                       ('new_question_credit', 1),
                       ('new_formal_declarations', 1),
                       ('new_factor', 1.0),
                       ('no_projected_IP', False),
                       ('no_alternating_induction', False),
                       ('no_even_degree_rigidity', False),
                       ('required_new_finite_programs', ['invented.py'])]:
        bad = copy.deepcopy(scope)
        bad[key] = value
        try:
            scope_check(bad)
        except ValueError:
            controls.append(key)
        else:
            raise ValueError('missed documentary control: ' + key)
    native = json.loads((here / 'native.json').read_text())
    pdf = here / native['pdf']
    if args.render:
        build = args.out / 'native'
        build.mkdir()
        shutil.copyfile(here / native['source_tex'], build / native['source_tex'])
        engine = shutil.which(native['engine']) or '/opt/homebrew/bin/pdflatex'
        for run in (1, 2):
            result = subprocess.run(
                [engine, '-interaction=nonstopmode', '-halt-on-error',
                 native['source_tex']], cwd=build,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)
            (build / ('pass%d.log' % run)).write_bytes(result.stdout)
        log = (build / 'four_fixed_transitive.log').read_text()
        require(not any(x in log for x in
                        ('LaTeX Warning:', 'Overfull', 'Underfull',
                         'Undefined control sequence')), 'render diagnostics')
        pdf = build / native['pdf']
    pages = [p.extract_text() or '' for p in PdfReader(pdf).pages]
    require(len(pages) == native['pages'] == 3, 'page count')
    require([digest(p.encode()) for p in pages] == native['page_text_sha256'],
            'native page texts')
    report = {'status': 'PASS', 'exports': exports,
              'external_bindings': external, 'pages': len(pages),
              'documentary_controls': controls,
              'mathematical_proof_automatically_verified': False,
              'new_finite_premises': 0, 'render': args.render}
    (args.out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
