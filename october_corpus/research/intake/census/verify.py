"""Stream census byte objects; this does not execute mathematical checkers."""
import argparse
import hashlib
import json
import re
import subprocess
import urllib.request
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--manifest', type=Path, default=HERE / 'checkpoints/job_155_subgroups/manifest.json')
parser.add_argument('--new-only', action='store_true', help='Check objects introduced by this checkpoint only.')
parser.add_argument('--remote', action='store_true', help='Read every selected body from the immutable public commit.')
args = parser.parse_args()
assert args.manifest.stat().st_size <= 4 * 2**20
manifest = json.loads(args.manifest.read_bytes())
assert manifest['schema'] in ['OCTOBER_ACTIVE_CENSUS_CHECKPOINT_V1', 'OCTOBER_ACTIVE_CENSUS_CHECKPOINT_V2']
assert len(manifest['files']) < 6000
commit = subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip()
assert re.fullmatch('[0-9a-f]{40}', commit)
seen = {}
checked = total = 0
for row in manifest['files']:
    assert type(row['bytes']) is int and 0 <= row['bytes'] <= 8 * 2**20
    assert re.fullmatch('[0-9a-f]{64}', row['sha256'])
    storage = row['storage']
    if args.new_only and 'commit' in storage:
        continue
    relative = PurePosixPath(storage['path'])
    assert not relative.is_absolute() and '..' not in relative.parts
    edition = storage.get('commit', commit)
    assert re.fullmatch('[0-9a-f]{40}', edition)
    key = (edition, str(relative))
    if key in seen:
        assert seen[key] == (row['bytes'], row['sha256'])
        continue
    seen[key] = (row['bytes'], row['sha256'])
    local = ROOT.joinpath(*relative.parts)
    use_local = not args.remote and edition == commit and local.is_file()
    if use_local:
        assert not local.is_symlink() and local.resolve().is_relative_to(ROOT)
        stream = local.open('rb')
    else:
        url = 'https://raw.githubusercontent.com/sashakolpakov/human_compression/' + edition + '/' + str(relative)
        stream = urllib.request.urlopen(url, timeout=30)
    h = hashlib.sha256()
    count = 0
    with stream:
        while block := stream.read(65536):
            count += len(block)
            total += len(block)
            assert count <= row['bytes'] and total <= 80 * 2**20
            h.update(block)
    assert count == row['bytes'] and h.hexdigest() == row['sha256'], row
    checked += 1
    if checked % 100 == 0:
        print(json.dumps(dict(checked_objects=checked, bytes=total)), flush=True)
print(json.dumps(dict(status='VERIFIED_BYTE_OBJECTS', objects=checked, bytes=total,
                      mathematical_checkers_executed=0, files_materialized=0)))
