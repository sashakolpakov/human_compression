# Stored library data only: no groups, cosets, or fusion search.
SetUserPreference("UseColorsInTerminal",false);;
Need:=function(b,m) if not b then Error(m); fi; end;;
Need(LoadPackage("ctbllib")=true,"Character Table Library unavailable");;
Need(LoadPackage("tomlib")=true,"Table of Marks Library unavailable");;
Emit:=function()
local name,t,f,m,names,perm,row,first;
first:=true;
Print("BEGIN_L036_MARK_INPUTS\n[\n");
for name in ["M12.2","J2.2","J3.2","HS.2","McL.2","He.2",
             "M11","M12","M22","M23","J1"] do
 t:=CharacterTable(name);
 Need(t<>fail and HasFusionToTom(t),Concatenation("Missing stored fusion: ",name));
 f:=FusionToTom(t);
 m:=TableOfMarks(f.name);
 Need(m<>fail and HasSubsTom(m),Concatenation("Missing stored table: ",name));
 Need(HasMarksTom(m) or (HasNrSubsTom(m) and HasOrdersTom(m)),"No stored marks or equivalent data");
 names:=[]; perm:=[];
 if name in ["M11","M12","M22","M23","J1"] then
  Need(HasMaxes(t),Concatenation("Missing complete maximal names: ",name));
  names:=Maxes(t);
  if IsBound(f.perm) then
   perm:=List([1..Length(names)],i->i^f.perm);
  else
   perm:=[1..Length(names)];
  fi;
 fi;
 row:=[name,Identifier(m),Size(t),OrdersTom(m),SubsTom(m),MarksTom(m),
       SizesCentralizers(t),PowerMap(t,2),OrdersClassRepresentatives(t),
       f.map,names,perm];
 if not first then Print(",\n"); fi;
 Print(row);
 first:=false;
od;
Print("\n]\nEND_L036_MARK_INPUTS\n");
end;;
Emit();;
QUIT;
