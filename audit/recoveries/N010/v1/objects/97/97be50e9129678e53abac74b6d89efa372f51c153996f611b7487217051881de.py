import argparse,ast,hashlib,json,os,re,subprocess,sys,time
from pathlib import Path
if sys.flags.optimize:raise ValueError('optimization forbidden')
def need(v,m):
 if not v:raise ValueError(m)
def mul(a,b):return tuple(b[x] for x in a)
def inv(a):return tuple(a.index(i) for i in range(len(a)))
def power(a,k):
 if k<0:a=inv(a);k=-k
 z=tuple(range(len(a)))
 for _ in range(k):z=mul(z,a)
 return z
def prod(xs,n):
 z=tuple(range(n))
 for x in xs:z=mul(z,x)
 return z
def closure(gens):
 n=len(gens[0]);ans={tuple(range(n))};todo=list(ans)
 for g in todo:
  for a in gens:
   h=mul(g,a)
   if h not in ans:ans.add(h);todo.append(h)
 return ans
def rels(a,st):
 u,v,w=a;n=len(u)
 return [power(u,4),power(v,4),power(w,4),power(mul(u,v),2),power(mul(v,w),2),power(prod(a,n),2),mul(power(mul(inv(u),v),st[0]),power(mul(u,inv(v)),st[1])),mul(mul(inv(v),w),power(mul(v,inv(w)),3))]
def literal(a,st,expected):
 n=len(a[0]);e=tuple(range(n))
 need(len(a)==3 and all(tuple(sorted(x))==e for x in a),'literal permutations')
 need(all(x==e for x in rels(a,st)),'literal relations')
 G=closure(a);F=closure(a[:2]);V=closure(a[1:]);cyc=[closure([x]) for x in a]
 need(len(G)==expected,'literal full generated group');need([len(F),len(V)]==[40,40],'actual local groups');need(F&V==cyc[1],'actual middle intersection')
 need(cyc[0]&cyc[1]=={e} and cyc[1]&cyc[2]=={e},'actual cyclic intersections')
 need(all(len(x)==4 for x in cyc),'exact type')
 reflected=[inv(a[0]),mul(power(a[0],2),a[1]),a[2]];bad=[i+1 for i,x in enumerate(rels(reflected,st)) if x!=e];need(bad==[7,8],'reflection obstruction')
 return {'parameters':st,'order':len(G),'degree':n,'local_orders':[len(F),len(V)],'middle_order':len(F&V),'reflection_relations_failing':bad}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);args=p.parse_args();args.out.mkdir(parents=True,exist_ok=False)
 base=Path(__file__).resolve().parent;script=base/'verify_amalgamations.g';t=time.monotonic();r=subprocess.run(['/opt/homebrew/bin/gap','-q','-T',str(script)],capture_output=True,timeout=60)
 (args.out/'gap.stdout').write_bytes(r.stdout);(args.out/'gap.stderr').write_bytes(r.stderr);need(r.returncode==0 and not r.stderr,'GAP execution');txt=r.stdout.decode();need('PASS_TWO_ORIENTED_AMALGAMATIONS' in txt,'GAP completion')
 arrays=[ast.literal_eval(x) for x in re.findall(r'^GENERATORS (.+)$',txt,re.M)];need(len(arrays)==2,'two literal arrays');results=[]
 for arr,st,N in zip(arrays,[[1,3],[3,1]],[2000,960]):results.append(literal([tuple(y-1 for y in x) for x in arr],st,N))
 damaged=[tuple(x-1 for x in row) for row in arrays[0]];damaged[2]=damaged[1]
 try:literal(damaged,[1,3],2000)
 except ValueError:pass
 else:raise ValueError('damaged marking passed')
 (args.out/'generators.json').write_text(json.dumps(arrays,indent=2)+'\n')
 report={'status':'PASS_TWO_EXACT_ORIENTED_AMALGAMATIONS','cases':results,'actual_fp_isomorphism_checked_in_GAP':True,'independent_literal_group_checks':True,'damage_controls':1,'elapsed_seconds':time.monotonic()-t,'GAP_source_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'proof_assistant_certificate':False,'whole_original_credit':0,'new_question_credit':0}
 (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
