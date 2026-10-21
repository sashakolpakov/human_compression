if LoadPackage("ctbllib")=fail then Error("CTblLib unavailable"); fi;
RunTableControls:=function()
local name,t,orders,sizes,indices,count,i,found;
found:=false;
for name in ["L4(2)","L4(3)","U4(2)","U4(3)","S4(3)","S6(2)","O7(3)","O8+(2)","O8-(2)"] do
 t:=CharacterTable(name);
 if t=fail then Error("required small ordinary table absent: ",name); fi;
 orders:=OrdersClassRepresentatives(t);sizes:=SizesConjugacyClasses(t);
 count:=0;
 for i in [1..Length(orders)] do
  if orders[i]=2 then count:=count+sizes[i];fi;
 od;
 if name="U4(3)" then
  if count<>2835 then Error("U4(3) exact count differs");fi;
  found:=true;
 fi;
 Print("TABLE ",name," ",Size(t)," ",count,"\n");
od;
if not found then Error("U4(3) control omitted");fi;
Print("PASS_CLASSICAL_LOWER_ORDINARY_TABLE_CONTROLS\n");
end;
RunTableControls();
QUIT;
