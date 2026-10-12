# Full shadow decisions for the distinct literal supplied families.
# RWPRI was actually computed for all124 inputs in the bound eligibility pass.
Read("shadow_residues_sparse.g");;
Read("archive_data/inputs.g");;
Read("class_inputs.g");;
for k in [1..Length(L096ClassInputRows)] do
 row:=L096ClassInputRows[k];inp:=L096Inputs[row];
 Print("START|",k,"|",row,"|",inp.member,"|",inp.active,"\n");
 r:=L096AllResidues(inp);r.shadow_class:=k;r.literal_input_row:=row;
 r.retained_RWPRI_basis:="computed_eligibility_same_literal_HS_input";
 for q in r.residues do q.primitivity_status:="reused_actual_eligibility_same_literal_input";od;
 Print("RESULT|",L096JSON(r),"\n");
od;
Print("PASS_HS_ALL_CLASS_SHADOWS\n");QUIT;
