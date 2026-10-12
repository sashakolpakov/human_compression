Read("prior_representatives.g");;
Read("shadow_residues_sparse.g");;
L096Inputs:=[];;n:=[0,0,0,0,0];;
for i in [1..Length(SporadicRepresentatives)] do
 r:=SporadicRepresentatives[i];k:=Length(r.parabolics);if k<3 then continue;fi;
 if not r.twot then Error("prior local2T premise");fi;
 n[k]:=n[k]+1;Add(L096Inputs,rec(member:=Concatenation("prior_m23.rk",String(k)),active:=n[k],construction:=i,expected_order:=10200960,parabolic_generators:=List(r.parabolics,GeneratorsOfGroup)));
 Print("PRIOR|",i,"|",k,"|",List(r.parabolics,Size),"|",r.borel_order,"\n");
od;
PrintTo("prior_inputs.g","L096Inputs:=",L096Inputs,";;\n");
Print("PASS_M23_PRIOR_ROSTER\n");QUIT;
