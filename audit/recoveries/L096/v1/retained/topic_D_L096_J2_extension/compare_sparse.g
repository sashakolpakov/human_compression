Read("shadow_residues.g");;
OldLocal:=L096Local;;
Read("shadow_residues_sparse.g");;
SparseLocal:=L096Local;;
models:=[];;
G:=SymmetricGroup(4);;Add(models,rec(name:="tetrahedron",G:=G,H:=[Group((2,3),(3,4)),Group((1,2),(3,4)),Group((1,2),(2,3))]));;
G:=Group((1,2),(3,4),(5,6));;Add(models,rec(name:="three_digonal_factors",G:=G,H:=[Group((3,4),(5,6)),Group((1,2),(5,6)),Group((1,2),(3,4))]));;
G:=Group((1,2),(3,4));;Add(models,rec(name:="non_flag_transitive_triangle",G:=G,H:=[Group((1,2)),Group((3,4)),Group((1,2)(3,4))]));;
G:=SymmetricGroup(4);;Add(models,rec(name:="cube_bipartite_graph",G:=G,H:=[Stabilizer(G,1),Stabilizer(G,2)]));;
G:=Group((1,2,3,4),(2,4));;Add(models,rec(name:="square",G:=G,H:=[Group((2,4)),Group((1,2)(3,4))]));;
G:=SymmetricGroup(3);;Add(models,rec(name:="triangle_edges",G:=G,H:=[Group((1,2)),Group((2,3))]));;
for m in models do
 a:=OldLocal(m.G,m.H,[1..Length(m.H)]);b:=SparseLocal(m.G,m.H,[1..Length(m.H)]);
 if a.flag_transitive<>b.flag_transitive then Error("FT discrepancy");fi;
 if a.flag_transitive and a.type_results<>b.type_results then Error("shadow discrepancy");fi;
 Print("SMALL|",m.name,"|",b.flag_transitive,"\n");
od;
G:=Group((1,2));;H:=[TrivialSubgroup(G)];;r:=SparseLocal(G,H,[1]);;
if r.panel_size<>2 or not r.firm or not r.two_transitive then Error("trivial panel");fi;
Print("TRIVIAL_PANEL_PASS\n");
K:=Group(());;P:=[];;cosets:=[];;
Read("prior_inputs.g");;
cases:=0;;shadows:=0;;translations:=0;;emptyuniverses:=0;;
for row in [1..Length(L096Inputs)] do
 inp:=L096Inputs[row];G:=Group(Concatenation(inp.parabolic_generators));H:=List(inp.parabolic_generators,x->Subgroup(G,x));n:=Length(H);
 for J in Combinations([1..n]) do
  if Length(J)=n then continue;fi;
  K:=Intersection(Concatenation([G],H{J}));rest:=Difference([1..n],J);P:=List(rest,i->Intersection(K,H[i]));k:=Length(P);
  if Maximum(List(P,h->Index(K,h)))>2000 then continue;fi;
  sets:=Combinations([1..k]);HG:=List(sets,T->Intersection(Concatenation([K],P{T})));cases:=cases+1;
  for i in [1..k] do
   cosets:=RightCosets(K,P[i]);phi:=ActionHomomorphism(K,cosets,OnRight);pt:=Position(cosets,RightCoset(P[i],One(K)));
   old:=Set(Orbit(Image(phi,K),pt));if Length(old)<>Index(K,P[i]) then Error("empty universe");fi;emptyuniverses:=emptyuniverses+1;
   for T in [1..Length(sets)] do
    if IsEmpty(sets[T]) then continue;fi;
    old:=Set(Orbit(Image(phi,HG[T]),pt));
    new:=Set(List(RightTransversal(HG[T],Intersection(P[i],HG[T])),x->CanonicalRightCosetElement(P[i],x)));
    decoded:=Set(List(old,x->CanonicalRightCosetElement(P[i],Representative(cosets[x]))));
    if new<>decoded then Error("nonempty shadow mismatch");fi;shadows:=shadows+1;
    for g in GeneratorsOfGroup(K) do
     moved:=Set(List(OnSets(old,Image(phi,g)),x->CanonicalRightCosetElement(P[i],Representative(cosets[x]))));
     if L096Shift(P[i],new,g)<>moved then Error("right action mismatch");fi;translations:=translations+1;
    od;
   od;
  od;
 od;
od;
Print("ACTUAL_SHADOW_COMPARISON|",cases,"|",shadows,"|",translations,"|",emptyuniverses,"\n");
Print("PASS_SPARSE_COMPARISON\n");QUIT;
