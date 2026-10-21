# Exact witness checks for the seven shared source rows. Models supplied by driver.
SetAssertionLevel(1);;
SizeScreen([100000,100000]);;
Need:=function(b,m) if not b then Error(m);fi;end;;
SameNamed:=function(H,K,label)
 local f;
 f:=IsomorphismGroups(H,K);Need(f<>fail and IsGroupHomomorphism(f) and IsBijective(f),Concatenation("named map ",label));
 Print("NAMED ",label," ORDER ",Size(H)," SOURCE ",GeneratorsOfGroup(H)," IMAGES ",List(GeneratorsOfGroup(H),h->Image(f,h))," TARGET ",GeneratorsOfGroup(K),"\n");return f;
end;;
Split:=function(G,N,C,label)
 local f,q,ci;
 Need(IsSubgroup(G,N) and IsNormal(G,N),Concatenation("normal ",label));
 Need(IsSubgroup(G,C) and Size(Intersection(N,C))=1,Concatenation("complement intersection ",label));
 Need(Size(N)*Size(C)=Size(G) and ClosureGroup(N,C)=G,Concatenation("complement generation ",label));
 f:=NaturalHomomorphismByNormalSubgroup(G,N);q:=Image(f);ci:=GroupHomomorphismByImages(C,q,GeneratorsOfGroup(C),List(GeneratorsOfGroup(C),g->Image(f,g)));Need(ci<>fail and IsBijective(ci),Concatenation("quotient map ",label));
 Print("QUOTIENT ",label," AMBIENT_IMAGES ",List(GeneratorsOfGroup(G),g->Image(f,g))," COMPLEMENT_IMAGES ",List(GeneratorsOfGroup(C),g->Image(f,g)),"\n");
 Print("SPLIT ",label," ",Size(G)," ",Size(N)," ",Size(C)," N ",GeneratorsOfGroup(N)," C ",GeneratorsOfGroup(C),"\n");
end;;
Direct:=function(G,A,B,label)
 Need(IsSubgroup(G,A) and IsSubgroup(G,B) and Size(Intersection(A,B))=1 and ClosureGroup(A,B)=G,Concatenation("direct factors ",label));
 Need(ForAll(GeneratorsOfGroup(A),a->ForAll(GeneratorsOfGroup(B),b->a*b=b*a)),Concatenation("direct commute ",label));
 Print("DIRECT ",label," ",Size(G)," ",Size(A)," ",Size(B),"\n");
end;;
Extra:=function(N,k,label)
 local z,d,f;
 z:=Centre(N);d:=DerivedSubgroup(N);f:=FrattiniSubgroup(N);
 Need(Size(N)=2^k and Size(z)=2 and z=d and d=f,Concatenation("extraspecial ",label));
 Print("EXTRASPECIAL ",label," ",Size(N)," ",Size(z)," EXPONENT ",Exponent(N)," SQUARE_ONE ",Number(Elements(N),g->g^2=One(N)),"\n");
end;;
SplitS4:=function(C,label)
 local f,V,S,E,h,k;
 f:=SameNamed(C,SymmetricGroup(4),Concatenation(label,"_S4"));
 V:=PCore(C,2);S:=PreImage(f,Stabilizer(SymmetricGroup(4),4));
 Need(Size(V)=4 and IsElementaryAbelian(V),"S4 V4");SameNamed(S,SymmetricGroup(3),Concatenation(label,"_S3"));Split(C,V,S,Concatenation(label,"_V4_S3"));
 return rec(V:=V,S:=S);
end;;
for r in CubicModels do
 rr:=List(r.marking,PermList);G:=Group(rr);T:=Group(List(r.translation_basis,PermList));Q:=Group(List(r.split_complement,PermList));
 Need(Size(G)=48*r.s^3 and Size(T)=r.s^3 and IsAbelian(T) and Exponent(T)=r.s,"accepted cubic model");
 Split(G,T,Q,Concatenation("CUBIC",String(r.s)));
 Need(Size(Q)=48,"B3 order");
 if r.s=3 then
  SameNamed(G,WreathProduct(SymmetricGroup(3),SymmetricGroup(3)),"T6_2");
 elif r.s=4 then
  N:=Group(Concatenation(List(GeneratorsOfGroup(T),t->t^2),[PermList(r.twice_coordinate)],List(r.split_complement{[1,2,3]},PermList)));
  C:=Group(rr{[1,2,4]});Extra(N,7,"T6_3_N");Split(G,N,C,"T6_3");SplitS4(C,"T6_3");
 elif r.s=5 then
  SameNamed(G,WreathProduct(DihedralGroup(IsPermGroup,10),SymmetricGroup(3)),"T6_4");
 else
  T2:=Group(List(GeneratorsOfGroup(T),t->t^3));T3:=Group(List(GeneratorsOfGroup(T),t->t^2));
  Need(Size(T2)=8 and IsElementaryAbelian(T2) and Size(T3)=27,"CRT factors");Direct(T,T2,T3,"T6_5_TRANSLATIONS");C:=ClosureGroup(T3,Q);Split(G,T2,C,"T6_5");SameNamed(C,WreathProduct(SymmetricGroup(3),SymmetricGroup(3)),"T6_5_QUOTIENT");
 fi;
 Print("PASS_SHARED_ROW ",r.row,"\n");
od;
# Fixed faithful linear group gives the uniform square-family result; no s-sampling.
Q:=Group(List(SquareLinear,PermList));Need(Size(Q)=1152,"F4 linear group");N:=PCore(Q,2);Extra(N,5,"T8_1_O2");
CC:=ComplementClassesRepresentatives(Q,N);Need(Length(CC)>0,"F4 actual complement");C:=CC[1];Split(Q,N,C,"T8_1_LINEAR");
f:=SameNamed(C,DirectProduct(SymmetricGroup(3),SymmetricGroup(3)),"T8_1_S3xS3");
A:=PreImage(f,Image(Embedding(Range(f),1)));B:=PreImage(f,Image(Embedding(Range(f),2)));Direct(C,A,B,"T8_1_OUTER_FACTORS");
Print("PASS_SHARED_ROW T8.1 UNIFORM_FROM_ACCEPTED_AFFINE_MODEL\n");
for r in FiniteModels do
 gg:=List(r.generators,PermList);G:=Group(gg);CenterG:=Centre(G);P:=PerfectResiduum(G);
 Need(Size(CenterG)=2 and IsNormal(G,P),"finite central C2 and normal perfect residual");N:=ClosureGroup(P,CenterG);Direct(N,P,CenterG,"FINITE_CENTRAL_FACTOR");
 if r.n=3 then
  Need(Size(G)=720 and Size(P)=60,"finite t1 orders");SameNamed(P,AlternatingGroup(5),"T8_2_A5");
  CC:=ComplementClassesRepresentatives(G,N);Need(Length(CC)>0,"t1 complement exists");C:=CC[1];Split(G,N,C,"T8_2");SameNamed(C,SymmetricGroup(3),"T8_2_S3");
  Print("PASS_SHARED_ROW T8.2\n");
 else
  Need(Size(G)=46080 and Size(P)=960,"finite t2 orders");V:=PCore(P,2);Need(Size(V)=16 and IsElementaryAbelian(V),"t2 elementary kernel");
  AA:=ComplementClassesRepresentatives(P,V);Need(Length(AA)>0,"t2 inner complement");A:=AA[1];Split(P,V,A,"T8_3_INNER");SameNamed(A,AlternatingGroup(5),"T8_3_A5");
  CC:=ComplementClassesRepresentatives(G,N);Need(Length(CC)>0,"t2 outer complement");C:=CC[1];Split(G,N,C,"T8_3_OUTER");cs:=SplitS4(C,"T8_3");
  # Reproduce the printed mixed string, with every colon at its own stage.
  va:=First(Elements(cs.V),g->g<>One(G));vb:=Difference(Elements(cs.V),Elements(Group(va)))[1];
  Ca:=Group(va);Cb:=Group(vb);K1:=ClosureGroup(P,Ca);Split(K1,P,Ca,"T8_3_COLON2_FIRST");
  K2:=ClosureGroup(K1,CenterG);Direct(K2,K1,CenterG,"T8_3_TIMES2");
  K3:=ClosureGroup(K2,Cb);Split(K3,K2,Cb,"T8_3_COLON2_SECOND");Split(G,K3,cs.S,"T8_3_FINAL_S3");
  Print("PASS_SHARED_ROW T8.3\n");
 fi;
od;
Print("PASS_SEVEN_SHARED_STRUCTURES\n");;
QUIT;
