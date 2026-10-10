#!/usr/bin/env python3
"""Independent public-only isolation, input-integrity and no-clobber controls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

MANIFEST='phase109_cover_families_generalization_manifest.json'
CHECKER='phase112_cover_families_review_check.py'

def require(ok,label):
    if not ok:raise RuntimeError(label)

def record(path):
    raw=path.read_bytes()
    return dict(sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw))

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input-root',type=Path,default=Path(__file__).resolve().parent)
    ap.add_argument('--output-dir',type=Path,required=True)
    args=ap.parse_args();root=args.input_root.resolve();out=args.output_dir.absolute()
    require(not os.path.lexists(out),'New controls output directory required')
    out.mkdir()
    tree=out/'isolated';tree.mkdir()
    original=json.loads((root/MANIFEST).read_text())
    names=original['export_allowlist']+[CHECKER]
    for name in names:shutil.copyfile(root/name,tree/name)
    require(sorted(p.name for p in tree.iterdir())==sorted(names),'Isolated exact public tree')
    before={name:record(tree/name) for name in names}
    def run(target):
        return subprocess.run([sys.executable,'-O',str(tree/CHECKER),'--output-dir',str(target)],capture_output=True,text=True)
    good=out/'isolated-replay';proc=run(good)
    require(proc.returncode==0,proc.stderr)
    isolated_report=json.loads((good/'report.json').read_text())
    require(isolated_report['status']=='PASS' and isolated_report['all_subset_pairs_checked']==272 and isolated_report['optional_original_bindings']=={},'Public-only replay scope')
    mutations=[]
    for name in [MANIFEST,'phase109_cover_families_generalization_theorem.md',
                 'phase109_cover_families_generalization_check.py',
                 'phase109_cover_families_generalization_model.json',
                 'phase109_cover_families_generalization_certificate.json']:
        original_bytes=(tree/name).read_bytes()
        (tree/name).write_bytes(original_bytes+b'\n')
        target=out/('reject-'+name.split('_')[-1].split('.')[0])
        p=run(target)
        require(p.returncode!=0 and not os.path.lexists(target) and 'Frozen' in p.stderr,'Mutated frozen input accepted: '+name)
        mutations.append(dict(file=name,rejected=True,no_output=True))
        (tree/name).write_bytes(original_bytes)
    frozen_output=record(good/'report.json')
    file=out/'occupied-file';file.write_text('preserve\n')
    dangling=out/'dangling-link';dangling.symlink_to(out/'nonexistent-target')
    controls=[]
    for kind,target in [('directory',good),('file',file),('dangling_symlink',dangling)]:
        p=run(target)
        require(p.returncode!=0 and 'Fresh independent output required' in p.stderr,'Occupied output accepted')
        controls.append(kind)
    require(record(good/'report.json')==frozen_output and file.read_text()=='preserve\n' and dangling.is_symlink(),'Occupied object changed')
    require({name:record(tree/name) for name in names}==before,'Isolated inputs changed')
    report=dict(status='PASS',date='2026-10-10',controls_program=record(Path(__file__)),
                optimized_python=True,isolated_input_files=before,
                isolated_replay_report=record(good/'report.json'),
                isolated_replay_seconds=isolated_report['seconds'],
                isolated_default_private_bindings_count=0,all_subset_pairs_checked=272,
                mutations=mutations,no_clobber=controls,inputs_and_existing_output_preserved=True,
                original_tree_changed=False,scope='Integrity/interface tests plus a fresh full independent arithmetic replay using only nine exact public author exports and this checker')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',isolated_seconds=report['isolated_replay_seconds'],mutations=len(mutations),no_clobber=len(controls)),indent=2))
if __name__=='__main__':main()
