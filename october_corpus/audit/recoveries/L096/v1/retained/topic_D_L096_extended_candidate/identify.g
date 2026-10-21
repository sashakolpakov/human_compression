Read("shadow_residues.g");;
for d in [11,12] do
 Read(Concatenation("data_m",String(d),"/inputs.g"));;
 first:=Group(Concatenation(L096Inputs[1].parabolic_generators));;
 c:=RepresentativeAction(SymmetricGroup(d),first,MathieuGroup(d));;
 if c=fail or first^c<>MathieuGroup(d) then Error("no verified named group transporter");fi;
 for inp in L096Inputs do G:=Group(Concatenation(inp.parabolic_generators));;if G<>first then Error("different ambient archive group");fi;od;
 Print("IDENTIFICATION|",L096JSON(rec(group:=Concatenation("M",String(d)),rows:=Length(L096Inputs),conjugator:=ListPerm(c,d))),"\n");
od;
Print("PASS_MATHIEU_IDENTIFICATION\n");QUIT;
