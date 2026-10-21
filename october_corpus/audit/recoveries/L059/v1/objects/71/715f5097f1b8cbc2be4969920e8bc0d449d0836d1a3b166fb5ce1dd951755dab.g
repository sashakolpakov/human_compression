Read("subdivision_markings.g");;
Read("cubic_markings/VT3_240_294.g");;
S:=L059SubdivisionFromBipartite(L059Result);;
PrintTo("subdivision_markings/CAT_240_3.g","L059Subdivision := ",S,";\n");
Print("L059_SUBDIVISION_COMPLETE CAT_240_3 ",Length(S.witnesses),"\n");
QUIT;
