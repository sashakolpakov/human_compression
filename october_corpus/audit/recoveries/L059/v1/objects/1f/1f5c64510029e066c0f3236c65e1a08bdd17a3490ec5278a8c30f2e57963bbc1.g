Read("subdivision_markings.g");;
Read("cubic_markings/VT3_256_30.g");;
S:=L059SubdivisionFromBipartite(L059Result);;
PrintTo("subdivision_markings/CAT_256_4.g","L059Subdivision := ",S,";\n");
Print("L059_SUBDIVISION_COMPLETE CAT_256_4 ",Length(S.witnesses),"\n");
QUIT;
