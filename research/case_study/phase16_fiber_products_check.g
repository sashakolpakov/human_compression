# Exact finite diagnostics for the full presentation, independently of the
# tuple construction. All subgroups and all subset intersections are checked.
# Run from any directory: gap -q phase16_fiber_products_check.g
SetInfoLevel(InfoWarning,0);;
cases := [[5],[6],[7],[5,6],[6,6],[5,7],[6,5,6],[5,6,5]];;
for ns in cases do
  d := Length(ns)+2;
  f := FreeGroup(d); r := GeneratorsOfGroup(f);
  rel := List(r,x->x^2);
  for i in [1..d] do
    for j in [i+1..d] do
      if j=i+1 then Add(rel,(r[i]*r[j])^4);
      else Add(rel,Comm(r[i],r[j])); fi;
    od;
  od;
  for i in [1..d-2] do
    t := r[i]*r[i+1]*r[i+2]*r[i+1];
    u := r[i+2]*r[i+1]*r[i]*r[i+1];
    n := ns[i];
    if n mod 2=1 then
      s := 2^((n-3)/2); Append(rel,[t^s,u^s]);
    else
      s := 2^((n-4)/2); Append(rel,[t^s*u^s,t^(-s)*u^s]);
    fi;
  od;
  if d>=4 then
    for i in [1..d-3] do
      Add(rel,Comm((r[i]*r[i+1])^2,(r[i+2]*r[i+3])^2));
    od;
  fi;
  q := f/rel;
  iso := IsomorphismPermGroup(q);
  g := Image(iso); rs := List(GeneratorsOfGroup(q),x->Image(iso,x));
  expected := 2^(Sum(ns)-3*(d-3));
  if Size(g)<>expected then Error("wrong presentation order"); fi;
  subsets := Combinations([1..d]); pars := [];
  for sub in subsets do
    gens := rs{sub};
    if IsEmpty(gens) then h := TrivialSubgroup(g); else h:=Group(gens); fi;
    Add(pars,h);
    imgs := List([1..d],function(j) if j in sub then return rs[j]; else return One(g); fi; end);
    hom := GroupHomomorphismByImages(g,g,rs,imgs);
    if hom=fail or Image(hom)<>h then Error("invalid deletion map"); fi;
  od;
  for i in [1..Length(subsets)] do
    for j in [1..Length(subsets)] do
      common := Intersection(subsets[i],subsets[j]);
      if Intersection(pars[i],pars[j])<>pars[Position(subsets,common)] then
        Error("intersection property fails");
      fi;
    od;
  od;
  kernels := [];
  for i in [1..d-2] do
    h := Group(rs{[i..i+2]});
    if Size(h)<>2^ns[i] then Error("wrong local triple"); fi;
    k := CommutatorSubgroup(DerivedSubgroup(h),h);
    if Size(k)<>2^(ns[i]-5) then Error("wrong local kernel"); fi;
    Add(kernels,k);
  od;
  kgens := Concatenation(List(kernels,GeneratorsOfGroup));
  if IsEmpty(kgens) then k := TrivialSubgroup(g); else k := Group(kgens); fi;
  if k<>CommutatorSubgroup(DerivedSubgroup(g),g)
    or Size(k)<>Product(List(kernels,Size)) then Error("kernel product fails"); fi;
  Print("PASS parameters=",ns," rank=",d," order=",Size(g),
        " kernel=",Size(k)," maps=",Length(subsets),
        " meets=",Length(subsets)^2,"\n");
od;
Print("PASS all presentation, local-group, Boolean-map, IP and kernel checks\n");
QUIT;
