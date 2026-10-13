Read("search.g");;
results:=[];;
for ab in [[2,3],[2,4],[3,3],[2,5],[3,4],[2,6],[3,5],[4,4]] do
 Add(results,RunProduct(ab[1],ab[2]));
od;
Add(results,RunNormalized(TransitiveGroup(6,9),6,"T6_9"));;
Add(results,RunNormalized(TransitiveGroup(6,11),6,"T6_11"));;
for result in results do
 if Length(result.solutions)<>0 then Error("surviving boundary marking");fi;
 Print("SUMMARY|",result.label,"|",result.k,"|",result.rank,"|",result.markings,"|",
 JoinStringsWithSeparator(List(result.extension_counts,String),"|"),"|",Length(result.solutions),"\n");
od;
control:=RunNormalizedRank(Group(()),3,"positive_rank3",0);;
if Length(control.solutions)<>6 then Error("positive control must recover six completions");fi;
if not AllIP(SymmetricGroup(3),[(1,2),(2,3)]) then Error("Coxeter path positive IP control");fi;
if AllIP(SymmetricGroup(3),[(1,2),(2,3),(1,3)]) then Error("redundant family negative IP control");fi;
if Independent(SymmetricGroup(3),[(1,2),(2,3),(1,3)]) then Error("redundant family negative independence control");fi;
Print("CONTROL|positive_rank3|",Length(control.solutions),"\n");
Print("PASS_L047_FINITE_BOUNDARY\n");
QUIT;
