Read("shadow_residues.g");;
Read("data_m12/inputs.g");;
for inp in L096Inputs do
 Print("START|",inp.member,"|",inp.active,"\n");
 r:=L096AllResidues(inp);;
 Print("RESULT|",L096JSON(r),"\n");
od;
Print("PASS_ALL_SELECTED_RESIDUES\n");QUIT;
