# Standalone natural-matrix certificate. GAP standard finite-field and
# permutation algorithms; no AtlasRep input or simple-group recognition.
Read("phase10_unitary_matrix_witness.g");;
q:=5;; f:=GF(q^2);; z:=Zero(f);; e:=One(f);;
h:=[[z,z,z,e],[z,z,e,z],[z,e,z,z],[e,z,z,z]];;
Assert(0,DeterminantMat(h)<>z);
Assert(0,ForAll(matrixWitness,m->DeterminantMat(m)=e));
bar:=m->List(m,row->List(row,x->x^q));;
Assert(0,ForAll(matrixWitness,m->m*h*TransposedMat(bar(m))=h));
Print("FIELD ",MinimalPolynomial(GF(q),Z(q^2)),"; Int(Z5)=",Int(Z(5)),"\n");
Print("DETERMINANTS all1; HERMITIAN exact antidiagonal preserved\n");
Assert(0,List(matrixWitness,m->m*m)=[IdentityMat(4,f),IdentityMat(4,f),-IdentityMat(4,f),-IdentityMat(4,f)]);
mg:=Group(matrixWitness);;
plane:=[[e,z,z,z],[z,e,z,z]];;
Assert(0,plane*h*TransposedMat(bar(plane))=NullMat(2,2,f));
orbit:=Orbit(mg,plane,OnSubspacesByCanonicalBasis);;
Assert(0,Length(orbit)=756);
hom:=ActionHomomorphism(mg,orbit,OnSubspacesByCanonicalBasis);;
projective:=List(matrixWitness,m->Image(hom,m));;
pg:=Group(projective);;
expected:=q^6*(q^2-1)*(q^3+1)*(q^4-1)/Gcd(4,q+1);;
Assert(0,Size(pg)=expected);
Print("PROJECTIVE_ORDER ",Size(pg)," equals |PSU4(5)|\n");
Assert(0,ForAll(projective,x->Order(x)=2));
Assert(0,List([1..3],i->Order(projective[i]*projective[i+1]))=[4,26,10]);
for i in [1..4] do
 for j in [1..4] do
  if AbsInt(i-j)>1 then Assert(0,Comm(projective[i],projective[j])=()); fi;
 od;
od;
subsets:=Combinations([1..4]);;
groups:=List(subsets,s->Subgroup(pg,projective{s}));;
for i in [1..16] do
 for j in [1..16] do
  k:=Position(subsets,Intersection(subsets[i],subsets[j]));;
  Assert(0,Intersection(groups[i],groups[j])=groups[k]);
 od;
od;
Print("PASS natural matrices, type{4,26,10},16subgroups,256meets; no simple-group recognition\n");
QUIT;
