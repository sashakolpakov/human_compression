# Exact presentation check for the forced order-32 quotient.
# Dependency: GAP and NQ. No SmallGroups catalogue.
if LoadPackage("nq")=fail then Error("NQ package required");fi;
F:=FreeGroup("a","b");;
a:=F.1;;b:=F.2;;d:=Comm(b,a);;
Q:=NilpotentQuotient(F/[a^4,b^4,d^2,Comm(d,a),Comm(d,b)*a^-2],3);;
gs:=GeneratorsOfGroup(Q);;a:=gs[1];;b:=gs[2];;d:=Comm(b,a);;
K:=Subgroup(Q,[a^2,b^2,d]);;
if Size(Q)<>32 or NilpotencyClassOfGroup(Q)<>3 then Error("Q invariants");fi;
if Size(K)<>8 or Exponent(K)<>2 then Error("Frattini invariants");fi;
if Comm(d,a)<>One(Q) or Comm(d,b)<>a^2 then Error("Relations");fi;
if not IsCentral(Q,a^2) then Error("Support centrality");fi;
if Comm(b^2,a)<>a^2 then Error("Canonical action");fi;
Print("GAP=",GAPInfo.Version,"; NQ=",PackageInfo("nq")[1].Version,"\n");
Print("quotient_order=",Size(Q),"; class=",NilpotencyClassOfGroup(Q),"; Frattini_order=",Size(K),"; Frattini_exponent=",Exponent(K),"\n");
Print("canonical_action_relations=PASS\n");
Print("PASS: the displayed presentation gives the required order-32 quotient.\n");
QUIT;
