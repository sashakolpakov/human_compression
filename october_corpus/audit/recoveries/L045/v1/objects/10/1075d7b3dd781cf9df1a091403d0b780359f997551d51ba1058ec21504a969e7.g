SizeScreen([1000000,1000000]);;
Need:=function(b,s) if not b then Error(s);fi;end;;
RunToriControls:=function()
 local q,k,E,F,N,z,basis,mat,v,x,M,r,m,A,B,expected,actual;
for q in [2,3,4,5,7,9] do
 for k in [3,4] do
  E:=GF(q^(2*k));F:=GF(q);N:=q^k+1;
  z:=Z(q^(2*k))^(q^k-1);
  basis:=Basis(AsVectorSpace(F,E));
  mat:=List(BasisVectors(basis),b->Coefficients(basis,b*z));
  Need(Order(z)=N and Order(mat)=N,"actual multiplier order");
  Need(DegreeOfUnivariateLaurentPolynomial(MinimalPolynomial(F,z))=2*k,"full field degree");
  if q mod 2=1 then
   v:=DeterminantMat(IdentityMat(2*k,F)+mat);
   Need(v<>Zero(F) and v^((q-1)/2)=-One(F),"nontrivial determinant spinor class");
   x:=z^2;M:=N/GcdInt(4,N);
   Need(x^M in [One(E),-One(E)],"projective order gives scalar");
   for r in Set(FactorsInt(M)) do
    Need(not x^(M/r) in [One(E),-One(E)],"projective order is minimal");
   od;
  else
   M:=N;
  fi;
  Need(OrderMod(q,M)=2*k,"full projective field degree");
  Print("TORUS|",q,"|",k,"|",N,"|",M,"\n");
 od;
od;
for q in [2,3,4,5,7,9] do
 for m in [4,5,6,7] do
  A:=q^(m-1)+1;B:=q+1;
  if q mod 2=0 then
   expected:=LcmInt(A,B);actual:=expected;
  else
   expected:=A/2;
   if m mod 2=1 then expected:=A*B/GcdInt(4,q^m-1);fi;
   actual:=LcmInt(A,B);
   if (actual/2) mod A=A/2 and (actual/2) mod B=B/2 then actual:=actual/2;fi;
  fi;
  Need(actual=expected,"paired scalar order");
  Print("PAIR|",q,"|",m,"|",actual,"|",A*B,"\n");
 od;
od;
Print("COMPLETE_TORI_CONTROLS\n");
end;;
RunToriControls();;
QUIT;
