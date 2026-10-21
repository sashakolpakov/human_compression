Read("programs/string_search.g");;Read("programs/unitary_models.g");;
if not IsBound(OUT) then Error("OUT must be an existing fresh output directory");fi;
Emit:=function(name,g,expected,nodes)
 local result,actual;
 actual:=FreshPermutationOrder(g,name);
 Need(actual=expected,"ambient actual permutation order");
 result:=SearchStrings(g);
 Need(result.complete,"complete enumeration");
 Need(result.nodes=nodes,"full prefix depth counts");
 if name="A5_control" then Need(Length(result.witnesses)=6,"positive connected control");else Need(Length(result.witnesses)=0,"exception elimination");fi;
 PrintTo(Concatenation(OUT,"/",name,"_receipt.g"),"Result:=",result,";\n");
 PrintTo(Concatenation(OUT,"/",name,"_generators.g"),"Generators:=",GeneratorsOfGroup(g),";\n");
 Print("RECORD|",name,"|",actual,"|",result.nodes,"|",result.involution_classes,"|",result.involutions,"|",Length(result.witnesses),"|",result.runtime_ms,"\n");
end;;
Emit("A5_control",AlternatingGroup(5),60,[1,3]);
Emit("A6",AlternatingGroup(6),360,[1,6,18]);
Emit("A7",AlternatingGroup(7),2520,[1,6,28,1]);
Emit("M11",MathieuGroup(11),7920,[1,6,32,3]);
Emit("M22",MathieuGroup(22),443520,[1,8,178,40]);
Emit("M23",MathieuGroup(23),10200960,[1,6,166,77,4]);
mcl:=PrimitiveGroup(275,1);;Need(Name(mcl)="McL","retained named catalogue identity");;
Emit("McL",mcl,898128000,[1,4,132,65,2]);
for nq in [[4,3],[5,2]] do
 model:=MakeUnitary(nq[1],nq[2]);;name:=Concatenation("U",String(nq[1]),"_",String(nq[2]));;
 PrintTo(Concatenation(OUT,"/",name,"_model.g"),"Model:=",model,";\n");
 if nq=[4,3] then Emit(name,model.group,3265920,[1,9,185,36,2]);else Emit(name,model.group,13685760,[2,13,145,26,2]);fi;
od;
Print("L011_CERTIFICATE_PASS\n");QUIT;
