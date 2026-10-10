# Generate one explicit witness; no subgroup catalogue or census is used.
# The separate Python verifier checks the exported permutation witness
# without GAP or NQ.
if LoadPackage("nq")=fail then Error("NQ required");fi;
SizeScreen([100000,24]);;
F:=FreeGroup(3);; f:=GeneratorsOfGroup(F);;
c:=[Comm(f[1],f[2]),Comm(f[2],f[3])];;
t:=Comm(c[1],f[3]);;
rels:=[f[1]^2,f[2]^2,f[3]^2,Comm(f[1],f[3]),
       c[1]^4,c[2]^4,t^2,c[1]^2*c[2]^2*Comm(c[1],c[2])];;
H:=NilpotentQuotient(F/rels,4);;
s:=GeneratorsOfGroup(H){[1..3]};;
iso:=IsomorphismPermGroup(H);; P:=Image(iso);;
r:=List(s,x->Image(iso,x));;
sets:=Combinations([1..3]);;
groups:=List(sets,I->Subgroup(P,r{I}));;
comparisons:=0;;
for i in [1..8] do for j in [1..8] do
 k:=Position(sets,Intersection(sets[i],sets[j]));
 if Intersection(groups[i],groups[j])<>groups[k] then Error("Original IP");fi;
 comparisons:=comparisons+1;
od;od;
lc:=LowerCentralSeries(P);;
a:=Comm(r[1],r[2]);; b:=Comm(r[2],r[3]);;
z1:=a^2;; z2:=b^2;; central:=lc[4];;
if Size(P)<>256 or Length(lc)<>5 or Size(central)<>2 then Error("Group invariants");fi;
if central<>Subgroup(P,[z1*z2]) or z1=z2 then Error("Diagonal central term");fi;
left:=Subgroup(P,r{[1,2]});; right:=Subgroup(P,r{[2,3]});;
if Size(left)<>16 or Size(right)<>16 or Size(Intersection(left,right))<>2 then Error("Original parabolics");fi;
if Size(Intersection(left,central))<>1 or Size(Intersection(right,central))<>1 then Error("Central intersections");fi;
hom:=NaturalHomomorphismByNormalSubgroup(P,central);; Q:=Image(hom);;
qr:=List(r,x->Image(hom,x));;
meet:=Intersection(Subgroup(Q,qr{[1,2]}),Subgroup(Q,qr{[2,3]}));;
if Size(meet)<>4 or meet<>Subgroup(Q,[qr[2],Image(hom,z1)]) then Error("Quotient meet");fi;
if Image(hom,z1)<>Image(hom,z2) or Order(Image(hom,z1))<>2 then Error("Shared quotient involution");fi;
Print("GAP=",GAPInfo.Version," NQ=",PackageInfo("nq")[1].Version,"\n");
Print("order=",Size(P)," class=",NilpotencyClassOfGroup(P)," type=",List([1..2],i->Order(r[i]*r[i+1])),
      " lower_central_orders=",List(lc,Size)," full_IP_comparisons=",comparisons,"\n");
Print("parabolic_orders=",[Size(left),Size(right)]," original_meet_order=2 last_central_order=2 quotient_meet_order=4\n");
Print("PERMUTATIONS_JSON=",List(r,x->ListPerm(x,LargestMovedPoint(P))),"\n");
Print("PASS: explicit class-four order-256 witness; last-central quotient fails IP.\n");
QUIT;
