Read("subdivision_markings.g");;
Read("cubic_markings/VT3_734_31.g");;
S:=L059SubdivisionFromBipartite(L059Result);;
PrintTo("subdivision_markings/CAT_734_1.g","L059Subdivision := ",S,";\n");
Print("L059_SUBDIVISION_COMPLETE CAT_734_1 ",Length(S.witnesses),"\n");
QUIT;
