Read("subdivision_actual_actions.g");;
Read("cubic_2048_markings/CAT_1792_3.g");;
S:=L059SubdivisionFromBipartite(L059Result);;
PrintTo("subdivision_markings/CAT_1792_3.g","L059Subdivision := ",S,";\n");
Print("L059_SUBDIVISION_COMPLETE CAT_1792_3 ",Length(S.witnesses),"\n");
QUIT;
