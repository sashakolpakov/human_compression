#!/usr/bin/env python3
"""Compile the seven scoped projective components from source in a fresh directory.

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

def countermodels():
    # A common invariant line makes the commutator singular.
    A=((1,1),(0,1)); B=((2,0),(0,1))
    mul=lambda X,Y:tuple(tuple(sum(X[i][k]*Y[k][j] for k in range(2)) for j in range(2)) for i in range(2))
    X=tuple(tuple(mul(A,B)[i][j]-mul(B,A)[i][j] for j in range(2)) for i in range(2))
    need(X!=((0,0),(0,0)) and X[0][0]*X[1][1]-X[0][1]*X[1][0]==0,'irreducibility countermodel')
    # Over F5, U=1,V=2 has zero squared norm. A nonzero solution of
    # both homogeneous linear coordinates destroys inverse uniqueness.
    need((1+4)%5==0 and (2*1-1*2)%5==0 and (1*1+2*2)%5==0,'denominator countermodel')
    # Trace-square equation alone does not supply a square root.
    need(2 not in {x*x%5 for x in range(5)},'square-existence countermodel')
    return [{'omitted':'absolute irreducibility','A':A,'B':B,'nonzero_singular_commutator':X},
      {'omitted':'nonzero U^2+V^2','field':5,'U':1,'V':2,'two_equal_coordinate_images':[[0,0],[1,2]]},
      {'omitted':'discriminant is a square','field':5,'discriminant':2}]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--source-dir',type=Path,default=ROOT)
    parser.add_argument('--lean',type=Path,default=Path('/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean'))
    parser.add_argument('--packages',type=Path,default=Path('/Users/sasha/bogachev/formal/.lake/packages'))
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
    def ensure_external(name):
        relative=Path(*name.split('.'));target=out/'dependency_lib'/relative.with_suffix('.olean')
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
        need(proc.returncode==0 and not re.search(r'error(?:\([^)]*\))?:|sorryAx',proc.stdout+proc.stderr),'Local compilation failed: '+source.name)
        warnings=[line for line in (proc.stdout+proc.stderr).splitlines() if re.search(r'warning(?:\([^)]*\))?:',line)]
        need(warnings==row['allowed_warning_lines'],'Unexpected diagnostic: '+source.name)
        raw=re.findall(r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",proc.stdout)
        need([name for name,_ in raw]==row['declarations'],'Wrong declaration inventory')
        axioms=[{'name':name,'axioms':re.findall(r'[\w.]+',value)} for name,value in raw]
        need(all(set(a['axioms'])<={'propext','Classical.choice','Quot.sound'} for a in axioms),'Unapproved axiom')
        reports.append({'source':row,'warnings':warnings,'seconds':round(time.monotonic()-started,3),'axioms':axioms,'object_sha256':sha(target),'log_sha256':sha(out/'logs'/(source.stem+'.txt'))})
    # These actual Lean compilation controls falsify one algebraic conclusion
    # at a time. They use the same pinned imports and cannot pass by a status label.
    source_text=(args.source_dir/'ProjectiveTraceExtension.lean').read_text()
    mutations=[
      ('wrong_commutator_scalar',"= -(comm A B).det •", "= (comm A B).det •"),
      ('wrong_linear_sign',"second U V b c z = -b * c := by", "second U V b c z = b * c := by"),
      ('wrong_inverse_coordinate',"second U V b c (U * R + V * S) = S := by", "second U V b c (U * R + V * S) = -S := by")]
    negative=[]
    for name,before,after in mutations:
        need(source_text.count(before)==1,'Mutation target: '+name)
        text=source_text.replace(before,after)
        source=out/'src'/(name+'.lean');source.write_text(text)
        proc=subprocess.run([args.lean,source.name],cwd=out/'src',env=env,capture_output=True,text=True,timeout=180)
        log=out/'logs'/(name+'.txt');log.write_text(proc.stdout+proc.stderr)
        need(proc.returncode!=0 and 'error:' in proc.stdout+proc.stderr,'False algebra accepted: '+name)
        negative.append({'name':name,'rejected':True,'source_sha256':sha(source),'log_sha256':sha(log)})
    result={'status':'PASS','lean_version':version,'dependencies':dependencies,'modules':reports,'rebuilt_external':rebuilt,'negative_compilation_controls':negative,'countermodels':countermodels(),'formal_scope':scope['formal_scope'],'not_formalized':scope['not_formalized'],'trust':'Fresh local sources and absent pinned dependencies compiled; remaining pinned package objects trusted. No full mathlib rebuild.','ratio':None,'source_credit_increment':0,'question_credit_increment':0}
    (out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','declarations':sum(len(x['axioms']) for x in reports),'countermodels':len(result['countermodels']),'report':str(out/'report.json')}))

if __name__=='__main__':main()
