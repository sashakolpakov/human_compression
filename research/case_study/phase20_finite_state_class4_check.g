# Phase20 class-four positive transition diagnostic.
# Standalone; initial c=3 pool is rebuilt independently, then the frozen
# phase19 noncentral families supply the other sixteen budget-two windows.
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


K2FamilyCheck19:=function(d,kind,edge,triple,betaBits)
 local F,f,r,u,z,rel,i,j,c,alpha,beta,Q,epi,iso,G,kg,K,Z,L,
 sets,pars,S,want,meets;
 F:=FreeGroup(d+2);f:=GeneratorsOfGroup(F);r:=f{[1..d]};u:=f[d+1];z:=f[d+2];
 rel:=List(r,x->x^2);Add(rel,z^2);
 for i in [1..d] do for j in [i+1..d] do
  if j-i>1 then Add(rel,Comm(r[i],r[j]));fi;
 od;od;
 for c in f do Add(rel,Comm(z,c));od;
 alpha:=List([1..d-1],i->One(F));beta:=List([1..d-2],i->One(F));
 if kind="C4" then
  Add(rel,u^2*z);alpha[edge]:=u;
  for i in [1..d] do
   if i=edge or i=edge+1 then Add(rel,u^r[i]*u);else Add(rel,Comm(u,r[i]));fi;
  od;
 else
  Add(rel,u^2);beta[triple]:=u;
  if edge<>0 then alpha[edge]:=z;fi;
  for i in [1..d] do
   if i=triple+1 then Add(rel,Comm(u,r[i])*z);else Add(rel,Comm(u,r[i]));fi;
  od;
 fi;
 for i in betaBits do beta[i]:=z;od;
 for i in [1..d-1] do
  c:=Comm(r[i],r[i+1]);Add(rel,c^2*alpha[i]^-1);
  if i<=d-2 then Add(rel,Comm(c,r[i+2])*beta[i]^-1);fi;
 od;
 Q:=F/rel;epi:=NqEpimorphismNilpotentQuotient(Q,4);G:=Image(epi);
 kg:=List(GeneratorsOfGroup(Q){[d+1,d+2]},x->Image(epi,x));
 r:=List(GeneratorsOfGroup(Q){[1..d]},x->Image(epi,x));
 iso:=IsomorphismPcGroup(G);r:=List(r,x->Image(iso,x));kg:=List(kg,x->Image(iso,x));G:=Image(iso);
 if Size(G)<>2^(2*d+1) or Subgroup(G,r)<>G then Error("Order/generation");fi;
 K:=CommutatorSubgroup(DerivedSubgroup(G),G);Z:=Subgroup(G,[kg[2]]);
 L:=CommutatorSubgroup(K,G);
 if K<>Subgroup(G,kg) or Size(K)<>4 or L<>Z or Size(Z)<>2 then Error("Lower central series");fi;
 if not IsSubgroup(Centre(G),Z) then Error("gamma4 central");fi;
 if (kind="C4")<>IsCyclic(K) then Error("Kernel type");fi;
 return rec(G:=G,r:=r);
end;;

pool:=ShallowCopy(built4);;
for e in [1..3] do
 for bits in Combinations(Filtered([e-1,e],i->i>=1 and i<=2)) do
  Add(pool,K2FamilyCheck19(4,"C4",e,0,bits));
 od;
od;
for t in [1..2] do
 Add(pool,K2FamilyCheck19(4,"V4",0,t,[]));
 for e in [t,t+1] do
  for bits in Combinations(Filtered([e-1,e],i->i>=1 and i<=2 and i<>t)) do
   Add(pool,K2FamilyCheck19(4,"V4",e,t,bits));
  od;
 od;
od;
for h in pool do
 h.first:=Subgroup(h.G,h.r{[1..3]});h.last:=Subgroup(h.G,h.r{[2..4]});
 h.R:=Intersection(h.last,NormalClosure(h.G,Subgroup(h.G,[h.r[1]])));
 h.N:=NormalClosure(h.G,Subgroup(h.G,[h.r[4]]));
 h.J:=Intersection(h.N,h.first);
od;
pool:=Filtered(pool,h->Size(h.G)<=512);;
alphabet:=pool;;states:=[];;initial:=[];;edges:=[];;
for hi in [1..Length(alphabet)] do Add(initial,FindState(hi,alphabet[hi].R));od;
at:=1;;ac:=0;;bc:=0;;oc:=0;;attempted:=0;;
while at<=Length(states) do
 old:=alphabet[states[at].hi];
 for hi in [1..Length(alphabet)] do
  attempted:=attempted+1;h:=alphabet[hi];
  theta:=GroupHomomorphismByImages(old.last,h.first,old.r{[2..4]},h.r{[1..3]});
  if theta=fail or Size(old.last)<>Size(h.first) or not IsBijective(theta) then oc:=oc+1;continue;fi;
  imR:=Image(theta,states[at].R);
  if Size(CommutatorSubgroup(imR,h.N))<>1 then ac:=ac+1;continue;fi;
  preJ:=PreImage(theta,h.J);
  if not ForAll(GeneratorsOfGroup(preJ),x->Comm(x,old.r[1])=One(old.G)) then bc:=bc+1;continue;fi;
  Rnew:=Intersection(h.last,NormalClosure(h.G,ClosureGroup(imR,h.r[1])));
  nxt:=FindState(hi,Rnew);
  Add(edges,rec(src:=at,dst:=nxt,hi:=hi,theta:=theta,J:=h.J,weight:=LogInt(Index(h.G,h.first),2)-2));
 od;
 at:=at+1;
od;
Print("CLASS4_BUDGET2 windows=",Length(alphabet)," states=",Length(states)," transitions=",Length(edges)," attempts=",attempted," A_reject=",ac," B_reject=",bc,"\n");
# Exact semidirect/diagonal realization of every edge from the initial
# rank-four states. This includes genuinely class-four windows; the pool
# itself uses the separately proved phase19 excess-two parameter list.
constructed5:=0;;noncentralDiagonal:=0;;nontrivialDiagonal:=0;;
for ed in edges do
 if not ed.src in initial then continue;fi;
 old:=alphabet[states[ed.src].hi];h:=alphabet[ed.hi];
 P:=old.G;N:=h.N;ng:=GeneratorsOfGroup(N);
 amaps:=List([1..4],i->IdentityMapping(N));
 for i in [2..4] do
  actor:=h.r[i-1];amaps[i]:=GroupHomomorphismByImages(N,N,ng,List(ng,x->x^actor));
 od;
 aut:=Group(amaps);
 if not IsGroupOfAutomorphisms(aut) then Error("Class-four action maps");fi;
 action:=GroupHomomorphismByImages(P,aut,old.r,amaps);
 if action=fail then Error("Class-four extended action");fi;
 SD:=SemidirectProduct(P,action,N);ep:=Embedding(SD,1);en:=Embedding(SD,2);
 dg:=List(GeneratorsOfGroup(ed.J),j->Image(ep,PreImagesRepresentative(ed.theta,j))*Image(en,j^-1));
 D:=Subgroup(SD,dg);
 if not IsNormal(SD,D) or Size(D)<>Size(ed.J) then Error("Class-four diagonal");fi;
 if Size(D)>1 then nontrivialDiagonal:=nontrivialDiagonal+1;fi;
 if not IsSubgroup(Centre(SD),D) then noncentralDiagonal:=noncentralDiagonal+1;fi;
 qu:=NaturalHomomorphismByNormalSubgroup(SD,D);G:=Image(qu);
 r:=Concatenation(List(old.r,x->Image(qu,Image(ep,x))),[Image(qu,Image(en,h.r[4]))]);
 if Subgroup(G,r)<>G or Size(G)<>Size(P)*Index(h.G,h.first) then Error("Class-four order/marking");fi;
 if Length(LowerCentralSeries(G))-1>4 or not IP(G,r) then Error("Class-four class/IP");fi;
 Hp:=Subgroup(G,r{[2..5]});Pm:=Subgroup(G,r{[1..4]});
 hm:=GroupHomomorphismByImages(h.G,Hp,h.r,r{[2..5]});
 pm:=GroupHomomorphismByImages(P,Pm,old.r,r{[1..4]});
 if hm=fail or pm=fail or not IsBijective(hm) or not IsBijective(pm) then Error("Class-four factor embeddings");fi;
 realR:=Intersection(Subgroup(G,r{[3..5]}),NormalClosure(G,Subgroup(G,r{[1,2]})));
 if realR<>Image(hm,states[ed.dst].R) then Error("Class-four deletion update");fi;
 constructed5:=constructed5+1;
od;
if constructed5<>258 then Error("Class-four construction count");fi;
Print("CLASS4_CONSTRUCTIONS rank5=",constructed5," nontrivial_diagonal=",nontrivialDiagonal," noncentral_diagonal=",noncentralDiagonal," cumulative_parabolics=",closureCount," cumulative_meets=",meetCount,"\n");
x:=Indeterminate(Rationals,"x");;vv:=List(states,s->0*x);;
for i in initial do vv[i]:=vv[i]+x^(LogInt(Size(alphabet[states[i].hi].G),2)-7);od;
for rank in [4..12] do
 got:=Sum(vv);expected:=1+(5*rank-10)*x+((25*rank^2-107*rank+122)/2)*x^2;
 if got<>expected then Error("Fixed excess two count mismatch");fi;
 Print("FIXED_EXCESS_TWO rank=",rank," coefficients=",CoefficientsOfUnivariatePolynomial(got),"\n");
 nv:=List(states,s->0*x);
 for ed in edges do nv[ed.dst]:=nv[ed.dst]+vv[ed.src]*x^ed.weight;od;
 vv:=List(nv,p->EuclideanRemainder(p,x^3));
od;
Print("PASS: bounded class-four transitions and exact fixed-excess-two walk counts; alphabet completeness retains phase18/19 classification, no unrestricted class-four census.\n");
QUIT;
