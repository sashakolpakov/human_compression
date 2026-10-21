Read("shadow_residues_sparse.g");;
Read("prior_inputs.g");;
if not IsBound(L096SelectedRows) then L096SelectedRows:=[1..Length(L096Inputs)];fi;
for row in L096SelectedRows do Print("START|",row,"|",L096Inputs[row].construction,"\n");r:=L096AllResidues(L096Inputs[row]);;Print("RESULT|",L096JSON(r),"\n");od;
Print("PASS_M23_SHADOWS\n");QUIT;
