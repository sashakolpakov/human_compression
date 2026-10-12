# Exact group naming and a redundant matrix-algebra check.
# Read the generated constructed.g first. No graph-isomorphism package is used.
F:=GF(3);;
G:=Group(List(coordinate_generators,PermList));;
P:=Group(List(point_generators,PermList));;
if Size(G)<>443520 or Size(P)<>443520 then Error("faithful action orders");fi;
natural:=GroupHomomorphismByImages(G,P,List(coordinate_generators,PermList),List(point_generators,PermList));;
if natural=fail or Size(Kernel(natural))<>1 or Image(natural)<>P then Error("natural action identification");fi;
iso:=IsomorphismGroups(P,MathieuGroup(22));;
if iso=fail or Size(Kernel(iso))<>1 or Size(Image(iso))<>443520 then Error("Mathieu identification");fi;
if not IsPrimitive(G,[1..176]) or Size(Stabilizer(G,1))<>2520 then Error("primitive source action");fi;
if IsomorphismGroups(Stabilizer(G,1),AlternatingGroup(7))=fail then Error("source action stabilizer");fi;
dim:=Dimension(AlgebraWithOne(F,List(module_matrices,M->M*One(F))));;
if dim<>441 then Error("matrix algebra");fi;
s:=OutputTextFile("identification.json",false);;SetPrintFormattingStatus(s,false);;
PrintTo(s,"{\"status\":\"PASS\",\"group\":\"M22\",\"order\":443520,\"point_degree\":22,\"coordinate_degree\":176,\"primitive\":true,\"coordinate_stabilizer\":\"A7\",\"stabilizer_order\":2520,\"matrix_algebra_dimension\":441,\"retained_group_name\":\"GAP MathieuGroup(22)\"}\n");
CloseStream(s);;
Print("LCD176_IDENTIFICATION_PASS\n");
