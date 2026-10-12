# Exact projective isotropic-point action of the named standard SU constructor.
MakeUnitary:=function(n,q)
 local f,m,mat,points,tuples,v,i,w,z,hom,g,expected,a,point,actual;
 f:=GF(q^2);m:=SU(n,q);mat:=InvariantSesquilinearForm(m).matrix;
 Need(mat=TransposedMat(List(mat,r->List(r,x->x^q))) and RankMat(mat)=n,"nonsingular Hermitian form");
 for a in GeneratorsOfGroup(m) do
  Need(DeterminantMat(a)=One(f),"special-unitary determinant");
  Need(a*mat*TransposedMat(List(a,r->List(r,x->x^q)))=mat,"unitary isometry");
 od;
 points:=[];
 for v in Tuples(Elements(f),n) do
  i:=PositionProperty(v,x->not IsZero(x));
  if i=fail or v[i]<>One(f) then continue;fi;
  if IsZero(v*mat*List(v,x->x^q)) then Add(points,v);fi;
 od;
 Sort(points);
 hom:=ActionHomomorphism(m,points,OnLines);g:=Image(hom);
 expected:=q^(n*(n-1)/2)*Product([2..n],i->q^i-(-1)^i)/Gcd(n,q+1);
 actual:=FreshPermutationOrder(g,Concatenation("unitary_model_",String(n),"_",String(q)));
 Need(actual=expected,"fresh projective permutation order");
 Need(Size(g)=expected,"projective unitary order");
 Need(Size(Kernel(hom))=Gcd(n,q+1),"projective scalar kernel");
 Need(IsSimpleGroup(g),"unitary simplicity");
 Print("unitary ",n," ",q," degree ",Length(points)," order ",Size(g),"\n");
 return rec(group:=g,points:=points,matrix_group_generators:=GeneratorsOfGroup(m),hermitian_form:=mat);
end;;
