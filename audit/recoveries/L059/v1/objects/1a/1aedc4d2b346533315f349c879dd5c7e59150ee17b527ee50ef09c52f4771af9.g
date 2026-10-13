Read("subdivision_markings.g");;
Read("cubic_markings/VT3_278_3.g");;
S:=L059SubdivisionFromBipartite(L059Result);;
PrintTo("subdivision_markings/CAT_278_1.g","L059Subdivision := ",S,";\n");
Print("L059_SUBDIVISION_COMPLETE CAT_278_1 ",Length(S.witnesses),"\n");
QUIT;
