Read("subdivision_markings.g");;
Read("cubic_markings/VT3_672_638.g");;
S:=L059SubdivisionFromBipartite(L059Result);;
PrintTo("subdivision_markings/CAT_672_7.g","L059Subdivision := ",S,";\n");
Print("L059_SUBDIVISION_COMPLETE CAT_672_7 ",Length(S.witnesses),"\n");
QUIT;
