# Independent geometric decoding of the author witnesses; no source table input.
SizeScreen([100000,24]);;
Read("phase164_m22_witnesses.g");;
moved22:=MovedPoints(G);;fixed:=Difference([1..24],moved22);;
if Length(moved22)<>22 or Length(fixed)<>2 then Error("wrong natural action");fi;
sourceReps:=maximalClassRepresentatives{[1,2,3,4,6,5,7,8]};;
shadowSizes:=[1,6,7,7,8,2,12,11];;
classes:=List(sourceReps,H->Orbit(G,H,OnPoints));;
allM:=Concatenation(classes);;types:=Concatenation(List([1..8],i->List(classes[i],H->i)));;
shadows:=[];;
for i in [1..Length(allM)] do
 choices:=List(Filtered(Orbits(allM[i],moved22),s->Length(s)=shadowSizes[types[i]]),Set);
 if (types[i]=8 and Length(choices)<>2) or (types[i]<>8 and Length(choices)<>1) then Error("wrong shadow multiplicity");fi;
 if not ForAll(choices,s->Stabilizer(G,s,OnSets)=allM[i]) then Error("shadow stabilizer mismatch");fi;
 Add(shadows,choices);
od;
families:=List([1..8],i->Set(Concatenation(shadows{Filtered([1..Length(allM)],j->types[j]=i)})));;
blocks:=Set(Concatenation(List(families[2],s->Union(s,fixed)),List(families[3],s->Union(s,[fixed[1]])),List(families[4],s->Union(s,[fixed[2]])),families[5]));;
fives:=Collected(Concatenation(List(blocks,s->Combinations(s,5))));;
if Length(blocks)<>759 or Length(fives)<>Binomial(24,5) or not ForAll(fives,x->x[2]=1) then Error("not Steiner S(5,8,24)");fi;
dodecads:=[];;
for i in [1..Length(blocks)] do
 for j in [i+1..Length(blocks)] do
  if Length(Intersection(blocks[i],blocks[j]))=2 then AddSet(dodecads,Union(Difference(blocks[i],blocks[j]),Difference(blocks[j],blocks[i])));fi;
 od;
od;
if Filtered(dodecads,s->IsSubset(moved22,s))<>families[7] then Error("dodecad family mismatch");fi;
endecads:=Set(Concatenation(List(fixed,f->List(Filtered(dodecads,s->f in s and Length(Intersection(s,fixed))=1),s->Difference(s,[f])))));;
if endecads<>families[8] then Error("endecad family mismatch");fi;
Print("SHADOW_FAMILIES ",List(families,Length)," STEINER_BLOCKS ",Length(blocks)," FIVE_SUBSETS ",Length(fives)," DODECADS ",Length(dodecads),"\n");
PrintTo("phase164_m22_shadow_data.json","{\"schema\":1,\"triples\":[\n");
for idx in [1..Length(M22Triples)] do
 t:=M22Triples[idx];positions:=List(t,H->Position(allM,H));
 ty:=types{positions};B:=Intersection(t);sigs:=[];
 for perm in PermutationsList([1,2,3]) do
  for sw in [false,true] do
   tt:=ty{perm};
   if sw then tt:=List(tt,x->x^(3,4));fi;
   if tt<>SortedList(tt) then continue;fi;
   for choices in Cartesian(shadows{positions{perm}}) do
    AddSet(sigs,Concatenation(tt,[Length(Intersection(choices[1],choices[2])),Length(Intersection(choices[1],choices[3])),Length(Intersection(choices[2],choices[3]))]));
   od;
  od;
 od;
 if idx>1 then AppendTo("phase164_m22_shadow_data.json",",\n");fi;
 AppendTo("phase164_m22_shadow_data.json","{\"witness\":",idx,",\"borel_id\":",IdGroup(B),",\"signatures\":",sigs,"}");
od;
AppendTo("phase164_m22_shadow_data.json","\n]}\n");
Print("SHADOW_DECODING_COMPLETE ",Length(M22Triples),"\n");
QUIT;
