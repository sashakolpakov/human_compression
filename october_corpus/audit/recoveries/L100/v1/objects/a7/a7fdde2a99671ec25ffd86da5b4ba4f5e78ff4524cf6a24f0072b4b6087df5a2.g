SizeScreen([1000000,24]);;
G:=Group(());;reps:=[];;maxorders:=rec();;maxinclusions:=[];;local2T:=[];;
REQUIRE_2T:=false;;OUTPUT_DIR:="";;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_component_v1/legacy_functions.g");;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_component_v1/accepted_verify.g");;
controlResults:=[];;controlVerified:=0;;controlNonTwo:=0;;
G:=SymmetricGroup(3);;
reps:=List(ConjugacyClassesSubgroups(G),Representative);;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_component_v1/legacy_initialization.g");;
OUTPUT_DIR:="/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_frozen_check01/small/S3";;
controlElts:=Elements(G);;
controlMul:=List(controlElts,x->List(controlElts,y->Position(controlElts,x*y)-1));;
controlEncode:=H->Set(List(Elements(H),x->Position(controlElts,x)-1));;
controlRows:=[];;
for controlBid in [1..Length(reps)] do
 RunBorel(controlBid);
 controlB:=reps[controlBid];controlPanels:=OvergroupsFromInclusions(controlB,maxinclusions);controlLevels:=[];
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
 Add(controlRows,[controlEncode(controlB),List(controlPanels,controlEncode),controlLevels,List(borelResult.geometries,t->List(t,controlEncode))]);
 for controlFam in borelResult.geometries do
  if Length(controlFam)<2 then continue;fi;
  controlPars:=List([1..Length(controlFam)],i->JoinPanels(controlB,controlFam{Difference([1..Length(controlFam)],[i])}));
  controlR:=VerifyGeometry(G,controlPars);
  if not (controlR.firm and controlR.ft and controlR.rc and controlR.rwpri and controlR.ip2 and controlR.join and controlR.borel=Size(controlB)) then Error("broad validation");fi;
  controlVerified:=controlVerified+1;if not controlR.twot then controlNonTwo:=controlNonTwo+1;fi;
 od;
od;
Add(controlResults,[Size(G),controlMul,List(reps,controlEncode),List(maxinclusions,p->List(p,controlEncode)),controlRows]);
G:=Group((1,2),(3,4));;
reps:=List(ConjugacyClassesSubgroups(G),Representative);;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_component_v1/legacy_initialization.g");;
OUTPUT_DIR:="/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_frozen_check01/small/C2xC2";;
controlElts:=Elements(G);;
controlMul:=List(controlElts,x->List(controlElts,y->Position(controlElts,x*y)-1));;
controlEncode:=H->Set(List(Elements(H),x->Position(controlElts,x)-1));;
controlRows:=[];;
for controlBid in [1..Length(reps)] do
 RunBorel(controlBid);
 controlB:=reps[controlBid];controlPanels:=OvergroupsFromInclusions(controlB,maxinclusions);controlLevels:=[];
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
 Add(controlRows,[controlEncode(controlB),List(controlPanels,controlEncode),controlLevels,List(borelResult.geometries,t->List(t,controlEncode))]);
 for controlFam in borelResult.geometries do
  if Length(controlFam)<2 then continue;fi;
  controlPars:=List([1..Length(controlFam)],i->JoinPanels(controlB,controlFam{Difference([1..Length(controlFam)],[i])}));
  controlR:=VerifyGeometry(G,controlPars);
  if not (controlR.firm and controlR.ft and controlR.rc and controlR.rwpri and controlR.ip2 and controlR.join and controlR.borel=Size(controlB)) then Error("broad validation");fi;
  controlVerified:=controlVerified+1;if not controlR.twot then controlNonTwo:=controlNonTwo+1;fi;
 od;
od;
Add(controlResults,[Size(G),controlMul,List(reps,controlEncode),List(maxinclusions,p->List(p,controlEncode)),controlRows]);
G:=Group((1,2,3,4),(2,4));;
reps:=List(ConjugacyClassesSubgroups(G),Representative);;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_component_v1/legacy_initialization.g");;
OUTPUT_DIR:="/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_frozen_check01/small/D8";;
controlElts:=Elements(G);;
controlMul:=List(controlElts,x->List(controlElts,y->Position(controlElts,x*y)-1));;
controlEncode:=H->Set(List(Elements(H),x->Position(controlElts,x)-1));;
controlRows:=[];;
for controlBid in [1..Length(reps)] do
 RunBorel(controlBid);
 controlB:=reps[controlBid];controlPanels:=OvergroupsFromInclusions(controlB,maxinclusions);controlLevels:=[];
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
 Add(controlRows,[controlEncode(controlB),List(controlPanels,controlEncode),controlLevels,List(borelResult.geometries,t->List(t,controlEncode))]);
 for controlFam in borelResult.geometries do
  if Length(controlFam)<2 then continue;fi;
  controlPars:=List([1..Length(controlFam)],i->JoinPanels(controlB,controlFam{Difference([1..Length(controlFam)],[i])}));
  controlR:=VerifyGeometry(G,controlPars);
  if not (controlR.firm and controlR.ft and controlR.rc and controlR.rwpri and controlR.ip2 and controlR.join and controlR.borel=Size(controlB)) then Error("broad validation");fi;
  controlVerified:=controlVerified+1;if not controlR.twot then controlNonTwo:=controlNonTwo+1;fi;
 od;
od;
Add(controlResults,[Size(G),controlMul,List(reps,controlEncode),List(maxinclusions,p->List(p,controlEncode)),controlRows]);
G:=AlternatingGroup(4);;
reps:=List(ConjugacyClassesSubgroups(G),Representative);;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_component_v1/legacy_initialization.g");;
OUTPUT_DIR:="/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_frozen_check01/small/A4";;
controlElts:=Elements(G);;
controlMul:=List(controlElts,x->List(controlElts,y->Position(controlElts,x*y)-1));;
controlEncode:=H->Set(List(Elements(H),x->Position(controlElts,x)-1));;
controlRows:=[];;
for controlBid in [1..Length(reps)] do
 RunBorel(controlBid);
 controlB:=reps[controlBid];controlPanels:=OvergroupsFromInclusions(controlB,maxinclusions);controlLevels:=[];
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
 Add(controlRows,[controlEncode(controlB),List(controlPanels,controlEncode),controlLevels,List(borelResult.geometries,t->List(t,controlEncode))]);
 for controlFam in borelResult.geometries do
  if Length(controlFam)<2 then continue;fi;
  controlPars:=List([1..Length(controlFam)],i->JoinPanels(controlB,controlFam{Difference([1..Length(controlFam)],[i])}));
  controlR:=VerifyGeometry(G,controlPars);
  if not (controlR.firm and controlR.ft and controlR.rc and controlR.rwpri and controlR.ip2 and controlR.join and controlR.borel=Size(controlB)) then Error("broad validation");fi;
  controlVerified:=controlVerified+1;if not controlR.twot then controlNonTwo:=controlNonTwo+1;fi;
 od;
od;
Add(controlResults,[Size(G),controlMul,List(reps,controlEncode),List(maxinclusions,p->List(p,controlEncode)),controlRows]);
G:=Group((1,2,3));;
reps:=List(ConjugacyClassesSubgroups(G),Representative);;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_component_v1/legacy_initialization.g");;
OUTPUT_DIR:="/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_frozen_check01/small/C3";;
controlElts:=Elements(G);;
controlMul:=List(controlElts,x->List(controlElts,y->Position(controlElts,x*y)-1));;
controlEncode:=H->Set(List(Elements(H),x->Position(controlElts,x)-1));;
controlRows:=[];;
for controlBid in [1..Length(reps)] do
 RunBorel(controlBid);
 controlB:=reps[controlBid];controlPanels:=OvergroupsFromInclusions(controlB,maxinclusions);controlLevels:=[];
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
 Add(controlRows,[controlEncode(controlB),List(controlPanels,controlEncode),controlLevels,List(borelResult.geometries,t->List(t,controlEncode))]);
 for controlFam in borelResult.geometries do
  if Length(controlFam)<2 then continue;fi;
  controlPars:=List([1..Length(controlFam)],i->JoinPanels(controlB,controlFam{Difference([1..Length(controlFam)],[i])}));
  controlR:=VerifyGeometry(G,controlPars);
  if not (controlR.firm and controlR.ft and controlR.rc and controlR.rwpri and controlR.ip2 and controlR.join and controlR.borel=Size(controlB)) then Error("broad validation");fi;
  controlVerified:=controlVerified+1;if not controlR.twot then controlNonTwo:=controlNonTwo+1;fi;
 od;
od;
Add(controlResults,[Size(G),controlMul,List(reps,controlEncode),List(maxinclusions,p->List(p,controlEncode)),controlRows]);
G:=Group((1,2,3),(4,5,6));;
reps:=List(ConjugacyClassesSubgroups(G),Representative);;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_component_v1/legacy_initialization.g");;
OUTPUT_DIR:="/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_frozen_check01/small/C3xC3";;
controlElts:=Elements(G);;
controlMul:=List(controlElts,x->List(controlElts,y->Position(controlElts,x*y)-1));;
controlEncode:=H->Set(List(Elements(H),x->Position(controlElts,x)-1));;
controlRows:=[];;
for controlBid in [1..Length(reps)] do
 RunBorel(controlBid);
 controlB:=reps[controlBid];controlPanels:=OvergroupsFromInclusions(controlB,maxinclusions);controlLevels:=[];
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
 Add(controlRows,[controlEncode(controlB),List(controlPanels,controlEncode),controlLevels,List(borelResult.geometries,t->List(t,controlEncode))]);
 for controlFam in borelResult.geometries do
  if Length(controlFam)<2 then continue;fi;
  controlPars:=List([1..Length(controlFam)],i->JoinPanels(controlB,controlFam{Difference([1..Length(controlFam)],[i])}));
  controlR:=VerifyGeometry(G,controlPars);
  if not (controlR.firm and controlR.ft and controlR.rc and controlR.rwpri and controlR.ip2 and controlR.join and controlR.borel=Size(controlB)) then Error("broad validation");fi;
  controlVerified:=controlVerified+1;if not controlR.twot then controlNonTwo:=controlNonTwo+1;fi;
 od;
od;
Add(controlResults,[Size(G),controlMul,List(reps,controlEncode),List(maxinclusions,p->List(p,controlEncode)),controlRows]);
G:=Group((1,2),(3,4),(5,6));;
reps:=List(ConjugacyClassesSubgroups(G),Representative);;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_component_v1/legacy_initialization.g");;
OUTPUT_DIR:="/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_frozen_check01/small/C2xC2xC2";;
controlElts:=Elements(G);;
controlMul:=List(controlElts,x->List(controlElts,y->Position(controlElts,x*y)-1));;
controlEncode:=H->Set(List(Elements(H),x->Position(controlElts,x)-1));;
controlRows:=[];;
for controlBid in [1..Length(reps)] do
 RunBorel(controlBid);
 controlB:=reps[controlBid];controlPanels:=OvergroupsFromInclusions(controlB,maxinclusions);controlLevels:=[];
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
 Add(controlRows,[controlEncode(controlB),List(controlPanels,controlEncode),controlLevels,List(borelResult.geometries,t->List(t,controlEncode))]);
 for controlFam in borelResult.geometries do
  if Length(controlFam)<2 then continue;fi;
  controlPars:=List([1..Length(controlFam)],i->JoinPanels(controlB,controlFam{Difference([1..Length(controlFam)],[i])}));
  controlR:=VerifyGeometry(G,controlPars);
  if not (controlR.firm and controlR.ft and controlR.rc and controlR.rwpri and controlR.ip2 and controlR.join and controlR.borel=Size(controlB)) then Error("broad validation");fi;
  controlVerified:=controlVerified+1;if not controlR.twot then controlNonTwo:=controlNonTwo+1;fi;
 od;
od;
Add(controlResults,[Size(G),controlMul,List(reps,controlEncode),List(maxinclusions,p->List(p,controlEncode)),controlRows]);
PrintTo("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_frozen_check01/small/models.json",controlResults,"\n");
if controlVerified<>64 or controlNonTwo<>8 then Error("recognition control inventory");fi;
INPUT_CATALOGUE:="/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_component_v1/input_catalogue01.g";;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_component_v1/catalogue_loader_v2.g");;
if Length(reps)<>95 or Length(maxinclusions)<>367 or REQUIRE_2T<>false then Error("loader contract");fi;
Print("PASS_FRESH_SEVEN_MODELS_AND_LOADER_NO_L100_EXTENSIONS\n");
QUIT_GAP(0);
