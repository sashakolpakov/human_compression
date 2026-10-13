Read("subdivision_markings.g");;
Read("cubic_markings/VT3_392_69.g");;
S:=L059SubdivisionFromBipartite(L059Result);;
PrintTo("subdivision_markings/CAT_392_1.g","L059Subdivision := ",S,";\n");
Print("L059_SUBDIVISION_COMPLETE CAT_392_1 ",Length(S.witnesses),"\n");
QUIT;
