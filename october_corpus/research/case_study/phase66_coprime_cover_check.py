#!/usr/bin/env python3
"""Fresh-output integer model and GAP source-binding checks for phase66."""
from pathlib import Path
import argparse,ast,hashlib,json,re,shutil,subprocess,tempfile,time
root=Path(__file__).resolve().parent
ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--report',type=Path,required=True);ap.add_argument('--log',type=Path,required=True);args=ap.parse_args()
assert not args.report.exists() and not args.log.exists(),'fresh output paths required'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
names=['phase66_coprime_cover_theorem.md','phase66_coprime_cover_ledger.md','phase66_coprime_cover_intake.json','phase66_coprime_cover_check.g','phase66_coprime_cover_coefficients.json','phase66_coprime_cover_permutation_model.json']
before={n:sha(root/n) for n in names}
mf='phase58_2primary_cover_manifest.json';before[mf]=sha(root/mf)
for n,md in json.loads((root/mf).read_text())['files'].items():assert sha(root/n)==md['sha256'];before[n]=md['sha256']
for n,d in json.loads((root/mf).read_text())['source_bindings'].items():assert sha(root/n)==d;before[n]=d
# Independent exact integer verification of the fixed model and literal orbit identity.
model=json.loads((root/names[-1]).read_text());n=model['degree'];ident=tuple(range(n));gs=[tuple(i-1 for i in p) for p in model['generators']]
assert n==128 and all(sorted(p)==list(range(n)) for p in gs)
mul=lambda p,q:tuple(q[p[i]] for i in range(n))
def power(p,k):
    r=ident
    for _ in range(k):r=mul(r,p)
    return r
def inv(p):
    q=[0]*n
    for i,j in enumerate(p):q[j]=i
    return tuple(q)
def group(gens):
    seen={ident};queue=[ident]
    for p in queue:
        for q in gens:
            t=mul(p,q)
            if t not in seen:seen.add(t);queue.append(t)
    return seen
assert all(mul(p,p)==ident for p in gs)
assert all(mul(gs[i],gs[j])==mul(gs[j],gs[i]) for i in range(4) for j in range(i+2,4))
G=group(gs);C=group(gs[1:3]);A=group(gs[:3]);B=group(gs[1:]);assert len(G)==1024 and len(C)==8
assert {p[0] for p in G}==set(range(n)) and all(p[0]==0 for p in C)
a,b,c=[mul(gs[i],gs[i+1]) for i in range(3)]
assert power(a,8)==power(b,4)==power(c,8)==ident
w1=mul(mul(b,power(a,2)),inv(mul(power(a,2),b)))
w2=mul(mul(power(c,2),b),inv(mul(b,power(c,2))))
assert w1==w2 and power(w1,2)==ident and all(mul(w1,p)==mul(p,w1) for p in [a,b,c])
z=mul(mul(mul(inv(power(c,2)),inv(b)),power(c,2)),b)
zword=ident
for j in model['z_word_1based']:zword=mul(zword,gs[j-1])
assert zword==z and z not in C and all(mul(z,p)==mul(p,z) for p in C)
assert A&B==group(list(C)+[z]) and len(A&B)==16
terms=json.loads((root/names[-2]).read_text())['terms'];assert len(terms)==55
embedded=ast.literal_eval((root/'phase66_coprime_cover_check.g').read_text().split('terms:=')[1].split(';;')[0]);assert embedded==terms
def act(v,p):
    result=[0]*n
    for i,j in enumerate(p):result[j]=v[i]
    return result
unit=[0]*n;unit[0]=1
sub=lambda x,y:[a-b for a,b in zip(x,y)]
y=sub(unit,act(unit,gs[3]));y=sub(y,act(y,gs[0]));d=sub(act(unit,z),unit);total=[0]*n
for coef,word in terms:
    assert isinstance(coef,int);v=y
    for j in word:assert 1<=j<=4;v=act(v,gs[j-1])
    total=[a+coef*b for a,b in zip(total,v)]
assert total==[2*a for a in d] and any(d)
# Source reconstruction and exact same certificate on eight cases.
start=time.monotonic()
with tempfile.TemporaryDirectory(prefix='phase66_coprime_') as td:
    p=Path(td)/'check.g';p.write_bytes((root/'phase66_coprime_cover_check.g').read_bytes())
    r=subprocess.run([shutil.which('gap'),'-q',str(p)],cwd=td,text=True,capture_output=True,timeout=1200)
elapsed=time.monotonic()-start
assert r.returncode==0 and not r.stderr.strip(),(r.returncode,r.stderr,r.stdout)
assert not re.search(r'FAIL|Error,|Syntax error',r.stdout),r.stdout
flat=re.sub(r'\s+',' ',r.stdout.replace('\\\n',''))
rows=re.findall(r'INTEGRAL_PASS \[ (\d+), (-?\d+), (-?\d+) \] terms 55 full (\d+) quotient 1024',flat)
params=[(b,e,f) for b in [5,6] for e in [-1,1] for f in [-1,1]]
assert [tuple(map(int,row[:3])) for row in rows]==params,rows
assert all(int(row[3])==256*2**int(row[0]) for row in rows)
assert 'SMITH_PASS 0^7 1^120 2^1' in flat and 'PASS COPRIME_INTEGRAL_CERTIFICATE 8' in flat
for name,digest in before.items():assert sha(root/name)==digest,name
args.log.write_text('PYTHON INTEGER MODEL PASS order1024 degree128 terms55 multiplier2\n'+r.stdout)
report={'date':'2026-10-10','status':'PASS','runner_sha256':sha(Path(__file__)),'seconds_GAP':elapsed,'GAP_version':re.search(r'GAP_VERSION (\S+)',flat).group(1),'inputs_pre_post_sha256':before,'log_sha256':sha(args.log),'literal_integer_certificate':{'terms':55,'multiplier':2,'model_order':1024,'degree':128},'parameter_crosschecks':params,'scope':'Uniform obstruction proved by fixed marked quotient plus exact integral identity; only odd abelian kernels and injective ends. Not global uniqueness, other families, priority or Lean.','frozen_phase58_unchanged':True,'phase58_independent_review_at_intake':'pending'}
args.report.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','seconds_GAP':elapsed,'log_sha256':sha(args.log)},indent=2))
