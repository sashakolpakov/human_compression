Read("subdivision_markings.g");;
Read("cubic_markings/VT3_120_64.g");;
S:=L059SubdivisionFromBipartite(L059Result);;
PrintTo("subdivision_markings/CAT_120_2.g","L059Subdivision := ",S,";\n");
Print("L059_SUBDIVISION_COMPLETE CAT_120_2 ",Length(S.witnesses),"\n");
QUIT;
