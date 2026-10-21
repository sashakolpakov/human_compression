# Exact q=8 matrix/group diagnostics; no source-paper counts are inputs.
# Run with gap -q -T phase10_suzuki_marked_groups_check.g.
F:=GF(8);; z0:=Zero(F);; e:=One(F);;
Zroot:=function(b)
  return [[e,z0,z0,z0],[z0,e,z0,z0],[b,z0,e,z0],[b^4,b,z0,e]];
end;;
w:=[[z0,z0,z0,e],[z0,z0,e,z0],[z0,e,z0,z0],[e,z0,z0,z0]];;
G:=SuzukiGroup(IsMatrixGroup,8);;
Assert(0,Size(G)=29120);
Assert(0,w in G and ForAll(Elements(F),b->Zroot(b) in G));
iso:=IsomorphismPermGroup(G);;
P:=Image(iso);;
indices:=Combinations([1..3]);;
tripleCount:=0;; intersectionCount:=0;; dualMatrixCount:=0;;
types:=[];;
rho:=[];; h:=IdentityMat(4,F);;
for b in Difference(Elements(F),[z0,e]) do
  for c in Difference(Elements(F),[z0]) do
    triple:=[Zroot(e),w*Zroot(c)*w,Zroot(b)];;
    rho:=List(triple,m->Image(iso,m));;
    Assert(0,ForAll(rho,r->Order(r)=2));
    Assert(0,rho[1]*rho[3]=rho[3]*rho[1]);
    Assert(0,Group(rho)=P);
    subgroupList:=List(indices,I->Subgroup(P,rho{I}));;
    for I in [1..8] do
      for J in [1..8] do
        K:=Position(indices,Intersection(indices[I],indices[J]));;
        Assert(0,Intersection(subgroupList[I],subgroupList[J])=subgroupList[K]);
        intersectionCount:=intersectionCount+1;
      od;
    od;
    # h^-1 z(x) h = z(lambda^6*x); theta=4 for GF(8).
    lambda:=First(Difference(Elements(F),[z0]),a->a^6=b^-1);;
    h:=DiagonalMat([lambda^5,lambda,lambda^-1,lambda^-5]);;
    Assert(0,h in G);
    reversed:=Reversed(triple);;
    dual:=[Zroot(e),w*Zroot(b*c)*w,Zroot(b^-1)];;
    Assert(0,List(reversed,m->m^h)=dual);
    dualMatrixCount:=dualMatrixCount+1;
    Add(types,[Order(rho[1]*rho[2]),Order(rho[2]*rho[3])]);
    tripleCount:=tripleCount+1;
  od;
od;
Print("{\"status\":\"PASS\",\"q\":8,\"group_order\":",Size(P),
  ",\"normalized_triples\":",tripleCount,
  ",\"subgroup_intersections\":",intersectionCount,
  ",\"duality_matrix_checks\":",dualMatrixCount,
  ",\"adjacent_order_pairs\":",Set(types),"}\n");
QUIT;
