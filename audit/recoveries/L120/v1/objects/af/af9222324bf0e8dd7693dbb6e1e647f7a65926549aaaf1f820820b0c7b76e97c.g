SizeScreen([1000000,1000000]);;
Read(inputFile);;
Need:=function(b,s)if not b then Error(s);fi;end;;
G:=SymmetricGroup(11);;pairs:=0;;t:=[];;
Need(Size(AutomorphismGroup(G))=39916800,"full automorphisms are inner");;
for indices in ids do
 t:=List(indices,i->ivs[i]);;r:=Length(t);;
 Need(Size(Group(t))=39916800 and ForAll(t,x->Order(x)=2),"actual target and involutions");;
 for u in [1..r] do for v in [u+2..r] do Need(Comm(t[u],t[v])=(),"string");od;od;
 sets:=Combinations([1..r]);;groups:=List(sets,z->Subgroup(G,t{z}));;
 for u in [1..Length(sets)] do for v in [1..Length(sets)] do
  Need(Intersection(groups[u],groups[v])=Subgroup(G,t{Intersection(sets[u],sets[v])}),"every subset intersection");
  pairs:=pairs+1;
 od;od;
 Print("SOLUTION|",List(t,g->List([1..11],x->x^g)),"\n");
od;
Print("SUBSET_PAIRS|",pairs,"\nCOMPLETE_S11_VALIDATION\n");
QUIT;
