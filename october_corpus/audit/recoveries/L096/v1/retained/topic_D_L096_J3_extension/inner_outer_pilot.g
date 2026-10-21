Read("inner_outer_direct.g");;Read("archive_data/inputs.g");;Read("intersection_profiles.g");;
G:=Group(Concatenation(L096Inputs[1].parabolic_generators));;ctx:=L096IOSetup(G);;Print("SETUP_PASS\n");
for pair in [[8,7],[10,9],[11,9],[14,13],[17,16]] do
 p:=List(L096Inputs[pair[1]].parabolic_generators,Group);q:=List(L096Inputs[pair[2]].parabolic_generators,Group);
 Print("START|",pair,"\n");
 Print("PAIR|",pair,"|",L096IOEquivalent(ctx,p,L096Profiles[pair[1]],q,L096Profiles[pair[2]]),"\n");
od;
Print("PASS_J3_INNER_OUTER_PILOT\n");QUIT;
