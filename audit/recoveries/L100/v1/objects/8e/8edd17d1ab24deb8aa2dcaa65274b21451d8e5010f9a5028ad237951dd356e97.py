"""Bounded receipt/audit controls. Never execute the L100 search driver."""
import argparse
import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

if not __debug__:
    raise SystemExit('optimized execution forbidden')
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('target_wrapper', HERE / 'run_target.py')
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    out = args.out
    w.require(out.is_absolute(), 'absolute output required')
    out.mkdir(parents=True, exist_ok=False)
    checks = []

    def check(name, condition):
        w.require(condition, name)
        checks.append(name)

    def rejects(name, fn):
        try:
            fn()
        except (ValueError, OSError, KeyError, TypeError):
            checks.append(name)
            return
        raise AssertionError('accepted damage: ' + name)

    rows = [[3, [], []], [2, [1, 0], [1]], [1, [2, 0], [1]]]
    requested = [3, 2, 1]
    text = '\n'.join('BOREL_COMPLETE id=%d rank_counts=%s full_group_ranks=%s' % tuple(r) for r in rows) + '\n'
    check('parse exact prefix', w.completed_rows(text, requested) == rows)
    rejects('duplicate anchor', lambda: w.completed_rows(text + text, requested))
    rejects('missing intermediate anchor', lambda: w.completed_rows(text.splitlines()[0] + '\n' + text.splitlines()[2], requested))
    rejects('wrong anchor order', lambda: w.completed_rows('\n'.join(reversed(text.splitlines())), requested))
    rejects('malformed complete marker', lambda: w.completed_rows('BOREL_COMPLETE id=3 rank_counts=broken', requested))
    rejects('premature final marker', lambda: w.completed_rows(text.splitlines()[0] + '\n' + w.FINAL, requested))
    rejects('duplicate final marker', lambda: w.completed_rows(text + w.FINAL + '\n' + w.FINAL, requested))
    returned = dict(status='RETURNED', returncode=0)
    for name, execution, err, txt, rr, audit, same, expected in [
        ('complete', returned, '', text + w.FINAL, rows, True, True, 'COMPLETE_REQUEST'),
        ('deadline', dict(status='DEADLINE', returncode=-9), '', text.splitlines()[0], rows[:1], True, True, 'PARTIAL_DEADLINE'),
        ('deadline even after all markers', dict(status='DEADLINE', returncode=-9), '', text + w.FINAL, rows, True, True, 'PARTIAL_DEADLINE'),
        ('nonzero', dict(status='RETURNED', returncode=1), '', text, rows, True, True, 'FAILED_EXECUTION'),
        ('interrupted', dict(status='INTERRUPTED', returncode=-9), '', text, rows, True, True, 'FAILED_EXECUTION'),
        ('warning', returned, 'Syntax warning', text + w.FINAL, rows, True, True, 'FAILED_EXECUTION'),
        ('GAP error stdout', returned, '', 'Error, failure\n' + text, rows, True, True, 'FAILED_EXECUTION'),
        ('missing final marker', returned, '', text, rows, True, True, 'INCOMPLETE_RETURN'),
        ('failed returned audit', returned, '', text + w.FINAL, rows, False, True, 'FAILED_RETURNED_ANCHOR_AUDIT'),
        ('changed input', returned, '', text + w.FINAL, rows, True, False, 'INVALIDATED_INPUT_CHANGE'),
    ]:
        check('classifier ' + name, w.classify(execution, err, txt, rr, requested, audit, same) == expected)

    reject_pin = out / 'pin.txt'
    reject_pin.write_text('one')
    original = w.pin(reject_pin)
    reject_pin.write_text('two')
    check('actual changed file', not w.unchanged([original]))
    reject_pin.unlink()
    check('actual missing file', not w.unchanged([original]))
    rejects('relative runtime namespace', lambda: w.resolve_row(dict(path='a', namespace='runtime')))
    rejects('unknown namespace', lambda: w.resolve_row(dict(path='/a', namespace='invented')))
    rejects('escaping study', lambda: w.resolve_row(dict(path='../a', namespace='study')))
    rejects('absolute wrong study', lambda: w.resolve_row(dict(path='/private/tmp/a', namespace='study')))

    # Actual generic process controller, using only tiny independent Python children.
    p = w.phase([sys.executable, '-c', 'print("clean")'], out / 'process_clean', 5, False)
    check('actual clean child', w.clean_phase(p, out / 'process_clean'))
    p = w.phase([sys.executable, '-c', 'import time; print("started",flush=True); time.sleep(2)'], out / 'process_deadline', 0.1, False)
    check('actual deadline waited', p['status'] == 'DEADLINE' and p['returncode'] is not None and p['child_pid'] > 0)
    p = w.phase(['/nonexistent/L100_control_executable'], out / 'process_launch_failure', 1, False)
    check('actual failed launch receipt', p['status'] == 'LAUNCH_FAILED' and (out / 'process_launch_failure/receipt.json').exists())

    # Reuse exact completed tiny S3 fixtures: no call to RunBorel or any search.
    fixture = w.P / 'small_models01/S3'
    literal = out / 'literal'
    shutil.copytree(fixture, literal)
    fixture_pins = [w.pin(p) for p in sorted(fixture.glob('*.g'))]
    setup = 'G:=SymmetricGroup(3);;reps:=[Group(()),Group((2,3)),AlternatingGroup(3),G];;'
    actual = [[4, [], []], [3, [1, 0], [1]], [2, [1, 0], [1]], [1, [2, 2, 0], [2, 2]]]
    check('all tiny checkpoint files bound', len(w.checkpoint_files(literal, actual)) == 8)

    def audit_trial(name, directory, expected, expected_rows=actual):
        folder = out / name
        folder.mkdir()
        driver = w.audit_driver(folder, directory, expected_rows, setup)
        result = w.phase([str(w.GAP), '-q', '-b', str(driver)], folder / 'process', 5, False)
        txt = (folder / 'process/stdout').read_text()
        ok = w.clean_phase(result, folder / 'process') and txt.splitlines().count('PASS_RETURNED_ANCHOR_AUDIT') == 1
        check(name, ok is expected)

    audit_trial('tiny_actual_returned_records', literal, True)
    changes = [
        ('wrong_borel_order', 'b1_done.g', lambda s: s.replace('order:=1,', 'order:=2,')),
        ('missing_terminal_empty', 'b1_done.g', lambda s: s.replace('[ 2, 2, 0 ]', '[ 2, 2, 1 ]')),
        ('wrong_checkpoint_rank', 'b1_r2.g', lambda s: s.replace('rank:=2', 'rank:=3')),
        ('truncated_checkpoint', 'b1_r3.g', lambda s: s[:len(s)//2]),
        ('missing_full_family', 'b1_done.g', lambda s: 'borelResult:=rec(id:=1,order:=1,levels:=[2,2,0],geometries:=[]);\n'),
        ('changed_panel', 'b1_r3.g', lambda s: s.replace('Group( [ (2,3) ] )', 'Group( [ (1,2,3) ] )', 1)),
        ('duplicate_family_index', 'b1_r2.g', lambda s: s.replace('[ 1, 2 ]', '[ 1, 1 ]', 1)),
        ('wrong_top_empty', 'b4_done.g', lambda s: s.replace('levels:=[]', 'levels:=[0]')),
    ]
    for name, filename, change in changes:
        folder = out / ('input_' + name)
        shutil.copytree(literal, folder)
        (folder / filename).write_text(change((folder / filename).read_text()))
        audit_trial(name, folder, False)
    folder = out / 'input_missing_checkpoint'
    shutil.copytree(literal, folder)
    (folder / 'b1_r2.g').unlink()
    rejects('missing checkpoint pin', lambda: w.checkpoint_files(folder, actual))

    # Actual public CLI only prepares the pinned fixed driver; never runs it.
    prepout = out / 'actual_prepare'
    cmd = [sys.executable, str(HERE / 'run_target.py'), '--prepare-only', '--out', str(prepout)]
    r = w.phase(cmd, out / 'prepare_cli', 20, False)
    check('actual preparation-only CLI', w.clean_phase(r, out / 'prepare_cli'))
    prep = json.loads((prepout / 'receipt.json').read_text())
    check('preparation never launched target', prep['status'] == 'PREPARED_ONLY_NO_TARGET' and prep['target_census'] is False and not (prepout / 'target').exists())
    check('literal fixed 95 anchors', prep['requested_anchors'] == list(range(95, 0, -1)))
    check('preparation pins still exact', w.unchanged(prep['inputs']))

    # Exercise actual main/preflight failure before it creates any output.
    for gate in ['AUTHOR_SHA', 'REVIEW_SHA', 'ADOPTION_SHA']:
        target = out / ('forbidden_' + gate)
        code = ('import importlib.util,sys; sys.dont_write_bytecode=True; '
                's=importlib.util.spec_from_file_location("w",' + repr(str(HERE / 'run_target.py')) + '); '
                'w=importlib.util.module_from_spec(s);s.loader.exec_module(w);w.' + gate + '="0"*64; '
                'sys.argv=["w","--prepare-only","--out",' + repr(str(target)) + '];w.main()')
        r = subprocess.run([sys.executable, '-c', code], capture_output=True, timeout=15)
        (out / (gate + '.stdout')).write_bytes(r.stdout)
        (out / (gate + '.stderr')).write_bytes(r.stderr)
        check('actual pre-output ' + gate + ' rejection', r.returncode != 0 and not target.exists())

    for filename in ['run_target.py', 'controls.py']:
        for style in ['argument', 'environment']:
            forbidden = out / ('optimized_' + filename + '_' + style)
            cmd = [sys.executable] + (['-O'] if style == 'argument' else []) + [str(HERE / filename), '--out', str(forbidden)]
            env = os.environ.copy()
            if style == 'environment':
                env['PYTHONOPTIMIZE'] = '1'
            r = subprocess.run(cmd, env=env, capture_output=True, timeout=5)
            check('pre-output optimization ' + filename + ' ' + style, r.returncode != 0 and not forbidden.exists() and b'optimized execution forbidden' in r.stderr)

    report = dict(status='PASS_L100_TARGET_RECEIPT_CONTROLS_NO_TARGET', target_runs=0,
                  checks=checks, fixture_inputs=fixture_pins,
                  source_inputs=[w.pin(HERE / n) for n in ('run_target.py', 'audit_returned.g', 'controls.py')],
                  preparation_receipt=w.pin(prepout / 'receipt.json'))
    w.save(out / 'report.json', report)
    print(json.dumps(dict(status=report['status'], checks=len(checks), target_runs=0)))


if __name__ == '__main__':
    main()
