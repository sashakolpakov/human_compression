# The literal universal group for {{4,4}_{(4,0)}, {4,6}_3}.
# A finite exact computation; no earlier table enumeration is repeated.
SetAssertionLevel(1);;
SizeScreen([100000,100000]);;
F:=FreeGroup("a","b","c","d");;rr:=GeneratorsOfGroup(F);;
rel:=List(rr,x->x^2);;
for i in [1..4] do
 for j in [i+1..4] do
  if j<=4 then
   if j=i+1 then m:=[4,4,6][i];else m:=2;fi;
   Add(rel,(rr[i]*rr[j])^m);
  fi;
 od;
od;
Add(rel,(rr[1]*rr[2]*rr[3]*rr[2])^4);;
Add(rel,(rr[2]*rr[3]*rr[4])^3);;
U:=F/rel;;Assert(0,Size(U)=768);;
iso:=IsomorphismPermGroup(U);;Assert(0,iso<>fail and IsBijective(iso));;
G:=Image(iso);;gs:=List(GeneratorsOfGroup(U),x->Image(iso,x));;
Assert(0,Size(G)=768 and List(gs,Order)=[2,2,2,2]);;
Print("GENERATORS ",gs,"\n");;
types:=Combinations([1..4]);;
sub:=List(types,T->Subgroup(G,gs{T}));;
for i in [1..Length(types)] do
 for j in [1..Length(types)] do
  Assert(0,Intersection(sub[i],sub[j])=sub[Position(types,Intersection(types[i],types[j]))]);
 od;
od;
Print("ALL_SUBGROUP_ORDERS ",List(sub,Size),"\n");;
P:=Subgroup(G,gs{[1..3]});;V:=Subgroup(G,gs{[2..4]});;
Assert(0,Size(P)=128 and Size(V)=48);;
Fp:=FreeGroup("x","y","z");;x:=Fp.1;;y:=Fp.2;;z:=Fp.3;;
Tp:=Fp/[x^2,y^2,z^2,(x*y)^4,(y*z)^4,(x*z)^2,(x*y*z*y)^4];;
Tv:=Fp/[x^2,y^2,z^2,(x*y)^4,(y*z)^6,(x*z)^2,(x*y*z)^3];;
Assert(0,Size(Tp)=128 and Size(Tv)=48);;
mp:=GroupHomomorphismByImages(Tp,P,GeneratorsOfGroup(Tp),gs{[1..3]});;
mv:=GroupHomomorphismByImages(Tv,V,GeneratorsOfGroup(Tv),gs{[2..4]});;
Assert(0,mp<>fail and mv<>fail and IsBijective(mp) and IsBijective(mv));;
Assert(0,List([gs[1]*gs[2],gs[2]*gs[3],gs[3]*gs[4]],Order)=[4,4,6]);;
Assert(0,Order(gs[1]*gs[2]*gs[3]*gs[2])=4 and Order(gs[2]*gs[3]*gs[4])=3);;
# A bipartite flag graph would give a C2 character taking each generator
# to its nonidentity element; the odd Petrie relation prevents it.
Ctwo:=Group((1,2));;odd:=GroupHomomorphismByImages(V,Ctwo,gs{[2..4]},[(1,2),(1,2),(1,2)]);;
Assert(0,odd=fail);;
vertices:=Index(V,Subgroup(V,gs{[3,4]}));;
edges:=Index(V,Subgroup(V,gs{[2,4]}));;
faces:=Index(V,Subgroup(V,gs{[2,3]}));;
Assert(0,[vertices,edges,faces]=[4,12,6] and vertices-edges+faces=-2);;
Print("UNIVERSAL_ORDER 768\nFACET_ORDER 128\nVERTEX_FIGURE_ORDER 48\nVERTEX_FIGURE_COUNTS ",[vertices,edges,faces],"\n");;
Print("PAIRWISE_INTERSECTIONS 256\nNONORIENTABLE true\nGENUS 4\nPASS_768_AND_GENUS4\n");;
QUIT;
