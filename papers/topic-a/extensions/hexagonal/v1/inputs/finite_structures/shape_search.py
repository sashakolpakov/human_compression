#!/usr/bin/env python3
from pathlib import Path
import argparse,json,time,subprocess
from accepted_image import group_code,HERE

def atom(*a):return ['atom',list(a)]
def op(t,a,b):return [t,a,b]
def chain(a,*bs):
 for b in bs:a=op('colon',a,b)
 return a
C=lambda n:atom('cyclic',n)
E=lambda p,n:atom('elementary',p,n)
P=lambda p,a,b:atom('special',p,a,b)
S=lambda n:atom('S',n)
A=lambda n:atom('A',n)
PSL=lambda n,q:atom('PSL',n,q)
PSU=lambda n,q:atom('PSU',n,q)
x=lambda a,b:op('direct',a,b)
dot=lambda a,b:op('dot',a,b)
Q=atom('Q8')
SHAPES={
'T3.1':chain(dot(C(2),PSL(2,7)),C(2),C(2)),
'T3.2':chain(dot(C(2),A(7)),C(2),C(2)),
'T3.5':chain(dot(Q,x(PSL(2,7),C(2))),S(3)),
'T4.3':chain(x(P(3,1,2),C(3)),S(3),S(3)),
'T4.5':chain(P(3,1,2),C(2),S(3)),
'T4.6':chain(P(2,1,6),E(3,2),S(3),S(3)),
'T4.7':chain(P(3,1,2),E(2,2)),
'T4.8':chain(dot(P(2,5,6),x(A(5),C(3))),S(3),S(3)),
'T4.12':chain(dot(C(2),PSL(2,7)),S(3)),
'T4.14':chain(dot(C(3),PSU(3,5)),S(3)),
'T4.15':chain(dot(C(2),PSL(2,7)),C(2)),
'T4.16':chain(dot(C(2),PSL(2,7)),S(3)),
'T4.17':chain(dot(C(2),PSL(2,7)),C(2)),
'T5.3':chain(P(2,1,6),chain(A(5),C(2))),
'T5.5':chain(C(6),S(3),S(3),S(3)),
'T5.6':chain(P(2,1,6),C(3),S(3),S(3)),
'T5.7':chain(P(2,1,6),C(6),S(3),S(3),S(3)),
'T5.9':chain(x(S(3),C(3)),S(3),S(3),S(3)),
'T5.11':chain(P(3,1,2),C(6),S(3)),
'T5.12':chain(x(E(3,2),S(3)),S(3)),
'T5.13':chain(x(P(3,1,2),C(3)),S(3),S(3)),
'T5.14':chain(x(S(3),C(3)),S(3),S(3),S(3)),
'T5.15':x(chain(dot(C(4),chain(E(2,4),A(5))),C(2)),C(2)),
'T5.19':chain(dot(Q,PSL(2,7)),S(3)),
'T5.21':chain(P(3,2,6),C(7),C(3),C(2)),
'T6.1':chain(x(P(2,1,4),C(2)),S(3)),
'T6.7':chain(E(2,4),S(3),S(3)),
'T6.9':chain(E(2,6),C(7),C(3),C(2)),
'T7.2':chain(E(2,4),A(5),C(2),C(2),S(3)),
'T7.5':chain(dot(E(2,9),PSL(2,8)),C(3)),
'T7.7':chain(P(2,1,4),C(3),S(3),S(3)),
'T8.4':chain(P(2,1,6),S(3),S(3),S(3),S(3)),
'T8.6':chain(P(2,1,6),C(3),S(3),S(3)),
'T8.7':chain(P(2,1,6),S(3),S(3),S(3),S(3)),
'T8.8':chain(dot(C(2),x(A(5),x(A(5),A(5)))),C(2),S(3)),
}
def gap(x):
 if isinstance(x,list):return '['+','.join(map(gap,x))+']'
 return json.dumps(x)
def main():
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--rows',nargs='*');a.add_argument('--timeout',type=int,default=60);q=a.parse_args();q.out.mkdir(exist_ok=False,parents=True);res=[]
 for i,s in SHAPES.items():
  if q.rows and i not in q.rows:continue
  d=q.out/i;d.mkdir();code=group_code(i)+'Read('+json.dumps(str(HERE/'shape_engine.g'))+');;\ns:='+gap(s)+';;Print("START_SHAPE '+i+' ",Size(G)," ",ShapeSize(s),"\\n");;w:=FindShape(G,s);;Print("WITNESS ",w,"\\n");;if w=fail then Print("SHAPE_UNRESOLVED '+i+'\\n");else Print("PASS_SHAPE '+i+'\\n");fi;;QUIT;\n';(d/'input.g').write_text(code);t=time.monotonic()
  with (d/'stdout').open('wb') as o,(d/'stderr').open('wb') as e:
   try:rc=subprocess.run(['/opt/homebrew/bin/gap','-q','-T',str(d/'input.g')],stdout=o,stderr=e,timeout=q.timeout).returncode
   except subprocess.TimeoutExpired:rc='TIMEOUT'
  r={'id':i,'returncode':rc,'seconds':round(time.monotonic()-t,3),'passed':rc==0 and 'PASS_SHAPE' in (d/'stdout').read_text() and not (d/'stderr').read_text().strip()};res.append(r);print(r,flush=True)
 (q.out/'report.json').write_text(json.dumps(res,indent=2)+'\n')
if __name__=='__main__':main()
