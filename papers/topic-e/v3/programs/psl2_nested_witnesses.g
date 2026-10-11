# Exact same-field witnesses for the small nested-degree cases of Conj. 6.1.
LogTo("research/leemans/psl2_nested_witnesses.log");
NestedWitness:=function(p,e)
  local K,j1,j2,u,v,s,q,k,value,omega,firstK,firstValue,firstJ2,
        primitiveCount,squareCount,zeroCount;
  K:=GF(p^e); q:=p^e;
  j1:=Z(q); u:=j1+j1^-1; s:=u^2;
  firstK:=fail; primitiveCount:=0; squareCount:=0; zeroCount:=0;
  for k in [1..q-2] do
    if Gcd(k,q-1)<>1 then continue; fi;
    primitiveCount:=primitiveCount+1;
    j2:=Z(q)^k; v:=j2+j2^-1;
    value:=(s-4)*(j2^2+1)^2-4*s*j2^2;
    omega:=s*v^2-4*(s+v^2);
    if value<>j2^2*omega then Error("Quartic normalization fails"); fi;
    if value=Zero(K) then
      zeroCount:=zeroCount+1;
    elif value^((q-1)/2)=One(K) then
      squareCount:=squareCount+1;
      if firstK=fail then firstK:=k; firstValue:=value; firstJ2:=j2; fi;
    fi;
  od;
  if firstK=fail then Error("No nonzero square witness"); fi;
  if Order(j1)<>q-1 or Order(firstJ2)<>q-1 then Error("Not primitive"); fi;
  Print("CASE p=",p," e1=e2=",e,"\n");
  Print("j1=Z(",p,"^",e,"), j2=Z(",p,"^",e,")^",firstK,"\n");
  Print("minimal polynomial j1 coefficients(low-to-high)=",
    List(CoefficientsOfUnivariatePolynomial(MinimalPolynomial(GF(p),j1)),IntFFE),"\n");
  Print("minimal polynomial j2 coefficients(low-to-high)=",
    List(CoefficientsOfUnivariatePolynomial(MinimalPolynomial(GF(p),firstJ2)),IntFFE),"\n");
  Print("quartic(j2)=Z(",p,"^",e,")^",LogFFE(firstValue,Z(q)),
    "; quadratic character=",firstValue^((q-1)/2),"\n");
  Print("fixed-j1 primitive j2 count=",primitiveCount,
    "; nonzero-square count=",squareCount,"; zero count=",zeroCount,
    "; inverse-pair trace counts=",primitiveCount/2,",",squareCount/2,"\n");
  Print("PASS\n");
end;
Print("GAP ",GAPInfo.Version,"\n");
for pair in [[3,3],[3,5],[5,3],[7,3],[11,3]] do CallFuncList(NestedWitness,pair); od;
LogTo();
QUIT;
