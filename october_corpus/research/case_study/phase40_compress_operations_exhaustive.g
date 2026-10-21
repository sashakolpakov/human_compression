# Complete finite J1 geometry census by proper-residue extension.
# Relative to the complete TomLib J1 subgroup table, not a geometry census.
LoadPackage("tomlib");;
SizeScreen([100000,24]);;
tom:=TableOfMarks("J1");;G:=UnderlyingGroup(tom);;
ids:=MaximalSubgroupsTom(tom)[1];;
ns:=Length(OrdersTom(tom));; incidence:=SubsTom(tom);;
derived:=Filtered([1..ns-1],i->not ForAny([i+1..ns-1],j->i in incidence[j]));;
if derived<>SortedList(ids) or ns<>40 then Error("maximal subgroup catalogue");fi;
Print("MAXIMAL_CLASSES ",derived," ORDERS ",List(ids,i->Size(RepresentativeTom(tom,i))),"\n");;
CheckCensus:=function(t)
 local n,I,i,j,k,K,L,ss,subs,P,rows,J,common,T;
 n:=Length(t); I:=[1..n];
 # Irredundance is necessary for IP and rejects most global extensions.
 for i in I do
  K:=Group(t{Difference(I,[i])});
  if t[i] in K then return fail;fi;
 od;
 ss:=Combinations(I);
 subs:=List(ss,J->Group(Concatenation([()],t{J})));
 for i in [1..Length(ss)] do for j in [i+1..Length(ss)] do
  if Intersection(subs[i],subs[j])<>subs[Position(ss,Intersection(ss[i],ss[j]))]
   then return fail;fi;
 od;od;
 P:=List(I,i->Group(t{Difference(I,[i])}));
 for i in I do
  rows:=[];
  for j in Difference(I,[i]) do
   K:=Intersection(P[i],P[j]);
   rows[j]:=Set(List(RightTransversal(P[j],K),x->RightCoset(P[i],x)));
  od;
  for J in Combinations(Difference(I,[i])) do
   if Length(J)<2 then continue;fi;
   T:=Intersection(P{J});
   if Length(Intersection(rows{J}))<>Index(T,Intersection(T,P[i]))
    then return fail;fi;
  od;
 od;
 return rec(marking:=t,order:=Size(Group(t)),parabolics:=List(P,Size));
end;;
localReps:=rec();;
for k in [3,4] do
 localReps.(String(k)):=[];
 for id in ids do
  M:=RepresentativeTom(tom,id);
  iv:=Filtered(Elements(M),x->Order(x)=2);
  A:=Image(ActionHomomorphism(M,iv,OnPoints));
  oo:=OrbitsDomain(A,Combinations([1..Length(iv)],k),OnSets);
  count:=0;
  for o in oo do
   t:=iv{o[1]}; r:=CheckCensus(t);
   if r<>fail then Add(localReps.(String(k)),t);count:=count+1;fi;
  od;
  Print("LOCAL ",k," MAXIMAL ",id," ORDER ",Size(M)," ORBITS ",Length(oo)," REGULAR ",count,"\n");
 od;
 Print("LOCAL_TOTAL ",k," ",Length(localReps.(String(k))),"\n");
od;
Print("LOCAL_ENUMERATION_DONE\n");
involClasses:=Filtered(ConjugacyClasses(G),c->Order(Representative(c))=2);;
if Length(involClasses)<>1 then Error("single involution class required");fi;
ivG:=SortedList(Elements(involClasses[1]));;
if Length(ivG)<>1463 then Error("involution count");fi;
a0:=ivG[1];; C0:=Elements(Centralizer(G,a0));;
if Length(C0)<>120 then Error("involution centralizer");fi;
conjCache:=[];;
CanonicalCensus:=function(t)
 local ans,x,p,g,c,key;
 ans:=fail;
 for x in t do
  p:=PositionSorted(ivG,x);
  if not IsBound(conjCache[p]) then
   g:=RepresentativeAction(G,x,a0);
   if g=fail or x^g<>a0 then Error("involution conjugator");fi;
   conjCache[p]:=g;
  fi;
  g:=conjCache[p];
  for c in C0 do
   key:=SortedList(List(t,y->PositionSorted(ivG,y^(g*c))));
   if ans=fail or key<ans then ans:=key;fi;
  od;
 od;
 return ans;
end;;
globalClasses:=[];;fiveClasses:=[];;classParabolics:=[];;
for k in [3,4] do
 keys:=[];unique:=[];
 for t in localReps.(String(k)) do
  key:=CanonicalCensus(t);
  if not key in keys then Add(keys,key);Add(unique,t);fi;
 od;
 Print("GLOBAL_LOCAL_ORBITS ",k," ",Length(unique),"\n");
 tested:=0;passed:=0;start:=Runtime();
 for i in [1..Length(unique)] do
  t:=unique[i];K:=Group(t);
  for x in ivG do
   if x in K then continue;fi;
   tested:=tested+1;
   r:=CheckCensus(Concatenation(t,[x]));
   if r=fail then continue;fi;
   if k=3 and r.order<>175560 then continue;fi;
   passed:=passed+1;
   key:=CanonicalCensus(r.marking);
   if k=3 and not key in globalClasses then
    Add(globalClasses,key);Add(classParabolics,SortedList(r.parabolics));
    Print("NEW_RANK4 ",key," PARABOLICS ",SortedList(r.parabolics),"\n");
   elif k=4 and not key in fiveClasses then
    Add(fiveClasses,key);
    Print("NEW_RANK5 ",key," GROUP_ORDER ",r.order," PARABOLICS ",r.parabolics,"\n");
   fi;
  od;
  Print("EXTENSION ",k+1," LOCAL ",i,"/",Length(unique)," TESTED ",tested,
   " PASSED ",passed," SECONDS ",(Runtime()-start)/1000,"\n");
 od;
 Print("STAGE_TOTAL ",k+1," TESTED ",tested," ACCEPTED ",passed,"\n");
od;
Print("RANK4_CLASSES ",Length(globalClasses)," RANK5_CLASSES ",Length(fiveClasses),"\n");
if Length(globalClasses)<>6 or Length(fiveClasses)<>0 then Error("geometry classification");fi;
expected:=[[20,20,60,120],[20,20,120,660],[20,60,60,120],
 [20,60,120,120],[60,60,120,120],[20,120,120,660]];;
if SortedList(classParabolics)<>SortedList(expected) then Error("six distinct types");fi;
PrintTo("phase40_compress_operations_exhaustive_classes.json",
 [globalClasses,fiveClasses,classParabolics],"\n");;
Print("COMPRESS_C_EXHAUSTIVE_PASS\n");
QUIT;
