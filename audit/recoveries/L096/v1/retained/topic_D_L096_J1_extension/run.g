Read("shadow_residues.g");;
Read("data/inputs.g");;
for inp in L096Inputs do
 Print("START|",inp.member,"|",inp.active,"\n");
 r:=L096AllResidues(inp);;Print("RESULT|",L096JSON(r),"\n");
od;
Print("PASS_J1_RESIDUES\n");QUIT;
