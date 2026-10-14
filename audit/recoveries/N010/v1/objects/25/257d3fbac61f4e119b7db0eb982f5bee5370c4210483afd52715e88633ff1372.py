"""Replay exact review inputs and source inventory, not mathematical proofs."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Normal Python is required before filesystem work')
sys.dont_write_bytecode = True
import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--study', type=Path, required=True)
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    packet = Path(__file__).resolve().parent
    out = a.out.resolve()
    need(not out.exists() and not out.is_relative_to(packet), 'Fresh external output required')
    roots = dict(study=a.study.resolve(), public=a.repo.resolve(), packet=packet)

    def verify(row):
        root = roots[row['namespace']]
        p = (root/row['path']).resolve()
        need(p.is_relative_to(root) and p.is_file(), 'Safe pinned file')
        raw = p.read_bytes()
        need((len(raw),hashlib.sha256(raw).hexdigest()) == (row['bytes'],row['sha256']),
             'Changed pinned bytes: '+row['path'])
        return p

    manifest = json.loads((packet/'manifest.json').read_text())
    for row in manifest['exports']:
        verify(dict(namespace='packet',**row))
    dependencies = json.loads((packet/'dependencies.json').read_text())
    for row in dependencies:
        verify(row)
    review = json.loads((packet/'review.json').read_text())
    need(review['status'] == 'ACCEPTED_N010_COMPLETE_SURVEY_DISPOSITION', 'Exact review status')
    need(review['whole_original_credit'] == review['new_question_credit'] == review['new_measurements']
         == review['new_Lean_declarations'] == 0, 'No automatic credit')
    author = verify(review['author_manifest']).parent
    out.mkdir(parents=True)
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE',None)
    cmd = [sys.executable,str(packet/'source_inventory.py'),'--study',str(roots['study']),
           '--packet',str(author),'--out',str(out/'source_inventory.json')]
    p = subprocess.run(cmd,env=env,capture_output=True,timeout=30)
    (out/'source_inventory.stdout').write_bytes(p.stdout)
    (out/'source_inventory.stderr').write_bytes(p.stderr)
    need(p.returncode == 0 and not p.stderr, 'Fresh independent source inventory')
    fresh = json.loads((out/'source_inventory.json').read_text())
    old = json.loads((packet/'source_inventory.json').read_text())
    need(fresh['counts'] == old['counts'] and fresh['damaged_controls'] == old['damaged_controls'],
         'Exact inventory and controls reproduced')
    guards = []
    for kind in ['argument','environment']:
        e = env.copy()
        cmd = [sys.executable]
        if kind == 'argument':
            cmd.append('-O')
        else:
            e['PYTHONOPTIMIZE'] = '1'
        target = out/('rejected_'+kind)
        p = subprocess.run(cmd+[str(packet/'check.py'),'--out',str(target)],env=e,capture_output=True,timeout=15)
        (out/('guard_'+kind+'.stderr')).write_bytes(p.stderr)
        need(p.returncode != 0 and b'Normal Python is required' in p.stderr and not target.exists(),
             'Pre-output optimization guard')
        guards.append(kind)
    report = dict(status='PASS_N010_DISTINCT_REVIEW_REPLAY',exports=len(manifest['exports']),
                  dependencies=len(dependencies),source_clauses=fresh['counts']['synthesis_clauses'],
                  source_inventory=True,damaged_source_controls=len(fresh['damaged_controls']),
                  optimization_guards=guards,mathematical_proof_checked_by_this_program=False,
                  acquired_censuses_repeated=False,whole_original_credit=0)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
