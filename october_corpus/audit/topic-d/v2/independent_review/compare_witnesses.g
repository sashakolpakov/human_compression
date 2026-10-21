# The wrapper sets AUTHOR_WITNESS and FRESH_WITNESS to the two exact files.
SizeScreen([200,24]);;
Read(AUTHOR_WITNESS);;
oldWitnesses:=J2Representatives;;oldGroup:=G;;
Read(FRESH_WITNESS);;
if G<>oldGroup then Error("Ambient group changed");fi;
SameWitnesses:=function(a,b)
 local i,key,j;
 if Length(a)<>Length(b) then return false;fi;
 for i in [1..Length(a)] do
  if a[i].borel_id<>b[i].borel_id or a[i].borel_order<>b[i].borel_order then return false;fi;
  for key in ["panels","parabolics"] do
   if Length(a[i].(key))<>Length(b[i].(key)) then return false;fi;
   for j in [1..Length(a[i].(key))] do
    if a[i].(key)[j]<>b[i].(key)[j] then return false;fi;
   od;
  od;
 od;
 return true;
end;;
if not SameWitnesses(oldWitnesses,J2Representatives) then Error("Actual subgroup changed");fi;
checks:=Sum(oldWitnesses,r->Length(r.panels)+Length(r.parabolics));;
if checks<>170 or Length(oldWitnesses)<>30 then Error("Wrong comparison scope");fi;
# Two real countermodels: omit a geometry, then alter an actual panel subgroup.
if SameWitnesses(oldWitnesses,J2Representatives{[2..Length(J2Representatives)]}) then Error("Omission accepted");fi;
saved:=J2Representatives[1].panels[1];;
J2Representatives[1].panels[1]:=TrivialSubgroup(G);;
if SameWitnesses(oldWitnesses,J2Representatives) then Error("Changed group accepted");fi;
J2Representatives[1].panels[1]:=saved;;
Print("PASS geometries=30 exact_subgroups=170 controls=2\n");
QUIT;
