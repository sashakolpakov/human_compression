"""Restore F006 public evidence and verify its completed execution records.

Written mathematical review and source reading remain separate evidence.
This does not rerun the five censuses or assert whole-source formalization.
"""
from pathlib import Path, PurePosixPath
import argparse
import gzip
import hashlib
import importlib.util
import json
import os
import re
import shutil

BASE = 'audit/recoveries/F006/v1'
HISTORICAL = Path('/Users/sasha/medusa/research/leemans')


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def child(root, name):
    p = PurePosixPath(name)
    need(name and not p.is_absolute() and '..' not in p.parts, 'unsafe logical path')
    result = (root/p).resolve()
    need(result.is_relative_to(root.resolve()), 'path escapes declared root')
    return result


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def main(a):
    need(__debug__, 'optimized Python is not supported')
    need(not a.out.exists(), 'fresh output directory required')
    repo = a.repo.resolve()
    payload = a.payload.resolve() if a.payload else repo
    transport_path = child(payload, BASE+'/transport.json')
    need(sha(transport_path) == a.expected_transport, 'frozen transport changed')
    tr = json.loads(transport_path.read_text())
    need(tr['logical_files'] == len(tr['files']), 'complete transport inventory')
    expected_packets = {n+'/manifest.json' for n in [
        'corpus106_F006_complete_v1','corpus106_F006_complete_independent_review',
        'corpus106_F006_complete_root_adoption','corpus106_F006_Dn_v2',
        'corpus106_F006_Dn_independent_review','corpus106_F006_small_coxeter_v1',
        'corpus106_F006_small_coxeter_independent_review',
        'corpus106_F006_validation_warning_assessment_v1']}
    need({p['path'] for p in tr['packets']} == expected_packets and
         len(tr['packets']) == len(expected_packets), 'complete accepted editions')
    a.out.mkdir(parents=True)
    study = a.out.resolve()/'restored/study'
    cache = a.out.resolve()/'payloads'
    study.mkdir(parents=True);cache.mkdir()
    seen, decoded, primary = set(), {}, []
    for row in tr['files']:
        need(row['origin'] == 'study', 'unexpected evidence namespace')
        key = row['path']
        need(key not in seen, 'duplicate logical evidence')
        seen.add(key)
        dest = child(study, key)
        if row['transport'].endswith('HASH_ONLY'):
            need(row['transport'] == 'PRIVATE_PRIMARY_SOURCE_HASH_ONLY',
                 'undeclared omitted evidence')
            primary.append(key)
            continue
        identity = (row['bytes'], row['sha256'])
        if identity not in decoded:
            need(row['transport'] in ['EXISTING_PUBLIC','NEW_FROZEN_FILE'],
                 'unknown transport kind')
            root = repo if row['transport'] == 'EXISTING_PUBLIC' else payload
            src = child(root, row['public_path'])
            need(src.stat().st_size == row['stored_bytes'] and
                 sha(src) == row['stored_sha256'], 'stored payload changed')
            need(row['encoding'] in ['identity','gzip'], 'unknown encoding')
            target = cache/row['sha256']
            opener = gzip.open if row['encoding'] == 'gzip' else open
            with opener(src,'rb') as inf, target.open('wb') as outf:
                shutil.copyfileobj(inf,outf)
            need(target.stat().st_size == row['bytes'] and sha(target) == row['sha256'],
                 'decoded evidence changed')
            decoded[identity] = target
        dest.parent.mkdir(parents=True,exist_ok=True)
        os.link(decoded[identity],dest)
    need(set(primary) == {'sources/coxeter_ranks2025.pdf','sources/coxeter_ranks2025.txt'},
         'only the two declared primary-source files may be omitted')
    exports = 0
    for packet in tr['packets']:
        p = child(study,packet['path'])
        need(sha(p) == packet['sha256'], 'manifest changed')
        m = json.loads(p.read_text())
        need(len(m['exports']) == packet['exports'], 'whole export inventory')
        for row in m['exports']:
            q = child(p.parent,row['path'])
            need(sha(q) == row['sha256'] and
                 ('bytes' not in row or q.stat().st_size == row['bytes']),
                 'missing or changed acquired export')
            exports += 1
    author = module('f006_author_restored',study/'corpus106_F006_complete_v1/check.py')
    result = author.verify(study/'corpus106_F006_complete_v1',study,True)
    need(result['status'] == 'PASS_COMPLETE_F006_RETAINED_EVIDENCE', 'author receipt checks')

    # Reuse the frozen assessor's pure mathematical record checks. Its sole
    # pin-reader replacement resolves historical names inside the restored
    # tree; neither the retained program nor its original receipts change.
    assessor = module('f006_warning_assessor_restored',
                      study/'corpus106_F006_validation_warning_assessment_v1/assess.py')
    def restored_pin(record):
        p = Path(record['path'])
        need(p.is_absolute() and p.is_relative_to(HISTORICAL), 'unknown historical pin')
        q = child(study,str(p.relative_to(HISTORICAL)))
        need(sha(q) == record['sha256'] and q.stat().st_size == record['bytes'],
             'changed restored execution pin')
    assessor.check_pin = restored_pin
    assessed, negative = [], []
    for name,(run_name,limit,total,pairs) in assessor.CASES.items():
        run = study/'reboot_20261013/F006_other_full_IP01'/name
        receipt = json.loads((run/'report.json').read_text())
        for p in receipt['pins']:
            restored_pin(p)
        raw = (study/'reboot_20261013'/run_name/'stdout.log').read_text()
        rows = [list(map(int,r)) for r in re.findall(author.PATTERN,raw)]
        values = (name,receipt,(run/'stderr.log').read_bytes(),
                  (run/'stdout.log').read_text(),(run/'validate.g').read_bytes(),rows)
        assessor.assess_values(*values)
        if name == 'F4':
            negative = assessor.controls(values)
        assessed.append(dict(name=name,tuples=total,subset_pairs=pairs))
    need(len(negative) == 13, 'all acquired warning controls')
    report = dict(status='PASS_PUBLIC_F006_RESTORATION_AND_RECEIPTS',
                  transport_sha256=sha(transport_path),logical_records=len(seen),
                  restored_files=len(seen)-len(primary),distinct_payloads=len(decoded),
                  acquired_packets=len(tr['packets']),acquired_exports=exports,
                  documentary_primary_only=primary,author_evidence=result,
                  fresh_warning_assessments=assessed,warning_controls=negative,
                  private_proof_fallback=False,long_censuses_repeated=False,
                  source_content_reread=False,new_native_page_review=False,
                  mathematical_review_replaced_by_hashes=False,
                  original_warning_receipts_unchanged=True,whole_original_credit=0)
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['author_evidence','warning_controls']}))


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--repo',type=Path,required=True);p.add_argument('--payload',type=Path)
    p.add_argument('--expected-transport',required=True);p.add_argument('--out',type=Path,required=True)
    main(p.parse_args())
