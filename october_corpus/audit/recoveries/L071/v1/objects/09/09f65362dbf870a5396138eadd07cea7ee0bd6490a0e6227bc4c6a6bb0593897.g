Read("model.g");;Read("checks.g");;Read("records.g");;Read("expected.g");;
if Size(G)<>495766656000 or not IsSimpleGroup(G) then Error("Co3 model");fi;
if not (2^38<=Size(G) and Size(G)<2^39) then Error("rank limit");fi;
total:=0;;actual:=[];;
for rank in [1..38] do
 types:=[];;
 for t in recordedMarks[rank] do
  if Length(t)<>rank or not ForAll(t,x->Order(x)=2 and x in G) then Error("marks");fi;
  for i in [1..rank] do for j in [i+2..rank] do
   if Comm(t[i],t[j])<>() then Error("string");fi;
  od;od;
  if Group(t)<>G then Error("generation");fi;
  if not FullIP(t) then Error("full subset intersection property");fi;
  Add(types,List([1..rank-1],j->Order(t[j]*t[j+1])));
  total:=total+1;
  if total mod 500=0 then Print("VALIDATION_PROGRESS ",total,"\n");fi;
 od;
 cells:=Collected(types);;
 Print("VERIFIED_TYPE_COUNTS ",rank," ",cells,"\n");
 for cell in cells do Add(actual,[rank,cell[1],cell[2]]);od;
od;
for row in expected do
 matches:=Filtered(actual,x->x[1]=row[1] and x[2]=row[2]);;
 if row[3]=0 then
  if Length(matches)<>0 then Error("printed zero cell");fi;
 elif Length(matches)<>1 or matches[1][3]<>row[3] then Error("printed positive cell");fi;
od;
for row in actual do
 if not row in expected then Error("unlisted type or rank occurred");fi;
od;
if total<>22908 or Length(expected)<>824 then Error("literal coverage count");fi;
if FullIP([recordedMarks[3][1][1],recordedMarks[3][1][2],recordedMarks[3][1][1]]) then
 Error("repetition control");fi;
Print("ALL_CO3_TABLE_CELLS_AND_FULL_IP_PASS TUPLES ",total," PRINTED_CELLS ",Length(expected),"\n");
Print("COMPLETE_CO3_VALIDATION\n");QUIT;
