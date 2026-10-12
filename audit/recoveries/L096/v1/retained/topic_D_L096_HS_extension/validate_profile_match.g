Read("profile_match.g");;
Read("intersection_profiles.g");;
Read("archive_data/inputs.g");;
G:=Group(Concatenation(L096Inputs[1].parabolic_generators));;ctx:=AutomorphismGroup(G);;
caches:=List([1..Length(L096Inputs)],i->rec());;
Print("AUT|",Size(ctx),"\n");
pairs:=[[1, 1, true], [2, 2, true], [3, 2, true], [4, 4, true], [5, 4, true], [6, 6, true], [7, 7, true], [8, 8, true], [9, 9, true], [10, 10, true], [11, 11, true], [12, 12, true], [13, 13, true], [14, 14, true], [15, 14, true], [16, 16, true], [17, 16, true], [18, 18, true], [19, 18, true], [20, 20, true], [21, 20, true], [22, 22, true], [23, 22, true], [24, 24, true], [25, 24, true], [26, 26, true], [27, 26, true], [28, 28, true], [29, 29, true], [30, 30, true], [31, 31, true], [1, 2, false], [2, 4, false], [4, 6, false], [6, 7, false], [7, 8, false], [8, 9, false], [9, 10, false], [10, 11, false], [11, 12, false], [12, 13, false], [13, 14, false], [14, 16, false], [16, 18, false], [18, 20, false], [20, 22, false], [22, 24, false], [24, 26, false], [26, 28, false], [28, 29, false], [29, 30, false], [30, 31, false]];;
for pair in pairs do
 p:=List(L096Inputs[pair[1]].parabolic_generators,Group);q:=List(L096Inputs[pair[2]].parabolic_generators,Group);
 if L096ProfileEquivalent(ctx,p,L096Profiles[pair[1]],q,L096Profiles[pair[2]],caches[pair[2]])<>pair[3] then Error("old/new transporter mismatch");fi;
 Print("PAIR|",pair,"\n");od;
Print("PASS_PROFILE_MATCHING\n");QUIT;
