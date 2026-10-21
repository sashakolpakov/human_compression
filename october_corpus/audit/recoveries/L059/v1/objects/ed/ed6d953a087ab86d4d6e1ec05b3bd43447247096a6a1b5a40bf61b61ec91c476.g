Read("subdivision_markings.g");;
Read("cubic_markings/VT3_576_952.g");;
S:=L059SubdivisionFromBipartite(L059Result);;
PrintTo("subdivision_markings/CAT_576_3.g","L059Subdivision := ",S,";\n");
Print("L059_SUBDIVISION_COMPLETE CAT_576_3 ",Length(S.witnesses),"\n");
QUIT;
