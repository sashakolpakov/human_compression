Read("actual_primitivity.g");;
Read("archive_data/inputs.g");;
L096ComputeShadow:=false;;
for row in [1..Length(L096Inputs)] do
 Print("START|",row,"|",L096Inputs[row].member,"|",L096Inputs[row].active,"\n");
 r:=L096AllResidues(L096Inputs[row]);;
 Print("RESULT|",L096JSON(r),"\n");
od;
Print("PASS_HS_ELIGIBILITY\n");QUIT;
