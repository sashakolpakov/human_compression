#!/usr/bin/env python3
"""Portable binding/render driver, not an analytic proof checker."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

HERE = Path(__file__).resolve().parent


def require(value, message):
    if not value:
        raise ValueError(message)


def load(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def binding(root, record):
    path = root/record['path']
    require(path.stat().st_size == record['bytes'], 'bound size: '+record['path'])
    require(sha(path) == record['sha256'], 'bound hash: '+record['path'])


def semantic(scope, deps, routes, inventory):
    require(scope['status'] == 'AUTHOR_FROZEN_AWAITING_DISTINCT_SCIENTIFIC_REVIEW', 'review status')
    require(scope['principal_claim'] == 'Theorem 1.3: strong three-dimensional side lengths have density strictly less than one', 'principal claim')
    for key in ['new_original_credit', 'new_question_credit', 'new_Lean', 'required_finite_programs']:
        require(scope[key] == 0, key)
    require(scope['measurement'] is None, 'no factor')
    require(scope['all_literal_source_assertions_reproved'] is False, 'no theorem-set equivalence')
    require(scope['unresolved'] == ['Conjecture 1.1', 'higher-dimensional extension', 'weaker distinct-box condition', 'general multiplicative weights in Remark 4(i)', 'improved exponential error in Remark 4(ii)'], 'scope limitations')
    require(scope['parameters'] == {'epsilon': '1/100', 'c': '49/50', 'kappa': '21/20', 'z': 'exp(log(x)/(log_2(x))^2)', 'Y': 'exp(log(x)/(10*log_2(x)))'}, 'fixed parameters')
    require(len(deps['whole_paid_companions']) == 2, 'both whole companions paid')
    require(deps['whole_paid_companions'][0]['pages'] == 5 and deps['whole_paid_companions'][1]['pages'] == 4, 'full prior papers')
    require({r['name'] for r in deps['retained_classical_inputs']} >= {'Chebyshev prime bound', 'Euler summation for zeta'}, 'classical inputs')
    table = {r['source']: r for r in routes['rows']}
    require(table['Conjecture 1.1']['disposition'] == 'OPEN', 'open conjecture')
    require(table['Theorem 1.3']['disposition'] == 'NEW_WRITTEN_PROOF_PENDING_REVIEW', '3D review scope')
    for name in ['Remark 4(i): general multiplicative weight', 'Remark 4(ii): improved exponential error']:
        require(table[name]['disposition'] == 'ANCILLARY_NOT_REPROVED', 'remark boundary')
    require(len(inventory['programs']) == 2, 'whole executable inventory')
    require({r['role'] for r in inventory['programs']} == {'OPERATIONAL_BINDING_RENDER_DRIVER', 'OPTIONAL_VALIDATION'}, 'no finite premise')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--study-root', type=Path)
    parser.add_argument('--render', action='store_true')
    parser.add_argument('--validate', action='store_true')
    parser.add_argument('--pdflatex', default='/opt/homebrew/bin/pdflatex')
    args = parser.parse_args(); start = time.monotonic()
    args.out.mkdir(parents=True, exist_ok=True)
    frozen = []
    if (HERE/'manifest.json').exists():
        frozen = load(HERE/'manifest.json')['exports']
        for row in frozen: binding(HERE, row)
    deps, scope, routes, inventory = [load(HERE/name) for name in ['dependencies.json', 'scope.json', 'source_map.json', 'program_inventory.json']]
    semantic(scope, deps, routes, inventory)
    author_manifest = load(HERE/'inherited/planar/manifest.json')
    require(sha(HERE/'inherited/planar/manifest.json') == '3c218b6f2a58276ca7566b7f94a0b687d7e3e486f4841532e420743080d3fb22', 'planar author pin')
    for row in author_manifest['exports']: binding(HERE/'inherited/planar', row)
    for row in deps['local_exact_records']: binding(HERE, row)
    external = 0
    if args.study_root:
        for row in deps['external_records']:
            binding(args.study_root, row); external += 1
    controls = []
    variants = []
    for key in ['new_original_credit', 'new_question_credit', 'new_Lean', 'required_finite_programs', 'measurement']:
        bad = copy.deepcopy(scope); bad[key] = 1; variants.append((key, bad, deps, routes, inventory))
    bad = copy.deepcopy(scope); bad['all_literal_source_assertions_reproved'] = True
    variants.append(('unqualified source equivalence', bad, deps, routes, inventory))
    bad = copy.deepcopy(scope); bad['unresolved'] = []
    variants.append(('erase open/ancillary limits', bad, deps, routes, inventory))
    bad = copy.deepcopy(scope); bad['parameters']['c'] = '9/10'
    variants.append(('reuse inadequate source threshold', bad, deps, routes, inventory))
    bad = copy.deepcopy(deps); bad['whole_paid_companions'] = bad['whole_paid_companions'][:1]
    variants.append(('omit paid geometric companion', scope, bad, routes, inventory))
    bad = copy.deepcopy(deps); bad['retained_classical_inputs'] = []
    variants.append(('erase retained prime estimate', scope, bad, routes, inventory))
    bad = copy.deepcopy(inventory); bad['programs'][0]['role'] = 'REQUIRED_FINITE_PREMISE'
    variants.append(('promote optional calculation', scope, deps, routes, bad))
    for name, s, d, r, inv in variants:
        try: semantic(s, d, r, inv)
        except ValueError: controls.append(name)
        else: raise ValueError('control accepted: '+name)
    with tempfile.TemporaryDirectory(prefix='F008_3D_binding_') as tmp:
        p = Path(tmp)/'file'; p.write_text('one')
        row = {'path': 'file', 'bytes': 3, 'sha256': sha(p)}
        p.write_text('two')
        try: binding(Path(tmp), row)
        except ValueError: controls.append('same-size hash corruption')
        else: raise ValueError('hash control accepted')
    validation = None
    if args.validate:
        from check_algebra import run
        validation = run()
        require(validation == load(HERE/'optional_validation.json'), 'exact optional algebra receipt')
    render = None
    if args.render:
        from pypdf import PdfReader
        target = args.out/'render'; target.mkdir(exist_ok=True)
        shutil.copyfile(HERE/'three_dimensional.tex', target/'three_dimensional.tex')
        for i in range(2):
            p = subprocess.run([args.pdflatex, '-halt-on-error', '-interaction=nonstopmode', 'three_dimensional.tex'], cwd=target, capture_output=True, text=True)
            (target/f'render{i}.log').write_text(p.stdout+p.stderr)
            require(p.returncode == 0, 'pdfLaTeX run')
        log = (target/'three_dimensional.log').read_text()
        require(not any(word in log for word in ['Overfull', 'undefined', 'LaTeX Warning:', 'Package hyperref Warning:']), 'clean final render')
        expected = [(p.extract_text() or '') for p in PdfReader(HERE/'three_dimensional.pdf').pages]
        actual = [(p.extract_text() or '') for p in PdfReader(target/'three_dimensional.pdf').pages]
        require(actual == expected, 'exact complete page text')
        render = {'pages': len(actual), 'all_page_texts_exact': True, 'diagnostics': []}
    report = {'status': 'PASS', 'scope': 'Bindings, scope controls, optional finite algebra and page-text replay only; analytic validity requires full written review.',
              'frozen_exports': len(frozen), 'inherited_author_exports': len(author_manifest['exports']),
              'external_bindings': external, 'source_rows': len(routes['rows']),
              'controls': controls, 'optional_validation': validation, 'render': render,
              'seconds': time.monotonic()-start}
    (args.out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ['status', 'frozen_exports', 'inherited_author_exports', 'external_bindings', 'source_rows', 'seconds']}))


if __name__ == '__main__': main()
