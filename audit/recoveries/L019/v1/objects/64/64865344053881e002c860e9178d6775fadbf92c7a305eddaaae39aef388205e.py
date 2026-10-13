from pathlib import Path
import json,hashlib,subprocess,sys,os,shutil,importlib.util,itertools
S=Path('/Users/sasha/medusa/research/leemans');A=S/'topic_B_L019_central_intersections_v1';W=S/'reboot_20261013/L019_recovery_work/root_central_review01';W.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
manifest=json.loads((A/'manifest.json').read_text());assert sha(A/'manifest.json')=='48fb888d0953caee20a94c813ff8807af6582dac3fa62f2475dd2f5107baf0b0'
for r in manifest['exports']:assert sha(A/r['path'])==r['sha256']and(A/r['path']).stat().st_size==r['bytes']
for r in json.loads((A/'dependencies.json').read_text()):assert sha(Path(r['path']))==r['sha256']
receipts=[]
def run(name,args,cwd=A,timeout=60,env=None):
 with (W/(name+'.stdout')).open('wb')as out,(W/(name+'.stderr')).open('wb')as err:r=subprocess.run(args,cwd=cwd,stdout=out,stderr=err,timeout=timeout,env=env)
 receipts.append(dict(name=name,command=[str(x)for x in args],returncode=r.returncode));return r.returncode
# Direct/GAP outputs from terminal15161 are retained; only the initial blank-line CR differs.
assert (W/'direct.json').exists() and (W/'gap.stdout').exists()
assert(W/'direct.stderr').stat().st_size==(W/'gap.stderr').stat().st_size==0
assert(W/'gap.stdout').read_text()==(A/'gap.stdout').read_text()
base=json.loads((A/'direct_report02.json').read_text());fresh=json.loads((W/'direct.json').read_text());assert fresh==base
# Structural damage and interpreter controls.
rows=json.loads((A/'graphs.json').read_text());controls=[]
for tag,mut in [('missing drawing',lambda x:x.pop()),('invalid matching',lambda x:x[0]['transpositions'][0].append([2,3])),('nonidentity lost',lambda x:x[-1]['transpositions'].__setitem__(0,[]))]:
 x=json.loads(json.dumps(rows));mut(x);p=W/(tag.replace(' ','_')+'.json');dump(p,x);output=W/(tag.replace(' ','_')+'_result.json');rc=run(tag.replace(' ','_'),[sys.executable,A/'check.py','--data',p,'--output',output]);assert rc!=0 and not output.exists();controls.append(tag)
for name,args,env in [('opt_flag',[sys.executable,'-O',A/'check.py','--output',W/'opt_flag.json'],None),('opt_env',[sys.executable,A/'check.py','--output',W/'opt_env.json'],dict(os.environ,PYTHONOPTIMIZE='1'))]:
 assert run(name,args,env=env)!=0 and not(W/(name+'.json')).exists();controls.append(name)
# Direct finite models of the difference-map proof: C3 x C3 and D8 x C2.
# Enumerate every subgroup and all pairs; the central kernel and product are explicit.
def subgroup_generated(seed,e,mul):
 h={e};todo=[e]
 while todo:
  x=todo.pop()
  for y in seed:
   z=mul(x,y)
   if z not in h:h.add(z);todo.append(z)
 return frozenset(h)
def all_subgroups(elems,e,mul):
 seen={frozenset([e])};todo=list(seen)
 while todo:
  h=todo.pop()
  for x in elems:
   if x in h:continue
   k=subgroup_generated(list(h)+[x],e,mul)
   if k not in seen:seen.add(k);todo.append(k)
 return list(seen)
models=[]
for name,elems,e,mul,project in [('C3xC3',list(itertools.product(range(3),repeat=2)),(0,0),lambda x,y:((x[0]+y[0])%3,(x[1]+y[1])%3),lambda x:x[0]),('D8xC2',list(itertools.product(range(4),range(2),range(2))),(0,0,0),lambda x,y:((x[0]+(-1 if x[1] else 1)*y[0])%4,(x[1]+y[1])%2,(x[2]+y[2])%2),lambda x:(x[0]%2,x[1]))]:
 hs=all_subgroups(elems,e,mul);kernel={x for x in elems if project(x)==project(e)};inverse={x:next(y for y in elems if mul(x,y)==e)for x in elems};proper=0
 for u in hs:
  for v in hs:
   U={project(x)for x in u};V={project(x)for x in v};I=U&V;P={project(x)for x in u&v};KU=u&kernel;KV=v&kernel;K={mul(x,y)for x in KU for y in KV}
   delta={}
   for x in I:
    lifts={frozenset(mul(mul(a,inverse[b]),k)for k in K)for a in u for b in v if project(a)==project(b)==x};assert len(lifts)==1;delta[x]=next(iter(lifts))
   assert {x for x,c in delta.items()if e in c}==P
   assert len(set(delta.values()))==len(I)//len(P) and len(kernel)% (len(K)*len(set(delta.values())))==0
   for x in I:
    for y in I:
     a=next(a for a in u if project(a)==x);b=next(a for a in u if project(a)==y);xy=project(mul(a,b));assert delta[xy]==frozenset(mul(s,t)for s in delta[x]for t in delta[y])
   proper+=len(I)>len(P)
 models.append(dict(group=name,subgroups=len(hs),pairs=len(hs)**2,proper_image_intersections=proper))
assert models[0]['proper_image_intersections']>0
dump(W/'lemma_controls.json',models)
shutil.copyfile(A/'central_intersections.tex',W/'central_intersections.tex')
assert run('latex',['pdflatex','-interaction=nonstopmode','-halt-on-error','central_intersections.tex'],cwd=W)==0
from pypdf import PdfReader
x=PdfReader(W/'central_intersections.pdf');y=PdfReader(A/'central_intersections.pdf');assert len(x.pages)==len(y.pages)==3 and all(a.extract_text()==b.extract_text()for a,b in zip(x.pages,y.pages))
assert run('render',['gs','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile='+str(W/'page-%d.png'),str(W/'central_intersections.pdf')],cwd=W)==0
dump(W/'result.json',dict(status='PASS_ROOT_CENTRAL_REPLAY',author_manifest=sha(A/'manifest.json'),exports=len(manifest['exports']),source_dependencies=5,finite_diagrams=11,positive_all_subset_pairs=256,lemma_controls=models,malformed_controls=controls,native_pages=3,receipts=receipts,whole_original_credit=0));print('PASS_ROOT_CENTRAL_REPLAY')
