# Exact independent enumeration of the dimension-doubling corollary.
LogTo("research/leemans/algebra_intersection_check.log");
start:=Runtime();;
k:=GF(2);; L:=GF(2^27);; z:=Z(2^27);;
if z^(2^9)=z then Error("The extension generator lacks degree 27"); fi;
I4:=IdentityMat(4,L);;
N0:=NullMat(4,4,k);; N0[1][3]:=One(k);; N0[2][4]:=One(k);;
N1:=TransposedMat(N0);;
N2:=NullMat(4,4,k);;
N2[1][4]:=One(k);; N2[2][3]:=One(k);; N2[2][4]:=One(k);;
for N in [N0,N1,N2] do
  if N*N<>NullMat(4,4,k) then Error("Not square-zero"); fi;
od;
U:=(I4+z*N0)*(I4+z^3*N1)*(I4+z^9*N2);; Uinv:=U^-1;;
all:=Elements(GL(4,2));;
if Length(all)<>20160 then Error("Wrong group order"); fi;
intersection:=[];;
for M in all do
  B:=Uinv*M*U;
  if ForAll(Flat(B),entry->entry^2=entry) then
    Add(intersection,M);
    if B<>M then Error("Nonconstant conjugate in intersection"); fi;
  fi;
od;
A:=One(k)*[[0,1],[1,1]];; expected:=[];;
for P in [IdentityMat(2,k),A,A^2] do
  M:=NullMat(4,4,k);
  for i in [1..2] do for j in [1..2] do
    M[i][j]:=P[i][j]; M[i+2][j+2]:=P[i][j];
  od; od;
  Add(expected,M);
od;
if Set(intersection)<>Set(expected) then Error("Incorrect algebra-unit intersection"); fi;
Print("GAP ",GAPInfo.Version,"\n");
Print("Base group GL(4,2), full enumeration ",Length(all),"\n");
Print("Extension degree 27; intersection size ",Length(intersection),"\n");
Print("Intersection exactly diag(P,P) for P in GF(4)^times\n");
Print("CPU milliseconds ",Runtime()-start,"\nPASS\n");
LogTo();
QUIT;
