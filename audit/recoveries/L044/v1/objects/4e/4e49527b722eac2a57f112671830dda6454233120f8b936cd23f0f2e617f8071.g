# Full tuple validation is independent of the search traversal and its pruning.
Read(modelFile);;Read(recordsFile);;Read(checksFile);;
if Size(G)<>expectedOrder or not IsNormal(A,G) then Error("model");fi;
if Size(A)/Size(Centralizer(A,G))<>expectedAutOrder then Error("full action");fi;
total:=0;;subsetPairs:=0;;t:=[];;ty:=[];;marks:=[];;dualMap:=[];;
for rank in recordedRanks do
 marks:=recordedMarks[rank];;types:=[];;dualMap:=[];;
 for j in [1..Length(marks)] do
  t:=marks[j];;
  if Length(t)<>rank or not ForAll(t,x->x in G and Order(x)=2) then Error("mark");fi;
  for a in [1..rank] do for b in [a+2..rank] do
   if Comm(t[a],t[b])<>() then Error("string");fi;
  od;od;
  if Group(t)<>G or not FullIP(t) then Error("generation/full IP");fi;
  subsetPairs:=subsetPairs+4^rank;
  ty:=List([1..rank-1],a->Order(t[a]*t[a+1]));;Add(types,ty);
  candidates:=Filtered([1..Length(marks)],k->List([1..rank-1],a->Order(marks[k][a]*marks[k][a+1]))=Reversed(ty));;
  dual:=Filtered(candidates,k->RepresentativeAction(A,t,Reversed(marks[k]),OnTuples)<>fail);;
  if Length(dual)<>1 then Error("duality pairing or duplicate orbit");fi;
  Add(dualMap,dual[1]);
  h1:=Group(t{[1..rank-1]});;h2:=Group(t{[2..rank]});;
  triples:=List([1..rank-2],a->Group(t{[a..a+2]}));;
  Print("VALIDATED_MARK ",rank," ",j," TYPE ",ty," ENDS ",[Size(h1),Size(h2)]," TRIPLES ",List(triples,Size),"\n");
  total:=total+1;
 od;
 if not ForAll([1..Length(marks)],j->dualMap[dualMap[j]]=j) then Error("reversal involution");fi;
 Print("VERIFIED_TYPE_COUNTS ",rank," ",Collected(types),"\n");
 Print("DUAL_MAP ",rank," ",dualMap,"\n");
od;
if total>0 then
 t:=recordedMarks[First(recordedRanks,r->Length(recordedMarks[r])>0)][1];;
 if FullIP([t[1],t[2],t[1]]) then Error("damaged repetition accepted");fi;
fi;
Print("VALIDATED_TOTAL ",total," SUBSET_PAIRS ",subsetPairs,"\n");
Print("COMPLETE_RECORD_VALIDATION\n");
QUIT;
