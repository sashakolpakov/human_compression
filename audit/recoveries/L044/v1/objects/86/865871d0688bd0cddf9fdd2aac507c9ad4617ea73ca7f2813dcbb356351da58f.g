Read("enumeration.g");;
positive:=Concatenation(translations,[Product(flips)]);;
if Size(Group(positive))<>16 or not IsTransitive(Group(positive),[1..16])
 or not ReferenceIP(positive) then Error("regular positive control");fi;
if ReferenceIP([translations[1],translations[1]]) then
 Error("dependent negative control");fi;
Print("CONTROLS_PASS\n");
referenceCalls:=0;;referencePairs:=0;;
patterns:=[[1,2,3,4,5],[1,2,3,4,6],[1,2,3,5,6],[1,2,3,5,7],[1,2,4,5,7],[1,2,4,6,8]];;
PrintTo("census.json","{\"model\":[",Size(W),",",Size(N),",",Length(allInvolutions),"],\"rows\":[");
for index in [1..Length(patterns)] do
 labels:=patterns[index];nodes:=List([0..5],i->0);leaves:=[];allLeaves:=0;
 Print("PATTERN_START ",labels,"\n");
 VisitFive(labels{[1,5,2,4,3]},[],[],TrivialSubgroup(W),N);
 if index>1 then AppendTo("census.json",",");fi;
 AppendTo("census.json","[",index,",",nodes,",",allLeaves,",",Length(leaves),"]");
 Print("PATTERN_COMPLETE ",labels," ",nodes," total ",allLeaves," transitive ",Length(leaves),"\n");
od;
AppendTo("census.json","],\"reference_calls\":",referenceCalls,",\"reference_pairs\":",referencePairs,"}\n");
Print("ALL_SIX_PATTERNS_COMPLETE\n");
QUIT;
