# Exact bounded normal-kernel census, preserving the universal marking.
# Small-kernel IP recognition is justified in phase22_N009_rank3.md.
# Every candidate quotient, including every profile rejection, is checked by direct full-group intersections.
# Phase22 specialization: rank three, excess five, class at most seven.
# Adapted from the reviewed phase21 invariant-kernel ladder; no catalogue.
# Every candidate kernel is reached through all G-invariant index-two steps;
# no alpha/beta pattern or expected census count is used as a filter.
if LoadPackage("nq")=fail then Error("NQ required");fi;
rank22:=3;
if not IsBound(checkpoint22) then checkpoint22:="phase22_N009_rank3";fi;
SizeScreen([240,40]);;
Run22:=function(d)
 local F,f,rel,i,j,Q,epi,iso,G,r,lc,K,pc,key,levels,M,C,pi,V,
  maxes,L,N,known,nxt,k,edges,maxdim,dim,at,start,allChecks,ss,
  pars,good,accepted,hist,typ,kernelType,rev,selfdual,dualclasses,
  acceptedKernels,totalCandidates,gi,gj,pos,typcounts,typekey,
  inds,ambientRows,pcweights,ks,ps,kg,qp,kpars,kchecks,profileGood,
  rejectedProfiles,acceptedSelfTypes,selfTypeKey,facetOrders,facets,
  acceptedDetails,checkpointName;
 F:=FreeGroup(d);f:=GeneratorsOfGroup(F);rel:=List(f,x->x^2);
 for i in [1..d] do for j in [i+1..d] do
  if j-i>1 then Add(rel,Comm(f[i],f[j]));fi;
 od;od;
 Q:=F/rel;epi:=NqEpimorphismNilpotentQuotient(Q,7);
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
 Print("UNIVERSAL rank=",d," order=",Size(G)," gamma3=",Size(K)," abelianization_type=",AbelianInvariants(K),"\n");
 levels:=[K];start:=Runtime();
 for k in [1..5] do
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
  if IsBound(checkpoint22) then
   checkpointName:=Concatenation(checkpoint22,".level",String(k),".json");
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
  # The kernel quotient has order 32 and need not be abelian.
  qp:=NaturalHomomorphismByNormalSubgroup(K,N);kg:=Image(qp);
  if Size(kg)<>32 then Error("Small kernel quotient");fi;
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
  if Size(Q)<>2^(2*d+4) or Subgroup(Q,f)<>Q then Error("Candidate order/marking");fi;
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
  fi;
  at:=at+1;
  if at mod 100=0 then Print("IP_PROGRESS candidates=",at,"/",totalCandidates," accepted=",accepted," elapsed_ms=",Runtime()-start,"\n");fi;
 od;
 dualclasses:=(accepted+selfdual)/2;
 Print("RESULT rank=",d," candidates=",totalCandidates," ordered=",accepted," selfdual=",selfdual," up_to_reversal=",dualclasses," actual_meets=",allChecks," elapsed_ms=",Runtime()-start,"\n");
 Print("CLASS_KERNEL_ABELIANIZATION_HISTOGRAM ",Collected(hist),"\n");
 Print("ORDERED_CANONICAL_TYPE_HISTOGRAM ",Collected(typcounts),"\n");
 Print("SELFDUAL_TYPE_HISTOGRAM ",Collected(acceptedSelfTypes),"\n");
 Print("KERNEL_PROFILE_CHECKS comparisons=",kchecks," rejected=",rejectedProfiles," directly_verified=",accepted,"\n");
 if IsBound(checkpoint22) then
  PrintTo(Concatenation(checkpoint22,".accepted.json"),acceptedDetails,"\n");
 fi;
 Print("PASS: exact bounded normal-index-32 kernel enumeration and actual-IP test; small-kernel recognition and all-candidate full-IP cross-check agree; no all-rank formula asserted.\n");
 return rec(rank:=d,ordered:=accepted,selfdual:=selfdual,dualclasses:=dualclasses,kernel_keys:=acceptedKernels);
end;;
result22:=Run22(rank22);;
QUIT;
