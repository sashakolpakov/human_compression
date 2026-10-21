# Focused algebra checks for phase12_class_three.md.
# No SmallGroups catalogue is used. Dependencies: GAP and NQ.
# Run: gap -q phase12_class_three_check.g

if LoadPackage("nq")=fail then Error("NQ package required");fi;
F:=FreeGroup("a","b");;
H:=NilpotentQuotient(F,3);;
gs:=GeneratorsOfGroup(H);;
a:=gs[1];;b:=gs[2];;
d:=Comm(b,a);;e:=Comm(d,a);;f:=Comm(d,b);;
identities:=[Comm(a^2,d)=e^-2,Comm(b^2,d)=f^-2,
 Comm(b^2,a^2)=d^4*e^2*f^2];;
if not ForAll(identities,x->x) then Error("Collection identity failure");fi;
if not ForAll([e,f],z->Comm(z,a)=One(H) and Comm(z,b)=One(H)) then
 Error("Centrality failure");fi;
if Size(H)<>infinity then Error("Expected free torsion-free nilpotent group");fi;

# An exact class-three 2-group whose Frattini subgroup is not powerful.
# This shows that the new class-three family is not contained in the
# earlier hereditary-powerful-Frattini family. It is not a TPP violation.
fa:=F.1;;fb:=F.2;;fd:=Comm(fb,fa);;fe:=Comm(fd,fa);;ff:=Comm(fd,fb);;
R:=NilpotentQuotient(F/[fa^8,fb^8,fd^4,fe^4,ff^4],3);;
rg:=GeneratorsOfGroup(R);;
ra:=rg[1];;rb:=rg[2];;rd:=Comm(rb,ra);;re:=Comm(rd,ra);;rf:=Comm(rd,rb);;
K:=Subgroup(R,[ra^2,rb^2,rd,re,rf]);;
W:=Subgroup(K,List(Elements(K),u->u^2));;
K4:=Subgroup(K,List(Elements(K),u->u^4));;
D:=DerivedSubgroup(K);;
if Size(R)<>4096 or NilpotencyClassOfGroup(R)<>3 then Error("R invariants");fi;
if Size(K)<>1024 or Exponent(K)<>4 then Error("K invariants");fi;
if Index(K,W)<>32 or Size(D)<>4 or Size(K4)<>1 then Error("Powerful boundary");fi;
if not IsSubgroup(Center(K),W) then Error("Central squares failure");fi;
if D<>Subgroup(K,[re^2,rf^2]) then Error("Commutator generation failure");fi;
# K is Phi(R): it contains the derived subgroup and both generator
# squares, and R/K is elementary abelian of order four.
if not IsNormal(R,K) then Error("K normality");fi;
if not IsSubgroup(K,DerivedSubgroup(R)) then Error("K contains derived");fi;
if Index(R,K)<>4 then Error("Frattini index");fi;

Print("GAP=",GAPInfo.Version,"; NQ=",PackageInfo("nq")[1].Version,"\n");
Print("free_class_three_collection_identities=",identities,"; central_weight_three_commutators=PASS\n");
Print("boundary_R_order=",Size(R),"; class=",NilpotencyClassOfGroup(R),"\n");
Print("Phi_R_order=",Size(K),"; exponent=",Exponent(K),"; generator_number=",LogInt(Index(K,W),2),"\n");
Print("Phi_R_derived_order=",Size(D),"; Phi_R_fourth_power_subgroup_order=",Size(K4),"; powerful=false\n");
Print("central_square_subgroup_order=",Size(W),"; exact_commutator_generation=PASS\n");
Print("PASS: universal collection identities and strict-family boundary witness.\n");
Print("Scope: no catalogue, no TPP census, and no computational proof of the uniform theorem.\n");
QUIT;
