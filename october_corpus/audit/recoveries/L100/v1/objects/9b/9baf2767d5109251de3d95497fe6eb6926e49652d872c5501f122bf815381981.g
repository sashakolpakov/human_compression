# Complete arbitrary-B RWPRI/FT/RC/(IP)2 augmentation for a named TomLib group.
# Optional REQUIRE_2T restricts panels; default true matches the sporadic source classifications.
# Completeness input: all TomLib subgroup classes and maximal-inclusion classes.
# No original geometry representatives are read.
LoadPackage("tomlib");;
SetInfoLevel(InfoWarning,0);;
SizeScreen([100000,24]);;
if not IsBound(GROUP_NAME) then GROUP_NAME:="M22";fi;
if not IsBound(REQUIRE_2T) then REQUIRE_2T:=true;fi;
if not IsBound(OUTPUT_DIR) then Error("Set OUTPUT_DIR to an existing directory");fi;
tom:=TableOfMarks(GROUP_NAME);;G:=UnderlyingGroup(tom);;
reps:=List([1..Length(OrdersTom(tom))],i->RepresentativeTom(tom,i));;
maxorders:=rec();;maxinclusions:=[];;local2T:=[];;
for K in reps do
 k:=Size(K);
 if not IsBound(maxorders.(String(k))) then maxorders.(String(k)):=[];fi;
 if k>1 then
  mm:=List(ConjugacyClassesMaximalSubgroups(K),Representative);
  UniteSet(maxorders.(String(k)),Set(List(mm,Size)));
  for H in mm do
   Add(maxinclusions,[K,H]);
   if Length(DoubleCosets(K,H,H))=2 then Add(local2T,[K,H]);fi;
  od;
 fi;
od;
Print("INPUT group=",GROUP_NAME," require_2T=",REQUIRE_2T," order=",Size(G)," subgroup_classes=",Length(reps)," maximal_inclusion_classes=",Length(maxinclusions)," locally_2T_inclusions=",Length(local2T)," GAP=",GAPInfo.Version," TomLib=",PackageInfo("tomlib")[1].Version,"\n");
IsMaxPair:=function(K,H)
 local ix,hom,p;
 if Size(K)=Size(H) or not Size(H) in maxorders.(String(Size(K))) then return false;fi;
 if Size(K)=Size(G) then
  return ForAny(maxinclusions,p->Size(p[1])=Size(G) and Size(p[2])=Size(H) and RepresentativeAction(G,H,p[2],OnPoints)<>fail);
 fi;
 ix:=Index(K,H);
 if IsPrimeInt(ix) then return true;fi;
 if Size(K)>1000 then
  return ForAny(ConjugacyClassesMaximalSubgroups(K),p->Size(Representative(p))=Size(H) and RepresentativeAction(K,H,Representative(p),OnPoints)<>fail);
 fi;
 hom:=ActionHomomorphism(K,RightCosets(K,H),OnRight);
 return IsPrimitive(Image(hom),[1..ix]);
end;
OvergroupsFromInclusions:=function(H,inclusions)
 local ans,N,p,c;
 ans:=[];N:=Normalizer(G,H);
 for p in inclusions do
  if Size(p[2])=Size(H) then
   c:=RepresentativeAction(G,p[2],H,OnPoints);
   if c<>fail then UniteSet(ans,Orbit(N,p[1]^c,OnPoints));fi;
  fi;
 od;
 return ans;
end;
JoinPanels:=function(B,panels)
 local K,P;
 K:=B;
 for P in panels do K:=ClosureGroup(K,P);od;
 return K;
end;
FlagTransitive:=function(K,pars)
 local i,j,J,other,T,candidates,expected,rows;
 for i in [1..Length(pars)] do
  other:=Difference([1..Length(pars)],[i]);rows:=[];
  for j in other do
   T:=Intersection(pars[i],pars[j]);
   rows[j]:=Set(List(RightTransversal(pars[j],T),x->RightCoset(pars[i],x)));
  od;
  for J in Combinations(other) do
   if Length(J)<2 then continue;fi;
   candidates:=Intersection(List(J,j->rows[j]));
   T:=Intersection(List(J,j->pars[j]));
   expected:=Index(T,Intersection(T,pars[i]));
   if Length(candidates)<>expected then return false;fi;
  od;
 od;
 return true;
end;
# Exact general partial-linear-space test: no local two-transitivity assumed.
# Any four-cycle can be moved to one through the base incident pair (P,Q).
# The remaining pair of P-cosets is classified by B double cosets in Q.
RankTwoAdmissible:=function(B,P,Q)
 local K,x,left,right,dc;
 if Intersection(P,Q)<>B then return fail;fi;
 K:=ClosureGroup(P,Q);
 if not (IsMaxPair(K,P) or IsMaxPair(K,Q)) then return fail;fi;
 if Size(P)*Size(Q)<>Size(K)*Size(B) then
  left:=Set(List(RightTransversal(P,B),h->RightCoset(Q,h)));
  for dc in DoubleCosets(Q,B,B) do
   x:=Representative(dc);
   if not x in B then
    right:=Set(List(RightTransversal(P,B),h->RightCoset(Q,h*x)));
    if Length(Intersection(left,right))<>1 then return fail;fi;
   fi;
  od;
 fi;
 return K;
end;
ValidPanels:=function(B,panels)
 local n,ss,subs,S,T,U;
 n:=Length(panels);ss:=Combinations([1..n]);subs:=List(ss,S->JoinPanels(B,panels{S}));
 for S in [1..Length(ss)] do
  for T in [S+1..Length(ss)] do
   U:=Position(ss,Intersection(ss[S],ss[T]));
   if Intersection(subs[S],subs[T])<>subs[U] then return false;fi;
  od;
  if Length(ss[S])>=2 and not ForAny(ss[S],i->IsMaxPair(subs[S],subs[Position(ss,Difference(ss[S],[i]))])) then return false;fi;
 od;
 for S in ss do
  if Length(S)>=3 then
   U:=subs[Position(ss,S)];
   if not FlagTransitive(U,List(S,i->subs[Position(ss,Difference(S,[i]))])) then return false;fi;
  fi;
 od;
 return true;
end;
RunBorel:=function(bid)
 local B,N,panels,hom,A,orders,paircache,PairJoin,Equivalent,levels,rank,next,sigs,checked,ix,t,H,C,over,poss,orb,oo,x,u,K,sig,bucket,allFull,checkpoint,maxrank;
 B:=reps[bid];N:=Normalizer(G,B);if REQUIRE_2T then panels:=OvergroupsFromInclusions(B,local2T);
 else panels:=OvergroupsFromInclusions(B,maxinclusions);fi;
 Print("BOREL_BEGIN id=",bid," order=",Size(B)," normalizer=",Size(N)," panels=",Length(panels),"\n");
 if Length(panels)=0 then
  PrintTo(Concatenation(OUTPUT_DIR,"/b",String(bid),"_done.g"),"borelResult:=rec(id:=",bid,",order:=",Size(B),",levels:=[],geometries:=[]);\n");
  Print("BOREL_COMPLETE id=",bid," rank_counts=[] full_group=[]\n");return;
 fi;
 hom:=ActionHomomorphism(N,panels,OnPoints);A:=Image(hom);orders:=List(panels,Size);paircache:=[];
 PairJoin:=function(i,j)
  local l,h,K;
  l:=Minimum(i,j);h:=Maximum(i,j);
  if not IsBound(paircache[l]) then paircache[l]:=[];fi;
  if not IsBound(paircache[l][h]) then paircache[l][h]:=RankTwoAdmissible(B,panels[l],panels[h]);fi;
  return paircache[l][h];
 end;
 Equivalent:=function(a,b)
  local p,ord,g,C,x,i;
  for p in SymmetricGroup(Length(a)) do
   ord:=Permuted(b,p);
   if orders{a}<>orders{ord} then continue;fi;
   if not ForAll(Combinations([1..Length(a)],2),ij->Size(PairJoin(a[ij[1]],a[ij[2]]))=Size(PairJoin(ord[ij[1]],ord[ij[2]]))) then continue;fi;
   g:=();C:=A;
   for i in [1..Length(a)] do
    x:=RepresentativeAction(C,a[i]^g,ord[i]);
    if x=fail then break;fi;
    g:=g*x;C:=Stabilizer(C,ord[i]);
   od;
   if x<>fail then return true;fi;
  od;
  return false;
 end;
 levels:=[List(Orbits(A,[1..Length(panels)]),o->[o[1]])];allFull:=[];
 Print("BOREL_LEVEL id=",bid," rank=1 classes=",Length(levels[1])," full_group=",Number(levels[1],t->panels[t[1]]=G),"\n");
 for t in levels[1] do if panels[t[1]]=G then Add(allFull,[panels[t[1]]]);fi;od;
 maxrank:=Length(FactorsInt(Index(G,B)))+1;
 for rank in [2..maxrank] do
  next:=[];sigs:=[];checked:=0;
  for ix in [1..Length(levels[rank-1])] do
   t:=levels[rank-1][ix];H:=JoinPanels(B,panels{t});C:=A;
   for x in t do C:=Stabilizer(C,x);od;
   over:=OvergroupsFromInclusions(H,maxinclusions);
   poss:=Filtered([1..Length(panels)],x->not IsSubgroup(H,panels[x]) and ForAny(over,K->IsSubgroup(K,panels[x])) and ForAll(t,y->PairJoin(x,y)<>fail));
   orb:=Orbits(C,poss);
   for oo in orb do
    x:=oo[1];u:=Concatenation(t,[x]);K:=First(over,K->IsSubgroup(K,panels[x]));checked:=checked+1;
    sig:=[Size(K),SortedList(orders{u}),SortedList(List(Combinations(u,2),ij->Size(PairJoin(ij[1],ij[2]))))];
    bucket:=Filtered([1..Length(next)],i->sigs[i]=sig);
    if ForAny(bucket,i->Equivalent(next[i],u)) then continue;fi;
    if not ValidPanels(B,panels{u}) then continue;fi;
    Add(next,u);Add(sigs,sig);
    if K=G then Add(allFull,panels{u});fi;
   od;
   if ix mod 10=0 or ix=Length(levels[rank-1]) then Print("BOREL_PROGRESS id=",bid," rank=",rank," anchor=",ix,"/",Length(levels[rank-1])," checked=",checked," accepted=",Length(next),"\n");fi;
  od;
  levels[rank]:=next;
  Print("BOREL_LEVEL id=",bid," rank=",rank," classes=",Length(next)," full_group=",Number(next,t->JoinPanels(B,panels{t})=G),"\n");
  checkpoint:=Concatenation(OUTPUT_DIR,"/b",String(bid),"_r",String(rank),".g");
  PrintTo(checkpoint,"borelCheckpoint:=rec(id:=",bid,",order:=",Size(B),",rank:=",rank,",panels:=",panels,",level:=",next,",geometries:=",allFull,");\n");
  if Length(next)=0 then break;fi;
 od;
 if Length(levels[Length(levels)])<>0 then Error("chain bound reached without an empty level");fi;
 PrintTo(Concatenation(OUTPUT_DIR,"/b",String(bid),"_done.g"),"borelResult:=rec(id:=",bid,",order:=",Size(B),",levels:=",List(levels,Length),",geometries:=",allFull,");\n");
 Print("BOREL_COMPLETE id=",bid," rank_counts=",List(levels,Length)," full_group_ranks=",List(allFull,Length),"\n");
end;
if not IsBound(BOREL_IDS) then BOREL_IDS:=[1..Length(reps)];fi;
for bid in BOREL_IDS do RunBorel(bid);od;
Print("SEARCH_COMPLETE borel_ids=",BOREL_IDS," CPU_RUNTIME_MS=",Runtime(),"\n");

