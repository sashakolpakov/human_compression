#!/usr/bin/env python3
"""Bounded independent F008 review replay; finite diagnostics do not prove asymptotics."""
import argparse
import copy
from decimal import Decimal, getcontext
from fractions import Fraction as F
import hashlib
import itertools
import json
import math
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

AUTHOR_PIN = '3c218b6f2a58276ca7566b7f94a0b687d7e3e486f4841532e420743080d3fb22'
HERE = Path(__file__).resolve().parent

def require(v, message):
    if not v:
        raise ValueError(message)

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def load(p):
    return json.loads(Path(p).read_text())

def binding(root, record):
    p = root / record['path']
    require(p.stat().st_size == record['bytes'], 'binding bytes: '+record['path'])
    require(sha(p) == record['sha256'], 'binding hash: '+record['path'])

def semantic(scope, routes, dependencies):
    require(scope['principal_pending'] == ['Theorem 1.3 strong three-dimensional density'], 'pending 3D')
    for key in ['new_original_credit', 'new_question_credit', 'new_Lean']:
        require(scope[key] == 0, key)
    require(scope['compression_ratio'] is None, 'no factor')
    require(len(routes['routes']) == 19, '19 source routes')
    rr = {r['source']: r['disposition'] for r in routes['routes']}
    require(rr['Conjecture 1.1'].startswith('Open;'), 'open conjecture')
    require(rr['Theorem 1.3'].startswith('Pending:'), 'pending theorem')
    require('outside scope' in rr['Remark 4(i)'], 'multiplicative scope')
    require('not established' in rr['Remark 4(ii)'], 'error scope')
    require(any(r['name'] == 'Hardy–Ramanujan normal order' for r in dependencies['required_classical_inputs']), 'retained normal order')

def diagnostic():
    getcontext().prec = 65
    D = Decimal
    mixed = 0
    for a in range(2, 5):
        for vals in itertools.product(range(5), repeat=a):
            for j in range(2, 8):
                w = sum(vals)**j - sum(v**j for v in vals)
                majorant = a**j * sum(vals[i]**(j-1)*vals[h] for i in range(a) for h in range(a) if i != h)
                require(0 <= w <= majorant, 'mixed monomial bound')
                mixed += 1
    gaps = 0
    smallest = None
    for a in range(2, 10):
        for t in map(D, ['0.01','0.1','0.25','0.5','0.9','1','2','3.75','8']):
            for j in [2,3,4,8,16,64]:
                if j < t:
                    continue
                at = (D(a).ln()*t).exp()
                half = (D(a).ln()*t/2).exp()
                aj = (D(a).ln()*t/j).exp()
                y = t/(at-1)
                gap = at*y-t+t/j-y*aj
                lower = t/j*(half-1)/(half+1)
                require(gap + D('1e-58') >= lower > 0, 'positive fractional gap')
                smallest = min(smallest or gap, gap)
                gaps += 1
    # Exact source counterexample, all exponents integral: a=3,t=j=2,y=1/4.
    gap = F(9,4)-2+1-F(3,4)
    require(gap == F(1,2) and gap < F(2,2), 'false source gap witness')
    # The exponents from the second Holder step, evaluated as rational identities.
    exponents = 0
    for j in range(2, 20):
        for t in [F(1,10),F(1,2),F(1),F(3,2)]:
            for z in [F(1,7), F(1), F(19,3)]:
                alpha=z-t+t/j
                require(1-t/j+z/(j-1) == 1+alpha/(j-1), 'Holder s exponent')
                exponents += 1
    # Exact threshold interpolation and squarefree-to-powerful decomposition.
    thresholds = 0
    for a in range(2, 8):
        for T in range(1, 8):
            y = F(T,a**T-1)
            require(a**T*y-T-1 == y-1, 'threshold exponent')
            thresholds += 1
    decompositions = 0
    for n in range(1, 1001):
        m=n; u=v=1; p=2
        while p*p<=m:
            e=0
            while m%p==0:
                e+=1; m//=p
            if e==1: u*=p
            elif e>=2: v*=p**e
            p+=1
        if m>1: u*=m
        require(u*v==n and math.gcd(u,v)==1, 'powerful decomposition')
        decompositions += 1
    values=[2,3,4,6,8,9]
    modulus=math.lcm(*values)
    complements=[]
    for mask in range(1<<len(values)):
        selected=[v for i,v in enumerate(values) if mask>>i&1]
        complements.append({x for x in range(1,modulus+1) if all(x%v for v in selected)})
    behrend=strict=0
    for A in complements:
        for B in complements:
            left=len(A&B)*modulus; right=len(A)*len(B)
            require(left>=right, 'finite Behrend')
            strict += left>right
            behrend+=1
    # Coefficients of P(z)P(z^-1), independently formed from exponent pairs.
    fourier={d:0 for d in range(-3,4)}
    for i in range(4):
        for j in range(4): fourier[i-j]+=1
    require(fourier=={-3:1,-2:2,-1:3,0:4,1:3,2:2,3:1}, 'Fourier convolution')
    z=1j
    require(sum(z**j for j in range(4))==0 and 16*F(1,2)**3==2, 'Fourier source witness')
    margin=D('1.8')+D('.75')-D('1.01')*D(4).ln()-D('1.1')
    require(margin>0, 'planar exponent margin')
    require(D('1.6')+D('.75')-D('1.01')*D(4).ln()-D('1.1')<0, 'weakened margin discriminates')
    eta=D('1.01')*D('1.005').ln()-D('.005')
    require(eta>0, 'exceptional-tail positive exponent')
    return {'mixed_monomial_cases':mixed,'fractional_gap_samples':gaps,
            'smallest_sampled_gap':str(smallest),'rational_exponent_identities':exponents,
            'threshold_identities':thresholds,'powerful_decompositions':decompositions,
            'finite_Behrend_pairs':behrend,'strict_Behrend_pairs':strict,
            'planar_margin_above_11_over_10':str(margin),'tail_eta_example':str(eta),
            'source_gap_counterexample':'1/2 < 1 at a=3,t=j=2,y=1/4',
            'source_Fourier_counterexample':'u=pi/2: actual 0, printed 2',
            'proof_role':'Optional discriminating checks only. Uniform analytic assertions are accepted by written proof review.'}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--author-dir',type=Path,required=True)
    p.add_argument('--study-root',type=Path)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--render',action='store_true')
    p.add_argument('--pdflatex',default='/opt/homebrew/bin/pdflatex')
    a=p.parse_args(); started=time.monotonic(); a.out.mkdir(parents=True,exist_ok=True)
    require(sha(a.author_dir/'manifest.json')==AUTHOR_PIN,'author manifest')
    manifest=load(a.author_dir/'manifest.json')
    for r in manifest['exports']: binding(a.author_dir,r)
    if (HERE/'manifest.json').exists():
        for r in load(HERE/'manifest.json')['exports']: binding(HERE,r)
    deps=load(a.author_dir/'dependencies.json'); scope=load(a.author_dir/'scope.json'); routes=load(a.author_dir/'source_map.json')
    semantic(scope,routes,deps)
    primary=0
    if a.study_root:
        for key in ['primary','auxiliary']:
            binding(a.study_root,deps[key]); primary+=1
    checks=[]
    for key in ['new_original_credit','new_question_credit','new_Lean','compression_ratio']:
        bad=copy.deepcopy(scope); bad[key]=1
        try: semantic(bad,routes,deps)
        except ValueError: checks.append(key)
        else: raise ValueError('scope control accepted')
    bad=copy.deepcopy(scope); bad['principal_pending']=[]
    try: semantic(bad,routes,deps)
    except ValueError: checks.append('remove unresolved 3D theorem')
    else: raise ValueError('pending mutation accepted')
    for target in ['Conjecture 1.1','Theorem 1.3','Remark 4(i)','Remark 4(ii)']:
        bad=copy.deepcopy(routes)
        for row in bad['routes']:
            if row['source']==target: row['disposition']='Fully solved'
        try: semantic(scope,bad,deps)
        except ValueError: checks.append(target)
        else: raise ValueError('source scope control accepted')
    bad=copy.deepcopy(deps); bad['required_classical_inputs']=[r for r in bad['required_classical_inputs'] if r['name']!='Hardy–Ramanujan normal order']
    try: semantic(scope,routes,bad)
    except ValueError: checks.append('remove retained normal order')
    else: raise ValueError('dependency control accepted')
    with tempfile.TemporaryDirectory(prefix='F008_binding_control_') as td:
        td=Path(td); row=manifest['exports'][1]; (td/row['path']).write_bytes((a.author_dir/row['path']).read_bytes()+b'\n')
        try: binding(td,row)
        except ValueError: checks.append('corrupt written proof')
        else: raise ValueError('binding control accepted')
    evidence=diagnostic()
    rendered={}
    if a.render:
        from pypdf import PdfReader
        expected=load(a.author_dir/'author_checks.json')
        d=a.out/'render'; d.mkdir(exist_ok=True)
        for stem in ['weighted_divisors','mondrian_density']:
            shutil.copy2(a.author_dir/(stem+'.tex'),d/(stem+'.tex'))
            for run in [1,2]:
                r=subprocess.run([a.pdflatex,'-halt-on-error','-interaction=nonstopmode',stem+'.tex'],cwd=d,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=30)
                (d/(stem+f'.run{run}.txt')).write_bytes(r.stdout)
                require(r.returncode==0,'TeX render')
            log=(d/(stem+'.log')).read_text()
            require(not any(x in log for x in ['Overfull','Underfull','LaTeX Warning:','undefined references']),'clean presentation')
            hh=[hashlib.sha256((pg.extract_text() or '').encode()).hexdigest() for pg in PdfReader(d/(stem+'.pdf')).pages]
            require(hh==expected[stem]['page_text_sha256'],'exact rebuilt page texts')
            rendered[stem]=len(hh)
    report={'status':'PASS','author_manifest':AUTHOR_PIN,'author_exports':len(manifest['exports']),
            'source_routes':len(routes['routes']),'private_source_bindings':primary,
            'rejected_controls':checks,'diagnostics':evidence,'rendered_pages':rendered,
            'elapsed_seconds':time.monotonic()-started}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','controls':len(checks),'source_routes':19,'pages':rendered}))

if __name__=='__main__': main()
