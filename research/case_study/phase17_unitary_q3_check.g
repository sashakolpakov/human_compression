# Exact finite generation base, with explicit field coordinates.
SizeScreen([4096,100000]);;
F:=GF(9);;o:=One(F);;z:=Zero(F);;lambda:=Z(9);;ii:=lambda+o;;
Assert(0,lambda^2=lambda+o and Order(lambda)=8 and ii^2=-o);;
Assert(0,List(CoefficientsOfUnivariatePolynomial(MinimalPolynomial(GF(3),lambda)),IntFFE)=[2,2,1]);;
H:=DiagonalMat([o,-o,o,-o]);;
r0:=DiagonalMat([o,o,-o,-o]);;
r1:=[[o,z,z,z],[z,z,z,o],[z,z,o,z],[z,o,z,z]];;
r2:=[[z,ii,z,z],[ii,z,z,z],[z,z,o,lambda],[z,z,lambda-o,-o]];;
r3:=[[z,z,o,z],[z,z,z,o],[o,z,z,z],[z,o,z,z]];;
rr:=[r0,r1,r2,r3];;bar:=m->List(m,row->List(row,t->t^3));;
normalized:=[r0,r1,lambda*r2,r3];;
Assert(0,ForAll(normalized,g->g*H*TransposedMat(bar(g))=H));;
# In U4(3), square determinants are exactly the index-two diagonal preimage.
Assert(0,ForAll(normalized,g->DeterminantMat(g)^2=o));;
Assert(0,DeterminantMat(lambda*r2)=-o);;
M:=Group(rr);;plane:=[[o,o,z,z],[z,z,o,o]];;
orb:=Orbit(M,plane,OnSubspacesByCanonicalBasis);;Assert(0,Length(orb)=112);;
hom:=ActionHomomorphism(M,orb,OnSubspacesByCanonicalBasis);;
pp:=List(rr,r->Image(hom,r));;G:=Group(pp);;
Assert(0,Size(G)=6531840 and 6531840=2*3^6*(3^2-1)*(3^3+1)*(3^4-1)/4);;
Assert(0,ForAll(pp,g->Order(g)=2));;
for j in [1..4] do for l in [1..4] do if AbsInt(j-l)>1 then Assert(0,Comm(pp[j],pp[l])=());fi;od;od;
Assert(0,List([1..3],j->Order(pp[j]*pp[j+1]))=[4,8,6]);;
sets:=Combinations([1..4]);;subs:=List(sets,s->Subgroup(G,pp{s}));;
for j in [1..16] do for l in [1..16] do Assert(0,Intersection(subs[j],subs[l])=subs[Position(sets,Intersection(sets[j],sets[l]))]);od;od;
Print("PASS q3 field_polynomial=[2,2,1] lambda=Z(9) i=lambda+1 k=1 planes=112 order=6531840 type=[4,8,6] closures=16 meets=256\n");
Print("PASS normalized-unitary membership, square determinant containment, and exact projective image order sandwich; no assumed faithfulness or recognition\n");
QUIT;
