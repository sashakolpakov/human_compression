# Exact counterexamples to literal N006 v2 hypotheses, not open conjectures.
Check:=function(b,s) if not b then Error(s);fi;end;;
# Thin rank-one factors with nontrivial Borel acting on the coordinate set.
e:=[(1,2),(3,4),(5,6)];;
c:=(1,3,5)(2,4,6);;d:=(1,3)(2,4);;
A:=Group(e);;B:=Group(c,d);;BI:=Group(c);;G:=Group(Concatenation(e,[c,d]));;
P:=Group(Concatenation(e,[c]));;Q:=B;;
Check(Size(A)=8 and Size(B)=6 and Size(BI)=3 and Size(G)=48,"named groups");;
Check(Index(B,BI)=2,"beta thin");;
O:=[[1,3,5],[1,3,5]];;
Check(ForAll([1..2],i->ForAll([1..2],j->Intersection(O[i],O[j])=O[Maximum(i,j)])),"all orbit intersection conditions");;
K:=Intersection(P,Q);;
Check(Size(K)=3 and Size(P)=24 and Size(Q)=6,"actual twisting parabolics");;
x:=RightCosets(G,P);;y:=RightCosets(G,Q);;
Check(Length(x)=2 and Length(y)=8 and ForAll(x,u->ForAll(y,v->Intersection(u,v)<>[])),"complete K2,8 geometry");;
Check(Index(P,K)=8 and Index(Q,K)=2,"one panel not thin");;
Print("N006_LITERAL_WREATH_THINNESS_COUNTEREXAMPLE order48 cosets2and8 panels8and2 PASS\n");
# Boolean rank-three self-dual polytope: A=C2^3, outer reversal tau.
A:=Group((1,2),(3,4),(5,6));;tau:=(1,5)(2,6);;H:=Group((1,2),(3,4),(5,6),tau);;
Check(Size(A)=8 and IsElementaryAbelian(A) and Size(H)=16,"rank3 reversal extension");;
Check(Size(AutomorphismGroup(A))=168 and 168 mod Size(H)<>0,"no embedding by Lagrange");;
Check(GeneratorsOfGroup(A)[1]^tau<>GeneratorsOfGroup(A)[1],"duality nontrivial hence outer on abelian group");;
Print("N006_LITERAL_DUALITY_EMBEDDING_COUNTEREXAMPLE order16 AutA168 PASS\n");
# Rank-four Boolean polytope and reversal extension of exponent four.
e:=[(1,2),(3,4),(5,6),(7,8)];;tau:=(1,7)(2,8)(3,5)(4,6);;
H:=Group(Concatenation(e,[tau]));;
Check(Size(H)=32 and Exponent(H)=4,"rank4 Boolean extension");;
# Written complete-diagram lower bound is64; this check is algebraic input only.
Print("N006_BOOLEAN_RANK4_ALGEBRA order32 exponent4 PASS\n");
QUIT;
