SetInfoLevel(InfoWarning,0);;
Control:=function()
 local q,F,E,m,b,bv,gamma,B,h,N,I,j,k,a,c,v,w,D,A,g,rows,tot,inv,uniq,expected,plus,minus,sy,al,G,vs,norm,els,formtests,mu,mat;
 rows:=[];
 for q in [2,4,8]do
  F:=GF(q);I:=IdentityMat(4,F);B:=NullMat(4,4,F);
  for j in [1,2]do B[j][j+2]:=One(F);B[j+2][j]:=One(F);od;
  N:=StructuralCopy(I);N[1][3]:=One(F);N[2][4]:=One(F);
  tot:=0;inv:=0;uniq:=[];
  for a in Elements(F)do
   A:=[[One(F)+a,a],[a,One(F)+a]];
   for c in Tuples(Elements(F),3)do
    D:=[[c[1],c[2]],[c[2],c[3]]];g:=NullMat(4,4,F);mat:=D*A;
    for j in [1,2]do for k in [1,2]do
     g[j][k]:=A[j][k];g[j+2][k+2]:=A[j][k];g[j][k+2]:=mat[j][k];
    od;od;
    if g*B*TransposedMat(g)<>B or g*N<>N*g then Error("symplectic centralizer equations");fi;
    if (g*g=I)<>(D=A*D*TransposedMat(A))then Error("symmetric-module involution fibre");fi;
    tot:=tot+1;Add(uniq,String(g));if g<>I and g*g=I then inv:=inv+1;fi;
   od;
  od;
  if tot<>q^4 or Length(Set(uniq))<>tot or inv<>2*q^3-q^2-1 then Error("degree-four even count");fi;
  Add(rows,["even_Sp4_centralizer",q,tot,inv]);
 od;
 for q in [3,5,7]do
  F:=GF(q);I:=IdentityMat(2,F);G:=Elements(GL(2,q));
  plus:=Number(G,A->A*A=I);minus:=Number(G,A->A*A=-I);
  sy:=Number(G,A->A=TransposedMat(A));al:=Number(G,A->A=-TransposedMat(A));
  expected:=q^2;if q mod 4=1 then expected:=q*(q+1)+1;fi;
  if (plus+minus)/2-1<>expected or sy<>q^2*(q-1)or al<>q-1 then Error("GL2 projective fibres");fi;
  Add(rows,["GL2_normalizer_fibres",q,plus,minus,sy,al]);
  E:=GF(q^2);I:=IdentityMat(2,E);els:=Elements(E);vs:=Filtered(Tuples(els,2),v->Sum(v,a->a*a^q)=One(E));G:=[];
  for v in vs do for w in vs do
   if Sum([1,2],j->v[j]*w[j]^q)=Zero(E)then Add(G,[v,w]);fi;
  od;od;
  if Length(G)<>q*(q-1)*(q+1)^2 then Error("GU2 literal orthonormal bases");fi;
  plus:=Number(G,A->A*A=I);minus:=Number(G,A->A*A=-I);
  sy:=Number(G,A->A=TransposedMat(A));al:=Number(G,A->A=-TransposedMat(A));
  expected:=q^2;if q mod 4=3 then expected:=q*(q-1)+1;fi;
  if (plus+minus)/2-1<>expected or sy<>q^2*(q+1)or al<>q+1 then Error("GU2 projective fibres");fi;
  Add(rows,["GU2_normalizer_fibres",q,plus,minus,sy,al]);
 od;
 formtests:=0;
 for a in [[2,2],[2,3],[2,4],[3,2],[3,3],[4,2]]do
  m:=a[1];q:=a[2];F:=GF(q);E:=GF(q^(2*m));b:=Basis(AsVectorSpace(F,E));bv:=BasisVectors(b);
  gamma:=First(Elements(E),c->c<>Zero(E)and c^(q^m)=-c);
  B:=List(bv,v->List(bv,w->Trace(E,F,gamma*v*w^(q^m))));
  h:=List(bv,v->Coefficients(b,v^(q^m)));I:=IdentityMat(2*m,F);
  if B<>-TransposedMat(B)or IsZero(DeterminantMat(B))or ForAny([1..2*m],j->B[j][j]<>Zero(F))then Error("trace symplectic form");fi;
  if h*B*TransposedMat(h)<>-B or h*h<>I then Error("Frobenius inverter");fi;
  if IsEvenInt(q)then
   if RankMat(h-I)<>m or ForAll([1..2*m],j->(B*TransposedMat(h))[j][j]=Zero(F))then Error("full-rank nonalternating inverter");fi;
  fi;
  formtests:=formtests+1;
 od;
 Print("PASS_SYMPLECTIC_CONTROLS ",rows," TRACE_MODELS ",formtests,"\n");
end;;
Control();
QUIT;
