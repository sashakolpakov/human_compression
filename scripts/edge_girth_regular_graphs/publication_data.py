"""Authenticate the selected public payload or restore its 53 written sources.

Transport only: no theorem evaluation, native build, scientific replay, download
or private fallback. The existing acquired Runtime performs all object checks.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import stat
from pathlib import Path, PurePosixPath
import sys

sys.dont_write_bytecode = True
MIB = 2**20
SELECTION = 'data/edge_girth_regular_graphs/publication_selection.json'
RUNTIME = 'scripts/edge_girth_regular_graphs/runtime.py'
RUNTIME_SHA = 'e76919bf176912ac7b655a01fd3c4bc051ebb2c1d14db7a94a09658207ff5799'


def need(value, message):
    if not value:
        raise ValueError(message)


def ordinary(root, name):
    relative = PurePosixPath(name)
    need(not relative.is_absolute() and relative.parts and '..' not in relative.parts
         and str(relative) == name, 'Canonical package-relative name')
    path = root.joinpath(*relative.parts)
    need(path.is_file() and not any(p.is_symlink() for p in (path, *path.parents)),
         'Ordinary exact public file')
    return path


def digest(path):
    h, count = hashlib.sha256(), 0
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(MIB), b''):
            h.update(block)
            count += len(block)
    return count, h.hexdigest()


def canonical_directory(value):
    """Require an existing absolute directory with a literal canonical spelling."""
    need(isinstance(value, str) and value and '\x00' not in value,
         'Literal directory path')
    path = Path(value)
    need(path.is_absolute() and path.anchor == '/' and str(path) == value
         and '..' not in path.parts, 'Canonical absolute directory spelling')
    for parent in (path, *path.parents):
        mode = parent.lstat().st_mode
        need(stat.S_ISDIR(mode) and not stat.S_ISLNK(mode),
             'Ordinary directory and ancestors')
    need(path.resolve(strict=True) == path, 'Canonical directory identity')
    return path


def restore_destination(root, value):
    """Reject aliases and overlap before importing Runtime or creating output."""
    root = canonical_directory(str(root))
    need(isinstance(value, str) and value and '\x00' not in value,
         'Literal restore path')
    out = Path(value)
    need(out.is_absolute() and out.anchor == '/' and str(out) == value
         and '..' not in out.parts, 'Canonical absolute restore spelling')
    canonical_directory(str(out.parent))
    need(not os.path.lexists(out), 'Fresh restore path, including no broken link')
    need(out.resolve(strict=False) == out, 'Canonical restore identity')
    need(not out.is_relative_to(root) and not root.is_relative_to(out),
         'Fresh restore outside the package')
    return out


def main():
    need(not sys.flags.optimize, 'Ordinary Python required')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    parser.add_argument('--selection-sha256', required=True)
    sub = parser.add_subparsers(dest='action', required=True)
    sub.add_parser('inspect')
    sub.add_parser('verify')
    restore = sub.add_parser('restore-written')
    restore.add_argument('--out', required=True)
    args = parser.parse_args()
    root = canonical_directory(args.root)
    out = restore_destination(root, args.out) if args.action == 'restore-written' else None
    selection_path = ordinary(root, SELECTION)
    need(selection_path.stat().st_size <= 2*MIB, 'Bounded publication selection')
    raw = selection_path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == args.selection_sha256, 'External publication selection pin')
    selection = json.loads(raw)
    need(selection['schema'] == 'F012_PUBLICATION_SELECTION_V1', 'Exact selection schema')
    parts = {row['relative_path']: row for row in selection['required_parts']}
    need(len(parts) == len(selection['required_parts']) == 1182
         and sum(row['bytes'] for row in parts.values()) == 531189137,
         'Exact selected payload count and bytes')
    runtime_path = ordinary(root, RUNTIME)
    need(digest(runtime_path)[1] == RUNTIME_SHA, 'Unchanged acquired transport source')
    if args.action == 'inspect':
        print(json.dumps(dict(status='SELECTION_METADATA_ONLY', objects=1176, parts=1182,
            declared_bytes=531189137, written_sources=53, payloads_read=0,
            scientific_calls=0, whole_original_credit=0)))
        return
    spec = importlib.util.spec_from_file_location('acquired_f012_publication_runtime', runtime_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if args.action == 'restore-written':
        written = selection['written']
        need(len(written['logical_paths']) == len(set(written['logical_paths'])) == 53,
             'All 53 exact written-source joins')
        runtime = module.Runtime(root, written['manifest']['relative_path'], written['manifest']['sha256'])
        report = runtime.materialize(written['logical_paths'], out, allow_unresolved=False)
        report.update(scientific_calls=0, written_source_count=53,
                      scope='Exact written-source bytes only; no theorem or TeX execution.')
        print(json.dumps(report, sort_keys=True))
        return
    checked_objects, seen_parts = set(), set()
    checked_bytes = 0
    for group in selection['selected_manifests']:
        record = group['manifest']
        runtime = module.Runtime(root, record['relative_path'], record['sha256'])
        for key in group['logical_paths']:
            _, entry = runtime.entry(key, allow_unresolved=True)
            object_name = entry['object']
            for part in runtime.objects[object_name]['parts']:
                need(parts.get(part['relative_path']) == part, 'Exact selected part metadata')
                seen_parts.add(part['relative_path'])
            if object_name in checked_objects:
                continue
            for _ in runtime.object_blocks(key, allow_unresolved=True):
                pass
            checked_objects.add(object_name)
            checked_bytes += entry['bytes']
        del runtime
    need(len(checked_objects) == 1176 and checked_bytes == 531189137 and seen_parts == set(parts),
         'Complete selected union, with no missing or extra part')
    for row in selection['figure_inputs']:
        need(digest(ordinary(root, row['relative_path'])) == (row['bytes'], row['sha256']),
             'Exact separate literal-figure input')
    print(json.dumps(dict(status='VERIFIED_PUBLICATION_PAYLOAD_BYTES_ONLY', objects=1176,
        parts=1182, bytes=checked_bytes, figure_inputs=len(selection['figure_inputs']),
        scientific_calls=0, whole_original_credit=0,
        qualification='Hashes authenticate selected bytes; they do not reproduce mathematical predicates, borrowed catalogue completeness, native toolchains or publication admission.')))


if __name__ == '__main__':
    main()
