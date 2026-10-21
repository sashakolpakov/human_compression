# UNINVOKED SOURCE. Root must authenticate the complete source/proof/runtime
# scope and create the fresh returned directory before one separate release.
# Fixed-prefix known-member proof is external; no candidate inventory is read.
Read("/Users/sasha/medusa/research/leemans/reboot_20261013/F004_recovery_work/q11_model.g");;
if modelName<>"G2_11" or not IsPermGroup(G) or not IsIdenticalObj(A,G) then
 Error("exact acquired saved q11 model and A=G alias");
fi;
Read("/Users/sasha/medusa/research/leemans/reboot_20261013/F004_recovery_work/q11_frontier_split01/pair01.g");;
Read("/Users/sasha/medusa/research/leemans/reboot_20261013/F004_recovery_work/q11_frontier_split01/branch0008.g");;
Read("/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/original_prefix8_matrix_export/frame_inverse.g");;
F004Prefix8Marks:=Concatenation(fixedPair,[thirdMark]);;
if Length(fixedPair)<>2 or Length(F004Prefix8Marks)<>3 or
 Length(Set(F004Prefix8Marks))<>3 or
 ForAny(F004Prefix8Marks,p->not IsPerm(p) or p=() or p*p<>()) or
 F004Prefix8Marks[1]*F004Prefix8Marks[2]<>F004Prefix8Marks[2]*F004Prefix8Marks[1] or
 F004Prefix8Marks[2]*F004Prefix8Marks[3]<>F004Prefix8Marks[3]*F004Prefix8Marks[2] or
 F004Prefix8Marks[1]*F004Prefix8Marks[3]=F004Prefix8Marks[3]*F004Prefix8Marks[1] then
 Error("complete original selected labels1,4,2 and exact prefix relations");
fi;
F004InitializeMatrixFrame("/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/matrix_frame_result/map.json",[16106,24092,112665,84593,5978,56521,10081],45517,[8,2,7,3,10,3,2]);;
F004Prefix8Matrices:=List(F004Prefix8Marks,F004MatrixLiftKnown);;
F004Prefix8Integers:=List(F004Prefix8Matrices,m->List(m,r->List(r,IntFFE)));;
if Length(F004Prefix8Integers)<>3 or ForAny(F004Prefix8Integers,m->
 Length(m)<>7 or ForAny(m,r->Length(r)<>7 or
 ForAny(r,x->not IsInt(x) or x<0 or x>10))) then
 Error("three whole canonical7x7 prime-field matrices");
fi;
F004Prefix8Output:="/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/original_prefix8_matrix_export/returned/raw_coordinates.json";;
if IsExistingFile(F004Prefix8Output) then Error("fresh Root-owned raw matrix output");fi;
F004Prefix8Stream:=OutputTextFile(F004Prefix8Output,false);;
if F004Prefix8Stream=fail then Error("raw matrix export open");fi;
SetPrintFormattingStatus(F004Prefix8Stream,false);
PrintTo(F004Prefix8Stream,"{\"candidate_credit\":0,\"convention\":\"RIGHT_ROW\",\"dimension\":7,\"end_order\":[1,4,2,3],\"field\":11,\"matrix_frame_result\":{\"bytes\":9384,\"path\":\"/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/matrix_frame_acquisition_result/result.json\",\"sha256\":\"b6259de58ace64a7bccf97db50e81e4686c5f6f501c3263c86186fadb09e8391\"},\"matrix_roles\":[\"a\",\"e\",\"b\"],\"original_job\":[8,4],\"original_prefix_binding\":{\"bytes\":3314,\"path\":\"/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/original_prefix8_matrix_export/original_prefix_binding.json\",\"sha256\":\"2197b2a814fa0f26d830d3654aa390010e9420c4fa8b7bb5dbc7f1148f0deaf7\"},\"original_prefix_index\":8,\"original_prefix_index_proof\":{\"bytes\":3172,\"path\":\"/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/original_prefix8_matrix_export/original_prefix_index_proof.rst\",\"sha256\":\"cc3bbc5859a6a73a650cf66563f054d629930f11a32993560edd4199eb5d2c84\"},\"rank\":4,\"schema\":\"F004_Q11_ORIGINAL_PREFIX_RAW_MATRICES_V1\",\"selected_labels\":[1,4,2],\"whole_original_credit\":0,\"matrices\":",F004Prefix8Integers,"}\n");
CloseStream(F004Prefix8Stream);
Print("COMPLETE_F004_Q11_ORIGINAL_PREFIX_MATRIX_EXPORT B 8 R 4 PREFIX 8 MATRICES 3","\n");
QUIT;
