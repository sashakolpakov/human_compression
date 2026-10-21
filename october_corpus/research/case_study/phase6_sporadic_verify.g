# Independent parabolic recognition of all freshly enumerated final witnesses.
# The recognition code is reused; no phase-four geometry data are read.
Read("phase4_geometry_checks.g");;
Read(WITNESS_FILE);;
LoadPackage("tomlib");;
SizeScreen([100000,24]);;
if G<>UnderlyingGroup(TableOfMarks(GROUP_NAME)) then Error("witness group differs from named group");fi;
for i in [1..Length(SporadicRepresentatives)] do
 entry:=SporadicRepresentatives[i];r:=VerifyGeometry(G,entry.parabolics);
 if not (r.firm and r.ft and r.rc and r.rwpri and r.ip2 and r.join and r.borel=entry.borel_order) then Error("independent recognition failed");fi;
 if Group(Concatenation(List(entry.panels,GeneratorsOfGroup)))<>G then Error("panel generation failed");fi;
 for j in [1..Length(entry.panels)] do
  if Intersection(entry.parabolics{Difference([1..Length(entry.panels)],[j])})<>entry.panels[j] then Error("panel reconstruction failed");fi;
 od;
 Print("WITNESS id=",i," rank=",Length(entry.panels)," borel=",r.borel," parabolic_orders=",r.orders," panel_orders=",r.panels," twot=",r.twot," all_requested_axioms=true\n");
od;
Print("ALL_WITNESSES_PASS count=",Length(SporadicRepresentatives),"\n");

