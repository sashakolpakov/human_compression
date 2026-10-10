# Six composite fields left by the exact arithmetic sieve; tower F_q[i], i^2=-1.
SizeScreen([4096,100000]);;
PairMul15:=function(a,b)return [a[1]*b[1]-a[2]*b[2],a[1]*b[2]+a[2]*b[1]];end;;
PairPow15:=function(a,n)local r;r:=[One(a[1]),Zero(a[1])];while n>0 do if IsOddInt(n) then r:=PairMul15(r,a);fi;a:=PairMul15(a,a);n:=QuoInt(n,2);od;return r;end;;
Run15:=function(q)
 local p,e,F,g,o,z,basis,co,poly,ps,k,s,aa,bb,A,B,lam,N,found,t,u,j,start;
 start:=Runtime();p:=Set(FactorsInt(q))[1];e:=Length(FactorsInt(q));F:=GF(q);g:=Z(q);o:=One(F);z:=Zero(F);N:=q*q-1;
 basis:=Basis(F,List([0..e-1],j->g^j));co:=v->List(Coefficients(basis,v),IntFFE);
 poly:=List(CoefficientsOfUnivariatePolynomial(MinimalPolynomial(GF(p),g)),IntFFE);
 ps:=Set(FactorsInt(N));found:=false;
 for k in [1..q-1] do
  if Gcd(k,q-1)<>1 then continue;fi;s:=g^k;
  aa:=(s*s+4*s+o)/4;bb:=-(s*s+o)/4;
  A:=aa^((q+1)/4);B:=bb^((q+1)/4);
  if A*A<>aa or B*B<>bb then continue;fi;lam:=[A,B];
  if ForAny(ps,r->PairPow15(lam,N/r)=[o,z]) then continue;fi;
  Assert(0,PairPow15(lam,N)=[o,z]);u:=[A*(o-s^-1),B*(o+s^-1)];
  Assert(0,u[1]^2+u[2]^2=-2*o);t:=-2*u[2];Assert(0,t<>z and t*t<>o and t*t<>-8*o);
  found:=true;break;
 od;
 Assert(0,found);
 Print("WITNESS ",[q,p,e,poly,co(A),co(B),co(s),co(t),ps],"\n");
 Print("PASS q=",q," runtime_ms=",Runtime()-start,"\n");
end;;
for q in [27,343,1331,6859,12167,29791] do Run15(q);od;
Print("ALL PASS: six composite norm-curve witnesses.\n");
QUIT;
