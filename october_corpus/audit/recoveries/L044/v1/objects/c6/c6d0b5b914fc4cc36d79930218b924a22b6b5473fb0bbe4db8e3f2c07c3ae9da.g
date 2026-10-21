Read("checks.g");;Read("records.g");;
Ambient:=AlternatingGroup(degree);;total:=0;;altTotal:=0;;altCounts:=[];;
if 2^(rankLimit+1)<=Size(Ambient) then Error("incomplete rank cutoff");fi;
for rank in [3..rankLimit] do
 altCount:=0;;orders:=[];;
 for ids in recordedMarks[rank] do
  t:=List(ids,i->recordedInvolutions[i]);;
  if Length(t)<>rank or not ForAll(t,x->Order(x)=2 and x in Ambient) then Error("invalid marks");fi;
  for i in [1..rank] do for j in [i+2..rank] do
   if Comm(t[i],t[j])<>() then Error("string commutation");fi;
  od;od;
  if not FullIP(t) then Error("full subset IP");fi;
  H:=Group(t);;
  if not IsTransitive(H,[1..degree]) then Error("record is not transitive");fi;
  total:=total+1;Add(orders,Size(H));
  if H=Ambient then altCount:=altCount+1;altTotal:=altTotal+1;fi;
 od;
 Add(altCounts,altCount);
 Print("VALIDATED_RANK ",rank," ALTERNATING ",altCount," GROUP_ORDERS ",Collected(orders),"\n");
od;
if FullIP([recordedInvolutions[1],recordedInvolutions[2],recordedInvolutions[1]]) then Error("repetition negative control");fi;
Print("ALT_COUNTS ",altCounts,"\n");
Print("ALL_RECORDS_FULL_SUBSET_IP_PASS DEGREE ",degree," TOTAL ",total," ALTERNATING ",altTotal,"\n");
Print("COMPLETE_VALIDATION\n");QUIT;
