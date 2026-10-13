Read("subdivision_markings.g");;
Read("cubic_markings/VT3_336_281.g");;
S:=L059SubdivisionFromBipartite(L059Result);;
PrintTo("subdivision_markings/CAT_336_4.g","L059Subdivision := ",S,";\n");
Print("L059_SUBDIVISION_COMPLETE CAT_336_4 ",Length(S.witnesses),"\n");
QUIT;
