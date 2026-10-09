# Rank-two RWPRI/(2T)_1/(IP)_2 census from an explicitly named subgroup dataset.
# Completeness input: GAP TomLib J2 table, 146 subgroup conjugacy classes.
LoadPackage("tomlib");;
RunJ2:=function()
 local tom,G,reps,maxs,PairAction,classes,localpairs,H,T,K,S,c,N,M,cand,orb,other,good,i,j,pair,ConjugatePair,ips,hh,xx,a,b,common,isDigon,A,AutoSub,AutoPair,autoclasses,recp,stats;
 tom:=TableOfMarks("J2"); G:=UnderlyingGroup(tom);
 reps:=List([1..Length(OrdersTom(tom))],i->RepresentativeTom(tom,i));
 maxs:=List(ConjugacyClassesMaximalSubgroups(G),Representative);
 Print("dataset=GAP_TomLib_J2 |G|=",Size(G)," class_reps=",Length(reps)," maximal_classes=",Length(maxs),"\n");
 # Cache all locally 2-transitive maximal-subgroup inclusions in proper K.
 localpairs:=[];
 for K in reps do
  if Size(K)>1 and Size(K)<Size(G) then
   for S in List(ConjugacyClassesMaximalSubgroups(K),Representative) do
    if Length(DoubleCosets(K,S,S))=2 then Add(localpairs,[K,S]);fi;
   od;
  fi;
 od;
 Print("local_2transitive_inclusion_classes=",Length(localpairs),"\n");
 ConjugatePair:=function(p1,p2)
  local ord,g,n;
  for ord in [p2,Reversed(p2)] do
   if Size(p1[1])=Size(ord[1]) and Size(p1[2])=Size(ord[2]) then
    g:=RepresentativeAction(G,p1[1],ord[1],OnPoints);
    if g<>fail then
     n:=RepresentativeAction(Normalizer(G,ord[1]),p1[2]^g,ord[2],OnPoints);
     if n<>fail then return true;fi;
    fi;
   fi;
  od;
  return false;
 end;
 classes:=[];
 for H in maxs do
  for T in List(ConjugacyClassesMaximalSubgroups(H),Representative) do
   if Length(DoubleCosets(H,T,T))=2 then
    N:=Normalizer(G,T); M:=Intersection(N,Normalizer(G,H)); cand:=[];
    for pair in localpairs do
     K:=pair[1];S:=pair[2];
     if Size(S)=Size(T) then
      c:=RepresentativeAction(G,S,T,OnPoints);
      if c<>fail then
       UniteSet(cand,Orbit(N,K^c,OnPoints));
      fi;
     fi;
    od;
    cand:=Filtered(cand,K->not IsSubgroup(H,K));
    orb:=Orbits(M,cand,OnPoints);
    Print("anchor H=",Size(H)," T=",Size(T)," N=",Size(N)," raw=",Length(cand)," orbits=",Length(orb),"\n");
    for other in orb do
     K:=other[1];
     if Size(Intersection(H,K))<>Size(T) or Size(ClosureGroup(H,K))<>Size(G) then Error("recognition theorem check failed"); fi;
     pair:=[H,K];
     if not ForAny(classes,p->ConjugatePair(p,pair)) then Add(classes,pair);fi;
    od;
   fi;
  od;
 od;
 Print("RWPRI_2T_unordered_Gclasses=",Length(classes),"\n");
 ips:=[];
 for pair in classes do
  H:=pair[1];K:=pair[2];T:=Intersection(H,K);
  xx:=First(GeneratorsOfGroup(K),x->not x in T);
  hh:=RightTransversal(H,T);
  a:=Set(List(hh,h->RightCoset(K,h)));
  b:=Set(List(hh,h->RightCoset(K,h*xx)));
  common:=Length(Intersection(a,b));
  isDigon:=Size(H)*Size(K)=Size(G)*Size(T);
  Print("pair_orders=",[Size(H),Size(K),Size(T)]," common_neighbors=",common," digon=",isDigon," IP2=",common=1 or isDigon,"\n");
  if common=1 or isDigon then Add(ips,pair);fi;
 od;
 Print("IP2_unordered_Gclasses=",Length(ips),"\n");
 # Inner-conjugacy representatives are now fused by the full automorphism group.
 A:=AutomorphismGroup(G);
 AutoSub:=function(H,a) return Image(a,H);end;
 AutoPair:=function(p1,p2)
  local ord,g,n;
  for ord in [p2,Reversed(p2)] do
   if Size(p1[1])=Size(ord[1]) and Size(p1[2])=Size(ord[2]) then
    g:=RepresentativeAction(A,p1[1],ord[1],AutoSub);
    if g<>fail then
     n:=RepresentativeAction(Stabilizer(A,ord[1],AutoSub),Image(g,p1[2]),ord[2],AutoSub);
     if n<>fail then return true;fi;
    fi;
   fi;
  od;
  return false;
 end;
 autoclasses:=[];
 for pair in ips do
  if not ForAny(autoclasses,p->AutoPair(p,pair)) then Add(autoclasses,pair);fi;
 od;
 Print("IP2_unordered_AutGclasses=",Length(autoclasses)," |AutG|=",Size(A),"\n");
 Print("canonical_order_summaries=",List(autoclasses,p->[Size(p[1]),Size(p[2]),Size(Intersection(p[1],p[2]))]),"\n");
end;
RunJ2();
QUIT;
