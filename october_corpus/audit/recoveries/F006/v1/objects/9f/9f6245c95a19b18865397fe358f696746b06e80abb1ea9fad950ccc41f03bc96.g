Read("model.g");;Read("checks.g");;Read("records.g");;
if Size(G)<>expectedOrder then Error("model order");fi;
if Set(ivs)<>Set(Concatenation(List(Filtered(ConjugacyClasses(G),
 c->Order(Representative(c))=2),AsList))) then Error("involution domain");fi;
aut:=AutomorphismGroup(G);;
if innerAction then
 if Size(G)/Size(Centre(G))<>Size(aut) then Error("full inner action");fi;
 A:=G;;
else
 A:=Image(ActionHomomorphism(aut,ivs,OnPoints));;
 if Size(A)<>Size(aut) then Error("full involution action");fi;
fi;
limit:=0;;while 2^(limit+1)<=Size(G) do limit:=limit+1;od;
if Length(recordedIds)<>limit then Error("rank limit");fi;
total:=0;;pairs:=0;;firstTuple:=fail;;
for rank in [1..limit] do
 self:=0;;connected:=0;;connectedSelf:=0;;types:=[];;
 for ids in recordedIds[rank] do
  if Length(ids)<>rank or not ForAll(ids,i->i in [1..Length(ivs)]) then Error("indices");fi;
  t:=List(ids,i->ivs[i]);;
  if not ForAll(t,x->Order(x)=2 and x in G) then Error("marks");fi;
  for i in [1..rank] do for j in [i+2..rank] do
   if Comm(t[i],t[j])<>() then Error("string");fi;
  od;od;
  if Group(t)<>G then Error("generation");fi;
  if not FullIP(t) then Error("full subset intersection property");fi;
  pairs:=pairs+4^rank;
  typ:=List([1..rank-1],j->Order(t[j]*t[j+1]));;Add(types,typ);
  if innerAction then sd:=RepresentativeAction(A,t,Reversed(t),OnTuples)<>fail;
  else sd:=RepresentativeAction(A,ids,Reversed(ids),OnTuples)<>fail;fi;
  conn:=ForAll(typ,x->x>2);;
  if sd then self:=self+1;fi;
  if conn then connected:=connected+1;if sd then connectedSelf:=connectedSelf+1;fi;fi;
  total:=total+1;
  if firstTuple=fail and rank>=3 then firstTuple:=t;fi;
 od;
 got:=[Length(recordedIds[rank]),self,(Length(recordedIds[rank])+self)/2,
       connected,connectedSelf,(connected+connectedSelf)/2];;
 if got<>reportedCounts[rank] then Error("rank/self-duality/connected count");fi;
 Print("VERIFIED_RANK ",rank," ",got,"\n");
 Print("VERIFIED_TYPE_COUNTS ",rank," ",Collected(types),"\n");
od;
if firstTuple<>fail and FullIP([firstTuple[1],firstTuple[2],firstTuple[1]]) then
 Error("repetition control");fi;
Print("VALIDATED_MODEL ",modelName," TUPLES ",total," SUBSET_PAIRS ",pairs,"\n");
Print("COMPLETE_EXCEPTIONAL_ROW_VALIDATION\n");QUIT;
