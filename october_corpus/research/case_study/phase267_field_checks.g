# Independent direct Omega checks, including a proper nested pair.
Need267:=function(ok,s) if not ok then Print("PHASE267_REJECT ",s,"\n");QUIT_GAP(2);fi;end;;
Run267:=function()
 local p,e,Q,F,primitive,j1,j2,u,v,o,counts,k,good,zero,n,L,N,poly,x,a,b,c,s,t;
 for t in [[3,3],[3,5],[5,3],[7,3],[11,3]] do
  p:=t[1];e:=t[2];Q:=p^e;F:=GF(Q);primitive:=List(Filtered([1..Q-2],k->Gcd(k,Q-1)=1),k->Z(Q)^k);counts:=[];
  for j1 in primitive do
   u:=(j1+j1^-1)^2;good:=0;zero:=0;
   for j2 in primitive do v:=(j2+j2^-1)^2;o:=u*v-4*(u+v);
    if IsZero(o) then zero:=zero+1;elif o^((Q-1)/2)=One(F) then good:=good+1;fi;
   od;Need267(good>0,"every first primitive element has a nonzero-square partner in small field");Add(counts,[good,zero]);
  od;
  Print("DIRECT_EQUAL_FIELD ",p,"^",e," PRIMITIVES ",Length(primitive)," PAIRS ",Length(primitive)^2," PARTNER_COUNTS ",Collected(counts)," PASS\n");
 od;
 # Direct embeddings include a proper intersection F27 and a degree45 compositum.
 for t in [[3,3,5,7],[3,3,9,1],[5,3,3,1],[3,9,15,1]] do
  p:=t[1];a:=t[2];b:=t[3];L:=GF(p^Lcm(a,b));F:=GF(p^b);
  j1:=Z(p^a);j2:=Z(p^b)^t[4];Need267(Order(j1)=p^a-1 and Order(j2)=p^b-1,"actual primitive markers");
  s:=(j1+j1^-1)^2;o:=s*(j2+j2^-1)^2-4*(s+(j2+j2^-1)^2);
  n:=Lcm(a,b)/b;N:=Norm(L,F,o);
  Need267(o^((Size(L)-1)/2)=N^((Size(F)-1)/2),"norm transports quadratic character");
  x:=Indeterminate(GF(p^a));poly:=One(x);
  for k in [0..n-1] do c:=s^(p^(Gcd(a,b)*k));poly:=poly*((c-4)*(x^2+1)^2-4*c*x^2);od;
  Need267(DegreeOfLaurentPolynomial(poly)=4*n,"full relative norm degree");
  Need267(ForAll(CoefficientsOfUnivariatePolynomial(poly),c->c^(p^Gcd(a,b))=c),"coefficient norm lies in intersection field");
  v:=Value(poly,j2);
  Need267(v=Norm(L,F,((s-4)*(j2^2+1)^2-4*s*j2^2)),"coefficient polynomial equals actual relative norm");
  Need267(v^((Size(F)-1)/2)=o^((Size(L)-1)/2),"quartic and Omega characters equal");
  Print("DIRECT_NORM ",t," RELATIVE_DEGREE ",n," POLYNOMIAL_DEGREE ",DegreeOfLaurentPolynomial(poly)," CHARACTER ",o^((Size(L)-1)/2)," PASS\n");
 od;
 Print("PHASE267_FIELD_PASS\n");
end;;
Run267();QUIT;
