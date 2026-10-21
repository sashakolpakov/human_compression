Read("model.g");;Read("checks.g");;Read("records.g");;
if Size(G)<>expectedOrder or not IsNormal(A,G) then Error("model");fi;
if Size(A)/Size(Centralizer(A,G))<>Size(AutomorphismGroup(G)) then
 Error("full automorphism action");fi;
limit:=0;;while 2^(limit+1)<=Size(G) do limit:=limit+1;od;
if Length(recordedMarks)<>limit then Error("full rank bound");fi;
total:=0;;firstTuple:=fail;;
for rank in [1..limit] do
 types:=[];;
 for t in recordedMarks[rank] do
  if Length(t)<>rank or not ForAll(t,x->Order(x)=2 and x in G) then
   Error("marks");fi;
  for i in [1..rank] do for j in [i+2..rank] do
   if Comm(t[i],t[j])<>() then Error("string");fi;
  od;od;
  if Group(t)<>G then Error("generation");fi;
  if not FullIP(t) then Error("full subset intersection property");fi;
  Add(types,List([1..rank-1],j->Order(t[j]*t[j+1])));
  if firstTuple=fail and rank>=3 then firstTuple:=t;fi;
  total:=total+1;
 od;
 if Length(recordedMarks[rank])<>reportedCounts[rank] then
  Error("reported rank count");fi;
 Print("VERIFIED_TYPE_COUNTS ",rank," ",Collected(types),"\n");
od;
if firstTuple<>fail and FullIP([firstTuple[1],firstTuple[2],firstTuple[1]]) then
 Error("repetition control");fi;
Print("VALIDATED_MODEL ",modelName," TUPLES ",total," RANK_LIMIT ",limit,"\n");
Print("COMPLETE_REMAINING_MODEL_VALIDATION\n");QUIT;
