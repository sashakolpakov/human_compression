# Literal finite certificate for the coprime-label counterexample.
# GAP subgroup arithmetic is the retained computational kernel.
Need := function(ok, msg)
  if not ok then Error(msg); fi;
end;
CheckIP := function(marks)
  local subs, mask, i, j, common, mask2;
  subs := [];
  for mask in [0..15] do
    Add(subs, Group(Filtered(marks, x -> QuoInt(mask,2^(Position(marks,x)-1)) mod 2 = 1), ()));
  od;
  for mask in [0..15] do
    for mask2 in [0..15] do
      common := Sum(Filtered([0..3], i -> QuoInt(mask,2^i) mod 2=1 and QuoInt(mask2,2^i) mod 2=1), i -> 2^i);
      Need(Intersection(subs[mask+1],subs[mask2+1])=subs[common+1], "input intersection property");
    od;
  od;
  return subs;
end;
a := [(1,2)(3,5)(4,7)(6,8), (1,3)(2,4)(5,7)(6,9),
      (3,6)(4,7)(5,8)(9,10), (1,3)(2,5)(4,7)(10,11)];;
b := [(12,13),(13,14),(14,15),(15,16)];;
for marks in [a,b] do
  Need(ForAll(marks, x -> Order(x)=2), "nonidentity involutions");
  for i in [1..4] do
    for j in [i+2..4] do
      if j<=4 then Need(marks[i]*marks[j]=marks[j]*marks[i], "string commutation"); fi;
    od;
  od;
od;
G := Group(a);; S := Group(b);;
Need(Size(G)=660 and IsSimpleGroup(G), "literal simple 660-group");
Need(Size(S)=120, "literal simplex S5");
Need(List([1..3], i -> Order(a[i]*a[i+1]))=[3,5,3], "first type");
Need(List([1..3], i -> Order(b[i]*b[i+1]))=[3,3,3], "second type");
sa:=CheckIP(a);;sb:=CheckIP(b);;
Need(Size(sa[8])=60 and Size(sa[15])=60 and IsSimpleGroup(sa[8]) and IsSimpleGroup(sa[15]), "first A5 ends");
Need(Size(sb[8])=24 and Size(sb[15])=24, "second S4 ends");
Need(ForAll(b,x->SignPerm(x)=-1), "second orientation character");
m:=List([1..4],i->a[i]*b[i]);;
M:=Group(m);;A:=Group(m{[1..3]});;B:=Group(m{[2..4]});;C:=Group(m{[2,3]});;
Need([Size(M),Size(A),Size(B),Size(C),Size(Intersection(A,B))]=[79200,1440,1440,30,60], "exact mixed orders");
Need(a[2] in A and a[2] in B and not(a[2] in C), "literal mixed intersection witness");
Print("COPRIME_CERTIFICATE_PASS\n");
Print("input_IP_checks=512; input_orders=660,120; types=3,5,3/3,3,3\n");
Print("mixed_orders=79200,1440,1440,30,60; witness=a1; second_orientable=true\n");
QUIT_GAP(0);
