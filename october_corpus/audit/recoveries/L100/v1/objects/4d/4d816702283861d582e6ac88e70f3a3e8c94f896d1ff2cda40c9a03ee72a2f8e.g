# Initialization-only diagnostic; no family comparison, census, or source result.
SizeScreen([100000,24]);;
Print("INIT_START\n");
INPUT_CATALOGUE:="/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_component_v2/input_catalogue01.g";;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_component_v2/catalogue_loader_v2.g");;
Print("FIXED_MODEL_LOADED\n");
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/postprocess_target01/automorphisms.g");;
ProbeSavedAut:=function(G,data,out)
 local gs,autgens,i,phi,A,nice,K;
 gs:=GeneratorsOfGroup(G);if gs<>data.group_generators then Error("literal model mismatch");fi;
 autgens:=[];
 for i in [1..Length(data.automorphism_generator_images)] do
  Print("MAP_BEGIN ",i,"\n");
  phi:=GroupHomomorphismByImages(G,G,gs,data.automorphism_generator_images[i]);
  if phi=fail then Error("not a homomorphism");fi;
  Print("MAP_CONSTRUCTED ",i,"\n");
  if not IsBijective(phi) then Error("not bijective");fi;
  Add(autgens,phi);Print("MAP_VERIFIED ",i,"\n");
 od;
 A:=Group(autgens);Print("GENERATOR_GROUP_CONSTRUCTED\n");
 if not IsGroupOfAutomorphismsFiniteGroup(A) then Error("automorphism group property");fi;
 Print("AUTOMORPHISM_GROUP_PROPERTY_CHECKED\n");
 # Acquired equality of these exact generator maps with the earlier full group.
 SetSize(A,data.automorphism_order);
 Print("EXACT_ACQUIRED_ORDER_SET ",Size(A),"\n");
 nice:=NiceMonomorphism(A);K:=Image(nice);
 if Size(K)<>data.automorphism_order then Error("faithful-image size mismatch");fi;
 PrintTo(Concatenation(out,"/action.g"),"SavedAutAction:=",rec(order:=Size(K),degree:=LargestMovedPoint(K),images:=List(autgens,a->Image(nice,a)),generator_images:=data.automorphism_generator_images),";\n");
 Print("PASS_SAVED_AUT_INITIALIZATION order=",Size(K)," degree=",LargestMovedPoint(K),"\n");
end;
ProbeSavedAut(G,L100FullAutData,OUTPUT_DIR);;
QUIT_GAP(0);
