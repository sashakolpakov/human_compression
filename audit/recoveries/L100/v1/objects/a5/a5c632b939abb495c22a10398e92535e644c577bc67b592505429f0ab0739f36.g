# Retained subgroup/inclusion input preparation only. No RunBorel or extension.
LoadPackage("tomlib");;
SizeScreen([100000,24]);;
inputTom:=TableOfMarks("L3(4)");;
inputOriginal:=UnderlyingGroup(inputTom);;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/result.g");;
G:=Group(PSL34RankTwo.group_generators);;
inputSources:=[(2,3)(4,6)(5,8)(9,12)(10,14)(11,15)(13,17)(20,21),
 (1,2,4,7)(3,5,9,13)(6,10,15,19)(8,11)(12,16)(14,18,20,17)];;
inputImages:=[(1,13)(2,15)(3,6)(4,20)(7,19)(9,14)(10,12)(16,21),
 (1,14,7,2)(3,17,21,19)(4,16,12,11)(5,15)(8,10,9,18)(13,20)];;
if Group(inputSources)<>inputOriginal then Error("wrong source model");fi;
inputMap:=GroupHomomorphismByImages(inputOriginal,G,inputSources,inputImages);;
if inputMap=fail or not IsBijective(inputMap) then Error("model map not bijective");fi;
reps:=List([1..Length(OrdersTom(inputTom))],i->Image(inputMap,RepresentativeTom(inputTom,i)));;
if List(reps,Size)<>OrdersTom(inputTom) then Error("representative orders changed");fi;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_applicability_work/legacy_initialization.g");;
inputFileIndex:=LIBTOMLIST.positions[Position(LIBTOMLIST.names,"l3(4)")][1];;
inputFile:=Concatenation(LIBTOMLIST.files[inputFileIndex],".tom");;
Print("EXACT_TABLE_FILE ",inputFile,"\n");
Print("INPUT_READY classes=",Length(reps)," maximal_inclusions=",Length(maxinclusions),
 " local2T_inclusions=",Length(local2T),"\n");
PrintTo("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_applicability_work/input_catalogue01.g",
 "PSL34CompleteInput:=rec(table_name:=\"L3(4)\",table_file:=\"",inputFile,"\",",
 "source_generators:=",inputSources,", image_generators:=",inputImages,",",
 "representatives:=",List(reps,GeneratorsOfGroup),",orders:=",List(reps,Size),",",
 "maximal_inclusions:=",List(maxinclusions,p->List(p,GeneratorsOfGroup)),",",
 "inclusion_orders:=",List(maxinclusions,p->List(p,Size)),",",
 "require_2T:=false);\n");
Print("PASS_COMPLETE_RETAINED_INPUT_PREPARATION_NO_EXTENSIONS\n");
QUIT_GAP(0);
