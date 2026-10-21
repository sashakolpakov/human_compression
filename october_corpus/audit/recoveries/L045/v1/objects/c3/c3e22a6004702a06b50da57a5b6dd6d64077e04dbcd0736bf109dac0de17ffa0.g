SetInfoLevel(InfoWarning,0);;
Control:=function()
 local row,q,n,K,F,b,X,c,B,coeff,forms,fields,A,G,J,v,z,g,bs,els,vs,seen,total,count,expected,I,u,j,k,matrices,square,rank,cases,pgl,wreath,auts;
 fields:=0;forms:=0;
 for row in [[4,2],[4,3],[4,4],[5,2],[5,3],[6,2],[7,2]] do
  n:=row[1];q:=row[2];K:=GF(q);F:=GF(q^n);b:=Basis(AsVectorSpace(K,F));
  c:=Z(q^n)^(q-1);
  X:=List(BasisVectors(b),u->Coefficients(b,u*c));
  if DeterminantMat(X)<>One(K) then Error("norm-one determinant");fi;
  for c in Filtered(Elements(F),z->not IsZero(z))do
   B:=List(BasisVectors(b),u->List(BasisVectors(b),v->Trace(F,K,c*u*v)));
   if IsZero(DeterminantMat(B))or B<>TransposedMat(B)or X*B<>B*TransposedMat(X)then Error("trace form");fi;
   if IsEvenInt(q)and ForAll([1..n],j->IsZero(B[j][j]))then Error("alternating trace form");fi;
   forms:=forms+1;
  od;
  fields:=fields+1;
 od;
 cases:=[];
 for row in [[4,2],[4,4],[6,2]]do
  n:=row[1];q:=row[2];K:=GF(q);G:=Sp(n-2,q);J:=InvariantBilinearForm(G).matrix;
  B:=NullMat(n,n,K);B[1][n]:=One(K);B[n][1]:=One(K);B[n][n]:=One(K);
  for j in [1..n-2]do for k in [1..n-2]do B[j+1][k+1]:=J[j][k];od;od;
  vs:=Tuples(Elements(K),n-2);I:=IdentityMat(n,K);total:=0;count:=0;seen:=NewDictionary(I,true);
  for A in Elements(G)do for v in vs do for c in Elements(K)do
   g:=NullMat(n,n,K);g[1][1]:=One(K);g[n][n]:=One(K);g[n][1]:=c;
   for j in [1..n-2]do
    g[j+1][1]:=A[j]*J*v;g[n][j+1]:=v[j];
    for k in [1..n-2]do g[j+1][k+1]:=A[j][k];od;
   od;
   if g*B*TransposedMat(g)<>B or DeterminantMat(g)<>One(K)then Error("J isometry");fi;
   if LookupDictionary(seen,g)<>fail then Error("duplicate parameters");fi;AddDictionary(seen,g,true);
   square:=g*g=I;
   if square<>(A*A=IdentityMat(n-2,K)and v*A=v)then Error("square condition");fi;
   if square and g<>I then count:=count+1;fi;total:=total+1;
  od;od;od;
  expected:=q^(n-1)-1;
  for A in Elements(G)do
   if Order(A)=2 then expected:=expected+q^(n-2-RankMat(A-IdentityMat(n-2,K))+1);fi;
  od;
  if count<>expected or total<>q^(n-1)*Size(G)then Error("J class count");fi;
  if n=4 and count<>q^4+q^3-q^2-1 then Error("J4 formula");fi;
  Add(cases,[n,q,total,count]);
 od;
 Print("PASS_TRACE_FORMS ",fields," ",forms,"\n");Print("PASS_J_ISOMETRIES ",cases,"\n");
end;;
Control();
QUIT;
