"""Portable invocation of the acquired literal checker; archive-path relocation only."""
import argparse
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys
import types


def need(ok, message):
    if not ok:
        raise ValueError(message)


def content(root, ref):
    rel = PurePosixPath(ref['relative_path'])
    need(not rel.is_absolute() and rel.parts and all(p not in ('', '.', '..') for p in rel.parts),
         'Canonical relative payload path')
    p = root
    for part in rel.parts:
        p = p / part
        need(not p.is_symlink(), 'Payload paths must not be symlinks')
    need(p.is_file(), 'Required regular payload: ' + str(rel))
    b = p.read_bytes()
    need(len(b) == ref['bytes'] and hashlib.sha256(b).hexdigest() == ref['sha256'],
         'Exact payload: ' + str(rel))
    return p, b


def main():
    need(not sys.flags.optimize, 'Ordinary Python required')
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--manifest', type=Path, required=True)
    p.add_argument('--manifest-sha256', required=True)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    need(not args.out.exists(), 'Fresh output directory')
    manifest_bytes = args.manifest.read_bytes()
    need(hashlib.sha256(manifest_bytes).hexdigest() == args.manifest_sha256,
         'Externally supplied manifest identity')
    manifest = json.loads(manifest_bytes)
    need(manifest['schema'] == 'F012_LITERAL_FIGURES_PORTABLE_RUNTIME_V1', 'Manifest schema')
    roles = manifest['runtime']
    need(set(roles) == {'checker', 'case', 'certificate', 'witness_archive'}, 'Exact four runtime roles')
    need(len({x['relative_path'] for x in roles.values()}) == 4, 'Distinct runtime paths')
    root = args.root.resolve(strict=True)
    files = {role: content(root, ref) for role, ref in roles.items()}
    case = json.loads(files['case'][1])
    certificate = json.loads(files['certificate'][1])
    original_archive = copy.deepcopy(case['witness_archive'])
    need(all(original_archive[key] == roles['witness_archive'][key] for key in ('bytes', 'sha256')),
         'Archive identity preserved from acquired case')
    relocated = copy.deepcopy(case)
    relocated['witness_archive']['path'] = str(files['witness_archive'][0])
    # No historical absolute path is dereferenced. Execute the exact authenticated
    # standard-library source bytes and leave verify() and all helper bodies intact.
    module = types.ModuleType('acquired_f012_literal_figure_check')
    module.__file__ = str(files['checker'][0])
    exec(compile(files['checker'][1], module.__file__, 'exec'), module.__dict__)
    result = module.verify(relocated, certificate)
    need(result['status'] == 'CHECKED_LITERAL_DESCRIPTIVE_CERTIFICATES', 'Exact checker conclusion')
    report = dict(status='PASS', mathematical_result=result,
                  manifest_sha256=args.manifest_sha256,
                  runtime=roles, archive_relocation_only=True,
                  historical_proposer_or_platform_binaries_executed=False,
                  whole_original_credit=0)
    args.out.mkdir(parents=True, exist_ok=False)
    (args.out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'checked_graph_orders': [16, 20, 40],
                      'whole_original_credit': 0}))


if __name__ == '__main__':
    main()
