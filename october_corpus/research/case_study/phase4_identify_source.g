# Check an explicit bijective homomorphism onto the named TomLib J2 group.
Read("research/leemans/phase4_j2_parsed.g");;
Read("research/leemans/phase4_source_isomorphism.g");;
LoadPackage("tomlib");;
target:=UnderlyingGroup(TableOfMarks("J2"));;
source:=sourceData[1].G;;
f:=GroupHomomorphismByImages(source,target,GeneratorsOfGroup(source),source_generator_images);;
if f=fail or not IsBijective(f) or Image(f)<>target then Error("source J2 identification failed");fi;
if not ForAll(sourceData,s->s.G=source) then Error("different source groups require separate identification");fi;
Print("SOURCE_IDENTIFICATION_PASS |source|=",Size(source)," |target|=",Size(target)," bijective=",IsBijective(f)," image_equals_TomLib_J2=",Image(f)=target,"\n");
QUIT;
