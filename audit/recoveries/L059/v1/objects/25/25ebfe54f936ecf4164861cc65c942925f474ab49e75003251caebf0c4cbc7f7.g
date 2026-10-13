Read("subdivision_markings.g");;
Read("cubic_markings/VT3_650_79.g");;
S:=L059SubdivisionFromBipartite(L059Result);;
PrintTo("subdivision_markings/CAT_650_2.g","L059Subdivision := ",S,";\n");
Print("L059_SUBDIVISION_COMPLETE CAT_650_2 ",Length(S.witnesses),"\n");
QUIT;
