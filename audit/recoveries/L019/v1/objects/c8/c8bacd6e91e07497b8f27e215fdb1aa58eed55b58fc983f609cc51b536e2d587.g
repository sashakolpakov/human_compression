Read("models.g");;
RunBoundary:=function()
 local models,expected,target,sym,mid,survivors,rows,ci,a,d,bs,cs,tr,paired,b,c,t,counts,i,orbs,count,x,g,subs,groups,checks,I,J,K,H,tailOrbits,anchorCentralizer;
models:=List(rawModels,row->List(row,PermList));;expected:=Set(List(rawExpected,row->List(row,PermList)));;target:=List(rawTarget,PermList);;
sym:=SymmetricGroup(9);;mid:=Filtered(Elements(Stabilizer(Stabilizer(sym,1),9)),x->Order(x)=2);;
if Length(mid)<>231 then Error("middle census");fi;
survivors:=[];;rows:=[];;
for ci in[1..Length(models)]do
 a:=models[ci][1];d:=models[ci][2];bs:=Filtered(mid,x->x*d=d*x);cs:=Filtered(mid,x->x*a=a*x);tr:=0;paired:=0;
 for b in bs do for c in cs do
  t:=[a,b,c,d];if Length(Set(t))<>4 or not IsTransitive(Group(t),[1..9])then continue;fi;tr:=tr+1;
  counts:=[];
  for i in[1..4]do
   orbs:=Orbits(Group(t{Difference([1..4],[i])}),[1..9]);count:=0;
   for x in[1..9]do if x<x^t[i]and PositionProperty(orbs,o->x in o)<>PositionProperty(orbs,o->x^t[i]in o)then count:=count+1;fi;od;
   Add(counts,count);
  od;
  if Minimum(counts)>=2 then Add(survivors,t);paired:=paired+1;fi;
 od;od;
 Add(rows,[Length(bs),Length(cs),tr,paired]);
od;
if Set(survivors)<>expected then Error("literal survivor sets differ");fi;
g:=Group(target);;if g<>AlternatingGroup(9)then Error("actual natural A9");fi;
subs:=Combinations([1..4]);;groups:=List(subs,I->Group(Concatenation([()],target{I})));;checks:=0;;
for I in[1..Length(subs)]do for J in[1..Length(subs)]do
 K:=Position(subs,Intersection(subs[I],subs[J]));if Intersection(groups[I],groups[J])<>groups[K]then Error("full subset IP");fi;checks:=checks+1;
od;od;
H:=Group(target{[2..4]});;tailOrbits:=Set(List(Orbits(H,[1..9]),Set));;if tailOrbits<>[[1],[2,3],[4,5,6,7,8,9]]then Error("literal tail orbits");fi;
anchorCentralizer:=Stabilizer(Stabilizer(Centralizer(sym,H),1),9);;if anchorCentralizer<>Group((2,3))then Error("literal anchored centralizer");fi;
Print("EXACT_ROWS ",rows,"\n");Print("ACTUAL_GROUP_ORDER ",Size(g)," SUBSET_PAIRS ",checks,"\n");Print("TAIL_ORBITS ",tailOrbits," CENTRALIZER ",Elements(anchorCentralizer),"\n");Print("COMPLETE_DEGREE9_BOUNDARY_CONTROL\n");end;;
RunBoundary();;QUIT;
