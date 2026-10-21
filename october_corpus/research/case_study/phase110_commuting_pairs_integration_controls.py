#!/usr/bin/env python3
"""Portable isolated controls; never modifies an author input or frozen file."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
P = 'phase110_commuting_pairs_integration_'

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def tree(path):
    return {str(f.relative_to(path)):digest(f) for f in path.rglob('*') if f.is_file()}

def run(command):
    result = subprocess.run(command,capture_output=True,text=True)
    return dict(command=[str(x) for x in command],returncode=result.returncode,
                stdout=result.stdout,stderr=result.stderr)

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-dir',type=Path,required=True)
    args = ap.parse_args()
    need(not args.output_dir.exists(),'Refusing existing controls directory')
    args.output_dir.mkdir(parents=True)
    snap = args.output_dir/'portable'
    snap.mkdir()
    intake = json.loads((ROOT/(P+'intake.json')).read_text())
    names = {str(f.relative_to(ROOT)) for f in ROOT.glob(P+'*') if f.is_file()}
    names.update(str(f.relative_to(ROOT)) for f in (ROOT/(P+'replay')).rglob('*') if f.is_file())
    names.update(r['path'] for r in intake['retained_input_bindings'])
    # A frozen manifest also binds later author reports; include its exact allowlist.
    manifest = ROOT/(P+'manifest.json')
    if manifest.exists():
        names.update(r['path'] for r in json.loads(manifest.read_text())['files'])
    for name in sorted(names):
        need(not name.startswith('sources/') and not name.endswith(('.pdf','.png')), 'Primary asset in portable copy')
        target = snap/name
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/name,target)
    checks = []
    verify = [sys.executable,'-B','-O',str(snap/(P+'verify.py')),'--output']
    fresh = run(verify+[str(args.output_dir/'portable_result.json')])
    need(fresh['returncode'] == 0,'Portable verification failed: '+fresh['stderr'])
    checks.append(dict(name='portable_nonprimary_reconstruction',**fresh))
    before = tree(snap)
    sentinel = args.output_dir/'sentinel.json'
    sentinel.write_text('DO NOT OVERWRITE\n')
    outputdir = args.output_dir/'existing'
    outputdir.mkdir()
    (outputdir/'sentinel').write_text('DO NOT OVERWRITE\n')
    no_clobbers = [
        ('verify',verify+[str(sentinel)]),
        ('build',[sys.executable,'-B','-O',str(snap/(P+'build.py')),'--output-dir',str(outputdir)]),
        ('run',[sys.executable,'-B','-O',str(snap/(P+'run.py')),'--output-dir',str(outputdir)]),
        ('formula',[sys.executable,'-B','-O',str(snap/(P+'formula.py')),'--output',str(sentinel)])]
    for name,command in no_clobbers:
        result = run(command)
        need(result['returncode'] != 0 and 'Refusing existing' in result['stderr'],'No-clobber failure '+name)
        need(sentinel.read_text() == 'DO NOT OVERWRITE\n' and tree(snap) == before,'No-clobber changed input')
        checks.append(dict(name='no_clobber_'+name,**result))
    mutations = [P+'manuscript.md',P+'core.md',P+'branch.md',P+'finite.g',P+'formula.py',
                 P+'replay/finite.log','phase78_n009_integration_manuscript.md']
    for index,name in enumerate(mutations):
        path = snap/name
        original = path.read_bytes()
        path.write_bytes(original+b'\n# isolated mutation\n')
        out = args.output_dir/('mutation-'+str(index)+'.json')
        result = run(verify+[str(out)])
        path.write_bytes(original)
        need(result['returncode'] != 0 and not out.exists(),'Mutation accepted '+name)
        need(tree(snap) == before,'Mutation restoration failed')
        checks.append(dict(name='mutation_'+name,**result))
    report = dict(status='PASS',portable_files=[dict(path=name,sha256=digest(snap/name)) for name in sorted(names)],
                  private_primary_assets_copied=False,portable_verification=True,
                  no_clobber_cases=4,mutation_cases=len(mutations),checks=checks,
                  note='Optimized controls detect bound-input changes; they do not replace mathematical review')
    (args.output_dir/'controls.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',portable_files=len(names),no_clobber_cases=4,mutation_cases=len(mutations))))

if __name__ == '__main__':
    main()
