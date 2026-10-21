Read("subdivision_markings.g");;
Read("cubic_markings/VT3_720_627.g");;
S:=L059SubdivisionFromBipartite(L059Result);;
PrintTo("subdivision_markings/CAT_720_6.g","L059Subdivision := ",S,";\n");
Print("L059_SUBDIVISION_COMPLETE CAT_720_6 ",Length(S.witnesses),"\n");
QUIT;
