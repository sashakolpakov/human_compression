# Independent geometric decoding of the author witnesses; no source table input.
SizeScreen([100000,24]);;
if not IsBound(WITNESS_FILE) then Error("Set WITNESS_FILE explicitly");fi;
Read(WITNESS_FILE);;
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

# Whole source definition allows both complementary endecad shadows.
# Canonical signatures additionally retain the older infinity extension.
L073Coordinates:=function(family,canonical)
 local output,idx,t,positions,ty,B,sigs,perm,sw,tt,inf,choices,pos,
       porders,ints,options,pp;
 output:=[];
 for idx in [1..Length(family)] do
  t:=family[idx];positions:=List(t,H->Position(allM,H));
  ty:=types{positions};B:=Intersection(t);sigs:=[];
  for perm in PermutationsList([1..Length(t)]) do
   for sw in [false,true] do
    tt:=ty{perm};inf:=fixed[2];
    if sw then tt:=List(tt,x->x^(3,4));inf:=fixed[1];fi;
    if tt<>SortedList(tt) then continue;fi;
    options:=[];
    for pos in positions{perm} do
     choices:=shadows[pos];
     if canonical and types[pos]=8 then
      choices:=Filtered(choices,s->Union(s,[inf]) in dodecads);
      if Length(choices)<>1 then Error("noncanonical endecad");fi;
     fi;
     Add(options,choices);
    od;
    pp:=Combinations([1..Length(t)],2);
    porders:=List(pp,p->Size(Intersection(t[perm[p[1]]],t[perm[p[2]]])));
    for choices in Cartesian(options) do
     ints:=List(pp,p->Length(Intersection(choices[p[1]],choices[p[2]])));
     AddSet(sigs,Concatenation(tt,ints,porders));
    od;
   od;
  od;
  Add(output,rec(witness:=idx,borel_id:=IdGroup(B),signatures:=sigs));
 od;
 return output;
end;;
L073Print:=function(path,family,canonical)
 local rows,i,r;
 rows:=L073Coordinates(family,canonical);
 PrintTo(path,"{\"fixed\":",fixed,",\"blocks\":",blocks,",\"triples\":[\n");
 for i in [1..Length(rows)] do
  r:=rows[i];if i>1 then AppendTo(path,",\n");fi;
  AppendTo(path,"{\"witness\":",r.witness,",\"borel_id\":",r.borel_id,",\"signatures\":",r.signatures,"}");
 od;
 AppendTo(path,"\n]}\n");
end;;
L073Print("canonical_triples.json",M22Triples,true);
L073Print("source_triples.json",M22Triples,false);
L073Print("canonical_pairs.json",M22Pairs,true);
L073Print("source_pairs.json",M22Pairs,false);
Print("L073_COMPLETE_COORDINATES ",Length(M22Pairs)," ",Length(M22Triples),"\n");
QUIT;
