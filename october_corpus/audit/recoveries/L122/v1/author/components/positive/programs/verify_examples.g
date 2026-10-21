Need:=function(x,m) if not x then Error(m);fi;end;;
Read("data/seeds.g");;
Need(DefaultStabChainOptions.random=1000,"guaranteed permutation chain verification");;
FreshOrders:=[];;
CheckFields:=function()
 local qfield,coeffs;
 for qfield in [8,27,64,125,512] do
 coeffs:=TrialityFieldPolynomials.(Concatenation("q",String(qfield)));
 Need(Sum([1..Length(coeffs)],i->coeffs[i]*Z(qfield)^(i-1))=Zero(GF(qfield)),"literal field defining polynomial");
 Need(Order(Z(qfield))=qfield-1,"primitive field generator");
 od;
end;;
CheckFields();;
Need(TrialitySeeds.psl64[2][1]=Z(64)^9,"published subfield coefficient");;
FreshOrder:=function(g)
 local h,o,s;
 h:=Group(ShallowCopy(GeneratorsOfGroup(g)),());
 Need(not HasSize(h) and not HasStabChainMutable(h),"uncached permutation group");
 Need(IsIdenticalObj(Parent(h),h),"no ambient order bound");
 Need(not IsBound(StabChainOptions(h).size) and not IsBound(StabChainOptions(h).limit),"no inherited size or upper bound");
 o:=rec(random:=1000,tryPcgs:=false);s:=StabChain(h,o);
 Need(not IsBound(o.size) and not IsBound(o.limit),"no supplied size bound");
 Need(not IsBound(StabChainOptions(h).size) and not IsBound(StabChainOptions(h).limit),"no chain supplied size or upper bound");
 Add(FreshOrders,SizeStabChain(s));
 Print("FRESH|",Length(FreshOrders),"|",SizeStabChain(s),"|NO_CACHED_SIZE_OR_CHAIN\n");
 return SizeStabChain(s);
end;;
FrobMatrix:=function(m,p) return List(m,r->List(r,x->x^p));end;;
MakePSL:=function(q,p)
 local f,e,z,M,points,hom,g,mg,sigma,c,cg,m,seed,tau,fp;
 f:=GF(q);e:=One(f);z:=Zero(f);M:=SL(2,q);
 points:=Concatenation(List(Elements(f),x->[e,x]),[[z,e]]);
 hom:=ActionHomomorphism(M,points,OnLines);g:=Image(hom);mg:=GeneratorsOfGroup(M);
 Need(FreshOrder(g)=q*(q^2-1)/Gcd(2,q-1),"exact projective linear image order");
 if q=8 then
  tau:=Image(hom,TrialitySeeds.psl8_inner);Need(Order(tau)=3,"inner element order three");
  sigma:=InnerAutomorphism(g,tau);c:=Centralizer(g,tau);
  Need(FreshOrder(c)=9 and IsCyclic(c),"inner reduced group cyclic nine");
 else
  sigma:=GroupHomomorphismByImages(g,g,List(mg,x->Image(hom,x)),List(mg,x->Image(hom,FrobMatrix(x,p))));
  fp:=PermList(List(points,v->Position(points,List(v,x->x^p))));
  Need(ForAll(GeneratorsOfGroup(g),x->Image(sigma,x)=x^fp),"field permutation realizes automorphism");
  Need(not fp in g and IsTransitive(Stabilizer(g,1),[2..q+1]),"outer action via trivial centralizer");
  cg:=List(GeneratorsOfGroup(SL(2,p)),m->List(m,r->List(r,x->x*e)));
  c:=Group(List(cg,m->Image(hom,m)));
  Need(FreshOrder(c)=p*(p^2-1)/Gcd(2,p-1),"exact fixed-subfield subgroup");
 fi;
 Need(IsBijective(sigma) and Order(sigma)=3,"order-three group automorphism");
 Need(ForAll(GeneratorsOfGroup(c),x->Image(sigma,x)=x),"fixed subgroup containment");
 seed:=TrialitySeeds.(Concatenation("psl",String(q)));
 Need(DeterminantMat(seed)=e and seed in M,"literal determinant-one seed");
 return rec(name:=Concatenation("PSL2_",String(q)),group:=g,sigma:=sigma,seed:=Image(hom,seed),fixed:=c,field:=q,base:=p);
end;;
MakeSz:=function()
 local M,mg,points,hom,g,sigma,e,z,u,w,c,fp;
 M:=SuzukiGroup(IsMatrixGroup,8);mg:=GeneratorsOfGroup(M);e:=One(GF(8));z:=Zero(GF(8));
 points:=ShallowCopy(Orbit(M,[e,z,z,z],OnLines));Sort(points);Need(Length(points)=65,"Suzuki ovoid");
 hom:=ActionHomomorphism(M,points,OnLines);g:=Image(hom);Need(FreshOrder(g)=29120,"faithful Suzuki ovoid action");
 sigma:=GroupHomomorphismByImages(g,g,List(mg,x->Image(hom,x)),List(mg,x->Image(hom,FrobMatrix(x,2))));
 Need(IsBijective(sigma) and Order(sigma)=3,"Suzuki field automorphism");
 fp:=PermList(List(points,v->Position(points,List(v,x->x^2))));
 Need(ForAll(GeneratorsOfGroup(g),x->Image(sigma,x)=x^fp),"Suzuki field permutation");
 Need(not fp in g and IsTransitive(Stabilizer(g,1),[2..65]),"Suzuki outer action via trivial centralizer");
 u:=[[e,z,z,z],[e,e,z,z],[e,e,e,z],[e,z,e,e]];
 w:=[[z,z,z,e],[z,z,e,z],[z,e,z,z],[e,z,z,z]];
 Need(u in M and w in M and TrialitySeeds.sz8 in M,"literal Suzuki matrices");
 c:=Group(Image(hom,u),Image(hom,w));Need(FreshOrder(c)=20,"fixed binary Suzuki subgroup");
 Need(ForAll(GeneratorsOfGroup(c),x->Image(sigma,x)=x),"fixed binary coefficients");
 Need(IsCyclic(DerivedSubgroup(c)) and Size(DerivedSubgroup(c))=5,"normal five subgroup");
 Need(ForAny(Elements(c),x->Order(x)=4),"cyclic complement four");
 Need(Size(Centralizer(c,DerivedSubgroup(c)))=5,"faithful complement action");
 Need(Number(Elements(g),x->Image(sigma,x)=x)=20,"complete Suzuki field-fixed group");
 return rec(name:="Sz8",group:=g,sigma:=sigma,seed:=Image(hom,TrialitySeeds.sz8),fixed:=c,field:=8,base:=2);
end;;
Verify:=function(model)
 local g,s,t,H,subs,sets,I,J,K,products,panels,orders,counts,n,cos,abs,C,orbit,reps,CC,Inc,i,j,k,x,y,z,missing,edges,triangles;
 g:=model.group;s:=model.sigma;t:=List([0..2],i->Image(s^i,model.seed));
 Need(Length(Set(t))=3 and ForAll(t,x->Order(x)=2),"three distinct involutions");
 Need(FreshOrder(Group(t))=Size(g),"full generated group");
 sets:=Combinations([1..3]);subs:=List(sets,I->Subgroup(g,t{I}));
 for I in [1..8] do for J in [1..8] do
  K:=Position(sets,Intersection(sets[I],sets[J]));Need(Intersection(subs[I],subs[J])=subs[K],"full 64 subgroup intersections");
 od;od;
 H:=List([1..3],i->Subgroup(g,t{Difference([1..3],[i])}));
 Need(ForAll([1..3],i->Image(s,H[i])=H[i mod 3+1]),"parabolics cyclically transported");
 products:=[];
 for i in [1..3] do
  j:=i mod 3+1;k:=j mod 3+1;
  n:=Number(Elements(H[i]),x->x in DoubleCoset(H[j],One(g),H[k]));Add(products,n);
  Need(n=4,"all exact chamber-completion products");
 od;
 orders:=List(H,Size);counts:=List(orders,x->Size(g)/x);
 Need(Length(Set(orders))=1,"equal parabolic orders");
 Print("EXAMPLE|",model.name,"|",Size(g),"|",orders[1],"|",counts[1],"|",Size(model.fixed),"|",Order(t[1]*t[2]),"\n");
 if model.name="Sz8" then
  cos:=RightCosets(g,H[1]);
  abs:=Filtered(cos,c->Representative(c)*Image(s,Representative(c))^-1 in DoubleCoset(H[1],One(g),H[2]));
  Need(Length(abs)=20,"twenty absolute type-zero cosets");
  C:=model.fixed;orbit:=Orbit(C,abs[1],OnRight);Need(Set(orbit)=Set(abs),"single regular absolute orbit");
  reps:=List(abs,Representative);CC:=List([0..2],i->List(reps,x->RightCoset(H[i+1],Image(s^i,x))));
  Inc:=function(i,x,j,y) return not IsEmpty(Intersection(CC[i][x],CC[j][y]));end;
  edges:=0;triangles:=0;missing:=0;
  for I in Combinations([1..3],2) do
   i:=I[1];j:=I[2];k:=Difference([1..3],I)[1];
   for x in [1..20] do for y in [1..20] do
    Need(Inc(i,x,j,y)=(x=y),"absolute triples are disjoint chambers");
    if Inc(i,x,j,y) then
     edges:=edges+1;n:=Number([1..20],z->Inc(i,x,k,z) and Inc(j,y,k,z));
     if n=0 then missing:=missing+1;fi;triangles:=triangles+n;
    fi;
   od;od;
  od;
  Need(edges=60 and triangles=60 and missing=0,"whole induced absolute subgeometry");
  Print("ABSOLUTE|20|20|60|20|0\n");
 fi;
end;;
Verify(MakeSz());;
for qp in [[8,2],[27,3],[64,4],[125,5],[512,8]] do Verify(MakePSL(qp[1],qp[2]));od;
Need(Length(FreshOrders)=18,"whole fresh-order boundary");;
Print("L122_FINITE_EXAMPLES_PASS\n");QUIT;
