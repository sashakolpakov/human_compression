# Generic rank-two RWPRI census from named GAP TomLib subgroup datasets.
# require2T selects locally two-transitive actions; requireIP2 adds partial linearity/digon.
# The one-common-neighbor IP2 shortcut is used only when require2T=true.
LoadPackage("tomlib");;
RunRank2:=function(name,require2T,requireIP2)
 local tom,G,reps,maxs,PairAction,classes,localpairs,H,T,K,S,c,N,M,cand,orb,other,good,i,j,pair,ConjugatePair,ips,hh,xx,a,b,common,isDigon,A,AutoSub,AutoPair,autoclasses,recp,stats,outfile,degree;
 if requireIP2 and not require2T then Error("IP2 shortcut requires local two-transitivity"); fi;
 tom:=TableOfMarks(name);
 if tom=fail then Error("required subgroup dataset unavailable");fi;
 G:=UnderlyingGroup(tom);
 reps:=List([1..Length(OrdersTom(tom))],i->RepresentativeTom(tom,i));
 maxs:=List(ConjugacyClassesMaximalSubgroups(G),Representative);
 Print("dataset=GAP_TomLib_",name," |G|=",Size(G)," class_reps=",Length(reps)," maximal_classes=",Length(maxs),"\n");
 # Cache all locally 2-transitive maximal-subgroup inclusions in proper K.
 localpairs:=[];
 for K in reps do
  if Size(K)>1 and Size(K)<Size(G) then
   for S in List(ConjugacyClassesMaximalSubgroups(K),Representative) do
    if not require2T or Length(DoubleCosets(K,S,S))=2 then Add(localpairs,[K,S]);fi;
   od;
  fi;
 od;
 Print("accepted_local_inclusion_classes=",Length(localpairs),"\n");
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
   if not require2T or Length(DoubleCosets(H,T,T))=2 then
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
 Print("RWPRI_with_local_filter_unordered_Gclasses=",Length(classes),"\n");
 ips:=[];
 for pair in classes do
  H:=pair[1];K:=pair[2];T:=Intersection(H,K);
  if not requireIP2 then Add(ips,pair); continue;fi;
  xx:=First(GeneratorsOfGroup(K),x->not x in T);
  hh:=RightTransversal(H,T);
  a:=Set(List(hh,h->RightCoset(K,h)));
  b:=Set(List(hh,h->RightCoset(K,h*xx)));
  common:=Length(Intersection(a,b));
  isDigon:=Size(H)*Size(K)=Size(G)*Size(T);
  Print("pair_orders=",[Size(H),Size(K),Size(T)]," common_neighbors=",common," digon=",isDigon," IP2=",common=1 or isDigon,"\n");
  if common=1 or isDigon then Add(ips,pair);fi;
 od;
 Print("after_IP2_filter_unordered_Gclasses=",Length(ips),"\n");
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
 Print("final_unordered_AutGclasses=",Length(autoclasses)," |AutG|=",Size(A),"\n");
 Print("canonical_order_summaries=",List(autoclasses,p->[Size(p[1]),Size(p[2]),Size(Intersection(p[1],p[2]))]),"\n");
 outfile:=Concatenation("research/leemans/classification_",Filtered(name,c->IsAlphaChar(c) or IsDigitChar(c)),"_representatives.json");
 degree:=LargestMovedPoint(G);
 PrintTo(outfile,"{\"group\":\"",name,"\",\"order\":",Size(G),",\"degree\":",degree,",\"tom_subgroup_classes\":",Length(reps),",\"local_inclusion_classes\":",Length(localpairs),",\"require_2transitive\":",require2T,",\"require_IP2\":",requireIP2,",\"ambient_generators\":",List(GeneratorsOfGroup(G),p->ListPerm(p,degree)),",\"representatives\":[");
 for i in [1..Length(autoclasses)] do
  pair:=autoclasses[i];
  if i>1 then AppendTo(outfile,",");fi;
  AppendTo(outfile,"{\"orders\":",[Size(pair[1]),Size(pair[2]),Size(Intersection(pair[1],pair[2]))],",\"H_generators\":",List(GeneratorsOfGroup(pair[1]),p->ListPerm(p,degree)),",\"K_generators\":",List(GeneratorsOfGroup(pair[2]),p->ListPerm(p,degree)),"}");
 od;
 AppendTo(outfile,"]}\n");
 if name="J2" and Length(autoclasses)<>8 then Error("J2 published census mismatch");fi;
 if name="Sz(8)" and Length(autoclasses)<>29 then Error("Sz8 published census mismatch");fi;
 Print("REPRODUCTION_PASS ",name,"\n");

end;
RunRank2("J2",true,true);
RunRank2("Sz(8)",false,false);
QUIT;
