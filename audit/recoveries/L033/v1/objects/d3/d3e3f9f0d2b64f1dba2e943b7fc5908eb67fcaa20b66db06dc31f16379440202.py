import sys
if sys.flags.optimize: raise SystemExit('optimized execution unsupported')
import argparse,ast,hashlib,itertools,json,pathlib,subprocess,time

def need(ok,msg):
 if not ok:raise ValueError(msg)
def mul(a,b):return tuple(b[i-1] for i in a)
def inv(a):return tuple(a.index(i)+1 for i in range(1,len(a)+1))
def power(a,n):
 r=tuple(range(1,len(a)+1))
 for _ in range(n):r=mul(r,a)
 return r
def closure(gens,n):
 one=tuple(range(1,n+1));seen={one};todo=[one]
 for x in todo:
  for y in gens:
   z=mul(x,y)
   if z not in seen:seen.add(z);todo.append(z)
 return seen
def conjugate(a,g):return mul(mul(inv(g),a),g)
def standard(n):return sorted(itertools.permutations(range(1,n+1)))
def matrix(r,label):return [[1 if i==j else label for j in range(r)]for i in range(r)]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',type=pathlib.Path,required=True);ap.add_argument('--out',type=pathlib.Path,required=True);a=ap.parse_args();a.out.mkdir(exist_ok=False)
 cases=[]
 cases.append((standard(3),matrix(2,6)))
 cases.append((standard(3),matrix(3,6)))
 cases.append((standard(4),[[1,3,2],[3,1,3],[2,3,1]]))
 cases.append((standard(4),matrix(3,12)))
 m=matrix(4,2);m[0][1]=m[1][0]=3;m[1][2]=m[2][1]=3;cases.append((standard(4),m))
 cases.append((standard(4),matrix(4,6)))
 cases.append((sorted(closure([(2,3,4,1),(1,4,3,2)],4)),matrix(3,4)))
 cases.append((sorted(closure([(2,1,4,3),(3,4,1,2)],4)),matrix(2,2)))
 driver='LoadPackage("LINS");;\nRead('+json.dumps(str(a.packet.resolve()/'coxeter_seeds.g'))+');;\n'
 driver+='MakeSource:=function(M) local f,x,r,i,j;f:=FreeGroup(Length(M));x:=GeneratorsOfGroup(f);r:=List(x,g->g^2);for i in [1..Length(M)] do for j in [i+1..Length(M)] do Add(r,(x[i]*x[j])^M[i][j]);od;od;return f/r;end;;\n'
 reports=[];expected=[]
 for k,(g,m) in enumerate(cases):
  n=len(g[0]);r=len(m);one=tuple(range(1,n+1));sq=[x for x in g if mul(x,x)==one];wanted=set();raw=ident=proper=0
  for t in itertools.product(sq,repeat=r):
   if any(power(mul(t[i],t[j]),m[i][j])!=one for i in range(r)for j in range(i+1,r)):continue
   if closure(t,n)!=set(g):continue
   raw+=1;ident+=one in t;proper+=any(m[i][j]>1 and power(mul(t[i],t[j]),m[i][j]//p)==one for i in range(r)for j in range(i+1,r)for p in range(2,m[i][j]+1)if m[i][j]%p==0)
   wanted.add(min(tuple(conjugate(x,z)for x in t)for z in g))
  expected.append(wanted);reports.append({'case':k,'group_order':len(g),'rank':r,'literal_surjections':raw,'inner_orbits':len(wanted),'surjections_with_identity':ident,'proper_bond_order_surjections':proper})
  driver+='Q:=Group(List('+str(g).replace('(','[').replace(')',']')+',PermList));;M:='+str(m)+';;F:=MakeSource(M);;hs:=CoxeterTargetEpis(F,Q,M);;\n'
  driver+='Print("INDEPENDENT_CASE '+str(k)+' ",List(hs,h->List(GeneratorsOfGroup(F),x->ListPerm(Image(h,x),'+str(n)+')))," END_CASE\\n");\n'
 driver+='QUIT;\n';p=a.out/'driver.g';p.write_text(driver);start=time.monotonic();run=subprocess.run(['/opt/homebrew/bin/gap','-q','-b','--quitonbreak',str(p.resolve())],capture_output=True,text=True,timeout=45);(a.out/'stdout').write_text(run.stdout);(a.out/'stderr').write_text(run.stderr);need(run.returncode==0 and not run.stderr.strip(),'unclean GAP control')
 for k,((g,m),want) in enumerate(zip(cases,expected)):
  part=run.stdout.split('INDEPENDENT_CASE '+str(k)+' ',1)[1].split(' END_CASE',1)[0];rows=ast.literal_eval(part);got=[tuple(tuple(z)for z in row)for row in rows];canon=[min(tuple(conjugate(x,z)for x in t)for z in g)for t in got];need(len(set(canon))==len(canon),'duplicate returned inner orbit');need(set(canon)==want,'literal orbit mismatch')
 data={'status':'PASS','cases':reports,'seconds':time.monotonic()-start,'source_pin':{'path':str(a.packet.resolve()/'coxeter_seeds.g'),'sha256':hashlib.sha256((a.packet/'coxeter_seeds.g').read_bytes()).hexdigest()},'target_credit':0};(a.out/'report.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data))
if __name__=='__main__':main()
