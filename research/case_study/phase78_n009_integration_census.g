# Complete path-marked two-group census, parameterized by rank and excess.
# Theorems Q5.5/Q5.6 prove candidate completeness and profile recognition.
# Adapted from the reviewed phase21/22 ladder; original markings are preserved.
# Every candidate, including profile rejections, receives all 4^d actual meets.
# Four parameter cases share this program; no source count or name filters it.
# The order-256 case additionally checks the four exact L035 seed word patterns.
# Use a fresh working directory. Existing mathematical output paths are refused.
if LoadPackage("nq")=fail then Error("NQ required");fi;
SizeScreen([240,40]);;
Run78:=function(d,excess78,prefix78)
 local F,f,rel,i,j,Q,epi,iso,G,r,lc,K,pc,key,levels,M,C,pi,V,
  maxes,L,N,known,nxt,k,edges,maxdim,dim,at,start,allChecks,ss,
  pars,good,accepted,hist,typ,kernelType,rev,selfdual,dualclasses,
  acceptedKernels,totalCandidates,gi,gj,pos,typcounts,typekey,
  inds,ambientRows,pcweights,ks,ps,kg,qp,kpars,kchecks,profileGood,
  rejectedProfiles,acceptedSelfTypes,selfTypeKey,facetOrders,facets,
  acceptedDetails,checkpointName,a78,b78,c78,r78,d078,z78,patterns78,seed78;
 if not (d>=3 and excess78>=1) then Error("Rank/excess input");fi;
 for k in [1..excess78] do
  if IsExistingFile(Concatenation(prefix78,".level",String(k),".json")) then Error("Existing checkpoint");fi;
 od;
 if IsExistingFile(Concatenation(prefix78,".accepted.json")) or IsExistingFile(Concatenation(prefix78,".seed.json")) then Error("Existing output");fi;
 seed78:=[];
 F:=FreeGroup(d);f:=GeneratorsOfGroup(F);rel:=List(f,x->x^2);
 for i in [1..d] do for j in [i+1..d] do
  if j-i>1 then Add(rel,Comm(f[i],f[j]));fi;
 od;od;
 Q:=F/rel;epi:=NqEpimorphismNilpotentQuotient(Q,excess78+2);
 iso:=IsomorphismPcGroup(Image(epi));G:=Image(iso);
 r:=List(GeneratorsOfGroup(Q),x->Image(iso,Image(epi,x)));
 lc:=LowerCentralSeries(G);K:=lc[3];pc:=Pcgs(G);pcweights:=List([1..Length(pc)],t->2^(t-1));
 if not ForAll(RelativeOrders(pc),n->n=2) then Error("Binary canonical-pcgs key requires relative orders two");fi;
 if Index(G,K)<>2^(2*d-1) then Error("Universal canonical quotient order");fi;
 key:=function(H)
  return List(CanonicalPcgs(InducedPcgsByGenerators(pc,GeneratorsOfGroup(H))),
   x->ExponentsOfPcElement(pc,x)*pcweights);
 end;
 Print("VERSION GAP=",GAPInfo.Version," NQ=",PackageInfo("nq")[1].Version,"\n");
 Print("UNIVERSAL rank=",d," excess=",excess78," order=",Size(G)," gamma3=",Size(K)," abelianization_type=",AbelianInvariants(K),"\n");
 levels:=[K];start:=Runtime();
 for k in [1..excess78] do
  known:=NewDictionary([],true);nxt:=[];edges:=0;maxdim:=0;at:=0;
  for M in levels do
   C:=ClosureGroup(CommutatorSubgroup(M,G),FrattiniSubgroup(M));
   pi:=NaturalHomomorphismByNormalSubgroup(M,C);V:=Image(pi);
   if not IsElementaryAbelian(V) then Error("Coinvariant square quotient");fi;
   dim:=LogInt(Size(V),2);maxdim:=Maximum(maxdim,dim);
   maxes:=MaximalSubgroups(V);
   if Length(maxes)<>2^dim-1 then Error("All hyperplanes");fi;
   for L in maxes do
    N:=PreImage(pi,L);edges:=edges+1;
    inds:=key(N);
    if LookupDictionary(known,inds)=fail then
     if Index(K,N)<>2^k or not IsNormal(G,N) then Error("Invariant ladder kernel");fi;
     AddDictionary(known,inds,Length(nxt)+1);Add(nxt,N);
    fi;
   od;
   at:=at+1;
   if at mod 100=0 then Print("PROGRESS depth=",k," parents=",at,"/",Length(levels)," unique=",Length(nxt)," elapsed_ms=",Runtime()-start,"\n");fi;
  od;
  Print("LEVEL index=",2^k," parents=",Length(levels)," hyperplane_edges=",edges," unique=",Length(nxt)," max_coinvariant_dimension=",maxdim," elapsed_ms=",Runtime()-start,"\n");
  levels:=nxt;
  if true then
   checkpointName:=Concatenation(prefix78,".level",String(k),".json");
   PrintTo(checkpointName,List(levels,key),"\n");
  fi;
 od;
 # Exact actual-IP checks for every final candidate, including every meet.
 ss:=Combinations([1..d]);allChecks:=0;accepted:=0;selfdual:=0;
 ks:=List(ss,S->Intersection(K,Subgroup(G,r{S})));
 kchecks:=0;rejectedProfiles:=0;acceptedSelfTypes:=[];acceptedDetails:=[];
 acceptedKernels:=[];hist:=[];typcounts:=[];totalCandidates:=Length(levels);
 rev:=GroupHomomorphismByImages(G,G,r,Reversed(r));
 if rev=fail or not IsBijective(rev) then Error("Marked reversal automorphism");fi;
 at:=0;
 for N in levels do
  # The kernel quotient has order 2^excess78 and need not be abelian.
  qp:=NaturalHomomorphismByNormalSubgroup(K,N);kg:=Image(qp);
  if Size(kg)<>2^excess78 then Error("Small kernel quotient");fi;
  kpars:=List(ks,H->Image(qp,H));profileGood:=true;
  for i in [1..Length(ss)] do
   for j in [i+1..Length(ss)] do
    pos:=Position(ss,Intersection(ss[i],ss[j]));
    kchecks:=kchecks+1;
    if Intersection(kpars[i],kpars[j])<>kpars[pos] then profileGood:=false;break;fi;
   od;
   if not profileGood then break;fi;
  od;
  if not profileGood then
   rejectedProfiles:=rejectedProfiles+1;
   if at mod 100=0 then Print("PROFILE_PROGRESS candidates=",at,"/",totalCandidates," accepted=",accepted," elapsed_ms=",Runtime()-start,"\n");fi;
  fi;
  pi:=NaturalHomomorphismByNormalSubgroup(G,N);Q:=Image(pi);
  f:=List(r,x->Image(pi,x));
  if Size(Q)<>2^(2*d-1+excess78) or Subgroup(Q,f)<>Q then Error("Candidate order/marking");fi;
  pars:=List(ss,S->Subgroup(Q,f{S}));good:=true;
  for i in [1..Length(ss)] do for j in [1..Length(ss)] do
   pos:=Position(ss,Intersection(ss[i],ss[j]));
   if Intersection(pars[i],pars[j])<>pars[pos] then good:=false;fi;
   allChecks:=allChecks+1;
  od;od;
  if good<>profileGood then Error("Kernel-profile and actual-IP criteria disagree");fi;
  if good then
   accepted:=accepted+1;Add(acceptedKernels,key(N));
   if Image(rev,N)=N then selfdual:=selfdual+1;fi;
   typ:=List([1..d-1],i->Order(f[i]*f[i+1]));
   if Minimum(typ)<4 then Error("Degenerate marking escaped canonical quotient");fi;
   kernelType:=AbelianInvariants(Image(pi,K)/DerivedSubgroup(Image(pi,K)));
   Add(hist,[Length(LowerCentralSeries(Q))-1,kernelType]);
   typekey:=Minimum(typ,Reversed(typ));Add(typcounts,typekey);
   if Image(rev,N)=N then Add(acceptedSelfTypes,typekey);fi;
   facetOrders:=[Size(Subgroup(Q,f{[1..d-1]})),Size(Subgroup(Q,f{[2..d]}))];
   Add(acceptedDetails,[key(N),typ,Length(LowerCentralSeries(Q))-1,kernelType,Image(rev,N)=N,facetOrders]);
   if d=3 and excess78=3 and typ=[4,8] then
    a78:=f[1];b78:=f[2];c78:=f[3];r78:=b78*c78;d078:=(a78*b78)^2;z78:=r78^4;
    patterns78:=[];
    if Comm(a78,r78^2)^2=One(Q) and Comm(a78,r78^4)=One(Q) then Add(patterns78,1);fi;
    if Comm(a78,r78^2)^2=z78 and Comm(a78,r78^4)=One(Q) then Add(patterns78,2);fi;
    if Comm(d078,r78^2)=z78 then Add(patterns78,3);fi;
    if Comm((r78^2)^a78,r78)=z78 then Add(patterns78,4);fi;
    if Length(patterns78)<>1 then Error("Unclassified or overlapping order-256 word pattern");fi;
    Add(seed78,[key(N),patterns78[1]]);
   fi;
  fi;
  at:=at+1;
  if at mod 100=0 then Print("IP_PROGRESS candidates=",at,"/",totalCandidates," accepted=",accepted," elapsed_ms=",Runtime()-start,"\n");fi;
 od;
 dualclasses:=(accepted+selfdual)/2;
 Print("RESULT rank=",d," excess=",excess78," candidates=",totalCandidates," ordered=",accepted," selfdual=",selfdual," up_to_reversal=",dualclasses," actual_meets=",allChecks," elapsed_ms=",Runtime()-start,"\n");
 Print("CLASS_KERNEL_ABELIANIZATION_HISTOGRAM ",Collected(hist),"\n");
 Print("ORDERED_CANONICAL_TYPE_HISTOGRAM ",Collected(typcounts),"\n");
 Print("SELFDUAL_TYPE_HISTOGRAM ",Collected(acceptedSelfTypes),"\n");
 Print("KERNEL_PROFILE_CHECKS comparisons=",kchecks," rejected=",rejectedProfiles," directly_verified=",accepted,"\n");
 if true then
  PrintTo(Concatenation(prefix78,".accepted.json"),acceptedDetails,"\n");
 fi;
 PrintTo(Concatenation(prefix78,".seed.json"),seed78,"\n");
 if Length(seed78)>0 then Print("SEED_WORD_PATTERNS ",Collected(List(seed78,x->x[2])),"\n");fi;
 Print("PASS: complete invariant-kernel ladder and all-candidate actual-IP cross-check; counts are output, never candidate filters.\n");
 return rec(rank:=d,ordered:=accepted,selfdual:=selfdual,dualclasses:=dualclasses,kernel_keys:=acceptedKernels);
end;;
if not IsBound(cases78) then cases78:=[[3,3],[3,5],[4,3],[5,1]];fi;
results78:=[];
for case78 in cases78 do
 Add(results78,Run78(case78[1],case78[2],Concatenation("phase78_d",String(case78[1]),"_k",String(case78[2]))));
od;
QUIT;
