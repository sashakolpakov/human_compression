SizeScreen([240,60]);;
Require:=function(x,m) if not x then Error(m);fi;end;;
PureRestriction:=function(p,domain,n) local images,x;images:=[1..n];for x in domain do images[x]:=x^p;od;return PermList(images);end;;
inputs:=[
 [9,(2,3)(6,9)(7,8),(1,2)(3,4)(5,6),(4,5)(6,7)(8,9),(1,2),(2,3,4)],
 [10,(1,2)(3,4)(9,10),(2,3)(4,5)(6,7)(8,9),(5,6)(7,8),(2,3),(1,2)],
 [13,(1,2)(3,4)(7,9)(8,10),(2,3)(4,5)(6,7)(10,11)(12,13),(5,6)(7,8)(9,10)(11,12),(2,3),(3,4,5)]
];;
expected:=[[12,288,40320,72,6,6], [12,1440,768,24,4,6], [12,1440,39916800,72,4,6]];;
for j in [1..3] do
 row:=inputs[j];;n:=row[1];;a:=row[2];;q:=row[3];;c:=row[4];;t:=row[5];;v:=row[6];;b:=t*q;;
 Require(Group([a,q,c])=SymmetricGroup(n),"exact old symmetric permutation group");
 Require(Order(a)=2 and Order(q)=2 and Order(c)=2 and a*c=c*a,"old string involutions");
 Require(Size(Intersection(Group([a,q]),Group([q,c])))=2,"rank-three end criterion");
 B:=Group([a,b]);;H:=Group([t,a,b]);;K:=Group([a,b,c]);;I:=Intersection(H,K);;
 Require(v in I and not v in B,"literal failed intersection element");
 Require([Size(B),Size(H),Size(K),Size(I),Order(t*a),Order(a*b)]=expected[j],"full source-example data and actual bonds");
 Require(ForAll(Orbits(B,[1..n]),x->Length(x)<=3),"source middle bound");
 O:=Orbit(H,SmallestMovedPoint(t));;outside:=Difference([1..n],O);;
 ao:=PureRestriction(a,outside,n);;
 bo:=PureRestriction(b,outside,n);;
 Require(H=Group(Concatenation(GeneratorsOfGroup(SymmetricGroup(O)),[ao,bo])),"actual supported direct factor");
 if n=9 then
  Require(Orbits(K,[1..n])=[[1],[2,3,4,5,6,7,8,9]] or Set(List(Orbits(K,[1..n]),Set))=Set([[1],[2..9]]),"actual first K orbits");
  Require(Action(K,[2..9])=SymmetricGroup(8),"first full symmetric image");
 elif n=10 then
  Require(Set(Orbit(K,[3,10],OnSets))=Set([[3,10],[4,9],[5,8],[6,7]]),"exact four blocks");
  Require(List([a,b,c],SignPerm)=[-1,-1,1],"missing parity hypothesis");
 else
  Require(Action(K,[3..13])=SymmetricGroup(11),"third full symmetric image");
  Require(ForAll([a,b,c],x->SignPerm(x)=1),"whole permutation parity");
 fi;
od;
a:=(1,2)(5,6)(7,8)(11,12)(13,14)(17,18);;
b:=(2,3)(4,5)(7,9)(10,11)(14,15)(16,17);;
c:=(3,4)(5,7)(6,8)(9,10)(11,13)(12,14)(15,16);;t:=(1,18);;
B:=Group([a,b]);;H:=Group([t,a,b]);;K:=Group([a,b,c]);;
N:=NormalClosure(H,Group([t]));;
Require(N=Group([(1,18),(2,17),(3,16)]) and Size(N)=8,"actual normal closure matching group");
Require(Size(Intersection(N,B))=1 and H=ClosureGroup(N,B),"matching complementary factor");
Require(Size(Intersection(N,K))=8 and Size(Intersection(H,K))=48,"all seven obstruction tests fail");
Print("PASS_DISTINCT_L020_POSITIVE:source_examples=3;actual_direct_factors=3;literal_defects=3;matching_normal_closure=8;matching_obstructions=7\n");
QUIT_GAP(0);
