Read("shadow_residues.g");;
L096Incidence:=function(G,H)
 local n,cos,vertices,i,j,a,b,inc,offsets,idx;
 n:=Length(H);cos:=List(H,P->RightCosets(G,P));vertices:=[];offsets:=[];
 for i in [1..n] do Add(offsets,Length(vertices));for a in [1..Length(cos[i])] do Add(vertices,i);od;od;
 inc:=List(vertices,x->List(vertices,y->false));
 for i in [1..n] do for a in [1..Length(cos[i])] do
  for j in [1..n] do for b in [1..Length(cos[j])] do
   inc[offsets[i]+a][offsets[j]+b]:=not IsEmpty(Intersection(Set(cos[i][a]),Set(cos[j][b])));
  od;od;
 od;od;
 return rec(types:=vertices,incidence:=inc);
end;;
models:=[];;
G:=SymmetricGroup(4);;Add(models,rec(name:="tetrahedron",G:=G,H:=[Group((2,3),(3,4)),Group((1,2),(3,4)),Group((1,2),(2,3))]));;
G:=Group((1,2),(3,4),(5,6));;Add(models,rec(name:="three_digonal_factors",G:=G,H:=[Group((3,4),(5,6)),Group((1,2),(5,6)),Group((1,2),(3,4))]));;
G:=Group((1,2),(3,4));;Add(models,rec(name:="non_flag_transitive_triangle",G:=G,H:=[Group((1,2)),Group((3,4)),Group((1,2)(3,4))]));;
G:=SymmetricGroup(4);;Add(models,rec(name:="cube_bipartite_graph",G:=G,H:=[Stabilizer(G,1),Stabilizer(G,2)]));;
G:=Group((1,2,3,4),(2,4));;Add(models,rec(name:="square",G:=G,H:=[Group((2,4)),Group((1,2)(3,4))]));;
G:=SymmetricGroup(3);;Add(models,rec(name:="triangle_edges",G:=G,H:=[Group((1,2)),Group((2,3))]));;
for model in models do
 r:=L096Local(model.G,model.H,[1..Length(model.H)]);;
 inc:=L096Incidence(model.G,model.H);;
 Print("MODEL|",L096JSON(rec(name:=model.name,local_result:=r,incidence:=inc)),"\n");
od;
Read("data_m11/inputs.g");;
comparison_count:=0;;
for inp in L096Inputs do
 G:=Group(Concatenation(inp.parabolic_generators));;H:=List(inp.parabolic_generators,x->Subgroup(G,x));;n:=Length(H);;
 for J in Combinations([1..n],n-2) do
  K:=Intersection(Concatenation([G],H{J}));;I:=Difference([1..n],J);;P:=[];;for i in I do Add(P,Intersection(K,H[i]));od;
  L096RankTwoShortcut:=true;;r:=L096Local(K,P,I);;
  L096RankTwoShortcut:=false;;s:=L096Local(K,P,I);;
  if r.type_results<>s.type_results then Error("rank-two shortcut disagrees with full witness search");fi;
  comparison_count:=comparison_count+1;
 od;
od;
Print("RANK_TWO_COMPARISONS|",comparison_count,"\n");
Print("PASS_SMALL_MODEL_EXPORT\n");QUIT;
