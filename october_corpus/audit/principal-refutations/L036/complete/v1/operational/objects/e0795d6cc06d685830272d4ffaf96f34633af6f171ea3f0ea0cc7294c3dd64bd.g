# Exact library-data export only. No group or coset construction.
SetUserPreference("UseColorsInTerminal",false);;
Need:=function(b,m) if not b then Error(m); fi; end;;
Need(LoadPackage("ctbllib")=true,"Character Table Library unavailable");;
Emit:=function()
local name,t,ms,mn,mt,f,rows,parents;
parents:=[];
for name in ["M11","M23","M24","J1","Ru"] do
 t:=CharacterTable(name);
 Need(t<>fail and HasMaxes(t),Concatenation("Missing complete maximal list: ",name));
 ms:=Maxes(t);
 rows:=[];
 for mn in ms do
  mt:=CharacterTable(mn);
  Need(mt<>fail,Concatenation("Missing maximal table: ",mn));
  f:=GetFusionMap(mt,t);
  Need(f<>fail,Concatenation("Missing stored compatible fusion: ",mn));
  Add(rows,[mn,Size(mt),SizesCentralizers(mt),f]);
 od;
 Add(parents,[name,Size(t),SizesCentralizers(t),PowerMap(t,2),rows]);
od;
Print("BEGIN_L036_CHARACTER_INPUTS\n");
Print(parents,"\n");
Print("END_L036_CHARACTER_INPUTS\n");
end;;
Emit();;
QUIT;
