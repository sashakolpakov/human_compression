"""Verify finite evidence bytes. Do not execute archived scientific programs."""
from pathlib import Path
import hashlib
import json
import resource
import signal
import stat
import sys
import time

assert not sys.flags.optimize, 'Run without -O or -OO.'
ROOT = Path(__file__).resolve().parent
INDEX_SHA256 = '5f297f5104419cc3a0635fcf5155ff84ee3870c51a339ec3cbba6ac457da8801'
START = time.monotonic()
signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('metadata verification limit')))
signal.alarm(125)


def read(path):
    assert time.monotonic() - START < 115
    assert path.resolve(strict=True) == path
    before = path.lstat()
    assert stat.S_ISREG(before.st_mode) and before.st_size <= 4 * 2**20
    body = path.read_bytes()
    signature = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
    assert len(body) == before.st_size and signature(path.lstat()) == signature(before)
    assert resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024) <= 256 * 2**20
    return body


index_bytes = read(ROOT / 'index.json')
assert hashlib.sha256(index_bytes).hexdigest() == INDEX_SHA256
index = json.loads(index_bytes)
assert index['schema'] == 'HUMAN_COMPRESSION_PARENT_COHORT_EVIDENCE_INDEX_V1'
assert [p['name'] for p in index['parts']] == ['science', 'audit', 'registration']
assert (index['begin'], index['end'], index['parent_count'], index['strict_slots']) == (330, 342, 12, 1872)
assert index['accepted_prefix_after'] == 342 and index['accepted_slots_after'] == 53352
assert index['mathematical_replay'] is index['full_recursive_dependency_closure'] is False
reports = []
for part in index['parts']:
    name = part['name']
    descriptor = part['manifest']
    assert descriptor['path'] == name + '/manifest.json'
    folder = ROOT / name
    manifest_bytes = read(ROOT / descriptor['path'])
    assert len(manifest_bytes) == descriptor['bytes'] and hashlib.sha256(manifest_bytes).hexdigest() == descriptor['sha256']
    manifest = json.loads(manifest_bytes)
    assert manifest['schema'] == 'HUMAN_COMPRESSION_FINITE_COHORT_EVIDENCE_PART_V1' and manifest['part'] == name
    assert manifest['mathematical_replay'] is manifest['full_recursive_dependency_closure'] is False
    assert manifest['file_count'] == len(manifest['files'])
    paths, objects = set(), {}
    for entry in manifest['files']:
        assert set(entry) == {'original_path', 'object', 'bytes', 'sha256'}
        assert type(entry['original_path']) is str and entry['original_path'].startswith('/') and entry['original_path'] not in paths
        paths.add(entry['original_path'])
        digest = entry['sha256']
        assert len(digest) == 64 and set(digest) <= set('0123456789abcdef')
        assert type(entry['bytes']) is int and 0 <= entry['bytes'] <= 4 * 2**20
        assert entry['object'] == 'objects/' + digest
        assert digest not in objects or objects[digest] == entry['bytes']
        objects[digest] = entry['bytes']
    assert len(objects) == manifest['unique_objects'] and len(objects) + 1 <= 512
    assert sum(objects.values()) == manifest['unique_bytes']
    objects_dir = folder / 'objects'
    assert objects_dir.is_dir() and not objects_dir.is_symlink()
    assert {p.name for p in objects_dir.iterdir()} == set(objects)
    read_bytes = len(manifest_bytes)
    for _ in range(2):
        for digest, size in sorted(objects.items()):
            body = read(objects_dir / digest)
            read_bytes += len(body)
            assert read_bytes + len(manifest_bytes) <= 64 * 2**20
            assert len(body) == size and hashlib.sha256(body).hexdigest() == digest
    closing = read(ROOT / descriptor['path'])
    assert closing == manifest_bytes
    read_bytes += len(closing)
    reports.append(dict(part=name, listed_files=len(paths), unique_objects=len(objects), read_bytes=read_bytes))
assert read(ROOT / 'index.json') == index_bytes
signal.alarm(0)
print(json.dumps(dict(status='PASS_FINITE_COHORT_EVIDENCE_BYTES', parts=reports,
    accepted_prefix=342, mathematical_replay=False, full_recursive_dependency_closure=False), sort_keys=True))
