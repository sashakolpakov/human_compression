#!/usr/bin/env python3
"""Identify specific full groups by checked bijective homomorphisms."""
import argparse,hashlib,json,pathlib,subprocess,time
HERE=pathlib.Path(__file__).resolve().parent

def job(row,out,gap,timeout):
 i=row['id'];d=out/i;d.mkdir();s=(HERE/'certificates'/(i+'.log')).read_text();gens=s.split('ROTATION_GENERATORS ',1)[1].split('\nLITERAL_RELATORS ',1)[0].strip();reg='CHIRALITY_WITNESS_RELATOR' not in s
 code='SetAssertionLevel(1);;SizeScreen([100000,100000]);;\ngg:='+gens+';;G:=Group(gg);;\n'
 if reg:code+='aut:=GroupHomomorphismByImages(G,G,gg,List(gg,Inverse));;Assert(0,aut<>fail and IsBijective(aut));;d:=LargestMovedPoint(G);;diag:=g->PermList(Concatenation(List([1..d],i->i^g),List([1..d],i->d+i^Image(aut,g))));;t:=PermList(Concatenation([d+1..2*d],[1..d]));;G:=Group(Concatenation([t],List(gg,diag)));;\n'
 code+='Fibre2:=function(A,B) local DA,DB,FA,FB,D,ea,eb,pa,pb,H;DA:=DerivedSubgroup(A);DB:=DerivedSubgroup(B);Assert(0,Index(A,DA)=2 and Index(B,DB)=2);D:=DirectProduct(A,B);ea:=Embedding(D,1);eb:=Embedding(D,2);pa:=First(GeneratorsOfGroup(A),a->not a in DA);pb:=First(GeneratorsOfGroup(B),b->not b in DB);H:=Group(Concatenation(List(GeneratorsOfGroup(DA),a->Image(ea,a)),List(GeneratorsOfGroup(DB),b->Image(eb,b)),[Image(ea,pa)*Image(eb,pb)]));Assert(0,Size(H)*2=Size(D));return H;end;;\nOddOuter:=function(S) local A,D,f,Q,P;A:=Image(IsomorphismPermGroup(AutomorphismGroup(S)));D:=DerivedSubgroup(A);f:=NaturalHomomorphismByNormalSubgroup(A,D);Q:=Image(f);P:=PreImage(f,SylowSubgroup(Q,3));Assert(0,Size(P)=3*Size(S));return P;end;;\n'
 code+='PSigma49:=function() local F,L,z,inf,u,v,w,f,pg;F:=GF(49);L:=Elements(F);z:=PrimitiveElement(F);inf:=50;u:=PermList(Concatenation(List(L,x->Position(L,x+One(F))),[inf]));v:=PermList(Concatenation(List(L,x->Position(L,z^2*x)),[inf]));w:=PermList(Concatenation(List(L,function(x) if IsZero(x) then return inf;else return Position(L,-x^-1);fi;end),[Position(L,Zero(F))]));f:=PermList(Concatenation(List(L,x->Position(L,x^7)),[inf]));pg:=Group(u,v,w);Assert(0,Size(pg)=58800 and not f in pg);return Group(u,v,w,f);end;;\n'
 code+='T:='+row['gap_constructor']+';;Print("GROUP_ORDERS ",Size(G)," ",Size(T),"\\n");;iso:=IsomorphismGroups(G,T);;Assert(0,iso<>fail);;Assert(0,IsGroupHomomorphism(iso) and IsBijective(iso));;Print("SOURCE_GENERATORS ",GeneratorsOfGroup(G),"\\n");;Print("TARGET_GENERATORS ",GeneratorsOfGroup(T),"\\n");;Print("ISOMORPHISM_IMAGES ",List(GeneratorsOfGroup(G),g->Image(iso,g)),"\\n");;Print("PASS_NAMED_ISOMORPHISM '+i+'\\n");;QUIT;\n'
 if i=='T8.11':
  code=code.split('T:=',1)[0]
  code+='M:=MinimalNormalSubgroups(G);;Print("MINIMAL_NORMAL_ORDERS ",List(M,Size),"\\n");;A:=First(M,m->Size(m)=2520);;B:=First(M,m->Size(m)=504);;Assert(0,A<>fail and B<>fail);;P:=Centralizer(G,B);;Q:=Centralizer(G,A);;Print("CENTRALIZER_ORDERS ",Size(P)," ",Size(Q),"\\n");;Assert(0,Size(P)=5040 and Size(Q)=1512);;Assert(0,Size(Intersection(P,Q))=1 and Size(Group(Concatenation(GeneratorsOfGroup(P),GeneratorsOfGroup(Q))))=Size(G));;Assert(0,ForAll(GeneratorsOfGroup(P),p->ForAll(GeneratorsOfGroup(Q),q->p*q=q*p)));;ip:=IsomorphismGroups(P,SymmetricGroup(7));;iq:=IsomorphismGroups(Q,Image(IsomorphismPermGroup(AutomorphismGroup(PSL(2,8)))));;Assert(0,ip<>fail and iq<>fail and IsBijective(ip) and IsBijective(iq));;Print("FACTOR_GENERATORS ",GeneratorsOfGroup(P)," ",GeneratorsOfGroup(Q),"\\n");;Print("FACTOR_IMAGES ",List(GeneratorsOfGroup(P),x->Image(ip,x))," ",List(GeneratorsOfGroup(Q),x->Image(iq,x)),"\\n");;Print("PASS_NAMED_ISOMORPHISM T8.11\\n");;QUIT;\n'
 (d/'input.g').write_text(code);start=time.monotonic()
 with (d/'stdout').open('wb') as o,(d/'stderr').open('wb') as e:
  try:rc=subprocess.run([gap,'-q','-T',str(d/'input.g')],stdout=o,stderr=e,timeout=timeout).returncode
  except subprocess.TimeoutExpired:rc='TIMEOUT'
 result=dict(row,returncode=rc,seconds=round(time.monotonic()-start,6),passed=rc==0 and ('PASS_NAMED_ISOMORPHISM '+i) in (d/'stdout').read_text() and not (d/'stderr').read_text().strip())
 (d/'receipt.json').write_text(json.dumps(result,indent=2)+'\n');print(i,result['passed'],result['seconds'],flush=True);return result

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=pathlib.Path,required=True);p.add_argument('--gap',default='/opt/homebrew/bin/gap');p.add_argument('--timeout',type=int,default=60);p.add_argument('--rows',nargs='*');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 targets=json.loads((HERE/'structural_targets.json').read_text())['targets'];targets=[r for r in targets if not a.rows or r['id'] in a.rows];res=[job(r,a.out,a.gap,a.timeout) for r in targets]
 (a.out/'report.json').write_text(json.dumps({'status':'PASS' if all(r['passed'] for r in res) else 'INCOMPLETE','rows':res},indent=2)+'\n')
if __name__=='__main__':main()
