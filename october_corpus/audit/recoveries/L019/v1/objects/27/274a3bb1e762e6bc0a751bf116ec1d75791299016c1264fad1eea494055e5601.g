Read("/Users/sasha/medusa/research/leemans/reboot_20261013/L071_A11_full_IP01/records.g");
RunWingCheck:=function()
local ids,marks,k,a,c,s,u,v,inter,middle,anchors;
k:=0;
for ids in recordedMarks[6] do
  k:=k+1;marks:=List(ids,x->recordedInvolutions[x]);
  if Group(marks)<>AlternatingGroup(11) then Error("wrong A11 group");fi;
  Print("MARKS ",k," ",List(marks,x->List([1..11],i->i^x)),"\n");
  anchors:=Filtered([1..11],a->a^marks[1]<>a and ForAll(marks{[2..6]},x->a^x=a));
  Print("ANCHORS ",k," ",anchors,"\n");
  for a in anchors do
    c:=Stabilizer(Centralizer(SymmetricGroup(11),Group(marks{[2..6]})),a);
    if Size(c)<>1 then Error("nontrivial anchored centralizer");fi;
    s:=Concatenation([(a,12)],marks);
    u:=Group(s{[2..5]});v:=Group(s{[1..4]});
    inter:=Intersection(u,v);middle:=Group(s{[2..4]});
    if Index(inter,middle)<>6 then Error("wrong obstruction");fi;
    Print("WITNESS ",k," ",a," ",[Size(c),Size(u),Size(v),Size(inter),Size(middle),Index(inter,middle)],"\n");
  od;
od;
if k<>4 then Error("wrong complete census size");fi;
Print("DONE_ACTUAL_A11_WINGS\n");
end;
RunWingCheck();QUIT_GAP(0);
