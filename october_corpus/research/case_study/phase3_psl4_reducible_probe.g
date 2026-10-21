# Exact, deliberately narrow mixed-sign reducible-endpoint probe.
# No random search, and no inference to all fields or middle generators.
if not IsBound(ProbeQ) then ProbeQ:=25; fi;
q:=ProbeQ;; F:=GF(q);; one:=One(F);; zero:=Zero(F);;
I2:=IdentityMat(2,F);;
Z2:=DiagonalMat([one,-one]);;
X2:=[[zero,one],[one,zero]];;
torusOdd:=First(DivisorsInt(q-1),d->d>1 and IsOddInt(d));;
if torusOdd=fail then Error("Need nontrivial odd split torus"); fi;
t:=Z(q)^((q-1)/torusOdd);;
R2:=[[zero,t],[t^-1,zero]];;
block:=function(A,B)
 return [[A[1][1],A[1][2],zero,zero],
 [A[2][1],A[2][2],zero,zero],
 [zero,zero,B[1][1],B[1][2]],
 [zero,zero,B[2][1],B[2][2]]];
end;;
a:=2*one;;
B2:=[[a,one],[one-a^2,-a]];;
mm:=[block(Z2,Z2),block(X2,I2),KroneckerProduct(B2,I2),
 block(X2,R2),block(X2,X2)];;
points:=Concatenation(List([0..3],j->List(Tuples(Elements(F),3-j),
 tail->Concatenation(List([1..j],i->zero),[one],tail))));;
Sort(points);;
Print("POINTS_READY ",Length(points),"\n");
rr:=List(mm,m->PermList(List(points,p->PositionSorted(points,OnLines(p,m)))));;
Print("FIELD ",q," projective_degree ",Length(points)," torder ",Order(t),"\n");
Print("INVOLUTION_ORDERS ",List(rr,Order),"\n");
Print("PSL_MEMBERSHIP_DETERMINANT_TEST ",List(mm,m->
 Determinant(m)^((q-1)/GcdInt(4,q-1))=one),"\n");
Print("ADJACENT_PRODUCTS ",List([1..4],i->Order(rr[i]*rr[i+1])),"\n");
Print("DISTANT_COMMUTATIONS ",List([[1,3],[1,4],[1,5],[2,4],[2,5],[3,5]],
 pair->rr[pair[1]]*rr[pair[2]]=rr[pair[2]]*rr[pair[1]]),"\n");
for indices in [[1,2],[4,5],[1,3,5],[1,2,3],[2,3,4],[3,4,5],
 [1,2,3,4],[2,3,4,5],[1,2,3,4,5]] do
 h:=Group(rr{indices});;
 Print("SUBGROUP ",indices," ORDER ",Size(h)," RUNTIME ",Runtime(),"\n");
od;
Print("LEFT_TRIPLE_IP ",Intersection(Group(rr{[1,2]}),Group(rr{[2,3]}))=Group(rr[2]),"\n");
Print("MIDDLE_TRIPLE_IP ",Intersection(Group(rr{[2,3]}),Group(rr{[3,4]}))=Group(rr[3]),"\n");
Print("RIGHT_TRIPLE_IP ",Intersection(Group(rr{[3,4]}),Group(rr{[4,5]}))=Group(rr[4]),"\n");
Print("LEFT_RANK4_IP_INTERSECTION ",Size(Intersection(Group(rr{[1,2,3]}),Group(rr{[2,3,4]}))),
 " EXPECTED ",Size(Group(rr{[2,3]})),"\n");
Print("RIGHT_RANK4_IP_INTERSECTION ",Size(Intersection(Group(rr{[2,3,4]}),Group(rr{[3,4,5]}))),
 " EXPECTED ",Size(Group(rr{[3,4]})),"\n");
form:=block(2*X2,X2);;
Print("EXPLICIT_FORM_MULTIPLIERS ",List(mm,m->First([one,-one],
 k->TransposedMat(m)*form*m=k*form)),"\n");
Print("PSL4_EXPECTED_ORDER ",q^6*(q^2-1)*(q^3-1)*(q^4-1)/GcdInt(4,q-1),"\n");
QUIT;
