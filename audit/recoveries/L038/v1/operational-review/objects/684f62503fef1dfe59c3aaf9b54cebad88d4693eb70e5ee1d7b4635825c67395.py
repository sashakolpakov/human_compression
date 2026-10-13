"""Restore L038 public evidence and verify its completed execution records.

Written mathematical review and source reading remain separate evidence.
This does not rerun the original censuses or assert whole-source formalization.
"""
from pathlib import Path, PurePosixPath
import argparse
import contextlib
import sys
import gzip
import hashlib
import importlib.util
import json
import os
import re
import shutil

BASE = 'audit/recoveries/L038/v1'
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
    expected_packets = {n+suffix+'/manifest.json' for n in [
        'corpus106_L038_low_rank','corpus106_L038_signed_ends','corpus106_L038_principal']
        for suffix in ['_v1','_independent_review','_root_adoption']}
    packet_names = {p['path'] for p in tr['packets']}
    need(expected_packets <= packet_names and len(packet_names) == len(tr['packets']),
         'all three complete reviewed components and no repeated packet')
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
    need(set(primary) == set(tr['primary_sources_hash_only']) and
         {'sources/alternating2019.pdf','sources/alternating2019.txt'} <= set(primary),
         'exact declared primary files')
    need(all(p.startswith('sources/') for p in primary), 'proof cannot be a primary omission')
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
    primary_pins = {r['path']:r for r in tr['files'] if r['path'] in primary}
    completed = []
    for stem, expected_pairs in [('low_rank',1600),('signed_ends',1280),('principal',320)]:
        p = study/('corpus106_L038_'+stem+'_v1')
        author = module('l038_'+stem+'_restored',p/'check.py')
        original_bind = author.bind
        def restored_bind(root,row,original=original_bind):
            target=(root/row['path']).resolve()
            need(target.is_relative_to(study), 'author binding escapes restored study')
            if root.resolve() == study and row['path'] in primary_pins:
                expected=primary_pins[row['path']]
                need(row['bytes']==expected['bytes'] and row['sha256']==expected['sha256'],
                     'documentary source pin changed')
                return
            original(root,row)
        author.bind=restored_bind
        previous_argv=sys.argv
        sys.argv=[str(p/'check.py'),'--study-root',str(study),
                  '--out',str(a.out.resolve()/stem),'--gap',a.gap]
        try:
            with (a.out/(stem+'.stdout')).open('w') as stdout:
                with contextlib.redirect_stdout(stdout):
                    author.main()
        finally:
            sys.argv=previous_argv
        result=json.loads((a.out/stem/'report.json').read_text())
        need(result['status']=='PASS', 'component finite replay')
        field='A12_subset_pairs' if stem=='principal' else 'finite_subset_pairs'
        need(result[field]==expected_pairs, 'complete finite premises')
        if stem=='principal':
            need(result['exact_retained_record_selection'] is True, 'two exact existing records')
        completed.append(dict(component=stem,subset_pairs=expected_pairs,report=result))
    report = dict(status='PASS_PUBLIC_L038_RESTORATION_AND_FINITE_PREMISES',
                  transport_sha256=sha(transport_path),logical_records=len(seen),
                  restored_files=len(seen)-len(primary),distinct_payloads=len(decoded),
                  acquired_packets=len(tr['packets']),acquired_exports=exports,
                  documentary_primary_only=primary,checks=completed,subset_pairs=3200,
                  private_proof_fallback=False,long_censuses_repeated=False,
                  source_content_reread=False,new_native_page_review=False,
                  mathematical_review_replaced_by_hashes=False,whole_original_credit=0)
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k != 'checks'}))


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--repo',type=Path,required=True);p.add_argument('--payload',type=Path)
    p.add_argument('--gap',default='gap')
    p.add_argument('--expected-transport',required=True);p.add_argument('--out',type=Path,required=True)
    main(p.parse_args())
