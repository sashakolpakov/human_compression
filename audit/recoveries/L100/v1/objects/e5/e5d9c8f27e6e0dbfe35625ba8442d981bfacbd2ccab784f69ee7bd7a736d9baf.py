"""One fixed broad L100 traversal; exact inputs, bounded process, returned-prefix audit."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time

if not __debug__:
    raise SystemExit('optimized execution forbidden')
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
S = HERE.parents[2]
G34 = S / 'geometry/psl3_4'
P = G34 / 'exhaustion_component_v2'
REVIEW = G34 / 'exhaustion_review_v2'
ADOPTION = G34 / 'exhaustion_adoption_v2'
AUTHOR_SHA = '01ab26a1194efdcbc980e358eb4da425d13eb5d30f5602b86827d27214d914ca'
REVIEW_SHA = '5ffd79c6177a1550a10c57edde2abae61769a024775180b176afa2c7b69d47e9'
ADOPTION_SHA = '1117e60a09345ab4060613c791b6e07c95f0581cf525486eed052c47c80a7c2d'
GAP = Path('/opt/homebrew/bin/gap')
LIBGAP = Path('/opt/homebrew/Cellar/gap/4.15.1/lib/libgap.10.dylib')
IDS = list(range(11, 0, -1))
TARGET_CAP = 180
AUDIT_CAP = 20
FINAL = 'L100_REQUESTED_ANCHORS_COMPLETE'


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def pin(path):
    p = Path(path).absolute()
    b = p.read_bytes()
    return dict(path=str(p), resolved=str(p.resolve()), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())


def save(path, data):
    p = Path(path)
    tmp = p.with_name(p.name + '.tmp')
    tmp.write_text(json.dumps(data, indent=2) + '\n')
    os.replace(tmp, p)


def resolve_row(row, study=S):
    p = Path(row['path'])
    ns = row.get('namespace')
    require(ns in (None, 'study', 'runtime'), 'unknown dependency namespace')
    require('..' not in p.parts, 'parent path component forbidden')
    if not p.is_absolute():
        require(ns == 'study', 'relative input must name study namespace')
        p = study / p
    if ns == 'study':
        require(p.resolve().is_relative_to(study.resolve()), 'study path escapes study')
    return p


def verify(row, study=S):
    p = resolve_row(row, study)
    actual = pin(p)
    require(actual['bytes'] == row['bytes'] and actual['sha256'] == row['sha256'], 'changed input: ' + str(p))
    if 'resolved' in row:
        require(actual['resolved'] == row['resolved'], 'changed symlink resolution: ' + str(p))
    return actual


def manifest_gate(folder, sha, status):
    mp = folder / 'manifest.json'
    require(pin(mp)['sha256'] == sha, 'manifest identity: ' + str(folder))
    m = json.loads(mp.read_text())
    require(m['status'] == status, 'manifest status: ' + str(folder))
    rows = [pin(mp)]
    names = []
    for e in m['exports']:
        q = Path(e['path'])
        require(not q.is_absolute() and '..' not in q.parts, 'unsafe export path')
        names.append(str(q))
        rows.append(verify(dict(e, path=str(folder / q))))
    require(len(set(names)) == len(names), 'duplicate manifest export')
    require('dependencies.json' in names, 'missing bound dependencies')
    for e in json.loads((folder / 'dependencies.json').read_text()):
        rows.append(verify(e))
    return rows


def preflight():
    rows = manifest_gate(P, AUTHOR_SHA, 'AUTHOR_COMPLETE_L100_BROAD_PRIMITIVE_PREPARATION_V2_AWAITING_DISTINCT_REVIEW')
    rows += manifest_gate(REVIEW, REVIEW_SHA, 'ACCEPTED_L100_BROAD_PRIMITIVE_PREPARATION_V2')
    r = json.loads((REVIEW / 'review.json').read_text())
    require(r['status'] == 'ACCEPTED_L100_BROAD_PRIMITIVE_PREPARATION_V2', 'review status')
    require(resolve_row(r['author_manifest']) == P / 'manifest.json' and r['author_manifest']['sha256'] == AUTHOR_SHA,
            'review does not bind exact author')
    rows += manifest_gate(ADOPTION, ADOPTION_SHA, 'ROOT_ADOPTED_L100_BROAD_PRIMITIVE_PREPARATION_V2')
    a = json.loads((ADOPTION / 'review.json').read_text())
    require(resolve_row(a['review_manifest']) == REVIEW / 'manifest.json' and a['review_manifest']['sha256'] == REVIEW_SHA,
            'adoption does not bind exact review')
    rows += [pin(p) for p in [Path(__file__), HERE / 'audit_returned.g', GAP, LIBGAP, Path(sys.executable)]]
    from previous_boundary import bind_previous
    rows += bind_previous(manifest_gate, verify, pin)
    rows.append(pin(HERE / 'previous_boundary.py'))
    return unique_pins(rows)


def unique_pins(rows):
    result = {}
    for r in rows:
        if r['path'] in result:
            require(result[r['path']] == r, 'conflicting input pins')
        result[r['path']] = r
    return list(result.values())


def unchanged(rows):
    try:
        for row in rows:
            verify(row)
        return True
    except (ValueError, OSError):
        return False


def phase(command, folder, cap, target):
    """Record before launch; kill and wait for this process group on deadline/interruption."""
    folder.mkdir()
    start = time.monotonic()
    r = dict(status='ACTIVE', command=command, cap_seconds=cap, target_census=target,
             owner_pid=os.getpid(), started_unix=time.time(), returncode=None)
    save(folder / 'receipt.json', r)
    proc = None
    with (folder / 'stdout').open('wb') as so, (folder / 'stderr').open('wb') as se:
        try:
            proc = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=so, stderr=se, start_new_session=True)
            r['child_pid'] = proc.pid
            save(folder / 'receipt.json', r)
            r['returncode'] = proc.wait(timeout=cap)
            r['status'] = 'RETURNED'
        except (subprocess.TimeoutExpired, KeyboardInterrupt) as exc:
            if proc is not None:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                r['returncode'] = proc.wait()
            r['status'] = 'DEADLINE' if isinstance(exc, subprocess.TimeoutExpired) else 'INTERRUPTED'
        except OSError as exc:
            r.update(status='LAUNCH_FAILED', error=str(exc))
    r['elapsed_seconds'] = time.monotonic() - start
    r['outputs'] = [pin(folder / n) for n in ('stdout', 'stderr')]
    save(folder / 'receipt.json', r)
    return r


def clean_phase(r, folder):
    return r['status'] == 'RETURNED' and r['returncode'] == 0 and not (folder / 'stderr').read_bytes()


def completed_rows(stdout, requested):
    rows = []
    for line in stdout.splitlines():
        if line.startswith('BOREL_COMPLETE'):
            m = re.fullmatch(r'BOREL_COMPLETE id=(\d+) rank_counts=(\[[\d, ]*\]) full_group(?:_ranks)?=(\[[\d, ]*\])', line)
            require(m is not None, 'malformed completion line')
            bid, levels, ranks = int(m[1]), json.loads(m[2]), json.loads(m[3])
            rows.append([bid, levels, ranks])
    ids = [r[0] for r in rows]
    require(ids == requested[:len(ids)], 'returned anchors are not the unique requested prefix')
    require(stdout.splitlines().count(FINAL) <= 1, 'duplicate final marker')
    if FINAL in stdout.splitlines():
        require(ids == requested, 'premature final marker')
    return rows


def classify(execution, stderr, stdout, rows, requested, audited, inputs_same):
    if not inputs_same:
        return 'INVALIDATED_INPUT_CHANGE'
    if not audited:
        return 'FAILED_RETURNED_ANCHOR_AUDIT'
    if stderr or re.search(r'(?m)^(?:Error|Syntax warning|Syntax error)', stdout):
        return 'FAILED_EXECUTION'
    if execution['status'] == 'DEADLINE':
        return 'PARTIAL_DEADLINE'
    if execution['status'] != 'RETURNED' or execution['returncode'] != 0:
        return 'FAILED_EXECUTION'
    if [r[0] for r in rows] == requested and stdout.splitlines().count(FINAL) == 1:
        return 'COMPLETE_REQUEST'
    return 'INCOMPLETE_RETURN'


def checkpoint_files(folder, rows):
    files = []
    for bid, levels, ranks in rows:
        require(all(type(x) is int and x >= 0 for x in levels + ranks), 'invalid numeric output')
        require(len(levels) <= 11, 'rank inventory exceeds fixed L100 bound')
        files.append(folder / f'b{bid}_done.g')
        for rank in range(2, len(levels) + 1):
            files.append(folder / f'b{bid}_r{rank}.g')
    return [pin(p) for p in files]


def audit_driver(folder, checkpoint_dir, rows, setup):
    """setup loads only the fixed model, never the search functions."""
    q = lambda x: json.dumps(str(x))
    s = ['SizeScreen([100000,24]);;', setup,
         'AUDIT_DIR:=' + q(checkpoint_dir) + ';;', 'AUDIT_ROWS:=' + json.dumps(rows) + ';;',
         'Read(' + q(HERE / 'audit_returned.g') + ');;', 'QUIT_GAP(0);']
    p = folder / 'audit_driver.g'
    p.write_text('\n'.join(s) + '\n')
    return p


def validate_preparation(prepared):
    req = json.loads((prepared / 'request.json').read_text())
    require(req['borels'] == IDS and req['require_2T'] is False and req['proposed_external_cap_seconds'] == 60,
            'changed target request')
    require(req['status'] == 'PREPARED_NOT_EXECUTED_NO_CENSUS_CREDIT', 'preparation status')
    require(req['output'] == str(prepared / 'checkpoints'), 'checkpoint output mismatch')
    expected = [P / 'input_catalogue01.g', S / 'phase7_sporadic_search.g', P / 'legacy_functions.g',
                P / 'catalogue_loader_v2.g', P / 'prepare_driver_v2.py']
    require([resolve_row(r) for r in req['inputs']] == expected, 'changed preparation input list')
    rows = [verify(r) for r in req['inputs']] + [verify(req['driver'])]
    require(resolve_row(req['driver']) == prepared / 'driver.g', 'driver path')
    driver = (prepared / 'driver.g').read_text()
    # The exact pinned preparer supplies the full bytes; inspect the actual scientific Read boundary too.
    require(re.findall(r'Read\(("[^"\n]+")\)', driver) ==
            [json.dumps(str(P / 'catalogue_loader_v2.g')), json.dumps(str(P / 'legacy_functions.g'))], 'actual Read list')
    require(driver.count('for bid in BOREL_IDS do RunBorel(bid);od;') == 1, 'target call changed')
    return rows + [pin(prepared / 'request.json')]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--prepare-only', action='store_true')
    args = ap.parse_args()
    require(args.out.is_absolute() and '..' not in args.out.parts, 'absolute output required')
    out = args.out
    require(not out.exists(), 'output already exists')
    inputs = preflight()  # All scientific gates fail before any output creation.
    out.mkdir(parents=True)
    receipt = dict(status='PREPARING', target_census=False, requested_anchors=IDS,
                   target_cap_seconds=TARGET_CAP, audit_cap_seconds=AUDIT_CAP,
                   preparer_proposed_cap_seconds=60,
                   previous_receipt=pin(G34 / 'exhaustion_target01/receipt.json'),
                   previously_completed_anchors=list(range(95, 11, -1)),
                   unfinished_anchor_restart=11,
                   completed_anchors=[], unpaid_anchors=IDS, whole_original_credit=0,
                   equivalence='inner conjugacy and type permutations only', inputs=inputs)
    save(out / 'receipt.json', receipt)
    try:
        prep = phase([sys.executable, str(P / 'prepare_driver_v2.py'), '--out', str(out / 'prepared'), '--borels', ','.join(map(str, IDS))], out / 'prepare', 15, False)
        require(clean_phase(prep, out / 'prepare'), 'preparation failed')
        inputs = unique_pins(inputs + validate_preparation(out / 'prepared'))
        receipt['inputs'] = inputs
        require(unchanged(inputs), 'input changed before execution')
        if args.prepare_only:
            receipt['status'] = 'PREPARED_ONLY_NO_TARGET'
        else:
            receipt.update(status='ACTIVE_TARGET', target_census=True)
            save(out / 'receipt.json', receipt)
            execution = phase([str(GAP), '-q', '-b', str(out / 'prepared/driver.g')], out / 'target', TARGET_CAP, True)
            receipt['execution'] = execution
            stdout = (out / 'target/stdout').read_text()
            stderr = (out / 'target/stderr').read_text()
            rows = completed_rows(stdout, IDS)
            receipt['reported_completed_rows'] = rows
            returned_pins = checkpoint_files(out / 'prepared/checkpoints', rows)
            inputs = unique_pins(inputs + returned_pins)
            receipt['inputs'] = inputs
            setup = 'INPUT_CATALOGUE:=' + json.dumps(str(P / 'input_catalogue01.g')) + ';;\nRead(' + json.dumps(str(P / 'catalogue_loader_v2.g')) + ');;'
            driver = audit_driver(out, out / 'prepared/checkpoints', rows, setup)
            inputs += [pin(driver)]
            require(unchanged(inputs), 'input changed before returned audit')
            audit = phase([str(GAP), '-q', '-b', str(driver)], out / 'audit', AUDIT_CAP, False)
            receipt['audit'] = audit
            atext = (out / 'audit/stdout').read_text()
            audited = clean_phase(audit, out / 'audit') and atext.splitlines().count('PASS_RETURNED_ANCHOR_AUDIT') == 1
            actual_rows = [json.loads(x[len('AUDITED '):]) for x in atext.splitlines() if x.startswith('AUDITED ')]
            audited = audited and actual_rows == rows
            same = unchanged(inputs)
            receipt['status'] = classify(execution, stderr, stdout, rows, IDS, audited, same)
            receipt['audited_returned_rows'] = actual_rows
            # Only a clean execution or a clean external deadline may expose verified anchor credit.
            if receipt['status'] in ('COMPLETE_REQUEST', 'PARTIAL_DEADLINE', 'INCOMPLETE_RETURN'):
                receipt['completed_anchors'] = [r[0] for r in rows]
                receipt['unpaid_anchors'] = IDS[len(rows):]
    except (Exception, KeyboardInterrupt) as exc:
        receipt.update(status='FAILED_INTERFACE', error=type(exc).__name__ + ': ' + str(exc))
    receipt['inputs'] = inputs
    if not unchanged(inputs):
        receipt.update(status='INVALIDATED_INPUT_CHANGE', completed_anchors=[], unpaid_anchors=IDS)
    receipt['outputs'] = [pin(p) for p in sorted(out.rglob('*')) if p.is_file() and p != out / 'receipt.json']
    receipt['finished_unix'] = time.time()
    save(out / 'receipt.json', receipt)
    print(json.dumps({k: receipt[k] for k in ('status', 'target_census', 'completed_anchors', 'unpaid_anchors')}))
    return 0 if receipt['status'] in ('PREPARED_ONLY_NO_TARGET', 'COMPLETE_REQUEST', 'PARTIAL_DEADLINE') else 1


if __name__ == '__main__':
    raise SystemExit(main())
