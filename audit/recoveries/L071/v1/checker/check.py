"""Restore the L071 public evidence and audit its completed finite receipts.

This repeats neither the censuses nor the mathematical peer review. Primary
source reading and native-page review are retained attestations, explicitly
separate from the public execution checks run here.
"""
from pathlib import Path, PurePosixPath
import argparse
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import sys

BASE = 'audit/recoveries/L071/v1'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def safe(name):
    p = PurePosixPath(name)
    need(name and not p.is_absolute() and '..' not in p.parts,
         'unsafe relative path: ' + name)
    return p


def child(root, name):
    p = (root / safe(name)).resolve()
    need(p.is_relative_to(root.resolve()), 'path escapes declared root')
    return p


def main(a):
    need(__debug__, 'run without Python optimization; assertions are required')
    need(not a.out.exists(), 'fresh output directory required')
    repo = a.repo.resolve()
    payload = a.payload.resolve() if a.payload else repo
    transport_path = child(payload, BASE + '/transport.json')
    transport = json.loads(transport_path.read_text())
    need(sha(transport_path) == EXPECTED_TRANSPORT, 'frozen transport changed')
    need(transport['logical_files'] == 1057 and len(transport['packets']) == 21,
         'complete acquisition inventory')
    a.out.mkdir(parents=True)
    tree = a.out.resolve() / 'restored'
    (tree / 'study').mkdir(parents=True)
    (tree / 'repo').mkdir()
    cache = a.out.resolve() / 'payloads'
    cache.mkdir()
    seen = set()
    decoded = {}
    documentary = []
    for row in transport['files']:
        key = (row['origin'], row['path'])
        need(key not in seen, 'duplicate logical identity')
        seen.add(key)
        if row['transport'].endswith('HASH_ONLY'):
            documentary.append(row)
            continue
        need(row['origin'] in ('study', 'repo'), 'unexpected evidence origin')
        identity = (row['bytes'], row['sha256'])
        if identity not in decoded:
            root = repo if row['transport'] == 'EXISTING_PUBLIC' else payload
            src = child(root, row['public_path'])
            need(src.stat().st_size == row['stored_bytes'] and
                 sha(src) == row['stored_sha256'], 'stored payload changed')
            target = cache / row['sha256']
            need(row['encoding'] in ('identity', 'gzip'), 'unsupported encoding')
            opener = gzip.open if row['encoding'] == 'gzip' else open
            with opener(src, 'rb') as inf, target.open('wb') as outf:
                shutil.copyfileobj(inf, outf)
            need(target.stat().st_size == row['bytes'] and sha(target) == row['sha256'],
                 'decoded evidence changed')
            decoded[identity] = target
        dest = child(tree / row['origin'], row['path'])
        dest.parent.mkdir(parents=True, exist_ok=True)
        # Restored files are disposable copies, never links to repository files.
        os.link(decoded[identity], dest)
    need({r['path'] for r in documentary} == {
        'sources/catalogue_L071.pdf', 'sources/catalogue_L071.txt',
        '/opt/homebrew/Cellar/gap/4.15.1/share/gap/doc/ref/chap79.txt'},
        'only the declared primary and documentary inputs may be omitted')
    # Check every acquired manifest export, not only a collection of loose hashes.
    export_count = 0
    for packet in transport['packets']:
        p = child(tree / packet['origin'], packet['path'])
        need(sha(p) == packet['sha256'], 'acquired manifest changed')
        m = json.loads(p.read_text())
        need(len(m['exports']) == packet['exports'], 'complete manifest exports')
        for row in m['exports']:
            q = child(p.parent, row['path'])
            need(q.is_file() and q.stat().st_size == row['bytes'] and
                 sha(q) == row['sha256'], 'acquired export missing or changed')
            export_count += 1
    checks = Path(__file__).resolve().parent
    env = os.environ.copy()
    env.pop('PYTHONOPTIMIZE', None)
    env.update(L071_RESTORED_STUDY=str(tree / 'study'),
               L071_TRANSPORT=str(transport_path), PYTHONDONTWRITEBYTECODE='1')
    completed = []
    for name in ('alternating', 'co3', 'remaining', 'source_comparison'):
        out = a.out.resolve() / name
        if name != 'source_comparison':
            out.mkdir()
        env['L071_CHECK_OUTPUT'] = str(out)
        command = [sys.executable, '-B', str(checks / (name + '.py'))]
        if name == 'source_comparison':
            command += ['--run', str(tree / 'study/reboot_20261013/L071_source_comparison01'),
                        '--out', str(out)]
        with (a.out / (name + '.stdout')).open('wb') as stdout, \
             (a.out / (name + '.stderr')).open('wb') as stderr:
            result = subprocess.run(command, env=env, cwd=tree,
                                    stdout=stdout, stderr=stderr)
        need(result.returncode == 0, 'portable check failed: ' + name)
        need((a.out / (name + '.stderr')).stat().st_size == 0,
             'unexpected portable diagnostic: ' + name)
        completed.append(name)
    # The checker files themselves are explicitly inventoried in the report.
    code = [dict(path=p.name, bytes=p.stat().st_size, sha256=sha(p))
            for p in sorted(checks.glob('*.py'))]
    report = dict(status='PASS_PUBLIC_RESTORATION_AND_COMPLETED_RECEIPT_CHECKS',
        transport_sha256=sha(transport_path), logical_records=len(seen),
        restored_files=len(seen)-len(documentary), distinct_payloads=len(decoded),
        acquired_packets=len(transport['packets']), acquired_exports=export_count,
        documentary_metadata_only=documentary, checks=completed, programs=code,
        private_proof_fallback=False, source_content_reread=False,
        new_native_page_review=False, long_censuses_repeated=False,
        mathematical_review_replaced_by_hashes=False,
        alternating_markings=12904, conway_markings=22908,
        other_model_markings=6868, original_archive_markings=6047,
        original_warning_receipts_unchanged=True,
        whole_original_credit=0)
    (a.out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k:v for k,v in report.items()
                      if k not in ('programs', 'documentary_metadata_only')}))


EXPECTED_TRANSPORT = '460ef417002d7ebbbbc536a889b8d1a6924dc6740b0c774072064e716d549c3a'

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--payload', type=Path,
                   help='Private staging root before publication; omit after publication')
    p.add_argument('--out', type=Path, required=True)
    main(p.parse_args())
