SizeScreen([1000000,24]);;
G:=Group(());;reps:=[];;maxorders:=rec();;maxinclusions:=[];;local2T:=[];;
REQUIRE_2T:=false;;OUTPUT_DIR:="";;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_applicability_work/legacy_functions.g");;
controlResults:=[];;
G:=SymmetricGroup(3);;
reps:=List(ConjugacyClassesSubgroups(G),Representative);;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_applicability_work/legacy_initialization.g");;
OUTPUT_DIR:="/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_applicability_work/small_models01/S3";;
controlElts:=Elements(G);;
controlMul:=List(controlElts,x->List(controlElts,y->Position(controlElts,x*y)-1));;
controlEncode:=H->Set(List(Elements(H),x->Position(controlElts,x)-1));;
controlRows:=[];;
for controlBid in [1..Length(reps)] do
 RunBorel(controlBid);
 controlB:=reps[controlBid];controlPanels:=OvergroupsFromInclusions(controlB,maxinclusions);
 controlLevels:=[];
 if Length(controlPanels)>0 then
  controlA:=Image(ActionHomomorphism(Normalizer(G,controlB),controlPanels,OnPoints));
  Add(controlLevels,List(Orbits(controlA,[1..Length(controlPanels)]),o->[o[1]-1]));
  for controlRank in [2..Length(FactorsInt(Index(G,controlB)))+1] do
   Read(Concatenation(OUTPUT_DIR,"/b",String(controlBid),"_r",String(controlRank),".g"));
   if borelCheckpoint.panels<>controlPanels then Error("panel ordering changed");fi;
   Add(controlLevels,List(borelCheckpoint.level,t->List(t,i->i-1)));
   if Length(borelCheckpoint.level)=0 then break;fi;
  od;
 fi;
 Read(Concatenation(OUTPUT_DIR,"/b",String(controlBid),"_done.g"));
 Add(controlRows,[controlEncode(controlB),List(controlPanels,controlEncode),controlLevels,
   List(borelResult.geometries,t->List(t,controlEncode))]);
od;
Add(controlResults,[Size(G),controlMul,List(reps,controlEncode),
 List(maxinclusions,p->List(p,controlEncode)),controlRows]);
G:=Group((1,2),(3,4));;
reps:=List(ConjugacyClassesSubgroups(G),Representative);;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_applicability_work/legacy_initialization.g");;
OUTPUT_DIR:="/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_applicability_work/small_models01/C2xC2";;
controlElts:=Elements(G);;
controlMul:=List(controlElts,x->List(controlElts,y->Position(controlElts,x*y)-1));;
controlEncode:=H->Set(List(Elements(H),x->Position(controlElts,x)-1));;
controlRows:=[];;
for controlBid in [1..Length(reps)] do
 RunBorel(controlBid);
 controlB:=reps[controlBid];controlPanels:=OvergroupsFromInclusions(controlB,maxinclusions);
 controlLevels:=[];
 if Length(controlPanels)>0 then
  controlA:=Image(ActionHomomorphism(Normalizer(G,controlB),controlPanels,OnPoints));
  Add(controlLevels,List(Orbits(controlA,[1..Length(controlPanels)]),o->[o[1]-1]));
  for controlRank in [2..Length(FactorsInt(Index(G,controlB)))+1] do
   Read(Concatenation(OUTPUT_DIR,"/b",String(controlBid),"_r",String(controlRank),".g"));
   if borelCheckpoint.panels<>controlPanels then Error("panel ordering changed");fi;
   Add(controlLevels,List(borelCheckpoint.level,t->List(t,i->i-1)));
   if Length(borelCheckpoint.level)=0 then break;fi;
  od;
 fi;
 Read(Concatenation(OUTPUT_DIR,"/b",String(controlBid),"_done.g"));
 Add(controlRows,[controlEncode(controlB),List(controlPanels,controlEncode),controlLevels,
   List(borelResult.geometries,t->List(t,controlEncode))]);
od;
Add(controlResults,[Size(G),controlMul,List(reps,controlEncode),
 List(maxinclusions,p->List(p,controlEncode)),controlRows]);
G:=Group((1,2,3,4),(2,4));;
reps:=List(ConjugacyClassesSubgroups(G),Representative);;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_applicability_work/legacy_initialization.g");;
OUTPUT_DIR:="/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_applicability_work/small_models01/D8";;
controlElts:=Elements(G);;
controlMul:=List(controlElts,x->List(controlElts,y->Position(controlElts,x*y)-1));;
controlEncode:=H->Set(List(Elements(H),x->Position(controlElts,x)-1));;
controlRows:=[];;
for controlBid in [1..Length(reps)] do
 RunBorel(controlBid);
 controlB:=reps[controlBid];controlPanels:=OvergroupsFromInclusions(controlB,maxinclusions);
 controlLevels:=[];
 if Length(controlPanels)>0 then
  controlA:=Image(ActionHomomorphism(Normalizer(G,controlB),controlPanels,OnPoints));
  Add(controlLevels,List(Orbits(controlA,[1..Length(controlPanels)]),o->[o[1]-1]));
  for controlRank in [2..Length(FactorsInt(Index(G,controlB)))+1] do
   Read(Concatenation(OUTPUT_DIR,"/b",String(controlBid),"_r",String(controlRank),".g"));
   if borelCheckpoint.panels<>controlPanels then Error("panel ordering changed");fi;
   Add(controlLevels,List(borelCheckpoint.level,t->List(t,i->i-1)));
   if Length(borelCheckpoint.level)=0 then break;fi;
  od;
 fi;
 Read(Concatenation(OUTPUT_DIR,"/b",String(controlBid),"_done.g"));
 Add(controlRows,[controlEncode(controlB),List(controlPanels,controlEncode),controlLevels,
   List(borelResult.geometries,t->List(t,controlEncode))]);
od;
Add(controlResults,[Size(G),controlMul,List(reps,controlEncode),
 List(maxinclusions,p->List(p,controlEncode)),controlRows]);
G:=AlternatingGroup(4);;
reps:=List(ConjugacyClassesSubgroups(G),Representative);;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_applicability_work/legacy_initialization.g");;
OUTPUT_DIR:="/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_applicability_work/small_models01/A4";;
controlElts:=Elements(G);;
controlMul:=List(controlElts,x->List(controlElts,y->Position(controlElts,x*y)-1));;
controlEncode:=H->Set(List(Elements(H),x->Position(controlElts,x)-1));;
controlRows:=[];;
for controlBid in [1..Length(reps)] do
 RunBorel(controlBid);
 controlB:=reps[controlBid];controlPanels:=OvergroupsFromInclusions(controlB,maxinclusions);
 controlLevels:=[];
 if Length(controlPanels)>0 then
  controlA:=Image(ActionHomomorphism(Normalizer(G,controlB),controlPanels,OnPoints));
  Add(controlLevels,List(Orbits(controlA,[1..Length(controlPanels)]),o->[o[1]-1]));
  for controlRank in [2..Length(FactorsInt(Index(G,controlB)))+1] do
   Read(Concatenation(OUTPUT_DIR,"/b",String(controlBid),"_r",String(controlRank),".g"));
   if borelCheckpoint.panels<>controlPanels then Error("panel ordering changed");fi;
   Add(controlLevels,List(borelCheckpoint.level,t->List(t,i->i-1)));
   if Length(borelCheckpoint.level)=0 then break;fi;
  od;
 fi;
 Read(Concatenation(OUTPUT_DIR,"/b",String(controlBid),"_done.g"));
 Add(controlRows,[controlEncode(controlB),List(controlPanels,controlEncode),controlLevels,
   List(borelResult.geometries,t->List(t,controlEncode))]);
od;
Add(controlResults,[Size(G),controlMul,List(reps,controlEncode),
 List(maxinclusions,p->List(p,controlEncode)),controlRows]);
G:=Group((1,2,3));;
reps:=List(ConjugacyClassesSubgroups(G),Representative);;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_applicability_work/legacy_initialization.g");;
OUTPUT_DIR:="/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_applicability_work/small_models01/C3";;
controlElts:=Elements(G);;
controlMul:=List(controlElts,x->List(controlElts,y->Position(controlElts,x*y)-1));;
controlEncode:=H->Set(List(Elements(H),x->Position(controlElts,x)-1));;
controlRows:=[];;
for controlBid in [1..Length(reps)] do
 RunBorel(controlBid);
 controlB:=reps[controlBid];controlPanels:=OvergroupsFromInclusions(controlB,maxinclusions);
 controlLevels:=[];
 if Length(controlPanels)>0 then
  controlA:=Image(ActionHomomorphism(Normalizer(G,controlB),controlPanels,OnPoints));
  Add(controlLevels,List(Orbits(controlA,[1..Length(controlPanels)]),o->[o[1]-1]));
  for controlRank in [2..Length(FactorsInt(Index(G,controlB)))+1] do
   Read(Concatenation(OUTPUT_DIR,"/b",String(controlBid),"_r",String(controlRank),".g"));
   if borelCheckpoint.panels<>controlPanels then Error("panel ordering changed");fi;
   Add(controlLevels,List(borelCheckpoint.level,t->List(t,i->i-1)));
   if Length(borelCheckpoint.level)=0 then break;fi;
  od;
 fi;
 Read(Concatenation(OUTPUT_DIR,"/b",String(controlBid),"_done.g"));
 Add(controlRows,[controlEncode(controlB),List(controlPanels,controlEncode),controlLevels,
   List(borelResult.geometries,t->List(t,controlEncode))]);
od;
Add(controlResults,[Size(G),controlMul,List(reps,controlEncode),
 List(maxinclusions,p->List(p,controlEncode)),controlRows]);
G:=Group((1,2,3),(4,5,6));;
reps:=List(ConjugacyClassesSubgroups(G),Representative);;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_applicability_work/legacy_initialization.g");;
OUTPUT_DIR:="/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_applicability_work/small_models01/C3xC3";;
controlElts:=Elements(G);;
controlMul:=List(controlElts,x->List(controlElts,y->Position(controlElts,x*y)-1));;
controlEncode:=H->Set(List(Elements(H),x->Position(controlElts,x)-1));;
controlRows:=[];;
for controlBid in [1..Length(reps)] do
 RunBorel(controlBid);
 controlB:=reps[controlBid];controlPanels:=OvergroupsFromInclusions(controlB,maxinclusions);
 controlLevels:=[];
 if Length(controlPanels)>0 then
  controlA:=Image(ActionHomomorphism(Normalizer(G,controlB),controlPanels,OnPoints));
  Add(controlLevels,List(Orbits(controlA,[1..Length(controlPanels)]),o->[o[1]-1]));
  for controlRank in [2..Length(FactorsInt(Index(G,controlB)))+1] do
   Read(Concatenation(OUTPUT_DIR,"/b",String(controlBid),"_r",String(controlRank),".g"));
   if borelCheckpoint.panels<>controlPanels then Error("panel ordering changed");fi;
   Add(controlLevels,List(borelCheckpoint.level,t->List(t,i->i-1)));
   if Length(borelCheckpoint.level)=0 then break;fi;
  od;
 fi;
 Read(Concatenation(OUTPUT_DIR,"/b",String(controlBid),"_done.g"));
 Add(controlRows,[controlEncode(controlB),List(controlPanels,controlEncode),controlLevels,
   List(borelResult.geometries,t->List(t,controlEncode))]);
od;
Add(controlResults,[Size(G),controlMul,List(reps,controlEncode),
 List(maxinclusions,p->List(p,controlEncode)),controlRows]);
PrintTo("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_applicability_work/small_models01/models.json",controlResults,"\n");
Print("PASS_SMALL_MODELS_UNCHANGED_ENGINE_NO_L100_CENSUS\n");
QUIT_GAP(0);
