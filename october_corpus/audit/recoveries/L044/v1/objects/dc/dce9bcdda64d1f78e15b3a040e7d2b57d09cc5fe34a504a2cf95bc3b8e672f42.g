CheckString:=function(t)
 local m;
 m:=Length(t);if m<=2 then return true;fi;
 return CheckString(t{[1..m-1]}) and CheckString(t{[2..m]}) and
 Intersection(Group(t{[1..m-1]}),Group(t{[2..m]}))=Group(t{[2..m-1]});
end;;
PartialC:=function(t,selected,H)
 local blocks,b,i;
 blocks:=[];b:=[];
 for i in selected do
  if Length(b)>0 and i<>b[Length(b)]+1 then Add(blocks,b);b:=[];fi;
  Add(b,i);
 od;
 if Length(b)>0 then Add(blocks,b);fi;
 for b in blocks do
  if not CheckString(t{b}) then return false;fi;
 od;
 return Product(blocks,b->Size(Group(t{b})))=Size(H);
end;;

G:=SymmetricGroup(4);;invs:=Filtered(Elements(G),x->Order(x)=2);;
FullIP:=function(t,selected)
 local subs,Hs,i,j;
 subs:=Combinations(selected);Hs:=List(subs,I->Group(Concatenation([()],t{I})));
 for i in [1..Length(subs)] do for j in [1..Length(subs)] do
  if Intersection(Hs[i],Hs[j])<>Group(Concatenation([()],t{Intersection(subs[i],subs[j])})) then return false;fi;
 od;od;return true;
end;;
cases:=0;;accepted:=0;;rejected:=0;;disconnected:=0;;
for selected in Filtered(Combinations([1..4]),I->Length(I)>0) do
 for marks in Tuples(invs,Length(selected)) do
  if Length(Set(marks))=Length(marks) then
   t:=[];;for i in [1..Length(selected)] do t[selected[i]]:=marks[i];od;
   string:=true;;for i in selected do for j in selected do
    if AbsInt(i-j)>1 and t[i]*t[j]<>t[j]*t[i] then string:=false;fi;
   od;od;
   if string then
    H:=Group(marks);;
    got:=PartialC(t,selected,H);;want:=FullIP(t,selected);;
    if got<>want then Error("partial criterion mismatch");fi;
    cases:=cases+1;;if got then accepted:=accepted+1;else rejected:=rejected+1;fi;
    if Length(selected)>1 and Length(selected)<>Maximum(selected)-Minimum(selected)+1 then disconnected:=disconnected+1;fi;
   fi;
  fi;
 od;
od;
if cases=0 or accepted=0 or rejected=0 or disconnected=0 then Error("nonvacuous oracle");fi;
Print("PARTIAL_CRITERION_ALL_CASES ",cases," ACCEPTED ",accepted," REJECTED ",rejected," DISCONNECTED ",disconnected,"\n");
Print("COMPLETE_PARTIAL_ORACLE\n");QUIT;
