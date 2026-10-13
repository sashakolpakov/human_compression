import sys
if sys.flags.optimize:
 raise SystemExit('Optimized Python is not permitted')
from pathlib import Path
import argparse,hashlib,json,os,subprocess,time

def need(c,m):
 if not c:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--gap',default='/opt/homebrew/bin/gap');a=p.parse_args()
W=Path(__file__).resolve().parent;need(not a.out.exists(),'Existing output directory')
pins={f:sha(W/f) for f in ['check.py','enumerate.g','checks.g']};a.out.mkdir(parents=True)
env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
for f in ['enumerate.g','checks.g']:(a.out/f).write_bytes((W/f).read_bytes())
def run(f,stem):
 with (a.out/(stem+'.stdout')).open('wb') as o,(a.out/(stem+'.stderr')).open('wb') as e:
  t=time.monotonic();q=subprocess.Popen([a.gap,'-q','-b',f],cwd=a.out,stdout=o,stderr=e,env=env)
  (a.out/(stem+'.pid')).write_text(str(q.pid)+'\n')
  try:rc=q.wait(timeout=120)
  except subprocess.TimeoutExpired:q.kill();q.wait();raise ValueError('TIMEOUT_NO_CERTIFICATE')
 text=(a.out/(stem+'.stdout')).read_text();need(rc==0 and not (a.out/(stem+'.stderr')).read_text().strip() and 'Error,' not in text,'GAP failed')
 return text,{'returncode':rc,'seconds':time.monotonic()-t,'sha256':sha(a.out/(stem+'.stdout'))}
text,execution=run('enumerate.g','enumeration')
need(text.count('PASS_PRIMITIVE_MARKINGS')==1,'Incomplete enumeration')
need('order=40320 target=6 max=6 involutions=763' in text,'Wrong enumeration model')
rows=[json.loads(line.split('|')[4]) for line in text.splitlines() if line.startswith('SOLUTION|8|0|')]
need(len(rows)==2,'Unexpected complete marking list')
(a.out/'records.json').write_text(json.dumps(rows,indent=2)+'\n')
code='Read("checks.g");;\nrows:='+json.dumps(rows)+';;\n'+'''S:=SymmetricGroup(8);;
c:=[(2,3),(1,2)(3,4),(4,5),(5,6),(6,7),(7,8)];;
for row in rows do
 t:=List(row,PermList);;
 if Length(t)<>6 or Group(t)<>S or not FullIP(t) then Error("actual full C marking");fi;
 if not ForAll(t,x->Order(x)=2) then Error("involutions");fi;
 for i in [1..6] do for j in [i+2..6] do if Comm(t[i],t[j])<>() then Error("string");fi;od;od;
 if RepresentativeAction(S,t,c,OnTuples)=fail and RepresentativeAction(S,t,Reversed(c),OnTuples)=fail then Error("core identification");fi;
od;
if RepresentativeAction(S,List(rows[1],PermList),List(rows[2],PermList),OnTuples)<>fail then Error("duplicate ordered classes");fi;
if FullIP([c[1],c[2],c[1]]) then Error("negative control");fi;
Print("TWO_COMPLETE_ORDERED_CORE_CLASSES_FULL_IP_PASS\\n");QUIT;
'''
(a.out/'validate.g').write_text(code)
v,validation=run('validate.g','validation');need(v.count('TWO_COMPLETE_ORDERED_CORE_CLASSES_FULL_IP_PASS')==1,'Incomplete validation')
need(all(sha(W/f)==h for f,h in pins.items()),'Input bytes changed')
r={'status':'COMPLETE_SYMMETRIC_EIGHT_RANK_SIX','input_pins':pins,'enumeration':execution,'validation':validation,'scope':'All connected string C-markings generating literal S8 of rank6; two ordered conjugacy classes, canonical core and its reverse. No higher-rank census claimed.','whole_original_credit':0}
(a.out/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
