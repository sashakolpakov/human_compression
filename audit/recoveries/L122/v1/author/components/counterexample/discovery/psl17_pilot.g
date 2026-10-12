T:=PSL(2,17);;
aa:=First(Elements(T),x->Order(x)=9);;
bb:=First(Elements(T),x->Order(x)=2 and Size(Group(aa^3,x))=12);;
if bb=fail then Error("no A4 found"); fi;
Print("T ",Size(T)," a ",aa," b ",bb," H ",StructureDescription(Group(aa^3,bb)),"\n");;
G:=DirectProduct(CyclicGroup(IsPermGroup,3),T);;
ec:=Embedding(G,1);; et:=Embedding(G,2);;
c:=Image(ec,GeneratorsOfGroup(Source(ec))[1]);;
a:=Image(et,aa);; b:=Image(et,bb);;
H:=Group(c*a^3,b);; Hs:=[H,H^a,H^(a^2)];;
Print("G ",Size(G)," H ",Size(H)," join ",Size(ClosureGroup(ClosureGroup(Hs[1],Hs[2]),Hs[3]))," pairs ",List([2,3],i->Size(Intersection(H,Hs[i])))," triple ",Size(Intersection(Hs)),"\n");;
elts:=Elements(G);; cs:=List(Hs,h->RightCosets(G,h));; n:=Length(cs[1]);;
positions:=List([1..3],i->List(elts,x->0));;
reps:=[];;
for i in [1..3] do
  for j in [1..n] do
    Add(reps,Representative(cs[i][j]));;
    for x in Elements(cs[i][j]) do positions[i][PositionSorted(elts,x)]:=(i-1)*n+j; od;
  od;
od;
pos:=function(i,x) return positions[i][PositionSorted(elts,x)]; end;;
adj:=List([1..3*n],x->[]);;
for ei in [1..Length(elts)] do
  vv:=List([1..3],i->positions[i][ei]);;
  for i in [1..3] do for j in [1..3] do
    if i<>j then AddSet(adj[vv[i]],vv[j]); fi;
  od; od;
od;
gens:=List(GeneratorsOfGroup(G),g->List([1..3*n],v->pos(QuoInt(v-1,n)+1,reps[v]*g)));;
sp:=List([1..3*n],v->pos((QuoInt(v-1,n)+1) mod 3+1,reps[v]^a));;
PrintTo("/private/tmp/L122_psl17_candidate.json","{\"n\":",n,",\"adj\":",adj,",\"gens\":",gens,",\"sigma\":",sp,",\"Tgens\":",List(GeneratorsOfGroup(T),g->ListPerm(g,18)),",\"a\":",ListPerm(aa,18),",\"b\":",ListPerm(bb,18),"}\n");;
Print("DONE n ",n," degree ",Length(adj[1])," sigmaorder ",Order(PermList(sp)),"\n");;
QUIT;
