# Fixed named model and exact retained-input edition, supplied by a hash gate.
Read(INPUT_CATALOGUE);;
if PSL34CompleteInput.require_2T<>false then Error("broad-mode input required");fi;
if PSL34CompleteInput.table_name<>"L3(4)" then Error("wrong table identifier");fi;
G:=Group(PSL34CompleteInput.image_generators);;
if Size(G)<>20160 then Error("wrong fixed-model order");fi;
reps:=List(PSL34CompleteInput.representatives,Group);;
if Length(reps)<>95 or List(reps,Size)<>PSL34CompleteInput.orders then
 Error("wrong complete representative inventory");fi;
if not ForAll(reps,H->IsSubgroup(G,H)) then Error("representative outside fixed model");fi;
maxinclusions:=List(PSL34CompleteInput.maximal_inclusions,p->List(p,Group));;
if Length(maxinclusions)<>367 or List(maxinclusions,p->List(p,Size))<>PSL34CompleteInput.inclusion_orders then
 Error("wrong complete inclusion inventory");fi;
if not ForAll(maxinclusions,p->p[1] in reps and p[1]<>p[2] and IsSubgroup(p[1],p[2])) then
 Error("invalid retained inclusion");fi;
maxorders:=rec();;
for K in reps do
 if not IsBound(maxorders.(String(Size(K)))) then maxorders.(String(Size(K))):=[];fi;
od;
for p in maxinclusions do AddSet(maxorders.(String(Size(p[1]))),Size(p[2]));od;
# Only this broad mode is supported. local2T is deliberately not a filter.
REQUIRE_2T:=false;;local2T:=[];;
