Read("subdivision_markings.g");;
Read("cubic_markings/VT3_378_60.g");;
S:=L059SubdivisionFromBipartite(L059Result);;
PrintTo("subdivision_markings/CAT_378_2.g","L059Subdivision := ",S,";\n");
Print("L059_SUBDIVISION_COMPLETE CAT_378_2 ",Length(S.witnesses),"\n");
QUIT;
