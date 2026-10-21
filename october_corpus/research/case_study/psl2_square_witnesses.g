# Exact primitive-element witnesses for the six small cases left by the
# proposed character-sum bound. No construction of the large compositum.
LogTo("research/leemans/psl2_square_witnesses.log");

SquareWitness := function(p,a,b)
  local A,B,j1,j2base,u,x,P,i,ui,coeff,Q,n,k,j2,val,root,
        primitiveCount,squareCount,firstK,firstVal,firstJ2,c,normpoly,
        candidateValues;
  A:=GF(p^a); B:=GF(p^b);
  j1:=Z(p^a); j2base:=Z(p^b);
  u:=j1+j1^-1;
  x:=Indeterminate(A);
  P:=One(A)+0*x;
  for i in [0..a-1] do
    ui:=u^(p^i);
    P:=P*((ui^2-4)*(x^2+1)^2-4*ui^2*x^2);
  od;
  coeff:=CoefficientsOfUnivariatePolynomial(P);
  if not ForAll(coeff,c->c^p=c) then Error("Norm coefficients not in prime field"); fi;
  coeff:=List(coeff,IntFFE);
  Q:=p^b; n:=Q-1;
  primitiveCount:=0; squareCount:=0; firstK:=fail;
  for k in [1..n-1] do
    if Gcd(k,n)<>1 then continue; fi;
    primitiveCount:=primitiveCount+1;
    j2:=j2base^k;
    val:=Zero(B);
    for c in Reversed(coeff) do val:=val*j2+c*One(B); od;
    if val<>Zero(B) and val^(n/2)=One(B) then
      squareCount:=squareCount+1;
      if firstK=fail then firstK:=k; firstVal:=val; firstJ2:=j2; fi;
    fi;
  od;
  if firstK=fail then Error("No witness"); fi;
  if Order(j1)<>p^a-1 or Order(firstJ2)<>p^b-1 then Error("Not primitive"); fi;
  Print("CASE p=",p," a=",a," b=",b,"\n");
  Print("j1=Z(",p,"^",a,"), j2=Z(",p,"^",b,")^",firstK,"\n");
  Print("minimal polynomial j1 coefficients(low-to-high)=",
    List(CoefficientsOfUnivariatePolynomial(MinimalPolynomial(GF(p),j1)),IntFFE),"\n");
  Print("minimal polynomial j2 coefficients(low-to-high)=",
    List(CoefficientsOfUnivariatePolynomial(MinimalPolynomial(GF(p),firstJ2)),IntFFE),"\n");
  Print("norm polynomial coefficients(low-to-high)=",coeff,"\n");
  Print("P(j2)=Z(",p,"^",b,")^",LogFFE(firstVal,j2base),
        "; quadratic character=",firstVal^(n/2),"\n");
  Print("fixed-j1 primitive j2 count=",primitiveCount,
        "; successful count=",squareCount,
        "; inverse-pair trace counts=",primitiveCount/2,",",squareCount/2,"\n");
  Print("PASS\n");
end;

Print("GAP ",GAPInfo.Version,"\n");
for triple in [[3,3,5],[5,3,5],[3,3,7],[3,5,7],[3,5,9],[3,7,9]] do
  CallFuncList(SquareWitness,triple);
od;
LogTo();
QUIT;
