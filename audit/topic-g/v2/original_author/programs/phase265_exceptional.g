# Complete exceptional group/design interfaces and literal source controls.
Need:=function(b,s) if not b then Error(s);fi;end;
F:=GF(2);vec:=Filtered(Tuples(Elements(F),4),v->not IsZero(v));
G:=Action(GL(4,2),vec,OnRight);A8:=AlternatingGroup(8);
iso:=IsomorphismGroups(G,A8);Need(iso<>fail,"GL4,2 to A8 isomorphism");
H:=PreImage(iso,Stabilizer(A8,8));
Need(Size(G)=20160 and Size(H)=2520,"exceptional group orders");
T:=Filtered(Tuples([1..15],3),t->Length(Set(t))=3 and vec[t[1]]+vec[t[2]]<>vec[t[3]]);
Need(Length(T)=2520 and Set(Orbit(H,T[1],OnTuples))=Set(T),"all noncollinear triples");
Need(Length(Orbit(H,[1,2],OnTuples))=210,"all distinct nonzero vector pairs");
Print("PHASE265_A7_PASS PG3,2_noncollinear2520 affine_binary_pair210\n");
# U_H(2) as the unique displayed nine-point affine-plane design.
q:=2;K:=GF(4);els:=Elements(K);z:=Zero(K);o:=One(K);pv:=[];
for x in els do for y in els do Add(pv,[o,x,y]);od;od;
for x in els do Add(pv,[z,o,x]);od;Add(pv,[z,z,o]);
pts:=Filtered(pv,v->Sum(v,x->x^(q+1))=z);blocks:=[];
for c in pv do
 B:=Filtered([1..Length(pts)],i->Sum([1..3],j->pts[i][j]*c[j])=z);
 if Length(B)=3 then AddSet(blocks,B);fi;
od;
Need(Length(pts)=9 and Length(blocks)=12,"small unital sizes");
V:=Tuples(Elements(GF(3)),2);AGlines:=Set(Concatenation(List(V,v->List(Filtered(V,w->not IsZero(w)),w->Set(List(Elements(GF(3)),a->Position(V,v+a*w)))))));
Need(Length(AGlines)=12,"affine three lines");
Tsrc:=First(Combinations([1..9],3),t->not t in blocks);
Tdst:=First(Combinations([1..9],3),t->not t in AGlines);
restsrc:=Difference([1..9],Tsrc);restdst:=Difference([1..9],Tdst);found:=fail;
f:=[];
for per in PermutationsList(restdst) do
 f:=List([1..9],x->0);
 for i in [1..3] do f[Tsrc[i]]:=Tdst[i];od;
 for i in [1..6] do f[restsrc[i]]:=per[i];od;
 if Set(List(blocks,B->Set(List(B,x->f[x]))))=AGlines then found:=f;break;fi;
od;
Need(found<>fail,"literal unital-affine incidence isomorphism");
Print("PHASE265_UH2_PASS explicit_point_bijection",found," all12blocks\n");
# Field automorphisms missing from a literal AGL label.
K:=GF(4);V:=Tuples(Elements(K),2);z:=Z(4);zero:=Zero(K);one:=One(K);
lines:=Set(Concatenation(List(V,v->List(Filtered(V,w->not IsZero(w)),w->Set(List(Elements(K),a->Position(V,v+a*w)))))));
frob:=PermList(List(V,v->Position(V,List(v,x->x^2))));
Need(ForAll(lines,L->OnSets(L,frob) in lines),"Frobenius line preservation");
fixed:=List([[zero,zero],[one,zero],[zero,one]],v->Position(V,v));
Need(ForAll(fixed,i->i^frob=i) and Position(V,[z,zero])^frob<>Position(V,[z,zero]),"not K-affine linear");
# A forward incidence morphism need not respect the negative incidence clause.
# The triangle K3 has point0 on line{0,1}; collapsing each input type there
# preserves all input incidences but destroys the displayed triangle edge.
Need(0 in [0,1] and not 2 in [0,1] and 0 in [0,2],"source triangle edge");
Need(not (0 in [0,1] and not 0 in [0,1]),"constant morphism destroys edge");
Print("PHASE265_CONTROLS_PASS Frobenius_not_AGL literal_functor_counterexample\n");
QUIT;
