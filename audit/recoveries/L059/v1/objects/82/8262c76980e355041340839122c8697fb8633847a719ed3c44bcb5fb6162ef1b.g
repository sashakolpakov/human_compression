Read("subdivision_markings.g");;
Read("cubic_markings/VT3_364_77.g");;
S:=L059SubdivisionFromBipartite(L059Result);;
PrintTo("subdivision_markings/CAT_364_7.g","L059Subdivision := ",S,";\n");
Print("L059_SUBDIVISION_COMPLETE CAT_364_7 ",Length(S.witnesses),"\n");
QUIT;
