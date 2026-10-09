# Exhaustive search for smallest possible cyclic-TPP counterexamples.
# A smallest counterexample is two-generated, every pair generates it, and
# all three cyclic subgroups avoid its center. Thus their generators lie in
# the three distinct nonzero cosets of the Frattini subgroup.
LogTo("research/leemans/phase3_cyclic_tpp_search.log");;
SetInfoLevel(InfoWarning,0);
Main:=function()
local start,lg,n,abtypes,i,j,ids,id,g,phi,hom,images,z,els,x,o,s,seen,
 cats,c,cls,a,b,ab,product,candidates,catmax,active,groups,tests,hits,
 classes,representatives,conj,orbit,recorded,cyc,inv,allgens;
start:=Runtime();;
Print("GAP ",GAPInfo.Version," SmallGroups ",PackageInfo("smallgrp")[1].Version,"\n");
for lg in [2..8] do
 n:=2^lg;abtypes:=[];
 for i in [1..lg] do for j in [i..lg] do
  if i+j<lg then Add(abtypes,[2^i,2^j]);fi;
 od;od;
 if Length(abtypes)=0 then continue;fi;
 ids:=IdsOfAllSmallGroups(n,AbelianInvariants,abtypes);
 active:=0;groups:=0;tests:=0;hits:=[];
 for id in ids do
  g:=SmallGroup(id);groups:=groups+1;
  if NilpotencyClassOfGroup(g)<=2 then continue;fi;
  if ForAny(MaximalSubgroups(g),IsAbelian) then continue;fi;
  phi:=FrattiniSubgroup(g);
  if Index(g,phi)<>4 then Error("Generator-rank filter");fi;
  hom:=NaturalHomomorphismByNormalSubgroup(g,phi);
  images:=Filtered(Elements(Image(hom)),x->not IsOne(x));
  z:=Centre(g);els:=Elements(g);seen:=[];cats:=[[],[],[]];
  for x in els do
   if x in phi or x in seen then continue;fi;
   o:=Order(x);inv:=x^(o/2);
   if inv in z then continue;fi;
   s:=Set(List([0..o-1],i->x^i));
   UniteSet(seen,Filtered(s,y->Order(y)=o));
   j:=Position(images,Image(hom,x));
   Add(cats[j],rec(gen:=x,size:=o,elements:=s,involution:=inv));
  od;
  if ForAny(cats,c->Length(c)=0) then continue;fi;
  catmax:=List(cats,c->Maximum(List(c,a->a.size)));
  if Product(catmax)<=n then continue;fi;
  active:=active+1;
  # Anchor A up to conjugacy in G; the Frattini coset stays fixed.
  candidates:=List(cats[1],a->a.elements);representatives:=[];
  while Length(candidates)>0 do
   cyc:=candidates[1];
   Add(representatives,First(cats[1],a->a.elements=cyc));
   orbit:=Set(List(els,x->Set(cyc,y->y^x)));
   candidates:=Difference(candidates,orbit);
  od;
  for a in representatives do for b in cats[2] do
   if a.involution=b.involution or a.size*b.size*catmax[3]<=n then continue;fi;
   ab:=Set(Concatenation(List(a.elements,x->List(b.elements,y->x*y))));
   if Length(ab)<>a.size*b.size then Error("Cyclic pair intersection");fi;
   for c in cats[3] do
    if a.size*b.size*c.size<=n or c.involution=a.involution
       or c.involution=b.involution then continue;fi;
    tests:=tests+1;
    if Intersection(ab,c.elements)=[One(g)] then
     Print("COUNTEREXAMPLE id=",id," class=",NilpotencyClassOfGroup(g),
       " orders=",[a.size,b.size,c.size]," generators=",[a.gen,b.gen,c.gen],"\n");
     Add(hits,[id,[a.gen,b.gen,c.gen]]);
     # All three pairs must generate, independently checked on a hit.
     if Size(Group(a.gen,b.gen))<>n or Size(Group(a.gen,c.gen))<>n
       or Size(Group(b.gen,c.gen))<>n then Error("Pair generation");fi;
    fi;
   od;
  od;od;
 od;
 Print("ORDER ",n," two_generator_nonabelian_groups=",groups,
  " active_center_free_three_cosets=",active," TPP_tests=",tests,
  " hits=",Length(hits)," elapsed_ms=",Runtime()-start,"\n");
 if Length(hits)>0 then
  Print("FOUND_HITS ",hits,"\n");return;
 fi;
od;
Print("PASS: no smallest cyclic-TPP counterexample through order256.\n");
end;
Main();
LogTo();
QUIT;
