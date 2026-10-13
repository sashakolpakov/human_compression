Read("subdivision_markings.g");;
Read("cubic_markings/VT3_448_111.g");;
S:=L059SubdivisionFromBipartite(L059Result);;
PrintTo("subdivision_markings/CAT_448_1.g","L059Subdivision := ",S,";\n");
Print("L059_SUBDIVISION_COMPLETE CAT_448_1 ",Length(S.witnesses),"\n");
QUIT;
