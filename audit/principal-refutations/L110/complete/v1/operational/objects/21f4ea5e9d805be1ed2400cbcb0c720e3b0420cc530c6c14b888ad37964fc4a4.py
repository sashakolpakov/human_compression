"""One reviewed library export; retain the child and terminal evidence on failure."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode = True
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import signal
import subprocess
import time

HERE = Path(__file__).resolve().parent


class OwnerInterrupted(Exception):
    pass


def interrupted(signum, frame):
    raise OwnerInterrupted('signal ' + str(signum))


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(2**20), b''):
            h.update(block)
    return h.hexdigest()


def rehash(bindings):
    failures = []
    for row in bindings:
        path = Path(row['path'])
        try:
            if not path.is_file() or path.stat().st_size != row['bytes'] or sha(path) != row['sha256']:
                failures.append(dict(path=str(path), reason='changed or missing exact input'))
        except Exception as exc:
            failures.append(dict(path=str(path), reason=type(exc).__name__ + ': ' + str(exc)))
    return failures


def stop_owned(child):
    """The child owns its process group; terminate it and reap the direct child."""
    if child.poll() is None:
        try:
            os.killpg(child.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            child.wait(timeout=2)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(child.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            child.wait()
    else:
        child.wait()


def limits(req, elapsed, output_bytes, free_bytes):
    return [name for name, failed in [
        ('deadline', elapsed > req['deadline_seconds']),
        ('output_cap', output_bytes > req['output_cap_bytes']),
        ('disk_floor', free_bytes < req['emergency_floor_bytes'])] if failed]


def main(args):
    request_path = HERE / 'request.json'
    need(sha(request_path) == args.expected_request, 'Exact reviewed request')
    req = json.loads(request_path.read_text())
    need(not rehash(req['bindings']), 'Exact request bindings before launch')
    need(args.out.is_absolute() and not args.out.exists(), 'Fresh absolute output')
    need(args.authorized_once, 'Explicit root authorization required')
    free = shutil.disk_usage(args.out.parent).free
    if free < req['launch_reserve_bytes'] + req['output_cap_bytes']:
        print(json.dumps(dict(status='HOLD_L036_MARK_EXPORT_DISK_RESERVE',
                              free_bytes=free, target_launched=False)))
        return
    args.out.mkdir()
    paths = [args.out / 'stdout', args.out / 'stderr']
    started = time.monotonic()
    child = None
    reason = 'completed'
    supervision_error = None
    previous_handlers = {s: signal.getsignal(s) for s in [signal.SIGINT, signal.SIGTERM]}
    try:
        for sig in previous_handlers:
            signal.signal(sig, interrupted)
        with paths[0].open('wb') as out, paths[1].open('wb') as err:
            child = subprocess.Popen(req['command'], cwd=HERE, stdout=out,
                                     stderr=err, start_new_session=True)
            while child.poll() is None:
                failures = limits(req, time.monotonic() - started,
                                  sum(p.stat().st_size for p in paths),
                                  shutil.disk_usage(args.out).free)
                if failures:
                    reason = failures[0]
                    break
                time.sleep(0.1)
    except BaseException as exc:
        reason = 'supervision_failure'
        supervision_error = type(exc).__name__ + ': ' + str(exc)
    finally:
        # Includes KeyboardInterrupt and exceptions from polling/filesystem I/O.
        # No terminal path leaves a live owned direct child.
        # A second ordinary interrupt must not interrupt kill-and-wait cleanup.
        for sig in previous_handlers:
            signal.signal(sig, signal.SIG_IGN)
        if child is not None:
            stop_owned(child)
    elapsed = time.monotonic() - started
    free = shutil.disk_usage(args.out).free
    outputs = [dict(path=p.name, bytes=p.stat().st_size, sha256=sha(p))
               for p in paths if p.is_file()]
    boundary_failures = limits(req, elapsed, sum(p['bytes'] for p in outputs), free)
    binding_failures = rehash(req['bindings'])
    try:
        request_unchanged = sha(request_path) == args.expected_request
    except Exception as exc:
        request_unchanged = False
        binding_failures.append(dict(path=str(request_path), reason=type(exc).__name__ + ': ' + str(exc)))
    if reason == 'completed' and boundary_failures:
        reason = 'final_' + boundary_failures[0]
    if reason == 'completed' and (binding_failures or not request_unchanged):
        reason = 'final_input_mismatch'
    result = dict(status='L036_MARK_EXPORT_TERMINAL', reason=reason,
        returncode=child.returncode if child is not None else None,
        seconds=elapsed, request_sha256=args.expected_request,
        target_launched=child is not None, supervision_error=supervision_error,
        child_reaped=child is not None and child.poll() is not None,
        final_boundary_failures=boundary_failures, final_free_bytes=free,
        final_bindings_checked=len(req['bindings']), final_binding_failures=binding_failures,
        final_request_unchanged=request_unchanged, science_accepted=False, outputs=outputs)
    (args.out / 'receipt.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))
    for sig, previous in previous_handlers.items():
        signal.signal(sig, previous)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected-request', required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--authorized-once', action='store_true')
    main(parser.parse_args())
