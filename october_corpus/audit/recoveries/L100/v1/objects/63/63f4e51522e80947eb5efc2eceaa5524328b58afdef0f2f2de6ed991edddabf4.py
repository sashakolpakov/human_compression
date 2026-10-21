"""Acquire the exact first partial run; its unfinished checkpoints are never read by GAP."""
import json
from pathlib import Path
if not __debug__:
    raise SystemExit('optimized execution forbidden')
G34 = Path(__file__).resolve().parent.parent
OLD_AUTHOR_SHA = 'f9c9220867406398e2fefa80c2946dd5a76d44469816a15defdb0ae18fde2163'
OLD_REVIEW_SHA = 'ec3321faba67fb77c7579bc23812177a1471f889bb5816f2b979a24cbbd9f96c'
RECEIPT_SHA = 'ba6a4d23edf478725737786fac96f7c7755ba456f0dc7e302ed9e00c2c86dc07'
ACCEPTANCE_SHA = 'bba090dadbf1fe330fdc3b1c8cf0ef034b85129d01c75607b9510b385db48928'
AUDIT_SHA = '05ef9b2b0846411fd228a2888a8ca94b05a16d7fe40c4444f6f9e69568550131'
PREFIX = list(range(95, 11, -1))
SUFFIX = list(range(11, 0, -1))


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def validate_boundary(r):
    require(r['status'] == 'PARTIAL_DEADLINE' and r['target_census'] is True, 'wrong prior terminal status')
    require(r['requested_anchors'] == PREFIX + SUFFIX, 'wrong original requested set')
    require(r['completed_anchors'] == PREFIX and r['unpaid_anchors'] == SUFFIX, 'wrong exact returned boundary')
    require(set(PREFIX).isdisjoint(SUFFIX), 'repeated completed anchor')
    require(r['execution']['status'] == 'DEADLINE' and r['execution']['returncode'] is not None, 'unclosed prior child')
    require(r['execution']['cap_seconds'] == 60 and r['target_cap_seconds'] == 60, 'prior cap changed')
    require(r['audit']['status'] == 'RETURNED' and r['audit']['returncode'] == 0, 'prior audit not clean')
    require(r['audited_returned_rows'] == r['reported_completed_rows'], 'prior rows disagree')
    require([x[0] for x in r['audited_returned_rows']] == PREFIX, 'prior audit is not completed prefix')


def bind_previous(manifest_gate, verify, pin):
    old = G34 / 'exhaustion_target_interface_v1'
    review = G34 / 'exhaustion_target_review_v1'
    rows = manifest_gate(old, OLD_AUTHOR_SHA, 'AUTHOR_COMPLETE_L100_BOUNDED_TARGET_INTERFACE_V1_AWAITING_ROOT_REVIEW')
    rows += manifest_gate(review, OLD_REVIEW_SHA, 'ACCEPTED_L100_BOUNDED_TARGET_INTERFACE_V1')
    v = json.loads((review / 'review.json').read_text())
    require(v['author_manifest']['path'] == str(old / 'manifest.json') and
            v['author_manifest']['sha256'] == OLD_AUTHOR_SHA, 'old review author binding')
    paths = [(G34 / 'exhaustion_target01/receipt.json', RECEIPT_SHA),
             (G34 / 'exhaustion_target01_acceptance_before.json', ACCEPTANCE_SHA),
             (G34 / 'exhaustion_target01_terminal_audit.json', AUDIT_SHA)]
    for path, sha in paths:
        actual = pin(path)
        require(actual['sha256'] == sha, 'prior evidence identity: ' + str(path))
        rows.append(actual)
    r = json.loads(paths[0][0].read_text())
    a = json.loads(paths[1][0].read_text())
    t = json.loads(paths[2][0].read_text())
    validate_boundary(r)
    require(a['command'] == v['authorized_next_run'], 'prior command not authorized exact command')
    require(t['receipt']['sha256'] == RECEIPT_SHA and t['completed_anchors'] == PREFIX and t['unpaid_anchors'] == SUFFIX,
            'terminal audit binding/boundary')
    for e in r['inputs'] + r['outputs'] + a['pins']:
        rows.append(verify(e))
    for name in ['target/stderr', 'audit/stderr']:
        require(not (G34 / 'exhaustion_target01' / name).read_bytes(), 'prior stderr nonempty')
    require(r['execution']['command'] == ['/opt/homebrew/bin/gap', '-q', '-b',
            str(G34 / 'exhaustion_target01/prepared/driver.g')], 'prior actual target command')
    return rows
