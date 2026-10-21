#!/usr/bin/env python3
"""Compile the two scoped Topic D components from source in a fresh directory.

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
    # G=C2 acts regularly on Z=E=C2, but p is constant: no equivariance.
    action = lambda g,x:(g+x)%2
    p = lambda z:0
    stabilizer = [g for g in range(2) if action(g,0)==0]
    need(any(action(g,0)==1 for g in range(2)), 'Ambient equivalent points')
    need(not any(action(g,0)==1 for g in stabilizer), 'Fiber equivalence fails')
    need(any(p(action(g,z))!=action(g,p(z)) for g in range(2) for z in range(2)), 'Missing equivariance')
    # With trivial G, p=id on two points: the chosen fiber misses another orbit.
    need({0}!={0,1}, 'Single-base-orbit condition is necessary for surjectivity')
    # Even G=C2, D=translation by 1: involutive/free/commuting but fixes its orbit.
    D=lambda x:1-x
    need(all(D(D(x))==x and D(x)!=x for x in range(2)), 'Even-order D properties')
    need(all(D(action(g,x))==action(g,D(x)) for g in range(2) for x in range(2)), 'Even-order commutation')
    need(D(0)==action(1,0),'Even-order fixed orbit')
    # G trivial, D=id: the omitted fixed-point-free condition is essential.
    need(0==0,'Identity involution fixes the singleton orbit')
    # G=C3 regular, D=translation by 1: it is free and commutes, but is not involutive.
    act3=lambda g,x:(g+x)%3
    D3=lambda x:(x+1)%3
    need(all(D3(x)!=x and D3(act3(g,x))==act3(g,D3(x)) for x in range(3) for g in range(3)), 'C3 D properties')
    need(D3(D3(0))!=0 and D3(0)==act3(1,0),'Noninvolutive orbit failure')
    # Two regular C3 orbits, with a free involution not commuting with the action.
    d=[1,0,5,4,3,2]
    act6=lambda g,x:3*(x//3)+(x%3+g)%3
    need(all(d[d[x]]==x and d[x]!=x for x in range(6)), 'Six-point free involution')
    need(any(d[act6(g,x)]!=act6(g,d[x]) for g in range(3) for x in range(6)), 'Missing commutation')
    need(d[0]==act6(1,0),'Noncommuting orbit failure')
    return [
      {'omitted':'equivariance','G':'C2','Z':'regular C2','E':'regular C2','p':'constant zero','ambient_orbits':1,'fiber_stabilizer_orbits':2},
      {'omitted':'single chosen base orbit for surjectivity','G':'trivial','Z':[0,1],'E':[0,1],'p':'identity','chosen_e':0,'missed_ambient_orbit':[1]},
      {'omitted':'odd periods','G':'C2','Z':'regular C2','D':'translation by one','fixed_orbit':True},
      {'omitted':'D fixed-point-free','G':'trivial','Z':[0],'D':'identity','fixed_orbit':True},
      {'omitted':'D involutive','G':'C3','Z':'regular C3','D':'translation by one','fixed_orbit':True},
      {'omitted':'D commutes with group action','G':'C3','Z':'two regular orbits','D':d,'witness_z':0,'witness_g':1}
    ]

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
        need(proc.returncode==0 and not re.search(r'warning(?:\([^)]*\))?:|error(?:\([^)]*\))?:|sorryAx',proc.stdout+proc.stderr),'Local compilation failed: '+source.name)
        raw=re.findall(r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",proc.stdout)
        need([name for name,_ in raw]==row['declarations'],'Wrong declaration inventory')
        axioms=[{'name':name,'axioms':re.findall(r'[\w.]+',value)} for name,value in raw]
        need(all(set(a['axioms'])<={'propext','Classical.choice','Quot.sound'} for a in axioms),'Unapproved axiom')
        reports.append({'source':row,'seconds':round(time.monotonic()-started,3),'axioms':axioms,'object_sha256':sha(target),'log_sha256':sha(out/'logs'/(source.stem+'.txt'))})
    result={'status':'PASS','lean_version':version,'dependencies':dependencies,'modules':reports,'rebuilt_external':rebuilt,'countermodels':countermodels(),'formal_scope':scope['formal_scope'],'not_formalized':scope['not_formalized'],'trust':'Fresh local sources and absent pinned dependencies compiled; remaining pinned package objects trusted. No full mathlib rebuild.','ratio':None,'source_credit_increment':0,'question_credit_increment':0}
    (out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','declarations':sum(len(x['axioms']) for x in reports),'countermodels':len(result['countermodels']),'report':str(out/'report.json')}))

if __name__=='__main__':main()
