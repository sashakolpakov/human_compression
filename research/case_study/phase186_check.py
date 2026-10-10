#!/usr/bin/env python3
"""Fresh replay of the Witt incidence/group calculations and Lean maps."""
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

ROOT = Path(__file__).resolve().parent
FILES = ['phase186_witt_derived_check.g','phase186_witt_validate.py',
         'phase186_witt_lean_generate.py','formal/WittDerivedPlanes.lean',
         'formal/DeletedLineFourResidue.lean','formal/CyclicBiplaneDelta.lean',
         'phase186_hermitian_labels.g','phase186_check.py']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--gap',default=shutil.which('gap') or '/opt/homebrew/bin/gap')
    parser.add_argument('--lean',default='/Users/sasha/.elan/bin/lean')
    parser.add_argument('--packages',type=Path,default=Path('/Users/sasha/bogachev/formal/.lake/packages'))
    args = parser.parse_args()
    if args.out.exists():
        parser.error('fresh output directory required')
    out = args.out.resolve()
    out.mkdir(parents=True)
    for name in FILES:
        dest = out / name
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/name,dest)
    if sha(out/'formal/DeletedLineFourResidue.lean') != '5327b4999903dc4236b7520f204fc0c21468b07b0b79bf30df0540599955afdb':
        raise RuntimeError('frozen F4 dependency changed')
    start = time.monotonic()
    witness = out/'phase186_witt_witness.json'
    driver = out/'driver.g'
    driver.write_text('P186_OUTPUT:='+json.dumps(str(witness))+';;\nRead("phase186_witt_derived_check.g");\n')
    result = subprocess.run([args.gap,'-q','-b',str(driver)],cwd=out,text=True,
                            stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
    (out/'phase186_gap.log').write_text(result.stdout)
    if result.returncode or 'P186_WITT_DERIVED_AND_FULL_AUT_PASS' not in result.stdout or 'Error,' in result.stdout:
        raise RuntimeError('GAP check failed')
    result = subprocess.run([args.gap,'-q','-b','phase186_hermitian_labels.g'],cwd=out,text=True,
                            stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
    (out/'phase186_hermitian_labels.log').write_text(result.stdout)
    if result.returncode or 'P186_HERMITIAN_LABELS_PASS' not in result.stdout or 'Error,' in result.stdout:
        raise RuntimeError('Hermitian root-coset check failed')
    subprocess.run([sys.executable,'phase186_witt_validate.py',str(witness),'--output',str(out/'phase186_validation.json')],
                   cwd=out,check=True,stdout=subprocess.DEVNULL,timeout=60)
    generated = out/'Generated.lean'
    subprocess.run([sys.executable,'phase186_witt_lean_generate.py',str(witness),str(generated)],cwd=out,check=True)
    if generated.read_bytes() != (out/'formal/WittDerivedPlanes.lean').read_bytes():
        raise RuntimeError('generated Lean source differs from reviewed source')
    env = os.environ.copy()
    env['ELAN_TOOLCHAIN']='leanprover/lean4:v4.32.2'
    env['LEAN_PATH']=':'.join([str(out)]+[str(args.packages/p/'.lake/build/lib/lean') for p in
       ['mathlib','plausible','proofwidgets','batteries','aesop','importGraph','LeanSearchClient','Qq']])
    revision = subprocess.run(['git','-C',str(args.packages/'mathlib'),'rev-parse','HEAD'],
                              capture_output=True,text=True,check=True).stdout.strip()
    if revision != '905b95818eb32af7874a58b427f50c1711a5e96c':
        raise RuntimeError('unexpected mathlib revision')
    for module, reports in [('DeletedLineFourResidue',7),('WittDerivedPlanes',9),('CyclicBiplaneDelta',6)]:
        source = out/'formal'/(module+'.lean')
        if re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s',source.read_text(),re.M):
            raise RuntimeError('untrusted proof source')
        r = subprocess.run([args.lean,'-o',str(out/(module+'.olean')),str(source)],cwd=out,env=env,text=True,
                           stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (out/(module+'.log')).write_text(r.stdout)
        if r.returncode or 'sorryAx' in r.stdout or r.stdout.count('depends on axioms:') != reports:
            raise RuntimeError('Lean check failed: '+module)
    original = (out/'formal/WittDerivedPlanes.lean').read_text()
    controls=[]
    biplane = (out/'formal/CyclicBiplaneDelta.lean').read_text()
    for label,source_text,old,new in [
        ('wrong_coordinate_incidence',original,'(coordinate l 2) = 0','(coordinate l 2) = one4'),
        ('swapped_point_images',original,'def pointMap22 : Fin 21 → Fin 21 :=\n  ![0, 1,','def pointMap22 : Fin 21 → Fin 21 :=\n  ![1, 0,'),
        ('alter_biplane_difference_set',biplane,'{1, 3, 4, 5, 9}','{1, 3, 4, 5, 8}'),
        ('replace_singleton_by_pair',biplane,'incident x a ∧ incident x b ↔ x = p','incident x a ∧ incident x b ↔ x = p ∨ x = p + 1')]:
        if source_text.count(old) != 1:
            raise RuntimeError('mutation site not unique')
        mutant=out/(label+'.lean');mutant.write_text(source_text.replace(old,new,1))
        r=subprocess.run([args.lean,str(mutant)],cwd=out,env=env,text=True,
                         stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        log=out/(label+'.log');log.write_text(r.stdout)
        if r.returncode==0 or 'error:' not in r.stdout:
            raise RuntimeError('semantic Lean mutation accepted')
        controls.append({'control':label,'status':'REJECTED','log_sha256':sha(log)})
    report={'status':'PASS','seconds':round(time.monotonic()-start,3),
            'inputs':{name:sha(out/name) for name in FILES},'mathlib_revision':revision,
            'finite_cases':5,'derived_coordinate_isomorphisms':3,'new_Lean_axiom_reports':15,
            'Hermitian_root_coset_parameters':[3,4,5,7,8,9,11,13,16],
            'biplane_delta_counterexample':'both Delta graphs connected; literal flag residue disconnected',
            'retained_dependency_axiom_reports':7,'Lean_negative_controls':controls,
            'artifact_hashes':{name:sha(out/name) for name in ['phase186_witt_witness.json','phase186_gap.log',
              'phase186_validation.json','DeletedLineFourResidue.log','WittDerivedPlanes.log','CyclicBiplaneDelta.log','phase186_hermitian_labels.log']},
            'scope':'Written uniform theory remains separate. GAP checks actual finite designs, full groups and stabilizer structures. Python independently checks incidence arithmetic. Lean checks the three explicit finite derived incidence maps and the literal cyclic-biplane Delta counterexample. Derivation from original Witt block systems, finite-group completeness and the uniform classification remain outside Lean.'}
    (out/'phase186_build.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','seconds':report['seconds'],'out':str(out)}))


if __name__ == '__main__':
    main()
