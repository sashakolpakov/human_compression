Check250:=function(ok,s) if not ok then Error(Concatenation("P250_REJECT ",s));fi;end;;
IP250:=function(rr)
 local subsets,hs,i,j;
 subsets:=Combinations([1..3]);hs:=List(subsets,x->Group(rr{x},One(rr[1])));
 for i in [1..8] do for j in [1..8] do
 if Intersection(hs[i],hs[j])<>hs[Position(subsets,Intersection(subsets[i],subsets[j]))] then return false;fi;
 od;od;return true;
end;;
Run250:=function()
 local F,a,b,c,x,w,s,U,iso,G,rr,D,dd,Q,qi,qp,qg,ep,x1,y1,z1,corrected,rels;
F:=FreeGroup("a","b","c");;a:=F.1;;b:=F.2;;c:=F.3;;x:=b*c;;
w:=b*a*c*b*a*(c*b)^2*a;;
for s in [2,3,4] do
 U:=F/[a^2,b^2,c^2,(a*b)^6,x^(2^s),(a*c)^2,Comm(a,x^4),w^2];;
 iso:=IsomorphismPermGroup(U);;G:=Image(iso);;rr:=List(GeneratorsOfGroup(U),g->Image(iso,g));;
 Check250(Size(G)=384*2^(s-2) and Order(rr[1]*rr[2])=6 and Order(rr[2]*rr[3])=2^s and IP250(rr),"exceptional family");
 # Use a literal dihedral presentation to avoid generator-convention assumptions.
 Q:=F/[a,b^2,c^2,x^(2^s)];;qi:=IsomorphismPermGroup(Q);;qp:=Image(qi);;qg:=List(GeneratorsOfGroup(Q),g->Image(qi,g));;
 ep:=GroupHomomorphismByImages(G,qp,rr,qg);;Check250(ep<>fail and IsSurjective(ep),"pair retraction");
 Print("EXCEPTIONAL64 s ",s," ORDER ",Size(G)," IP64 RETRACTION PASS\n");
od;
x1:=(b*c^(b*a))^2;;y1:=(c^b*b^a)^2;;z1:=(c*b^(a*b))^2;;

for corrected in [false,true] do
 rels:=[a^2,b^2,c^2,(a*b)^6,x^16,(a*c)^2,Comm(a,x^2)^2,Comm(a,x^4),y1^2*x^-4,z1^2*x^4];
 if corrected then Add(rels,x1^2*x^4);else Add(rels,x1^2*x^-4);fi;
 U:=F/rels;iso:=IsomorphismPermGroup(U);G:=Image(iso);rr:=List(GeneratorsOfGroup(U),g->Image(iso,g));
 if corrected then
  Check250(Size(G)=3072 and Order(rr[2]*rr[3])=16 and IP250(rr),"corrected source sign");
  Print("CORRECTED45 n10 s4 ORDER3072 ROTATION16 IP64 PASS\n");
 else
  Check250(Size(G)=1536 and Order(rr[2]*rr[3])=8,"literal source sign discrepancy");
  Print("LITERAL45 n10 s4 ORDER1536 ROTATION8 REJECTED_TARGET\n");
 fi;
od;

a:=(1,2);x:=(1,2,3);b:=x^2;
Check250(a^-1*b*a=b^-1 and b^2=x^4 and x^8<>One(Group(a,x)),"commutation false weakening");
Print("PERIOD_COMMUTATION_FALSE_WEAKENING_REJECTED\nPHASE250_FIXED_GROUPS_PASS\n");


end;;
Run250();
QUIT_GAP(0);
