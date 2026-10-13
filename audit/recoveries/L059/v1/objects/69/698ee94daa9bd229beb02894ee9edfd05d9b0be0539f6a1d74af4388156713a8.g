Read("subdivision_markings.g");;
Read("cubic_markings/VT3_192_220.g");;
S:=L059SubdivisionFromBipartite(L059Result);;
PrintTo("subdivision_markings/CAT_192_3.g","L059Subdivision := ",S,";\n");
Print("L059_SUBDIVISION_COMPLETE CAT_192_3 ",Length(S.witnesses),"\n");
QUIT;
