"""Check this finite archive without executing archived mathematics."""
from pathlib import Path
import hashlib
import json
import os
import resource
import signal
import stat
import sys
import time

if sys.flags.optimize:
    raise SystemExit('Run without -O: assertions perform verification.')
BASE = Path(__file__).resolve().parent
START = time.monotonic()
READ = 0
signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('125 second verification limit')))
signal.alarm(125)


def read(relative, expected=None):
    global READ
    path = BASE / relative
    assert path.is_relative_to(BASE) and '..' not in Path(relative).parts
    before = path.lstat()
    assert path.resolve(strict=True) == path and stat.S_ISREG(before.st_mode)
    assert before.st_size <= 4 * 2**20 and time.monotonic() - START < 115
    assert resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024) <= 256 * 2**20
    with path.open('rb') as stream:
        opened = os.fstat(stream.fileno())
        body = stream.read(before.st_size + 1)
        finished = os.fstat(stream.fileno())
    sig = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
    assert len(body) == before.st_size and sig(before) == sig(opened) == sig(finished) == sig(path.lstat())
    READ += len(body)
    assert READ <= 128 * 2**20
    if expected is not None:
        assert len(body) == expected['bytes'] and hashlib.sha256(body).hexdigest() == expected['sha256']
    return body


index = json.loads(read('index.json'))
assert index['schema'] == 'REVIEWED_INTAKE_PROGRESS_ARCHIVE_V2'
assert 8 <= len(index['parts']) <= 64
objects = {}
logical_files = 0
for part in index['parts']:
    manifest = json.loads(read(part['manifest']['path'], part['manifest']))
    assert manifest['schema'] == 'FINITE_REVIEWED_INTAKE_EVIDENCE_PART_V1'
    assert manifest['name'] == part['name']
    assert len(manifest['files']) == manifest['file_count'] <= 512
    for entry in manifest['files']:
        digest = entry['sha256']
        assert len(digest) == 64 and set(digest) <= set('0123456789abcdef')
        assert entry['object'] == 'objects/' + digest
        if digest not in objects:
            read(entry['object'], entry)
            objects[digest] = entry['bytes']
        else:
            assert objects[digest] == entry['bytes']
        logical_files += 1
assert len(objects) == index['unique_objects']
assert sum(objects.values()) == index['unique_bytes']
theory = json.loads(read('theory.json'))
assert theory['schema'] == 'FINITE_REVIEWED_INTAKE_THEORY_V1'
assert len(theory['files']) == theory['file_count'] == 11
for entry in theory['files']:
    assert Path(entry['object']).parts[0] == 'theory'
    read(entry['object'], entry)
signal.alarm(0)
print(json.dumps(dict(status='PASS', files=logical_files, unique_objects=len(objects),
    unique_bytes=sum(objects.values()), theory_files=len(theory['files']),
    physical_read_bytes=READ, mathematical_replay=False), sort_keys=True, indent=2))
