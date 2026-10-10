LogTo("research/leemans/phase2_cubic_kernel_check.log");;
F:=FreeGroup("a","b","c");;
a:=F.1;; b:=F.2;; c:=F.3;;
U:=F/[a^2,b^2,c^2,(a*b)^6,(b*c)^6,(a*c)^2,(c*b*a*b)^3];;
ug:=GeneratorsOfGroup(U);;
Q:=Group((1,2)(4,5),(1,4)(2,3)(5,6),(1,5)(2,4));;
qg:=[(1,2)(4,5),(1,4)(2,3)(5,6),(1,5)(2,4)];;
if Size(Q)<>48 then Error("Wrong point group"); fi;
phi:=GroupHomomorphismByImages(U,Q,ug,qg);;
if phi=fail or not IsSurjective(phi) then Error("No point quotient"); fi;
Print("POINT QUOTIENT order=",Size(Q)," epimorphism=true\n");
K:=Kernel(phi);;
Print("KERNEL index=",Index(U,K)," Schreier generators=",Length(GeneratorsOfGroup(K)),"\n");
Print("KERNEL WORD GENERATORS=",GeneratorsOfGroup(K),"\n");
iso:=IsomorphismFpGroup(K);;
P:=Image(iso);;
Print("RAW KERNEL PRESENTATION generators=",Length(GeneratorsOfGroup(P)),
      " relators=",Length(RelatorsOfFpGroup(P)),"\n");
Print("RAW RELATORS=",RelatorsOfFpGroup(P),"\n");
S:=SimplifiedFpGroup(P);;
Print("SIMPLIFIED generators=",GeneratorsOfGroup(S)," relators=",RelatorsOfFpGroup(S),"\n");
if Length(GeneratorsOfGroup(S))<>3 then Error("Unexpected kernel rank"); fi;
# IsAbelian for this explicit small presentation is an exact proof, not an
# inference from abelianization. The separate affine certificate proves its
# abelianization has rank three, hence no omitted torsion relations.
if not IsAbelian(S) then Error("Kernel presentation is not abelian"); fi;
if AbelianInvariants(S)<>[0,0,0] then Error("Kernel is not free abelian rank3"); fi;
Print("KERNEL IS Z^3: exact Reidemeister-Schreier/Tietze presentation PASS\n");
LogTo();
QUIT;
