Read("shadow_residues.g");;
Read("data_m12/inputs.g");;
for inp in L096Inputs do
 if inp.member="m12.rk3" or (inp.member="m12.rk4" and inp.active<=18) then continue;fi;
 Print("START|",inp.member,"|",inp.active,"\n");
 r:=L096AllResidues(inp);;
 Print("RESULT|",L096JSON(r),"\n");
od;
Print("PASS_REMAINING_SELECTED_RESIDUES\n");QUIT;
