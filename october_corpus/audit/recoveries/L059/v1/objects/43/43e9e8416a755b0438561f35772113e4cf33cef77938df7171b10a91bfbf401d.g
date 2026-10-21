Read("subdivision_markings.g");;
Read("cubic_markings/VT3_728_175.g");;
S:=L059SubdivisionFromBipartite(L059Result);;
PrintTo("subdivision_markings/CAT_728_5.g","L059Subdivision := ",S,";\n");
Print("L059_SUBDIVISION_COMPLETE CAT_728_5 ",Length(S.witnesses),"\n");
QUIT;
