# Exact bounded normal-kernel census, preserving the universal marking.
# Small-kernel IP recognition is justified in phase21_kernel_ladder.md.
# Every passing quotient is then checked by direct full-group intersections.
# Set rank21 before Read(...) to choose rank 3, 4, or 5. No catalogue.
# Every candidate kernel is reached through all G-invariant index-two steps;
# no alpha/beta pattern or expected census count is used as a filter.
if LoadPackage("nq")=fail then Error("NQ required");fi;
if not IsBound(rank21) then rank21:=3;fi;
SizeScreen([240,40]);;
Run21:=function(d)
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
 Q:=F/rel;epi:=NqEpimorphismNilpotentQuotient(Q,5);
 iso:=IsomorphismPcGroup(Image(epi));G:=Image(iso);
 r:=List(GeneratorsOfGroup(Q),x->Image(iso,Image(epi,x)));
 lc:=LowerCentralSeries(G);K:=lc[3];pc:=Pcgs(G);pcweights:=List([1..Length(pc)],t->2^(t-1));
 if not ForAll(RelativeOrders(pc),n->n=2) then Error("Binary canonical-pcgs key requires relative orders two");fi;
 if Index(G,K)<>2^(2*d-1) or not IsAbelian(K) then Error("Universal gamma3");fi;
 key:=function(H)
  return List(CanonicalPcgs(InducedPcgsByGenerators(pc,GeneratorsOfGroup(H))),
   x->ExponentsOfPcElement(pc,x)*pcweights);
 end;
 Print("VERSION GAP=",GAPInfo.Version," NQ=",PackageInfo("nq")[1].Version,"\n");
 Print("UNIVERSAL rank=",d," order=",Size(G)," gamma3=",Size(K)," type=",AbelianInvariants(K),"\n");
 levels:=[K];start:=Runtime();
 for k in [1..3] do
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
  if IsBound(checkpoint21) then
   checkpointName:=Concatenation(checkpoint21,".level",String(k),".json");
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
  # The kernel quotient has order eight, independent of ambient |U|.
  qp:=NaturalHomomorphismByNormalSubgroup(K,N);kg:=Image(qp);
  if Size(kg)<>8 then Error("Small kernel quotient");fi;
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
   rejectedProfiles:=rejectedProfiles+1;at:=at+1;
   if at mod 100=0 then Print("PROFILE_PROGRESS candidates=",at,"/",totalCandidates," accepted=",accepted," elapsed_ms=",Runtime()-start,"\n");fi;
   continue;
  fi;
  pi:=NaturalHomomorphismByNormalSubgroup(G,N);Q:=Image(pi);
  f:=List(r,x->Image(pi,x));
  if Size(Q)<>2^(2*d+2) or Subgroup(Q,f)<>Q then Error("Candidate order/marking");fi;
  pars:=List(ss,S->Subgroup(Q,f{S}));good:=true;
  for i in [1..Length(ss)] do for j in [1..Length(ss)] do
   pos:=Position(ss,Intersection(ss[i],ss[j]));
   if Intersection(pars[i],pars[j])<>pars[pos] then good:=false;fi;
   allChecks:=allChecks+1;
  od;od;
  if good then
   accepted:=accepted+1;Add(acceptedKernels,key(N));
   if Image(rev,N)=N then selfdual:=selfdual+1;fi;
   typ:=List([1..d-1],i->Order(f[i]*f[i+1]));
   if Minimum(typ)<4 then Error("Degenerate marking escaped canonical quotient");fi;
   kernelType:=AbelianInvariants(Image(pi,K));
   Add(hist,[Length(LowerCentralSeries(Q))-1,kernelType]);
   typekey:=Minimum(typ,Reversed(typ));Add(typcounts,typekey);
   if Image(rev,N)=N then Add(acceptedSelfTypes,typekey);fi;
   facetOrders:=[Size(Subgroup(Q,f{[1..d-1]})),Size(Subgroup(Q,f{[2..d]}))];
   Add(acceptedDetails,[key(N),typ,Length(LowerCentralSeries(Q))-1,kernelType,Image(rev,N)=N,facetOrders]);
  else Error("Kernel-profile and actual-IP criteria disagree");fi;
  at:=at+1;
  if at mod 100=0 then Print("IP_PROGRESS candidates=",at,"/",totalCandidates," accepted=",accepted," elapsed_ms=",Runtime()-start,"\n");fi;
 od;
 dualclasses:=(accepted+selfdual)/2;
 Print("RESULT rank=",d," candidates=",totalCandidates," ordered=",accepted," selfdual=",selfdual," up_to_reversal=",dualclasses," actual_meets=",allChecks," elapsed_ms=",Runtime()-start,"\n");
 Print("CLASS_KERNEL_HISTOGRAM ",Collected(hist),"\n");
 Print("ORDERED_CANONICAL_TYPE_HISTOGRAM ",Collected(typcounts),"\n");
 Print("SELFDUAL_TYPE_HISTOGRAM ",Collected(acceptedSelfTypes),"\n");
 Print("KERNEL_PROFILE_CHECKS comparisons=",kchecks," rejected=",rejectedProfiles," directly_verified=",accepted,"\n");
 if IsBound(checkpoint21) then
  PrintTo(Concatenation(checkpoint21,".accepted.json"),acceptedDetails,"\n");
 fi;
 Print("PASS: exact bounded normal-index-eight kernel enumeration and actual-IP test; small-kernel recognition and full-IP cross-check agree; no all-rank formula asserted.\n");
 return rec(rank:=d,ordered:=accepted,selfdual:=selfdual,dualclasses:=dualclasses,kernel_keys:=acceptedKernels);
end;;
result21:=Run21(rank21);;
QUIT;
