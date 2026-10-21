Read("subdivision_markings.g");;
Read("cubic_markings/VT3_512_746.g");;
S:=L059SubdivisionFromBipartite(L059Result);;
PrintTo("subdivision_markings/CAT_512_6.g","L059Subdivision := ",S,";\n");
Print("L059_SUBDIVISION_COMPLETE CAT_512_6 ",Length(S.witnesses),"\n");
QUIT;
