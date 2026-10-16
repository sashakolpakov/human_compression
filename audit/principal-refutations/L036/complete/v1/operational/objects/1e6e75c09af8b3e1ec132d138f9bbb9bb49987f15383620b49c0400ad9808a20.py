"""Small ownership checks with disposable Python children, never GAP."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from types import SimpleNamespace
import contextlib
import hashlib
import importlib.util
import io
import json
import tempfile

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('mark_owner', HERE / 'run.py')
owner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owner)


def one(name, code, cap=1024, interrupt=False):
    with tempfile.TemporaryDirectory(prefix='L036-owner-', dir=HERE) as folder:
        root = Path(folder)
        fixture = root / 'fixture'
        fixture.write_text('original')
        req = dict(bindings=[dict(path=str(fixture), bytes=fixture.stat().st_size,
                   sha256=owner.sha(fixture))], command=[sys.executable, '-c', code],
                   deadline_seconds=3, output_cap_bytes=cap,
                   launch_reserve_bytes=4 * 2**30, emergency_floor_bytes=2 * 2**30)
        path = root / 'request.json'
        path.write_text(json.dumps(req))
        previous_here = owner.HERE
        previous_sleep = owner.time.sleep
        owner.HERE = root
        if interrupt:
            def fail_sleep(seconds):
                # Inject once; subprocess.wait also uses the shared time module.
                owner.time.sleep = previous_sleep
                raise KeyboardInterrupt('injected after Popen')
            owner.time.sleep = fail_sleep
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                owner.main(SimpleNamespace(expected_request=owner.sha(path), out=root / 'out', authorized_once=True))
        finally:
            owner.HERE = previous_here
            owner.time.sleep = previous_sleep
        result = json.loads((root / 'out/receipt.json').read_text())
        owner.need(result['target_launched'] and result['child_reaped'], 'owned child reaped')
        owner.need(result['final_bindings_checked'] == 1, 'final binding pass executed')
        if name == 'supervision_interrupt':
            owner.need(result['reason'] == 'supervision_failure' and result['returncode'] < 0,
                       'interrupt preserved and live child terminated')
        elif name == 'changed_input':
            owner.need(result['reason'] == 'final_input_mismatch' and len(result['final_binding_failures']) == 1,
                       'post-return input change rejected')
        elif name == 'completed_output_limit':
            owner.need('output_cap' in result['final_boundary_failures'], 'final output boundary rejected')
        else:
            owner.need(result['reason'] == 'completed' and result['returncode'] == 0 and
                       not result['final_boundary_failures'] and not result['final_binding_failures'],
                       'ordinary terminal receipt')
        return dict(name=name, reason=result['reason'], returncode=result['returncode'],
                    child_reaped=result['child_reaped'], final_boundary_failures=result['final_boundary_failures'],
                    changed_bindings=len(result['final_binding_failures']))


def main():
    results = [one('ordinary_completion', 'print("done")'),
               one('supervision_interrupt', 'import time; time.sleep(30)', interrupt=True),
               one('changed_input', 'from pathlib import Path; Path("fixture").write_text("changed")'),
               one('completed_output_limit', 'print("x"*8192)', cap=1024)]
    print(json.dumps(dict(status='PASS_L036_MARK_OWNER_CONTROLS', cases=results, GAP_launched=False)))


if __name__ == '__main__':
    main()
