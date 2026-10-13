Read("/Users/sasha/medusa/research/leemans/corpus106_F004_ends_enumeration_v1/q3_model.g");;
    B:=Group(GeneratorsOfGroup(PrimitiveGroup(351,7)));;
    iso:=IsomorphismGroups(B,G);;
    if iso=fail or not IsBijective(iso) then Error("standard model identity");fi;
    if Size(AutomorphismGroup(B))<>expectedAutOrder then Error("full Aut order");fi;
    if not IsNormal(A,G) or Size(A)/Size(Centralizer(A,G))<>expectedAutOrder then Error("compatible action");fi;
    Print("MODEL_CONTROL_COMPLETE\n");QUIT;
    