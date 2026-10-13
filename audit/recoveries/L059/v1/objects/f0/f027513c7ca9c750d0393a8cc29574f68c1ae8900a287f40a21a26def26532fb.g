Read("subdivision_markings.g");;
Read("cubic_2048_markings/CAT_864_4.g");;
S:=L059SubdivisionFromBipartite(L059Result);;
PrintTo("subdivision_markings/CAT_864_4.g","L059Subdivision := ",S,";\n");
Print("L059_SUBDIVISION_COMPLETE CAT_864_4 ",Length(S.witnesses),"\n");
QUIT;
