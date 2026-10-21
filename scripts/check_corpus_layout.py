#!/usr/bin/env python3
"""Check one exact Git-tree prefix migration; does not replay scientific work."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess

BASELINE = '0466df5e0b0f1c83da3980c4e7b85c69cdca103a'
BASELINE_TREE = '9ce41a39a1e31d63ee3b2e5fa31abf0e2723f2d8'
PREFIX = 'october_corpus/'
LEGACY_README_SHA = 'eec244690cf93dd922dd94666b36cc0f97dbf0182d1cdde4bd0c84aa2bbe2f6c'
NEW = {'.gitignore', '.gitattributes', 'LICENSE', 'README.md',
    'scripts/check_corpus_layout.py', 'corpora.json', 'october_corpus/README.md',
    'october_corpus/REPRODUCING.md', 'november_corpus/README.md'}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def git_text(root, *args):
    p = subprocess.run(['git', '--no-optional-locks', '-c', 'core.fsmonitor=false',
        *args], cwd=root, capture_output=True, timeout=60)
    need(p.returncode == 0 and len(p.stdout) <= 4096, 'Git query failed: ' + ' '.join(args))
    return p.stdout.decode().strip()


def git_records(root, *args):
    """Stream NUL records; never buffer a complete tree/index/blob subprocess."""
    p = subprocess.Popen(['git', '--no-optional-locks', '-c', 'core.fsmonitor=false',
        *args], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    pending = b''
    try:
        while True:
            chunk = p.stdout.read(65536)
            if not chunk:
                break
            records = (pending + chunk).split(b'\0')
            pending = records.pop()
            for record in records:
                yield record.decode()
            need(len(pending) <= 65536, 'Bounded individual Git record')
        need(not pending and p.wait(timeout=60) == 0, 'Complete successful Git record stream')
    finally:
        p.stdout.close()
        if p.poll() is None:
            p.kill()
            p.wait()


def blob_pin(root, name, oid):
    p = subprocess.Popen(['git', '--no-optional-locks', 'cat-file', 'blob', oid],
        cwd=root, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    h = hashlib.sha256()
    size = 0
    try:
        while True:
            block = p.stdout.read(65536)
            if not block:
                break
            size += len(block)
            need(size <= 2 * 1024**2, 'Bounded added documentation/Source blob')
            h.update(block)
        need(p.wait(timeout=60) == 0, 'Complete added Git blob')
    finally:
        p.stdout.close()
        if p.poll() is None:
            p.kill()
            p.wait()
    return dict(path=name, bytes=size, sha256=h.hexdigest())


def verify(root, revision=None, *, baseline=BASELINE,
           baseline_tree=BASELINE_TREE, baseline_count=48690):
    root = Path(root).absolute()
    need(root.resolve(strict=True) == root, 'Use the canonical actual repository root')
    need(Path(git_text(root, 'rev-parse', '--show-toplevel')).resolve() == root, 'Actual Git root')
    need(git_text(root, 'rev-parse', baseline + '^{tree}') == baseline_tree, 'Exact retained baseline tree')
    git_text(root, 'merge-base', '--is-ancestor', baseline, 'HEAD')
    current_head = git_text(root, 'rev-parse', 'HEAD')
    selected = None
    if revision is not None:
        selected = git_text(root, 'rev-parse', '--verify', revision + '^{commit}')
        need(git_text(root, 'show', '-s', '--format=%P', selected) == baseline,
            'The selected layout commit has exactly the frozen baseline parent')
        git_text(root, 'merge-base', '--is-ancestor', selected, current_head)
    else:
        need(current_head == baseline, 'Precommit --index mode starts at the frozen baseline')
    expected = {}
    for record in git_records(root, 'ls-tree', '-r', '--full-tree', '-z', baseline):
        head, name = record.split('\t', 1)
        mode, kind, oid = head.split()
        need(kind == 'blob' and mode in {'100644', '100755', '120000'}, 'Original file/symlink mode')
        expected[PREFIX + name] = (mode, oid)
    need(len(expected) == baseline_count, 'Complete baseline path count, including formerly sparse files')
    seen = set()
    args = ('ls-files', '--stage', '-z') if selected is None else (
        'ls-tree', '-r', '--full-tree', '-z', selected)
    for record in git_records(root, *args):
        head, name = record.split('\t', 1)
        if selected is None:
            mode, oid, stage = head.split()
            need(stage == '0', 'Resolved index')
        else:
            mode, kind, oid = head.split()
            need(kind == 'blob', 'Migration contains only the declared files and symlinks')
        need(name not in seen, 'Unique migrated path')
        seen.add(name)
        need(name in expected or name in NEW, 'Undeclared indexed path: ' + name)
        if name in expected:
            need((mode, oid) == expected[name], 'Changed baseline mode/blob: ' + name)
        else:
            need(mode == '100644', 'New documentation has ordinary nonexecutable mode')
            expected[name] = (mode, oid)
    need(NEW <= seen and seen == set(expected), 'No omitted baseline or declared new path')
    for name in git_records(root, 'ls-files', '--others', '--exclude-standard', '-z'):
        need(False, 'Ordinary undeclared untracked file: ' + name)
    if selected is not None:
        # This concerns the CURRENT checkout, separately from historical mapping.
        git_text(root, 'diff', '--quiet', '--no-ext-diff', '--')
        git_text(root, 'diff', '--cached', '--quiet', '--no-ext-diff', '--')
        need(git_text(root, 'rev-parse', 'HEAD') == current_head, 'Stable current HEAD')
        pins = [blob_pin(root, name, expected[name][1]) for name in sorted(NEW)]
        return dict(status='PASS_EXACT_OCTOBER_CORPUS_LAYOUT', verification_mode='revision',
            baseline=baseline, baseline_tree=baseline_tree, migration_revision=selected,
            current_head=current_head, current_worktree_clean=True,
            corpus_prefix=PREFIX, inherited_paths=baseline_count, declared_new_files=sorted(NEW),
            new_file_pins=pins, whole_working_tree_bytes_streamed=0,
            legacy_readme_source_sha256=LEGACY_README_SHA,
            new_document_contents_scientifically_validated=False,
            historical_verifier_replayed=False, scientific_replay=False, original_or_census_credit=0)
    for record in git_records(root, 'ls-files', '-v', '-z'):
        need(record.startswith('H '), 'No skip-worktree/assume-unchanged path in migrated materialization')
    directories = {root}
    total = 0
    readme_identical = False
    new_pins = []
    for name, (mode, oid) in expected.items():
        rel = PurePosixPath(name)
        need(not rel.is_absolute() and '..' not in rel.parts, 'Literal repository-relative path')
        path = root / name
        parent = path.parent
        while parent not in directories:
            need(stat.S_ISDIR(parent.lstat().st_mode), 'Ordinary in-tree directory: ' + str(parent))
            directories.add(parent)
            parent = parent.parent
        before = path.lstat()
        if mode == '120000':
            need(stat.S_ISLNK(before.st_mode), 'Preserved relative symlink: ' + name)
            raw = os.fsencode(os.readlink(path))
            need(not os.path.isabs(os.fsdecode(raw)) and path.resolve().is_relative_to(root / 'october_corpus'),
                'Preserved symlink stays inside the corpus: ' + name)
            actual = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
            size = len(raw)
        else:
            need(stat.S_ISREG(before.st_mode) and bool(before.st_mode & 0o111) == (mode == '100755'),
                'Preserved regular/executable mode: ' + name)
            size = before.st_size
            if name in NEW:
                need(size <= 2 * 1024**2, 'Bounded new documentation/verification Source: ' + name)
            h = hashlib.sha1(b'blob ' + str(size).encode() + b'\0')
            q = hashlib.sha256() if name in NEW else None
            with path.open('rb') as stream:
                opened = os.fstat(stream.fileno())
                while True:
                    block = stream.read(512 * 1024)
                    if not block:
                        break
                    h.update(block)
                    if q is not None:
                        q.update(block)
                finished = os.fstat(stream.fileno())
            signature = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
            need(signature(before) == signature(opened) == signature(finished) == signature(path.lstat()),
                'Stable streamed whole file: ' + name)
            actual = h.hexdigest()
            if q is not None:
                new_pins.append(dict(path=name, bytes=size, sha256=q.hexdigest()))
                if name == 'october_corpus/README.md':
                    readme_identical = q.hexdigest() == LEGACY_README_SHA
        need(actual == oid, 'Working-tree bytes differ from the exact staged blob: ' + name)
        total += size
    # Recheck the index after streaming; no checker/manifest/metadata is rewritten.
    final = {}
    for record in git_records(root, 'ls-files', '--stage', '-z'):
        head, name = record.split('\t', 1)
        mode, oid, stage = head.split()
        need(stage == '0' and name not in final, 'Stable resolved final index')
        final[name] = (mode, oid)
    need(final == expected, 'Index stayed identical during whole-file verification')
    need(git_text(root, 'rev-parse', 'HEAD') == current_head, 'Stable precommit HEAD')
    return dict(status='PASS_EXACT_OCTOBER_CORPUS_LAYOUT', verification_mode='index', baseline=baseline,
        baseline_tree=baseline_tree, corpus_prefix=PREFIX, inherited_paths=baseline_count,
        declared_new_files=sorted(NEW), new_file_pins=sorted(new_pins,key=lambda q:q['path']),
        whole_working_tree_bytes_streamed=total,
        legacy_readme_source_sha256=LEGACY_README_SHA, legacy_readme_byte_identical=readme_identical,
        new_document_contents_scientifically_validated=False, historical_verifier_replayed=False,
        scientific_replay=False, original_or_census_credit=0)


def main():
    p = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    p.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1])
    mode = p.add_mutually_exclusive_group()
    mode.add_argument('--index', action='store_true', help='Check the staged migration before its commit.')
    mode.add_argument('--revision', help='Check the fixed migration commit, not later corpus edits.')
    a = p.parse_args()
    revision = a.revision
    if not a.index and revision is None:
        registry = a.repo / 'corpora.json'
        need(stat.S_ISREG(registry.lstat().st_mode) and registry.stat().st_size <= 65536,
            'Ordinary bounded root corpus registry')
        revision = json.loads(registry.read_text()).get('layout_commit')
        need(type(revision) is str and len(revision) == 40
            and all(c in '0123456789abcdef' for c in revision),
            'Use --index before commitment; otherwise pin the actual layout_commit in corpora.json')
    print(json.dumps(verify(a.repo, revision), sort_keys=True))


if __name__ == '__main__':
    main()
