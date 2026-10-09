# Verify the two independently discovered thin representatives without TomLib.
Read("research/leemans/phase4_geometry_checks.g");;
Read("research/leemans/phase4_thin_j2_witnesses.g");;
if Size(G)<>604800 or not IsSimpleGroup(G) then Error("ambient group failed simple/order check");fi;
for i in [1..Length(thinWitnesses)] do
 t:=thinWitnesses[i];
 if Group(t)<>G or not ForAll(t,x->Order(x)=2) then Error("generator witness failed");fi;
 pars:=List([1..Length(t)],j->Group(t{Difference([1..Length(t)],[j])}));
 r:=VerifyGeometry(G,pars);
 if not (r.firm and r.ft and r.rc and r.rwpri and r.twot and r.ip2 and r.join and r.borel=1) then Error("geometry witness failed");fi;
 Print("WITNESS ",i," orders=",r.orders," borel=",r.borel," all_source_axioms=true\n");
od;
Print("THIN_WITNESSES_PASS count=",Length(thinWitnesses),"\n");
QUIT;
