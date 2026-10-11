#!/usr/bin/env python3
"""Dispatch the two existing Lean checkers; preserve their fresh reports.

Default: the canonical Lake library AND Topic B's separate proof packet.
No previous successful report is accepted in place of a fresh child run.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

COMPONENTS = ('legacy', 'topic-b')
FORMAL = Path('research/case_study/formal')
TOPIC_B = Path('papers/topic-b/v2')


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def repository(explicit):
    if explicit:
        candidates = [explicit.resolve()]
    else:
        candidates = [Path.cwd(), *Path.cwd().parents, *Path(__file__).resolve().parents]
    for root in candidates:
        if (root / 'scripts/check_lean.py').is_file() and (root / TOPIC_B / 'check.py').is_file():
            return root
    raise RuntimeError('Cannot locate both existing checkers; pass --repo CHECKOUT.')


def inventory(root):
    old = sorted(p for p in (root / FORMAL).glob('*.lean') if p.name != 'lakefile.lean')
    need(old, 'No canonical Lean modules found.')
    result = {}
    for key, checker, sources, support in [
        ('legacy', Path('scripts/check_lean.py'), old,
         [FORMAL / n for n in ('lakefile.lean', 'lean-toolchain', 'dependency_manifest.json')]
         + [p.relative_to(root).with_suffix('.check.json') for p in old]),
        ('topic-b', TOPIC_B / 'check.py', [root / TOPIC_B / 'formal/ResidualGeneration.lean'],
         [TOPIC_B / n for n in ('manifest.json', 'formal/scope.json',
                                'formal/dependency_manifest.json')])]:
        paths = [checker, *[p.relative_to(root) for p in sources], *support]
        need(all((root / p).is_file() and not (root / p).is_symlink() for p in paths),
             key + ': missing or symlinked input')
        bindings = {str(p): sha(root / p) for p in paths}
        result[key] = dict(checker=str(checker), checker_sha256=bindings[str(checker)],
            sources=[dict(path=str(p.relative_to(root)), sha256=sha(p)) for p in sources],
            input_bindings=bindings)
    return result


def validate_report(key, report, row, root):
    need(report.get('status') == 'PASS', key + ': child report did not pass')
    if key == 'legacy':
        modules = report['modules']
        actual = {m['source_path']: m['source_sha256'] for m in modules}
        expected = {s['path']: s['sha256'] for s in row['sources']}
        need(len(modules) == len(actual) and actual == expected, 'legacy: exact fresh source coverage')
        need(report['checker_sha256'] == row['checker_sha256'], 'legacy: checker report binding')
        need(report['compiled_modules'] == report['module_count'] == len(modules),
             'legacy: inconsistent compiled count')
        need(all(m['exit_code'] == 0 for m in modules), 'legacy: failed module in PASS report')
        declarations = sum(len(m['axiom_reports']) for m in modules)
        need(report['axiom_declarations'] == declarations, 'legacy: declaration-report count')
    else:
        need(report['source_sha256'] == row['sources'][0]['sha256'], 'topic-b: source report binding')
        need(report['author_manifest_sha256'] == row['input_bindings'][str(TOPIC_B / 'manifest.json')],
             'topic-b: packet report binding')
        names = load(root / TOPIC_B / 'formal/scope.json')['reported_declarations']
        need([r['name'] for r in report['axioms']] == names, 'topic-b: exact declaration reports')
        need(all(set(r['axioms']) <= {'propext', 'Classical.choice', 'Quot.sound'}
                 for r in report['axioms']), 'topic-b: nonstandard axiom')
        runs = {r['label']: r['returncode'] for r in report['executions']}
        expected_labels = {'ResidualGeneration', 'without_membership', 'without_outside',
                           'without_maximality'}
        need(set(runs) == expected_labels and len(report['executions']) == 4 and
             runs['ResidualGeneration'] == 0 and
             all(runs[n] != 0 for n in expected_labels - {'ResidualGeneration'}),
             'topic-b: actual compilation and three weakened-hypothesis controls')
        need(report['altered_countermodel_rejected'] is True and
             len(report['finite_hypothesis_countermodels']) == 3, 'topic-b: finite controls')
        declarations = len(names)
    return dict(fresh_source_count=len(row['sources']), axiom_declaration_reports=declarations,
                sources=row['sources'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, help='Checkout; auto-detected from cwd/script ancestors if omitted.')
    parser.add_argument('--lean', type=Path, required=True)
    parser.add_argument('--packages', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--jobs', type=int, default=2, help='Legacy checker worker limit; Topic B runs serially.')
    parser.add_argument('--components', nargs='+', choices=['all', *COMPONENTS], default=['all'])
    args = parser.parse_args()
    need(args.jobs > 0, '--jobs must be positive')
    need(len(args.components) == len(set(args.components)), 'No repeated component selection')
    need('all' not in args.components or args.components == ['all'], 'Use all alone')
    chosen = list(COMPONENTS) if args.components == ['all'] else [
        key for key in COMPONENTS if key in args.components]
    root = repository(args.repo)
    need(not args.out.exists() and not args.out.is_symlink(), 'Output must be fresh, including dangling symlinks')
    out = args.out.resolve()
    need(not out.is_relative_to(root) and not out.is_relative_to(Path(__file__).resolve().parent),
         'Output must be outside the checkout and runner packet')
    out.mkdir(parents=True)
    start = time.monotonic()
    report = dict(status='RUNNING', started_utc=datetime.now(timezone.utc).isoformat(),
        runner_sha256=sha(Path(__file__)), repository=str(root), selected_components=chosen,
        jobs=args.jobs, components={},
        scope='Fresh runs of the existing Lean checkers; not formalization of all manuscript proofs.',
        cached_external_objects_trusted=True, prior_reports_used_as_fresh_results=False)

    def save():
        report['elapsed_seconds'] = round(time.monotonic() - start, 3)
        (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')

    save()
    try:
        inputs = inventory(root)
        report['input_inventory'] = inputs
        report['configured_source_count_inventory_only'] = sum(len(r['sources']) for r in inputs.values())
        report['lean_executable_sha256'] = sha(args.lean.resolve())
        report['packages_path'] = str(args.packages.resolve())
        for key in COMPONENTS:
            report['components'][key] = dict(status='PENDING' if key in chosen else 'NOT_SELECTED')
        env = dict(os.environ)
        for name in ('LEAN_PATH', 'LEAN_SRC_PATH', 'PYTHONOPTIMIZE'):
            env.pop(name, None)
        for key in chosen:
            row = inputs[key]
            component = report['components'][key]
            command = [sys.executable, '-B', '-E', str(root / row['checker']),
                       '--lean', str(args.lean.resolve()), '--packages', str(args.packages.resolve()),
                       '--out', str(out / key)]
            if key == 'legacy':
                command += ['--jobs', str(args.jobs)]
            component.update(status='RUNNING', command=command, checker_sha256=row['checker_sha256'])
            save()
            print('Checking ' + key + '; child output is in ' + str(out), flush=True)
            with (out / (key + '.stdout')).open('wb') as stdout, (out / (key + '.stderr')).open('wb') as stderr:
                result = subprocess.run(command, cwd=root, env=env, stdout=stdout, stderr=stderr)
            component.update(exit_code=result.returncode,
                stdout_sha256=sha(out / (key + '.stdout')), stderr_sha256=sha(out / (key + '.stderr')))
            child_path = out / key / 'report.json'
            if child_path.is_file():
                component.update(report_path=str(child_path.relative_to(out)), report_sha256=sha(child_path))
            need(result.returncode == 0, key + ': checker process failed; inspect preserved child logs/report')
            need(child_path.is_file() and not child_path.is_symlink(), key + ': missing fresh child report')
            need(all(sha(root / p) == h for p, h in row['input_bindings'].items()),
                 key + ': input changed during check')
            component.update(validate_report(key, load(child_path), row, root), status='PASS')
            save()
        need(inventory(root) == inputs, 'Input inventory changed during the invocation')
        report['fresh_source_count'] = sum(report['components'][key]['fresh_source_count'] for key in chosen)
        report['fresh_axiom_declaration_reports'] = sum(
            report['components'][key]['axiom_declaration_reports'] for key in chosen)
        complete = set(chosen) == set(COMPONENTS)
        report.update(status='PASS_FULL_CONFIGURED_PROJECT' if complete else 'PASS_PARTIAL',
            all_configured_sources_recompiled_this_invocation=complete,
            coverage_label='Both configured components freshly checked' if complete else
                           'Only explicitly selected components freshly checked',
            unchecked_sources=[s for key in COMPONENTS if key not in chosen for s in inputs[key]['sources']])
        save()
        print(report['status'] + ': ' + str(report['fresh_source_count']) + ' source files; ' + str(out / 'report.json'))
        return 0
    except (Exception, KeyboardInterrupt) as exc:
        for component in report['components'].values():
            if component['status'] == 'RUNNING':
                component['status'] = 'FAIL'
            elif component['status'] == 'PENDING':
                component['status'] = 'NOT_RUN_AFTER_FAILURE'
        report.update(status='FAIL', error=str(exc), all_configured_sources_recompiled_this_invocation=False,
            fresh_source_count=sum(c.get('fresh_source_count', 0) for c in report['components'].values()
                                   if c['status'] == 'PASS'))
        save()
        print('FAIL: ' + str(exc) + '; ' + str(out / 'report.json'), file=sys.stderr)
        return 130 if isinstance(exc, KeyboardInterrupt) else 1


if __name__ == '__main__':
    sys.exit(main())
