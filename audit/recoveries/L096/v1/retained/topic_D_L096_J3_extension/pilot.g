Read("actual_maximality.g");;
Read("archive_data/inputs.g");;
L096ComputeShadow:=false;;
Print("START|1\n");r:=L096AllResidues(L096Inputs[1]);;
Print("RESULT|",L096JSON(r),"\n");
Print("PASS_J3_ELIGIBILITY_PILOT\n");QUIT;
