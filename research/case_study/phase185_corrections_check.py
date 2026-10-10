#!/usr/bin/env python3
"""Replay the scoped L092 corrections without requiring primary publications.

Written uniform proofs and their primary-source identifications are reviewed
mathematics; this driver checks the finite cases and the literal F4 Lean graph.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time


def require(ok, msg):
    if not ok:
        raise RuntimeError(msg)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(cmd, cwd, logfile, env=None):
    start = time.monotonic()
    result = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=600)
    logfile.write_text(result.stdout + result.stderr)
    return result, time.monotonic()-start


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-dir', type=Path, required=True)
    ap.add_argument('--packages', type=Path, required=True)
    ap.add_argument('--lean', default='lean')
    ap.add_argument('--gap', default='gap')
    args = ap.parse_args()
    root = Path(__file__).resolve().parent
    out = args.output_dir.absolute()
    require(not out.exists() and not out.is_symlink(), 'fresh output directory required')
    out.mkdir(parents=True)
    names = ['phase182_inversive_geometry_check.py', 'phase182_inversive_residues.md',
             'phase182_deleted_line_check.py', 'phase182_deleted_line_independent_theorem.md',
             'phase182_deleted_line_lean_bridge.md', 'phase183_review.py',
             'phase183_inversive_review.g', 'formal/DeletedLineFourResidue.lean',
             'formal/dependency_manifest.json', 'phase185_corrections_check.py']
    bound = {name:sha(root/name) for name in names}
    allstart = time.monotonic()
    py = [sys.executable, '-B', '-O']
    r, deleted_time = run(py+[str(root/'phase182_deleted_line_check.py'),
                   '--output', str(out/'deleted_line.json')], root, out/'deleted_line.log')
    require(r.returncode == 0, 'literal deleted-line checker failed')
    deleted = json.loads((out/'deleted_line.json').read_text())
    require(deleted['status']=='PASS', 'deleted-line status failed')
    r, inversive_time = run(py+[str(root/'phase183_review.py'), '--output-dir',
                         str(out/'inversive'), '--gap', args.gap], root, out/'inversive.log')
    require(r.returncode == 0 and 'PHASE183_INDEPENDENT_REVIEW_PASS' in r.stdout,
            'independent inversive replay failed')
    inv = json.loads((out/'inversive/review.json').read_text())

    deps = json.loads((root/'formal/dependency_manifest.json').read_text())
    packages = args.packages.resolve()
    checked_deps = []
    for p in deps['packages']:
        directory = packages/p['name']
        rev = subprocess.run(['git','-C',str(directory),'rev-parse','HEAD'],
                             capture_output=True,text=True,check=True).stdout.strip()
        status = subprocess.run(['git','-C',str(directory),'status','--porcelain',
                                 '--untracked-files=no'],capture_output=True,text=True,check=True).stdout
        require(rev==p['rev'] and not status, 'dependency revision/cleanliness mismatch: '+p['name'])
        lib = directory/'.lake/build/lib/lean'
        checked_deps.append({'name':p['name'], 'revision':rev, 'tracked_files_clean':True,
                             'compiled_library_present':lib.is_dir()})
    env = os.environ.copy()
    env['ELAN_TOOLCHAIN'] = deps['lean']
    env['LEAN_PATH'] = os.pathsep.join(str(packages/p['name']/'.lake/build/lib/lean')
                       for p in deps['packages'] if (packages/p['name']/'.lake/build/lib/lean').is_dir())
    version = subprocess.run([args.lean,'--version'],env=env,capture_output=True,text=True,check=True).stdout.strip()
    require('version 4.32.2,' in version, 'unexpected Lean compiler')
    formal = out/'formal'; formal.mkdir()
    src = root/'formal/DeletedLineFourResidue.lean'
    copy = formal/src.name; shutil.copyfile(src,copy)
    result, lean_time = run([args.lean,'-o',str(formal/'DeletedLineFourResidue.olean'),str(copy)],
                           out, out/'lean.log',env)
    reports = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",result.stdout,re.S)
    expected = ['field_table_laws','nonzero_bijection','incidence_formula',
                'reachable_preserves_component','not_connected','three_hexagons_adjacency','vertex_count']
    require(result.returncode==0 and [name.split('.')[-1] for name,_ in reports]==expected,
            'Lean declarations did not all compile')
    require(all(set(x.strip() for x in ax.split(',') if x.strip()) <=
                {'propext','Classical.choice','Quot.sound'} for _,ax in reports),
            'unexpected Lean axiom')
    require(not re.search(r'\b(sorry|admit|native_decide|axiom)\b',src.read_text()),
            'unexpected source trust primitive')
    check = {'source':src.name,'sha256':sha(src),'exit_code':result.returncode,
             'elapsed_seconds':lean_time,'stdout':result.stdout,'stderr':result.stderr,
             'lean':version,'dependency_manifest':'dependency_manifest.json',
             'dependency_manifest_sha256':sha(root/'formal/dependency_manifest.json'),
             'dependencies':checked_deps,'verification':'fresh compiler run',
             'dependency_scope':'Recorded git HEADs and tracked-file cleanliness checked; compiled dependencies are trusted build inputs.'}
    (out/'DeletedLineFourResidue.check.json').write_text(json.dumps(check,indent=2)+'\n')
    mutations = [('dropped_flag_center','nonzero point.2 + nonzero flag.2','nonzero point.2'),
                 ('wrong_cycle_modulus','(i.val + 1) % 6 = j.val','(i.val + 1) % 5 = j.val')]
    controls = []
    for name,old,new in mutations:
        require(src.read_text().count(old)==1, 'nonunique semantic mutation')
        mutant = formal/(name+'.lean')
        mutant.write_text(src.read_text().replace(old,new,1))
        failed,seconds = run([args.lean,str(mutant)],out,out/(name+'.log'),env)
        require(failed.returncode!=0 and 'error:' in failed.stdout+failed.stderr,
                'semantic change accepted: '+name)
        controls.append({'name':name,'rejected':True,'seconds':seconds,
                         'log_sha256':sha(out/(name+'.log'))})
    require(bound=={name:sha(root/name) for name in names}, 'input changed during replay')
    report = {'status':'PASS','input_sha256':bound,'seconds':time.monotonic()-allstart,
              'timings':{'deleted_line':deleted_time,'independent_inversive':inversive_time,'lean':lean_time},
              'finite_deleted_line_parameters':[4,8],
              'independent_inversive_certificate_sha256':inv['certificate_sha256'],
              'inversive_negative_controls':inv['negative_controls'],
              'lean_axiom_reports':len(reports),'lean_semantic_controls':controls,
              'source_publication_required_for_replay':False,
              'uniform_proofs_formalized':False,
              'new_whole_source_credit':0,'new_open_conjecture_solution':False}
    (out/'replay.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','seconds':report['seconds'],'out':str(out)}))


if __name__=='__main__':
    main()
