SizeScreen([100000,24]);;
G:=Group((1,2),(3,4));;reps:=[TrivialSubgroup(G)];;borelResult:=rec();;
INPUT_ROWS:=[[1,"/Users/sasha/medusa/research/leemans/geometry/psl3_4/postprocess_caller_control01/b1_done.g",[3,3,0],[2,2,2]]];;OUTPUT_DIR:="/Users/sasha/medusa/research/leemans/geometry/psl3_4/postprocess_caller_control01";;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/postprocess_work/legacy_fusion_functions.g");;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/postprocess_work/fusion_witness.g");;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/postprocess_work/fusion_driver.g");;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/postprocess_caller_control01/result.g");;Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/postprocess_caller_control01/automorphisms.g");;
if L100PartialFusion.counts<>[[2,3,1]] or Length(L100PartialFusion.members)<>3 or L100FullAutData.automorphism_order<>6 then Error("tiny caller output mismatch");fi;
Print("PASS_TINY_ACTUAL_CALLER_SERIALIZATION\n");QUIT_GAP(0);
