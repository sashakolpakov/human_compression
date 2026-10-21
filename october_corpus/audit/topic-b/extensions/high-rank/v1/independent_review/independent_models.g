# Independent finite diagnostics for the written L040 arguments.
# These do not establish the all-parameter classification.
Need:=function(b,s) if not b then Error(s); fi; end;;
TreeGroup:=function(edges)
 local F,x,rel,i,j,k,p,G;
 F:=FreeGroup(Length(edges));x:=GeneratorsOfGroup(F);rel:=List(x,g->g^2);
 for i in [1..Length(edges)] do
  for j in [i+1..Length(edges)] do
   if j<=Length(edges) then
    if Intersection(edges[i],edges[j])=[] then p:=2;else p:=3;fi;
    Add(rel,(x[i]*x[j])^p);
   fi;
  od;
 od;
 for i in [1..Length(edges)] do
  for j in [i+1..Length(edges)] do
   for k in [j+1..Length(edges)] do
    if j<=Length(edges) and k<=Length(edges) and
     Intersection(Intersection(edges[i],edges[j]),edges[k])<>[] then
      Add(rel,(x[i]*x[j]*x[k]*x[j])^2);
    fi;
   od;
  od;
 od;
 G:=F/rel;return Size(G);
end;;
for edges in [
 [[1,2],[2,3],[3,4],[4,5],[5,6]],
 [[1,2],[1,3],[1,4],[1,5],[1,6]],
 [[1,2],[2,3],[2,4],[4,5],[4,6]]
] do
 Need(TreeGroup(edges)=720,"Literal tree presentation order");
od;
Print("TREE_PRESENTATIONS path/star/two-branch each S6 PASS\n");

# The leaf requirement in the attachment theorem is substantive.
H:=Group((1,2)(3,4),(1,3)(2,4));;
A:=Group(Concatenation(GeneratorsOfGroup(H),[(4,5)]));;
B:=Group(Concatenation(GeneratorsOfGroup(H),[(4,6)]));;
Need(Size(H)=4 and Size(A)=120 and Size(B)=120,"Attachment model sizes");
Need(Size(Intersection(A,B))=24,"Without root leaf intersection grows");
Print("CONTROL remove-root-leaf: intersection S4 order24 > coreV4 order4 PASS\n");

# A finite affine quotient of the triangle Coxeter presentation violates
# the additional triangle relation: thus those relations cannot be omitted.
pts:=List(Cartesian([0..4],[0..4]),p->[p[1],p[2],(-p[1]-p[2]) mod 5]);;
maps:=[p->[p[2],p[1],p[3]],p->[p[1],p[3],p[2]],
 p->[(p[3]+1) mod 5,p[2],(p[1]-1) mod 5]];;
rr:=List(maps,f->PermList(List(pts,p->Position(pts,f(p)))));;
Need(ForAll(rr,g->Order(g)=2),"Affine involutions");
Need(ForAll(Combinations([1..3],2),ij->Order(rr[ij[1]]*rr[ij[2]])=3),"Affine pair labels");
Need(Order(rr[1]*rr[2]*rr[3]*rr[2])=5,"Missing triangle relation countermodel");
Print("CONTROL omit-triangle: involutions/pair3 but triangleword order5 PASS\n");

# Literal branching counterexample, independently specified.
r:=[(2,3),(1,2)(3,4),(4,5),(5,6),(5,7),(6,8),(7,9)];;
Need(Size(Group(r))=Factorial(9),"Branching group S9");
Need(Order(r[3]*r[4])=3 and Order(r[3]*r[5])=3,"Two neighbours of bridge");
six:=Filtered(Combinations([1..7],2),ij->Order(r[ij[1]]*r[ij[2]])=6);;
Need(six=[[2,3]],"Unique six-labelled pair identifies bridge");
Print("SOURCE_CORRECTION branching S9 has two noncommuting tail neighbours PASS\n");
Print("PASS independent written-interface models\n");
QUIT;
