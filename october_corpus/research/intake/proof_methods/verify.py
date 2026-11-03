"""Verify the finite evidence archive's bytes; do not execute its contents."""
import hashlib
import json
from pathlib import Path
import re
import stat
import sys
import time

ROOT = Path(__file__).resolve().parent
MANIFEST_SHA256 = 'b3305761299d83d43c5ed7e5de02ca1284e617c9461da14426077961c6b77a3e'
MAX_READ = 64 * 2**20


def main():
    if sys.flags.optimize:
        raise RuntimeError('Run without -O or -OO so that every check is enabled.')
    started = time.monotonic()
    read_bytes = 0
    signatures = {}

    def read(path):
        nonlocal read_bytes
        before = path.lstat()
        assert stat.S_ISREG(before.st_mode) and before.st_size <= 4 * 2**20
        assert time.monotonic() - started < 100
        with path.open('rb') as stream:
            body = stream.read(4 * 2**20 + 1)
        assert len(body) == before.st_size <= 4 * 2**20
        read_bytes += len(body)
        assert read_bytes <= MAX_READ
        after = path.lstat()
        sig = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mode, s.st_mtime_ns, s.st_ctime_ns)
        assert sig(before) == sig(after)
        assert path not in signatures or signatures[path] == sig(after)
        signatures[path] = sig(after)
        return body

    raw = read(ROOT / 'manifest.json')
    assert hashlib.sha256(raw).hexdigest() == MANIFEST_SHA256
    manifest = json.loads(raw)
    assert manifest['schema'] == 'HUMAN_COMPRESSION_FINITE_PROOF_METHOD_ARCHIVE_V1'
    assert manifest['file_count'] == len(manifest['files']) == 299
    assert manifest['unique_objects'] == 290
    assert manifest['mathematical_replay'] is False
    assert manifest['complete_recursive_or_clean_clone_reproduction_claimed'] is False
    assert manifest['intake_complete'] == 101 and manifest['intake_mathematical_originals'] == 104
    originals = {}
    objects = {}
    for item in manifest['files']:
        assert set(item) == {'original_path', 'object', 'bytes', 'sha256'}
        name = item['original_path']
        assert type(name) is str and name.startswith('/') and name not in originals
        assert type(item['bytes']) is int and 0 <= item['bytes'] <= 4 * 2**20
        assert re.fullmatch(r'[0-9a-f]{64}', item['sha256'])
        assert item['object'] == 'objects/' + item['sha256']
        assert item['object'] not in objects or objects[item['object']] == item['bytes']
        objects[item['object']] = item['bytes']
        originals[name] = item
    assert len(objects) == 290 and len(signatures) + len(objects) <= 512
    assert (ROOT / 'objects').is_dir() and not (ROOT / 'objects').is_symlink()
    assert {p.name for p in (ROOT / 'objects').iterdir()} == {name[8:] for name in objects}
    for name, size in objects.items():
        body = read(ROOT / name)
        assert len(body) == size and hashlib.sha256(body).hexdigest() == name[8:]
    old_sha = manifest['source_retention_manifest_sha256']
    assert old_sha == 'd24a87db4a35a2cd44c184b0a922b27bedb854eb0a597e3a2e4199d9a77075f2'
    previous = json.loads(read(ROOT / 'objects' / old_sha))
    assert previous['file_count'] == len(previous['files']) == manifest['original_listed_files'] == 273
    for item in previous['files']:
        exported = originals[item['original_path']]
        assert exported['bytes'] == item['bytes'] and exported['sha256'] == item['sha256']
    for name, size in objects.items():
        body = read(ROOT / name)
        assert len(body) == size and hashlib.sha256(body).hexdigest() == name[8:]
    assert read(ROOT / 'manifest.json') == raw
    print(json.dumps(dict(status='PASS_FINITE_EVIDENCE_BYTES', listed_files=299,
        unique_objects=290, original_retained_files=273, read_bytes=read_bytes,
        mathematical_replay=False, full_dependency_closure_verified=False,
        completed_manuscript_or_conjecture_credit=0), sort_keys=True))


if __name__ == '__main__':
    main()
