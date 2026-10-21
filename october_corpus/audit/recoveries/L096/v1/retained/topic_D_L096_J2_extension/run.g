Read("shadow_residues_sparse.g");;
Read("prior_inputs.g");;
for row in [1..22] do Print("START|",row,"\n");r:=L096AllResidues(L096Inputs[row]);;Print("RESULT|",L096JSON(r),"\n");od;
Print("PASS_J2_SPARSE\n");QUIT;
