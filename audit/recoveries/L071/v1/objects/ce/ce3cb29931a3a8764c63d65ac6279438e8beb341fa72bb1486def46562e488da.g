Read("checks.g");;Read("records.g");;
Ambient:=AlternatingGroup(degree);; total:=0;; altTotal:=0;;
if 2^(rankLimit+1)<=Size(Ambient) then Error("incomplete rank limit");fi;
for rank in [3..rankLimit] do
 counts:=[];;altCount:=0;;
 for ids in recordedMarks[rank] do
  t:=List(ids,i->recordedInvolutions[i]);;
  if Length(t)<>rank or not ForAll(t,x->Order(x)=2 and x in Ambient) then Error("marks");fi;
  for i in [1..rank] do for j in [i+2..rank] do
   if Comm(t[i],t[j])<>() then Error("string");fi;
  od;od;
  if not FullIP(t) then Error("full subset IP");fi;
  H:=Group(t);;
  if not IsTransitive(H,[1..degree]) then Error("transitivity");fi;
  Add(counts,Size(H));total:=total+1;
  if H=Ambient then altCount:=altCount+1;altTotal:=altTotal+1;fi;
 od;
 Print("VALIDATED_RANK ",rank," ALTERNATING ",altCount," GROUP_ORDERS ",Collected(counts),"\n");
od;
if FullIP([recordedInvolutions[1],recordedInvolutions[2],recordedInvolutions[1]]) then Error("repetition control");fi;
Print("ALL_RECORDS_FULL_SUBSET_IP_PASS DEGREE ",degree," TOTAL ",total," ALTERNATING ",altTotal,"\n");
Print("COMPLETE_VALIDATION\n");QUIT;
