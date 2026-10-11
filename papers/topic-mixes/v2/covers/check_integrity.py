#!/usr/bin/env python3
"""Small rejection controls on exact scientific, program and formal bindings."""
import argparse,importlib.util,json,shutil,tempfile
from pathlib import Path
P=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--study-root',type=Path,default=P.parent);a=ap.parse_args()
    spec=importlib.util.spec_from_file_location('packet_check',P/'check.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    mod.bindings(a.study_root);rejected=[]
    for name,old,new in [('cover_fibers.tex','faithful thin rank-four','thin rank-four'),
      ('base_certificate.g','Size(U)=96','Size(U)=192'),
      ('CoverFibers.lean','(hCB : C ≤ B)','(hCB : C ≤ C)')]:
        with tempfile.TemporaryDirectory()as td:
            q=Path(td);shutil.copytree(P,q/'copy');q=q/'copy'
            s=(q/name).read_text()
            if old not in s:raise RuntimeError('Control anchor '+name)
            (q/name).write_text(s.replace(old,new));mod.P=q
            try:mod.bindings(a.study_root)
            except RuntimeError as e:
                if 'Changed local'not in str(e):raise
                rejected.append(name)
            else:raise RuntimeError('Changed input accepted '+name)
    a.out.write_text(json.dumps({'status':'PASS','rejected_changed_inputs':rejected,
      'scope':'integrity only; mathematical controls are in the complete replay'},indent=2)+'\n')
if __name__=='__main__':main()
