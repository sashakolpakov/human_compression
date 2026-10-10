# Independently generated projective actions; no author finite program imported.
F:=fail;; G:=fail;;
Need234:=function(ok,msg) if not ok then Error(msg);fi;end;
for p in [3,5] do
 F:=GF(p^2);; small:=GF(p);;
 points:=Concatenation(List(Elements(F),x->[One(F),x]),[[Zero(F),One(F)]]);;
 full:=GL(2,F);; phi:=ActionHomomorphism(full,points,OnLines);; P:=Image(phi);;
 smallGL:=GL(2,small);; beta:=ActionHomomorphism(smallGL,points,OnLines);; B:=Image(beta);;
 Need234(Size(P)=p^2*(p^4-1) and Size(B)=p*(p^2-1),"wrong projective actions");
 invol:=Filtered(Elements(B),g->Order(g)=2);; semi:=0;; uni:=0;; labels:=[];;
 for aa in invol do for bb in invol do
  u:=aa*bb;; n:=Order(u);;
  if n>2 then
   D:=Group(aa,bb);; C:=Centralizer(P,D);;
   Need234(IsSubgroup(B,C),"new field-extension centralizer");
   AddSet(labels,n);
   if n=p then
    Need234(Size(C)=1,"unipotent centralizer nontrivial");uni:=uni+1;
   else
    Need234(Size(C)=2,"semisimple centralizer not order2");
    A:=PreImagesRepresentative(beta,u);;
    traceZero:=A-(TraceMat(A)/(2*One(small)))*IdentityMat(2,small);;
    Need234(DeterminantMat(traceZero)<>Zero(small),"trace-zero representative singular");
    z:=Image(beta,traceZero);;
    Need234(z<>One(B) and C=Group(z),"trace-zero formula fails");semi:=semi+1;
   fi;
  fi;
 od;od;
 Print("FIELD ",p," TO ",p^2," SEMISIMPLE_PAIRS ",semi," UNIPOTENT_PAIRS ",uni," LABELS ",labels," PASS\n");
od;
for q in [4,8] do
 G:=PGL(2,q);;
 invol:=Filtered(Elements(G),g->Order(g)=2);;
 Need234(ForAll(invol,g->IsAbelian(Centralizer(G,g))),"characteristic2 centralizer");
 Print("CHAR2 ",q," INVOLUTIONS ",Length(invol)," PASS\n");
od;
# Omitting the odd-order condition is false, even for normal facets.
# A simpler C2 x C2 quotient supplies an explicit independent involution.
s:=(1,2);; H:=Group((3,4));; G:=Group((1,2),(3,4));;
Need234(IsNormal(G,H) and not s in H and Order((3,4)*s)=2,"even-order control");
# Omitting the normalizer condition is false with an odd adjacent product.
s:=(2,3);; t:=(1,2);; H:=Group(t);; G:=Group(s,t);;
Need234(Order(t*s)=3 and not s in H and not s in Normalizer(G,H),"normalizer control");
Print("ODDNESS_AND_NORMALIZER_WEAKENINGS_REFUTED\n");
Print("PHASE234_INDEPENDENT_CENTRALIZERS_PASS\n");
QUIT;
