Read("actual_maximality.g");;
Read("archive_data/inputs.g");;
L096ComputeShadow:=false;;
for row in [9..15] do
 Print("START|",row,"|",L096Inputs[row].member,"|",L096Inputs[row].active,"\n");
 r:=L096AllResidues(L096Inputs[row]);;
 Print("RESULT|",L096JSON(r),"\n");
od;
Print("PASS_J3_ELIGIBILITY_9_15\n");QUIT;
