Read("actual_maximality.g");;
Read("archive_data/inputs.g");;
L096ComputeShadow:=false;;
# First six complete rows are preserved from the actual coset-action pass.
for row in [7..Length(L096Inputs)] do
 Print("START|",row,"|",L096Inputs[row].member,"|",L096Inputs[row].active,"\n");
 r:=L096AllResidues(L096Inputs[row]);;
 Print("RESULT|",L096JSON(r),"\n");
od;
Print("PASS_HS_REMAINING_ELIGIBILITY\n");QUIT;
