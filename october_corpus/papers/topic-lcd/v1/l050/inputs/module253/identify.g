# Read constructed.g from the exact Python certificate first.
P:=Group(List(point_generators,PermList));;
G:=Group(List(coordinate_generators,PermList));;
if Size(P)<>proved_upper or Size(G)<>proved_upper then Error("order bound not attained");fi;
iso:=IsomorphismGroups(P,MathieuGroup(23));;
if iso=fail or Size(Kernel(iso))<>1 or Size(Image(iso))<>proved_upper then Error("M23 identification");fi;
phi:=GroupHomomorphismByImages(P,G,List(point_generators,PermList),List(coordinate_generators,PermList));;
if phi=fail or Size(Kernel(phi))<>1 or Image(phi)<>G then Error("faithful induced block action");fi;
dim:=Dimension(AlgebraWithOne(GF(3),List(module_matrices,M->M*One(GF(3)))));;
if dim<>484 then Error("augmentation matrix algebra");fi;
t:=BrauerTable("M23",3);;
degrees:=List(Irr(t),x->x[1]);;
if degrees<>[1,22,45,45,104,104,231,253,770,770,990,990,1035] then Error("retained Brauer table");fi;
s:=OutputTextFile("identification.json",false);;SetPrintFormattingStatus(s,false);;
PrintTo(s,"{\"status\":\"PASS\",\"group\":\"M23\",\"order\":",Size(G),",\"matrix_algebra_dimension\":484,\"faithful_block_action\":true,\"retained_Brauer_table\":\"M23mod3\",\"retained_irreducible_degrees\":",degrees,"}\n");
CloseStream(s);;
Print("LCD253_IDENTIFICATION_PASS\n");
