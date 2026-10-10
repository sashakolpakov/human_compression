"""Exact interval certificate; reads frozen phase41 input, writes only fresh outputs."""
from pathlib import Path
import argparse,hashlib,json,re,shutil,subprocess,tempfile,time
root=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);p.add_argument('--log',type=Path,required=True);args=p.parse_args()
assert not args.report.exists() and not args.log.exists(),'fresh output paths required'
sha=lambda b:hashlib.sha256(b).hexdigest()
source=root/'phase41_chiral_cover_check.g';base=source.read_bytes()
assert sha(base)=='59bf1cd96626df42e1e1baed82b88538416f336443c1a4076dfbb5f09bdcc69e'
assert base.decode().endswith('QUIT_GAP(0);\n')
old={}
for mf in ['phase41_chiral_cover_manifest.json','phase44_cover_poset_manifest.json']:
    m=json.loads((root/mf).read_text())
    for name,meta in m['files'].items():
        assert sha((root/name).read_bytes())==meta['sha256'],name
        old[name]=meta['sha256']
extra=r'''
S:=mix(Q,Qd);;
e1:=GroupHomomorphismByImages(S.g,Q.g,S.s,Q.s);;
e2:=GroupHomomorphismByImages(S.g,Qd.g,S.s,Qd.s);;
eR:=GroupHomomorphismByImages(S.g,R.g,S.s,R.s);;
check(e1<>fail and e2<>fail and eR<>fail,"all marked maps");
check(IsSurjective(e1) and IsSurjective(e2) and IsSurjective(eR),"maps onto");
L:=Kernel(eR);; A:=Group(S.s{[1,2]});;B:=Group(S.s{[2,3]});;C:=Group([S.s[2]]);;
check(Size(S.g)=8748 and Size(L)=9,"source and kernel orders");
check(IsAbelian(L) and Exponent(L)=3,"elementary abelian kernel");
check(Size(A)=162 and Size(B)=162 and Size(C)=9,"end orders");
check(Intersection(A,B)=C,"source end IP");
check(Intersection(Group([S.s[1]]),C)=TrivialSubgroup(S.g),"source facet IP");
check(Intersection(Group([S.s[3]]),C)=TrivialSubgroup(S.g),"source vertex IP");
check(Intersection(L,A)=TrivialSubgroup(S.g) and Intersection(L,B)=TrivialSubgroup(S.g),"end injectivity");
check(ForAll(base,w->MappedWord(w,GeneratorsOfGroup(F),S.s)=One(S.g)),"source rotation relators");
mu:=GroupHomomorphismByImages(S.g,S.g,S.s,[S.s[1]^-1,S.s[1]^2*S.s[2],S.s[3]]);;
check(mu<>fail and IsBijective(mu),"source mirror automorphism");
D:=Intersection(Set(Elements(L)),Set(List(Cartesian(Elements(A),Elements(B)),p->p[1]*p[2])));;
u:=MappedWord((b*c^-1)^2*a*c^2*a^-1,GeneratorsOfGroup(F),S.s);;
v:=MappedWord((b^-1*a)^2*c^-1*a^-2*c,GeneratorsOfGroup(F),S.s);;
check(Order(u)=3 and Order(v)=3 and Group([u,v])=L and u*v=v*u,"literal basis");
check(Group([u])=Kernel(e1) and Group([v])=Kernel(e2),"known quotient kernels");
check(u^S.s[1]=u and v^S.s[1]=v^-1,"a character");
check(u^S.s[2]=u and v^S.s[2]=v,"b character");
check(u^S.s[3]=u^-1 and v^S.s[3]=v,"c character");
check(Image(mu,u)=u and Image(mu,v)=v^-1,"mirror character");
check(D=Set([One(L),u*v,u^2*v^2]),"exact diagonal defect");
check(not IsNormal(S.g,Group(D)),"defect is not normal");
check(not IsSubgroup(Centre(S.g),L),"abelian kernel not central");
subs:=AllSubgroups(L);;
stable:=Filtered(subs,N->IsNormal(S.g,N) and Image(mu,N)=N);;
check(Length(subs)=6 and Length(stable)=4,"complete subspace and invariant counts");
check(Set(stable)=Set([TrivialSubgroup(S.g),Group([u]),Group([v]),L]),"complete invariant list");
good:=Filtered(stable,N->Intersection(Elements(N),D)=[One(S.g)]);;
check(Set(good)=Set([TrivialSubgroup(S.g),Group([u]),Group([v])]),"complete admissible list");
M:=L;;qp:=eR;;
for M in stable do
 qp:=NaturalHomomorphismByNormalSubgroup(S.g,M);;
 qs:=List(S.s,g->Image(qp,g));;
 qa:=Group(qs{[1,2]});;qb:=Group(qs{[2,3]});;qc:=Group([qs[2]]);;
 check((Intersection(qa,qb)=qc)=(M in good),"all intermediate IP checks");
 qm:=GroupHomomorphismByImages(Image(qp),Image(qp),qs,[qs[1]^-1,qs[1]^2*qs[2],qs[3]]);;
 check(qm<>fail and IsBijective(qm),"every stable quotient mirror");
od;
maxgood:=Filtered(good,M->not ForAny(good,N->M<>N and IsSubgroup(N,M)));;
check(Set(maxgood)=Set([Group([u]),Group([v])]),"exact maximal admissible list");
check(Group(Concatenation(List(maxgood,GeneratorsOfGroup)))=L,"interval join density");
Print("INTERVAL_PASS order=8748 L=C3xC3 subspaces=6 invariant=4 good=3 maximal=2\n");
Print("ACTION_PASS a=(+,-) b=(+,+) c=(-,+) mirror=(+,-)\n");
Print("DEFECT_PASS D=<uv> nonnormal; maximal=<u>,<v>; join=L\n");
# A fully explicit counterexample to D always being a subgroup.
rs:=[(1,2),(2,3),(3,4)];;Htet:=Group(rs);;
Atet:=Group(rs{[1,2]});;Btet:=Group(rs{[2,3]});;
Ltet:=Group([(1,2)(3,4),(1,3)(2,4)]);;
indices:=Combinations([1..3]);;it:=[];;jt:=[];;
for it in indices do for jt in indices do
 check(Intersection(Subgroup(Htet,rs{it}),Subgroup(Htet,rs{jt}))=Subgroup(Htet,rs{Intersection(it,jt)}),"tetra full IP");
od;od;
check(IsNormal(Htet,Ltet) and Size(Ltet)=4,"tetra normal kernel");
check(Intersection(Atet,Ltet)=TrivialSubgroup(Htet) and Intersection(Btet,Ltet)=TrivialSubgroup(Htet),"tetra end injectivity");
Dtet:=Intersection(Set(Elements(Ltet)),Set(List(Cartesian(Elements(Atet),Elements(Btet)),p->p[1]*p[2])));;
check(Dtet=Set([(),(1,2)(3,4),(1,3)(2,4)]),"tetra exact defect set");
check(not (1,4)(2,3) in Dtet and Size(Group(Dtet))=4,"defect not subgroup");
qtet:=NaturalHomomorphismByNormalSubgroup(Htet,Ltet);;
check(Image(qtet,rs[1])=Image(qtet,rs[3]),"nonadjacent collapse limitation");
Print("TETRA_PASS D_size=3 generated_size=4 nonadjacent_marks_collapse\n");
QUIT_GAP(0);
'''
assembled=base.decode()[:-len('QUIT_GAP(0);\n')]+extra
start=time.monotonic()
with tempfile.TemporaryDirectory(prefix='phase46_cover_') as tmp:
    f=Path(tmp)/'check.g';f.write_text(assembled)
    res=subprocess.run([shutil.which('gap'),'-q',str(f)],cwd=tmp,capture_output=True,text=True,timeout=300)
assert res.returncode==0 and not res.stderr.strip(),(res.returncode,res.stderr,res.stdout)
assert not re.search(r'FAIL|Error,|Syntax error',res.stdout),res.stdout
clean=res.stdout.replace('\\\n','')
for tag in ['INTERVAL_PASS order=8748 L=C3xC3 subspaces=6 invariant=4 good=3 maximal=2','ACTION_PASS a=(+,-) b=(+,+) c=(-,+) mirror=(+,-)','DEFECT_PASS D=<uv> nonnormal; maximal=<u>,<v>; join=L','TETRA_PASS D_size=3 generated_size=4 nonadjacent_marks_collapse']:
    assert tag in clean,(tag,res.stdout)
for name,h in old.items():assert sha((root/name).read_bytes())==h,name
args.log.write_text(res.stdout)
report={'date':'2026-10-10','status':'PASS','wall_seconds':time.monotonic()-start,'runner_sha256':sha(Path(__file__).read_bytes()),'frozen_source_sha256':sha(base),'assembled_script_sha256':sha(assembled.encode()),'log_sha256':sha(args.log.read_bytes()),'GAP_version':re.search(r'PASS GAP (\S+)',res.stdout).group(1),'all_phase41_and44_bound_files_unchanged':True,'source_rotation_order':8748,'kernel':'C3 x C3','literal_basis':['(b c^-1)^2 a c^2 a^-1','(b^-1 a)^2 c^-1 a^-2 c'],'actions':{'a':[1,-1],'b':[1,1],'c':[-1,1],'mirror':[1,-1]},'defect_coordinates':[[0,0],[1,1],[2,2]],'subspaces':6,'invariant_subgroups':4,'admissible_kernels':3,'maximal_admissible_kernels':2,'interval_join_is_full_kernel':True,'defect_is_normal':False,'tetra_defect_size':3,'tetra_defect_generated_subgroup_size':4,'tetra_is_monodromy_counterexample':False,'retained':'Exact stock GAP algorithms; standard string C/C+ recognition. No new Lean theorem; no general conjecture resolution.'}
args.report.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
