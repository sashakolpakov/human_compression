Need:=function(b,s) if not b then Error(s);fi;end;;
IPCheckIn:=function(r,g)
 local n,sets,subs,i,j;
 n:=Length(r);sets:=Combinations([1..n]);subs:=List(sets,s->Group(r{s},()));
 subs[Position(sets,[1..n])]:=g;
 for i in [1..Length(sets)] do for j in [1..Length(sets)] do
  Need(Intersection(subs[i],subs[j])=subs[Position(sets,Intersection(sets[i],sets[j]))],"IP");
 od;od;
 return Length(sets)^2;
end;;
IPCheck:=r->IPCheckIn(r,Group(r));;
FT3Check:=function(r)
 local h,a,b,c,ab,ac,rhs;
 h:=[Group(r{[2,3]}),Group(r{[1,3]}),Group(r{[1,2]})];
 for a in [1..3] do
  b:=Difference([1..3],[a])[1];c:=Difference([1..3],[a])[2];
  ab:=Set(ListX(Elements(h[a]),Elements(h[b]),function(x,y)return x*y;end));
  ac:=Set(ListX(Elements(h[a]),Elements(h[c]),function(x,y)return x*y;end));
  rhs:=Set(ListX(Elements(h[a]),Elements(Intersection(h[b],h[c])),function(x,y)return x*y;end));
  Need(Intersection(ab,ac)=rhs,"full rank-three flag-transitivity");
 od;
 return List(h,Size);
end;;
CheckTriple:=function(name,r,size)
 local g,ip,pan;
 Need(Length(Set(r))=3 and ForAll(r,x->Order(x)=2),"three distinct involutions");
 g:=Group(r);Need(Size(g)=size,"generated whole named group");ip:=IPCheckIn(r,g);pan:=FT3Check(r);
 Print(name," order=",Size(g)," pair_orders=",[Order(r[1]*r[2]),Order(r[1]*r[3]),Order(r[2]*r[3])]," IP=",ip," flag_anchors=3 panels=",pan," PASS\n");
 return g;
end;;
