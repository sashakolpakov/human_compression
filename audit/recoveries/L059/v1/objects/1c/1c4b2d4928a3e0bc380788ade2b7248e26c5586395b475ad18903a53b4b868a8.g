Read("subdivision_markings.g");;
Read("cubic_2048_markings/CAT_2048_17.g");;
S:=L059SubdivisionFromBipartite(L059Result);;
PrintTo("subdivision_markings/CAT_2048_17.g","L059Subdivision := ",S,";\n");
Print("L059_SUBDIVISION_COMPLETE CAT_2048_17 ",Length(S.witnesses),"\n");
QUIT;
