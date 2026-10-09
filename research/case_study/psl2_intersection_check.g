# Exact matrix check of Conjecture 6.2 at its first residual case q=3^15.
# Enumerates the SMALL containing SL(2,27), not PSL(2,3^15).
LogTo("research/leemans/psl2_intersection_check.log");
p:=3;; e1:=3;; e2:=5;; q:=p^(e1*e2);;
L:=GF(q);; one:=One(L);;
j1:=Z(p^e1)*one;; j2base:=Z(p^e2)*one;;
u:=j1+j1^-1;;
for k in [1..p^e2-2] do
  if Gcd(k,p^e2-1)<>1 then continue; fi;
  j2:=j2base^k;; v:=j2+j2^-1;;
  omega:=u^2*v^2-4*(u^2+v^2);;
  if omega<>Zero(L) and omega^((q-1)/2)=one then break; fi;
od;
delta:=omega^((q+1)/4);;
if delta^2<>omega then Error("No square root found"); fi;
alpha:=[[u,u+2],[u-2,u]]/2;;
beta:=[[2+u,u],[-u,2-u]]/2;;
gamma:=[[v*(u-2),delta],[delta,v*(u+2)]]/(2*u);;
T:=[[one,2/u],[-one,Zero(L)]];;
Unip:=t->[[one,t],[Zero(L),one]];;
Amat:=w->[[one,(2-w)/w],[-w,w-one]];;
t:=delta/(2*u*v)+1/v-1/2*one-1/u;;
if beta^T<>Unip(one) or alpha^T<>Amat(u) or (gamma^T)^Unip(t)<>Amat(v) then
  Error("Normalization identity fails");
fi;
small:=SL(2,p^e1);;
intersection:=[];;
for M in Elements(small) do
  Mlarge:=List(M,row->List(row,x->x*one));;
  N:=Mlarge^Unip(t);;
  if ForAll(Flat(N),x->x^(p^e2)=x) then Add(intersection,Mlarge); fi;
od;
if Length(intersection)<>2*p then Error("Unexpected containing intersection"); fi;
if not ForAll(intersection,M->M[2][1]=Zero(L) and M[1][1]=M[2][2] and
    M[1][1]^2=one and M[1][2]^p=M[1][2]) then Error("Intersection shape fails"); fi;
Print("GAP ",GAPInfo.Version," p=",p," e1=",e1," e2=",e2," q=",q,"\n");
Print("primitive exponents 1,",k,"; normalization identities verified\n");
Print("SL(2,27) enumerated=",Size(small)," intersection size=",Length(intersection),
      " projective intersection size=",Length(intersection)/2,"\n");
Print("PASS: containing intersection is projective U(F_3)=<beta>\n");
LogTo();
QUIT;
