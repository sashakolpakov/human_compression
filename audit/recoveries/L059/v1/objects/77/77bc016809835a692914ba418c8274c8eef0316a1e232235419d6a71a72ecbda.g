Read("subdivision_actual_actions.g");;
Read("cubic_2048_markings/CAT_1152_5.g");;
S:=L059SubdivisionFromBipartite(L059Result);;
PrintTo("subdivision_markings/CAT_1152_5.g","L059Subdivision := ",S,";\n");
Print("L059_SUBDIVISION_COMPLETE CAT_1152_5 ",Length(S.witnesses),"\n");
QUIT;
