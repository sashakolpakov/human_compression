# Distinct review model: an unfaithful quotient of a three-generator Coxeter group.
# Maximal-parabolic intersections and generated supports differ in this model.
Require:=function(t,s) if not t then Error(s);fi;end;
F:=FreeGroup(3); f:=GeneratorsOfGroup(F); c:=Comm(f[1],f[2]);
rels:=Concatenation(List(f,x->x^2),List(f,x->Comm(c,x)),
  [Comm(f[1],f[3])*c^-1,Comm(f[2],f[3])*c^-1]);
Q:=F/rels; iso:=IsomorphismPermGroup(Q); C:=Image(iso);
a:=List(GeneratorsOfGroup(Q),x->Image(iso,x));
Require(Size(C)=16,"order16 quotient");
P:=List([1..3],i->Subgroup(C,a{Difference([1..3],[i])}));
H:=Intersection(P);Require(Size(H)=2 and IsNormal(C,H),"chamber kernel");
Require(Intersection(P[2],P[3])<>Subgroup(C,[a[1]]),"generated support must differ");
Require(not IsSubgroup(TrivialSubgroup(C),H),"empty generated support omits kernel");
pi:=NaturalHomomorphismByNormalSubgroup(C,H);
Require(Size(Image(pi))=8 and IsElementaryAbelian(Image(pi)),"faithful Boolean quotient");
B:=Group((1,2),(2,3)); b:=[(1,2),(2,3)];
s:=GroupHomomorphismByImages(C,C,a,[a[2],a[1],a[3]]);
t:=GroupHomomorphismByImages(C,C,a,[a[1],a[3],a[2]]);
Require(s<>fail and t<>fail,"label permutation action");
eta:=GroupHomomorphismByImages(B,Group(s,t),b,[s,t]);
Require(eta<>fail,"action homomorphism");
G:=SemidirectProduct(B,eta,C); eB:=Embedding(G,1);eC:=Embedding(G,2);
K:=Image(eC,H);Require(Size(G)=96 and IsNormal(G,K),"twisting chamber kernel");
BP:=[Subgroup(B,[b[2]]),Subgroup(B,[b[1]])];
CP:=[Intersection(P[2],P[3]),P[3],H];
pars:=List([1..2],i->ClosureGroup(Image(eC,CP[i]),Image(eB,BP[i])));
Add(pars,ClosureGroup(Image(eC,H),Image(eB,B)));
Require(List(pars,Size)=[8,16,12],"intersection-defined parabolics");
Require(ForAll(pars,p->IsSubgroup(p,K)),"all parabolics contain kernel");
proj:=NaturalHomomorphismByNormalSubgroup(G,K);
Require(Size(Image(proj))=48,"faithful twisted group");
Require(ForAll(pars,p->PreImage(proj,Image(proj,p))=p),"parabolics are full preimages");
cosets:=List(pars,p->Set(List(Elements(G),g->Set(List(Elements(p),x->g*x)))));
chambers:=0; full:=0;
for x in cosets[1] do for y in cosets[2] do for z in cosets[3] do
  if Length(Intersection(x,y))>0 and Length(Intersection(x,z))>0 and Length(Intersection(y,z))>0 then
    chambers:=chambers+1;
    if Length(Intersection(x,y,z))=2 then full:=full+1;fi;
  fi;
od;od;od;
Require(chambers=48 and full=48,"every chamber has exactly one kernel coset");
Require(Intersection(pars)=K,"exact chamber stabilizer");
Print("UNFAITHFUL_QUOTIENT_CHECK PASS order96 kernel2 faithful48 chambers48\n");
QUIT;
