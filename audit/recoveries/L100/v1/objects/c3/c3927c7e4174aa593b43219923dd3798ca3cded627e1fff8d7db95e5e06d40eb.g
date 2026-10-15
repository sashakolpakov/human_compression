SizeScreen([100000,24]);;
Read("/Users/sasha/medusa/research/leemans/phase4_geometry_checks.g");;
broadCount:=0;;notTwoCount:=0;;
G:=SymmetricGroup(3);;
for bid in [1..4] do
 Read(Concatenation("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_applicability_work/small_models01/S3","/b",String(bid),"_done.g"));
 for fam in borelResult.geometries do
  if Length(fam)<2 then continue;fi;
  pars:=List([1..Length(fam)],i->Group(Concatenation(List(fam{Difference([1..Length(fam)],[i])},GeneratorsOfGroup))));
  r:=VerifyGeometry(G,pars);
  if not (r.firm and r.ft and r.rc and r.rwpri and r.ip2 and r.join and r.borel=borelResult.order) then Error("broad witness failure");fi;
  broadCount:=broadCount+1;if not r.twot then notTwoCount:=notTwoCount+1;fi;
 od;
od;
G:=Group((1,2),(3,4));;
for bid in [1..5] do
 Read(Concatenation("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_applicability_work/small_models01/C2xC2","/b",String(bid),"_done.g"));
 for fam in borelResult.geometries do
  if Length(fam)<2 then continue;fi;
  pars:=List([1..Length(fam)],i->Group(Concatenation(List(fam{Difference([1..Length(fam)],[i])},GeneratorsOfGroup))));
  r:=VerifyGeometry(G,pars);
  if not (r.firm and r.ft and r.rc and r.rwpri and r.ip2 and r.join and r.borel=borelResult.order) then Error("broad witness failure");fi;
  broadCount:=broadCount+1;if not r.twot then notTwoCount:=notTwoCount+1;fi;
 od;
od;
G:=Group((1,2,3,4),(2,4));;
for bid in [1..8] do
 Read(Concatenation("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_applicability_work/small_models01/D8","/b",String(bid),"_done.g"));
 for fam in borelResult.geometries do
  if Length(fam)<2 then continue;fi;
  pars:=List([1..Length(fam)],i->Group(Concatenation(List(fam{Difference([1..Length(fam)],[i])},GeneratorsOfGroup))));
  r:=VerifyGeometry(G,pars);
  if not (r.firm and r.ft and r.rc and r.rwpri and r.ip2 and r.join and r.borel=borelResult.order) then Error("broad witness failure");fi;
  broadCount:=broadCount+1;if not r.twot then notTwoCount:=notTwoCount+1;fi;
 od;
od;
G:=AlternatingGroup(4);;
for bid in [1..5] do
 Read(Concatenation("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_applicability_work/small_models01/A4","/b",String(bid),"_done.g"));
 for fam in borelResult.geometries do
  if Length(fam)<2 then continue;fi;
  pars:=List([1..Length(fam)],i->Group(Concatenation(List(fam{Difference([1..Length(fam)],[i])},GeneratorsOfGroup))));
  r:=VerifyGeometry(G,pars);
  if not (r.firm and r.ft and r.rc and r.rwpri and r.ip2 and r.join and r.borel=borelResult.order) then Error("broad witness failure");fi;
  broadCount:=broadCount+1;if not r.twot then notTwoCount:=notTwoCount+1;fi;
 od;
od;
G:=Group((1,2,3));;
for bid in [1..2] do
 Read(Concatenation("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_applicability_work/small_models01/C3","/b",String(bid),"_done.g"));
 for fam in borelResult.geometries do
  if Length(fam)<2 then continue;fi;
  pars:=List([1..Length(fam)],i->Group(Concatenation(List(fam{Difference([1..Length(fam)],[i])},GeneratorsOfGroup))));
  r:=VerifyGeometry(G,pars);
  if not (r.firm and r.ft and r.rc and r.rwpri and r.ip2 and r.join and r.borel=borelResult.order) then Error("broad witness failure");fi;
  broadCount:=broadCount+1;if not r.twot then notTwoCount:=notTwoCount+1;fi;
 od;
od;
G:=Group((1,2,3),(4,5,6));;
for bid in [1..6] do
 Read(Concatenation("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_applicability_work/small_models01/C3xC3","/b",String(bid),"_done.g"));
 for fam in borelResult.geometries do
  if Length(fam)<2 then continue;fi;
  pars:=List([1..Length(fam)],i->Group(Concatenation(List(fam{Difference([1..Length(fam)],[i])},GeneratorsOfGroup))));
  r:=VerifyGeometry(G,pars);
  if not (r.firm and r.ft and r.rc and r.rwpri and r.ip2 and r.join and r.borel=borelResult.order) then Error("broad witness failure");fi;
  broadCount:=broadCount+1;if not r.twot then notTwoCount:=notTwoCount+1;fi;
 od;
od;
G:=Group((1,2),(3,4),(5,6));;
for bid in [1..16] do
 Read(Concatenation("/Users/sasha/medusa/research/leemans/geometry/psl3_4/exhaustion_applicability_work/rank3_models01/C2xC2xC2","/b",String(bid),"_done.g"));
 for fam in borelResult.geometries do
  if Length(fam)<2 then continue;fi;
  pars:=List([1..Length(fam)],i->Group(Concatenation(List(fam{Difference([1..Length(fam)],[i])},GeneratorsOfGroup))));
  r:=VerifyGeometry(G,pars);
  if not (r.firm and r.ft and r.rc and r.rwpri and r.ip2 and r.join and r.borel=borelResult.order) then Error("broad witness failure");fi;
  broadCount:=broadCount+1;if not r.twot then notTwoCount:=notTwoCount+1;fi;
 od;
od;
if notTwoCount=0 then Error("no strict non-2T control");fi;
Print("PASS_BROAD_RECOGNITION_SMALL_MODELS count=",broadCount," non_2T=",notTwoCount,"\n");
QUIT_GAP(0);
