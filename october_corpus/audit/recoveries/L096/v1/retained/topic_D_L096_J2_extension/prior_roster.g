Read("prior_representatives.g");;
SizeScreen([100000,100000]);;
Read("shadow_residues.g");;
L096Inputs:=[];;
n:=[0,0,0,0];;
for i in [1..Length(J2Representatives)] do
 r:=J2Representatives[i];k:=Length(r.parabolics);if k<3 then continue;fi;
 n[k]:=n[k]+1;Add(L096Inputs,rec(member:=Concatenation("prior_j2.rk",String(k)),active:=n[k],construction:=i,expected_order:=604800,parabolic_generators:=List(r.parabolics,GeneratorsOfGroup)));
 Print("PRIOR|",i,"|",k,"|",List(r.parabolics,Size),"|",r.borel_order,"\n");
od;
PrintTo("prior_inputs.g","L096Inputs:=",L096Inputs,";;\n");
Print("PASS_J2_PRIOR_ROSTER\n");QUIT;
