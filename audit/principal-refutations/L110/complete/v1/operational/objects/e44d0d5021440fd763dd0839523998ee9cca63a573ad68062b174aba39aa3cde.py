"""Freeze the one unexecuted library-input request; no GAP invocation."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
P = HERE.parent
GAP = Path('/opt/homebrew/Cellar/gap/4.15.1')
PKG = GAP / 'lib/gap/pkg'


def pin(path, base=None):
    data = path.read_bytes()
    return dict(path=str(path.relative_to(base) if base else path),
                bytes=len(data), sha256=hashlib.sha256(data).hexdigest())


def main():
    if (HERE / 'request.json').exists() or (HERE / 'manifest.json').exists():
        raise RuntimeError('Fresh request only')
    paths = [HERE / n for n in ['export.g', 'run.py', 'argument.rst', 'freeze.py', 'owner_controls.py', 'owner_controls.json']]
    paths += [P / 'character_application/theory.tex',
              P / 'character_application_root_review/manifest.json',
              P / 'algorithm_scope_review_adoption/manifest.json',
              Path('/opt/homebrew/bin/gap')]
    # Reuse the complete character-library data binding set already inspected.
    previous = json.loads((P / 'character_request02/request.json').read_text())
    paths += [Path(r['path']) for r in previous['bindings']
              if r['path'].startswith(str(PKG / 'ctbllib'))]
    for package, folder in [('ctbllib', 'gap4'), ('tomlib', 'gap')]:
        paths += [PKG / package / n for n in ['PackageInfo.g', 'init.g', 'read.g']]
        paths += sorted(p for p in (PKG / package / folder).iterdir() if p.is_file())
    paths += [GAP / 'share/gap/lib/tom.gd', GAP / 'share/gap/lib/tom.gi',
              PKG / 'tomlib/doc/tomlib.xml']
    paths += [PKG / 'tomlib/data' / (name + '.tom.gz') for name in
              ['tmmath', 'tmjank', 'tmhs2', 'tmhsmcl', 'tmhe2']]
    paths = list(dict.fromkeys(paths))
    req = dict(status='FROZEN_L036_MARK_INPUT_EXPORT_AWAITING_ROOT_REVIEW',
        source_ids=['L036'],
        outer_groups=['M12.2', 'J2.2', 'J3.2', 'HS.2', 'McL.2', 'He.2'],
        simple_suborbit_groups=['M11', 'M12', 'M22', 'M23', 'J1'],
        command=['/opt/homebrew/bin/gap', '-q', '-b', '-T', '-o', '512m',
                 '-K', '512m', str(HERE / 'export.g')],
        deadline_seconds=60, output_cap_bytes=64 * 2**20,
        launch_reserve_bytes=4 * 2**30, emergency_floor_bytes=2 * 2**30,
        software_premise='Installed GAP 4.15.1 and its library loaders; no kernel verification claimed.',
        successor_authorized=False, supersedes_unexecuted_request=pin(P/'table_request01/request.json'),
        revision='Supervision cleanup, final resource checks and final exact input rehash only; exporter byte-identical.',
        bindings=[pin(p) for p in paths])
    (HERE / 'request.json').write_text(json.dumps(req, indent=2) + '\n')
    manifest = dict(status=req['status'], source_ids=['L036'], target_executed=False,
                    exports=[pin(p, HERE) for p in sorted(HERE.iterdir()) if p.is_file()])
    (HERE / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(dict(manifest=pin(HERE / 'manifest.json'),
                         request=pin(HERE / 'request.json'), bindings=len(paths),
                         target_executed=False)))


if __name__ == '__main__':
    main()
