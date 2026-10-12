#!/usr/bin/env python3
"""Fail-closed orchestration and bounded controls for the complete certificate."""
import argparse
import collections
import copy
import hashlib
import itertools
import json
import subprocess
import sys
from pathlib import Path
import verify_groups
import weights


def need(x,message):
    if not x:
        raise ValueError(message)


def run(cmd, cwd, log, expected=None):
    p=subprocess.run(list(map(str,cmd)),cwd=cwd,text=True,capture_output=True,timeout=120)
    log.write_text(p.stdout+p.stderr)
    need(p.returncode==0 and 'Error,' not in p.stdout+p.stderr,'command failed: '+str(cmd))
    if expected:
        need(expected in p.stdout,'success marker absent')
    return p.stdout


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--gap',default='/opt/homebrew/bin/gap')
    p.add_argument('--cc',default='cc')
    p.add_argument('--render',action='store_true')
    p.add_argument('--pdflatex',default='pdflatex')
    a=p.parse_args();root=Path(__file__).resolve().parent
    if (root/'manifest.json').exists():
        manifest=json.loads((root/'manifest.json').read_text())
        for row in manifest['exports']:
            file=root/row['path']
            need(file.is_file() and len(file.read_bytes())==row['bytes'] and
                 hashlib.sha256(file.read_bytes()).hexdigest()==row['sha256'],
                 'frozen export mismatch: '+row['path'])
    out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
    run([sys.executable,'-B','-O',root/'construct.py','--out',out/'construction'],root,out/'construction.log')
    con=out/'construction'
    run([a.gap,'-q','-b','-T',con/'constructed.g',root/'verify_modules.g'],con,out/'modules.log','LCD120_MODULE_CERTIFICATE_PASS')
    run([a.cc,'-O3',root/'enumerate_ternary.c','-o',out/'enumerate'],root,out/'compile.log')
    for name in ['K','N']:
        s=run([out/'enumerate',con/(name+'_basis.txt')],out,out/(name+'_enumeration.log'))
        (out/(name+'_enumeration.json')).write_text(json.dumps(json.loads(s),indent=2)+'\n')
    run([sys.executable,'-B','-O',root/'weights.py','--K',out/'K_enumeration.json',
         '--N',out/'N_enumeration.json','--out',out/'weights.json'],root,out/'weights.log')
    run([sys.executable,'-B','-O',root/'verify_groups.py','--constructed',con/'constructed.json',
         '--supports',con/'support_data.json','--out',out/'groups.json'],root,out/'groups.log')
    controls=[]
    # The two-bit arithmetic is also checked against literal ternary enumeration.
    for k in [1,2,3,4]:
        n=7
        basis=[[int(j==i) if j<k else (i+2*j+1)%3 for j in range(n)] for i in range(k)]
        f=out/f'small_{k}.txt'
        f.write_text(f'{n} {k}\n'+''.join(''.join(map(str,r))+'\n' for r in basis))
        actual=json.loads(run([out/'enumerate',f],out,out/f'small_{k}.log'))['weight_counts']
        expected=[0]*(n+1)
        for coeff in itertools.product(range(3),repeat=k):
            w=sum(sum(coeff[i]*basis[i][j] for i in range(k))%3 != 0 for j in range(n))
            expected[w]+=1
        need(actual==expected,'independent small enumeration')
        controls.append({'name':f'literal ternary comparison k={k}','status':'PASS'})
    original=(con/'constructed.g').read_text()
    mutations=[('rank-deficient filtration','filtration_basis[1]:=filtration_basis[2];;','filtration basis'),
               ('wrong filtration cut','filtration_cuts[2]:=14;;','filtration dimensions'),
               ('collapsed N','N_basis:=K_basis;;','code ranks'),
               ('changed seed','minimum_seed[1]:=(minimum_seed[1]+1) mod 3;;','minimum seed')]
    for i,(name,edit,interface) in enumerate(mutations):
        f=out/f'mutation_{i}.g';f.write_text(original+'\n'+edit+'\n')
        r=subprocess.run([a.gap,'-q','-b','-T',str(f),str(root/'verify_modules.g')],cwd=out,
                         text=True,capture_output=True,timeout=120)
        (out/f'mutation_{i}.log').write_text(r.stdout+r.stderr)
        need('LCD120_MODULE_CERTIFICATE_PASS' not in r.stdout and interface in r.stdout+r.stderr,
             'module mutation not rejected at intended interface: '+name)
        controls.append({'name':name,'rejected_at':interface})
    constructed=json.loads((con/'constructed.json').read_text());support=json.loads((con/'support_data.json').read_text())
    changed=copy.deepcopy(constructed);changed['full_generators']=[list(range(1,121))]
    changed_support=copy.deepcopy(support);changed_support['coordinate_generators']=changed['full_generators']
    try:
        verify_groups.inspect(changed,changed_support)
    except ValueError as e:
        need('does not attain full upper bound' in str(e),'group mutation wrong failure')
        controls.append({'name':'proper subgroup substituted for full group','rejected_at':str(e)})
    else:
        raise ValueError('proper subgroup accepted')
    changed=copy.deepcopy(json.loads((out/'K_enumeration.json').read_text()))
    changed['weight_counts'][0]+=1
    try:
        weights.derive(changed,15)
    except ValueError as e:
        need('complete enumeration counts' in str(e),'enumeration mutation wrong failure')
        controls.append({'name':'incomplete word count','rejected_at':str(e)})
    else:
        raise ValueError('wrong enumeration count accepted')
    if a.render:
        render=out/'render';render.mkdir()
        for i in range(2):
            run([a.pdflatex,'-interaction=nonstopmode','-halt-on-error','-output-directory='+str(render),root/'modules.tex'],root,out/f'render_{i}.log')
        log=(out/'render_1.log').read_text()
        need(not any(x in log for x in ['Overfull','Missing character','undefined references']),'render diagnostics')
    inputs=['construct.py','steiner_construction.py','module_data.json','verify_modules.g',
            'enumerate_ternary.c','weights.py','verify_groups.py','check.py','modules.tex']
    result={'status':'PASS','scope':'L050120-coordinate N/K assertions only; no whole-source admission',
            'construction':json.loads((con/'construction_report.json').read_text()),
            'modules':json.loads((con/'module_report.json').read_text()),
            'groups':json.loads((out/'groups.json').read_text()),
            'weights':{name:{k:v for k,v in json.loads((out/'weights.json').read_text())[name].items()
                             if not k.startswith('full_')} for name in ['K','N']},
            'controls':controls,'input_sha256':{n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in inputs},
            'rendered':a.render}
    (out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','controls':len(controls),'weights':result['weights']},sort_keys=True))


if __name__=='__main__':
    main()
