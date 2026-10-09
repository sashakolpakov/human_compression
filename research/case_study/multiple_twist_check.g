# Complete local-group enumeration, using exact finite-field arithmetic.
LogTo("research/leemans/multiple_twist_check.log");
start:=Runtime();;
L:=GF(3^9);; z:=Z(3^9);;
if z^(3^9)<>z or z^3=z or z^(3^3)=z then Error("Wrong field degree"); fi;
U1:=IdentityMat(3,L);; U1[1][2]:=z;
U2:=IdentityMat(3,L);; U2[2][3]:=z^3;
U:=U1*U2;; Uinv:=U^-1;;
G:=SL(3,3);; all:=Elements(G);;
if Length(all)<>5616 then Error("Wrong base-group order"); fi;
intersection:=[];;
for M in all do
  B:=Uinv*M*U;
  if ForAll(Flat(B),entry->entry^3=entry) then
    Add(intersection,M);
    if B<>M then Error("Intersection element not fixed by the twist"); fi;
  fi;
od;
expected:=[];;
for c in GF(3) do
  M:=IdentityMat(3,GF(3)); M[1][3]:=c; Add(expected,M);
od;
if Set(intersection)<>Set(expected) then Error("Incorrect intersection"); fi;
Print("GAP ",GAPInfo.Version,"\n");
Print("Base field 3, extension degree 9, base-group order ",Length(all),"\n");
Print("Full intersection order ",Length(intersection),"\n");
Print("Intersection is exactly {I+cE13 : c in GF(3)}\n");
Print("CPU milliseconds ",Runtime()-start,"\nPASS\n");
LogTo();
QUIT;
