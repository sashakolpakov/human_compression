# Independent exhaustive rank-three/class-at-most-four marked quotient census.
# The candidates are ALL normal kernels of the universal class-four quotient
# having order 128 upstairs and preserving the full class-two quotient.
# No proposed alpha/beta parameter filter or group catalogue is used.
if LoadPackage("nq")=fail then Error("NQ required"); fi;
SizeScreen([240,40]);;
F:=FreeGroup("a","b","c");; f:=GeneratorsOfGroup(F);;
Fpres:=F/[f[1]^2,f[2]^2,f[3]^2,Comm(f[1],f[3])];;
epi:=NqEpimorphismNilpotentQuotient(Fpres,4);; Q:=Image(epi);;
qmark:=List(GeneratorsOfGroup(Fpres),x->Image(epi,x));;
iso:=IsomorphismPermGroup(Q);; P:=Image(iso);;
r:=List(qmark,x->Image(iso,x));;
if Subgroup(P,r)<>P or not ForAll(r,x->Order(x)=2) or Comm(r[1],r[3])<>One(P) then Error("Distinguished marking");fi;
lc:=LowerCentralSeries(P);; K:=lc[3];;
if Size(P)<>4096 or Size(K)<>128 then Error("Universal order mismatch");fi;
NN:=NormalSubgroups(P);;
subsets:=Combinations([1..3]);;
candidates:=0;;accepted:=0;;meets:=0;;closureCount:=0;;
central:=0;;cyclic:=0;;noncyclic:=0;;
Print("VERSION GAP=",GAPInfo.Version," NQ=",PackageInfo("nq")[1].Version,"\n");
Print("UNIVERSAL order=",Size(P)," gamma3=",Size(K)," normals=",Length(NN),"\n");
pi:=fail;;G:=fail;;s:=[];;
for N in NN do
 if Size(N)<>32 or not IsSubgroup(K,N) then continue;fi;
 candidates:=candidates+1;
 pi:=NaturalHomomorphismByNormalSubgroup(P,N);;
 G:=Image(pi);;s:=List(r,x->Image(pi,x));;
 if Size(G)<>128 then Error("Quotient order");fi;
 groups:=List(subsets,J->Subgroup(G,s{J}));;
 closureCount:=closureCount+Length(groups);
 ip:=true;
 for i in [1..8] do
  for j in [1..8] do
   pos:=Position(subsets,Intersection(subsets[i],subsets[j]));
   if Intersection(groups[i],groups[j])<>groups[pos] then ip:=false;fi;
   meets:=meets+1;
  od;
 od;
 type:=List([1..2],i->Order(s[i]*s[i+1]));
 if Minimum(type)<4 then Error("Unexpected degenerate retained class-two quotient");fi;
 if ip then
  accepted:=accepted+1;
  gam:=LowerCentralSeries(G);;kh:=gam[3];;
  if Size(kh)<>4 then Error("Kernel size");fi;
  cent:=IsSubgroup(Centre(G),kh);
  if cent then central:=central+1;kind:="central";
  elif IsCyclic(kh) then cyclic:=cyclic+1;kind:="C4";
  else noncyclic:=noncyclic+1;kind:="V4";fi;
  Print("ACCEPT type=",type," class=",Length(gam)-1," kernel=",kind,"\n");
 fi;
od;
Print("RESULT candidates=",candidates," accepted=",accepted," central=",central," cyclic_noncentral=",cyclic," V4_noncentral=",noncyclic," parabolics=",closureCount," meets=",meets,"\n");
if accepted<>13 or central<>6 or cyclic<>4 or noncyclic<>3 then Error("Proposed rank-three count disagrees with exhaustive census");fi;
Print("PASS: exhaustive bounded quotient census; no all-rank conclusion from this computation.\n");
QUIT;
