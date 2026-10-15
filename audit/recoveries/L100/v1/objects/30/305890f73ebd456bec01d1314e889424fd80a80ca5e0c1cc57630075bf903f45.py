"""Freeze exact bounded target interface; this never invokes the target."""
import hashlib
import json
from pathlib import Path
import shutil
if not __debug__:
    raise SystemExit('optimized execution forbidden')
HERE = Path(__file__).resolve().parent
G34 = HERE.parent
OUT = G34 / 'exhaustion_target_interface_v1'
def pin(p):
    b = p.read_bytes()
    return dict(path=str(p), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
def main():
    OUT.mkdir()
    for name in ['run_target.py', 'audit_returned.g', 'controls.py', 'check.py', 'route.rst', 'freeze.py']:
        shutil.copy2(HERE / name, OUT / name)
    control = G34 / 'exhaustion_target_controls01'
    report = json.loads((control / 'report.json').read_text())
    assert report['status'] == 'PASS_L100_TARGET_RECEIPT_CONTROLS_NO_TARGET' and report['target_runs'] == 0
    shutil.copytree(control, OUT / 'author_controls01')
    dependencies = [pin(HERE / n) for n in ['run_target.py', 'audit_returned.g', 'controls.py']]
    dependencies += [pin(G34 / d / 'manifest.json') for d in ['exhaustion_component_v2', 'exhaustion_review_v2', 'exhaustion_adoption_v2']]
    dependencies += [pin(control / 'report.json')]
    (OUT / 'dependencies.json').write_text(json.dumps(dependencies, indent=2) + '\n')
    handoff = dict(status='AUTHOR_COMPLETE_L100_BOUNDED_TARGET_INTERFACE_V1_AWAITING_ROOT_REVIEW',
        scope='One fixed 95..1 traversal, broad primitive mode, 60-second target cap; no target executed.',
        controls=48, target_runs=0, mathematical_delta=None,
        actual_runtime=str(OUT / 'run_target.py'),
        check_command=['/Users/sasha/.venvs/global/bin/python', str(OUT / 'check.py'), '--out', str(G34 / 'TARGET_REVIEW_OUT_REPLACE')],
        proposed_target_command=['/Users/sasha/.venvs/global/bin/python', str(OUT / 'run_target.py'), '--out', str(G34 / 'exhaustion_target01')],
        instruction='Run the proposed target command only after the separate root operational review; no automatic continuation.')
    (OUT / 'handoff.json').write_text(json.dumps(handoff, indent=2) + '\n')
    exports=[]
    for p in sorted(OUT.rglob('*')):
        if p.is_file():
            row=pin(p);row['path']=str(p.relative_to(OUT));exports.append(row)
    (OUT / 'manifest.json').write_text(json.dumps(dict(status=handoff['status'], exports=exports), indent=2) + '\n')
    print(json.dumps(pin(OUT / 'manifest.json')))
if __name__ == '__main__':
    main()
