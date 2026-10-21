Read("subdivision_markings.g");;
Read("cubic_markings/VT3_314_20.g");;
S:=L059SubdivisionFromBipartite(L059Result);;
PrintTo("subdivision_markings/CAT_314_1.g","L059Subdivision := ",S,";\n");
Print("L059_SUBDIVISION_COMPLETE CAT_314_1 ",Length(S.witnesses),"\n");
QUIT;
