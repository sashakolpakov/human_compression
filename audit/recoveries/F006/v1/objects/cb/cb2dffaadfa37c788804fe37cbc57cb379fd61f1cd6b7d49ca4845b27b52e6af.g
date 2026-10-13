Read("model.g");;Read("records.g");;Read("checks.g");;
total:=0;;
for rank in [1..Length(oldMarks)] do
 oldTuples:=List(oldMarks[rank],ids->List(ids,i->ivs[i]));;
 if Length(oldTuples)<>Length(newMarks[rank]) then Error("count");fi;
 used:=[];;
 for t in newMarks[rank] do
  if Group(t)<>G or not FullIP(t) then Error("new marking generation or IP");fi;
  if not ForAll(t,x->Order(x)=2) then Error("involution");fi;
  for i in [1..rank] do for j in [i+2..rank] do
   if Comm(t[i],t[j])<>() then Error("string");fi;
  od;od;
  found:=false;;
  for j in [1..Length(oldTuples)] do
   if not j in used then
    h:=RepresentativeAction(A,t,oldTuples[j],OnTuples);;
    if h<>fail then
     if not h in A or List(t,x->x^h)<>oldTuples[j] then Error("transport witness");fi;
     Add(used,j);found:=true;break;
    fi;
   fi;
  od;
  if not found then Error("missing unused old orbit");fi;
 od;
 if Set(used)<>[1..Length(oldTuples)] then Error("coverage");fi;
 total:=total+Length(used);
 Print("RANK_ORBIT_BIJECTION ",rank," ",Length(used),"\n");
od;
Print("COMPLETE_LITERAL_ORBIT_BIJECTION_AND_FULL_IP ",total,"\n");QUIT;
