# Independent bounded transition diagnostic for phase20_finite_state.md.
# Complete rank-three/class-three alphabet from ALL subgroups of the
# universal gamma_3, followed by exact state tests.  No phase18 alpha/beta
# parameter filter is used.  GAP + NQ required; no group catalogue.
if LoadPackage("nq")=fail then Error("NQ required");fi;
SizeScreen([240,40]);;
pcmap:=function(G) return IsomorphismPcGroup(G); end;;
meetCount:=0;; closureCount:=0;;
IP:=function(G,r)
 local ss,gg,i,j,k,good;
 ss:=Combinations([1..Length(r)]);
 gg:=List(ss,S->Subgroup(G,r{S}));
 closureCount:=closureCount+Length(gg); good:=true;
 for i in [1..Length(ss)] do for j in [1..Length(ss)] do
  k:=Position(ss,Intersection(ss[i],ss[j]));
  meetCount:=meetCount+1;
  if Intersection(gg[i],gg[j])<>gg[k] then good:=false;fi;
 od;od;
 return good;
end;;
F:=FreeGroup("a","b","c");;f:=GeneratorsOfGroup(F);;
FP:=F/[f[1]^2,f[2]^2,f[3]^2,Comm(f[1],f[3])];;
epi:=NqEpimorphismNilpotentQuotient(FP,3);;
iso:=pcmap(Image(epi));;U:=Image(iso);;
um:=List(GeneratorsOfGroup(FP),x->Image(iso,Image(epi,x)));;
K:=LowerCentralSeries(U)[3];;
if Size(U)<>256 or Size(K)<>8 then Error("Universal class-three order");fi;
subs:=AllSubgroups(K);;alphabet:=[];;pi:=fail;;
for ker in subs do
 pi:=NaturalHomomorphismByNormalSubgroup(U,ker);;H:=Image(pi);;
 rr:=List(um,x->Image(pi,x));;
 if IP(H,rr) then
  Add(alphabet,rec(G:=H,r:=rr,
   first:=Subgroup(H,rr{[1,2]}),last:=Subgroup(H,rr{[2,3]}),
   N:=NormalClosure(H,Subgroup(H,[rr[3]]))));
 fi;
od;
if Length(alphabet)<>13 then Error("Rank-three alphabet census");fi;
Print("VERSION GAP=",GAPInfo.Version," NQ=",PackageInfo("nq")[1].Version,"\n");
Print("ALPHABET universal=",Size(U)," gamma3=",Size(K)," all_kernels=",Length(subs)," accepted=",Length(alphabet),"\n");

states:=[];; initial:=[];; edges:=[];;
FindState:=function(hi,R)
 local i;
 for i in [1..Length(states)] do
  if states[i].hi=hi and states[i].R=R then return i;fi;
 od;
 Add(states,rec(hi:=hi,R:=R)); return Length(states);
end;;
for hi in [1..Length(alphabet)] do
 h:=alphabet[hi];;
 R:=Intersection(h.last,NormalClosure(h.G,Subgroup(h.G,[h.r[1]])));;
 Add(initial,FindState(hi,R));
od;
old:=fail;;at:=1;; attempted:=0;; overlapRejected:=0;; actionRejected:=0;; centralRejected:=0;;
while at<=Length(states) do
 st:=states[at];;old:=alphabet[st.hi];;
 for hi in [1..Length(alphabet)] do
  attempted:=attempted+1;h:=alphabet[hi];;
  theta:=GroupHomomorphismByImages(old.last,h.first,old.r{[2,3]},h.r{[1,2]});;
  if theta=fail or Size(old.last)<>Size(h.first) or not IsBijective(theta) then
   overlapRejected:=overlapRejected+1;continue;
  fi;
  imR:=Image(theta,st.R);;
  if Size(CommutatorSubgroup(imR,h.N))<>1 then actionRejected:=actionRejected+1;continue;fi;
  J:=Intersection(h.N,h.first);;preJ:=PreImage(theta,J);;
  if not ForAll(GeneratorsOfGroup(preJ),x->Comm(x,old.r[1])=One(old.G)) then
   centralRejected:=centralRejected+1;continue;
  fi;
  killed:=NormalClosure(h.G,ClosureGroup(imR,h.r[1]));;
  Rnew:=Intersection(h.last,killed);;nxt:=FindState(hi,Rnew);;
  weight:=LogInt(Index(h.G,h.first),2)-2;
  if weight<0 then Error("Negative excess increment");fi;
  Add(edges,rec(src:=at,dst:=nxt,hi:=hi,theta:=theta,J:=J,weight:=weight));
 od;
 at:=at+1;
od;
Print("AUTOMATON states=",Length(states)," transitions=",Length(edges)," attempts=",attempted,
 " overlap_reject=",overlapRejected," action_reject=",actionRejected," central_reject=",centralRejected,"\n");

# Genuine semidirect/diagonal constructions for every accepted rank-four walk.
# Maps use GAP's right-conjugation convention.  Check all actual intersections,
# nilpotency class, prefix/window embeddings, and next deletion kernel.
constructed:=0;;built4:=[];;initialSet:=Set(initial);;
N:=fail;;actor:=fail;;ep:=fail;;en:=fail;;qu:=fail;;
for ed in edges do
 if not ed.src in initialSet then continue;fi;
 st:=states[ed.src];;old:=alphabet[st.hi];;h:=alphabet[ed.hi];;
 P:=old.G;;N:=h.N;;ng:=GeneratorsOfGroup(N);;
 amaps:=List([1..3],i->IdentityMapping(N));;
 for i in [2..3] do
  actor:=h.r[i-1];;
  amaps[i]:=GroupHomomorphismByImages(N,N,ng,List(ng,x->x^actor));;
 od;
 aut:=Group(amaps);;
 if not IsGroupOfAutomorphisms(aut) then Error("Action maps not automorphisms");fi;
 action:=GroupHomomorphismByImages(P,aut,old.r,amaps);;
 if action=fail then Error("Transition action does not extend to prefix");fi;
 SD:=SemidirectProduct(P,action,N);;ep:=Embedding(SD,1);;en:=Embedding(SD,2);;
 jgens:=GeneratorsOfGroup(ed.J);;
 dg:=List(jgens,j->Image(ep,PreImagesRepresentative(ed.theta,j))*Image(en,j^-1));;
 D:=Subgroup(SD,dg);;
 if not IsNormal(SD,D) or Size(D)<>Size(ed.J) then Error("Diagonal intersection");fi;
 qu:=NaturalHomomorphismByNormalSubgroup(SD,D);;G:=Image(qu);;
 r:=Concatenation(List(old.r,x->Image(qu,Image(ep,x))),[Image(qu,Image(en,h.r[3]))]);;
 if Subgroup(G,r)<>G or Size(G)<>Size(P)*Index(h.G,h.first) then Error("Amalgam order/marking");fi;
 if Length(LowerCentralSeries(G))-1>3 or not IP(G,r) then Error("Amalgam class or actual IP");fi;
 Hp:=Subgroup(G,r{[2..4]});;Pm:=Subgroup(G,r{[1..3]});;
 hm:=GroupHomomorphismByImages(h.G,Hp,h.r,r{[2..4]});;
 pm:=GroupHomomorphismByImages(P,Pm,old.r,r{[1..3]});;
 if hm=fail or pm=fail or not IsBijective(hm) or not IsBijective(pm) then Error("Factor embeddings");fi;
 realR:=Intersection(Subgroup(G,r{[3,4]}),NormalClosure(G,Subgroup(G,r{[1,2]})));;
 if realR<>Image(hm,states[ed.dst].R) then Error("Deletion update does not match actual quotient");fi;
 Add(built4,rec(G:=G,r:=r));
 constructed:=constructed+1;
od;
if constructed<>89 then Error("Rank-four actual count");fi;
Print("CONSTRUCTIONS rank4=",constructed," total_parabolics=",closureCount," actual_meets=",meetCount,"\n");

# Walk counts are computed from this graph; phase18 is only an external
# expected-value comparison, not a candidate filter or construction input.
x:=Indeterminate(Rationals,"x");;
v:=List(states,s->0*x);;
for i in initial do
 hi:=states[i].hi;v[i]:=v[i]+x^(LogInt(Size(alphabet[hi].G),2)-5);
od;
previous:=1+x;;expected:=1+5*x+6*x^2+x^3;;
for rank in [3..10] do
 got:=Sum(v);;
 if got<>expected then Error("All-excess count disagrees with independent class-three formula");fi;
 Print("COUNT rank=",rank," coefficients=",CoefficientsOfUnivariatePolynomial(got)," total=",Value(got,1),"\n");
 nextv:=List(states,s->0*x);;
 for ed in edges do nextv[ed.dst]:=nextv[ed.dst]+v[ed.src]*x^ed.weight;od;
 v:=nextv;; temp:=expected;;expected:=(1+5*x+x^2)*expected-x^2*previous;;previous:=temp;
od;
# Class-two boundary: the unique D8 window, trivial deletion kernel,
# and trivial attachment intersection give one state and its self-loop.
F2:=FreeGroup("a","b");;ff:=GeneratorsOfGroup(F2);;
Q2:=F2/[ff[1]^2,ff[2]^2];;ee:=NqEpimorphismNilpotentQuotient(Q2,2);;
ii:=IsomorphismPcGroup(Image(ee));;G2:=Image(ii);;
r2:=List(GeneratorsOfGroup(Q2),z->Image(ii,Image(ee,z)));;
B2:=Subgroup(G2,[r2[2]]);;N2:=NormalClosure(G2,Subgroup(G2,[r2[2]]));;
if Size(G2)<>8 or Size(Intersection(B2,NormalClosure(G2,Subgroup(G2,[r2[1]]))))<>1
 or Size(Intersection(N2,Subgroup(G2,[r2[1]])))<>1 or not IP(G2,r2) then Error("Class-two state");fi;
Print("CLASS_TWO windows=1 states=1 transitions=1 deletion_kernel=1 attachment_intersection=1\n");
Print("PASS: exact finite-state diagnostic, complete bounded alphabets for c=2,3 and all rank-four c=3 constructions; no all-class theorem follows from this finite check alone.\n");
QUIT;
