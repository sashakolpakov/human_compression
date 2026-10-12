# Operational bounded batch wrapper; the mathematical engine is unchanged.
if not IsBound(L096First) or not IsBound(L096Last) then Error("explicit batch interval required");fi;
Read("shadow_residues.g");;
Read("data_m12/inputs.g");;
if L096First<1 or L096Last>Length(L096Inputs) or L096First>L096Last then Error("invalid batch interval");fi;
for inp in L096Inputs{[L096First..L096Last]} do
 Print("START|",inp.member,"|",inp.active,"\n");
 r:=L096AllResidues(inp);;
 Print("RESULT|",L096JSON(r),"\n");
od;
Print("PASS_BOUNDED_M12_RESIDUES\n");QUIT;
