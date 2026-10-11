#!/usr/bin/env python3
"""Compile the full exact-support orbit decomposition and Möbius/Burnside component from source in a fresh directory.

Missing pinned mathlib objects are compiled into a private overlay; the supplied
package caches are never modified. No source-specific theorem is inferred from
these compilations. The finite countermodels test omitted hypotheses, not the
quantified conclusions.
"""
import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parent

def need(condition, message):
    if not condition:
        raise RuntimeError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def imports(text):
    # Pinned modules here use ordinary import declarations. Handle nested block comments.
    clean = []
    i = depth = 0
    while i < len(text):
        if text[i:i+2] == '/-':
            depth += 1; i += 2
        elif depth and text[i:i+2] == '-/':
            depth -= 1; i += 2
        elif depth:
            i += 1
        elif text[i:i+2] == '--':
            end = text.find('\n', i)
            i = len(text) if end < 0 else end
        else:
            clean.append(text[i]); i += 1
    return re.findall(r'(?m)^\s*(?:public\s+)?import\s+([\w.]+)', ''.join(clean))

from controls import countermodels

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--source-dir',type=Path,default=ROOT)
    parser.add_argument('--lean',type=Path,required=True)
    parser.add_argument('--packages',type=Path,required=True)
    args=parser.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(),'Use a fresh output directory')
    out=args.out.resolve();out.mkdir()
    for name in ['lib','src','dependency_lib','dependency_src','logs']:(out/name).mkdir()
    scope=json.loads((ROOT/'scope.json').read_text());pins=json.loads((ROOT/'dependency_manifest.json').read_text())
    version=subprocess.check_output([args.lean,'--version'],text=True).strip()
    need('version 4.32.2,' in version,'Wrong Lean version')
    packages=[];libraries=[];dependencies=[]
    for pin in pins['packages']:
        path=args.packages/pin['name'];packages.append(path)
        rev=subprocess.check_output(['git','-C',path,'rev-parse','HEAD'],text=True).strip()
        need(rev==pin['rev'],'Wrong package revision: '+pin['name'])
        need(subprocess.run(['git','-C',path,'diff','--quiet','HEAD','--']).returncode==0,'Modified pinned source: '+pin['name'])
        lib=path/'.lake/build/lib/lean'
        if lib.is_dir():libraries.append(lib)
        dependencies.append({'name':pin['name'],'revision':rev})
    for library in libraries:
        for cached in library.rglob('*'):
            if not cached.is_file():continue
            target=out/'dependency_lib'/cached.relative_to(library)
            need(not target.exists(),'Overlapping cache path')
            target.parent.mkdir(parents=True,exist_ok=True);target.symlink_to(cached.resolve())
    env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join(map(str,[out/'lib',out/'dependency_lib']));env.pop('LEAN_SRC_PATH',None)
    prefix=Path(subprocess.check_output([args.lean,'--print-prefix'],text=True).strip())
    rebuilt=[];building=set()
    local_names={Path(r['file']).stem for r in scope['modules']}
    def ensure_external(name):
        relative=Path(*name.split('.'));target=out/'dependency_lib'/relative.with_suffix('.olean')
        if name in local_names:
            need((out/'lib'/relative.with_suffix('.olean')).is_file(),'Local imports must be compiled in the declared order: '+name)
            return
        if target.is_file() or (prefix/'lib/lean'/relative.with_suffix('.olean')).is_file():return
        need(name not in building,'External import cycle');building.add(name)
        sources=[p/relative.with_suffix('.lean') for p in packages if (p/relative.with_suffix('.lean')).is_file()]
        need(len(sources)==1,'Missing/ambiguous pinned dependency: '+name)
        source=sources[0];raw=source.read_bytes()
        for dep in imports(raw.decode()):ensure_external(dep)
        copied=out/'dependency_src'/relative.with_suffix('.lean');copied.parent.mkdir(parents=True,exist_ok=True);copied.write_bytes(raw)
        target.parent.mkdir(parents=True,exist_ok=True)
        started=time.monotonic();proc=subprocess.run([args.lean,'-o',target,relative.with_suffix('.lean')],cwd=out/'dependency_src',env=env,capture_output=True,text=True,timeout=180)
        (out/'logs'/(name+'.txt')).write_text(proc.stdout+proc.stderr)
        need(proc.returncode==0,'External compilation failed: '+name)
        rebuilt.append({'module':name,'source_sha256':sha(source),'object_sha256':sha(target),'seconds':round(time.monotonic()-started,3)})
        building.remove(name)
    reports=[]
    for row in scope['modules']:
        source=args.source_dir/row['file']
        need(source.stat().st_size==row['bytes'] and sha(source)==row['sha256'],'Changed proof source: '+row['file'])
        text=source.read_text()
        need(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s',text,re.M),'Unapproved mechanism')
        for name in imports(text):ensure_external(name)
        copied=out/'src'/source.name;copied.write_bytes(source.read_bytes());target=out/'lib'/source.with_suffix('.olean').name
        started=time.monotonic();proc=subprocess.run([args.lean,'-o',target,source.name],cwd=out/'src',env=env,capture_output=True,text=True,timeout=180)
        (out/'logs'/(source.stem+'.txt')).write_text(proc.stdout+proc.stderr)
        need(proc.returncode==0 and not re.search(r'warning(?:\([^)]*\))?:|error(?:\([^)]*\))?:|sorryAx',proc.stdout+proc.stderr),'Local compilation failed: '+source.name)
        raw=re.findall(r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",proc.stdout)
        need([name for name,_ in raw]==row['declarations'],'Wrong declaration inventory')
        axioms=[{'name':name,'axioms':re.findall(r'[\w.]+',value)} for name,value in raw]
        need(all(set(a['axioms'])<={'propext','Classical.choice','Quot.sound'} for a in axioms),'Unapproved axiom')
        reports.append({'source':row,'seconds':round(time.monotonic()-started,3),'axioms':axioms,'object_sha256':sha(target),'log_sha256':sha(out/'logs'/(source.stem+'.txt'))})
    source=(args.source_dir/'SupportCounting.lean').read_text()
    mutations=[
      ('zero_mobius', 'IncidenceAlgebra.mu ℚ l ⊤', '(0 : ℚ)'),
      ('omit_exact_support', '(Nat.card {x : X // P x ∧ s x = ⊤} : ℚ)', '(Nat.card {x : X // P x} : ℚ)'),
      ('exact_instead_of_sublevel', '(Nat.card {x : X // P x ∧ s x ≤ l} : ℚ)', '(Nat.card {x : X // P x ∧ s x = l} : ℚ)'),
      ('omit_burnside_denominator', ' / (Nat.card G : ℚ)', ' / (1 : ℚ)')]
    rejected=[]
    for name,old,new in mutations:
        need(old in source,'Mutation target present')
        changed=source.replace(old,new,1);file=out/'src'/(name+'.lean');file.write_text(changed)
        proc=subprocess.run([args.lean,file.name],cwd=out/'src',env=env,capture_output=True,text=True,timeout=180)
        (out/'logs'/(name+'.txt')).write_text(proc.stdout+proc.stderr)
        need(proc.returncode!=0 and 'error' in proc.stdout+proc.stderr,'False altered statement must be rejected: '+name)
        rejected.append({'name':name,'source_sha256':sha(file),'log_sha256':sha(out/'logs'/(name+'.txt')),'rejected':True})
    global_source=(args.source_dir/'OrbitFiberDecomposition.lean').read_text()
    global_mutations=[
      ('omit_transversal_separation', '(hseparate : ∀ (i j : I) (g : G), g • representative j = representative i → i = j)', '(hseparate : True)'),
      ('omit_transversal_coverage', '(hcover : ∀ x : X, ∃ (i : I) (g : G), g • p x = representative i)', '(hcover : True)'),
      ('omit_base_equivariance', '(hp : ∀ (g : G) (x : X), p (g • x) = g • p x)', '(hp : True)')]
    for name,old,new in global_mutations:
        need(old in global_source,'Global mutation target present')
        changed=global_source.replace(old,new,1);file=out/'src'/(name+'.lean');file.write_text(changed)
        proc=subprocess.run([args.lean,file.name],cwd=out/'src',env=env,capture_output=True,text=True,timeout=180)
        (out/'logs'/(name+'.txt')).write_text(proc.stdout+proc.stderr)
        need(proc.returncode!=0 and 'error' in proc.stdout+proc.stderr,'Weakened global assumptions must be rejected: '+name)
        rejected.append({'name':name,'source_sha256':sha(file),'log_sha256':sha(out/'logs'/(name+'.txt')),'rejected':True})
    result={'status':'PASS','lean_version':version,'dependencies':dependencies,'modules':reports,'rebuilt_external':rebuilt,'countermodels':countermodels(),'Lean_mutations':rejected,'formal_scope':scope['formal_scope'],'not_formalized':scope['not_formalized'],'trust':'Fresh local sources and absent pinned dependencies compiled; remaining pinned package objects trusted. No full mathlib rebuild.','ratio':None,'source_credit_increment':0,'question_credit_increment':0}
    (out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','declarations':sum(len(x['axioms']) for x in reports),'countermodels':len(result['countermodels']),'Lean_mutations':len(rejected),'report':str(out/'report.json')}))

if __name__=='__main__':main()
