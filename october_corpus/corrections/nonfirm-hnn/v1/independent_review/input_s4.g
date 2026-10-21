# Distinct reconstruction: no author script, output, or helper is read.
A := SymmetricGroup(4);;
a := (3,4);; b := (1,2);; r := (1,3)(2,4);; s := (1,4)(2,3);;
P := [Group(a), Group(b), Group((1,3),(2,4)),
      Group((1,4),(2,3)), Group(a,b,r), Group(r)];;
Need := function(ok,msg) if not ok then Error(msg); fi; end;;
Par := [];;
for I in Combinations([1..6]) do
  Q := A;
  for i in I do Q := Intersection(Q,P[i]); od;
  AddSet(Par,Q);
od;
Need(Length(Par)=9,"nine actual parabolics");;
Need(Set(List(Par,Q->Q^b))=Set(Par),"admissible unlabelled lattice map");;
Prod := function(X,Y) return Set(Concatenation(List(X,x->List(Y,y->x*y)))); end;;
Sets := List(Par,Elements);; checks:=0;;
for sx in Sets do
  for sy in Sets do
    for sz in Sets do
      Need(Intersection(Prod(sx,sy),Prod(sx,sz))=Prod(sx,Intersection(sy,sz)),
           "full parabolic coset Helly criterion");
      checks:=checks+1;
    od;
  od;
od;
Need(checks=729,"all nine-cubed product identities");;
K := Group(r,s);;
Need(Size(K)=4 and r^b=s and s^b=r and a*b in K,"orbit closure");;
F := [Elements(P[1]),Elements(P[2]),Set(List(Elements(K),k->a*k))];;
Need(List(Combinations([1..3],2),I->Length(Intersection(F{I})))=[1,1,1],
     "three pairwise intersections");;
Need(Intersection(F)=[],"empty triple intersection");;
Need(Intersection(P[1],P[2])=TrivialSubgroup(A),"output intersection is stable cyclic factor");;
Need(not a in K and ForAll(Elements(K),k->SignPerm(k)=1),"odd coset avoids identity");;
Print("PASS_N005_S4_DISTINCT: order=24; parabolics=9; product-identities=",checks,
      "; pair-intersections=[1,1,1]; triple=0\n");
QUIT;
