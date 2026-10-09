LogTo("research/leemans/phase3_order_bound_check.log");;

HasTPP:=function(A,B,C)
  local product;
  if Size(Intersection(A,B))<>1 then return false; fi;
  product:=Set(Concatenation(List(Elements(A),a->List(Elements(B),b->a*b))));
  return Intersection(product,Set(Elements(C)))=[One(A)];
end;

RunOrderBoundChecks:=function()
  local G,subs,V,i,j,k,found,A,B,C,cyclic,tests,t,a,b,c,gs,p0,p1,p2,
        lhs,rhs,P,orders;
  G:=SymmetricGroup(3);
  subs:=List([(1,2),(1,3),(2,3)],x->Group(x));
  if not HasTPP(subs[1],subs[2],subs[3]) then Error("S3 TPP"); fi;
  Print("S3 cyclic TPP: product=8 group_order=6; unrestricted cyclic claim FALSE\n");

  G:=SmallGroup(32,49);
  if NilpotencyClassOfGroup(G)<>2 then Error("Wrong extraspecial example"); fi;
  subs:=AllSubgroups(G);
  V:=Filtered(subs,H->Size(H)=4 and IsElementaryAbelian(H));
  found:=false;
  for i in [1..Length(V)] do
    for j in [i+1..Length(V)] do
      for k in [j+1..Length(V)] do
        if HasTPP(V[i],V[j],V[k]) then
          found:=true;
          Print("EXTRASPECIAL32 noncyclic TPP: product=64 group_order=32 class=2\n");
          Print("Subgroup generators: ",List([V[i],V[j],V[k]],GeneratorsOfGroup),"\n");
          break;
        fi;
      od;
      if found then break; fi;
    od;
    if found then break; fi;
  od;
  if not found then Error("Missing noncyclic TPP example"); fi;
  cyclic:=Filtered(subs,IsCyclic);tests:=0;
  for i in [1..Length(cyclic)] do
    for j in [i..Length(cyclic)] do
      for k in [j..Length(cyclic)] do
        A:=cyclic[i];B:=cyclic[j];C:=cyclic[k];
        if Size(A)*Size(B)*Size(C)>Size(G) then
          tests:=tests+1;
          if HasTPP(A,B,C) then Error("Cyclic class2 theorem violated"); fi;
        fi;
      od;
    od;
  od;
  Print("EXTRASPECIAL32 cyclic triples exceeding group size rejected: ",tests,"\n");

  # Generalized dihedral C4^2: IP holds but Helly does not.
  a:=PermList(Concatenation(List([0..3],i->List([0..3],j->4*((-i) mod 4)+((-j) mod 4)+1))));
  b:=PermList(Concatenation(List([0..3],i->List([0..3],j->4*((1-i) mod 4)+((-j) mod 4)+1))));
  c:=PermList(Concatenation(List([0..3],i->List([0..3],j->4*((-i) mod 4)+((1-j) mod 4)+1))));
  G:=Group(a,b,c);p0:=Group(b,c);p1:=Group(a,c);p2:=Group(a,b);
  if Size(G)<>32 then Error("Generalized dihedral order"); fi;
  if Intersection(p0,p1)<>Group(c) or Intersection(p0,p2)<>Group(b)
     or Intersection(p1,p2)<>Group(a) then Error("IP expected"); fi;
  orders:=[Order(a*b),Order(b*c),Order(a*c)];
  if orders<>[4,4,4] then Error("Pair types"); fi;
  lhs:=Set(Concatenation(List(Elements(Intersection(p0,p1)),
       x->List(Elements(Intersection(p0,p2)),y->x*y))));
  rhs:=Filtered(Elements(p0),x->ForAny(Elements(p1),y->y^-1*x in p2));
  if lhs=Set(rhs) then Error("Helly must fail"); fi;
  P:=DerivedSubgroup(G);
  A:=Group((a*b)^2);B:=Group((b*c)^2);C:=Group((a*c)^2);
  if P<>FrattiniSubgroup(G) or Size(P)<>4 or HasTPP(A,B,C) then
    Error("Derived TPP obstruction");
  fi;
  Print("DIH(C4^2): order32 type4,4,4 IP=true Helly=false; Tits sizes ",
        Length(lhs)," and ",Length(rhs),"; square-rotation TPP=false\n");
  Print("ALL ASSUMPTION/OBSTRUCTION CHECKS PASS\n");
end;

RunOrderBoundChecks();
LogTo();
QUIT;
