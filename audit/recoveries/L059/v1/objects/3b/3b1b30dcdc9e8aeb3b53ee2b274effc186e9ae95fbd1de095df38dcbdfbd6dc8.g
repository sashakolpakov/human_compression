Read("subdivision_markings.g");;
Read("cubic_markings/VT3_256_21.g");;
S:=L059SubdivisionFromBipartite(L059Result);;
PrintTo("subdivision_markings/CAT_256_2.g","L059Subdivision := ",S,";\n");
Print("L059_SUBDIVISION_COMPLETE CAT_256_2 ",Length(S.witnesses),"\n");
QUIT;
