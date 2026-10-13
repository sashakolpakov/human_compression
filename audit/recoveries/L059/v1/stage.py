"""Stage exact portable L059 evidence privately, with lossless large logs."""
import sys
if sys.flags.optimize:
    raise RuntimeError("No optimization")
from pathlib import Path, PurePosixPath
import argparse
import gzip
import hashlib
import json
import shutil

S = Path(__file__).resolve().parents[2]
R = S.parents[1] / 'math_compression'
BASE = 'audit/recoveries/L059/v1'
PAPERS = 'papers/recoveries/L059/v1'
COMPONENTS = {}



def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def safe(name):
    p = PurePosixPath(name)
    need(not p.is_absolute() and '..' not in p.parts, 'unsafe logical path')
    return p


def main(a):
    need(not a.stage.exists(), 'fresh staging directory required')
    inv = json.loads(a.inventory.read_text())
    need(not inv['missing_final_reviews'], 'component reviews incomplete')
    rows = inv['files']
    by_hash = {}
    routes = []
    a.stage.mkdir(parents=True)
    # Exact existing public copies take precedence over any duplicate payload.
    for row in rows:
        if row['transport'] != 'EXISTING_PUBLIC':
            continue
        src = R / safe(row['public_path'])
        need(src.stat().st_size == row['stored_bytes'] and sha(src) == row['stored_sha256'],
             'changed public file')
        by_hash.setdefault((row['bytes'], row['sha256']),
                           dict(public_path=row['public_path'], encoding=row['encoding'],
                                transport='EXISTING_PUBLIC', stored_bytes=row['stored_bytes'],
                                stored_sha256=row['stored_sha256']))
    for row in rows:
        route = dict(row)
        if row['transport'].endswith('HASH_ONLY'):
            routes.append(route)
            continue
        key = (row['bytes'], row['sha256'])
        if key in by_hash:
            route.update(by_hash[key])
            routes.append(route)
            continue
        src = (S if row['origin'] == 'study' else R) / safe(row.get('source_path', row['path']))
        need(src.stat().st_size == row['bytes'] and sha(src) == row['sha256'],
             'changed frozen input ' + row['path'])
        parts = PurePosixPath(row['path']).parts
        suffix = row.get("public_suffix_override", src.suffix)
        if row['origin'] == 'study' and 'L059' in parts[0] and suffix in ['.tex', '.pdf'] and len(parts)==2:
            label='principal' if parts[0]=='corpus106_L059_principal_v2' else parts[0]
            dest=PAPERS+'/'+label+'/'+src.name
        else:
            ending = suffix if suffix and len(suffix) <= 8 else '.dat'
            dest = BASE + '/objects/' + row['sha256'][:2] + '/' + row['sha256'] + ending
        compressed = row['bytes'] > 64000 and suffix not in ['.pdf', '.png', '.tgz', '.gz']
        if compressed:
            dest += '.gz'
        target = a.stage / safe(dest)
        target.parent.mkdir(parents=True, exist_ok=True)
        need(not target.exists(), 'destination collision')
        if compressed:
            with src.open('rb') as inf, target.open('wb') as raw:
                with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as outf:
                    shutil.copyfileobj(inf, outf)
            with gzip.open(target, 'rb') as inf:
                h = hashlib.sha256()
                length = 0
                for chunk in iter(lambda: inf.read(1024 * 1024), b''):
                    length += len(chunk)
                    h.update(chunk)
            need((length, h.hexdigest()) == key, 'lossless payload round trip')
        else:
            shutil.copyfile(src, target)
            need(sha(target) == row['sha256'], 'exact payload copy')
        need(target.stat().st_size < 99000000, 'stored file exceeds publication limit')
        entry = dict(public_path=dest, encoding='gzip' if compressed else 'identity',
                     transport='NEW_FROZEN_FILE', stored_bytes=target.stat().st_size,
                     stored_sha256=sha(target))
        by_hash[key] = entry
        route.update(entry)
        routes.append(route)
    unique = {r['public_path']: r for r in routes if 'public_path' in r}
    new = [r for r in unique.values() if r['transport'] == 'NEW_FROZEN_FILE']
    report = dict(status='PRIVATE_EXACT_PAYLOAD_STAGE_NOT_ADMISSION',
        inventory_sha256=sha(a.inventory), files=routes, packets=inv['packets'],
        primary_sources_hash_only=inv['primary_sources_hash_only'],
        exact_primary_omission_addendum=inv['primary_omission_addendum'],
        historical_documentary_exceptions=inv['historical_documentary_exceptions'],
        relative_locator_resolutions=inv['relative_locator_resolutions'],
        legacy_common_aliases=inv['legacy_common_aliases'],
        closure_boundary=inv['closure_boundary'],
        predecessor_transports=inv['predecessor_transports'],
        markdown_transport=inv['markdown_transport'],
        logical_files=len(routes), unique_public_files=len(unique),
        new_public_files=len(new), new_stored_bytes=sum(r['stored_bytes'] for r in new),
        largest_new_stored_file=max(r['stored_bytes'] for r in new),
        all_large_payload_roundtrips_verified=True, source_assets_exported=False,
        private_mathematical_proof_fallback=False, whole_original_credit=0,
        remaining='Whole-source scope audit, public-only restoration/checker, final admission and publication.')
    dest = a.stage / BASE / 'transport.json'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['files', 'packets']}))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--inventory', type=Path, required=True)
    p.add_argument('--stage', type=Path, required=True)
    main(p.parse_args())
