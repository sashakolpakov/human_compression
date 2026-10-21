Read("shadow_residues.g");;
Read("prior_representatives.g");;
oldG:=G;;old:=SporadicRepresentatives[18];;
if Length(old.parabolics)<>3 then Error("wrong retained census rank");fi;
Print("PRIOR_RECORDED_TWO_T|",old.twot,"\n");;
inp:=rec(member:="prior_m12.rk3",active:=1,construction:=18,expected_order:=95040,
parabolic_generators:=List(old.parabolics,GeneratorsOfGroup));;
Print("INPUT|",L096JSON(List(inp.parabolic_generators,gs->List(gs,g->ListPerm(g,12)))),"\n");;
ans:=L096AllResidues(inp);;
Print("RESULT|",L096JSON(ans),"\n");;
Print("PASS_M12_MISSING_CLASS18\n");;QUIT;
