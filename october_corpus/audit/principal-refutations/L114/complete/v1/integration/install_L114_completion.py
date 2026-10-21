"""Install the exact L114 supplement only when the root explicitly requests it."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode = True
from pathlib import Path
import argparse
import ctypes
import importlib.util
import json
import os
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
PUBLIC = Path('/Users/sasha/medusa/math_compression')
spec = importlib.util.spec_from_file_location('completion_guard', HERE/'check_L114_completion.py')
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


def clone_or_copy(source, destination):
    guard.need(shutil.disk_usage(destination.parent).free >= 4*2**30+source.stat().st_size, 'Preserve 4 GiB reserve')
    guard.need(not destination.exists(), 'Fresh destination')
    if sys.platform == 'darwin':
        fn = ctypes.CDLL('/usr/lib/libSystem.B.dylib', use_errno=True).clonefile
        fn.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
        fn.restype = ctypes.c_int
        if fn(os.fsencode(source), os.fsencode(destination), 0):
            raise OSError(ctypes.get_errno(), str(destination))
        guard.need(source.stat().st_ino != destination.stat().st_ino, 'Independent clone inode')
    else:
        shutil.copyfile(source, destination)
    guard.need(guard.sha(source) == guard.sha(destination), 'Exact installed bytes')


def main(args):
    root = args.repo.resolve()
    guard.need(root == PUBLIC.resolve(), 'One explicit public destination')
    guard.need(args.verify_inputs != args.allow_public_write, 'Choose verification or explicit root installation')
    guard.need(guard.git(root, 'rev-parse', 'HEAD').decode().strip() == guard.BASELINE, 'Exact predecessor commit')
    guard.need(not guard.git(root, 'status', '--porcelain').strip(), 'Clean predecessor')
    rows = guard.load(HERE/'install_files.json')['files']
    guard.need(not any(r['path'].lower().endswith('.md') for r in rows), 'No new public Markdown paths')
    payload = guard.load(HERE/'payload_manifest.json')
    params = guard.load(HERE/'parameters.json')
    guard.need([{k:v for k,v in r.items() if k!='source_path'} for r in rows] == payload['files'], 'Exact installation plan')
    guard.need(not (root/guard.AUD).exists(), 'Fresh supplement; do not replace evidence')
    for r in rows:
        source = Path(r['source_path'])
        guard.need(source.is_file() and source.stat().st_size == r['bytes'] and guard.sha(source) == r['sha256'], 'Exact installation source '+str(source))
        dest = guard.safe(root, r['path'])
        guard.need(not dest.exists() or r['path'] in params['replaced_paths'], 'Fresh or declared replacement')
    for row in params['preserved']:
        guard.bind(root, row)
    for old_path, row in params['old_mutable'].items():
        guard.need(guard.pin(root/old_path, root) == row, 'Exact old mutable bytes')
    route = {r['path']: Path(r['source_path']) for r in rows}
    old = guard.load(root/'audit/corpus/latest.json')
    new = guard.load(route['audit/corpus/latest.json'])
    admission = guard.load(route[guard.AUD+'/admission.json'])
    guard.semantic(old,new,admission)
    guard.need(route['scripts/verify_snapshot.py'].read_text() == guard.verifier_delta((root/'scripts/verify_snapshot.py').read_text()), 'Only verifier dispatch changes')
    mapping = guard.load(route[guard.AUD+'/operational/mapping.json'])
    transport = guard.load(route[guard.AUD+'/transport.json'])
    premises = guard.operational_boundary(mapping, transport)
    guard.need(all(row['sha256'] not in premises for row in rows), 'No documentary or environment premise in installation payload')
    documentary_controls = guard.boundary_controls(mapping, transport)
    controls = guard.controls(old,new,admission)
    report = dict(status='PASS_L114_INSTALLATION_INPUTS', payload_files=len(rows), payload_bytes=sum(r['bytes'] for r in rows),
                  controls=controls, documentary_controls=documentary_controls, premise_objects=len(premises), public_writes=False, historical_science_replayed=False)
    if args.verify_inputs:
        print(json.dumps(report, sort_keys=True))
        return
    guard.need(shutil.disk_usage(root).free >= 4*2**30+sum(r['bytes'] for r in rows)+2**20, '4 GiB reserve plus full exact publication bound')
    # All bindings, semantics and target paths were checked before the first mutation.
    # History is first in the frozen plan, so every old mutable file survives before replacement.
    for r in rows:
        source = Path(r['source_path'])
        dest = guard.safe(root,r['path'])
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            temporary = dest.with_name(dest.name+'.L114-install')
            clone_or_copy(source,temporary)
            os.replace(temporary,dest)
        else:
            clone_or_copy(source,dest)
    for name in ['parameters.json','payload_manifest.json']:
        dest=root/guard.AUD/'integration'/name
        clone_or_copy(HERE/name,dest)
    report.update(status='L114_INSTALLED_REQUIRING_ROOT_GATE', public_writes=True, final_root_gate_created=False)
    print(json.dumps(report, sort_keys=True))


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--verify-inputs',action='store_true')
    p.add_argument('--allow-public-write',action='store_true')
    main(p.parse_args())
