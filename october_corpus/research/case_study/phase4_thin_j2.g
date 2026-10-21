# Exhaustive thin RWPRI geometry search by maximal-residue augmentation.
# Completeness imports TomLib subgroup classes and maximal-inclusion classes.
# Every candidate is independently checked for the exact geometry conditions.
LoadPackage("tomlib");;
SetInfoLevel(InfoWarning,0);;
tom:=TableOfMarks("J2");; G:=UnderlyingGroup(tom);;
reps:=List([1..Length(OrdersTom(tom))],i->RepresentativeTom(tom,i));;
maxorders:=[];;maxinclusions:=[];;
for K in reps do
 k:=Size(K);
 if not IsBound(maxorders[k]) then maxorders[k]:=[];fi;
 if k>1 then
  mm:=List(ConjugacyClassesMaximalSubgroups(K),Representative);
  UniteSet(maxorders[k],Set(List(mm,Size)));
  for H in mm do Add(maxinclusions,[K,H]);od;
 fi;
od;
ivclasses:=Filtered(ConjugacyClasses(G),c->Order(Representative(c))=2);;
invs:=Set(Concatenation(List(ivclasses,AsList)));;
Print("involutions=",Length(invs)," classes=",Length(ivclasses),"\n");
IsMaxPair:=function(K,H)
 local ix,hom,p;
 if not Size(H) in maxorders[Size(K)] then return false;fi;
 if Size(K)=Size(G) then
  return ForAny(maxinclusions,p->Size(p[1])=Size(G) and Size(p[2])=Size(H) and RepresentativeAction(G,H,p[2],OnPoints)<>fail);
 fi;
 ix:=Index(K,H);
 if IsPrimeInt(ix) then return true;fi;
 hom:=ActionHomomorphism(K,RightCosets(K,H),OnRight);
 return IsPrimitive(Image(hom),[1..ix]);
end;
# Ordered conjugacy reduces to successive centralizers; full type permutations follow.
Equivalent:=function(a,b)
 local p,ord,g,h,C,x,i;
 for p in SymmetricGroup(Length(a)) do
  ord:=Permuted(b,p);
  if ForAll([1..Length(a)],i->CycleStructurePerm(a[i])=CycleStructurePerm(ord[i])) and
    ForAll(Combinations([1..Length(a)],2),ij->Order(a[ij[1]]*a[ij[2]])=Order(ord[ij[1]]*ord[ij[2]])) then
   g:=();C:=G;
   for i in [1..Length(a)] do
    x:=RepresentativeAction(C,a[i]^g,ord[i]);
    if x=fail then break;fi;
    g:=g*x; C:=Centralizer(C,ord[i]);
   od;
   if x<>fail then return true;fi;
  fi;
 od;
 return false;
end;
Signature:=function(t)
 return [Size(Group(t)),SortedList(List(Combinations([1..Length(t)],2),ij->Order(t[ij[1]]*t[ij[2]]))),SortedList(List(t,CycleStructurePerm))];
end;
FlagTransitive:=function(K,pars)
 local i,j,J,other,sets,T,candidates,expected,rows;
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
ValidThin:=function(t)
 local n,ss,subs,S,T,U,pars;
 n:=Length(t);ss:=Combinations([1..n]);subs:=List(ss,S->Group(Concatenation([()],t{S})));
 for S in [1..Length(ss)] do
  for T in [S+1..Length(ss)] do
   U:=Position(ss,Intersection(ss[S],ss[T]));
   if Intersection(subs[S],subs[T])<>subs[U] then return false;fi;
  od;
  if Length(ss[S])>=2 and not ForAny(ss[S],i->IsMaxPair(subs[S],subs[Position(ss,Difference(ss[S],[i]))])) then return false;fi;
 od;
 pars:=List([1..n],i->Group(t{Difference([1..n],[i])}));
 # All proper residues have passed by the subset loop plus recursive FT below.
 for S in ss do
  if Length(S)>=3 then
   U:=Group(t{S});
   if not FlagTransitive(U,List(S,i->Group(t{Difference(S,[i])}))) then return false;fi;
  fi;
 od;
 return true;
end;
MaximalOvergroups:=function(H)
 local ans,N,p,c;
 ans:=[];N:=Normalizer(G,H);
 for p in maxinclusions do
  if Size(p[2])=Size(H) then
   c:=RepresentativeAction(G,p[2],H,OnPoints);
   if c<>fail then UniteSet(ans,Orbit(N,p[1]^c,OnPoints));fi;
  fi;
 od;
 return ans;
end;
RunThin:=function()
 local levels,rank,next,sigs,checked,prepass,ix,t,H,C,over,poss,orb,oo,x,u,K,sig,bucket;
 levels:=[List(ivclasses,c->[Representative(c)])];
for rank in [2..14] do
 next:=[];sigs:=[]; checked:=0; prepass:=0;
 for ix in [1..Length(levels[rank-1])] do
  t:=levels[rank-1][ix];H:=Group(t);C:=Centralizer(G,H);
  over:=MaximalOvergroups(H);
  poss:=Filtered(invs,x->not x in H and ForAll(t,y->IsPrimeInt(Order(x*y))) and ForAny(over,K->x in K));
  orb:=Orbits(C,poss);
  for oo in orb do
   x:=oo[1];u:=Concatenation(t,[x]);K:=First(over,K->x in K);checked:=checked+1;
   sig:=[Size(K),SortedList(List(Combinations([1..Length(u)],2),ij->Order(u[ij[1]]*u[ij[2]]))),SortedList(List(u,CycleStructurePerm))];
   bucket:=Filtered([1..Length(next)],i->sigs[i]=sig);
   if ForAny(bucket,i->Equivalent(next[i],u)) then continue;fi;
   if not ValidThin(u) then continue;fi;
   Add(next,u);Add(sigs,sig);prepass:=prepass+1;
  od;
  Print("rank=",rank," anchor=",ix,"/",Length(levels[rank-1])," overgroups=",Length(over)," checked=",checked," accepted=",Length(next),"\n");
 od;
 levels[rank]:=next;
 Print("LEVEL_DONE rank=",rank," classes=",Length(next)," J2=",Number(next,t->Size(Group(t))=Size(G))," orders=",Collected(List(next,t->Size(Group(t)))),"\n");
 PrintTo(Concatenation("research/leemans/phase4_thin_rank",String(rank),".g"),"thinLevel:=",next,";\n");
 if Length(next)=0 then Print("EXHAUSTION_COMPLETE\n");break;fi;
od;
return levels;
end;
levels:=RunThin();;
Print("INPUT subgroup_classes=",Length(reps)," maximal_inclusion_classes=",Length(maxinclusions)," GAP=",GAPInfo.Version," TomLib=",PackageInfo("tomlib")[1].Version,"\n");
Print("CPU_RUNTIME_MS=",Runtime(),"\n");
QUIT;
