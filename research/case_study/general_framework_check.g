# Exact checks of the all-dimension transvection intersection theorem.
LogTo("research/leemans/general_framework_check.log");
CheckTransvectionIntersection := function(p)
  local K,L,n,one,z,t,U,U0,G,good,M,ML,N,C;
  K:=GF(p); L:=GF(p^2); n:=3;
  one:=One(L); z:=Zero(L); t:=Z(p^2);
  U:=IdentityMat(n,L); U[1][2]:=t;
  U0:=IdentityMat(n,K); U0[1][2]:=One(K);
  G:=SL(n,p); good:=[];
  for M in Elements(G) do
    ML:=List(M,row->List(row,a->a*one));
    N:=ML^U;
    if ForAll(Flat(N),a->a^p=a) then Add(good,M); fi;
  od;
  C:=Centralizer(G,U0);
  if Set(good)<>Set(Elements(C)) then Error("General intersection theorem check failed"); fi;
  Print("p=",p," n=",n," |SL_n(p)|=",Size(G),
    " intersection=centralizer order ",Size(C)," PASS\n");
end;
for p in [2,3] do CheckTransvectionIntersection(p); od;
LogTo();
QUIT;
