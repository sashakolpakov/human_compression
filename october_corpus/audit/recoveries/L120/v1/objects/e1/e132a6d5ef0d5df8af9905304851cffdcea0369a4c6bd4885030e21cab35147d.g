SizeScreen([1000000,1000000]);;
Read(inputFile);;
Need:=function(b,s)if not b then Error(s);fi;end;;
G:=SymmetricGroup(6);;A:=AutomorphismGroup(G);;
Need(Size(A)=1440,"full automorphism order");;
phi:=First(GeneratorsOfGroup(A),f->NrMovedPoints(Image(f,(1,2)))=6);;
Need(phi<>fail and IsBijective(phi),"genuine outer automorphism");;
inn:=InnerAutomorphismsAutomorphismGroup(A);;
Need(Size(inn)=720 and Size(Group(Concatenation(GeneratorsOfGroup(inn),[phi])))=1440,"full automorphism generation");;
subsetPairs:=0;;
Need(ivs=Set(Concatenation(List(Filtered(ConjugacyClasses(G),c->Order(Representative(c))=2),AsList))),"exact sorted involution input");;
tuples:=[];;Locate:=fail;;
for k in [3,4,5] do
 tuples:=List(Filtered(ids,x->Length(x)=k),x->List(x,i->ivs[i]));;
 Locate:=function(t)
  local js;
  js:=Filtered([1..Length(tuples)],j->RepresentativeAction(G,t,tuples[j],OnTuples)<>fail);
  Need(Length(js)=1,"unique point-conjugacy representative");return js[1];
 end;;
 for t in tuples do
  Need(Size(Group(t))=720 and ForAll(t,x->Order(x)=2),"target involutions and generation");
  for u in [1..k] do for v in [u+2..k] do Need(Comm(t[u],t[v])=(),"string relation");od;od;
  subsets:=Combinations([1..k]);; groups:=List(subsets,z->Subgroup(G,t{z}));;
  for u in [1..Length(subsets)] do for v in [1..Length(subsets)] do
   Need(Intersection(groups[u],groups[v])=Subgroup(G,t{Intersection(subsets[u],subsets[v])}),"every actual subset intersection");
   subsetPairs:=subsetPairs+1;
  od;od;
 od;
 outer:=List(tuples,t->Locate(List(t,x->Image(phi,x))));;
 reversal:=List(tuples,t->Locate(Reversed(t)));;
 Need(Set(outer)=[1..Length(tuples)] and Set(reversal)=[1..Length(tuples)],"actual fusion permutations");;
 autClasses:=Orbits(Group(PermList(outer)),[1..Length(tuples)]);;
 dualClasses:=Orbits(Group(PermList(outer),PermList(reversal)),[1..Length(tuples)]);;
 Print("RANK ",k," POINT_CLASSES ",Length(tuples)," OUTER ",outer," REVERSE ",reversal," FULL_AUT ",Length(autClasses)," WITH_DUAL ",Length(dualClasses),"\n");
od;
Need(subsetPairs=6016,"complete subset-pair coverage");;
Print("SUBSET_PAIRS ",subsetPairs,"\n");
Print("TERMINAL_S6_FUSION\n");
QUIT;
