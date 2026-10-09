# Exhaust all two-generator groups of order 512 in SmallGroups 1.5.4.
# Library range: SmallGroupsInformation(512), rank-two entries 2..2044.
# Proof of the reduction is in phase3_cyclic_tpp_exploration.md.
# Run from the directory containing this file; output is written there.
LogTo("phase7_cyclic_tpp_search.log");;
SetInfoLevel(InfoWarning,0);;
Main := function()
local start, id, g, phi, z, hom, images, seen, cats, x, o, inv, s, j,
      maxima, classes, abelian, smallclass, abindex, remaining, eligible,
      hist, key, pos, n, a, b, c, ab, tests, hits, allmax;
start := Runtime();
Print("GAP ", GAPInfo.Version, " SmallGroups ",
      PackageInfo("smallgrp")[1].Version, "\n");
SmallGroupsInformation(512);
classes := 0; abelian := 0; smallclass := 0; abindex := 0;
remaining := 0; eligible := 0; tests := 0; hits := 0; hist := [];
allmax := 0;
for id in [2..2044] do
  g := SmallGroup(512,id); classes := classes+1;
  phi := FrattiniSubgroup(g);
  if Size(g)<>512 or Index(g,phi)<>4 then
    Error("Catalogue range is not exactly rank two");
  fi;
  if IsAbelian(g) then abelian := abelian+1; continue; fi;
  if NilpotencyClassOfGroup(g)<=2 then
    smallclass := smallclass+1; continue;
  fi;
  if ForAny(MaximalSubgroups(g),IsAbelian) then
    abindex := abindex+1; continue;
  fi;
  remaining := remaining+1;
  z := Centre(g);
  hom := NaturalHomomorphismByNormalSubgroup(g,phi);
  images := Filtered(Elements(Image(hom)),x->not IsOne(x));
  seen := []; cats := [[],[],[]];
  for x in Elements(g) do
    if x in phi or x in seen then continue; fi;
    o := Order(x); inv := x^(o/2);
    if inv in z then continue; fi;
    s := Set(List([0..o-1],j->x^j));
    UniteSet(seen,Filtered(s,x->Order(x)=o));
    j := Position(images,Image(hom,x));
    Add(cats[j],rec(gen:=x,size:=o,elements:=s,involution:=inv));
  od;
  maxima := List(cats,c->Maximum(Concatenation([0],List(c,a->a.size))));
  allmax := Maximum(allmax,Product(maxima));
  key := SortedList(maxima);
  pos := PositionProperty(hist,x->x[1]=key);
  if pos=fail then Add(hist,[key,1]); else hist[pos][2]:=hist[pos][2]+1; fi;
  if Product(maxima)<=512 then continue; fi;
  eligible := eligible+1;
  Print("ACTIVE id=",id," class=",NilpotencyClassOfGroup(g),
        " maxima=",maxima,"\n");
  # No orbit reduction: every qualifying cyclic triple is tested literally.
  for a in cats[1] do for b in cats[2] do
    if a.involution=b.involution or a.size*b.size*maxima[3]<=512 then
      continue;
    fi;
    ab := Set(Concatenation(List(a.elements,x->List(b.elements,y->x*y))));
    if Length(ab)<>a.size*b.size then Error("Pair intersection failure"); fi;
    for c in cats[3] do
      if a.size*b.size*c.size<=512 or c.involution=a.involution
         or c.involution=b.involution then continue; fi;
      tests := tests+1;
      if Intersection(ab,c.elements)=[One(g)] then
        hits := hits+1;
        Print("HIT id=",id," orders=",[a.size,b.size,c.size],
              " generators=",[a.gen,b.gen,c.gen],"\n");
      fi;
    od;
  od; od;
od;
Sort(hist);
Print("COUNTS all_rank_two=",classes," abelian=",abelian,
      " class_at_most_two=",smallclass," abelian_index_two=",abindex,
      " remaining=",remaining," active=",eligible," tests=",tests,
      " hits=",hits," max_product=",allmax,"\n");
Print("HISTOGRAM ",hist,"\n");
if hits=0 then
  Print("PASS: cyclic TPP bound at order512, conditional on prior smaller-order certificate and library completeness.\n");
else
  Print("COUNTEREXAMPLES require independent checking.\n");
fi;
Print("elapsed_ms=",Runtime()-start,"\n");
end;;
Main();
LogTo();
QUIT;
