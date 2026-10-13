Read("subdivision_markings.g");;
Read("cubic_2048_markings/CAT_1296_10.g");;
S:=L059SubdivisionFromBipartite(L059Result);;
PrintTo("subdivision_markings/CAT_1296_10.g","L059Subdivision := ",S,";\n");
Print("L059_SUBDIVISION_COMPLETE CAT_1296_10 ",Length(S.witnesses),"\n");
QUIT;
