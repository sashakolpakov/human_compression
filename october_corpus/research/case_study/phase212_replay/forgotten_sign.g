# Exploratory checks for the currently missing odd labels in F014.
# This is not a general proof and does not identify universal presentations.
P212Require := function(ok,msg) if not ok then Print("P212_FAIL ",msg,"\n"); QUIT_GAP(1);fi;end;;
P212Marking := function(q,n,d)
 local F,alpha,a,H,one,marks,i,r;
 F:=GF(q); alpha:=fail;
 for a in Elements(F) do
  if not IsZero(a) then
   H:=[[One(F),a],[a,One(F)+a^2]];
   if Order(H)=n then alpha:=a;break;fi;
  fi;
 od;
 P212Require(alpha<>fail,"no exact-order coefficient");
 one:=IdentityMat(d,F);marks:=[];
 for i in [1..d] do
  r:=StructuralCopy(one);
  if i>1 then r[i][i-1]:=alpha;fi;
  if i<d then r[i][i+1]:=alpha;fi;
  Add(marks,r);
 od;
 return rec(q:=q,n:=n,d:=d,alpha:=alpha,marks:=marks,one:=one);
end;;
P212Q := function(u,a)
 return Sum(u,x->x^2)+a*Sum([1..Length(u)-1],i->u[i]*u[i+1]);
end;;
P212Reflection := function(u,a)
 local d,M,i,j,v,q;
 d:=Length(u); M:=IdentityMat(d,GF(32)); q:=P212Q(u,a);
 P212Require(q<>Zero(GF(32)),"nonsingular reflection support");
 v:=List([1..d],j->Zero(GF(32)));
 for j in [1..d] do
   v[j]:=Zero(GF(32));
   if j>1 then v[j]:=v[j]+a*u[j-1];fi;
   if j<d then v[j]:=v[j]+a*u[j+1];fi;
 od;
 for i in [1..d] do for j in [1..d] do M[i][j]:=M[i][j]+u[i]*v[j]/q;od;od;
 return M;
end;;

F:=GF(32);; a:=Z(32)^5;; beta:=Z(32)^3;; e:=One(F);;o:=Zero(F);;
P212Require(Z(32)^5+Z(32)^2+e=o,"GF32 defining polynomial");
BAS:=Basis(F,List([0..4],i->Z(32)^i));;
Code:=function(x)return Sum([1..5],i->IntFFE(Coefficients(BAS,x)[i])*2^(i-1));end;;
Codes:=v->List(v,Code);;
Q:=v->P212Q(v,a);;
M:=P212Marking(32,11,5);;r:=M.marks;;
P212Require(M.alpha=a,"fixed coefficient");
for i in [1..5] do
 P212Require(Order(r[i])=2,"marker order");
 for j in [i+1..5] do
  if j=i+1 then P212Require(Order(r[i]*r[j])=11,"adjacent order");
  else P212Require((r[i]*r[j])^2=M.one,"distant commute");fi;
 od;
od;
for i in [1..3] do for k in [1..10] do
 P212Require(((r[i+1]*r[i+2])^k*(r[i]*r[i+1])^k)^2=M.one,"local power relator");
od;od;
Print("P212_LITERAL_RELATORS_PASS 45\n");
# Rank-four images on their singular quadrics.
M4:=P212Marking(32,11,4);;
Gt:=Group(List(M4.marks,TransposedMat));;
orb:=Orbit(Gt,[e,o,e,o],OnLines);;
act:=ActionHomomorphism(Gt,orb,OnLines);;
P4gens:=List(M4.marks,x->Permutation(TransposedMat(x),orb,OnLines));;
P4:=Group(P4gens);;
P212Require(Length(orb)=1025 and Size(P4)=2147481600,"rank4 image bound");
P4sign:=Group(List(P4gens,g->g*(1026,1027)));;
P212Require(Size(P4sign)=2147481600,"rank4 signed image bound");
# Produce a projective frame in the quadric. Its four first vectors are a basis;
# the fifth has no zero coefficient in that basis.
frame:=[];;
for v in orb do if RankMat(Concatenation(frame,[v]))>Length(frame) then Add(frame,v);fi;if Length(frame)=4 then break;fi;od;
P212Require(Length(frame)=4,"quadric spanning");
frame5:=fail;;coords:=fail;;
for v in orb do
 c:=SolutionMat(frame,v);
 if ForAll(c,x->x<>o) then frame5:=v;coords:=c;break;fi;
od;
P212Require(frame5<>fail,"quadric projective frame");
Print("P212_QUADRIC_FRAME ",List(frame,Codes)," ",Codes(frame5)," ",Codes(coords),"\n");
S5:=P212Reflection([o,e,beta,o,o],a);;
for side in [1,2] do
 if side=1 then target:=P212Reflection([o,e,beta,o],a);else target:=P212Reflection([e,beta,o,o],a);fi;
 perm:=Permutation(TransposedMat(target),orb,OnLines);
 P212Require(perm in P4,"rank4 reflection image membership");
 P212Require(perm*(1026,1027) in P4sign,"rank4 signed reflection membership");
 Print("P212_ENDPOINT_REFLECTION_MEMBER ",side," signed 1\n");
od;
# Quotient the middle three-space by its singular radical e2+e4.
MidQuot:=function(A)
 return [[A[2][2]+A[4][2],A[2][3]+A[4][3]],[A[3][2],A[3][3]]];
end;;
D:=Group(List([2..4],j->MidQuot(r[j])));;
P212Require(Size(D)=22,"middle quotient order");
P212Require(not MidQuot(S5) in D,"reflection outside middle");
P212Require(Order(MidQuot(r[2])*MidQuot(S5))=33,"outside rotation order");
Print("P212_MIDDLE_QUOTIENT_BOUND 22 outside_rotation33\n");
# Exact full middle order, using its elementary translation group.
# Enumerate the small 3-dimensional restriction, whose singular radical acts
# trivially and whose translations are faithful on this three-space.
Mid3:=Group(List([2..4],j->r[j]{[2..4]}{[2..4]}));;
P212Require(Size(Mid3)=22528,"middle restriction image order");
Print("P212_MIDDLE_RESTRICTION_ORDER 22528\n");
# Projection onto V/rad(B), rad(B)=span(e1+e3+e5).
P212Quotient:=function(A)
 return [List([1..4],j->A[1][j]+A[5][j]),A[2]{[1..4]},List([1..4],j->A[3][j]+A[5][j]),A[4]{[1..4]}];
end;;
rs:=List(r,P212Quotient);;
G5:=Group(List(rs,TransposedMat));;
orb5:=Orbit(G5,[e,o,o,o],OnLines);;
act5:=ActionHomomorphism(G5,orb5,OnLines);;
P5gens:=List(rs,x->Permutation(TransposedMat(x),orb5,OnLines));;
P5:=Group(P5gens);;
P212Require(Length(orb5)=33825 and Size(P5)=1124799322521600,"rank5 image bound");
P212Require(IsSimpleGroup(P5),"rank5 image simplicity");
Print("P212_SP4_IMAGE ",Size(P5)," simple true\n");
P5sign:=Group(List(P5gens,g->g));;
P212Require(Size(P5sign)=2249598645043200,"rank5 signed image bound");
Print("P212_SIGNED_IMAGE_ORDER ",Size(P5sign),"\n");
Print("P212_LITERAL_MATRIX_CERTIFICATE_PASS\n");
QUIT_GAP(0);
