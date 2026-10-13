Read("subdivision_markings.g");;
Read("cubic_markings/VT3_162_22.g");;
S:=L059SubdivisionFromBipartite(L059Result);;
PrintTo("subdivision_markings/CAT_162_3.g","L059Subdivision := ",S,";\n");
Print("L059_SUBDIVISION_COMPLETE CAT_162_3 ",Length(S.witnesses),"\n");
QUIT;
