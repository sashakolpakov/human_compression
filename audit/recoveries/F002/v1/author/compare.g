Read("checks.g");;Read("source_markings.g");;Read("generated_markings.g");;
S:=SymmetricGroup(11);;Ambient:=AlternatingGroup(11);;
t:=[];;u:=[];;
PermEquivalent:=function(t,u)
 return RepresentativeAction(S,t,u,OnTuples)<>fail;
end;;
StringTest:=function(t)
 local i,j;
 if not ForAll(t,x->Order(x)=2 and x in Ambient) then return false;fi;
 for i in [1..Length(t)] do for j in [i+2..Length(t)] do
  if Comm(t[i],t[j])<>() then return false;fi;
 od;od;return true;
end;;
small:=[];;totals:=[];;
for r in [3,4,5] do
 marks:=List(recordedMarks[r],ids->List(ids,i->recordedInvolutions[i]));;
 counts:=[];;
 for t in marks do
  if not StringTest(t) or not FullIP(t) or not IsTransitive(Group(t),[1..11]) then Error("recorded tuple");fi;
  Add(counts,Size(Group(t)));
  if Size(Group(t))=660 then Add(small,t);
  elif Group(t)<>Ambient then Error("unexpected transitive group");fi;
 od;
 Print("RANK_GROUP_ORDERS ",r," ",Collected(counts),"\n");
 Add(totals,Length(marks));
od;
if totals<>[130,2,0] then Error("transitive count");fi;
if Length(small)<>10 then Error("small tuple count");fi;
for i in [1..Length(sourceMarks)] do
 t:=sourceMarks[i];
 if not StringTest(t) or not FullIP(t) or Size(Group(t))<>660 then Error("source tuple");fi;
 if IsomorphismGroups(Group(t),PSL(2,11))=fail then Error("source identification");fi;
 matches:=Filtered(small,u->Length(u)=Length(t) and (PermEquivalent(t,u) or PermEquivalent(Reversed(t),u)));
 if Length(matches)<>2 then Error("source orbit multiplicity");fi;
 Print("SOURCE_ORBIT ",i," RECORDS ",Length(matches)," SELF_DUAL_ABSTRACT ",AbstractEquivalent(t,Reversed(t)),
       " SELF_DUAL_PERMUTATION ",PermEquivalent(t,Reversed(t)),"\n");
 Print("SOURCE_SUFFIX_ORBITS ",i," ",SortedList(List(Orbits(Group(t{[2..Length(t)]}),[1..11]),Length)),"\n");
 u:=Reversed(t);
 Print("SOURCE_DUAL_SUFFIX_ORBITS ",i," ",SortedList(List(Orbits(Group(u{[2..Length(u)]}),[1..11]),Length)),"\n");
od;
for t in small do
 matches:=Filtered(sourceMarks,u->Length(u)=Length(t) and (PermEquivalent(t,u) or PermEquivalent(t,Reversed(u))));
 if Length(matches)<>1 then Error("unique source class");fi;
od;
if not AbstractEquivalent(sourceMarks[2],sourceMarks[3]) then Error("abstract rows2and3");fi;
for i in [1,4,5] do
 if not AbstractEquivalent(sourceMarks[i],Reversed(sourceMarks[i])) then Error("abstract self-duality");fi;
od;
if FullIP([sourceMarks[1][1],sourceMarks[1][2],sourceMarks[1][1]]) then Error("duplicate control");fi;
if StringTest([(1,2),sourceMarks[1][2],sourceMarks[1][3]]) then Error("odd control");fi;
Print("ALL_132_RECORDED_TUPLES_FULL_SUBSET_IP_PASS\n");
Print("COMPLETE_COMPARISON_PASS\n");
QUIT;
